# Skill: Paper Cross-Review Critique (多角色审查) — Phase P3

## 触发场景
P2 章节写作完成，需要从多个审稿人视角对全文进行独立审查。

## 输入
- `Papers/sections/` — 所有章节文件
- `Papers/outline.md` — 论文大纲
- `Papers/notation.md` — 符号表
- `research/contribution.md` — 贡献列表
- `research/method-design.md` — 方法设计（用于验证论文是否准确反映方法）
- `research/experiment-design.md` — 实验设计（用于验证论文是否准确反映实验）

## 执行流程

### Step 1: 组装全文

将 `Papers/sections/` 中的所有章节按顺序拼接，形成完整的论文草稿视图。阅读并理解全文。

### Step 2: 执行 5 角色审查

依次以 5 个不同的审稿人角色审查全文。每个角色关注不同维度，产出独立的审查报告。

使用 `Praxis/subagents/paper-critic-subagent.md` 模板，分别以以下 5 个角色执行审查：

#### Role 1: Novelty Critic (新颖性审查)

**审稿人画像**：你是该领域的资深研究者，发表过 20+ 篇论文，对领域内的技术脉络和近期进展了如指掌。你判断新颖性的标准不是"是否没人做过完全一样的事"，而是"是否提供了新的理解或新的能力"。

**审查维度**：
- **增量改进 vs 本质创新**：
  - 方法是现有技术的简单组合/堆叠（A+B），还是有新的 insight 驱动的创新？
  - 如果是组合，组合本身是否带来了超越各部分之和的效果？组合的 insight 是什么？
  - 技术洞察的深度：是表面的工程改进（换了个 attention 机制），还是对问题本质有新的理解？
- **与最相关 Prior Work 的区分度**：
  - 找到与本文最接近的 1-3 篇已发表工作，逐一分析差异
  - 差异是否在技术上 substantial 且在效果上 meaningful？
  - 如果审稿人问"这和 [具体论文] 有什么区别？"，论文是否给出了令人信服的回答？
- **Related Work 完整性**：
  - 是否遗漏了关键的竞争工作？尤其是最近 6 个月的 arXiv 预印本
  - 是否遗漏了方法所借鉴的技术的原始出处？
  - 是否有明显的"选择性引用"——只引用支持自己叙事的工作而忽略质疑自己叙事的工作？
- **Novelty 表述的诚实性**：
  - 论文是否过度声称新颖性？（"first to..."——是否真的是 first？）
  - 贡献的表述是否与实际的技术创新匹配？

#### Role 2: Soundness Critic (严谨性审查)

**审稿人画像**：你是注重理论严谨性的研究者，习惯从数学推导和逻辑链条中找漏洞。你的标准是"每一步推理都要有依据"。

**审查维度**：
- **方法描述的完整性与可复现性**：
  - 给定论文描述，一个该领域的 PhD 学生能否不看代码就复现方法？
  - 是否有关键步骤被"手波"带过？（"We then apply standard techniques to..."——什么 standard techniques？）
  - 模型架构的所有细节是否明确？（层数、维度、激活函数等）
- **数学推导的正确性**：
  - 公式推导中是否有跳步？隐含假设是否明确？
  - 梯度是否可以正确反向传播？（如果涉及不可微操作，是否说明了处理方式？）
  - 概率模型中的条件独立假设是否合理？
- **因果论证链的完整性**：
  - Gap → Insight → Method → Experiments 的逻辑链是否有断裂？
  - 是否存在逻辑跳跃？（"因此我们使用 Transformer"——为什么是 Transformer 而不是其他架构？）
  - Claim 与 evidence 的对应关系是否严密？
- **DL 论文常见的 unsound 模式**：
  - **Train/Test data leakage**：数据预处理是否在 split 之前还是之后？预训练数据是否包含测试集？
  - **Unfair comparison**：不同方法是否使用了相同的 backbone、相同的预训练权重、相同的数据增强？
  - **Missing variance reports**：结果是否只报告了 single run？如果涉及随机性，是否报告了多次运行的 mean±std？
  - **Hyperparameter overfitting**：是否在 test set 上调参？validation set 是否足够大？
  - **Missing statistical tests**：性能差异是否有统计显著性？（尤其是差异 < 1% 时）

#### Role 3: Experiment Critic (实验审查)

**审稿人画像**：你是实验方法论的专家，做过大量消融实验和对比实验。你最在意的是"实验是否真的证明了论文的 claim"。

