# Skill: Full Implementation & Experiments (补全实现与完整实验) — Phase 8b

## 触发场景
`/impl-validate` 完成（Dim 0 通过），进入补全实现和 Dim 1-4 完整实验。

## 输入
- `method-design.md` — 方法组件结构
- `experiment-design.md` — Dim 1-4 实验设计
- `contribution.md` — 当前贡献记录
- Code/ 目录（含已通过 Dim 0 的核心代码）
- CLAUDE.md 的 Code/ 子节
- code-todo.md、experiment-todo.md

## 执行流程

### Step 1: 更新 code-todo.md 第二轮

补充实现清单：
- [ ] 消融变体实现（配置驱动，无需改核心代码）
- [ ] 额外 baselines 实现
- [ ] 完整评估 pipeline（所有 Dim 1-4 需要的 metrics）
- [ ] Dimension 4 科学发现实验所需的代码
- [ ] 可视化与图表生成代码

### Step 2: 更新 experiment-todo.md 第二轮

按 Dimension 1-4 生成完整实验清单：

**Dim 1 核心验证**:
- [ ] 主实验：全数据集对比所有 baselines
- [ ] 消融实验：每个组件的独立贡献
- [ ] 反事实验证（如适用）

**Dim 2 应用价值**:
- [ ] 下游任务实验

**Dim 3 效率验证**:
- [ ] 计算成本对比（FLOPs、内存、推理时间）

**Dim 4 科学发现**:
- [ ] 利用方法作为工具探索科学问题

### Step 3: 交替执行 code-todo 和 experiment-todo

```
code-todo (补全实现)
    → experiment-todo (Dim 1 核心验证)
        → code-todo (如需补充)
            → experiment-todo (Dim 2-4)
```

**铁律**：
1. **每次实验运行后，立即更新 `experiment-todo.md`** — 标记完成、记录结果
2. **每次实验结果产出后，立即记录到 `experiment-design.md` 对应章节** — 数值结果、关键观察、与预期对比

### Step 4: 实验结果分析

对每组实验结果：
- 与预期对比：符合 / 超出 / 不及
- 异常分析：不及预期的实验，分析原因
- 可视化：生成核心图表
- insights 提取：实验结果揭示了什么？

### Step 5: 实验失败处理

如果 Dim 1-4 的实验结果不理想（部分或全部）：

触发 Iteration Diagnosis SubAgent（同 `/impl-validate` 的流程）：
- L1 Tune → 调参后重试（留在本 Skill）
- L2-4 → 写 iteration-log.md → Exit Assessment Gate → 路由

**注意**：Dim 1-4 的失败判断比 Dim 0 更复杂：
- 部分 Dimension 通过、部分不通过？→ 分析具体原因
- 消融实验显示某组件无效？→ 可能是 L2 Swap
- 整体效果与 Dim 0 不一致（小数据好、大数据差）？→ 需要深入分析

### Step 6: 更新 contribution.md

实验全部完成后：
- 更新 Phase 8 部分的贡献
- 特别关注 Dimension 4 的科学发现——这往往是最有价值的贡献
- 评估所有贡献加在一起是否足够支撑发表

### Step 7: 生成核心图表

- 主实验结果表格
- 消融实验表格
- 关键可视化（如适用：t-SNE、attention map、case study 等）
- 效率对比图

## AI Co-Author 关键行为
- 管理 code-todo.md 和 experiment-todo.md 的交替执行
- 实验结果出来后主动进行初步分析和可视化
- 遇到异常结果时主动分析原因
- 帮助提取 Dimension 4 的科学发现 insights
- 确保可复现性：种子管理、完整依赖记录、实验配置版本化

## 输出
- 完整代码（含消融变体、额外 baselines）
- 全部实验结果 + 图表
- 更新后的 code-todo.md 和 experiment-todo.md
- 更新后的 experiment-design.md（含实验结果）
- 更新后的 contribution.md
- （失败时）iteration-log.md 新 Entry

## Exit Criteria
- [ ] 所有 experiment-todo.md 中的实验项已完成
- [ ] 所有实验结果已实时记录到 experiment-design.md
- [ ] 核心表格和图表已生成
- [ ] 结果支撑 contribution.md 中的 claims
- [ ] contribution.md 已更新（含实验发现的新贡献）
- [ ] 配置驱动的消融实验可复现

## 完成后
提示用户：全部实验完成，建议进入 `/paper-writing` 开始撰写论文。
