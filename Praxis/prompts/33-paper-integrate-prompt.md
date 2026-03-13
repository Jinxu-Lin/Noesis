# Skill: Paper Integration & Editing (编辑整合) — Phase P4

## 触发场景
P3 审查完成（或 P5 revise 回退），需要整合审查意见、修改章节、输出完整论文。

## 输入判断

Agent 首先判断本次执行属于哪种模式：

| 模式 | 判断条件 | 额外输入 |
|------|---------|---------|
| **首次整合** | 不存在 `Papers/review.md` | P3 critique 报告 |
| **P5 Revise 回退** | 存在 `Papers/review.md` | P5 终审意见 |

**基础输入（所有模式共用）**：
- `Papers/sections/` — 各章节文件
- `Papers/critique/summary.md` — P3 审查汇总
- `Papers/outline.md` — 大纲
- `Papers/notation.md` — 符号表

## 执行流程

### Step 1: 制定修改计划

根据审查意见（P3 critique 或 P5 review），制定修改计划：

**1.1 问题分类与优先级排序**

将所有审查问题分为三类，按优先级处理：

| 优先级 | 类别 | 描述 | 处理方式 |
|--------|------|------|---------|
| P0 | **致命性问题** | 逻辑错误、数学推导错误、数据错误 | 必须立即修复，可能需要重写整段 |
| P1 | **结构性问题** | 叙事断裂、论证不充分、贡献与实验不对齐 | 需要较大改动，可能跨章节联动 |
| P2 | **表达性问题** | 语言不精确、notation 不一致、冗余/简略 | 局部修改，不影响论证结构 |
| P3 | **润色类问题** | 语法、格式、caption 改进 | 最后统一处理 |

**1.2 跨章节影响分析**

对每个 P0/P1 问题，分析修改的连锁反应：
- 修改 Method 的公式 → 需要同步更新 notation.md 和 Experiments 中引用该公式的地方
- 修改 Introduction 的 contribution 表述 → 需要同步更新 Abstract 和 Conclusion
- 修改实验分析 → 需要检查 Introduction 中对应的 claim 是否还成立
- 添加新 baseline / 新实验 → 标注为"无法仅通过论文修改解决"

**1.3 "不修改"的判断**

并非所有审查意见都需要采纳。以下情况可以不修改，但需要记录理由：
- 审查意见基于对方法的误解（说明是表达问题还是审查错误）
- 审查意见要求超出论文范围的实验（记录为 future work）
- 不同审查角色的意见相互矛盾（选择更合理的一方并说明理由）

### Step 2: 逐章节修改

按修改计划逐一修改 `Papers/sections/` 中的文件。

**修改原则**：

- **最小侵入原则**：每次修改只改需要改的部分，不做无关的"顺手"修改。大范围重写容易引入新问题
- **保持叙事流不断裂**：修改某段后，检查与前后段的衔接是否仍然通顺。添加内容时注意过渡句
- **修改追踪**：对每个修改，在心中记录修改原因（对应哪条审查意见）。如果某个修改不对应任何审查意见，三思是否必要
- **符号一致性**：任何新增符号都更新 `Papers/notation.md`
- Minor 问题也要处理（语言润色、格式统一等）——它们累积起来严重影响论文的"专业感"

**各章节的修改要点**：

- **Method**：修改公式时确保推导链不断裂；新增 motivation 时与 Introduction 的 gap 对齐；如果 reviewer 说"不够清晰"，先加 intuition 再加细节
- **Experiments**：补充分析时关注 "why" 而非 "what"；如果被指出 cherry-picking，增加全面的结果展示；如果被指出 baseline 不公平，明确说明实验设置
- **Introduction**：修改 contribution 表述时确保与 Method/Experiments 对齐；调整 gap 描述时保持与 Method motivation 的因果关系
- **Related Work**：补充遗漏引用时，不要简单追加，而是融入已有的主题分组
- **Abstract**：几乎总是需要最后重新检查，确保与修改后的正文一致

### Step 3: 组装完整论文

将修改后的各章节合并为完整的论文文档 `Papers/paper.md`：

```markdown
# [论文标题]

## Abstract
[from sections/abstract.md]

## 1. Introduction
[from sections/intro.md]

## 2. Related Work
[from sections/related_work.md]

## 3. Method
[from sections/method.md]

## 4. Experiments
[from sections/experiments.md]

## 5. Conclusion
[from sections/conclusion.md]

## References
[参考文献列表]
```

### Step 4: 精炼 Abstract

全文定型后，重新审视并精炼 Abstract：
- 确保与正文内容完全一致（修改可能导致 Abstract 过时）
- 包含核心数值结果（如 "improves by X% on dataset Y"）
- 150-250 词
- 删除任何正文中已删除或修改的 claim

### Step 5: 全文自检

| 检查项 | 方法 |
|--------|------|
| 叙事一致性 | Introduction 的 claim 全部被 Experiments 覆盖？ |
| 贡献完整性 | research/contribution.md 中每个贡献都被充分论证？ |
| 无凭空内容 | 论文是否引入了研究文档中没有的新内容？ |
| 图表自包含 | 每个图表的 caption 足够独立理解？ |
| 逻辑自洽 | Intro → Method → Experiments → Conclusion 逻辑链通顺？ |
| 符号一致 | 全文符号与 notation.md 一致？ |
| 审查意见覆盖 | 所有 Critical/Major 问题都已处理？ |
| 数字一致 | Abstract/Introduction/Experiments/Conclusion 中同一数字是否一致？ |
| 交叉引用 | 所有 "as shown in Table X" / "see Figure Y" 引用是否正确？ |

### P5 Revise 模式的额外步骤

如果是从 P5 回退的修订：
1. **优先处理 P5 review 中的问题**，不重新做全面修改
2. 阅读 `Papers/review.md`，逐条定位问题
3. **针对性修改，保持其他已稳定的内容不变**——这一点极其重要。P5 Revise 的目标是修复特定问题，不是重写论文。过度修改可能引入新问题导致无限循环
4. 如果 P5 指出了"需要补充实验"的问题，在修改计划中标注为"无法在本轮解决"，但尽量通过改善实验分析、增加 discussion 来部分缓解
5. 更新 `Papers/paper.md`

## AI Co-Author 关键行为
- 修改要**精准对应**审查意见，不做无关修改
- 保持跨章节的叙事一致性
- 学术语言标准：精确、客观、简洁
- **不遗漏 Minor 问题**——它们影响整体质量感
- Revise 模式要**最小修改原则**——只改需要改的
- **修改后重读**：每个章节修改完后，从头到尾重读一遍该章节，确保修改没有破坏原有的流畅性
- **不引入新问题**：每个修改都要自问"这个修改是否会被下一轮审查指出新问题？"

## 输出
- `Papers/sections/*.md` — 更新后的各章节文件
- `Papers/paper.md` — 完整论文
- `Papers/notation.md` — 更新后的符号表

## Exit Criteria
- [ ] 所有 Critical 和 Major 审查问题已处理（或标注了"无法仅通过改写解决"的理由）
- [ ] 完整论文 `paper.md` 已生成
- [ ] Abstract 已精炼，包含核心数值结果，与修改后正文一致
- [ ] 全文自检通过
- [ ] 符号表已更新
- [ ] 修改未引入新的叙事断裂或逻辑矛盾
