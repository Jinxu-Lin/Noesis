# Noesis — AI Agent 自动科研系统使用说明

> **Noesis**（希腊语 νόησις，认知/洞察）是一套运行在本地 Claude Code 上的 AI Agent 自动科研框架，面向 AI/ML/DL 方向。它将知识积累与研究执行分为两个独立子系统，从读论文到写出论文全流程自动化，同时保留关键节点的人机交互。

---

## 一、系统总览

```
Logos（知识积累）              Praxis（研究执行）
  /logos-discover               /praxis-start
  /logos-read                   /praxis-research
        │                        /praxis-paper
        │  知识注入               /praxis-evolve
        ▼
   Episteme（知识库）
   ~/Documents/Episteme
        │
        ├─ Gaps & Assumptions  →  R1 Gap Discovery
        ├─ Methods Bank        →  R3 Method Design
        └─ Experimental Patterns + Reusable Resources  →  R5 Experiment Design
```

**两个子系统**完全独立运行，唯一连接点是 **Episteme 知识库**：Logos 持续填充，Praxis 在 R1/R3/R5 三个阶段消费。

---

## 二、环境与路径

| 路径 | 说明 | 同步方式 |
|------|------|---------|
| `~/Documents/Noesis` | Noesis 系统根目录 | GitHub |
| `~/Documents/Episteme` | 知识库（Logos 产出） | GitHub |
| `~/Documents/<项目名>` | 各研究项目 | GitHub（独立仓库） |
| `~/.noesis/lessons/` | 跨项目经验教训 | 本地（各 Mac 独立积累） |

**多机协作**：Mac Mini + MacBook 通过 git 同步，所有路径使用 `~`，不硬编码用户名。

**远程 GPU 服务器**：R7（Impl Planning）完成后，实验通过 SSH MCP 在远程服务器执行，代码经 git 同步，结果回传本地。

---

## 三、Logos — 持续知识积累

Logos 是一个没有终点的**循环知识引擎**：发现 → 阅读 → 知识沉淀 → 重复。

### 使用流程

**第一次使用：初始化知识库**

```bash
KB_DIR="$HOME/Documents/Episteme"
LOGOS="$HOME/Documents/Noesis/Logos"
cp "$LOGOS/templates/kb-index.md" "$KB_DIR/"
cp "$LOGOS/templates/reading-queue.md" "$KB_DIR/"
cp "$LOGOS/templates/research-directions.md" "$KB_DIR/"
```

然后编辑 `Episteme/research-directions.md`，填入研究方向、核心关键词、种子论文、目标 Venue、关注作者。

**日常循环**

```
/logos-discover          ← 发现新论文，更新阅读队列
/logos-read              ← 深度阅读，提取知识资产，更新知识库
```

### `/logos-discover` — 论文发现

执行 5 种搜索策略，将高质量论文加入阅读队列：

| 策略 | 说明 |
|------|------|
| A. 关键词搜索 | arXiv API + Semantic Scholar API，核心 × 扩展关键词 |
| B. 引用链追踪 | 种子论文的前向/后向引用 |
| C. 作者追踪 | 关注作者最新发表 |
| D. Venue 追踪 | 目标会议最新论文 |
| E. 争议/负面搜索 | negative results / criticism / replication failures |

每篇候选论文经 **Quick Scan**（Title + Abstract + Conclusion）按 4 维度评分：

| 维度 | 说明 |
|------|------|
| 研究方向相关性 | 与设定方向的匹配程度 |
| 方法可复用性 | 核心方法/组件迁移潜力 |
| 知识库互补性 | 是否填补 KB 空白 |
| 隐式假设潜力 | 是否存在可被质疑的假设 |

评分 ≥ 4 → 高优先队列；= 3 → 普通优先队列；≤ 2 → 跳过。

完成后自动 git commit + push `reading-queue.md`。

### `/logos-read [参数]` — 深度阅读

参数格式：
- 无参数 → 读队列最高优先级 1 篇
- 数字（如 `5`）→ 依次读 N 篇
- arXiv ID（如 `2405.12186`）→ 直接读指定论文
- 标题关键词 → 在队列中匹配，匹配不到则直接搜索

**提取 5 类知识资产**：

