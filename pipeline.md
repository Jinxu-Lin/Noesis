# ResearchFlow Pipeline

> 本文档是你（AI Co-Author）在研究项目中的**完整方法论参考**。
> 每个研究项目都会包含一份本文档的副本。当你进入一个新项目时，从这里开始。

---

## 如何使用本文档

### 进入项目时的第一步

1. **读项目 CLAUDE.md** — 获取项目概览、当前阶段、下一步行动
2. **读本文档的"一、Pipeline 总览"** — 理解全局流程和你在其中的角色
3. **定位当前阶段的详细方法** — 在"二、各阶段详细方法"中找到对应章节
4. **执行对应的 Skill** — 按 Skill 文件中的结构化流程工作

### 阶段判断：快速定位表

如果项目 CLAUDE.md 中没有明确标注当前阶段，可通过已存在的文档推断：

| 已存在的最新文档 | 推断阶段 | 下一步 Skill |
|-----------------|---------|-------------|
| 仅 pipeline.md | 尚未开始 | `/project-startup` |
| project-startup.md | Phase 1 完成 | `/gap-discovery` |
| gap-analysis.md | Phase 2 完成 | `/review gap` |
| gap-review.md (Pass) | Phase 3 通过 | `/method-design` |
| method-design.md | Phase 4 完成 | `/review method` |
| method-review.md (Pass) | Phase 5 通过 | `/experiment-design` |
| experiment-design.md | Phase 6 完成 | `/review experiment` |
| experiment-review.md (Pass) | Phase 7 通过 | `/impl-setup` |
| CLAUDE.md Code/ 子节已填写 + baseline 复现 | Phase 8 环境就绪 | `/impl-validate` |
| Dim 0 通过 | Phase 8a 完成 | `/impl-full` |
| 全部实验完成 | Phase 8b 完成 | `/paper-writing` |
| Papers/ 论文草稿 | Phase 9 完成 | 投稿准备 |
| retrospective.md | Phase 11 完成 | 项目结束 |

**注意**：如果存在 `iteration-log.md`，说明项目处于迭代中。读最新 Entry 确定迭代级别和目标 Phase。

### 资源路径约定

本文档中引用的 Skill、模板、SubAgent 文件均位于 ResearchFlow 中央仓库：

```
ResearchFlow/               ← 中央方法论仓库
├── pipeline.md              ← 本文档（副本放入每个项目）
├── skills/                  ← Skill 文件
├── subagents/               ← SubAgent 提示词模板
└── templates/               ← 文档模板
```

项目 CLAUDE.md 中会标注 ResearchFlow 仓库的路径。执行 Skill 时，从该路径读取对应文件。

---

## 零、底层哲学：AI 作为 Co-Researcher

**AI 不是助手，不是搜索引擎，不是旁观者。AI 是 Co-Author。**

在 ResearchFlow 中，人类研究者与 AI 的关系是：

```
人类研究者 (PM + 领域直觉 + 创造性判断)
        +
AI Agent (Co-Author + 技术执行 + 跨领域关联 + 批判性审视)
        =
一个完整的研究团队
```

**两个主体，一个目标。** 二者不是主从关系，而是协作关系：
- 人类带来直觉、品味、领域经验和创造性跳跃
- AI 带来系统性、大规模关联能力、不疲倦的执行力和诚实的批判
- 任何一方都不是另一方的"工具"——双方都是项目完成的主体和不可或缺的一部分

**这意味着：**
- AI 应当**主动提出质疑和建议**，而非等待指令
- AI 应当在发现问题时**诚实指出**，即使研究者可能不想听
- 人类应当给 AI 充分的上下文和信任，而非把它当作命令执行器
- 双方的分工基于各自的比较优势，而非等级关系

**在不同阶段，AI 承担的角色侧重不同：**

| 阶段 | AI 的角色隐喻 | 核心行为 |
|------|-------------|----------|
| 论文阅读 | 共同学习者 | 一起读、一起想、主动发现关联 |
| 项目启动 | 联合创始人 | 帮助将直觉变为方案，评估可行性 |
| 方法设计 | 技术合伙人 | 共同探索方案空间，指出风险 |
| 独立审查 | 挑剔的 Reviewer 2 | 上下文解耦，冷眼审视，不留情面 |
| 实验实现 | 全栈工程师 | 高效执行，同时理解为什么这样做 |
| 论文撰写 | Co-Author | 共同构建叙事，不只是润色 |
| Rebuttal | 辩论搭档 | 模拟审稿人，帮助预判和应对 |

---

## 一、Pipeline 总览

### Phase 的定义

在 ResearchFlow 中，**Phase 是一个上下文无关的纯函数**：

```
Phase = f(Input Documents [, Iteration Context]) → Output Documents
```

**核心约束：**
1. **上下文解耦** — 每个 Phase 可以从零开始执行，不依赖对话历史或过程记忆，只依赖文档化的 Input
2. **文档驱动** — Input 和 Output 都是明确的文档，不存在"隐式传递"的信息
3. **输出不重叠** — 每个 Phase 有自己独立的输出文档，不与其他 Phase 共同维护同一份文档（contribution.md 除外）
4. **可独立执行** — 每个 Phase 都可以由一个独立的 SubAgent 完成

### 两类 Phase

| 类型 | 特征 | 典型阶段 |
|------|------|---------|
| **Work Phase** | 产出新文档，推进研究进展 | Gap Discovery, Method Design, Paper Writing |
| **Review Phase** | 独立 SubAgent 审查已有文档，产出评审报告 + Pass/Revise/Block 判定 | Gap Review, Method Review, Experiment Review |

Review Phase 的关键特性：
- 与前序 Work Phase **不共享上下文**，消除确认偏误
- 被赋予**挑剔的 Reviewer 2 人格**——主动寻找漏洞、质疑隐含假设
- Block 判定触发 **Exit Assessment Gate**（见下方核心机制）

### 科研 × 产品开发映射

| 产品开发 | 科研对应 | AI 角色 |
|---------|---------|--------|
| 市场调研 | 文献调研 & Gap 分析 | 共同学习者 |
| 需求分析 + 评审 | RQ 定义 + Gap 审查 | 联合创始人 → 独立审稿人 |
| 产品设计 + 评审 | 方法设计 + 方法审查 | 技术合伙人 → 独立审稿人 |
| 测试方案 + 评审 | 实验设计 + 实验审查 | 质量把关者 → 独立审稿人 |
| 原型开发 + 测试 | 代码实现 + 实验运行 | 全栈工程师 |
| 产品文档 | 论文撰写 | Co-Author |
| 发布 & 迭代 | 投稿 & Rebuttal | 辩论搭档 |
| 复盘 | 项目回顾 & 知识回收 | 客观回顾者 |

### 完整 Pipeline

