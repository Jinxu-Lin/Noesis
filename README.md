# Noesis — 基于 Agents 的科研项目管理系统

> **Noesis**（希腊语 νόησις）——认知与洞察。
> **Logos**（希腊语 λόγος）——理性与知识。
> **Praxis**（希腊语 πρᾶξις）——实践与行动。

---

## 系统定位

市面上已有不少端到端的全流程自动科研系统，试图让 AI 从头到尾独立完成研究。Noesis 选择了不同的路径。

**Noesis 相信：深度科研项目的推进，离不开研究者的监督、判断与协同。**

Noesis 不追求全自动，而是将研究者置于**产品经理**的位置——定义方向、把握节奏、做出关键决策——并通过一套精心设计的 Agent 编排系统，让 AI 高效承担繁重的执行工作。

```
研究者（产品经理）
    ↕ 监督 · 确认 · 介入
AI Agent 团队（执行层）
    ↕ 搜索 · 分析 · 设计 · 写作
结构化 Pipeline（管理层）
```

这种模式下，研究者不会被淹没在繁琐的执行细节中，也不会对 AI 的输出失去控制。

---

## 设计哲学

**科研灵感的迸发，离不开知识的深度积累。**

在尝试提出新想法之前，研究者需要广泛而深入地阅读相关文献，理解领域的已知边界和潜在空白。Noesis 将这一过程制度化：在执行研究之前，先系统地积累知识。

因此，Noesis 含有两个独立子系统：

| 子系统 | 词源含义 | 职责 |
|--------|---------|------|
| **Logos** | 理性、知识 | 持续积累知识，维护 Episteme 知识库 |
| **Praxis** | 实践、行动 | 管理研究项目从立项到发表的全生命周期 |

两者通过 **Episteme**（希腊语 ἐπιστήμη，意为"科学知识"）连接：Logos 持续填充知识库，Praxis 在关键研究阶段从中汲取养分。

```
    Logos                        Praxis
  （知识积累）                  （研究执行）
  /logos-discover              /praxis-start
  /logos-read                  /praxis-research
       │                       /praxis-paper
       │   知识注入              /praxis-evolve
       ▼
  Episteme（知识库）
  ~/Documents/Episteme
       │
       ├─ Gaps & Assumptions    →  R1 研究空白发现
       ├─ Methods Bank          →  R3 方法设计
       └─ Experimental Patterns →  R5 实验设计
```

---

## Logos — 持续知识积累

Logos 是一个**没有终点的循环知识引擎**：发现 → 阅读 → 知识沉淀 → 重复。

### 论文发现：`/logos-discover`

用户配置研究方向后，Logos 通过 5 种搜索策略系统扫描学术前沿：

- **关键词搜索** — arXiv + Semantic Scholar，核心与扩展关键词组合
- **引用链追踪** — 种子论文的前向/后向引用网络
- **作者追踪** — 关注研究者的最新发表
- **Venue 追踪** — 目标顶会/期刊的最新收录
- **争议/负面搜索** — 负面结果、复现失败、批评性论文

每篇候选论文经 Quick Scan（标题+摘要+结论）进行 4 维评分（**相关性 · 方法可复用性 · 知识互补性 · 假设可攻击性**），按优先级写入阅读队列。

### 深度阅读：`/logos-read [参数]`

Agents 按优先级自动阅读队列论文，从每篇提取 5 类结构化知识资产，沉淀到 Episteme 知识库：

| 知识资产 | 内容 |
|---------|------|
| **Methods Bank** | 核心机制、公式、适用条件、组件可解耦性 |
| **Gaps & Assumptions** | 显式 limitation + 隐式可质疑假设（含可攻击性评估） |
| **Experimental Patterns** | Baseline、Metric、消融策略、数据集选择逻辑 |
| **Cross-Paper Connections** | 与已有论文的互补/矛盾/延伸/可结合关系 |
| **Reusable Resources** | 代码、数据集、预训练模型 |

读够 5 篇后自动生成 `domain-landscape.md`（领域地图）。

---

## Praxis — 科研项目管理

Praxis 将研究项目分为**五大模块**，由 Python 状态机编排，研究者在关键节点参与决策。

```
Module 1: Startup      /praxis-start       交互式项目孵化
           ↓
Module 2: Research     /praxis-research    R1→R8 自动化研究循环
           ↓
Module 3: Code         （研究者 + AI 协同编码实验）
           ↓
Module 4: Paper        /praxis-paper       P1→P7 自动化论文写作
           ↓
Module 5: Evolution    /praxis-evolve      提取跨项目经验，进化框架
```

### Module 1 · Startup — 项目立项

**这一阶段是 Praxis 与研究者协作最密集的时刻。**

立项有三种触发方式，均支持：

