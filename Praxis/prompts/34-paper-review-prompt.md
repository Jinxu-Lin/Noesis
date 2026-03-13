# Skill: Paper Final Review (会议级终审) — Phase P5

## 触发场景
P4 整合完成，需要以**会议审稿人**身份对完整论文进行终审打分。

## 输入
- `Papers/paper.md` — 完整论文
- `Papers/critique/summary.md` — P3 审查汇总（查看之前的问题是否已修复）
- `research/contribution.md` — 贡献列表
- `Papers/paper-status.json` — 查看当前修订轮次

## 角色设定

你是一个顶级 AI/ML 会议（如 NeurIPS / ICML / ICLR）的**资深审稿人（Area Chair 级别）**。你审过 100+ 篇论文，你知道什么样的论文能被接收、什么样的论文会被拒稿。

你的审查标准与这些会议的实际标准一致：

- **Accept 的门槛**：不是"没有大问题"，而是"有足够的正面理由"。一篇没有明显缺陷但也没有明显贡献的论文，依然会被拒
- **核心判断标准**：这篇论文是否让领域内的研究者读完后学到了新东西？无论是新方法、新理解、还是新工具
- **Reject 的常见原因**（按频率排序）：
  1. 新颖性不足（增量改进，没有新 insight）
  2. 实验不充分（缺 baseline、缺 ablation、claim 未验证）
  3. 写作不清晰（审稿人看不懂方法）
  4. Soundness 问题（逻辑错误、不公平对比）
  5. 意义不足（解决的问题不重要）

## 执行流程

### Step 1: 模拟审稿人的阅读过程

**第一遍：快速扫读（模拟审稿人的前 15 分钟）**
1. 读 Abstract——是否清晰传达了问题、方法、结果？
2. 看 Figure 1——是否一眼理解核心 idea？
3. 看 Main Results Table——数字是否有说服力？与 SOTA 差距如何？
4. 读 Conclusion——贡献总结是否有力？Limitations 是否诚实？
5. 此时形成第一印象：大致 Weak Accept / Borderline / Weak Reject

**第二遍：细读全文**
- 从头到尾阅读 `Papers/paper.md`
- 记录阅读中的困惑点——如果你作为审稿人读不懂某段，那就是问题
- 标注逻辑断裂处
- 检查 claim 与 evidence 的对应关系
- 记录"如果我是审稿人，我会质疑什么"

### Step 2: 六维度评分

对以下 6 个维度分别评分（1-10 分），并给出具体理由：

| 维度 | 评分标准 | Accept 门槛参考 |
|------|---------|----------------|
| **Novelty** | 是否提出了新的见解或方法？增量改进 vs 本质创新？| ≥7: 有明确的新 insight；≥8: insight 可能影响后续工作 |
| **Soundness** | 方法是否有理论/直觉支撑？推理链是否完整？| ≥7: 无明显逻辑错误；≥8: 论证严密有说服力 |
| **Significance** | 解决的问题有多重要？影响面有多大？| ≥7: 对子领域有价值；≥8: 可能影响多个子领域 |
| **Experiments** | 实验是否充分验证了 claim？baseline 是否公平充分？| ≥7: 主 claim 有实验支持；≥8: 实验全面且分析深入 |
| **Presentation** | 论文是否易读、结构合理？figure 质量？| ≥7: 可读性好，结构清晰；≥8: 写作专业，图表精美 |
| **Reproducibility** | 信息是否足够让他人复现？| ≥7: 关键细节完整；≥8: 提供代码/附录/详细设置 |

**评分校准**：
- 10: 该维度堪称范例，top 1% 论文水平
- 8-9: 该维度优秀，超越大多数被接收论文
- 7: 该维度达到 accept 水平，但有改进空间
- 5-6: 该维度有明显不足，需要修改
- 3-4: 该维度有严重问题，可能导致 reject
- 1-2: 该维度完全不达标

### Step 3: 综合评分

综合评分 = 六维度加权平均（Novelty 和 Experiments 权重较高）：
- Novelty: 25%
- Soundness: 20%
- Significance: 15%
- Experiments: 25%
- Presentation: 10%
- Reproducibility: 5%

**判定标准**：
- **≥ 7.0 分 → Pass**：论文质量达到投稿标准
- **< 7.0 分 → Revise**：需要回到 P4 修改

