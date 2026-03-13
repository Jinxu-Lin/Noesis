# Skill: Paper Sections Writing (章节写作) — Phase P2

## 触发场景
P1 大纲完成，按照大纲顺序写作各章节。

## 输入
- `Papers/outline.md` — 论文大纲（结构、素材映射、图表规划）
- `Papers/notation.md` — 符号表
- `research/problem-statement.md`、`research/method-design.md`、`research/experiment-design.md` — 研究文档
- `research/contribution.md` — 贡献列表
- `project-startup.md` — 背景材料
- `Codes/` — 实验结果、图表

## 执行流程

### 写作模式选择（执行前先确认）

在开始写作前，尝试调用 `codex-cli` 检测 Codex MCP 是否可用：

**模式 A — Codex 辅助写作**（Codex MCP 可用时）：
1. 按照 `Praxis/prompts/codex-writer-prompt.md` 的步骤，逐章节委托 Codex 起草初稿
2. Codex 草稿保存到 `Papers/sections/<section_id>-codex-draft.md`
3. 对每个草稿执行 Claude 精炼（见下方各章节的"精炼要点"）：
   - 填充 `[RESULT: ...]` 占位符（来自实际实验数据）
   - 修正符号/术语不一致
   - 删除虚构内容，补充来自研究文档的细节
   - 将精炼后版本保存为 `Papers/sections/<section_id>.md`
4. 继续执行 Step 7（可选跨章节一致性审查）

**模式 B — Claude 直接写作**（Codex MCP 不可用，non-blocking）：
- 按以下 Steps 1-6 顺序直接写作，跳过 Codex 相关步骤

---

**严格按以下顺序写作**，每个章节单独产出一个文件到 `Papers/sections/` 目录。

### Step 1: Method (`Papers/sections/method.md`)

**为什么第一个写 Method**：Method 是论文的事实基础。先写 Method 确定了"我们到底做了什么"，之后的 Introduction 才知道如何 setup story，Experiments 才知道验证什么。

- **素材来源**：`research/method-design.md` 直接转化
- **结构模板**：
  1. **Overview / Problem Formulation**（0.5-1 页）：先给读者 big picture。用一段文字或一个 overview figure 让读者在深入细节之前理解方法的整体思路。明确定义输入/输出、问题形式化（$\text{Given } X, \text{ find } Y \text{ such that } Z$）
  2. **各组件详细展开**（按逻辑顺序，非按代码结构）：每个子节对应一个方法组件。关键模式——**Motivation → Design → Formulation**：先说"为什么需要这个组件"（1-2 句），再说"我们如何设计"（直觉解释），最后给出数学形式化。避免直接甩公式而不解释动机
  3. **Training / Inference**（0.5 页）：完整的 Loss function（各项 loss 如何组合）、训练流程、推理流程。如果 training 和 inference 有差异（如 dropout、teacher forcing），要明确说明
- **数学写作要点**：
  - 每个公式都要有前导文字（"We define the attention score as:"），不要突然出现公式
  - 重要公式用独立编号（`\begin{equation}`），辅助推导用 inline 或 align
  - 复杂公式紧跟一句直觉解释（"Intuitively, this measures..."）
  - 符号首次出现时定义，使用 `notation.md` 统一
- 包含方法图（Framework Figure）描述——说明图中应包含的元素和布局
- **不发明新方法**——所有内容必须来自 `research/method-design.md`
- **模式 A 精炼要点**：检查所有数学符号是否与 `notation.md` 完全一致；确认 Framework Figure 描述完整；删除任何 Codex 补充的超出 `research/method-design.md` 范围的技术细节

### Step 2: Experiments (`Papers/sections/experiments.md`)

