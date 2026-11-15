import json,sys,collections,urllib.request,time
sys.argv=sys.argv  # D O R
D,O,R=sys.argv[1:4]
exec(open(sys.argv[4]).read().split("# ---------- stats")[0])  # reuse helpers and layers from render_catch
gb=L("gbif_catch")
soils=clipfeats(L("c_sols"))
WET={"FLUVIOSOL","REDUCTISOL","REDOXISOL","LUVISOL-REDOXISOL","BRUNISOL-REDOXISOL","PLANOSOL"}
# Day 1 map
fp=[T(*f["geometry"]["coordinates"]) for f in gb if f["properties"]["sp"]=="Filipendula ulmaria"]
fig,ax=plt.subplots(figsize=(8,11),facecolor=BG); base(ax)
fill(ax,soils,lambda p:"#CFE1EA" if p["nom_sol_dominant"] in WET else "#F1EEE4")
draw_rivers(ax,"#7FAFD8",0.8,z=3)
ax.scatter(*zip(*fp),s=9,color="#2E6650",alpha=.55,lw=0,zorder=10)
frame(ax); towns(ax,["Meaux","Melun","Fontainebleau","Provins","Nemours","Coulommiers"]); scalebar(ax)
ax.legend(handles=[Line2D([],[],marker="o",ls="",color="#2E6650",label=f"Reine-des-prés, {len(fp):,} relevés GBIF depuis 2000".replace(","," ")),Patch(fc="#CFE1EA",label="Sols hydromorphes dominants (INRAE)"),Line2D([],[],color="#7FAFD8",lw=1.2,label="Cours d'eau > 5 m"),CATLEG,DEPLEG],**LEGKW)
ax.set_title("Reine-des-prés\nFilipendula ulmaria",loc="left",fontsize=18,fontweight="bold")
credit(fig,"Bassins versants de la Seine-et-Marne. GBIF.org (15 nov. 2026, au plus 2 400 relevés lus), INRAE, IGN BD CARTO. Lambert-93. L. Angulo López, nov. 2026.")
fig.savefig(f"{O}/day1-filipendula.png",dpi=150,bbox_inches="tight",facecolor=BG); plt.close(fig)
# web data
def rnd(o):
    if isinstance(o,list): return [rnd(x) for x in o]
    if isinstance(o,float): return round(o,4)
    return o
def wr(name,fc): 
    s=json.dumps(fc,separators=(",",":"),ensure_ascii=False); open(f"{R}/docs/data/{name}.geojson","w").write(s); print(name,round(len(s)/1e6,2),"MB")
from shapely.geometry import shape as sh, mapping
def simp(f,tol): 
    g=sh(f["geometry"]).simplify(tol,preserve_topology=True); return {"type":"Feature","geometry":rnd(mapping(g)),"properties":f["properties"]}
cg=json.load(open(f"{D}/catch_groups.geojson")); wr("catchments",{"type":"FeatureCollection","features":[simp(f,0.0008) for f in cg["features"]]})
cz=json.load(open(f"{D}/catch_zones.geojson")); wr("catchment_zones",{"type":"FeatureCollection","features":[simp(f,0.0008) for f in cz["features"]]})
dep=json.load(open(f"{D}/dep77.geojson")); wr("dep77",{"type":"FeatureCollection","features":[{"type":"Feature","geometry":rnd(mapping(sh(f["geometry"]).simplify(0.0005))),"properties":{"nom":"Seine-et-Marne"}} for f in dep["features"]]})
U=sh(json.load(open(f"{D}/catch_union.geojson"))["features"][0]["geometry"])
def n2(name,typ):
    out=[]
    for f in json.load(open(f"{D}/{name}.geojson"))["features"]:
        g=sh(f["geometry"])
        if g.intersects(U): out.append({"type":"Feature","geometry":rnd(mapping(g.simplify(0.0004))),"properties":{"nom_site":f["properties"]["nom_site"],"url_fiche":f["properties"]["url_fiche"],"type":typ}})
    return out
wr("natura2000",{"type":"FeatureCollection","features":n2("c_sic","ZSC/SIC")+n2("c_zps","ZPS")})
wr("znieff1",{"type":"FeatureCollection","features":n2("c_znieff1","ZNIEFF1")})
# gbif thinned: max 350 per species
by=collections.defaultdict(list)
for f in gb: by[f["properties"]["sp"]].append(f)
import random; random.seed(77)
thin=[]
for sp,fs in by.items():
    pick=fs if len(fs)<=350 else random.sample(fs,350)
    for f in pick: thin.append({"type":"Feature","geometry":f["geometry"],"properties":{k:f["properties"][k] for k in("sp","g","y","u")}})
wr("gbif",{"type":"FeatureCollection","features":thin})
# datasets
ds=collections.Counter(f["properties"]["ds"] for f in gb)
top=[]
for key,c in ds.most_common(15):
    d=json.load(urllib.request.urlopen(urllib.request.Request("https://api.gbif.org/v1/dataset/"+key,headers={"User-Agent":"wetland-study-map/1.0"}),timeout=60))
    top.append({"n":c,"title":d.get("title"),"doi":d.get("doi"),"key":key})
json.dump({"datasets_total":len(ds),"records":len(gb),"top":top},open(f"{O}/gbif_datasets.json","w"),indent=1,ensure_ascii=False)
print(len(ds),"datasets"); [print(t["n"],t["doi"],t["title"][:90]) for t in top]
