# Validation actually executed

- unchanged_original_files: 23
- sample_and_distribution_totals: pass
- streaming_parser_chunk_boundaries_and_truncation: pass
- missing_history_not_filled_and_shanghai_conversion: pass
- within_transform_matches_dummy_paper_FE: pass
- publication_privacy_scan: pass; no person IDs, emails or credential literals
- matplotlib_version: 3.8.4

审计完整运行成功；早期运行曾遇内存不足，已改为内容指纹与仅保留相关ID的集合后全量重跑成功。Supplemental coverage曾因null profile中断，修复后成功重跑。未重跑原网络采集、登录或写源文件的notebooks；旧图表均traced only。
