---
description: "Praxis Research：设计审查（6 Agent 辩论）"
---

# /praxis-r-design-review <project_path>

运行研究模块的 design_review 阶段：6 Agent 技术辩论（Theorist、Methodologist、Empiricist、Skeptic、Pragmatist、Contrarian）+ 综合判定。

## 变量

```
PROJECT_PATH = $ARGUMENTS
RUNNER = ~/Research/Noesis/Praxis/orchestrator/research_runner.py
SM = ~/Research/Noesis/Praxis/orchestrator/research_state_machine.py
```

## 前提检查

当前阶段必须是 `design_review`。检查：

```bash
python3 $RUNNER status $PROJECT_PATH
```

如果当前 phase 不是 `design_review`，使用 `init-phase` 强制设置：
```bash
python3 $SM init-phase $PROJECT_PATH design_review
```

## 执行

### Step 1: 获取动作

```bash
python3 $RUNNER next $PROJECT_PATH
```

### Step 2: 执行 Fork Agent

使用 Agent tool：
- `description`: JSON 中的 `description`
- `prompt`: JSON 中的 `fork_prompt`
- `model`: `opus`

若 `action_type` 为 `"skills_parallel"`，同时发起多个 Agent（main + codex）。

### Step 3: 推进状态机

```bash
python3 $RUNNER advance $PROJECT_PATH
```

解析结果并显示：
- `pass` → `✓ 审查通过，进入实现蓝图`
- `revise` → `↩ 需要修改，回到 design`
- `fundamental` → `↩ 方向层问题，回到 formalize`
- `abandon` → `✗ 方向终止`
