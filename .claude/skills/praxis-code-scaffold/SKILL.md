---
description: "Praxis Code Scaffold：按 blueprint 搭建代码骨架 + 实现核心模型组件"
---

# /praxis-code-scaffold <project_path>

按 blueprint 的文件映射表，创建项目代码骨架并逐个实现所有核心模型组件，每个组件通过验证测试后 commit。

## 变量

```
PROJECT_PATH = $ARGUMENTS
PROMPT = ~/Research/Noesis/Praxis/prompts/code-scaffold-prompt.md
```

## 前提检查

验证 blueprint 产出存在：

```bash
ls $PROJECT_PATH/Codes/CLAUDE.md $PROJECT_PATH/research/method-design.md
```

两个文件都必须存在。如果缺失，提示用户先运行 `/praxis-r-blueprint`。

## 执行

### Step 1: 读取 Prompt

读取 `$PROMPT` 的完整内容。

### Step 2: 构建 Fork Prompt

将 prompt 中所有 `<project_path>` 替换为 `$PROJECT_PATH` 的实际值。

在 prompt 末尾追加项目路径上下文：

```
---
项目路径：$PROJECT_PATH
---
```

### Step 3: 执行 Fork Agent

使用 Agent tool：
- `description`: "按 blueprint 搭建代码骨架并实现核心模型组件"
- `prompt`: Step 2 构建的完整 prompt
- `model`: `opus`

### Step 4: 报告结果

显示 Fork Agent 的执行摘要：

```
✓ 代码骨架搭建完成。

下一步：
  /praxis-code-pipeline $PROJECT_PATH    ← 构建训练/评估/配置体系
```
