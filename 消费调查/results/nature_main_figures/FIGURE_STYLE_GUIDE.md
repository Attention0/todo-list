# Unified figure style

All four main and six extended figures are180mm wide, white-background vector PDF/SVG and600dpi PNG. Main heights78/78/78/87mm; extended heights76/117/143/78/93/118mm. Combined PDF retains exact original page dimensions and vector objects. SVG uses editable text (`svg.fonttype=none`); PDF embeds TrueType text (`pdf.fonttype=42`). Arial is the available preferred font; fallbacks Liberation Sans/DejaVu Sans.

Final-size typography: axis/subtitles8-8.5pt, ticks/legend7pt, panel letters10pt bold, sparse annotations6.7-7.5pt. No giant embedded figure titles, boxes, stars, shadows or gradients. Remove top/right spines;0.6pt axis edges, very faint horizontal guide lines. Wide main layouts are intended at180mm. QA provides89-90mm reduction previews; the1×3 centerpiece and dense multi-panel extended figures should **not** be printed as single-column thumbnails. Reduction previews do not promise3-4pt print text is readable.

Palette and treatment grammar are fixed:

| Representation | Color | Marker / line |
| --- | --- | --- |
| Cash | #1F4E79 | filled circle,1.6pt solid |
| Food | #2A9D8F | filled square,1.15pt solid |
| Medical | #D97757 | filled triangle,1.15pt solid |
| Restricted | #7564A3 | hollow diamond,1.15pt dashed |
| Reference / observables | #7A7A7A | neutral only |

Restricted is always a derived equal-weight contrast. Do not invent a fourth treatment color/legend category without that qualifier. Grayscale access relies on marker shape, line dash and filled/open glyphs, not color alone. No CVD-simulation dependency was available; grayscale proofs and redundant encoding are checked without claiming a color-vision simulation passed.

Discrete amounts appear as¥200/¥1,000/¥5,000 at evenly spaced positions (fivefold/log spacing). Connect only observed randomized doses. Probability/share ticks are percentages; ordinal is mean response category, not cardinal MPC. Main share axis starts0; ordinal starts at its valid lower bound1, with mean-display range1-4 (individual scale remains1-6); no magnified narrow-range inset. Probability plot ranges are0-18% (Top75),0-35% (midpoint),0-100% (any spending), explicitly different outcomes. Figure1 panels have identical amount alignment and treatment grammar, not identical incompatible y-units.

Use only approved pointwise95% intervals, thin0.65pt error bars with1.7pt caps. Never bootstrap/re-fit/recompute inferential procedures in the visualization script. Arithmetic ordinal endpoints reproduce the already approved PR9 mean±1.96SE convention. Other approved intervals are copied, never recomputed from midpoint values. Grey gap segments have no CI interpretation.

Figure4 deliberately uses the workplan's compact family-minimum-q alternative: per-SD numeric effects, category differences and multi-df omnibus tests are not scientifically commensurate effect rankings. Six corrected minima, full q rugs and four-group counts preserve the decisive corrected-screen information without raw-p-value storytelling. Detailed approved coefficient/omnibus display stays in Extended Data6, all900 primary rows remain in source. No equating non-rejection with zero effects.

Editing workflow: change presentation parameters in `plot_figures.py`, regenerate exports, run fidelity/vector/size/privacy tests, render final PDFs with Poppler, inspect all main/extended renderings/contact sheet/grayscale proof. Do not modify upstream approved CSVs or manuscript. `source_manifest.json` records exact local aggregate-input hashes and commits; row mapping in `plot_statistic_audit.csv` uses1-based data rows (header excluded). Cross-platform text hashes may differ with line-ending serialization; numerical-source equality remains the operative fidelity check.
