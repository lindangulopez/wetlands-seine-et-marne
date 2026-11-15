# Wetlands of Seine-et-Marne, a catchment view

Maps of soils, vegetation and wetland species in the 14 river catchments that drain Seine-et-Marne (France), built from open data: IGN BD CARTO, INRAE soil map, CORINE Land Cover 2018, PatriNat/INPN protected sites, and GBIF species records.

Site (English and French): https://lindangulopez.github.io/wetlands-seine-et-marne/ · version française : https://lindangulopez.github.io/wetlands-seine-et-marne/fr/

- `docs/` MkDocs pages, maps (`docs/maps/`), web layers and statistics (`docs/data/`), interactive map (`docs/carte.html`)
- `scripts/` code to fetch the data and draw the maps
- `.github/workflows/deploy.yml` builds the site and publishes it to GitHub Pages on every push to `main`

Build locally:

```bash
pip install -r requirements.txt
mkdocs serve
```

Linda Angulo Lopez, November 2026. Written with the help of Claude (Anthropic). Source data keep their own licences; see `docs/sources.md`.
