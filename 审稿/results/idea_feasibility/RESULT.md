# RESULT — ICLR 2026 matching ideas feasibility

## Summary

8 ideas均完成clean-identification筛查。0 CLEAN NOW，0 CLEAN WITH SPECIFIC ADDITIONAL DATA；1/2/4保留条件关联，3B/5/6/7/8强因果主张当前不可可信识别。3A单独保留measurement fact。没有真实assignment instrument；补更多controls不改变结论。只用ICLR2026，不新增结果回归。

## Files changed

本目录：matrix、assignment audit、core constructs、8个idea报告、5项priority tests、README/RESULT/RUN_METADATA/VALIDATION、可复现只读code与aggregate tables。初轮initial_audit未改动。

## Key implementation decisions

三人自动+第四人AC手工不能作为准随机设计；现公开18,054 reviewer不等于冻结eligible pool。strict pre2025机构交叠556个候选正例，缺完整负例；无validated publication corpus，expertise/portfolio留unknown而非弱代理。snapshot标签倒置与incident规则阻断自然pre/post。公开API样本403后不绕权限。没有将日志“缺失”解释为制度“从未存在”。

## Testing performed

已实际运行全本地main/profile/current review availability、dated institution overlap、missingness selection；公开2026 roster及匿名权限/3-link出版availability probes。预期权限拒绝与URLError记录为失败/未验证，不声称通过。validator检查构念边界逻辑、8 verdict与必需文件、aggregate privacy扫描和原23文件hash只读性，实际结果见VALIDATION.json。未运行不可定义样本的balance/RD/placebo/future-edge或mechanism regression。

## Acceptance Criteria

- 每个idea都有estimand、actual variation、assignment、危险confound及可测/可差分判断、fatal objection、specific data、kill/support test与verdict。
- assignment每个candidate shock列明rule、running variable、threshold、N、jump、balance；未观察值明确NA，末句按WORK原文。
- 三构念的cutoff/definitions/coverage/validation/leakage全部报告，缺输入不伪造结果。
- 5 priority tests按信息价值排列，实际执行与待数据明确区分。
- 仅code/aggregate/docs提交到规定路径；无原始身份或private rows。

## Known issues

无冻结eligibility/affinity/capacity/override或随机化日志；publication probe未成功、无validated E/C；完整dated proximity缺失；review edit权限样本失败、正常chronology与meta/decision本地缺失。因果不可识别是本轮审计结果，不应以新增回归补救。

## Branch

feature/iclr-initial-audit-20261003

## Commit SHA

本报告随audit implementation commit提交。确切immutable SHA在紧接其后的PUBLICATION.json记录，避免文件包含自身SHA的不可能循环。

## PR

https://github.com/Attention0/todo-list/pull/18 （更新现有PR，不merge）
