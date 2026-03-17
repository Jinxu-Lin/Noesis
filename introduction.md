# Noesis 系统说明书

> 本文档是 Noesis 的完整使用手册与架构说明。  
> 如果 [README.md](README.md) 更像产品首页，那么这里就是可顺读、可查阅、可落地执行的系统说明书。

---

## 阅读导航

如果你第一次接触 Noesis，建议按这个顺序阅读：

1. `1-3` 节：理解 Noesis 的定位、路线与总体结构
2. `4-5` 节：完成环境准备与最小可运行设置
3. `6-13` 节：了解 Logos、Praxis 与所有核心命令
4. `14-16` 节：查看典型工作流、CLI 与文件布局
5. `17-19` 节：理解系统的设计原则与适用场景

---

## 1. Noesis 是什么

**Noesis**（νόησις，认知与洞察）是一套运行在本地 **Claude Code** 上、面向 **AI/ML/DL 研究者与研究团队** 的科研操作系统。

它的目标不是把研究者排除出流程，也不是把一切都压缩成一次性的 prompt 调用。  
Noesis 更接近一套长期可运营的方法论框架：

- 让知识积累成为系统资产，而不是聊天记录
- 让研究推进成为可审查、可恢复、可复盘的过程
- 让每个项目结束后沉淀出可回流的经验，而不是只留下零散文件

Noesis 的基本立场很明确：

**研究者负责方向判断与关键取舍，Agents 负责高强度执行与结构化劳动。**

---

## 2. Noesis 选择的路线

同类科研辅助系统大致在朝两类方向发展：

- **自治优先**：尽可能把端到端科研闭环交给 AI 自动完成
- **广覆盖优先**：用大量 skills、commands、hooks 覆盖更多研究与开发场景

Noesis 选择的是第三条路线：

**监督优先、知识优先、复利优先。**

这意味着 Noesis 的核心卖点不是“最像一个自主科研组织”，而是：

- 更像一个**长期可运营的研究系统**
- 更适合**对研究结果负责任的人**来使用
- 更适合**个人或团队跨项目积累能力**

---

## 3. 系统总览

Noesis 由两个**彼此独立**、但通过知识库相连的子系统组成。

```text
Logos  ─────────────→  Episteme  ─────────────→  Praxis
知识积累                    知识库                    研究执行

/logos-discover           Methods Bank            /praxis-start
/logos-read               Gaps & Assumptions      /praxis-research
                          Experimental Patterns   /praxis-paper
                          Reusable Resources      /praxis-evolve
                                                   /praxis-present
                                                   /praxis-assimilate
```

### 3.1 四个核心概念

| 概念 | 角色 | 职责 |
|------|------|------|
| **Noesis** | 顶层方法论框架 | 统一命令接口、流程约束、状态机、经验回流机制 |
| **Logos** | 知识积累子系统 | 发现论文、深度阅读、提取结构化知识资产 |
| **Episteme** | 外部知识库 | 存放阅读队列、论文笔记、领域地图与知识索引 |
| **Praxis** | 研究执行子系统 | 管理项目从立项到论文写作再到复盘演化的生命周期 |

### 3.2 为什么要拆成两个子系统

Noesis 不把“读论文”和“做项目”混成一个大流程，原因很简单：

- **知识积累** 是长期循环，没有固定终点
- **项目推进** 是阶段性工作，有明确的状态和出口

因此：

- `Logos` 负责持续积累
- `Praxis` 负责阶段推进
- `Episteme` 负责把前者的产出转化为后者可消费的研究资产

这使 Noesis 的整体形态更像一个闭环：

**知识 → 判断 → 行动 → 经验回流 → 更好的知识与判断**

---

## 4. 环境与目录约定

Noesis 当前面向 **本地 macOS + Claude Code + GitHub** 的工作流设计。

### 4.1 推荐目录布局

```text
~/Research/
├── Noesis/           ← Noesis 系统本体（本仓库）
├── Episteme/         ← 知识库仓库
└── <ProjectName>/    ← 各研究项目，各自独立仓库

~/.noesis/lessons/    ← 跨项目经验教训
```

