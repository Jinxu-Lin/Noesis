# Skill: Paper Reading (论文阅读与知识沉淀)

## 触发场景
研究者提供论文（PDF / arXiv / 粘贴的内容），希望 AI 帮助理解并将知识沉淀到知识库中。

## 输入
- 论文内容（任意形式）
- (可选) 研究者的阅读重点或问题
- (可选) 已有知识库的索引，用于建立 cross-paper connections

## 执行流程

### Step 1: 论文级深度理解
按以下维度系统阅读论文：
1. **Storyline & Motivation** — 问题是什么？为什么重要？叙事逻辑？
2. **Research Gap** — 作者认为现有工作缺了什么？
3. **Core Method** — 技术细节，保留关键公式
4. **Experimental Design** — 数据集、baselines、metrics、消融设计
5. **Results & Conclusions** — 核心结论 + 作者自述的 limitations & future work

### Step 2: 知识库级资产提取
从论文中提取四类可复用资产：

**A. Methods Bank Entry**
- 该方法的核心机制
- 适用条件与边界
- 已知局限
- 潜在延伸方向（AI 主动分析，不限于作者所述）

**B. Gaps & Questionable Assumptions**
- 作者声明的 limitations（显式）
- 作者未声明但可被质疑的假设（隐式）— 这是最高价值的提取
- 未解决的问题

**C. Experimental Patterns**
- 领域通用的 baselines 和 metrics
- 值得借鉴的消融实验设计
- 数据集选择的逻辑

**D. Cross-Paper Connections**
- 如果有已有知识库，主动建立关联
- 标注关联类型：互补 / 矛盾 / 延伸 / 同类 / 可结合
- 如果发现两篇论文的方法可互补或某论文的方法能填补另一论文的 gap，**主动向研究者提示**——这是 AI 作为"共同思考者"的关键价值

### Step 3: 生成文档
按 `templates/paper-reading-note.md` 模板输出。

### Step 4: 与研究者交互
- 确认理解是否准确
- 如果 AI 在 Step 2D 中发现了有价值的 cross-paper connection，主动提出
- 询问研究者是否有特别想深入的部分

## 输出
- 单篇论文笔记文档
- (如有) 对知识库索引的更新建议

## 关键原则
- **AI 不仅是记录员，更是共同思考者**。在 Gaps & Assumptions 和 Cross-Paper Connections 中，AI 应主动贡献自己的分析，而不仅仅是摘录论文原文。
- 隐式假设的识别是区分"AI 辅助阅读"和"自己读论文"的核心差异化价值。
- 知识库的价值随积累量指数增长——论文越多，cross-paper connections 越丰富，涌现洞察的概率越高。
