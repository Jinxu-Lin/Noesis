# CLAUDE.md — Logos 子系统

This file provides guidance to Claude Code when working within the Logos subsystem.

## What Logos Is

Logos 是 Noesis 的**知识积累子系统**，独立于 Praxis 运行。它是一个循环运行的知识引擎，没有固定的起止点。

核心循环：**发现 (Discover) → 阅读 (Read) → 知识沉淀 → 重复**

## Paths

| 路径 | 说明 |
|------|------|
| Logos 系统 | `~/Documents/Noesis/Logos` |
| 知识库产出 (LogosBase) | `~/Documents/LogosBase` |
| Noesis 根目录 | `~/Documents/Noesis` |

系统代码与知识库产出**分离存放**。两者均通过 GitHub 跨 Mac 同步。

## Skills (model: sonnet)

| 命令 | 说明 |
|------|------|
| `/paper-reading-discover [kb_path]` | 论文发现：多策略搜索、评分、更新阅读队列 |
| `/paper-reading-read [kb_path]` | 深度阅读：阅读论文、提取知识资产、更新知识库 |

`kb_path` 可省略，默认为 LogosBase 路径。

Skill 定义位于项目根目录 `.claude/skills/paper-reading-discover/` 和 `.claude/skills/paper-reading-read/`，均设置 `model: sonnet` 强制使用 Sonnet 模型。

## File Layout

```
Logos/
├── CLAUDE.md                        ← 本文件
├── OVERVIEW.md                      ← 子系统详细说明与快速开始
├── skills/
│   ├── paper-discovery-skill.md     ← 论文发现：5 种搜索策略 + Quick Scan 评分
│   └── paper-reading-skill.md       ← 深度阅读：5 类知识资产提取
├── templates/
│   ├── research-directions.md       ← 研究方向配置（关键词、种子论文、venue）
│   ├── reading-queue.md             ← 阅读队列（discover 写入，read 消费）
│   ├── kb-index.md                  ← 知识库总索引（所有资产的汇总入口）
│   └── paper-reading-note.md        ← 单篇论文笔记模板
└── (skills & templates only — slash commands in .claude/skills/)
```

## Knowledge Base (LogosBase) Structure

```
LogosBase/
├── research-directions.md   ← 研究方向配置（从 templates/ 初始化后由用户编辑）
├── reading-queue.md         ← 阅读队列（discover 自动维护）
├── kb-index.md              ← 知识库总索引（read 自动更新）
├── domain-landscape.md      ← 领域地图（某方向已读 ≥ 5 篇后自动生成）
└── [arxiv-id].md            ← 每篇论文的结构化笔记
```

## Discovery Workflow (paper-discovery-skill.md)

5 种搜索策略：
- **A. 关键词搜索** — arXiv API + Semantic Scholar API
- **B. 引用链追踪** — 种子论文的前向/后向引用
- **C. 作者追踪** — 关注作者最新发表
- **D. Venue 追踪** — 目标会议最新论文
- **E. 争议搜索** — negative results / criticism / replication failures

搜索后执行 Quick Scan（title + abstract + conclusion），按 4 维度评分（相关性、可复用性、互补性、隐式假设潜力），≥ 3 分进入 `reading-queue.md`。

## Reading Workflow (paper-reading-skill.md)

提取 5 类知识资产：
- **Methods Bank** — 方法机制、公式、适用条件、组件可解耦性
- **Gaps & Assumptions** — 显式 limitation + 隐式可质疑假设（最高价值）
- **Experimental Patterns** — baselines、metrics、消融策略、数据集
- **Cross-Paper Connections** — 与已有论文的互补/矛盾/可结合关系
- **Reusable Resources** — GitHub 代码、数据集、预训练模型

完成后更新 `kb-index.md`、`reading-queue.md`，当某方向已读 ≥ 5 篇时自动生成 `domain-landscape.md`。

## Key Behaviors

- Agent 不只是记录员，而是**共同思考者**——主动识别隐式假设和 cross-paper connections
- 隐式假设识别是核心差异化价值：重点标注"作者没意识到但可以被质疑"的假设
- 随着 KB 增长，cross-paper connections 涌现概率指数增长——每次深读都要与整个 KB 对照
- 每次 discover/read 完成后 git commit KB 变更
- 完成后提示用户下一步操作，并执行 `/reflect-pipeline` 进行流程反思

## Downstream Consumers (Praxis)

Logos 产出的知识库被 Praxis 在以下阶段消费：
- **P2 Gap Discovery** ← Gaps & Assumptions
- **P4 Method Design** ← Methods Bank
- **P6 Experiment Design** ← Experimental Patterns + Reusable Resources
