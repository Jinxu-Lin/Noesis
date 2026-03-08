# Skill: Paper Discovery

## 触发

```
/paper-reading:discover <kb_path>
```

`<kb_path>` 是知识库目录的绝对路径（包含 `reading-queue.md`、`kb-index.md`、`research-directions.md`）。

---

## 执行步骤

### 步骤 1：加载 Skill 内容

读取文件：`/home/jinxulin/ResearchFlow/paper-reading/skills/paper-discovery-skill.md`

### 步骤 2：构建并发送 Fork Agent

使用 **Agent tool**，传入：

- `description`：`Paper Discovery — 论文发现与筛选`
- `prompt`：以下内容（将 `<kb_path>` 替换为实际路径）

---

```
# 任务上下文

**知识库路径**：`<kb_path>`
**PaperReading 子系统根目录**：`/home/jinxulin/ResearchFlow/paper-reading`

所有读写操作均使用绝对路径（以 `<kb_path>/` 为前缀）。
`research-directions.md`、`reading-queue.md`、`kb-index.md` 均位于 `<kb_path>/`。

---

# Skill 执行指令

[此处粘贴 paper-discovery-skill.md 的完整内容]
```

---

### 步骤 3：等待完成

等待 Fork Agent 完成。向用户确认：阅读队列已更新，可运行 `/paper-reading:read <kb_path>` 进行深度阅读。
