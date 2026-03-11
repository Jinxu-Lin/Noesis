---
description: "Praxis 研究模块：自动化执行 R2→R8 研究流程"
---

# Skill: Praxis 研究模块运行器 (R2→R8)

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

解析返回 JSON：

| `action_type` 值 | 行为 |
|------------------|------|
| `"done"` | 输出完成信息，**退出循环** |
| `"error"` | 输出错误信息，**退出循环** |
| `"manual"` | 输出 `message` 字段内容，**退出循环**（研究模块完成，进入人工编码阶段） |
| `"skill"` | 继续步骤 2 |
| `"skills_parallel"` | 继续步骤 2（并行模式） |

---

### 步骤 2：人工检查点（仅当 JSON 含 `checkpoint_message`）

向用户展示 `checkpoint_message` 字段内容，等待回复：

- `yes` → 继续步骤 3
- `skip` → 直接执行步骤 4
- `stop` → 输出"已暂停，下次运行 `/praxis-research <project_path>` 继续。"，**退出循环**

若 JSON 含 `iteration_warning`，展示后同样等待用户确认（yes/stop）再继续。

---

### 步骤 3：执行 Fork Agent

**若 `action_type` 为 `"skill"`：**

使用 **Agent tool**，传入：

- `description`：JSON 的 `description` 字段
- `prompt`：JSON 的 `fork_prompt` 字段（**原样传入，不修改**）

等待 fork agent 完成。

**若 `action_type` 为 `"skills_parallel"`：**

同时（**并行**）发起多个 Agent tool 调用。遍历 JSON 的 `skills` 数组，为每个 skill 发起一个 Agent：

- `description`：该 skill 的 `description` 字段
- `prompt`：该 skill 的 `fork_prompt` 字段（**原样传入，不修改**）

在单条消息中发出所有 Agent 调用，等待全部完成。

> `role: "main"` 的 agent 写入 `phase-outcomes/<phase>.json`（决定路由）。
> `role: "codex"` 的 agent 写入 `codex-reviews/<phase>-review.md`（仅供参考）。
> 如果 Codex MCP 不可用，`role: "codex"` 的 agent 会自行跳过，不影响主流程。

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

## 研究模块完成时输出

当 `action_type` 为 `"manual"` 时，输出：

```
✅ 研究模块（R2→R8）已完成！
   项目：<project_path>

   下一步：
   1. 进入 Codes/ 目录，按 code-todo.md 和 experiment-todo.md 进行编码与实验
   2. 快速验证通过 → /praxis-goto <project_path> paper_writing 进入论文写作
   3. 快速验证失败 → /praxis-conclude <project_path> 总结并重启研究
```

当 `action_type` 为 `"done"` 时，输出：

```
🎉 Praxis Pipeline 完成！
   项目：<project_path>
```
