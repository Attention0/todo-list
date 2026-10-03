# Hero-figure audit

## Scope and freeze

Presentation-only follow-up to PR #9–#13, based directly on PR #13 branch commit `167ccbd993826991d43ae3d27880913a8cfe674b`; latest `origin/main` checked at `6867cac8c61a3d084e42f7885d0c39336bc5b8f9`. New branch `feature/mpc-hero-figure`, stacked on `feature/nature-main-figures`. No manuscript, prior result, estimand, respondent sample or empirical code changed. No raw respondent data accessed. No new tests, bootstrap, smoothing, moderators or latent traits.

Only two aggregate files are read:

- `消费调查/results/nature_main_figures/figureS_distribution_source.csv` (nine cells, original PR #9 six-bin probabilities).
- `消费调查/results/nature_main_figures/figure1_main_source.csv` (only nine approved midpoint rows, original PR #10 means/95% CIs).

Their exact SHA-256 hashes are in `source_manifest.json`; before/after rendering hashes are identical. Every plotted value has local and upstream source-file/data-row/commit provenance in the two source CSVs. Row numbers exclude the header. Hero source has 54 bin-share rows and nine midpoint/CI rows; companion has 18 differences, each retaining both endpoint probabilities, source rows and cell N. No respondent-level output.

## Numerical fidelity

Atlas strips have identical physical length; six segment widths are the unmodified unconditional approved shares. No normalization, minimum-width inflation or rescaling of a tail. All nine strips sum to one within floating-point tolerance. Bin1 is the full original “basically no additional spending” category; legend wording is abbreviated, not a recode. Mean coding remains `[0,.05,.175,.375,.625,.875]`. Its weighted-bin consistency is verified but means and CIs are copied, not re-estimated. CIs are approved pointwise 95% percentile intervals from PR #10's 5,000 stratified bootstrap resamples.

Approved Cash tail endpoints: 0.1340872374798061 / 0.0530821917808219, rounded only for the 13.4% / 5.3% annotation. Cash no-spending endpoints: 0.2730210016155089 / 0.2722602739726027. Fingerprint is exactly `100 × (p_bin,5000 − p_bin,200)`; each form's six differences sum to zero. Top75 differences: Cash −8.10050456989842 pp; Food −2.45977036371704 pp; Medical −1.92820984813622 pp. Cash no-spending difference −0.07607276429062 pp. No bin-difference CIs exist in the frozen source, so none are invented. Stem length is difference magnitude, not uncertainty.

## Visual decisions

Hero: 180 × 138 mm, panel A 3×3 response atlas plus a single six-bin intensity legend; panel B common-axis midpoint summary. Amount centers align precisely across A/B. The top's neutral-to-navy six **discrete** shades express MPC intensity, not treatment identity; the darkest >75% bin is always rightmost. Treatment colors/marker shapes are confined to B and match PR #13 (Cash navy circle, Food teal square, Medical terracotta triangle). No huge title, decorative gradient, star or inference badge. Midpoint axis starts at zero and spans 0–35%, consistent with prior approved main figures. Only observed amounts are joined; no continuous fitted curve.

Companion: 180 × 79 mm, three aligned form panels, common −10 to +6 percentage-point range, zero line, same bin shades. “None” is explicitly defined in its caption. No individual movement, Sankey/alluvial or mass-flow inference. The optional puzzle figure is deliberately not duplicated: PR #13 Figure2 already supplies the approved Cash/derived-Restricted comparison, and these two new figures have distinct distribution-focused jobs.

White background; Arial at final size; editable SVG text, embedded PDF font/vector objects; PNG 600 dpi. Panel system and summary grammar match PR #13. Atlas encodes intensity redundantly by order and lightness; summary adds marker shapes. Full-width typesetting at 180 mm is recommended. An 89 mm preview was inspected, but is not a claim that the entire atlas/three-panel fingerprint is suitable at single-column print size. No color-vision simulation dependency was available; grayscale checks were performed, not a claimed CVD-simulation test.

## Verification actually performed

- Ran `plot_hero.py` successfully; strict on-page content bounding-box checks passed for both exports.
- Ran `verify_hero.py`: **423 checks passed**, including every bin/mean/CI/N/provenance identity, zero-sum arithmetic, frozen source hashes, coding consistency, privacy/import safeguards, PDF dimensions, vector content, editable SVG and 600 dpi metadata. Recorded in `verification_results.json`.
- PDF dimension serialization uses a 1e−7 mm tolerance, while numeric-source checks use absolute 1e−14 tolerance. An initial dimension check was too strict for PDF decimal serialization and was corrected; no statistical values changed.
- Rendered both final PDF pages using Poppler, inspected them and both final PNGs. Confirmed no clipping, overlapping legend/text or hidden uncertainty. Corrected the fingerprint's first-bin label to “None” after the initial long label crowded its neighbor.
- Inspected final grayscale proofs and reduced-width previews. Tail order/intensity and curve marker identity remain distinguishable. QA renders/previews are locally retained in ignored `qa/`, not submitted as extra scientific figures.

## Claim boundaries

This displays a descriptive difference in the form-specific size profiles. The Cash endpoint high-tail compression is conspicuous, not proof that all changes are uniquely concentrated above75%. Frozen multiplicity-adjusted cross-threshold tests do not establish exclusive tail-specificity. Mean/ordinal differential-slope interpretation remains suggestive, not upgraded to a universal law. Bin probability changes are between independent randomized cells, never individual transitions or causal mediation. Hypothetical stated MPC is not realized spending. The original ordinal representation must remain in the paper's evidence package.

## Reproduction

Use the same Python environment as PR #13 with numpy/pandas/matplotlib/Pillow/pypdf and Arial available. Run `plot_hero.py`, then `verify_hero.py`. Use Poppler to render the resulting PDFs for visual inspection. Both scripts resolve inputs relative to their location, not the working directory. Regeneration reads aggregate sources only. Review any changed upstream hashes before accepting a changed freeze.
