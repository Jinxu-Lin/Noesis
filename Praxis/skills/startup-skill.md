# Skill: Project Startup (研究项目启动)

> **执行模式：交互式** — 本阶段由研究者与 Claude 协作完成，不在自动化循环中运行。

## 触发

通过 `/praxis-start <project_name>` 触发。

## 输入

研究者提供以下**任意组合**（至少一种）：

- 论文 PDF / arXiv 链接 / 论文内容
- 领域描述 / 关键词
- 研究者自己的初步想法或直觉
- 已有的笔记或草稿
- **"一起看看 Episteme 知识库"** — Claude 与研究者共同探索 `~/Documents/Episteme` 中已积累的知识资产，从中发现可做的方向

## 执行流程

### Step 0: 项目初始化

**0a. 确定项目名称与路径**

与研究者确认项目名称，项目默认创建在 `~/Documents/` 下：

```bash
mkdir -p ~/Documents/<project_name>/phase-outcomes
```

**0b. 创建项目脚手架**

```
~/Documents/<project_name>/
├── CLAUDE.md                  ← 本步骤创建（项目入口文件）
├── phase-outcomes/            ← fork agent 写入 outcome JSON
├── contribution.md            ← 空文件，Phase 2 时填写
└── pipeline-evolution-log.md  ← 空文件，各阶段反思记录
```

**0c. 创建 CLAUDE.md**

按 `Praxis/templates/project-claude-md.md` 模板，填入实际项目信息。关键字段：
- `Noesis 路径`: `~/Documents/Noesis`（使用 `~`，不硬编码用户名）
- `当前阶段`: Phase 1 (Project Startup)

---

### Step 1: 研究种子定位与核心假设提取

**1a. 识别研究种子来源**

根据研究者提供的信息（或 Episteme 探索结果），判断属于哪种类型：
- 方法融合型（多个方法结合）
- 方法延伸型（改进已有方法）
- 领域迁移型（方法迁移到新领域）
- 问题驱动型（从问题出发）
- 现象启发型（从观察出发）
- 混合型（以上多种的组合）

如果是从 Episteme 探索出发：记录"灵感来自哪些知识资产"（论文笔记/Methods Bank/Gaps 等），建立可追溯链接。

**1b. 显性化核心假设**

研究者的直觉背后隐含着一系列前提假设——在阅读源材料之前，先把这些假设写成清单并标注：

| 假设 | 来源 | 当前支撑强度 |
|------|------|------------|
| 假设描述 | 研究者推断 / 源材料名称 | 强（有直接证据）/ 弱（间接推断）/ 无（待验证） |

**要求**：至少提取 3 条假设。每条必须是"如果为假则整个方向站不住脚"的关键命题，不能是无关紧要的细节。

---

### Step 2: 深度理解源材料

对每份源材料执行：
1. **阅读与理解** — 全面理解材料内容
2. **结构化提取** — 提取核心方法、关键贡献、技术细节
3. **正向关联标注** — 标注与研究者洞察相关的支持性证据
4. **反向标注** — 标注源材料中与 Step 1 假设相矛盾、构成挑战、或暗示边界条件的内容（哪怕是轻微的信号）

要点：
- 不要泛泛总结，要聚焦于与研究种子相关的技术细节
- 保留数学公式和关键定义的精确表述
- 如果是论文，重点关注方法论部分，而非实验结果
- **反向标注不是为了否定方向，而是为 Step 4 的辩论积累原材料**

如果源材料来自 Episteme：直接引用知识库中已有的笔记和提取结果，避免重复工作。

---

### Step 3: 知识综合与 Gap 分析

1. 分析源材料之间的**关系图谱**（互补/竞争/正交）
2. 识别现有工作的**空白地带**
3. 评估研究者洞察的**技术可行性**（定性判断）
4. 识别潜在的**技术风险**

本步骤产出"**第一版研究方向**"，作为 Step 4 辩论的检验对象。
在本步骤不必追求完美——有瑕疵的第一版比过度打磨更好，因为 Step 4 会暴露真实问题。

---

### Step 4: 六维创意辩论（多 Agent 并行压力测试）

> 目标：对 Step 3 产出的研究方向从六个独立视角施加结构化压力，在进入 R2 之前发现盲点。
> 执行方式：并行召唤 6 个独立 Agent，再由综合者顺序汇总决策。

---

#### 4a. 准备辩论上下文

整理以下内容，作为每个辩论 Agent 的共享输入（构建 prompt 时直接嵌入）：

```
## 研究方向草稿（Step 3 产出）
[直接引用 Step 3 的第一版研究方向，完整内容]

## 核心假设清单（Step 1 产出）
[直接引用 Step 1 的假设表格，含假设编号]

## 源材料关键发现（Step 2 产出）
[每份源材料各 3-5 句核心发现摘要]

project_path: <project_path>
debate_output_path: <project_path>/phase-outcomes/debate/<role>.md
```

创建辩论输出目录：
```bash
mkdir -p <project_path>/phase-outcomes/debate
```

---

#### 4b. 并行召唤六个辩论 Agent

**在单条消息中**同时发起以下 6 个 Agent 调用（完全并行）。

每个 Agent 的 `prompt` = 4a 整理的辩论上下文 + 对应 subagent 文件的完整内容（从 `<noesis_path>/Praxis/subagents/` 读取并嵌入）：

