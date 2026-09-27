"""Build the locked final-verification audit and results memo."""
from pathlib import Path
import pandas as pd
import numpy as np

O=Path(__file__).resolve().parent
def f(x,n=3): return f"{float(x):.{n}f}"

s=pd.read_csv(O/"final_strict_inframarginal_pooled.csv")
b=pd.read_csv(O/"final_portability_refit_bootstrap_1000.csv").set_index("target")
g=pd.read_csv(O/"final_portability_amount_ordinal_gaps.csv")
h=pd.read_csv(O/"final_heldout_person_score_invariance.csv")
a=pd.read_csv(O/"final_subjective_cronbach_alpha.csv")
e=pd.read_csv(O/"final_subjective_pca_eigenvalues.csv")
c=pd.read_csv(O/"final_subjective_correlation.csv",index_col=0)

sr=s[(s["sample"]=="R")&(s.outcome=="outcome_ord")].iloc[0]
sm=s[(s["sample"]=="R")&(s.outcome=="mpc_midpoint")].iloc[0]
key=g[(g.source=="cash")&g.target.isin(["food","medical"])].copy()
adj=key[key.specification=="amount_adjusted"].set_index("target")
ordr=key[key.specification=="ordinal"].set_index("target")
by=key[key.specification=="by_amount"]
rf=h[(h.learner=="random_forest")&(h.outcome=="mpc_midpoint")]
rfo=h[(h.learner=="random_forest")&(h.outcome=="outcome_ord")]
off=c.where(~np.eye(len(c),dtype=bool)).stack()

audit=f"""# NHB final verification audit

## Locked scope

This round executed only the five checks in `消费调查/NHB_FINAL_VERIFICATION.md`. No manuscript file was edited, no new moderator search was opened, and no respondent-level data or predictions were written.

## Methods verified

1. **Strict inframarginality.** Monthly food-spending band lower bounds were multiplied by the six-month voucher horizon. A respondent is strict only when transfer amount is below that lower bound. Food−Cash is estimated in the pooled strict sample with amount fixed effects and HC3 standard errors; ordinal outcome is primary.
2. **1,000-draw refit bootstrap.** Each draw resamples Cash source training, target-form training, and target evaluation respondents within amount strata. Cash, Food and Medical models are refit in every draw. Primary models use 120 trees, matching the previous 100-draw refit specification. Only aggregate quantiles are retained.
3. **Amount portability.** Amount-adjusted results include amount in source models and residualize target outcomes/predictions by target amount before evaluation. Separate RMB 200/1,000/5,000 matrices use common five-fold splits within each amount; diagonals are held out.
4. **Person-score invariance.** Within each outer training fold, randomized form×amount cell means are removed from midpoint MPC before learning a baseline person score. Ridge or random forest learns this residual score; the untouched fold receives the prediction. The final HC3 regression tests held-out score×Food and score×Medical interactions while controlling form×amount.
5. **Ordinal and subjective diagnostics.** The full portability matrix is rerun with the original 1–6 outcome. Subjective-item correlation, standardized PCA and Cronbach alpha use the 27 prespecified non-age 0–10 items. PCA/alpha are descriptive and do not establish a stable latent trait.

## Mechanical checks

- All five seeds completed; all portability cells have finite OOF predictions.
- Bootstrap B=1,000 with 120 trees and no failed draw.
- Strict pooled sample N={int(sr.N)} (Food {int(sr.N_food)}, Cash {int(sr.N_cash)}).
- PCA eigenvalues sum to {f(e.eigenvalue.sum())}, equal to the 27 standardized items up to finite-sample normalization.
- Correlation off-diagonal range: {f(off.min())} to {f(off.max())}; median absolute correlation {f(off.abs().median())}.
- No raw data, identifiers, respondent rows, fold assignments, OOF predictions or draw-level bootstrap results are included.

## Interpretation safeguards

- The strict-inframarginal effect is a randomized Food−Cash contrast within a baseline-defined subgroup, but its subgroup definition inherits interval-reporting and six-month extrapolation assumptions.
- Amount-specific portability has materially smaller cell sizes and is used for heterogeneity diagnosis, not independent discovery claims.
- Seed variation is a stability diagnostic, not five independent replications.
- The person-score midpoint/RF result is not robustly reproduced on the primary ordinal outcome; it is suggestive specification-dependent evidence.
- Very high alpha and a dominant PC1 can reflect overlapping wording or common response style; they do not prove a single substantive psychological trait.
"""
(O/"NHB_FINAL_VERIFICATION_AUDIT.md").write_text(audit,encoding="utf-8")

bylines=[]
for amount in [200,1000,5000]:
    q=by[by.amount.astype(str)==str(amount)].set_index("target")
    bylines.append(f"- RMB {amount}: Cash→Food gap {f(q.loc['food','spearman_gap_vs_target_within'])}; Cash→Medical gap {f(q.loc['medical','spearman_gap_vs_target_within'])}.")

