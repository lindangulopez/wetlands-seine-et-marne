# Sources and method

All data are open and were read on 15 November 2026. Each source keeps its own licence and citation terms; follow the links.

## Layers

| Layer | Source | Access |
| --- | --- | --- |
| Département outline | IGN, Admin Express COG Carto | Géoplateforme WFS `ADMINEXPRESS-COG-CARTO.LATEST:departement` |
| Catchments and rivers | IGN, BD CARTO V5, bassins versants topographiques and tronçons hydrographiques | Géoplateforme WFS `BDCARTO_V5` |
| Dominant soils | INRAE, *Les sols dominants de France métropolitaine*, carte harmonisée | Géoplateforme WFS `INRAE_CARTE-SOLS:sols_dominants_france_metropolitaine` |
| Land cover | CORINE Land Cover 2018, EU Copernicus, French edition by SDES | Géoplateforme WFS `LANDCOVER.CLC18_FR` |
| Natura 2000, ZNIEFF type 1 | PatriNat (OFB, MNHN, CNRS, IRD), INPN | Géoplateforme WFS `patrinat_sic`, `patrinat_zps`, `patrinat_znieff1` |
| World base map (interactive map) | Natural Earth countries, from the QGIS `world_map.gpkg` | Simplified with GDAL ogr2ogr |
| Species records | GBIF.org occurrence API | [api.gbif.org](https://api.gbif.org/v1/occurrence/search) |

## Method

(i) **Study area.** BD CARTO topographic catchments overlapping Seine-et-Marne (81 zones), grouped by receiving river into 14 catchments; their union is the study area.

(ii) **Areas.** All layers clipped to the catchments with shapely and measured in Lambert-93 (EPSG:2154). Shares in the tables are of each catchment's area.

(iii) **GBIF.** Species matched to the GBIF backbone (strict). Counts per département use the GADM filter FRA.8.4_1. Map points: records since 2000 with coordinates and no geospatial issue in the catchments' bounding box, at most 2,400 read per species, then kept if inside the catchments; for birds, only records located to 1 km or better. The interactive map shows a random subset of up to 350 points per species.

(iv) **Limits.** The soil map is at 1:1,000,000 and shows dominant soils only; dense urban areas are unmapped. CORINE Land Cover misses units below 25 ha. Much botanical data in GBIF is blurred to a grid. None of these maps delimits a wetland in the legal sense.

## GBIF datasets

The 66,342 records mapped come from 593 datasets. The 15 largest:

| Records | Dataset | DOI |
| ---: | --- | --- |
| 15,140 | Données acquises par le Conservatoire botanique national du Bassin parisien et son réseau, Flore du Bassin parisien (CBNBP) | [10.15468/vctras](https://doi.org/10.15468/vctras) |
| 4,915 | iNaturalist Research-grade Observations | [10.15468/ab3s5x](https://doi.org/10.15468/ab3s5x) |
| 3,725 | Observations opportunistes, CPIE Boucles de la Marne | [10.15468/abmycz](https://doi.org/10.15468/abmycz) |
| 3,442 | Anciennes données CBNBP, données Habitat | [10.15468/4zddkf](https://doi.org/10.15468/4zddkf) |
| 2,993 | Pl@ntNet automatically identified occurrences | [10.15468/mma2ec](https://doi.org/10.15468/mma2ec) |
| 2,284 | INPN, données flore des CBN agrégées par la FCBN | [10.15468/omae84](https://doi.org/10.15468/omae84) |
| 2,150 | SINP Île-de-France (CETTIA), données d'un naturaliste | [10.15468/qvzekx](https://doi.org/10.15468/qvzekx) |
| 2,075 | Inventaire de la flore vasculaire par maille 5 km × 5 km | [10.15468/m6bxc7](https://doi.org/10.15468/m6bxc7) |
| 1,277 | Inventaire de la flore vasculaire à l'échelle communale | [10.15468/fy5vkt](https://doi.org/10.15468/fy5vkt) |
| 1,266 | Anciennes données CBNBP, données Flora | [10.15468/gqfks3](https://doi.org/10.15468/gqfks3) |
| 1,233 | SINP Île-de-France (CETTIA), données d'une structure | [10.15468/nlto1y](https://doi.org/10.15468/nlto1y) |
| 1,227 | SINP Île-de-France (CETTIA), données d'une structure | [10.15468/ruvxhy](https://doi.org/10.15468/ruvxhy) |
| 1,171 | Observations du Conservatoire botanique national du Bassin parisien | [10.15468/megroo](https://doi.org/10.15468/megroo) |
| 1,155 | SINP Île-de-France (CETTIA), données d'un naturaliste | [10.15468/kqktar](https://doi.org/10.15468/kqktar) |
| 994 | Pl@ntNet observations | [10.15468/gtebaa](https://doi.org/10.15468/gtebaa) |

Full list with keys: [gbif_datasets.json](data/gbif_datasets.json). These queries used the open search API, which does not mint a citation DOI; a GBIF download of the same filter would.

## Literature

Maurice, A.-C. et al. (2013). Mixing plants from different origins to restore a declining population: ecological outcomes and local perceptions 10 years later. *PLoS ONE* 8(1): e50934. [PMC3549913](https://pmc.ncbi.nlm.nih.gov/articles/PMC3549913/)

Brisset et al. (2025). Genetic rescue in action: long-term monitoring reveals admixture-driven fitness gains in a translocated plant. *Conservation Letters*. [doi:10.1111/con4.70012](https://doi.org/10.1111/con4.70012)

## Rebuild the maps

The `scripts/` folder holds the code: `fetch_layers.py` (WFS layers and catchments), `gbif_species_counts.py` and `gbif_catchment_records.py` (GBIF), `render_maps.py` and `render_extras.py` (maps, statistics, web layers). Python 3 with shapely, pyproj and matplotlib.
