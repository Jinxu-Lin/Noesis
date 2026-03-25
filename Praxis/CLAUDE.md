# CLAUDE.md — Praxis 子系统

This file provides guidance to Claude Code when working within the Praxis subsystem.

## What Praxis Is

Praxis 是 Noesis 的**研究执行子系统**，独立于 Logos 运行。v3 架构由**三个独立模块**组成，各自拥有独立的状态机和 runner：

```
┌─────────────────────────────────────────────────────────────┐
│  Module 1: Init (/praxis-init-auto)                         │
│    init → start → probe_design → review → probe_impl        │
│    → complete                                                │
│    交互式项目孵化 + 六维辩论压力测试 + 探针设计与实现        │
│    状态: Docs/init-module-status.json                        │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Module 2: Research (/praxis-r-auto)                        │
│    formalize → formalize_review → design → design_review    │
│    → blueprint → implement(manual) → retrospective          │
│    → complete                                                │
│    状态: Docs/research-module-status.json                    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Module 3: Paper (/praxis-paper)                            │
│    P1 → P2 → P3 → P4 → P5 → P6 → P7                       │
│    可在实验完成前启动 ({{PENDING:...}} 占位符)               │
│    状态: Papers/paper-status.json                            │
└─────────────────────────────────────────────────────────────┘
```

辅助命令（可在任意阶段调用）：

- **`/praxis-conclude`** — 实验失败诊断 → `iterate_method` / `iterate_direction` / `abandon`
- **`/praxis-present`** — 进展演示（三模块感知）
- **`/praxis-assimilate`** — 外部项目纳入 Noesis 框架（三模块架构）
- **`/praxis-evolve`** — 跨项目学习
- **`/praxis-optimize`** — prompt/skill 深度优化

## Paths

| 路径 | 说明 |
|------|------|
| Praxis 系统 | `~/Research/Noesis/Praxis` |
| 知识库 (Episteme) | `~/Research/Episteme` |
| 研究项目 | `~/Research/<项目名>` |
| Cross-project lessons | `~/.noesis/lessons/` |

所有路径使用 `~`，勿硬编码用户名（多 Mac 协作）。

## Quick Start

### 1. Init 模块（项目启动）

```
/praxis-init-auto <项目名>          ← 全自动：init → start → probe_design → review → probe_impl → complete
```

个别阶段命令：
```
/praxis-init <项目名>               ← 仅 init 阶段
/praxis-start <项目名>              ← 仅 start 阶段
/praxis-probe-design <项目路径>     ← 探针设计
/praxis-review <项目路径>           ← 六维辩论审查
/praxis-probe-impl <项目路径>       ← 探针实现
```

### 2. Research 模块（研究执行）

```
/praxis-r-auto <项目路径>           ← 全自动：formalize → formalize_review → design → design_review → blueprint → implement(manual) → retrospective → complete
```

个别阶段命令：
```
/praxis-r-formalize <项目路径>      ← 问题形式化
/praxis-r-formalize-review <项目路径> ← 形式化审查（4 debaters + codex）
/praxis-r-design <项目路径>         ← 方法+实验联合设计
/praxis-r-design-review <项目路径>  ← 设计审查（6 debaters + codex）
/praxis-r-blueprint <项目路径>      ← 实现蓝图
/praxis-r-implement <项目路径>      ← 实现（手动阶段）
/praxis-r-retrospective <项目路径>  ← 知识回收
```

### 3. Paper 模块（论文写作）

```
/praxis-paper <项目路径>            ← 自动执行 P1→P7
/praxis-paper-fill <项目路径>       ← 用实验结果填充 {{PENDING:...}} 占位符
```

可在实验完成前启动，占位符后续通过 `/praxis-paper-fill` 补全。

### 4. 失败诊断

```
/praxis-conclude <项目路径>
```

交互式分析失败原因。分层回退：方法层问题 → `iterate_method` → 回退到 design；方向层问题 → `iterate_direction` → 回退到 formalize。写入 `iteration-log.md` + `Codes/_Results/experiment_result.md`。

### 5. 其他辅助命令

```
/praxis-present <项目路径>          ← 生成进展演示文档（三模块感知，支持热启动）
/praxis-assimilate <项目路径>       ← 将外部项目纳入 Noesis 框架
/praxis-evolve <项目路径>           ← 提取跨项目 lessons + 更新 Noesis 框架文档
/praxis-optimize                    ← prompt/skill 深度优化
```

## Orchestrator CLI

### Init Module

