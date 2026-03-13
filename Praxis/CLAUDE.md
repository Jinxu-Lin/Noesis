# CLAUDE.md — Praxis 子系统

This file provides guidance to Claude Code when working within the Praxis subsystem.

## What Praxis Is

Praxis 是 Noesis 的**研究执行子系统**，独立于 Logos 运行。分为五大模块：

```
┌─────────────────────────────────────────────────────────────┐
│  Module 1: Startup (/praxis-start)                          │
│    交互式项目种子孵化（六维辩论压力测试）     ← 交互式 🗣️   │
│    完成后设状态 → C，进入 Research 模块                      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Module 2: Research (/praxis-research)   ← 自动化 + 手动    │
│    C   Crystallize (问题锐化)           ← Episteme: Gaps    │
│    RS  Strategic Review 🔒 + Codex      ← 4 debaters 战略审查│
│    P   Probe (探针实验)                 ← 手动 🔧            │
│    D   Joint Design (联合设计)          ← Episteme: Methods  │
│    RT  Technical Review 🔒 + Codex      ← 6 debaters 技术审查│
│    I   Implementation (实现规划)        ← 产出 Codes/ 规划   │
│    E   Execution (实验执行)             ← 手动 🔧            │
│    W   Paper Writing (论文写作)         ← 独立 paper pipeline │
│    R   Retrospective (知识回收)         ← 流程末尾，可标记验证│
└─────────────────────────────────────────────────────────────┘
                            ↓ (R 完成 → complete)
┌─────────────────────────────────────────────────────────────┐
│  Module 3: Evolution (/praxis-evolve)                       │
│    ├── 跨项目 Lessons → ~/.noesis/lessons/（自动注入）       │
│    └── 框架进化 → pipeline-evolution-log → Noesis 文档更新  │
└─────────────────────────────────────────────────────────────┘
```

正常流程：`S → C → RS(pass) → P(signal) → D → RT(pass) → I → E(success) → W → R → complete`

此外还有两个辅助功能，可在任意阶段调用：

- **`/praxis-assimilate`** — 同化现有项目：将任意状态的外部科研项目纳入 Noesis 框架，重建阶段文档、实际运行 RS/RT 评审、写入状态文件，使其可被 `/praxis-research` 或 `/praxis-paper` 直接接管。
- **`/praxis-present`** — 进展演示：读取项目当前状态，生成结构化的 `presentation.md`，用于与导师或合作者的进展汇报会议。支持热启动（已有 presentation.md 时增量更新，保留人工编辑）。

## Paths

| 路径 | 说明 |
|------|------|
| Praxis 系统 | `~/Research/Noesis/Praxis` |
| 知识库 (Episteme) | `~/Research/Episteme` |
| 研究项目 | `~/Research/<项目名>` |
| Cross-project lessons | `~/.noesis/lessons/` |

所有路径使用 `~`，勿硬编码用户名（多 Mac 协作）。

## Quick Start

### 1. 启动新项目

```
/praxis-start <项目名>
```

交互式创建项目，在 `~/Research/<项目名>/` 下生成 `CLAUDE.md`、`pipeline-status.json`、`project-startup.md` 等，完成后自动设置状态为 C。

### 2. 运行研究模块

```
/praxis-research <项目路径>
```

自动执行 C→RS→P→D→RT→I→E→W→R：问题锐化、两轮独立审查（RS 战略审查 + RT 技术审查，含 Codex 并行）、探针实验、方法+实验联合设计、实现规划、实验执行、论文写作、知识回收。手动阶段（P、E、W）等待研究者操作后通过 `advance --outcome` 推进。

### 3. 编码阶段总结（验证失败时）

```
/praxis-conclude <项目路径>
```

交互式分析失败原因。v2 采用分层回退：方法层问题 → 回退到 D（联合设计）；方向层问题 → 回退到 C（问题锐化）。写入 `iteration-log.md` + `research/result.md`，然后 `/praxis-research` 热重启。

### 4. 论文写作

```
/praxis-paper <项目路径>
```

### 5. 自我进化

