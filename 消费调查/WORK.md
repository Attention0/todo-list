# 消费调查项目 — CURRENT WORK INSTRUCTIONS

## Current execution plan 2026-10-03

This section supersedes all old instructions below. The user explicitly authorizes actual analysis and subsequent manuscript revision, with an NC target. New output only results/nc_evidence_revision/ and manuscript/nc_v5/. Branch feature/nc-evidence-revision is stacked on PR15 and includes latest main. Historical packages unchanged.

1. Read v4, original questionnaire/data, PR3–15 results and reviewer critiques; benchmark NC official requirements and actual related articles. Commit this plan and freeze.json before new estimates; this is post hoc, not preregistration.
2. Primary adultA, fullR historical bridge. Reproduce focal results; construct nine-cell distributions, equal-weight factorial marginal effects and amount-specific form contrasts. Never choose sample by significance.
3. Scientific family: 7 outcomes × omnibus/Cash–Food/Cash–Medical, z=-1/0/1, OLS/LPM HC3 =21 tests. Holm21 mandatory; centered unrestricted-estimator influence Gaussian min-P B10000 supplementary. Use full residual covariance rather than legacy constrained-null covariance to estimate the joint centered estimation-error law; asymptotic, not exact randomization inference. Scalar simultaneous Bonferroni21 and pointwise95%CI. Old1500 grid receives df-normalized same-grid min-P diagnostic only, retaining its incompatible-null/scale caveats.
4. Validate with3 fixed multinomial DGPs ×1000 full estimator/covariance refits: pooled zero effects; additive category-probability main effects; partial null with Food interaction only between intermediate categories so Top75 remains null.999 Gaussian calibration draws per simulation. Report true-null FWER, binomial CI, power on false hypotheses, failures. No tuning after seeing results.
5. Top75 marginal main-effect family6: form/amount omnibus and2reference contrasts each; Holm6. Cell form contrasts6: Food/Medical−Cash at3amounts; Holm6. Seven-outcome full descriptive appendix. Existing relative-scale/endpoint results reused, no new thresholds.
6. Exactly7 mechanism/selection tests, adultTop75, Holm7: log-income ABS income-coefficients=0 (3df), REL amount+income coefficients=0 (3df), form×logamount×logincome (2df); fixed inframarginal Food×z×G (1df); decomposed ratio's opposite-coefficient restriction (1df); Q1/Q2 pass×form×z (2df each). All lower-order terms retained. G=food_lower6>5000; complement is not confirmed binding. M1 mapping primary, oldM2 descriptive sensitivity only. Report subgroup estimates/CI.
7. Five prediction models: additive, ABS, REL, unrestricted amount+income, triple. AdultA, original cell-stratified5fold seed20261003, M1/M2 only. Report raw/relative loss and fold differences; no individual-independent loss CI or1% pass/fail mechanism gate.
8. Existing specification curves only, scales separated. Top75 LPM endpoint-equivalent contrasts across5samples×3representations are descriptive. Omit prior memo's inferential median-of-specifications test before results: selected samples have different estimands, not independent replications.
9. Bounded official2020 age×education calibration attempt. Match18+ and q43 labels; no invented age split or benchmark. Joint poststratification if possible, marginal raking labelled if only marginals. Top75 A, cap10 plus uncapped sensitivity, ESS/balance/max weight. Incompatible source/support → explicit not feasible, no stand-in numbers.
10. Independent statsmodels and contrast algebra, frozen inputs, interval/P consistency and aggregate privacy checks. Review plots. No new estimand after results; log bugs before fixing.
11. Rewrite v4→v5 from actual outputs: economic question→levels→interaction/distribution→sensitivity→limits. Remove unsupported mechanism, individual fungibility, universality and realized-MPC claims; retain interesting supported facts. Correct internal language, positive-control naming, Q1/Q2 definitions, figure sequence and light-to-dark Fig1. Preserve source v4; author-only missing ethics/recruitment remains explicit.
12. Deliver v5 Word, supplement, reviewer response/change map, NC benchmark note, aggregate source tables/figures/code and RESULT. Render and inspect every final Word page. Native git add/commit/push first, connector on credentials failure, GUI last; PR without merge. Record exact SHA/PR; never publish raw/respondent/OOF data.

Stop after these finite packages irrespective of significance; evaluate NC readiness honestly. No new moderator/HTE/SHAP/latent search, thresholds, income mappings, sample tuning, Bayesian rescue, or false independent replication. Missing author documentation cannot be inferred.

## Historical execution brief retained for provenance

## Current phase: NHB reviewer-driven claim validation and re-analysis

This file supersedes the previous initial-audit execution brief.

Read, in this order:

1. `消费调查/SPEC.md` — project background and evidence discipline.
2. `消费调查/NHB_REVIEW_REANALYSIS.md` — **the binding execution protocol for the current round**.

Then locate the existing survey data, questionnaire/codebook, current manuscript-analysis scripts, and existing results in the Work environment and execute the protocol.

### Critical instruction

Do **not** begin by editing the manuscript.

The first objective is to determine whether the current “limited cross-context portability” interpretation survives:
- a proper within-context benchmark;
- target-normalized portability comparisons;
- direct X×transfer-form invariance tests;
- adult-only / clean-sample robustness;
- food-voucher inframarginality analysis;
- corrected HTE validation and inference.

Reviewer-provided numerical claims are **not data**. Independently reproduce or reject them using the raw data and code.

### Required return path

Commit code and aggregate outputs to:

`消费调查/results/nhb_reanalysis/`

Never commit respondent-level raw data or sensitive identifiers.

The final substantive decision must be one of the empirical patterns defined in `NHB_REVIEW_REANALYSIS.md`:
- A: broad non-portability;
- B: boundary condition (cash-food relatively stable, medical different);
- C: low predictability without strong evidence of remapping;
- D: unresolved / specification-sensitive.

Only after that decision should Chat revise the NHB manuscript.
