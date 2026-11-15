"""Download the open layers used by the maps (IGN Géoplateforme WFS), into DATA_DIR.

Usage: python fetch_layers.py DATA_DIR
Steps: (i) Seine-et-Marne outline (Admin Express), (ii) BD CARTO topographic catchments
touching it, grouped by river, (iii) soils, CORINE Land Cover 2018, Natura 2000,
ZNIEFF type 1 and rivers over the catchments' extent.
"""
import json, sys, urllib.request, urllib.parse
from shapely.geometry import shape, mapping
from shapely.ops import unary_union
D = sys.argv[1]
WFS = "https://data.geopf.fr/wfs/ows?"
def wfs(typename, bbox=None, cql=None, count=5000):
    feats, start = [], 0
    while True:
        q = {"SERVICE": "WFS", "VERSION": "2.0.0", "REQUEST": "GetFeature", "TYPENAMES": typename,
             "OUTPUTFORMAT": "application/json", "SRSNAME": "EPSG:4326", "COUNT": str(count), "STARTINDEX": str(start)}
        if bbox: q["BBOX"] = f"{bbox[1]},{bbox[0]},{bbox[3]},{bbox[2]},urn:ogc:def:crs:EPSG::4326"
        if cql: q["CQL_FILTER"] = cql
        g = json.loads(urllib.request.urlopen(WFS + urllib.parse.urlencode(q), timeout=600).read())
        feats += g["features"]
        if len(g["features"]) < count: return feats
        start += count
def save(name, feats): json.dump({"type": "FeatureCollection", "features": feats}, open(f"{D}/{name}.geojson", "w"))

dep = wfs("ADMINEXPRESS-COG-CARTO.LATEST:departement", cql="code_insee='77'"); save("dep77", dep)
DEP = shape(dep[0]["geometry"])
GROUP = [(["F621","F622","F626","F640","F642","F643","F660","F662","F663","F664","F641","F661"], "Marne"),
 (["F637","F638"], "Ourcq"), (["F624","F625"], "Petit Morin"), (["F65"], "Grand Morin"), (["F47","F48"], "Yerres"),
 (["F202","F211","F213","F214","F215","F220","F221","F222","F223","F240","F241","F242","F243","F400"], "Seine (Bassée)"),
 (["F23"], "Voulzie"), (["F444","F445","F446"], "Almont"), (["F440","F441","F442","F443","F447","F449","F460"], "Seine (Melun)"),
 (["F448"], "École"), (["F452"], "Essonne"), (["F42","F43"], "Loing"), (["F359"], "Yonne"), (["F70","H2"], "Crould, Oise")]
def grp(code): return next((n for keys, n in GROUP if any(code.startswith(k) for k in keys)), None)
zones, by = [], {}
for f in wfs("BDCARTO_V5:bassin_versant_topographique", bbox=DEP.bounds):
    s = shape(f["geometry"])
    if not s.intersects(DEP) or s.intersection(DEP).area / s.area < 0.001: continue
    code = f["properties"]["code_bdcarthage"]; n = grp(code)
    zones.append({"type": "Feature", "geometry": mapping(s), "properties": {"code": code, "toponyme": f["properties"]["toponyme"], "catchment": n}})
    by.setdefault(n, []).append(s)
save("catch_zones", zones)
save("catch_groups", [{"type": "Feature", "geometry": mapping(unary_union(v)), "properties": {"catchment": k, "zones": len(v)}} for k, v in by.items()])
U = unary_union([shape(z["geometry"]) for z in zones])
save("catch_union", [{"type": "Feature", "geometry": mapping(U), "properties": {}}])
b = U.bounds
for tn, fn in [("INRAE_CARTE-SOLS:sols_dominants_france_metropolitaine", "c_sols"), ("patrinat_sic:sic", "c_sic"),
               ("patrinat_zps:zps", "c_zps"), ("patrinat_znieff1:znieff1", "c_znieff1"), ("LANDCOVER.CLC18_FR:clc18_fr", "c_clc18")]:
    save(fn, wfs(tn, bbox=b))
save("c_rivers", wfs("BDCARTO_V5:troncon_hydrographique", count=10000,
    cql="classe_de_largeur IN ('Entre 5 et 15 m','Entre 15 et 50 m','Plus de 50 m') AND BBOX(geometrie,%f,%f,%f,%f)" % (b[1], b[0], b[3], b[2])))
print("layers saved in", D)
