import json, sys, collections
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch, Patch
from matplotlib.lines import Line2D
from pyproj import Transformer
from shapely.geometry import shape, mapping
from shapely.ops import transform as stx, unary_union
from shapely.prepared import prep
D,O=sys.argv[1],sys.argv[2]
T=Transformer.from_crs(4326,2154,always_xy=True).transform
def L(n): return json.load(open(f"{D}/{n}.geojson"))["features"]
def proj(g): return stx(T, shape(g))
U=proj(L("catch_union")[0]["geometry"]); PU=prep(U)
DEP=proj(L("dep77")[0]["geometry"])
groups=[(f["properties"]["catchment"],proj(f["geometry"])) for f in L("catch_groups")]
def clipfeats(feats, key=None):
    out=[]
    for f in feats:
        g=proj(f["geometry"])
        if not PU.intersects(g): continue
        gi=g.intersection(U)
        if gi.is_empty: continue
        out.append((f["properties"],gi))
    return out
def path_of(g):
    v=[];c=[]
    polys=[g] if g.geom_type=="Polygon" else [p for p in getattr(g,"geoms",[]) if p.geom_type=="Polygon"]
    for p in polys:
        for r in [p.exterior,*p.interiors]:
            cs=list(r.coords); v+=cs; c+=[Path.MOVETO]+[Path.LINETO]*(len(cs)-2)+[Path.CLOSEPOLY]
    return Path(v,c) if v else None
def lines_of(g):
    if g.geom_type=="LineString": return [g]
    return [x for x in getattr(g,"geoms",[]) if x.geom_type=="LineString"]
INK="#1C2822"; BG="#FAFBF7"; MUTED="#5B6A61"
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11,"text.color":INK})
LEGKW=dict(loc="upper left",bbox_to_anchor=(0.0,0.0),frameon=False,fontsize=10.5,ncol=2,title_fontsize=11.5,columnspacing=1.2,handlelength=1.6)
def base(ax,bounds=None,pad=3000):
    ax.set_aspect("equal"); ax.axis("off")
    b=bounds or U.bounds
    ax.set_xlim(b[0]-pad,b[2]+pad); ax.set_ylim(b[1]-pad,b[3]+pad)
def fill(ax,items,colfn,z=1,alpha=1,ec="none",lw=0):
    for p,g in items:
        c=colfn(p)
        if c is None: continue
        pa=path_of(g)
        if pa: ax.add_patch(PathPatch(pa,fc=c,ec=ec,lw=lw,alpha=alpha,zorder=z))
def edge(ax,g,color=INK,lw=1,ls="-",z=20):
    pa=path_of(g); ax.add_patch(PathPatch(pa,fc="none",ec=color,lw=lw,ls=ls,zorder=z))
def frame(ax):
    for _,g in groups: edge(ax,g,"#FFFFFF",0.9,z=18)
    edge(ax,U,INK,1.3,z=21); edge(ax,DEP,"#B03A2E",1.4,(0,(4,2)),z=22)
TOWNS={"Meaux":(2.878,48.960),"Melun":(2.656,48.540),"Fontainebleau":(2.700,48.405),"Provins":(3.299,48.560),"Nemours":(2.698,48.268),"Montereau":(2.958,48.385),"Coulommiers":(3.084,48.813),"Moret":(2.815,48.372),"Episy":(2.780,48.330),"Montargis":(2.733,47.997),"Château-Thierry":(3.403,49.046),"Nogent-sur-Seine":(3.503,48.494),"Corbeil":(2.483,48.613)}
def towns(ax,names=None,bounds=None):
    for n,(lo,la) in TOWNS.items():
        if names and n not in names: continue
        x,y=T(lo,la)
        if not U.buffer(2000).contains(shape({"type":"Point","coordinates":[x,y]})) and not bounds: continue
        if bounds and not(bounds[0]<x<bounds[2] and bounds[1]<y<bounds[3]): continue
        ax.plot(x,y,"o",ms=3,color=INK,zorder=30)
        ax.annotate(n,(x,y),xytext=(4,3),textcoords="offset points",fontsize=9.5,zorder=31,bbox=dict(boxstyle="round,pad=0.15",fc=BG,ec="none",alpha=.8))
