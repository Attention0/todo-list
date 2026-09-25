# 消费调查项目 — CURRENT WORK INSTRUCTIONS

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
