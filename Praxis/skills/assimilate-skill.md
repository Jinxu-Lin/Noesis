# Skill: Project Assimilation（现有项目完整同化）— v2

将任意状态的现有科研项目**完整纳入** Noesis/Praxis v2 框架，输出结果：所有阶段文档已生成、所有评审已完成、pipeline 状态精确对齐，可立即继续推进。

---

## 设计哲学

**不是"打标签"，是"真正完成工作"。**

同化不只是创建 JSON 文件和修改 CLAUDE.md——而是用 Noesis 的 AI 能力，从现有材料中完整重建每个阶段的产出文档，并实际运行 RS/RT 评审。同化结束后，项目与从 `/praxis-start` 原生启动的项目无任何结构区别。

**同化也是一次研究审计。** 在 DL 领域，很多项目在没有系统框架的情况下已经走了很远——可能代码已经写完、实验已经跑完，但核心假设从未被显性化、实验设计中的对照和 ablation 可能有缺陷、方法的核心贡献 claim 可能站不住。同化不是简单的格式化，而是用严格的审查流程对项目做一次全面体检。

---

## 执行流程

### Step 0：前置检测

检查 `<project_path>/pipeline-status.json` 是否存在：
- **存在** → 读取并展示，询问用户"是否要重置并重新同化"，若否则退出
- **不存在** → 继续

---

### Step 1：一次性深度扫描

**目标**：彻底理解这个项目，只问一轮问题，然后全自动执行。

#### 1.1 读取所有相关文件

扫描整个 `<project_path>`（忽略 `.git/`、`__pycache__/`、`.venv/`、`node_modules/`、`wandb/`、`runs/`），重点阅读：

**高价值文件（全文读取）**：
- `README.md`、`OVERVIEW.md`、`proposal.md`
- `*.pdf`（若可读）、`main.tex`、`paper.tex`、`draft.md`
- `project-startup.md`
- `research/problem-statement.md`、`research/method-design.md`、`research/experiment-design.md`、`research/contribution.md`
- `research/probe-results.md`、`research/result.md`
- `related-work.md`、`literature-review.md`
- `research/retrospective.md`、`retrospective.md`、`iteration-log.md`
- `Papers/paper-status.json`、`Papers/phase-outcomes/*.json`

**代码结构（只读 README + 目录树 + 关键模块顶部注释）**

**实验结果（存在性 + 摘要）**

**论文目录（若存在）**：
- `Papers/` 下的章节草稿、review、LaTeX、PDF

#### 1.2 构建项目理解

基于阅读，在内部建立对项目的完整理解：
- **研究问题**：项目在解决什么问题？
- **攻击角度**：核心方法思路是什么？
- **探针状态**：是否有早期验证实验？
- **方法/实验状态**：完成到什么程度？
- **论文状态**：有草稿/已投/已发表？

#### 1.3 DL 项目质量评估

在构建项目理解的过程中，同步评估以下 DL 领域特有的质量维度。这些评估不影响同化的执行（同化始终完成），但会影响评审的严格程度和阶段设定的保守程度：

**方法学成熟度**：
- 核心方法是否有明确的因果论证（"因为 X 问题存在，所以 Y 设计是合理的"），还是仅仅是"试了有效"？
- 方法各组件之间的关系是否清晰？是否存在冗余组件（可能是过度设计的信号）？
- 是否有与最相关 baseline 的公平对比？（同等计算预算、同等数据、同等调参力度）

**实验完备性**：
- 是否有 ablation study 证实每个核心组件的贡献？
- 是否有不同规模（模型大小 / 数据量 / 序列长度）下的表现报告？
- baseline 的选择是否合理？是否包含了当前 SOTA 和公认的 strong baseline？
- 统计显著性：是否有多 seed 结果？是否报告了 std / confidence interval？

**可复现性**：
- 是否有完整的训练配置（learning rate, batch size, epochs, optimizer, scheduler）？
- 数据预处理流程是否有文档记录？
- 是否有 requirements.txt / environment.yml 或等效的环境说明？

**贡献清晰度**：
- 核心贡献 claim 是否与实验结果匹配？（例如声称"提出了更高效的方法"但没有效率对比）
- 贡献是否可被解耦？即是否可以说清楚"因为我们做了 X 所以得到了 Y 的提升"？

#### 1.4 判断项目是否值得继续

对于半完成的项目，以下信号帮助判断是否值得投入资源继续：

