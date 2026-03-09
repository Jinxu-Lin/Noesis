# Skill: Review (通用审查框架)

> 本 Skill 是 R3/R5/R7 的通用框架。具体审查维度和辩论配置由 YAML 配置文件决定。
>
> **核心原则**：Review 是**上下文隔离的独立审查** — 此 Agent 只接收文档内容，
> 不接收任何工作阶段的过程记忆。通过**多 Agent 并行辩论 + 综合** 替代单一审查者，
> 大幅提升审查深度和发现盲点的能力。

## 触发场景

前序工作 Phase 完成后，由 runner 自动触发（或用户手动调用）：
- R3: 审查 `gap-analysis.md`      → 加载 `review-configs/gap-review.yaml`
- R5: 审查 `method-design.md`     → 加载 `review-configs/method-review.yaml`
- R7: 审查 `experiment-design.md` → 加载 `review-configs/experiment-review.yaml`

---

## 执行流程

### Step 1: 加载配置

读取对应的配置文件，获取：
- `debate_agents`: 本次审查要召唤的辩论 Agent 列表
- `debate_output_subdir`: 辩论输出目录（如 `R3`、`R5`、`R7`）
- `input_docs`: 需要读取的文档列表
- `review_dimensions`: 审查维度（作为辩论 Agent 的关注方向引导）
- `routing`: 判定后的路由配置

---

### Step 2: 读取文档

按 `input_docs` 列表读取项目目录中的文档。
**必选文档**缺失时报错停止；**可选文档**缺失时跳过。

将文档内容组装为后续步骤的共享上下文，格式：

```
## 待审查文档

### [文档名1]
[完整内容]

### [文档名2]
[完整内容]
...
```

---

### Step 3: 多视角辩论

> 目标：从 N 个独立专家视角对待审查文档施加压力，发现作者视角的盲点。
> 辩论 Agents 互相不可见，各自独立输出，最终由综合者汇总裁判。

**3a. 准备辩论上下文**

整理以下内容作为所有辩论 Agent 的共享输入：

```
## 审查文档（完整内容）
[Step 2 组装的全部文档内容]

## 审查重点维度
[来自配置文件 review_dimensions 的维度名称和核心问题列表]

project_path: <project_path>
debate_output_path: <project_path>/phase-outcomes/debate/<debate_output_subdir>/<role>.md
```

创建辩论输出目录：
```bash
mkdir -p <project_path>/phase-outcomes/debate/<debate_output_subdir>
```

**3b. 并行召唤辩论 Agents**

根据配置的 `debate_agents` 列表，**在单条消息中**同时发起所有 Agent 调用（完全并行）。

每个 Agent 的 `prompt` = 3a 中的辩论上下文 + 对应 subagent 文件的完整内容（从 `<noesis_path>/Praxis/subagents/<agent_name>-subagent.md` 读取并嵌入）。

**重要**：为每个 Agent 构建 prompt 时，将 3a 模板中的 `<role>` 替换为该 Agent 的实际名称：

> 各 review 类型的 Agent → 输出路径 映射（来自 yaml 配置的 `debate_output_subdir`）：
>
> **R3 Gap Review**（5 个 Agents）：
> | Agent | Subagent 文件 | 输出路径 |
> |-------|--------------|---------|
> | 反对者（Contrarian） | `contrarian-subagent.md` | `phase-outcomes/debate/R3/contrarian.md` |
> | 文献对标者（Comparativist） | `comparativist-subagent.md` | `phase-outcomes/debate/R3/comparativist.md` |
> | 理论家（Theorist） | `theorist-subagent.md` | `phase-outcomes/debate/R3/theorist.md` |
> | 跨学科者（Interdisciplinary） | `interdisciplinary-subagent.md` | `phase-outcomes/debate/R3/interdisciplinary.md` |
> | 务实者（Pragmatist） | `pragmatist-subagent.md` | `phase-outcomes/debate/R3/pragmatist.md` |
>
> **R5 Method Review**（6 个 Agents）：
> | Agent | Subagent 文件 | 输出路径 |
> |-------|--------------|---------|
> | 理论家（Theorist） | `theorist-subagent.md` | `phase-outcomes/debate/R5/theorist.md` |
> | 务实者（Pragmatist） | `pragmatist-subagent.md` | `phase-outcomes/debate/R5/pragmatist.md` |
> | 反对者（Contrarian） | `contrarian-subagent.md` | `phase-outcomes/debate/R5/contrarian.md` |
> | 方法论审查者（Methodologist） | `methodologist-subagent.md` | `phase-outcomes/debate/R5/methodologist.md` |
> | 创新者（Innovator） | `innovator-subagent.md` | `phase-outcomes/debate/R5/innovator.md` |
> | 实验主义者（Empiricist） | `empiricist-subagent.md` | `phase-outcomes/debate/R5/empiricist.md` |
>
> **R7 Experiment Review**（5 个 Agents）：
> | Agent | Subagent 文件 | 输出路径 |
> |-------|--------------|---------|
> | 实验主义者（Empiricist） | `empiricist-subagent.md` | `phase-outcomes/debate/R7/empiricist.md` |
> | 方法论审查者（Methodologist） | `methodologist-subagent.md` | `phase-outcomes/debate/R7/methodologist.md` |
> | 文献对标者（Comparativist） | `comparativist-subagent.md` | `phase-outcomes/debate/R7/comparativist.md` |
> | 统计怀疑论者（Skeptic） | `skeptic-subagent.md` | `phase-outcomes/debate/R7/skeptic.md` |
> | 务实者（Pragmatist） | `pragmatist-subagent.md` | `phase-outcomes/debate/R7/pragmatist.md` |

