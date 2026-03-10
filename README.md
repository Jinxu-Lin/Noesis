<div align="center">

# Noesis

**基于 Agents 的 AI/ML 科研项目管理系统**

*νόησις · λόγος · πρᾶξις · ἐπιστήμη*

---

*Noesis（认知与洞察）· Logos（理性与知识）· Praxis（实践与行动）· Episteme（科学知识）*

</div>

---

## 系统定位

Noesis 是一套运行在 Claude Code 上的 **AI Agent 科研项目管理系统**，面向 AI/ML/DL 方向的研究者。

它的核心主张是：**深度科研项目的推进，离不开研究者的监督、判断与协同。** Noesis 将研究者置于**产品经理**的位置——定义方向、把握节奏、做出关键决策——同时通过一套精心设计的 Agent 编排系统，让 AI 高效承担从文献调研、方法设计、实验规划到论文写作的繁重执行工作。

Noesis 包含两个独立子系统，通过 **Episteme** 知识库连接：

- **Logos**（理性与知识）— 持续知识积累引擎。自动发现、阅读、结构化提取论文中的方法、研究空白、实验模式等知识资产，沉淀到 Episteme 知识库，为研究提供持续的知识供给。

- **Praxis**（实践与行动）— 科研项目管理系统。从项目立项到论文发表，分五大模块驱动完整的研究生命周期，在关键节点与研究者深度协同，并在每个阶段从 Episteme 知识库中汲取养分。

```
  Logos ──────────→ Episteme ──────────→ Praxis
 知识积累             知识库               研究执行
/logos-discover     Methods Bank        /praxis-start
/logos-read         Gaps & Assumptions  /praxis-research
                    Experimental        /praxis-paper
                    Patterns ...        /praxis-evolve
```

---

## 核心优势

| | 特性 | 说明 |
|---|---|---|
| **8+7自动化阶段** | 复杂模块（Research/PaperWriting）由状态机驱动，每阶段由独立 Agent 执行，多轮上下文隔离审查防止重要内容偏误 |
| **9核心Commands** | 通过命令执行知识积累，项目管理，一键同步外部科研项目至Noesis系统，一键准备对外展示报表 |
| **∞** | Noesis系统具备自我进化功能，每阶段完成后自动记录流程反思；`/praxis-evolve` 提取跨项目经验教训，Runner 在后续项目中自动注入——越用越聪明 |
| **5核心模块**  | 项目初始化 · 方法探索 · 代码编写 · 论文撰写 · 自我进化，并在每个阶段与Episteme 知识库深度链接 |

---

## 设计哲学

**科研灵感的迸发，离不开知识的深度积累。**

在尝试提出新想法之前，研究者需要广泛而深入地阅读相关文献，理解领域的已知边界和潜在空白。Noesis 将这一过程制度化：在执行研究之前，先系统地积累知识。

因此，Noesis 含有两个独立子系统：

| 子系统 | 词源 | 职责 |
|--------|------|------|
| **Logos** | λόγος，理性与知识 | 持续积累知识，维护 Episteme 知识库 |
| **Praxis** | πρᾶξις，实践与行动 | 管理研究项目从立项到发表的全生命周期 |

两者通过 **Episteme** 知识库连接：Logos 持续填充，Praxis 在关键研究阶段从中汲取养分。

```
    Logos                            Praxis
  （知识积累）                      （研究执行）
  /logos-discover                  /praxis-start
  /logos-read                      /praxis-research
       │                           /praxis-paper
       │         知识注入            /praxis-evolve
       ▼
  Episteme（知识库）  ~/Documents/Episteme
       │
       ├─ Gaps & Assumptions    ──→  R1  研究空白发现
       ├─ Methods Bank          ──→  R3  方法设计
       └─ Experimental Patterns ──→  R5  实验设计
```

---

## Logos — 持续知识积累

Logos 是一个**没有终点的循环知识引擎**：发现 → 阅读 → 知识沉淀 → 重复。

**初始化知识库（首次使用）**

```bash
KB="$HOME/Documents/Episteme"
cp ~/Documents/Noesis/Logos/templates/kb-index.md $KB/
cp ~/Documents/Noesis/Logos/templates/reading-queue.md $KB/
cp ~/Documents/Noesis/Logos/templates/research-directions.md $KB/
# 编辑 Episteme/research-directions.md，填入研究方向与关键词
```

### `/logos-discover` — 论文发现

```bash
/logos-discover      # 发现论文，按优先级写入阅读队列
```

用户配置研究方向后，Logos 通过 5 种搜索策略系统扫描学术前沿：

| 策略 | 说明 |
|------|------|
| **关键词搜索** | arXiv + Semantic Scholar，核心与扩展关键词组合 |
| **引用链追踪** | 种子论文的前向/后向引用网络 |
| **作者追踪** | 关注研究者的最新发表 |
| **Venue 追踪** | 目标顶会/期刊的最新收录 |
| **争议/负面搜索** | 负面结果、复现失败、批评性论文 |

每篇候选论文经 Quick Scan（标题 + 摘要 + 结论）进行 4 维评分（**相关性 · 方法可复用性 · 知识互补性 · 假设可攻击性**），按优先级写入阅读队列。

