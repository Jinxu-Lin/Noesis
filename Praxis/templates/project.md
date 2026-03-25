---
version: "1.0"
status: "init"
decision: null
created: "<date>"
last_modified: "<date>"
---

# Project: <项目名称>

## 1. Overview

### 1.1 Topic
<!-- 一句话：这个项目研究什么 -->

### 1.2 Initial Idea
<!-- 2-3 段：从对话上下文提取的 idea 描述（what, why, how 的初始直觉）-->
<!-- 忠实于用户表述，不美化不扩展 -->

### 1.3 Baseline Papers

| # | Paper | Link | Relevance |
|---|-------|------|-----------|

### 1.4 Available Resources
- **GPU**:
- **Timeline / DDL**:
- **Existing Assets**:

---

## 2. Problem & Approach

### 2.1 Baseline Analysis

#### 它们解决了什么
<!-- 每篇 baseline 的核心贡献 + 共同覆盖的问题空间 -->

#### 它们没解决什么
<!-- 来自实验结果表、ablation、limitation 的发现 -->

#### 为什么没解决
<!-- 方法/数据/评估/计算资源层面的局限 -->

### 2.2 Problem Definition
- **问题一句话**: 现有方法做了 X，但因为 Y 所以存在 Z 问题
- **真实性论证**:
- **重要性论证**:
- **问题价值层次**: "没人做过" / "做了但有根本缺陷" / "条件变了"

### 2.3 Root Cause Analysis
<!-- 至少 3 层 Why: symptom → intermediate cause → root cause -->
<!-- Root Cause 类型：技术局限 / 错误假设 / 被忽视的维度 -->
<!-- 思想实验验证：假设 oracle 完美解决 Root Cause，问题是否消失？ -->

### 2.4 Proposed Approach
<!-- 严格 1-2 段：核心直觉 + 为什么可能有效 + 与 Root Cause 的因果匹配 -->
<!-- 候选攻击角度（如有多个） -->
<!-- 必须评估计算可行性（基于 §1.4 的资源约束） -->

### 2.5 Core Assumptions

| # | 假设 | 类型 | 来源 | 支撑强度 | 若为假会怎样 |
|---|------|------|------|---------|------------|

---

## 3. Validation Strategy

### 3.1 Idea Type Classification
<!-- 新问题定义 / 新方法 / 新视角 / 效率改进 / 混合 -->
<!-- 验证重心说明 -->

### 3.2 Core Hypothesis
<!-- 从 §2.5 提取最关键的 1-2 条 -->
<!-- 精确到可验证的预测 -->

### 3.3 Probe Experiment Design
<!-- 数据、模型/方法、实验模式 -->

### 3.4 Pass / Fail Criteria

| 结果 | 条件 | 后续动作 |
|------|------|---------|
| Pass | | 进入完整设计 |
| Marginal | | 补充验证 |
| Fail | | 重新定义问题 |

### 3.5 Time Budget & Resources
<!-- 预估时间（小时级）、GPU 需求（必须在 §1.4 范围内）、代码复杂度 -->

### 3.6 Failure Diagnosis Plan

| 失败模式 | 特征 | 意味着什么 | 后续动作 |
|---------|------|----------|---------|

---

## 4. Review

### 4.1 Review History

| Round | Date | Decision | Key Changes |
|-------|------|----------|-------------|

### 4.2 Latest Assessment Summary
<!-- 每个视角 1-2 句核心洞见 -->

### 4.3 Decision
- **Decision**: Pass / Revise / Hold / Stop
- **Rationale**:
- **Key Risks**:
- **Unresolved Disputes**:

### 4.4 Conditions for Next Module
<!-- 仅 Pass 时填写 -->
<!-- 优先问题 + 最值得先验证的假设 + Probe 执行注意事项 -->

<!-- 完整辩论记录：Reviews/init/round-{N}/ -->
