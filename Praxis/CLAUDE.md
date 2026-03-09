# CLAUDE.md — Praxis 子系统

This file provides guidance to Claude Code when working within the Praxis subsystem.

## What Praxis Is

Praxis 是 Noesis 的**研究执行子系统**，独立于 Logos 运行。分为五大模块：

```
┌─────────────────────────────────────────────────────────────┐
│  Module 1: Startup (/praxis-start)                          │
│    交互式项目种子孵化（六维辩论压力测试）     ← 交互式 🗣️   │
│    完成后设状态 → R1，进入 Research 模块                     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Module 2: Research (/praxis-research)   ← 自动化循环       │
│    R1  Gap Discovery                   ← Episteme: Gaps     │
│    R2  Gap Review 🔒 + Codex           ← 独立审查           │
│    R3  Method Design                   ← Episteme: Methods  │
│    R4  Method Review 🔒 + Codex        ← 独立审查           │
│    R5  Experiment Design               ← Episteme: Patterns │
│    R6  Experiment Review 🔒 + Codex    ← 独立审查           │
│    R7  Impl Planning                   ← 产出 Codes/ 规划   │
│    R8  Retrospective                   ← 知识回收，进入 coding 前
└─────────────────────────────────────────────────────────────┘
                            ↓ (R1→R8 完成)
┌─────────────────────────────────────────────────────────────┐
│  Module 3: Code (manual)                 ← 人机协作 🔧      │
│    人工编码 & 实验                                           │
│    ├── 验证通过 → /praxis-paper 启动论文模块                 │
│    └── 验证失败 → /praxis-conclude → /praxis-research 热重启 │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Module 4: Paper (/praxis-paper)         ← 独立状态机       │
│    P1  Outline         ← 从研究文档映射论文结构              │
│    P2  Sections        ← 顺序写作各章节                     │
│    P3  Critique        ← 多角色并行审查（全文视角）🔒 + Codex│
│    P4  Integrate       ← 编辑整合 + Abstract 精炼           │
│    P5  Final Review    ← 会议级终审（< 7.0 → P4，最多2轮）  │
│    P6  LaTeX           ← 编译 PDF                           │
│    P7  Project Review  ← 多视角项目级审查 🔒 + Codex        │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Module 5: Evolution (/praxis-evolve)                       │
│    ├── 跨项目 Lessons → ~/.noesis/lessons/（自动注入）       │
│    └── 框架进化 → pipeline-evolution-log → Noesis 文档更新  │
└─────────────────────────────────────────────────────────────┘
```

此外还有两个辅助功能，可在任意阶段调用：

- **`/praxis-assimilate`** — 同化现有项目：将任意状态的外部科研项目纳入 Noesis 框架，重建阶段文档、实际运行 R2/R4/R6 评审、写入状态文件，使其可被 `/praxis-research` 或 `/praxis-paper` 直接接管。
- **`/praxis-present`** — 进展演示：读取项目当前状态，生成结构化的 `presentation.md`，用于与导师或合作者的进展汇报会议。支持热启动（已有 presentation.md 时增量更新，保留人工编辑）。

## Paths

| 路径 | 说明 |
|------|------|
| Praxis 系统 | `~/Documents/Noesis/Praxis` |
| 知识库 (Episteme) | `~/Documents/Episteme` |
| 研究项目 | `~/Documents/<项目名>` |
| Cross-project lessons | `~/.noesis/lessons/` |

所有路径使用 `~`，勿硬编码用户名（多 Mac 协作）。

## Quick Start

### 1. 启动新项目

```
/praxis-start <项目名>
```

交互式创建项目，在 `~/Documents/<项目名>/` 下生成 `CLAUDE.md`、`pipeline-status.json`、`project-startup.md` 等，完成后自动设置状态为 R1。

### 2. 运行研究模块

```
/praxis-research <项目路径>
```

自动执行 R1→R8：发现研究空白、三轮独立审查（R2/R4/R6，含 Codex 并行）、方法设计、实验规划、知识回收。R8 完成后进入人工编码阶段。

### 3. 编码阶段总结（验证失败时）

```
/praxis-conclude <项目路径>
```

交互式分析失败原因（L2 换组件 / L3 换框架 / L4 换方向），写入 `iteration-log.md`，重置状态，然后 `/praxis-research` 热重启。

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
python3 ~/Documents/Noesis/Praxis/orchestrator/research_runner.py next    <project_path>

