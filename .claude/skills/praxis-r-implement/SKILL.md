---
description: "Praxis Research：编码实验（手动阶段）"
---

# /praxis-r-implement <project_path>

研究模块的 implement 阶段：这是一个**手动阶段**，由研究者编写代码、执行实验、记录结果。

## 变量

```
PROJECT_PATH = $ARGUMENTS
RUNNER = ~/Research/Noesis/Praxis/orchestrator/research_runner.py
SM = ~/Research/Noesis/Praxis/orchestrator/research_state_machine.py
```

## 前提检查

当前阶段必须是 `implement`。检查：

```bash
python3 $RUNNER status $PROJECT_PATH
```

如果当前 phase 不是 `implement`，使用 `init-phase` 强制设置：
```bash
python3 $SM init-phase $PROJECT_PATH implement
```

## 执行

### Step 1: 获取动作

```bash
python3 $RUNNER next $PROJECT_PATH
```

### Step 2: 显示手动阶段指引

这是手动阶段，**不启动 Fork Agent**。显示以下信息：

1. 显示 JSON 中的 `message` 字段内容（包含实验执行指南）
2. 提示研究者参考以下文件：
   - `$PROJECT_PATH/Codes/experiment-todo.md` — 实验执行清单
   - `$PROJECT_PATH/research/method-design.md` — 方法设计
   - `$PROJECT_PATH/research/experiment-design.md` — 实验设计
3. 显示完成后的推进命令：

```
完成实验后，根据结果选择推进方向：

  成功（进入知识回收）：
    python3 $RUNNER advance $PROJECT_PATH --outcome success

  方法层问题（回到联合设计）：
    python3 $RUNNER advance $PROJECT_PATH --outcome iterate_method

  方向层问题（回到问题锐化）：
    python3 $RUNNER advance $PROJECT_PATH --outcome iterate_direction

  放弃（进入知识回收后终止）：
    python3 $RUNNER advance $PROJECT_PATH --outcome abandon
```