```
/praxis-evolve <项目路径>
```

项目完成后，提取跨阶段经验教训写入 `~/.noesis/lessons/`（两个产出：lessons 自动注入 + Noesis 框架文档更新）。

### 辅助命令

```
/praxis-assimilate <项目路径>   ← 将外部项目纳入 Noesis 框架
/praxis-present <项目路径>      ← 生成进展演示文档（支持热启动）
```

## Orchestrator CLI

`research_runner.py` 是科研模块的执行骨架，**始终通过 `research_runner.py` 操作**（除 `init-phase` 外不要直接调用 `research_state_machine.py`）。

```bash
# 获取下一步动作（返回 JSON，含 fork_prompt）
python3 ~/Research/Noesis/Praxis/orchestrator/research_runner.py next    <project_path>

# 推进状态（自动化阶段：fork agent 写完 phase-outcomes 后调用）
python3 ~/Research/Noesis/Praxis/orchestrator/research_runner.py advance <project_path>

# 推进状态（手动阶段 P/E/W：研究者指定 outcome）
python3 ~/Research/Noesis/Praxis/orchestrator/research_runner.py advance <project_path> --outcome <outcome>

# 查看状态
python3 ~/Research/Noesis/Praxis/orchestrator/research_runner.py status  <project_path>

# 强制设置阶段（恢复/覆盖）
python3 ~/Research/Noesis/Praxis/orchestrator/research_state_machine.py init-phase <project_path> <phase>
```

**手动阶段 outcome 值**：

| 阶段 | 可用 outcome | 含义 |
|------|-------------|------|
| P | `signal` | 有信号，进入联合设计 D |
| P | `pivot` | 无信号，换攻击角度，回退到 C |
| P | `abandon` | 放弃，进入 R |
| E | `success` | 验证通过，进入论文写作 W |
| E | `iterate_method` | 方法层问题，回退到 D |
| E | `iterate_direction` | 方向层问题，回退到 C |
| E | `abandon` | 放弃，进入 R |
| W | `done` | 论文完成，进入知识回收 R |

状态持久化在 `<project>/pipeline-status.json`（含 `entry_context` + `history`）。Fork agent 将结果写入 `<project>/phase-outcomes/<phase>.json`，格式为 `{"outcome": "...", "notes": "..."}`。

### Paper Writing Orchestrator

`paper_runner.py` 是论文写作模块的执行骨架，**始终通过 `paper_runner.py` 操作**（除 `init-phase` 外不要直接调用 `paper_state_machine.py`）。

```bash
# 获取下一步动作（返回 JSON，含 fork_prompt）
python3 ~/Research/Noesis/Praxis/orchestrator/paper_runner.py next    <project_path>

# 推进状态（fork agent 写完 phase-outcomes 后调用）
python3 ~/Research/Noesis/Praxis/orchestrator/paper_runner.py advance <project_path>

# 查看状态
python3 ~/Research/Noesis/Praxis/orchestrator/paper_runner.py status  <project_path>

# 强制设置阶段（恢复/覆盖）
python3 ~/Research/Noesis/Praxis/orchestrator/paper_state_machine.py init-phase <project_path> <phase>
```

状态持久化在 `<project>/Papers/paper-status.json`。Fork agent 将结果写入 `<project>/Papers/phase-outcomes/<phase>.json`，格式为 `{"outcome": "...", "notes": "..."}`。

## Three Agent Tiers

| Tier | 模型 | 角色 | 阶段 |
|------|------|------|------|
| `standard` | claude-sonnet-4-6 | AI Co-Author，执行性/模板化工作 | I, P2, P4, P6 |
| `heavy` | claude-opus-4-6 | 发散性思考 / 独立批判审查 | C, RS, D, RT, R, P1, P3, P5, P7 |
| `codex` | gpt-4.5-high | 可选外部 AI 审查，提供第三方视角 | RS, RT, P3, P7（并行） |

Runner 根据 tier 为 fork agent 注入不同的 preamble：

