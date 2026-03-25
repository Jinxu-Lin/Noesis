# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

**Noesis** 是一个 AI Agent 自动科研系统，面向 AI/ML/DL 方向。系统名取自希腊语 νόησις（认知/洞察），包含两个**独立**子系统：

**Logos**（`Logos/`）— 持续知识积累系统，循环运行：
- 论文发现（arXiv/Semantic Scholar 多策略搜索，含争议/负面结果搜索）
- 深度阅读、知识资产提取（Methods Bank、Gaps & Assumptions、Experimental Patterns、Cross-Paper Connections、Reusable Resources）
- 命令：`/logos-discover`、`/logos-read`（强制使用 Sonnet 模型）
- 知识库产出位于：`~/Research/Episteme`

**Praxis**（`Praxis/`）— 研究执行流程，**三个独立模块**（各有独立状态机）+ 辅助命令：
- **Init Module**：项目初始化 + 探针实验（init→start→probe_design→review→probe_impl→complete）
- **Research Module**：核心研究循环（formalize→formalize_review→design→design_review→blueprint→implement→retrospective→complete）
- **Paper Module**：论文写作（P1→P7），独立状态机，可在实验完成前启动

两个子系统通过**知识库（Episteme）**连接：Logos 填充知识库，Praxis 在研究阶段消费（formalize ← Gaps & Assumptions + Cross-Paper Connections；design ← Methods Bank + Experimental Patterns）。

This repo itself is not a research project — it is the **central methodology library** referenced by individual research project repos.

## Environment

Noesis 运行在本地 macOS 上，存放于 `~/Research/`，通过 GitHub 在多台 Mac 间同步：

| 路径 | 说明 | 同步方式 |
|------|------|---------|
| `~/Research/Noesis` | Noesis 系统根目录 | GitHub |
| `~/Research/Episteme` | Logos 知识库产出 | GitHub |
| `~/Research/<项目名>` | 各研究项目 | GitHub（每个项目独立仓库） |
| `~/.noesis/lessons/` | 跨项目经验教训 | 本地（各 Mac 独立积累） |

**多机协作**：两台 Mac（Mac Mini / MacBook）通过 `git push` / `git pull` 同步，用户名不同（`jlin8272` / `linjinxu`），因此所有配置使用 `~` 而非硬编码绝对路径。

**远程服务器**：implement 后的实验通过 SSH MCP 在远程 GPU 服务器上执行，代码通过 git 同步到服务器，结果通过 git 或 SSH MCP 回传本地。

## Skills (Slash Commands)

所有自定义命令通过 `.claude/skills/` 注册（项目级），无需额外配置。

### Logos skills（model: sonnet）
- `/logos-discover [kb_path]` — 论文发现：多策略搜索、Quick Scan 评分（4维度）、更新阅读队列
- `/logos-read [参数]` — 深度阅读：提取 5 类知识资产、更新知识库
- `kb_path` 默认为 `~/Research/Episteme`，可省略
- `/logos-read` 参数：无参（读队列第1篇）/ 数字（读N篇）/ arXiv ID / 标题关键词

### Praxis skills — Init Module
- `/praxis-init-auto <project_path>` — 自动运行 Init Module 完整流程
- `/praxis-init <project_path>` — init 阶段（项目配置初始化）
- `/praxis-start <project_path>` — start 阶段（交互式项目分析）
- `/praxis-probe-design <project_path>` — probe_design 阶段（探针实验设计）
- `/praxis-review <project_path>` — review 阶段（init 审查，4 debaters）
- `/praxis-probe-impl <project_path>` — probe_impl 阶段（探针实验执行）

### Praxis skills — Research Module
- `/praxis-r-auto <project_path>` — 自动运行 Research Module 完整流程
- `/praxis-r-formalize <project_path>` — formalize 阶段（问题锐化）
- `/praxis-r-formalize-review <project_path>` — formalize_review 阶段（战略审查，4 debaters）
- `/praxis-r-design <project_path>` — design 阶段（方法+实验联合设计）
- `/praxis-r-design-review <project_path>` — design_review 阶段（技术审查，6 debaters）
- `/praxis-r-blueprint <project_path>` — blueprint 阶段（实现蓝图）
- `/praxis-r-implement <project_path>` — implement 阶段（代码实现）
- `/praxis-r-retrospective <project_path>` — retrospective 阶段（知识回收）

