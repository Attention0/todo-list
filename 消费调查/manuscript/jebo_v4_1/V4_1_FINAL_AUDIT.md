# JEBO v4.1 final writing and logic audit

## Review scope and verdict

Reviewed the manuscript's inferential logic against the frozen PR19/PR20 aggregate results, v4 supplementary tables and questionnaire wording. No major error requiring reversal of the frozen statistical conclusions was identified. This is a writing and reported-result consistency review, not an independent rerun or certification of the underlying statistical pipeline. No new empirical analysis was run.

## Ten required questions

| Question | Finding |
| --- | --- |
| 1. Finding-led abstract? | Yes. Economic question, three observed mean paths and their anatomy come first; 186 words. |
| 2. Three puzzles within 500 introduction words? | Yes. Cash versus Medical, gentler Food decline, narrowing mean form gaps appear in the opening three paragraphs. |
| 3. Section 5 central? | Yes. Four subsections and Figure 3 give Cash contraction, Food redistribution, Medical offsets and convergence without identity. |
| 4. Section 6 economic reasoning? | Yes. Seven economic questions lead to evidence and interim conclusions; detailed statistics remain in S4–S8. |
| 5. Unified interpretation sufficiently explicit? | Yes. Section 7 identifies resource categorization as the most coherent organizing interpretation and explains each form's path. It does not claim tested superiority. |
| 6. Substantive Discussion ending? | Yes. Different distributional paths toward closer means lead to a direct-measurement experiment; Section 9 gives a short conclusion. |
| 7. Scientific boundaries preserved? | Yes. See the checks below and the unchanged numerical tables/figures. |
| 8. Descriptive convergence upgraded to a population interaction? | No. The abstract, introduction, Section 4.3 and Discussion distinguish observed cells from corrected interaction inference. |
| 9. Spendability/categorization treated as measured? | No. They are explicitly unmeasured constructs in the proposed interpretation. |
| 10. Any new analysis? | No. Only editorial transformations, document building, file/text comparisons and layout inspection were executed. |

## Substantive logical checks

| Potential error | Evidence and resolution | Status |
| --- | --- | --- |
| Independent treatment cells interpreted as the same person's transition | Different respondents answer each amount. Introduction, Section 5 and Figure 3 now explicitly describe between-cell frequencies; the earlier individual-shift contrast was removed. | Inferential wording corrected |
| Mean convergence attributed to a shared middle-category frequency | One bin cannot establish its contribution to the mean without the other categories and weights. Section 5.4 describes coexistence, not a causal or exclusive decomposition. | Unsupported attribution removed |
| Ordinal-score inference used as a test of the whole distribution shifting down | A scalar score is not a stochastic-dominance test. Section 4.3 now treats midpoint, ordinal and highest-category results as different summaries. | Logical implication corrected |
| Flat Medical mean equated with no response-distribution change | The retained category frequencies and decomposition have offsetting components. Sections 5.3 and 7 retain those offsets; the introduction refers specifically to mean shares. | Distinction enforced |
| Medical persistence equated with measured mental categorization | Persistence is in the scenario; the psychological process is not observed. Section 7 explicitly separates them and does not claim uniquely predicted cancellation. | Mechanism overclaim prevented |
| A preferred interpretation selected by eliminating alternatives | Imprecise or null diagnostics do not eliminate mechanisms. Sections 6–7 distinguish the sharp conditional Food sign contradiction from inconclusive broader explanations. | Boundary retained |
| Food sign or comparison reversed | S6 preserves positive G0/G1 Food–Cash gradients and a negative G1–G0 difference as different contrasts. Main +8.00 and continuous +0.29 interval [−2.33, 2.91] agree with the existing tables. | No numerical correction needed |
| Equal affine slopes inferred from nonrejection | Main Sections 4.2 and 6.2 retain uncertainty; intervals permit similar and meaningfully different slopes. Yuan transformations are descriptive, not structural MPCs. | No equivalence claim |
| Relative-scale prediction gains confused with a ratio law | S7 separates relative-versus-nominal gains from unrestricted-model gains and retains joint restrictions. Small prediction gains do not establish the ratio law. | Correct distinction retained |
| Multiple testing hidden by more confident prose | Main Table 3 remains identical; 42-test inference and min-P comparable null scales remain in Section 3/S3. Within-Cash evidence is not presented as corrected cross-form evidence. | Frozen conclusion retained |
| Q1/Q2 assumed to use confirmed pretreatment responses | Questionnaire numbering alone does not establish deployed order. S8 now says numbered before the scenario and retains field-sequence confirmation as pending. Nonrejection of pass/fail differences is not equivalence. | Temporal claim qualified |
| Reweighting or observable nulls establish representativeness/universality | S7–S8 retain precision, ESS and calibration limitations; main Section 6.7 permits unobserved or imprecisely measured heterogeneity. | No such inference |

These include actual invalid implications and preventable ambiguities; they are not all major empirical errors. Remaining uncertainty is disclosed, not repaired by stronger prose.

## Executed verification

- `scripts/verify_writing.py`: 118/118 checks passed. This compares text, existing numerical content, figure/source hashes, references, questionnaire, DOCX structure and protected paths; it is not a statistical analysis.
- Main Tables 1–3 unchanged; all 36 supplement Markdown table bodies unchanged; original questionnaire and all 25 references unchanged.
- Four main figures and one supplementary figure, in both PNG and PDF, plus seven aggregate source CSVs match v4 byte for byte.
- Abstract 186 words; introduction 1,187; Section 6 1,085 versus 1,746; main text before References 6,402 including tables/captions.
- Built all three DOCX documents. Main: 16 pages, four tables/four figures. Supplement: 46 pages, 37 rendered tables/one figure. Highlights: one page.
- Visually inspected all 63 rendered pages at native raster size, including a fresh main-text render after the last wording changes. No clipping, text overflow, broken figure/caption placement or unreadable table cells identified.
- PDF character-bound checks found no overflow. Fonts are Times New Roman, with SimSun for the original Chinese questionnaire. Body is 12 pt with inherited v4 formatting; page numbers present; no tracked changes or comments.
- Standard document renderer was attempted but LibreOffice was unavailable. Rendered through a separate hidden Microsoft Word instance and Poppler instead. Poppler emitted generic Symbol/ArialUnicode font warnings; actual page inventories and visual inspection found no missing glyphs.

## Remaining author items

Author identity, affiliations, recruitment/fieldwork, allocation implementation, deployed question order, ethics/consent, funding, competing interests, contributions and human approval of the AI declaration remain to be confirmed before submission. See `AUTHOR_INFORMATION_REQUIRED.md`. This draft does not assert that JEBO acceptance is assured.