`init_runner.py` 是 Init 模块的执行骨架，**始终通过 `init_runner.py` 操作**（除 `init-phase` 外不要直接调用 `init_state_machine.py`）。

```bash
python3 ~/Research/Noesis/Praxis/orchestrator/init_runner.py next    <project_path>
python3 ~/Research/Noesis/Praxis/orchestrator/init_runner.py advance <project_path>
python3 ~/Research/Noesis/Praxis/orchestrator/init_runner.py status  <project_path>
python3 ~/Research/Noesis/Praxis/orchestrator/init_state_machine.py init-phase <project_path> <phase>
```

状态持久化在 `<project>/Docs/init-module-status.json`。

### Research Module

`research_runner.py` 是 Research 模块的执行骨架，**始终通过 `research_runner.py` 操作**（除 `init-phase` 外不要直接调用 `research_state_machine.py`）。

```bash
# 获取下一步动作（返回 JSON，含 fork_prompt）
python3 ~/Research/Noesis/Praxis/orchestrator/research_runner.py next    <project_path>

# 推进状态（自动化阶段：fork agent 写完 phase-outcomes 后调用）
python3 ~/Research/Noesis/Praxis/orchestrator/research_runner.py advance <project_path>

# 推进状态（手动阶段 implement：研究者指定 outcome）
python3 ~/Research/Noesis/Praxis/orchestrator/research_runner.py advance <project_path> --outcome <outcome>

# 查看状态
python3 ~/Research/Noesis/Praxis/orchestrator/research_runner.py status  <project_path>

# 强制设置阶段（恢复/覆盖）
python3 ~/Research/Noesis/Praxis/orchestrator/research_state_machine.py init-phase <project_path> <phase>

# 跨模块回退
python3 ~/Research/Noesis/Praxis/orchestrator/research_runner.py rollback <project_path> --phase <phase> --mode <mode> [--context <file>]
```

**手动阶段 outcome 值**：

| 阶段 | 可用 outcome | 含义 |
|------|-------------|------|
| implement | `success` | 验证通过，进入 retrospective |
| implement | `iterate_method` | 方法层问题，回退到 design |
| implement | `iterate_direction` | 方向层问题，回退到 formalize |
| implement | `abandon` | 放弃，进入 complete |

状态持久化在 `<project>/Docs/research-module-status.json`（含 `entry_context` + `history`），`<project>/pipeline-status.json` 仅记录 `active_module`。Fork agent 将结果写入 `<project>/phase-outcomes/<phase>.json`，格式为 `{"outcome": "...", "notes": "..."}`。

### Paper Module

`paper_runner.py` 是 Paper 模块的执行骨架，**始终通过 `paper_runner.py` 操作**（除 `init-phase` 外不要直接调用 `paper_state_machine.py`）。

```bash
python3 ~/Research/Noesis/Praxis/orchestrator/paper_runner.py next    <project_path>
python3 ~/Research/Noesis/Praxis/orchestrator/paper_runner.py advance <project_path>
python3 ~/Research/Noesis/Praxis/orchestrator/paper_runner.py status  <project_path>
python3 ~/Research/Noesis/Praxis/orchestrator/paper_state_machine.py init-phase <project_path> <phase>
```

状态持久化在 `<project>/Papers/paper-status.json`。Fork agent 将结果写入 `<project>/Papers/phase-outcomes/<phase>.json`。

## Agent Tier

v3 统一使用 **opus** 模型。Init 和 Research 模块使用**单一 tier preamble**（不再区分 standard/heavy）。Paper 模块保留 heavy/standard 区分。

| Tier | 模型 | 阶段 |
|------|------|------|
| `standard` | claude-opus-4-6 | Paper: P2, P4, P6 |
| `heavy` | claude-opus-4-6 | Paper: P1, P3, P5, P7 |
| `codex` | gpt-4.5-high | formalize_review, design_review, P3, P7（并行，non-blocking） |

Codex 通过 Codex MCP 调用，完全独立的第三方外部审查者。MCP 不可用时自动跳过，不影响主流程路由。

## Pipeline Phase Map

### Module 1: Init

| Phase | Prompt | Type | Multi-Agent |
|-------|--------|------|-------------|
| init | `init-setup` | work | — |
| start | `start-analysis` | work | — |
| probe_design | `probe-design` | work | — |
| review | `init-review` | review | 6 debaters + synthesizer |
| probe_impl | `probe-impl` | work | — |

正常流程：`init → start → probe_design → review → probe_impl → complete`

Review 辩论结果存放在 `Reviews/init/round-N/`。

**Review Debaters（6 人）**：Innovator、Pragmatist、Theorist、Contrarian、Interdisciplinary、Empiricist

