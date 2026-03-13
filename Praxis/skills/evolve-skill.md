# Skill: Praxis 系统进化（Evolve）

> 从已完成的项目中提取两类进化产出：
> 1. **跨项目 Lessons**：注入到 `~/.noesis/lessons/`，使未来项目的 fork agent 自动受益
> 2. **框架改进**：综合 `pipeline-evolution-log.md` 中的流程反思，更新 Noesis 的 prompts / skills / templates
>
> 通常在 R（知识回收）完成后运行。

---

## 执行步骤

### Step 1：读取项目产出

读取以下文件（存在则读取，不存在跳过）：

- `<project_path>/research/retrospective.md` — 项目回顾与研究经验总结（v2 标准路径）
- `<project_path>/retrospective.md` — 旧项目兼容路径；若存在，作为补充材料读取
- `<project_path>/pipeline-evolution-log.md` — 各阶段流程反思记录（X-reflect 自动积累）
- `<project_path>/iteration-log.md` — 迭代失败诊断历史
- `<project_path>/pipeline-status.json` — 迭代次数与历史

---

### Step 2：读取现有 lessons 文件

在提取新教训之前，读取 `~/.noesis/lessons/` 下**所有已存在**的 `<skill_name>.md` 文件。

目的：
- 了解哪些教训已经存在（用于 RECURRING 判定和有效性评估）
- 了解哪些教训在本项目执行期间被自动注入到 fork agent 的 prompt 中

---

### Step 3：提取各阶段的跨项目教训

对以下每个 skill，分析 Step 1 的文档，提取**与该 skill 直接相关**的可操作教训：

**Research Pipeline：**

| Skill | 对应阶段 |
|-------|---------|
| `start` | S（Startup） |
| `crystallize` | C（问题锐化） |
| `strategic-review` | RS（战略审查） |
| `joint-design` | D（联合设计） |
| `technical-review` | RT（技术审查） |
| `implementation` | I（实现规划） |
| `retrospective` | R（知识回收） |

**Paper Pipeline：**

| Skill | 对应阶段 |
|-------|---------|
| `30-paper-outline` | P1 |
| `31-paper-sections` | P2 |
| `32-paper-critique` | P3 |
| `33-paper-integrate` | P4 |
| `34-paper-review` | P5 |
| `35-paper-latex` | P6 |
| `36-project-review` | P7 |

提取标准：
- **有效教训**：具体、可操作、在本项目中有正面或负面验证
- **排除**：过于宽泛的观察（"要更仔细"）、尚未验证的猜测
- 每条教训格式：`- [类别][频率][有效性] 描述（1-2句，聚焦具体行为或检查点）`

#### 什么样的 lesson 是真正可迁移的

DL 研究中，不是所有经验都能跨项目复用。提取 lesson 时必须区分：

**可迁移的（应该提取）**：
- **方法论级别的洞察**："在多任务学习中，如果各任务 loss scale 差异 >10x，需要加 loss balancing" — 这适用于所有多任务学习项目
- **实验设计模式**："Dim 0 实验应覆盖 edge case（极短序列 + 极长序列），而不只是 average case" — 适用于所有需要验证鲁棒性的项目
- **流程节点的检查项**："I 阶段必须确认 GPU 显存是否足够跑最大 batch size 配置" — 系统性问题，每个项目都会遇到
- **反模式**："不要在 C 阶段过早固定 metric，应留到 D 阶段与方法设计联合确定" — 流程优化，跨项目有效
- **工程模式**："自定义 loss function 实现后，先用 gradient checking 验证梯度计算正确性" — DL 开发的通用最佳实践

**不可迁移的（不应提取，或应标注为仅供参考）**：
- **特定数据集/任务的 trick**："在 CIFAR-10 上用 cutout 增强能提升 1%" — 只对该数据集有效
- **特定架构的实现细节**："ViT 的 patch embedding 用 conv2d 比 linear projection 快 10%" — 仅限 ViT
- **特定超参数**："learning rate 3e-4 最优" — 高度依赖模型和数据
- **一次性环境问题**："服务器 X 的 CUDA 驱动需要升级" — 不可复用

#### DL 研究中跨项目有效的元知识模式

以下是经验证有效的跨项目设计模式，提取 lesson 时可以参照（但只有在本项目中确实验证过的才应写入）：

**实验设计模式**：
- 先小后大（Dim 0 → Dim 1）：先在小数据集/小模型上验证核心假设，通过后再扩展到完整规模。这是 DL 研究中最重要的效率模式
- Ablation 分层设计：核心组件 → 辅助组件 → 超参数，按贡献预期大小排序
- Baseline 的公平性检查：给 baseline 和你的方法相同的调参预算和计算资源
- 定性 + 定量结合：光有数字不够，需要 case study、attention visualization 等定性分析来建立方法有效性的直觉

