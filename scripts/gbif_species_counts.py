import json,urllib.request,urllib.parse,time,sys
UA={"User-Agent":"wetland-study-map/1.0"}
def get(u):
    for k in range(4):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=60))
        except Exception as e: time.sleep(3*(k+1)); err=e
    raise err
groups={
 "plante":"Phragmites australis|Typha latifolia|Phalaris arundinacea|Glyceria maxima|Carex riparia|Carex acutiformis|Carex elata|Juncus effusus|Juncus inflexus|Iris pseudacorus|Lythrum salicaria|Filipendula ulmaria|Lysimachia vulgaris|Eupatorium cannabinum|Epilobium hirsutum|Mentha aquatica|Lycopus europaeus|Caltha palustris|Angelica sylvestris|Cirsium oleraceum|Sparganium erectum|Solanum dulcamara|Alnus glutinosa|Salix cinerea",
 "oiseau":"Tachybaptus ruficollis|Anas crecca|Anas platyrhynchos|Aythya ferina|Aythya fuligula|Fulica atra|Gallinula chloropus|Phalacrocorax carbo|Ardea cinerea|Ardea alba|Alcedo atthis|Rallus aquaticus|Gallinago gallinago|Emberiza schoeniclus",
 "invasive":"Ludwigia grandiflora|Ludwigia peploides|Reynoutria japonica|Impatiens glandulifera|Elodea nuttallii|Myocastor coypus|Ondatra zibethicus|Procambarus clarkii|Pacifastacus leniusculus|Branta canadensis",
 "fontainebleau":"Arenaria grandiflora"}
GADM="FRA.8.4_1"
out=[];summary=[]
for grp,names in groups.items():
  for n in names.split("|"):
    m=get("https://api.gbif.org/v1/species/match?"+urllib.parse.urlencode({"name":n,"strict":"true"}))
    key=m.get("usageKey"); 
    if m.get("acceptedUsageKey"): key=m["acceptedUsageKey"]
    base={"taxonKey":key,"gadmGid":GADM,"hasCoordinate":"true","hasGeospatialIssue":"false","occurrenceStatus":"PRESENT"}
    tot=get("https://api.gbif.org/v1/occurrence/search?"+urllib.parse.urlencode({**base,"limit":0}))["count"]
    q={**base,"year":"2000,2026","coordinateUncertaintyInMeters":"0,1000"}
    recent=get("https://api.gbif.org/v1/occurrence/search?"+urllib.parse.urlencode({**q,"limit":0}))["count"]
    pts=[];off=0
    while off<600:
        r=get("https://api.gbif.org/v1/occurrence/search?"+urllib.parse.urlencode({**q,"limit":300,"offset":off}))
        for o in r["results"]:
            pts.append([round(o["decimalLongitude"],4),round(o["decimalLatitude"],4),o.get("year"),o.get("datasetKey")])
        off+=300
        if r.get("endOfRecords"): break
        time.sleep(0.5)
    summary.append({"name":n,"group":grp,"taxonKey":key,"matched":m.get("scientificName"),"total":tot,"recent_precise":recent,"mapped":len(pts)})
    for p in pts: out.append({"type":"Feature","geometry":{"type":"Point","coordinates":p[:2]},"properties":{"sp":n,"g":grp,"y":p[2],"ds":p[3]}})
    print(n,key,tot,recent,len(pts),flush=True)
json.dump({"type":"FeatureCollection","features":out},open("gbif.geojson","w"),separators=(",",":"))
json.dump(summary,open("gbif_summary.json","w"),indent=1,ensure_ascii=False)
