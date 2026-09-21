"""Targeted Nature revision; only aggregate outputs leave memory.

Usage: python nature_revision.py delivery.dta --out tables_dir --figdir figures_dir
The raw Stata file remains external. Core outcome, estimands, and cleaning are
imported unchanged from the locked pipeline.
"""
from argparse import ArgumentParser
from pathlib import Path
import json
import math
import sys

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.base import clone
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score
from sklearn.model_selection import StratifiedKFold

sys.path.insert(0, str(Path(__file__).resolve().parent))
import heterogeneity_formal as hf
import final_exploration as fe
import nature_empirical as ne


SEED = ne.SEED
SPLIT_SEEDS = [SEED, SEED + 1, SEED + 2]
FORMS = ne.FORMS
BOOT = 1000

# Frozen before inspecting form-specific coefficients/importances. Every locked
# predictor appears exactly once. Q7 is isolated as a narrowly defined liquidity
# domain; subjective SES (Q18/Q19) is kept outside objective resources.
DOMAINS = {
    "resources_position": ["q43_edu", "income_h", "q24_workstat", "q25_unittype", "q26_housing"],
    "liquidity": ["q07_emergfund"],
    "household_needs": ["q27_minorchild", "q28_hhsize", "q29_foodexp", "q30_medexp"],
    "expectations": ["q15_fut_self", "q16_fut_society", "q17a_fut_econ", "q17b_fut_job", "q17c_fut_price", "q17d_fut_fair", "q17e_fut_welfare", "q20_ses_next1"],
    "security_pressure": ["q06_socsec", "q09_gain", "q10_effort", "q11_mobility", "q13_pressure", "q18_ses_now", "q19_ses_past5"],
    "social_wellbeing": ["q01_lifesat", "q02_safety", "q03a_fair_dist", "q03b_fair_opp", "q03c_fair_rule", "q04_trust_gov", "q05_trust_soc", "q08_support", "q12_voice", "q21_order", "q22_vitality"],
    "demographics_exposure": ["q42_age", "q41_gender", "q23_hukou", "q31_gotsubsidy", "q49_citytier"],
}
assert len(sum(DOMAINS.values(), [])) == len(hf.FEATURES)
assert set(sum(DOMAINS.values(), [])) == set(hf.FEATURES)


def interval(x, rng, b=BOOT):
    x = np.asarray(x, float)
    ix = rng.integers(0, len(x), (b, len(x)))
    return np.quantile(x[ix].mean(axis=1), [.025, .975])


def bootstrap_r2(y, predictions, index):
    """R2 on a fixed resample; predictions has seed x respondent shape."""
    yy = y[index]
    den = np.sum((yy - yy.mean()) ** 2)
    return np.array([1 - np.sum((yy - p[index]) ** 2) / den for p in predictions])


