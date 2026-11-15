import sys,json,urllib.request,urllib.parse
import numpy as np
from osgeo import gdal
from scipy import ndimage
D,W=sys.argv[1:3]
gdal.UseExceptions()
zh=gdal.Open(f"{W}/zh20.tif"); gt=zh.GetGeoTransform(); A=zh.ReadAsArray()
I=gdal.Open(f"{W}/idf20.tif").ReadAsArray().astype(bool)
mA=(A==1)&I&gdal.Open(f"{W}/union20.tif").ReadAsArray().astype(bool)
# merge nearby patches: dilate 200 m, label, then measure true class-A area per label
lab,n=ndimage.label(ndimage.binary_dilation(mA,iterations=10))
areas=ndimage.sum(mA,lab,index=np.arange(1,n+1))*400/1e6
order=np.argsort(-areas)[:12]
from pyproj import Transformer
from shapely.geometry import shape, Point
inv=Transformer.from_crs(2154,4326,always_xy=True)
sites=[]
for fn,kind in [("c_znieff1","ZNIEFF 1"),("c_sic","Natura 2000"),("c_zps","Natura 2000")]:
    for f in json.load(open(f"{D}/{fn}.geojson"))["features"]: sites.append((kind,f["properties"]["nom_site"],shape(f["geometry"])))
out=[]
for i in order:
    L=i+1; ys,xs=np.nonzero((lab==L)&mA)
    my,mx=ys.mean(),xs.mean(); j0=int(np.argmin((ys-my)**2+(xs-mx)**2)); cy,cx=ys[j0]+0.5,xs[j0]+0.5; X=gt[0]+cx*gt[1]; Y=gt[3]+cy*gt[5]; lon,lat=inv.transform(X,Y)
    # sample points of the patch to find intersecting sites
    idx=np.random.default_rng(0).choice(len(xs),min(300,len(xs)),replace=False)
    cnt={}
    for j in idx:
        lo,la=inv.transform(gt[0]+xs[j]*gt[1],gt[3]+ys[j]*gt[5]); p=Point(lo,la)
        for kind,name,g in sites:
            if g.contains(p): cnt[(kind,name)]=cnt.get((kind,name),0)+1
    best=sorted(cnt.items(),key=lambda x:(-x[1], x[0][0]!="ZNIEFF 1"))[:2]
    com=json.load(urllib.request.urlopen(urllib.request.Request("https://geo.api.gouv.fr/communes?"+urllib.parse.urlencode({"lat":lat,"lon":lon,"fields":"nom,codeDepartement"}),headers={"User-Agent":"wetland-study-map/1.0"}),timeout=30))
    out.append({"rank":len(out)+1,"A_km2":round(float(areas[i]),1),"lon":round(lon,4),"lat":round(lat,4),"x":X,"y":Y,"commune":(com[0]["nom"]+" ("+com[0]["codeDepartement"]+")") if com else None,"sites":[{"type":k,"name":nm,"share":round(c/len(idx)*100)} for (k,nm),c in best]})
for o in out: print(o["rank"],o["A_km2"],o["commune"],[ (s["type"],s["name"],s["share"]) for s in o["sites"]])
json.dump(out,open(f"{W}/classA_top.json","w"),indent=1,ensure_ascii=False)