### Praxis skills — Paper Module
- `/praxis-paper <project_path>` — 自动化论文写作（P1→P7）
- `/praxis-paper-fill <project_path>` — 填充论文中的 `{{PENDING:...}}` 占位符

### Praxis skills — Auxiliary
- `/praxis-conclude <project_path>` — 实验失败诊断（implement 阶段）
- `/praxis-present <project_path>` — 生成 presentation.md（热启动支持，保留人工编辑）
- `/praxis-assimilate <project_path>` — 同化现有项目（重建文档 + 审查）
- `/praxis-evolve <project_path>` — 提取跨项目 lessons + 更新 Noesis 框架文档
- `/praxis-optimize` — 深度 prompt/skill 优化

## Orchestrator CLI (Praxis)

三个独立模块各有 runner + state machine。始终通过 runner 操作（除 `init-phase` 外不直接调用 state machine）。

### Init Module

```bash
python3 ~/Research/Noesis/Praxis/orchestrator/init_runner.py next    <project_path>
python3 ~/Research/Noesis/Praxis/orchestrator/init_runner.py advance <project_path>
python3 ~/Research/Noesis/Praxis/orchestrator/init_runner.py status  <project_path>
python3 ~/Research/Noesis/Praxis/orchestrator/init_state_machine.py init-phase <project_path> <phase>
```

状态持久化在 `<project>/Docs/init-module-status.json`。

### Research Module

```bash
python3 ~/Research/Noesis/Praxis/orchestrator/research_runner.py next    <project_path>
python3 ~/Research/Noesis/Praxis/orchestrator/research_runner.py advance <project_path>
# implement 阶段需指定 --outcome：
python3 ~/Research/Noesis/Praxis/orchestrator/research_runner.py advance <project_path> --outcome success
python3 ~/Research/Noesis/Praxis/orchestrator/research_runner.py advance <project_path> --outcome iterate_method
python3 ~/Research/Noesis/Praxis/orchestrator/research_runner.py advance <project_path> --outcome iterate_direction
python3 ~/Research/Noesis/Praxis/orchestrator/research_runner.py advance <project_path> --outcome abandon
python3 ~/Research/Noesis/Praxis/orchestrator/research_runner.py status  <project_path>
python3 ~/Research/Noesis/Praxis/orchestrator/research_state_machine.py init-phase <project_path> <phase>
```

状态持久化在 `<project>/Docs/research-module-status.json`（含 `entry_context` + `history`）。

### Paper Module

```bash
python3 ~/Research/Noesis/Praxis/orchestrator/paper_runner.py next    <project_path>
python3 ~/Research/Noesis/Praxis/orchestrator/paper_runner.py advance <project_path>
python3 ~/Research/Noesis/Praxis/orchestrator/paper_runner.py status  <project_path>
python3 ~/Research/Noesis/Praxis/orchestrator/paper_state_machine.py init-phase <project_path> <phase>
```

论文状态持久化在 `<project>/Papers/paper-status.json`。Paper outcomes 写入 `<project>/Papers/phase-outcomes/<phase>.json`。

### 通用约定
- `pipeline-status.json` 仅记录 `active_module`，各模块各有独立状态文件
- Fork agents 将结果写入 `<project>/phase-outcomes/<phase>.json`，格式：`{"outcome": "...", "notes": "..."}`
- 所有模型使用 opus

## Pipeline Phase Map (Praxis)

### Init Module（`/praxis-init-auto` 自动运行）

| Phase | Prompt | Type | Debaters |
|-------|--------|------|----------|
| init | init-setup-prompt | work | — |
| start | start-analysis-prompt | work | — |
| probe_design | probe-design-prompt | work | — |
| review | init-review-prompt | review | 4 debaters (contrarian, comparativist, pragmatist, interdisciplinary) |
| probe_impl | probe-impl-prompt | work | — |

流程：init → start → probe_design → review → probe_impl → complete

产出：`project.md`、`Codes/probe/`、`Codes/_Results/probe_result.md`、`Reviews/init/round-N/`

### Research Module（`/praxis-r-auto` 自动运行）

| Phase | Prompt | Type | Debaters | Codex |
|-------|--------|------|----------|-------|
| formalize | formalize-prompt | work | — | — |
| formalize_review | formalize-review-prompt | review | 4 (contrarian, comparativist, pragmatist, interdisciplinary) | ✓ |
| design | design-prompt | work | — | — |
| design_review | design-review-prompt | review | 6 (theorist, methodologist, empiricist, skeptic, pragmatist, contrarian) | ✓ |
| blueprint | blueprint-prompt | work | — | — |
| implement | implement-prompt | work/manual | — | — |
| retrospective | retrospective-prompt | work | — | — |

