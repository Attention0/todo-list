# Visual QA — JEBO v1

Date: 2026-10-03. Final Word-rendered manuscript: 17 pages, 3 tables, 3 figures.
Final supplement: 13 pages, 15 tables. Every page was inspected as a readable
110-dpi raster; changed pages were inspected again after repair. The three
standalone figure PDFs were also rasterized and inspected, alongside the PNG
figures embedded in the manuscript. SVG/vector sources are retained.

## Repairs made

- Removed an otherwise empty “Tables and figures” divider page.
- Preserved the author email during typographic spacing normalization.
- Widened the treatment-description, conditional-mean and screen-label columns.
- Kept short tables and their notes together; long tables repeat column headings.
- Restricted caption styling to actual numbered captions, preserving body font size.
- Corrected two incomplete bibliographic page ranges against publisher/author records.
- Kept the article title black and the atlas categories in ordered light-to-dark shades.

## Final inspection

Main pages 1–5: title, contact, abstract, introduction and design readable; no
cropping or broken symbols. Pages 6–9: results, decomposition and discussion
readable, including minus signs, percentages and Greek delta. Pages 10–11:
references readable and links wrap within margins. Pages 12–14: all three
tables and notes fit. Pages 15–17: figure labels, error bars, legends and captions
are legible; the figures agree with the adult source CSVs.

Supplement pages 1–13: all sections and tables inspected. No clipped cell text,
overlapping elements, blank pages or missing mathematical characters observed.
Long Table S5 continues with a repeated header. Short tables and their explanatory
notes remain together. Intentional whitespace around intact tables is retained.

## Renderer and limits

The bundled render_docx.py failed because soffice.exe was unavailable. A separate,
hidden Microsoft Word COM instance successfully produced the QA PDFs, followed
by Poppler rasterization. Poppler reported display-font warnings for Symbol and
ArialUnicode; actual rendered mathematical glyphs were visually checked and were
present. No user Word session was closed. QA files are ignored and are not submission
deliverables. Final DOCX hashes are recorded in final_audit.json.

This verifies the delivered author manuscript layout, not the journal's current
submission portal requirements. The official Guide for Authors returned 403.
