# Praxis Pipeline v2 设计方针

> 本文档是 Praxis 研究流程重构的完整行动方针。所有实现工作以本文档为准。

---

## 一、设计哲学

### 1.1 核心变更动机

当前 Pipeline（v1）是线性瀑布式流程：Gap → Review → Method → Review → Experiment → Review → Impl → Retro。其核心问题：

1. **Gap/Method/Experiment 过度解耦**：三者之间存在强循环依赖，但被切成三个独立瀑布阶段。方法设计不知道实验约束，实验设计不参与方法组件分解。
2. **经验信号获取过晚**：必须走完 R1→R6（6 个阶段）才能接触代码。核心假设在设计阶段从未被实验验证，导致高概率全链返工。
3. **审查一刀切**：三次 Review 共享同一个框架模板，但战略判断（方向对不对）和技术判断（做法对不对）需要完全不同的思维模式。
4. **回退粒度过粗**：所有失败统一回退到 R1。方法某组件有问题时，不必从问题定义开始重做。
5. **文档版本混乱**：迭代时文档覆盖 vs 新建不统一，AI Agent 难以区分"当前版本"和"历史版本"。

### 1.2 重构原则

- **按决策性质切分阶段**，而非按文档类型切分
- **耦合的设计决策放在同一阶段**：gap + 攻击角度共同设计；method + experiment 联合设计
- **经验信号前置**：在完整方法设计之前，用最小成本验证核心直觉
- **审查按决策层次分化**：战略审查（值不值得做）vs 技术审查（做得对不对）
- **分层回退**：失败根因在哪个层次，就回退到哪个阶段
- **文档版本统一机制**：单文件 + 元数据版本号 + iteration-log 记录变更历史

---

## 二、阶段定义

### 2.0 阶段总览

| 阶段 | 代号 | 核心决策问题 | 性质 | Tier | Multi-Agent | Codex |
|------|------|-------------|------|------|-------------|-------|
| 种子验证 | S | 这个方向值不值得探索？ | 交互式 🗣️ | — | 6 debaters + synthesizer | — |
| 问题锐化 | C | 精确的 Gap 是什么？攻击角度是什么？如何最小验证？ | 自动化 | heavy | — | — |
| 战略审查 | RS | 方向+攻击角度值得投入吗？ | 审查 🔒 | heavy | 4 debaters + synthesizer | ✓ |
| 探针实验 | P | 核心直觉有没有经验信号？ | 手动 🔧 | — | — | — |
| 联合设计 | D | 完整的方法+实验方案是什么？ | 自动化 | heavy | — | — |
| 技术审查 | RT | 方法逻辑自洽吗？实验能有效验证吗？ | 审查 🔒 | heavy | 6 debaters + synthesizer | ✓ |
| 实现规划 | I | 代码怎么组织？执行什么顺序？ | 自动化 | standard | — | — |
| 实验执行 | E | 结果是否支持 claims？ | 手动 🔧 | — | — | — |
| 论文写作 | W | 如何讲好故事？ | 自动化 | (P1-P7) | (保持现有) | (保持现有) |
| 知识回收 | R | 这个项目贡献了什么知识？ | 自动化 | heavy | — | — |

### 2.1 正常流程

```
S → C → RS(pass) → P(signal) → D → RT(pass) → I → E(success) → W → R → complete
```

### 2.2 与 v1 的对应关系

```
v1                              v2
─────────────────────────────────────────────
Startup                    →    S（保持不变）
R1 Gap Discovery           ─┐
                            ├→  C（gap + 攻击角度 + 探针方案，不可分离）
R2 Gap Review              →   RS（战略审查：合并审查 gap + 攻击角度 + 探针可行性）
（无）                      →   P（全新阶段：探针实验）
R3 Method Design           ─┐
R4 Method Review            ├→  D + RT（方法实验联合设计 + 统一技术审查）
R5 Experiment Design       ─┤
R6 Experiment Review       ─┘
R7 Impl Planning           →   I（保持不变，增加探针代码复用评估）
R8 Retrospective           →   R（移到最后，可标记 validated/refuted）
Coding                     →   E（保持不变，增强失败诊断）
Paper                      →   W（保持不变）
```

核心阶段数：v1 = 8 研究阶段 + 3 审查 = 11；v2 = 7 核心阶段 + 2 审查 = 9。

---

## 三、文档版本控制策略

### 3.1 核心策略：单文件 + 元数据版本号 + iteration-log

**原则**：每个文档从始至终只维护一份文件。不新建 v1/v2 后缀文件。版本信息通过三个机制追踪：

| 机制 | 存储位置 | 用途 | 读者 |
|------|---------|------|------|
| **文档元数据** | 各文档头部 YAML frontmatter | 标记当前版本号 | Agent（读取当前版本状态） |
| **iteration-log.md** | 项目根目录 | 结构化变更历史（what + why + excluded） | Agent（理解迭代历史、避免重复方向） |
| **git history** | .git | 完整文件级 diff | 人类（需要时回溯具体内容） |

### 3.2 版本号规则

采用 **`<major>.<minor>`** 二级版本号：

| 级别 | 触发条件 | 版本变化 | 含义 |
|------|---------|---------|------|
| **Major**（大迭代） | E 或 P 回退导致重写 | `1.x → 2.0` | 方向或方法的根本性变更 |
| **Minor**（小修改） | Review 后 Revise | `1.0 → 1.1` | 在当前方向内的改进修正 |

**示例版本演进**：
```
problem-statement.md:
  1.0  首次编写
  1.1  RS 审查后修改（补充攻击角度论证）
  1.2  RS 二次审查后修改
  2.0  探针失败，更换攻击角度（P → C pivot）
  2.1  RS 审查后修改
  3.0  实验失败，重新定义问题（E → C pivot）
```

### 3.3 文档元数据格式

每个研究文档头部统一使用以下 frontmatter：

```yaml
---
version: "1.2"
created: "2026-03-13"
last_modified: "2026-03-15"
entry_mode: "rs_revise"        # first | rs_revise | probe_pivot | rt_revise | execute_iterate | execute_pivot
iteration_major: 1              # 大迭代轮次
iteration_minor: 2              # 当前大迭代内的小修改次数
---
```

