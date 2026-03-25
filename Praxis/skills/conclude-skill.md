# Skill: Praxis Conclude（实验阶段总结）— v3

交互式诊断实验失败的根因层次，写入 iteration-log.md + experiment_result.md，推进状态到正确的回退目标。

**前置条件**：Research Module phase = `implement`。

---

## Step 1: 确认状态

读取 `<project_path>/Docs/research-module-status.json`，取 `"phase"` 字段。
- phase = `implement` → 继续。
- 否则 → 告知用户当前 phase，询问是否继续。

---

## Step 2: 收集实验信息

读取项目现有文档辅助分析：
- `research/method-design.md`、`research/experiment-design.md`
- `Codes/_Results/probe_result.md`、`Codes/_Results/experiment_result.md`、`Codes/_Results/pilot_result.md`
- `Codes/experiment-todo.md`
- `iteration-log.md`

与用户交互，逐项确认：

1. **实现了什么** — experiment-todo.md 中哪些已完成
2. **验证了什么** — 运行了哪些实验（Dim 0 或更多），结果数据
3. **失败了什么** — 具体失败现象、指标偏差

### 深度追问（不满足于表面描述）

**训练过程**：
- loss 曲线形状？完全不下降 / 下降后平台 / 下降后发散？
- 多 random seed 复现？单次失败可能只是运气
- gradient norm 趋势？梯度爆炸/消失？
- 训练速度是否符合预期？data loading bottleneck？

**实验结果**：
- "完全不 work" vs "work 但不够好"？诊断方向完全不同
- 与 baseline 差距量级？1% vs 10%？
- 不同数据集/任务表现是否一致？不一致本身是诊断线索
- Ablation 中核心组件贡献是否符合预期？无贡献 → 问题在方法层

**工程实现**：
- 代码实现与 method-design.md 一致性？实现 bug 是 DL 研究失败的最常见原因
- 自定义 loss / layer 做过 gradient check / unit test？
- 数据 pipeline 验证？（数据泄漏、标签错误、normalization 不一致）

---

## Step 3: 失败层次诊断

与用户讨论，**必须明确选择一个层次**：

| 层次 | 判据 | 去向 |
|------|------|------|
| 执行层（bug/工程） | 设计正确但实现有问题，修复后预期恢复性能 | 留在 implement |
| 方法层（组件不 work） | Gap 仍存在，但技术方案需调整 | → design |
| 方向层（假设不成立） | 换方法也不行，问题定义有根本错误 | → formalize |

### 各层次典型症状

**执行层**（留在 implement）：
- OOM / CUDA 错误 — gradient accumulation / mixed precision 可解决
- 训练不收敛但可定位到实现 bug — loss reduction 模式错误、维度 broadcasting 异常、shuffle 设置不当
- 数据 pipeline 问题 — 数据泄漏、预处理不一致、标签偏移
- 环境/依赖问题 — 库版本不兼容、CUDA 版本不匹配
- 数值不稳定但可简单 fix — 加 epsilon、gradient clipping、log_softmax 替代 log(softmax)

**方法层**（→ design）：
- 核心组件在 ablation 中无信号 — 去掉核心贡献后性能不变（区分"确实无效" vs "被其他因素掩盖"）
- 训练不稳定且根因在方法架构 — GAN 模式崩塌、RL reward hacking、对比学习表征坍缩
- 性能提升来自非核心组件 — 主要来自通用数据增强或更大容量，核心贡献 claim 站不住
- 方法 work 但代价过高 — 10x 计算量换 2% 提升
- 仅在特定条件下 work — 限于某数据集/超参范围/模型规模
- 组件间冲突 — 多 loss 互相拉扯、最优超参互相矛盾

**方向层**（→ formalize）：
- Gap 被证明不存在 — SOTA 充分训练后问题消失
- 问题定义有误 — bottleneck 不在预期位置
- 攻击角度理论行不通 — 用局部信息解决需要全局信息的任务
- 核心假设被实验证伪 — probing 实验否定前提假设
- 评估范式的根本问题 — benchmark/metric 不反映真正问题
- 信息论/理论下界约束 — 试图突破理论天花板

### 关键区分判据

ablation 是最有效的区分工具：
- 核心组件有信号但不够强 → 方法层（组件设计需优化）
- 核心组件完全无信号，即使 oracle 输入也无改善 → 方向层

写入诊断模板：

