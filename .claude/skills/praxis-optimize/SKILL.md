---
description: "Praxis Optimize：深度优化一个 prompt 或 skill 文件"
---

# /praxis-optimize <file_path>

对 Noesis/Praxis 系统中的一个 prompt 或 skill 文件进行深度分析和优化重写。

## 变量

```
TARGET_FILE = $ARGUMENTS
PRAXIS_ROOT = ~/Research/Noesis/Praxis
OPTIMIZE_PROMPT = ~/Research/Noesis/Praxis/prompts/optimize-prompt.md
```

## 前提检查

确认目标文件存在：

```bash
test -f $TARGET_FILE && echo "OK" || echo "MISSING"
```

如果文件不存在，提示用户检查路径后退出。

## 执行

### Step 1: 读取目标文件 + 优化方法论

读取两个文件：
1. `$OPTIMIZE_PROMPT` — 优化方法论（6 个 Phase 的完整流程）
2. `$TARGET_FILE` — 待优化的目标文件

记录目标文件的原始行数：
```bash
wc -l < $TARGET_FILE
```

### Step 2: 读取系统上下文

为了确保优化后的文件与系统一致，读取以下上下文文件：
- `~/Research/Noesis/Praxis/CLAUDE.md` — 系统架构和约定
- 目标文件所引用的上下游文件（如果 prompt 引用了其他 prompt 或 config，读取它们确认接口）

### Step 3: 启动优化 Agent

使用 Agent tool 启动 fork agent：

- **description**: `深度优化: <TARGET_FILE 的文件名>`
- **model**: `opus`
- **prompt**: 组装以下内容：

```
# 优化任务

## 目标文件路径
<TARGET_FILE>

## 目标文件当前内容
<TARGET_FILE 的完整内容>

## 系统上下文摘要
- Noesis v3 系统：3 个模块（Init, Research, Paper）
- Init: init → start → probe_design → review → probe_impl → complete
- Research: formalize → formalize_review → design → design_review → blueprint → implement → retrospective → complete
- Paper: P1→P7（独立）
- 状态文件: Docs/*-module-status.json
- 实验结果: Codes/_Results/ (md 文件)
- 审查记录: Reviews/
- 所有模型使用 opus

## 优化方法论
<OPTIMIZE_PROMPT 的完整内容>

## 执行
按照优化方法论的 6 个 Phase 执行。完成后将优化后的文件写入原路径。
```

### Step 4: 验证

优化 Agent 完成后：

1. 确认文件已被写入：
```bash
test -f $TARGET_FILE && echo "OK"
```

2. 检查新文件行数：
```bash
wc -l < $TARGET_FILE
```

3. 显示优化 Agent 输出的优化报告

### Step 5: Git 同步

```bash
cd ~/Research/Noesis
git add $TARGET_FILE
git commit -m "optimize: refine $(basename $TARGET_FILE)"
git push
```
