# Skill: Research Retrospective (研究设计回顾与知识回收) — Phase R11

## 触发场景
R8 Implementation Planning 完成后自动执行，在进入人工编码阶段之前。

此时研究设计已完全确定（Gap → Method → Experiment → Impl Plan），实验尚未运行。
这是将研究设计决策沉淀为 Episteme 知识资产的最佳时机。

## 角色
你是这个项目研究设计阶段的**知识萃取者**。你的任务是将 R1-R8 阶段形成的研究设计决策，转化为 Episteme 知识库中可复用的结构化资产，标注为"设计阶段（待实验验证）"。

## 输入
- `research/gap-analysis.md` — Gap 发现与 RQ 定义
- `research/method-design.md` — 方法设计文档
- `research/experiment-design.md` — 实验设计文档
- `Codes/code-todo.md`、`Codes/experiment-todo.md` — 实现规划
- `iteration-log.md`（如有，记录 R2-R8 中的迭代历史）
- `pipeline-evolution-log.md`（如有，供 /praxis-evolve 后续使用，本阶段不处理）
- `retrospective.md` 模板（`~/Research/Noesis/Praxis/templates/retrospective.md`）

## 执行流程

### Step 1: 研究设计时间线重建

回顾从 R1 到 R8 的关键决策节点：
- 选择了什么 Gap？为什么选这个而不是其他候选？
- 方法设计经历了哪些迭代？哪些方向被放弃，原因是什么？
- 实验设计中做了哪些重要取舍？
- 如果 iteration-log.md 存在，提取研究设计阶段的迭代模式

产出：关键决策时间线表格

### Step 2: 研究设计质量评估

**研究定位（Gap）**：
- 这个 Gap 的重要性和可解性如何？有多大把握它是真实的 Gap？
- Gap 的界定是否足够精确，不会被已有工作覆盖？
- 这是本次迭代中排除过的 Gap 吗？如果是，记录为什么重新选择

**方法设计**：
- 方法的核心 insight 是什么？它解决 Gap 的逻辑链是否严密？
- 方法中有哪些关键假设？哪些是高风险假设（实验可能证伪）？
- 哪些组件是创新的，哪些是直接借用已有工作的？

**实验设计**：
- Dim 0 快速验证方案的通过标准是否清晰可测？
- 实验覆盖了所有 RQ 吗？消融设计是否完整？
- 有哪些潜在的实验陷阱或评估风险需要特别注意？

### Step 3: 知识库资产提取（标注为"待验证"）

将研究设计决策提取为四类 Episteme 资产，所有条目标注 `[? 待实验验证]`：

#### Methods Bank — 新增条目
提取本项目提出的方法：
- 方法名称、核心思路、所解决的问题类型
- 关键组件及其设计原理
- 预期适用场景与局限性（基于设计逻辑，非实验验证）
- 标注：`[? 待实验验证] 来源项目：<项目名>`

#### Gaps & Assumptions — 新增/更新条目
- 本项目针对的 Gap：标记为 `[in-progress]`
- 方法设计的核心假设列表：每条标注置信度（高/中/低）
- 被排除的 Gap 候选：记录排除原因（避免未来重复探索）

#### Experimental Patterns — 新增条目
提取本次实验设计的方案：
- Dim 0 快速验证方案（baseline + 通过标准）
- 核心实验结构（对比设置、消融策略）
- 选择的 metrics 及理由
- 标注：`[? 设计阶段，未经验证]`

#### Cross-Paper Connections — 新增条目
- 本方法与哪些已有工作存在关联、借鉴或竞争关系
- 发现的潜在协同（跨域迁移机会）

### Step 4: 写入 retrospective.md

按 `templates/retrospective.md` 模板生成研究设计阶段回顾文档。
**注意**：此时是研究设计回顾，不是项目最终总结。实验结果部分留空或标注"待实验填充"。

### Step 5: 执行知识库更新

将 Step 3 提取的资产**实际写入 Episteme 知识库**（路径：`~/Research/Episteme/`）：
- 写入 Methods Bank 新条目
- 更新 Gaps & Assumptions（新 Gap 标记 in-progress，新假设列表）
- 写入 Experimental Patterns 新条目
- 写入 Cross-Paper Connections 新条目

提交：
```bash
cd <project_path>
git add retrospective.md
git commit -m "R11: research design retrospective"
git push origin main

cd ~/Research/Episteme
git add .
git commit -m "update: [项目名] research design knowledge assets (pending validation)"
git push origin main
```

## 关键行为原则
- **此时没有实验结果**——所有知识资产标注为"待验证"，这是正确的，不是缺陷
- **高风险假设要明确列出**——这是给未来自己的预警，实验失败时可以快速定位原因
- **被放弃的 Gap 和方向同样宝贵**——记录为"已探索并排除"，避免未来项目重复走弯路
- **实验设计的细节要完整记录**——Dim 0 方案尤其重要，实验成功与否的判断标准现在最清晰
- `pipeline-evolution-log.md` 留给 `/praxis-evolve` 处理，本阶段不处理框架改进

## 输出
- `retrospective.md`（研究设计阶段回顾，实验结果部分留白）
- Episteme 四类资产更新（全部标注待验证）

## Exit Criteria
- [ ] retrospective.md 完成，包含决策时间线和设计质量评估
- [ ] Methods Bank 新条目已写入（标注待验证）
- [ ] Gaps & Assumptions 已更新（新 Gap 标记 in-progress，假设列表完整）
- [ ] Experimental Patterns 新条目已写入
- [ ] Cross-Paper Connections 已更新
- [ ] 项目 repo 和 Episteme 均已 commit + push