**正常流程**：formalize → formalize_review(pass) → design → design_review(pass) → blueprint → implement(success) → retrospective → complete

**formalize_review 出口**：pass→design / revise→formalize / abandon→retrospective
**design_review 出口**：pass→blueprint / revise→design / fundamental→formalize / abandon→retrospective
**implement 出口**：success→retrospective / iterate_method→design / iterate_direction→formalize / abandon→retrospective

产出：`research/problem-statement.md`、`research/method-design.md`、`research/experiment-design.md`、`Codes/_Results/experiment_result.md`、`Reviews/research-formalize/round-N/`、`Reviews/research-design/round-N/`

### Paper Module（`/praxis-paper` 自动运行）

| Phase | Prompt | Type | Codex |
|-------|--------|------|-------|
| P1 | 30-paper-outline-prompt | work | — |
| P2 | 31-paper-sections-prompt | work | — |
| P3 | 32-paper-critique-prompt | review | ✓ |
| P4 | 33-paper-integrate-prompt | work | — |
| P5 | 34-paper-review-prompt | paper_review | — |
| P6 | 35-paper-latex-prompt | work | — |
| P7 | 36-project-review-prompt | review | ✓ |

P5: 评分 < 7.0 → 回到 P4（最多 2 轮，超限强制通过）。
支持 `{{PENDING:...}}` 占位符，可在实验完成前启动写作，后续 `/praxis-paper-fill` 填充。

### 项目目录结构

- `research/`：problem-statement.md, method-design.md, experiment-design.md, contribution.md, retrospective.md
- `Reviews/`：init/round-N/, research-formalize/round-N/, research-design/round-N/（审查辩论记录）
- `codex-reviews/`：外部 AI 审查（仅参考）
- `Codes/_Results/`：probe_result.md, experiment_result.md（实验结果）
- `phase-outcomes/`：阶段结果 JSON + 辩论中间文件

## Entry Context Modes (Research Module)

Runner 根据 mode 自动注入对应的审查文档、iteration-log、result.md 等上下文。4 种模式：

| Mode | 触发条件 | 目标阶段 |
|------|---------|---------|
| `fr_revise` | formalize_review → revise | formalize |
| `dr_revise` | design_review → revise | design |
| `direction_pivot` | design_review fundamental / implement iterate_direction / design escalate | formalize |
| `method_iterate` | implement iterate_method | design |

## Key Architecture Decisions

**两个独立子系统** — Logos 和 Praxis 各有独立的 skills 和 templates，无运行时依赖。唯一连接：Praxis 在 formalize/design 消费 Logos 产出的 Episteme 知识库（formalize ← Gaps & Assumptions + Cross-Paper Connections；design ← Methods Bank + Experimental Patterns）。

**三个独立状态机** — Init Module（`init_state_machine.py` + `init_runner.py`，状态 `Docs/init-module-status.json`）、Research Module（`research_state_machine.py` + `research_runner.py`，状态 `Docs/research-module-status.json`）、Paper Module（`paper_state_machine.py` + `paper_runner.py`，状态 `Papers/paper-status.json`）。完全解耦。`pipeline-status.json` 仅记录 `active_module`。

**三层架构（Praxis）** — Orchestrator（runner.py）决定 WHAT/WHEN + 构建 fork_prompt；Prompts（`Praxis/prompts/*-prompt.md`）是纯 agent 指令；Slash commands（`.claude/skills/praxis-*/SKILL.md`）是薄封装运行器；State machines 是纯转换 + I/O，无 prompt 逻辑。

**按决策性质切分阶段** — formalize = 战略决策（Gap + 攻击角度 + 探针信号整合）；design = 技术决策（方法 + 实验联合设计，组件与 ablation 同步）。两次审查分别对应：formalize_review = 战略审查（值不值得做）；design_review = 技术审查（做得对不对）。

**探针实验前置（Init Module）** — 在进入 Research Module 之前，通过 Init Module 的 probe_design + probe_impl 用最小成本验证核心直觉，产出 `Codes/_Results/probe_result.md`。确保方向判断基于经验信号而非纯理论推演。

**分层回退** — 失败根因在哪个层次，就回退到哪个阶段。implement 失败时：方法层问题（iterate_method）→ design；方向层问题（iterate_direction）→ formalize。迭代守卫：design 回退 ≥ 2 次强制升级到 formalize 回退；formalize 回退 ≥ 3 次触发 abandon 评估。