**规则**：
- Agent 每次修改文档时，**必须更新** frontmatter
- Minor 修改（review revise）：`iteration_minor += 1`，`entry_mode` 更新
- Major 修改（pivot/restart）：`iteration_major += 1`，`iteration_minor = 0`，`entry_mode` 更新
- Runner 读取 frontmatter 来判断迭代状态（替代当前的文件存在性推断）

### 3.4 iteration-log.md 格式

项目根目录下的 `iteration-log.md` 记录所有版本变更的结构化历史。**每次版本号变化时追加一条记录**：

```markdown
# Iteration Log

## [2.0] — 2026-03-15 — Direction Pivot (E → C)

- **触发**: Dim 1 实验失败，attention mechanism 在稀疏场景下性能退化
- **诊断层次**: direction_level
- **变更文档**: problem-statement.md (2.0), method-design.md (2.0), experiment-design.md (2.0)
- **排除方向**: attention-based sparse recovery — 原因: 理论上 attention 的 softmax 归一化在极端稀疏(<1%)时导致梯度消失，实验证实
- **从失败中获得的关键洞察**: 稀疏场景需要 hard selection 而非 soft weighting
- **实验数据保留**: `experiments/iter-1/` 目录保留完整实验日志

---

## [1.2] — 2026-03-14 — Review Revise (RS → C)

- **触发**: 战略审查指出攻击角度缺乏理论支撑
- **变更文档**: problem-statement.md (1.2)
- **修改内容**: §2 攻击角度补充了信息论角度的理论论证
- **审查参考**: inner-reviews/strategic-review.md

---

## [1.1] — 2026-03-13 — Review Revise (RS → C)

- **触发**: 战略审查发现 gap 与近期论文 [XXX, 2026] 有重叠
- **变更文档**: problem-statement.md (1.1)
- **修改内容**: §1 Gap 定义增加与 [XXX] 的差异化论证
- **审查参考**: inner-reviews/strategic-review.md

---

## [1.0] — 2026-03-12 — Initial (S → C)

- **项目启动**: 基于 project-startup.md 首次编写
- **创建文档**: problem-statement.md (1.0)
```

**设计要点**：
- **倒序排列**（最新在最上方），方便 Agent 快速读取最近的迭代上下文
- **排除方向必须记录**：这是防止 Agent 重复已失败方向的核心数据
- **关键洞察必须记录**：失败经验是最有价值的知识资产
- Minor 修改记录简洁（2-3 行）；Major 修改记录详尽（包含诊断、排除方向、洞察）

### 3.5 审查文档的版本策略

`inner-reviews/` 下的审查文档（`strategic-review.md`、`technical-review.md`）采用**覆盖策略**：

- 每次审查产生新的 review 文档，直接覆盖旧版
- 审查文档不需要版本号——它服务于**当前这一次**审查决策，历史审查通过 git 回溯
- 审查产出的辩论中间文件（`phase-outcomes/debate/`）同样每次覆盖

**理由**：审查文档的消费者是"下一次 Revise 修改"。一旦 Revise 完成，旧审查文档就失去了作用价值。保留它只会增加 Agent 的阅读负担。

### 3.6 大迭代时的旧文档处理

当发生 Major 版本变更（pivot/restart）时：

1. **不删除旧文档内容**——直接在原文件上修改，旧内容通过 git history 保留
2. **iteration-log.md 记录完整的排除方向和失败原因**——这是 Agent 避免重复的数据源
3. **实验数据按迭代轮次归档**：`experiments/iter-<N>/`——保留可复用的实验日志和代码

**Agent 在 pivot 模式下的行为**：先读 `iteration-log.md` 了解排除方向，再修改文档。不需要读旧版文档（git history），因为 iteration-log 已经提取了必要信息。

---

## 四、Prompt 设计规范

### 4.1 Prompt 解耦原则

每个 phase prompt 必须满足以下解耦要求：

1. **自包含**：一个 Agent 只读这个 prompt + 输入文档，就能完成任务。不依赖对 pipeline 结构的理解。
2. **不引用阶段代号**：prompt 中不出现"R1""Phase C"等管线术语。只描述输入文档名和输出文档名。
3. **不感知迭代机制**：prompt 本身不处理"这是第几次迭代"。迭代上下文由 Runner 在 prompt 末尾注入，prompt 只需要定义"如果收到迭代上下文，应该如何行动"。
4. **不感知 tier**：prompt 不知道自己是 heavy 还是 standard。角色定义（"你是严格的独立审查者"vs"你是协作的 Co-Author"）由 Runner 根据 tier 注入 preamble。

**解耦的连接机制是 Runner**——Runner 负责：选择 prompt → 注入 tier preamble → 注入输入文档路径 → 注入迭代上下文 → 注入 lessons → 注入 X-reflect。Prompt 本身是纯粹的任务指令。

### 4.2 标准 Prompt 结构

所有 phase prompt 统一采用以下结构：

```markdown
# <Phase Name>

## 角色与核心目标

你是 [角色描述]。你的核心任务是 [一句话目标]。

你必须产出 [输出文档名]。

## 输入文档

### 必读文档
- `<doc_path>`: [该文档中需要提取什么信息，用于什么目的]
- `<doc_path>`: [...]

### 选读文档（如果存在）
- `<doc_path>`: [在什么条件下需要读，读了之后如何使用]

### 知识库资源（如果提供）
- Episteme `<asset_type>`: [如何使用这类知识资产]

## 行动流程

按以下步骤执行：

### Step 1: [步骤名]
[具体指令]

### Step 2: [步骤名]
[具体指令]

...

## 输出规范

### 输出文档结构
[完整的输出文档模板/大纲]

### 元数据更新
[frontmatter 更新规则]

### 质量标准
[这个阶段的输出必须满足什么条件才算合格]

## 迭代上下文处理

> 以下内容仅在 Runner 注入迭代上下文时适用。首次执行时忽略本节。

### 如果收到 Review Revise 上下文
[如何基于审查意见修改，而非从头重写]

### 如果收到 Pivot 上下文
[如何利用失败经验、避免重复方向、保留可复用内容]

## 禁止事项
- [明确列出该阶段不应该做的事]
```

