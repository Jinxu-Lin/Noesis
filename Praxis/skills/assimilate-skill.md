# Skill: Project Assimilation（现有项目完整同化）

将任意状态的现有科研项目**完整纳入** Noesis/Praxis 框架，输出结果：所有阶段文档已生成、所有评审已完成、pipeline 状态精确对齐，可立即继续推进。

---

## 设计哲学

**不是"打标签"，是"真正完成工作"。**

同化不只是创建 JSON 文件和修改 CLAUDE.md——而是用 Noesis 的 AI 能力，从现有材料中完整重建每个阶段的产出文档，并实际运行 R3/R5/R7 评审。同化结束后，项目与从 `/praxis-start` 原生启动的项目无任何结构区别。

---

## 执行流程

### Step 0：前置检测

检查 `<project_path>/pipeline-status.json` 是否存在：
- **存在** → 读取并展示，询问用户"是否要重置并重新同化"，若否则退出（建议直接使用 `/praxis-research`）
- **不存在** → 继续

---

### Step 1：一次性深度扫描

**目标**：彻底理解这个项目，只问一轮问题，然后全自动执行。

#### 1.1 读取所有相关文件

扫描整个 `<project_path>`（忽略 `.git/`、`__pycache__/`、`.venv/`、`node_modules/`、`wandb/`、`runs/`），重点阅读：

**高价值文件（全文读取）**：
- `README.md`、`OVERVIEW.md`、`proposal.md`
- `*.pdf`（若可读）、`main.tex`、`paper.tex`、`draft.md`
- `research/gap-analysis.md`、`research/method-design.md`、`research/experiment-design.md`、`research/contribution.md`
- `related-work.md`、`literature-review.md`、`survey.md`
- `retrospective.md`、`iteration-log.md`

**代码结构（只读 README + 目录树 + 关键模块顶部注释）**：
- `src/`、`code/`、`scripts/`下的主要 `.py` 文件（只读前 50 行）
- `requirements.txt`、`environment.yml`、`setup.py`
- `configs/` 下的配置文件

**实验结果（存在性 + 摘要）**：
- `results/`、`experiments/` 目录下的 `.csv`/`.json` 结果文件（只读文件名和少量内容）
- `wandb/`、`runs/` 目录（只确认存在）

#### 1.2 构建项目理解

基于阅读，在内部建立对项目的完整理解：
- **研究问题**：项目在解决什么问题？
- **现有方法**：核心方法/算法是什么？
- **实验状态**：实验做到了什么程度？有哪些结果？
- **论文状态**：有草稿/已投/已发表？
- **缺失部分**：哪些 Noesis 阶段文档不存在？

---

### Step 2：单轮用户确认

向用户展示扫描摘要，只问**一个问题**：

```
扫描完成：~/Research/my-paper/

项目理解：
  研究问题：[你提炼出的一句话描述]
  方法：[核心方法摘要]
  当前状态推断：[代码已有 + 实验结果存在 → 推断在 coding 阶段]

推断当前阶段：coding（代码和实验结果存在，论文草稿尚未发现）

同化计划：
  [重建] project-startup.md — 从 README.md 提炼
  [重建] research/gap-analysis.md — 从论文 Related Work 段落提炼
  [评审] 运行 R3 Gap 评审
  [重建] research/method-design.md — 从论文 Method 章节提炼
  [评审] 运行 R5 Method 评审
  [重建] research/experiment-design.md — 从实验配置和结果提炼
  [评审] 运行 R7 Experiment 评审
  [重建] Codes/ 规划文档 — 从现有代码结构提炼
  → 最终设置状态：coding

这是你的意图吗？还是有什么我理解错了？
[yes / 修正描述 / 我来告诉你当前阶段]
```

用户可以：
- **直接确认**：执行计划
- **描述修正**：告知哪里理解有误，重新规划
- **直接告知阶段**：跳过推断，直接指定当前阶段（会重建该阶段之前所有文档）

