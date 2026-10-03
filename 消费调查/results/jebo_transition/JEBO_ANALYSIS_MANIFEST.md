# JEBO target transition analysis manifest

Date: 3 October 2026. Base: PR16, f3124aa820e0b4de3540aaaeb64ffdeb7ca19228. This is a post hoc target-transition protocol, not preregistration. It is committed before new decomposition calculations. JEBO_SPEC.md and JEBO_WORK.md were obtained from origin/main; no historical branch is merged.

## Only new empirical analysis

Use the nine adult cells (A, age at least 18, N=5,480) from the approved nc_evidence_revision/distribution.csv. Its 54 category counts are sufficient statistics for all authorized calculations; no respondent-level file needs to be opened. Forms in fixed order: Cash, Food, Medical. Amounts: RMB 200, 1,000, 5,000. Original six categories and midpoint scores 0, .05, .175, .375, .625, .875 remain unchanged. Any additional spending means category 2–6, using the existing convention that the lowest category is essentially no additional spending.

For each cell report N, six-bin counts, p=P(any), unconditional midpoint mean m, conditional-positive midpoint mean mplus, and the existing Top75 probability. Verify m=p*mplus. No conditional-positive comparison is a causal estimand: positive responders are selected after treatment, and membership can differ across cells.

For each form compare 5,000 with 200 only. Define Delta m=mhigh-mlow. Extensive contribution=(phigh-plow)*(mplushigh+mpluslow)/2. Intensive contribution=(mplushigh-mpluslow)*(phigh+plow)/2. Verify that the two contributions sum to Delta m. Report levels and contributions for all three forms; do not select a form or component by significance. Do not report ratios of contributions to near-zero total changes. No new P values or multiplicity family.

Uncertainty: 4,000 independent nonparametric bootstrap draws within each of the nine fixed-size randomized cells; seed 2026100316, NumPy default_rng. Implement this exactly as multinomial resampling of each cell's six empirical category probabilities, equivalent to resampling observed categorical respondent records. Draws are generated in the fixed form/amount order. Report pointwise 2.5th/97.5th percentile intervals for p, mplus, m and both endpoint contributions/total change. Record any zero-positive draw as invalid rather than redrawing; if any occur, disclose and omit the affected interval. These are descriptive intervals, not simultaneous or mechanism tests. No bootstrap tuning or alternative seed selection.

## Literature and conceptual outputs

Prepare a non-meta-analytic size benchmark with the four approved Cash outcomes: any spending, midpoint, Top75 and conditional-positive midpoint. Compare with Fuster–Kaplan–Zafar, at least one realized-transfer size study and recent shock-size research. Explicitly distinguish horizons, questions, samples and outcome definitions; no cross-study statistical test.

Prepare a qualitative behavioral prediction table for the six accounts in JEBO_SPEC. Predictions without sufficient assumptions are marked ambiguous. No structural fitting, new moderators, cutoffs, screens, need variables, Bayesian analysis or mechanism scales.

## Reuse and presentation

All other statistics are copied from PR16 or clearly labelled historical aggregates. Ordinal score is a representation check, not fully invariant to arbitrary category spacing; the raw distribution remains the most design-faithful display. Preserve the 21-test Holm/min-P inference and all inconvenient earlier results in the supplement/source map. No new regression or changed family.

Reuse PR14 Hero geometry but populate it with PR16 adult aggregates, because literal reuse of the earlier full-sample graphic would mix adult and full samples. Keep six sequential shades. Figure2: approved adult ordinal/midpoint curves. Figure3: approved adult any/Top75 probabilities. No optional decomposition figure unless the final table proves unreadable; three main figures are the limit. All uncertainty labels follow the actual source, not the old full-sample bootstrap labels.

## Outputs and stop

extensive_intensive_cells.csv; extensive_intensive_decomposition.csv; EXTENSIVE_INTENSIVE_NOTE.md; MPC_SIZE_LITERATURE_BENCHMARK.md and CSV; BEHAVIORAL_PREDICTIONS.md; evidence and literature maps; story-decision memo; new jebo_v1 manuscript/supplement and audits. Commit the story decision before manuscript authoring. Stop new empirical work after this decomposition; unresolved novelty changes wording or triggers the specified stop, never new data exploration.