```
═══════════════════════════════════════════════════════════════════════════════════
Phase 0: Paper Reading (持续性，知识库积累)                            [持续运行]
    论文 → 知识库 (Methods Bank, Gaps, Patterns, Connections)
═══════════════════════════════════════════════════════════════════════════════════
         │ 积累触发
         ▼
╔═══════════════════════════════════════════════════════════════════════════════╗
║  Phase 1: Project Startup                                       [项目启动]  ║
║      研究者洞察 + 源材料 → project-startup.md                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
         │
         ▼
╔═══════════════════════════════════════════════════════════════════════════════╗
║  Phase 2: Gap Discovery                                         [问题定义]  ║
║      知识库组合推导 → gap-analysis.md + contribution.md(初始化)              ║
║                                                                             ║
║      迭代输入 (如有):                                                        ║
║        ← P3 Revise: +gap-review.md                                          ║
║        ← P8 L4 Pivot: +iteration-log.md + 当前 gap-analysis.md             ║
╚═══════════════════════════════════════════════════════════════════════════════╝
         │                        ▲                  ▲
         ▼                        │ Revise           │ L4 Pivot
┌─────────────────────────────────┼──────────────────┼──────────────────────┐
│  Phase 3: Gap Review 🔒         │                  │                     │
│    Pass ──→ P4                  │                  │                     │
│    Revise ──────────────────────┘                  │                     │
│    Block → Exit Assessment Gate                    │                     │
│              ├─ Continue → P1 (重新选题)            │                     │
│              └─ Abandon ─────────────────────────────────────→ P11       │
└──────────────────────────────────────────────────────────────────────────┘
         │ Pass
         ▼
╔═══════════════════════════════════════════════════════════════════════════════╗
║  Phase 4: Method Design                                         [方法设计]  ║
║      gap-analysis.md + Methods Bank → method-design.md + contribution.md↑   ║
║                                                                             ║
║      迭代输入 (如有):                                                        ║
║        ← P5 Revise: +method-review.md                                       ║
║        ← P8 L2 Swap: +iteration-log.md + 当前 method-design.md             ║
║        ← P8 L3 Redesign: +iteration-log.md + 当前 method-design.md         ║
╚═══════════════════════════════════════════════════════════════════════════════╝
         │                        ▲              ▲           ▲
         ▼                        │ Revise       │ L2 Swap   │ L3 Redesign
┌─────────────────────────────────┼──────────────┼───────────┼─────────────┐
│  Phase 5: Method Review 🔒      │              │           │             │
│    Pass ──→ P6                  │              │           │             │
│    Revise ──────────────────────┘              │           │             │
│    Block → Exit Assessment Gate                │           │             │
│              ├─ Continue → P2 (重新定义Gap)     │           │             │
│              └─ Abandon ─────────────────────────────────────────→ P11   │
└──────────────────────────────────────────────────────────────────────────┘
         │ Pass
         ▼
╔═══════════════════════════════════════════════════════════════════════════════╗
║  Phase 6: Experiment Design                                     [实验设计]  ║
║      gap-analysis.md + method-design.md → experiment-design.md (Dim 0-4)    ║
║                                                                             ║
║      迭代输入 (如有):                                                        ║
║        ← P7 Revise: +experiment-review.md                                   ║
╚═══════════════════════════════════════════════════════════════════════════════╝
         │                        ▲
         ▼                        │ Revise
┌─────────────────────────────────┼────────────────────────────────────────┐
│  Phase 7: Experiment Review 🔒  │                                        │
│    Pass ──→ P8                  │                                        │
│    Revise ──────────────────────┘                                        │
│    Block → Exit Assessment Gate                                          │
│              ├─ Continue → P4 (重新设计方法)                               │
│              └─ Abandon ─────────────────────────────────────→ P11       │
└──────────────────────────────────────────────────────────────────────────┘
         │ Pass
         ▼
╔═════════════════════════════════════════════════════════════════════════════╗
║  Phase 8: Implementation & Experimentation              [代码实现+实验运行] ║
║                                                                            ║
║  ┌─ 8a: 核心实现 → Dim 0 快速验证 ──────────────────────────────────────┐  ║
║  │    code-todo (核心) → experiment-todo (Dim 0)                        │  ║
║  │         │                                                            │  ║
║  │         ▼                                                            │  ║
║  │      通过? ── 否 ──┬─ L1 Tune (调参/微调，留在 P8) ──→ 重试 Dim 0   │  ║
║  │         │          │                                                 │  ║
║  │         │          ├─ L2 Swap ──────→ iteration-log.md ──┐           │  ║
║  │         │          ├─ L3 Redesign ──→ iteration-log.md ──┤           │  ║
║  │         │          └─ L4 Pivot ─────→ iteration-log.md ──┤           │  ║
║  │         │                                                │           │  ║
║  │         │                         Exit Assessment Gate ◄─┘           │  ║
║  │         │                          ├─ Continue → 回调目标Phase       │  ║
║  │         │                          │    L2/L3 → P4 | L4 → P2        │  ║
║  │         │                          └─ Abandon → P11                  │  ║
║  │       是 ▼                                ▲     ▲     ▲              │  ║
║  └──────────┼────────────────────────────────┼─────┼─────┼──────────────┘  ║
║             ▼                                │     │     │                 ║
║  ┌─ 8b: 补全实现 → 完整实验 (Dim 1-4) ──────┼─────┼─────┼──────────────┐  ║
║  │    code-todo (补全) → experiment-todo (Dim 1-4)  │     │             │  ║
║  │         │                                 │     │     │             │  ║
║  │         ▼                                 │     │     │             │  ║
║  │    结果不理想? ── 是 ─ L1-4 同上逻辑 ─────┘─────┘─────┘             │  ║
║  │         │                                                           │  ║
║  │       否 ▼                                                          │  ║
║  │    实验结果 + 图表 + contribution.md↑                                │  ║
║  └─────────────────────────────────────────────────────────────────────┘  ║
╚═════════════════════════════════════════════════════════════════════════════╝
         │                          ┌─ L2 Swap ──────────→ P4 (替换组件)
         │                          ├─ L3 Redesign ──────→ P4 (重新设计)
         │    ◄── 回调路径汇总 ──── ├─ L4 Pivot ─────────→ P2 (重新选Gap)
         │                          └─ Abandon ──────────→ P11 (中止退出)
         │
         ▼ (实验全部通过)
╔═══════════════════════════════════════════════════════════════════════════════╗
║  Phase 9: Paper Writing                                         [论文撰写]  ║
║      所有文档 → 论文草稿 (Papers/ 文件夹)                                    ║
╚═══════════════════════════════════════════════════════════════════════════════╝
         │
         ▼
╔═══════════════════════════════════════════════════════════════════════════════╗
║  Phase 10: Submission & Rebuttal                                [投稿迭代]  ║
║      论文终稿 + 审稿意见 → Rebuttal + 修改稿                                ║
╚═══════════════════════════════════════════════════════════════════════════════╝
         │
         ▼ 自然完成
╔═══════════════════════════════════════════════════════════════════════════════╗
║  Phase 11: Project Retrospective                    [知识回收 — 终止态Phase] ║
║                                                                              ║
║      ●─────────────────────────────────────────────────────────● ◄──────────╗║
║      │  入口 A: P10 完成 (自然完成)                            │            ║║
║      │  入口 B: Exit Assessment Gate Abandon (中止退出)        │  ◄─ P3/P5 ║║
║      │                                                        │  ◄─ P7/P8 ║║
║      │  所有项目文档 + iteration-log.md                        │            ║║
║      │    → retrospective.md + 知识库更新                      │            ║║
║      ●─────────────────────────────────────────────────────────●            ║║
║                                                                    Abandon ║║
╚═══════════════════════════════════════════════════════════════════════════════╝
         │ 知识库更新
         ▼
═══════════════════════════════════════════════════════════════════════════════
Phase 0: Paper Reading (知识库持续积累)                      [闭环 — 复利效应]
═══════════════════════════════════════════════════════════════════════════════
```

### 核心机制

**1. 跨阶段贡献跟踪 (contribution.md)**

唯一一个跨阶段维护的文档。在 Phase 2（Gap 贡献）、Phase 4（方法贡献）、Phase 8（实验发现）更新。Review Phase 审查"发表价值"时直接依据此文档。

**2. 四级迭代决策**

Phase 8 实验失败时，按影响范围递增选择迭代级别：

| 级别 | 行动 | 去向 | 影响范围 |
|------|------|------|---------|
| L1 调参 | 调整超参数/训练策略 | 留在 Phase 8 | 仅改配置 |
| L2 换组件 | 替换失败组件 | → P4 → P5 → ... → P8 | 改一个模块 |
| L3 换框架 | 重新设计方法框架 | → P4 → P5 → P6 → P7 → P8 | 重写大部分代码 |
| L4 换方向 | 回到 Gap Discovery | → P2 | 项目方向调整 |

L2-4 退出时产出 `iteration-log.md`（追加模式），作为目标 Phase 的迭代输入，携带失败诊断和约束传递。

**3. Exit Assessment Gate（退出评估关卡）**

嵌入在 L2-4 回调和 Review Block 中。由独立 SubAgent 评估：方案是否穷尽、趋势是否停滞、根因是否可解、Gap 是否仍有效。**判定原则：只要有一条合理可行的路径，就 Continue。** Abandon 需要强论证，进入 Phase 11。

**4. 迭代输入接口**

Phase 的函数签名区分首次和迭代：首次只需 Base Input；Review Revise 回调携带 review 报告；Phase 8 L2-4 回调携带 iteration-log.md + 当前版本文档。

### 文档流转图

```
project-startup.md ──→ gap-analysis.md ──→ method-design.md ──→ experiment-design.md
     (Phase 1)            (Phase 2)          (Phase 4)            (Phase 6)
         │                    │                  │                     │
         │              gap-review.md      method-review.md    experiment-review.md
         │                (Phase 3)          (Phase 5)            (Phase 7)
         │                    │                  │                     │
         │                    │                  │                     ↓
         │                    │                  │          ┌─── Phase 8 ───────┐
         │                    │                  │          │ code-todo.md      │
         │                    │                  │          │ experiment-todo.md│
         │                    │                  │          └──────────────────┘
         │                    │                  │                     │
         └────────────────────┴──────────────────┴─────────────────────┘
                                                 ↓
                              contribution.md (跨阶段维护: Phase 2, 4, 8)
                                                 ↓
                                     Papers/ (Phase 9)
                                 (Abstract, Intro, Related Work,
                                  Method, Experiments, Conclusion)
                                                 ↓
                              retrospective.md (Phase 11 → 知识库闭环)
```