- **Standard**：作为研究合作者，基于上下文忠实执行当前阶段的工作任务。
- **Heavy**：以严格独立评审人/综合决策者身份工作，上下文隔离，批判性、不妥协的评估。
- **Codex**：通过 Codex MCP 调用 GPT-4.5-high，完全独立的第三方外部审查者；non-blocking，MCP 不可用时自动跳过，不影响主流程路由。

## Pipeline Phase Map

**Module 1: Startup**

| Phase | Skill | Type | Tier |
|-------|-------|------|------|
| S (startup) | `start-skill` | interactive 🗣️ | standard |

Startup 完成后通过 `init-phase` 将状态设为 C，由 `/praxis-research` 接管。

**Module 2: Research**

| Phase | Skill | Type | Tier | Codex | Multi-Agent |
|-------|-------|------|------|-------|-------------|
| C | `crystallize` | work | heavy | — | — |
| RS | `strategic-review` | review 🔒 | heavy | ✓ | 4 debaters + synthesizer |
| P | — | manual 🔧 | — | — | — |
| D | `joint-design` | work | heavy | — | — |
| RT | `technical-review` | review 🔒 | heavy | ✓ | 6 debaters + synthesizer |
| I | `implementation` | work | standard | — | — |
| E | — | manual 🔧 | — | — | — |
| W | — | manual 🔧 (独立 paper pipeline) | — | — | — |
| R | `retrospective` | work | heavy | — | — |

**Review 出口路由**：

RS (战略审查)：`pass`→P / `revise`→C / `abandon`→R
RT (技术审查)：`pass`→I / `revise`→D / `fundamental`→C / `abandon`→R

**手动阶段出口路由**：

P (探针实验)：`signal`→D / `pivot`→C / `abandon`→R
E (实验执行)：`success`→W / `iterate_method`→D / `iterate_direction`→C / `abandon`→R
W (论文写作)：`done`→R

**RS Debaters（战略层面）**：

| Debater | 核心视角 |
|---------|---------|
| Contrarian | 构建最强反驳：Gap 真实性、攻击角度致命缺陷 |
| Comparativist | 文献对照 + 在线搜索：Gap 新颖性、近期竞争工作 |
| Pragmatist | 可行性约束：探针可执行性、资源约束 |
| Interdisciplinary | 跨领域视角：替代问题框定、替代攻击角度 |

**RT Debaters（技术层面）**：

| Debater | 核心视角 |
|---------|---------|
| Theorist | 数学/理论正确性：逻辑闭合、理论保证、隐含假设 |
| Methodologist | 评估协议完整性：数据泄漏、超参选择、ablation 覆盖 |
| Empiricist | 实验科学性：Dim 0→1 衔接、统计效力、baseline 公平 |
| Skeptic | 极端怀疑：最弱组件、最可能失败点、替代解释 |
| Pragmatist | 工程可行性：计算资源、实现复杂度、时间估计 |
| Contrarian | 构建最强反驳：与探针结果的一致性、过拟合探针信号风险 |

**Module 3: Paper（独立状态机）**

| Phase | Skill | Type | Tier | Codex |
|-------|-------|------|------|-------|
| P1 | `30-paper-outline` | work | heavy | — |
| P2 | `31-paper-sections` | work | standard | — |
| P3 | `32-paper-critique` | work 🔒 | heavy | ✓ |
| P4 | `33-paper-integrate` | work | standard | — |
| P5 | `34-paper-review` | paper_review 🔒 | heavy | — |
| P6 | `35-paper-latex` | work | standard | — |
| P7 | `36-project-review` | work 🔒 | heavy | ✓ |

P5: 评分 < 7.0 → 回到 P4（最多 2 轮，超限强制通过）。

🗣️ = 与研究者交互。🔧 = 人工阶段。🔒 = 独立审查（上下文隔离）。

## File Layout