# 推进状态（fork agent 写完 phase-outcomes 后调用）
python3 ~/Documents/Noesis/Praxis/orchestrator/research_runner.py advance <project_path>

# 查看状态
python3 ~/Documents/Noesis/Praxis/orchestrator/research_runner.py status  <project_path>

# 强制设置阶段（恢复/覆盖）
python3 ~/Documents/Noesis/Praxis/orchestrator/research_state_machine.py init-phase <project_path> <phase>
```

状态持久化在 `<project>/pipeline-status.json`。Fork agent 将结果写入 `<project>/phase-outcomes/<phase>.json`，格式为 `{"outcome": "...", "notes": "..."}`。

### Paper Writing Orchestrator

`paper_runner.py` 是论文写作模块的执行骨架，**始终通过 `paper_runner.py` 操作**（除 `init-phase` 外不要直接调用 `paper_state_machine.py`）。

```bash
# 获取下一步动作（返回 JSON，含 fork_prompt）
python3 ~/Documents/Noesis/Praxis/orchestrator/paper_runner.py next    <project_path>

# 推进状态（fork agent 写完 phase-outcomes 后调用）
python3 ~/Documents/Noesis/Praxis/orchestrator/paper_runner.py advance <project_path>

# 查看状态
python3 ~/Documents/Noesis/Praxis/orchestrator/paper_runner.py status  <project_path>

