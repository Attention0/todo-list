"""Aggregate-only revision figures and exact panel source CSVs."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm

FORMS = ["cash", "food", "medical"]
COLORS = {"cash": "#30343B", "food": "#2B7A91", "medical": "#C46B38"}
DOMAIN_LABELS = {
    "resources_position": "Resources / position",
    "liquidity": "Liquidity",
    "household_needs": "Household needs",
    "expectations": "Expectations",
    "security_pressure": "Security / pressure",
    "social_wellbeing": "Social / wellbeing",
    "demographics_exposure": "Demographics / exposure",
}


def save(fig, figs, stem):
    fig.savefig(figs / (stem + ".pdf"), bbox_inches="tight")
    fig.savefig(figs / (stem + ".png"), dpi=600, bbox_inches="tight")
    plt.close(fig)


def predictor_map(tables, figs):
    tab = pd.read_csv(tables / "nature_revision_domain_importance.csv")
    order = list(DOMAIN_LABELS)
    matrix = tab.pivot(index="domain", columns="form", values="delta_r2").loc[order, FORMS]
    source = tab.copy()
    source["panel"] = "A"
    source["domain_label"] = source.domain.map(DOMAIN_LABELS)
    source.to_csv(tables / "nature_revision_panel_predictor_map.csv", index=False)
    vmax = max(.012, np.nanmax(np.abs(matrix.to_numpy())) * 1.1)
    fig, ax = plt.subplots(figsize=(8.7, 5.2))
    im = ax.imshow(matrix.to_numpy(), cmap="RdBu_r", norm=TwoSlopeNorm(vcenter=0, vmin=-vmax, vmax=vmax), aspect="auto")
    ax.set_xticks(np.arange(3), ["Cash", "Food", "Medical"], fontsize=11)
    ax.set_yticks(np.arange(len(order)), [DOMAIN_LABELS[d] for d in order], fontsize=10)
    for i, domain in enumerate(order):
        for j, form in enumerate(FORMS):
            z = tab[(tab.domain == domain) & (tab.form == form)].iloc[0]
            ax.text(j, i, f"{z.delta_r2:+.3f}\n[{z.lo:+.3f}, {z.hi:+.3f}]", ha="center", va="center", fontsize=8.2)
    ax.set_title("A  Held-out domain-drop importance by randomized context", loc="left", fontsize=12, fontweight="bold", pad=15)
    ax.set_xlabel("Randomized transfer form")
    cb = fig.colorbar(im, ax=ax, fraction=.035, pad=.03)
    cb.set_label("ALL minus domain-dropped OOF R²")
    fig.text(.13, .015, "Same scale across forms; negative values are retained. Intervals bootstrap respondents conditional on fitted models.", fontsize=8.2)
    fig.subplots_adjust(left=.27, right=.91, top=.87, bottom=.13)
    save(fig, figs, "nature_revision_predictor_map")


def ridge_map(tables, figs):
    tab = pd.read_csv(tables / "nature_revision_ridge_maps.csv")
    view = tab[(tab.row_type == "form") & tab.fixed_display_subset].copy()
    order = (view[view.context == "cash"].sort_values(["domain", "encoded_predictor"])
             .encoded_predictor.tolist())
    matrix = view.pivot(index="encoded_predictor", columns="context", values="standardized_coef").loc[order, FORMS]
    src = view.copy()
    src["panel"] = "A"
    src.to_csv(tables / "nature_revision_panel_ridge_map.csv", index=False)
    vmax = max(.01, np.abs(matrix.to_numpy()).max() * 1.05)
    fig, ax = plt.subplots(figsize=(8.3, 7.7))
    im = ax.imshow(matrix.to_numpy(), cmap="RdBu_r", norm=TwoSlopeNorm(vmin=-vmax, vcenter=0, vmax=vmax), aspect="auto")
    ax.set_yticks(np.arange(len(order)), order, fontsize=8.5)
    ax.set_xticks(np.arange(3), ["Cash", "Food", "Medical"], fontsize=10)
    ax.set_title("A  Standardized ridge predictor map", loc="left", fontsize=12, fontweight="bold", pad=12)
    cb = fig.colorbar(im, ax=ax, fraction=.038, pad=.03)
    cb.set_label("Predictive coefficient")
    fig.text(.12, .014, "Fixed top-20 display subset selected by pooled treatment-blind absolute coefficient; associations are not mechanisms.", fontsize=8)
    fig.subplots_adjust(left=.3, right=.9, top=.92, bottom=.075)
    save(fig, figs, "nature_revision_ridge_map")


def reliability(tables, figs):
    tab = pd.read_csv(tables / "nature_revision_reliability_r2.csv")
    tab.to_csv(tables / "nature_revision_panel_reliability_r2.csv", index=False)
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.6), gridspec_kw={"width_ratios": [1.5, 1]})
    scenarios = tab[tab.kind == "reliability_scenario"]
    for name, color in [("ALL", COLORS["medical"]), ("O", COLORS["cash"]), ("O+S-minus-O", COLORS["food"])]:
        z = scenarios[scenarios.model == name].sort_values("assumed_reliability")
        ax[0].plot(z.assumed_reliability, z.conditional_latent_r2, label=name, color=color, lw=2)
        ax[0].fill_between(z.assumed_reliability.to_numpy(), z.conditional_lo.to_numpy(), z.conditional_hi.to_numpy(), color=color, alpha=.13)
    for rel in [.4, .6, .8]:
        ax[0].axvline(rel, color=".78", lw=.8, ls="--")
    ax[0].set(xlabel="Assumed outcome reliability", ylabel="Reliability-conditional latent R²", xlim=(.3, 1))
    ax[0].legend(frameon=False, fontsize=9)
    ax[0].set_title("A  Classical-error sensitivity (not an estimate)", loc="left", fontsize=10.8, fontweight="bold")
    quality = tab[tab.kind == "quality_screen"].copy()
    for i, feature in enumerate(["O", "ALL"]):
        z = quality[quality.model.str.startswith(feature + "_")].copy()
        z["sample"] = z.model.str.replace(feature + "_", "", regex=False)
        z = z.set_index("sample").loc[["R", "C", "Q1", "Q2"]]
        ax[1].plot(np.arange(4), z.observed_r2, marker="o", lw=1.6, label=feature,
                   color=COLORS["cash"] if feature == "O" else COLORS["medical"])
    ax[1].set_xticks(np.arange(4), ["R", "C", "Q1", "Q2"])
    ax[1].set(ylabel="Observed OOF R²", xlabel="Response-quality restriction")
    ax[1].set_title("B  Empirical sample screens", loc="left", fontsize=10.8, fontweight="bold")
    ax[1].legend(frameon=False)
    for a in ax:
        a.spines[["top", "right"]].set_visible(False)
        a.axhline(0, color=".6", lw=.8)
    fig.text(.04, .005, "No repeated outcome is available; quality screens do not measure test-retest reliability.", fontsize=8.3)
    fig.tight_layout(rect=(0, .04, 1, 1))
    save(fig, figs, "nature_revision_reliability_r2")


def policy(tables, figs):
    hist = pd.read_csv(tables / "nature_revision_panel_policy_advantages.csv")
    crossing = pd.read_csv(tables / "nature_revision_predicted_crossing.csv")
    decomp = pd.read_csv(tables / "nature_revision_policy_decomposition.csv")
    stress = pd.read_csv(tables / "nature_revision_policy_1000.csv")
    combined = []
    for panel, frame in [("A", hist), ("B", crossing), ("C", decomp), ("D", stress)]:
        z = frame.copy()
        z.insert(0, "panel", panel)
        combined.append(z)
    pd.concat(combined, ignore_index=True, sort=False).to_csv(tables / "nature_revision_panel_policy_decomposition.csv", index=False)
    fig, ax = plt.subplots(2, 2, figsize=(11, 7.5))
    for form in ["food", "medical"]:
        z = hist[hist.form_vs_cash == form]
        mid = (z.bin_left + z.bin_right) / 2
        ax[0, 0].plot(mid, z.share, color=COLORS[form], lw=1.8, label=form.title())
    ax[0, 0].axvline(0, color=".4", ls="--", lw=.8)
    ax[0, 0].set(xlabel="OOF predicted advantage over Cash", ylabel="Share per bin")
    ax[0, 0].legend(frameon=False)
    ax[0, 0].set_title("A  Predicted crossing, not true benefit", loc="left", fontsize=10.8, fontweight="bold")
    for j, form in enumerate(["food", "medical"]):
        z = crossing[crossing.form_vs_cash == form].iloc[0]
        ax[0, 1].errorbar(j, z.positive_subgroup_DR_contrast,
                          yerr=[[z.positive_subgroup_DR_contrast-z.contrast_lo], [z.contrast_hi-z.positive_subgroup_DR_contrast]],
                          fmt="o", capsize=4, color=COLORS[form])
        ax[0, 1].text(j, z.contrast_hi + .005, f"{100*z.predicted_positive_share:.1f}% predicted +", ha="center", fontsize=8)
    ax[0, 1].set_xticks([0, 1], ["Food", "Medical"])
    ax[0, 1].axhline(0, color=".6", lw=.8)
    ax[0, 1].set(ylabel="DR contrast vs Cash among predicted +")
    ax[0, 1].set_title("B  Held-out subgroup validation", loc="left", fontsize=10.8, fontweight="bold")
    z = decomp[decomp.selected_form.isin(["food", "medical"])]
    for j, form in enumerate(["food", "medical"]):
        row = z[z.selected_form == form].iloc[0]
        ax[1, 0].bar(j, row.contribution, color=COLORS[form], width=.56)
        ax[1, 0].errorbar(j, row.contribution,
                          yerr=[[row.contribution-row.contribution_lo], [row.contribution_hi-row.contribution]],
                          fmt="none", ecolor="black", capsize=4)
        ax[1, 0].text(j, row.contribution_hi + .0008, f"{100*row.assignment_share:.1f}% assigned", ha="center", fontsize=8)
    ax[1, 0].set_xticks([0, 1], ["Food-selected", "Medical-selected"])
    ax[1, 0].axhline(0, color=".6", lw=.8)
    ax[1, 0].set(ylabel="Contribution to DR gain vs all Cash")
    ax[1, 0].set_title("C  Exact additive policy decomposition", loc="left", fontsize=10.8, fontweight="bold")
    s = stress[stress.seed == stress.seed.min()]
    for j, est in enumerate(["DR", "IPW"]):
        row = s[s.estimator == est].iloc[0]
        ax[1, 1].errorbar(j, row.gain_vs_cash,
                          yerr=[[row.gain_vs_cash-row.gain_lo], [row.gain_hi-row.gain_vs_cash]],
                          fmt="o", color=COLORS["medical"], capsize=4)
    ax[1, 1].set_xticks([0, 1], ["DR", "IPW"])
    ax[1, 1].axhline(0, color=".6", lw=.8)
    ax[1, 1].set(ylabel="RMB 1,000 policy gain vs all Cash")
    ax[1, 1].set_title("D  Best-case Medical stress test", loc="left", fontsize=10.8, fontweight="bold")
    for a in ax.flat:
        a.spines[["top", "right"]].set_visible(False)
    fig.text(.04, .008, "All predictions are out of fold. Outcomes are hypothetical stated MPC; no welfare inference.", fontsize=8.3)
    fig.tight_layout(rect=(0, .035, 1, 1), h_pad=2.2, w_pad=2.2)
    save(fig, figs, "nature_revision_policy_decomposition")


def make_figures(tables, figs):
    tables = Path(tables)
    figs = Path(figs)
    plt.rcParams.update({"font.family": "DejaVu Sans", "pdf.fonttype": 42, "font.size": 9,
                         "axes.linewidth": .7, "savefig.facecolor": "white"})
    predictor_map(tables, figs)
    ridge_map(tables, figs)
    reliability(tables, figs)
    policy(tables, figs)


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("tables")
    p.add_argument("figures")
    args = p.parse_args()
    make_figures(args.tables, args.figures)