def scalebar(ax,km=10):
    x0,x1=ax.get_xlim(); y0,y1=ax.get_ylim(); x=x0+(x1-x0)*.04; y=y0+(y1-y0)*.035
    ax.plot([x,x+km*1000],[y,y],color=INK,lw=2.5,zorder=40); ax.text(x+km*500,y+(y1-y0)*.012,f"{km} km",ha="center",fontsize=8)
import textwrap
def credit(fig,t): fig.text(0.01,-0.005,textwrap.fill(t,105),fontsize=8,color=MUTED,ha="left",va="top")
DEPLEG=Line2D([],[],color="#B03A2E",lw=1.4,ls=(0,(4,2)),label="Limite de la Seine-et-Marne")
CATLEG=Line2D([],[],color=INK,lw=1.3,label="Bassins versants (BD CARTO)")

rivers=[]
for f in L("c_rivers"):
    g=proj(f["geometry"])
    if PU.intersects(g): rivers.append((f["properties"]["classe_de_largeur"],g.intersection(U)))
RW={"Entre 5 et 15 m":.5,"Entre 15 et 50 m":1.0,"Plus de 50 m":1.8}
def draw_rivers(ax,color="#2C6FB0",scale=1,z=12):
    for cl,g in rivers:
        for ln in lines_of(g):
            xs,ys=ln.xy; ax.plot(xs,ys,color=color,lw=RW[cl]*scale,zorder=z,solid_capstyle="round")

# ---------- stats
soils=clipfeats(L("c_sols")); clc=clipfeats(L("c_clc18"))
n2k=clipfeats(L("c_sic"))+clipfeats(L("c_zps")); zn=clipfeats(L("c_znieff1"))
WET={"FLUVIOSOL","REDUCTISOL","REDOXISOL","LUVISOL-REDOXISOL","BRUNISOL-REDOXISOL","PLANOSOL","LUVISOL-REDOXISOL"}
def lc(code):
    if code[0]=="1": return "Artificialisé"
    if code in("211","212","213"): return "Terres arables"
    if code=="231": return "Prairies"
    if code[0]=="2": return "Autres agricoles"
    if code[:2]=="31": return "Forêts"
    if code[0]=="3": return "Landes, milieux ouverts"
    return "Eaux et zones humides"
stats=[]
N2U=unary_union([g for _,g in n2k])
for name,gg in sorted(groups,key=lambda x:-x[1].area):
    a=gg.area; pg=prep(gg)
    def share(items,pred):
        s=0
        for p,g in items:
            if pred(p) and pg.intersects(g): s+=g.intersection(gg).area
        return s/a
    lcs=collections.Counter()
    for p,g in clc:
        if pg.intersects(g): lcs[lc(p["code_18"])]+=g.intersection(gg).area
    stats.append({"catchment":name,"km2":round(a/1e6),"in77":round(gg.intersection(DEP).area/a*100),
        "hydro":round(share(soils,lambda p:p["nom_sol_dominant"] in WET)*100),
        "forest":round(lcs["Forêts"]/a*100),"arable":round(lcs["Terres arables"]/a*100),"artif":round(lcs["Artificialisé"]/a*100),
        "grass":round(lcs["Prairies"]/a*100),"water":round(lcs["Eaux et zones humides"]/a*100),
        "n2k":round(N2U.intersection(gg).area/a*100)})
tot={"km2":round(U.area/1e6),"in77":round(DEP.intersection(U).area/U.area*100),"dep_km2":round(DEP.area/1e6)}
lct=collections.Counter()
for p,g in clc: lct[lc(p["code_18"])]+=g.area
tot["lc"]={k:round(v/U.area*100,1) for k,v in lct.most_common()}
tot["hydro"]=round(sum(g.area for p,g in soils if p["nom_sol_dominant"] in WET)/U.area*100,1)
tot["n2k"]=round(N2U.area/U.area*100,1)
json.dump({"total":tot,"catchments":stats},open(f"{O}/stats.json","w"),indent=1,ensure_ascii=False)
print(json.dumps(tot,ensure_ascii=False))

# ---------- 00 catchments
PAL=["#C7DDE8","#E5D7B5","#D3E4C7","#EBC9B7","#CFC9E3","#F0E2A8","#BFDCD2","#E3CAD8","#D9D2C3","#C9D9EE","#E9DCC9","#CDE3DD","#E2D0B0","#D6DDE5"]
fig,ax=plt.subplots(figsize=(8,11.5),facecolor=BG); base(ax)
order=sorted(groups,key=lambda x:-x[1].area)
for i,(n,g) in enumerate(order):
    pa=path_of(g); ax.add_patch(PathPatch(pa,fc=PAL[i%len(PAL)],ec="none",zorder=1))