```
Praxis/
├── CLAUDE.md                              ← 本文件
├── orchestrator/
│   ├── research_state_machine.py          ← 研究 pipeline 状态机（S→C→RS→P→D→RT→I→E→W→R）
│   ├── research_runner.py                 ← 研究 pipeline runner（含 --outcome 支持）
│   ├── paper_state_machine.py             ← 论文 pipeline 状态机（P1-P7）
│   └── paper_runner.py                    ← 论文 pipeline runner
├── skills/                                ← 非自动化模块的详细指令（由 .claude/skills/ 薄包装调用）
│   ├── start-skill.md                     ← /praxis-start 详细指令（含六维辩论）
│   ├── conclude-skill.md                  ← /praxis-conclude 详细指令（含分层回退诊断）
│   ├── assimilate-skill.md                ← /praxis-assimilate 详细指令
│   ├── evolve-skill.md                    ← /praxis-evolve 详细指令
│   └── present-skill.md                   ← /praxis-present 详细指令
├── prompts/                               ← 状态机 fork agent 指令（runner 自动加载）
│   ├── crystallize-prompt.md              ← C 问题锐化（gap + 攻击角度 + 探针设计）
│   ├── strategic-review-prompt.md         ← RS 战略审查（4 debaters）
│   ├── probe-guide.md                     ← P 探针实验执行指南（手动阶段参考）
│   ├── joint-design-prompt.md             ← D 联合设计（方法 + 实验，交叉引用）
│   ├── technical-review-prompt.md         ← RT 技术审查（6 debaters）
│   ├── implementation-prompt.md           ← I 实现规划（含探针代码复用评估）
│   ├── retrospective-prompt.md            ← R 知识回收（流程末尾，支持 validated/refuted）
│   ├── 30-paper-outline-prompt.md         ← P1 论文大纲
│   ├── 31-paper-sections-prompt.md        ← P2 章节写作
│   ├── 32-paper-critique-prompt.md        ← P3 多角色审查
│   ├── 33-paper-integrate-prompt.md       ← P4 编辑整合
│   ├── 34-paper-review-prompt.md          ← P5 终审
│   ├── 35-paper-latex-prompt.md           ← P6 LaTeX 编译
│   ├── 36-project-review-prompt.md        ← P7 项目级审查
│   ├── codex-reviewer-prompt.md           ← 可复用 Codex 外部审查者
│   ├── codex-writer-prompt.md             ← Codex 写作辅助
│   ├── X-reflect-pipeline-prompt.md       ← 跨阶段流程反思（每阶段自动注入）
│   └── review-configs/                    ← 审查配置（YAML）
│       ├── strategic-review.yaml          ← RS 审查维度（7 项）
│       └── technical-review.yaml          ← RT 审查维度（10 项，方法+实验+联合）
├── subagents/                             ← SubAgent prompt 模板
│   ├── — Startup 六维辩论（/praxis-start Step 4）—
│   ├── innovator-subagent.md              ← 创新者
│   ├── pragmatist-subagent.md             ← 务实者
│   ├── theorist-subagent.md               ← 理论家
│   ├── contrarian-subagent.md             ← 反对者
│   ├── interdisciplinary-subagent.md      ← 跨学科者
│   ├── empiricist-subagent.md             ← 实验主义者
│   ├── synthesizer-subagent.md            ← 综合者（汇总六维辩论结果）
│   ├── — 其他专用子 Agent —
│   ├── comparativist-subagent.md          ← 对比分析者（RS debater）
│   ├── methodologist-subagent.md          ← 方法论者（RT debater）
│   ├── skeptic-subagent.md                ← 怀疑论者（RT debater）
│   ├── work-synthesizer-subagent.md       ← 工作综合者
│   ├── paper-critic-subagent.md           ← 论文审查（5 角色）
│   └── exit-assessment-subagent.md        ← 退出评估
└── templates/
    ├── project-claude-md.md               ← 新项目 CLAUDE.md 模板
    ├── project-start.md                   ← Startup 输出模板（含候选攻击角度字段）
    ├── problem-statement.md               ← C 输出模板（gap + 攻击角度 + 探针方案）
    ├── method-design.md                   ← D 输出模板（含实验交叉引用格式）
    ├── experiment-design.md               ← D 输出模板（含方法反向引用格式）
    ├── contribution.md                    ← 跨阶段贡献跟踪
    ├── iteration-log.md                   ← 迭代历史（conclude 追加，含版本号+排除方向）
    ├── result.md                          ← 实验结果与洞察（conclude 追加）
    ├── retrospective.md                   ← R 输出模板
    ├── probe-results.md                   ← P 输出模板（探针实验结果）
    ├── proposal.md                        ← 提案模板
    ├── experiment-todo.md                 ← 实验待办（I 产出）
    └── pipeline-evolution-log.md          ← 流水线演进日志（X-reflect 追加）
```

