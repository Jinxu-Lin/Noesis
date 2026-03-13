# Method Design: [项目名称]

---
version: "1.0"
created: "<date>"
last_modified: "<date>"
entry_mode: "first"
iteration_major: 1
iteration_minor: 0
---

> 基于 `problem-statement.md` 的 Gap 根因和 `probe-results.md` 的经验信号，本文档设计解决方案并论证因果关系。
> 核心逻辑链：Gap → 根因 → 方法设计 → 为什么能解决 → 怎么验证。每一环都不能断。
> 与 `experiment-design.md` 通过交叉引用关联：每个组件指向其对应的 ablation 实验。

---

## 1. 方法概述
<!-- 用 1 段话概括：我们提出了什么方法，核心思路是什么 -->


## 2. 方法框架

### 2.1 组件拆解
<!-- 方法由哪些可解耦的组件构成？每个组件标注对应的 ablation 实验 -->

| 组件 | 功能 | 输入 | 输出 | 可解耦? | Ablation → |
|------|------|------|------|--------|-----------|
| | | | | | `→ experiment-design.md §7 Ablation-X` |

### 2.2 核心机制
<!-- 方法的技术细节，包含关键公式和定义 -->


### 2.3 因果论证
<!-- 显式论证：Gap 根因 → 方法设计 → 为什么能解决 -->
<!-- 这是论文叙事的脊柱 -->

```
Gap (problem-statement.md §1): ...
    ↓ 根因 (problem-statement.md §1.3): ...
        ↓ 方法设计: ...
            ↓ 为什么能解决: ...
```

## 3. 探针信号整合
<!-- 从 probe-results.md 中提取的关键经验信号如何约束/指导方法设计 -->
<!-- 哪些探针发现直接影响了组件选择？ -->


## 4. 理论分析 (如适用)
<!-- 理论保证、复杂度分析、收敛性、误差界等 -->


## 5. 方法定位

### 5.1 继承了什么
<!-- 从哪些现有方法中借鉴了什么？ -->

### 5.2 改变了什么
<!-- 与最相近现有方法的本质区别是什么？ -->


## 6. 组件审查记录
<!-- 记录组件级审查的结果 -->

| 组件 | 功能抽象 | 当前实现 | 已考虑的替代方案 | 跨领域搜索? | 结论 |
|------|---------|---------|----------------|-----------|------|
| | | | | | |

## 7. 风险评估与备选方案
<!-- 方法设计中的风险点，以及如果核心假设不成立的备选路线 -->
<!-- Gap 是稳定的，Method 可以迭代 -->


---

## Metadata
- **基于**: `problem-statement.md`, `probe-results.md`, `project-startup.md`
- **交叉引用**: `experiment-design.md`（组件 → ablation 映射）
- **状态**: Draft / Under Review / Finalized
- **Technical Review 判定**: 待审查 / Pass / Revise / Block
