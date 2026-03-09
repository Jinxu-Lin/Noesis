# Skill: Praxis Present（项目进展展示）

生成 `presentation.md`，一份供研究者与导师/合作者讨论的 read-friendly 项目进展总结。
支持冷启动（首次生成）和热启动（基于已有版本增量更新）。

---

## 核心设计原则

**导师读 presentation 的优先级与 AI 执行流水线相反。**

流水线顺序：Gap → Method → Experiment → Result
导师关注顺序：**当前进展 → 核心主张 → 悬而未决的问题 → 背景支撑**

因此 presentation.md 不是研究文档的线性摘要，而是**为"15分钟讨论"重新排列信息优先级的独立文档**。
最重要的 section 是 Open Questions，不是 Our Approach。

---

## Step 0：热启动检测

检查 `<project_path>/presentation.md` 是否存在：

**不存在（冷启动）**：
- 继续 Step 1，全量生成

**存在（热启动）**：
- 读取文件头部 YAML frontmatter，提取：
  - `last_phase_at_generation`（上次生成时的阶段）
  - `update_history`（版本历史）
- 读取当前 `pipeline-status.json`，确定当前阶段
- 计算"新产出文档"：上次生成后新增了哪些 phase-outcomes/*.json 和阶段文档
- 对每个 Section，判断：`rewrite`（内容完全变化）/ `update`（部分更新）/ `stable`（无需更改）
- 对 S4 Open Questions：读取上次版本中的 `[DECISION NEEDED]` 问题，检查是否在新 phase-outcomes 中被解决
- 继续 Step 1，只重写/更新需要变化的 Section

---

## Step 1：读取项目文档

根据文件是否存在**条件性读取**（不存在的文件跳过，不报错）：

**必读**：
- `<project_path>/pipeline-status.json` ← 当前阶段、历史、迭代次数
- `<project_path>/phase-outcomes/*.json` ← 各阶段完成状态和备注

**按存在情况读取**：
- `<project_path>/project-startup.md` ← P1 产出
- `<project_path>/contribution.md` ← 贡献跟踪
- `<project_path>/gap-analysis.md` ← P2 产出
- `<project_path>/gap-review.md` ← P3 产出（含评审意见）
- `<project_path>/method-design.md` ← P4 产出
- `<project_path>/method-review.md` ← P5 产出（含评审意见）
- `<project_path>/experiment-design.md` ← P6 产出
- `<project_path>/experiment-review.md` ← P7 产出（含评审意见）
- `<project_path>/Codes/code-todo.md` ← P8 产出
- `<project_path>/Codes/experiment-todo.md` ← P8 产出（实验 checklist）
- `<project_path>/iteration-log.md` ← 迭代历史（如有失败迭代）
- `<project_path>/CLAUDE.md` ← 项目名称、venue 目标

---

## Step 2：确定当前阶段和阶段权重

根据 `pipeline-status.json` 中的 `phase` 字段，确定内容重心：

| 当前阶段 | 内容重心 | 必须出现的 Section |
|---------|---------|-----------------|
| P1-P3 | 问题定义与 Gap 确认 | S0, S1, S4, S9 |
| P4-P5 | 方法设计与验证 | S0, S1, S2, S4, S5, S6, S9 |
| P6-P8 | 实验设计与实现规划 | S0, S1, S2, S3, S4, S5, S6, S9 |
| coding | 实验执行与结果 | S0, S1, S2, S3, S4, S5, S6, S7, (S8), S9 |
| paper_writing | 论文写作 | S0, S1, S2, S3, S4(轻量), S5, S6, S7 |
| P11/complete | 项目总结 | S0, S1, S2, S3, S5, S6, S7, (S8) |

S8 Iteration History 仅当 `iteration-log.md` 存在时出现。

---

## Step 3：生成各 Section

### 文件头部（YAML Frontmatter）

```yaml
---
project: [从 CLAUDE.md 提取项目名，或目录名]
version: v1  # 热启动时递增
generated_at: [今日日期]
current_phase: [当前阶段]
last_phase_at_generation: [当前阶段]  # 供下次热启动比对

update_history:
  - v1 | [日期] | phase: [阶段] | sections: all | trigger: initial

status_snapshot: [从 phase-outcomes/*.json 压缩生成，格式：P1:done | P2:done | P3:pass | ...]
---
```

---

### S0: Project Snapshot（状态快照）

**每次生成都完整重写此节。**

```markdown
## 📍 Project Snapshot

**项目**: [名称] | **阶段**: [当前阶段描述] | **目标**: [venue 和截稿日，若已知]
**本次更新**: [日期]  [热启动时追加：| 距上次 presentation: X 天]

**进展概括**（1-2句）：
[基于 pipeline-status.json 的 history 和 phase-outcomes 的 notes，提炼当前最重要的进展]

**今日议题**（优先级排序，来自 S4 的提炼）：
1. [DECISION] [最需要拍板的问题，一句话]
2. [INPUT] [需要导师领域知识的问题]
3. [UPDATE] [需要知晓的最新进展]
```

**内容来源**：pipeline-status.json、phase-outcomes notes、S4 内容的提炼

---

### S1: The Problem We're Solving（问题陈述）

**P3 Pass 后稳定；L3 Redesign 迭代回 P2 后需重写。**

```markdown
## The Problem We're Solving

**领域背景**（1句）：[领域 + 任务 + 重要性]

**现有方法的局限**（2-3句）：
[最强竞争方法] 在 [具体场景] 下存在 [具体问题]。
这个问题的根因是 [技术根因]。
定量上，这意味着 [metric 损失]（文献数据）。

**我们要解决的核心 Gap**：
> "[现有方法]做了X，但因为Y所以在Z场景下失效。"

**Research Questions**:
- RQ1: [精确表述]
- RQ2: [精确表述，如有]
```

**内容来源**：
- 主：`gap-analysis.md`（Gap 陈述节、根因分析节、Research Questions 节）
- 辅：`project-startup.md`（研究动机节）
- 注意：若 P3 曾有 Revise，使用最终修订版的 gap 陈述（不是初稿）

---

### S2: Our Approach（方法核心）

**仅在 P4 之后出现。P5 Pass 后稳定；L2/L3 迭代后更新。**

```markdown
## Our Approach

**核心 Idea**（1-2句，纯自然语言，无公式）：
[直觉性描述，非技术读者能理解]

**因果论证**：
Gap 根因是 [X] → 因此我们设计了 [Y] → 理论上这会带来 [Z]

**方法组件概览**：
| 组件 | 功能 | 解决什么子问题 |
|------|------|--------------|
| [组件 A] | [功能] | [子问题] |
| [组件 B] | [功能] | [子问题] |

**与现有方法的本质区别**（2句）：
与 [最相近方法] 相比，我们 [核心差异]，这带来了 [理论优势]。

[如有迭代历史] **当前方法版本**: v[N]（迭代详情见 S8）
```

**内容来源**：
- 主：`method-design.md`（概述节、因果论证节、组件列表、与已有方法对比节）
- 辅：`contribution.md`（方法贡献节）
- 辅（有迭代时）：`iteration-log.md` 最新 Entry 的"当前版本快照"

---

### S3: Validation Design（验证体系）

**仅在 P6 之后出现。P7 Pass 后稳定；coding 阶段根据实际结果可能局部更新。**

```markdown
## Validation Design

**验证逻辑**：
| RQ | 核心实验 | 关键 Metric | 通过标准 |
|----|---------|------------|---------|
| RQ1 | [实验名] | [Metric] | [标准] |
| RQ2 | [实验名] | [Metric] | [标准] |

**Baselines**：[B1, B2, B3]
**数据集**：[D1, D2]

**快速验证（Dim 0）**：[1-2句描述最小验证实验和通过标准]
```

**内容来源**：
- 主：`experiment-design.md`（RQ 与实验映射表、Baselines 节、Dim 0 节）
- 辅：`experiment-review.md`（确认实验设计通过；注意审查意见可能修改了实验）

---

### S4: Open Questions & Decisions Needed（核心讨论节）

**每次生成都重写此节。这是 presentation.md 最重要的 section。**

**过滤规则——纳入 S4 的条件（满足任一）**：
1. Review 文档标注"Revise"/"Block"且未被后续阶段解决
2. 方法/实验设计中有"备选方案未选择"且选择依赖领域判断
3. 实验结果偏离预期，且偏离的解释有多种可能性
4. `phase-outcomes/*.json` 的 `notes` 中出现"存疑"/"需要确认"类标注

**不纳入 S4 的情况**：
- 已在后续阶段被解决的问题（review revise → 后来 pass）
- 纯工程技术问题（不需要导师判断）
- 已有充分支撑证据的早期假设性质疑

```markdown
## Open Questions & Decisions Needed

> 这是今日讨论的重点。

### [DECISION NEEDED] 需要拍板的问题

**Q1: [问题标题]**
- **背景**：[为什么出现这个问题，1-2句]
- **Option A**：[描述 + 优劣]
- **Option B**：[描述 + 优劣]
- **我们的倾向**：选 Option [X]，因为 [理由]；但若 [条件成立] 则应选 Option [Y]
- **来源**：[具体来源文档和节]

### [INPUT NEEDED] 需要导师领域知识的问题

**Q2: [问题标题]**
- **背景**：[描述]
- **我们的困惑**：[具体不确定点]
- **来源**：[来源]

### [FYI] 已解决但导师应知道的问题

**Q3: [问题标题]**（如有）
- **解决方案**：[1句]

[热启动时：已在上次 presentation 后解决的问题，标注 [RESOLVED: <解决方案>]]
```

**内容来源**（按优先级）：
1. `phase-outcomes/*.json` 的 `notes` 字段
2. `gap-review.md`、`method-review.md`、`experiment-review.md` 中 Revise/Block 意见
3. `iteration-log.md` 中的"建议方向"（失败迭代的教训）
4. `method-design.md` 风险评估节、`experiment-design.md` 风险与预案节

**每个 DECISION NEEDED 问题必须包含"我们的倾向"**，不把决策完全甩给导师。

---

### S5: Current Progress（阶段进展）

**内容随当前阶段显著变化。**

#### 若当前阶段 <= P5：

```markdown
## Current Progress

**阶段历史**：[P1 ✓ → P2 ✓ → P3 Pass → 当前：P4]
**当前工作**：[当前阶段描述]
**关键待决**：[来自 S4 的最主要问题，1句]
```

#### 若当前阶段 P6-P8：

```markdown
## Current Progress

**已完成**：P1-P[N]（含 [N] 次独立评审）
**当前**：[当前阶段描述]
**实验体系**：[M] 个实验，分 [N] 个 Dimension，Dim 0 快速验证预计 [X] 小时
```

#### 若当前阶段 coding：

```markdown
## Current Progress

**已完成**：完整研究设计（P1-P8）[如有迭代：，经历 [N] 次迭代]
**当前**：实验执行中

### 实验进度总览

| 实验 | 状态 | 主要指标 | 备注 |
|------|------|---------|------|
| Dim 0 快速验证 | ✅通过 / ⚠️低于预期 / ❌失败 / 🔄进行中 | [数值或—] | |
| [Dim 1 主实验] | [状态] | [数值或—] | |
| [消融实验] | 待做 | — | |

**核心假设初步结论**（1句）：[基于 Dim 0 结果的结论，或"暂无结果"若未完成]

**当前 Blocking Issues**：[阻塞进展的具体问题，若有]
```

#### 若当前阶段 paper_writing 或之后：

```markdown
## Current Progress

**实验**：全部完成（[X] 个实验）
**核心结论**（1-2句）：[最重要的实验发现]
**当前**：[论文写作中 / 回顾总结中]

### 核心实验结果

| 方法 | [Metric A] | [Metric B] | 备注 |
|------|-----------|-----------|------|
| **[我们的方法]** | **[值]** | **[值]** | |
| [Baseline 1] | [值] | [值] | |
| [Baseline 2] | [值] | [值] | |
```

**内容来源**：
- pipeline-status.json（history）
- Codes/experiment-todo.md（checkbox 完成状态）
- experiment-design.md（各 Dim 的"实际结果"字段，若已填写）
- iteration-log.md（如有迭代历史）

---

### S6: Contribution Claims（贡献主张）

**仅在 P4 之后出现。随阶段递增更新验证状态。**

```markdown
## Contribution Claims

> 当前进展下的贡献预估，实验完成后将更新验证状态。

| # | 贡献描述 | 验证状态 | 支撑证据 |
|---|---------|---------|---------|
| C1 | 提出 [方法名]，解决 [Gap] | 理论完成，实验[待验证/进行中/已验证] | method-design.md |
| C2 | [理论证明 / 算法分析] | [状态] | method-design.md §[N] |
| C3 | 在 [Benchmark] 超越 SOTA [X%] | [待验证/已达到] | [结果文件，若有] |

**目标会议**：[Venue] | **截稿**：[Date，若已知]
```

**内容来源**：
- 主：contribution.md（全部贡献条目）
- 辅：method-review.md、experiment-review.md（审查者认可的贡献点）
- coding/paper_writing 阶段：experiment-design.md 或 Papers/ 的实际结果数字

---

### S7: Experimental Results（实验详情）

**仅在 coding 阶段或之后出现。每次有新实验结果时更新。**

```markdown
## Experimental Results

### Dim 0: [实验名称]（核心假设验证）

**假设**：[假设陈述]
**设置**：[数据集规模 + 关键配置]
**结果**：[数值]
**结论**：✅ 成立 / ⚠️ 部分成立（[条件]）/ ❌ 不成立 / 🔄 进行中
**分析**：[1-3句，为什么出现这个结果]

### Dim 1: [实验名称]

[完整结果表格]
[分析]

...

### 未完成的实验

| 实验 | 原因 | 预计完成 |
|------|------|---------|
| [实验] | [原因] | [时间] |
```

**内容来源**：
- 主：experiment-design.md（各 Dim 模板的"实际结果"字段）
- 主：Codes/experiment-todo.md（checkbox 状态 + 实验配置备注）
- 辅：iteration-log.md（历次迭代的实验数据快照，若有）

---

### S8: Iteration History（迭代历史）

**仅当 iteration-log.md 存在时出现。热启动时只追加新 Entry，不重写旧 Entry。**

```markdown
## Iteration History

> 项目经历了 [N] 次迭代。此节记录已排除路径，避免重复讨论。

### 迭代 #1（[日期]，级别：[L1/L2/L3]）

**失败核心原因**：[1句]
**已排除方案**：[具体方案，供导师参考]
**当前版本的调整**：[改进方向]

### 迭代 #2...

---

**已知不可行路径**（供参考，不再讨论）：
- [路径 X]：[排除原因]
```

**内容来源**：
- 主：iteration-log.md（各 Entry 的失败诊断、已排除方案、改进方向节）
- 辅：pipeline-status.json 中的 `iter_P4`、`iter_P2` 计数

---

### S9: Next Steps（下一步）

**每次生成都重写。P11/complete 阶段不出现。**

```markdown
## Next Steps

**下次 presentation 预计节点**：[具体里程碑，如"Dim 1 主实验完成后"]

### 研究者行动项

- [ ] [具体任务] — 预计完成：[时间估计]
- [ ] ...

### 待导师/合作者提供

- [ ] [来自 S4 Q[N] 的具体需求] — 请在 [时间] 前给出意见

### 条件分支

**若 S4 Q1 决定 Option A**：下一步需要 [...]
**若 S4 Q1 决定 Option B**：下一步需要 [...]
```

**内容来源**：
- 主：基于 S4 Open Questions 生成行动项
- 辅：Codes/experiment-todo.md（未完成的实验 checklist）
- 辅：experiment-design.md §风险与预案节（对应条件分支）
- AI 自主推导：根据当前阶段和 blocking issues 给出合理的下一步

---

## Step 4：组合并写入

将所有 Section 按顺序组合，写入 `<project_path>/presentation.md`。

**热启动时**：
- 只替换 `rewrite`/`update` 的 Section，保留 `stable` Section 的原有内容（包括任何人工编辑）
- 追加 `update_history` 条目，`sections_updated` 只列出实际发生变化的 Section
- 将上次 S4 中已被解决的 `[DECISION NEEDED]` 问题标注为 `[RESOLVED: ...]`

---

## Exit Criteria

- [ ] 已读取 pipeline-status.json 确定当前阶段
- [ ] 热启动时已完成变更分析，确定哪些 Section 需要更新
- [ ] S0 Snapshot 已生成（含今日议题）
- [ ] S1-S3 按存在的源文档生成（不存在的文档对应的 Section 不强行生成）
- [ ] S4 Open Questions 经过过滤逻辑，只包含真正需要讨论的问题，每个问题含"我们的倾向"
- [ ] S5 Current Progress 使用了与当前阶段匹配的变体
- [ ] S6-S9 按阶段感知规则选择性生成
- [ ] 文件头部 YAML frontmatter 已正确写入（热启动时已更新 update_history）
- [ ] presentation.md 已写入 `<project_path>/presentation.md`

## 完成后

向用户报告：
- presentation.md 已生成/更新，路径 `<project_path>/presentation.md`
- 本次更新了哪些 Section（热启动时）
- S4 中有几个待讨论问题（提示今日议题数量）
