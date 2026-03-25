# Skill: Praxis Evolve（系统进化）— v3

从已完成项目中提取两类进化产出：
1. **跨项目 Lessons** → `~/.noesis/lessons/<skill_name>.md`，使未来项目 fork agent 自动受益
2. **框架改进** → 基于 `pipeline-evolution-log.md` 更新 Noesis prompts/skills/templates

通常在 R（Retrospective）完成后运行。

---

## Step 1：读取项目产出

读取以下文件（存在则读，不存在跳过）：

- `<project_path>/research/retrospective.md` — 项目回顾（v3 标准路径）
- `<project_path>/retrospective.md` — 旧路径兼容，作为补充
- `<project_path>/pipeline-evolution-log.md` — 各阶段流程反思（X-reflect 积累）
- `<project_path>/iteration-log.md` — 迭代失败诊断历史
- `<project_path>/pipeline-status.json` — 迭代次数与历史
- `<project_path>/Docs/research-module-status.json` — Research Module history

---

## Step 2：读取现有 lessons

读取 `~/.noesis/lessons/` 下所有已存在的 `<skill_name>.md`。

目的：了解哪些教训已存在（用于 RECURRING 判定和有效性评估）、哪些在本项目中被注入。

---

## Step 3：提取跨项目教训

对以下每个 skill，分析 Step 1 文档，提取与该 skill 直接相关的可操作教训：

**Research Pipeline**：

| Skill | 阶段 |
|-------|------|
| `start` | S（Startup） |
| `crystallize` | C（问题锐化） |
| `strategic-review` | RS（战略审查） |
| `joint-design` | D（联合设计） |
| `technical-review` | RT（技术审查） |
| `implementation` | I（实现规划） |
| `retrospective` | R（知识回收） |

**Paper Pipeline**：

| Skill | 阶段 |
|-------|------|
| `30-paper-outline` | P1 |
| `31-paper-sections` | P2 |
| `32-paper-critique` | P3 |
| `33-paper-integrate` | P4 |
| `34-paper-review` | P5 |
| `35-paper-latex` | P6 |
| `36-project-review` | P7 |

### 提取标准

- **纳入**：具体、可操作、在本项目中有正面或负面验证
- **排除**：过于宽泛（"要更仔细"）、未验证的猜测
- 格式：`- [类别][频率][有效性] 描述（1-2句，聚焦行为或检查点）`

### 可迁移性判断

**应提取**：
- 方法论洞察 — "多任务学习中各任务 loss scale 差异 >10x 需 loss balancing"
- 实验设计模式 — "Dim 0 应覆盖 edge case 而非仅 average case"
- 流程检查项 — "I 阶段确认 GPU 显存足够跑最大 batch size"
- 反模式 — "不要在 C 阶段过早固定 metric"
- 工程最佳实践 — "自定义 loss 实现后先 gradient checking 验证"

**不提取**（或标注仅供参考）：
- 特定数据集 trick、特定架构细节、特定超参数值、一次性环境问题

### 时效性判断

| 保质期 | 类型 | 处理 |
|--------|------|------|
| > 2 年 | 实验方法论、研究流程、心态 | 正常写入 |
| 6月-2年 | 特定技术范式、工具/框架 | 正常写入 |
| < 6 月 | SOTA 基准线、竞赛策略、API 经验 | 末尾标注 `[时效性: 短, 提取于 YYYY-MM]` |

### 标签体系

**类别（必填一项）**：

| 标签 | 场景 |
|------|------|
| `[SYSTEM]` | SSH/GPU/环境/格式 |
| `[EXPERIMENT]` | 实验设计、baseline、ablation、metrics |
| `[WRITING]` | 论文写作质量、结构、notation |
| `[ANALYSIS]` | 结果分析、cherry-pick、讨论 |
| `[PLANNING]` | 任务拆分、资源估算 |
| `[PIPELINE]` | 流程顺序、冗余步骤 |
| `[IDEATION]` | 创新性、novelty 论证 |

**频率**：`[RECURRING]`（已存在，末尾追加 `(出现 N 次)`）/ `[NEW]`（首次）

**有效性**：`[verified]`（注入后问题未再出现）/ `[ineffective]`（注入后仍出现）/ `[? unverified]`（首次提取）

---

## Step 4：有效性评估