| Agent | Subagent 文件 | 输出路径 |
|-------|--------------|---------|
| 创新者（Innovator） | `innovator-subagent.md` | `phase-outcomes/debate/innovator.md` |
| 务实者（Pragmatist） | `pragmatist-subagent.md` | `phase-outcomes/debate/pragmatist.md` |
| 理论家（Theorist） | `theorist-subagent.md` | `phase-outcomes/debate/theorist.md` |
| 反对者（Contrarian） | `contrarian-subagent.md` | `phase-outcomes/debate/contrarian.md` |
| 跨学科者（Interdisciplinary） | `interdisciplinary-subagent.md` | `phase-outcomes/debate/interdisciplinary.md` |
| 实验主义者（Empiricist） | `empiricist-subagent.md` | `phase-outcomes/debate/empiricist.md` |

等待全部 6 个 Agent 完成。

---

#### 4c. 召唤综合者 Agent

6 个辩论 Agent 全部完成后，顺序发起综合者 Agent 调用：

`prompt` = 以下内容 + `synthesizer-subagent.md` 完整内容：

```
## 研究方向草稿
[与 4a 相同的方向草稿]

## 核心假设清单
[与 4a 相同的假设表格]

debate_dir: <project_path>/phase-outcomes/debate
project_path: <project_path>
```

综合者输出写入：`<project_path>/phase-outcomes/debate/synthesis.md`

---

#### 4d. 将综合结果呈现给研究者

综合者完成后，读取 `synthesis.md`，向研究者呈现：
- 判定结果（方向确认 / 方向强化 / 方向修正 / HIGH RISK）
- 必须处理的优先问题列表
- 进入 R2 时带着的已知风险

等待研究者反馈：
- 对某个辩论视角有异议 → 记录异议和理由，追加到 `synthesis.md` 末尾的研究者异议节
- 认可综合结论 → 进入 Step 5

---

### Step 5: 生成 Startup 文档

按照 `Praxis/templates/project-startup.md` 模板，生成完整的项目启动文档，写入 `<project_path>/project-startup.md`。

**Step 4 的六维辩论综合结果以完整形式纳入文档**（不压缩、不删减），作为后续阶段的参考基线。

要求：
- 源材料总结要**深入而精准**，有技术深度，而非浅层概述
- Gap 分析要**具体而尖锐**，指出确切的技术缺口
- 研究方向要与 Gap 直接对应，形成逻辑闭环
- **方向描述反映六维辩论综合后的最终版本**（如有修正，注明修正了什么及原因）

---

### Step 6: 与研究者确认

将文档呈现给研究者，确认：
- 对源材料的理解是否准确？
- Gap 分析是否命中要害？
- 六维辩论发现的问题，研究者是否认可？是否有需要补充的上下文来消解质疑？
- 否证条件（Empiricist 提出的）是否符合预期？

如果研究者对某个辩论视角的分析有异议，记录异议和理由，纳入文档的研究者异议部分。

---

### Step 7: 收尾 — Git 初始化 + 状态机推进

**7a. 初始化 Git 仓库并创建 GitHub repo**：

```bash
cd ~/Documents/<project_name>
git init
gh repo create <project_name> --private --source=. --remote=origin
git add CLAUDE.md project-startup.md contribution.md pipeline-evolution-log.md phase-outcomes/
git commit -m "phase/1: project startup complete"
git push -u origin main
```

如果用户暂时不想建 GitHub 仓库（项目还太早期），可以跳过 `gh repo create` 和 `git push`，只做 `git init` + local commit。

**7b. 写入 pipeline-status.json，推进到 R1（Gap Discovery）**：

```bash
python3 ~/Documents/Noesis/Praxis/orchestrator/research_state_machine.py init-phase ~/Documents/<project_name> R1
```

同时写入 startup 的 outcome 文件（保持记录一致性）：

```json
// ~/Documents/<project_name>/phase-outcomes/startup.json
{
  "outcome": "done",
  "notes": "<1-2 句总结>"
}
```

**7c. 告知研究者下一步**：

```
Startup 完成。后续阶段将由自动化运行器推进。
运行：/praxis-research ~/Documents/<project_name>
```

## 输出

一份结构化的 `project-startup.md` 文档，包含：
- 项目知识基础（源材料深度解读）
- 知识综合与 Gap 分析
- **六维辩论综合结果**（6 视角分析 + 综合判定 + 修正方向）
- 研究方向（经过压力测试后的确认/修正版本）

## 质量标准

- 技术深度：能体现对方法论的深层理解，而非表面总结
- 结构清晰：后续阶段可直接引用本文档的特定章节
- 逻辑闭环：从源材料 → Gap → 六维辩论 → 修正方向，形成自然推导链
- **辩论有效性**：每个辩论视角至少提出 1 条可被当场验证或反驳的具体质疑
- 可操作性：读完文档后，AI 应能独立理解项目的技术语境和已知风险

## 注意事项

- 研究者的核心洞察是起点，AI 的角色是帮助**显性化、结构化并压力测试**，而非替代研究者的创造性判断
- 不要急于提出方法细节，startup 阶段的目标是建立共识 + 发现盲点，不是设计方案
- **六维辩论是善意的压力测试，不是否定研究者**——经过检验仍能站住脚的方向反而更有信心进入 R2
- 如果辩论发现了研究者明显不知道的根本性问题，应当诚实指出，即使研究者可能不想听
- R2（Gap Discovery）将在本文档基础上深入分析——辩论中未解决的质疑（"进入 R2 时带着的已知风险"）会自动成为 R2 的重点
