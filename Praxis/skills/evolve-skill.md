# Skill: Praxis 系统进化（Evolve）

> 从已完成的项目中提取两类进化产出：
> 1. **跨项目 Lessons**：注入到 `~/.noesis/lessons/`，使未来项目的 fork agent 自动受益
> 2. **框架改进**：综合 `pipeline-evolution-log.md` 中的流程反思，更新 Noesis 的 prompts / skills / templates
>
> 通常在 R11 Retrospective 完成后运行。

---

## 执行步骤

### Step 1：读取项目产出

读取以下文件（存在则读取，不存在跳过）：

- `<project_path>/retrospective.md` — 项目回顾与研究经验总结
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
| `00-project-startup` | R1 |
| `10-gap-discovery` | R2 |
| `1X-review` | R3、R5、R7 |
| `11-method-design` | R4 |
| `12-experiment-design` | R6 |
| `13-impl-planning` | R8 |
| `40-retrospective` | R11 |

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
2. 回顾 `retrospective.md` 和 `iteration-log.md`，判断该教训描述的问题是否在本项目中再次出现：
   - **未再出现** → 标记为 `[✓ verified]`
   - **仍然出现** → 标记为 `[✗ ineffective]`，并在条目末尾加注 `（仍出现，需策略调整）`
   - **无法判断** → 保持 `[? unverified]`

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
- [NEW][PLANNING][? unverified] R8 规划时需提前确认 GPU 资源可用性
- [RECURRING][SYSTEM][✗ ineffective] SSH 超时需在实验前检查连接，当前措施无效 (出现 4 次，需策略调整)

## 成功模式（值得复用）
- [RECURRING] 先用小数据集做 sanity check，再跑完整实验 (出现 2 次)
- [NEW] 在 gap-analysis 中明确标注假设前提，有助于后续方法设计对齐
```

**注意**：Runner 自动过滤 `[✗ ineffective]` 条目，不将其注入未来项目的 prompt。
`[RECURRING]` 条目在注入时排在普通条目之前。

---

### Step 6：Pipeline 框架进化

这是 Noesis 系统自我迭代的核心步骤，基于 `pipeline-evolution-log.md` 中积累的流程反思。

**6a. 读取并汇总 pipeline-evolution-log.md**

读取项目的 `pipeline-evolution-log.md`（包含 R2-R11、P1-P7 各阶段的 X-reflect 条目）。
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
✓ Praxis Evolution 完成

── 跨项目 Lessons ──────────────────────────────────────
更新的 lessons 文件：
  - 10-gap-discovery.md  (+2 条新教训, 1 条升级为 RECURRING, 1 条标记为 ineffective)
  - 11-method-design.md  (+1 条新教训)
  - 31-paper-sections.md (+1 条新教训)

有效性评估：
  - [✓ verified]:    2 条（注入后问题消失，有效）
  - [✗ ineffective]: 1 条（注入后仍出现，需策略调整）
  - [? unverified]:  4 条（首次提取，待验证）

── 框架改进 ─────────────────────────────────────────────
处理的 pipeline-evolution-log 条目：X 条
执行的框架修改：
  - Praxis/prompts/10-gap-discovery-prompt.md：[改动描述]
  （无修改时：无高置信度改进，已记录低置信度观察，待后续项目验证）

Noesis 框架已推送到 GitHub（或：无框架改动，跳过推送）
```