### 4.3 各阶段 Prompt 设计

---

#### S — 种子验证 Prompt

**保持现有 `start-skill.md` 基本不变。** 这是唯一的交互式阶段，设计已经成熟。

微调：
- Startup 输出模板中增加"候选攻击角度"字段（1-2 段描述，为 C 阶段提供起点）
- 明确标注"攻击角度是初步直觉，不是方法设计"

---

#### C — 问题锐化 Prompt

```
文件名: crystallize-prompt.md
```

**角色与核心目标**：

你是一位资深研究科学家，正在将模糊的研究直觉精确化为可操作的研究计划。你的核心任务是：**同时**完成三个不可分离的设计决策——精确定义研究缺口（Gap）、确定攻击角度（Attack Angle）、设计最小验证实验（Probe）。

这三者之间存在循环依赖：Gap 的"可解性"取决于攻击角度是否可信；攻击角度的选择取决于 Gap 的根因类型；Probe 的设计取决于 Gap 和攻击角度的组合。因此它们必须在同一次思考中共同设计。

**输入文档**：

| 文档 | 必读 | 提取什么 |
|------|------|---------|
| `project-startup.md` | ✓ | 研究种子、核心假设、辩论结论、候选攻击角度 |
| Episteme: Gaps & Assumptions | ✓ | 已知缺口、隐含假设、交叉连接 |
| Episteme: Cross-Paper Connections | ✓ | 跨论文关系，用于组合创新 |
| Episteme: Methods Bank | 选读 | 已有方法的适用性，用于评估攻击角度可行性 |
| `iteration-log.md` | 如存在 | 已排除方向、失败经验 |

**行动流程**：

1. **Gap 候选生成**（继承 v1 R1 的 5 种策略）：Future Work 组合、假设矛盾、方法局限 × 领域需求、跨论文挖掘、主动关联
2. **Gap 评价与选择**（三维矩阵：重要性、新颖性、可解性）——注意"可解性"必须基于对候选攻击角度的评估，不能在没有攻击思路的情况下评价可解性
3. **Root Cause 分析**（技术局限 / 错误假设 / 忽视维度）
4. **RQ 表述**（具体、可回答、可验证、可证伪）
5. **攻击角度设计**：基于 root cause 类型，从 Methods Bank + 跨领域搜索中识别候选攻击思路。每个候选写 1-2 段：核心 idea、为什么可能有效、与 root cause 的匹配关系。选择一个最优攻击角度并论证选择理由
6. **探针方案设计**：核心假设（"如果这一点不成立，整个方向就不成立"）、最小实验方案（规模、数据、代码量）、pass 标准（具体数字）、时间预算（小时级）、fail 时的信息价值（即使 fail 也能学到什么）
7. **初始化 `contribution.md`**

**输出**：`research/problem-statement.md`

**输出文档结构**：

```markdown
---
version: "1.0"
created: "<date>"
last_modified: "<date>"
entry_mode: "first"
iteration_major: 1
iteration_minor: 0
---

# Problem Statement

## 1. Gap 定义
### 1.1 现有方法概览
### 1.2 Gap 陈述（一句话 + 详细分析）
### 1.3 Root Cause 分析（类型 + 论证）
### 1.4 Gap 评价（重要性 / 新颖性 / 可解性）
### 1.5 Research Questions

## 2. 攻击角度
### 2.1 候选攻击角度（简表）
### 2.2 选定攻击角度（核心 idea + 为什么可能有效 + 与 root cause 的匹配）
### 2.3 攻击角度的局限性与风险

## 3. 探针方案（Dim 0）
### 3.1 核心假设（如果这一点不成立，整个方向就不成立）
### 3.2 最小实验方案
### 3.3 Pass 标准（具体数字）
### 3.4 时间预算
### 3.5 Fail 时的信息价值

## 4. 元数据
```

**迭代上下文处理**：

- **RS-Revise**：读审查意见，定位修改点，在原文档上修改对应段落。不重新生成 Gap 候选列表（除非审查明确要求）
- **Probe-Pivot**：Gap 定义可能保留（如果探针失败是攻击角度的问题而非 Gap 的问题），重点重新设计 §2 攻击角度和 §3 探针方案。读 `probe-results.md` 理解失败原因，读 `iteration-log.md` 确认排除方向
- **Execute-Pivot**：Gap 定义和攻击角度都可能需要重新审视。读 `result.md` 和 `iteration-log.md` 理解完整失败路径

**禁止事项**：
- 不做完整的方法设计（组件分解、理论分析等属于 D 阶段）
- 不做完整的实验设计（Dim 1-4 属于 D 阶段）
- 不做文献综述（只读支持 Gap/攻击角度评价的材料）
- 攻击角度描述不超过 2 段话（防止越界成方法设计）

**设计理念**：

C 阶段的 prompt 是整个流程中最关键的创新。它的核心挑战是让 Agent **同时思考三个互相依赖的问题**，而不是串行解决。prompt 必须明确传达这种耦合关系，特别是 Step 2 中"可解性评价必须基于攻击角度"这一约束。

与上游 S 的解耦：C 只知道"我收到一份 project-startup.md"，不知道 Startup 的六维辩论机制。它从 startup 中提取研究种子和候选攻击角度作为起点。

与下游 RS 的解耦：C 只负责产出 problem-statement.md。RS 如何审查、用什么 debaters，C 不知道。

与下游 P 的解耦：C 设计探针方案（§3），但不执行。P 阶段读取 §3 执行实验，C 不知道 P 如何执行。

---

#### RS — 战略审查 Prompt

```
文件名: strategic-review-prompt.md
审查配置: review-configs/strategic-review.yaml
```

**角色与核心目标**：

你是独立的研究方向评审委员会。你的核心任务是判断：**这个研究方向 + 这个攻击角度 + 这个探针方案，值不值得投入时间去验证？**

这是一个战略决策，不是技术细节审查。你不需要评价方法的组件分解是否合理（那是技术审查的工作），你只需要判断：方向有没有前途？攻击角度在直觉上有没有可能 work？探针能不能有效验证核心假设？

