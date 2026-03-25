---
description: "Praxis Init：项目初始化（目录 + 上下文提取 + Git）"
---

# /praxis-init <project_name>

初始化一个新的研究项目。从当前对话上下文中提取 idea、baseline 论文和资源信息，创建项目目录和初始文档。

## 变量

```
PROJECT_NAME = $ARGUMENTS
PROJECT_PATH = ~/Research/$PROJECT_NAME
RUNNER = ~/Research/Noesis/Praxis/orchestrator/init_runner.py
```

## 执行

### Step 1: 获取下一步动作

```bash
python3 $RUNNER next $PROJECT_PATH
```

如果项目路径不存在，先创建：
```bash
mkdir -p $PROJECT_PATH
python3 ~/Research/Noesis/Praxis/orchestrator/init_state_machine.py init $PROJECT_PATH
```

然后重新获取动作：
```bash
python3 $RUNNER next $PROJECT_PATH
```

### Step 2: 检查动作类型

解析返回的 JSON：

- 如果 `action_type == "done"` → 显示完成信息，退出
- 如果 `action_type == "error"` → 显示错误，退出
- 如果 `action_type == "skill"` → 继续 Step 3

### Step 3: 执行 Fork Agent

使用 Agent tool 启动 fork agent：
- `description`: JSON 中的 `description`
- `prompt`: JSON 中的 `fork_prompt`
- `model`: `opus`

### Step 4: 推进状态机

```bash
python3 $RUNNER advance $PROJECT_PATH
```

显示结果：`✓ init 完成 → 下一阶段: {next_phase}`