### 项目文件夹结构

```
project/
├── CLAUDE.md                  ← 项目入口：概览、当前阶段、下一步、文档目录
├── pipeline.md                ← 方法论参考（从 ResearchFlow 复制）
├── project-startup.md         ← Phase 1 产出
├── gap-analysis.md            ← Phase 2 产出
├── gap-review.md              ← Phase 3 产出
├── method-design.md           ← Phase 4 产出
├── method-review.md           ← Phase 5 产出
├── experiment-design.md       ← Phase 6 产出
├── experiment-review.md       ← Phase 7 产出
├── contribution.md            ← 跨阶段维护
├── iteration-log.md           ← Phase 8 迭代退出时产出（追加模式）
├── retrospective.md           ← Phase 11 产出（项目回顾与知识回收）
│
├── Code/                      ← 代码实现 & 实验运行 (Phase 8)
│   ├── code-todo.md           ← 代码实现清单
│   ├── experiment-todo.md     ← 实验执行清单
│   ├── configs/               ← 配置驱动实验
│   ├── src/                   ← 源代码
│   ├── scripts/               ← 运行脚本
│   └── experiments/           ← 实验结果存储
│
└── Papers/                    ← 论文撰写 (Phase 9)
    ├── main.tex               ← 论文主文件
    ├── figures/               ← 图表
    └── ...
```

**CLAUDE.md 结构**：项目级 CLAUDE.md 包含三个区域——项目概览（所有 Phase 读）+ Code/ 子节（Phase 8 填写）+ Papers/ 子节（Phase 9 填写），统一在一个文件中管理。参见 `templates/project-claude-md.md`。

### 关键文档清单

| 文档 | 创建阶段 | 主要使用阶段 | 内容 |
|------|---------|------------|------|
| 知识库 (论文笔记) | Phase 0 | Phase 1, 2, 4, 6, 9 | 持续积累的可复用研究资产 |
| `project-startup.md` | Phase 1 | Phase 2, 4, 9 | 项目知识基础 |
| `gap-analysis.md` | Phase 2 | Phase 3-9 | Gap 陈述 + 根因 + RQ |
| `gap-review.md` | Phase 3 | Phase 2 (如需修改) | Gap 审查报告 |
| `method-design.md` | Phase 4 | Phase 5-9 | 方法框架 + 组件 + 理论 |
| `method-review.md` | Phase 5 | Phase 4 (如需修改) | 方法审查报告 |
| `experiment-design.md` | Phase 6 | Phase 7-9 | 实验 spec (Dim 0-4) + 实验结果 |
| `experiment-review.md` | Phase 7 | Phase 6 (如需修改) | 实验设计审查报告 |
| `contribution.md` | Phase 2 | Phase 3, 5, 7, 8, 9 | 贡献列表 (跨阶段更新) |
| `CLAUDE.md` | 项目初始化 | 所有 Phase | 项目入口：概览 + 当前阶段 + Code/ 子节 + Papers/ 子节 |
| `pipeline.md` | 项目初始化 | 所有 Phase | 方法论参考（本文档的副本） |
| `Code/code-todo.md` | Phase 8 | Phase 8 | 代码实现清单 |
| `Code/experiment-todo.md` | Phase 8 | Phase 8 | 实验执行清单 |
| `iteration-log.md` | Phase 8 (L2-4退出时) | Phase 2/4 (迭代时), Exit Gate | 失败诊断 + 约束传递 + 迭代历史 |
| `retrospective.md` | Phase 11 | Phase 0 (知识库更新) | 项目回顾 + 知识回收 |

---

## 二、各阶段详细方法

### Phase 0: Paper Reading & Knowledge Accumulation (论文阅读与知识积累)

> **Input**: 论文 PDF / arXiv / 论文内容
> **Output**: 单篇论文笔记 + 知识库更新（Methods Bank, Gaps & Assumptions, Experimental Patterns, Cross-Paper Connections）

**本质**: 持续性的"市场调研"。不绑定任何特定项目，是研究者日常知识积累的过程。

**与 Phase 1 的关系**:
```
Phase 0 (持续性) ——积累触发——> Phase 1 (触发性)
论文阅读是土壤，研究洞察是从土壤中长出的种子。
```

**论文阅读的两层产出**:

| 层次 | 内容 | 价值 |
|------|------|------|
| 论文级 | 单篇论文的完整理解 (storyline, method, experiments) | 当下理解 |
| 知识库级 | 可复用资产提取 | 长期复利 |

**四类可复用资产**:
1. **Methods Bank** — 核心方法/技术，含适用条件和局限
2. **Gaps & Assumptions** — 未解决的问题 + 可被质疑的隐式假设 (最高价值)
3. **Experimental Patterns** — baselines, metrics, 消融设计模式
4. **Cross-Paper Connections** — 论文间的关联 (互补/矛盾/延伸/可结合)

**AI 的独特价值**:
- 不仅是记录员，更是**共同思考者**
- 主动识别隐式假设（作者自己没意识到的局限）
- 随着知识库增长，主动发现 cross-paper connections，提示潜在研究方向
- 知识库的价值随积累量**指数增长**

**关键原则**:
- 隐式假设 > 显式 future work（后者所有人都能看到，前者是差异化来源）
- 结构化存储 > 自由笔记（结构化才能被 AI 跨论文检索和关联）
- 每篇论文阅读后都应更新知识库索引，而非孤立存放

**Exit Criteria**:
- [ ] 论文级理解完整（能说清 storyline、核心方法、实验设计）
- [ ] 至少提取了 1 个 Methods Bank 条目
- [ ] 至少识别了 1 个 Gap/隐式假设
- [ ] 知识库索引已更新

**对应 Skill**: `/paper-reading` (`skills/paper-reading-skill.md`)
**对应模板**: `templates/paper-reading-note.md`

---

### Phase 1: Project Startup (项目启动与知识建基)

> **Input**: 研究者的初步洞察 + 相关论文/材料 + 知识库
> **Output**: `project-startup.md`

**本质**: 将研究者脑中的隐性洞察显性化，建立人与 AI 之间的共享知识基础。

**核心模型**:
```
研究种子(Seed) = 源材料(Sources) + 研究者洞察(Insight)
```

**五种 Seed 类型**:
| 类型 | 描述 | 典型场景 |
|------|------|----------|
| 方法融合型 | 多个方法/论文的结合 | "A的机制和B的机制可以互补" |
| 方法延伸型 | 改进/拓展已有方法 | "这个方法的XX假设可以放松" |
| 领域迁移型 | 方法迁移到新领域 | "这个NLP技术可以用在CV上" |
| 问题驱动型 | 从未解决的问题出发 | "现有方法都无法处理XX场景" |
| 现象启发型 | 从实验观察/直觉出发 | "我发现XX现象，背后一定有规律" |

**流程**: 识别种子类型 -> 深度理解源材料 -> 知识综合与Gap分析 -> 生成Startup文档 -> 与研究者确认

**产出**: `project-startup.md` — 项目全周期的知识基础文档

**关键原则**:
- 源材料总结要有技术深度，保留公式和精确定义，而非浅层概述
- Gap分析要具体尖锐，指出确切的技术缺口
- 研究方向要与Gap直接对应，形成 Sources -> Gap -> Direction 的逻辑闭环
- AI 作为 Co-Author 参与知识建基：不仅帮助显性化和结构化，还应主动评估可行性、指出潜在风险、提出替代方向

**Exit Criteria**:
- [ ] Seed 类型已明确，洞察已显性化
- [ ] 源材料总结有技术深度（保留公式和精确定义）
- [ ] Gap 分析具体尖锐，指向明确的技术缺口
- [ ] Sources → Gap → Direction 逻辑闭环成立
- [ ] 研究者确认 project-startup.md 内容

**对应 Skill**: `/project-startup` (`skills/project-startup-skill.md`)
**对应模板**: `templates/project-startup.md`

---

### Phase 2: Gap Discovery (研究空白发现)

> **Input (首次)**: `project-startup.md` + 知识库 (Gaps & Assumptions, Cross-Paper Connections)
> **Input (迭代 — Phase 3 Revise)**: + `gap-review.md`（审查意见，需针对性修改）
> **Input (迭代 — Phase 8 L4 Pivot)**: + `iteration-log.md` + 当前 `gap-analysis.md`（上一轮 Gap 方向走不通，需换方向）
> **Output**: `gap-analysis.md` + `contribution.md` (初始化)

