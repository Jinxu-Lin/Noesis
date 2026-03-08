# PaperReading 子系统

> 独立于 ResearchFlow 研究流程的**持续知识积累系统**。在项目启动之前、期间和之后均可独立运行。

---

## 这是什么

PaperReading 是 ResearchFlow 生态的前置子系统，负责持续扩充**领域知识库 (Knowledge Base)**，为未来的研究项目提供知识储备。

与 ResearchFlow（P1-P11 线性研究流程）不同，PaperReading **没有固定的起止点**——它是一个循环运行的知识积累引擎。

---

## 两个子系统的关系

```
PaperReading（知识积累）
    │
    ├── 论文发现 (/paper-reading:discover)
    │       ↓
    ├── 深度阅读 (/paper-reading:read)
    │       ↓
    └── 知识库 (kb/)
            │
            ↓  知识注入
    ResearchFlow（研究执行）
    P1 → P2 → P3 → P4 → P5 → P6 → P7 → P8 → P9 → P11
```

- **Phase 2 (Gap Discovery)** 从知识库的 Gaps & Assumptions 中提取研究空白
- **Phase 4 (Method Design)** 从知识库的 Methods Bank 中寻找可复用组件
- **Phase 6 (Experiment Design)** 从知识库的 Experimental Patterns 中借鉴设计模式

---

## 子系统文件结构

```
paper-reading/
├── OVERVIEW.md              ← 本文件
├── skills/
│   ├── paper-discovery-skill.md   ← 论文发现与筛选
│   └── paper-reading-skill.md     ← 深度阅读与知识沉淀
└── templates/
    ├── research-directions.md     ← 研究方向配置（搜索参数）
    ├── reading-queue.md           ← 论文阅读队列
    ├── kb-index.md                ← 知识库总索引
    └── paper-reading-note.md      ← 单篇论文笔记模板
```

**知识库目录结构**（在具体项目或共享知识库目录中）：

```
kb/
├── kb-index.md              ← 从 templates/ 初始化
├── reading-queue.md         ← 从 templates/ 初始化
├── research-directions.md   ← 从 templates/ 初始化
└── [arxiv-id].md            ← 每篇论文的笔记（由 /paper-reading:read 生成）
```

---

## 快速开始

### 1. 初始化知识库

在你的项目目录或共享知识库目录中，复制模板文件：

```bash
KB_DIR=/path/to/your/kb
mkdir -p $KB_DIR
cp /home/jinxulin/ResearchFlow/paper-reading/templates/kb-index.md $KB_DIR/
cp /home/jinxulin/ResearchFlow/paper-reading/templates/reading-queue.md $KB_DIR/
cp /home/jinxulin/ResearchFlow/paper-reading/templates/research-directions.md $KB_DIR/
```

### 2. 配置研究方向

编辑 `kb/research-directions.md`，填入：
- 核心关键词 / 扩展关键词
- 种子论文（用于引用链追踪）
- 目标 Venue 列表
- 关注作者

### 3. 发现论文

```
/paper-reading:discover <kb_path>
```

自动搜索 arXiv、Semantic Scholar，按相关性评分，更新 `reading-queue.md`。

### 4. 深度阅读

```
/paper-reading:read <kb_path>
```

对 `reading-queue.md` 中的高优先论文进行深度阅读，提取五类知识资产，更新 `kb-index.md`。

---

## Plugin 命令

在 `~/.claude/settings.json` 中启用 plugin 后可用：

```json
{ "pluginDirs": ["/home/jinxulin/ResearchFlow/plugin"] }
```

| 命令 | 说明 |
|------|------|
| `/paper-reading:discover <kb_path>` | 论文发现：搜索、评分、更新阅读队列 |
| `/paper-reading:read <kb_path>` | 深度阅读：阅读论文、提取知识资产、更新知识库 |

---

## 共用工具

`/reflect-pipeline`（位于 `ResearchFlow/skills/reflect-pipeline-skill.md`）由两个子系统共享。每个阶段完成后调用，将流程反思追加到 `pipeline-evolution-log.md`。
