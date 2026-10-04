# Execution repairs and limitations

All repairs below occurred inside the frozen analyses; no outcomes, samples,
families, seeds, mappings or empirical questions were changed.

| Issue | Resolution / verification |
| --- | --- |
| Patsy namespace collision with a local contrast variable | Isolated formula evaluation namespace; Food model checks match independent fits |
| Optional `tabulate` package absent | Deterministic Markdown table writer; no package installation needed |
| Incremental-mean standard errors initially lacked the finite-cell HC3 factor | Used individual-observation-equivalent N/(N−1) correction; independent validator verifies SEs and Holm6 |
| Dependent-outcome covariance has numerically degenerate eigenvalues | Independent covariance agrees to 1e−12; min-P regeneration uses the canonical stored covariance/eigenbasis, rather than assuming bit-level equality of eigenvectors for separately accumulated matrices |
| Raw Stata label names differ from variable names | Resolved each variable's actual label-set association; displayed category labels verified |
| Relative prediction gain was conflated with unrestricted-model gain | Corrected main-text REL-vs-ABS improvement to 0.12–0.17%; historical source unchanged |
| Affine lack-of-fit summary rounded an earlier SE version | Final common-slope lack-of-fit p rounds to .178 in both generated note and source |
| Log-axis minor labels overlapped in Figures 2/4 | Removed minor ticks; Food plot extends below zero to show complete normal CI |
| Nine-column table width rule overcompressed outcomes/numbers | Equal-width numeric columns; headers use spaces; repeated headers and no row splitting retained |
| Preferred document renderer unavailable | LibreOffice executable was absent; separate hidden Word COM instance exported both PDFs, then Poppler rasterized all pages for visual inspection |
| Poppler reported Symbol/ArialUnicode display-font warnings | Actual rendered math, Chinese questionnaire text and figures inspected; no missing glyphs observed |
| Live official JEBO guide returned403 | No unverified current limit asserted; abstract185 words, author must check submission portal |
| Missing recruitment/ethics/fieldwork records | Author question sent; explicit checklist retained and PR remains draft |

All 8,000 interval-bootstrap fits converged; no failed draws were deleted or
redrawn. These optimizer successes do not cure the substantive calibration
problems reported in the manuscript.
