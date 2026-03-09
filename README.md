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
         论文发现/阅读      R1→R8 研究循环
              │            P1→P7 论文写作
              └── Episteme ────┘
                  (知识库)
```

### Logos — 持续知识积累

独立于研究流程的**循环知识引擎**：

- **论文发现** (`/logos-discover`) — arXiv / Semantic Scholar 5 种搜索策略 + Quick Scan 评分，维护阅读队列
- **深度阅读** (`/logos-read`) — 提取 5 类知识资产（Methods Bank、Gaps & Assumptions、Experimental Patterns、Cross-Paper Connections、Reusable Resources），生成论文笔记，条件触发领域地图生成

### Praxis — 自动化研究执行

五大模块，由 Python 状态机驱动：

| 模块 | 内容 | 命令 |
|------|------|------|
| **Startup** | 交互式项目孵化（六维辩论压力测试）| `/praxis-start` |
| **Research** | R1→R8 自动化研究循环 | `/praxis-research` |
| **Code** | 人工编码 & 实验 | `/praxis-conclude`（失败重启） |
| **Paper** | P1→P7 自动化论文写作 | `/praxis-paper` |
| **Evolution** | 提取跨项目经验，进化框架 | `/praxis-evolve` |

**Research 模块**（3 轮独立审查 + 可选 Codex 并行）：

```
R1 Gap Discovery → R2 审查🔒 → R3 Method Design → R4 审查🔒
→ R5 Experiment Design → R6 审查🔒 → R7 Impl Planning → R8 Retrospective
```

**Paper 模块**（独立状态机）：

```
P1 Outline → P2 Sections → P3 Critique🔒 → P4 Integrate → P5 Final Review🔒 → P6 LaTeX → P7 Project Review🔒
```

其他命令：`/praxis-assimilate`（同化外部项目）、`/praxis-present`（生成进展演示）

## 快速开始

### 1. 积累知识（Logos）

```bash
# 初始化知识库（首次）
KB="$HOME/Documents/Episteme"
cp ~/Documents/Noesis/Logos/templates/kb-index.md $KB/
cp ~/Documents/Noesis/Logos/templates/reading-queue.md $KB/
cp ~/Documents/Noesis/Logos/templates/research-directions.md $KB/
# 编辑 Episteme/research-directions.md

/logos-discover      # 发现论文，更新阅读队列
/logos-read 5        # 深度阅读 5 篇
```

### 2. 启动与执行研究（Praxis）

```bash
/praxis-start MyProject           # 交互式项目孵化
/praxis-research ~/Documents/MyProject   # R1→R8 自动化

# 人工编码实验...

/praxis-paper ~/Documents/MyProject      # P1→P7 论文写作
/praxis-evolve ~/Documents/MyProject     # 提取跨项目经验
```

### 编码失败时热重启

```bash
/praxis-conclude ~/Documents/MyProject   # 分析失败，写入 iteration-log
/praxis-research ~/Documents/MyProject   # 热重启，自动跳过已排除方向
```

### 同化已有项目

```bash
/praxis-assimilate ~/Documents/ExistingProject
# 重建阶段文档 + 运行真实 R2/R4/R6 评审，使其可被 /praxis-research 或 /praxis-paper 接管
```

### 生成进展演示

```bash
/praxis-present ~/Documents/MyProject
# 生成 presentation.md，用于与导师/合作者的进展汇报
# 支持热启动：已有 presentation.md 时增量更新，保留人工编辑
```

## 环境

```
~/Documents/
├── Noesis/          ← 系统本身（GitHub 同步）
├── Episteme/        ← 知识库（独立 GitHub 仓库）
└── <项目名>/        ← 各研究项目（各自独立 GitHub 仓库）

~/.noesis/lessons/   ← 跨项目经验教训（本地积累）
```

多机协作（Mac Mini + MacBook）通过 git 同步。R7 后的实验通过 SSH MCP 在远程 GPU 服务器执行。

## 文档

详细使用说明见 [introduction.md](introduction.md)。