### 4.2 各路径的含义

| 路径 | 说明 | 同步方式 |
|------|------|---------|
| `~/Research/Noesis` | Noesis 系统根目录 | GitHub |
| `~/Research/Episteme` | Logos 产出的知识库 | GitHub |
| `~/Research/<项目名>` | 具体研究项目目录 | GitHub（每个项目独立仓库） |
| `~/.noesis/lessons/` | 跨项目 lessons | 本地积累 |

### 4.3 环境假设

- 多机协作通过 `git push` / `git pull` 完成
- 所有路径统一使用 `~`，避免硬编码用户名
- I 之后的编码与实验可通过 SSH MCP 在远程 GPU 服务器执行
- Noesis 仓库本身**不是具体项目仓库**，而是中央方法库与执行框架

---

## 5. 快速开始

### 5.1 初始化 Episteme

首次使用时，先初始化知识库目录：

```bash
KB="$HOME/Research/Episteme"
cp "$HOME/Research/Noesis/Logos/templates/kb-index.md" "$KB/"
cp "$HOME/Research/Noesis/Logos/templates/reading-queue.md" "$KB/"
cp "$HOME/Research/Noesis/Logos/templates/research-directions.md" "$KB/"
```

然后编辑：

- `~/Research/Episteme/research-directions.md`

填入：

- 研究方向
- 核心关键词
- 种子论文
- 目标 venue
- 关注作者

### 5.2 建立知识循环

```bash
/logos-discover
/logos-read 5
```

### 5.3 启动一个新项目

```bash
/praxis-start MyResearchProject
/praxis-research ~/Research/MyResearchProject
```

### 5.4 编码完成后进入论文模块

```bash
/praxis-paper ~/Research/MyResearchProject
/praxis-evolve ~/Research/MyResearchProject
```

---

## 6. Logos：持续知识积累子系统

`Logos` 是一个没有终点的循环引擎：

**发现 → 阅读 → 知识沉淀 → 再发现**

### 6.1 Logos 解决什么问题

很多研究系统直接从 idea 开始，但 Noesis 认为真正决定研究上限的往往不是 idea 本身，而是背后的知识密度。

`Logos` 的作用是把“看过很多论文”转换成“拥有一个长期可检索、可组合、可复用的研究知识库”。

### 6.2 命令入口

| 命令 | 作用 |
|------|------|
| `/logos-discover [kb_path]` | 多策略发现论文，更新阅读队列 |
| `/logos-read [参数]` | 深读论文，提取结构化知识资产 |

默认知识库路径为 `~/Research/Episteme`。

### 6.3 `/logos-discover`

`/logos-discover` 会执行 5 种搜索策略：

| 策略 | 说明 |
|------|------|
| **关键词搜索** | arXiv + Semantic Scholar，核心关键词 × 扩展关键词 |
| **引用链追踪** | 种子论文的前向 / 后向引用网络 |
| **作者追踪** | 持续关注目标研究者的最新发表 |
| **Venue 追踪** | 关注目标会议 / 期刊的最新论文 |
| **争议搜索** | negative results / criticism / replication failures |

候选论文会经过 **Quick Scan**，按 4 个维度评分：

| 维度 | 含义 |
|------|------|
| 相关性 | 是否真正属于设定研究方向 |
| 可复用性 | 方法或组件是否适合迁移 |
| 互补性 | 是否填补现有知识库空白 |
| 隐式假设潜力 | 是否存在值得攻击的隐含前提 |

评分之后，系统会更新：

- `reading-queue.md`

并提交知识库变更，便于多机同步。

### 6.4 `/logos-read`

`/logos-read` 支持四种输入：

- 无参数：读取队列最高优先级论文
- 数字：连续深读 N 篇
- arXiv ID：直接读取指定论文
- 标题关键词：在队列中匹配，匹配不到则直接搜索

例如：

```bash
/logos-read
/logos-read 3
/logos-read 2405.12186
```

### 6.5 Logos 提取的 5 类知识资产

