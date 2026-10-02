# Figure audit

## Authority and scope

Complete701-line `NATURE_FIGURES_WORK.md` read with SPEC/WORK and approved PR9/10/12 legends/results. Current visualization-only request supersedes stale WORK routing to NHB re-analysis. New `feature/nature-main-figures` is based on PR12 aa449de, with latest main6867cac task merged. No estimator, raw-data or prior analysis script import; `plot_figures.py` reads only eleven existing aggregate CSVs. No manuscript, outcome, sample, estimand, coefficient, interval, correction family or substantive headline changed.

## Statistical traceability

`source_manifest.json` records exact local input byte hashes and source commits. `plot_statistic_audit.csv` maps figure/panel/outcome/form/amount/X to approved file and1-based data row (header excluded); source CSVs retain individual approved result fields. Unsupported X records are retained as context with status, not plotted effects. Source maps may also contain preserved contextual rows not individually drawn; no respondent-level data are read/exported.

| Figure | Approved source and definition |
| --- | --- |
| Main1A | PR9 `mpc_size_curve/fig1_source.csv`, ordinal_mean±1.96ordinal_se, original approved mean-CI convention |
| Main1B/C | PR10 `mpc_final_strengthening/figA_source.csv`, midpoint/top75 estimate/lo/hi; N from corresponding PR9 nine-cell summaries |
| Main2 | PR10 figA, Cash and Restricted; Restricted estimate=.5Food+.5Medical, existing mixture bootstrap CI copied unchanged |
| Main3A/B | PR9 fig3 any_spending probability/lo/hi; PR10 figA top75. Different approved interval conventions disclosed, no silent harmonizing inference |
| Main4 | PR12 all_screen_results (900 primary tests, including24 unsupported rows), family_summary six min_q, subjective_objective_summary full group counts |
| ED1 | PR10 figB, five existing RC threshold differential slopes with approved covariance-based intervals |
| ED2 | PR10 figC, all21 within/between absolute/relative scale results; null0/1 and log ratio axes |
| ED3 | PR10 figD,60 comparable results in fixed sample/adjustment/amount representation order; no outcome-based specification sorting |
| ED4 | PR10 figE, all12 form/derived rows; midpoint and implied_yuan, same approved intervals |
| ED5 / Figure S | PR9 fig2, all nine cells' p1-p6; unconditional composition, no newly estimated uncertainty |
| ED6 | PR12 all_screen_results primary rows; numeric effects and factor omnibus distinguished. Raw p neutral, no new rejection thresholds |

Six main-data sources, five ED sources plus family-minimum supplement and one audit table =13 CSVs. CI arithmetic in Main1A is presentation of PR9's existing convention, not a new CI method. Grey gap segments indicate differences between existing means only, not pseudo gap CIs. Figure4 deliberately uses the workplan's allowed compact alternative; categorical omnibus effects cannot be silently standardized into scalar interactions. No discovery counts are reinterpreted as independent replications.

## Executed checks

`verification_results.json`: **231 assertions passed**, including unchanged eleven input hashes, row-wise values/interval/N checks, equal-weight mixture identity, all900 X rows/24 inference failures, all six original family minima, exact ED schemas and numerics, nine six-bin compositions, vector/no-image PDFs, editable-text SVGs,180mm page size/600dpi PNG, combined-vector-page identity, source-row/commit mapping and aggregate-only schema. Plot exports separately enforce exact on-page tight bounds before save. Failed initial relative-scale role/expected yuan row-count assumptions were corrected to match the existing source schema, not by altering source data/results.

All ten final PNGs inspected; eleven PDFs rendered by Poppler (ten single pages plus four combined pages =14 page proofs), reviewed as individual figure proofs and combined-page proof. Visual QA checked labels/legend/CI clarity, no clipping, treatment order/colors/marker consistency, panel alignment, clean full-width typesetting and equal-width contact sheet. Page-edge panel letters and duplicate q-threshold annotation were repaired; no statistical numbers changed. Final ED1 top margin increased and strict on-page bound check passed.

Grayscale contact sheet inspected: Cash/Food/Medical retain distinct circle/square/triangle grammar; Restricted retains hollow diamond and dashed line.89-90mm reduction proofs retained locally for review, not promised as publication-ready multi-panel single-column layouts. CVD simulation unavailable/not executed; no false test claim. Temporary proofs reside in ignored `qa/`; publication exports/contact sheet are committed. Font/spacing/palette/ranges and reduction caution are specified in FIGURE_STYLE_GUIDE.md. PDF skill influenced vector exports, full-page rendering and final proof inspection.

## Reproduce

With the existing Python environment containing numpy/pandas/matplotlib/Pillow/pypdf and Poppler on PATH:

    python plot_figures.py
    python verify_figures.py

No raw-data path, model fitting, bootstrap, internet request, manuscript access or tuning step. Frozen upstream aggregate files are the inputs; hash checks prevent unnoticed changes. Arial available locally; fallback font changes must trigger fresh visual review. Byte hashes refer to local working-copy serialization; Git line-ending normalization may change text byte hashes across platforms, while all numerical equality checks remain applicable.

## Claim discipline / final decision

Four main figures communicate descriptive form-size profiles, attenuating Cash-restricted gaps, visually salient tail compression and lack of a corrected observable signature. They do not establish an ordinal mean-law, equivalence, causal mechanism, tail-specificity, realized spending, theory violation or within-person change. Prior PR10 judgment remains suggestive; PR12 correction/null limitations remain intact. No further empirical analysis performed or requested by this package. New stacked PR, no automatic merge.
