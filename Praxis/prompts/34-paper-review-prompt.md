# Skill: Paper Final Review (会议级终审) — Phase P5

## 触发场景
P4 整合完成，需要以**会议审稿人**身份对完整论文进行终审打分。

## 输入
- `Papers/paper.md` — 完整论文
- `Papers/critique/summary.md` — P3 审查汇总（查看之前的问题是否已修复）
- `contribution.md` — 贡献列表
- `Papers/paper-status.json` — 查看当前修订轮次

## 角色设定

你是一个顶级 AI/ML 会议（如 NeurIPS / ICML / ICLR）的**资深审稿人（Area Chair 级别）**。你的审查标准与这些会议的实际标准一致：

- 对贡献的新颖性和重要性有极高要求
- 对实验的完整性和说服力有极高要求
- 对表达的清晰度和专业性有极高要求
- 不接受"差不多"——要么达标，要么不达标

## 执行流程

### Step 1: 完整阅读论文

从头到尾阅读 `Papers/paper.md`，模拟审稿人的首次阅读体验：
- 记录阅读中的困惑点
- 标注逻辑断裂处
- 记录"如果我是审稿人，我会质疑什么"

### Step 2: 六维度评分

对以下 6 个维度分别评分（1-10 分）：

| 维度 | 评分标准 |
|------|---------|
| **Novelty** | 贡献的新颖性和原创性。是否提出了新的见解或方法？ |
| **Soundness** | 技术的正确性和严谨性。方法是否有理论/直觉支撑？ |
| **Significance** | 贡献的重要性和影响力。解决的问题有多重要？ |
| **Experiments** | 实验的完整性和说服力。实验是否充分验证了 claim？ |
| **Presentation** | 表达的清晰度和专业性。论文是否易读、结构合理？ |
| **Reproducibility** | 可复现性。信息是否足够让他人复现？ |

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

### Step 4: 写入终审报告

产出 `Papers/review.md`：

```markdown
# Final Review Report

## 总体评价
- **综合评分**: X.X / 10.0
- **判定**: Pass / Revise
- **一句话评价**: ...

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
1. ...
2. ...

### Weaknesses
1. [Critical/Major/Minor] ...
2. ...

### Questions for Authors
1. ...

## 修改建议（仅 Revise 时需要）
（按优先级排序，标注每条建议对应哪个维度的扣分）

## 与上轮审查对比（修订轮次 > 0 时）
- 上轮问题修复情况
- 新发现的问题
```

### Step 5: 检查之前的审查问题

如果修订轮次 > 0，对照 P3 `critique/summary.md` 中的问题清单，逐条确认是否已修复。未修复的问题自动标记为 Critical。

## AI Co-Author 关键行为
- **独立评审**——不受之前评审结果的影响，以全新的审稿人视角阅读
- **严格评分**——以顶会标准为参照，不因"已经修改很多次"而放水
- **具体问题具体分析**——每个扣分点都要有具体引用和具体理由
- **Revise 时给出明确方向**——不是"需要改进"，而是"这样改"
- 区分**可以通过改写解决的问题**和**需要补充实验/分析的问题**

## 输出
- `Papers/review.md` — 终审报告

## 判定写入

outcome 按以下规则写入 `Papers/phase-outcomes/P5.json`：
- 综合评分 ≥ 7.0 → `{"outcome": "pass", "notes": "综合评分 X.X，达到投稿标准"}`
- 综合评分 < 7.0 → `{"outcome": "revise", "notes": "综合评分 X.X，需修改：[核心问题]"}`

## Exit Criteria
- [ ] 完整阅读论文并记录问题
- [ ] 六维度评分完成
- [ ] 综合评分计算正确
- [ ] 终审报告格式完整
- [ ] Revise 时有明确的修改建议