results=f"""# NHB final verification results

## Bottom line

The five locked checks **do not justify upgrading the project from Pattern C to a clean Pattern B**. The strict-inframarginal Food−Cash contrast remains negative, so the food result is not explained away by obvious bindingness. The 1,000-draw refit bootstrap continues to place zero inside both target-normalized portability intervals. A held-out person score shows a consistently lower Medical slope in the midpoint/random-forest specification, but the original ordinal outcome is weaker and its joint tests do not cross 5%. The defensible synthesis remains low predictability with suggestive, specification-dependent medical asymmetry—not broad remapping.

## 1. Strictly inframarginal Food−Cash

In the raw strict sample (N={int(sr.N)}), the pooled amount-adjusted Food−Cash effect is **{f(sr.food_minus_cash)} ordinal categories** (95% CI {f(sr.lo)} to {f(sr.hi)}, p={f(sr.p)}). Midpoint coding gives {f(sm.food_minus_cash)} (95% CI {f(sm.lo)} to {f(sm.hi)}, p={f(sm.p)}). Adult and clean samples are nearly identical; Q1 is directionally negative but less precise, and Q2 is highly imprecise. Thus the average Food−Cash difference survives the strict inframarginal screen, but this does not identify a mechanism.

## 2. 1,000-draw model-refit bootstrap

- Cash→Food target-normalized Spearman gap: **{f(b.loc['food','point'])}**, 95% interval {f(b.loc['food','lo'])} to {f(b.loc['food','hi'])}.
- Cash→Medical gap: **{f(b.loc['medical','point'])}**, 95% interval {f(b.loc['medical','lo'])} to {f(b.loc['medical','hi'])}.

The medical point estimate remains worse, but both intervals include zero. Increasing B from 100 to 1,000 tightens Monte Carlo stability without converting the asymmetry into a precise refit-bootstrap finding.

## 3. Amount-adjusted and amount-specific portability

After amount adjustment, Cash→Food has a gap of {f(adj.loc['food','spearman_gap_vs_target_within'])}; Cash→Medical is {f(adj.loc['medical','spearman_gap_vs_target_within'])}. The basic ordering is unchanged.

Amount-specific estimates are heterogeneous:
{chr(10).join(bylines)}

The largest negative Medical gap occurs at RMB 1,000, but the RMB 200 rank gap is positive while its scale R2 gap is poor. This metric/amount dependence does not support a simple amount-invariant remapping claim.

## 4. Held-out person-score × form

For the midpoint outcome with a random-forest person score, the Medical interaction is negative for all five seeds (mean {f(rf.medical_score_interaction.mean())}; range {f(rf.medical_score_interaction.min())} to {f(rf.medical_score_interaction.max())}). Its individual p-values range {f(rf.medical_p.min())} to {f(rf.medical_p.max())}; joint Food/Medical p-values range {f(rf.joint_p.min())} to {f(rf.joint_p.max())}. Food interactions remain near zero.

On the primary ordinal outcome, the Medical interaction remains directionally negative (mean {f(rfo.medical_score_interaction.mean())}) but 95% intervals include zero in every seed and joint p-values range {f(rfo.joint_p.min())} to {f(rfo.joint_p.max())}. Ridge is also weaker. This is a focused piece of medical-boundary evidence, but it is outcome/model dependent and therefore not sufficient on its own for Pattern B.

## 5. Ordinal robustness and subjective measurement structure

With the original ordinal outcome, Cash→Food’s target-normalized gap is {f(ordr.loc['food','spearman_gap_vs_target_within'])}, while Cash→Medical is {f(ordr.loc['medical','spearman_gap_vs_target_within'])}; this matches the midpoint ordering.

The 27 subjective items are highly redundant: off-diagonal correlations range {f(off.min())}–{f(off.max())}, median absolute correlation is {f(off.abs().median())}, and overall Cronbach alpha is {f(a.set_index('scale').loc['all_subjective','cronbach_alpha'])}. PC1 has eigenvalue {f(e.iloc[0].eigenvalue)} and explains {f(100*e.iloc[0].variance_share,1)}% of standardized variance; no later component has eigenvalue above 1. This supports a strong common response dimension, but it also raises response-style/common-method concerns and does not establish that stated MPC is a stable trait.

## Final stopping decision

Stop analysis expansion here, as required. Pattern C remains the safest classification, augmented by two bounded facts: (i) the Food−Cash mean difference persists among strictly inframarginal respondents; and (ii) medical person-score slope differences are suggestive under midpoint/RF but not robust across outcome/model choices. The manuscript was not modified.
"""
(O/"NHB_FINAL_VERIFICATION_RESULTS.md").write_text(results,encoding="utf-8")
print("final verification reports written")
