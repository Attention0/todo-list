# ICLR 2026 idea feasibility audit

阅读顺序：FEASIBILITY_MATRIX → ASSIGNMENT_IDENTIFICATION → CORE_CONSTRUCTS → IDEA_1–8 → PRIORITY_TESTS → RESULT。

只研究ICLR2026；没有新增结果回归、其他年份conference数据、身份mapping、原始数据、email或凭据。代码只读本地原项目，输出aggregate diagnostics。public-probes可选，只访问匿名public链接/标准API，拒绝后停止，不使用notebook登录。

复现（在本目录执行；需Python+pandas）：

```text
python code/evidence_audit.py --project <LOCAL_ICLR_PROJECT> --out .
python code/evidence_audit.py --project <LOCAL_ICLR_PROJECT> --out . --public-probes
python code/validate.py --out . --inventory ../initial_audit/tables/file_inventory.csv --project <LOCAL_ICLR_PROJECT>
```

默认不请求网络；重新运行非public模式不会刷新上次public tables，应以RUN_METADATA的network_requests_enabled和run_time解释快照，不混作新的网络验证。原项目只读，输出路径必须位于独立audit目录。网络可用性与会后roster可能变化。本次public快照见RUN_METADATA.json和tables。全部输入历史hash复核见VALIDATION.json。
