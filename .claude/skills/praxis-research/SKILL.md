---
description: "Praxis 研究模块：自动化执行 C→R 研究流程"
---

# Skill: Praxis 研究模块运行器 (C→I, 自动化阶段)

## 触发

```
/praxis-research <project_path>
```

---

## 初始化

1. 从项目 `CLAUDE.md` 读取 `Noesis 路径` 字段（默认通过 `echo $HOME` 推导为 `$HOME/Research/Noesis`）。
2. 设 `RUNNER = <noesis_path>/Praxis/orchestrator/research_runner.py`。

---

## 主循环

这是一个**纯机械循环**。不做任何解释，不补充任何步骤，严格按以下 5 步重复执行。

---

### 步骤 1：获取下一个 Action

```bash
python3 $RUNNER next <project_path>
```

**如果命令执行失败**（非零退出码、输出不是合法 JSON）→ 向用户报告错误，**退出循环**。

解析返回 JSON：

| `action_type` 值 | 行为 |
|------------------|------|
| `"done"` | 输出完成信息，**退出循环** |
| `"error"` | 输出错误信息，**退出循环** |
| `"manual"` | 输出 `message` 字段内容，**退出循环**（进入手动阶段：P 探针实验 / E 实验执行 / W 论文写作） |
| `"skill"` | 继续步骤 2 |
| `"skills_parallel"` | 继续步骤 2（并行模式） |

---

### 步骤 2：人工检查点（仅当 JSON 含 `iteration_warning`）

若 JSON 含 `iteration_warning`，向用户展示警告内容。

**根据当前 `phase` 提供对应选项**（不同阶段支持不同的 outcome）：

**若 `phase` 为 `"D"`（联合设计迭代守卫）**：
- `yes` → 继续步骤 3
- `escalate` → 执行 `python3 $RUNNER advance <project_path> --outcome escalate`，输出结果，**回到步骤 1**
- `stop` → 输出"已暂停"，**退出循环**

**若 `phase` 为 `"C"`（问题锐化迭代守卫）**：
- `yes` → 继续步骤 3
- `abandon` → 执行 `python3 $RUNNER advance <project_path> --outcome abandon`，输出结果，**回到步骤 1**
- `stop` → 输出"已暂停"，**退出循环**

**其他阶段**（通用迭代警告）：
- `yes` → 继续步骤 3
- `stop` → 输出"已暂停"，**退出循环**

若 JSON 不含 `iteration_warning` → 直接进入步骤 3。

---

### 步骤 3：执行 Fork Agent

**模型路由**：从 JSON 中读取 `model` 字段（单任务模式）或各 skill 条目的 `model` 字段（并行模式），传给 Agent tool 的 `model` 参数。

**若 `action_type` 为 `"skill"`：**

使用 **Agent tool**，传入：

- `description`：JSON 的 `description` 字段
- `prompt`：JSON 的 `fork_prompt` 字段（**原样传入，不修改**）
- `model`：JSON 的 `model` 字段

等待 fork agent 完成。

**若 `action_type` 为 `"skills_parallel"`：**

同时（**并行**）发起多个 Agent tool 调用。遍历 JSON 的 `skills` 数组，为每个 skill 发起一个 Agent：

- `description`：该 skill 的 `description` 字段
- `prompt`：该 skill 的 `fork_prompt` 字段（**原样传入，不修改**）
- `model`：该 skill 的 `model` 字段

在单条消息中发出所有 Agent 调用，等待全部完成。

> `role: "main"` 的 agent 写入 `phase-outcomes/<phase>.json`（决定路由）。
> `role: "codex"` 的 agent 写入 `codex-reviews/<phase>-review.md`（仅供参考）。
> 如果 Codex MCP 不可用，`role: "codex"` 的 agent 会自行跳过，不影响主流程。

**错误处理**：如果 Agent tool 返回错误或失败，**不执行步骤 4**。向用户报告错误，**退出循环**。仅当 fork agent 成功完成时，才继续步骤 4。

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

## 手动阶段退出时的输出

当 `action_type` 为 `"manual"` 时，**直接输出 JSON 中的 `message` 字段内容**。

状态机已在 `message` 中填入了正确的绝对路径和可执行命令，无需二次替换。

当 `action_type` 为 `"done"` 时：
```
🎉 Praxis Pipeline 完成！
   项目：<project_path>
```