**值得继续的信号**：
- Dim 0 / 初步实验已经显示正面信号（核心假设有初步验证）
- 代码框架完整，主要缺少 ablation 和对比实验
- 论文框架已有，需要补充实验或修订
- 问题仍然 timely（没有在搁置期间被其他工作解决）

**需要慎重考虑的信号**：
- 项目搁置超过 6 个月，且领域进展快（尤其是 LLM、多模态等快速迭代的方向）
- 初步实验结果不明确或为负面
- 代码质量差，技术债务重（重写可能比修改更快）
- 核心思路与搁置期间出现的新工作高度重叠

**应该在用户确认时明确告知这些评估**，但最终决定权在用户。

---

### Step 2：单轮用户确认

向用户展示扫描摘要和同化计划，至少包含以下判断，等待确认：

- 拟设定的**主 pipeline 阶段**（C/P/D/I/E/W/R/complete）
- 如项目包含论文材料，拟设定的**论文 pipeline 阶段**（P1-P7/complete）
- 哪些文档会直接纳入，哪些文档会被规范化重建
- RS/RT 是否会作为**真实评审**运行，还是仅作为已投稿/已发表项目的**advisory review**
- **项目质量评估摘要**：基于 1.3 的评估，指出最大的风险点和需要补充的工作

---

### Step 3：目录结构创建 + 文档重建

#### Step 3.0：创建必要目录

```bash
mkdir -p <project_path>/research
mkdir -p <project_path>/inner-reviews
mkdir -p <project_path>/codex-reviews
mkdir -p <project_path>/phase-outcomes/debate/RS
mkdir -p <project_path>/phase-outcomes/debate/RT
mkdir -p <project_path>/Codes
```

若项目已有论文材料，或拟设定主阶段为 `W/R/complete`，额外创建：

```bash
mkdir -p <project_path>/Papers/phase-outcomes
mkdir -p <project_path>/Papers/codex-reviews
```

#### 重建规则

- **已有对应文档且已满足 v2 结构** → 直接使用，追加 `> [原始文档，由 /praxis-assimilate 纳入]` 标注
- **已有对应文档但不满足 v2 结构** → 先保留原件为同目录 sibling 备份（如 `problem-statement.pre-assimilate.md`），再写入规范化后的 v2 文档
- **有源材料但无文档** → 生成，标注 `> [ASSIMILATED: generated from <来源>]`
- **无任何源材料** → 生成占位文档，标注 `> [ASSIMILATED: synthesized from context, requires verification]`

规范化的最低要求：
- phase 文档必须有 v2 YAML frontmatter（`version`、`entry_mode`、`iteration_major`、`iteration_minor`）
- `method-design.md` / `experiment-design.md` 必须补全双向交叉引用
- 旧项目的根目录 `retrospective.md` 若存在，应被规范化迁移为 `research/retrospective.md`

#### 从代码和实验结果逆向工程研究设计

对于没有文档但有代码和实验结果的项目（DL 领域中非常常见），需要从实现逆推研究设计：

**从代码逆推方法设计**：
- 模型定义文件（`model.py`、`network.py`）→ 提取架构设计、核心组件
- 损失函数定义 → 提取训练目标和多任务学习策略
- 训练脚本中的超参数 → 提取训练策略决策（optimizer choice、scheduler、warmup 等）
- 数据加载和预处理代码 → 提取数据假设和增强策略
- 推理/评估脚本 → 提取评估 protocol

**从实验结果逆推实验设计**：
- WandB/TensorBoard 日志 → 提取实验配置和训练曲线
- 结果文件/checkpoint 命名 → 提取 ablation 结构和实验矩阵
- 配置文件（`config.yaml`、`args.py`）→ 提取超参搜索空间和最终选择
- saved models / checkpoints → 判断哪些实验已完成

**逆向工程时的注意事项**：
- 代码中的实际实现可能与研究者的"意图"不一致（常见的是代码中有 bug 但结果看起来 OK）
- 实验日志中可能包含未被清理的失败实验 → 需要与用户确认哪些是最终结果
- 标注所有逆向工程产出为 `[ASSIMILATED: reverse-engineered from code/experiments, requires verification]`，因为代码到设计的映射可能不精确

#### Step 3.1：`project-startup.md`

输出文件名是 `<project_path>/project-startup.md`。
模板参照 `<noesis_root>/Praxis/templates/project-start.md`。
从 README、proposal、论文 Abstract+Introduction 提炼。