**文档版本控制** — 单文件 + 元数据版本号 + iteration-log。每个研究文档头部使用 YAML frontmatter（version, iteration_major, iteration_minor, entry_mode）。版本号 `<major>.<minor>`：Major = implement 回退导致重写；Minor = Review 后 Revise。`iteration-log.md` 倒序排列，记录排除方向和失败洞察。

**单一事实源** — Init 模块：`Docs/init-module-status.json`；Research 模块：`Docs/research-module-status.json`（含 entry_context + history）；Paper 模块：`Papers/paper-status.json`。无自动检测或回退推断。

**跨项目学习** — `/praxis-evolve` 产出两类成果：lessons → `~/.noesis/lessons/<skill_name>.md`，Runner 在相同阶段自动注入（`[✗ineffective]` 自动过滤，`[RECURRING]` 排在最前）；框架进化 → 基于 `pipeline-evolution-log.md` 直接修改 Noesis 框架文档并 push GitHub。

**`skills_parallel` 行动类型** — PHASES 含 `codex_agent` 字段时，runner 返回 `action_type: "skills_parallel"`，SKILL.md 同时启动 main + codex Agent；main 写 `phase-outcomes/`（决定路由），codex 写 `codex-reviews/`（仅参考，不影响路由）。

**X-reflect 自动注入** — 每个非 manual 阶段完成后，runner 在 fork_prompt 末尾自动注入 `X-reflect-pipeline-prompt.md`，agent 将流程反思追加到 `pipeline-evolution-log.md`（供 `/praxis-evolve` 汇总处理）。

## File Layout

```
Noesis/
├── Logos/                           ← 知识积累子系统（独立）
│   ├── CLAUDE.md                    ← Logos 子系统指导文档
│   ├── skills/
│   │   ├── paper-discovery-skill.md ← 论文发现：5 种搜索策略 + Quick Scan 评分
│   │   └── paper-reading-skill.md   ← 深度阅读：5 类知识资产提取
│   └── templates/
│       ├── research-directions.md   ← 研究方向配置（关键词、种子论文、venue）
│       ├── reading-queue.md         ← 阅读队列（discover 写入，read 消费）
│       ├── kb-index.md              ← 知识库总索引
│       └── paper-reading-note.md    ← 论文笔记模板
│
├── Praxis/                          ← 研究执行子系统（独立）
│   ├── CLAUDE.md                    ← Praxis 子系统指导文档
│   ├── orchestrator/
│   │   ├── init_state_machine.py    ← Init Module 状态机（init→...→complete）
│   │   ├── init_runner.py           ← Init Module runner
│   │   ├── research_state_machine.py ← Research Module 状态机（formalize→...→complete）
│   │   ├── research_runner.py        ← Research Module runner
│   │   ├── paper_state_machine.py    ← Paper Module 状态机（P1→P7）
│   │   └── paper_runner.py           ← Paper Module runner
│   ├── prompts/                     ← 状态机 fork agent 指令（runner 自动加载）
│   │   ├── init-setup-prompt.md          ← init 项目配置
│   │   ├── start-analysis-prompt.md      ← start 项目分析
│   │   ├── probe-design-prompt.md        ← probe_design 探针设计
│   │   ├── init-review-prompt.md         ← review Init 审查
│   │   ├── probe-impl-prompt.md          ← probe_impl 探针执行
│   │   ├── formalize-prompt.md           ← formalize 问题锐化
│   │   ├── formalize-review-prompt.md    ← formalize_review 战略审查
│   │   ├── design-prompt.md              ← design 联合设计
│   │   ├── design-review-prompt.md       ← design_review 技术审查
│   │   ├── blueprint-prompt.md           ← blueprint 实现蓝图
│   │   ├── implement-prompt.md           ← implement 代码实现
│   │   ├── retrospective-prompt.md       ← retrospective 知识回收
│   │   ├── 30-36 paper prompts           ← Paper Module (P1-P7)
│   │   ├── paper-fill-prompt.md          ← PENDING 占位符填充
│   │   ├── codex-reviewer-prompt.md      ← Codex 外部审查者
│   │   ├── codex-writer-prompt.md        ← Codex 外部写作者
│   │   ├── optimize-prompt.md            ← prompt/skill 优化
│   │   ├── X-reflect-pipeline-prompt.md  ← 阶段反思（每阶段自动注入）
│   │   └── review-configs/               ← 审查配置 YAML
│   │       ├── init-review.yaml          ← Init review 审查维度
│   │       ├── formalize-review.yaml     ← formalize_review 审查维度
│   │       └── design-review.yaml        ← design_review 审查维度
│   ├── skills/                      ← 辅助命令详细指令
│   │   ├── conclude-skill.md        ← /praxis-conclude（失败诊断）
│   │   ├── assimilate-skill.md      ← /praxis-assimilate
│   │   ├── evolve-skill.md          ← /praxis-evolve
│   │   └── present-skill.md         ← /praxis-present
│   ├── subagents/                   ← SubAgent prompt 模板（13 个辩论角色）
│   ├── templates/                   ← 项目文档模板
│   │   ├── project.md               ← 项目主文档模板
│   │   ├── project-claude-md.md     ← 项目 CLAUDE.md 模板
│   │   └── ...                      ← iteration-log, result, retrospective 等
│   └── docs/
│       └── init-module-iteration-plan.md
│
├── .claude/skills/                  ← 项目级 skills (slash commands)
│   ├── logos-discover/              ← /logos-discover (model: sonnet)
│   ├── logos-read/                  ← /logos-read (model: sonnet)
│   ├── praxis-init-auto/            ← /praxis-init-auto (Init 全流程)
│   ├── praxis-init/                 ← /praxis-init
│   ├── praxis-start/                ← /praxis-start
│   ├── praxis-probe-design/         ← /praxis-probe-design
│   ├── praxis-review/               ← /praxis-review
│   ├── praxis-probe-impl/           ← /praxis-probe-impl
│   ├── praxis-r-auto/               ← /praxis-r-auto (Research 全流程)
│   ├── praxis-r-formalize/          ← /praxis-r-formalize
│   ├── praxis-r-formalize-review/   ← /praxis-r-formalize-review
│   ├── praxis-r-design/             ← /praxis-r-design
│   ├── praxis-r-design-review/      ← /praxis-r-design-review
│   ├── praxis-r-blueprint/          ← /praxis-r-blueprint
│   ├── praxis-r-implement/          ← /praxis-r-implement
│   ├── praxis-r-retrospective/      ← /praxis-r-retrospective
│   ├── praxis-paper/                ← /praxis-paper (P1→P7)
│   ├── praxis-paper-fill/           ← /praxis-paper-fill
│   ├── praxis-conclude/             ← /praxis-conclude
│   ├── praxis-present/              ← /praxis-present
│   ├── praxis-assimilate/           ← /praxis-assimilate
│   ├── praxis-evolve/               ← /praxis-evolve
│   └── praxis-optimize/             ← /praxis-optimize
│
├── introduction.md                  ← 系统说明书（人类阅读）
├── CLAUDE.md                        ← 本文件
└── README.md
```

