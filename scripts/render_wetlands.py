import sys,json
import numpy as np
from osgeo import gdal, ogr
gdal.UseExceptions(); ogr.UseExceptions()
D,O,W,RM=sys.argv[1:5]
exec(open(RM).read().split("# ---------- stats")[0])
IDF=proj(json.load(open(f"{D}/idf.geojson"))["features"][0]["geometry"])
NODATA=U.difference(IDF)
zh=gdal.Open(f"{W}/zh20.tif"); gt=zh.GetGeoTransform(); A=zh.ReadAsArray()
I=gdal.Open(f"{W}/idf20.tif").ReadAsArray().astype(bool)
mem=gdal.GetDriverByName("MEM")
def burn(geom):
    ds=mem.Create("",zh.RasterXSize,zh.RasterYSize,1,gdal.GDT_Byte); ds.SetGeoTransform(gt); ds.SetProjection(zh.GetProjection())
    src=ogr.GetDriverByName("Memory").CreateDataSource(""); lyr=src.CreateLayer("g",zh.GetSpatialRef() if hasattr(zh,'GetSpatialRef') else None)
    f=ogr.Feature(lyr.GetLayerDefn()); f.SetGeometry(ogr.CreateGeometryFromWkb(geom.wkb)); lyr.CreateFeature(f)
    gdal.RasterizeLayer(ds,[1],lyr,burn_values=[1]); return ds.ReadAsArray().astype(bool)
cell=400/1e6
CATCH=burn(U)
rows=[]
for n,g in groups:
    m=burn(g); tot=m.sum()*cell; cov=(m&I); covk=cov.sum()*cell
    if covk<5: rows.append({"catchment":n,"km2":round(tot),"covered_pct":round(covk/tot*100) if tot else 0,"A_km2":None,"B_km2":None,"AB_pct":None}); continue
    a=((A==1)&cov).sum()*cell; b=((A==2)&cov).sum()*cell
    rows.append({"catchment":n,"km2":round(tot),"covered_pct":round(covk/tot*100),"A_km2":round(a,1),"B_km2":round(b,1),"AB_pct":round((a+b)/covk*100,1)})
covall=(CATCH&I); tA=((A==1)&covall).sum()*cell; tB=((A==2)&covall).sum()*cell; tD=((A==4)&covall).sum()*cell
res={"catch_km2":round(CATCH.sum()*cell),"covered_km2":round(covall.sum()*cell),"A_km2":round(tA,1),"B_km2":round(tB,1),"D_km2":round(tD,1),"AB_pct_covered":round((tA+tB)/(covall.sum()*cell)*100,1),"catchments":sorted(rows,key=lambda r:-(r["AB_pct"] or -1))}
json.dump(res,open(f"{O}/wetlands_catchments.json","w"),indent=1,ensure_ascii=False)
print(json.dumps({k:v for k,v in res.items() if k!="catchments"},ensure_ascii=False))
for r in res["catchments"]: print(r)
# image: downsample 2x2 (40 m), priority A > B > D, only inside catchments ∩ IDF
k=2; h=(A.shape[0]//k)*k; w=(A.shape[1]//k)*k
a=np.where(covall,A,0)[:h,:w].reshape(h//k,k,w//k,k)
prio=np.zeros((h//k,w//k),np.uint8)
for v in (4,2,1): prio[(a==v).any(axis=(1,3))]=v
COL={1:"#6A2C91",2:"#F2A93B",4:"#1F78B4"}
rgba=np.zeros(prio.shape+(4,))
for v,c in COL.items(): rgba[prio==v]=matplotlib.colors.to_rgba(c)
ext=(gt[0],gt[0]+w*gt[1],gt[3]+h*gt[5],gt[3])
fig,ax=plt.subplots(figsize=(8,11.5),facecolor=BG); base(ax)
ax.add_patch(PathPatch(path_of(U),fc="#F1EFE8",ec="none",zorder=0))
if not NODATA.is_empty:
    ax.add_patch(PathPatch(path_of(NODATA),fc="#E9E7E1",ec="#B9B4A9",lw=0,hatch="////",zorder=1))
ax.imshow(rgba,extent=ext,interpolation="nearest",zorder=3)
for n,g in groups: edge(ax,g,"#2B2B2B",0.9,z=6)
edge(ax,U,INK,1.5,z=7); edge(ax,DEP,"#C0392B",1.6,(0,(4,2)),z=8)
for n,g in groups:
    rp=g.representative_point()
    if g.area>8e7: ax.text(rp.x,rp.y,n,ha="center",va="center",fontsize=9.5,fontweight="bold",color=INK,zorder=9,bbox=dict(boxstyle="round,pad=0.2",fc="#FFFFFFCC",ec="none"))
scalebar(ax)
f=lambda x:format(x,",.0f").replace(","," ")
ax.legend(handles=[Patch(fc=COL[1],label=f"Classe A, zones humides avérées ({f(tA)} km²)"),Patch(fc=COL[2],label=f"Classe B, zones humides probables ({f(tB)} km²)"),Patch(fc=COL[4],label=f"Classe D, plans d'eau et cours d'eau ({f(tD)} km²)"),Patch(fc="#E9E7E1",ec="#B9B4A9",hatch="////",label="Hors Île-de-France : pas de données"),Line2D([],[],color="#2B2B2B",lw=1,label="Bassins versants (BD CARTO)"),Line2D([],[],color="#C0392B",lw=1.6,ls=(0,(4,2)),label="Limite de la Seine-et-Marne")],**LEGKW)
ax.set_title("Les zones humides\ndes bassins versants de la Seine-et-Marne",loc="left",fontsize=18,fontweight="bold")
credit(fig,f"Partie francilienne des bassins ({f(covall.sum()*cell)} km² sur {f(CATCH.sum()*cell)}) : zones humides avérées et probables sur {res['AB_pct_covered']} %. Données : DRIEAT Île-de-France, Enveloppes d'alerte des zones humides (mise à jour 2021, Licence Ouverte 2.0), rastérisées à 20 m ; classe C non représentée. IGN BD CARTO, Admin Express. Lambert-93. L. Angulo López, nov. 2026.")
fig.savefig(f"{O}/05-zones-humides.png",dpi=150,bbox_inches="tight",facecolor=BG); plt.close(fig); print("map done")
