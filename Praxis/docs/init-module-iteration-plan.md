# Init Module Iteration Plan

> 迭代目标：将当前 Praxis 的 Startup（单体 8 步）+ Crystallize 拆分为模块化的初始化模块（init → start → probe_design → review → probe_impl），支持自动运行和单步执行两种模式。

---

## 1. 架构概览

### 1.1 状态机

```
init → start → probe_design → review ──Pass──→ probe_impl → complete
                 ↑                      │           │
                 │              revise ──┘    infeasible → probe_design
                 │
                 │  ← 后续模块 probe 失败可回退到 start
```

### 1.2 核心设计原则

- **单一文档**：所有子模块共同维护 `project.md`
- **独立状态机**：`Docs/init-module-status.json`，与后续模块状态文件分离
- **双入口模式**：`/praxis-init-auto` 运行全流程；各子命令可单独运行
- **全 opus 模型**：所有子模块均使用 opus
- **无用户交互**：所有子模块由 agent 自主完成，信息从对话上下文提取
- **Git 同步**：每个子模块完成后 commit + push
- **计算资源感知**：GPU 信息写入 CLAUDE.md + project.md，所有分析基于资源约束
- **Review 记录分离**：辩论记录放 `Reviews/init/round-N/`，project.md §4 只放摘要

### 1.3 回退机制

| 触发 | entry_context.mode | start 的行为 |
|------|-------------------|-------------|
| init 完成后首次进入 | `first` | 从零分析 |
| review 判定 revise | `review_revise` | 读 synthesis.md，针对性修改 §2 |
| 后续模块 probe 失败 | `probe_failure` | 读 probe 结果，重新审视 §2 |

---

## 2. 文件变更清单

### 2.1 新建文件

| 文件 | 类型 | 说明 |
|------|------|------|
| `Praxis/orchestrator/init_state_machine.py` | 状态机 | init 模块状态转移 |
| `Praxis/orchestrator/init_runner.py` | Runner | init 模块 prompt 组装 + CLI |
| `Praxis/prompts/init-setup-prompt.md` | Prompt | init 子模块：上下文提取 + 脚手架 |
| `Praxis/prompts/start-analysis-prompt.md` | Prompt | start 子模块：深度分析 |
| `Praxis/prompts/probe-design-prompt.md` | Prompt | probe_design 子模块 |
| `Praxis/prompts/init-review-prompt.md` | Prompt | review 子模块：辩论 + 综合 |
| `Praxis/prompts/review-configs/init-review.yaml` | Config | review 辩论配置 |
| `Praxis/templates/project.md` | Template | project.md 模板 |
| `.claude/skills/praxis-init/SKILL.md` | Skill | `/praxis-init` 命令 |
| `.claude/skills/praxis-init-auto/SKILL.md` | Skill | `/praxis-init-auto` 命令 |
| `.claude/skills/praxis-probe-design/SKILL.md` | Skill | `/praxis-probe-design` 命令 |
| `.claude/skills/praxis-review/SKILL.md` | Skill | `/praxis-review` 命令 |

### 2.2 修改文件

| 文件 | 变更 |
|------|------|
| `.claude/skills/praxis-start/SKILL.md` | 重写：从当前 8 步 Startup 改为新 start 子模块的调度 |
| `Praxis/templates/project-claude-md.md` | 更新：加入 GPU 资源、init 模块状态、目录结构 |

### 2.3 保留不动

| 文件 | 原因 |
|------|------|
| `research_state_machine.py` / `research_runner.py` | 研究模块独立，后续迭代 |
| `paper_state_machine.py` / `paper_runner.py` | 论文模块独立 |
| `Praxis/prompts/crystallize-prompt.md` | 研究模块使用，后续迭代调整 |
| `Praxis/skills/start-skill.md` | 保留为参考，新 prompt 替代其功能 |
| `Praxis/subagents/*.md` | review 子模块复用 |
| 所有 paper prompts (30-36) | 论文模块使用 |

---

## 3. 各子模块详细规格

### 3.1 init 子模块

**输入**: 当前对话上下文
**输出**: 项目目录 + project.md §1 + CLAUDE.md + Git repo
**Prompt**: `init-setup-prompt.md`

**执行步骤**:
1. 创建目录结构: `Docs/`, `Reviews/`, `Codes/`, `Papers/`, `.gitignore`
2. 从对话上下文提取 topic, idea, baseline papers, GPU resources
3. 填充 project.md §1 (Overview)
4. 生成 CLAUDE.md (含 GPU 资源信息)
5. 初始化 `pipeline-status.json` + `Docs/init-module-status.json`
6. `git init` + `gh repo create` + 首次 commit + push

### 3.2 start 子模块

**输入**: project.md §1 + entry_context (first / review_revise / probe_failure)
**输出**: project.md §2 (Problem & Approach)
**Prompt**: `start-analysis-prompt.md`

**§2 内容**:
- §2.1 Baseline Analysis: 解决了什么 / 没解决什么 / 为什么没解决（含计算资源约束分析）
- §2.2 Problem Definition: 一句话问题 + 真实性论证 + 重要性论证 + 价值层次
- §2.3 Root Cause Analysis: 3 层 Why + 类型 + 思想实验验证
- §2.4 Proposed Approach: 1-2 段核心直觉（含计算可行性评估）
- §2.5 Core Assumptions: 3-5 条，四类框架（数据/模型/优化/评估）

**迭代模式处理**:
- `review_revise`: 注入 `Reviews/init/round-N/synthesis.md`，针对性修改
- `probe_failure`: 注入 probe 失败结果，重新审视问题定义和方法

