# Reproducing the bounded NC evidence revision

This is a post hoc evidence repair, not a preregistered study. Read freeze.json and the current sections of ../../SPEC.md and ../../WORK.md. The plan was committed before the new estimates; previous analyses remain unchanged. Primary sample: adults, N=5480. Full N=5497 supplies historical bridge results only.

From repository root, with Python and the packages in requirements.txt:

```text
python 消费调查/results/nc_evidence_revision/analyze.py --data <authorized_raw.dta> --part core
python 消费调查/results/nc_evidence_revision/analyze.py --data <authorized_raw.dta> --part simulation
python 消费调查/results/nc_evidence_revision/analyze.py --data <authorized_raw.dta> --part legacy
python 消费调查/results/nc_evidence_revision/calibrate.py --data <authorized_raw.dta>
python 消费调查/results/nc_evidence_revision/figures.py
python 消费调查/results/nc_evidence_revision/build_documents.py
python 消费调查/results/nc_evidence_revision/verify_package.py
```

The raw file hash is checked by analyze.py. Raw data and original questionnaire/manuscripts require authorized author access and are not bundled. No ID, row-level response or individual fold export is written. Core preparation is inherited from ../mpc_size_curve/size_curve.py, covariates from ../nc_revision_audit/secondary.py and grid definitions from ../nc_revision_audit/grid_models.py. Those historical files are not modified.

The new joint min-P uses a Gaussian approximation to the unrestricted centered estimator influence distribution with HC3 covariance. It is not exact randomization inference. Simulation scenarios, seeds and draw counts are explicit. Local families are 21 interaction tests, 6 first-order Top75 tests, 6 amount-specific form contrasts, 7 diagnostics and 3 tests within each calibration sensitivity. They do not collectively promise whole-paper FWER protection; no secondary discovery replaces the focal interaction.

Census target counts are manually transcribed from the official NBS image, accessed2026-10-03. Target groups and education labels were checked before using response values. Normalized cap10 is enforced through min(lambda*w,10), not clipping before renormalization; it cannot also match all target cells. See calibration_diagnostics.csv and bug_log.md.

Plots contain pointwise uncertainty unless labelled Bonferroni. The descriptive specification display uses the same endpoint probability estimand, with overlapping samples. Documentary references are remapped to first citation order. reference_check.py optionally refreshes Crossref metadata and accepts HTTPS_PROXY from the environment; retrieval failures are recorded, never silently marked verified. Metadata retrieval is not full-text claim verification.

Word files are in ../../manuscript/nc_v5/. Packaged LibreOffice rendering was attempted and failed because it is absent; final visual QA uses installed Word export and bundled Poppler. QA intermediates are ignored by Git. Author ethics/recruitment/contribution/funding information remains unresolved. No further exploratory models are authorized by this package.
