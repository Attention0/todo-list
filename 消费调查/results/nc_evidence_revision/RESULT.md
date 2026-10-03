# NC evidence revision result

## Summary

Executed the bounded reviewer-driven plan on the original data, then rewrote the manuscript and supplement from the results. Primary adults5480, full5497 historical bridge. Scientific content is stronger through corrected inference, direct diagnostic comparisons and explicit uncertainty, but a robust form-by-amount mechanism is not established and NC acceptance is not claimed.

Adult Top75 omnibus rawP=.009025, Holm21=.180508, jointminP=.082092. Cash–Medical raw=.003773, Holm=.079229, minP=.039096; Cash–Food Holm=.223668, minP=.105489. Both Bonferroni21 scalar intervals include zero. Old1500 same-grid df-normalized focalminP=.369926 versus maxnorm=.413717. The original maximum came fromdf4 in4949/5000 draws. Medical and amount marginal effects are more secure. Food's5000 point crossover is uncertain. Bindingness triple raw=.008396/Holm7=.050373 requires withdrawal of mechanism-exclusion claims. Q1/Q2 direct pass/fail tests do not show effect disappearance. Calibration runs, but ESS315 uncapped/1191 normalized-cap10 precludes a representativeness claim.

## Files changed

- 消费调查/SPEC.md and WORK.md: current authorized scope and pre-result finite plan, historical instructions retained.
- 消费调查/results/nc_evidence_revision/: freeze, analysis/calibration/simulation/figure/document/verification code; aggregate tables; original-family diagnostics; census transcription; metadata checks; documentation.
- 消费调查/manuscript/nc_v5/: rewritten manuscript and supplement Word files; editable text;3 main and2 supplemental figures inPNG/PDF/SVG; structured M1–M7 memo; NC benchmark; author-information checklist; source/reference manifests.
- No raw data, respondent records, original manuscripts or historical analysis outputs changed. Untracked Python caches outside the new directories are not included in publication.

## Key implementation decisions

The post hoc plan was committed atac4e7cb before new estimates. No Bayesian rescue, new outcome threshold, sample tuning, income mapping, moderator mining or claimed replication. Twenty-one scientific interaction tests are distinct from descriptive model/sample sensitivity. Holm is retained beside jointminP, which uses a centered unrestricted-estimator influence law with HC3 covariance. Seven direct diagnostic tests retain all lower-order interactions and shareHolm7. Relative-scale prediction has no1% gate. Q1/Q2 are response-style sensitivity populations. Census counts come from the official adult-compatible table with exact18/19-year counts; no fabricated benchmarks. Final normalized weight cap10 is enforced explicitly and target imbalance reported. No median-specification inference across changing sample targets.

## Testing performed

- Independent individual-row statsmodels recovery of all7 coefficients/HC3 covariances: maximum discrepancies below6e−16/4e−17.
- Historical focal nominalP and all1500 original maxnorm adjustedP values reproduced.
- Three fixed simulation DGPs ×1000 complete estimator/covariance refits,999 joint calibration draws each; zero failed refits. MinP FWER=.055/.053/.041, exact intervals reported. No claim of broad or exact finite-sample validity.
- All50 training-fold logistic fits converged.
-58 package checks passed: family counts/Holm arithmetic, interval/P algebra, independently derived saturated cell means and HC3 variance, disjoint-subgroup triple contrast algebra, target matching/cap diagnostics, frozen hash, numerical sources, aggregate-column privacy, figure order and document title style/tokens.
- Word visual rendering and layout checks recorded in VISUAL_QA.md. Packaged renderer failed due absent LibreOffice; installed Microsoft Word exported PDFs in hidden read-only mode, bundled Poppler generated page images.
- Bibliographic metadata:23 current Crossref successes,7HTTP429 failures recorded. Supplementary publisher checks and previous metadata are explicitly distinguished. Metadata review is not full-text validation.

## Acceptance Criteria

Finite feasible analyses and manuscript rewrite completed. Original inputs preserved; aggregate outputs reproducible; scientific and historical evidence distinguished; figure numbering and requested colors corrected; source-linked statistics and direct response memo delivered. No author-required fact was fabricated. No claim of submission readiness or confirmed mechanism. Publication to branch/PR only; no merge.

## Known issues

Ethics/consent/minor coverage, actual recruitment and field dates, prospective sample-size/stopping information, author contributions/funding and durable archival/access policy require author evidence. Platform appendix only establishes background-field provenance. Census adjustment cannot repair sparse support, missing older ages or nonprobability selection. Hypothetical responses and bundled form attributes remain design limits. Interaction conclusions remain method-sensitive after correction. Three simulated DGPs are not exhaustive. Crossref refresh failures are preserved in reference_checks_v5.csv.

## Branch

feature/nc-evidence-revision, stacked on feature/nc-revision-audit (PR15); no merge.

## Commit SHA

Plan commit: ac4e7cb. Delivery commit and PR are recorded after successful native publication.

## PR

Pending native push and PR creation; this line is replaced only after confirmed success.
