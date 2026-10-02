# Nature main-figure package - result

已按 `NATURE_FIGURES_WORK.md` 完成四张统一风格主图，输出在 `results/nature_main_figures/`。仅使用 PR9-12 范围内已批准的汇总结果；没有读取 respondent-level data、重跑模型、改样本、改 estimand、新增 smoothing/moderator 搜索或修改 manuscript。

| 主图 | 布局与信息 |
| --- | --- |
| Figure1 | 严格1×3：原始 ordinal category、midpoint-coded stated MPC、Top75；Cash/Food/Medical 九格均值及原有95% CI |
| Figure2 | 1×2：Cash 与 equal-weight Restricted 的 midpoint / Top75 曲线；Restricted 明确为派生对比 |
| Figure3 | 1×2：any spending 对比 Top75；仅标 Cash 尾部端点13.4%与5.3%，不声称 tail-specificity 已建立 |
| Figure4 | 1×2＋四类变量 summary strip：六族最小 BH q、全部可估计 q 的浅色 rug、每族0/150发现 |

Figure4 采用任务书第25节允许的 compact family-minimum-q 方案，而不是混合不同单位的 scalar coefficients、category contrasts 和 omnibus statistics 做排名。完整900条主要检验仍在 source CSV，详细原始 p/interaction 图保留为 Extended Data6；不挑 nominal p-value 故事，不把 null 当 equivalence。

四张主图和六张 Extended Data 均有 vector PDF、editable-text SVG、600dpi PNG。另有四页合并 PDF、2×2 contact sheet、13个 source/audit CSV、主文与 Extended Data captions、style guide、source manifest、逐图审计、可编辑制图脚本与核验脚本。ED1-6 分别为 threshold profile、relative scales、finite specification curve、share vs implied yuan、六档分布、all-X detailed screen；ED5 同时为 supplementary full distribution。

## Exact approved inputs

- `results/mpc_size_curve/fig1_source.csv`
- `results/mpc_size_curve/fig2_source.csv`
- `results/mpc_size_curve/fig3_source.csv`
- `results/mpc_final_strengthening/figA_source.csv`
- `results/mpc_final_strengthening/figB_source.csv`
- `results/mpc_final_strengthening/figC_source.csv`
- `results/mpc_final_strengthening/figD_source.csv`
- `results/mpc_final_strengthening/figE_source.csv`
- `results/mpc_allx_screen/all_screen_results.csv`
- `results/mpc_allx_screen/family_summary.csv`
- `results/mpc_allx_screen/subjective_objective_summary.csv`

每个输入的 SHA256、最后来源 commit、每个绘图统计的1-based data row 均已记录。Ordinal CI 仅照 PR9 已批准的 mean±1.96SE 图例做展示算术；其余 CI 原样复制，不引入新 inferential procedure。PR11 是分支依赖及证据背景，不需要重复其分析。

## Quality control and limitations

231项自动核验通过；11个输入哈希不变，绘图数值/CI/q/编码/N 与来源一致，六档比例完整，PDF无 raster image、SVG文字可编辑、180mm 页面和600dpi导出合格，合并页保持原矢量内容。Poppler 渲染14页用于检查，主图/Extended PNG、最终 PDF proofs、contact sheet 和灰度 proof 已目视检查；页边 panel 字母、参考线重复标签已修正。制图器还强制内容 bounds 全部位于固定页面内。

主图按180mm full width 设计；提供89-90mm QA reduction previews，但1×3和多 panel 图不推荐单栏缩印。未安装 CVD simulator，未声称通过 CVD simulation；以灰度、不同 marker/line styles 和 hollow Restricted 确保不只依赖颜色。保留原有 suggestive scope、tail-specificity未建立及 all-X non-rejection 非 equivalence 的解释边界。

新 PR stacked on PR12 `feature/mpc-allx-screen`，不自动 merge。此轮停止于视觉交付，没有新实证或 headline。