def domain_importance(d, out):
    stored = {}
    seed_rows = []
    for form in FORMS:
        ix = np.flatnonzero(d.transfer_type.to_numpy() == form)
        y = d.mpc_midpoint.to_numpy()[ix]
        sets = {"ALL": hf.FEATURES}
        sets.update({domain: [v for v in hf.FEATURES if v not in cols] for domain, cols in DOMAINS.items()})
        pred = {name: [] for name in sets}
        for seed in SPLIT_SEEDS:
            global_fold = np.full(len(d), -1)
            for fold, _, te in ne.folds(d, seed):
                global_fold[te] = fold
            arm_fold = global_fold[ix]
            for name, cols in sets.items():
                pp = np.full(len(ix), np.nan)
                for fold in range(5):
                    tr = ix[arm_fold != fold]
                    te = ix[arm_fold == fold]
                    a = d.iloc[tr]
                    Xtr, names = fe.design(a, cols)
                    Xte, _ = fe.design(d.iloc[te], cols)
                    model = fe.pipe_for(names, "rf")
                    model.set_params(model__random_state=seed + fold)
                    model.fit(Xtr, a.mpc_midpoint)
                    pp[arm_fold == fold] = model.predict(Xte)
                assert np.isfinite(pp).all()
                pred[name].append(pp)
            for name in DOMAINS:
                delta = r2_score(y, pred["ALL"][-1]) - r2_score(y, pred[name][-1])
                seed_rows.append([form, name, seed, delta])
            print("domain RF", form, seed, flush=True)
        stored[form] = (y, {k: np.asarray(v) for k, v in pred.items()})

    rng = np.random.default_rng(SEED + 31)
    rows = []
    diffs = []
    for name in DOMAINS:
        boot_form = {}
        for form in FORMS:
            y, pred = stored[form]
            vals = np.array([r2_score(y, p) - r2_score(y, q) for p, q in zip(pred["ALL"], pred[name])])
            boot = np.empty(BOOT)
            for b in range(BOOT):
                ix = rng.integers(0, len(y), len(y))
                boot[b] = (bootstrap_r2(y, pred["ALL"], ix) - bootstrap_r2(y, pred[name], ix)).mean()
            lo, hi = np.quantile(boot, [.025, .975])
            rows.append([name, form, len(y), vals.mean(), lo, hi, vals.min(), vals.max(), len(vals),
                         r2_score(y, pred["ALL"].mean(axis=0)), r2_score(y, pred[name].mean(axis=0))])
            boot_form[form] = boot
        for left, right in [("cash", "food"), ("cash", "medical"), ("food", "medical")]:
            a = next(z for z in rows if z[0] == name and z[1] == left)[3]
            b = next(z for z in rows if z[0] == name and z[1] == right)[3]
            lo, hi = np.quantile(boot_form[left] - boot_form[right], [.025, .975])
            diffs.append([name, left + "-" + right, a - b, lo, hi, BOOT,
                          "independent arm respondent bootstrap; fixed repeated OOF fits"])
    pd.DataFrame(rows, columns=["domain", "form", "N", "delta_r2", "lo", "hi", "seed_min", "seed_max", "seeds", "all_r2_mean_prediction", "dropped_r2_mean_prediction"]).to_csv(out / "nature_revision_domain_importance.csv", index=False)
    pd.DataFrame(diffs, columns=["domain", "comparison", "difference", "lo", "hi", "bootstrap_B", "method"]).to_csv(out / "nature_revision_domain_differences.csv", index=False)
    pd.DataFrame(seed_rows, columns=["form", "domain", "seed", "delta_r2"]).to_csv(out / "nature_revision_domain_seed_stability.csv", index=False)


def ridge_maps(d, out):
    cols = hf.FEATURES
    cats = [c for c in cols if c in hf.NOMINAL + hf.ORDERED]
    X = pd.get_dummies(d[cols], columns=cats, dtype=float)
    X = ((X - X.mean()) / X.std().replace(0, 1)).fillna(0)
    names = list(X.columns)
    owner = {name: next(dom for dom, raw in DOMAINS.items() if name == raw[0] or any(name == v or name.startswith(v + "_") for v in raw)) for name in names}
    # A 41-variable map expands to 88 columns; float32 preserves the reported
    # coefficient precision while limiting copies during 900 bootstrap refits.
    xx = X.to_numpy(dtype=np.float32)
    y = d.mpc_midpoint.to_numpy(dtype=np.float32)
    arms = {f: np.flatnonzero(d.transfer_type.to_numpy() == f) for f in FORMS}
    pooled = Ridge(alpha=10).fit(xx, y).coef_
    display = set(np.asarray(names)[np.argsort(np.abs(pooled))[-20:]])
    base = {f: Ridge(alpha=10).fit(xx[ix], y[ix]).coef_ for f, ix in arms.items()}
    rng = np.random.default_rng(SEED + 32)
    boots = {f: np.empty((300, len(names)), dtype=np.float32) for f in FORMS}
    for b in range(300):
        for f, ix in arms.items():
            sample = rng.choice(ix, len(ix), replace=True)
            boots[f][b] = Ridge(alpha=10).fit(xx[sample], y[sample]).coef_
    rows = []
    for j, name in enumerate(names):
        for f in FORMS:
            q = np.quantile(boots[f][:, j], [.025, .10, .25, .50, .75, .90, .975])
            rows.append([owner[name], name, f, "form", base[f][j], *q, pooled[j], name in display, 300])
        for a, b in [("cash", "food"), ("cash", "medical"), ("food", "medical")]:
            q = np.quantile(boots[a][:, j] - boots[b][:, j], [.025, .10, .25, .50, .75, .90, .975])
            rows.append([owner[name], name, a + "-" + b, "difference", base[a][j] - base[b][j], *q, pooled[j], name in display, 300])
    pd.DataFrame(rows, columns=["domain", "encoded_predictor", "context", "row_type", "standardized_coef", "lo", "p10", "p25", "p50", "p75", "p90", "hi", "pooled_coef", "fixed_display_subset", "bootstrap_B"]).to_csv(out / "nature_revision_ridge_maps.csv", index=False)
    domain_rows = []
    for domain in DOMAINS:
        chosen = np.array([owner[name] == domain for name in names])
        magnitudes = {f: np.abs(boots[f][:, chosen]).mean(axis=1) for f in FORMS}
        for f in FORMS:
            value = np.abs(base[f][chosen]).mean()
            lo, hi = np.quantile(magnitudes[f], [.025, .975])
            domain_rows.append([domain, f, "form", value, lo, hi, int(chosen.sum())])
        for a, b in [("cash", "food"), ("cash", "medical"), ("food", "medical")]:
            value = np.abs(base[a][chosen]).mean() - np.abs(base[b][chosen]).mean()
            lo, hi = np.quantile(magnitudes[a] - magnitudes[b], [.025, .975])
            domain_rows.append([domain, a + "-" + b, "difference", value, lo, hi, int(chosen.sum())])
    pd.DataFrame(domain_rows, columns=["domain", "context", "row_type", "mean_abs_standardized_coef", "lo", "hi", "encoded_predictors"]).to_csv(out / "nature_revision_ridge_domain_summary.csv", index=False)


