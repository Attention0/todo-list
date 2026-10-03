# Post-freeze implementation corrections

2026-10-03: First grid execution completed, but the focal-table export stopped because renaming `contrast` to `estimand` collided with an existing description column. Rename that description to `estimand_definition` before concatenation. No model, outcome, sample, contrast, multiplicity family or decision rule changed. Re-run the identical grid and bootstrap with the identical seed.

2026-10-03: The focal export filter used DataFrame `.sample`, which resolves to a method rather than the column and returned an empty focal table. Use bracket column access and assert exactly five focal contrasts. The full1500-row grid and its numerical estimates were unaffected; rerun identical seeds and null simulation. This is an export bug, not a specification change.

2026-10-03: Historical all-X file contains two supplemental pairwise targets beyond the six primary Cash/RC families. Filter the QQ plot to those six primary families explicitly; otherwise the seventh group overran a six-panel layout. No new moderator test.

2026-10-03: Initial title-only Crossref search occasionally matched a working-paper/reprint instead of the manuscript's journal version. Switch to externally verified exact DOIs and audit journal/year/pages, not merely title similarity. HTTP429 records were not counted as verification; no statistical analysis changes.

2026-10-03: Visual inspection found QQ identity line nearly absent: unary minus was applied after max(logP), giving a near-zero endpoint. Use max(-logP) before choosing the line limit. Explicit Top75 y ticks avoid rounding fractional percentage ticks. Figure-only fixes, no specification/data change. Model diagnostics additionally export full parameter/SE vectors, including log-scale coefficients; no new tests.

2026-10-03: Clarify manifest wording only (saved manifest not modified): the saturated indicators and coefficient profiles are 1000-vs200 and5000-vs200 changes, not successive adjacent differences. Its two-dimensional joint test spans the same space as adjacent-difference coding; the implemented design/estimates/tests have not changed. CSV estimand definitions give the exact reference category.