**方法设计模式**：
- 单一变量原则：每次只改变一个组件，确保能归因改进来源
- 模块化设计：核心贡献组件应可被独立替换和测试
- Inductive bias 与数据规模的 trade-off：小数据需要强归纳偏置，大数据下简单方法可能更好

**论文写作模式**：
- "贡献 claim 必须有实验数字直接支撑"——如果 claim 是"更高效"，必须有 FLOPs/latency 对比表
- "Related Work 应按问题分组而非按时间排列"——按问题分组能更好地凸显 gap

#### 判断 lesson 的"保质期"

DL 领域发展极快，有些经验会很快过时。在提取 lesson 时，对每条教训做一个简单的时效性判断：

**长保质期（>2 年）**：
- 关于实验方法论的教训（如统计显著性、对照实验设计）
- 关于研究流程的教训（如文档管理、迭代策略）
- 关于研究心态的教训（如何处理失败、何时放弃）

**中保质期（6 个月 - 2 年）**：
- 关于特定技术范式的教训（如 Transformer 训练技巧、扩散模型采样策略）
- 关于特定工具/框架的教训（如 PyTorch、HuggingFace 使用经验）

**短保质期（< 6 个月）**：
- 关于 SOTA 基准线的教训（SOTA 更新很快）
- 关于特定竞赛/benchmark 的策略
- 关于特定 API/service 的使用经验

对短保质期的 lesson，建议在条目末尾标注 `[时效性: 短, 提取于 YYYY-MM]`，Runner 注入时可供 agent 参考。

#### 类别标签（必填其一）

| 标签 | 适用场景 |
|------|---------|
| `[SYSTEM]` | SSH/GPU/环境/格式错误等系统性问题 |
| `[EXPERIMENT]` | 实验设计、baseline 对比、ablation、评估 metrics |
| `[WRITING]` | 论文写作质量、结构、notation 一致性 |
| `[ANALYSIS]` | 结果分析不充分、cherry-pick、讨论缺失 |
| `[PLANNING]` | 计划不周、任务拆分、资源估算 |
| `[PIPELINE]` | 流程顺序、冗余步骤、阶段设计 |
| `[IDEATION]` | 创新性、研究贡献、novelty 论证 |

#### 频率标签（必填其一）

- `[RECURRING]` — 该教训在现有 lessons 文件中已存在，末尾追加 `(出现 N 次)`
- `[NEW]` — 首次出现

#### 有效性标签（必填其一）

- `[✓ verified]` — 该教训曾被注入本项目，相关问题**未再出现**（有效）
- `[✗ ineffective]` — 该教训曾被注入本项目，相关问题**仍然出现**（无效，需策略调整）
- `[? unverified]` — 首次提取，尚未验证

---

### Step 4：有效性评估（针对已注入的教训）

对 Step 2 读取到的现有 lessons 中的每条教训，逐条评估：

1. 该教训对应的 skill 在本项目中是否执行过？
2. 回顾 `research/retrospective.md`（若不存在则回退到 `retrospective.md`）和 `iteration-log.md`，判断该教训描述的问题是否在本项目中再次出现：
   - **未再出现** → 标记为 `[✓ verified]`
   - **仍然出现** → 标记为 `[✗ ineffective]`，并在条目末尾加注 `（仍出现，需策略调整）`
   - **无法判断** → 保持 `[? unverified]`

#### 有效性评估的深层逻辑

当一条教训被标记为 `[✗ ineffective]` 时，不应简单地删除它——应该分析无效的原因：

**教训本身正确但表述不够可操作**：
- 例如 "实验前检查数据质量" 是正确的，但太宽泛。应改为 "实验前运行 data_sanity_check.py 脚本，验证：(1) 无 NaN/Inf, (2) 标签分布与预期一致, (3) 训练/测试无交集"
- 这种情况应修改教训的表述，而非标记为无效

**教训的前提条件已改变**：
- 例如 "用 FP16 训练时需要 loss scaling" 在使用 BF16 的项目中不适用
- 应标注适用条件，而非标记为无效

**教训确实无效**：
- 例如 "在 C 阶段枚举所有可能的攻击角度" — 如果实践表明穷举反而导致选择困难，那这条教训确实应该被废弃
- 此时标记为 `[✗ ineffective]` 并附上具体失效原因

---

### Step 5：更新全局 lessons 文件

Lessons 目录：`~/.noesis/lessons/`

对每个有教训的 skill：

1. 检查 `~/.noesis/lessons/<skill_name>.md` 是否存在
2. **若存在**，读取现有内容后执行：
   - 更新已有教训的有效性标签（Step 4 评估结果）
   - 对 `[RECURRING]` 条目更新出现次数（+1）
   - 追加新教训（与已有条目去重）
3. **若不存在**，新建文件

文件格式：

