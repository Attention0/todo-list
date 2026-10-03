# Final document visual verification

Date: 2026-10-03. Final manuscript: 22 pages. Final supplement: 10 pages.

The supplied document renderer was attempted and failed because LibreOffice is not installed. The installed Microsoft Word application then opened both final DOCX files read-only and exported PDFs with its window hidden. Bundled Poppler rendered those PDFs to 1,500-pixel-high page images. Every final page was inspected individually at full display size: manuscript pages 1–22 and supplement pages 1–10. The final images use the `checked-` prefix in the locally ignored `qa-final` directory; older preview images are superseded.

Verified readable text, complete tables, intact equations and symbols, figure labels and confidence intervals, numbered citations, captions, sequential figure order, and page numbers. There are no clipped figures, isolated table headers, blank pages or overlapping content in this rendering. Figures and associated captions remain together. Normal paragraph continuation across pages is retained. The manuscript uses black titles and no decorative title border; Figure 1 uses a single light-to-dark sequential palette. Supplement tables were kept together to eliminate header-only page breaks seen in preliminary renders.

The manuscript retains three conspicuous author-information fields rather than inventing ethics, funding or contribution facts. This is an author-review draft, not a certification of submission readiness. Visual verification does not replace the numerical checks in `package_verification.json`, whose DOCX hashes identify the checked document contents.

PDFs and page images are local verification artifacts only and are excluded from Git publication. Published DOCX files, figure exports and editable sources are the deliverables.
