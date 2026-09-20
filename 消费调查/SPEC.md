# 消费调查项目 — Research Specification

## 1. 当前研究目标

本项目使用“社会心态小调查”中的随机情景实验，研究政府转移支付的形式与金额如何影响居民的边际消费反应，并进一步判断能否形成具有一般经济学意义的研究问题。

当前问卷的核心实验是一个 3×3 随机设计：

- 转移形式：
  1. 无限制现金补贴；
  2. 食品/日用品消费券（6个月有效，不能提现）；
  3. 医保个人账户注入（长期有效，只能用于医疗相关支出）。

- 转移金额：
  - 200 元；
  - 1000 元；
  - 5000 元。

每位受访者仅随机看到其中一个版本，并回答收到该补贴后“总消费预计会比原计划多花多少钱”。回答为 6 档消费比例区间。

本阶段目标不是尽快确定论文结论，而是回答：

> 数据是否真的支持一个有识别力、有机制含义、可以继续扩展到 JDE 水平的研究设计？

---

## 2. 当前最值得检验的经济学问题

### A. Fungibility / cash equivalence

标准消费者理论下，如果定向转移是 inframarginal 的，即受访者本来在对应类别上的消费已经超过补贴额度，则用途限制原则上不应改变预算集中的最优选择：

Cash ≈ In-kind transfer.

因此核心问题是：

> 当用途约束理论上并不 binding 时，现金、食品券和医疗账户是否仍然产生不同的消费反应？

若仍有差异，则可能指向：
- mental accounting；
- labeling；
- salience；
- commitment / spending cue；
- 对不同“账户”的非完全可替代认知。

### B. Bindingness

问卷同时观测：
- 家庭月度食品支出；
- 过去一年家庭自费医疗支出。

因此可以初步研究：

> 转移金额相对于家庭原有对应类别支出的大小，是否决定 restricted transfer 与 cash 的差异？

食品券尤其适合，因为存在 200 / 1000 / 5000 元三个金额，且有效期为 6 个月。

医疗账户的 baseline medical expenditure 只能作为不完全 proxy：账户长期有效，而问卷只问过去一年医疗支出，因此不能机械解释为严格的预算约束测试。

### C. Precautionary saving / earmarked wealth

医保个人账户长期有效且可覆盖未来医疗风险，因此它可能不仅是“受限消费券”，也可能是一种 earmarked precautionary asset。

候选机制：
- 对社会保障信心较低的人；
- 应急流动性较弱的人；
- 医疗支出较高的人；
- 对未来更悲观的人；

收到医疗账户注入后，现金预防性储蓄需求可能发生不同变化。

这是候选机制，现阶段不得在数据审计前把它当作已证实结论。

### D. Welfare vs stimulus（后续扩展）

当前问卷只测 stated consumption response，并没有直接测：
- transfer preference；
- willingness to accept；
- cash equivalent；
- welfare。

因此现有数据不能直接回答“居民更喜欢现金还是实物”。

若第一轮数据有强烈且可信的事实，后续可考虑补充 incentivized choice / cash-equivalent experiment，研究：

> 更能刺激消费的受限转移，是否同时给受助者带来福利损失？

---

## 3. 当前阶段的证据纪律

1. 先审计随机化、样本质量和 outcome，再讲机制。
2. 不因为某个 treatment cell 均值显著就立即形成论文故事。
3. 主要结果应首先以原始 6 档 ordered outcome 展示；把区间 midpoint 映射为 MPC 只能作为直观化/稳健性分析。
4. 区分：
   - 设计直接识别的 causal treatment effects；
   - 基于 baseline characteristics 的异质性；
   - 仅具相关性的机制变量。
5. 食品支出是“月度分档”，食品券期限为 6 个月，bindingness 只能在合理转换和区间边界下谨慎构造。
6. 医疗支出是“过去一年自费支出”，医保账户长期有效，不能把二者直接视为完全匹配的预算约束。
7. 若数据中 treatment assignment 并非真正随机或存在大量异常记录，应优先报告问题，而不是继续跑回归。
8. 不将原始调查数据、个人级记录或可能敏感的信息直接提交到 GitHub；GitHub 中只保存研究说明、代码和汇总结果，除非研究者明确要求。

---

## 4. 本阶段成功标准

完成本轮数据审计后，应能明确回答：

1. 有效样本量是多少？九个随机 cell 各有多少人？
2. 随机化是否执行正确？baseline characteristics 是否平衡？
3. 6 档消费反应的整体分布和 cell-level 分布是什么？
4. transfer type、amount 以及二者 interaction 是否有明显且稳健的 reduced-form pattern？
5. 是否存在严重 floor / ceiling effect？
6. 食品券结果是否随“transfer / baseline food spending”出现有理论含义的变化？
7. 医疗账户是否呈现与食品券不同的模式？
8. 哪些异质性模式最值得进一步追踪，哪些只是噪声？
9. 当前样本和 outcome 是否有足够 power 支撑主问题？
10. 数据最致命的局限是什么？下一轮问卷最值得补哪几个变量或 treatment？

最终目的不是证明某个预设故事，而是决定：
- 哪条论文主线值得继续；
- 哪条应放弃；
- 下一轮实验应如何设计。