等待全部辩论 Agents 完成。

**3c. 召唤综合者 Agent**

所有辩论 Agents 完成后，顺序发起综合者 Agent 调用。

`prompt` = 以下内容 + `work-synthesizer-subagent.md` 完整内容：

```
## 当前审查阶段：<review_type>（来自 yaml 的 review_type 字段）

## 待审查文档摘要
[Step 2 文档内容的关键信息摘要，约 300-500 字]

debate_dir: <project_path>/phase-outcomes/debate/<debate_output_subdir>
project_path: <project_path>
```

综合者输出写入：`<project_path>/phase-outcomes/debate/<debate_output_subdir>/synthesis.md`

---

### Step 4: 生成正式审查报告

读取 `synthesis.md` + 原始文档，结合配置的 `review_dimensions`，生成正式审查报告，写入 `<output_doc>`（由配置决定）。

**4a. 综合判定 → Pass / Revise / Block**

synthesis.md 的判定与正式判定的映射：
| 综合者判定 | 正式审查判定 | 说明 |
|-----------|-------------|------|
| 小幅修订即可 | **Pass** | 附带改进建议，研究者可自行决定是否采纳 |
| 需要较大修改 | **Revise** | 明确列出必须修改的问题清单，进入下一个 Revise 迭代 |
| 需要重大返工 | **Block** | 触发 Exit Assessment Gate |

**4b. 审查报告结构**

```markdown
# [审查类型] 审查报告

## 多视角辩论摘要
**辩论 Agents**：[列出参与的 Agents]
**强信号问题**（多视角共识）：
- [问题1]：[来源 Agents，核心内容]
- [问题2]

**重要独立发现**：
- [[Agent名]] [发现内容]

**分歧议题裁判**：
- [视角A] vs [视角B]：[分歧 + 综合裁判]

---

## 各维度评估
[按配置的 review_dimensions 逐条评估，每条附 Pass/Revise/Block 判定]

---

## 问题清单
**必须修改（Block / Revise 级）**：
1. [问题1 — 来源 Agent — 具体描述]
2. [问题2]

**建议改进（Pass 级，可选采纳）**：
- [改进建议]

---

## 战略预判
[结合配置的 strategic_foresight_hint，给出下一阶段的风险预警和备选路径]

---

## 整体判定：[Pass / Revise / Block]
[3-5句判定理由，直接引用多视角辩论的关键发现]
```

---

### Step 4c: 外部 AI 审查（可选）

尝试调用 `mcp__codex__codex` tool 获取外部 AI 的独立视角。

**执行条件**：调用前不做额外判断，直接尝试。如果 MCP 不可用，跳过本步骤并在报告中注明"外部审查：不可用"。

**外部审查 Prompt**：
1. 将待审查文档核心内容精简为摘要（控制 token 量）
2. 要求外部 AI 以独立第三方视角评审：
   - 指出被忽略的风险、假设漏洞、方法论缺陷
   - 与已知文献的冲突或重叠
   - 具体可执行的改进建议
   - 评分 1-10 + 理由
   - 使用中文输出
3. 设置 `approval-policy: "never"`

**结果处理**：
- 成功：写入 `<output_doc 同目录>/external-review.md`，追加摘要到审查报告末尾
- 失败/不可用：跳过（non-blocking），不影响整体判定

外部审查结果**仅作参考**，不参与 Pass/Revise/Block 判定。

---

### Step 5: 根据判定路由

读取配置的 `routing`，根据整体判定执行：

**Pass**：
- 通知用户审查通过
- 展示战略预判中的"风险预警"（Pass 时同样重要）
- 提示下一步：`routing.pass.next_skill`

**Revise**：
- 展示必须修改的问题清单
- 提示用户：`routing.revise.next_skill`（进入工作阶段的 Revise 迭代模式）

**Block**：
- 触发 Exit Assessment Gate SubAgent（传入 `subagents/exit-assessment-subagent.md`）
  - SubAgent 输入：当前所有项目文档 + 迭代历史 + 战略预判候选方向
  - SubAgent 输出：Continue / Abandon + 理由
- 根据结果：
  - **Continue** → 提示 `routing.block.continue_skill`
  - **Abandon** → 提示 `/retrospective`

---

## 注意事项

- **上下文隔离是根本**：此 Agent（review fork agent）只接收文档内容，无工作过程记忆
- **辩论 Agents 独立运行**：各 Agent 互不知晓对方存在，保证视角独立性
- **综合者判断优先**：synthesis.md 的「必须修改」直接映射到 Revise/Block，不需要额外主观判断
- **Pass 不等于完美**：战略预判中的风险提示在 Pass 时同样需要呈现给研究者
- **Block 必须经过 Exit Assessment Gate**：不能直接跳到 Abandon
- **外部 AI non-blocking**：MCP 不可用时流程继续，不中断
