import json,urllib.request,urllib.parse,time,sys
from shapely.geometry import shape, Point
from shapely.prepared import prep
UA={"User-Agent":"wetland-study-map/1.0"}
def get(u):
    for k in range(5):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=90))
        except Exception as e: time.sleep(4*(k+1)); err=e
    raise err
U=shape(json.load(open("catch_union.geojson"))["features"][0]["geometry"]); PU=prep(U)
b=U.bounds
summ=json.load(open("gbif_summary.json"))
feats=[]
for s in summ:
    q={"taxonKey":s["taxonKey"],"decimalLatitude":f"{b[1]},{b[3]}","decimalLongitude":f"{b[0]},{b[2]}","hasCoordinate":"true","hasGeospatialIssue":"false","occurrenceStatus":"PRESENT","year":"2000,2026"}
    if s["group"]=="oiseau": q["coordinateUncertaintyInMeters"]="0,1000"
    tot=get("https://api.gbif.org/v1/occurrence/search?"+urllib.parse.urlencode({**q,"limit":0}))["count"]
    off=0;k=0;seen=0
    cap=2400
    while off<min(tot,cap):
        r=get("https://api.gbif.org/v1/occurrence/search?"+urllib.parse.urlencode({**q,"limit":300,"offset":off}))
        for o in r["results"]:
            seen+=1
            x,y=o["decimalLongitude"],o["decimalLatitude"]
            if PU.contains(Point(x,y)):
                feats.append({"type":"Feature","geometry":{"type":"Point","coordinates":[round(x,4),round(y,4)]},"properties":{"sp":s["name"],"g":s["group"],"y":o.get("year"),"u":o.get("coordinateUncertaintyInMeters"),"ds":o.get("datasetKey")}}); k+=1
        off+=300
        if r.get("endOfRecords"): break
    s["bbox_since2000"]=tot; s["catch_mapped"]=k; s["catch_seen"]=seen
    print(s["name"],tot,seen,k,flush=True)
json.dump({"type":"FeatureCollection","features":feats},open("gbif_catch.geojson","w"),separators=(",",":"))
json.dump(summ,open("gbif_summary.json","w"),indent=1,ensure_ascii=False)
print("DONE",len(feats))
