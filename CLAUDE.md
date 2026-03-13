# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

**Noesis** 是一个 AI Agent 自动科研系统，面向 AI/ML/DL 方向。系统名取自希腊语 νόησις（认知/洞察），包含两个**独立**子系统：

**Logos**（`Logos/`）— 持续知识积累系统，循环运行：
- 论文发现（arXiv/Semantic Scholar 多策略搜索，含争议/负面结果搜索）
- 深度阅读、知识资产提取（Methods Bank、Gaps & Assumptions、Experimental Patterns、Cross-Paper Connections、Reusable Resources）
- 命令：`/logos-discover`、`/logos-read`（强制使用 Sonnet 模型）
- 知识库产出位于：`~/Research/Episteme`

**Praxis**（`Praxis/`）— 研究执行流程，五大模块：
- **Startup**：`/praxis-start` — 交互式项目种子孵化（六维辩论压力测试），完成后设状态 → C
- **Research**：`/praxis-research` — 自动化研究循环（C→RS→P→D→RT→I→E→W→R），产出方法设计+实验规划+知识回收
- **Code**：人工编码与实验（E 阶段），失败时 `/praxis-conclude` 总结并分层回退（方法层→D / 方向层→C）
- **Paper**：`/praxis-paper` — 自动化论文写作（P1→P7），独立状态机驱动
- **Evolution**：`/praxis-evolve` — 提取跨项目教训 + 更新 Noesis 框架文档
- 其他命令：`/praxis-assimilate`、`/praxis-present`、`/praxis-conclude`

两个子系统通过**知识库（Episteme）**连接：Logos 填充知识库，Praxis 在以下阶段消费：
- **C (Crystallize)** ← Episteme: Gaps & Assumptions, Cross-Paper Connections
- **D (Joint Design)** ← Episteme: Methods Bank, Experimental Patterns

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

**远程服务器**：I（Impl Planning）后的实验通过 SSH MCP 在远程 GPU 服务器上执行，代码通过 git 同步到服务器，结果通过 git 或 SSH MCP 回传本地。

## Skills (Slash Commands)

所有自定义命令通过 `.claude/skills/` 注册（项目级），无需额外配置。

### Logos skills（model: sonnet）
- `/logos-discover [kb_path]` — 论文发现：多策略搜索、Quick Scan 评分（4维度）、更新阅读队列
- `/logos-read [参数]` — 深度阅读：提取 5 类知识资产、更新知识库
- `kb_path` 默认为 `~/Research/Episteme`，可省略
- `/logos-read` 参数：无参（读队列第1篇）/ 数字（读N篇）/ arXiv ID / 标题关键词

### Praxis skills
- `/praxis-start <project_name>` — 交互式项目启动（六维辩论），创建项目于 `~/Research/<project_name>/`，完成后状态设为 C
- `/praxis-research <project_path>` — 自动化研究循环（C→RS→P→D→RT→I→E→W→R）
- `/praxis-paper <project_path>` — 自动化论文写作（P1→P7）
- `/praxis-conclude <project_path>` — 实验失败总结，写 iteration-log + result.md，分层回退（方法层→D / 方向层→C）
- `/praxis-assimilate <project_path>` — 同化现有项目（重建文档 + 真实运行 RS/RT 评审）
- `/praxis-present <project_path>` — 生成 presentation.md（热启动支持，保留人工编辑）
- `/praxis-evolve <project_path>` — 提取跨项目 lessons + 更新 Noesis 框架文档

## Orchestrator CLI (Praxis)

始终通过 `research_runner.py` 操作（除 `init-phase` 外不直接调用 state machine）。

