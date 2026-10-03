# Source and version manifest

Current branch: feature/nc-evidence-revision, based on PR15 head12c5e5bb6a8b827f20c2f5cb8930fe24f6bbe12d and including mainb5f26e5. Analysis plan commitac4e7cb preceded the new estimates. The original files were read locally and not overwritten or uploaded.

- Raw data: 社会心态小调研数据(1).dta; SHA25616996c88fdd20f5084b62a8503a8eec1d4c6ec7caff489eff109500f629694fe.
- Questionnaire: 社会心态小调查问卷（整合文字版）(1).docx; SHA2564054f5c4de1f7bdc35ad3507778f03766eb2134b91da939a58b1687dd91d794a.
- Source manuscript: NC_MPC_manuscript_draft_v4_reviewer_response.docx. Conversation cosmetic v2 was not available locally; this revision recreates the requested gradient and black title styling.
- [New aggregate data and code](https://github.com/Attention0/todo-list/tree/feature/nc-evidence-revision/%E6%B6%88%E8%B4%B9%E8%B0%83%E6%9F%A5/results/nc_evidence_revision).
- [Historical PR15](https://github.com/Attention0/todo-list/pull/15). Historical files remain unchanged and contain earlier model families, moderators, measurement diagnostics and selection history.
- [Official census source](https://www.stats.gov.cn/sj/pcsj/rkpc/7rp/zk/html/A0401.jpg), accessed2026-10-03. The local original image was inspected; transcription is in census_2020_transcription.csv. Census2020 targets are not current survey population weights.

| Manuscript item | Aggregate source |
|---|---|
| Abstract and focal interaction | scientific_family21.csv; profiles.csv |
| Table1 and first-order effects | main_effects.csv |
| Fig1 | distribution.csv; profiles.csv |
| Fig2 | profiles.csv; form_contrasts.csv |
| Fig3a | figure3a_source.csv, copied from historical quality_gradient_source.csv |
| Fig3b and bindingness | mechanism_details.csv; mechanism_tests.csv |
| Relative scales and income prediction | adult_endpoint_ratios.csv; prediction_scores.csv; prediction_folds.csv; income_LR_sensitivity.csv |
| Q1/Q2 | screen_cell_counts.csv; mechanism_tests.csv; mechanism_details.csv |
| Supplementary Fig1 | spec_curve_source.csv |
| Supplementary Fig2 | calibration_effects.csv; calibration_diagnostics.csv; calibration_cells.csv |
| Inference calibration | simulation_results.csv; legacy_family_comparison.csv; both legacy extreme-source tables |
| Reference numbers | reference_number_map.json; references_original_order.json; reference_checks_v5.csv |
| Numerical verification | verification.json; package_verification.json |

Reference checks distinguish 2026-10-03 Crossref retrieval, earlier verified metadata and directly inspected publisher/institutional pages. Seven Crossref requests encountered HTTP429; no failed request is labelled a successful refresh. Shapiro–Slemrod, Arkes and Drescher were additionally checked against AEA/Elsevier pages, and Boehm against the AEA2025 issue. Previously checked Thaler1985/1999 and Kooreman metadata remain available in the historical package. Live checks verified the v4 references13/16/26 including volume/page metadata. Neither metadata matching nor abstract reading is represented as independent replication of a cited paper.

An archival DOI and actual participant-data access policy remain author tasks. A Git branch URL supplies reviewable code now but does not substitute for long-term archival deposition.
