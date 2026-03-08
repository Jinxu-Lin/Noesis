# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

ResearchFlow 包含两个独立子系统：

**PaperReading**（`paper-reading/`）— 持续知识积累系统，独立于研究流程运行：
- 论文发现（arXiv/Semantic Scholar 多策略搜索）
- 深度阅读与知识库沉淀（Methods Bank、Gaps、Experimental Patterns）
- Plugin 命令：`/paper-reading:discover`、`/paper-reading:read`

**ResearchFlow**（主目录）— 自动化研究执行流程（P1→P11）：
- 结构化 12 阶段研究流程（Startup → Gap → Method → Experiment → Impl → Paper → Retrospective）
- Python 状态机 + 分叉 Agent 自动化执行
- Plugin 命令：`/researchflow:run`、`/researchflow:status`、`/researchflow:goto`、`/researchflow:evolve`

两个子系统通过**知识库（kb/）**连接：PaperReading 填充知识库，ResearchFlow 在 P2/P4/P6 阶段消费知识库内容。

This repo itself is not a research project — it is the **central methodology library** referenced by individual research project repos.

## Plugin Setup

To enable `/researchflow:*` commands in any project:

```json
// Add to ~/.claude/settings.json
{ "pluginDirs": ["/home/jinxulin/ResearchFlow/plugin"] }
```

ResearchFlow pipeline commands:
- `/researchflow:run <project_path>` — run the full pipeline loop (automated)
- `/researchflow:status <project_path>` — view current pipeline state
- `/researchflow:goto <project_path> <phase>` — force-set state to a specific phase
- `/researchflow:evolve <project_path>` — extract lessons from a completed project into `~/.researchflow/lessons/`

PaperReading commands:
- `/paper-reading:discover <kb_path>` — search papers, score relevance, update reading queue
- `/paper-reading:read <kb_path>` — deep-read papers, extract knowledge assets, update kb-index

## Orchestrator CLI

The orchestrator is the backbone of automated pipeline execution. Always use `runner.py`, not `state_machine.py` directly (except for `init-phase`).

```bash
# Get next action (returns JSON with fork_prompt)
python3 orchestrator/runner.py next    <project_path>

# Advance state after fork agent writes phase-outcomes/<phase>.json
python3 orchestrator/runner.py advance <project_path>

# View current state
python3 orchestrator/runner.py status  <project_path>

# Force-set phase (override/recovery)
python3 orchestrator/state_machine.py init-phase <project_path> <phase>
```

State is persisted in `<project>/pipeline-status.json`. Fork agents write outcomes to `<project>/phase-outcomes/<phase>.json` as `{"outcome": "...", "notes": "..."}`.

## Pipeline Phase Map

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

**State machine is pure** — `state_machine.py` only handles transitions and status I/O. `runner.py` builds the full `fork_prompt` by composing tier preamble + skill file content + cross-project lessons overlay.

**Two agent tiers:**
- `standard` — AI Co-Author executing a work phase
- `heavy` — strict independent critic (P3, P5, P7, P11); injected with a preamble demanding rigorous, unforgiving evaluation

**Review verdict detection** uses regex on the output document: `整体判定[：:] Pass/Revise/Block`. The state machine reads this to determine transitions.

**Cross-project learning** — After P11, `/researchflow:evolve` extracts lessons to `~/.researchflow/lessons/<skill_name>.md`. Runner auto-injects these into future fork prompts for the same skill.

**Auto-detection fallback** — If `pipeline-status.json` is missing, `state_machine.py` infers the current phase by scanning for output documents (e.g., presence of `gap-analysis.md` → P3).

## File Layout

```
ResearchFlow/
├── paper-reading/                   ← PaperReading 子系统
│   ├── OVERVIEW.md                  ← 子系统说明与快速开始
│   ├── skills/
│   │   ├── paper-discovery-skill.md ← 论文发现与筛选
│   │   └── paper-reading-skill.md   ← 深度阅读与知识沉淀
│   └── templates/
│       ├── research-directions.md   ← 研究方向配置
│       ├── reading-queue.md         ← 阅读队列
│       ├── kb-index.md              ← 知识库总索引
│       └── paper-reading-note.md   ← 论文笔记模板
│
├── pipeline.md              ← ResearchFlow 方法论文档（人类阅读）
├── orchestrator/
│   ├── state_machine.py     ← Pure state machine: transitions, status I/O
│   └── runner.py            ← Builds fork_prompt; CLI for next/advance/status
├── plugin/commands/
│   ├── researchflow-run/    ← Main loop executor skill
│   ├── researchflow-status/ ← Status viewer
│   ├── researchflow-evolve/ ← Cross-project lesson extraction
│   ├── researchflow-goto/   ← Force phase override
│   ├── paper-reading-discover/ ← /paper-reading:discover command
│   └── paper-reading-read/     ← /paper-reading:read command
├── skills/
│   ├── *-skill.md           ← ResearchFlow P1-P11 skill files
│   ├── reflect-pipeline-skill.md  ← Post-phase reflection (shared by both subsystems)
│   └── review-configs/      ← YAML configs for P3/P5/P7 review dimensions
├── subagents/               ← SubAgent prompt templates (review, exit-assessment, etc.)
└── templates/               ← ResearchFlow project document templates
```

## Adding or Modifying a Phase

1. Edit `PHASES` dict in `orchestrator/state_machine.py` — add the phase key, skill name, outcome_type, tier, and transition map.
2. Create or update the corresponding `skills/<skill_name>-skill.md`.
3. If it's a review phase, add `skills/review-configs/<type>-review.yaml`.
4. If it requires human confirmation, add the phase key to `HUMAN_CHECKPOINT_PHASES` in `state_machine.py`.

## Project CLAUDE.md Template

When starting a new research project, copy `templates/project-claude-md.md` as the project's `CLAUDE.md`. It must include a `researchflow_path` field pointing to this repo so `/researchflow:run` can locate `runner.py`.
