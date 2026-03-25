# Skill: Project Assimilation（现有项目完整同化）— v3

将任意状态的现有科研项目完整纳入 Noesis/Praxis v3 框架：重建所有模块文档、运行真实 RS/RT 评审、对齐三模块状态，使其可被 `/praxis-r-auto` 或 `/praxis-paper` 直接接管。

**不是"打标签"，是"真正完成工作"。** 同化结束后，项目与 `/praxis-start` 原生启动的项目无结构区别。同化也是一次研究审计：对核心假设、实验设计、贡献 claim 做全面体检。

---

## Step 0：前置检测

检查是否存在：`pipeline-status.json`、`Docs/init-module-status.json`、`Docs/research-module-status.json`。

- **任一存在** → 展示已有状态，询问"是否重置并重新同化"，否则退出。
- **均不存在** → 继续。

---

## Step 1：一次性深度扫描

### 1.1 读取所有相关文件

扫描 `<project_path>`（忽略 `.git/`、`__pycache__/`、`.venv/`、`node_modules/`、`wandb/`、`runs/`）。

**高价值文件（全文读取）**：
- README.md、OVERVIEW.md、proposal.md
- *.pdf（若可读）、main.tex、paper.tex、draft.md
- project.md（v3 Init 产出）
- research/problem-statement.md、research/method-design.md、research/experiment-design.md、research/contribution.md
- Codes/_Results/probe_result.md、Codes/_Results/experiment_result.md
- related-work.md、literature-review.md
- research/retrospective.md、retrospective.md、iteration-log.md
- Docs/*.json、Reviews/*/、Papers/paper-status.json、Papers/phase-outcomes/*.json

**v2 兼容扫描**：
- project-startup.md → v3 project.md
- research/probe-results.md → v3 Codes/_Results/probe_result.md
- research/result.md → v3 Codes/_Results/experiment_result.md
- pipeline-status.json（v2 单 pipeline）
- inner-reviews/、codex-reviews/、phase-outcomes/debate/

**代码结构**：只读 README + 目录树 + 关键模块顶部注释。
**实验结果**：存在性 + 摘要。
**论文目录**：Papers/ 下章节草稿、review、LaTeX、PDF。

### 1.2 构建项目理解

- 研究问题、攻击角度、探针状态、方法/实验完成度、论文状态

### 1.3 DL 质量评估

评估不影响同化执行（始终完成），但影响评审严格度和阶段保守程度：

- **方法学成熟度** — 因果论证是否明确？组件间关系是否清晰？与 baseline 对比是否公平？
- **实验完备性** — ablation？不同规模表现？baseline 选择？多 seed + std/CI？
- **可复现性** — 训练配置完整？数据预处理有文档？环境说明？
- **贡献清晰度** — claim 与实验匹配？贡献可解耦归因？

### 1.4 是否值得继续

**正面信号**：初步实验有正面信号、代码框架完整仅缺对比实验、论文框架已有、问题仍 timely。
**慎重信号**：搁置 > 6 个月且领域快速迭代、初步结果不明确/负面、技术债重、与新工作高度重叠。

告知用户评估结果，最终决定权在用户。

### 1.5 从代码逆向工程（无文档但有代码时）

**从代码逆推方法设计**：model.py → 架构；loss 定义 → 训练目标；训练脚本超参 → 策略决策；数据代码 → 增强策略；评估脚本 → protocol。

**从结果逆推实验设计**：WandB/TensorBoard → 配置 + 曲线；checkpoint 命名 → ablation 结构；config.yaml → 超参空间。

所有逆向工程产出标注 `[ASSIMILATED: reverse-engineered from code/experiments, requires verification]`。

---

## Step 2：单轮用户确认

展示扫描摘要和同化计划：

- 拟设定的 **Init Module 阶段**（含 history 程度）
- 拟设定的 **Research Module 阶段**
- 拟设定的 **Paper Module 阶段**（如适用）
- 哪些文档直接纳入、哪些规范化重建
- formalize_review / design_review 运行为真实评审还是 advisory review（已投稿/已发表）
- **质量评估摘要**：最大风险点和需补充工作

等待用户确认后执行。

---

## Step 3：目录结构 + 文档重建

### 3.0 创建目录

```bash
mkdir -p <project_path>/{Docs,Codes/{probe,core,experiments,configs,scripts,_Data,_Results},Papers,phase-outcomes,research}
mkdir -p <project_path>/Reviews/{init,research-formalize,research-design}
```

若有论文材料或 Research Module 为 retrospective/complete：`mkdir -p <project_path>/Papers/phase-outcomes`

### 重建规则

| 情况 | 处理 |
|------|------|
| 已有 v3 结构文档 | 直接使用，追加 `> [原始文档，由 /praxis-assimilate 纳入]` |
| 已有但不满足 v3 | 备份为 `*.pre-assimilate.md`，写入规范化 v3 版本 |
| 有源材料无文档 | 生成，标注 `> [ASSIMILATED: generated from <来源>]` |
| 无源材料 | 生成占位文档，标注 `> [ASSIMILATED: synthesized from context, requires verification]` |

**规范化最低要求**：YAML frontmatter（version, entry_mode, iteration_major, iteration_minor）；method-design.md / experiment-design.md 补全双向交叉引用；根目录 retrospective.md 迁移至 research/retrospective.md。

### 3.1 project.md
从 README、proposal、论文 Abstract+Introduction 提炼。模板：`<noesis_root>/Praxis/templates/project.md`。v2 的 project-startup.md 迁移并备份。

### 3.2 research/problem-statement.md
三段式（Gap + 攻击角度 + 探针方案），含 YAML frontmatter。

### 3.3 Codes/_Results/probe_result.md
如有早期验证实验则重建。v2 的 research/probe-results.md 迁移。

### 3.4 research/method-design.md
从论文 Method + 代码提炼，含交叉引用 `→ experiment-design.md §X`。

### 3.5 research/experiment-design.md
从论文 Experiments + 配置 + 结果提炼，含反向引用 `← method-design.md §X`。

### 3.6 Codes/ 目录
已有代码组织到 v3 结构：core/、experiments/、configs/、scripts/、probe/、_Data/、_Results/。生成 Codes/CLAUDE.md。

### 3.7 Codes/_Results/experiment_result.md
如有实验结果则重建。v2 的 research/result.md 迁移。

### 3.8 辅助文档

不存在则从模板创建：
- `research/contribution.md`、`pipeline-evolution-log.md`、`iteration-log.md`
- `research/retrospective.md`（仅当项目已有回顾材料或进入 retrospective/complete）

---

## Step 4：运行真实评审

**已投稿/已发表项目**：在辩论上下文追加 advisory review 声明（评估框架覆盖度，倾向 Pass）。

### 4.1 Formalize Review

**前提**：research/problem-statement.md 已重建。

1. 读取 `<noesis_root>/Praxis/prompts/review-configs/formalize-review.yaml`
2. 按 YAML `input_docs` 读取项目文档
3. 组装辩论上下文（文档全文 + review_dimensions + project_path + debate_output_path）
4. **并行召唤 4 个 debater Agent**（model: opus）：

   | Agent | Subagent | 输出 |
   |-------|----------|------|
   | Contrarian | contrarian-subagent.md | Reviews/research-formalize/round-1/contrarian.md |
   | Comparativist | comparativist-subagent.md | .../comparativist.md |
   | Pragmatist | pragmatist-subagent.md | .../pragmatist.md |
   | Interdisciplinary | interdisciplinary-subagent.md | .../interdisciplinary.md |

   **单条消息发出所有 4 个调用。**

5. 综合者 Agent（model: opus）→ `Reviews/research-formalize/round-1/synthesis.md`
6. 写入 `phase-outcomes/formalize_review.json`（Pass/Revise/Abandon；advisory 模式统一 "pass"）

### 4.2 Design Review

**前提**：method-design.md + experiment-design.md 已重建。

1. 读取 `<noesis_root>/Praxis/prompts/review-configs/design-review.yaml`
2. 按 YAML `input_docs` 读取
3. 组装辩论上下文
4. **并行召唤 6 个 debater Agent**（model: opus）：

   | Agent | Subagent | 输出 |
   |-------|----------|------|
   | Theorist | theorist-subagent.md | Reviews/research-design/round-1/theorist.md |
   | Methodologist | methodologist-subagent.md | .../methodologist.md |
   | Empiricist | empiricist-subagent.md | .../empiricist.md |
   | Skeptic | skeptic-subagent.md | .../skeptic.md |
   | Pragmatist | pragmatist-subagent.md | .../pragmatist.md |
   | Contrarian | contrarian-subagent.md | .../contrarian.md |

   **单条消息发出所有 6 个调用。**

5. 综合者 → `Reviews/research-design/round-1/synthesis.md`（Pass/Revise/Fundamental/Abandon）
6. 写入 `phase-outcomes/design_review.json`（advisory 模式统一 "pass"）

### 4.3 评审结果对阶段的影响

| 评审结果 | Research Module 阶段覆盖 |
|----------|------------------------|
| FR=Pass, DR=Pass | 按原计划 |
| FR=Revise | → formalize |
| FR=Abandon | → complete |
| DR=Revise | → design |
| DR=Fundamental | → formalize |
| DR=Abandon | → complete |

**已投稿/已发表覆盖保护**：除非用户明确要求降级，不因 review 把已发表项目回退。发现写入 review notes 和报告。

评审覆盖原计划时，向用户报告原因。

---

## Step 5：写入 Pipeline 状态

### 5.1 确定各模块阶段

初步阶段（由 Step 4.3 评审覆盖）：

| 项目状态 | Init | Research | Paper |
|---------|------|----------|-------|
| 只有想法 | complete | formalize | — |
| 问题已定义 | complete | formalize | — |
| 有早期实验 | complete | design | — |
| 方法+实验已设计 | complete | blueprint | — |
| 代码已有、实验未完 | complete | implement | — |
| 实验完成、无论文 | complete | retrospective/complete | — |
| 有论文草稿 | complete | complete | P1-P7 |
| 已投稿/已发表 | complete | complete | complete |

**前提约束**：design 及以后需 FR Pass；blueprint 及以后需 FR+DR Pass。

### 5.1b Paper 阶段推断（有论文材料时）

已有 paper-status.json 则沿用。否则按最早安全阶段推断（只有 outline → P1；已有章节草稿 → P2；完整 draft → P3；有 critique → P4；整合稿 → P5；LaTeX → P6；project review → P7；已投稿 → complete）。

### 5.2 构建 history

三模块分别构建，所有条目添加 `"mode": "assimilated"`，使用当天日期。只为已完成阶段添加 history。

同时写入对应 `phase-outcomes/<phase>.json`（和 `Papers/phase-outcomes/P*.json`）。

### 5.3 写入状态文件

**pipeline-status.json**：
```json
{"active_module": "<init|research|paper>", "assimilated": true, "assimilated_date": "<日期>"}
```

active_module：Research 未 complete → "research"；Research complete + Paper 未 complete → "paper"。

**Docs/init-module-status.json**：phase "complete" + init history。

**Docs/research-module-status.json**：确定的 phase + research history。如被 review 打回，写入正确 entry_context：
- FR Revise → `{"mode": "fr_revise", "source_phase": "formalize_review", "formalize_iteration_count": 1}`
- DR Revise → `{"mode": "dr_revise", "source_phase": "design_review", "design_iteration_count": 1}`
- DR Fundamental → `{"mode": "direction_pivot", "source_phase": "design_review", "diagnosis": "direction_level", "formalize_iteration_count": 1}`

**Papers/paper-status.json**（如适用）：phase + history + `"assimilated": true`。

### 5.4 CLAUDE.md

按 `<noesis_root>/Praxis/templates/project-claude-md.md` 创建或更新。关键字段：Noesis 路径（~/Research/Noesis）、计算资源、各模块当前阶段、文档状态表、v3 目录架构、Orchestrator CLI。

---

## Step 6：同化报告

```
同化完成报告

## 文档重建
| 文档 | 状态 | 来源 |
|------|------|------|
| project.md | 重建 | README + proposal |
| ... | ... | ... |

## 质量评估
- 方法学成熟度：[高/中/低] — [说明]
- 实验完备性：[高/中/低] — [说明]
- 可复现性：[高/中/低] — [说明]
- 核心风险点：[1-3个]

## 评审结果
- Formalize Review：[Pass/Revise/Abandon] — [摘要]
- Design Review：[Pass/Revise/Fundamental/Abandon] — [摘要]

## 模块状态
- Init：complete | Research：[阶段] | Paper：[阶段/无]
- Active Module：[模块]
- 评审覆盖：[是/否]（原 → 实际）

## 下一步
- Research 未 complete：`/praxis-r-auto <project_path>`
- Paper 已初始化：`/praxis-paper <project_path>`
- 完成后：`/praxis-evolve <project_path>`
```

---

## Exit Criteria

- [ ] 已深度阅读全部相关文件
- [ ] 已完成 DL 质量评估（方法学、实验、可复现性、贡献）
- [ ] 已与用户完成单轮确认
- [ ] 目录结构已创建
- [ ] v3 文档已生成（含 YAML frontmatter）
- [ ] v2 遗留文件已迁移（project-startup.md、probe-results.md、result.md）
- [ ] 辅助文档已创建
- [ ] Formalize Review 已运行（4 debaters + synthesizer，opus）
- [ ] Design Review 已运行（6 debaters + synthesizer，opus）
- [ ] 评审结果已反馈到阶段设定
- [ ] 三个状态文件 + phase-outcomes 已写入
- [ ] CLAUDE.md 已按 v3 模板创建/更新
- [ ] 同化报告已输出

## 核心原则

- **一次问清，全程自动**
- **实际运行评审，不跳过** — 完整 debater + synthesizer，model: opus
- **评审结果影响阶段** — 不通过则不设到下游
- **三模块独立状态**
- **同化产物必须可被下游消费** — 文件名、entry_context、phase-outcomes 与 runner 对齐
- **非破坏性** — 已有文件不覆盖
- **逆向工程诚实标注** — 从代码逆推的文档标注来源和不确定性
