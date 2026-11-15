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
| Wetlands (slide 6) | DRIEAT Île-de-France, Enveloppes d'alerte des zones humides, 2021 update, Licence Ouverte 2.0 | [data.gouv.fr](https://www.data.gouv.fr/datasets/enveloppes-dalerte-des-zones-humides-dile-de-france-1), shapefile, rasterised at 20 m |
| Wetlands outside Île-de-France (slide 6) | Agence de l'eau Seine-Normandie, Prélocalisation des zones humides potentielles, 2016, Licence Ouverte 2.0 | [data.gouv.fr](https://www.data.gouv.fr/datasets/prelocalisation-des-zones-humides-potentielles-dans-le-bassin-seine-normandie), shapefile, rasterised at 20 m |
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

## Photo credits

Species photos on the story pages are the lead images of the English Wikipedia articles, hosted on Wikimedia Commons; one photo (puddle milkcap) is a Commons file. Each file page gives the author and the licence (Creative Commons or public domain).

| Species | Wikimedia Commons file |
| --- | --- |
| *Acrocephalus scirpaceus* | [PleidelsheimerWiesentalTeichrohrsaenger.jpg](https://commons.wikimedia.org/wiki/File:PleidelsheimerWiesentalTeichrohrsaenger.jpg) |
| *Alcedo atthis* | [Alcedo_atthis_-England-8_%28cropped%29.jpg](https://commons.wikimedia.org/wiki/File:Alcedo_atthis_-England-8_%28cropped%29.jpg) |
| *Alnus glutinosa* | [20120904Alnus_glutinosa01.jpg](https://commons.wikimedia.org/wiki/File:20120904Alnus_glutinosa01.jpg) |
| *Auricularia auricula-judae* | [Jelly_Ear%2C_Auricularia_auricula-judae%2C_UK_2.jpg](https://commons.wikimedia.org/wiki/File:Jelly_Ear%2C_Auricularia_auricula-judae%2C_UK_2.jpg) |
| *Botaurus stellaris* | [Eurasian_Bittern_-_Torrile_-_Italy_4528_%2815409347121%29.jpg](https://commons.wikimedia.org/wiki/File:Eurasian_Bittern_-_Torrile_-_Italy_4528_%2815409347121%29.jpg) |
| *Bufo bufo* | [Common_Toad_Cornwall.jpeg](https://commons.wikimedia.org/wiki/File:Common_Toad_Cornwall.jpeg) |
| *Calopteryx splendens* | [Banded_demoiselle_damselfly_%28Calopteryx_splendens%29_male_4.jpg](https://commons.wikimedia.org/wiki/File:Banded_demoiselle_damselfly_%28Calopteryx_splendens%29_male_4.jpg) |
| *Caltha palustris* | [Caltha_palustris_plant.JPG](https://commons.wikimedia.org/wiki/File:Caltha_palustris_plant.JPG) |
| *Cerioporus squamosus* | [Polyporus_squamosus_Molter.jpg](https://commons.wikimedia.org/wiki/File:Polyporus_squamosus_Molter.jpg) |
| *Coenagrion puella* | [Azure_damselfly_%28Coenagrion_puella%29_male_Montiaghs_Moss.jpg](https://commons.wikimedia.org/wiki/File:Azure_damselfly_%28Coenagrion_puella%29_male_Montiaghs_Moss.jpg) |
| *Daedaleopsis confragosa* | [R%C3%B6tende_Bl%C3%A4tterwirrling_Daedaleopsis_confragosa.JPG](https://commons.wikimedia.org/wiki/File:R%C3%B6tende_Bl%C3%A4tterwirrling_Daedaleopsis_confragosa.JPG) |
| *Dytiscus marginalis* | [Geelgerande02.jpg](https://commons.wikimedia.org/wiki/File:Geelgerande02.jpg) |
| *Esox lucius* | [Esox_lucius_ZOO_1.jpg](https://commons.wikimedia.org/wiki/File:Esox_lucius_ZOO_1.jpg) |
| *Filipendula ulmaria* | [20140715Filipendula_ulmaria.jpg](https://commons.wikimedia.org/wiki/File:20140715Filipendula_ulmaria.jpg) |
| *Gallinago gallinago* | [Common_snipe_%28Gallinago_gallinago%29_2022.jpg](https://commons.wikimedia.org/wiki/File:Common_snipe_%28Gallinago_gallinago%29_2022.jpg) |
| *Kuehneromyces mutabilis* | [Stockschwaemmchen.jpg](https://commons.wikimedia.org/wiki/File:Stockschwaemmchen.jpg) |
| *Lactarius lacunarum* | [Lactarius_lacunarum_a1_(1).JPG](https://commons.wikimedia.org/wiki/File:Lactarius_lacunarum_a1_(1).JPG) |
| *Lythrum salicaria* | [Lythrum_salicaria_-_harilik_kukesaba.jpg](https://commons.wikimedia.org/wiki/File:Lythrum_salicaria_-_harilik_kukesaba.jpg) |
| *Micromys minutus* | [Micromysminutus1.jpg](https://commons.wikimedia.org/wiki/File:Micromysminutus1.jpg) |
| *Myotis daubentonii* | [Myotis_daubentoni01.jpg](https://commons.wikimedia.org/wiki/File:Myotis_daubentoni01.jpg) |
| *Natrix helvetica* | [BennyTrapp_Natrix_helvetica.jpg](https://commons.wikimedia.org/wiki/File:BennyTrapp_Natrix_helvetica.jpg) |
| *Phragmites australis* | [Reed_panicle_at_Brodalen_1.jpg](https://commons.wikimedia.org/wiki/File:Reed_panicle_at_Brodalen_1.jpg) |
| *Pleurotus ostreatus* | [Pleurotus_ostreatus_JPG7.jpg](https://commons.wikimedia.org/wiki/File:Pleurotus_ostreatus_JPG7.jpg) |
| *Sarcoscypha coccinea* | [Sarcoscypha_coccinea_74716.jpg](https://commons.wikimedia.org/wiki/File:Sarcoscypha_coccinea_74716.jpg) |
| *Sympetrum sanguineum* | [Sympetrum_sanguineum_LC0316.jpg](https://commons.wikimedia.org/wiki/File:Sympetrum_sanguineum_LC0316.jpg) |
| *Anax imperator* | [Anax_imperator_qtl2.jpg](https://commons.wikimedia.org/wiki/File:Anax_imperator_qtl2.jpg) |