| 资产类型 | 内容 |
|---------|------|
| **Methods Bank** | 核心机制、公式、适用条件、组件可解耦性分析 |
| **Gaps & Assumptions** | 显式 limitation + 隐式可质疑假设（含可攻击性评估） |
| **Experimental Patterns** | Baselines、metrics、消融策略、数据集选择逻辑 |
| **Cross-Paper Connections** | 与 KB 已有论文的互补/矛盾/延伸/可结合关系 |
| **Reusable Resources** | GitHub 代码、数据集、预训练模型 |

完成后自动生成论文笔记、更新 `kb-index.md`，并在该方向已读 ≥ 5 篇时触发生成/更新 `domain-landscape.md`（领域地图）。

---

## 四、Praxis — 研究执行

Praxis 分为五大模块，驱动一个项目从研究想法到发表论文的完整生命周期。

```
Module 1: Startup      /praxis-start       交互式项目孵化
           ↓
Module 2: Research     /praxis-research    R1→R8 自动化研究循环
           ↓
Module 3: Code         （人工编码 + 实验）  /praxis-conclude 处理失败
           ↓
Module 4: Paper        /praxis-paper       P1→P7 自动化论文写作
           ↓
Module 5: Evolution    /praxis-evolve      提取跨项目经验教训
```

### Module 1：Startup — `/praxis-start <项目名>`

交互式项目种子孵化，分七步完成：

1. 研究者提供初始想法
2. AI 整理研究背景与当前 SOTA
3. AI 分析候选研究空白
4. **六维辩论压力测试**（并行召唤 6 个 SubAgent）：
   - 创新者（Innovator）— 放大亮点
   - 务实者（Pragmatist）— 实现可行性
   - 理论家（Theorist）— 理论基础
   - 反对者（Contrarian）— 质疑假设
   - 跨学科者（Interdisciplinary）— 跨领域视角
   - 实验主义者（Empiricist）— 实验设计可行性
   - 综合者汇总判定：方向确认 / 强化 / 修正 / HIGH RISK
5. 研究者与 AI 共同确认研究方向
6. 输出 `project-startup.md`（含完整辩论记录和已知风险列表）
7. Git 初始化 + GitHub repo 创建，状态设为 R1

完成后，`~/Documents/<项目名>/` 下已有完整的项目 `CLAUDE.md`、`pipeline-status.json`、`project-startup.md`。

### Module 2：Research — `/praxis-research <项目路径>`

自动化执行 R1→R8，由 `research_runner.py` 编排，每阶段 fork 独立 Agent 执行。

#### 研究 Pipeline 阶段表

| Phase | 内容 | Agent Tier | Codex | 出口 |
|-------|------|-----------|-------|------|
| **R1** Gap Discovery | 从 Episteme 提取 Gaps，发现研究空白，输出 `gap-analysis.md` | heavy | — | → R2 |
| **R2** Gap Review | 独立审查 R1 成果（上下文隔离）+ 可选 Codex 外部视角 | heavy | ✓ | pass→R3 / revise→R1 / abandon→R8 |
| **R3** Method Design | 从 Episteme Methods Bank 汲取，设计核心方法，输出 `method-design.md` | heavy | — | → R4 |
| **R4** Method Review | 独立审查 R3 成果 + 可选 Codex | heavy | ✓ | pass→R5 / revise→R3 / continue_R1→R1 / abandon→R8 |
| **R5** Experiment Design | 从 Episteme Patterns 汲取，设计实验规划，输出 `experiment-design.md` | heavy | — | → R6 |
| **R6** Experiment Review | 独立审查 R5 成果 + 可选 Codex | heavy | ✓ | pass→R7 / revise→R5 / continue_R3→R3 / abandon→R8 |
| **R7** Impl Planning | 产出 `Codes/` 目录（code-todo.md、experiment-todo.md），纯规划不写代码 | standard | — | → R8 |
| **R8** Retrospective | 知识回收，总结本轮研究经验，写入迭代日志 | heavy | — | → coding |

> **注意**：R8 在 R7 完成后、编码开始前执行（知识回收，不是在论文完成后）。

#### Agent Tier 说明