## Adding or Modifying a Phase (Praxis)

1. 确定目标模块（Init / Research / Paper），编辑对应 `Praxis/orchestrator/*_state_machine.py` 的 `PHASES` 字典 — 添加 phase key、skill name、outcome_type、tier、transitions、debate_agents（如适用）
2. 创建或更新 `Praxis/prompts/<skill_name>-prompt.md`
3. 如果是审查阶段，添加 `Praxis/prompts/review-configs/<type>-review.yaml` 并配置 `debate_agents` 列表
4. 如果是手动阶段，设置 `skill: None`、`outcome_type: "manual"`，确保 `advance` 命令支持 `--outcome` 标志
5. 如果需要 Codex 并行审查，在 PHASES 条目中添加 `"codex_agent": "codex-reviewer"`

## Project CLAUDE.md Template

启动新项目时，Init Module 自动从 `Praxis/templates/project-claude-md.md` 创建项目 `CLAUDE.md`，包含 `noesis_path` 字段（指向本 repo），供各模块 runner 定位状态机。

**CLAUDE.md 设计原则**：行动指南与约束纲领，非项目介绍文书。放目录架构让 Claude 知道去哪找信息，不放冗余文件内容。

**项目代码约束**：
- 所有代码存放在 `./Codes/`
- **深浅解耦**：`Codes/core/`（深内核，可复用核心）+ `Codes/experiments/<exp>/`（浅包装，实验特定）
- **数据独立**：外部数据（数据集/backbone）→ `~/Resources/Datasets/` 或 `~/Resources/Models/`；生成数据（权重/梯度/样本）→ `./Codes/_Data/`
- **版本同步**：每次修改完文件/代码后，commit + push 同步至 GitHub