### 3.3 probe_design 子模块

**输入**: project.md §1-2
**输出**: project.md §3 (Validation Strategy)
**Prompt**: `probe-design-prompt.md`

**§3 内容**:
- §3.1 Idea Type Classification: 5 种类型 + 验证重心
- §3.2 Core Hypothesis: 从 §2.5 提取最关键假设
- §3.3 Probe Experiment Design: 数据 + 模型 + 实验模式
- §3.4 Pass/Fail Criteria: 数值化标准
- §3.5 Time Budget & Resources: 必须在 §1.4 资源范围内
- §3.6 Failure Diagnosis Plan: 失败模式 × 特征 × 后续动作

### 3.4 review 子模块

**输入**: project.md §1-3 完整内容
**输出**: `Reviews/init/round-N/*.md` + project.md §4 摘要
**Prompt**: `init-review-prompt.md` + `review-configs/init-review.yaml`

**6 debater roles**: Innovator, Pragmatist, Theorist, Contrarian, Interdisciplinary, Empiricist
**每个 debater 输出**: `Reviews/init/round-N/<role>.md`
**Synthesizer 输出**: `Reviews/init/round-N/synthesis.md`

**Decision**: Pass / Revise / Hold / Stop
- Pass → complete，写入 §4.3 + §4.4
- Revise → 回到 start（entry_context: review_revise）
- Hold → 等待用户补充
- Stop → 记录终止原因

---

## 4. 状态机规格

### 4.1 状态文件

**pipeline-status.json** (顶层):
```json
{"active_module": "init", "module_history": [...]}
```

**Docs/init-module-status.json** (模块内):
```json
{"phase": "start", "entry_context": {...}, "history": [...]}
```

### 4.2 状态转移表

```python
PHASES = {
    "init":         next: {done → start}
    "start":        next: {done → probe_design}
    "probe_design": next: {done → review}
    "review":       next: {pass → complete, revise → start, hold → hold, stop → complete}
    "hold":         next: {resume → review}  # manual
    "complete":     terminal
}
```

### 4.3 回退 CLI

```bash
# review revise（自动触发）
python3 init_runner.py advance <path> --outcome revise

# 后续模块 probe 失败回退
python3 init_runner.py rollback <path> --phase start --mode probe_failure --context <file>
```

---

## 5. 实施顺序

1. 状态机 + Runner（骨架）
2. project.md 模板
3. 4 个子模块的 Prompt
4. Review 配置 (YAML)
5. 5 个 Skill（slash commands）
6. 更新 CLAUDE.md 模板

---

## 6. Research Module（研究模块）

> Init Module 完成后，项目进入 Research Module。以下为研究模块的状态机、命令和阶段说明。

### 6.1 状态机

```
formalize → formalize_review ──Pass──→ design → design_review ──Pass──→ blueprint → implement → retrospective → complete
               ↑                │                    ↑            │
               │        revise ─┘                    │    revise ─┘
               │                                     │
               │  ← design_review fundamental 回退   │
               │                                     │
               └─────────── implement 失败可回退 ────┘
```

### 6.2 命令

```bash
# 自动运行全流程
/praxis-r-auto

# 单步命令
/praxis-r-formalize        # 运行 formalize 阶段
/praxis-r-formalize-review # 运行 formalize_review 阶段
/praxis-r-design           # 运行 design 阶段
/praxis-r-design-review    # 运行 design_review 阶段
/praxis-r-blueprint        # 运行 blueprint 阶段
/praxis-r-implement        # 运行 implement 阶段
/praxis-r-retrospective    # 运行 retrospective 阶段
```

#### CLI

```bash
# 获取下一步动作
python3 ~/Research/Noesis/Praxis/orchestrator/research_runner.py next <project_path>

# 推进状态（自动阶段）
python3 ~/Research/Noesis/Praxis/orchestrator/research_runner.py advance <project_path>

# 推进状态（手动，含 outcome）
python3 ~/Research/Noesis/Praxis/orchestrator/research_runner.py advance <project_path> --outcome <outcome>

# 查看状态
python3 ~/Research/Noesis/Praxis/orchestrator/research_runner.py status <project_path>
```

### 6.3 阶段说明

| 阶段 | 说明 |
|------|------|
| **formalize** | 将 Init Module 的 project.md 中的问题定义和方法直觉，形式化为严格的研究问题、假设和方法框架 |
| **formalize_review** | 对形式化结果进行多角色辩论审查（战略层面），判定 Pass / Revise / Hold / Stop |
| **design** | 基于形式化的研究问题，进行方法与实验的联合设计（技术细节层面） |
| **design_review** | 对技术设计进行多角色辩论审查（技术层面），判定 Pass / Revise / Fundamental（回退到 formalize） |
| **blueprint** | 将设计转化为可执行的实现蓝图（代码结构、依赖、接口规范） |
| **implement** | 按蓝图执行实现，产出可运行的实验代码 |
| **retrospective** | 实验完成后的知识回收，提取经验教训，标记假设验证状态 |
| **complete** | 终态，研究模块完成 |

### 6.4 跨模块回退路径

| 触发场景 | 回退目标 | entry_context.mode |
|----------|---------|-------------------|
| formalize_review 判定 Revise | formalize | `review_revise` |
| design_review 判定 Revise | design | `review_revise` |
| design_review 判定 Fundamental | formalize | `fundamental_revise` |
| implement 方法层失败 | design | `implement_iterate` |
| implement 方向层失败 | formalize | `implement_pivot` |
| Research Module 需要重新审视问题定义 | Init Module start | `probe_failure`（跨模块回退） |