#### Step 3.2：research/problem-statement.md（v2 新格式）

从以下来源提炼，按 v2 三段式结构（Gap + 攻击角度 + 探针方案）：
- 论文 Related Work / Introduction 中的 gap 陈述
- 方法章节暗示的攻击角度
- 实验章节暗示的探针/验证逻辑

提炼格式遵循 `<noesis_root>/Praxis/templates/problem-statement.md` 模板（含 YAML frontmatter：version、entry_mode、iteration_major、iteration_minor）。

#### Step 3.3：research/probe-results.md（如有早期验证实验）

如果项目有类似探针的早期实验，从结果中重建。
模板参照 `<noesis_root>/Praxis/templates/probe-results.md`。

#### Step 3.4：research/method-design.md（v2 含交叉引用）

从论文 Method/Approach 章节和代码提炼。
模板参照 `<noesis_root>/Praxis/templates/method-design.md`（含 YAML frontmatter + 与 experiment-design.md 的交叉引用格式 `→ experiment-design.md §X`）。

#### Step 3.5：research/experiment-design.md（v2 含反向引用）

从论文 Experiments 章节、配置文件、结果文件提炼。
模板参照 `<noesis_root>/Praxis/templates/experiment-design.md`（含 YAML frontmatter + 与 method-design.md 的反向引用格式 `← method-design.md §X`）。

#### Step 3.6：Codes/ 目录

如代码已有，生成 `Codes/code-todo.md`、`Codes/experiment-todo.md`、`Codes/CLAUDE.md`（代码子目录指引文档）。

#### Step 3.7：辅助文档

以下文档如不存在，从模板创建：

| 文档 | 模板 | 说明 |
|------|------|------|
| `research/contribution.md` | `<noesis_root>/Praxis/templates/contribution.md` | 跨阶段贡献跟踪 |
| `pipeline-evolution-log.md` | `<noesis_root>/Praxis/templates/pipeline-evolution-log.md` | X-reflect 追加日志 |
| `iteration-log.md` | `<noesis_root>/Praxis/templates/iteration-log.md` | 迭代历史（如无迭代记录，创建空模板） |
| `research/result.md` | `<noesis_root>/Praxis/templates/result.md` | 实验结果（如有实验数据则重建，否则创建空模板） |
| `research/retrospective.md` | `<noesis_root>/Praxis/templates/retrospective.md` | 仅当项目已进入 R/complete 或已有回顾材料时创建/规范化 |

---

### Step 4：实际运行评审

对重建的关键文档，用 Agent tool fork 独立评审 subagent 运行**真实**评审。

**已发表/已投稿项目的特殊处理**：在辩论上下文中追加以下段落：

```
> 本项目已投稿/已发表。评审目的是检验框架适配性，而非质疑已完成的研究。
> 请以"评估框架覆盖度 + 发现对未来项目有价值的补充视角"为导向，
> 而非"是否应该继续/放弃"。最终判定应倾向 Pass。
```

#### Step 4.1：RS 战略审查

**前提条件**：`research/problem-statement.md` 已重建。

**执行步骤**（严格对齐当前 runner 使用的 prompt / YAML / subagent）：

1. **加载审查配置**：读取 `<noesis_root>/Praxis/prompts/review-configs/strategic-review.yaml`

2. **读取文档**：按 YAML 的 `input_docs` 列表读取项目文档

3. **组装辩论上下文**（与 `strategic-review-prompt.md` Step 3a 完全一致）：
   ```
   ## 审查文档（完整内容）
   [problem-statement.md 全文 + 其他 input_docs 内容]

   ## 审查重点维度
   [来自 strategic-review.yaml 的 review_dimensions]

   project_path: <project_path>
   debate_output_path: <project_path>/phase-outcomes/debate/RS/<role>.md
   ```

4. **并行召唤 4 个 debater Agent**（**model: opus**，重要！）：

   | Agent | Subagent 文件 | 输出路径 |
   |-------|--------------|---------|
   | Contrarian | `<noesis_root>/Praxis/subagents/contrarian-subagent.md` | `phase-outcomes/debate/RS/contrarian.md` |
   | Comparativist | `<noesis_root>/Praxis/subagents/comparativist-subagent.md` | `phase-outcomes/debate/RS/comparativist.md` |
   | Pragmatist | `<noesis_root>/Praxis/subagents/pragmatist-subagent.md` | `phase-outcomes/debate/RS/pragmatist.md` |
   | Interdisciplinary | `<noesis_root>/Praxis/subagents/interdisciplinary-subagent.md` | `phase-outcomes/debate/RS/interdisciplinary.md` |

   每个 Agent 的 `prompt` = 辩论上下文 + 对应 subagent 文件完整内容。
   **在单条消息中发出所有 4 个 Agent 调用。**