```markdown
## 失败诊断

### 失败层次
- [x] [执行层/方法层/方向层]

### 诊断依据
[具体实验证据：哪个实验、什么结果、与预期偏差]

### 如果回退到 design
- 需修改组件: [列表]
- 应保留组件: [列表 + 理由]
- 已排除替代方案: [列表 + 理由]

### 如果回退到 formalize
- Gap 定义是否仍有效: [是/否 + 理由]
- 攻击角度失败原因: [分析]
- 关键洞察: [用于指导下一轮 formalize]
```

---

## Step 4: 迭代守卫

读取 `Docs/research-module-status.json` 的 `history` 字段：

- **design 回退 >= 2 次** → 告知用户"方法层多次失败，建议升级到方向层（formalize）回退"
- **formalize 回退 >= 3 次** → 告知用户"方向层多次失败，建议评估是否 abandon"

守卫逻辑：
- design 回退 >= 2 次 → 问题大概率不在方法细节，而在 Gap 分析不准或攻击角度不可行
- formalize 回退 >= 3 次 → 可能领域理解不够、问题当前不可解、或所需资源远超可用
- Abandon 不是耻辱 — 充分记录的 abandoned 项目为知识库贡献排除性知识

---

## Step 5: 写入文档

### 5.1 iteration-log.md

在项目 `iteration-log.md` 中**倒序追加**一条记录。

**方法层回退**：
```markdown
## [X.0] — YYYY-MM-DD — Method Iterate (implement → design)

- **触发**: [什么组件失败了，具体现象]
- **诊断层次**: method_level
- **变更文档**: method-design.md (X.0), experiment-design.md (X.0)
- **排除方案**: [组件/方法名] — 原因: [具体分析]
- **应保留组件**: [列表 + 理由]
- **关键洞察**: [最有价值的发现]
```

**方向层回退**：
```markdown
## [X.0] — YYYY-MM-DD — Direction Pivot (implement → formalize)

- **触发**: [什么实验失败了，具体现象]
- **诊断层次**: direction_level
- **变更文档**: problem-statement.md (X.0), method-design.md (X.0), experiment-design.md (X.0)
- **排除方向**: [方向/攻击角度名] — 原因: [具体分析]
- **关键洞察**: [最有价值的发现]
- **实验数据保留**: `experiments/iter-<N>/` 保留完整日志
```

### 写好 iteration-log 的要求

**排除方案必须写清为什么排除**：
- 差："方法 A 不 work"
- 好："方法 A（基于 linear attention 的 O(n) 近似）在序列长度 > 4096 时 PPL 从 15.2 升到 45.7，原因是线性近似在 long-range dependency 下信息损失过大。排除所有 linear kernel approximation 路线"

**关键洞察应可迁移**：
- 差："这次实验让我们学到了很多"
- 好："multi-task 训练中各任务 loss scale 差异超过 10x 时梯度冲突导致训练振荡，需在 design 阶段加入 loss balancing 策略"

### 5.2 experiment_result.md

追加至 `Codes/_Results/experiment_result.md`，记录所有实验一手数据。

### 5.3 从失败中提取价值

即使项目失败，记录以下复用资产：
- **负面结果知识** — "X 方法在数据规模 < 10K 时不行"比"X 不行"有价值得多
- **实验设施** — 训练好的 baseline、数据 pipeline、evaluation code、超参搜索结果
- **意外发现** — 与主问题无关但有趣的现象可能是新研究种子

---

## Step 6: 推进状态

```bash
python3 <noesis_root>/Praxis/orchestrator/research_runner.py advance <project_path> --outcome <outcome>
```

| 诊断结果 | outcome | 目标 Phase |
|---------|---------|-----------|
| 执行层（bug） | — | 留在 implement，用户自行修复 |
| 方法层 | `iterate_method` | design |
| 方向层 | `iterate_direction` | formalize |
| 成功 | `success` | retrospective |
| 放弃 | `abandon` | complete |

---

## Step 7: 提示下一步

```
实验阶段总结完成。
   诊断层次：[执行层/方法层/方向层]
   iteration-log.md 已更新（版本 X.0）。
   状态已推进到 [target_phase]。

   下一步：运行 /praxis-r-auto <project_path> 继续研究流程。
```

如果 Abandon：提示运行 `/praxis-evolve <project_path>` 提取经验教训。

---

## 注意事项

- **交互式** skill，需与用户深入讨论失败原因
- iteration-log.md **倒序追加**（最新在最上方）
- 排除方向/方案的列表确保后续研究不重复犯错
- 不要过早放弃：确认已尝试合理范围的 lr、batch size、warmup 等关键超参
- 不要过晚放弃：连续三次不同方法变体都无法在 Dim 0 超过 simple baseline → 方向需重新审视
- Paper Module 已解耦，success 进入 retrospective 而非论文写作
