# Final scientific and delivery audit

## Frozen scope and provenance

- Exact base: `926b05022189661bdfe4dc41d24ad900c77bbd12` (PR17).
- First protocol commit: `0aa5681e2ceb148759b0f01a74db726bc464f6e5`.
- Immutable plan unchanged; analyses limited to the authorized yuan/affine,
  family42, Food and precision package, plus specified methods/literature audits.
- Canonical raw hash verified, adult N5,480, Food/Cash N3,621.
- 577 historical files retain their recorded hashes; original v2 remains read-only.

## Independent numerical verification

`verify_revision.py` reconstructs the required quantities rather than copying
the reported answers. `verification.json` contains40 passing checks, covering:

- all54 original adult response counts, nine Ns and share-to-yuan transformations;
- all six incremental responses and six pairwise HC3/Holm comparisons;
- endpoint elasticities, affine coefficients, fit and covariance;
- all42 raw/Holm/min-P p-values, simultaneous scalar intervals and covariance;
- all12 Food subgroup cells, Food−Cash signs, continuous moderation,
  two-degree-of-freedom ratio restrictions and six-test corrections;
- interval fit/calibration outputs and all8,000 bootstrap convergence statuses;
- precision formulas, historical provenance, manuscript structure, figure/table
  references, questionnaire boundary handling and protected-file hashes.

Joint min-P is independently validated against the canonical covariance and
fixed seed; the independently accumulated covariance agrees numerically, but
degenerate eigenbases need not produce identical draw realizations.

## Claim audit

- Cash midpoint and Top75 survive the42-test correction; Cash ordinal does not.
- Top75 cross-form omnibus remains weak after correction (Holm=.334,
  min-P=.149); all pairwise simultaneous cross-form intervals include zero.
- High-amount incremental responses are numerically close; uncertainty does not
  establish equivalence. Absolute Cash−Medical yuan differences grow with amount.
- Common-slope midpoint affine fit is a descriptive benchmark, not an identified
  structural MPC. Interval sensitivity is poorly calibrated and scale-dependent.
- Food−Cash historical proxy slopes are positive (+8.00/+1.33pp); the sharp
  negative prediction is contradicted conditional on the imperfect proxy.
- Full Food ratio restrictions are rejected; old interaction-only nonrejection
  cannot validate the complete ratio-only model.
- Continuous null moderation is accompanied by MDEs and compatible ranges;
  no equivalence or sequential exclusion of mechanisms is claimed.
- Bottom-category decomposition is arithmetic, not measured participation or a
  causal intensive-margin estimate; cross-amount thresholds differ.
- Spendability occurs only in Discussion as a candidate; no measured mediator
  or title-level mechanism claim remains. Prior positive controls are descriptive.
- Q1/Q2 are precisely defined response-style screens; fielded ordering remains
  an author check. Reweighting is sensitivity, not national representativeness.
- Hypothetical measurement, open/approximate bins and absent common spending
  horizon are explicit. No recruitment, ethics, consent or incentive fact invented.
- Methods disclose post-results freezing; manuscript omits internal PR/workflow
  language. Claim/reference ledgers and eight-point response letter are complete.

## Document and figure QA

Main Word:16 pages, four tables, four figures. Supplement:39 pages,32 tables.
Both were exported through hidden Word, rasterized at110dpi and visually checked
page by page. Table headers repeat; no clipped figures, missing Chinese glyphs
or overlapping axis labels observed. Numeric column widths were repaired after
the first rendering. Figures retain the original six response bins and adult
aggregate source data. Private cache, raw data and QA renders are excluded.

## Remaining author work

Recruitment, field dates/stopping, compensation, assignment implementation,
formal ethics/consent, deployment order, authorship, funding/conflicts, CRediT,
raw-data release authorization and human approval of AI disclosure remain open.
The current official JEBO guide could not be refreshed (403); the live portal
must be checked before submission. These are documented limitations, not
unperformed empirical analyses. Deliver as a draft; do not merge.
