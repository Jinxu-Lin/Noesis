# Skill: Paper Sections Writing (章节写作) — Phase P2

## 触发场景
P1 大纲完成，按照大纲顺序写作各章节。

## 输入
- `Papers/outline.md` — 论文大纲（结构、素材映射、图表规划）
- `Papers/notation.md` — 符号表
- `research/gap-analysis.md`、`research/method-design.md`、`research/experiment-design.md` — 研究文档
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

- **素材来源**：`research/method-design.md` 直接转化
- **核心叙事**：Gap → 根因 → 方法设计理由 → 技术细节 → 为什么能解决
- 保留数学公式的精确表述，使用 `notation.md` 统一符号
- 包含方法图（Framework Figure）描述——说明图中应包含的元素和布局
- **不发明新方法**——所有内容必须来自 `research/method-design.md`
- **模式 A 精炼要点**：检查所有数学符号是否与 `notation.md` 完全一致；确认 Framework Figure 描述完整；删除任何 Codex 补充的超出 `research/method-design.md` 范围的技术细节

### Step 2: Experiments (`Papers/sections/experiments.md`)

- **素材来源**：`research/experiment-design.md` + `Codes/` 实验结果
- 结构：
  1. Experimental Setup（数据集、baselines、超参数、硬件）
  2. Main Results（主表/主图 + 分析）
  3. Ablation Study（消融实验 + 分析）
  4. Analysis（Case Study / 可视化 / 错误分析）
- 每个实验明确说清"它验证了什么 claim"
- 表格和图的 caption 要**自包含**（只读 caption 就能理解图表）
- 与 baselines 对比要公平：相同数据集、相同评估指标
- **模式 A 精炼要点**：填充所有 `[RESULT: ...]` 占位符（来自 `Codes/` 实际数据）；确认所有 baseline 数字与 `research/experiment-design.md` 一致；删除 Codex 可能虚构的数字

### Step 3: Introduction (`Papers/sections/intro.md`)

- **素材来源**：`research/gap-analysis.md` + `research/contribution.md` + `project-startup.md`
- 叙事结构（约 4-5 段）：
  1. 领域背景 + 任务重要性
  2. 现有方法 + 它们的局限性
  3. Gap 的精确描述 + 根因
  4. 我们的方法概述 + 关键洞察
  5. 贡献列表（每个贡献 1 bullet）
- 贡献列表**直接来自 `research/contribution.md`**——不在论文中发明新贡献
- 每个贡献 claim 都必须在 Experiments 中有对应验证

### Step 4: Related Work (`Papers/sections/related_work.md`)

- **素材来源**：`project-startup.md` + 知识库（如可用）
- 不是罗列文献，而是构建**技术谱系**：
  - 按面（大类别）→ 按线（技术路线）→ 按点（具体工作）
  - 最终落脚到"以上所有工作都没做到 X，这就是我们的 Gap"
- 每个被引用的工作都要说清：做了什么、与我们的关系、差异点
- 如果素材不足，在文件末尾标注"需要补充阅读的方向"

### Step 5: Conclusion (`Papers/sections/conclusion.md`)

- 总结贡献（与 Introduction 呼应但不重复）
- Limitations——诚实列出，审稿人看得出回避
- Future Work——基于 limitations 自然延伸

### Step 6: Abstract (`Papers/sections/abstract.md`)

- **最后写**——此时全文已定型
- 结构：问题 → 方法 → 结果 → 贡献
- 4-6 句话，150-250 词
- 不使用"In this paper, we..."等套话
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

## AI Co-Author 关键行为
- 从研究文档**提取和转化**素材，不是创造新内容
- 确保跨章节的**术语一致性**（参考 notation.md）
- 确保**叙事一致性**：Introduction 的 claim = Method 的方法 = Experiments 的验证
- 学术论文语言：精确、简洁、客观，避免夸大（"dramatically improves" → "improves by X%"）
- 每个章节写完后，快速检查与 outline.md 的一致性

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