5. **召唤综合者 Agent**（model: opus）：
   - `prompt` = 审查阶段标识 + 文档摘要 + debate_dir 路径 + `<noesis_root>/Praxis/subagents/work-synthesizer-subagent.md` 完整内容
   - 输出：`phase-outcomes/debate/RS/synthesis.md`

6. **生成正式审查报告**：读取 synthesis.md，写入 `inner-reviews/strategic-review.md`，包含 Pass/Revise/Block 判定

7. **记录 RS outcome**：将审查结果写入 `phase-outcomes/RS.json`：
   ```json
   {"outcome": "pass|revise|abandon", "notes": "..."}
   ```
   - Pass → outcome: "pass"
   - Revise → outcome: "revise"
   - Block → outcome: "abandon"
   - **Advisory review 模式（已投稿/已发表，且不降级）** → outcome 统一写 `"pass"`，把额外问题写进 `notes`

#### Step 4.2：RT 技术审查

**前提条件**：`research/method-design.md` + `research/experiment-design.md` 已重建。

**执行步骤**（与 RS 类似，使用 RT 配置）：

1. **加载审查配置**：读取 `<noesis_root>/Praxis/prompts/review-configs/technical-review.yaml`

2. **读取文档**：按 YAML 的 `input_docs` 列表读取项目文档

3. **组装辩论上下文**（与 `technical-review-prompt.md` Step 3a 一致）：
   ```
   ## 审查文档（完整内容）
   [method-design.md + experiment-design.md + 其他 input_docs]

   ## 审查重点维度
   [来自 technical-review.yaml 的 review_dimensions]

   project_path: <project_path>
   debate_output_path: <project_path>/phase-outcomes/debate/RT/<role>.md
   ```

4. **并行召唤 6 个 debater Agent**（**model: opus**）：

   | Agent | Subagent 文件 | 输出路径 |
   |-------|--------------|---------|
   | Theorist | `theorist-subagent.md` | `phase-outcomes/debate/RT/theorist.md` |
   | Methodologist | `methodologist-subagent.md` | `phase-outcomes/debate/RT/methodologist.md` |
   | Empiricist | `empiricist-subagent.md` | `phase-outcomes/debate/RT/empiricist.md` |
   | Skeptic | `skeptic-subagent.md` | `phase-outcomes/debate/RT/skeptic.md` |
   | Pragmatist | `pragmatist-subagent.md` | `phase-outcomes/debate/RT/pragmatist.md` |
   | Contrarian | `contrarian-subagent.md` | `phase-outcomes/debate/RT/contrarian.md` |

   **在单条消息中发出所有 6 个 Agent 调用。**

5. **召唤综合者 Agent**（model: opus）

6. **生成正式审查报告**：写入 `inner-reviews/technical-review.md`，包含 Pass/Revise/Fundamental/Block 判定

7. **记录 RT outcome**：写入 `phase-outcomes/RT.json`：
   - Pass → outcome: "pass"
   - Revise → outcome: "revise"
   - Fundamental → outcome: "fundamental"
   - Block → outcome: "abandon"
   - **Advisory review 模式（已投稿/已发表，且不降级）** → outcome 统一写 `"pass"`，把额外问题写进 `notes`

#### Step 4.3：评审结果对阶段的影响

**重要**：评审结果可能改变 Step 5 中的阶段设定。遵循以下优先级：

| 评审结果 | 阶段覆盖 | 理由 |
|----------|---------|------|
| RS = Pass, RT = Pass | 按原计划设定 | 一切正常 |
| RS = Revise | 强制设为 C | 问题定义需修改 |
| RS = Block/Abandon | 强制设为 R | 方向有根本问题 |
| RT = Revise | 强制设为 D | 方法/实验需修改 |
| RT = Fundamental | 强制设为 C | 方向层面有误 |
| RT = Block/Abandon | 强制设为 R | 方法不可救药 |