| 资产类型 | 说明 |
|----------|------|
| **Methods Bank** | 机制、公式、适用条件、组件可解耦性 |
| **Gaps & Assumptions** | 显式 limitation 与隐式可攻击假设 |
| **Experimental Patterns** | baseline、metric、ablation、数据集与验证逻辑 |
| **Cross-Paper Connections** | 论文之间的互补、矛盾、延伸与组合关系 |
| **Reusable Resources** | 代码、数据集、模型与工程资源 |

### 6.6 Logos 的核心产物

在 `~/Research/Episteme/` 中，Logos 主要维护：

```text
Episteme/
├── research-directions.md
├── reading-queue.md
├── kb-index.md
├── domain-landscape.md
└── [arxiv-id].md
```

其中：

- `reading-queue.md` 由 discover 写入，由 read 消费
- `kb-index.md` 是整个知识库的总入口
- `[arxiv-id].md` 是单篇论文的结构化笔记
- `domain-landscape.md` 在某方向已读论文达到阈值后生成

### 6.7 Logos 如何为 Praxis 供给知识

`Praxis` 不会“直接复用所有阅读笔记”，而是在关键阶段消费特定资产：

| Praxis 阶段 | 消费内容 |
|-------------|----------|
| `C Crystallize` | `Gaps & Assumptions` + `Cross-Paper Connections` |
| `D Joint Design` | `Methods Bank` + `Experimental Patterns` + `Reusable Resources` |

---

## 7. Praxis：研究执行子系统

`Praxis` 将项目推进拆成五大模块：

```text
Startup → Research → Code → Paper → Evolution
```

### 7.1 Praxis 解决什么问题

单纯“让 AI 生成一些研究文档”并不能真正推进项目。  
真正困难的是：

- 在关键节点做判断
- 在失败后回到正确位置
- 在阶段之间保持状态和约束
- 在论文写作时保留对前期研究逻辑的忠实映射

`Praxis` 用状态机、审查门、迭代日志和演化机制来解决这些问题。

### 7.2 命令入口

| 命令 | 作用 |
|------|------|
| `/praxis-start <project_name>` | 交互式立项与项目脚手架创建 |
| `/praxis-research <project_path>` | 自动推进 `C→R`（C→I 自动化，P/E/W 手动） |
| `/praxis-conclude <project_path>` | 实验失败后总结并分层回退 |
| `/praxis-paper <project_path>` | 自动推进 `P1→P7` |
| `/praxis-assimilate <project_path>` | 将现有项目同化进 Noesis |
| `/praxis-present <project_path>` | 生成用于汇报的 `presentation.md` |
| `/praxis-evolve <project_path>` | 提取 lessons 与框架改进 |

---

## 8. Module 1：Startup

命令：

```bash
/praxis-start <project_name>
```

### 8.1 Startup 的作用

Startup 不是单纯“创建项目目录”，而是把模糊的研究种子转化为一份可进入自动化研究阶段的、经过压力测试的项目起点。

### 8.2 Startup 的基本流程

1. 收集研究者提供的 idea、论文、笔记或 Episteme 线索
2. 识别研究种子类型与核心假设
3. 整理背景、SOTA、候选 gap 与技术风险
4. 进行 **六维辩论压力测试**
5. 与研究者确认方向是否成立
6. 生成 `project-startup.md`
7. 初始化项目目录、Git 与研究状态

### 8.3 六维辩论角色

Startup 并行调用 6 个辩论 Agent：

- Innovator
- Pragmatist
- Theorist
- Contrarian
- Interdisciplinary
- Empiricist

然后再由综合者输出判定：

- 方向确认
- 方向强化
- 方向修正
- HIGH RISK

### 8.4 Startup 结束后项目中会出现什么

至少包括：

- `CLAUDE.md`
- `project-startup.md`
- `pipeline-status.json`
- `phase-outcomes/`
- `pipeline-evolution-log.md`

并将主研究状态设置为 `C`。

---

## 9. Module 2：Research

命令：

```bash
/praxis-research <project_path>
```

Research 模块由：

- `research_state_machine.py`
- `research_runner.py`

共同驱动。