**本质**: 从知识库中**组合推导**出有价值的研究空白。这不是灵感闪现，而是系统性搜索。

**为什么独立成阶段？**
Gap 是稳定的锚点，Method 可以迭代。两者必须解耦——好的 gap 不应因为第一个 method 失败而被放弃。

**Gap 的组合推导模型**:
```
知识库中的多篇论文
    ├── Future Work A + Future Work B → 组合推导 → Gap 候选 1
    ├── Assumption X (论文P) + 反例 Y (论文Q) → 质疑推导 → Gap 候选 2
    ├── 方法 M 的局限 + 领域 C 的需求 → 迁移推导 → Gap 候选 3
    └── ...
```
Gap 不是"看到一篇论文就有了"，而是知识库中多个条目的**交叉点**。
知识库越丰富，可发现的 gap 越多——这就是 Phase 0 持续积累的回报。

**流程**:
1. **Gap 候选生成** — 从知识库的 Gaps & Assumptions、Future Work、Cross-Paper Connections 中组合推导
2. **Gap 评估矩阵** — 按三个维度评估每个候选：
   - 重要性：解决它对领域有多大影响？
   - 新颖性：是否已被他人解决或正在被解决？
   - 可解决性：以现有技术条件，是否有希望攻克？
3. **Gap 根因分析** — 对选定的 gap 追问"为什么存在？"
   - 是技术限制？（需要新方法）
   - 是错误假设？（需要重新建模）
   - 是被忽视的维度？（需要新视角）
   - 根因直接决定 Phase 4 的方法方向
4. **RQ 公式化** — 将 gap 转化为可回答的研究问题
5. **初始化 contribution.md** — 明确当前阶段可见的潜在贡献

**迭代执行时的行为差异**:

| 迭代来源 | 行为 |
|---------|------|
| Phase 3 Revise | 读 `gap-review.md`，针对审查意见逐条修改 `gap-analysis.md`，不需要从零开始 |
| Phase 8 L4 Pivot | 读 `iteration-log.md`，理解上一轮 Gap 方向为什么走不通；读当前 `gap-analysis.md` 作为参考；在避免已排除方向的前提下，重新从知识库组合推导新 Gap |

**AI Co-Author 在此阶段的关键行为**:
- **主动从知识库中做组合搜索**——人类难以同时关联 10+ 篇论文，AI 可以
- 对每个 gap 进行批判性评估：是否真的是 gap？是否已被解决？
- 帮助做根因分析
- **迭代时**：严格遵守 iteration-log.md 中的"已排除方案"约束，不重蹈覆辙

**`gap-analysis.md` 包含**:
- Gap 陈述（一句话版本 + 详细版本）
- 根因分析
- Research Questions
- Gap 评估矩阵结果

**Exit Criteria**:
- [ ] 能用一句话说清"现有方法做了X，但因为Y所以存在Z问题"——说不清就是没收敛到位
- [ ] Gap 有明确的根因分析（技术限制 / 错误假设 / 被忽视维度）
- [ ] RQ 是具体的、可回答的、可验证的
- [ ] Gap 候选经过评估矩阵筛选，不是拍脑袋选的
- [ ] contribution.md 已初始化

**对应 Skill**: `/gap-discovery` (`skills/gap-discovery-skill.md`)
**对应模板**: `templates/gap-analysis.md`

---

### Phase 3: Gap Review (研究空白审查) [Review Phase]

> **Input**: `gap-analysis.md` + `contribution.md`
> **Output**: `gap-review.md` + **判定 (Pass / Revise / Block)**

**本质**: 独立 SubAgent 对 Gap 的质量和发表价值进行严格审查。

**为什么独立成 Phase？**
参与 Gap 推导的 AI 存在确认偏误——自己推导的结论倾向于自己认可。
独立 SubAgent 只看文档，没有过程记忆，能以"冷眼"审视。

**审查维度**:

| 审查维度 | 核心问题 | 判定标准 |
|---------|---------|---------|
| **真实性** | 这真的是一个未解决的 gap，还是 pseudo-gap？ | 需要引用具体证据说明无人解决 |
| **重要性** | 解决这个 gap 对领域有多大影响？ | 影响范围是否足够支撑一篇论文 |
| **新颖性** | 是否有其他团队正在做类似工作？ | 需检查最新 arXiv/会议 |
| **根因深度** | 根因分析是否到位？是否还能再追问一层？ | 根因应直接指向方法设计方向 |
| **RQ 可回答性** | RQ 是否可以被实验验证？ | 需有明确的验证路径 |
| **贡献价值** | 当前可见的贡献是否足够支撑发表？ | 审查 contribution.md 的初始条目 |

**审查报告格式**:
```
## Gap Review Report
- 各维度判定: Pass / Revise / Block
- 逐条问题清单
- 贡献价值评估
- 整体判定: Pass / Revise / Block
```

**判定后的流向**:
- **Pass** → 进入 Phase 4
- **Revise** → 返回 Phase 2 修改后重新提交审查
- **Block** → 触发 Exit Assessment Gate → Continue 则返回 Phase 1（Gap 方向需重大调整）| Abandon 则进入 Phase 11

**对应 Skill**: `/review gap` (`skills/review-skill.md` + `review-configs/gap-review.yaml`)
**对应 SubAgent**: `subagents/review-subagent.md` + `subagents/exit-assessment-subagent.md`

---

### Phase 4: Method Design (方法设计)

> **Input (首次)**: `gap-analysis.md` + `project-startup.md` + 知识库 (Methods Bank)
> **Input (迭代 — Phase 5 Revise)**: + `method-review.md`（审查意见，需针对性修改）
> **Input (迭代 — Phase 8 L2 Swap)**: + `iteration-log.md` + 当前 `method-design.md`（定位到失败组件，需替换）
> **Input (迭代 — Phase 8 L3 Redesign)**: + `iteration-log.md` + 当前 `method-design.md`（方法框架需重新设计）
> **Output**: `method-design.md` + `contribution.md` (更新)

**本质**: 从知识库的 Methods Bank 中**组合推导**出能解决 Gap 的方法，并论证因果关系。

**方法的组合推导模型**:
```
Gap 根因 (来自 gap-analysis.md)
    ↓ 查询知识库 Methods Bank
方法 A 的核心机制 + 方法 B 的某个组件 + 新的理论连接
    ↓ 组合与适配
新方法框架
    ↓ 论证
为什么这个方法能解决这个 Gap
```

**流程**:
1. **方案空间探索** — 基于 Gap 根因，从知识库中检索相关方法/技术
2. **方法框架搭建** — 组合现有方法组件，设计核心机制
3. **因果论证** — Gap根因 → 方法设计 → 为什么能解决（逻辑闭环）
4. **理论分析** — 形式化论证（如适用）
5. **方法定位** — 在技术谱系中的位置（继承了什么、改变了什么）
6. **组件级审查** (见下方)
7. **更新 contribution.md** — 明确方法层面的技术贡献

**组件级审查 (Component-Level Review)**:

这是 AI Co-Author 的独特优势所在。方法框架搭建完成后，执行以下审查：

```
对方法中的每个组件 C:
    1. 明确 C 的输入、输出、功能
    2. 判断 C 是否可从框架中解耦（接口是否清晰）
    3. 如果可解耦:
       a. C 的功能本质是什么？（抽象化）
       b. 本领域是否有更好的替代方案？
       c. 跨领域是否有更好的替代方案？（AI 的知识广度优势）
       d. 替代方案是否与框架的其他组件兼容？
    4. 如果发现更优替代 → 提议替换，论证优势
```

**为什么这一步至关重要？**
- 人类研究者受知识边界限制，通常只能用自己知道的方法
- AI 拥有跨领域知识，能发现"NLP 领域的 X 技术其实完美适配你 CV 方法中的 Y 组件"
- 这种跨域组件替换往往是论文的亮点和 novelty 来源

**`method-design.md` 包含**:
- 方法框架总览（组件拆解、各组件 I/O）
- 核心机制详述（含数学公式）
- 因果论证：Gap → 根因 → 方法 → 为什么解决
- 理论分析（如适用）
- 方法定位（技术谱系中的位置）
- 组件审查记录

**迭代执行时的行为差异**:

| 迭代来源 | 行为 |
|---------|------|
| Phase 5 Revise | 读 `method-review.md`，针对审查意见逐条修改 `method-design.md`，保留通过审查的部分 |
| Phase 8 L2 Swap | 读 `iteration-log.md`，定位失败组件；读当前 `method-design.md`，**仅替换失败组件**，保留其余设计不变；从知识库搜索替代组件 |
| Phase 8 L3 Redesign | 读 `iteration-log.md`，理解整体失败原因；读当前 `method-design.md` 作为参考；在已排除方案的约束下重新设计方法框架 |