**已投稿/已发表项目的覆盖保护**：
- 默认将 RS/RT 视为 **advisory review**
- 除非用户明确要求把项目降级回研究阶段，否则**不要**因 review 结果把已投稿/已发表项目从 `W/R/complete` 降到 `C/D`
- 此时应把发现写进 review notes 和 assimilation report，而不是强行回退主状态

**如果评审结果覆盖了原计划阶段，向用户报告原因。**

---

### Step 5：写入 Pipeline 状态

#### 5.1 确定当前阶段（v2 阶段代号）

先按下表确定**初步阶段**，再由 Step 4.3 的评审结果覆盖（如触发）：

| 项目实际状态 | 初步阶段 | 前提 |
|------------|---------|------|
| 只有想法/早期 | C（问题锐化） | — |
| 问题已定义，未验证 | P（探针实验） | RS 必须 Pass |
| 有早期实验结果 | D（联合设计） | RS 必须 Pass |
| 方法+实验已设计 | I（实现规划） | RS + RT 必须 Pass |
| 代码已有，实验未完成 | E（实验执行） | RS + RT 必须 Pass |
| 实验已完成，无论文 | W（论文写作） | RS + RT 必须 Pass |
| 有论文草稿 | W（论文写作） | RS + RT 必须 Pass |
| 已投稿/已发表 | R（知识回收） | — |
| 有完整回顾文档 | complete | — |

#### 5.1b 论文 pipeline 阶段推断（仅当存在论文材料）

若 `<project_path>/Papers/paper-status.json` 已存在，直接沿用。

若不存在且项目已进入 `W/R/complete`，按**最早安全阶段**推断 paper phase：

| 论文材料状态 | 论文阶段 |
|------------|---------|
| 只有 outline / section plan | `P1` |
| 已有章节草稿，但未形成完整 draft | `P2` |
| 已有完整 draft，尚未形成系统 critique | `P3` |
| 已有 critique/comment list，正在整合修订 | `P4` |
| 已有整合后的完整稿，待终审 | `P5` |
| 已有 LaTeX 工程 / 排版阶段 | `P6` |
| 已有项目级 review 材料，待项目终审 | `P7` |
| 已投稿 / 已发表且论文链路已结束 | `complete` |

若证据不足，不要乐观跳到更后阶段；宁可设早一阶段，也不要伪造已完成状态。

#### 5.2 构建 history

为已完成的阶段构建 history 条目：

```python
# 示例：项目已有方法+实验设计（初步阶段 = I）
history = [
    {"phase": "C", "outcome": "done", "date": "<同化日期>", "mode": "assimilated"},
    {"phase": "RS", "outcome": "pass", "date": "<同化日期>", "mode": "assimilated"},
    {"phase": "P", "outcome": "signal", "date": "<同化日期>", "mode": "assimilated"},
    {"phase": "D", "outcome": "done", "date": "<同化日期>", "mode": "assimilated"},
    {"phase": "RT", "outcome": "pass", "date": "<同化日期>", "mode": "assimilated"},
]
```

规则：
- 所有 assimilated history 条目添加 `"mode": "assimilated"` 标记
- 使用当天日期
- outcome 使用正常路径的值（done/pass/signal 等）
- 只为**已完成**的阶段添加 history，不为当前阶段添加

同时，为每个已完成的 research phase 写入对应的 `phase-outcomes/<phase>.json`：

```json
{
  "outcome": "<history 中的 outcome>",
  "notes": "assimilated from <sources>"
}
```

这样 `praxis-present`、热启动判断和后续人工检查都能消费到一致的阶段摘要。

若存在论文 pipeline，同样为已完成的 paper phase 写入：
- `Papers/paper-status.json`
- `Papers/phase-outcomes/P*.json`

paper status 建议结构：

```json
{
  "phase": "<推断的 paper phase>",
  "history": [<已完成的 P1-P7 条目>],
  "revision_rounds": 0,
  "assimilated": true,
  "assimilated_date": "<当天日期>"
}
```

paper history 条目也添加 `"mode": "assimilated"`，与主 pipeline 保持一致。

#### 5.3 写入 pipeline-status.json

```json
{
  "phase": "<确定的阶段>",
  "history": [<构建的 history>],
  "assimilated": true,
  "assimilated_date": "<当天日期>",
  "notes": "由 /praxis-assimilate 纳入"
}
```

若 Step 4.3 的 review 覆盖把项目回退到上游阶段，必须写入与主状态机兼容的 `entry_context`：

