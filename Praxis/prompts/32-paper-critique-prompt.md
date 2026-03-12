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
- 贡献是否真正新颖？还是已有工作的简单组合？
- 与最相关的 prior work 区分度是否足够？
- Related Work 是否遗漏了关键的竞争工作？
- 技术洞察是否有深度，还是表面的工程改进？

#### Role 2: Soundness Critic (严谨性审查)
- 方法描述是否完整、可复现？
- 数学推导是否正确？假设是否明确？
- 因果论证链是否有断裂？
- 是否存在逻辑跳跃或未论证的 claim？

#### Role 3: Experiment Critic (实验审查)
- 实验设置是否公平？Baselines 是否足够强和足够新？
- 消融实验是否覆盖所有关键组件？
- 结果分析是否充分？是否有 cherry-picking 嫌疑？
- 数据集选择是否能支撑 generalizability claim？

#### Role 4: Presentation Critic (表达审查)
- 叙事是否流畅？读者能否顺着逻辑链自然理解？
- 图表是否清晰？Caption 是否自包含？
- 篇幅分配是否合理？是否有过于冗余或过于简略的部分？
- 术语使用是否一致？

#### Role 5: Reproducibility Critic (可复现性审查)
- 实现细节是否足够复现？
- 超参数、数据预处理、评估指标是否完整说明？
- 是否提到代码/数据的可用性？
- 随机性控制（seed、多次运行均值/方差）是否说明？

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

## 问题清单
（按严重程度排序）

### [Critical] 问题标题
- **位置**: 章节名 + 具体段落引用
- **问题**: 具体描述
- **建议修改**: 具体方案

### [Major] 问题标题
...

### [Minor] 问题标题
...

## 亮点
（该维度下做得好的部分）

## 总结建议
（1-2 段概括性建议）
```

### Step 4: 生成汇总

产出 `Papers/critique/summary.md`：
- 汇总所有 Critical 和 Major 问题（含外部审查的发现，标注 `[External]`）
- 按章节分组，方便 P4 逐章节修改
- 标注哪些问题需要**补充实验/分析**（可能需要回到代码阶段）
- 如有外部审查，在汇总末尾增加"外部视角独特发现"章节

## AI Co-Author 关键行为
- 每个角色**独立审查**，不受其他角色结论影响
- **引用原文**：每个问题都指出具体位置和原文
- **给出具体修改建议**，不要模糊的"需要加强"
- 严格但公平——也要承认做得好的部分
- 区分**论文表达问题**和**研究本身问题**（后者标注需要回到代码阶段）

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

