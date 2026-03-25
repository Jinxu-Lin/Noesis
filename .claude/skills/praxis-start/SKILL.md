---
description: "Praxis Start：核心分析（Baseline + 问题定义 + Root Cause + 方法）"
---

# /praxis-start <project_path>

运行 Init Module 的 start 子模块：分析 baseline、定义问题、分析 root cause、确定方法方向、显性化假设。

## 变量

```
PROJECT_PATH = $ARGUMENTS
RUNNER = ~/Research/Noesis/Praxis/orchestrator/init_runner.py
SM = ~/Research/Noesis/Praxis/orchestrator/init_state_machine.py
```

## 前提检查

当前阶段必须是 `start`。检查：

```bash
python3 $RUNNER status $PROJECT_PATH
```

如果当前 phase 不是 `start`，有两种情况：
- phase 是 `init` → 提示先运行 `/praxis-init`
- phase 是其他 → 使用 `init-phase` 强制设置：
  ```bash
  python3 $SM init-phase $PROJECT_PATH start
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

显示结果：`✓ start 完成 → 下一阶段: {next_phase}`
