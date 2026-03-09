# Skill: Experiment Design (实验设计) — Phase R6

## 输入

**基础输入**：`gap-analysis.md` + `method-design.md` + 知识库 (Experimental Patterns)

**Revise 模式额外输入**：`experiment-review.md`（审查意见，由 runner 在上方注入时说明）

## 执行流程

### 首次执行

**Step 1: Dimension 0 — 快速验证设计**
最关键的第一步。定义：
- 验证什么核心假设？（最核心的 1-2 个）
- 最小实验规模？（小数据集/子集、少 epoch）
- 通过标准？（具体数值或趋势，不是"看起来 work"）
- 预计时间？（应控制在数小时内）

**Step 2: Dimension 1 — 核心验证**
每个 RQ 对应至少一个实验：
- 主实验：与 baselines 的定量对比
- 消融实验：每个组件的必要性（与 method-design.md 组件一一对应）
- 反事实验证：ground-truth 级别的验证（如可行）

**Step 3: Baseline 选择**
- 选择什么对比方法？为什么选这些？
- 必须覆盖当前 SOTA
- 从知识库 Experimental Patterns 中复用已验证的 baseline 列表

**Step 4: Metrics 定义**
- 用什么指标？指标与 RQ 的对应关系
- 确保指标真的衡量了想衡量的东西
- 主 metric vs 辅助 metric

**Step 5: Dimension 2 — 应用价值**
下游任务实验，证明方法不只是"数字上好"，而是"有用"。

**Step 6: Dimension 3 — 效率验证**
计算成本分析，证明方法是 practical 的。

**Step 7: Dimension 4 — 科学发现实验**
（非必须，但非常加分）
- 方法已被验证 → 将方法作为可信工具 → 回答此前无法回答的问题
- 主动提议："如果方法 work 了，可以用它回答什么有趣的问题？"

**Step 8: 数据集与计算规划**
- 多尺度验证策略
- 计算资源估算与可行性评估

**Step 9: 预期结果与失败预案**
- 每个实验的预期结果
- 如果结果不如预期，说明什么？
- 失败时的诊断线索

**Step 10: 生成 experiment-design.md**
按 `templates/experiment-design.md` 模板输出。

### Revise 迭代（R7 审查返回）

1. 读 `experiment-review.md`，逐条理解审查意见
2. 针对性修改：补充遗漏实验、调整 baseline、修正 metrics 等；**不从零开始**
3. 更新 `experiment-design.md`

## AI Co-Author 关键行为
- 从知识库 Experimental Patterns 中复用已验证的实验设计模式
- 检查 RQ 覆盖率——是否有 RQ 没被实验覆盖？
- 预判审稿人质疑，提前设计对应实验
- 主动提议 Dimension 4 科学发现实验
- 设计明确的 Dim 0 快速验证方案——定义通过标准和时间预算

## 输出
- `experiment-design.md`

## Exit Criteria
- [ ] Dim 0 有明确方案、通过标准和时间预算
- [ ] 每个 RQ 有至少一个核心实验覆盖
- [ ] Baseline 选择有理由，覆盖 SOTA
- [ ] 消融与方法组件一一对应
- [ ] Metrics 与 RQ 有明确对应关系
- [ ] 计算资源在可行范围内
- [ ] 每个实验定义了预期结果和失败预案
