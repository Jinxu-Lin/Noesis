# Skill: Gap Discovery (研究空白发现) — Phase R2

## 输入

**基础输入（所有模式共用）**：`project-startup.md` + 知识库 (Gaps & Assumptions, Cross-Paper Connections)

**Revise 模式额外输入**：`gap-review.md`（审查意见，由 runner 在上方注入时说明）

**Pivot 模式额外输入**：`iteration-log.md` + 当前 `gap-analysis.md`（由 runner 在上方注入时说明）

## 执行流程

### 首次执行

**Step 1: Gap 候选生成**
从知识库中做组合推导（不是灵感闪现）：
- Future Work A + Future Work B → 组合推导
- Assumption X (论文P) + 反例 Y (论文Q) → 质疑推导
- 方法 M 的局限 + 领域 C 的需求 → 迁移推导
- 主动做跨论文交叉搜索——AI 应同时关联 10+ 篇论文

**Step 2: Gap 评估矩阵**
对每个候选 Gap，按三维度评估：
| 维度 | 核心问题 |
|------|---------|
| 重要性 | 解决它对领域有多大影响？ |
| 新颖性 | 是否已被他人解决或正在被解决？ |
| 可解决性 | 以现有技术条件，是否有希望攻克？ |

**Step 3: Gap 根因分析**
对选定的 Gap 追问"为什么存在？"：
- 技术限制？（需要新方法）
- 错误假设？（需要重新建模）
- 被忽视的维度？（需要新视角）
根因直接决定 Phase R4 的方法方向。

**Step 4: RQ 公式化**
将 Gap 转化为具体的、可回答的、可验证的研究问题。

**Step 5: 初始化 contribution.md**
按 `templates/contribution.md` 模板初始化，记录当前阶段可见的潜在贡献。

**Step 6: 生成 gap-analysis.md**
按 `templates/gap-analysis.md` 模板输出。

### Revise 迭代（R3 审查返回）

1. 读 `gap-review.md`，逐条理解审查意见
2. 定位 `gap-analysis.md` 中的对应段落，针对性修改
3. 重点修复 Revise / Block 级维度；**不从零开始**
4. 更新 `gap-analysis.md`

### Pivot 迭代（L4 重启）

1. 读完整 `iteration-log.md`，理解所有已排除的 Gap 方向和根因
2. 读当前 `gap-analysis.md` 作参考
3. **严禁**重复 iteration-log.md 中已排除的方向
4. 在约束下重新从知识库组合推导新 Gap
5. 更新 `gap-analysis.md` 和 `contribution.md`

## AI Co-Author 关键行为
- 主动从知识库做组合搜索——人类难以同时关联 10+ 篇论文，AI 可以
- 对每个 Gap 进行批判性评估：是否真的是 Gap？是否已被解决？
- 隐式假设 > 显式 future work（后者人人都能看到，前者是差异化来源）
- 迭代时：严格遵守 iteration-log.md 中的"已排除方案"约束

## 输出
- `gap-analysis.md`
- `contribution.md`（初始化或更新）

## Exit Criteria
- [ ] 能用一句话说清"现有方法做了X，但因为Y所以存在Z问题"
- [ ] Gap 有明确的根因分析（技术限制 / 错误假设 / 被忽视维度）
- [ ] RQ 是具体的、可回答的、可验证的
- [ ] Gap 候选经过评估矩阵筛选
- [ ] contribution.md 已初始化
