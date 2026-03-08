# Skill: Implementation & Quick Validation (核心实现与快速验证) — Phase 8a

## 触发场景
`/impl-setup` 完成（环境就绪、baseline 已复现），进入核心实现和 Dim 0 快速验证。

## 输入
- `method-design.md` — 方法组件结构和数学公式
- `experiment-design.md` — Dim 0 的通过标准
- `code-todo.md` — 第一轮代码清单
- `experiment-todo.md` — Dim 0 实验项
- Code/ 目录（含 baseline 代码和评估 pipeline）
- CLAUDE.md 的 Code/ 子节 — 代码域上下文

## 执行流程

### Step 1: 核心组件实现

按 `code-todo.md` 逐项实现。对每个组件：

1. **阅读 method-design.md 对应章节** — 理解数学定义和 I/O 规格
2. **实现组件** — 代码与数学公式严格对应
3. **单元验证** — 每个组件实现后立即验证：
   - 输入/输出维度是否正确？
   - 边界条件是否处理？
   - 数值稳定性（NaN/Inf 检查）？
   - 与公式的一致性（手算小例子对比）？
4. **更新 code-todo.md** — 标记完成状态

**组件实现顺序**：按数据流方向（输入端 → 输出端），确保每个组件可以立即测试。

### Step 2: Pipeline 组装

将各组件按 `method-design.md` 的框架图组装为端到端 pipeline：
- 组件间的接口是否匹配（维度、类型）？
- 数据流是否通畅？
- 是否可以用小数据跑通一个 forward pass？

### Step 3: 执行 Dim 0 快速验证

按 `experiment-todo.md` 执行快速验证：
- 在小规模数据上对比核心 baseline
- 通过标准参照 `experiment-design.md` Dim 0 的量化定义
- **应在数小时内完成**

**实时记录**：
- 每次实验后立即更新 `experiment-todo.md`（标记完成、记录结果）
- 将结果记录到 `experiment-design.md` 的 Dim 0 章节

### Step 4: 验证决策

**通过 → 结束本 Skill，进入 `/impl-full`**

**不通过 → 触发 Iteration Diagnosis SubAgent**

使用 Agent tool 生成 Iteration Diagnosis SubAgent（`subagents/iteration-diagnosis-subagent.md`），传入：
- 实验结果数据
- experiment-design.md（通过标准）
- method-design.md（组件结构）
- gap-analysis.md（核心假设）
- iteration-log.md（已有历史，如有）

根据 SubAgent 返回的诊断结果：

**L1 Tune**:
- 按诊断建议调整超参数/训练策略
- 重新执行 Step 3（留在本 Skill 内循环）
- L1 最多尝试 3 次，仍不通过则重新触发诊断升级

**L2/L3/L4**:
1. 将 SubAgent 产出的 Entry 追加到 `iteration-log.md`
2. 触发 Exit Assessment Gate SubAgent（`subagents/exit-assessment-subagent.md`）
3. 根据 Gate 结果路由：
   - **Continue**:
     - L2 Swap → 提示用户进入 `/method-design`（替换失败组件）
     - L3 Redesign → 提示用户进入 `/method-design`（重新设计）
     - L4 Pivot → 提示用户进入 `/gap-discovery`（重新选 Gap）
   - **Abandon** → 提示用户进入 `/retrospective`

## AI Co-Author 关键行为
- 实现时持续对照 `method-design.md` 中的数学公式，确保代码与理论一致
- 每个组件实现后进行单元验证（维度检查、边界条件、数值稳定性）
- 代码中的关键实现决策记录在 CLAUDE.md 的 Code/ 子节 中
- 遇到异常实验结果时主动分析原因，而非机械执行
- **不要在 Dim 0 通过前写消融变体等非必要代码**

## 输出
- 核心组件代码
- Dim 0 实验结果
- 更新后的 code-todo.md 和 experiment-todo.md
- （不通过时）iteration-log.md 新 Entry

## Exit Criteria
- [ ] 所有核心组件已实现并通过单元验证
- [ ] Pipeline 可端到端运行
- [ ] Dim 0 快速验证通过（按 experiment-design.md 标准）
- [ ] 结果已实时记录

## 完成后
- 通过：提示用户进入 `/impl-full` 执行完整实验。
- L2-4 Continue：提示用户进入对应的回调 Skill。
- Abandon：提示用户进入 `/retrospective`。
然后执行 `/reflect-pipeline` 对本阶段的流程进行反思，记录改进观察。
