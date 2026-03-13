# Skill: Paper Outline (论文大纲) — Phase P1

## 触发场景
项目进入论文写作模块（`/praxis-paper`），需要从研究文档映射出论文结构。

## 输入
- `project-startup.md` — 背景材料、研究动机
- `research/problem-statement.md` — Gap 定义、RQ、根因分析
- `research/method-design.md` — 方法框架、因果论证
- `research/experiment-design.md` — 实验设计
- `research/contribution.md` — 贡献列表
- `Codes/` 目录 — 实验结果、图表

## 执行流程

### Step 1: 审查研究素材

完整阅读所有输入文档，建立以下映射关系：

**1.1 叙事脊柱构建**

好的论文像一个精心设计的故事，有四个核心张力节点：
- **张力建立（Gap）**：当前领域看似没问题，但实际上存在一个被忽视或未解决的根本性问题
- **洞察转折（Insight）**：我们发现了一个独特的切入角度——不是暴力堆叠，而是对问题本质的深刻理解
- **方案展开（Method）**：基于这个洞察，我们设计了一个优雅且自洽的解决方案
- **验证闭环（Experiments）**：实验不仅证明方法有效，还验证了我们的核心洞察确实成立

构建叙事脊柱时，问自己：**"如果审稿人只记住一件事，那应该是什么？"** 这个"一件事"就是论文的 key insight，整个叙事都应该围绕它展开。

**1.2 素材清单**：每个文档中哪些内容会映射到论文的哪个章节

**1.3 图表清单**：Codes/ 中已有的实验结果图表，以及需要新制作的图表

### Step 2: 确定目标会议/期刊与论文类型

**2.1 目标会议/期刊**

检查 `project-startup.md` 中是否指定了目标会议/期刊。如果没有，在 outline 中标注为 TBD，但按通用 ML 会议格式（8-10 页）规划。

**2.2 论文类型判定**

根据研究内容的性质，确定论文属于哪种类型，不同类型的篇幅分配策略不同：

| 论文类型 | Method 占比 | Experiments 占比 | 核心卖点 | 典型标志 |
|---------|------------|-----------------|---------|---------|
| **Method-Heavy** | 40-45% | 30-35% | 方法的创新性和理论优雅性 | 有新 loss、新架构、新训练范式 |
| **Experiment-Heavy** | 20-25% | 45-50% | 大规模实验揭示的洞察 | Scaling law、benchmark study、empirical finding |
| **Analysis Paper** | 15-20% | 50-55% | 对现有方法/现象的深入理解 | "Why does X work?"、failure mode analysis |
| **System Paper** | 30-35% | 35-40% | 系统设计 + 工程贡献 | 端到端系统、新 benchmark、新数据集 |

这个判定将影响 Step 3 的篇幅分配和叙事重心。

### Step 3: 确定写作顺序与叙事策略

**为什么要先写 Method 再写 Introduction**：Method 是论文的"事实"，它决定了 story 的方向。先写 Method，才能知道 Introduction 应该如何 setup gap、如何 motivate 方法。如果先写 Introduction，容易陷入过度承诺（promise 了 Method 没做到的事）或承诺不足（Method 的精妙之处在 Introduction 没有铺垫）。

**推荐写作顺序**：Method → Experiments → Introduction → Related Work → Conclusion → Abstract

**叙事策略选择**：
- **对比式叙事**（适合有明确 baseline 改进的工作）：先展示现有方法的不足，再展示我们的解法
- **洞察驱动叙事**（适合有独特 insight 的工作）：先阐述一个被忽视的观察/发现，再基于它构建方法
- **问题驱动叙事**（适合解决明确 failure case 的工作）：先展示 failure case，分析根因，再提出解决方案

在 outline 中明确选择哪种叙事策略，并说明理由。

### Step 4: 生成论文大纲

产出 `Papers/outline.md`，包含：

#### 4.1 论文元信息
- 暂定标题（2-3 个候选）
  - **标题策略**：好标题 = 方法名 + 核心 idea 的一句话概括。避免过长（≤12 词为佳）。DL 领域标题惯例：动词短语（"Learning to..."）或名词短语（"X: A Y for Z"）。如果方法有独特命名，放在标题中增加辨识度
- 目标会议/期刊
- 论文类型（Step 2 的判定结果）
- 页数限制
- 核心叙事策略

#### 4.2 章节大纲
对每个章节（Abstract, Introduction, Related Work, Method, Experiments, Conclusion）提供：
- **核心论点**：该章节要传达的 1-2 个核心信息
- **素材映射**：从哪些文档的哪些部分提取内容
- **预估篇幅**：占总篇幅的百分比（参照 Step 2 的论文类型分配）
- **子节结构**：2 级子标题
- **章节间逻辑衔接**：上一章节如何过渡到本章节（一句话描述过渡逻辑）

**各章节大纲要点**：

- **Abstract**：最后写。标注依赖哪些章节的核心数据
- **Introduction**：
  - 规划段落级结构（通常 4-5 段），每段的核心功能明确
  - 第 4 段"In this paper, we..."之后，贡献列表直接来自 `research/contribution.md`
  - 是否需要 Figure 1 在 Introduction 中展示（大多数顶会论文需要）
