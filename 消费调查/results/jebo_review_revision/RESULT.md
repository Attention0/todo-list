# JEBO reviewer-driven revision result

## Summary

Executed the complete bounded reviewer revision from PR17's exact head after
committing the frozen plan. The review was correct about the bindingness sign,
bottom-bin overinterpretation, missing yuan/incremental estimands, incomplete
ratio restrictions, overly strong null-mechanism claims and incomplete methods.
Numerically close slopes and nonrejected restrictions still cannot prove equal
MPCs; the revised paper does not make that stronger inference.

## Findings and narrative

- High-amount incremental midpoint-implied responses are Cash .1954, Food .1937,
  Medical .1785. All six pairwise interval contrasts have Holm6>.05, with intervals
  wide enough to retain meaningful differences.
- A form-intercept/common-slope midpoint affine benchmark has RMSE18.28 yuan
  and lack-of-fit p=.178. Slope equality p=.381 is nonrejection, not equivalence.
  Censored-normal models converge but fit category probabilities poorly and
  change with the residual-scale assumption; structural claims are withdrawn.
- In family42, Cash midpoint Holm=.0392/min-P=.0199 and Cash Top75
  Holm=.0000514/min-P=.000100 survive. Cash ordinal Holm=.400/min-P=.182 does not.
  The Top75 interaction Holm=.334/min-P=.149 remains uncertain.
- Food−Cash +8.00/+1.33pp slopes contradict the frozen sharp negative prediction
  conditional on the historical proxy. Six continuous moderation tests have
  Holm=1; their precision is reported. Full Food ratio restrictions reject for
  both mappings (Top75 Holm=.0426/.0437).
- The core question now separates form differences in levels, incremental
  response and distributions. Spendability is a Discussion hypothesis, not the
  measured explanation. Sequential mechanism exclusion, positive-control
  validation and participation/extensive-margin claims are removed.

## Files changed

- `results/jebo_review_revision/`: frozen protocol, issue matrix, reproducible
  analyses, aggregate tables, covariance/diagnostics, metadata/questionnaire/
  literature audits, precision ledger, verification, final audit and this result.
- `manuscript/jebo_v3/`: revised Markdown/Word manuscript and supplement,
  four figures in PNG/PDF, aggregate source CSVs, response letter, claim/reference
  ledgers and author-information checklist.
- The reviewer SPEC/WORK copied unchanged from the repository into the protocol
  commit. Historical PR9–17 scientific outputs were not edited.

## Key implementation decisions

Original adult sample and all outcome definitions retained. Nine-cell stratified
bootstraps use4,000 fixed-N draws; interval models use4,000 per scale model.
The42 family uses p-value normalization and joint dependent-outcome covariance
before min-P (10,000 centered Gaussian draws), never unscaled mixed-df max-T.
Food models contain full lower-order interactions and only authorized controls.
No new mediator, subgroup, weighting or broad covariate search was performed.

## Testing performed

40 independent checks passed (`verification.json`). Original raw SHA256 and577
historical hashes verified. All8,000 interval bootstrap fits converged. Both Word
documents rendered successfully and checked on all16/39 pages, including all
figures and Chinese questionnaire text. Preferred LibreOffice rendering was
unavailable; separate hidden Word export plus Poppler was used. See BUG_LOG.

## Acceptance Criteria

Frozen protocol precedes calculations; required adult, yuan/affine, interval,
family42, Food, precision, metadata and literature deliverables complete.
Manuscript, supplement, response letter and evidence ledgers agree with results.
Draft publication is stacked onto `feature/jebo-repositioning`; no old PR merged.
No analysis outside the frozen plan is included.

## Known issues

Author records are still needed for recruitment, field dates/stopping, incentives,
assignment implementation, ethics/consent, deployment order, authorship and
submission declarations. Author confirmation of AI disclosure is pending.
The live official JEBO guide returned403; submission portal requirements require
author verification. These limitations are explicit in both manuscript and
`AUTHOR_INFORMATION_REQUIRED.md`; this is a review draft, not a submission-ready
certification. Statistical uncertainty and hypothetical measurement remain.

## Delivery

- Branch: `feature/jebo-review-revision`
- Base: `feature/jebo-repositioning@926b05022189661bdfe4dc41d24ad900c77bbd12`
- Protocol commit: `0aa5681e2ceb148759b0f01a74db726bc464f6e5`
- Analysis/delivery commit SHA: `aecc41a027da62967ed8c017ec289b8774d90ba9`
- PR: https://github.com/Attention0/todo-list/pull/19 (draft, open, not merged)
- Remote base/head and draft status verified at creation; subsequent commit
  records this delivery metadata without changing the analyses or documents.
- Main: `../../manuscript/jebo_v3/JEBO_manuscript_v3.docx`
- Supplement: `../../manuscript/jebo_v3/JEBO_supplement_v3.docx`
- Response: `../../manuscript/jebo_v3/RESPONSE_TO_JEBO_REVIEW.md`