### Module 2: Research

| Phase | Prompt | Type | Multi-Agent | Codex |
|-------|--------|------|-------------|-------|
| formalize | `formalize` | work | — | — |
| formalize_review | `formalize-review` | review | 4 debaters + codex | ✓ |
| design | `design` | work | — | — |
| design_review | `design-review` | review | 6 debaters + codex | ✓ |
| blueprint | `blueprint` | work | — | — |
| implement | `implement` | manual | — | — |
| retrospective | `retrospective` | work | — | — |

正常流程：`formalize → formalize_review(pass) → design → design_review(pass) → blueprint → implement(success) → retrospective → complete`

**formalize_review 出口**：`pass` → design / `revise` → formalize / `abandon` → complete

**design_review 出口**：`pass` → blueprint / `revise` → design / `fundamental` → formalize / `abandon` → complete

**implement 出口**：`success` → retrospective / `iterate_method` → design / `iterate_direction` → formalize / `abandon` → complete

**formalize_review Debaters（4 人，战略层面）**：

| Debater | 核心视角 |
|---------|---------|
| Contrarian | 构建最强反驳：Gap 真实性、攻击角度致命缺陷 |
| Comparativist | 文献对照 + 在线搜索：Gap 新颖性、近期竞争工作 |
| Pragmatist | 可行性约束：探针可执行性、资源约束 |
| Interdisciplinary | 跨领域视角：替代问题框定、替代攻击角度 |

**design_review Debaters（6 人，技术层面）**：

| Debater | 核心视角 |
|---------|---------|
| Theorist | 数学/理论正确性：逻辑闭合、理论保证、隐含假设 |
| Methodologist | 评估协议完整性：数据泄漏、超参选择、ablation 覆盖 |
| Empiricist | 实验科学性：统计效力、baseline 公平 |
| Skeptic | 极端怀疑：最弱组件、最可能失败点、替代解释 |
| Pragmatist | 工程可行性：计算资源、实现复杂度、时间估计 |
| Contrarian | 构建最强反驳：与探针结果的一致性、过拟合探针信号风险 |

### Module 3: Paper（独立状态机）

| Phase | Prompt | Type | Tier | Codex |
|-------|--------|------|------|-------|
| P1 | `30-paper-outline` | work | heavy | — |
| P2 | `31-paper-sections` | work | standard | — |
| P3 | `32-paper-critique` | work | heavy | ✓ |
| P4 | `33-paper-integrate` | work | standard | — |
| P5 | `34-paper-review` | paper_review | heavy | — |
| P6 | `35-paper-latex` | work | standard | — |
| P7 | `36-project-review` | work | heavy | ✓ |

P5: 评分 < 7.0 → 回到 P4（最多 2 轮，超限强制通过）。

## Entry Context Modes

Runner 根据回退/修订路由自动注入上下文到 fork agent：

| mode | 触发条件 | 注入的额外文档 | 注入的指令关键词 |
|------|---------|--------------|----------------|
| `fr_revise` | formalize_review → revise | `Reviews/research-formalize/round-N/synthesis.md` | "基于审查修改，不从零开始" |
| `dr_revise` | design_review → revise | `Reviews/research-design/round-N/synthesis.md` | "基于设计审查修改" |
| `direction_pivot` | design_review → fundamental / implement → iterate_direction / design → escalate | `iteration-log.md` + 下游文档(参考) | "方向层问题，重新审视 Gap 和攻击角度" |
| `method_iterate` | implement → iterate_method | `Codes/_Results/experiment_result.md` + `iteration-log.md` | "方法层问题，修改失败组件，保留有效组件" |

## Iteration Guards

- **design 回退 >= 2 次** → 强制升级（escalate warning）→ 回退到 formalize
- **formalize 回退 >= 3 次** → 触发 abandon 评估（abandon warning）

## Key Behaviors

**文档版本控制**
- **单文件 + 元数据版本号**：每个研究文档头部 YAML frontmatter 记录 `version`、`entry_mode`、`iteration_major`、`iteration_minor`
- **版本号规则**：Major（大迭代，implement 回退重写）`1.x → 2.0`；Minor（review 后修改）`1.0 → 1.1`
- **审查文档覆盖策略**：`Reviews/` 下的审查文档每次覆盖旧版，不保留历史
- **iteration-log.md 倒序排列**：最新在最上方，排除方向和关键洞察必须记录

