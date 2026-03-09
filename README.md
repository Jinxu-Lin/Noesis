# Noesis: AI-Agent 自动科研系统

> νόησις (noesis) — 希腊语，意为"认知"与"洞察"

## 愿景

将 AI/ML/DL 方向的科研全流程自动化。研究者作为"产品经理"定义方向与判断，AI Agent 作为"工程团队"执行搜索、分析、设计、实现与写作。

## 核心理念

- 论文 = 产品，研究者 = PM，AI Agent = 可调度的工程团队
- 科研流程 = 产品开发生命周期，可被结构化和自动化
- 知识积累与研究执行解耦，两个子系统**完全独立**运行、通过知识库连接

## 系统架构

```
                    Noesis
                   ╱      ╲
             Logos           Praxis
          (知识积累)        (研究执行)
              │                 │
         论文发现/阅读      P1→P11 Pipeline
              │                 │
              └── LogosBase ────┘
                  (知识库产出)
```

### Logos — 持续知识积累

独立于研究流程的**知识引擎**，负责持续扩充领域知识库：

- **论文发现** — arXiv / Semantic Scholar 多策略搜索，按相关性评分，维护阅读队列
- **深度阅读** — 提取五类知识资产（Methods Bank、Gaps、Experimental Patterns 等）
- **知识沉淀** — 结构化索引，供 Praxis 在研究阶段消费

命令：`/paper-reading-discover`、`/paper-reading-read`

### Praxis — 自动化研究执行

结构化 **12 阶段研究 Pipeline**，由 Python 状态机驱动：

| 阶段 | 内容 | 类型 |
|------|------|------|
| P1 | 项目启动 | work |
| P2 | Gap 发现 | work |
| P3 | Gap 评审 | review 🔒 |
| P4 | 方法设计 | work |
| P5 | 方法评审 | review 🔒 |
| P6 | 实验设计 | work |
| P7 | 实验评审 | review 🔒 |
| P8a/b | 实现（环境→验证→全量） | work ⏸ |
| P9 | 论文写作 | work |
| P11 | 回顾与知识提炼 | work |

命令：`/researchflow-run`、`/researchflow-status`、`/researchflow-goto`、`/researchflow-evolve`

## 环境

所有内容存放于 `~/Documents/`，通过 GitHub 跨 Mac 同步：

```
~/Documents/
├── Noesis/                        ← 系统本身（GitHub 同步）
│   ├── Logos/                     ← 知识积累子系统
│   │   ├── skills/                ← 论文发现与阅读 skill
│   │   └── templates/             ← 知识库模板
│   ├── Praxis/                    ← 研究执行子系统
│   │   ├── orchestrator/          ← Python 状态机 + runner
│   │   ├── skills/                ← P1-P11 各阶段 skill
│   │   ├── subagents/             ← SubAgent 提示词模板
│   │   └── templates/             ← 研究项目文档模板
│   ├── .claude/skills/            ← Slash commands 注册
│   ├── pipeline.md                ← 方法论主文档
│   └── CLAUDE.md                  ← Claude Code 项目指令
│
├── LogosBase/                     ← 知识库产出（独立 GitHub 仓库）
│   ├── research-directions.md     ← 研究方向配置
│   ├── reading-queue.md           ← 阅读队列
│   ├── kb-index.md                ← 知识库总索引
│   └── [arxiv-id].md              ← 论文笔记
│
└── <项目名>/                      ← 各研究项目（各自独立 GitHub 仓库）
    ├── CLAUDE.md                  ← 项目入口（含 noesis_path）
    ├── pipeline-status.json       ← Pipeline 状态
    ├── phase-outcomes/            ← 各阶段产出
    ├── Code/                      ← 代码（P8 阶段）
    └── Papers/                    ← 论文（P9 阶段）
```

**多机协作**：两台 Mac 通过 `git push` / `git pull` 同步。P8 阶段实验通过 SSH MCP 在远程 GPU 服务器执行。

## 快速开始

### 1. 积累知识（Logos）

```bash
# 初始化知识库（首次）
cp ~/Documents/Noesis/Logos/templates/*.md ~/Documents/LogosBase/

# 编辑研究方向
# 打开 LogosBase/research-directions.md 填入关键词、种子论文等

# 发现论文（在 Noesis 目录下使用 Claude Code）
/paper-reading-discover

# 深度阅读
/paper-reading-read
```

### 2. 启动研究（Praxis）

```bash
# 查看项目状态
/researchflow-status <project_path>

# 运行自动化 pipeline
/researchflow-run <project_path>
```

## 状态

正在积极开发中。基于真实 AI/ML 科研项目经验持续迭代。