```markdown
# Lessons: <skill_name>

<!-- 最近更新：<date> | 来源项目：<project_name> -->

## 高频问题（需主动检查）
- [RECURRING][EXPERIMENT][✓ verified] 方法对比必须包含消融实验，缺失会导致审查 Block (出现 3 次)
- [NEW][PLANNING][? unverified] I 规划时需提前确认 GPU 资源可用性
- [RECURRING][SYSTEM][✗ ineffective] SSH 超时需在实验前检查连接，当前措施无效 (出现 4 次，需策略调整)

## 成功模式（值得复用）
- [RECURRING] 先用小数据集做 sanity check，再跑完整实验 (出现 2 次)
- [NEW] 在 problem-statement 中明确标注假设前提，有助于后续方法设计对齐
```

**注意**：Runner 自动过滤 `[✗ ineffective]` 条目，不将其注入未来项目的 prompt。
`[RECURRING]` 条目在注入时排在普通条目之前。

---

### Step 6：Pipeline 框架进化

这是 Noesis 系统自我迭代的核心步骤，基于 `pipeline-evolution-log.md` 中积累的流程反思。

**6a. 读取并汇总 pipeline-evolution-log.md**

读取项目的 `pipeline-evolution-log.md`（包含 C-R、P1-P7 各阶段的 X-reflect 条目）。
汇总所有未处理（`[ ]`）的观察。

**6b. 模式识别与聚合**

将分散的观察聚合为改进主题：
- 多个 Entry 指向同一方向 → 高置信度，应行动
- 单次低置信度观察 → 记录但暂不行动
- `[URGENT]` 标记的观察 → 优先确认是否已处理

产出**改进清单**，每条包含：
- 改进描述（具体到哪个文件的哪部分）
- 涉及的文件：`Praxis/prompts/<name>-prompt.md` / `Praxis/skills/<name>-skill.md` / `Praxis/templates/<name>.md`
- 证据来源（Entry 编号）
- 综合置信度

#### 框架改进的审慎原则

框架改进是高杠杆但也高风险的操作——修改 prompt 或 template 会影响所有未来项目。因此需要特别审慎：

**应该修改的**：
- 被多个项目独立验证的模式（至少 2 个项目的 evolution-log 指向同一方向）
- 流程中被证明冗余或有害的步骤（例如某个检查项总是被跳过且跳过后没有负面后果）
- 输出模板中缺少的关键字段（例如发现 method-design 模板缺少"计算开销估算"字段，导致 RT 审查总是提出此问题）

**不应该修改的**：
- 仅基于单个项目的观察（可能是特例而非通用模式）
- 仅仅是"换一种措辞"的改动（除非原措辞确实导致了误解）
- 增加流程复杂度的改动（除非复杂度增加带来了明确的价值提升）

**DL 领域快速发展的影响**：
- 如果改进涉及特定技术栈（如 PyTorch 2.0 的 compile 特性），要评估这些技术是否已经足够稳定，值得写入框架
- 如果改进涉及特定评估范式（如某些 benchmark），要考虑该 benchmark 的生命周期
- 框架应保持"方法论永恒性"：写入的应该是关于如何做研究的方法论，而非关于特定技术的操作手册

**6c. 与用户确认改进清单**

将改进清单呈现给用户，说明每条改进的理由和预期效果。
等待用户确认后再执行修改。

**6d. 执行框架文档修改**

按确认后的清单修改 Noesis 框架文件：
- `Praxis/prompts/*.md`：更新 prompt 内容、输出格式等
- `Praxis/skills/*.md`：更新执行流程、输入判断、关键行为等
- `Praxis/templates/*.md`：更新模板结构（如需）

**6e. 标记已处理的观察**

回到 `pipeline-evolution-log.md`，将已处理的观察项由 `[ ]` 改为 `[x]`。

**6f. 推送 Noesis 框架到 GitHub**

如果 Step 6d 执行了任何修改：
```bash
cd ~/Research/Noesis
git add Praxis/prompts/ Praxis/skills/ Praxis/templates/
git commit -m "evolve: [项目名] — [改进主题简述]"
git push origin main
```

---

### Step 7：输出汇总

```
Praxis Evolution 完成

-- 跨项目 Lessons -----------------------------------------------
更新的 lessons 文件：
  - crystallize.md  (+2 条新教训, 1 条升级为 RECURRING, 1 条标记为 ineffective)
  - joint-design.md  (+1 条新教训)
  - 31-paper-sections.md (+1 条新教训)

有效性评估：
  - [verified]:    2 条（注入后问题消失，有效）
  - [ineffective]: 1 条（注入后仍出现，需策略调整）
  - [unverified]:  4 条（首次提取，待验证）

-- 框架改进 -----------------------------------------------------
处理的 pipeline-evolution-log 条目：X 条
执行的框架修改：
  - Praxis/prompts/crystallize-prompt.md：[改动描述]
  （无修改时：无高置信度改进，已记录低置信度观察，待后续项目验证）

Noesis 框架已推送到 GitHub（或：无框架改动，跳过推送）
```
