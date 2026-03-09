---
description: "从已完成项目提取经验教训，注入全局 lessons"
---

# Skill: ResearchFlow 跨项目进化（Evolution）

> 从已完成的项目中提取经验教训，注入到全局 lessons 目录，使未来项目的 fork agent 自动获益。
> 通常在 Phase 11 Retrospective 完成后运行。

## 触发

```
/researchflow-evolve <project_path>
```

---

## 执行步骤

### Step 1：读取项目产出

读取以下文件（存在则读取，不存在跳过）：

- `<project_path>/retrospective.md` — 项目回顾与教训总结
- `<project_path>/pipeline-evolution-log.md` — 各阶段流程反思记录
- `<project_path>/iteration-log.md` — 迭代失败诊断历史
- `<project_path>/pipeline-status.json` — 迭代次数与历史

---

### Step 2：提取各 Skill 的教训

对以下每个 skill，分析上述文档，提取**与该 skill 直接相关**的教训：

| Skill | 对应阶段 |
|-------|---------|
| `project-startup` | P1 |
| `gap-discovery` | P2 |
| `review` (gap) | P3 |
| `method-design` | P4 |
| `review` (method) | P5 |
| `experiment-design` | P6 |
| `review` (experiment) | P7 |
| `impl-setup` | P8a |
| `impl-validate` | P8a_validate |
| `impl-full` | P8b |
| `paper-writing` | P9 |
| `retrospective` | P11 |

提取标准：
- **有效教训**：具体、可操作、在本项目中有正面或负面验证
- **排除**：过于宽泛的观察（"要更仔细"）、尚未验证的猜测
- 每条教训格式：`- [经验描述，1-2句，聚焦具体行为或检查点]`

---

### Step 3：更新全局 lessons 文件

Lessons 目录：`~/.researchflow/lessons/`

对每个有教训的 skill：

1. 检查 `~/.researchflow/lessons/<skill_name>.md` 是否存在
2. 若存在，读取现有内容，**去重后追加**新教训（避免重复条目）
3. 若不存在，创建文件，写入标题和教训列表

文件格式：

```markdown
# Lessons: <skill_name>

<!-- 最近更新：<date> | 来源项目：<project_name> -->

## 高频问题（需主动检查）
- [教训条目]
- [教训条目]

## 成功模式（值得复用）
- [教训条目]
```

---

### Step 4：输出汇总

列出本次更新的 skill 及新增教训数量：

```
✓ Evolution 完成

更新的 lessons 文件：
  - gap-discovery.md  (+2 条)
  - method-design.md  (+1 条)
  - impl-validate.md  (+3 条)

全局 lessons 目录：~/.researchflow/lessons/
这些教训将在下个项目的对应阶段自动注入到 fork agent 的 prompt 中。
```