### 9.1 研究阶段总览

| Phase | 内容 | Tier | Codex | 主要出口 |
|------|------|------|-------|----------|
| `C` | Crystallize（问题锐化） | heavy | — | `done → RS` |
| `RS` | Strategic Review（战略审查）🔒 | heavy | ✓ | `pass / revise / abandon` |
| `P` | Probe（探针实验）🔧 | — | — | `signal / pivot / abandon` |
| `D` | Joint Design（联合设计） | heavy | — | `done → RT` |
| `RT` | Technical Review（技术审查）🔒 | heavy | ✓ | `pass / revise / fundamental / abandon` |
| `I` | Implementation（实现规划） | standard | — | `done → E` |
| `E` | Execution（实验执行）🔧 | — | — | `success / iterate_method / iterate_direction / abandon` |
| `W` | Paper Writing（论文写作）🔧 | — | — | `done → R` |
| `R` | Retrospective（知识回收） | heavy | — | `done → complete` |

### 9.2 每个阶段在做什么

| 阶段 | 核心输出 |
|------|----------|
| `C` | `research/problem-statement.md`（Gap + 攻击角度 + 探针方案） |
| `RS` | `inner-reviews/strategic-review.md` + 路由决策 |
| `P` | `research/probe-results.md`（手动） |
| `D` | `research/method-design.md` + `research/experiment-design.md`（交叉引用） |
| `RT` | `inner-reviews/technical-review.md` + 路由决策 |
| `I` | `Codes/code-todo.md` + `Codes/experiment-todo.md` |
| `E` | `research/result.md`（手动） |
| `W` | 独立论文 pipeline（`/praxis-paper`） |
| `R` | `research/retrospective.md` |

### 9.3 Research 模块的几个关键特征

#### 1. 决策性质驱动的阶段拆分

v2 按**决策性质**而非文档类型组织阶段：

- **C（Crystallize）**：战略决策 — Gap、攻击角度、探针方案三者循环耦合，必须同时设计
- **D（Joint Design）**：技术决策 — 方法与实验同步设计，通过交叉引用保持对齐

#### 2. 探针实验前置经验信号

P 阶段在战略审查通过后、联合设计前执行。用最小成本验证核心直觉是否有经验信号。
这避免了走完完整设计后才发现核心假设不成立的高成本返工。

#### 3. 两种差异化审查

- **RS（战略审查）**：4 个 debater（Contrarian, Comparativist, Pragmatist, Interdisciplinary），回答"方向对不对"
- **RT（技术审查）**：6 个 debater（Theorist, Methodologist, Empiricist, Skeptic, Pragmatist, Contrarian），回答"做法对不对"

#### 4. 分层回退

v2 不再统一回退到起点，而是按失败根因层次回退：

- 方法层问题 → 回退到 D（保留 problem-statement.md）
- 方向层问题 → 回退到 C（重新审视 Gap 和攻击角度）
- 迭代守卫：D 回退 ≥ 2 次强制升级到 C；C 回退 ≥ 3 次触发 abandon 评估

#### 5. 6 种迭代上下文模式

Runner 根据转换来源自动注入上下文（`first / rs_revise / probe_pivot / rt_revise / execute_iterate / execute_pivot`），
让 Agent 精确知道为什么回到当前阶段、应该修改什么、应该避免什么。

Codex 并行审查是 **non-blocking** 的：
MCP 不可用时不会阻塞主流程，结果仅写入 `codex-reviews/` 供参考。

### 9.4 R（Retrospective）的位置

`R Retrospective` 发生在：

**W（论文写作）完成之后，或 abandon 时**

它是流程末尾的知识回收阶段。因为此时已有完整实验结果，可以基于实际验证标记知识资产为 `[✓ validated]` / `[✗ refuted]` / `[~ partially validated]`。

---

## 10. 手动阶段：P / E / W

研究流程中有三个手动阶段，不由状态机自动完成。

### 10.1 P（探针实验）

进入条件：RS 战略审查通过。

- 参考 `research/problem-statement.md` §3 探针方案
- 将结果写入 `research/probe-results.md`
- 通过 `advance --outcome signal/pivot/abandon` 推进

