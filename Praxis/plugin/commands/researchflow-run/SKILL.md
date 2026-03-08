# Skill: ResearchFlow 自动化运行器

## 触发

```
/researchflow:run <project_path>
```

---

## 初始化

1. 从项目 `CLAUDE.md` 读取 `researchflow_path` 字段（默认 `/home/jinxulin/ResearchFlow`）。
2. 设 `RUNNER = <researchflow_path>/orchestrator/runner.py`。

---

## 主循环

这是一个**纯机械循环**。不做任何解释，不补充任何步骤，严格按以下 5 步重复执行。

---

### 步骤 1：获取下一个 Action

```bash
python3 $RUNNER next <project_path>
```

解析返回 JSON：

| `action_type` 值 | 行为 |
|------------------|------|
| `"done"` | 输出完成信息（见下方），**退出循环** |
| `"error"` | 输出错误信息，**退出循环** |
| `"skill"` | 继续步骤 2 |

---

### 步骤 2：人工检查点（仅当 JSON 含 `checkpoint_message`）

向用户展示 `checkpoint_message` 字段内容，等待回复：

- `yes` → 继续步骤 3
- `skip` → 直接执行步骤 4（runner.py advance 会读取已有 outcome 或以 done 推进）
- `stop` → 输出"已暂停，下次运行 `/researchflow:run <project_path>` 继续。"，**退出循环**

若 JSON 含 `iteration_warning`，展示后同样等待用户确认（yes/stop）再继续。

---

### 步骤 3：执行 Fork Agent

使用 **Agent tool**，传入：

- `description`：JSON 的 `description` 字段
- `prompt`：JSON 的 `fork_prompt` 字段（**原样传入，不修改**）

等待 fork agent 完成。

---

### 步骤 4：推进状态机

```bash
python3 $RUNNER advance <project_path>
```

解析返回 JSON：

- 含 `error` → 向用户展示错误，**退出循环**
- 否则输出一行进度：`✓ <from_phase> → <outcome> → <next_phase>  <notes>`

---

### 步骤 5：回到步骤 1

---

## 完成时输出

```
🎉 ResearchFlow Pipeline 完成！
   项目：<project_path>
   查阅 Papers/ 获取论文草稿。
```
