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

1. 列出所有 Critical 和 Major 问题
2. 对每个问题确定修改方案
3. 标注跨章节影响（修改一处可能需要同步修改其他章节）
4. 如果存在**需要补充实验**的问题，在修改计划中标注为"无法仅通过论文修改解决"

### Step 2: 逐章节修改

按修改计划逐一修改 `Papers/sections/` 中的文件：

- 对每个修改，记录修改原因（对应哪条审查意见）
- 修改时保持叙事一致性——一处改动可能需要连锁修改其他章节
- **符号一致性**：任何新增符号都更新 `Papers/notation.md`
- Minor 问题也要处理（语言润色、格式统一等）

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
- 确保与正文内容完全一致
- 包含核心数值结果（如 "improves by X% on dataset Y"）
- 150-250 词

### Step 5: 全文自检

| 检查项 | 方法 |
|--------|------|
| 叙事一致性 | Introduction 的 claim 全部被 Experiments 覆盖？ |
| 贡献完整性 | contribution.md 中每个贡献都被充分论证？ |
| 无凭空内容 | 论文是否引入了研究文档中没有的新内容？ |
| 图表自包含 | 每个图表的 caption 足够独立理解？ |
| 逻辑自洽 | Intro → Method → Experiments → Conclusion 逻辑链通顺？ |
| 符号一致 | 全文符号与 notation.md 一致？ |
| 审查意见覆盖 | 所有 Critical/Major 问题都已处理？ |

### P5 Revise 模式的额外步骤

如果是从 P5 回退的修订：
1. **优先处理 P5 review 中的问题**，不重新做全面修改
2. 阅读 `Papers/review.md`，逐条定位问题
3. 针对性修改，保持其他已稳定的内容不变
4. 更新 `Papers/paper.md`

## AI Co-Author 关键行为
- 修改要**精准对应**审查意见，不做无关修改
- 保持跨章节的叙事一致性
- 学术语言标准：精确、客观、简洁
- **不遗漏 Minor 问题**——它们影响整体质量感
- Revise 模式要**最小修改原则**——只改需要改的

## 输出
- `Papers/sections/*.md` — 更新后的各章节文件
- `Papers/paper.md` — 完整论文
- `Papers/notation.md` — 更新后的符号表

## Exit Criteria
- [ ] 所有 Critical 和 Major 审查问题已处理
- [ ] 完整论文 `paper.md` 已生成
- [ ] Abstract 已精炼，包含核心数值结果
- [ ] 全文自检通过
- [ ] 符号表已更新

