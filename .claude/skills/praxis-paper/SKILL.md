---
description: "Praxis 论文写作模块：自动化执行 P1→P7 论文写作流程"
---

# Skill: Praxis 论文写作模块运行器 (P1→P7)

## 触发

```
/praxis-paper <project_path>
```

---

## 初始化

1. 从项目 `CLAUDE.md` 读取 `Noesis 路径` 字段（默认通过 `echo $HOME` 推导为 `$HOME/Documents/Noesis`）。
2. 设 `RUNNER = <noesis_path>/Praxis/orchestrator/paper_runner.py`。
3. 确认项目 `Papers/` 目录存在（不存在则创建）。

---

## 前置检查

检查项目主 pipeline 状态：

```bash
python3 <noesis_path>/Praxis/orchestrator/research_runner.py status <project_path>
```

确认当前 phase 为 `paper_writing`。如果不是，向用户展示当前状态并询问是否继续。

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
| `"skill"` | 继续步骤 2 |
| `"skills_parallel"` | 继续步骤 2（并行模式） |

---

### 步骤 2：检查警告信息

若 JSON 含 `iteration_warning`，展示后等待用户确认（yes/stop）再继续。

若 JSON 含 `revision_warning`，展示后等待用户确认（yes/stop）再继续。

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

> `role: "main"` 的 agent 写入 `Papers/phase-outcomes/<phase>.json`（决定路由）。
> `role: "codex"` 的 agent 写入 `Papers/codex-reviews/<phase>-review.md`（仅供参考）。
> 如果 Codex MCP 不可用，`role: "codex"` 的 agent 会自行跳过，不影响主流程。

---

### 步骤 4：推进状态机

```bash
python3 $RUNNER advance <project_path>
```

解析返回 JSON：

- 含 `error` → 向用户展示错误，**退出循环**
- 否则输出一行进度：`✓ <from_phase> → <outcome> → <next_phase>  <notes>`

如果 `next_phase` 为 `P4` 且 `outcome` 为 `revise`，输出修订提示：
```
↩ P5 终审未通过（评分 < 7.0），回到 P4 修订。修订轮次：<revision_rounds>
```

---

### 步骤 5：回到步骤 1

---

## 论文模块完成时输出

当 `action_type` 为 `"done"` 时，输出：

```
🎉 论文写作模块（P1→P7）已完成！
   项目：<project_path>
   论文文件：<project_path>/Papers/latex/main.tex
   项目审查：<project_path>/Papers/project-review/synthesis.md

   下一步：
   1. 检查 Papers/latex/main.pdf，确认格式和内容
   2. 查看 Papers/project-review/synthesis.md，了解项目审查结论
   3. 运行 /praxis-goto <project_path> R11 进入项目回顾
   4. 运行 /praxis-evolve <project_path> 提取经验教训
```

---

## 注意事项

- 论文写作模块使用**独立的状态机**（`paper_runner.py` / `paper_state_machine.py`），与主研究 pipeline 状态互不影响
- P5 终审如果评分 < 7.0，会自动回退到 P4 修订（最多 2 轮）
- 所有论文相关文件位于 `<project_path>/Papers/` 目录下
- P3 的 5 角色审查在 main fork agent 中顺序执行；Codex 外部审查以独立并行 agent 同步进行
- P7 的 Critic + Supervisor 在 main fork agent 中顺序执行；Codex 外部审查以独立并行 agent 同步进行
- Codex 并行 agent 的结果为**参考信息**，不影响 Pass/Revise 路由决策
