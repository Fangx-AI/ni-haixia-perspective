# 医案与临床日志索引

`case-index.json` 从全局来源注册表中的“医案/日志”记录生成，只保存标题、URL、来源层级、出处家族和核验状态，不复制病例全文。

## 检索方法

1. 用病名、症状或方剂搜索 `case-index.json` 的 `title`。
2. 优先选择 `source_tier = original_hantang_public_archive` 的记录。
3. 打开 `source_url` 阅读完整上下文；镜像记录须回看其声明的原始出处。
4. 抽取患者背景、诊断、并行治疗、辨证、干预、随访和缺失信息。
5. 医案只能说明“公开记录怎样叙述”，不能单独证明疗效，也不能直接复制为个人处方。

## 主题标签

- `cancer`
- `cardiovascular`
- `metabolic_renal`
- `autoimmune_musculoskeletal`
- `neurological`
- `reproductive_womens_health`
- `respiratory_ent`
- `digestive`
- `other`

## 重建

```bash
python scripts/build_case_index.py references/source-registry/global-source-registry.json cases/case-index.json
```

输出是确定性的；更新全局来源注册表后重新运行即可。
