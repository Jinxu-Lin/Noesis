# Skill: Paper Reading (论文深度阅读与知识沉淀) — Phase 0

## 触发场景
- 从 `reading-queue.md` 中选取高优先论文进行深度阅读
- 研究者直接提供论文进行阅读（跳过 discovery 流程）

## 输入
- 论文内容（PDF / arXiv URL / 粘贴的内容）
- `kb-index.md`（知识库索引，用于建立 cross-paper connections）
- `reading-queue.md`（如论文来自阅读队列，读取其 Quick Scan 摘要作为预读背景）
- (可选) 研究者的阅读重点或特定问题

## 执行流程

### Step 1: 预读准备
- 如果论文来自 `reading-queue.md`，读取其 Quick Scan 摘要，带着初步理解进入深读
- 读取 `kb-index.md`，了解当前知识库的覆盖范围，为 Step 4 的 cross-paper connections 做准备

### Step 2: 论文级深度理解
按以下维度系统阅读论文：
1. **Storyline & Motivation** — 问题是什么？为什么重要？叙事逻辑？
2. **Research Gap** — 作者认为现有工作缺了什么？
3. **Core Method** — 技术细节，保留关键公式和精确定义
4. **Experimental Design** — 数据集、baselines、metrics、消融设计
5. **Results & Conclusions** — 核心结论 + 作者自述的 limitations & future work

### Step 3: 知识库级资产提取
从论文中提取五类可复用资产：

**A. Methods Bank Entry**
- 该方法的核心机制（保留数学公式）
- 适用条件与边界
- 已知局限
- 潜在延伸方向（AI 主动分析，不限于作者所述）
- 方法中各组件的可解耦性分析

**B. Gaps & Questionable Assumptions**
- 作者声明的 limitations（显式）
- 作者未声明但可被质疑的假设（隐式）— **最高价值的提取**
- 未解决的问题
- 对每个隐式假设，评估其"可攻击性"（质疑它能否导向有价值的研究）

**C. Experimental Patterns**
- 领域通用的 baselines 和 metrics
- 值得借鉴的消融实验设计
- 数据集选择的逻辑
- 评估 pipeline 的可复用部分

**D. Cross-Paper Connections**
- 对照 `kb-index.md`，主动建立与已有论文的关联
- 标注关联类型：互补 / 矛盾 / 延伸 / 同类 / 可结合
- **重点关注**：两篇论文的方法可互补、或某论文的方法能填补另一论文的 gap
- 如果发现高价值 connection，向研究者主动提示

**E. Reusable Resources**
- 开源代码仓库：GitHub URL + stars + 维护状态（活跃/存档）+ 代码质量印象
- 公开数据集：名称 + 获取方式 + 规模 + 许可证
- 预训练模型：HuggingFace / 其他平台 URL + 模型规模 + 适用任务
- 可复用评估脚本/pipeline：如论文提供了评估代码，记录其路径和用法
- **目的**：为 Phase 8 实现阶段提供工程起点，避免从零构建

### Step 4: 上传至 NotebookLM
- 将论文上传到 NotebookLM 对应研究方向的 notebook 中
- 如果 notebook 不存在，创建一个
- 上传方式：优先使用 arXiv URL（NotebookLM 可直接解析），其次使用文本粘贴

### Step 5: 生成论文笔记
按 `templates/paper-reading-note.md` 模板输出，保存到知识库目录。

### Step 6: 更新知识库索引
更新 `kb-index.md`：
- 已读论文索引：新增论文条目
- Methods Bank 索引：新增方法条目
- Gaps & Assumptions 索引：新增 gap/假设条目
- Experimental Patterns 索引：新增模式条目
- Cross-Paper Connections 索引：新增关联条目
- Reusable Resources 索引：新增代码/数据集/模型条目
- 更新统计数字

### Step 7: 更新阅读队列
如论文来自 `reading-queue.md`，将其状态从"待读"更新为"已完成"，记录笔记文件路径。

### Step 7a: 更新领域地图（条件触发）
检查该论文所属研究方向在 `kb-index.md` 中的已读论文数量：
- **≥ 5 篇且 `domain-landscape.md` 不存在**：生成该方向的领域地图（按 `templates/domain-landscape.md` 模板）
- **已存在 `domain-landscape.md`**：基于新论文的资产更新相关章节（现状摘要、SOTA、方向饱和度、资源汇总）
- **< 5 篇**：跳过，积累不足以支撑方向级判断

领域地图包含：
1. 领域现状摘要（当前发展阶段、主流范式）
2. SOTA 方法与基准（最优方法、主流数据集、评估指标）
3. 方向饱和度评估（红海 vs 蓝海子方向）
4. 研究方向信号（有前景的方向、值得警惕的陷阱、跨领域启发）
5. 可用资源汇总（聚合该方向下所有论文的 Reusable Resources）

### Step 7.5: Git 提交 KB 更新
将本次阅读产出提交到项目仓库：
```bash
git add kb/[paper-id].md kb-index.md reading-queue.md
git commit -m "kb: add [论文标题简写] ([arXiv ID])"
```

如果当前在 worktree 分支（`kb/[arxiv-id]`），提交后通知协调 Agent 可以合并此分支。

### Step 8: 与研究者交互
- 确认理解是否准确
- 如果发现了高价值的 cross-paper connection 或隐式假设，主动提出
- 询问研究者是否有特别想深入的部分
- 如果发现的 connection 或 gap 可能触发项目启动（Phase 1），主动建议

## AI Co-Author 关键行为
- **AI 不仅是记录员，更是共同思考者**。在 Gaps & Assumptions 和 Cross-Paper Connections 中，AI 应主动贡献自己的分析
- 隐式假设的识别是核心差异化价值——重点标注"作者没意识到但可以被质疑"的假设
- 随着知识库增长，cross-paper connections 的涌现概率指数增长——每次深读都要与整个 KB 对照
- 组件可解耦性分析为 Phase 4 的方法设计提供直接素材
- 对 Methods Bank 的条目，要分析到组件级别，不只是笼统记录

## 输出
- 论文笔记文档（保存到知识库目录）
- `kb-index.md`（更新）
- `reading-queue.md`（更新，如适用）
- NotebookLM notebook（论文已上传）

## Exit Criteria
- [ ] 论文级理解完整（能说清 storyline、核心方法、实验设计）
- [ ] 至少提取了 1 个 Methods Bank 条目（含组件级分析）
- [ ] 至少识别了 1 个 Gap/隐式假设（含可攻击性评估）
- [ ] 已提取 Reusable Resources（开源代码/数据集/预训练模型，如有）
- [ ] 已与 kb-index.md 中的已有论文建立 connections（如有）
- [ ] 论文已上传至 NotebookLM
- [ ] kb-index.md 已更新
- [ ] reading-queue.md 已更新（如适用）
- [ ] 如该方向已读论文 ≥ 5 篇，domain-landscape.md 已生成或更新
- [ ] KB 更新已 git commit（worktree 场景已通知协调 Agent 可合并）

## 完成后
提示用户：论文深度阅读完成，知识库已更新。如果阅读队列中还有高优先论文，建议继续执行 `/paper-reading`。
然后执行 `/reflect-pipeline` 对本阶段的流程进行反思，记录改进观察。
