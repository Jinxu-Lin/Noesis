# Logos 子系统

> 独立于 Praxis 研究流程的**持续知识积累系统**。在项目启动之前、期间和之后均可独立运行。

---

## 这是什么

Logos 是 Noesis 生态的知识积累子系统，负责持续扩充**领域知识库 (Knowledge Base)**，为未来的研究项目提供知识储备。

与 Praxis（P1-P11 线性研究流程）不同，Logos **没有固定的起止点**——它是一个循环运行的知识积累引擎。

---

## 两个子系统的关系

```
Logos（知识积累）
    │
    ├── 论文发现 (/paper-reading:discover)
    │       ↓
    ├── 深度阅读 (/paper-reading:read)
    │       ↓
    └── 知识库 (LogosBase/)
            │
            ↓  知识注入
    Praxis（研究执行）
    P1 → P2 → P3 → P4 → P5 → P6 → P7 → P8 → P9 → P11
```

- **Phase 2 (Gap Discovery)** 从知识库的 Gaps & Assumptions 中提取研究空白
- **Phase 4 (Method Design)** 从知识库的 Methods Bank 中寻找可复用组件
- **Phase 6 (Experiment Design)** 从知识库的 Experimental Patterns 中借鉴设计模式

---

## 路径约定

| 路径 | 说明 |
|------|------|
| Noesis 根目录 | `~/Documents/Noesis` |
| Logos 子系统 | `~/Documents/Noesis/Logos/` |
| 知识库产出 (LogosBase) | `~/Documents/LogosBase` |

Logos 系统代码与知识库产出**分离存放**：系统本身在 Noesis 仓库中，产出在 LogosBase 中。两者均通过 GitHub 跨 Mac 同步。

---

## 子系统文件结构

```
Logos/                               ← Noesis 仓库内
├── OVERVIEW.md                      ← 本文件
├── skills/
│   ├── paper-discovery-skill.md     ← 论文发现与筛选
│   └── paper-reading-skill.md       ← 深度阅读与知识沉淀
├── templates/
│   ├── research-directions.md       ← 研究方向配置（搜索参数）
│   ├── reading-queue.md             ← 阅读队列
│   ├── kb-index.md                  ← 知识库总索引
│   └── paper-reading-note.md        ← 单篇论文笔记模板
└── plugin/commands/
    ├── paper-reading-discover/      ← /paper-reading:discover 命令
    └── paper-reading-read/          ← /paper-reading:read 命令
```

**知识库产出目录**（LogosBase）：

```
LogosBase/
├── kb-index.md              ← 从 templates/ 初始化
├── reading-queue.md         ← 从 templates/ 初始化
├── research-directions.md   ← 从 templates/ 初始化
└── [arxiv-id].md            ← 每篇论文的笔记（由 /paper-reading:read 生成）
```

---

## 快速开始

### 1. 配置 Plugin

Logos 的 slash commands 通过 `.claude/skills/` 注册（项目级），在 Noesis 仓库目录下使用 Claude Code 即可直接调用，无需额外配置。

### 2. 初始化知识库

```bash
KB_DIR="$HOME/Documents/LogosBase"
LOGOS="$HOME/Documents/Noesis/Logos"
cp "$LOGOS/templates/kb-index.md" "$KB_DIR/"
cp "$LOGOS/templates/reading-queue.md" "$KB_DIR/"
cp "$LOGOS/templates/research-directions.md" "$KB_DIR/"
```

### 3. 配置研究方向

编辑 `LogosBase/research-directions.md`，填入：
- 核心关键词 / 扩展关键词
- 种子论文（用于引用链追踪）
- 目标 Venue 列表
- 关注作者

### 4. 发现论文

```
/paper-reading-discover ~/Documents/LogosBase
```

或省略路径（使用默认 LogosBase 路径）：
```
/paper-reading:discover
```

### 5. 深度阅读

```
/paper-reading:read
```

对 `reading-queue.md` 中的高优先论文进行深度阅读，提取五类知识资产，更新 `kb-index.md`。

---

## Plugin 命令

| 命令 | 说明 |
|------|------|
| `/paper-reading:discover [kb_path]` | 论文发现：搜索、评分、更新阅读队列 |
| `/paper-reading:read [kb_path]` | 深度阅读：阅读论文、提取知识资产、更新知识库 |

`kb_path` 可省略，默认为 LogosBase 路径。
