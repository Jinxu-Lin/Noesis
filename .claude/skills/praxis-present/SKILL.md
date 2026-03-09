---
description: "项目进展展示：生成 presentation.md，供与导师/合作者讨论"
model: sonnet
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
---

# Skill: Praxis Present

## 触发

```
/praxis-present <project_path>
```

`<project_path>` 是研究项目的绝对路径。

如 `presentation.md` 已存在，自动进入热启动模式（只更新变化的部分）。

---

## 执行步骤

### 步骤 0：确定路径

```bash
echo $HOME
```

- `noesis_root` = `HOME_DIR/Documents/Noesis`
- `project_path` = 用户提供的路径

### 步骤 1：加载 Skill 内容

读取文件：`<noesis_root>/Praxis/skills/present-skill.md`

### 步骤 2：Fork Agent 执行

使用 **Agent tool**，传入：

- `description`：`Praxis Present — 生成项目进展 presentation`
- `prompt`：以下内容（替换实际路径）

---

```
# 任务上下文

**项目路径**：`<project_path>`
**Noesis 根目录**：`<noesis_root>`

输出文件：`<project_path>/presentation.md`

---

# Skill 执行指令

[此处粘贴 present-skill.md 的完整内容]
```

---

### 步骤 3：完成

等待 Fork Agent 完成。告知用户：`presentation.md` 已生成/更新，路径为 `<project_path>/presentation.md`。
