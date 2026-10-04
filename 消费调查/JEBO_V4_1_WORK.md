# JEBO v4.1 Work Plan — writing-only refinement

## Mission

Use PR #20 as the complete scientific and manuscript base, and perform a **pure writing refinement** according to:

- `消费调查/JEBO_V4_1_WRITING_SPEC.md`

Scientific base:
- PR20
- branch `feature/jebo-v4-narrative-rewrite`
- head `0685af82e06df1f43590c015379c2fb94fc4ac86`

Do not run new empirical analyses.

---

## 1. Branching

Create:

`feature/jebo-v4-1-writing-refine`

from exact PR20 head:

`0685af82e06df1f43590c015379c2fb94fc4ac86`

Open a stacked draft PR against:

`feature/jebo-v4-narrative-rewrite`

Do not merge.

---

## 2. Read before editing

Read:
- `消费调查/manuscript/jebo_v4/JEBO_manuscript_v4.md`
- `JEBO_supplement_v4.md`
- `V4_STORY_MEMO.md`
- `V4_FIGURE_STORYBOARD.md`
- `V4_LITERATURE_DIALOGUE.md`
- `V4_FINAL_AUDIT.md`
- PR19 result/audit files for numerical source checks

Then read the new v4.1 writing specification.

---

## 3. Strict no-analysis rule

Allowed:
- rewrite prose;
- reorganize paragraphs;
- shorten main-text technical detail;
- move existing details to supplement;
- reuse/reformat existing tables/figures;
- update Highlights;
- verify that every number matches PR19/PR20.

Not allowed:
- new regressions;
- new bootstrap;
- new tests;
- new moderator or subgroup work;
- new correction families;
- new outcome codings;
- new literature-driven empirical analysis.

If a stronger sentence would require new evidence, do not write it.

---

## 4. Main revision tasks

### A. Abstract
Rewrite to foreground:
- three puzzles;
- distributional anatomy;
- share/yuan distinction;
- unified organizing interpretation.

Reduce audit language.

### B. Introduction
Retain v4 logic but sharpen:
- standard Cash decline as benchmark;
- Medical flatness / Food gentler decline / convergence as the puzzles;
- distributional anatomy as first substantive contribution;
- explanation sequence as second substantive contribution.

### C. Section 6
This is the priority edit.

Rewrite every subsection to:
- lead with economic question/prediction;
- use only the most informative main-text evidence;
- end with a clear interim conclusion.

Move technical statistics to supplement where already available.

### D. Section 7
Strengthen to:
> “the most coherent organizing interpretation of the joint pattern…”

Explain Cash/Food/Medical paths explicitly.

Keep the unmeasured-mediator boundary once, clearly.

### E. Discussion
Rewrite the final 2–3 paragraphs.

Do not end with “the most secure result is narrower.”

End on:
- different distributional paths;
- closer mean shares;
- transfer size changes the behavioral importance of form;
- direct-measurement future test.

### F. Conclusion
Shorten and sharpen.

---

## 5. Supplement migration

Where technical material is removed from main text, ensure it remains in the supplement.

Do not delete:
- affine details;
- interval calibration;
- family42;
- ratio tests;
- MDE/precision;
- all-X/Q1/Q2;
- weighting;
- questionnaire details.

Only change placement and exposition.

---

## 6. Deliverables

Create new directory:

`消费调查/manuscript/jebo_v4_1/`

Required:
- `JEBO_manuscript_v4_1.md`
- `JEBO_manuscript_v4_1.docx`
- `JEBO_supplement_v4_1.md`
- `JEBO_supplement_v4_1.docx`
- `JEBO_Highlights_v4_1.docx`
- `V4_1_CHANGELOG.md`
- `V4_1_FINAL_AUDIT.md`
- copied/linked figure package and source data as needed

No need for a new empirical result package.

---

## 7. Formatting

Inherit v4 formatting:
- Times New Roman;
- body 12pt;
- justified;
- first-line indent ~0.74cm;
- title 16–18pt;
- section heading 14pt;
- subsection 12pt bold;
- notes 9–10pt;
- page numbers;
- clean figures/tables;
- no tracked changes/comments.

Render the final DOCX and visually inspect every page.

---

## 8. Changelog

The changelog must state:
- no new analysis was run;
- which main-text technical details moved to supplement;
- how Abstract/Introduction/Section6/Section7/Discussion changed;
- all PR19/PR20 scientific boundaries preserved.

---

## 9. Final PR

Open draft stacked PR:

- head: `feature/jebo-v4-1-writing-refine`
- base: `feature/jebo-v4-narrative-rewrite`

Suggested title:

**JEBO v4.1: sharpen the three-puzzle narrative and remove audit tone**

Do not merge.