**AI Co-Author 在此阶段的关键行为**:
- 不被人类的知识边界限制，主动搜索跨领域的替代组件
- 对每个组件的接口进行形式化分析（输入/输出类型、维度、语义）
- 帮助构建理论论证
- **迭代时**：先读 iteration-log.md 确认失败原因和约束，再决定改动范围；L2 只改组件，L3 重设计但不重复已排除方案

**Exit Criteria**:
- [ ] 核心叙事脊柱完整：Gap → 根因 → 方法设计 → 为什么能解决 → 怎么验证
- [ ] 方法中每个组件都能回溯到 gap 根因——没有"因为好所以加"的组件
- [ ] 组件级审查已完成，每个可解耦组件都经过替代方案评估
- [ ] 方法定位清晰——继承了什么、改变了什么、与最相近方法的差异
- [ ] 理论分析/论证已完成（如适用）
- [ ] contribution.md 已更新（方法层面的技术贡献）

**对应 Skill**: `/method-design` (`skills/method-design-skill.md`)
**对应模板**: `templates/method-design.md`

---

### Phase 5: Method Review (方法审查) [Review Phase]

> **Input**: `gap-analysis.md` + `method-design.md` + `contribution.md`
> **Output**: `method-review.md` + **判定 (Pass / Revise / Block)**

**本质**: 独立 SubAgent 对方法的逻辑完整性、理论正确性和贡献价值进行严格审查。

**审查维度**:

| 审查维度 | 核心问题 | 判定标准 |
|---------|---------|---------|
| **逻辑闭环** | Gap→根因→方法→为什么解决，链条是否完整？ | 每一环都能严格推导，无逻辑跳跃 |
| **组件必要性** | 每个组件是否不可或缺？去掉任何一个会怎样？ | 每个组件都有明确的必要性论证 |
| **理论正确性** | 数学推导是否正确？假设是否合理？ | 公式推导无误，假设被明确声明 |
| **差异化** | 与最相近现有方法的本质区别是什么？ | 差异必须是实质性的，非 trivial 变体 |
| **可实现性** | 方法是否可以被实现和验证？ | 无需不现实的计算资源或数据 |
| **贡献充分性** | contribution.md 中的贡献是否足够支撑发表？ | novelty + significance 达标 |

**审查报告格式**:
```
## Method Review Report
- 各维度判定: Pass / Revise / Block
- 逐条问题清单（特别关注逻辑跳跃和隐含假设）
- 贡献价值评估：当前贡献是否达到发表门槛？
- 整体判定: Pass / Revise / Block
```

**判定后的流向**:
- **Pass** → 进入 Phase 6
- **Revise** → 返回 Phase 4 修改后重新提交审查
- **Block** → 触发 Exit Assessment Gate → Continue 则返回 Phase 2（方法路线需重新审视）| Abandon 则进入 Phase 11

**对应 Skill**: `/review method` (`skills/review-skill.md` + `review-configs/method-review.yaml`)
**对应 SubAgent**: `subagents/review-subagent.md` + `subagents/exit-assessment-subagent.md`

---

### Phase 6: Experiment Design (实验设计)

> **Input (首次)**: `gap-analysis.md` + `method-design.md` + 知识库 (Experimental Patterns)
> **Input (迭代 — Phase 7 Revise)**: + `experiment-review.md`（审查意见，需针对性修改）
> **Output**: `experiment-design.md` (high-level 实验 spec)

**本质**: 独立于方法设计的验证方案。这是一份 high-level 的"实验 spec"。

**为什么要独立成文档和阶段？**
- 实验设计文档在编码阶段会被高频调用，作为实现的直接 spec
- 实验设计需要独立思考——好的实验不只是"跑一下看结果"，而是精心设计的验证体系
- 将实验从方法设计中解耦，使两者都能独立迭代

**实验设计的五个维度**:
```
Dimension 0: 快速验证 (Sanity Check Spec)
    ├── 验证什么核心假设？（最核心的 1-2 个）
    ├── 最小实验规模？（小数据集/子集、少 epoch）
    ├── 通过标准？（什么信号算"正向"？具体数值或趋势）
    └── 预计时间？（应控制在数小时内）

Dimension 1: 核心验证 (证明方法 work)
    ├── 主实验: 与 baselines 的定量对比
    ├── 消融实验: 每个组件的必要性
    └── 反事实验证: ground-truth 级别的验证（如可行）

Dimension 2: 应用价值 (证明方法 useful)
    └── 下游任务实验

Dimension 3: 效率验证 (证明方法 practical)
    └── 计算成本分析

Dimension 4: 科学发现 (bonus, 非常加分)
    └── 利用所提方法作为工具，探索研究社区关心的科学问题
    └── 产出有价值的 insight，而非仅仅验证方法本身
```

**Dimension 0 的特殊说明**:
Dimension 0 是为 Phase 8 Sub-phase 8a (快速验证) 提供的**明确 spec**。它定义了：
- 用什么实验来快速验证方法的核心假设
- "通过"的具体标准是什么（不是模糊的"看起来 work"）
- 预期的时间成本（如果快速验证需要一周，那就不是快速验证）

**Dimension 4 的特殊说明**:
科学发现实验不是必须的，但是对论文**非常加分**。它的逻辑是：
方法本身已被验证 → 将方法作为一个可信的工具 → 用它去回答一些此前无法回答的问题 → 产生新的科学洞察。
这体现了方法的价值不止于"比 baseline 好"，而是能**推动对领域的理解**。

**流程**:
1. **快速验证设计 (Dim 0)** — 最小成本验证核心假设的实验方案
2. **验证体系设计 (Dim 1)** — 每个 RQ 对应至少一个核心实验
3. **Baseline 选择** — 选择什么对比方法？为什么选这些？
4. **Metrics 定义** — 用什么指标？指标与 RQ 的对应关系
5. **消融实验设计** — 与方法的模块化结构一一对应
6. **科学发现实验设计 (Dim 4)** — 利用方法探索什么科学问题？
7. **数据集与模型规模规划** — 多尺度验证策略
8. **计算资源估算** — 可行性评估
9. **预期结果与失败预案** — 如果结果不如预期，说明什么？

**迭代执行时的行为差异**:

| 迭代来源 | 行为 |
|---------|------|
| Phase 7 Revise | 读 `experiment-review.md`，针对审查意见修改实验设计（补充遗漏实验、调整 baseline、修正 metrics 等） |

**AI Co-Author 在此阶段的关键行为**:
- 从知识库的 Experimental Patterns 中复用已验证的实验设计模式
- 检查实验设计与 RQ 的覆盖率——是否有 RQ 没有被实验覆盖？
- 预判潜在的审稿人质疑，提前设计对应实验
- 主动提议 Dimension 4 的科学发现实验——"如果你的方法 work 了，可以用它来回答什么有趣的问题？"
- **设计明确的 Dimension 0 快速验证方案**——定义通过标准和时间预算

**Exit Criteria**:
- [ ] Dimension 0 (快速验证) 有明确的实验方案、通过标准和时间预算
- [ ] 每个 RQ 都有至少一个核心实验覆盖
- [ ] Baseline 选择有明确理由，覆盖当前 SOTA
- [ ] 消融实验与方法组件一一对应
- [ ] Metrics 与 RQ 有明确对应关系
- [ ] 计算资源估算在可行范围内
- [ ] 每个实验都定义了预期结果和失败预案

**对应 Skill**: `/experiment-design` (`skills/experiment-design-skill.md`)
**对应模板**: `templates/experiment-design.md`

---

### Phase 7: Experiment Review (实验设计审查) [Review Phase]

> **Input**: `gap-analysis.md` + `method-design.md` + `experiment-design.md` + `contribution.md`
> **Output**: `experiment-review.md` + **判定 (Pass / Revise / Block)**

**本质**: 独立 SubAgent 对实验设计的完备性和公平性进行严格审查。

**审查维度**:

| 审查维度 | 核心问题 | 判定标准 |
|---------|---------|---------|
| **RQ 覆盖率** | 是否每个 claim 都有实验支撑？ | 无遗漏的 claim-experiment 映射 |
| **Baseline 公平性** | 对比方法是否是当前最强？设置是否公平？ | 不能只挑弱 baseline 比 |
| **消融充分性** | 是否能区分各组件的贡献？ | 每个组件的必要性都可被验证 |
| **Metrics 合理性** | 指标是否真的衡量了想衡量的东西？ | 指标与 RQ 的语义对应关系 |
| **快速验证合理性** | Dimension 0 的通过标准是否合理？ | 标准不能太松也不能太严 |
| **可复现性** | 实验描述是否足够详细以复现？ | 数据集、超参数、随机种子等 |
| **审稿人预判** | 审稿人最可能要求的额外实验？ | 提前识别可能的 weakness |