对 Step 2 读取的现有 lessons 逐条评估：

1. 该教训对应的 skill 在本项目中是否执行过？
2. 回顾 research/retrospective.md 和 iteration-log.md，判断问题是否再次出现：
   - 未再出现 → `[verified]`
   - 仍然出现 → `[ineffective]`，加注"仍出现，需策略调整"
   - 无法判断 → 保持 `[? unverified]`

### ineffective 分析

标记 ineffective 时分析无效原因：

| 原因 | 处理 |
|------|------|
| 表述不够可操作 | 修改表述使其更具体（如"检查数据质量" → "运行 data_sanity_check.py 验证无 NaN、标签一致、训练/测试无交集"） |
| 前提条件已变 | 标注适用条件而非标记无效 |
| 确实无效 | 标记 `[ineffective]` 并附失效原因 |

---

## Step 5：更新 lessons 文件

目录：`~/.noesis/lessons/`

对每个有教训的 skill：

1. 检查 `~/.noesis/lessons/<skill_name>.md` 是否存在
2. **存在** → 更新有效性标签、RECURRING 计数+1、追加新教训（去重）
3. **不存在** → 新建

文件格式：

```markdown
# Lessons: <skill_name>

<!-- 最近更新：<date> | 来源项目：<project_name> -->

## 高频问题（需主动检查）
- [RECURRING][EXPERIMENT][verified] 方法对比必须包含消融实验 (出现 3 次)
- [NEW][PLANNING][? unverified] I 规划时需提前确认 GPU 资源可用性
- [RECURRING][SYSTEM][ineffective] SSH 超时需实验前检查连接 (出现 4 次，需策略调整)

## 成功模式（值得复用）
- [RECURRING] 先小数据 sanity check 再跑完整实验 (出现 2 次)
- [NEW] problem-statement 中标注假设前提，有助方法设计对齐
```

**Runner 行为**：`[ineffective]` 不注入未来项目；`[RECURRING]` 排在最前。

---

## Step 6：Pipeline 框架进化

### 6a. 读取 pipeline-evolution-log.md

汇总所有未处理（`[ ]`）的 X-reflect 观察。

### 6b. 模式识别

聚合为改进主题：
- 多 Entry 指向同一方向 → 高置信度，应行动
- 单次低置信度 → 记录但暂不行动
- `[URGENT]` → 优先确认

产出**改进清单**，每条含：改进描述（具体到文件哪部分）、涉及文件、证据来源（Entry 编号）、综合置信度。

### 审慎原则

**应修改**：多项目独立验证的模式（>= 2 个项目）、被证明冗余/有害的步骤、模板缺少的关键字段。

**不应修改**：仅基于单个项目、仅换措辞（除非原措辞导致误解）、增加复杂度但无明确价值。

**框架保持"方法论永恒性"**：写入的应是如何做研究的方法论，而非特定技术操作手册。

### 6c. 与用户确认改进清单

展示每条理由和预期效果，等待确认。

### 6d. 执行修改

按确认清单修改：`Praxis/prompts/*.md`、`Praxis/skills/*.md`、`Praxis/templates/*.md`。

### 6e. 标记已处理

pipeline-evolution-log.md 中已处理观察由 `[ ]` 改为 `[x]`。

### 6f. 推送

```bash
cd ~/Research/Noesis
git add Praxis/prompts/ Praxis/skills/ Praxis/templates/
git commit -m "evolve: [项目名] — [改进主题]"
git push origin main
```

---

## Step 7：输出汇总

```
Praxis Evolution 完成

-- 跨项目 Lessons -----------------------------------------------
更新的 lessons 文件：
  - crystallize.md  (+2 新, 1 升级 RECURRING, 1 标记 ineffective)
  - joint-design.md  (+1 新)

有效性评估：
  - [verified]:     N 条（注入后问题消失）
  - [ineffective]:  N 条（注入后仍出现，需调整）
  - [unverified]:   N 条（首次提取，待验证）

-- 框架改进 -----------------------------------------------------
处理的 evolution-log 条目：X 条
执行的框架修改：
  - Praxis/prompts/crystallize-prompt.md：[改动]
  （无修改时：无高置信度改进，已记录待验证）

Noesis 框架已推送到 GitHub（或：无改动，跳过推送）
```