draw_rivers(ax)
frame(ax)
for n,g in order:
    rp=g.representative_point()
    if g.area>8e7: ax.text(rp.x,rp.y,n,ha="center",va="center",fontsize=10,fontweight="bold",color="#33433A",zorder=35,bbox=dict(boxstyle="round,pad=0.2",fc="#FFFFFFAA",ec="none"))
towns(ax,["Meaux","Melun","Fontainebleau","Provins","Nemours","Montereau","Coulommiers","Château-Thierry","Montargis"])
scalebar(ax)
ax.legend(handles=[CATLEG,DEPLEG,Line2D([],[],color="#2C6FB0",lw=1.4,label="Cours d'eau permanents > 5 m")],**LEGKW)
ax.set_title("Les bassins versants\nqui drainent la Seine-et-Marne",loc="left",fontsize=17,fontweight="bold")
credit(fig,"81 zones hydrographiques BD CARTO touchant le département, regroupées en 14 bassins ; "+format(tot['km2'],",").replace(","," ")+f" km², dont {tot['in77']} % en Seine-et-Marne. Données : IGN BD CARTO V5 (Géoplateforme), Admin Express. Lambert-93. L. Angulo López, nov. 2026.")
fig.savefig(f"{O}/00-bassins.png",dpi=150,bbox_inches="tight",facecolor=BG); plt.close(fig)

# ---------- 01 soils
SOILC={"FLUVIOSOL":"#3E7CB1","REDUCTISOL":"#1B3F6B","REDOXISOL":"#5FA8A0","LUVISOL-REDOXISOL":"#8CC5B8","BRUNISOL-REDOXISOL":"#A9D3C6","PLANOSOL":"#7FB3D5",
 "LUVISOL":"#E7D9B0","NEOLUVISOL":"#EFE3C2","CALCOSOL":"#D8C27A","CALCISOL":"#C9AE5D","RENDOSOL":"#B8954A","BRUNISOL":"#CDB59A","PODZOSOL":"#9C8BB0",
 "ARENOSOL":"#F1E6A6","LITHOSOL":"#A39E93","FERSIALSOL":"#C98B6B","COLLUVIOSOL":"#D9C7A8","REGOSOL":"#C2BCAF","ALOCRISOL":"#BBA58C","PEYROSOL":"#AFA89A"}
sa=collections.Counter()
for p,g in soils: sa[p["nom_sol_dominant"]]+=g.area
fig,ax=plt.subplots(figsize=(8,11.5),facecolor=BG); base(ax)
fill(ax,soils,lambda p:SOILC.get(p["nom_sol_dominant"],"#ccc"))
frame(ax); towns(ax,["Meaux","Melun","Fontainebleau","Provins","Nemours","Montereau","Coulommiers"]); scalebar(ax)
keys=[k for k,_ in sa.most_common() if sa[k]/U.area>0.002]
hand=[Patch(fc=SOILC.get(k,"#ccc"),label=k.capitalize()+" "+(f"{sa[k]/U.area*100:.0f} %" if sa[k]/U.area>=0.005 else "< 1 %")+(" (hydromorphe)" if k in WET else "")) for k in sorted(keys,key=lambda k:(k not in WET,-sa[k]))]
ax.legend(handles=hand+[Patch(fc="#FFFFFF",ec="#CDD5CB",label="Non cartographié (zones urbaines denses)"),CATLEG,DEPLEG],title="Sol dominant, part de la surface",**LEGKW)
ax.set_title("Sols dominants\ndes bassins versants de la Seine-et-Marne",loc="left",fontsize=17,fontweight="bold")
credit(fig,f"Sols hydromorphes dominants sur {tot['hydro']} % de la surface. Données : INRAE, Les sols dominants de France métropolitaine, carte harmonisée (Géoplateforme, WFS INRAE_CARTE-SOLS) ; IGN BD CARTO. Lambert-93. L. Angulo López, nov. 2026.")
fig.savefig(f"{O}/01-sols.png",dpi=150,bbox_inches="tight",facecolor=BG); plt.close(fig)

