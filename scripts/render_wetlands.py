import sys,json
import numpy as np
from osgeo import gdal, ogr
gdal.UseExceptions(); ogr.UseExceptions()
D,O,W,RM=sys.argv[1:5]
exec(open(RM).read().split("# ---------- stats")[0])   # helpers: T, U, DEP, groups, draw_rivers, edge, towns, scalebar, credit, LEGKW, BG, INK
zh=gdal.Open(f"{W}/zh10.tif"); gt=zh.GetGeoTransform(); A=zh.ReadAsArray()
M=gdal.Open(f"{W}/dep10.tif").ReadAsArray().astype(bool)
# catchment id raster
drv=gdal.GetDriverByName("MEM"); C=drv.Create("",zh.RasterXSize,zh.RasterYSize,1,gdal.GDT_Byte); C.SetGeoTransform(gt); C.SetProjection(zh.GetProjection())
cds=ogr.Open(f"{W}/catch_l93.gpkg"); cl=cds.GetLayer(); names={}
for i,f in enumerate(cl,1): names[i]=f.GetField("catchment")
cl.ResetReading()
# burn ids via attribute: add temp field-less approach: rasterize one at a time
for i in names:
    cl.SetAttributeFilter(f"catchment = '{names[i].replace(chr(39),chr(39)*2)}'")
    gdal.RasterizeLayer(C,[1],cl,burn_values=[i])
cl.SetAttributeFilter(None)
CID=C.ReadAsArray()
cell=100/1e6  # km2 per 10 m cell
tot={k:round(float(((A==v)&M).sum())*cell,1) for k,v in [("A",1),("B",2),("D",4)]}
dep_km2=round(float(M.sum())*cell)
per=[]
for i,n in names.items():
    m=(CID==i)&M; a=float(m.sum())*cell
    if a<20: continue
    per.append({"catchment":n,"km2_in77":round(a),"A_km2":round(float(((A==1)&m).sum())*cell,1),"B_km2":round(float(((A==2)&m).sum())*cell,1),"AB_pct":round(float(((A==1)|(A==2))[m].sum())/m.sum()*100,1)})
per.sort(key=lambda r:-r["AB_pct"])
res={"dep_km2":dep_km2,"classes_km2":tot,"AB_pct_dep":round((tot["A"]+tot["B"])/dep_km2*100,1),"A_pct_dep":round(tot["A"]/dep_km2*100,1),"catchments":per}
json.dump(res,open(f"{O}/wetlands_stats.json","w"),indent=1,ensure_ascii=False); print(json.dumps(res,ensure_ascii=False)[:900])
# downsample 4x4 (40 m) with priority A>B>D, only inside dept
k=4; h=(A.shape[0]//k)*k; w=(A.shape[1]//k)*k
a=np.where(M,A,0)[:h,:w].reshape(h//k,k,w//k,k)
prio=np.zeros((h//k,w//k),np.uint8)
for v in (4,2,1): prio[(a==v).any(axis=(1,3))]=v
from matplotlib.colors import ListedColormap
rgba=np.zeros(prio.shape+(4,))
for v,c in {1:"#0B5A6B",2:"#4FB3A9",4:"#2F7FD0"}.items():
    rgb=matplotlib.colors.to_rgba(c); rgba[prio==v]=rgb
ext=(gt[0],gt[0]+w*gt[1],gt[3]+h*gt[5],gt[3])
fig,ax=plt.subplots(figsize=(8,11.2),facecolor=BG)
b=DEP.bounds; ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(b[0]-2500,b[2]+2500); ax.set_ylim(b[1]-2500,b[3]+2500)
ax.add_patch(PathPatch(path_of(DEP),fc="#F4F2EA",ec="none",zorder=0))
ax.imshow(rgba,extent=ext,interpolation="nearest",zorder=2)
for _,g in groups: 
    gi=g.intersection(DEP)
    if not gi.is_empty: edge(ax,gi,"#9AA59E",0.6,z=5)
edge(ax,DEP,INK,1.4,z=6)
towns(ax,["Meaux","Melun","Fontainebleau","Provins","Nemours","Coulommiers","Montereau","Episy"])
scalebar(ax)
f=lambda x:format(x,",.0f").replace(","," ")
ax.legend(handles=[Patch(fc="#0B5A6B",label=f"Classe A, zones humides avérées ({f(tot['A'])} km²)"),Patch(fc="#4FB3A9",label=f"Classe B, zones humides probables ({f(tot['B'])} km²)"),Patch(fc="#2F7FD0",label=f"Classe D, plans d'eau et cours d'eau ({f(tot['D'])} km²)"),Line2D([],[],color="#9AA59E",lw=1,label="Limites des bassins versants"),Line2D([],[],color=INK,lw=1.4,label="Seine-et-Marne")],**LEGKW)
ax.set_title("Les zones humides\nde la Seine-et-Marne",loc="left",fontsize=18,fontweight="bold")
credit(fig,f"Zones humides avérées et probables : {res['AB_pct_dep']} % du département ({f(tot['A']+tot['B'])} km² sur {f(dep_km2)}). Données : DRIEAT Île-de-France, Enveloppes d'alerte des zones humides (mise à jour 2021, Licence Ouverte 2.0), rastérisées à 10 m ; classe C (faible probabilité) non représentée. IGN BD CARTO. Lambert-93. L. Angulo López, nov. 2026.")
fig.savefig(f"{O}/05-zones-humides.png",dpi=150,bbox_inches="tight",facecolor=BG); plt.close(fig); print("map done")
