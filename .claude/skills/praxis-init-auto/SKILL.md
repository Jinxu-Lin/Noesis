---
description: "Praxis Init Auto：自动运行完整初始化模块（init→start→probe_design→review）"
---

# /praxis-init-auto <project_name>

自动运行初始化模块的完整流程：init → start → probe_design → review。

## 变量

```
PROJECT_NAME = $ARGUMENTS
PROJECT_PATH = ~/Research/$PROJECT_NAME
RUNNER = ~/Research/Noesis/Praxis/orchestrator/init_runner.py
SM = ~/Research/Noesis/Praxis/orchestrator/init_state_machine.py
```

## 执行

### Step 0: 初始化（如果项目尚不存在）

```bash
mkdir -p $PROJECT_PATH
python3 $SM init $PROJECT_PATH
```

### Step 1-N: 自动循环

重复执行以下循环，直到收到 `done`、`error` 或 `manual`：

**1. 获取下一步动作**

```bash
python3 $RUNNER next $PROJECT_PATH
```

**2. 解析返回的 JSON 并分发**

- `action_type == "done"` → 显示 Init Module 完成信息（含 decision），退出循环
- `action_type == "error"` → 显示错误信息，退出循环
- `action_type == "manual"` → 显示手动阶段指引（hold），退出循环
- `action_type == "skill"` → 继续执行

**3. 执行 Fork Agent**

使用 Agent tool 启动 fork agent：
- `description`: JSON 中的 `description`
- `prompt`: JSON 中的 `fork_prompt`
- `model`: `opus`

**4. 推进状态机**

```bash
python3 $RUNNER advance $PROJECT_PATH
```

解析结果：
- 显示进度：`✓ {from_phase} → {outcome} → {next_phase}`
- 如果 `next_phase == "start"` 且是从 review revise 回退 → 显示：`↩ Review 要求修改，回到 start`

**5. 回到 Step 1**

继续循环。

### 完成条件

- `action_type == "done"` → Init Module 完成
  - 如果 `decision == "Pass"` → 显示成功，提示运行下一模块
  - 如果 `decision == "Stop"` → 显示终止原因
- `action_type == "manual"` (hold) → 显示等待信息，提示用户补充后运行 `/praxis-review`
- 循环超过 10 次 → 安全退出，提示检查状态