# 强制设置阶段（恢复/覆盖）
python3 ~/Documents/Noesis/Praxis/orchestrator/paper_state_machine.py init-phase <project_path> <phase>
```

状态持久化在 `<project>/Papers/paper-status.json`。Fork agent 将结果写入 `<project>/Papers/phase-outcomes/<phase>.json`，格式为 `{"outcome": "...", "notes": "..."}`。

## Three Agent Tiers

| Tier | 模型 | 角色 | 阶段 |
|------|------|------|------|
| `standard` | claude-sonnet-4-6 | AI Co-Author，执行性/模板化工作 | R7, P2, P4, P6 |
| `heavy` | claude-opus-4-6 | 发散性思考 / 独立批判审查 | R1, R2, R3, R4, R5, R6, R8, P1, P3, P5, P7 |
| `codex` | gpt-4.5-high | 可选外部 AI 审查，提供第三方视角 | R2, R4, R6, P3, P7（并行） |

Runner 根据 tier 为 fork agent 注入不同的 preamble：

- **Standard**：作为研究合作者，基于上下文忠实执行当前阶段的工作任务。
- **Heavy**：以严格独立评审人/综合决策者身份工作，上下文隔离，批判性、不妥协的评估。
- **Codex**：通过 Codex MCP 调用 GPT-4.5-high，完全独立的第三方外部审查者；non-blocking，MCP 不可用时自动跳过，不影响主流程路由。

## Pipeline Phase Map

**Module 1: Startup**

| Phase | Skill | Type | Tier |
|-------|-------|------|------|
| startup | `startup-skill` | interactive 🗣️ | standard |

Startup 完成后通过 `init-phase` 将状态设为 R1，由 `/praxis-research` 接管。

**Module 2: Research**

| Phase | Skill | Type | Tier | Codex |
|-------|-------|------|------|-------|
| R1 | `10-gap-discovery` | work | heavy | — |
| R2 | `1X-review` (gap) | review 🔒 | heavy | ✓ |
| R3 | `11-method-design` | work | heavy | — |
| R4 | `1X-review` (method) | review 🔒 | heavy | ✓ |
| R5 | `12-experiment-design` | work | heavy | — |
| R6 | `1X-review` (experiment) | review 🔒 | heavy | ✓ |
| R7 | `13-impl-planning` | work | standard | — |
| R8 | `14-retrospective` | work | heavy | — |

R2 review 出口：`pass`→R3 / `revise`→R1 / `abandon`→R8
R4 review 出口：`pass`→R5 / `revise`→R3 / `continue_R1`→R1 / `abandon`→R8
R6 review 出口：`pass`→R7 / `revise`→R5 / `continue_R3`→R3 / `abandon`→R8

**Module 3: Code**

| Phase | Skill | Type | Tier |
|-------|-------|------|------|
| coding | — | manual 🔧 | — |
| paper_writing | — | manual 🔧 | — |

coding 出口：`success`→paper_writing / `iterate_R3`→R3 / `iterate_R1`→R1 / `abandon`→complete

**Module 4: Paper**

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
├── CLAUDE.md                           ← 本文件
├── orchestrator/
│   ├── research_state_machine.py       ← 研究 pipeline 状态机（R1-R8）
│   ├── research_runner.py              ← 研究 pipeline runner
│   ├── paper_state_machine.py          ← 论文 pipeline 状态机（P1-P7）
│   └── paper_runner.py                 ← 论文 pipeline runner
├── skills/                             ← 非自动化模块的详细指令（由 .claude/skills/ 薄包装调用）
│   ├── startup-skill.md                ← /praxis-start 详细指令（含六维辩论）
│   ├── conclude-skill.md               ← /praxis-conclude 详细指令
│   ├── assimilate-skill.md             ← /praxis-assimilate 详细指令
│   ├── evolve-skill.md                 ← /praxis-evolve 详细指令
│   └── present-skill.md               ← /praxis-present 详细指令
├── prompts/                            ← 状态机 fork agent 指令（runner 自动加载）
│   ├── 10-gap-discovery-prompt.md      ← R1 Gap 发现
│   ├── 1X-review-prompt.md             ← R2/R4/R6 通用审查
│   ├── 11-method-design-prompt.md      ← R3 方法设计
│   ├── 12-experiment-design-prompt.md  ← R5 实验设计
│   ├── 13-impl-planning-prompt.md      ← R7 实验规划（纯规划）
│   ├── 14-retrospective-prompt.md      ← R8 研究回顾
│   ├── 30-paper-outline-prompt.md      ← P1 论文大纲
│   ├── 31-paper-sections-prompt.md     ← P2 章节写作
│   ├── 32-paper-critique-prompt.md     ← P3 多角色审查
│   ├── 33-paper-integrate-prompt.md    ← P4 编辑整合
│   ├── 34-paper-review-prompt.md       ← P5 终审
│   ├── 35-paper-latex-prompt.md        ← P6 LaTeX 编译
│   ├── 36-project-review-prompt.md     ← P7 项目级审查
│   ├── codex-reviewer-prompt.md        ← 可复用 Codex 外部审查者
│   ├── codex-writer-prompt.md          ← Codex 写作辅助
│   ├── X-reflect-pipeline-prompt.md    ← 跨阶段流程反思（每阶段自动注入）
│   └── review-configs/                 ← 审查配置（YAML，gap/method/experiment）
├── subagents/                          ← SubAgent prompt 模板
│   ├── — Startup 六维辩论（/praxis-start Step 4）—
│   ├── innovator-subagent.md           ← 创新者
│   ├── pragmatist-subagent.md          ← 务实者
│   ├── theorist-subagent.md            ← 理论家
│   ├── contrarian-subagent.md          ← 反对者
│   ├── interdisciplinary-subagent.md   ← 跨学科者
│   ├── empiricist-subagent.md          ← 实验主义者
│   ├── synthesizer-subagent.md         ← 综合者（汇总六维辩论结果）
│   ├── — 其他专用子 Agent —
│   ├── comparativist-subagent.md       ← 对比分析者
│   ├── methodologist-subagent.md       ← 方法论者
│   ├── skeptic-subagent.md             ← 怀疑论者
│   ├── work-synthesizer-subagent.md    ← 工作综合者
│   ├── paper-critic-subagent.md        ← 论文审查（5 角色）
│   └── exit-assessment-subagent.md     ← 退出评估
└── templates/
    ├── project-claude-md.md            ← 新项目 CLAUDE.md 模板
    ├── project-startup.md              ← Startup 输出模板
    ├── gap-analysis.md                 ← R1 输出模板
    ├── method-design.md                ← R3 输出模板
    ├── experiment-design.md            ← R5 输出模板
    ├── contribution.md                 ← 跨阶段贡献跟踪
    ├── iteration-log.md                ← 迭代历史（conclude 追加）
    ├── retrospective.md                ← R8 输出模板
    ├── proposal.md                     ← 提案模板
    ├── experiment-todo.md              ← 实验待办（R7 产出）
    └── pipeline-evolution-log.md       ← 流水线演进日志（X-reflect 追加）
```