def reliability(out, locked):
    cv = pd.read_csv(locked / "nature_level_cv_summary.csv")
    inc = pd.read_csv(locked / "nature_level_increment.csv")
    q = pd.read_csv(locked / "nature_quality_predictability.csv")
    rows = []
    for label in ["O", "ALL"]:
        z = cv[(cv.model == "rf") & (cv.feature_set == label)].iloc[0]
        for rel in np.round(np.arange(.3, 1.0001, .01), 2):
            rows.append(["reliability_scenario", label, rel, z.r2, z.lo, z.hi,
                         min(1, z.r2 / rel), min(1, z.lo / rel), min(1, z.hi / rel), "fold-bootstrap interval transformed; reliability assumed, not estimated"])
    z = inc[(inc.model == "rf") & (inc.expanded == "O+S")].iloc[0]
    for rel in np.round(np.arange(.3, 1.0001, .01), 2):
        rows.append(["reliability_scenario", "O+S-minus-O", rel, z.delta_r2, z.lo, z.hi,
                     np.clip(z.delta_r2 / rel, -1, 1), np.clip(z.lo / rel, -1, 1), np.clip(z.hi / rel, -1, 1),
                     "paired-fold interval transformed; reliability assumed, not estimated"])
    for _, z in q.iterrows():
        rows.append(["quality_screen", z.feature_set + "_" + z["sample"], np.nan, z.r2, np.nan, np.nan,
                     z.r2, np.nan, np.nan, "sample restriction, not a reliability estimate"])
    pd.DataFrame(rows, columns=["kind", "model", "assumed_reliability", "observed_r2", "observed_lo", "observed_hi", "conditional_latent_r2", "conditional_lo", "conditional_hi", "interpretation"]).to_csv(out / "nature_revision_reliability_r2.csv", index=False)


def oof_form_means(d, seed=SEED, forms=FORMS):
    """Same model and global nine-cell folds as the locked policy calculation."""
    mu = np.zeros((len(d), len(forms)))
    for fold, tr, te in ne.folds(d, seed):
        for j, form in enumerate(forms):
            a = d.iloc[tr]
            a = a[a.transfer_type.eq(form)]
            Xtr, names = fe.design(a, hf.FEATURES)
            Xte, _ = fe.design(d.iloc[te], hf.FEATURES)
            m = fe.pipe_for(names, "rf").fit(Xtr, a.mpc_midpoint)
            mu[te, j] = m.predict(Xte)
    return mu


def arm_scores(d, mu, forms=FORMS):
    y = d.mpc_midpoint.to_numpy()
    actual = d.transfer_type.map({form: j for j, form in enumerate(forms)}).to_numpy()
    # Conditional on randomized amount, each form has known 1/3 probability
    # in the full experiment and 1/2 in the two-form stress test.
    p = 1 / len(forms)
    dr = np.column_stack([mu[:, j] + (actual == j) * (y - mu[:, j]) / p for j in range(len(forms))])
    ipw = np.column_stack([(actual == j) * y / p for j in range(len(forms))])
    return dr, ipw


