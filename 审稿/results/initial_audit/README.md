# Initial ICLR audit deliverables

按顺序阅读 PROJECT_AUDIT、DATA_DICTIONARY、BLINDNESS_DESIGN、MATCHING_DESIGN、EMPIRICAL_FACTS、RESEARCH_OPTIONS；RESULT记录测试与发布。

所有代码与结果局限于本目录，原始项目read-only。tables只包含统计量/字段名/输入相对文件名与fingerprints；不含person/paper/review行级数据，未复制原notebooks或docx。figures/distributions.svg为聚合图。

## Reproduce locally

Python 3.12.4，pandas 2.2.2，numpy 1.26.4，statsmodels 0.14.2，matplotlib（实际版本见VALIDATION）。不需要联网、模型下载或原项目登录信息。

```powershell
python code/audit.py --project 'G:\桌面\科研\项目-iclr审稿' --out .
python code/coverage.py --project 'G:\桌面\科研\项目-iclr审稿' --out .
```

可以换成自己合法持有的同schema local project路径。原始identity snapshot获取步骤不可公开复现，本目录不提供或重新抓取身份名单。

Schema：统计字段见DATA_DICTIONARY；empty/nested missing定义见报告；raw原文件SHA256保存在tables/file_inventory.csv。RUN_METADATA含实际运行版本与checks。read-only验证与发布内容扫描见VALIDATION。