**架构原则**
- **三层架构**：Orchestrator (runner.py) 决定 WHAT/WHEN + 构建 fork_prompt；Prompts (prompts/*-prompt.md) 是纯 agent 指令；Slash commands (.claude/skills/) 是薄封装
- **Prompt 解耦原则**：prompt 自包含、不引用阶段代号、不感知迭代机制、不感知 tier。迭代上下文和 tier preamble 由 Runner 注入
- **`skills_parallel` 行动类型**：PHASES 含 `codex_agent` 字段时，runner 返回 `skills_parallel`，同时启动 main + codex Agent；main 写 `phase-outcomes/`（决定路由），codex 写 `codex-reviews/`（仅参考）
- **单一事实源**：Init 模块 `Docs/init-module-status.json`；Research 模块 `Docs/research-module-status.json`（含 `entry_context` + `history`）；Paper 模块 `Papers/paper-status.json`。`pipeline-status.json` 仅记录 `active_module`
- **X-reflect 自动注入**：每个非 manual 阶段完成后，runner 自动在 fork_prompt 末尾注入 `X-reflect-pipeline-prompt.md`，agent 将反思追加到 `pipeline-evolution-log.md`
- **Results 管理**：`Codes/_Results/`（md 文件，git tracked）；`Codes/_Data/`（生成数据，gitignored）

**项目目录结构**
- `research/`：problem-statement.md, method-design.md, experiment-design.md, contribution.md, retrospective.md
- `Reviews/`：init/round-N/, research-formalize/round-N/, research-design/round-N/（审查辩论记录）
- `codex-reviews/`：外部 AI 审查（仅参考）
- `Codes/_Results/`：probe_result.md, experiment_result.md（实验结果，git tracked）
- `Codes/_Data/`：生成数据（gitignored）
- `phase-outcomes/`：阶段结果 JSON + 辩论中间文件

## Cross-Project Learning

项目 retrospective 完成后，运行 `/praxis-evolve` 产出两类成果：

1. **跨项目 Lessons** → `~/.noesis/lessons/<skill_name>.md`：含类别标签 `[SYSTEM/EXPERIMENT/WRITING/...]`、频率标签 `[RECURRING/NEW]`、有效性标签 `[verified/ineffective/unverified]`。Runner 在后续项目的相同阶段自动注入有效 lessons；`[ineffective]` 自动过滤；`[RECURRING]` 排在最前。

2. **框架进化** → 基于 `pipeline-evolution-log.md` 中各阶段的 X-reflect 条目，更新 `Praxis/prompts/`、`Praxis/skills/`、`Praxis/templates/` 文档，并 push 到 Noesis GitHub。

## File Layout

```
Praxis/
├── CLAUDE.md                                ← 本文件
├── orchestrator/
│   ├── init_state_machine.py               ← Init 模块状态机 (init→start→probe_design→review→probe_impl)
│   ├── init_runner.py                      ← Init 模块 runner
│   ├── research_state_machine.py           ← Research 模块状态机 (formalize→...→retrospective)
│   ├── research_runner.py                  ← Research 模块 runner
│   ├── paper_state_machine.py              ← Paper 模块状态机 (P1→P7)
│   └── paper_runner.py                     ← Paper 模块 runner
├── prompts/
│   ├── ── Init Module ──
│   ├── init-setup-prompt.md                ← init 阶段
│   ├── start-analysis-prompt.md            ← start 阶段
│   ├── probe-design-prompt.md              ← probe_design 阶段
│   ├── init-review-prompt.md               ← review 阶段（6 debaters）
│   ├── probe-impl-prompt.md                ← probe_impl 阶段
│   ├── ── Research Module ──
│   ├── formalize-prompt.md                 ← 问题形式化
│   ├── formalize-review-prompt.md          ← 形式化审查（4 debaters）
│   ├── design-prompt.md                    ← 方法+实验联合设计
│   ├── design-review-prompt.md             ← 设计审查（6 debaters）
│   ├── blueprint-prompt.md                 ← 实现蓝图
│   ├── implement-prompt.md                 ← 实现规划
│   ├── retrospective-prompt.md             ← 知识回收
│   ├── ── Paper Module ──
│   ├── 30-paper-outline-prompt.md          ← P1 论文大纲
│   ├── 31-paper-sections-prompt.md         ← P2 章节写作
│   ├── 32-paper-critique-prompt.md         ← P3 多角色审查
│   ├── 33-paper-integrate-prompt.md        ← P4 编辑整合
│   ├── 34-paper-review-prompt.md           ← P5 终审
│   ├── 35-paper-latex-prompt.md            ← P6 LaTeX 编译
│   ├── 36-project-review-prompt.md         ← P7 项目级审查
│   ├── paper-fill-prompt.md                ← {{PENDING:...}} 占位符填充
│   ├── ── Shared / Utility ──
│   ├── codex-reviewer-prompt.md            ← Codex 外部审查者
│   ├── codex-writer-prompt.md              ← Codex 写作辅助
│   ├── X-reflect-pipeline-prompt.md        ← 跨阶段流程反思（每阶段自动注入）
│   ├── optimize-prompt.md                  ← prompt/skill 优化
│   └── review-configs/                     ← 审查配置（YAML）
│       ├── init-review.yaml                ← Init review 审查维度
│       ├── formalize-review.yaml           ← formalize_review 审查维度
│       └── design-review.yaml              ← design_review 审查维度
├── skills/                                  ← 非自动化模块的详细指令
│   ├── conclude-skill.md                   ← /praxis-conclude（分层失败诊断）
│   ├── present-skill.md                    ← /praxis-present（三模块感知）
│   ├── assimilate-skill.md                 ← /praxis-assimilate（三模块架构）
│   └── evolve-skill.md                     ← /praxis-evolve
├── subagents/                               ← SubAgent prompt 模板（13 角色）
│   ├── innovator-subagent.md               ← 创新者（Init review）
│   ├── pragmatist-subagent.md              ← 务实者（Init review + design_review）
│   ├── theorist-subagent.md                ← 理论家（Init review + design_review）
│   ├── contrarian-subagent.md              ← 反对者（Init review + formalize_review + design_review）
│   ├── interdisciplinary-subagent.md       ← 跨学科者（Init review + formalize_review）
│   ├── empiricist-subagent.md              ← 实验主义者（Init review + design_review）
│   ├── synthesizer-subagent.md             ← 综合者（汇总辩论结果）
│   ├── comparativist-subagent.md           ← 对比分析者（formalize_review）
│   ├── methodologist-subagent.md           ← 方法论者（design_review）
│   ├── skeptic-subagent.md                 ← 怀疑论者（design_review）
│   ├── work-synthesizer-subagent.md        ← 工作综合者
│   ├── paper-critic-subagent.md            ← 论文审查（5 角色）
│   └── exit-assessment-subagent.md         ← 退出评估
├── templates/
│   ├── project-claude-md.md                ← 新项目 CLAUDE.md 模板
│   ├── project.md                          ← 项目文档模板
│   ├── contribution.md                     ← 跨阶段贡献跟踪
│   ├── iteration-log.md                    ← 迭代历史模板
│   ├── result.md                           ← 实验结果模板
│   ├── retrospective.md                    ← retrospective 输出模板
│   ├── proposal.md                         ← 提案模板
│   └── pipeline-evolution-log.md           ← 流水线演进日志
└── docs/
    └── init-module-iteration-plan.md       ← Init 模块迭代计划
```

## Adding or Modifying a Phase

### Init Module
1. 编辑 `init_state_machine.py` 中的 `PHASES` 字典 — 添加 phase key、skill name、outcome_type、transitions map
2. 创建或更新 `prompts/<skill_name>-prompt.md`
3. 如果是审查阶段，在 `prompts/review-configs/` 下添加对应 YAML 配置
4. 更新本文件（`Praxis/CLAUDE.md`）和根目录 `Noesis/CLAUDE.md`

### Research Module
1. 编辑 `research_state_machine.py` 中的 `PHASES` 字典 — 添加 phase key、skill name、outcome_type、transitions、debate_agents（如适用）
2. 创建或更新 `prompts/<skill_name>-prompt.md`（遵循标准 Prompt 结构：角色与核心目标 → 输入文档 → 行动流程 → 输出规范 → 迭代上下文处理 → 禁止事项）
3. 如果是审查阶段，添加 `prompts/review-configs/<type>-review.yaml`，定义 `debate_agents` 列表和审查维度
4. 如果需要 Codex 并行审查，在 PHASES 条目中添加 `"codex_agent": "codex-reviewer"`
5. 如果是手动阶段，设置 `skill: None, outcome_type: "manual"`，确保 Runner 支持 `--outcome` 参数
6. 如需新增 debater SubAgent，在 `subagents/` 下创建 `<role>-subagent.md`
7. 更新本文件（`Praxis/CLAUDE.md`）和根目录 `Noesis/CLAUDE.md` 的阶段表

### Paper Module
1. 编辑 `paper_state_machine.py` 中的 `PHASES` 字典
2. 创建或更新 `prompts/<number>-<name>-prompt.md`
3. 更新本文件和根目录 `Noesis/CLAUDE.md`