```bash
# 获取下一步动作（返回 JSON，含 fork_prompt）
python3 ~/Research/Noesis/Praxis/orchestrator/research_runner.py next    <project_path>

# 推进状态（fork agent 写完 phase-outcomes/<phase>.json 后调用）
# 自动化阶段（无需 --outcome）：
python3 ~/Research/Noesis/Praxis/orchestrator/research_runner.py advance <project_path>
# 手动阶段（P/E 需指定 --outcome）：
python3 ~/Research/Noesis/Praxis/orchestrator/research_runner.py advance <project_path> --outcome signal
python3 ~/Research/Noesis/Praxis/orchestrator/research_runner.py advance <project_path> --outcome pivot
python3 ~/Research/Noesis/Praxis/orchestrator/research_runner.py advance <project_path> --outcome iterate_method
python3 ~/Research/Noesis/Praxis/orchestrator/research_runner.py advance <project_path> --outcome iterate_direction

# 查看当前状态
python3 ~/Research/Noesis/Praxis/orchestrator/research_runner.py status  <project_path>

# 强制设置阶段（恢复/覆盖）
python3 ~/Research/Noesis/Praxis/orchestrator/research_state_machine.py init-phase <project_path> <phase>
```

状态持久化在 `<project>/pipeline-status.json`（含 `entry_context` + `history`）。Fork agents 将结果写入 `<project>/phase-outcomes/<phase>.json`，格式：`{"outcome": "...", "notes": "..."}`。

### Paper Writing Orchestrator

```bash
python3 ~/Research/Noesis/Praxis/orchestrator/paper_runner.py next    <project_path>
python3 ~/Research/Noesis/Praxis/orchestrator/paper_runner.py advance <project_path>
python3 ~/Research/Noesis/Praxis/orchestrator/paper_runner.py status  <project_path>
python3 ~/Research/Noesis/Praxis/orchestrator/paper_state_machine.py init-phase <project_path> <phase>
```

论文状态持久化在 `<project>/Papers/paper-status.json`。Paper outcomes 写入 `<project>/Papers/phase-outcomes/<phase>.json`。

## Pipeline Phase Map (Praxis)

### Main Pipeline（startup 独立，/praxis-research 从 C 开始）

| Phase | Skill | Type | Tier | Multi-Agent | Codex |
|-------|-------|------|------|-------------|-------|
| S (startup) | `start-skill` | interactive | — | 6 debaters + synthesizer | — |
| C (crystallize) | `crystallize` | work | heavy | — | — |
| RS (strategic review) | `strategic-review` | review | heavy | 4 debaters + synthesizer | ✓ |
| P (probe) | — | manual | — | — | — |
| D (joint design) | `joint-design` | work | heavy | — | — |
| RT (technical review) | `technical-review` | review | heavy | 6 debaters + synthesizer | ✓ |
| I (implementation) | `implementation` | work | standard | — | — |
| E (execution) | — | manual | — | — | — |
| W (paper writing) | — | manual (独立 paper pipeline) | — | — | — |
| R (retrospective) | `retrospective` | work | heavy | — | — |

**正常流程**：S → C → RS(pass) → P(signal) → D → RT(pass) → I → E(success) → W → R → complete

**RS 出口**：pass→P / revise→C / abandon→R
**P 出口**：signal→D / pivot→C / abandon→R
**RT 出口**：pass→I / revise→D / fundamental→C / abandon→R
**E 出口**：success→W / iterate_method→D / iterate_direction→C / abandon→R

**RS debaters**（4 人，战略层面）：Contrarian、Comparativist、Pragmatist、Interdisciplinary
**RT debaters**（6 人，技术层面）：Theorist、Methodologist、Empiricist、Skeptic、Pragmatist、Contrarian

R (Retrospective) 在 W (Paper Writing) 完成后执行（知识回收，可标记 validated/refuted）。

**项目目录结构**（研究文档和审查文件分别存放在子目录中）：
- `research/`：problem-statement.md, probe-results.md, method-design.md, experiment-design.md, contribution.md, result.md, retrospective.md
- `inner-reviews/`：strategic-review.md, technical-review.md
- `codex-reviews/`：外部 AI 审查（仅参考）
- `phase-outcomes/`：阶段结果 JSON + 辩论中间文件（`debate/RS/`、`debate/RT/`）
- `experiments/`：probe/（探针实验）、iter-N/（大迭代历史数据）

### Paper Writing Module（独立状态机）

