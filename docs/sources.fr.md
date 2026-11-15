# Sources et méthode

Toutes les données sont ouvertes et ont été lues le 15 novembre 2026. Chaque source garde sa propre licence et ses conditions de citation ; suivez les liens.

## Couches

| Couche | Source | Accès |
| --- | --- | --- |
| Limite du département | IGN, Admin Express COG Carto | WFS Géoplateforme `ADMINEXPRESS-COG-CARTO.LATEST:departement` |
| Bassins versants et cours d'eau | IGN, BD CARTO V5, bassins versants topographiques et tronçons hydrographiques | WFS Géoplateforme `BDCARTO_V5` |
| Sols dominants | INRAE, *Les sols dominants de France métropolitaine*, carte harmonisée | WFS Géoplateforme `INRAE_CARTE-SOLS:sols_dominants_france_metropolitaine` |
| Occupation du sol | CORINE Land Cover 2018, Copernicus (UE), édition française du SDES | WFS Géoplateforme `LANDCOVER.CLC18_FR` |
| Natura 2000, ZNIEFF de type 1 | PatriNat (OFB, MNHN, CNRS, IRD), INPN | WFS Géoplateforme `patrinat_sic`, `patrinat_zps`, `patrinat_znieff1` |
| Fond du monde (carte interactive) | Pays Natural Earth, depuis le `world_map.gpkg` de QGIS | Simplifié avec GDAL ogr2ogr |
| Zones humides (diapositive 6) | DRIEAT Île-de-France, Enveloppes d'alerte des zones humides, mise à jour 2021, Licence Ouverte 2.0 | [data.gouv.fr](https://www.data.gouv.fr/datasets/enveloppes-dalerte-des-zones-humides-dile-de-france-1), shapefile, rastérisé à 20 m |
| Zones humides hors Île-de-France (diapositive 6) | Agence de l'eau Seine-Normandie, Prélocalisation des zones humides potentielles, 2016, Licence Ouverte 2.0 | [data.gouv.fr](https://www.data.gouv.fr/datasets/prelocalisation-des-zones-humides-potentielles-dans-le-bassin-seine-normandie), shapefile, rastérisé à 20 m |
| Observations d'espèces | API d'occurrences de GBIF.org | [api.gbif.org](https://api.gbif.org/v1/occurrence/search) |

## Méthode

(i) **Zone d'étude.** Les bassins versants topographiques de la BD CARTO qui touchent la Seine-et-Marne (81 zones), regroupés selon la rivière réceptrice en 14 bassins ; leur union forme la zone d'étude.

(ii) **Surfaces.** Toutes les couches sont découpées aux bassins avec shapely et mesurées en Lambert-93 (EPSG:2154). Les parts des tableaux sont rapportées à la surface de chaque bassin.

(iii) **GBIF.** Espèces rapprochées du référentiel taxonomique GBIF (mode strict). Les comptes par département utilisent le filtre GADM FRA.8.4_1. Points des cartes : observations depuis 2000, avec coordonnées et sans problème géospatial, dans l'emprise des bassins, au plus 2 400 lues par espèce, puis gardées si elles tombent dans les bassins ; pour les oiseaux, seulement les observations localisées à 1 km près ou mieux. La carte interactive montre un tirage aléatoire d'au plus 350 points par espèce.

(iv) **Limites.** La carte des sols est au 1/1 000 000 et ne montre que les sols dominants ; les zones urbaines denses ne sont pas cartographiées. CORINE Land Cover ignore les unités de moins de 25 ha. Une grande partie des données botaniques du GBIF est floutée à la maille. Aucune de ces cartes ne délimite une zone humide au sens réglementaire.

## Jeux de données GBIF

Les 66 342 observations cartographiées viennent de 593 jeux de données. Les 15 plus importants :

| Observations | Jeu de données | DOI |
| ---: | --- | --- |
| 15 140 | Données acquises par le Conservatoire botanique national du Bassin parisien et son réseau, Flore du Bassin parisien (CBNBP) | [10.15468/vctras](https://doi.org/10.15468/vctras) |
| 4 915 | iNaturalist Research-grade Observations | [10.15468/ab3s5x](https://doi.org/10.15468/ab3s5x) |
| 3 725 | Observations opportunistes, CPIE Boucles de la Marne | [10.15468/abmycz](https://doi.org/10.15468/abmycz) |
| 3 442 | Anciennes données CBNBP, données Habitat | [10.15468/4zddkf](https://doi.org/10.15468/4zddkf) |
| 2 993 | Pl@ntNet automatically identified occurrences | [10.15468/mma2ec](https://doi.org/10.15468/mma2ec) |
| 2 284 | INPN, données flore des CBN agrégées par la FCBN | [10.15468/omae84](https://doi.org/10.15468/omae84) |
| 2 150 | SINP Île-de-France (CETTIA), données d'un naturaliste | [10.15468/qvzekx](https://doi.org/10.15468/qvzekx) |
| 2 075 | Inventaire de la flore vasculaire par maille 5 km × 5 km | [10.15468/m6bxc7](https://doi.org/10.15468/m6bxc7) |
| 1 277 | Inventaire de la flore vasculaire à l'échelle communale | [10.15468/fy5vkt](https://doi.org/10.15468/fy5vkt) |
| 1 266 | Anciennes données CBNBP, données Flora | [10.15468/gqfks3](https://doi.org/10.15468/gqfks3) |
| 1 233 | SINP Île-de-France (CETTIA), données d'une structure | [10.15468/nlto1y](https://doi.org/10.15468/nlto1y) |
| 1 227 | SINP Île-de-France (CETTIA), données d'une structure | [10.15468/ruvxhy](https://doi.org/10.15468/ruvxhy) |
| 1 171 | Observations du Conservatoire botanique national du Bassin parisien | [10.15468/megroo](https://doi.org/10.15468/megroo) |
| 1 155 | SINP Île-de-France (CETTIA), données d'un naturaliste | [10.15468/kqktar](https://doi.org/10.15468/kqktar) |
| 994 | Pl@ntNet observations | [10.15468/gtebaa](https://doi.org/10.15468/gtebaa) |

Liste complète avec les clés : [gbif_datasets.json](data/gbif_datasets.json). Ces requêtes utilisent l'API de recherche ouverte, qui ne produit pas de DOI de citation ; un téléchargement GBIF avec le même filtre en produirait un.

## Bibliographie

Maurice, A.-C. et al. (2013). Mixing plants from different origins to restore a declining population: ecological outcomes and local perceptions 10 years later. *PLoS ONE* 8(1): e50934. [PMC3549913](https://pmc.ncbi.nlm.nih.gov/articles/PMC3549913/)

Brisset et al. (2025). Genetic rescue in action: long-term monitoring reveals admixture-driven fitness gains in a translocated plant. *Conservation Letters*. [doi:10.1111/con4.70012](https://doi.org/10.1111/con4.70012)

## Refaire les cartes

Le dossier `scripts/` contient le code : `fetch_layers.py` (couches WFS et bassins), `gbif_species_counts.py` et `gbif_catchment_records.py` (GBIF), `render_maps.py` et `render_extras.py` (cartes, statistiques, couches web). Python 3 avec shapely, pyproj et matplotlib.

## Crédits photo { #photo-credits }

Les photos d'espèces des pages du récit sont les images principales des articles de Wikipédia en anglais, hébergées sur Wikimedia Commons ; une photo (lactaire des flaques) est un fichier Commons. Chaque page de fichier donne l'auteur et la licence (Creative Commons ou domaine public).

| Espèce | Fichier Wikimedia Commons |
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