**审查维度**：
- **实验是否真正验证了 Claim（Claim-Evidence 对齐）**：
  - 对照 `research/contribution.md`，每个 claim 是否都有对应的实验验证？
  - 实验结果是否真的支持论文的 claim？（correlation ≠ causation）
  - 如果 claim 是"方法 A 导致改进"，是否有消融实验证明改进确实来自 A 而非其他因素？
- **Baseline 选择的公平性和充分性**：
  - Baseline 是否足够强？是否包含当前 SOTA？
  - Baseline 是否足够新？2+ 年前的 baseline 需要特别理由
  - 是否遗漏了最直接的竞争方法？
  - 对比是否公平？（相同 backbone、相同预训练、相同数据增强、相同训练时长？）
  - 如果方法引入了额外参数/计算量，是否与参数量/FLOPs 相当的 baseline 做了对比？
- **消融实验的覆盖度和说服力**：
  - 是否覆盖了所有关键设计选择？
  - 消融的 baseline 是否合理？（移除组件 A 时，是用零替代还是用简单替代？）
  - 是否有"消融偏差"——只展示移除后下降的消融，隐藏了移除后不变或上升的消融？
- **Cherry-Picking 检测**：
  - 是否只展示了有利的结果？是否有选择性地报告了某些 metric 而忽略其他？
  - 可视化案例是否只挑了最好的？是否包含 failure case？
  - 如果在多个数据集上实验，是否所有数据集都报告了？
- **Generalizability 的支撑**：
  - 数据集的多样性是否足以支撑论文的 generalizability claim？
  - 不同 domain / scale / setting 下方法是否都有效？
  - 如果方法声称 "general"，是否在足够多元的场景中验证？

#### Role 4: Presentation Critic (表达审查)

**审稿人画像**：你是一个注重论文可读性的 AC（Area Chair），你知道审稿人的时间有限，论文的可读性直接影响审稿人的评分。

**审查维度**：
- **叙事流畅性与逻辑链**：
  - 从 Introduction 到 Conclusion，读者能否顺着逻辑链自然理解？
  - 章节之间是否有逻辑断裂？（读完 Introduction 后，Method 是否自然地接上？）
  - 是否有"信息缺口"——某段用到了之前没有引入的概念？
  - 是否有"信息冗余"——同一件事在多处重复说明？
- **Figure 质量**：
  - Figure 1 是否有效传达了论文核心 idea？（审稿人通常先看 Abstract + Figure 1）
  - 架构图是否清晰？信息密度是否合适？（太密看不清，太疏浪费空间）
  - 实验图表是否专业？（字体大小、线条粗细、颜色选择、legend 位置）
  - Caption 是否自包含？（只读 caption 能否理解图表？）
- **篇幅分配**：
  - Method vs Experiments 的比例是否与论文类型匹配？（见 P1 outline 的论文类型判定）
  - 是否有过于冗余的部分？（如花一整页写 dataset 描述）
  - 是否有过于简略的部分？（如消融实验只给了一个表没有分析）
- **语言质量**：
  - 术语使用是否一致？（同一概念是否在不同地方使用不同表述？）
  - Notation 是否一致？（是否符合 notation.md？）
  - 是否有语法错误、拼写错误？
  - 句子是否过长或过于复杂？（学术写作追求清晰简洁）
  - 是否过度使用被动语态？
- **论文"第一印象"评估**：
  - 标题是否准确且有吸引力？
  - Abstract 是否让人想继续读？
  - 如果审稿人只花 10 分钟扫读，能否抓住核心贡献？

#### Role 5: Reproducibility Critic (可复现性审查)

**审稿人画像**：你是一个尝试复现过很多论文的研究者，你深知 DL 论文复现的痛点——"paper 里说的和实际做的往往不一样"。

**审查维度**：
- **DL 论文复现的核心难点检查**：
  - **Hidden hyperparameters**：论文是否遗漏了关键的训练细节？（weight initialization、gradient clipping、warmup steps、EMA 等）
  - **Training tricks**：是否使用了论文中未提及的 tricks？（label smoothing、mixup、stochastic depth 等）
  - **Hardware dependence**：结果是否依赖特定硬件？（large batch size 需要多 GPU 同步、某些操作在 TPU 和 GPU 上行为不同）
  - **Data preprocessing**：数据预处理的每一步是否明确？（tokenization、normalization、augmentation 的具体参数）
  - **Random seed sensitivity**：结果对 random seed 是否敏感？是否报告了多次运行结果？
- **实现细节的完整性**：
  - 超参数是否完整列出？（可以在 appendix 但至少 main paper 列出最关键的）
  - 训练细节：optimizer、learning rate schedule、总训练步数/epochs、early stopping 策略
  - 评估细节：评估频率、评估时的设置（beam size、sampling temperature 等）
  - 数据集版本、split 方式、是否有 data leakage 风险
