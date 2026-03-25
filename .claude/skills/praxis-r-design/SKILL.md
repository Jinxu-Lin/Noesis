---
description: "Praxis Research：方法 + 实验联合设计"
---

# /praxis-r-design <project_path>

运行研究模块的 design 阶段：方法 + 实验同步设计。

## 变量

```
PROJECT_PATH = $ARGUMENTS
RUNNER = ~/Research/Noesis/Praxis/orchestrator/research_runner.py
SM = ~/Research/Noesis/Praxis/orchestrator/research_state_machine.py
```

## 前提检查

当前阶段必须是 `design`。检查：

```bash
python3 $RUNNER status $PROJECT_PATH
```

如果当前 phase 不是 `design`，使用 `init-phase` 强制设置：
```bash
python3 $SM init-phase $PROJECT_PATH design
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

### Step 3: 推进状态机

```bash
python3 $RUNNER advance $PROJECT_PATH
```

显示结果：`✓ design 完成 → 下一阶段: {next_phase}`