---

### Step 3：文档重建

对每个"需要重建"的阶段，从现有材料中生成 Noesis 标准格式文档。

#### 重建规则

- **已有对应文档**（文件存在且有实质内容）→ 直接使用，追加 `> [原始文档，由 /praxis-assimilate 纳入]` 标注
- **有源材料但无文档** → 生成，在文件顶部标注 `> [ASSIMILATED: generated from <来源> by /praxis-assimilate]`
- **无任何源材料** → 生成占位文档，标注 `> [ASSIMILATED: synthesized from project context, requires verification]`

#### Step 3.1：project-startup.md

若不存在：从 README、proposal、论文 Abstract+Introduction 提炼：
- 研究背景与动机
- 核心研究问题
- 预期贡献
- 目标 venue（若已知）

#### Step 3.2：research/gap-analysis.md

若不存在：从以下来源提炼：
- 论文 Related Work / Introduction 中的 gap 陈述
- 现有 literature-review.md 或 survey.md
- 代码中 `# TODO: baseline comparison` 类注释暗示的空白

提炼格式遵循 `<noesis_root>/Praxis/templates/gap-analysis.md` 模板。

#### Step 3.3：research/method-design.md

若不存在：从以下来源提炼：
- 论文 Method/Approach 章节
- 代码核心模块（`src/methods/`、`src/models/` 等）的结构和注释
- 配置文件中的超参数和模块定义

提炼时保留数学公式，分析各组件的可解耦性。

#### Step 3.4：research/experiment-design.md

若不存在：从以下来源提炼：
- 论文 Experiments 章节（baselines、datasets、metrics）
- 实验配置文件（`config.yaml`、`args.py` 等）
- results/ 目录下的实验结果文件（反推实验设计）

#### Step 3.5：Codes/ 目录（若不存在且代码已有）

生成 `Codes/code-todo.md`（从现有代码结构反向提炼，标注已完成部分）和 `Codes/experiment-todo.md`（标注已完成和待完成实验）。

**若代码和实验都已完成**：Codes/ 内容全部标注为 [已完成]。

---

### Step 4：实际运行评审

对重建（或已有）的关键文档，用 Agent tool fork 独立评审 subagent 运行真实的 Noesis 评审。

#### Step 4.1：R3 Gap 评审

Fork 一个重量级评审 agent，传入：
- `research/gap-analysis.md` 全文
- `<noesis_root>/Praxis/skills/1X-review-skill.md` 内容（review_type=gap）
- 评审任务：对 gap analysis 进行严格独立评审，输出 pass/revise

**若评审结果为 pass** → 写入 `phase-outcomes/R3.json: {"outcome": "pass", ...}`

**若评审结果为 revise** → 根据评审意见修订 `research/gap-analysis.md`，然后重新评审（最多 1 轮修订；若仍 revise，写入 `{"outcome": "revise_flagged", ...}` 并在报告中提示用户）

#### Step 4.2：R5 Method 评审

同上，fork agent 评审 `research/method-design.md`。

#### Step 4.3：R7 Experiment 评审

同上，fork agent 评审 `research/experiment-design.md`。

**注意**：若项目已发表/已投稿，评审时在 prompt 中注明"该方法已经过同行评审并发表"，评审者应以更宽松的标准处理（重点在于文档质量而非方法本身）。

---

### Step 5：写入 Pipeline 状态

#### 5.1 确定当前阶段

基于重建和评审结果，确定项目应处于哪个阶段：

| 项目实际状态 | 设置阶段 |
|------------|---------|
| 只有想法/早期 | R2（从 Gap Discovery 开始） |
| Gap 分析已完成，但没有方法 | R4 |
| 方法已有，但实验未设计 | R6 |
| 实验已设计，但代码未写 | R8 |
| 代码已有，实验未完成 | coding |
| 实验已完成，无论文 | coding → paper_writing（询问用户） |
| 有论文草稿 | paper_writing |
| 已投稿/已发表 | R11 |
| 有完整回顾文档 | complete |