**Multi-Agent 设计**：

4 个 debaters（并行、互不可见）+ 1 个 synthesizer（顺序）：

| Debater | 核心视角 | 负责审查维度 |
|---------|---------|------------|
| **Contrarian** | 构建最强反驳 | Gap 真实性、是否为伪问题、攻击角度的致命缺陷 |
| **Comparativist** | 文献对照 + 在线搜索 | Gap 新颖性、近期竞争工作、攻击角度是否已被尝试 |
| **Pragmatist** | 可行性约束 | 探针可执行性、资源约束、时间预算合理性 |
| **Interdisciplinary** | 跨领域视角 | 其他领域的更好问题框定、替代攻击角度 |

**Codex 外部审查**：并行调用 GPT-4.5-high，提供独立第三方视角。非阻塞——MCP 不可用时静默跳过。

**审查维度**（7 项）：
1. Gap 真实性：是真正的未解决缺口还是伪问题？
2. Gap 重要性：影响力是否足以支撑一篇论文？
3. Gap 新颖性 + 在线检查：近期有无竞争工作？
4. Root cause 深度：是否可以挖得更深？
5. 攻击角度可信度（**新增**）：这个思路在直觉上有没有可能 work？与 root cause 匹配吗？
6. 探针方案合理性（**新增**）：Dim 0 能否有效验证核心假设？pass 标准合理吗？
7. RQ 可回答性与可证伪性

**出口路由**：

| 判定 | 去向 | entry_context.mode |
|------|------|-------------------|
| pass | → P | — |
| revise | → C | rs_revise |
| abandon | → R | — |

**设计理念**：

RS 的 prompt 与 v1 R2 的核心区别是审查范围更大（同时审查 gap + 攻击角度 + 探针），但审查深度更浅（战略层面，不涉及方法组件细节）。Debater 的选择侧重"方向判断"：Contrarian 找致命缺陷，Comparativist 确认新颖性，Pragmatist 验证探针可行性，Interdisciplinary 提供替代视角。

不包含 Theorist 和 Methodologist——因为此时没有完整方法设计，理论审查和方法学审查无从开展。

Codex 在此阶段的价值是提供完全外部的视角（不受系统 prompt 影响的 LLM），适合判断"这个方向是否有人已经在做"这类需要广泛知识的问题。

---

#### P — 探针实验（手动阶段）

```
无 Agent prompt（手动阶段）
引导文档: probe-guide.md（提供给研究者的执行指南）
```

**核心目标**：用最小成本验证核心直觉是否有经验信号。

**执行者**：研究者（人类），不是 AI Agent。

**输入**：`research/problem-statement.md` §3 探针方案

**输出**：`research/probe-results.md`

**输出文档结构**：

```markdown
---
version: "1.0"
created: "<date>"
last_modified: "<date>"
---

# Probe Results

## 1. 探针假设
[从 problem-statement.md §3.1 复制]

## 2. 实际实验描述
[具体做了什么：代码、数据、设置]

## 3. 定量结果
| 指标 | Pass 标准 | 实际值 | 判定 |
|------|----------|-------|------|
| ... | ... | ... | ✓/✗ |

## 4. 判定
signal / no-signal / ambiguous

## 5. 意外发现
[实验过程中的意外观察——这往往是最有价值的部分]

## 6. 修正后的直觉
[基于实验结果，对问题/攻击角度的理解发生了什么变化]

## 7. 代码与数据
[探针代码位置、可复用组件、数据位置]
```

**出口判断**：研究者自行判断，调用 Runner 的 advance 命令时指定 outcome：

```bash
# 有信号，进入联合设计
python3 research_runner.py advance <project_path> --outcome signal

# 无信号但问题有价值，换攻击角度
python3 research_runner.py advance <project_path> --outcome pivot

# 放弃
python3 research_runner.py advance <project_path> --outcome abandon
```

**设计理念**：

P 阶段是全新的设计。它存在的核心理由是：**在 DL 研究中，一个下午的实验结果往往比一周的文献分析更能指明方向。** 把经验信号的获取从 E 阶段（流程末尾）前置到 P 阶段（流程前段），是整个 v2 重构中 ROI 最高的改变。

P 是手动阶段，不需要 AI Agent prompt。但提供 `probe-guide.md` 作为执行指南，提醒研究者：
- 探针不是缩小版的完整实验——它验证的是**核心假设**，不是方法效果
- 时间预算严格遵守（problem-statement.md §3.4 定义的小时数）
- 即使 fail 也要记录信息价值（§3.5 定义的"fail 时学到什么"）
- 意外发现要详细记录——方向的调整往往来自意外观察

---

#### D — 联合设计 Prompt

```
文件名: joint-design-prompt.md
```

**角色与核心目标**：

你是一位经验丰富的研究科学家，正在将经过验证的研究直觉发展为完整的方法和实验方案。你的核心任务是：**基于探针实验的经验信号，同时完成方法设计和实验设计，确保两者紧密耦合。**

"同时"的含义是：每设计一个方法组件，立即设计它的验证实验（ablation）。每设计一个实验，确认它在验证一个明确的方法 claim。方法和实验不是两个独立的文档——它们是同一个设计决策的两个视角。

**输入文档**：

| 文档 | 必读 | 提取什么 |
|------|------|---------|
| `research/problem-statement.md` | ✓ | Gap、RQ、攻击角度、探针方案 |
| `research/probe-results.md` | ✓ | Dim 0 结果、意外发现、修正后的直觉、可复用代码 |
| Episteme: Methods Bank | ✓ | 已有方法的组件、适用条件、局限性 |
| Episteme: Experimental Patterns | ✓ | 验证模式、baseline 选择经验 |
| `iteration-log.md` | 如存在 | 已排除的方法方案、失败原因 |

**行动流程**：

