---
description: "论文发现：多策略搜索、评分、更新阅读队列"
model: sonnet
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch, WebSearch, Agent
---

# Skill: Paper Discovery

## 触发

```
/logos-discover <kb_path>
```

`<kb_path>` 是知识库目录的绝对路径（包含 `reading-queue.md`、`kb-index.md`、`research-directions.md`）。

如未提供 `<kb_path>`，**执行步骤 0** 自动检测默认路径。

---

## 执行步骤

### 步骤 0：确定路径（仅当未提供 kb_path 时）

运行以下 Bash 命令获取当前用户主目录：

```bash
echo $HOME
```

将结果记为 `HOME_DIR`，然后：
- `kb_path` = `HOME_DIR/Documents/Episteme`
- `noesis_root` = `HOME_DIR/Documents/Noesis`

### 步骤 1：加载 Skill 内容

读取文件：`<noesis_root>/Logos/skills/paper-discovery-skill.md`

（若已提供 kb_path，noesis_root 同样通过 `echo $HOME` 推导。）

### 步骤 2：构建并发送 Fork Agent

使用 **Agent tool**，传入：

- `description`：`Paper Discovery — 论文发现与筛选`
- `prompt`：以下内容（将 `<kb_path>` 和 `<noesis_root>` 替换为实际路径）

---

```
# 任务上下文

**知识库路径**：`<kb_path>`
**Logos 子系统根目录**：`<noesis_root>/Logos`

所有读写操作均使用绝对路径（以 `<kb_path>/` 为前缀）。
`research-directions.md`、`reading-queue.md`、`kb-index.md` 均位于 `<kb_path>/`。

---

# Skill 执行指令

[此处粘贴 paper-discovery-skill.md 的完整内容]
```

---

### 步骤 3：等待完成

等待 Fork Agent 完成。向用户确认：阅读队列已更新，可运行 `/logos-read <kb_path>` 进行深度阅读。
