---
description: "Praxis Code Pipeline：数据/训练/评估/配置体系实现"
---

# /praxis-code-pipeline <project_path>

在 scaffold 产出的核心组件上构建完整的数据 pipeline、训练循环、评估脚本和 config 体系。

## 变量

```
PROJECT_PATH = $ARGUMENTS
PROMPT = ~/Research/Noesis/Praxis/prompts/code-pipeline-prompt.md
```

## 前提检查

1. 确认 scaffold 已完成（核心组件已实现）：
   - `$PROJECT_PATH/Codes/core/` 存在且包含 `.py` 文件
   - `$PROJECT_PATH/Codes/tests/` 存在（scaffold 测试）

2. 确认必要输入文档存在：
   - `$PROJECT_PATH/Codes/CLAUDE.md`
   - `$PROJECT_PATH/research/experiment-design.md`
   - `$PROJECT_PATH/research/method-design.md`

如果前提不满足，提示用户先运行 `/praxis-code-scaffold`。

## 执行

### Step 1: 构建 Prompt

读取 `$PROMPT` 的完整内容。

构建 fork_prompt：

```
<prompt 内容>

---

## 项目路径

PROJECT_PATH = $PROJECT_PATH

## 关键输入文件

- Codes/CLAUDE.md: $PROJECT_PATH/Codes/CLAUDE.md
- experiment-design.md: $PROJECT_PATH/research/experiment-design.md
- method-design.md: $PROJECT_PATH/research/method-design.md
- experiment-todo.md: $PROJECT_PATH/Codes/experiment-todo.md（如存在）
- core/: $PROJECT_PATH/Codes/core/
- probe/: $PROJECT_PATH/Codes/probe/（如存在，可复用 data loader）
```

### Step 2: 执行 Fork Agent

使用 Agent tool：
- `description`: "实现数据 pipeline、训练循环、评估脚本和 config 体系"
- `prompt`: 上一步构建的 fork_prompt
- `model`: `opus`

### Step 3: 验证产出

检查以下文件/目录已创建：
- `$PROJECT_PATH/Codes/configs/base.yaml`
- `$PROJECT_PATH/Codes/configs/pilot.yaml`
- 至少一个 `$PROJECT_PATH/Codes/configs/ablation_*.yaml`
- `$PROJECT_PATH/Codes/scripts/run_all.sh`
- 训练脚本（`train.py` 或 `experiments/*/train.py`）
- 评估脚本（`evaluate.py` 或 `experiments/*/evaluate.py`）

### Step 4: 显示结果

```
Pipeline 实现完成。

  产出：
    - 数据 pipeline (data loading + preprocessing)
    - 训练循环 (seed 管理 + logging + checkpointing + dry-run + resume)
    - 评估脚本 (所有指标 + _Results/ 输出)
    - Config 体系 (base + ablation + baseline + pilot)
    - Run scripts (pilot/baseline/main/ablation/all)

  下一步：运行 /praxis-code-baseline $PROJECT_PATH
    - Sanity checks
    - Pilot 快速验证
    - Baseline 复现
```
