---
description: "Praxis Review：多视角压力测试（6 Agent 辩论 + 综合判定）"
---

# /praxis-review <project_path>

运行 Init Module 的 review 子模块：6 Agent 并行辩论 + Synthesizer 综合判定。

## 变量

```
PROJECT_PATH = $ARGUMENTS
RUNNER = ~/Research/Noesis/Praxis/orchestrator/init_runner.py
SM = ~/Research/Noesis/Praxis/orchestrator/init_state_machine.py
```

## 前提检查

当前阶段必须是 `review`。检查：

```bash
python3 $RUNNER status $PROJECT_PATH
```

如果当前 phase 不是 `review`，使用 `init-phase` 强制设置：
```bash
python3 $SM init-phase $PROJECT_PATH review
```

## 执行

### Step 1: 获取动作

```bash
python3 $RUNNER next $PROJECT_PATH
```

### Step 2: 执行 Fork Agent

review 子模块的 fork agent 负责完成以下工作（定义在 init-review-prompt.md 中）：
1. 确定 review round
2. 并行发起 6 个 debater Agent
3. 综合判定（Synthesizer）
4. 更新 project.md §4
5. Git 同步

使用 Agent tool：
- `description`: JSON 中的 `description`
- `prompt`: JSON 中的 `fork_prompt`
- `model`: `opus`

### Step 3: 推进状态机

```bash
python3 $RUNNER advance $PROJECT_PATH
```

解析结果并显示：
- `pass` → `✓ Review Pass — Init Module 完成，可进入下一模块`
- `revise` → `↩ Review Revise — 回到 start 修改。运行 /praxis-start 或 /praxis-init-auto 继续`
- `hold` → `⏸ Review Hold — 等待补充信息。补充后运行 /praxis-review 继续`
- `stop` → `✗ Review Stop — 方向终止。终止原因见 project.md §4.3`