## Cross-Project Learning

项目 R (Retrospective) 完成后，运行 `/praxis-evolve` 产出两类成果：

1. **跨项目 Lessons** → `~/.noesis/lessons/<skill_name>.md`：含类别标签 `[SYSTEM/EXPERIMENT/WRITING/...]`、频率标签 `[RECURRING/NEW]`、有效性标签 `[✓verified/✗ineffective/?unverified]`。Runner 在后续项目的相同阶段自动注入有效 lessons；`[✗ineffective]` 自动过滤；`[RECURRING]` 排在最前。

2. **框架进化** → 基于 `pipeline-evolution-log.md` 中各阶段的 X-reflect 条目，更新 `Praxis/prompts/`、`Praxis/skills/`、`Praxis/templates/` 文档，并 push 到 Noesis GitHub。

v2 中 skill name 变更（影响 lessons 文件名映射）：`10-gap-discovery` → `crystallize`；`1X-review` → `strategic-review` / `technical-review`；`11-method-design` + `12-experiment-design` → `joint-design`；`13-impl-planning` → `implementation`；`14-retrospective` → `retrospective`。

## Key Behaviors

**Pipeline 流程**
- **正常流程**：Startup (`/praxis-start`) → C → RS → P → D → RT → I → E → W → R → complete
- **R (Retrospective) 时机**：在 W (论文写作) 完成后或 abandon 时执行（流程末尾），可基于实验结果标记知识资产为 `[✓ validated]` / `[✗ refuted]` / `[~ partially validated]`
- **P (Probe) 探针实验**：全新手动阶段，在 RS 通过后、D 联合设计前执行。用最小成本验证核心直觉，前置经验信号获取。时间预算由 C 阶段在 problem-statement.md §3.4 定义（小时级）
- **分层回退**：v2 采用按失败根因层次回退，而非统一回退。方法层问题 → 回退到 D（保留 problem-statement.md）；方向层问题 → 回退到 C（重新审视 Gap 和攻击角度）。`/praxis-conclude` 增加失败层次诊断（执行层/方法层/方向层）
- **迭代守卫**：D 回退 >= 2 次 → 强制升级到 C 回退；C 回退 >= 3 次 → 触发 abandon 评估（Exit Assessment Gate SubAgent）

**文档版本控制**
- **单文件 + 元数据版本号**：每个研究文档头部 YAML frontmatter 记录 `version`、`entry_mode`、`iteration_major`、`iteration_minor`
- **版本号规则**：Major（大迭代，E/P 回退重写）`1.x → 2.0`；Minor（review 后修改）`1.0 → 1.1`
- **审查文档覆盖策略**：`inner-reviews/` 下的审查文档每次覆盖旧版，不保留历史
- **iteration-log.md 倒序排列**：最新在最上方，排除方向和关键洞察必须记录

**Startup 六维辩论**
- `/praxis-start` 的 Step 4 并行召唤 6 个辩论 Agent（创新者、务实者、理论家、反对者、跨学科者、实验主义者），再由综合者汇总判定（方向确认/强化/修正/HIGH RISK）
- Startup 输出模板增加"候选攻击角度"字段（1-2 段描述，为 C 阶段提供起点）
- 辩论结果完整纳入 `project-startup.md`，进入 C 时带着已知风险列表
- Step 7 完成 Git 初始化 + GitHub repo 创建，设状态为 C

