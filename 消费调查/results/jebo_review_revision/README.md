# JEBO reviewer revision replication

Base: PR17, commit `926b05022189661bdfe4dc41d24ad900c77bbd12`.
Protocol was committed first as `0aa5681e2ceb148759b0f01a74db726bc464f6e5`.
The immutable manifest fixes the samples, outcomes, mappings, tests, bootstrap
draw counts and seeds. This is a post-results reviewer plan, not preregistration.

## Inputs and runtime

Run from the repository root with Python and the packages in `requirements.txt`.
`software_versions.json` records the executed versions. Keep historical
`mpc_size_curve`, `nc_revision_audit`, `nc_evidence_revision` and
`jebo_transition` directories available; they supply the inherited preparation
and frozen estimates. The original Stata file and integrated questionnaire are
private external inputs; no respondent records are committed here.

The raw file must have SHA256
`16996c88fdd20f5084b62a8503a8eec1d4c6ec7caff489eff109500f629694fe`.
Use single-thread BLAS (`OPENBLAS_NUM_THREADS=1`, `OMP_NUM_THREADS=1`) for the
recorded numerical run. Scripts reject the wrong raw file.

## Ordered execution

1. Preserve/commit the manifest and issue matrix before calculations.
2. Run `audit_inputs.py --data <raw.dta> --questionnaire <original.docx>`.
   This writes the questionnaire gate and verifies the adult source and metadata.
3. Run `analyze_core.py --data <raw.dta>` (adult cells, yuan, affine, 42 tests).
4. After reviewing `QUESTION_INTERVAL_AUDIT.md`, run `analyze_interval.py`.
   It reads only aggregate cells and writes all 8,000 draw-level statuses.
5. Run `analyze_food.py --data <raw.dta>` then `analyze_precision.py`.
6. Run `prepare_assets.py --data <raw.dta>`, `build_reference_audit.py`,
   `build_manuscripts.py`, `build_response.py`, then `build_docx.py`.
7. Run `verify_revision.py --data <raw.dta>`; all checks must pass.
8. Render both Word documents and inspect every page. `render_word.ps1` uses
   a separate hidden Word instance when the preferred LibreOffice renderer is
   unavailable. PDF/page-image QA files are ignored, not publication outputs.

The literature audit records a bounded primary-source verification, with access
limitations explicit. Regeneration does not perform a fresh literature search.
Do not regenerate the historical files or redefine the protocol to fit results.

## Interpretation boundaries

Midpoint-implied yuan is a coding-dependent transform of a hypothetical answer.
Affine intercepts extrapolate outside the three randomized amounts. Interval
models are censored latent-normal sensitivities; their calibration failures
prevent a coding-robust structural MPC interpretation. Joint min-P42 is a
centered Gaussian asymptotic procedure using p-value normalization across
degrees of freedom, not exact randomization inference. Continuous Food
moderators are observational. Nonrejection does not establish equality.

Final paper files, figures, aggregate source data and response letter are under
`../../manuscript/jebo_v3/`. See `RESULT.md` and `FINAL_AUDIT.md` for delivery.
