---
description: "Praxis Code Review：对照 blueprint 审查代码实现的忠实度和质量（6 维度）"
---

# /praxis-code-review <project_path>

对照 blueprint 和 method-design 系统性审查代码质量。可在 implement 阶段任意时间点调用。

## 变量

```
PROJECT_PATH = $ARGUMENTS
PRAXIS_ROOT = ~/Research/Noesis/Praxis
REVIEW_PROMPT = ~/Research/Noesis/Praxis/prompts/code-review-prompt.md
```

## 前提检查

确认项目代码目录存在：

```bash
test -d $PROJECT_PATH/Codes && echo "OK" || echo "MISSING: Codes/ directory"
test -f $PROJECT_PATH/Codes/CLAUDE.md && echo "OK" || echo "MISSING: Codes/CLAUDE.md"
test -f $PROJECT_PATH/research/method-design.md && echo "OK" || echo "MISSING: research/method-design.md"
```

如果 `Codes/` 或 `Codes/CLAUDE.md` 不存在，提示用户先完成 blueprint 阶段后退出。

## 执行

### Step 1: 读取审查方法论 + 项目上下文

读取以下文件：
1. `$REVIEW_PROMPT` — 审查方法论（6 维度完整流程）
2. `$PROJECT_PATH/Codes/CLAUDE.md` — 文件映射表 + 编码指南
3. `$PROJECT_PATH/research/method-design.md` — 组件规格

### Step 2: 启动审查 Agent

使用 Agent tool 启动 fork agent：

- **description**: `Code Review: $(basename $PROJECT_PATH)`
- **model**: `opus`
- **prompt**: 组装以下内容：

```
# Code Review 任务

## 项目路径
<PROJECT_PATH>

## 审查方法论
<REVIEW_PROMPT 的完整内容>

## 项目上下文: Codes/CLAUDE.md
<Codes/CLAUDE.md 的完整内容>

## 项目上下文: method-design.md
<method-design.md 的完整内容>

## 执行
按照审查方法论的完整流程执行。
将 prompt 中所有 Codes/ 路径替换为 <PROJECT_PATH>/Codes/。
将 prompt 中所有 research/ 路径替换为 <PROJECT_PATH>/research/。
将审查报告写入 <PROJECT_PATH>/Codes/_Results/code_review.md。
```

### Step 3: 显示结果

审查 Agent 完成后，读取 `$PROJECT_PATH/Codes/_Results/code_review.md` 并在对话中显示总体评估表格和修复建议摘要。