**迭代模式（Runner 自动注入上下文）**
- **RS-Revise 模式**：`inner-reviews/strategic-review.md` 存在 → C 阶段提示"基于审查意见修改，不从零开始"
- **Probe-Pivot 模式**：P 阶段返回 pivot → C 阶段读 `probe-results.md` + `iteration-log.md`，换攻击角度，严禁重复已排除方向
- **RT-Revise 模式**：`inner-reviews/technical-review.md` 存在 → D 阶段提示"基于技术审查修改"
- **Execute-Iterate 模式**：E 阶段方法层失败 → D 阶段读 `result.md` + `iteration-log.md`，修改失败组件，保留有效组件
- **Execute-Pivot 模式**：E 阶段方向层失败 → C 阶段重新审视 Gap 和攻击角度
- **迭代守卫**：研究 pipeline D 回退 >= 2 次强制升级到 C；C 回退 >= 3 次触发 abandon 评估

**Entry Context 注入逻辑**

| mode | 注入的额外文档 | 注入的指令关键词 |
|------|--------------|----------------|
| `first` | （无） | "从零开始" |
| `rs_revise` | `inner-reviews/strategic-review.md` | "基于审查修改，不重启" |
| `probe_pivot` | `research/probe-results.md` + `iteration-log.md` | "探针失败，换攻击角度，禁止重复已排除方向" |
| `rt_revise` | `inner-reviews/technical-review.md` | "基于技术审查修改" |
| `execute_iterate` | `research/result.md` + `iteration-log.md` | "方法层问题，修改失败组件，保留有效组件" |
| `execute_pivot` | `research/result.md` + `iteration-log.md` + 下游文档(参考) | "方向层问题，重新审视 Gap 和攻击角度" |

**Paper 独立状态机**
- `paper_state_machine.py` + `paper_runner.py`，状态在 `Papers/paper-status.json`，与主 pipeline 完全解耦
- P5 修订循环：评分 < 7.0 → P4，最多 2 轮，超限强制通过
- P7 项目级审查：Critic + Supervisor + 可选 Codex 外部 AI 多视角审查

**架构原则**
- **三层架构**：Orchestrator (runner.py) 决定 WHAT/WHEN + 构建 fork_prompt；Prompts (prompts/*-prompt.md) 是纯 agent 指令；Slash commands (.claude/skills/) 是薄封装
- **Prompt 解耦原则**：prompt 自包含、不引用阶段代号、不感知迭代机制、不感知 tier。迭代上下文和 tier preamble 由 Runner 注入
- **`skills_parallel` 行动类型**：PHASES 含 `codex_agent` 字段时，runner 返回 `skills_parallel`，同时启动 main + codex Agent；main 写 `phase-outcomes/`（决定路由），codex 写 `codex-reviews/`（仅参考）
- **单一事实源**：主 pipeline `pipeline-status.json`（含 `entry_context` + `history` 数组），论文模块 `Papers/paper-status.json`
- **X-reflect 自动注入**：每个非 manual 阶段完成后，runner 自动在 fork_prompt 末尾注入 `X-reflect-pipeline-prompt.md`，agent 将反思追加到 `pipeline-evolution-log.md`

## Adding or Modifying a Phase

1. 编辑 `research_state_machine.py` 中的 `PHASES` 字典 — 添加 phase key、skill name、output_doc、tier、outcome_type、transitions map；手动阶段设 `skill: None, outcome_type: "manual"`
2. 创建或更新 `prompts/<skill_name>-prompt.md`（遵循标准 Prompt 结构：角色与核心目标 → 输入文档 → 行动流程 → 输出规范 → 迭代上下文处理 → 禁止事项）
3. 如果是审查阶段，添加 `prompts/review-configs/<type>-review.yaml`，定义 `debate_agents` 列表和审查维度
4. 如果需要 Codex 并行审查，在 PHASES 条目中添加 `"codex_agent": "codex-reviewer"`
5. 如果是手动阶段，在 Runner 中支持 `--outcome` 参数和对应的 transition 值
6. 如需新增 debater SubAgent，在 `subagents/` 下创建 `<role>-subagent.md`
7. 更新本文件（`Praxis/CLAUDE.md`）和根目录 `Noesis/CLAUDE.md` 的阶段表
