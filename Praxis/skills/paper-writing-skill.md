# Skill: Paper Writing (论文撰写) — Phase 9

## 触发场景
Phase 8 全部实验完成，所有素材就绪，开始撰写论文。

## 输入
- `gap-analysis.md` — Gap 定义、RQ、根因分析
- `method-design.md` — 方法框架、因果论证、理论分析
- `experiment-design.md` — 实验设计 + 实验结果
- `project-startup.md` — 背景材料、源材料分析
- `contribution.md` — 贡献列表
- 论文模板（会议/期刊格式）
- Code/ 中的图表

## 执行流程

### 撰写顺序

**不按章节顺序写。** 推荐顺序：

#### Step 1: Method
- 来源：`method-design.md` 直接转化
- 核心叙事脊柱：Gap → 根因 → 方法 → 为什么能解决
- 保留数学公式的精确表述
- 方法图（framework figure）的设计

#### Step 2: Experiments
- 来源：`experiment-design.md`（设计 + 结果）
- 每个实验：目的 → 设置 → 结果 → 分析
- 确保每个实验都说清"它验证了什么 claim"
- 表格和图的 caption 要自包含（读 caption 就能理解图表）

#### Step 3: Introduction
- 来源：`gap-analysis.md` + `contribution.md` + `project-startup.md`
- 叙事结构：领域背景 → 现有工作 → Gap → 我们的贡献
- 贡献列表直接来自 `contribution.md`——**不在论文中"发明"新贡献**
- 每个贡献 claim 都必须在 Experiments 中有对应验证

#### Step 4: Related Work
- 来源：`project-startup.md` + 知识库 + 补充文献调研
- 不是罗列文献，而是构建**技术谱系**：
  - 按面 → 按线 → 按点展开
  - 最终落脚到"以上所有工作都没做到 X，这就是我们的 Gap"
- 如果需要补充阅读更多论文，提示用户使用 `/paper-reading`

#### Step 5: Abstract & Conclusion
- 最后写，此时全文已定型
- Abstract：问题-方法-结果-贡献，4-5句话
- Conclusion：总结贡献 + limitations + future work
- limitations 和 future work 要诚实——审稿人看得出来回避

### 质量检查（写完后执行）

| 检查项 | 方法 |
|--------|------|
| 叙事一致性 | Introduction 的 claim 是否全部被 Experiments 覆盖？ |
| 贡献完整性 | contribution.md 中每个贡献是否在论文中被充分论证？ |
| 无凭空内容 | 论文是否引入了前序文档中没有的新内容？ |
| 图表自包含 | 每个图表的 caption 是否足够理解？ |
| 逻辑自洽 | Introduction → Method → Experiments → Conclusion 逻辑链是否通顺？ |
| 格式规范 | 是否符合目标会议/期刊的格式要求？ |

## AI Co-Author 关键行为
- 从各文档提取素材，构建各章节初稿
- 确保叙事与前序文档的逻辑链一致
- 检查论文内部逻辑自洽性
- 帮助润色语言，但不改变技术内容的准确性
- Related Work 部分主动提示需要补充阅读的方向
- **论文是叙事产品**——不是堆砌工作，而是讲一个有说服力的故事

## 输出
- Papers/ 目录下的论文草稿
- （如需）补充文献阅读的需求列表

## Exit Criteria
- [ ] 叙事脊柱完整且自洽
- [ ] Introduction 中每个 claim 都被 Experiments 覆盖
- [ ] contribution.md 中每个贡献都被充分论证
- [ ] 所有图表有 caption、有分析、有结论
- [ ] Related Work 定位清晰，落脚到本工作的 Gap
- [ ] 无前序文档中没有的新内容
- [ ] 符合目标会议/期刊格式

## 完成后
提示用户：论文草稿完成，建议审阅后准备投稿。
然后执行 `/reflect-pipeline` 对本阶段的流程进行反思，记录改进观察。