- **素材来源**：`research/experiment-design.md` + `Codes/` 实验结果
- **结构**（按论证顺序组织，不是按实验执行顺序）：
  1. **Experimental Setup**（0.5-1 页）：
     - 数据集：名称、规模、划分方式、预处理。如果使用标准 benchmark，引用原文并说明版本
     - Baselines：每个 baseline 一句话说明，引用原文。选择 baseline 的理由（为什么选这些而不是其他）。确保包含最近 1-2 年的 SOTA
     - 评估指标：每个指标的定义或引用。如果使用不常见指标，解释选择理由
     - 实现细节：关键超参数（learning rate、batch size、optimizer、scheduler）、硬件、训练时长。可放在附录但主文至少列出最关键的
  2. **Main Results**（1-1.5 页）：
     - 主表/主图展示核心对比。表格设计：最好的结果加粗，次好的下划线。每列对齐，数字保留合适的小数位
     - 分析不是复述数字（"Our method achieves 85.3%"），而是解释 pattern（"The improvement is more pronounced on X, suggesting that our method particularly benefits..."）
     - 如果有些 baseline 上没有提升或提升微弱，诚实讨论原因
  3. **Ablation Study**（0.5-1 页）：
     - 每个消融实验验证一个设计选择。标准做法：移除或替换一个组件，观察性能变化
     - 消融顺序 = 重要性顺序（最核心的组件先消融）
     - 分析：不仅报告数字，还要解释"为什么移除 X 导致下降 Y%"
  4. **Analysis / Case Study**（0.5-1 页，视论文类型而定）：
     - 可视化：attention map、feature distribution、t-SNE 等
     - Error analysis：失败案例分析，什么类型的输入方法表现不好
     - Sensitivity analysis / hyperparameter study（如空间允许）
     - 这部分展示你对方法行为的深入理解，而非仅仅"方法 work 了"
- **实验写作的关键原则**：
  - 每个实验都明确说清"它验证了什么 claim"（对应 contribution.md 中的哪条贡献）
  - 表格和图的 caption 要**自包含**（只读 caption 就能理解图表内容、设置和核心结论）
  - 与 baselines 对比要公平：相同数据集、相同评估指标、相同数据划分
  - **不 cherry-pick**：如果在某些设置下没有提升，要报告并讨论
  - 报告 variance / std：如果实验涉及随机性（如不同 seed），报告多次运行的均值和标准差
- **模式 A 精炼要点**：填充所有 `[RESULT: ...]` 占位符（来自 `Codes/` 实际数据）；确认所有 baseline 数字与 `research/experiment-design.md` 一致；删除 Codex 可能虚构的数字

### Step 3: Introduction (`Papers/sections/intro.md`)

- **素材来源**：`research/problem-statement.md` + `research/contribution.md` + `project-startup.md`
- **段落级结构**（约 4-5 段，1.5-2 页含 Figure 1）：

  **第 1 段：定义领域和建立重要性（3-5 句）**
  - 开头一句话定义研究领域/任务，让非专家也能理解
  - 快速建立"这个问题很重要"——可以是应用价值、理论意义、或领域关注度
  - 不要从太远的地方开始（不要"深度学习在过去十年取得了..."），直接切入具体领域
  - 好的开头模式：直接陈述任务 → 为什么重要 → 近期进展概述

  **第 2 段：现有方法与它们的局限性——Gap Setup（4-6 句）**
  - 概述现有方法的主流范式（1-2 类主要方法）
  - 指出它们的共同局限性——这就是 Gap
  - Gap 的描述要**具体**（不是"现有方法有局限"，而是"现有方法假设 X，但实际上 Y"）
  - 可以用一个具体的例子/failure case 让 gap 更直观
  - **关键技巧**：Gap 的措辞要自然地引出你的方法——读者读完 Gap 应该能预感到解决方向

  **第 3 段："In this paper, we..." — Contribution Statement（3-5 句）**
  - 一句话概述方法的核心 idea（key insight）
  - 简述方法的 high-level 工作方式（1-2 句，对应 Method 节的 overview）
  - 可以在这里引用 Figure 1（"As illustrated in Figure 1, ..."）

  **第 4 段：贡献列表**
  - 贡献列表使用 bullet points，每个贡献 1-2 句
  - 贡献表述 = 做了什么 + 效果/意义（"We propose X, which achieves Y"）
  - 贡献**直接来自 `research/contribution.md`**——不在论文中发明新贡献
  - 每个 claim 都必须在 Experiments 中有对应验证
  - 通常 3-4 条贡献：方法贡献 + 实验/分析贡献 + 实用贡献（代码/数据集开源等）

  **第 5 段（可选）：论文结构导读（1-2 句）**
  - "The rest of this paper is organized as follows..." 有些会议论文省略