#### 5.2 写入文件

**`phase-outcomes/<phase>.json`**（对所有已完成阶段）：
```json
{
  "outcome": "<done|pass|success>",
  "notes": "[ASSIMILATED] <来源描述>",
  "assimilated": true,
  "evidence": ["<文件1>", "<文件2>"],
  "confidence": "<high|medium>",
  "review_run": true
}
```

评审阶段（R3/R5/R7）的 `review_run: true` 表示确实运行了真实评审（非跳过）。

**`pipeline-status.json`**：
```json
{
  "phase": "<current_phase>",
  "assimilated": true,
  "assimilation_date": "<date>",
  "history": [...],
  "last_updated": "<date>"
}
```

**规则**：不覆盖已存在的 `phase-outcomes/*.json`（已有的比重建的优先级高）。`pipeline-status.json` 若已存在，需用户明确确认后才覆盖。

#### 5.3 处理 CLAUDE.md

- **不存在** → 从模板 `<noesis_root>/Praxis/templates/project-claude-md.md` 创建，填入项目信息，填写完整的"关键文档"和"当前状态"章节
- **已存在无 `noesis_path`** → 在末尾追加 `Praxis Integration` 节（不修改现有内容）
- **已存在有 `noesis_path`** → 只更新"当前状态"节（如果存在该节）

---

### Step 6：完整同化报告

```
同化完成：~/Research/my-paper/

重建的文档：
  ✓ project-startup.md [从 README.md + Abstract 生成]
  ✓ research/gap-analysis.md [从 Related Work 提炼]
  ✓ research/method-design.md [从 Method 章节 + src/models/ 提炼]
  ✓ research/experiment-design.md [从 Experiments 章节 + configs/ 提炼]
  ✓ Codes/code-todo.md [从现有代码结构反向生成，全部标注已完成]

评审结果：
  ✓ R3 Gap 评审：PASS（评审意见：gap 陈述清晰，可攻击性强）
  ✓ R5 Method 评审：PASS（1 轮修订后通过）
  ✓ R7 Experiment 评审：PASS

当前阶段：coding（代码已有，实验结果已存在）
推荐下一步：
  论文写作：/praxis-goto ~/Research/my-paper/ paper_writing
           → /praxis-paper ~/Research/my-paper/

注意：所有 [ASSIMILATED] 文档是从现有材料提炼的，建议通读一遍确认准确性。
     如有偏差，直接编辑对应文档即可，不影响 Noesis pipeline 使用。
```

---

## Exit Criteria

- [ ] 已深度阅读项目全部相关文件
- [ ] 已与用户完成单轮确认
- [ ] 所有缺失的 Noesis 阶段文档已生成（project-startup.md、research/gap-analysis.md、research/method-design.md、research/experiment-design.md）
- [ ] R3/R5/R7 真实评审已运行（fork agent），结果已记录
- [ ] 所有 phase-outcomes/*.json 已写入（不覆盖已有文件）
- [ ] pipeline-status.json 已写入正确的当前阶段
- [ ] CLAUDE.md 已创建或更新（含 noesis_path）
- [ ] 同化报告已输出，含推荐的下一步命令

## 核心原则

- **一次问清，全程自动** — 最多一轮用户交互，之后完全自主执行
- **实际运行评审，而非跳过** — R3/R5/R7 fork 真实 agent，不用"用户确认代替评审"
- **内容优先于形式** — 重建的文档内容准确比格式完美更重要；追加的标注说明出处
- **非破坏性** — 已有文件不覆盖（phase-outcomes/*.json 优先级高于重建；现有文档保留）
- **完全可继续** — 同化结束后，`/praxis-research` 或 `/praxis-paper` 可立即接管