| Tier | 模型 | 角色 |
|------|------|------|
| `standard` | claude-sonnet-4-6 | AI Co-Author，执行性工作（R7, P2, P4, P6） |
| `heavy` | claude-opus-4-6 | 独立批判审查者，严格不妥协（R1-R6, R8, P1, P3, P5, P7） |
| `codex` | gpt-4.5-high | 可选外部 AI 审查，提供第三方视角（R2/R4/R6/P3/P7 并行） |

Codex 审查 non-blocking：MCP 不可用时自动跳过，不影响主流程路由。Codex 结果写入 `codex-reviews/`，仅供参考，不参与路由决策。

#### 迭代模式（Runner 自动注入）

- **Revise 模式**：review 文件存在（如 `gap-review.md`）→ 工作阶段被提示"基于审查意见修改，不从零开始"
- **Pivot 模式**：`iteration-log.md` 存在且阶段已迭代 → 被提示"热重启第 N 轮，严禁重复已排除方向"
- **迭代守卫**：研究 pipeline ≥ 3 次迭代自动发出警告

### Module 3：Code — 人工阶段

R8 完成后进入人工编码阶段。参照 `Codes/` 目录中的规划文档：
- `code-todo.md` — 代码实现任务列表
- `experiment-todo.md` — 实验运行任务列表
- 项目 `Codes/CLAUDE.md` — 编码阶段专用指导

**验证通过** → 进入论文写作（`paper_writing` 阶段，再运行 `/praxis-paper`）

**验证失败** → 运行 `/praxis-conclude` 进行失败总结：

```
/praxis-conclude <项目路径>
```

分析失败层级：
- L2（换组件）→ 重置到 R3（Method Design）
- L3（换框架）→ 重置到 R3
- L4（换方向）→ 重置到 R1

写入 `iteration-log.md`，重置 `pipeline-status.json`，然后重新运行 `/praxis-research` 热重启。热重启时 Runner 自动注入迭代历史，避免重复已排除方向。

### Module 4：Paper — `/praxis-paper <项目路径>`

独立状态机（`paper_state_machine.py` + `paper_runner.py`），与主 pipeline 完全解耦，状态持久化在 `Papers/paper-status.json`。

#### 论文 Pipeline 阶段表

| Phase | 内容 | Agent Tier | Codex |
|-------|------|-----------|-------|
| **P1** Outline | 从研究文档映射论文结构，输出完整大纲 | heavy | — |
| **P2** Sections | 顺序写作各章节正文 | standard | — |
| **P3** Critique | 5 角色并行审查（新颖性/方法/实验/写作/复现性）+ Codex 🔒 | heavy | ✓ |
| **P4** Integrate | 编辑整合审查意见，精炼 Abstract | standard | — |
| **P5** Final Review | 会议级终审评分（< 7.0 → 回到 P4，最多 2 轮）🔒 | heavy | — |
| **P6** LaTeX | 生成 LaTeX 源码，编译 PDF | standard | — |
| **P7** Project Review | 多视角项目级审查（Critic + Supervisor + 可选 Codex）🔒 | heavy | ✓ |

🔒 = 上下文隔离的独立审查

### Module 5：Evolution — `/praxis-evolve <项目路径>`

项目完成后，提取跨项目可复用经验，产出两类成果：

1. **跨项目 Lessons** → `~/.noesis/lessons/<skill_name>.md`
   - 标签系统：`[SYSTEM/EXPERIMENT/WRITING/...]` × `[RECURRING/NEW]` × `[✓verified/✗ineffective/?unverified]`
   - Runner 在后续项目相同阶段**自动注入**有效 lessons
   - `[✗ineffective]` 自动过滤；`[RECURRING]` 优先显示

2. **框架进化** → 基于各阶段积累的 `pipeline-evolution-log.md`，直接修改 `Praxis/prompts/`、`Praxis/skills/`、`Praxis/templates/` 文档，并 push 到 Noesis GitHub

---

## 五、辅助命令

### `/praxis-assimilate <项目路径>` — 同化外部项目

将任意状态的现有科研项目纳入 Noesis 框架：
- 重建各阶段文档（gap-analysis.md / method-design.md / experiment-design.md）
- 实际运行 R2/R4/R6 评审
- 写入 `pipeline-status.json`，使项目可被 `/praxis-research` 或 `/praxis-paper` 直接接管

### `/praxis-present <项目路径>` — 生成进展演示