1. **探针结果消化**：从 probe-results.md 提取关键经验信号——什么 work 了、什么没 work、意外发现意味着什么。这些信号直接约束方法设计空间
2. **方法框架设计**：
   a. 解空间探索（跨领域方法搜索，不局限于本领域）
   b. 方法框架组装（Root cause → 组件组合 + 新连接 → 为什么能解决）
   c. **每个组件立即设计验证方案**：组件 X 做什么 → 移除/替换 X 的 ablation → 预期 ablation 结果 → 如果 ablation 不显著怎么解释
   d. 严格因果论证链（每一步：逻辑推理，不跳跃）
   e. 理论分析（如适用）
   f. 方法定位（继承了什么、改变了什么、与最近方法的差异）
3. **实验矩阵设计**：
   a. Dim 0 → Dim 1 衔接（探针方案如何自然扩展为完整实验）
   b. Dim 1：核心验证（主实验 + 上面已设计的 ablations + counterfactual if possible）
   c. Dim 2：应用价值（下游任务）
   d. Dim 3：效率验证（计算成本分析）
   e. Dim 4：科学发现（如果 Dim 1 成功，可以回答什么新问题）
4. **Baseline 选择**：覆盖 SOTA，来源于 Methods Bank，论证选择理由
5. **指标定义**：每个指标与 RQ 的语义对齐
6. **风险与失败预测**：每个实验的失败模式 + 备选方案
7. **更新 `contribution.md`**

**输出**：`research/method-design.md` + `research/experiment-design.md`（两个文件，通过交叉引用关联）+ 更新 `research/contribution.md`

**method-design.md 中的交叉引用示例**：

```markdown
### Component: Sparse Attention Module
- **功能**: 在极端稀疏场景下执行 hard selection
- **输入/输出**: [...]
- **验证方案**: → experiment-design.md §Ablation-2（移除 hard selection，替换为 standard softmax attention）
- **预期 ablation 结果**: 性能在稀疏度 < 1% 时下降 > 15%
```

**experiment-design.md 中的反向引用示例**：

```markdown
### Ablation-2: Hard Selection vs Soft Attention
- **移除组件**: method-design.md §Component: Sparse Attention Module
- **替换方案**: standard softmax attention
- **验证的 claim**: hard selection 对极端稀疏场景是必要的
- **预期结果**: [...]
```

**迭代上下文处理**：

- **RT-Revise**：读技术审查意见，定位需要修改的组件/实验，在原文档上修改。保留未被质疑的部分
- **E-Iterate（方法层）**：读 result.md 理解哪些组件有问题。保留已验证有效的组件，只重新设计失败组件及其对应实验。读 iteration-log.md 确认排除方案

**禁止事项**：
- 不重新定义 Gap 或 RQ（那是 C 阶段的工作）
- 不写代码或实现细节（那是 I 阶段的工作）
- 不执行实验（那是 E 阶段的工作）
- 不忽视探针结果——方法设计必须与探针经验一致

**设计理念**：

D 阶段是 v2 中变化最大的阶段。它合并了 v1 的 R3（Method）和 R5（Experiment），核心创新是**组件-ablation 同步设计**。prompt 的关键挑战是让 Agent 在思考方法的同时思考验证——而不是先设计完整方法再设计实验。Step 2c 是实现这一点的关键步骤。

与上游 C/P 的解耦：D 只知道"我收到 problem-statement.md 和 probe-results.md"。它不知道 C 如何生成 Gap，也不知道 P 如何执行探针。

与下游 RT 的解耦：D 产出两个文档，RT 如何审查、用什么标准，D 不知道。

与探针结果的耦合：这是唯一有意的耦合——D 必须基于 probe-results.md 设计方法。prompt 在 Step 1 要求 Agent 首先消化探针结果，确保后续设计受到经验信号的约束。

**不引入 Multi-Agent 的理由**：方法设计和实验设计是一个紧密耦合的创造性过程，需要单一思维的连贯性。如果用多个 Agent 分别设计方法和实验，会失去"组件-ablation 同步"的核心优势。审查（质疑、验证）交给 RT 阶段的 multi-agent 辩论。

---

#### RT — 技术审查 Prompt

```
文件名: technical-review-prompt.md
审查配置: review-configs/technical-review.yaml
```

**角色与核心目标**：

你是独立的技术评审委员会。你的核心任务是同时审查两个紧密关联的问题：**方法在逻辑上是否站得住？实验能否有效验证我们的 claims？**

与战略审查（RS）不同，你不质疑方向是否值得做（那个问题已经通过了战略审查 + 探针验证）。你关注的是：在这个方向上，这套方法+实验设计**做得对不对**。

**Multi-Agent 设计**：

6 个 debaters（并行、互不可见）+ 1 个 synthesizer（顺序）：

| Debater | 核心视角 | 负责审查维度 |
|---------|---------|------------|
| **Theorist** | 数学/理论正确性 | 逻辑闭合、理论保证、隐含假设 |
| **Methodologist** | 评估协议完整性 | 数据泄漏、超参选择、proxy 指标、ablation 覆盖 |
| **Empiricist** | 实验科学性 | Dim 0→1 衔接、统计效力、可复现性、baseline 公平 |
| **Skeptic** | 极端怀疑 | 最弱组件、最可能失败点、替代解释 |
| **Pragmatist** | 工程可行性 | 计算资源、实现复杂度、时间估计 |
| **Contrarian** | 构建最强反驳 | 与探针结果的一致性、过拟合探针信号的风险 |

**Codex 外部审查**：并行调用 GPT-4.5-high。非阻塞。

**审查维度**（10 项，合并 v1 R4 + R6）：

方法侧：
1. 逻辑闭合（Gap → Root → Method → Why Solves）
2. 组件必要性（remove-one 分析）
3. 理论正确性
4. 与探针结果的一致性（**新增**）

实验侧：
5. RQ 覆盖度
6. Baseline 公平性与时效性（含在线检查）
7. Ablation 完整性
8. Dim 0 → Dim 1 衔接（**新增**）
9. 评估协议完整性

联合维度：
10. **方法-实验对齐**（**核心新增**）：每个方法组件是否都有对应 ablation？每个实验是否都在验证明确的 claim？交叉引用是否一致？

**出口路由**：

| 判定 | 含义 | 去向 | entry_context.mode |
|------|------|------|-------------------|
| pass | 方法+实验均通过 | → I | — |
| revise | 技术问题，方向正确 | → D | rt_revise |
| fundamental | 问题定义层面有误 | → C | execute_pivot (diagnosis=direction) |
| abandon | 不可救药 | → R | — |