- `RS = Revise -> C`：
  ```json
  {
    "mode": "rs_revise",
    "source_phase": "RS",
    "c_iteration_count": <history 中 C 的数量>
  }
  ```
- `RT = Revise -> D`：
  ```json
  {
    "mode": "rt_revise",
    "source_phase": "RT",
    "d_iteration_count": <history 中 D 的数量>
  }
  ```
- `RT = Fundamental -> C`：
  ```json
  {
    "mode": "execute_pivot",
    "source_phase": "RT",
    "diagnosis": "direction_level",
    "c_iteration_count": <history 中 C 的数量>
  }
  ```

只有在没有 review 覆盖、确实是首次进入当前阶段时，才不设 `entry_context`。

#### 5.4 处理 CLAUDE.md

按 v2 模板 `<noesis_root>/Praxis/templates/project-claude-md.md` 创建或更新。

关键字段：
- `Noesis 路径`: `~/Research/Noesis`
- 当前阶段信息
- 关键文档表（标注各文档状态：已重建/原始/占位）

如果存在论文 pipeline，也在 `CLAUDE.md` 中注明当前 paper phase（如 `P5`）。

---

### Step 6：完整同化报告

输出同化摘要，包含：

```
同化完成报告

## 文档重建
| 文档 | 状态 | 来源 |
|------|------|------|
| project-startup.md | 重建 | README + proposal |
| research/problem-statement.md | 重建 | 论文 Introduction |
| ... | ... | ... |

## 项目质量评估
- 方法学成熟度：[高/中/低] — [一句话说明]
- 实验完备性：[高/中/低] — [一句话说明]
- 可复现性：[高/中/低] — [一句话说明]
- 核心风险点：[列出 1-3 个最关键的风险]

## 评审结果
- RS 战略审查：[Pass/Revise/Block] — [摘要]
- RT 技术审查：[Pass/Revise/Fundamental/Block] — [摘要]

## Pipeline 状态
- 当前阶段：[阶段代号]（[阶段名称]）
- 评审覆盖：[是/否]（如是，原计划阶段 → 实际阶段）
- 论文阶段：[P1-P7/complete/无]

## 下一步
- 若当前阶段为 `W` 且 `Papers/paper-status.json` 已初始化：`/praxis-paper <project_path>`
- 其他研究阶段：`/praxis-research <project_path>`
```

---

## Exit Criteria

- [ ] 已深度阅读项目全部相关文件
- [ ] 已完成 DL 领域特有的质量评估（方法学成熟度、实验完备性、可复现性、贡献清晰度）
- [ ] 已与用户完成单轮确认
- [ ] 所有必要目录已创建（research/、inner-reviews/、codex-reviews/、phase-outcomes/）
- [ ] 所有缺失的 v2 阶段文档已生成（含 YAML frontmatter）
- [ ] 辅助文档已创建（contribution.md、pipeline-evolution-log.md、iteration-log.md、result.md）
- [ ] RS 真实评审已运行（4 debaters + synthesizer，model: opus），结果记录在 inner-reviews/ 和 phase-outcomes/
- [ ] RT 真实评审已运行（6 debaters + synthesizer，model: opus），结果记录在 inner-reviews/ 和 phase-outcomes/
- [ ] 评审结果已反馈到阶段设定（Revise/Block 覆盖原计划阶段）
- [ ] pipeline-status.json 已写入正确的当前阶段（含 history + assimilated 标记；如被 review 打回，含正确 entry_context）
- [ ] 已完成阶段的 `phase-outcomes/*.json` 已补齐
- [ ] 若项目含论文材料，`Papers/paper-status.json` 与 `Papers/phase-outcomes/` 已初始化
- [ ] CLAUDE.md 已创建或更新
- [ ] 同化报告已输出（含质量评估）

## 核心原则

- **一次问清，全程自动**
- **实际运行评审，而非跳过** — 使用完整的 debater + synthesizer 流程，model: opus
- **评审结果影响阶段** — 如果 RS/RT 不通过，不能设到下游阶段
- **同化产物必须可被下游模块消费** — 文件名、entry_context、phase-outcomes、paper-status 必须与当前 runner 对齐
- **内容优先于形式**
- **非破坏性** — 已有文件不覆盖
- **完全可继续** — 同化结束后，`/praxis-research` 可立即接管
- **逆向工程要诚实标注** — 从代码/结果逆推的设计文档必须标注来源和不确定性，避免给人"精心设计"的错觉