- **Related Work**：
  - 规划按哪些主题分组（不按时间线）
  - 每组结尾如何落脚到本文的差异点
  - 注意：Related Work 可以放在 Method 之后（适合方法理解门槛高的论文）
- **Method**：
  - 是否需要 Preliminary/Background 子节（引入 notation 和背景知识）
  - Overview → 各组件详细展开 → 训练/推理流程
  - 每个设计选择对应一个 motivation（"为什么这样设计"比"怎样设计"更重要）
- **Experiments**：
  - 规划实验呈现顺序 = 论证顺序（先主 claim → 再组件验证 → 再深入分析）
  - 哪些实验用表格、哪些用图
  - 是否需要 Case Study / 可视化 / Error Analysis 子节
- **Conclusion**：
  - Limitations 子节（审稿人必看，诚实 > 回避）
  - Future Work（基于 limitations 自然延伸，不天马行空）

#### 4.3 Figure 与 Table 规划

**Figure 规划原则**：
- **Figure 1（全文视觉摘要）**：这是审稿人打开论文最先看的东西，决定第一印象。Figure 1 应该在一张图中传达论文的核心 idea——要么是方法的 high-level overview + 关键 insight 的直观展示，要么是问题的直观展示（现有方法 vs 我们的方法）。信息密度要高但不拥挤
- **Method Figure（架构图）**：信息密度是关键。包含所有必要组件但不过度详细。用颜色编码区分不同模块。数据流方向统一（左→右或上→下）。Loss function 的作用点要标注。如有多个 loss 或多阶段训练，用虚线/实线区分
- **实验图表**：
  - 表格用于精确数值对比（main results 通常用表格）
  - 折线图/柱状图用于趋势展示（ablation、scaling、sensitivity analysis）
  - 热力图/可视化用于定性分析（attention map、feature visualization）
  - 每个图表要有明确的 takeaway message
- **Figure 数量建议**：8 页论文通常 4-6 个 figure + 2-4 个 table。过多导致挤压正文空间，过少导致论文"文字墙"

| 图/表编号 | 类型 | 内容描述 | 核心 Takeaway | 数据来源 | 所在章节 |
|-----------|------|---------|--------------|---------|---------|
| Fig.1 | Concept | 方法核心 idea 的视觉摘要 | 一句话说清方法的直觉 | method-design.md | Intro/Method |
| Fig.2 | Framework | 方法整体架构 | 组件间关系和数据流 | method-design.md | Method |
| Tab.1 | Results | 主实验结果 | 我们的方法在 X 上超越 SOTA | Codes/ | Experiments |
| ... | ... | ... | ... | ... | ... |

#### 4.4 叙事一致性检查
- research/contribution.md 中每个贡献 → 在论文中如何论证（Method 的哪个子节）和验证（Experiments 的哪个子节）
- 每个实验 → 验证哪个 claim
- 确保无悬空贡献（有 claim 无验证）和无悬空实验（有验证无 claim）
- **Contribution-Evidence 对齐矩阵**：

| 贡献 | Method 论证位置 | Experiment 验证位置 | 验证强度 |
|------|---------------|-------------------|---------|
| C1: ... | §3.2 | Tab.1, Fig.4 | 定量+定性 |
| C2: ... | §3.3 | Tab.2 (ablation) | 定量 |
| ... | ... | ... | ... |

### Step 5: 生成符号表

产出 `Papers/notation.md`：
- 统一全文的数学符号和缩写
- 避免同一概念在不同章节使用不同符号
- **符号选择原则**：遵循领域惯例（如 $\theta$ 表示模型参数、$\mathcal{L}$ 表示 loss、$\mathcal{D}$ 表示数据集）；输入输出用 $x, y$；中间表示用 $h, z$；集合用花体字母；矩阵用大写粗体；向量用小写粗体
- 格式：`| 符号 | 含义 | 首次出现 |`

## AI Co-Author 关键行为
- 从研究文档**映射**到论文结构，而非从零创作
- 叙事脊柱必须与 research/problem-statement → research/method-design → experiments 的逻辑链一致
- 大纲阶段不写正文，只规划结构和素材映射
- 图表规划要考虑审稿人的阅读体验——审稿人通常先看 Abstract → Figure 1 → 实验表格 → 再决定是否细读
- **"一个 insight 贯穿全文"原则**：从 Introduction 的 motivation 到 Method 的每个设计选择到 Experiments 的每个验证，都应该围绕同一个核心 insight 展开
- **思考对标论文**：在叙事策略和篇幅分配上，参考领域内与本文最相似的已发表顶会论文

## 输出
- `Papers/outline.md` — 论文大纲
- `Papers/notation.md` — 符号表

## Exit Criteria
- [ ] 叙事脊柱完整（Gap → 洞察 → 方法 → 验证 → 贡献），核心 insight 明确
- [ ] 论文类型已判定，篇幅分配与类型匹配
- [ ] 叙事策略已选择并说明理由
- [ ] 每个贡献都有对应的论证和验证路径（Contribution-Evidence 矩阵完成）
- [ ] Figure 规划覆盖关键结果，Figure 1 的功能明确
- [ ] 符号表统一且无歧义，遵循领域惯例
- [ ] 章节篇幅分配合理，章节间逻辑衔接明确
- [ ] 写作顺序已规划（Method → Experiments → Introduction → ...）
