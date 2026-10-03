# Reproduction

Run from the repository root with the Python environment listed in `run_manifest.json`:

```powershell
python 消费调查/results/nhb_reanalysis/extract_inputs.py
python 消费调查/results/nhb_reanalysis/nhb_reanalysis.py "G:\桌面\科研\项目-消费调查\社会心态小调研数据(1).dta" --out 消费调查/results/nhb_reanalysis
python 消费调查/results/nhb_reanalysis/build_reports.py
```

The source data and respondent-level predictions are never written to this directory. The extraction scripts write only questionnaire/manuscript text used for wording/claim auditing and non-identifying Stata metadata.
