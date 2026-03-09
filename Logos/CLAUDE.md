# CLAUDE.md — Logos 子系统

This file provides guidance to Claude Code when working within the Logos subsystem.

## What Logos Is

Logos 是 Noesis 的**知识积累子系统**，独立于 Praxis 运行。它是一个循环运行的知识引擎，没有固定的起止点。

核心循环：**发现 (Discover) → 阅读 (Read) → 知识沉淀 → 重复**

```
Logos（知识积累）
    │
    ├── 论文发现 (/logos-discover)
    │       ↓
    ├── 深度阅读 (/logos-read)
    │       ↓
    └── Episteme 知识库 (~/Documents/Episteme)
            │
            ↓  知识注入
    Praxis（研究执行）
    R1 → R2 → R3 → R4 → R5 → R6 → R7 → R8 → coding → R11
                （独立）P1 → P2 → P3 → P4 → P5 → P6 → P7
```

Logos 产出的知识库被 Praxis 在以下阶段消费：
- **R2 Gap Discovery** ← Gaps & Assumptions
- **R4 Method Design** ← Methods Bank
- **R6 Experiment Design** ← Experimental Patterns + Reusable Resources

## Paths

| 路径 | 说明 |
|------|------|
| Logos 系统 | `~/Documents/Noesis/Logos` |
| 知识库产出 (Episteme) | `~/Documents/Episteme` |
| Noesis 根目录 | `~/Documents/Noesis` |

系统代码与知识库产出**分离存放**。两者均通过 GitHub 跨 Mac 同步。

## Quick Start

### 1. 初始化知识库

```bash
KB_DIR="$HOME/Documents/Episteme"
LOGOS="$HOME/Documents/Noesis/Logos"
cp "$LOGOS/templates/kb-index.md" "$KB_DIR/"
cp "$LOGOS/templates/reading-queue.md" "$KB_DIR/"
cp "$LOGOS/templates/research-directions.md" "$KB_DIR/"
```

### 2. 配置研究方向

编辑 `Episteme/research-directions.md`，填入核心关键词、种子论文、目标 Venue、关注作者。

### 3. 运行

```
/logos-discover    ← 论文发现（可省略 kb_path，默认 Episteme）
/logos-read        ← 深度阅读（可省略参数，默认读队列第 1 篇）
```

## Skills (model: sonnet)

| 命令 | 说明 |
|------|------|
| `/logos-discover [kb_path]` | 论文发现：多策略搜索、评分、更新阅读队列 |
| `/logos-read [参数]` | 深度阅读：阅读论文、提取知识资产、更新知识库 |

`kb_path` 可省略，默认为 `~/Documents/Episteme`。

`/logos-read` 参数说明：
- 无参数：从阅读队列读取 1 篇最高优先级论文
- 数字（如 `5`）：从阅读队列依次读取 N 篇
- arXiv ID（如 `2405.12186`）：直接阅读指定论文，跳过队列
- 论文标题关键词：在队列中匹配，匹配不到则直接搜索

Skill 定义位于项目根目录 `.claude/skills/logos-discover/` 和 `.claude/skills/logos-read/`，均通过 frontmatter 设置 `model: sonnet` 强制使用 Sonnet 模型。

## File Layout

```
Logos/
├── CLAUDE.md                        ← 本文件
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

## Knowledge Base (Episteme) Structure

```
Episteme/
├── research-directions.md   ← 研究方向配置（从 templates/ 初始化后由用户编辑）
├── reading-queue.md         ← 阅读队列（discover 自动维护）
├── kb-index.md              ← 知识库总索引（read 自动更新）
├── domain-landscape.md      ← 领域地图（某方向已读 ≥ 5 篇后自动生成）
└── [arxiv-id].md            ← 每篇论文的结构化笔记
```

## Discovery Workflow (paper-discovery-skill.md)

5 种搜索策略：
- **A. 关键词搜索** — arXiv API + Semantic Scholar API，核心关键词 × 扩展关键词
- **B. 引用链追踪** — 种子论文的前向/后向引用（首次执行或有新种子论文时）
- **C. 作者追踪** — 关注作者最新发表
- **D. Venue 追踪** — 目标会议最新论文
- **E. 争议搜索** — negative results / criticism / replication failures（每个研究方向至少一次）

搜索后执行 Quick Scan（title + abstract + conclusion），按 4 维度评分（相关性、可复用性、互补性、隐式假设潜力）：
- **综合评分 ≥ 4**：高优先级加入深读队列
- **综合评分 = 3**：普通优先级加入深读队列
- **综合评分 ≤ 2**：跳过，仅记录 metadata

完成后 git commit + push `reading-queue.md`。

## Reading Workflow (paper-reading-skill.md)

提取 5 类知识资产：
- **Methods Bank** — 方法机制、公式、适用条件、组件可解耦性
- **Gaps & Assumptions** — 显式 limitation + 隐式可质疑假设（最高价值，含可攻击性评估）
- **Experimental Patterns** — baselines、metrics、消融策略、数据集
- **Cross-Paper Connections** — 与已有论文的互补/矛盾/可结合关系（对照整个 KB 建立）
- **Reusable Resources** — GitHub 代码、数据集、预训练模型（为 R8 实现阶段提供工程起点）

完整流程：
1. git pull KB → 重复检查 → 预读准备
2. 论文级深度理解（storyline、gap、方法、实验、结论）
3. 提取 5 类知识资产
4. 生成论文笔记（按 `templates/paper-reading-note.md` 模板）
5. 更新 `kb-index.md`（已读论文 + 各类资产索引）
6. 更新 `reading-queue.md`（状态改为"已完成"）
7. **条件触发**：该方向已读 ≥ 5 篇时，生成或更新 `domain-landscape.md`
8. git commit + push KB 更新
9. 与研究者交互，主动提示高价值 connections 和 gaps

## Key Behaviors

- Agent 不只是记录员，而是**共同思考者**——主动识别隐式假设和 cross-paper connections
- 隐式假设识别是核心差异化价值：重点标注"作者没意识到但可以被质疑"的假设
- 随着 KB 增长，cross-paper connections 涌现概率指数增长——每次深读都要与整个 KB 对照
- 对 Methods Bank 的条目，要分析到组件级别（可解耦性分析），不只是笼统记录
- 每次 discover/read 完成后 git commit + push KB 变更（多机同步）
- 完成后提示用户下一步操作（读了 discover → 建议 read；读了 read → 如队列有余则继续）