| Phase | Skill | Type | Tier | Codex |
|-------|-------|------|------|-------|
| P1 | `30-paper-outline` | work | heavy | — |
| P2 | `31-paper-sections` | work | standard | — |
| P3 | `32-paper-critique` | work | heavy | ✓ |
| P4 | `33-paper-integrate` | work | standard | — |
| P5 | `34-paper-review` | paper_review | heavy | — |
| P6 | `35-paper-latex` | work | standard | — |
| P7 | `36-project-review` | work | heavy | ✓ |

P5: 评分 < 7.0 → 回到 P4（最多 2 轮，超限强制通过）。

## Key Architecture Decisions

**两个独立子系统** — Logos 和 Praxis 各有独立的 skills 和 templates，无运行时依赖。唯一连接：Praxis 在 C/D 消费 Logos 产出的 Episteme 知识库（C ← Gaps & Assumptions + Cross-Paper Connections；D ← Methods Bank + Experimental Patterns）。

**三层架构（Praxis）** — Orchestrator（runner.py）决定 WHAT/WHEN + 构建 fork_prompt；Prompts（`Praxis/prompts/*-prompt.md`）是纯 agent 指令；Slash commands（`.claude/skills/praxis-*/SKILL.md`）是薄封装运行器；State machines 是纯转换 + I/O，无 prompt 逻辑。

**三种 Agent Tier（Praxis）**：
- `standard` — AI Co-Author，执行性/模板化工作（I, P2, P4, P6）
- `heavy` — 严格独立批判审查者/深度思考者（C, RS, D, RT, R, P1, P3, P5, P7）；注入"严格、不妥协"preamble
- `codex` — 通过 Codex MCP 调用 GPT-4.5-high，第三方外部视角（RS, RT, P3, P7）；non-blocking，MCP 不可用时自动跳过

**五大模块** — Startup（`/praxis-start`，交互式）→ Research（`/praxis-research`，C→RS→P→D→RT→I）→ Execution（E，人工编码实验，`/praxis-conclude` 处理失败）→ Paper（`/praxis-paper` 或 W，P1→P7）→ Retrospective（R）→ Evolution（`/praxis-evolve`）

**按决策性质切分阶段** — v2 不再按文档类型切分（gap/method/experiment），而是按决策层次：C = 战略决策（Gap + 攻击角度 + 探针方案，三者循环耦合不可分离）；D = 技术决策（方法 + 实验联合设计，组件与 ablation 同步）。两次审查分别对应：RS = 战略审查（值不值得做）；RT = 技术审查（做得对不对）。

**探针实验前置（P 阶段）** — 在完整方法设计之前，用最小成本验证核心直觉。P 是手动阶段，研究者执行 problem-statement.md §3 中定义的探针方案，产出 probe-results.md。这确保方向判断基于经验信号而非纯理论推演。

**分层回退** — 失败根因在哪个层次，就回退到哪个阶段。E 阶段失败时：方法层问题（iterate_method）→ D；方向层问题（iterate_direction）→ C。不再统一回退到起点。迭代守卫：D 回退 ≥ 2 次强制升级到 C 回退；C 回退 ≥ 3 次触发 abandon 评估。

**文档版本控制** — 单文件 + 元数据版本号 + iteration-log。每个研究文档头部使用 YAML frontmatter（version, iteration_major, iteration_minor, entry_mode）。版本号采用 `<major>.<minor>`：Major = E 或 P 回退导致重写（1.x → 2.0）；Minor = Review 后 Revise（1.0 → 1.1）。`iteration-log.md` 倒序排列，记录排除方向和失败洞察。审查文档采用覆盖策略（不保留历史版本）。

**两套独立状态机** — 主 pipeline（`research_state_machine.py` + `research_runner.py`，状态 `pipeline-status.json`）和 Paper 模块（`paper_state_machine.py` + `paper_runner.py`，状态 `Papers/paper-status.json`）。完全解耦。

**单一事实源** — 主 pipeline 唯一状态源：`pipeline-status.json`（含 entry_context + history）；论文模块：`Papers/paper-status.json`。无自动检测或回退推断。