def boot_selected(score, selected, rng, b=2000):
    """Paired respondent bootstrap for subgroup mean or population contribution."""
    n = len(score)
    vals = np.empty((b, 2))
    for k in range(b):
        ix = rng.integers(0, n, n)
        ss = selected[ix]
        vals[k, 0] = np.mean(score[ix] * ss)
        vals[k, 1] = np.sum(score[ix] * ss) / np.sum(ss) if ss.any() else np.nan
    return np.nanquantile(vals, [.025, .975], axis=0)


def policy_decomposition(d, out):
    mu = oof_form_means(d)
    dr, ipw = arm_scores(d, mu)
    policy = mu.argmax(axis=1)
    rng = np.random.default_rng(SEED + 33)
    rows = []
    for j, form in enumerate(FORMS[1:], start=1):
        selected = policy == j
        score = dr[:, j] - dr[:, 0]
        q = boot_selected(score, selected, rng)
        rows.append(["ml_argmax", form, len(d), int(selected.sum()), selected.mean(),
                     score[selected].mean(), q[0, 1], q[1, 1],
                     np.mean(score * selected), q[0, 0], q[1, 0]])
    total = np.where(policy == 0, 0, dr[np.arange(len(d)), policy] - dr[:, 0])
    q = ne.ci_mean(total, B=2000, seed=SEED + 34)
    rows.append(["ml_argmax", "total", len(d), int((policy != 0).sum()), (policy != 0).mean(),
                 np.nan, np.nan, np.nan, total.mean(), *q])
    pd.DataFrame(rows, columns=["policy", "selected_form", "N", "selected_N", "assignment_share", "selected_DR_contrast", "selected_lo", "selected_hi", "contribution", "contribution_lo", "contribution_hi"]).to_csv(out / "nature_revision_policy_decomposition.csv", index=False)

    crossing = []
    span = max(.25, float(np.max(np.abs(mu[:, 1:] - mu[:, [0]]))) * 1.01)
    bins = np.linspace(-span, span, 51)
    hist = []
    for j, form in enumerate(FORMS[1:], start=1):
        predicted = mu[:, j] - mu[:, 0]
        selected = predicted > 0
        contrast = dr[:, j] - dr[:, 0]
        q = boot_selected(contrast, selected, rng)
        crossing.append([form, len(d), int(selected.sum()), selected.mean(), predicted.mean(),
                         np.quantile(predicted, .05), np.quantile(predicted, .5), np.quantile(predicted, .95),
                         contrast[selected].mean(), q[0, 1], q[1, 1],
                         np.mean(contrast * selected), q[0, 0], q[1, 0]])
        counts, edges = np.histogram(predicted, bins=bins)
        assert counts.sum() == len(d)
        for left, right, count in zip(edges[:-1], edges[1:], counts):
            hist.append([form, left, right, int(count), count / len(d)])
    pd.DataFrame(crossing, columns=["form_vs_cash", "N", "predicted_positive_N", "predicted_positive_share", "predicted_advantage_mean", "predicted_p05", "predicted_p50", "predicted_p95", "positive_subgroup_DR_contrast", "contrast_lo", "contrast_hi", "population_contribution", "contribution_lo", "contribution_hi"]).to_csv(out / "nature_revision_predicted_crossing.csv", index=False)
    pd.DataFrame(hist, columns=["form_vs_cash", "bin_left", "bin_right", "count", "share"]).to_csv(out / "nature_revision_panel_policy_advantages.csv", index=False)

    # Exact same OOF model as locked policy; the decomposition should sum to
    # the locked DR argmax-minus-Cash gain to numerical tolerance.
    locked = pd.read_csv(Path(__file__).resolve().parents[1] / "tables" / "nature_policy_value.csv")
    old = locked[(locked.policy == "ml_argmax") & (locked.estimator == "DR")].gain_vs_cash.iloc[0]
    assert np.isclose(total.mean(), old, atol=1e-10), (total.mean(), old)
    print("policy decomposition", total.mean(), flush=True)


