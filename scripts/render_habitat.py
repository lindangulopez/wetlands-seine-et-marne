import sys,json
D,O,RM=sys.argv[1:4]
exec(open(RM).read().split("# ---------- stats")[0])
gb=L("gbif_catch"); soils=clipfeats(L("c_sols"))
WET={"FLUVIOSOL","REDUCTISOL","REDOXISOL","LUVISOL-REDOXISOL","BRUNISOL-REDOXISOL","PLANOSOL"}
SP=["Filipendula ulmaria","Lythrum salicaria","Eupatorium cannabinum","Epilobium hirsutum","Lysimachia vulgaris","Angelica sylvestris"]
pts=[T(*f["geometry"]["coordinates"]) for f in gb if f["properties"]["sp"] in SP]
fp=[T(*f["geometry"]["coordinates"]) for f in gb if f["properties"]["sp"]=="Filipendula ulmaria"]
fig,ax=plt.subplots(figsize=(8,11),facecolor=BG); base(ax)
fill(ax,soils,lambda p:"#CFE1EA" if p["nom_sol_dominant"] in WET else "#F1EEE4")
draw_rivers(ax,"#7FAFD8",0.8,z=3)
ax.scatter(*zip(*pts),s=7,color="#9B6FA8",alpha=.35,lw=0,zorder=9)
ax.scatter(*zip(*fp),s=10,color="#2E6650",alpha=.7,lw=0,zorder=10)
frame(ax); towns(ax,["Meaux","Melun","Fontainebleau","Provins","Nemours","Coulommiers"]); scalebar(ax)
f=lambda n:format(n,",").replace(","," ")
ax.legend(handles=[Line2D([],[],marker="o",ls="",color="#2E6650",label=f"Reine-des-prés, espèce phare ({f(len(fp))} points)"),Line2D([],[],marker="o",ls="",color="#9B6FA8",label=f"Les 6 plantes de la mégaphorbiaie ({f(len(pts))} points)"),Patch(fc="#CFE1EA",label="Sols hydromorphes dominants"),Line2D([],[],color="#7FAFD8",lw=1.2,label="Cours d'eau > 5 m"),CATLEG,DEPLEG],**LEGKW)
ax.set_title("La mégaphorbiaie (habitat 6430)\ndans les bassins de la Seine-et-Marne",loc="left",fontsize=17,fontweight="bold")
credit(fig,"Reine-des-prés, salicaire, eupatoire chanvrine, épilobe hérissé, lysimaque commune, angélique des bois : observations GBIF depuis 2000 (15 nov. 2026, au plus 2 400 lues par espèce). Fonds : INRAE, IGN BD CARTO. Lambert-93. L. Angulo López, nov. 2026.")
fig.savefig(f"{O}/habitat-megaphorbiaie.png",dpi=150,bbox_inches="tight",facecolor=BG)
print(len(fp),len(pts))
