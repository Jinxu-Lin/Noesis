# Experiment Design: [项目名称]

---
version: "1.0"
created: "<date>"
last_modified: "<date>"
entry_mode: "first"
iteration_major: 1
iteration_minor: 0
---

> 本文档是实验的完整 spec，同时也是实验结果的记录地。
> 基于 `problem-statement.md` 的 RQ 和 `method-design.md` 的方法设计。
> 与 `method-design.md` 通过反向引用关联：每个 ablation 指向其对应的方法组件。
> **铁律**: 每次实验结果产出后，立即记录到本文档对应章节的"实际结果"区域。

---

## 1. Research Questions 与实验映射

| RQ | 核心实验 | 消融实验 | 预期结果 | 失败说明什么 |
|----|---------|---------|---------|------------|
| RQ1 | | | | |
| RQ2 | | | | |

---

## 2. 模型与数据集

| 规模 | 模型 | 参数量 | 数据集 | 训练方式 |
|------|------|--------|--------|---------|
| 小 | | | | |
| 中 | | | | |
| 大 | | | | |

---

## 3. Baselines

| 方法 | 为什么选 | 它验证什么 |
|------|---------|----------|
| | | |

---

## 4. Evaluation Metrics

| Metric | 定义 | 对应 RQ | 为什么选这个 |
|--------|------|---------|------------|
| | | | |

---

## 5. Dim 0 → Dim 1 衔接
<!-- 探针实验（Dim 0）到正式实验（Dim 1）的衔接说明 -->

### 5.1 探针信号如何指导实验设计
<!-- 从 probe-results.md 中提取的关键发现对实验设计的影响 -->

### 5.2 规模扩展方案
<!-- 从探针的小规模设置到正式实验的完整规模，需要哪些调整 -->

---

## 6. 核心实验 (Dimension 1: 方法有效性)

### 6.1 主实验
<!-- 实验设置、步骤、对比方式 -->

**实际结果**:
<!-- 实验完成后在此记录：数值、关键观察、与预期的对比 -->


### 6.2 反事实验证 (如可行)
<!-- Ground-truth 级别的验证 -->

**实际结果**:


---

## 7. 消融实验 (Dimension 1: 组件必要性)
<!-- 每个 ablation 反向引用 method-design.md 中的对应组件 -->

| Ablation ID | 移除/替换什么 | ← 方法组件 | 预期影响 |
|-------------|-------------|-----------|---------|
| Ablation-1 | | `← method-design.md §2.1 Component-X` | |
| Ablation-2 | | `← method-design.md §2.1 Component-Y` | |

---

## 8. 应用实验 (Dimension 2: 实用价值)

<!-- 下游任务实验设计 -->

**实际结果**:


---

## 9. 效率分析 (Dimension 3: 实际可行性)

<!-- 计算成本、时间、内存分析 -->

**实际结果**:


---

## 10. 科学发现实验 (Dimension 4: Bonus)

<!-- 用方法作为工具探索新问题 -->

**实际结果与 Insights**:


---

## 11. 计算资源估算

| 实验 | GPU 类型 | 预计时长 | 存储需求 |
|------|---------|---------|---------|
| | | | |

---

## 12. 风险与预案

| 风险 | 可能性 | 影响 | 预案 |
|------|--------|------|------|
| 核心实验结果不显著 | | | |
| 计算资源不足 | | | |
| | | | |

---

## Metadata
- **基于**: `problem-statement.md`, `probe-results.md`, `method-design.md`
- **反向引用**: `method-design.md`（ablation → 组件映射）
- **状态**: Draft / Under Review / Finalized
- **Technical Review 判定**: 待审查 / Pass / Revise / Block