**迭代模式（Runner 自动注入）** — 6 种 entry_context mode：`first`（首次）、`rs_revise`（战略审查修改）、`probe_pivot`（探针失败换攻击角度）、`rt_revise`（技术审查修改）、`execute_iterate`（方法层回退）、`execute_pivot`（方向层回退）。Runner 根据 mode 注入对应的审查文档、iteration-log、result.md 等上下文。

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
│   │   ├── research_state_machine.py ← 研究 pipeline 状态机（C→RS→P→D→RT→I→E→W→R）
│   │   ├── research_runner.py        ← 研究 pipeline runner
│   │   ├── paper_state_machine.py    ← 论文 pipeline 状态机（P1-P7）
│   │   └── paper_runner.py           ← 论文 pipeline runner
│   ├── skills/                      ← 非自动化模块详细指令
│   │   ├── start-skill.md           ← /praxis-start（六维辩论）
│   │   ├── conclude-skill.md        ← /praxis-conclude（分层失败诊断）
│   │   ├── assimilate-skill.md      ← /praxis-assimilate
│   │   ├── evolve-skill.md          ← /praxis-evolve
│   │   └── present-skill.md         ← /praxis-present
│   ├── prompts/                     ← 状态机 fork agent 指令（runner 自动加载）
│   │   ├── crystallize-prompt.md           ← C 问题锐化
│   │   ├── strategic-review-prompt.md      ← RS 战略审查
│   │   ├── probe-guide.md                  ← P 探针实验执行指南
│   │   ├── joint-design-prompt.md          ← D 联合设计
│   │   ├── technical-review-prompt.md      ← RT 技术审查
│   │   ├── implementation-prompt.md        ← I 实现规划
│   │   ├── retrospective-prompt.md         ← R 知识回收
│   │   ├── 3?-*-prompt.md                  ← Paper module (P1-P7)
│   │   ├── codex-reviewer-prompt.md        ← Codex 外部审查者
│   │   ├── X-reflect-pipeline-prompt.md    ← 阶段反思（每阶段自动注入）
│   │   └── review-configs/                 ← 审查配置 YAML
│   │       ├── strategic-review.yaml       ← RS 审查维度（7 项）
│   │       └── technical-review.yaml       ← RT 审查维度（10 项）
│   ├── subagents/                   ← SubAgent prompt 模板（startup 六维辩论 + RS/RT debaters）
│   └── templates/                   ← 项目文档模板
│
├── .claude/skills/                  ← 项目级 skills (slash commands)
│   ├── logos-discover/              ← /logos-discover (model: sonnet)
│   ├── logos-read/                  ← /logos-read (model: sonnet)
│   ├── praxis-start/                ← /praxis-start
│   ├── praxis-research/             ← /praxis-research (C→R, automated)
│   ├── praxis-paper/                ← /praxis-paper (P1→P7, automated)
│   ├── praxis-assimilate/           ← /praxis-assimilate
│   ├── praxis-conclude/             ← /praxis-conclude
│   ├── praxis-present/              ← /praxis-present
│   └── praxis-evolve/               ← /praxis-evolve
│
├── introduction.md                  ← 系统说明书（人类阅读）
├── CLAUDE.md                        ← 本文件
└── README.md
```

## Adding or Modifying a Phase (Praxis)

1. 编辑 `Praxis/orchestrator/research_state_machine.py` 的 `PHASES` 字典 — 添加 phase key、skill name、outcome_type、tier、transitions、debate_agents（如适用）
2. 创建或更新 `Praxis/prompts/<skill_name>-prompt.md`
3. 如果是审查阶段，添加 `Praxis/prompts/review-configs/<type>-review.yaml` 并配置 `debate_agents` 列表
4. 如果是手动阶段，设置 `skill: None`、`outcome_type: "manual"`，确保 `advance` 命令支持 `--outcome` 标志
5. 如果需要 Codex 并行审查，在 PHASES 条目中添加 `"codex_agent": "codex-reviewer"`

## Project CLAUDE.md Template

启动新项目时，`/praxis-start` 自动从 `Praxis/templates/project-claude-md.md` 创建项目 `CLAUDE.md`，包含 `noesis_path` 字段（指向本 repo），供 `/praxis-research` 定位 `research_runner.py`。
