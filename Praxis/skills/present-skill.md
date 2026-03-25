# Skill: Praxis Present（项目进展展示）— v3

生成 `presentation.md`，供研究者与导师/合作者讨论的结构化进展总结。
支持冷启动（首次生成）和热启动（增量更新，保留人工编辑）。

---

## 核心原则

**导师读 presentation 的优先级与 pipeline 相反。**

Pipeline：Gap → Method → Experiment → Result
导师：**当前进展 → 核心主张 → 悬而未决的问题 → 背景支撑**

presentation.md 是为"15分钟讨论"重排信息优先级的独立文档。最重要的 section 是 Open Questions。

**沟通原则**：
- 先传达直觉再展示细节 — 每个技术概念先用自然语言解释"它在干什么"
- 数字比文字有力 — "推理速度 3.2 倍，训练时间减少 40%" 优于 "显著更快"
- 类比建立桥梁但必须准确 — 不能为通俗化引入错误暗示

---

## Step 0：热启动检测

检查 `<project_path>/presentation.md`：

**不存在（冷启动）** → 继续 Step 1，全量生成。

**存在（热启动）** → 读取 YAML frontmatter 的 `last_module_state` 和 `update_history`，读取当前各模块状态文件，计算"新产出文档"。对每个 Section 判断 `rewrite`/`update`/`stable`。检查上次 `[DECISION NEEDED]` 问题是否已解决。只重写/更新需变化的 Section。

---

## Step 1：读取项目文档

条件性读取（不存在则跳过）：

**必读（状态文件）**：
- `pipeline-status.json` ← active_module
- `Docs/init-module-status.json` ← Init Module 状态
- `Docs/research-module-status.json` ← Research Module 状态
- `Papers/paper-status.json` ← Paper Module 状态
- `phase-outcomes/*.json` ← 各阶段完成状态

**按存在情况读取**：
- `project.md`、`research/contribution.md`
- `research/problem-statement.md`、`research/method-design.md`、`research/experiment-design.md`
- `Reviews/research-formalize/round-N/synthesis.md`（N 为最新轮次）
- `Reviews/research-design/round-N/synthesis.md`
- `Reviews/init/round-N/synthesis.md`
- `Codes/experiment-todo.md`
- `Codes/_Results/probe_result.md`、`Codes/_Results/experiment_result.md`
- `iteration-log.md`、`CLAUDE.md`

---

## Step 2：确定内容权重

根据 `pipeline-status.json` 的 `active_module` 确定活跃模块，再读取对应状态文件确定当前阶段：

| 当前模块 | 当前阶段 | 内容重心 | 必须 Section |
|---------|---------|---------|-------------|
| Init | init → review | 问题定义与方向确认 | S0, S1, S4, S9 |
| Research | formalize → design_review | 方法设计与验证 | S0, S1, S2, S4, S5, S6, S9 |
| Research | blueprint → implement | 实验执行与结果 | S0-S7, (S8), S9 |
| Research | retrospective / complete | 知识回收 | S0-S3, S5-S7, (S8) |
| Paper | P1 → P7 | 论文写作 | S0-S4(轻量), S5-S7 |

S8 仅当 `iteration-log.md` 存在时出现。多模块并行时以 `active_module` 为主，S5 体现所有模块状态。

---

## Step 3：生成各 Section

### YAML Frontmatter

```yaml
---
project: [项目名]
version: v1  # 热启动时递增
generated_at: [日期]
active_module: [init/research/paper]
current_phase: [当前阶段]
last_module_state: [active_module:phase]
update_history:
  - v1 | [日期] | module: [模块] phase: [阶段] | sections: all | trigger: initial
module_snapshot:
  init: [phase/"complete"/"not_started"]
  research: [phase/"complete"/"not_started"]
  paper: [phase/"complete"/"not_started"]
---
```

---

### S0: Project Snapshot

**每次完整重写。**

```markdown
## Project Snapshot

**项目**: [名称] | **活跃模块**: [模块] — [阶段] | **目标**: [venue + 截稿日]
**本次更新**: [日期] [热启动：| 距上次: X 天]

**模块状态总览**：
| 模块 | 状态 | 当前阶段 |
|------|------|---------|
| Init | [完成/进行中/未开始] | [阶段] |
| Research | ... | ... |
| Paper | ... | ... |

**进展概括**（1-2句）：[提炼最重要进展]

**今日议题**（优先级排序，提炼自 S4）：
1. [DECISION] [最需拍板的问题]
2. [INPUT] [需要领域知识的问题]
3. [UPDATE] [最新进展]
```

