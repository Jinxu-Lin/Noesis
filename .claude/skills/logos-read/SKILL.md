---
description: "深度阅读：阅读论文、提取知识资产、更新知识库"
model: sonnet
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch, WebSearch, Agent
---

# Skill: Paper Reading

## 触发

```
/logos-read [参数]
```

**参数说明**（可省略，可组合）：
- 无参数：从阅读队列读取 1 篇最高优先级论文
- 数字（如 `5`）：从阅读队列依次读取 N 篇
- arXiv ID（如 `2405.12186`）：直接阅读指定论文，跳过队列
- 论文标题关键词（如 `attention mechanism survey`）：在队列中匹配并阅读，匹配不到则直接搜索
- 数字 + ID/标题（如 `3 2405.12186`）：**无效**，指定论文时 N 固定为 1

---

## 执行步骤

### 步骤 0：确定路径

```bash
echo $HOME
```

- `kb_path` = `HOME_DIR/Documents/Episteme`
- `noesis_root` = `HOME_DIR/Documents/Noesis`

### 步骤 1：解析参数

解析用户传入的参数，确定：
- `target`：`queue`（从队列取）/ `arxiv:<ID>`（指定 arXiv ID）/ `title:<关键词>`（标题匹配）
- `n`：要读取的篇数（默认 1；指定具体论文时固定为 1）

**参数解析规则**：
- 参数为纯数字 → `target=queue, n=该数字`
- 参数为 arXiv ID 格式（`\d{4}\.\d{4,5}` 或含 `arxiv.org`）→ `target=arxiv:<ID>, n=1`
- 参数为其他字符串 → `target=title:<参数>, n=1`
- 无参数 → `target=queue, n=1`

### 步骤 2：加载 Skill 内容

读取文件：`<noesis_root>/Logos/skills/paper-reading-skill.md`

### 步骤 3：循环执行 Fork Agent

**对每一篇（共 n 篇），依次执行**（串行，不并行，每篇完成后再开始下一篇）：

#### 3a. 确定本轮论文

- `target=queue`：读取 `<kb_path>/reading-queue.md`，取当前最高优先级的"待读"论文（跳过已完成的）
  - 若队列已空或无待读论文，提前结束循环，告知用户
- `target=arxiv:<ID>`：直接使用该 arXiv ID
- `target=title:<关键词>`：在 `reading-queue.md` 中模糊匹配标题，匹配到则使用，匹配不到则通过 WebSearch 搜索

#### 3b. 构建并发送 Fork Agent

使用 **Agent tool**，传入：

- `description`：`Paper Reading [第X篇/共N篇] — <论文标题或ID>`
- `prompt`：

```
# 任务上下文

**知识库路径**：`<kb_path>`
**Logos 子系统根目录**：`<noesis_root>/Logos`
**本轮目标论文**：<arXiv ID 或标题，或"从阅读队列取最高优先级待读论文">

所有读写操作均使用绝对路径（以 `<kb_path>/` 为前缀）。
论文笔记保存到 `<kb_path>/[arxiv-id].md`（使用模板 `<noesis_root>/Logos/templates/paper-reading-note.md`）。
`reading-queue.md`、`kb-index.md` 均位于 `<kb_path>/`。

---

# Skill 执行指令

[此处粘贴 paper-reading-skill.md 的完整内容]
```

#### 3c. 等待当前 Fork Agent 完成，再开始下一篇

每篇完成后，向用户简报：`[X/N] <论文标题> — 完成`

### 步骤 4：完成汇报

全部完成后，向用户汇报：
- 本次共读了 N 篇（列出标题）
- 阅读队列剩余待读论文数
- 如队列仍有高优先论文，建议继续执行 `/logos-read <数量>`
