# Reproduce NC revision audit

Use Python3.11+ and requirements.txt; Windows Arial/Poppler for visual QA. Run from repository root. Raw data and questionnaire/manuscript stay local and require author access, not bundled. Replace local paths in report_package.py/reference_audit.py for document audit; analysis accepts --data. Historical preparation/AME/screen dependencies are inherited in this branch. No previously stored respondent data is loaded/exported by the new reporting scripts.

```text
python 消费调查/results/nc_revision_audit/run_revision.py --data <authorized_raw.dta>
python 消费调查/results/nc_revision_audit/secondary.py --data <authorized_raw.dta>
python 消费调查/results/nc_revision_audit/reference_audit.py
python 消费调查/results/nc_revision_audit/figures.py
python 消费调查/results/nc_revision_audit/report_package.py
python 消费调查/results/nc_revision_audit/verify_package.py --data <authorized_raw.dta>
```

Reference audit makes network requests to publisher-deposited Crossref metadata (proxy configuration in script may be removed for another machine), with bounded claim scopes; reference metadata can change. Online NC/census audit is dated2026-10-03. Seed/fold/multiplicity settings are in manifest and scripts. Do not edit the saved manifest after examining results. All numerical exports are aggregate. qa/ renders are ignored; no IDs/raw rows/fold assignment release. NOT FEASIBLE and unresolved author items are not passed tests. See NC_REVISION_RESULT.md for finalB decision. No further exploratory work follows.
