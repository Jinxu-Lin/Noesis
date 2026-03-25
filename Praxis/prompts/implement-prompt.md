# 编码实验执行指南（Implement Guide）

> 本文档是给研究者（人类或 AI Agent）的执行指南，不是自动化 fork-agent prompt。
> 状态机对本阶段返回 `action_type: "manual"`。

## 核心目标

按 `Codes/experiment-todo.md` 逐步编写代码、运行实验、记录结果。最终产出 `Codes/_Results/experiment_result.md`。

## 输入

- `Codes/experiment-todo.md` — 实验执行清单（blueprint 产出）
- `Codes/CLAUDE.md` — 编码指导（组件映射、环境、debug 指南）
- `research/method-design.md` — 方法设计（实现参考）
- `research/experiment-design.md` — 实验设计（指标、通过标准参考）

## 执行流程

### Phase 0: 环境准备

1. 按 CLAUDE.md 配置环境（依赖、数据路径、GPU 验证）
2. 确认 experiment-todo.md 环境准备项全部完成
3. 初始化 git 分支（建议为实验创建独立分支）

### Phase 1: 代码实现

按 CLAUDE.md 组件 → 文件映射表逐模块实现：
1. **深内核优先**：先完成 `Codes/core/`
2. **浅包装后做**：再编写 `Codes/experiments/`
3. **Config 驱动**：确保所有可 ablate 组件通过 config 控制

每完成一个模块：sanity check（shape/gradient）+ `git add` + `git commit`。

### Phase 2: Sanity Checks

按 experiment-todo.md Phase 0：overfit check、gradient check、shape check。失败 = 代码 bug，debug 修复后重跑。

### Phase 3: Pilot 快速验证

按 experiment-todo.md Phase 1，**完整实验前的门控**：
- 小规模数据/少量 epoch 验证核心组件
- 结果写入 `Codes/_Results/pilot_result.md`
- 对照 experiment-design.md §2.3 Pass/Adjust/Fail 标准

判断：
- **Pass** → 继续 Phase 4
- **Adjust** → 回到 design 微调，不继续后续实验
- **Fail** → 回到 formalize 重新审视攻击角度

> Pilot 用 1/10 成本发现 90% 设计问题。不通过就跑完整实验是最大资源浪费。

### Phase 4: Baseline 复现

按 experiment-todo.md Phase 2：复现到论文值 ±2%。记录隐含超参。复现困难时检查 data preprocessing、lr schedule、training epochs、tricks（EMA、gradient clipping）。

### Phase 5: 主实验 + Ablation

按 experiment-todo.md Phase 3-4：
1. 先跑 full model 确认有效
2. 逐个 ablation（每次只改一个组件）
3. 至少 **3 次 random seed**，报告 mean ± std
4. 异常结果立即记录分析

### Phase 6: 结果记录

写入 `Codes/_Results/experiment_result.md`：

```markdown
# Experiment Results

## 1. 环境信息
- GPU: [型号, 显存] / PyTorch: [版本] / CUDA: [版本]

## 2. Baseline 复现结果
| Method | 论文值 | 复现值 | 差异 |

## 3. 主实验结果
| Method | [指标1] | [指标2] | ... |
（所有数值为 3 次 seed 的 mean ± std）

## 4. Ablation 实验结果
| 变体 | [指标1] | [指标2] | 对应组件 |

## 5. 分析
### 5.1 假设验证
| 假设 | 验证结果 | 证据 |
### 5.2 意外发现
### 5.3 失败分析（如有）

## 6. 结论
**总体判定**：success / iterate_method / iterate_direction / abandon
**判定依据**：[基于实验数据的具体论证]

**如果 iterate_method**：失败组件、建议修改方向、保留组件
**如果 iterate_direction**：方向层失败原因、关键洞察
```

## 判定指南

### success
- 主实验指标优于 baseline（达到通过标准）
- Ablation 支持因果论证
- 多次运行结果稳定

### iterate_method
方向正确但整体未达标。典型信号：接近但未超过 baseline、某组件无效/有害、性能对某超参极敏感。

### iterate_direction
Root cause 分析可能有误。典型信号：远逊于 baseline、所有 ablation 无正面信号、与探针信号不一致。

### abandon
多轮迭代无进展、根本性不可行、资源耗尽无希望。

## 失败时使用 /praxis-conclude

判定为 `iterate_method` 或 `iterate_direction` 时，推进状态前可用 `/praxis-conclude` 进行结构化失败诊断：交互式分析失败根因 → 写入 `iteration-log.md` + 更新 `experiment_result.md`。

## 推进状态

```bash
# 验证通过 → 知识回收
python3 ~/Research/Noesis/Praxis/orchestrator/research_runner.py advance <project_path> --outcome success

# 方法层失败 → 联合设计
python3 ~/Research/Noesis/Praxis/orchestrator/research_runner.py advance <project_path> --outcome iterate_method

# 方向层失败 → 问题锐化
python3 ~/Research/Noesis/Praxis/orchestrator/research_runner.py advance <project_path> --outcome iterate_direction

# 放弃
python3 ~/Research/Noesis/Praxis/orchestrator/research_runner.py advance <project_path> --outcome abandon
```

## Git 同步

在以下时间点执行：每个核心模块实现完成后、每个实验结果产出后、最终结果记录完成后。

```bash
cd <project_path>
git add Codes/
git commit -m "implement: [简述完成内容]"
git push origin main
```

## 编码辅助 Skill（可选）

implement 阶段可使用以下 skill 辅助编码，按顺序执行：

| Skill | 做什么 | 验证方式 |
|-------|--------|---------|
| `/praxis-code-scaffold` | 搭骨架 + 实现核心模型组件 | 单元测试全通过 + config 开关 |
| `/praxis-code-pipeline` | 数据 + 训练 + 评估 + config 体系 | 所有 config dry run 通过 |
| `/praxis-code-baseline` | sanity check + pilot + baseline 复现 | pilot 正确 + baseline ±2% |

随时可用：`/praxis-code-review` — 对照 blueprint 审查代码质量

这些 skill 是辅助工具，不是强制流程。也可以手动编码。

## 最佳实践

1. **小步验证**：每完成一个模块就 sanity check，不要全写完再跑
2. **记录一切**：训练曲线 shape 比最终数字更有诊断价值
3. **独立 config**：每次实验记录完整 config（不是"跟上次一样除了 X"）
4. **异常优先**：异常结果立即分析，往往最有价值
5. **时间管理**：超出预估 2x 时暂停评估是否值得继续
6. **数据独立**：外部数据 `~/Resources/`，生成数据 `Codes/_Data/`
