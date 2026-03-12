# Skill: Method Design (方法设计) — Phase R4

## 输入

**基础输入（所有模式共用）**：`research/gap-analysis.md` + `project-startup.md` + 知识库 (Methods Bank)

**Revise 模式额外输入**：`inner-reviews/method-review.md`（审查意见，由 runner 在上方注入时说明）

## 执行流程

### 首次执行

**Step 1: 方案空间探索**
基于 Gap 根因（来自 `research/gap-analysis.md`），从知识库 Methods Bank 检索相关方法/技术。
不限于本领域——跨领域的方法迁移往往是 novelty 来源。

**Step 2: 方法框架搭建**
```
Gap 根因 (来自 research/gap-analysis.md)
    ↓ 查询知识库 Methods Bank
方法 A 的核心机制 + 方法 B 的某个组件 + 新的理论连接
    ↓ 组合与适配
新方法框架
    ↓ 论证
为什么这个方法能解决这个 Gap
```

**Step 3: 因果论证**
构建完整的逻辑链：Gap根因 → 方法设计 → 为什么能解决。
每一环都必须有严格的推导，无逻辑跳跃。

**Step 4: 组件级审查 (Component-Level Review)**
对方法中的每个组件执行：
1. 明确组件的输入、输出、功能
2. 判断组件是否可从框架中解耦（接口是否清晰）
3. 如果可解耦：
   a. 组件的功能本质是什么？（抽象化）
   b. 本领域是否有更好的替代方案？
   c. **跨领域**是否有更好的替代方案？（AI 知识广度优势）
   d. 替代方案是否与框架其他组件兼容？
4. 如果发现更优替代 → 提议替换，论证优势

**Step 5: 理论分析**
形式化论证（如适用）：复杂度分析、收敛性分析、表达能力分析等。

**Step 6: 方法定位**
在技术谱系中定位：继承了什么、改变了什么、与最相近方法的差异。

**Step 7: 更新 research/contribution.md**
记录方法层面的技术贡献（方法创新、理论分析等）。

**Step 8: 生成 research/method-design.md**
按 `templates/method-design.md` 模板输出，包含：
- 方法框架总览（组件拆解、各组件 I/O）
- 核心机制详述（含数学公式）
- 因果论证
- 理论分析（如适用）
- 方法定位
- 组件审查记录

### Revise 迭代（R5 审查返回）

1. 读 `inner-reviews/method-review.md`，逐条理解审查意见
2. 针对性修改 `research/method-design.md`，保留通过审查的部分
3. 重点修复逻辑跳跃、组件必要性、差异化等被标记的问题；**不从零开始**

### 注意：热重启

本阶段不再接收 Pivot 热重启。所有编码失败后的重启统一从 R1（Gap Discovery）开始，确保叙事脊柱完整。

## AI Co-Author 关键行为
- 不被人类知识边界限制，主动搜索跨领域替代组件
- 对每个组件的接口进行形式化分析（输入/输出类型、维度、语义）
- 帮助构建理论论证
- 迭代时：先读 iteration-log.md 确认失败层级和约束，再决定改动范围

## 输出
- `research/method-design.md`
- `research/contribution.md`（更新）

## Exit Criteria
- [ ] 叙事脊柱完整：Gap → 根因 → 方法 → 为什么能解决 → 怎么验证
- [ ] 每个组件可回溯到 Gap 根因——没有"因为好所以加"的组件
- [ ] 组件级审查已完成（每个可解耦组件经过替代方案评估）
- [ ] 方法定位清晰（与最相近方法的差异）
- [ ] 理论分析已完成（如适用）
- [ ] research/contribution.md 已更新
