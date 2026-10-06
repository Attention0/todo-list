# Five priority tests, ranked by information value

仅以下5项。顺序体现是否能结束整个识别搜索，而非idea品味。当前没有“promising clean causal”设计；前两项必须先过，不能用大量评分回归替代。每项区分已运行availability gate与尚未获数据的实证检验。

1. **Actual assignment randomization gate（1/2/4/5/7）**。取得冻结pool、逐paper候选/COI、bids/affinity、实际solver参数/概率/seed、capacity、auto/manual/replacement日志。复现真实分配与概率，再在同eligibility stratum检验预处理topic、seniority、paper属性、前期harshness平衡；冻结paper属性作为placebo。若AC discretion/缺候选集无法排除，kill assignment causal。真实随机tie内类型变动且平衡支持，只能升级到设计证据，仍需exclusion。**已运行**公开roster与本地字段/slot availability审计；未运行balance，因为没有实际identifying sample。指南确认第四人手工，否定“人数即可随机”。

2. **Independent chronology gate（3B/8）**。合法review edits+原始snapshot+meta/decision逐条恢复提交、正常讨论、rollback/freeze/AC transfer，独立对照日期。若无法区分原始与reset，或只剩新AC回溯判断，kill常规influence。若恢复一个独立未污染窗口，仅解决时序，不解决意见采纳内生性。**已运行**current-note字段与初轮lineage核验，匿名edits样本403后停止；没有虚构正常revision treatment。

3. **Pre-treatment measurement/coverage gate（全部）**。先补身份验证的dated publication corpus与freeze paper；模型/词表先冻结，计算max/top-5/centroid/lexical，dated network/institution与portfolio。盲评identity/topic；报告coverage分层及missingness选择；leave-one-definition-out。未来edge作为敏感时点diagnostic而非treatment，解释post-treatment可能性。若结果只依赖undated relation/单一模型/后期citation，kill相应构念；若多定义一致且验证充分，只支持测量可靠。**已运行**全profile字段、严格bounded institution overlap、missing-ID outcome/area诊断、3-link public publication probe；0 validated E/C，缺完整negative P，因此尚未计算embedding或未来edge。

4. **Actual threshold/first-stage gate（1/4/5，条件触发）**。只有日志显示真实2026 cutoff才获取running variable、规则值、阈值两侧eligible/unassigned候选、near-cutoff N、密度/操纵与预处理balance、assignment probability jump。未知COI年限不能抄平台默认值。若无实际jump/共同支持或assigned-only截断，则kill RD/IV。若有规则且复现，评估paper-level policy effect；仍不得宣称随机化了friendship。**未运行**：未发现实际规则/near-cutoff sample，所有N/jump/balance=NA。

5. **Competing-mechanism isolation gate（2/3B/5/6/7/8）**。在通过前述gate后，检验target X变化是否同时改变technical knowledge、workload/time、identity exposure、pressure/AC政策。独立盲评unique且正确technical issues/质量benchmark与实际身份接触记录，用预指定方向的反证：收益全由individual E解释→kill纯团队互补；严厉只对应正确技术批评→kill战略评价；visibility变化同时带来pressure/信息→kill纯status channel；仅预测final label而无quality truth→kill“应有权重”。高分与更多技术信息并存并不排除favoritism。**未运行机制回归**：没有能隔离路径的已观察冲击，也没有technical gold standard。没有独立路径隔离则停止机制主张，不能以负结果或controls通过此gate。
