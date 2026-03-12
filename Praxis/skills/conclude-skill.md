# Skill: Praxis 编码阶段总结（Conclude）

## 前置条件

项目当前状态应为 `coding` 阶段（R8 完成后的人工编码阶段）。

---

## 执行流程

### Step 1: 确认项目状态

直接读取项目状态文件：

```
<project_path>/pipeline-status.json
```

取 `"phase"` 字段，确认当前 phase 为 `coding`。如果不是，提示用户当前状态并询问是否继续。

> research_runner 的职责在 R8 完成后已结束，无需调用。状态直接从 `pipeline-status.json` 读取即可。

### Step 2: 收集编码阶段信息

与用户交互，了解编码阶段发生了什么：

1. **实现了什么？** — 哪些 code-todo.md 项目已完成
2. **验证了什么？** — 运行了哪些实验（Dim 0 或更多）
3. **失败了什么？** — 具体的失败现象、指标数据
4. **失败原因分析** — 与用户讨论：
   - 是某个组件不 work？（→ L2 Swap，回到 R1，R1 agent 会根据 L2 标签微调 Gap）
   - 是整体方法框架有问题？（→ L3 Redesign，回到 R1，R1 agent 重新框架化 Gap）
   - 是 Gap/RQ 方向本身有问题？（→ L4 Pivot，回到 R1，换全新方向）
   - 是否应该放弃该项目？（→ Abandon，进入 R8 回顾）

同时读取项目中的现有文档（`research/method-design.md`、`research/experiment-design.md`、`Codes/` 下的文件）来辅助分析。

### Step 3: 写入 iteration-log.md

按 `<noesis_root>/Praxis/templates/iteration-log.md` 模板格式，在项目的 `iteration-log.md` 中追加一个新 Entry：

- **迭代级别**：L2 / L3 / L4 / Abandon
- **目标 Phase**：R1 / R8
- **失败诊断**：核心发现、失败定位、根因分析、证据
- **约束传递**：已验证可行的部分、已排除方案、建议方向
- **当前版本快照**：research/method-design.md 摘要、关键实验结果

同时写入 `research/result.md`（追加模式）：

将实验过程中所有有价值的发现和洞察记录在此文件中。与 iteration-log.md 不同，result.md 不受结构化格式限制，可以详细记录：
- 实验观察到的现象和数据
- 与用户讨论中产生的 insight
- 各组件的实际行为 vs 预期行为
- 意外发现（即使方法失败，这些发现可能指向新方向）
- 具体的实验数据、图表描述、日志片段等

> 这些一手信息是后续研究迭代最宝贵的输入。

### Step 4: 设置状态

根据诊断结果，使用状态机设置下一阶段：

```bash
python3 <noesis_root>/Praxis/orchestrator/research_state_machine.py init-phase <project_path> <target_phase>
```

| 诊断结果 | 目标 Phase | 说明 |
|---------|-----------|------|
| L2 Swap（换组件） | R1 | gap-discovery 读 iteration-log + result.md，微调 Gap 后重建完整叙事 |
| L3 Redesign（换框架） | R1 | gap-discovery 读 iteration-log + result.md，重新框架化 Gap |
| L4 Pivot（换方向） | R1 | gap-discovery 读 iteration-log + result.md，避免已排除方向 |
| Abandon | R8 | 进入回顾，提取经验教训 |

### Step 5: 提示下一步

```
✅ 编码阶段总结完成。
   迭代级别：[L2/L3/L4/Abandon]
   iteration-log.md 已更新。
   状态已设置为 [target_phase]。

   下一步：运行 /praxis-research <project_path> 重启研究模块。
```

（如果是 Abandon：提示运行 `/praxis-evolve <project_path>` 提取经验教训）

---

## 注意事项

- 这是一个**交互式** skill，需要与用户深入讨论失败原因
- iteration-log.md 是**追加模式**，不要覆盖已有的 Entry
- 已排除方案的列表非常重要——确保后续研究不会重复犯错
- 如果用户不确定迭代级别，帮助分析并给出建议