- **代码/数据的可获取性**：
  - 是否提到将开源代码？
  - 是否使用了 publicly available 的数据集？
  - 如果使用了私有数据，是否提供了足够的统计描述？
- **复现成本评估**：
  - 训练一次需要多少 GPU hours / 花费多少钱？
  - 普通研究者（如只有 1-2 张 GPU 的 PhD 学生）能否在合理时间内复现？

#### Role 6: External Perspective (外部视角) — 可选

如果系统配置了外部 AI MCP（如 Codex / GPT-5.4），调用外部模型对完整论文进行独立审查，获取不同 AI 生态的差异化视角。

**执行条件**：尝试调用 `mcp__codex__codex` tool。如果 MCP 不可用，跳过本角色。

**外部审查 Prompt**：
- 将完整论文内容传入
- 要求以独立第三方视角审查，不受 Claude 生态偏见影响
- 关注：被忽略的风险、假设漏洞、方法论缺陷、新颖性评估
- 提供具体改进建议（不是泛泛而谈）
- 评分 1-10 + 理由，中文输出
- 设置 `approval-policy: "never"`

**结果**：写入 `Papers/critique/external.md`，格式与其他 5 个角色一致。失败时跳过（non-blocking）。

### Step 3: 写入审查报告

每个角色产出独立的审查报告到 `Papers/critique/`：

- `Papers/critique/novelty.md`
- `Papers/critique/soundness.md`
- `Papers/critique/experiment.md`
- `Papers/critique/presentation.md`
- `Papers/critique/reproducibility.md`

每份报告格式：

```markdown
# [角色名] Critique Report

## 总体评价
- **评分**: X / 10
- **核心评价**: （2-3句话）
- **如果是顶会审稿人，这个维度会导致 reject 吗？**: Yes/No + 理由

## 问题清单
（按严重程度排序）

### [Critical] 问题标题
- **位置**: 章节名 + 具体段落引用
- **问题**: 具体描述
- **审稿人可能的措辞**: （模拟真实审稿意见的措辞，帮助作者预判）
- **建议修改**: 具体方案

### [Major] 问题标题
...

### [Minor] 问题标题
...

## 亮点
（该维度下做得好的部分——好的审稿也要指出优点）

## 总结建议
（1-2 段概括性建议）
```

### Step 4: 生成汇总

产出 `Papers/critique/summary.md`：
- 汇总所有 Critical 和 Major 问题（含外部审查的发现，标注 `[External]`）
- 按章节分组，方便 P4 逐章节修改
- 标注哪些问题需要**补充实验/分析**（可能需要回到代码阶段）
- 标注哪些问题可以**纯粹通过改写解决**
- 如有外部审查，在汇总末尾增加"外部视角独特发现"章节
- **"如果投稿会被 reject 吗？"综合判断**：基于 5 个角色的评分，给出初步判断

## AI Co-Author 关键行为
- 每个角色**独立审查**，不受其他角色结论影响
- **引用原文**：每个问题都指出具体位置和原文
- **给出具体修改建议**，不要模糊的"需要加强"
- 严格但公平——也要承认做得好的部分
- 区分**论文表达问题**和**研究本身问题**（后者标注需要回到代码阶段）
- **模拟真实审稿人的思维**：审稿人通常花 2-4 小时审一篇论文，他们会先快速扫读（Abstract → Figure → Tables → Conclusion），然后再细读。你的审查要反映这种阅读模式——"第一印象"和"深入分析"都要覆盖
- **避免假阳性批评**：不要为了"显得严格"而提出不成立的批评。每个批评都要有具体依据

## 输出
- `Papers/critique/novelty.md`
- `Papers/critique/soundness.md`
- `Papers/critique/experiment.md`
- `Papers/critique/presentation.md`
- `Papers/critique/reproducibility.md`
- `Papers/critique/external.md`（可选，依赖外部 AI MCP）
- `Papers/critique/summary.md`

## Exit Criteria
- [ ] 5 份独立审查报告已生成（+ 外部审查如 MCP 可用）
- [ ] 每份报告有明确的评分和问题清单
- [ ] 汇总文件按章节分组了所有 Critical/Major 问题
- [ ] 问题有具体的原文引用和修改建议
- [ ] 区分了表达问题和研究问题
- [ ] 每个 Critical 问题都模拟了审稿人可能的措辞
- [ ] 综合判断了"是否会导致 reject"
