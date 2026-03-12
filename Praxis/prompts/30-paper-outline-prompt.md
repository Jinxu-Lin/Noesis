# Skill: Paper Outline (论文大纲) — Phase P1

## 触发场景
项目进入论文写作模块（`/praxis-paper`），需要从研究文档映射出论文结构。

## 输入
- `project-startup.md` — 背景材料、研究动机
- `research/gap-analysis.md` — Gap 定义、RQ、根因分析
- `research/method-design.md` — 方法框架、因果论证
- `research/experiment-design.md` — 实验设计
- `research/contribution.md` — 贡献列表
- `Codes/` 目录 — 实验结果、图表

## 执行流程

### Step 1: 审查研究素材

完整阅读所有输入文档，建立以下映射关系：
- **叙事脊柱**：Gap → 根因 → 方法 → 验证 → 贡献
- **素材清单**：每个文档中哪些内容会映射到论文的哪个章节
- **图表清单**：Codes/ 中已有的实验结果图表，以及需要新制作的图表

### Step 2: 确定目标会议/期刊

检查 `project-startup.md` 中是否指定了目标会议/期刊。如果没有，在 outline 中标注为 TBD，但按通用 ML 会议格式（8-10 页）规划。

### Step 3: 生成论文大纲

产出 `Papers/outline.md`，包含：

#### 3.1 论文元信息
- 暂定标题（2-3 个候选）
- 目标会议/期刊
- 页数限制

#### 3.2 章节大纲
对每个章节（Abstract, Introduction, Related Work, Method, Experiments, Conclusion）提供：
- **核心论点**：该章节要传达的 1-2 个核心信息
- **素材映射**：从哪些文档的哪些部分提取内容
- **预估篇幅**：占总篇幅的百分比
- **子节结构**：2 级子标题

#### 3.3 图表规划
| 图/表编号 | 类型 | 内容描述 | 数据来源 | 所在章节 |
|-----------|------|---------|---------|---------|
| Fig.1 | Framework | 方法整体架构 | research/method-design.md | Method |
| Tab.1 | Results | 主实验结果 | Codes/ | Experiments |
| ... | ... | ... | ... | ... |

#### 3.4 叙事一致性检查
- research/contribution.md 中每个贡献 → 在论文中如何论证和验证
- 每个实验 → 验证哪个 claim
- 确保无悬空贡献（有 claim 无验证）和无悬空实验（有验证无 claim）

### Step 4: 生成符号表

产出 `Papers/notation.md`：
- 统一全文的数学符号和缩写
- 避免同一概念在不同章节使用不同符号
- 格式：`| 符号 | 含义 | 首次出现 |`

## AI Co-Author 关键行为
- 从研究文档**映射**到论文结构，而非从零创作
- 叙事脊柱必须与 research/gap-analysis → research/method-design → experiments 的逻辑链一致
- 大纲阶段不写正文，只规划结构和素材映射
- 图表规划要考虑审稿人的阅读体验

## 输出
- `Papers/outline.md` — 论文大纲
- `Papers/notation.md` — 符号表

## Exit Criteria
- [ ] 叙事脊柱完整（Gap → 根因 → 方法 → 验证 → 贡献）
- [ ] 每个贡献都有对应的论证和验证路径
- [ ] 图表规划覆盖关键结果
- [ ] 符号表统一且无歧义
- [ ] 章节篇幅分配合理

