---
description: "深度阅读：阅读论文、提取知识资产、更新知识库"
model: sonnet
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch, WebSearch, Agent
---

# Skill: Paper Reading

## 触发

```
/paper-reading-read <kb_path>
```

`<kb_path>` 是知识库目录的绝对路径（包含 `reading-queue.md`、`kb-index.md`）。

如未提供 `<kb_path>`，**执行步骤 0** 自动检测默认路径。

可选：在 `<kb_path>` 后追加论文 URL 或 arXiv ID，直接阅读指定论文（跳过队列）。

---

## 执行步骤

### 步骤 0：确定路径（仅当未提供 kb_path 时）

运行以下 Bash 命令获取当前用户主目录：

```bash
echo $HOME
```

将结果记为 `HOME_DIR`，然后：
- `kb_path` = `HOME_DIR/Documents/LogosBase`
- `noesis_root` = `HOME_DIR/Documents/Noesis`

### 步骤 1：加载 Skill 内容

读取文件：`<noesis_root>/Logos/skills/paper-reading-skill.md`

（若已提供 kb_path，noesis_root 同样通过 `echo $HOME` 推导。）

### 步骤 2：构建并发送 Fork Agent

使用 **Agent tool**，传入：

- `description`：`Paper Reading — 深度阅读与知识沉淀`
- `prompt`：以下内容（将 `<kb_path>` 和 `<noesis_root>` 替换为实际路径）

---

```
# 任务上下文

**知识库路径**：`<kb_path>`
**Logos 子系统根目录**：`<noesis_root>/Logos`

所有读写操作均使用绝对路径（以 `<kb_path>/` 为前缀）。
论文笔记保存到 `<kb_path>/[arxiv-id].md`（使用模板 `<noesis_root>/Logos/templates/paper-reading-note.md`）。
`reading-queue.md`、`kb-index.md` 均位于 `<kb_path>/`。

---

# Skill 执行指令

[此处粘贴 paper-reading-skill.md 的完整内容]
```

---

### 步骤 3：等待完成

等待 Fork Agent 完成。向用户确认：知识库已更新。如阅读队列仍有高优先论文，建议继续执行 `/paper-reading-read <kb_path>`。
