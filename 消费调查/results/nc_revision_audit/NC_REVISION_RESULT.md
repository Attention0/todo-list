# NC revision evidence audit — decision memo

Date: 2026-10-03. All findings concern hypothetical stated additional total spending, not realized expenditure. This revision-stage finite family follows the saved manifest; neither the original study nor the accumulated story was preregistered. No manuscript text was changed.

## Eight required answers

1. **Global correction: NO.** R Top75 three-form equal-slope Wald=9.6480 (2 df), raw P=.00803447, global max-T P=.41371726. Cash−Food=-2.81935 pp per fivefold increase, 95% CI [-5.09262,-0.54608], raw P=.0150645, global P=.88062388. Cash−Medical=-3.08952 pp, CI [-5.12198,-1.05705], raw P=.00288847, global P=.51009798. These are pointwise, not simultaneous, CIs. See full focal table below. No scalar CI exists for the omnibus; its two-component estimate/CI vector is in the CSV.
2. **Separate forms:** Cash Top75 slope=-4.05460 pp; Food=-1.23524 pp; Medical=-.96508 pp per fivefold. Cash has the largest observed upper-tail compression. Midpoint and ordinal form profiles below show the mean pattern separately. Food and Medical cannot be asserted identical: their slope contrast P=.790906 is not equivalence. No fourth randomized Restricted arm exists.
3. **Simple bindingness: incomplete, not supported as a sufficient explanation.** Conditional on amount, Food−Cash log-r Top75 gradient=+.0196842 (CI [.0060452,.0333232]), raw P=.0046733, Holm across 75 C tests=.322456. Thus observed Cash−Food gap declines, rather than increases, with this baseline-dependent ratio. This is an association, not a causal ratio effect. Fixed strictly inframarginal sample n=2815: Food−Cash slope difference=+.0123031 (CI [-.0144757,.0390818], P=.3679); pooled equal-amount level difference=-.0117278 (CI [-.0328810,.0094253], P=.2772). The slope mechanism remains unresolved; a non-significant level is not equivalence.
4. **Relative-scale categorization: unsupported by the focal prediction comparison; direct process evidence NOT FEASIBLE.** R Top75 REL improvements are .1601%, .1114%, .0328% (M1/M2/rank), all below the revision-stage 1% criterion and all paired loss CIs include zero. Secondary ordinal/midpoint improvements are also below 1%. These do not establish income-based collapse. Questionnaire has no intended-use, planning-horizon, spendability or earmarking process response. Scale-dependent categorization remains a Discussion hypothesis only.
5. **Broadly shared tendency: cannot claim.** Four theory moderators × three outcomes × three targets: no Holm-36 rejection. Top75 Cash-slope 80% MDE is about 2.48–2.93 pp/1SD; Cash−Food differential MDE 3.34–3.88 pp exceeds the average 2.82 pp contrast; Cash−Medical MDE 3.08–3.59 pp is comparable to/exceeds its 3.09 pp contrast. The design cannot rule out moderation on the scale of the average interaction. Normal-design MDE uses actual HC3 uncertainty, not a simulated exact power guarantee.
6. **Positive controls: MIXED.** Cash size gradient is negative and survives Holm-9 for Top75. Higher fundraising capacity predicts lower Top75, raw P=.02097 but Holm P=.06291. Income rank predicts *higher* Top75 (estimate +.0240527, CI [.0097183,.0383871], Holm P=.006036), opposite the frozen expected sign. Income is not liquid wealth and the literature direction is not universal. This is limited construct-validity evidence, never validation of stated as realized MPC.
7. **Quality/weighting:** same-signed Cash−Food/Cash−Medical contrasts across R/A/C/Q1/Q2; omnibus raw P=.00803/.00903/.00364/.15392/.41061; global P=.41372/.44411/.25815/.99360/1.00000. Smaller quality samples have wider uncertainty; their composition differs. Weighting NOT FEASIBLE in this run because compatible official adult age×education margins could not be verified/retrieved; unweighted robustness is not a weighting test. No nationally representative claim. See status files.
8. **Recommended strength: B — interesting but should be framed as suggestive.**

## Rationale (eight sentences)

**Fact:** the observed Cash Top75 decline exceeds the Food and Medical declines. **Fact:** the focal omnibus and both primary contrasts fail the finite-family global correction. **Inference:** the form-by-size pattern remains a useful descriptive candidate, not strong corrected evidence. **Fact:** ordered location-scale sensitivity does not restore a robust full-distribution interaction. **Elimination:** the available bindingness and relative-scale tests do not establish either mechanism, but cannot exclude every version of them. **Inference:** null moderation is limited by differential-slope MDEs and cannot support universality. **Fact:** positive controls are mixed and ethics/minor coverage and recruitment details remain unresolved. **Interpretation:** a bounded account of stated response patterns is warranted; endogenous earmarking is speculation and no further exploratory analysis follows this package.

## Focal table — probability units, not percentage points

| estimand | estimate | lo | hi | p | global_maxT_p | N | df |
| --- | --- | --- | --- | --- | --- | --- | --- |
| cash_slope | -0.040546 | -0.05684 | -0.024252 | 1.0757e-06 | — | 5497 | 1 |
| food_slope | -0.0123524 | -0.0282043 | 0.00349945 | 0.126683 | — | 5497 | 1 |
| medical_slope | -0.00965079 | -0.0217997 | 0.00249816 | 0.119478 | — | 5497 | 1 |
| omnibus | — | — | — | 0.00803447 | 0.413717 | 5497 | 2 |
| cash-food | -0.0281935 | -0.0509262 | -0.00546078 | 0.0150645 | 0.880624 | 5497 | 1 |
| cash-medical | -0.0308952 | -0.0512198 | -0.0105705 | 0.00288847 | 0.510098 | 5497 | 1 |
| food-medical | -0.00270166 | -0.0226736 | 0.0172703 | 0.790906 | 1 | 5497 | 1 |
| restricted-cash | 0.0295443 | 0.0104338 | 0.0486549 | 0.00244476 | 0.473305 | 5497 | 1 |