读取项目当前状态，生成结构化的 `presentation.md`，用于与导师/合作者的进展汇报。支持热启动：已有 `presentation.md` 时增量更新，保留人工编辑内容。

---

## 六、全流程操作示例

### 从零开始一个新项目

```bash
# Step 1: 积累领域知识（可先于项目启动，也可并行进行）
/logos-discover
/logos-read 5

# Step 2: 孵化研究想法
/praxis-start MyResearchProject

# Step 3: 自动化研究阶段（R1→R8）
/praxis-research ~/Documents/MyResearchProject

# Step 4: 人工编码 + 实验
# 参照 Codes/code-todo.md 和 Codes/experiment-todo.md

# Step 5a: 编码成功 → 论文写作
/praxis-paper ~/Documents/MyResearchProject

# Step 5b: 编码失败 → 总结并热重启
/praxis-conclude ~/Documents/MyResearchProject
/praxis-research ~/Documents/MyResearchProject   # 热重启

# Step 6: 项目完成后提取经验
/praxis-evolve ~/Documents/MyResearchProject
```

### 同化已有项目

```bash
/praxis-assimilate ~/Documents/ExistingProject
# 完成后根据同化结果选择 /praxis-research 或 /praxis-paper 接管
```

---

## 七、Orchestrator CLI 参考

### 研究 Pipeline（research_runner.py）

```bash
# 查看当前状态
python3 ~/Documents/Noesis/Praxis/orchestrator/research_runner.py status <project_path>

# 获取下一步动作（返回 JSON，含 fork_prompt）
python3 ~/Documents/Noesis/Praxis/orchestrator/research_runner.py next <project_path>

# 推进状态（fork agent 写完 phase-outcomes/<phase>.json 后调用）
python3 ~/Documents/Noesis/Praxis/orchestrator/research_runner.py advance <project_path>

# 强制设置阶段（用于恢复/覆盖）
python3 ~/Documents/Noesis/Praxis/orchestrator/research_state_machine.py init-phase <project_path> <phase>
```

状态持久化：`<project>/pipeline-status.json`
Fork agent 输出：`<project>/phase-outcomes/<phase>.json`（格式：`{"outcome": "...", "notes": "..."}`）

### 论文 Pipeline（paper_runner.py）

```bash
python3 ~/Documents/Noesis/Praxis/orchestrator/paper_runner.py status  <project_path>
python3 ~/Documents/Noesis/Praxis/orchestrator/paper_runner.py next    <project_path>
python3 ~/Documents/Noesis/Praxis/orchestrator/paper_runner.py advance <project_path>
python3 ~/Documents/Noesis/Praxis/orchestrator/paper_state_machine.py init-phase <project_path> <phase>
```

状态持久化：`<project>/Papers/paper-status.json`
Fork agent 输出：`<project>/Papers/phase-outcomes/<phase>.json`

---

## 八、文件结构

### Noesis 系统

```
~/Documents/Noesis/
├── Logos/
│   ├── CLAUDE.md                    ← Logos 子系统指导
│   ├── skills/
│   │   ├── paper-discovery-skill.md ← 论文发现详细指令
│   │   └── paper-reading-skill.md   ← 深度阅读详细指令
│   └── templates/
│       ├── research-directions.md   ← 研究方向配置模板
│       ├── reading-queue.md         ← 阅读队列模板
│       ├── kb-index.md              ← 知识库索引模板
│       └── paper-reading-note.md    ← 论文笔记模板
│
├── Praxis/
│   ├── CLAUDE.md                    ← Praxis 子系统指导
│   ├── orchestrator/
│   │   ├── research_state_machine.py
│   │   ├── research_runner.py
│   │   ├── paper_state_machine.py
│   │   └── paper_runner.py
│   ├── skills/                      ← 非自动化模块详细指令
│   │   ├── startup-skill.md         ← /praxis-start（六维辩论）
│   │   ├── conclude-skill.md
│   │   ├── assimilate-skill.md
│   │   ├── evolve-skill.md
│   │   └── present-skill.md
│   ├── prompts/                     ← 状态机 Fork Agent 指令
│   │   ├── 10-gap-discovery-prompt.md      ← R1
│   │   ├── 1X-review-prompt.md             ← R2/R4/R6 通用审查
│   │   ├── 11-method-design-prompt.md      ← R3
│   │   ├── 12-experiment-design-prompt.md  ← R5
│   │   ├── 13-impl-planning-prompt.md      ← R7
│   │   ├── 14-retrospective-prompt.md      ← R8
│   │   ├── 30~36-*-prompt.md               ← P1~P7
│   │   ├── codex-reviewer-prompt.md
│   │   ├── X-reflect-pipeline-prompt.md    ← 每阶段自动注入
│   │   └── review-configs/                 ← 审查 YAML 配置
│   ├── subagents/                   ← SubAgent prompt 模板
│   └── templates/                   ← 项目文档模板
│
├── .claude/skills/                  ← slash commands 注册
│   ├── logos-discover/
│   ├── logos-read/
│   ├── praxis-start/
│   ├── praxis-research/
│   ├── praxis-paper/
│   ├── praxis-assimilate/
│   ├── praxis-conclude/
│   ├── praxis-present/
│   └── praxis-evolve/
│
├── introduction.md                  ← 本文件
├── CLAUDE.md                        ← Claude Code 指导
└── README.md
```