### `/logos-read` — 深度阅读

```bash
/logos-read              # 读队列最高优先级 1 篇
/logos-read 5            # 依次深度阅读 5 篇
/logos-read 2405.12186   # 直接读指定 arXiv 论文
```

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
  ┌─────────────────────────────────────────────────────────────┐
  │                        Praxis Pipeline                      │
  │                                                             │
  │  M1 Startup   →   M2 Research   →   M3 Code                │
  │  /praxis-start    /praxis-research   （人机协同）            │
  │                                          ↓                  │
  │               M5 Evolution   ←   M4 Paper                  │
  │               /praxis-evolve     /praxis-paper              │
  └─────────────────────────────────────────────────────────────┘
```

### Module 1 · Startup — `/praxis-start <项目名>`

```bash
/praxis-start MyProject    # 交互式立项，完成后自动初始化项目仓库
```

**这一阶段是 Praxis 与研究者协作最密集的时刻。** 立项支持三种触发方式：

- **研究者主动提供 Idea** — 将初始想法交给 Noesis，由 AI 补充背景、梳理 SOTA、分析研究空白
- **人机共同头脑风暴** — 研究者向 Noesis 询问 Episteme 知识库内容，结合已积累的 Gaps 和 Methods 共同发散
- **Noesis 主动迸发灵感** — 由 Noesis 自主梳理 Episteme 库，发现跨论文的潜在联系与未填补的空白，向研究者提出候选方向

无论哪种方式，立项都经历**六维辩论压力测试**（6 个 SubAgent 并行批判候选方向：创新者 · 务实者 · 理论家 · 反对者 · 跨学科者 · 实验主义者），确保方向在进入后续耗时流程前经过充分检验。立项完成后自动生成 `project-startup.md`（含完整辩论记录与已知风险清单），初始化项目仓库。

### Module 2 · Research — `/praxis-research <项目路径>`

```bash
/praxis-research ~/Documents/MyProject    # 驱动 R1→R8，可随时中断续跑
```

每阶段 fork 独立 Agent，3 轮上下文隔离审查防止确认偏误，可选 Codex（GPT-4.5-high）提供第三方外部视角：

```
R1 研究空白发现 ──→ R2 审查 🔒 ──→ R3 方法设计 ──→ R4 审查 🔒
──→ R5 实验设计 ──→ R6 审查 🔒 ──→ R7 实现规划 ──→ R8 知识回收
```

审查结果驱动分支路由：`pass`（进入下一阶段）·`revise`（打回修改）·`abandon`（放弃本方向）。Runner 自动注入**迭代历史**，严禁 Agent 重复已排除路径。

### Module 3 · Code — 研究者主导

R8 完成后进入编码实验阶段，参照 R7 产出的 `Codes/` 目录（`code-todo.md`、`experiment-todo.md`）执行。验证失败时：

```bash
/praxis-conclude ~/Documents/MyProject    # 分析失败层级，写入迭代日志，重置状态
/praxis-research ~/Documents/MyProject    # 热重启，自动跳过已排除方向
```

### Module 4 · Paper — `/praxis-paper <项目路径>`

```bash
/praxis-paper ~/Documents/MyProject      # 驱动 P1→P7，独立状态机，与研究 pipeline 解耦
```

```
P1 大纲 ──→ P2 写作 ──→ P3 五角色批判审查 🔒 ──→ P4 整合修改
──→ P5 终审评分 🔒（< 7.0 回 P4，最多 2 轮）──→ P6 LaTeX ──→ P7 项目级审查 🔒
```

### Module 5 · Evolution — `/praxis-evolve <项目路径>`

```bash
/praxis-evolve ~/Documents/MyProject     # 提取跨项目经验，进化框架文档
```

提取跨项目可复用经验，写入 `~/.noesis/lessons/`。Runner 在后续项目**自动注入**已验证的 lessons——系统随每个项目变得更聪明。同时直接修改 Noesis 框架文档并推送 GitHub，实现框架自我进化。

### 辅助命令

```bash
/praxis-assimilate ~/Documents/ExistingProject  # 同化现有项目，接入 Noesis 管理
/praxis-present ~/Documents/MyProject           # 生成结构化进展演示（用于导师汇报）
```

---

## 环境要求

Noesis 运行在本地 macOS + Claude Code 上，通过 GitHub 在多台设备间同步。

```
~/Documents/
├── Noesis/           ← Noesis 系统本体（GitHub 同步）
├── Episteme/         ← 知识库（独立 GitHub 仓库）
└── <项目名>/         ← 各研究项目（各自独立 GitHub 仓库）

~/.noesis/lessons/    ← 跨项目经验教训（本地积累）
```

多机协作（Mac Mini + MacBook）通过 git 同步，所有路径使用 `~`，不硬编码用户名。R7 后的实验通过 SSH MCP 在远程 GPU 服务器执行，代码经 git 同步，结果回传本地。

---

## 致谢

[Sibyl Research System](https://github.com/Sibyl-Research/sibyl-research-system) 对 Noesis 部分阶段的设计提供了灵感，在此表示感谢。

---

## 详细文档

完整使用说明（各阶段细节、Orchestrator CLI 参考、文件结构）见 [introduction.md](introduction.md)。
