# ni-haixia-perspective

一个基于倪海厦公开材料蒸馏的 Codex Skill，用于分析其可验证的思维框架、表达特征与历史立场。

本项目不是倪海厦本人复刻、数字分身或医疗服务，也不隶属于倪海厦家属、汉唐中医或任何相关机构。

## 能做什么

- 用六个心智模型和八条决策启发式分析问题；
- 区分本人署名材料、公开整理稿、原声切片与第三方转述；
- 核查公开主张的来源、归属、置信度与待验证项；
- 在涉及现实健康问题时，强制分离“历史人物观点”和“当前医学证据”。

## 安装

macOS / Linux：

```bash
git clone https://github.com/Fangx-AI/ni-haixia-perspective.git ~/.codex/skills/ni-haixia-perspective
```

Windows PowerShell：

```powershell
git clone https://github.com/Fangx-AI/ni-haixia-perspective.git "$env:USERPROFILE\.codex\skills\ni-haixia-perspective"
```

安装后可直接说：

```text
用倪海厦视角分析这个问题……
```

或显式调用 `$ni-haixia-perspective`。

## 公开发行版内容

- `SKILL.md`：核心路由、六个心智模型、八条启发式、表达 DNA 与安全边界；
- `agents/openai.yaml`：Codex 展示与调用配置；
- `references/research/`：六维研究摘要；
- `references/synthesis/`：心智模型验证和表达统计；
- `references/evidence/`：释义化主张账本及元数据化医学核验队列；
- `references/source-registry/`：8,058 条公开来源元数据及来源家族说明；
- `references/video-transcript-registry/`：300 条高传播视频索引和风险筛查，不含文稿；
- `references/timestamp-packs/`：10 个长视频研究包的来源、哈希、时间轴和证据指针，不含完整转写；
- `evals/eval-summary.json`：120 题行为评测与医疗安全评测摘要。

`PUBLICATION_MANIFEST.json` 记录公开版明确包含和排除的内容。

## 数据与版权边界

公开仓库不包含音频、视频、完整网页正文、完整字幕、ASR 文稿、500 段医学核验原文摘录或本机工作路径。视频标题、上传者、链接和来源网页信息属于公开元数据；原始内容权利仍归各自权利人所有。

自动转写产生的统计只用于检索覆盖度说明。未经回听校正，不能作为倪海厦逐字原话。

## 医学安全

本 Skill 不提供诊断、处方、剂量、针刺操作、停药、拒绝疫苗或替代治疗建议。历史观点与现代医学证据冲突时，现实安全和当前权威证据优先。详见 [DISCLAIMER.md](DISCLAIMER.md)。

## 验证状态

- Skill 结构校验：通过；
- 女娲质量检查：6/6；
- 行为评测：120/120；
- 来源标注：66/66；
- 不确定性标注：70/70；
- 医疗安全常规题与红队：118/118；
- 时间戳研究包独立复审：10/10。

这些结果验证 Skill 的规则执行，不证明任何历史医学主张正确。

## 致谢

本项目使用 [女娲 / Nuwa Skill](https://github.com/alchaincyf/nuwa-skill) 的人物深度蒸馏方法生成，并在公开发行前执行了来源、版权、医学安全和行为评测审计。

## 许可证

项目原创的 Skill 指令与研究性整理采用 MIT License。第三方名称、商标、标题、链接、来源元数据及原始材料不因收录而获得重新授权，详见 [NOTICE.md](NOTICE.md)。
