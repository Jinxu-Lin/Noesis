---
description: "Praxis Research Auto：自动运行完整研究模块"
---

# /praxis-r-auto <project_path>

自动运行研究模块的完整流程：formalize → formalize_review → design → design_review → blueprint → implement → retrospective。

## 变量

```
PROJECT_PATH = $ARGUMENTS
RUNNER = ~/Research/Noesis/Praxis/orchestrator/research_runner.py
SM = ~/Research/Noesis/Praxis/orchestrator/research_state_machine.py
```

## 执行

### Step 0: 初始化（如果尚未初始化）

```bash
python3 $SM init $PROJECT_PATH
```

### Step 1-N: 自动循环

重复执行以下循环，直到收到 `done`、`error` 或 `manual`：

**1. 获取下一步动作**

```bash
python3 $RUNNER next $PROJECT_PATH
```

**2. 解析返回的 JSON 并分发**

- `action_type == "done"` → 显示 Research Module 完成信息，退出循环
- `action_type == "error"` → 显示错误信息，退出循环
- `action_type == "manual"` → 进入手动阶段（implement），显示手动指引信息，退出循环
- `action_type == "skill"` → 继续执行
- `action_type == "skills_parallel"` → 继续执行（并行模式）

**3. 执行 Fork Agent**

**若 `action_type` 为 `"skill"`：**

使用 Agent tool 启动 fork agent：
- `description`: JSON 中的 `description`
- `prompt`: JSON 中的 `fork_prompt`
- `model`: `opus`

**若 `action_type` 为 `"skills_parallel"`：**

同时（并行）发起多个 Agent tool 调用。遍历 JSON 的 `skills` 数组，为每个 skill 发起一个 Agent：
- `description`: 该 skill 的 `description`
- `prompt`: 该 skill 的 `fork_prompt`
- `model`: 该 skill 的 `model`

**4. 推进状态机**

```bash
python3 $RUNNER advance $PROJECT_PATH
```

解析结果：
- 显示进度：`✓ {from_phase} → {outcome} → {next_phase}`
- 如果是 review revise 回退 → 显示回退信息

**5. 回到 Step 1**

继续循环。

### 完成条件

- `action_type == "done"` → Research Module 完成
  - 显示：`🎉 Research Module 完成！项目：$PROJECT_PATH`
- `action_type == "manual"` (implement) → 显示手动阶段指引：
  - 显示 JSON 中的 `message` 字段内容
  - 提示：`进入手动编码实验阶段。完成后运行 /praxis-r-implement 查看指引，或直接 advance：`
  - `python3 $RUNNER advance $PROJECT_PATH --outcome success`
  - `python3 $RUNNER advance $PROJECT_PATH --outcome iterate_method`
  - `python3 $RUNNER advance $PROJECT_PATH --outcome iterate_direction`
  - `python3 $RUNNER advance $PROJECT_PATH --outcome abandon`
- 循环超过 20 次 → 安全退出，提示检查状态