- **Introduction 写作反模式（避免）**：
  - 开头段落过于宏大（"AI is transforming the world..."）
  - Gap 描述模糊（"existing methods have limitations"而不说具体什么 limitation）
  - 过度承诺（"we solve this problem"——用"we address/tackle"更安全）
  - 贡献条目不可验证（"we provide insights"——insights 是什么？怎么验证？）

### Step 4: Related Work (`Papers/sections/related_work.md`)

- **素材来源**：`project-startup.md` + 知识库（如可用）
- **核心定位**：Related Work 不是文献列表，而是**"我们的工作如何定位在已有工作的景观中"**。它的功能是：(1) 证明你了解领域，(2) 证明你的工作确实是新的，(3) 帮读者理解技术脉络

- **组织结构**：按**主题/技术路线**分组，不按时间线。每组：
  - 组标题 = 一个研究方向/技术类别
  - 组内按技术演进逻辑排列（不一定是时间顺序）
  - 每段结尾用 1-2 句说明与本文的关系/差异（"Unlike these approaches, our method..."或"Our work is complementary to..."）

- **写作要点**：
  - 每个被引用的工作都要说清：做了什么（1 句）、与我们的关系（1 句）
  - 不要过度贬低 prior work（"X fails to..."→ "X focuses on... rather than..."）——审稿人可能就是那些工作的作者
  - 如果有直接竞争的同期工作（concurrent work），要明确说明差异
  - Related Work 的最后一段或最后几句应该收束到"以上所有工作都没有解决 X，这正是我们的切入点"

- **常见遗漏检查**：
  - 是否覆盖了最近 1-2 年（尤其是最近 6 个月）的相关工作？
  - 是否覆盖了方法所借鉴的技术来源（即使不在同一领域）？
  - 是否覆盖了使用相同 benchmark/数据集的工作？

- 如果素材不足，在文件末尾标注"需要补充阅读的方向"

### Step 5: Conclusion (`Papers/sections/conclusion.md`)

- **结构**（0.5-0.75 页）：

  **总结段**（3-5 句）：
  - 不是重复 Abstract，而是更高层次的反思
  - 模式：我们做了什么（1 句）→ 核心发现/insight（1 句）→ 实验验证了什么（1 句）→ 意义（1 句）
  - 用不同的措辞重新表达，避免与 Abstract 完全重复

  **Limitations 子节**：
  - 诚实列出 2-3 个主要限制。审稿人能看出来的限制你不提，比你主动提出来更减分
  - 常见的合理 limitations：计算成本、特定领域/数据的假设、scaling 行为未充分验证、某些 edge case 处理不好
  - **技巧**：将 limitation 框定为"有意识的 trade-off"而非"缺陷"（"We trade X for Y, which may limit..."）

  **Future Work 子节**：
  - 基于 limitations 自然延伸，不要天马行空
  - 1-3 个具体的后续方向，每个 1-2 句
  - 好的 future work 应该让读者感觉"这个方向确实值得继续探索"

### Step 6: Abstract (`Papers/sections/abstract.md`)

- **最后写**——此时全文已定型
- **结构**（4-6 句，150-250 词）：
  1. **问题**（1 句）：定义任务 + 现有方法的关键局限
  2. **方法**（1-2 句）：我们提出了什么 + 核心 idea 的一句话概括
  3. **结果**（1-2 句）：关键定量结果（"achieves X% on Y, outperforming Z by W%"）
  4. **意义**（0-1 句）：更广泛的影响（可选）
- **写作要点**：
  - 不使用"In this paper, we..."等套话——直接陈述
  - 数字要具体且与正文一致
  - 避免模糊的定性表述（"significantly improves" → "improves by 5.3%"）
  - 不要引入正文中没有的概念或 claim
  - **自包含**：不引用文献、不引用图表编号
- **模式 A 精炼要点**：确认摘要中的数字与 Experiments 节一致；确认贡献表述与 `research/contribution.md` 对齐

### Step 7（可选）: 外部 AI 跨章节一致性审查