def policy_1000(d, out):
    dd = d[d.amount.eq(1000) & d.transfer_type.isin(["cash", "medical"])].reset_index(drop=True)
    rows = []
    for seed in SPLIT_SEEDS:
        mu = oof_form_means(dd, seed=seed, forms=["cash", "medical"])
        dr, ipw = arm_scores(dd, mu, forms=["cash", "medical"])
        choose = mu[:, 1] > mu[:, 0]
        rng = np.random.default_rng(seed + 90)
        for estimator, score in [("DR", dr), ("IPW", ipw)]:
            gain = np.where(choose, score[:, 1] - score[:, 0], 0)
            q = ne.ci_mean(gain, B=2000, seed=seed + (90 if estimator == "DR" else 91))
            rows.append([seed, estimator, len(dd), int(choose.sum()), choose.mean(), score[:, 0].mean(),
                         np.where(choose, score[:, 1], score[:, 0]).mean(), gain.mean(), *q,
                         "exploratory RMB1000 Cash-Medical two-arm stress test"])
        print("RMB1000 policy", seed, flush=True)
    pd.DataFrame(rows, columns=["seed", "estimator", "N", "medical_selected_N", "medical_selected_share", "all_cash_value", "policy_value", "gain_vs_cash", "gain_lo", "gain_hi", "status"]).to_csv(out / "nature_revision_policy_1000.csv", index=False)


def composition(d, out):
    strata = {
        "age_under35": d.q42_age < 35,
        "college_plus": d.q43_edu >= 3,
        "income_upper_half": d.income_h >= 4,
        "nonagricultural_hukou": d.q23_hukou == 2,
        "top_two_city_tiers": d.q49_citytier <= 2,
    }
    rows = []
    for name, mask in strata.items():
        for val in [False, True]:
            dd = d.loc[mask.eq(val)].reset_index(drop=True)
            counts = dd.transfer_type.value_counts()
            effects = {}
            for form in ["food", "medical"]:
                a = dd[dd.transfer_type.eq(form)].outcome_ord
                b = dd[dd.transfer_type.eq("cash")].outcome_ord
                effect = a.mean() - b.mean()
                se = math.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
                effects[form] = (effect, effect - 1.96 * se, effect + 1.96 * se)
            r2 = np.nan
            if len(dd) >= 800 and dd.cell.value_counts().min() >= 30:
                X = hf.add_design(dd, hf.FEATURES)
                for form in FORMS:
                    X["form_" + form] = dd.transfer_type.eq(form).astype(int)
                X = X.drop(columns="type")
                pred = np.full(len(dd), np.nan)
                for _, tr, te in ne.folds(dd):
                    p = fe.pipe_for(list(X.columns), "rf")
                    p.fit(X.iloc[tr], dd.mpc_midpoint.iloc[tr])
                    pred[te] = p.predict(X.iloc[te])
                r2 = r2_score(dd.mpc_midpoint, pred)
            rows.append([name, val, len(dd), min(counts.get(x, 0) for x in FORMS),
                         *effects["food"], *effects["medical"], r2])
        print("composition", name, flush=True)
    pd.DataFrame(rows, columns=["stratum", "group", "N", "minimum_form_N", "food_cash_ord", "food_lo", "food_hi", "medical_cash_ord", "medical_lo", "medical_hi", "all_rf_oof_r2"]).to_csv(out / "nature_revision_composition.csv", index=False)


def main(data, output, figdir):
    out = Path(output)
    figs = Path(figdir)
    out.mkdir(parents=True, exist_ok=True)
    figs.mkdir(parents=True, exist_ok=True)
    locked = Path(__file__).resolve().parents[1] / "tables"
    d = hf.prep(pd.read_stata(data, convert_categoricals=False)).reset_index(drop=True)
    assert len(d) == 5497 and d.cell.nunique() == 9
    domain_importance(d, out)
    ridge_maps(d, out)
    reliability(out, locked)
    policy_decomposition(d, out)
    policy_1000(d, out)
    composition(d, out)
    import nature_revision_figures as rf
    rf.make_figures(out, figs)
    print(json.dumps({"N": len(d), "split_seeds": SPLIT_SEEDS, "bootstrap_B": BOOT,
                      "individual_outputs_written": False}), flush=True)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("data")
    parser.add_argument("--out", default="nature-revision-output")
    parser.add_argument("--figdir", default="nature-revision-figures")
    args = parser.parse_args()
    main(args.data, args.out, args.figdir)
