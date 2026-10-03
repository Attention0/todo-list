# Fertility Geography Project — Project Status

## Executive finding

The active empirical project is at `/home/liuze/project-cmds_fertility`. The corrected build dated 2026-09-14 supports a province-level retrospective fertility event study for 21,383 cross-province work/business migrant women surveyed in CMDS 2013–2017. It does **not** create a true panel, a stayer comparison, or a complete residence history.

The defensible current object is annual birth history in a balanced `r=-5,...,+5` window around reported arrival in the current destination, interacted with a destination-minus-hukou-origin province crude-birth-rate gap. Marriage timing is usable only for 2013–2016. A city treatment is not ready: only the 4,819 women from 2017 have usable origin city/county detail.

## Evidence and project map

| Area | Location | Role |
|---|---|---|
| Project overview | external `README.md` | Current build decisions |
| Base construction | `code/rebuild_main_base_fixed.py` | Current 2012–2018 woman-level base |
| Panel construction | `code/build_main_panel_40cols.py` | Retrospective annual expansion |
| Revision workflow | `work/revision_20260914/` | Corrected build, verification, final export |
| Survey evidence | `work/audit_20260914/` | Questionnaires, metadata, diagnostics |
| Corrected base | `output/data_revision_20260914/cmds_2012_2018_mother_base_variables_FIXED.*` | 507,225 women × 215 columns |
| General panel | `output/data_revision_20260914/cmds_2012_2018_mother_year_panel_MAIN40.csv` | 8,733,782 rows × 47 columns |
| Final files | `output/data_revision_20260914/final_analysis/` | 21,383 women; 235,213 woman-years |
| Existing analyses | `output/phase_reports/`, `strict_aer/`, `marriage_fertility_geography/`, `province_exact_year_exploration/` | Mixed vintages; verify inputs before use |

Older root data/caches and many historical reports predate the 2026-09-14 spouse and 2017 fertility revisions. Do not mix them with revised inputs.

## Survey waves

| Year | Base women | Final sample | Decision / limitation |
|---:|---:|---:|---|
| 2009 | outside base | 0 | Current marriage and outside-hukou birth experience exist, but no first-marriage date or complete child dates |
| 2010–2011 | outside base | 0 | Excluded; no comparable current-move reason |
| 2012 | 74,380 | 0 | No question comparable to later current-move reason |
| 2013 | 92,067 | 4,666 | Included |
| 2014 | 7,200 | 363 | Included; raw wave is small |
| 2015 | 96,692 | 4,721 | Included |
| 2016 | 80,912 | 6,814 | Included; migration count available |
| 2017 | 82,118 | 4,819 | Included; city origin available, marriage date absent, fertility roster-derived |
| 2018 | 73,856 | 0 | Required origin unavailable |

## Current corrected artifacts and decisions

- Final women: 21,383 × 103; final balanced panel: 235,213 × 63, exactly 11 rows per woman.
- Move years 2003–2012; event calendar years 1998–2017; 31 origin and destination provinces; zero stayers.
- Spouses are located in roster slots 2–10 using relationship code 2; 1,032 unique spouses are outside slot 2.
- In 2017, 24,152 base women with no listed child are assigned zero children under an explicit roster assumption; provenance is retained.
- `direct_move` is a proxy, not proof of one move.
- Revised data reproduce the short-run estimate: +2.862 percentage points per 10‰ higher destination-origin pre-move CBR gap (SE 0.844 pp, p=0.00196).

## Status

Province-level retrospective fertility analysis is operational with major identification caveats. Marriage-event, city-treatment, full multiple-move, and mechanism analyses remain incomplete. Historical reports should be treated as provisional until rebuilt from the revised final files.
