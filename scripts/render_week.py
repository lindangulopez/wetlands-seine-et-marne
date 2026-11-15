import sys,json
D,O,RM=sys.argv[1:4]
exec(open(RM).read().split("# ---------- stats")[0])
gb=L("gbif_catch")+L("gbif_week"); soils=clipfeats(L("c_sols")); clc=clipfeats(L("c_clc18"))
water=[(p,g) for p,g in clc if p["code_18"][0] in "45"]
WET={"FLUVIOSOL","REDUCTISOL","REDOXISOL","LUVISOL-REDOXISOL","BRUNISOL-REDOXISOL","PLANOSOL"}
f=lambda n:format(n,",").replace(","," ")
def sp_map(fn,sp,col,title,lab,cred,month_filter=None):
    pts=[T(*x["geometry"]["coordinates"]) for x in gb if x["properties"]["sp"]==sp and (month_filter is None or x["properties"].get("m") in month_filter)]
    fig,ax=plt.subplots(figsize=(8,11),facecolor=BG); base(ax)
    fill(ax,soils,lambda p:"#CFE1EA" if p["nom_sol_dominant"] in WET else "#F1EEE4")
    fill(ax,water,lambda p:"#8DB8DE",z=2); draw_rivers(ax,"#7FAFD8",0.8,z=3)
    ax.scatter(*zip(*pts),s=10,color=col,alpha=.55,lw=0,zorder=10)
    frame(ax); towns(ax,["Meaux","Melun","Fontainebleau","Provins","Nemours","Coulommiers"]); scalebar(ax)
    ax.legend(handles=[Line2D([],[],marker="o",ls="",color=col,label=f"{lab} ({f(len(pts))} points)"),Patch(fc="#CFE1EA",label="Sols hydromorphes dominants"),Patch(fc="#8DB8DE",label="Eaux, zones humides (CLC)"),CATLEG,DEPLEG],**LEGKW)
    ax.set_title(title,loc="left",fontsize=18,fontweight="bold")
    credit(fig,cred+" Fonds : INRAE, CLC 2018, IGN BD CARTO. Lambert-93. L. Angulo López, nov. 2026.")
    fig.savefig(f"{O}/{fn}.png",dpi=150,bbox_inches="tight",facecolor=BG); plt.close(fig); print(fn,len(pts))
sp_map("day2-grebe","Tachybaptus ruficollis","#2C5D8A","Grèbe castagneux\nTachybaptus ruficollis","Observations GBIF depuis 2000, précision ≤ 1 km","GBIF.org (15 nov. 2026), au plus 2 400 lues dans l'emprise.")
sp_map("day3-anax","Anax imperator","#B8860B","Anax empereur\nAnax imperator","Observations GBIF depuis 2000, précision ≤ 1 km","GBIF.org (15 nov. 2026), au plus 2 400 lues dans l'emprise.")
sp_map("day4-frog","Rana dalmatina","#A0522D","Grenouille agile\nRana dalmatina","Observations GBIF depuis 2000, précision ≤ 1 km","GBIF.org (15 nov. 2026), au plus 2 400 lues dans l'emprise.")
# day 5 soils: hydromorphic only
SC={"FLUVIOSOL":"#3E7CB1","REDUCTISOL":"#1B3F6B","REDOXISOL":"#5FA8A0","LUVISOL-REDOXISOL":"#8CC5B8","BRUNISOL-REDOXISOL":"#A9D3C6","PLANOSOL":"#7FB3D5"}
fig,ax=plt.subplots(figsize=(8,11),facecolor=BG); base(ax)
fill(ax,soils,lambda p:SC.get(p["nom_sol_dominant"],"#EFEDE4")); draw_rivers(ax,"#FFFFFF",0.5,z=3)
frame(ax); towns(ax,["Meaux","Melun","Fontainebleau","Provins","Nemours","Coulommiers","Montereau"]); scalebar(ax)
ax.legend(handles=[Patch(fc=SC[k],label=l) for k,l in [("FLUVIOSOL","Fluviosol, alluvions des vallées (7 %)"),("REDUCTISOL","Réductisol, engorgé en permanence (1 %)"),("LUVISOL-REDOXISOL","Luvisol-rédoxisol, engorgé en hiver (2 %)"),("BRUNISOL-REDOXISOL","Brunisol-rédoxisol (1 %)"),("PLANOSOL","Planosol (1 %)"),("REDOXISOL","Rédoxisol (< 1 %)")]]+[Patch(fc="#EFEDE4",label="Autres sols"),CATLEG,DEPLEG],title="Sols hydromorphes dominants, part de la surface",**LEGKW)
ax.set_title("Les sols qui gardent l'eau\nen hiver",loc="left",fontsize=18,fontweight="bold")
credit(fig,"Données : INRAE, Les sols dominants de France métropolitaine (Géoplateforme) ; IGN BD CARTO. Lambert-93. L. Angulo López, nov. 2026.")
fig.savefig(f"{O}/day5-soils.png",dpi=150,bbox_inches="tight",facecolor=BG); plt.close(fig)
# day 6 ecosystem: Loing/Bassée window, all five
x0,y0=T(2.62,48.22); x1,y1=T(3.25,48.52); bnd=(x0,y0,x1,y1)
fig,ax=plt.subplots(figsize=(8,10),facecolor=BG); base(ax,bnd,0)
fill(ax,soils,lambda p:SC.get(p["nom_sol_dominant"],"#F1EEE4"),alpha=.85)
fill(ax,water,lambda p:"#4F8FCB",z=3); draw_rivers(ax,"#1F5E99",1.0,z=4)
for _,g in groups: edge(ax,g,INK,1.0,z=18)
edge(ax,DEP,"#B03A2E",1.4,(0,(4,2)),z=22)
layers=[("Filipendula ulmaria","#2E6650","o","Reine-des-prés"),("Tachybaptus ruficollis","#123A66","D","Grèbe castagneux"),("Anax imperator","#E0A100","^","Anax empereur"),("Rana dalmatina","#A0522D","s","Grenouille agile")]
hand=[]
for sp,c,m,l in layers:
    pts=[T(*x["geometry"]["coordinates"]) for x in gb if x["properties"]["sp"]==sp]
    pts=[p for p in pts if x0<p[0]<x1 and y0<p[1]<y1]
    if pts: ax.scatter(*zip(*pts),s=16,color=c,marker=m,alpha=.7,lw=0,zorder=12)
    hand.append(Line2D([],[],marker=m,ls="",color=c,label=f"{l} ({f(len(pts))})"))
towns(ax,["Fontainebleau","Moret","Episy","Nemours","Montereau","Provins"],bounds=bnd); scalebar(ax,5)
hand+=[Patch(fc=SC["FLUVIOSOL"],label="Fluviosol"),Patch(fc=SC["REDUCTISOL"],label="Réductisol"),Patch(fc="#4F8FCB",label="Eaux, zones humides (CLC)"),Line2D([],[],color=INK,lw=1,label="Limites des bassins"),DEPLEG]
ax.legend(handles=hand,**LEGKW)
ax.set_title("Une zone humide, du sol à l'oiseau\nLoing aval et Bassée",loc="left",fontsize=18,fontweight="bold")
credit(fig,"Observations GBIF depuis 2000 (15 nov. 2026) ; sols INRAE ; CLC 2018 ; IGN BD CARTO. Lambert-93. L. Angulo López, nov. 2026.")
fig.savefig(f"{O}/day6-ecosystem.png",dpi=150,bbox_inches="tight",facecolor=BG); plt.close(fig)
print("done")