1. **研究者主动提供 Idea** — 将初始想法交给 Noesis，由 AI 补充背景、梳理 SOTA、分析研究空白
2. **人机共同头脑风暴** — 研究者向 Noesis 询问 Episteme 知识库的内容，结合已积累的 Gaps 和 Methods 共同发散
3. **Noesis 主动迸发灵感** — 由 Noesis 自主梳理 Episteme 库中的知识，发现跨论文的潜在联系与未填补的空白，向研究者提出候选方向

无论哪种方式，立项都经历**六维辩论压力测试**（6 个 SubAgent 并行从不同视角批判候选方向：创新者、务实者、理论家、反对者、跨学科者、实验主义者），确保方向在进入后续耗时流程前经过充分的批判性检验。

立项完成后：生成 `project-startup.md`（含完整辩论记录与已知风险清单），初始化项目仓库，状态进入 R1。

### Module 2 · Research — 自动化研究循环

`/praxis-research` 驱动 R1→R8，每阶段 fork 独立 Agent，三轮独立审查（上下文隔离，防止确认偏误），可选 Codex（GPT-4.5-high）提供第三方外部视角：

```
R1 研究空白发现 → R2 审查🔒 → R3 方法设计 → R4 审查🔒
→ R5 实验设计 → R6 审查🔒 → R7 实现规划 → R8 知识回收
```

审查结果驱动路由：`pass`（进入下一阶段）/ `revise`（打回修改）/ `abandon`（放弃本方向）。

Runner 自动注入**迭代历史**（若本方向已经历失败迭代），严禁 Agent 重复已排除路径。

### Module 3 · Code — 研究者主导阶段

R8 完成后进入编码实验阶段。参照 R7 产出的 `Codes/` 目录（`code-todo.md`、`experiment-todo.md`）执行。

**验证失败时**，运行 `/praxis-conclude` 分析失败层级，写入迭代日志，重置状态，热重启 `/praxis-research`——自动跳过已排除方向。

### Module 4 · Paper — 自动化论文写作

独立状态机（`paper_state_machine.py`），与主 pipeline 完全解耦：

```
P1 大纲 → P2 写作 → P3 五角色批判审查🔒 → P4 整合修改
→ P5 终审评分🔒（< 7.0 → 回 P4，最多 2 轮）→ P6 LaTeX → P7 项目级审查🔒
```

### Module 5 · Evolution — 框架进化

项目完成后，`/praxis-evolve` 提取跨项目可复用经验，写入 `~/.noesis/lessons/`。Runner 在后续项目**自动注入**已验证的 lessons——系统随每个项目变得更聪明。

同时基于各阶段积累的 `pipeline-evolution-log.md`，直接修改 Noesis 框架文档并推送 GitHub，实现框架自我进化。

---

## 快速开始

### 初始化知识库（首次）

```bash
KB="$HOME/Documents/Episteme"
cp ~/Documents/Noesis/Logos/templates/kb-index.md $KB/
cp ~/Documents/Noesis/Logos/templates/reading-queue.md $KB/
cp ~/Documents/Noesis/Logos/templates/research-directions.md $KB/
# 编辑 Episteme/research-directions.md，填入研究方向与关键词
```

### 积累知识

```bash
/logos-discover      # 发现论文，更新阅读队列
/logos-read 5        # 深度阅读 5 篇，提取知识资产
```

### 启动与执行研究

```bash
/praxis-start MyProject                        # 交互式项目孵化（立项）
/praxis-research ~/Documents/MyProject         # R1→R8 自动化研究

# 人工编码实验...（参照 Codes/ 目录）

/praxis-paper ~/Documents/MyProject            # P1→P7 论文写作
/praxis-evolve ~/Documents/MyProject           # 提取经验，进化框架
```

### 编码失败时热重启

```bash
/praxis-conclude ~/Documents/MyProject         # 分析失败，写入迭代日志
/praxis-research ~/Documents/MyProject         # 热重启，自动跳过已排除方向
```

### 辅助命令

```bash
/praxis-assimilate ~/Documents/ExistingProject # 同化现有项目，接入 Noesis 管理
/praxis-present ~/Documents/MyProject          # 生成进展演示（用于导师汇报）
```

---

## 环境

```
~/Documents/
├── Noesis/          ← Noesis 系统（GitHub 同步）
├── Episteme/        ← 知识库（独立 GitHub 仓库）
└── <项目名>/        ← 各研究项目（各自独立 GitHub 仓库）

~/.noesis/lessons/   ← 跨项目经验教训（本地积累）
```

多机协作（Mac Mini + MacBook）通过 git 同步，所有路径使用 `~`，不硬编码用户名。R7 后的实验通过 SSH MCP 在远程 GPU 服务器执行。

---

## 详细文档

完整使用说明（含各阶段细节、Orchestrator CLI 参考、文件结构）见 [introduction.md](introduction.md)。
