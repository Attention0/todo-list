# Implementation log

Before interpretation: first core execution stopped in income models because a local contrast matrix named C shadowed Patsy's categorical C(). Renamed local matrices; no estimand, family, seed or sample changed. Partial outputs overwritten by complete deterministic rerun. Freeze remains unchanged.

Second execution: verification used DataFrame.ravel, corrected by explicit numpy conversion. CV unpenalized logistic LBFGS reached iteration limits on raw-scale interaction columns; switched to Newton-Cholesky with training-only scale normalization (same unpenalized likelihood and model space). Convergence is asserted for every fold; incomplete run not counted as passed.
# Final calibration and reporting checks

The first calibration implementation clipped weights before renormalizing, which allowed normalized weights above the frozen cap of 10. Corrected to min(lambda*w,10), choosing lambda for mean one. This changes a normalization implementation error, not the frozen target, cap, estimand or subgroup. Final ESS is 1190.954; exact target balance is explicitly not claimed.

Added reporting of which rows supply the original max-norm extreme, alongside min-P extremes, using the same frozen draws. This completes the planned diagnostic, without changing any P value or test family.

Packaged DOCX renderer failed because LibreOffice is absent on Windows. Logged the failure and used installed Microsoft Word in hidden read-only mode to export PDF, followed by bundled Poppler/PyMuPDF page rendering for visual inspection. No renderer installation or source document modification.
