# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

**Noesis** 是一个 AI Agent 自动科研系统，面向 AI/ML/DL 方向。系统名取自希腊语 νόησις（认知/洞察），包含两个**独立**子系统：

**Logos**（`Logos/`）— 持续知识积累系统，独立运行：
- 论文发现（arXiv/Semantic Scholar 多策略搜索）
- 深度阅读与知识库沉淀（Methods Bank、Gaps、Experimental Patterns）
- 命令：`/paper-reading-discover`、`/paper-reading-read`（强制使用 Sonnet 模型）
- 知识库产出位于：`~/Documents/LogosBase`

**Praxis**（`Praxis/`）— 自动化研究执行流程（P1→P11），独立运行：
- 结构化 12 阶段研究流程（Startup → Gap → Method → Experiment → Impl → Paper → Retrospective）
- Python 状态机 + 分叉 Agent 自动化执行
- 命令：`/researchflow-run`、`/researchflow-status`、`/researchflow-goto`、`/researchflow-evolve`

两个子系统通过**知识库（LogosBase/）**连接：Logos 填充知识库，Praxis 在 P2/P4/P6 阶段消费知识库内容。

**sibyl-system/**（临时）— 一个较成熟的外部自动科研系统，作为设计参考。借鉴完成后将从仓库中移除。

This repo itself is not a research project — it is the **central methodology library** referenced by individual research project repos.

## Environment

Noesis 运行在本地 macOS 上，存放于 `~/Documents/`，通过 GitHub 在多台 Mac 间同步：

| 路径 | 说明 | 同步方式 |
|------|------|---------|
| `~/Documents/Noesis` | Noesis 系统根目录 | GitHub |
| `~/Documents/LogosBase` | Logos 知识库产出 | GitHub |
| `~/Documents/<项目名>` | 各研究项目 | GitHub（每个项目独立仓库） |

**多机协作**：两台 Mac（Mac Mini / MacBook）通过 `git push` / `git pull` 同步，用户名不同（`jlin8272` / `linjinxu`），因此所有配置使用 `~` 而非硬编码绝对路径。

**远程服务器**：P8 阶段的实验通过 SSH MCP 在远程 GPU 服务器上执行，代码通过 git 同步到服务器，结果通过 git 或 SSH MCP 回传本地。

## Skills (Slash Commands)

所有自定义命令通过 `.claude/skills/` 注册（项目级），无需额外配置。

### Logos skills（model: sonnet）
- `/paper-reading-discover [kb_path]` — search papers, score relevance, update reading queue
- `/paper-reading-read [kb_path]` — deep-read papers, extract knowledge assets, update kb-index
- `kb_path` 默认为 LogosBase 路径，可省略

### Praxis skills
- `/researchflow-run <project_path>` — run the full pipeline loop (automated)
- `/researchflow-status <project_path>` — view current pipeline state
- `/researchflow-goto <project_path> <phase>` — force-set state to a specific phase
- `/researchflow-evolve <project_path>` — extract lessons from a completed project into `~/.researchflow/lessons/`

## Orchestrator CLI (Praxis)

The orchestrator is the backbone of Praxis automated pipeline execution. Always use `runner.py`, not `state_machine.py` directly (except for `init-phase`).

```bash
# Get next action (returns JSON with fork_prompt)
python3 Praxis/orchestrator/runner.py next    <project_path>

# Advance state after fork agent writes phase-outcomes/<phase>.json
python3 Praxis/orchestrator/runner.py advance <project_path>

# View current state
python3 Praxis/orchestrator/runner.py status  <project_path>

# Force-set phase (override/recovery)
python3 Praxis/orchestrator/state_machine.py init-phase <project_path> <phase>
```

State is persisted in `<project>/pipeline-status.json`. Fork agents write outcomes to `<project>/phase-outcomes/<phase>.json` as `{"outcome": "...", "notes": "..."}`.

## Pipeline Phase Map (Praxis)

| Phase | Skill | Type | Tier |
|-------|-------|------|------|
| P1 | `project-startup` | work | standard |
| P2 | `gap-discovery` | work | standard |
| P3 | `review gap` | review 🔒 | heavy |
| P4 | `method-design` | work | standard |
| P5 | `review method` | review 🔒 | heavy |
| P6 | `experiment-design` | work | standard |
| P7 | `review experiment` | review 🔒 | heavy |
| P8a | `impl-setup` | work ⏸ | standard |
| P8a_validate | `impl-validate` | work ⏸ | standard |
| P8b | `impl-full` | work ⏸ | standard |
| P9 | `paper-writing` | work | standard |
| P11 | `retrospective` | work | heavy |

⏸ = human checkpoint required before proceeding. 🔒 = independent SubAgent review (context-isolated).

## Key Architecture Decisions

**Two independent subsystems** — Logos and Praxis each have their own skills and templates. They share no runtime dependencies. The only connection is that Praxis reads from the knowledge base that Logos produces.

**State machine is pure** — `state_machine.py` only handles transitions and status I/O. `runner.py` builds the full `fork_prompt` by composing tier preamble + skill file content + cross-project lessons overlay.

**Two agent tiers (Praxis):**
- `standard` — AI Co-Author executing a work phase
- `heavy` — strict independent critic (P3, P5, P7, P11); injected with a preamble demanding rigorous, unforgiving evaluation

**Review verdict detection** uses regex on the output document: `整体判定[：:] Pass/Revise/Block`. The state machine reads this to determine transitions.

**Cross-project learning** — After P11, `/researchflow-evolve` extracts lessons to `~/.researchflow/lessons/<skill_name>.md`. Runner auto-injects these into future fork prompts for the same skill.

**Auto-detection fallback** — If `pipeline-status.json` is missing, `state_machine.py` infers the current phase by scanning for output documents (e.g., presence of `gap-analysis.md` → P3).

## File Layout

```
Noesis/
├── Logos/                           ← 知识积累子系统（独立）
│   ├── OVERVIEW.md                  ← 子系统说明与快速开始
│   ├── skills/
│   │   ├── paper-discovery-skill.md ← 论文发现与筛选
│   │   └── paper-reading-skill.md   ← 深度阅读与知识沉淀
│   ├── templates/
│   │   ├── research-directions.md   ← 研究方向配置
│   │   ├── reading-queue.md         ← 阅读队列
│   │   ├── kb-index.md              ← 知识库总索引
│   │   └── paper-reading-note.md    ← 论文笔记模板
│   └── (skills & templates only)
│
├── Praxis/                          ← 研究执行子系统（独立）
│   ├── orchestrator/
│   │   ├── state_machine.py         ← Pure state machine: transitions, status I/O
│   │   └── runner.py                ← Builds fork_prompt; CLI for next/advance/status
│   ├── skills/
│   │   ├── *-skill.md               ← P1-P11 skill files
│   │   ├── reflect-pipeline-skill.md ← Post-phase reflection
│   │   └── review-configs/          ← YAML configs for P3/P5/P7
│   ├── subagents/                   ← SubAgent prompt templates
│   └── templates/                   ← Project document templates
│
├── .claude/skills/                   ← 项目级 skills (slash commands)
│   ├── paper-reading-discover/      ← /paper-reading-discover (model: sonnet)
│   ├── paper-reading-read/          ← /paper-reading-read (model: sonnet)
│   ├── researchflow-run/            ← /researchflow-run
│   ├── researchflow-status/         ← /researchflow-status
│   ├── researchflow-goto/           ← /researchflow-goto
│   └── researchflow-evolve/         ← /researchflow-evolve
│
├── pipeline.md                      ← 方法论文档（人类阅读）
├── sibyl-system/                    ← 外部参考系统（临时，借鉴后移除）
├── CLAUDE.md                        ← 本文件
└── README.md
```

## Adding or Modifying a Phase (Praxis)

1. Edit `PHASES` dict in `Praxis/orchestrator/state_machine.py` — add the phase key, skill name, outcome_type, tier, and transition map.
2. Create or update the corresponding `Praxis/skills/<skill_name>-skill.md`.
3. If it's a review phase, add `Praxis/skills/review-configs/<type>-review.yaml`.
4. If it requires human confirmation, add the phase key to `HUMAN_CHECKPOINT_PHASES` in `state_machine.py`.

## Project CLAUDE.md Template

When starting a new research project, copy `Praxis/templates/project-claude-md.md` as the project's `CLAUDE.md`. It must include a `noesis_path` field pointing to this repo so `/researchflow-run` can locate `runner.py`.