# ---------- 02 vegetation
def clcc(p):
    c=p["code_18"]
    if c[0]=="1": return "#B9B4B0"
    if c in("211","212","213"): return "#F3EBC3"
    if c in("221","222"): return "#E3C27E"
    if c=="231": return "#C8DF8F"
    if c[:2]=="24": return "#E8D29A"
    if c=="311": return "#5E9A55"
    if c=="312": return "#2F5E3A"
    if c=="313": return "#4A7E4A"
    if c[:2]=="32": return "#A7B86A"
    if c[:2]=="33": return "#E6DCC8"
    if c[0]=="4": return "#9A6FB0"
    return "#4F8FCB"
fig,ax=plt.subplots(figsize=(8,11.5),facecolor=BG); base(ax)
fill(ax,clc,clcc)
for p,g in n2k: edge(ax,g,"#B03A2E",0.9,z=15)
frame(ax); towns(ax,["Meaux","Melun","Fontainebleau","Provins","Nemours","Montereau","Coulommiers"]); scalebar(ax)
LEG=[("#B9B4B0","Artificialisé (1xx)"),("#F3EBC3","Terres arables (21x)"),("#E8D29A","Zones agricoles hétérogènes (24x)"),("#E3C27E","Vignes, vergers (22x)"),("#C8DF8F","Prairies (231)"),("#5E9A55","Forêts de feuillus (311)"),("#4A7E4A","Forêts mélangées (313)"),("#2F5E3A","Forêts de conifères (312)"),("#A7B86A","Landes, broussailles (32x)"),("#E6DCC8","Sables, rochers, espaces ouverts (33x)"),("#9A6FB0","Zones humides (4xx)"),("#4F8FCB","Eaux (5xx)")]
lcl=tot["lc"]
ax.legend(handles=[Patch(fc=c,label=l) for c,l in LEG]+[Line2D([],[],color="#B03A2E",lw=1,label="Natura 2000 (ZSC/SIC et ZPS)"),CATLEG,DEPLEG],title="CORINE Land Cover 2018",**LEGKW)
ax.set_title("Végétation et occupation du sol\ndes bassins versants de la Seine-et-Marne",loc="left",fontsize=17,fontweight="bold")
credit(fig,"Surface : "+", ".join(f"{k.lower()} {v} %" for k,v in lcl.items())+f" ; Natura 2000 {tot['n2k']} %. Données : CORINE Land Cover 2018 (UE Copernicus, SDES) ; PatriNat/INPN ; IGN. Lambert-93. L. Angulo López, nov. 2026.")
fig.savefig(f"{O}/02-vegetation.png",dpi=150,bbox_inches="tight",facecolor=BG); plt.close(fig)

# ---------- 03 GBIF
gb=L("gbif_catch")
water=[(p,g) for p,g in clc if p["code_18"][0] in "45"]
grp={"plante":("Plantes indicatrices (24 espèces), depuis 2000","#2E6650"),"oiseau":("Oiseaux d'eau hivernants (14), précision ≤ 1 km, depuis 2000","#2C5D8A"),"invasive":("Espèces exotiques envahissantes (9), depuis 2000","#B03A2E")}
fig,axs=plt.subplots(3,1,figsize=(7.2,19.5),facecolor=BG); fig.subplots_adjust(hspace=0.12,top=0.915,bottom=0.04)
for ax,(k,(t,c)) in zip(axs,grp.items()):
    base(ax)
    fill(ax,soils,lambda p:"#D6E6EC" if p["nom_sol_dominant"] in WET else "#EFEDE4")
    draw_rivers(ax,"#8DB8DE",0.7,z=3)
    pts=[f["geometry"]["coordinates"] for f in gb if f["properties"]["g"]==k]
    xs,ys=zip(*[T(*p) for p in pts]) if pts else ([],[])
    ax.scatter(xs,ys,s=3.5,color=c,alpha=.4,lw=0,zorder=10)
    frame(ax); ax.set_title(t.replace(", ","\n",1)+" · "+format(len(pts),",").replace(","," ")+" points",fontsize=13,loc="left")
    towns(ax,["Meaux","Melun","Fontainebleau","Provins","Nemours"])