**审查报告格式**:
```
## Experiment Review Report
- 各维度判定: Pass / Revise / Block
- 逐条问题清单
- 审稿人可能的额外实验要求（预判）
- 整体判定: Pass / Revise / Block
```

**判定后的流向**:
- **Pass** → 进入 Phase 8
- **Revise** → 返回 Phase 6 修改后重新提交审查
- **Block** → 触发 Exit Assessment Gate → Continue 则返回 Phase 4（根本问题可能源于方法设计）| Abandon 则进入 Phase 11

**对应 Skill**: `/review experiment` (`skills/review-skill.md` + `review-configs/experiment-review.yaml`)
**对应 SubAgent**: `subagents/review-subagent.md` + `subagents/exit-assessment-subagent.md`

---

### Phase 8: Implementation & Experimentation (代码实现与实验运行)

> **Input**: `method-design.md` + `experiment-design.md`
> **Output**: 代码 + `code-todo.md` + `experiment-todo.md` + CLAUDE.md Code/ 子节 + 实验结果 + `contribution.md` (更新)
> **Output (迭代退出时)**: + `iteration-log.md`（L2/L3/L4 退出时产出，作为目标 Phase 的迭代输入）

**本质**: 将方法设计变成可运行的代码，快速验证核心假设，通过后推进完整实验。
核心原则：**快速部署、快速验证、通过后再补全**——不要在没验证核心假设的情况下就把所有代码写完。

**为什么合并为一个 Phase？**
代码实现和实验运行共享**代码库**这一工作状态。将它们拆成独立 Phase 会导致每个 SubAgent 都需要重新理解整个代码库——这是效率灾难。合并后，这个 Phase 内部通过子流程和两份 todo 清单管理复杂性。

---

#### 两份 Todo 清单：code-todo.md + experiment-todo.md

| 清单 | 职责 | 内容 |
|------|------|------|
| `code-todo.md` | 写什么代码 | 环境搭建、组件实现、pipeline 组装、评估实现 |
| `experiment-todo.md` | 跑什么实验 | 每个实验的具体步骤、命令、参数、结果记录 |

两份清单**交替执行**，各司其职：

```
code-todo (核心实现)
    → experiment-todo (Dim 0 快速验证)
        → 决策分支
            ├── 不通过 → 退出 Phase 8，回到 Phase 4/2
            └── 通过 → code-todo (补全实现)
                          → experiment-todo (Dim 1-4 完整实验)
```

---

#### Sub-phase 8a: 核心实现 + 快速验证

**目标**: 用最小代码量跑通 Dimension 0 的快速验证。

**第一步：选择代码起点**

不要从零开始写。寻找顺序：
1. **Baseline 方法的官方代码** — 最优先。保证评估公平，且评估 pipeline 已就绪
2. **同领域成熟框架** — 如 diffusers, timm, transformers 等
3. **相关方法的开源实现** — 代码质量和社区活跃度是选择标准

选择标准：评估 pipeline 是否完整、代码是否模块化可扩展、文档和社区支持。

**第二步：复现 Baseline（必须）**

在写任何新代码之前，先用选定的代码库复现 baseline 的论文结果。
这一步验证了：环境正确、数据处理正确、评估代码正确、训练流程正确。
如果连 baseline 都复现不了，后续所有实验结果都不可信。

**第三步：填写 CLAUDE.md 的 Code/ 子节**

CLAUDE.md 的 Code/ 子节是 AI Co-Author 在代码域的入职手册，包含代码架构、组件映射、环境配置、运行命令等。

**第四步：核心实现（仅 Dim 0 所需）**

`code-todo.md` 第一轮只包含跑通 Dim 0 所需的最少代码：
- 核心方法各组件实现
- 端到端 pipeline 组装
- 一个核心 baseline 的对比实现
- 基本评估（Dim 0 指定的 metrics）

**不写**：消融变体、完整评估 pipeline、额外 baseline——这些等验证通过后再补。

**代码结构设计原则**：**代码模块 = 方法组件。** 这样消融实验就是改配置文件，而非改代码。

```
Code/
├── code-todo.md                 ← 代码实现清单
├── experiment-todo.md           ← 实验执行清单
├── configs/                     ← 配置驱动实验
│   ├── method_full.yaml         ← 完整方法
│   ├── ablation_no_X.yaml       ← 消融变体 (Sub-phase 8b)
│   └── baseline_Y.yaml          ← baseline 配置
├── src/
│   ├── methods/
│   │   ├── component_a.py       ← 对应 method-design.md 中的组件 A
│   │   ├── component_b.py       ← 对应 method-design.md 中的组件 B
│   │   └── pipeline.py          ← 组装各组件
│   ├── evaluation/              ← 评估 pipeline（尽量复用 baseline 的）
│   ├── data/                    ← 数据处理
│   └── utils/                   ← 工具函数
├── scripts/                     ← 运行脚本
└── experiments/                 ← 实验结果存储
```

**第五步：快速验证（Dimension 0）**

按 `experiment-design.md` Dimension 0 的 spec 执行快速验证：
- 在小规模数据上，对比核心 baseline 算法
- 通过标准参照 Dim 0 中的量化定义——不是"看起来还行"
- 应在数小时内完成

**快速验证失败后的诊断决策树**:

```
Q1: 结果完全没有正向信号？
    ├── 否（有正向信号但不够好）→ Level 1: 调参（留在 Phase 8）
    └── 是（完全不 work）→ 继续 Q2

Q2: 能否定位到具体的失败组件？
    ├── 是（某个组件输出明显异常）→ Level 2: 换组件（退出 Phase 8 → Phase 4）
    └── 否（整体都不对）→ 继续 Q3

Q3: 方法的核心假设是否成立？（回到 Gap 根因检验）
    ├── 是（假设成立，但方法路线不对）→ Level 3: 换框架（退出 → Phase 4）
    └── 否（假设本身有问题）→ Level 4: 换方向（退出 → Phase 2）
```

**四级迭代决策**:

| 级别 | 行动 | 去向 | 影响范围 |
|------|------|------|---------|
| **Level 1: 调参 (Tune)** | 调整超参数、训练策略 | 留在 Phase 8 | 仅改配置 |
| **Level 2: 换组件 (Swap)** | 替换为更好的组件 | → Phase 4 → 5 → ... → 8 | 改一个模块 |
| **Level 3: 换框架 (Redesign)** | 重新设计方法框架 | → Phase 4 → 5 → 6 → 7 → 8 | 重写大部分代码 |
| **Level 4: 换方向 (Pivot)** | 回到 Gap Discovery | → Phase 2 | 项目方向调整 |

**关键原则**: 优先低级别迭代。Level 1 留在 Phase 8 内部循环，Level 2-4 退出 Phase 8。

**退出 Phase 8 时必须产出 `iteration-log.md`**:

当决策为 L2/L3/L4 时，在退出前必须写入结构化的迭代日志，作为目标 Phase 的迭代输入。日志包含：
- **失败诊断**：实验观察到什么、哪个组件/假设出了问题、根因是什么
- **约束传递**：哪些部分已验证可行（不需要改）、哪些方案已排除（不要再试）、建议的改进方向
- **证据**：支撑诊断的具体实验数据

`iteration-log.md` 采用追加模式——每次迭代追加一个 Entry，保留完整的迭代历史。

**Exit Assessment Gate（退出评估关卡）**:

在 L2/L3/L4 回调执行前，由**独立 SubAgent** 对项目进行退出评估。这个关卡回答一个元问题：**继续迭代是否还有合理预期？**

```
Phase 8 L2-4 决策 → 写 iteration-log.md → 【Exit Assessment Gate】
    ├── Continue → 执行回调（→ Phase 4 或 Phase 2）
    └── Abandon  → 进入 Phase 11 (Project Retrospective)
```

Exit Assessment SubAgent 的输入：
- `iteration-log.md`（完整迭代历史）
- `gap-analysis.md` + `method-design.md`（当前项目状态）
- `contribution.md`（已有贡献）
- 知识库（评估剩余方案空间）

评估维度：

