# Hero Figure delivery

## 最终结构

采用用户首选的 **3×3 randomized-cell response atlas + midpoint summary curve**。上半部分九条同长度100% composition strips，行是Cash/Food/Medical，列是¥200/¥1,000/¥5,000；所有六档都保留，颜色仅编码MPC强度，>75%为最深色。下半部分复制已批准的midpoint均值与95% CI，三个金额位置与atlas对齐。配套完成三个同尺度panel的distribution-shift fingerprint，直接显示六档概率的¥5,000−¥200变化。

Hero exports为180×138mm，companion为180×79mm；均提供vector PDF、editable SVG、600dpi PNG、逐值溯源CSV和英文caption。全套在`results/mpc_hero_figure/`，另有audit、hash manifest、复现与验证脚本及423项通过记录。没有重复制作可选puzzle：PR #13的Figure2已完整承担该用途。

## 为什么比当前Figure1更适合作为引子

当前Figure1并行展示ordinal/midpoint/Top75三个口径，适合证明同一事实不依赖单一outcome表示；但读者仍需自行拼接“平均曲线下降”和“分布哪里变了”。新Hero先展示完整概率质量，再给出平均曲线，阅读路径直接是 **完整分布 → 平均反应**。Cash最深色尾部由13.4%到5.3%，而最浅色no-spending部分约27.3%到27.2%，无需先读模型表即可辨别现象；Food/Medical的尾部压缩较弱也在同一几何尺度上可见。

Fingerprint补充回答“哪些bin的份额更大/更小”，不是个人的档位迁移。Cash高尾端点下降8.10pp、Food2.46pp、Medical1.93pp；Cash第一档只下降0.08pp。均为冻结概率的展示性相减，没有新增估计、CI或显著性判断。

## 排版建议

**建议作为新的opening figure（首张主图），不是删除并完全替代原Figure1。** 原1×3图保留为紧随其后的三口径证据图，尤其不能因Hero仅总结midpoint而丢弃原ordinal主口径。最终图号由稿件编辑阶段决定；本轮不改manuscript或现有图。Companion可作为紧邻Hero的Extended Data分布诊断，避免两张主图重复讲同一事实。

## 证据纪律与验证

只读取PR #13封装的两个approved aggregate source CSV，保留PR #9/#10上游溯源；PR #11/#12既有结论不改变。来源hash生成前后不变；54个bin、9个均值/CI、18个概率差及样本量全部核验。423项自动检查通过，实际检查两张最终PNG、Poppler渲染PDF、灰度和缩小预览。完整宽度180mm是推荐排版，不承诺89mm可读。没有新增实证、raw data访问或上传、smoothing、individual transitions、理论曲线或尾部独占性声明。原有“mean/ordinal suggestive、direct tail-specificity未确立”的边界在caption/audit中保留。

## Git delivery

Branch: `feature/mpc-hero-figure`; stacked on PR #13 `feature/nature-main-figures`. Artifact commit: `ca177e3f6523f4f61f7a112437a4a8cfac74af08`. New PR: https://github.com/Attention0/todo-list/pull/14 . 已推送，未merge。Publication record另行提交，不记录自身hash。