### 10.2 E（实验执行）

进入条件：I 实现规划完成。

参考 `Codes/code-todo.md` 与 `Codes/experiment-todo.md` 进行编码与实验。

#### 情况 A：验证成功

通过 `advance --outcome success` 进入 W（论文写作）。

#### 情况 B：验证失败

运行：

```bash
/praxis-conclude <project_path>
```

`/praxis-conclude` 会：

- 诊断失败层次（执行层 / 方法层 / 方向层）
- 追加 `iteration-log.md` + 更新 `research/result.md`
- 按层次分层回退

失败层次与回退关系：

| 失败层次 | 含义 | 回退位置 |
|----------|------|----------|
| 执行层 | 调参/bug，不需要改方法 | 继续在 E |
| 方法层 | 方法组件有问题 | D（联合设计） |
| 方向层 | 攻击角度或 Gap 定义有问题 | C（问题锐化） |

之后重新运行 `/praxis-research <project_path>` 完成热重启。

### 10.3 W（论文写作）

进入条件：E 实验验证成功。

运行 `/praxis-paper <project_path>` 启动独立论文 pipeline。
完成后通过 `advance --outcome done` 进入 R（知识回收）。

---

## 11. Module 4：Paper

命令：

```bash
/praxis-paper <project_path>
```

Paper 模块拥有一套与主研究流程**完全独立**的状态机：

- `paper_state_machine.py`
- `paper_runner.py`

状态文件位于：

- `<project>/Papers/paper-status.json`

### 11.1 论文阶段总览

| Phase | 内容 | Tier | Codex |
|------|------|------|-------|
| `P1` | Outline | heavy | — |
| `P2` | Sections | standard | — |
| `P3` | Critique | heavy | ✓ |
| `P4` | Integrate | standard | — |
| `P5` | Final Review | heavy | — |
| `P6` | LaTeX | standard | — |
| `P7` | Project Review | heavy | ✓ |

### 11.2 各阶段的典型产物

| 阶段 | 典型产物 |
|------|----------|
| `P1` | `Papers/outline.md`, `Papers/notation.md` |
| `P2` | `Papers/sections/*.md` |
| `P3` | 多角色 critique + 可选 Codex 审查 |
| `P4` | `Papers/paper.md` |
| `P5` | 终审评分与 revise/pass 决策 |
| `P6` | `Papers/latex/main.tex`, `references.bib`, 可选 `main.pdf` |
| `P7` | `Papers/project-review/*.md`, `synthesis.md` |

### 11.3 Paper 模块的关键机制

#### 1. 它不是“直接生成整篇论文”

Noesis 先用 `P1` 建立叙事脊柱和符号表，再用 `P2` 分章节写作，之后通过 `P3-P5` 做真正的质量控制。

#### 2. 它带有修订循环

`P5 Final Review` 的结果如果低于阈值，会回到 `P4`。  
当前实现最多允许 2 轮修订，超限后强制通过，以避免无休止循环。

#### 3. 它忠实映射研究文档，而不是重新发明项目

Paper 阶段的基本原则是：

- 从 `research/problem-statement.md`、`research/method-design.md`、`research/experiment-design.md` 和 `Codes/` 提取素材
- 保持 `Gap → 根因 → 方法 → 验证 → 贡献` 的叙事一致性
- 不在论文阶段凭空发明研究贡献

---

## 12. Module 5：Evolution

命令：

```bash
/praxis-evolve <project_path>
```

`/praxis-evolve` 的作用不是再写一份总结，而是提取两类真正会影响后续系统行为的结果。

### 12.1 产物一：跨项目 lessons

写入：

- `~/.noesis/lessons/<skill_name>.md`

每条 lesson 带有三类标签：

- 类别：`[SYSTEM]`、`[EXPERIMENT]`、`[WRITING]` 等
- 频率：`[RECURRING]`、`[NEW]`
- 有效性：`[✓ verified]`、`[✗ ineffective]`、`[? unverified]`

Runner 会在后续项目的相同阶段自动注入 lessons，并自动过滤：