## Separate-form profiles — all three outcomes

| form | amount | outcome | N | estimate | lo | hi |
| --- | --- | --- | --- | --- | --- | --- |
| cash | 200 | ordinal | 619 | 2.93376 | 2.80103 | 3.06649 |
| cash | 200 | midpoint | 619 | 0.252666 | 0.229366 | 0.275965 |
| cash | 200 | top75 | 619 | 0.134087 | 0.107222 | 0.160953 |
| cash | 1000 | ordinal | 595 | 2.80336 | 2.67525 | 2.93147 |
| cash | 1000 | midpoint | 595 | 0.226807 | 0.205048 | 0.248566 |
| cash | 1000 | top75 | 595 | 0.0890756 | 0.0661678 | 0.111983 |
| cash | 5000 | ordinal | 584 | 2.70205 | 2.58405 | 2.82006 |
| cash | 5000 | midpoint | 584 | 0.200813 | 0.181434 | 0.220193 |
| cash | 5000 | top75 | 584 | 0.0530822 | 0.034883 | 0.0712814 |
| food | 200 | ordinal | 614 | 2.78502 | 2.65557 | 2.91446 |
| food | 200 | midpoint | 614 | 0.228054 | 0.206067 | 0.250041 |
| food | 200 | top75 | 614 | 0.0993485 | 0.0756684 | 0.123029 |
| food | 1000 | ordinal | 620 | 2.66935 | 2.55025 | 2.78846 |
| food | 1000 | midpoint | 620 | 0.200927 | 0.181169 | 0.220686 |
| food | 1000 | top75 | 620 | 0.0709677 | 0.0507396 | 0.0911959 |
| food | 5000 | ordinal | 602 | 2.62791 | 2.50709 | 2.74872 |
| food | 5000 | midpoint | 602 | 0.194684 | 0.174417 | 0.214952 |
| food | 5000 | top75 | 602 | 0.0747508 | 0.0537249 | 0.0957768 |
| medical | 200 | ordinal | 615 | 2.46179 | 2.34097 | 2.58261 |
| medical | 200 | midpoint | 615 | 0.176992 | 0.157531 | 0.196453 |
| medical | 200 | top75 | 615 | 0.0601626 | 0.0413538 | 0.0789714 |
| medical | 1000 | ordinal | 612 | 2.53105 | 2.41564 | 2.64645 |
| medical | 1000 | midpoint | 612 | 0.178595 | 0.159989 | 0.1972 |
| medical | 1000 | top75 | 612 | 0.0522876 | 0.0346364 | 0.0699387 |
| medical | 5000 | ordinal | 636 | 2.52044 | 2.4065 | 2.63438 |
| medical | 5000 | midpoint | 636 | 0.179245 | 0.161277 | 0.197213 |
| medical | 5000 | top75 | 636 | 0.0408805 | 0.025479 | 0.056282 |

## Interpretation boundaries

- **Fact:** 300/300 fitted models and 1,500/1,500 contrast rows were estimable. Global family covers seven outcomes, five samples, three dose representations and appropriate links. 5,000 centered constrained-null score-multiplier draws; zero draw-level optimizer refits. Null score-level simulation: 7/200 rejections (3.5%; 95% binomial CI 1.42–7.08%). This is an asymptotic joint resampling check, not exact randomization inference or a full model-refit bootstrap.
- **Fact:** ordered-model primary ordinal omnibus raw P spans .078–.118 for the nonlinear models; global P>.94. Location and scale are allowed to vary by form/dose; no strong location effect after correction. The alternative alone cannot prove which scale mechanism generated the ordinal pattern.
- **Fact:** at ¥5000 only Cash−Medical and Restricted−Cash meet Holm-12 TOST at the widest ±5pp margin; Food−Medical does not. No independent SESOI was available. **Inference:** do not claim convergence or equal arms; wide-margin descriptive sensitivity is weaker than substantive equivalence.
- **Fact:** all-X supplemental six primary families have zero BH q<.10 and zero q<.05. Old analysis is not an independent replication. No nominal winner is highlighted.
- **Inference:** upper-tail visibility does not establish tail-specificity. No new cross-threshold claim is introduced here; all threshold probabilities, endpoint RR/OR and probability AMEs are disclosed.
- **SUBMISSION BLOCKER:** current documentation does not establish ethics/consent coverage of 17 minors. Recommend adult-only primary sample n=5480 unless authors supply appropriate coverage; analysis manifest is unchanged and R remains disclosed.
- **NOT FEASIBLE:** response-time/process measures and adult-compatible calibration in this run. Optional Bayesian model was not run. No substitute proxy, new moderator, outcome, tuned threshold or manuscript rewrite.

## Audit navigation

Methods/limits: maxT_diagnostics.md; analysis_history.md; wording_identification_note.md; relative_scale_falsification_memo.md. Mechanisms: mechanism_prediction_table.md; questionnaire_mechanism_audit.md; response_time_audit.md. Submission: ethics_minors_audit.md; author_information_needed.md; open_science_release_checklist.md; NC_submission_requirements.md. Literature: reference_audit.csv; NC_revision_literature_map.md; revised_intro_outline.md. Verification: verification_results.json; figure_audit.md. Reproduction/publication details: README.md; RESULT.md.
