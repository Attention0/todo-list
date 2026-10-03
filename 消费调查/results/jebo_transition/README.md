# JEBO transition: reproduction and scope

This package implements JEBO_SPEC.md / JEBO_WORK.md on PR16 head
`f3124aa820e0b4de3540aaaeb64ffdeb7ca19228`. It does not rerun the historical
respondent-level analyses. All numerical inputs are approved aggregate CSVs.
The protocol was committed at `950e90f`; the literature/story gate at `b6e7b22`
preceded manuscript writing. The chosen story is C.

## Reading order

1. RESULT.md and GITHUB_LITERATURE_RECONCILIATION.md: outcome and positioning.
2. JEBO_EVIDENCE_FREEZE.md / approved_source_rows.csv: numerical authority.
3. JEBO_ANALYSIS_MANIFEST.md / EXTENSIVE_INTENSIVE_NOTE.md: only new calculation.
4. JEBO_LITERATURE_MAP.md, JEBO_OUTLET_BENCHMARK.md and their CSV matrices.
5. JEBO_STORY_DECISION.md, MPC_SIZE_LITERATURE_BENCHMARK.md, BEHAVIORAL_PREDICTIONS.md.
6. ../../manuscript/jebo_v1/: main text, supplement, figures, claim/reference audits.

## Reproduce the finite calculation and author package

Use Python with NumPy, pandas, matplotlib, python-docx and pypdf. Exact versions
used are in software_versions.json. Set OPENBLAS_NUM_THREADS=1 and
OMP_NUM_THREADS=1 on memory-constrained machines. Run from the repository root:

```text
python 消费调查/results/jebo_transition/decompose.py
python 消费调查/results/jebo_transition/build_literature.py
python 消费调查/results/jebo_transition/build_positioning.py
python 消费调查/results/jebo_transition/make_figures.py
python 消费调查/results/jebo_transition/assemble_package.py
python 消费调查/results/jebo_transition/build_docx.py
```

The decomposition uses 4,000 multinomial draws with seed 2026100316 in fixed
form/amount order. Cell Ns stay fixed; no raw record is read. Repeating it in
the recorded environment reproduced all four analysis outputs byte-for-byte
(deterministic_reproduction.json). The nine point identities and every
bootstrap decomposition identity are checked at 1e-14.

The literature scripts consume the curated bibliography_metadata.csv.
collect_sources.py and read_primary_pdfs.py document the earlier source-access
work, not a prerequisite to numerical reproduction. Live metadata and working
paper versions may change. Do not rerun source collection to silently replace
the reviewed bibliography. Abstract text and downloaded papers are not distributed.

## Render and verify

The standard documents renderer was attempted but LibreOffice was unavailable.
On this Windows host, render_word.ps1 used a new hidden Word automation instance
to export both DOCX files to `manuscript/jebo_v1/qa/final/<stem>/<stem>.pdf`.
It closes only its own documents and Word instance. Poppler rendered every page
at 110 dpi into `page-01.png`, etc. No Office or TeX installation was added.

After rendering both documents and their page images:

```text
python 消费调查/results/jebo_transition/verify_transition.py
python 消费调查/results/jebo_transition/finalize_audit.py
```

The verifier checks historical hashes, all 63 adult profile means, grouped HC3
slopes/standard errors, the 21 nominal interaction tests and Holm values,
decomposition identities, sample provenance, document structure and page counts.
It does not pretend to rerun the prior min-P simulation or respondent-level models.
finalize_audit.py adds source paths to the reviewed claim blocks and records
document hashes. VISUAL_QA.md records the separate human-readable page inspection.

## Publication boundaries

No new thresholds, screens, models, moderators or correction families are used.
The prior 21-test min-P and Holm results remain unchanged. The manuscript is an
author-review draft, not certified ready for journal submission: see
AUTHOR_INFORMATION_REQUIRED.md. The official JEBO author-guide page returned
403; current portal rules still need confirmation. QA renders and copyrighted
research PDFs are ignored, and no respondent-level file belongs in this package.