**设计理念**：

RT 合并了 v1 的 R4（Method Review）和 R6（Experiment Review）。合并的核心原因是审查维度 10（方法-实验对齐）——这个最关键的审查维度在 v1 中**无法实现**，因为 R4 审查 Method 时 Experiment 还没设计，R6 审查 Experiment 时 Method 已经定型。

6 debaters 的选择兼顾了方法审查（Theorist、Skeptic）和实验审查（Methodologist、Empiricist），并增加了 Contrarian 的新职责——审查设计是否过度拟合探针信号。这是 v2 特有的风险：Agent 可能因为探针成功而过度乐观，设计出只在探针设置下有效的方法。

RT 新增 `fundamental` 出口。这对应 v1 中 R4 的 `continue_R1` 和 R6 的 `continue_R3`——当技术审查发现问题不在方法/实验层面而在 gap 定义层面时（例如"你定义的 gap 已被近期论文解决"），直接路由到 C。在 v1 中这两个出口的触发条件和语义不够清晰，v2 统一为 `fundamental` 并在 synthesizer prompt 中明确定义触发标准。

---

#### I — 实现规划 Prompt

```
文件名: implementation-prompt.md
```

**角色与核心目标**：

你是一位资深软件架构师。你的核心任务是：**将研究设计翻译为可执行的代码计划，使得一个新 AI Agent（无前期上下文）能独立完成实现。**

**输入文档**：

| 文档 | 必读 | 提取什么 |
|------|------|---------|
| `research/method-design.md` | ✓ | 方法组件、接口、依赖关系 |
| `research/experiment-design.md` | ✓ | 实验矩阵、baseline、指标 |
| `research/probe-results.md` | ✓ | 可复用代码/基础设施（§7） |

**新增与 v1 R7 的区别**：
- 评估探针代码的可复用性，作为实现计划的起点（而非从零开始）
- `Codes/CLAUDE.md` 中包含探针代码的引用和改造说明

**输出**：`Codes/code-todo.md`、`Codes/experiment-todo.md`、`Codes/CLAUDE.md`

**不引入 Multi-Agent 和 Codex 的理由**：这是一个执行性、模板化的翻译工作，不涉及创造性判断或方向性决策。单 Agent（standard tier）足够。

**设计理念**：

I 阶段基本保持 v1 R7 不变。唯一的增强是探针代码复用评估——这确保了 P 阶段的工程投入不会浪费。prompt 的解耦方式与 v1 相同：只引用输入文档名，不引用管线术语。

---

#### E — 实验执行（手动阶段）

```
无 Agent prompt（手动阶段）
失败诊断通过 /praxis-conclude 执行
```

**出口判断增强**：

`/praxis-conclude` 在 v2 中增加**失败层次诊断**。研究者或 AI 必须回答：

```markdown
## 失败诊断

### 失败层次（必选一项）
- [ ] 执行层（bug、工程问题）→ 留在 E 修复
- [ ] 方法层（某组件不 work，但方向正确）→ iterate_method → D
- [ ] 方向层（核心假设不成立，方向有问题）→ iterate_direction → C

### 诊断依据
[具体的实验证据：哪个实验、什么结果、与预期的偏差]

### 如果回退到 D
- 需要修改的组件: [列表]
- 应该保留的组件: [列表 + 理由]
- 已排除的替代方案: [列表 + 理由]

### 如果回退到 C
- Gap 定义是否仍然有效: [是/否 + 理由]
- 攻击角度的失败原因: [具体分析]
- 从失败中获得的关键洞察: [用于指导下一轮 C]
```

**迭代守卫**：
- D 回退 ≥ 2 次 → 强制升级到 C 回退
- C 回退 ≥ 3 次 → 触发 abandon 评估（Exit Assessment Gate SubAgent）

---

#### R — 知识回收 Prompt

```
文件名: retrospective-prompt.md
```

**角色与核心目标**：

你是一位研究历史学家。你的核心任务是：**从这个项目的完整生命周期中提取可复用的知识资产，更新 Episteme 知识库。**

**与 v1 R8 的核心区别**：

v1 R8 在 coding 前执行，所有知识资产标记 `[? pending validation]`。v2 R 在**论文完成后或 abandon 时**执行，可以基于实验结果标记：
- `[✓ validated]`：实验支持
- `[✗ refuted]`：实验否定
- `[~ partially validated]`：部分支持

**输入文档**：全部研究文档 + `result.md` + `iteration-log.md` + 论文（如有）

**输出**：`research/retrospective.md` + Episteme 知识库更新

**不引入 Multi-Agent 的理由**：知识回收是归纳性工作（从已有材料中提取模式），不涉及多角度辩论。单 Agent（heavy tier，因为需要深度理解和跨文档关联）足够。

---

## 五、完整状态转移表

### 5.1 PHASES 字典（研究状态机）