axs[2].legend(handles=[Patch(fc="#D6E6EC",label="Sols hydromorphes dominants"),Line2D([],[],color="#8DB8DE",lw=1,label="Cours d'eau > 5 m"),CATLEG,DEPLEG],**LEGKW)
fig.suptitle("Où sont observées les espèces\nde l'aide-mémoire (GBIF)",x=0.02,y=0.995,ha="left",fontsize=17,fontweight="bold")
credit(fig,"GBIF.org, API d'occurrences (15 nov. 2026), au plus 2 400 enregistrements lus par espèce dans l'emprise, puis filtrés aux bassins. Jeux principaux : CBNBP, CPIE Boucles de la Marne, iNaturalist, Pl@ntNet, Observation.org, SINP Île-de-France. Données flore souvent floutées à la maille. Fonds : INRAE, IGN.")
fig.savefig(f"{O}/03-gbif-especes.png",dpi=140,bbox_inches="tight",facecolor=BG); plt.close(fig)

# ---------- 04 Loing
lo=[g for n,g in groups if n=="Loing"][0]
x0,y0=T(2.60,48.20); x1,y1=T(3.00,48.45); bnd=(x0,y0,x1,y1)
fig,ax=plt.subplots(figsize=(8,10),facecolor=BG); base(ax,bnd,0)
fill(ax,soils,lambda p:SOILC.get(p["nom_sol_dominant"],"#ccc"),alpha=.9)
fill(ax,water,lambda p:"#4F8FCB",z=3)
draw_rivers(ax,"#1F5E99",1.2,z=4)
for p,g in n2k: edge(ax,g,"#B03A2E",1.1,z=15)
for p,g in zn: edge(ax,g,"#6B4E9B",.7,":",z=14)
for _,g in groups: edge(ax,g,INK,1.2,z=18)
edge(ax,DEP,"#B03A2E",1.4,(0,(4,2)),z=22)
pl=[T(*f["geometry"]["coordinates"]) for f in gb if f["properties"]["g"]=="plante"]
ax.scatter(*zip(*pl),s=6,color="#2E6650",alpha=.55,lw=0,zorder=16)
ar=[T(*f["geometry"]["coordinates"]) for f in gb if f["properties"]["g"]=="fontainebleau"]
if ar: ax.scatter(*zip(*ar),s=45,marker="*",color="#E0A100",edgecolor=INK,lw=.4,zorder=17)
for n,g in groups:
    rp=g.intersection(shape({"type":"Polygon","coordinates":[[(x0,y0),(x1,y0),(x1,y1),(x0,y1),(x0,y0)]]}))
    if rp.area>3e7:
        q=rp.representative_point(); dx,dy={"Seine (Melun)":(0,4500),"École":(3000,0)}.get(n,(0,0)); ax.text(q.x+dx,q.y+dy,"Bassin : "+n,fontsize=8,fontweight="bold",color=INK,zorder=36,ha="center",bbox=dict(boxstyle="round,pad=0.2",fc="#FFFFFFB0",ec="none"))
towns(ax,["Fontainebleau","Moret","Episy","Nemours","Montereau"],bounds=bnd); scalebar(ax,5)
hand=[Patch(fc=SOILC[k],label=k.capitalize()) for k in ["FLUVIOSOL","REDUCTISOL","PODZOSOL","CALCOSOL","LUVISOL","FERSIALSOL"]]+[Patch(fc="#4F8FCB",label="Eaux, zones humides (CLC)"),Line2D([],[],color="#B03A2E",lw=1.2,label="Natura 2000"),Line2D([],[],color="#6B4E9B",lw=1,ls=":",label="ZNIEFF type 1"),Line2D([],[],color=INK,lw=1.2,label="Limites des bassins"),DEPLEG,Line2D([],[],marker="o",ls="",color="#2E6650",label="Plantes indicatrices (GBIF)"),Line2D([],[],marker="*",ls="",color="#E0A100",mec=INK,ms=10,label="Arenaria grandiflora (GBIF)")]
ax.legend(handles=hand,**LEGKW)
ax.set_title("Bassin du Loing aval\net massif de Fontainebleau",loc="left",fontsize=17,fontweight="bold")
credit(fig,"Données : INRAE (sols), CLC 2018, IGN BD CARTO (cours d'eau, bassins), PatriNat/INPN (Natura 2000, ZNIEFF), GBIF.org (15 nov. 2026). Lambert-93. L. Angulo López, nov. 2026.")
fig.savefig(f"{O}/04-loing.png",dpi=150,bbox_inches="tight",facecolor=BG); plt.close(fig)
print("maps done")