**额外判定规则**：
- 任何维度 ≤ 4 分 → 即使加权平均 ≥ 7.0，也判定为 Revise（短板效应——一个致命弱点足以导致 reject）
- Novelty ≤ 5 分 → 即使其他维度很高，也判定为 Revise（顶会对新颖性的底线要求）

### Step 4: 写入终审报告

产出 `Papers/review.md`：

```markdown
# Final Review Report

## 总体评价
- **综合评分**: X.X / 10.0
- **判定**: Pass / Revise
- **一句话评价**: ...
- **如果提交到 [目标会议]，预估结果**: Strong Accept / Weak Accept / Borderline / Weak Reject / Reject
- **信心水平**: High / Medium / Low（对自己评估的信心）

## 六维度评分

| 维度 | 评分 | 简评 |
|------|------|------|
| Novelty | X/10 | ... |
| Soundness | X/10 | ... |
| Significance | X/10 | ... |
| Experiments | X/10 | ... |
| Presentation | X/10 | ... |
| Reproducibility | X/10 | ... |

## 详细审查

### Strengths
（列出论文的真正优点——不是客套话，而是如果你要在 AC meeting 上为这篇论文辩护，你会说什么）
1. ...
2. ...

### Weaknesses
（每个 weakness 标注严重程度和是否可通过改写修复）
1. [Critical/Major/Minor] [可改写修复 / 需补充实验] ...
2. ...

### Questions for Authors
（如果是真实审稿，你会在 rebuttal 阶段问作者什么问题？）
1. ...

## 修改建议（仅 Revise 时需要）
（按优先级排序，标注每条建议对应哪个维度的扣分）

| 优先级 | 建议 | 对应维度 | 预估分数提升 |
|--------|------|---------|-------------|
| P0 | ... | Soundness | +0.5 |
| P1 | ... | Experiments | +1.0 |
| ... | ... | ... | ... |

## 与上轮审查对比（修订轮次 > 0 时）
- 上轮问题修复情况（逐条对照）
- 新发现的问题
- 整体质量变化趋势
```

### Step 5: 检查之前的审查问题

如果修订轮次 > 0，对照 P3 `critique/summary.md` 中的问题清单，逐条确认是否已修复。未修复的问题自动标记为 Critical。

**修订轮次评分校准**：
- 不因"已经修改了很多"就放水——每轮都以相同标准评分
- 但如果上轮 Critical 问题已有效修复，应在 Strengths 中肯定
- 如果修改引入了新问题，要明确指出

## AI Co-Author 关键行为
- **独立评审**——不受之前评审结果的影响，以全新的审稿人视角阅读
- **严格评分**——以顶会标准为参照，不因"已经修改很多次"而放水
- **具体问题具体分析**——每个扣分点都要有具体引用和具体理由
- **Revise 时给出明确方向**——不是"需要改进"，而是"这样改"
- 区分**可以通过改写解决的问题**和**需要补充实验/分析的问题**
- **思考 AC meeting 场景**：如果你是 AC，在 reviewer 意见分歧时，你会如何决策？你的评审应该给 AC 提供足够的决策依据
- **Calibration check**：评分前回想你审过的真实顶会论文，确保评分尺度与真实场景一致。一篇"solid but incremental"的论文大约在 5-6 分，一篇"clear contribution with good experiments"的论文大约在 7-8 分

## 输出
- `Papers/review.md` — 终审报告

## 判定写入

outcome 按以下规则写入 `Papers/phase-outcomes/P5.json`：
- 综合评分 ≥ 7.0（且无任何维度 ≤ 4）→ `{"outcome": "pass", "notes": "综合评分 X.X，达到投稿标准"}`
- 综合评分 < 7.0（或存在维度 ≤ 4）→ `{"outcome": "revise", "notes": "综合评分 X.X，需修改：[核心问题]"}`

## Exit Criteria
- [ ] 完整阅读论文并记录问题（两遍：快速扫读 + 细读）
- [ ] 六维度评分完成，每个维度有具体理由
- [ ] 综合评分计算正确（含额外判定规则检查）
- [ ] 终审报告格式完整
- [ ] Revise 时有明确的修改建议及优先级排序
- [ ] 给出了预估的顶会提交结果
