# 消费调查项目 — CURRENT WORK INSTRUCTIONS

## Current phase: NHB round-2 reviewer closure

The core empirical story has already been rebuilt. This round is **not** a new exploration round.

Read, in this order:

1. `消费调查/SPEC.md`
2. `消费调查/NHB_REVIEW_REANALYSIS.md`
3. `消费调查/NHB_FINAL_VERIFICATION.md`
4. `消费调查/NHB_ROUND2_REVIEW_WORK.md` — **binding protocol for the current round**

Then locate the raw survey data, questionnaire/codebook, existing NHB analysis scripts and prior aggregate results.

### Core story that must not be changed by default

> Transfer form can shift average stated spending without generating a clearly identifiable set of responders or broadly remapping observable individual differences.

The current round closes reviewer questions around:
- full mean-effect/ordinal robustness;
- food-voucher bindingness and wording sensitivity;
- model-family robustness, feature ablation and learning curves;
- complete six-direction target-normalized portability uncertainty;
- equal-training-size remapping tests;
- direct Food and Medical HTE validation;
- HTE detectability simulations;
- medical-spending/bindingness and floor-effect checks.

Do **not** open broad moderator searches, SHAP fishing, new policy exercises, or new manuscript stories.

### Required return path

Write code and aggregate outputs to:

`消费调查/results/nhb_round2/`

Do not commit respondent-level raw data, identifiers, respondent-level predictions or bootstrap samples.

After finishing, update:
- `ROUND2_RESULTS.md`
- `ROUND2_AUDIT.md`
- `ROUND2_MANUSCRIPT_NOTES.md`

Then stop analysis expansion and report whether the current headline should be strengthened, unchanged or weakened.