**来源**：pipeline-status.json、各模块 status.json、phase-outcomes notes

**议题排序**：阻塞性决策 > 需导师领域知识 > 有时间窗口 > 信息同步。纯工程问题、已有充分证据的决策不上会。

---

### S1: The Problem We're Solving

**formalize_review Pass 后稳定；direction pivot 后重写。**

```markdown
## The Problem We're Solving

**领域背景**（1句）：[领域 + 任务 + 重要性]

**现有方法的局限**（2-3句）：
[最强方法] 在 [场景] 下 [问题]。根因是 [技术根因]。定量：[metric 损失]。

**核心 Gap**：
> "[现有方法]做了X，但因为Y所以在Z场景下失效。"

**Research Questions**:
- RQ1: [表述]
- RQ2: [表述]
```

**来源**：主 `research/problem-statement.md`；辅 `project.md`、`Codes/_Results/probe_result.md`。

**表达**：30秒内让读者理解"为什么重要"。根因分析指向技术层面，暗示解决方案方向。

---

### S2: Our Approach

**仅 design 阶段之后。design_review Pass 后稳定；method iterate / direction pivot 后更新。**

```markdown
## Our Approach

**核心 Idea**（1-2句，纯自然语言）：[直觉描述]

**因果论证**：
Gap 根因 [X] → 设计 [Y] → 预期 [Z]

**组件概览**：
| 组件 | 功能 | 解决子问题 |
|------|------|-----------|
| [A] | [功能] | [子问题] |

**与现有方法本质区别**（2句）：与 [最相近方法] 相比，[核心差异] → [理论优势]。

[迭代时] **当前版本**: v[N]（详见 S8）
```

**来源**：主 `research/method-design.md`；辅 `research/contribution.md`、`iteration-log.md`。

**分层表达**：第一层（所有人）= 直觉 + 类比；第二层（同行）= 因果论证 + 组件分工；第三层（细节）= 留给 Q&A。对比要公平但鲜明，突出本质区别而非表面差异。

---

### S3: Validation Design

**仅 design 阶段之后。design_review Pass 后稳定。**

```markdown
## Validation Design

| RQ | 核心实验 | 关键 Metric | 通过标准 |
|----|---------|------------|---------|
| RQ1 | [实验] | [Metric] | [标准] |

**Baselines**：[B1, B2, B3]
**数据集**：[D1, D2]
**快速验证（Dim 0）**：[最小验证实验 + 通过标准]
```

**来源**：主 `research/experiment-design.md`；辅 `Reviews/research-design/round-N/synthesis.md`。

---

### S4: Open Questions & Decisions Needed

**每次完整重写。最重要的 section。**

**纳入条件（满足任一）**：
1. Review 文档标注 Revise/Block 且未被后续阶段解决
2. 设计中有备选方案未选择且依赖领域判断
3. 实验结果偏离预期，解释有多种可能
4. phase-outcomes notes 中出现"存疑"/"需确认"

**排除**：已被后续阶段解决的问题、纯工程问题、已有充分证据的早期质疑。

```markdown
## Open Questions & Decisions Needed

### [DECISION NEEDED]

**Q1: [标题]**
- **背景**：[1-2句]
- **Option A**：[描述 + 优劣]
- **Option B**：[描述 + 优劣]
- **我们的倾向**：Option [X]，因为 [理由]；若 [条件] 则选 [Y]
- **来源**：[文档和节]

### [INPUT NEEDED]

**Q2: [标题]**
- **背景**：[描述]
- **困惑**：[不确定点]

### [FYI]
**Q3: [标题]**（如有）
- **解决方案**：[1句]

[热启动：已解决的标注 [RESOLVED: <方案>]]
```

**来源**（优先级）：phase-outcomes notes > Review synthesis 中 Revise/Block > iteration-log 建议方向 > 风险评估节。

**每个 DECISION NEEDED 必须含"我们的倾向"**。

**DL 常见决策类型**：方法选择（创新性 vs 可行性）、实验设计（baseline 完备性 vs 时间）、论文定位（venue 选择、pitch angle）。

---

### S5: Current Progress

**内容随模块/阶段变化，需体现多模块进度。**

按当前模块选择对应变体：

**Init Module**：模块进度 + 阶段历史 + 当前工作 + 关键待决 + 探针结果（如有）

**Research formalize → design_review**：多模块进度 + 阶段历史 + 当前工作 + 关键待决