| 维度 | 核心问题 |
|------|---------|
| **方案穷尽度** | 知识库中是否还有未尝试的、本质不同的方案？ |
| **趋势判断** | 历次迭代的实验信号是在改善、停滞、还是恶化？ |
| **根因可解性** | iteration-log 中的失败根因是技术上可解决的，还是根本性障碍？ |
| **Gap 有效性** | Gap 本身是否仍然成立？是否有新工作已解决？ |
| **预判分析** | 剩余的候选方向，是否可以合理预期会成功？ |

**判定原则：只要有一条合理可行的路径，就判定 Continue。** Abandon 需要强论证：所有方向已穷尽，或存在不可逾越的根本障碍。

此关卡同样适用于 Review Phase (3/5/7) 的 **Block** 判定——Block 意味着方向根本错误，回退前也应通过 Exit Assessment Gate 评估是否值得继续。

---

#### Sub-phase 8b: 补全实现 + 完整实验

**快速验证通过后**，进入第二轮：

`code-todo.md` 第二轮：
- 实现所有消融变体（配置驱动，无需改核心代码）
- 完善评估 pipeline（所有 Dimension 1-4 需要的 metrics）
- 实现额外 baselines
- 实现 Dimension 4 科学发现实验所需的代码

`experiment-todo.md` 第二轮：
- 按 Dimension 1-4 逐项执行完整实验
- 每个实验记录：具体步骤、命令、参数

**铁律：实验执行的两条硬性规则**:

1. **每次实验运行后，立即更新 `experiment-todo.md`** — 标记完成状态，记录实际结果
2. **每次实验结果产出后，立即记录到 `experiment-design.md` 的对应实验章节** — 包括数值结果、关键观察、与预期的对比

不要"先跑完所有实验再统一记录"——实验记录是**实时的**，不是事后的。

**完整实验结束后**：更新 `contribution.md`——特别是 Dimension 4 的科学发现。

---

#### Phase 8 整体

**AI Co-Author 在此阶段的关键行为**:
- 阅读 baseline 代码，理解架构后再动手修改（不要盲改）
- 实现时持续对照 `method-design.md` 中的数学公式，确保代码与理论一致
- 每个组件实现后进行单元验证（维度检查、边界条件、数值稳定性）
- 代码中的关键实现决策记录在 CLAUDE.md 的 Code/ 子节中
- 管理 code-todo.md 和 experiment-todo.md 的交替执行
- 遇到异常实验结果时主动分析原因，而非机械执行
- 实验结果出来后，主动进行初步分析和可视化

**关键原则**:
- **快速部署快速验证**：先实现最少代码跑通 Dim 0，验证核心假设后再补全
- **配置驱动实验**：所有可变参数通过配置文件控制
- **评估代码复用**：尽量使用 baseline 已有的评估代码
- **可复现性**：种子管理、完整的依赖记录、实验配置版本化
- **代码 = 方法**：代码模块边界 = 方法组件边界
- **实时记录铁律**：每次实验后立即更新 todo 和 experiment-design.md

**Exit Criteria**:
- [ ] Baseline 已复现
- [ ] 快速验证 (Dim 0) 通过
- [ ] 所有 experiment-todo.md 中的实验项已完成
- [ ] 所有实验结果已实时记录到 experiment-design.md 对应章节
- [ ] 核心表格和图表已生成
- [ ] 结果支撑 contribution.md 中的 claims
- [ ] contribution.md 已更新（含实验发现的新贡献）

**对应 Skill**: `/impl-setup` + `/impl-validate` + `/impl-full` (`skills/impl-*-skill.md`)
**对应 SubAgent**: `subagents/iteration-diagnosis-subagent.md` + `subagents/exit-assessment-subagent.md`
**对应模板**: `templates/project-claude-md.md`, `templates/experiment-todo.md`

---

### Phase 9: Paper Writing (论文撰写)

> **Input**: `gap-analysis.md` + `method-design.md` + `experiment-design.md`(含实验结果) + `project-startup.md` + `contribution.md` + 论文模板
> **Output**: 论文草稿

**本质**: 将之前所有阶段的产出，组装为一篇完整的学术论文。
到了这一步，论文的素材几乎已经全部就绪——撰写的核心工作是**叙事构建**和**逻辑组织**。

**论文各章节的文档来源映射**:

| 论文章节 | 主要来源文档 | 撰写要点 |
|---------|------------|---------|
| **Abstract** | `contribution.md` (浓缩) + 实验核心结果 | 问题-方法-结果-贡献，4-5句话 |
| **Introduction** | `gap-analysis.md` (Gap, Motivation) + `project-startup.md` (背景) + `contribution.md` (贡献列表) | 构建叙事：领域背景→现有工作→Gap→我们的贡献 |
| **Related Work** | `project-startup.md` + 知识库 + 补充文献调研 | 不是罗列，而是构建"技术谱系"，定位本工作的位置 |
| **Method** | `method-design.md` (方法细节) | 核心叙事脊柱：Gap→根因→方法→为什么能解决 |
| **Experiments** | `experiment-design.md` (设计+结果) | 每个实验都要说清：目的→设置→结果→分析 |
| **Conclusion** | `contribution.md` (贡献) + 实验 insights | 总结贡献 + limitations + future work |

**撰写顺序建议**:

不要按章节顺序写。推荐顺序：
1. **Method** — 最核心，最确定，先写（直接从 method-design.md 转化）
2. **Experiments** — 有数据有图表，结构清晰（从 experiment-design.md 转化）
3. **Introduction** — 需要全局视角，在 method 和 experiments 确定后写更顺畅
4. **Related Work** — 需要额外的文献调研来完善
5. **Abstract & Conclusion** — 最后写，此时全文已定型

**Related Work 的特殊处理**:

Related Work 不是简单的文献罗列。它需要：
1. 从 `project-startup.md` 中提取已有的源材料分析
2. 补充阅读更多相关论文（可能触发 Phase 0 的论文阅读流程）
3. 组织为**有逻辑的技术谱系**——按面→按线→按点展开
4. 最终落脚到"以上所有工作都没做到 X，这就是我们的 Gap"

**AI Co-Author 在此阶段的关键行为**:
- 从各文档中提取素材，构建论文各章节的初稿
- 确保论文叙事与 gap-analysis.md / method-design.md 中的逻辑链一致（Gap→根因→方法→验证）
- 检查论文内部的逻辑自洽性——Introduction 中 claim 的贡献是否被 Experiments 覆盖？
- 帮助润色语言，但不改变技术内容的准确性
- Related Work 部分可能需要额外的文献调研——主动提示需要补充阅读的方向

**关键原则**:
- 论文是**叙事产品**——不是把所有工作堆上去，而是讲一个有说服力的故事
- Introduction 的贡献列表直接来自 contribution.md——不在论文中"发明"新贡献
- Experiments 中的每个实验都要说清"它验证了什么 claim"
- 不要在论文中引入前序文档中没有的新内容——如果需要，说明前面的流程有遗漏

**Exit Criteria**:
- [ ] 叙事脊柱完整且自洽：Gap→方法→实验→结论 一以贯之
- [ ] Introduction 中 claim 的贡献全部被 Experiments 覆盖
- [ ] contribution.md 中的每个贡献都在论文中被充分论证
- [ ] 所有图表有 caption、有分析、有结论
- [ ] Related Work 定位清晰，落脚到本工作的 Gap
- [ ] 无前序文档中没有的新内容

**对应 Skill**: `/paper-writing` (`skills/paper-writing-skill.md`)

---

### Phase 10: Submission & Rebuttal (投稿与 Rebuttal)

> **Input**: 论文终稿 + 审稿意见
> **Output**: Rebuttal + 修改稿

**AI Co-Author 在此阶段的关键行为**:
- **模拟审稿人**：在投稿前，从不同角度（理论、实验、写作、novelty）审视论文，预判可能的质疑
- **Rebuttal 撰写**：逐条回应审稿意见，礼貌但有力
- **补充实验**：如果审稿人要求额外实验，回到 Phase 8 的流程执行
- **论文修改**：确保修改与 rebuttal 中的承诺一致

（待用户实际投稿经验后进一步补充）

**对应 Skill**: `/rebuttal`（暂缓，待实际投稿经验后创建）

---

### Phase 11: Project Retrospective (项目回顾与知识回收)

> **Input**: 所有已产出文档 + `iteration-log.md`(如有) + 项目结局 (完成/中止)
> **Output**: `retrospective.md` + 知识库更新

**本质**: 将项目经验——无论成功还是失败——系统性地沉淀回知识库，形成复利闭环。