```python
PHASES = {
    "C": {
        "skill": "crystallize",
        "output_doc": "research/problem-statement.md",
        "tier": "heavy",
        "outcome_type": "work",
        "transitions": {"done": "RS"}
    },
    "RS": {
        "skill": "strategic-review",
        "output_doc": "inner-reviews/strategic-review.md",
        "tier": "heavy",
        "outcome_type": "review",
        "codex_agent": "codex-reviewer",
        "debate_agents": ["contrarian", "comparativist", "pragmatist", "interdisciplinary"],
        "transitions": {
            "pass": "P",
            "revise": "C",      # entry_context: rs_revise
            "abandon": "R"
        }
    },
    "P": {
        "skill": None,          # 手动阶段
        "output_doc": "research/probe-results.md",
        "tier": None,
        "outcome_type": "manual",
        "transitions": {
            "signal": "D",
            "pivot": "C",       # entry_context: probe_pivot
            "abandon": "R"
        }
    },
    "D": {
        "skill": "joint-design",
        "output_doc": ["research/method-design.md", "research/experiment-design.md"],
        "tier": "heavy",
        "outcome_type": "work",
        "transitions": {"done": "RT"}
    },
    "RT": {
        "skill": "technical-review",
        "output_doc": "inner-reviews/technical-review.md",
        "tier": "heavy",
        "outcome_type": "review",
        "codex_agent": "codex-reviewer",
        "debate_agents": ["theorist", "methodologist", "empiricist", "skeptic", "pragmatist", "contrarian"],
        "transitions": {
            "pass": "I",
            "revise": "D",      # entry_context: rt_revise
            "fundamental": "C", # entry_context: execute_pivot (direction)
            "abandon": "R"
        }
    },
    "I": {
        "skill": "implementation",
        "output_doc": ["Codes/code-todo.md", "Codes/experiment-todo.md", "Codes/CLAUDE.md"],
        "tier": "standard",
        "outcome_type": "work",
        "transitions": {"done": "E"}
    },
    "E": {
        "skill": None,          # 手动阶段
        "output_doc": "research/result.md",
        "tier": None,
        "outcome_type": "manual",
        "transitions": {
            "success": "W",
            "iterate_method": "D",      # entry_context: execute_iterate
            "iterate_direction": "C",   # entry_context: execute_pivot
            "abandon": "R"
        }
    },
    "W": {
        "skill": None,          # 独立 paper pipeline
        "tier": None,
        "outcome_type": "manual",
        "transitions": {"done": "R"}
    },
    "R": {
        "skill": "retrospective",
        "output_doc": "research/retrospective.md",
        "tier": "heavy",
        "outcome_type": "work",
        "transitions": {"done": "complete"}
    },
    "complete": {
        "skill": None,
        "tier": None,
        "outcome_type": "terminal",
        "transitions": {}
    }
}
```

### 5.2 pipeline-status.json 格式

```json
{
    "phase": "D",
    "entry_context": {
        "mode": "execute_iterate",
        "source_phase": "E",
        "iteration": 1,
        "diagnosis": "method_level",
        "d_iteration_count": 1,
        "c_iteration_count": 0
    },
    "history": [
        {"phase": "C", "mode": "first", "version": "1.0", "date": "2026-03-12"},
        {"phase": "RS", "outcome": "pass", "date": "2026-03-12"},
        {"phase": "P", "outcome": "signal", "date": "2026-03-13"},
        {"phase": "D", "mode": "first", "version": "1.0", "date": "2026-03-13"},
        {"phase": "RT", "outcome": "pass", "date": "2026-03-14"},
        {"phase": "I", "date": "2026-03-14"},
        {"phase": "E", "outcome": "iterate_method", "diagnosis": "method_level", "date": "2026-03-15"}
    ]
}
```

`history` 数组记录完整的阶段执行历史（纯追加），用于迭代守卫和 retrospective 回顾。

### 5.3 Entry Context 注入逻辑

Runner 在构建 fork_prompt 时，根据 `entry_context.mode` 执行不同的注入：

| mode | 注入的额外文档 | 注入的指令关键词 |
|------|--------------|----------------|
| `first` | （无） | "从零开始" |
| `rs_revise` | `inner-reviews/strategic-review.md` | "基于审查修改，不重启" |
| `probe_pivot` | `research/probe-results.md` + `iteration-log.md` | "探针失败，换攻击角度，禁止重复已排除方向" |
| `rt_revise` | `inner-reviews/technical-review.md` | "基于技术审查修改" |
| `execute_iterate` | `research/result.md` + `iteration-log.md` | "方法层问题，修改失败组件，保留有效组件" |
| `execute_pivot` | `research/result.md` + `iteration-log.md` + 下游文档(参考) | "方向层问题，重新审视 Gap 和攻击角度" |

---

## 六、文档流全景图

```
project-startup.md ──────────────────────────────────────────────────┐
    │                                                                │
    ↓                                                                │
research/problem-statement.md ←──── Episteme (Gaps, Connections)     │
    │   §1 Gap  §2 攻击角度  §3 探针方案  §4 contribution.md初始化     │
    │                                                                │
    ├──→ inner-reviews/strategic-review.md (RS 产出)                  │
    │                                                                │
    ↓                                                                │
research/probe-results.md                                            │
    │   §3 结果  §5 意外发现  §6 修正直觉  §7 可复用代码              │
    │                                                                │
    ├──────────────┐                                                  │
    ↓              ↓                                                  │
research/         research/              ←── Episteme (Methods,      │
method-design.md  experiment-design.md        Patterns)              │
    │ (交叉引用)      │                                               │
    │              │                                                  │
    ├──→ inner-reviews/technical-review.md (RT 产出)                  │
    │                                                                │
    ↓                                                                │
Codes/code-todo.md                                                   │
Codes/experiment-todo.md                                             │
Codes/CLAUDE.md ←── probe-results.md §7（复用探针代码）               │
    │                                                                │
    ↓                                                                │
research/result.md                                                   │
    │                                                                │
    ├──→ Papers/ (W 阶段，独立 pipeline)                              │
    │                                                                │
    ↓                                                                │
research/retrospective.md                                            │
    │                                                                │
    └──→ Episteme 更新（标记 validated/refuted）                       │
                                                                     │
iteration-log.md ←── 每次版本变更时追加 ─────────────────────────────┘
contribution.md  ←── C 初始化，D 更新，I 最终化
```

---

## 七、项目目录结构（v2）