**Research blueprint → implement**：多模块进度 + 已完成 + 当前 + 实验进度总览表（实验/状态/指标/备注）+ 核心假设初步结论 + Blocking Issues

**Research retrospective/complete 或 Paper**：多模块进度 + 实验全部完成 + 核心结论 + 核心实验结果表（方法/Metric A/Metric B）

**来源**：各模块 status.json、experiment-todo.md、experiment_result.md、probe_result.md、iteration-log.md。

---

### S6: Contribution Claims

**仅 design 阶段之后。验证状态随阶段递增更新。**

```markdown
## Contribution Claims

| # | 贡献描述 | 验证状态 | 支撑证据 |
|---|---------|---------|---------|
| C1 | 提出 [方法]，解决 [Gap] | [待验证/进行中/已验证] | method-design.md |
| C2 | [理论/算法分析] | [状态] | method-design.md §N |
| C3 | 在 [Benchmark] 超越 SOTA [X%] | [状态] | [结果文件] |

**目标会议**：[Venue] | **截稿**：[Date]
```

**来源**：主 `research/contribution.md`；辅 `project.md` §2、Review synthesis、experiment_result.md。

---

### S7: Experimental Results

**仅 implement 阶段或之后。有新结果时更新。**

```markdown
## Experimental Results

### Dim 0: [名称]（核心假设验证）
**假设**：[陈述] | **设置**：[数据集 + 配置] | **结果**：[数值]
**结论**：成立 / 部分成立 / 不成立 / 进行中
**分析**：[1-3句，为什么]

### Dim 1: [名称]
[结果表格 + 分析]

### 未完成实验
| 实验 | 原因 | 预计完成 |
```

**来源**：主 experiment_result.md、probe_result.md；辅 experiment-todo.md、iteration-log.md。

**表达**：重要 metric 放最左列，我方方法加粗。不只罗列数字，要说明"数字意味着什么"。不符合预期的结果坦诚面对，放入 S4 讨论。矛盾结果指出矛盾并提出解释。

---

### S8: Iteration History

**仅当 iteration-log.md 存在。热启动时只追加新 Entry。**

```markdown
## Iteration History

> 项目经历 [N] 次迭代。

### 迭代 #1（[日期]，[method_iterate/direction_pivot]）
**失败核心原因**：[1句]
**已排除方案**：[方案]
**当前版本调整**：[改进方向]

---
**已知不可行路径**：
- [路径 X]：[排除原因]
```

**来源**：主 `iteration-log.md`；辅 `Docs/research-module-status.json` history。

---

### S9: Next Steps

**每次重写。Research complete + Paper complete 后不出现。**

```markdown
## Next Steps

**下次 presentation 预计节点**：[里程碑]

### 研究者行动项
- [ ] [任务] — 预计：[时间]

### 待导师/合作者提供
- [ ] [S4 Q[N] 的需求] — 请在 [时间] 前给出意见

### 条件分支
**若 Q1 选 Option A**：[下一步]
**若 Q1 选 Option B**：[下一步]
```

**来源**：主 S4 生成行动项；辅 experiment-todo.md、experiment-design.md 风险与预案。

**下一步命令**（按状态建议）：
- Research formalize：`/praxis-r-auto <project_path>`
- Research implement（失败）：`/praxis-conclude <project_path>`
- Paper：`/praxis-paper <project_path>`

---

## Step 4：组合并写入

写入 `<project_path>/presentation.md`。

**热启动时**：只替换 rewrite/update 的 Section，保留 stable Section 的原有内容（含人工编辑）。追加 update_history。将已解决的 `[DECISION NEEDED]` 标注为 `[RESOLVED]`。

---

## Exit Criteria

- [ ] 已读取 pipeline-status.json + 各模块状态文件确定当前阶段
- [ ] 热启动时已完成变更分析
- [ ] S0 含模块状态总览 + 今日议题（按优先级排序）
- [ ] S1 能 30 秒内传达"为什么重要"
- [ ] S2 分层清晰（直觉层 + 技术层）
- [ ] S4 经过过滤，每个问题含"我们的倾向"，按阻塞性排序
- [ ] S5 使用匹配当前阶段的变体，体现多模块状态
- [ ] S7 结果含分析而非仅罗列数字
- [ ] YAML frontmatter 正确
- [ ] presentation.md 已写入

## 完成后

报告：路径、更新了哪些 Section（热启动时）、S4 待讨论问题数、建议的会议时间分配（如"前 8 分钟聚焦 2 个 DECISION NEEDED，后 7 分钟同步进展"）。
