# JEBO v4 narrative revision

Scientific base: PR19 `363313c8adc52cce252c11390a32e46c7a98d25f`.
Writing authority: main `dc020b1`, JEBO_V4_WRITING_SPEC.md and JEBO_V4_WORK.md.
This directory is a writing and aggregate-figure package. It contains no new
inferential analysis and never reads respondent-level records.

## Read first

JEBO_manuscript_v4.docx, JEBO_supplement_v4.docx and JEBO_Highlights_v4.docx are
the editable deliverables. Their Markdown sources are included. The story memo
and figure storyboard preceded the full draft. V4_EDITOR_SUMMARY.md includes the
five-title comparison; V4_LITERATURE_DIALOGUE.md positions the closest studies.

The main sequence is puzzles, scales, distributional anatomy, progressively
sharper diagnostics, and a unified candidate behavioral interpretation. All
formal uncertainty is inherited from the base. AUTHOR_INFORMATION_REQUIRED.md
is a draft-only checklist, not fabricated submission metadata.

## Reproduce the writing package

Use Python with pandas, numpy, matplotlib, python-docx, Pillow and pdfplumber.
The scripts are relative to this directory and write only here:

1. `python scripts/prepare_package.py` reads existing aggregate CSVs, redraws
   figures, copies exact figure sources and reorders the existing supplement.
   It also refreshes the author checklist from the historical base; retain the
   v4-specific status note if rebuilding that file.
2. `python scripts/references.py --cached` restores the bibliography and
   supplementary reference audit from the checked-in verification table.
   Without `--cached`, it performs a focused Crossref metadata refresh; primary
   abstract/claim verification is documented separately and is not automated.
3. `python scripts/build_docx.py` generates all three editable Word files.
4. `python scripts/audit_package.py` checks aggregate identities, protected base
   files, claim coverage, document structure and the explicit writing contract.

No regressions, bootstrap draws, new thresholds or new tests are run by these
scripts. Figure 3 only subtracts original endpoint category frequencies.
Figure 4 reproduces the original normal-binomial cell whisker arithmetic.
The 42-test table and other fit outputs are copied or quoted, never recalculated.

## Rendering

The document skill's renderer was attempted first; the bundled environment has
no LibreOffice executable. The fallback `scripts/render_word.ps1` exports PDFs
using a separate hidden Word instance and closes only its own documents.
Poppler renders page PNGs; `scripts/inspect_render.py` makes native-size paired
pages and an automated bounds/font inventory for visual review. QA intermediates
are ignored by Git. Final visual findings are recorded in V4_FINAL_AUDIT.md.

Chinese questionnaire glyphs use SimSun fallback because Times New Roman lacks
those glyphs; Latin body, headings, tables and figures use Times New Roman.
Long supplementary tables retain repeated headers. The eleven-column arithmetic
table is divided into two column panels without changing any source values.

The original scientific files, scripts and all older manuscripts remain unchanged.
Raw data and local caches are excluded from this package.