```
<project>/
├── CLAUDE.md                    ← 项目元数据（noesis_path、当前阶段等）
├── project-startup.md           ← S 阶段产出
├── iteration-log.md             ← 版本变更历史（跨阶段共享）
├── pipeline-status.json         ← 状态机状态（含 entry_context + history）
│
├── research/                    ← 研究文档（单文件，元数据版本号）
│   ├── problem-statement.md     ← C 阶段产出（gap + 攻击角度 + 探针方案）
│   ├── probe-results.md         ← P 阶段产出（探针实验结果）
│   ├── method-design.md         ← D 阶段产出（方法设计，含实验交叉引用）
│   ├── experiment-design.md     ← D 阶段产出（实验设计，含方法交叉引用）
│   ├── contribution.md          ← C 初始化 → D 更新 → I 最终化
│   ├── result.md                ← E 阶段产出（实验结果）
│   └── retrospective.md         ← R 阶段产出
│
├── inner-reviews/               ← 审查文档（覆盖策略，不保留历史版本）
│   ├── strategic-review.md      ← RS 阶段产出
│   └── technical-review.md      ← RT 阶段产出
│
├── codex-reviews/               ← 外部 AI 审查（仅参考）
│
├── phase-outcomes/              ← 阶段结果 JSON + 辩论中间文件
│   ├── C.json
│   ├── RS.json
│   ├── D.json
│   ├── RT.json
│   ├── I.json
│   └── debate/
│       ├── RS/                  ← 战略审查辩论
│       │   ├── contrarian.md
│       │   ├── comparativist.md
│       │   ├── pragmatist.md
│       │   ├── interdisciplinary.md
│       │   └── synthesis.md
│       └── RT/                  ← 技术审查辩论
│           ├── theorist.md
│           ├── methodologist.md
│           ├── empiricist.md
│           ├── skeptic.md
│           ├── pragmatist.md
│           ├── contrarian.md
│           └── synthesis.md
│
├── Codes/                       ← I 阶段产出
│   ├── CLAUDE.md
│   ├── code-todo.md
│   └── experiment-todo.md
│
├── Papers/                      ← W 阶段（独立 pipeline）
│   ├── paper-status.json
│   └── phase-outcomes/
│
├── experiments/                 ← 实验数据归档
│   ├── probe/                   ← P 阶段探针实验代码/数据
│   └── iter-<N>/                ← 大迭代时的历史实验数据
│
└── pipeline-evolution-log.md    ← X-reflect 反思日志
```

---

## 八、Prompt 文件清单与对应关系

### 8.1 新 Prompt 文件

| 文件名 | 阶段 | 替代 v1 文件 | 变更程度 |
|--------|------|-------------|---------|
| `crystallize-prompt.md` | C | `10-gap-discovery-prompt.md` | **重写**（合并 gap + 攻击角度 + 探针设计） |
| `strategic-review-prompt.md` | RS | `1X-review-prompt.md`(gap 配置) | **重写**（专注战略层面，增加攻击角度+探针审查） |
| `strategic-review.yaml` | RS | `gap-review.yaml` | **重写** |
| `probe-guide.md` | P | （新增） | **新建**（手动阶段执行指南） |
| `joint-design-prompt.md` | D | `11-method-design-prompt.md` + `12-experiment-design-prompt.md` | **重写**（合并方法+实验，增加交叉引用机制） |
| `technical-review-prompt.md` | RT | `1X-review-prompt.md`(method+exp 配置) | **重写**（合并方法审查+实验审查，增加对齐维度） |
| `technical-review.yaml` | RT | `method-review.yaml` + `experiment-review.yaml` | **重写**（合并审查维度） |
| `implementation-prompt.md` | I | `13-impl-planning-prompt.md` | **微调**（增加探针代码复用评估） |
| `retrospective-prompt.md` | R | `14-retrospective-prompt.md` | **中度修改**（移到流程末尾，支持 validated/refuted 标记） |

### 8.2 保留/删除的 v1 文件

| v1 文件 | 处理 | 原因 |
|--------|------|------|
| `1X-review-prompt.md` | **删除** | 拆分为独立的 strategic-review 和 technical-review |
| `gap-review.yaml` | **删除** | 替换为 `strategic-review.yaml` |
| `method-review.yaml` | **删除** | 合并入 `technical-review.yaml` |
| `experiment-review.yaml` | **删除** | 合并入 `technical-review.yaml` |
| `X-reflect-pipeline-prompt.md` | **保留** | 机制不变，每个非手动阶段自动注入 |
| `codex-reviewer-prompt.md` | **保留** | 机制不变 |
| SubAgents（debaters） | **调整** | 保留 6 角色，重新分配到 RS/RT |

### 8.3 模板文件调整

| 模板 | 处理 | 变更 |
|------|------|------|
| `project-start.md` | **微调** | 增加"候选攻击角度"字段 |
| `gap-analysis.md` | **替换** | 改为 `problem-statement.md` 模板（含 gap + 攻击角度 + 探针方案） |
| `method-design.md` | **修改** | 增加交叉引用格式 |
| `experiment-design.md` | **修改** | 增加反向引用格式 |
| `project-claude-md.md` | **修改** | 更新阶段代号和文档列表 |

---

## 九、实现路线

### Phase 1: 状态机与 Runner 重写
1. 重写 `research_state_machine.py`（PHASES 字典、entry_context 机制）
2. 重写 `research_runner.py`（entry_context 注入逻辑、新 prompt 加载）
3. 更新 `pipeline-status.json` 格式（增加 entry_context + history）
4. 更新 `/praxis-conclude` 增加失败层次诊断

### Phase 2: Prompt 重写
1. 编写 `crystallize-prompt.md` (C)
2. 编写 `strategic-review-prompt.md` + `strategic-review.yaml` (RS)
3. 编写 `probe-guide.md` (P)
4. 编写 `joint-design-prompt.md` (D)
5. 编写 `technical-review-prompt.md` + `technical-review.yaml` (RT)
6. 修改 `implementation-prompt.md` (I)
7. 修改 `retrospective-prompt.md` (R)

### Phase 3: 模板与 Skills 更新
1. 更新文档模板（problem-statement.md, method/experiment 交叉引用格式）
2. 更新 `.claude/skills/` 注册
3. 更新 SubAgent 文件（debater 重新分配）
4. 更新 Startup skill（增加候选攻击角度字段）

### Phase 4: 文档更新
1. 更新 `Noesis/CLAUDE.md`（阶段表、架构决策、文件布局）
2. 更新 `Praxis/CLAUDE.md`
3. 更新 `project-claude-md.md` 模板
4. 更新 `introduction.md`

### Phase 5: 验证
1. 在一个新项目上端到端测试完整流程
2. 验证迭代场景（RS revise、P pivot、RT revise、E iterate）
3. 验证版本控制机制（frontmatter 更新、iteration-log 追加）
4. 验证迭代守卫（D ≥ 2 次强制 C、C ≥ 3 次触发 abandon 评估）
