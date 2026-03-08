# Skill: Project Retrospective (项目回顾与知识回收) — Phase 11

## 触发场景
- **路径 A**: Phase 10 完成后（自然完成）
- **路径 B**: Exit Assessment Gate 判定 Abandon 后（中止退出）

## 输入
- 所有已产出的项目文档
- `iteration-log.md`（如有）
- `pipeline-evolution-log.md`（如有，包含项目周期内积累的流程反思）
- 项目结局标记：完成 / 中止

## 执行流程

### Step 1: 项目时间线重建

回顾从 Phase 1 到当前的关键节点：
- 什么时候做了什么决策？
- 哪些是转折点（方向变化、重大发现、关键失败）？
- 迭代了多少轮？每轮的级别？

产出：关键决策时间线表格

### Step 2: 成败分析

**What Worked (做对了什么)**:
- 哪些决策/组件/方法是有效的？
- 为什么有效？是因为方法好，还是因为问题选得好？
- 可以被未来项目复用的成功模式

**What Didn't Work (什么没 work)**:
- 哪些尝试失败了？
- 失败的根本原因是什么？（不是表面现象，是根因）
- 是否可以在更早的阶段发现这些问题？

**Surprises (意外发现)**:
- 有没有预期之外的发现？
- 正面：意外有效的方法、意外发现的规律
- 负面：看似合理但完全不 work 的假设

### Step 3: 迭代历史总结（如有 iteration-log.md）

从完整的 `iteration-log.md` 中提取模式：
- 迭代中反复出现的问题类型
- 从失败到成功的关键转折是什么
- 哪些约束传递是有效的，哪些被忽视了
- 迭代策略的效率分析（L1-4 各用了多少次，是否倾向合理）

### Step 4: 知识库资产提取

这是 Phase 11 最关键的产出。将项目经验转化为四类可复用资产：

#### Methods Bank 更新
| 项目结局 | 提取内容 |
|---------|---------|
| 成功 | 新方法条目、验证有效的组件组合、最优超参数范围 |
| 失败 | 哪些组件在什么条件下不 work、失败的组合方式、边界条件 |

#### Gaps & Assumptions 更新
| 项目结局 | 提取内容 |
|---------|---------|
| 成功 | 已解决的 Gap（标记 resolved）、验证成立的假设 |
| 失败 | 被证伪的假设、比预想更难的 Gap、新发现的子问题 |

#### Experimental Patterns 更新
| 项目结局 | 提取内容 |
|---------|---------|
| 成功 | 有效的实验设计模式、可靠的评估 pipeline |
| 失败 | 有误导性的 metrics、评估陷阱、不公平的对比设置 |

#### Cross-Paper Connections 更新
| 项目结局 | 提取内容 |
|---------|---------|
| 成功 | 新发现的方法间关联、成功的跨域迁移 |
| 失败 | 看似相关但实际不兼容的方法组合 |

### Step 5: 写入 retrospective.md

按 `templates/retrospective.md` 模板生成结构化回顾文档。

### Step 6: Pipeline 进化（综合反思 → 正式修改）

这是流程自进化机制的**正式修改点**。在项目完成/中止后，综合整个项目周期的流程反思，决定是否更新 pipeline.md 和 Skills。

**6a. 读取 pipeline-evolution-log.md**

读取项目的 `pipeline-evolution-log.md`，汇总所有 Entry 中的观察。

**6b. 模式识别与聚合**

将分散的观察聚合为改进主题：
- 多个 Entry 指向同一方向的观察 → 高置信度改进需求
- 单次出现的低置信度观察 → 记录但暂不行动
- `[URGENT]` 标记的观察 → 确认是否已处理

产出一个**改进清单**，每条包含：
- 改进描述
- 涉及的文件（pipeline.md / 哪个 skill / 哪个模板）
- 证据来源（哪些 Entry 支持）
- 置信度综合评估

**6c. 与用户确认改进清单**

将改进清单呈现给用户，说明每条改进的理由和预期效果。
用户确认后，执行修改。

**6d. 执行流程文档修改**

按确认后的清单修改：
- `pipeline.md`：更新阶段描述、Exit Criteria、核心机制等
- `skills/*.md`：更新执行流程、输入判断、输出格式等
- `templates/*.md`：更新模板结构（如需）

每次修改在 pipeline.md 末尾的"变更记录"中追加条目。

**6e. 标记已处理的观察**

回到 `pipeline-evolution-log.md`，将已处理的观察标记为 `[x]`。

**6f. 推送 ResearchFlow 框架到 GitHub**

如果 Step 6d 执行了任何 pipeline.md / skills / templates 的修改，立即同步到 ResearchFlow 中央仓库：
```bash
cd [ResearchFlow路径]
git add pipeline.md skills/ templates/
git commit -m "pipeline: [项目名] retrospective — [改进主题简述]"
git push origin main
```
提示用户：ResearchFlow 框架已更新并推送，其他 Agent 下次启动时将获取最新版本。

**6g. 更新全局跨项目 Lessons（Evolution）**

运行以下命令，将本项目经验提取并注入全局 lessons 目录，使未来项目的 fork agent 自动受益：

```
/researchflow:evolve <项目路径>
```

此命令读取 `retrospective.md` 和 `pipeline-evolution-log.md`，提取各阶段的可操作教训，写入 `~/.researchflow/lessons/<skill_name>.md`。下一个项目运行时，这些教训将自动出现在对应阶段 fork agent 的 prompt 末尾。

### Step 7: 执行知识库更新

将 Step 4 提取的资产**实际写入知识库**：
- 更新 Methods Bank 条目
- 更新 Gaps & Assumptions 条目
- 更新 Experimental Patterns 条目
- 更新 Cross-Paper Connections 条目
- 每个更新都标注来源项目

## AI Co-Author 关键行为
- 客观回顾项目全程，不美化也不过度自责
- **主动从失败中提取可复用知识**——"虽然整体没 work，但组件 X 在条件 Y 下是有效的"
- 帮助将经验转化为结构化的知识库条目
- 识别意外发现——失败项目中可能藏着通往其他方向的线索
- "负面知识"往往比正面知识更稀缺——论文不发表负面结果，但知识库可以记录

## 输出
- `retrospective.md`
- 知识库条目更新（四类资产）
- pipeline.md / skills / templates 更新（如 pipeline 进化步骤产出了改进）

## Exit Criteria
- [ ] retrospective.md 完成
- [ ] 知识库四类资产已更新
- [ ] 失败项目：根因清晰、已排除方案标注
- [ ] 成功项目：成功因素提炼、可复用模式识别
- [ ] 对未来相关项目的建议已记录
- [ ] Pipeline 进化：pipeline-evolution-log.md 已审阅，高置信度改进已执行或记录
- [ ] 如有框架改动：ResearchFlow 已 commit + push 到 GitHub
- [ ] 项目 repo 最终状态已 commit + push（retrospective.md + 知识库更新）

## 完成后
提交项目最终状态：
```bash
# 项目 repo：归档最终状态
git add retrospective.md pipeline-evolution-log.md kb-index.md kb/
git commit -m "phase/11: project retrospective complete — [项目名]"
git push origin main
```
通知用户：项目回顾完成，知识库已更新，流程文档已进化。知识将通过 Phase 0 的持续积累在未来项目中发挥复利效应。
然后执行 `/reflect-pipeline` 对本阶段的流程进行反思，记录改进观察。
