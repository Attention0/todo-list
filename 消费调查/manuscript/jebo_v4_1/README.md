# JEBO v4.1 writing package

Start with `JEBO_manuscript_v4_1.docx`; editable Markdown has the same stem. Supplement and Highlights are separate Word documents. `V4_1_CHANGELOG.md` records revisions and migration; `V4_1_FINAL_AUDIT.md` records the substantive logic review and actual validation. `RESULT.md` records publication provenance.

The scientific base is PR20 `0685af82e06df1f43590c015379c2fb94fc4ac86`, retaining PR19 results. No new analysis was run. Figures and source data are unchanged aggregate copies from `../jebo_v4/`; the existing reference audit remains at `../jebo_v4/JEBO_V4_REFERENCE_AUDIT.csv`.

Editorial reproduction, from this directory, with Python and python-docx installed:

```text
python scripts/refine_text.py
python scripts/build_docx.py
python scripts/verify_writing.py
```

`refine_text.py` transforms the fixed v4 manuscript and supplement; it does not fit models or load respondent records. `build_docx.py` formats the documents. Verification compares existing text/results and file hashes. `scripts/render_word.ps1` and `scripts/inspect_render.py` support Windows Word/PDF layout QA; local render products are ignored under `qa/`. Do not run earlier empirical preparation scripts as part of this writing-only task.