如果系统配置了外部 AI MCP（如 Codex / GPT-5.4），在所有章节写完后，调用外部模型对全文进行跨章节一致性审查。

**执行条件**：尝试调用 `mcp__codex__codex` tool。如果 MCP 不可用，跳过本步骤。

**外部审查 Prompt**：
- 将所有 6 个章节的完整内容传入
- 要求检查：
  1. **术语一致性**：同一概念是否使用了不同表述？
  2. **叙事连贯性**：Introduction 的 claim 是否在 Method/Experiments 中得到充分支撑？
  3. **逻辑断裂**：章节间是否有信息断层或矛盾？
  4. **贡献对齐**：每个贡献是否在实验中有对应验证？
  5. **改进建议**：具体的修改方案
- 设置 `approval-policy: "never"`，中文输出

**结果处理**：
- 成功：写入 `Papers/sections/external-review.md`，供 P3/P4 参考
- 失败：跳过（non-blocking），不影响 P2 产出

## 写作反模式清单（全文通用，每个章节写完后对照检查）

| 反模式 | 描述 | 修正 |
|--------|------|------|
| **过度 Claim** | "significantly outperforms" 但提升 < 2% | 用具体数字替代模糊副词 |
| **模糊 Contribution** | "we propose a novel method" 但不说 novel 在哪 | 说清楚 novelty 的具体内容 |
| **缺少 Limitations** | 全文无 limitation 讨论 | Conclusion 中增加 Limitations 子节 |
| **贡献膨胀** | 把"我们在 X 上做了实验"列为贡献 | 只有真正的创新性工作才是贡献 |
| **Notation 不一致** | 同一变量在不同章节用不同符号 | 严格遵守 notation.md |
| **断裂的逻辑链** | Introduction 的 gap 与 Method 的设计动机不对应 | 确保 Gap → Method 的因果链完整 |
| **复述数字** | 实验分析只是"我们取得了 X%"的复读 | 分析 pattern 和原因，而非复述表格 |
| **过度贬低 Prior Work** | "Prior methods completely fail to..." | 用中性语言描述差异 |
| **遗漏误差报告** | 实验结果无 std / confidence interval | 多次运行取均值±标准差 |

## AI Co-Author 关键行为
- 从研究文档**提取和转化**素材，不是创造新内容
- 确保跨章节的**术语一致性**（参考 notation.md）
- 确保**叙事一致性**：Introduction 的 claim = Method 的方法 = Experiments 的验证
- 学术论文语言：精确、简洁、客观，避免夸大（"dramatically improves" → "improves by X%"）
- 每个章节写完后，快速检查与 outline.md 的一致性
- **段落结构**：每段有 topic sentence，中间展开论证，结尾过渡到下一段。避免一段话内讨论多个主题
- **被动语态 vs 主动语态**："We propose" 比 "A method is proposed" 更直接有力。DL 领域论文普遍使用 "we" 主语

## 输出

**必须产出（两种模式均适用）**：
- `Papers/sections/method.md`
- `Papers/sections/experiments.md`
- `Papers/sections/intro.md`
- `Papers/sections/related_work.md`
- `Papers/sections/conclusion.md`
- `Papers/sections/abstract.md`

**模式 A 额外产出（Codex 可用时）**：
- `Papers/sections/<section_id>-codex-draft.md`（6 份 Codex 原始草稿，供 P3/P4 审查时对比参考）
- `Papers/sections/codex-writer-summary.md`（草稿质量说明与已知问题列表）

**可选产出（Step 7）**：
- `Papers/sections/external-review.md`（Codex 跨章节一致性审查，依赖外部 AI MCP）

## Exit Criteria
- [ ] 所有 6 个章节文件已生成
- [ ] 符号使用与 notation.md 一致
- [ ] Introduction 中每个贡献在 Experiments 中有对应验证
- [ ] 无凭空内容（所有内容可追溯到研究文档）
- [ ] 各章节篇幅与 outline.md 规划大致匹配
- [ ] 语言学术规范，无夸大和主观表述
- [ ] 写作反模式清单逐项检查通过
- [ ] 每个数学公式有前导文字和直觉解释
- [ ] 实验分析不是数字复述，而是 pattern 解释