- `[✗ ineffective]`

### 12.2 产物二：框架自我进化

`/praxis-evolve` 还会读取：

- `pipeline-evolution-log.md`

据此决定是否修改：

- `Praxis/prompts/`
- `Praxis/skills/`
- `Praxis/templates/`

这意味着 Noesis 的进化不只发生在“项目层”，也发生在“框架层”。

---

## 13. 辅助命令

### 13.1 `/praxis-assimilate`

```bash
/praxis-assimilate <project_path>
```

作用：

- 将任意阶段的已有科研项目纳入 Noesis
- 重建缺失的阶段文档
- 补跑关键评审
- 写入 `pipeline-status.json`

适用场景：

- 你已经有一个在研项目，但还没用 Noesis 管理
- 你想让旧项目获得状态机、审查门和演化能力

### 13.2 `/praxis-present`

```bash
/praxis-present <project_path>
```

作用：

- 读取当前项目状态
- 生成适合导师 / 合作者阅读的 `presentation.md`
- 支持热启动，不覆盖已有人工编辑内容

`presentation.md` 的设计目标不是流水线归档，而是：

**服务 15 分钟研究讨论。**

因此它会优先呈现：

- 当前进展
- 关键主张
- Open Questions
- 需要拍板的问题

---

## 14. 两条典型使用路径

### 14.1 从零开始新项目

```bash
# Step 1: 建立知识循环
/logos-discover
/logos-read 5

# Step 2: 启动项目
/praxis-start MyResearchProject

# Step 3: 推进研究阶段
/praxis-research ~/Research/MyResearchProject

# Step 4: 人工编码与实验
# 参考 Codes/code-todo.md 与 Codes/experiment-todo.md

# Step 5a: 成功后进入论文
/praxis-paper ~/Research/MyResearchProject

# Step 6: 项目结束后提取 lessons
/praxis-evolve ~/Research/MyResearchProject
```

### 14.2 接管已有项目

```bash
/praxis-assimilate ~/Research/ExistingProject
```

之后根据同化结果，继续运行：

- `/praxis-research`
- 或 `/praxis-paper`

---

## 15. Orchestrator CLI 参考

除了 slash commands，Praxis 还提供底层 runner CLI，适合调试、恢复和脚本化调用。

### 15.1 研究状态机

```bash
python3 ~/Research/Noesis/Praxis/orchestrator/research_runner.py status  <project_path>
python3 ~/Research/Noesis/Praxis/orchestrator/research_runner.py next    <project_path>
python3 ~/Research/Noesis/Praxis/orchestrator/research_runner.py advance <project_path>
python3 ~/Research/Noesis/Praxis/orchestrator/research_runner.py advance <project_path> --outcome <outcome>
python3 ~/Research/Noesis/Praxis/orchestrator/research_state_machine.py init-phase <project_path> <phase>
```

相关文件：

- 状态：`<project>/pipeline-status.json`
- outcome：`<project>/phase-outcomes/<phase>.json`

### 15.2 论文状态机

```bash
python3 ~/Research/Noesis/Praxis/orchestrator/paper_runner.py status  <project_path>
python3 ~/Research/Noesis/Praxis/orchestrator/paper_runner.py next    <project_path>
python3 ~/Research/Noesis/Praxis/orchestrator/paper_runner.py advance <project_path>
python3 ~/Research/Noesis/Praxis/orchestrator/paper_state_machine.py init-phase <project_path> <phase>
```

相关文件：

- 状态：`<project>/Papers/paper-status.json`
- outcome：`<project>/Papers/phase-outcomes/<phase>.json`

### 15.3 outcome 文件格式

主流程与论文流程的 outcome 文件都采用同一种最小结构：

```json
{
  "outcome": "<outcome_key>",
  "notes": "<1-2 句简短说明>"
}
```

状态机只基于 `outcome` 路由，`notes` 供人类阅读和汇报使用。

---

## 16. 文件结构总览

### 16.1 Noesis 系统仓库