**为什么是正式 Phase？**
知识回收不是可选的"如果有时间就做"的事情。每个项目都会产生大量经验，如果不沉淀，这些经验就随着上下文窗口的关闭而消失。Phase 11 确保**没有项目是白做的**——即使方法失败了，失败的原因本身就是有价值的知识。

**两个入口**:

```
路径 A：自然完成
    Phase 10 (投稿/Rebuttal) → Phase 11

路径 B：中止退出
    Exit Assessment Gate (Abandon) → Phase 11
```

**流程**:

1. **项目时间线重建** — 回顾从 Phase 1 到当前的关键决策点和转折
2. **成败分析** — 什么 work 了？什么没 work？为什么？
3. **迭代历史总结** — 如果有 iteration-log.md，总结迭代历程和每次迭代的教训
4. **知识库资产提取** — 将项目经验转化为四类可复用资产（见下方）
5. **写入 retrospective.md** — 结构化的项目回顾文档

**知识库更新（回馈 Phase 0）**:

这是 Phase 11 最关键的产出——项目经验沉淀回知识库的四类资产：

| 知识库资产 | 成功项目贡献 | 失败/中止项目贡献 |
|-----------|------------|----------------|
| **Methods Bank** | 新方法、验证有效的组件组合、最优超参数范围 | 哪些组件在什么条件下不 work、失败的组合方式 |
| **Gaps & Assumptions** | 已解决的 Gap（标记为 resolved）、验证成立的假设 | 被证伪的假设、比预想更难的 Gap、仍然 open 的子问题 |
| **Experimental Patterns** | 有效的实验设计模式、可靠的评估 pipeline | 有误导性的 metrics、评估陷阱、不公平的对比设置 |
| **Cross-Paper Connections** | 新发现的方法间关联、成功的跨域迁移 | 看似相关但实际不兼容的方法组合 |

**失败项目的特殊价值**:
- "负面知识"（什么不 work）往往比正面知识更稀缺——论文不发表负面结果，但知识库可以记录
- 失败诊断中的根因分析，可以防止未来项目在相同的地方跌倒
- 部分组件可能是 work 的，只是整体组合不成功——这些组件仍然有复用价值

**`retrospective.md` 包含**:
- 项目概述（一句话总结 + 最终结局）
- 关键决策时间线
- 成败分析（what worked / what didn't / why）
- 迭代历史总结（如有）
- 知识库更新清单（新增/修改了哪些知识库条目）
- 对未来相关项目的建议

**AI Co-Author 在此阶段的关键行为**:
- 客观回顾项目全程，不美化也不过度自责
- 主动从失败中提取可复用知识——"虽然整体没 work，但组件 X 在条件 Y 下是有效的"
- 帮助将经验转化为结构化的知识库条目
- 识别项目中的意外发现——有时失败的项目中藏着通往其他方向的线索

**Exit Criteria**:
- [ ] retrospective.md 完成
- [ ] 知识库四类资产已更新
- [ ] 失败项目：失败根因已清晰记录，已排除方案已标注
- [ ] 成功项目：关键成功因素已提炼，可复用模式已识别
- [ ] 对未来相关项目的建议已记录

**对应 Skill**: `/retrospective` (`skills/retrospective-skill.md`)
**对应模板**: `templates/retrospective.md`

---

## 三、可复用模式（从用户实践中提炼）

### 已识别的模式

1. **Phase 即纯函数** — 每个 Phase 是 `f(Input Docs) → Output Docs`，上下文无关，输出不重叠
2. **知识库驱动的组合推导** — Gap 和 Method 都不是灵感闪现，而是从知识库中系统性组合推导出来的
3. **组件化方法设计** — 方法 = 可插拔组件的框架，组件可独立审查和替换
4. **双 Todo 交替执行** — code-todo.md (写什么代码) + experiment-todo.md (跑什么实验)，交替推进
5. **五维实验设计** — Dim 0 快速验证 + Dim 1-3 核心验证 + Dim 4 科学发现
6. **快速部署快速验证** — 先实现最少代码跑通 Dim 0，验证核心假设后再补全代码和实验
7. **四级迭代决策** — 调参→换组件→换框架→换方向，优先低级别迭代
8. **实时记录铁律** — 实验结果即时记录，不拖延
9. **独立审查消除确认偏误** — Review Phase 上下文解耦，Reviewer 2 人格，审查正确性 + 发表价值
10. **贡献跟踪贯穿全程** — contribution.md 从 Gap 到实验持续演化，确保 novelty 始终达标
11. **统一 CLAUDE.md** — 一个文件三个区域（项目概览 + Code/ 子节 + Papers/ 子节），按阶段渐进填写
12. **迭代输入接口** — Phase 签名 `f(Base [, Iteration Context]) → Output`，回调时携带 review 报告或 iteration-log.md，避免从零开始或重蹈覆辙
13. **Exit Assessment Gate** — Agent 驱动的退出评估，嵌入在 L2-4 回调和 Review Block 中，只要有合理可能就不放弃
14. **知识闭环** — Phase 11 Retrospective 将项目经验（含失败）沉淀回 Phase 0 知识库，形成复利效应

### 待探索的优化方向
- Related Work 的自动化文献调研流程
- 知识库生命周期管理（索引、淘汰、跨项目复用）
- 并行工作流的同步策略
- 多个消融实验的并行执行策略

---

## 四、模板与 Skill 索引

### 模板
| 模板 | 文件 | 用于 |
|------|------|------|
| 论文阅读笔记 | `templates/paper-reading-note.md` | Phase 0 |
| 项目启动文档 | `templates/project-startup.md` | Phase 1 |
| Gap 分析 | `templates/gap-analysis.md` | Phase 2 |
| 方法设计 | `templates/method-design.md` | Phase 4 |
| 实验设计 | `templates/experiment-design.md` | Phase 6 |
| 实验执行清单 | `templates/experiment-todo.md` | Phase 8 |
| 贡献跟踪 | `templates/contribution.md` | Phase 2, 4, 8 |
| 迭代日志 | `templates/iteration-log.md` | Phase 8 (L2-4退出时) |
| 项目回顾 | `templates/retrospective.md` | Phase 11 |
| 项目 CLAUDE.md | `templates/project-claude-md.md` | Phase 8 |

### Skills

#### 工作 Phase Skills
| Skill | 文件 | Phase | 触发场景 |
|-------|------|-------|---------|
| `/paper-reading` | `skills/paper-reading-skill.md` | Phase 0 | 阅读并沉淀论文 |
| `/project-startup` | `skills/project-startup-skill.md` | Phase 1 | 启动新研究项目 |
| `/gap-discovery` | `skills/gap-discovery-skill.md` | Phase 2 | 系统性发现研究空白 |
| `/method-design` | `skills/method-design-skill.md` | Phase 4 | 设计解决 Gap 的方法 |
| `/experiment-design` | `skills/experiment-design-skill.md` | Phase 6 | 设计五维验证体系 |
| `/impl-setup` | `skills/impl-setup-skill.md` | Phase 8 环境 | 代码起点选择 + Baseline 复现 |
| `/impl-validate` | `skills/impl-validate-skill.md` | Phase 8a | 核心实现 + Dim 0 快速验证 |
| `/impl-full` | `skills/impl-full-skill.md` | Phase 8b | 补全实现 + Dim 1-4 完整实验 |
| `/paper-writing` | `skills/paper-writing-skill.md` | Phase 9 | 论文撰写 |
| `/rebuttal` | — | Phase 10 | 投稿与 Rebuttal（暂缓） |
| `/retrospective` | `skills/retrospective-skill.md` | Phase 11 | 项目回顾与知识回收 |

#### Review Skill（通用框架 + 配置）
| Skill | 文件 | Phase | 触发场景 |
|-------|------|-------|---------|
| `/review gap` | `skills/review-skill.md` + `review-configs/gap-review.yaml` | Phase 3 | Gap 独立审查 |
| `/review method` | `skills/review-skill.md` + `review-configs/method-review.yaml` | Phase 5 | 方法独立审查 |
| `/review experiment` | `skills/review-skill.md` + `review-configs/experiment-review.yaml` | Phase 7 | 实验设计独立审查 |

### SubAgents
| SubAgent | 文件 | 调用方 | 职责 |
|----------|------|--------|------|
| Review SubAgent | `subagents/review-subagent.md` | `/review` Skill | 独立审查，消除确认偏误 |
| Exit Assessment Gate | `subagents/exit-assessment-subagent.md` | `/review` (Block) + `/impl-validate` (L2-4) | 评估项目是否值得继续 |
| Iteration Diagnosis | `subagents/iteration-diagnosis-subagent.md` | `/impl-validate` + `/impl-full` | 实验失败诊断 + 迭代级别判定 |