### 研究项目（单个项目）

```
~/Documents/<项目名>/
├── CLAUDE.md                        ← 项目级 Claude 指导（含 noesis_path）
├── pipeline-status.json             ← 主 pipeline 状态（单一事实源）
├── project-startup.md               ← Startup 产出（研究方向 + 辩论记录）
├── gap-analysis.md                  ← R1 产出
├── method-design.md                 ← R3 产出
├── experiment-design.md             ← R5 产出
├── iteration-log.md                 ← 迭代历史（conclude 追加）
├── pipeline-evolution-log.md        ← 流程反思日志（X-reflect 追加）
├── phase-outcomes/                  ← Fork agent 输出
├── codex-reviews/                   ← Codex 审查输出（仅参考）
├── Codes/                           ← R7 产出（实现规划）
│   ├── CLAUDE.md
│   ├── code-todo.md
│   └── experiment-todo.md
└── Papers/                          ← 论文写作模块
    ├── paper-status.json            ← 论文 pipeline 状态
    ├── paper-outline.md             ← P1 产出
    ├── paper-draft.md               ← P2/P4 产出
    ├── paper-final.tex              ← P6 产出
    ├── phase-outcomes/
    └── project-review/              ← P7 产出
```

### Episteme 知识库

```
~/Documents/Episteme/
├── research-directions.md           ← 研究方向配置（用户维护）
├── reading-queue.md                 ← 阅读队列（discover 写，read 消费）
├── kb-index.md                      ← 知识库总索引（read 自动更新）
├── domain-landscape.md              ← 领域地图（≥5篇后自动生成）
└── [arxiv-id].md                    ← 每篇论文的结构化笔记
```

---

## 九、设计原则

**两个独立子系统** — Logos 和 Praxis 各自运行，无运行时依赖，唯一连接是 Episteme 知识库。

**三层架构（Praxis）** — Orchestrator（runner.py）决定 WHAT/WHEN；Prompts（`prompts/*-prompt.md`）是纯 agent 指令；Slash commands（`.claude/skills/`）是薄封装调用层。State machine 只做纯状态转换和 I/O，不含 prompt 逻辑。

**单一事实源** — 主 pipeline 状态唯一来源：`pipeline-status.json`；论文模块：`Papers/paper-status.json`。无自动检测或状态推断。

**独立审查隔离** — R2/R4/R6（研究审查）和 P3/P5/P7（论文审查）均在上下文隔离的独立 Agent 中执行，避免确认偏误。

**Codex 并行审查** — 第三方 GPT-4.5-high 外部视角，non-blocking，不影响主流程路由，提供额外的独立参考意见。

**跨项目学习** — `/praxis-evolve` 将经验写入 `~/.noesis/lessons/`，Runner 在后续项目自动注入已验证的 lessons，系统随每个项目变得更聪明。

**X-reflect 自动注入** — 每个非 manual 阶段完成后，Runner 自动在 fork_prompt 末尾注入流程反思指令，agent 将观察追加到 `pipeline-evolution-log.md`，作为 `/praxis-evolve` 的原材料。