## Cross-Project Learning

项目 R8 Retrospective 完成、论文写作结束后，运行 `/praxis-evolve` 产出两类成果：

1. **跨项目 Lessons** → `~/.noesis/lessons/<skill_name>.md`：含类别标签 `[SYSTEM/EXPERIMENT/WRITING/...]`、频率标签 `[RECURRING/NEW]`、有效性标签 `[✓verified/✗ineffective/?unverified]`。Runner 在后续项目的相同阶段自动注入有效 lessons；`[✗ineffective]` 自动过滤；`[RECURRING]` 排在最前。

2. **框架进化** → 基于 `pipeline-evolution-log.md` 中各阶段的 X-reflect 条目，更新 `Praxis/prompts/`、`Praxis/skills/`、`Praxis/templates/` 文档，并 push 到 Noesis GitHub。

## Key Behaviors

**Pipeline 流程**
- **五大模块**：Startup (`/praxis-start`) → Research (`/praxis-research`, R1→R8) → Code (人工) → Paper (`/praxis-paper`, P1→P7) → Evolution (`/praxis-evolve`)
- **R8 Retrospective 时机**：在 R7 impl-planning 完成后、coding 开始前执行，不是在论文完成后
- **coding 热重启**：`/praxis-conclude` 写入 `iteration-log.md` 并通过 `init-phase` 重置状态（L2→R3 / L3→R3 / L4→R1），`/praxis-research` 读取迭代日志避免重复已排除方向

**Startup 六维辩论**
- `/praxis-start` 的 Step 4 并行召唤 6 个辩论 Agent（创新者、务实者、理论家、反对者、跨学科者、实验主义者），再由综合者汇总判定（方向确认/强化/修正/HIGH RISK）
- 辩论结果完整纳入 `project-startup.md`，进入 R1 时带着已知风险列表
- Step 7 完成 Git 初始化 + GitHub repo 创建，设状态为 R1

**迭代模式（Runner 自动注入上下文）**
- **Revise 模式**：review 文件存在（如 `gap-review.md`）→ 工作阶段（R1/R3/R5）提示"基于审查意见修改，不从零开始"
- **Pivot 模式**：`iteration-log.md` 存在且阶段已迭代 → 提示"热重启第 N 轮，严禁重复已排除方向"
- **迭代守卫**：研究 pipeline ≥ 3 次迭代发警告；论文 pipeline ≥ 5 次迭代发警告

**Paper 独立状态机**
- `paper_state_machine.py` + `paper_runner.py`，状态在 `Papers/paper-status.json`，与主 pipeline 完全解耦
- P5 修订循环：评分 < 7.0 → P4，最多 2 轮，超限强制通过
- P7 项目级审查：Critic + Supervisor + 可选 Codex 外部 AI 多视角审查

**架构原则**
- **三层架构**：Orchestrator (runner.py) 决定 WHAT/WHEN + 构建 fork_prompt；Prompts (prompts/*-prompt.md) 是纯 agent 指令；Slash commands (.claude/skills/) 是薄封装
- **`skills_parallel` 行动类型**：PHASES 含 `codex_agent` 字段时，runner 返回 `skills_parallel`，同时启动 main + codex Agent；main 写 `phase-outcomes/`（决定路由），codex 写 `codex-reviews/`（仅参考）
- **单一事实源**：主 pipeline `pipeline-status.json`，论文模块 `Papers/paper-status.json`
- **X-reflect 自动注入**：每个非 manual 阶段完成后，runner 自动在 fork_prompt 末尾注入 `X-reflect-pipeline-prompt.md`，agent 将反思追加到 `pipeline-evolution-log.md`

## Adding or Modifying a Phase

1. 编辑 `research_state_machine.py` 中的 `PHASES` 字典 — 添加 phase key、skill name、outcome_type、tier、transition map
2. 创建或更新 `prompts/<skill_name>-prompt.md`
3. 如果是审查阶段，添加 `prompts/review-configs/<type>-review.yaml`
4. 如果需要人工确认，将 phase key 加入 `research_state_machine.py` 的 `HUMAN_CHECKPOINT_PHASES`
5. 如果需要 Codex 并行审查，在 PHASES 条目中添加 `"codex_agent": "codex-reviewer"`