```text
~/Research/Noesis/
├── Logos/
│   ├── CLAUDE.md
│   ├── skills/
│   └── templates/
├── Praxis/
│   ├── CLAUDE.md
│   ├── orchestrator/
│   ├── prompts/
│   ├── skills/
│   ├── subagents/
│   └── templates/
├── .claude/skills/
├── README.md
├── introduction.md
└── CLAUDE.md
```

### 16.2 单个研究项目

```text
~/Research/<ProjectName>/
├── CLAUDE.md
├── pipeline-status.json
├── project-startup.md
├── research/
│   ├── problem-statement.md
│   ├── probe-results.md
│   ├── method-design.md
│   ├── experiment-design.md
│   ├── contribution.md
│   ├── result.md
│   └── retrospective.md
├── inner-reviews/
│   ├── strategic-review.md
│   └── technical-review.md
├── iteration-log.md
├── pipeline-evolution-log.md
├── phase-outcomes/
├── codex-reviews/
├── Codes/
│   ├── code-todo.md
│   └── experiment-todo.md
└── Papers/
    ├── paper-status.json
    ├── outline.md
    ├── notation.md
    ├── paper.md
    ├── sections/
    ├── phase-outcomes/
    ├── codex-reviews/
    ├── project-review/
    └── latex/
```

### 16.3 Episteme 知识库

```text
~/Research/Episteme/
├── research-directions.md
├── reading-queue.md
├── kb-index.md
├── domain-landscape.md
└── [arxiv-id].md
```

---

## 17. 关键架构原则

### 17.1 两个独立子系统

`Logos` 与 `Praxis` 在运行时没有直接耦合。  
唯一连接点是 `Episteme` 知识库。

### 17.2 双状态机

Noesis 不把研究和论文写作混在一套状态里。

- 主流程状态机：研究阶段
- 论文状态机：写作阶段

这让两者可以独立恢复、独立迭代。

### 17.3 单一事实源

项目当前状态只以两个文件为准：

- `pipeline-status.json`
- `Papers/paper-status.json`

Noesis 不通过“扫描目录结构猜测状态”来决定流程位置。

### 17.4 Prompt / Runner / State Machine 三层分离

`Praxis` 的内部结构遵循明确的职责分离：

| 层级 | 职责 |
|------|------|
| `runner.py` | 决定下一步动作、拼装 fork prompt、注入 lessons |
| `prompts/*.md` | 纯 Agent 指令，不负责状态推进 |
| `state_machine.py` | 纯状态转换与 I/O，不负责 prompt 逻辑 |

### 17.5 独立审查隔离

以下阶段都在上下文隔离的独立审查中完成：

- `RS / RT`
- `P3 / P5 / P7`

它的目的不是增加复杂度，而是降低确认偏误。

### 17.6 lessons 自动注入

Runner 会读取：

- `~/.noesis/lessons/<skill_name>.md`

将有效经验自动注入后续同类阶段。  
这使 Noesis 具备真正的跨项目复利，而不是每个项目都从零开始。

### 17.7 X-reflect 自动积累

每个非 manual 阶段完成后，runner 会自动注入：

- `X-reflect-pipeline-prompt.md`

Agent 会把对流程本身的观察追加到：

- `pipeline-evolution-log.md`

随后由 `/praxis-evolve` 决定是否把这些观察转化为框架升级。

---

## 18. 谁适合使用 Noesis

Noesis 尤其适合：

- 需要长期维护知识库的博士生与独立研究者
- 需要让研究项目更制度化、更可追踪的实验室
- 希望把 AI 从“对话助手”升级为“研究系统”的个人或团队
- 已经有多个项目并行，希望跨项目积累研究经验的人

如果你要的是“一次性写一份文档”，Noesis 可能偏重。  
如果你关心的是**研究能力如何持续复利**，它就是为这个问题设计的。

---

## 19. 进一步阅读

- 产品化总览见 [README.md](README.md)
- 系统内部开发约定见 [CLAUDE.md](CLAUDE.md)
- Logos 子系统约定见 `Logos/CLAUDE.md`
- Praxis 子系统约定见 `Praxis/CLAUDE.md`
