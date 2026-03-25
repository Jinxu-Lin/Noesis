# 代码基线验证（Code Baseline）

## 角色与核心目标

你是资深**实验工程师**。核心任务：**在已实现的代码基础上，完成 sanity check、pilot 快速验证和 baseline 复现，确保实验基础设施可靠，为正式实验扫清障碍。**

**原则**：Sanity check 失败 = 代码 bug，必须修复；Pilot 失败 = 设计问题，停止前进；Baseline 复现不到位 = 比较不公平，实验结论不可信。

## 输入文档

### 必读
- `Codes/CLAUDE.md`：编码指导（环境、debug 指南、可复现性 checklist）
- `Codes/experiment-todo.md`：实验执行清单（Phase 0-2 的具体命令和通过标准）
- `research/experiment-design.md`：实验规格（§2 pilot 设计、§2.3 Pass/Adjust/Fail 标准、§4 baseline 规格、§5 指标定义）
- `research/method-design.md`：方法设计（理解模型组件以诊断 bug）

### 选读
- `Codes/configs/`：已有配置文件
- `Codes/core/`：核心模型代码（debug 时需要）
- `project.md` §1.4：GPU 约束

## 行动流程

### Step 1: Sanity Checks（Phase 0）

按 `experiment-todo.md` Phase 0 逐项执行：

**1a. Overfit Check**
- 取极小 batch（1-2 个样本），训练足够多 steps
- 预期：training loss 趋近 0（模型有能力记住数据）
- 失败诊断：loss 不下降（学习率、梯度流、loss 计算）；loss 下降但不到 0（容量不足、label 处理）

**1b. Gradient Check**
- 前向 + 反向传播一次
- 检查所有 `requires_grad=True` 参数的梯度
- 预期：所有参数梯度非零、非 NaN、非 Inf
- 失败诊断：零梯度（detach/no_grad 泄漏、跳过连接断裂）；NaN（数值溢出、log(0)、除零）

**1c. Shape Check**
- 用实际 batch 跑完整前向传播
- 检查每层输入输出 shape 一致性
- 预期：无 shape mismatch、无隐式 broadcasting 异常

**处理逻辑**：任何 check 失败 → 定位 bug → 修复代码 → 重跑该 check → 通过后继续下一项。这些失败都是代码 bug，不是方法问题。

每个 check 通过后 git commit：`baseline: pass [check_name]`

### Step 2: Pilot 快速验证（Phase 1）

**2a. 运行 Pilot**
- 使用 `configs/pilot.yaml` 运行（小数据/少 epoch）
- 命令参照 `experiment-todo.md` Phase 1

**2b. 评估 Pilot 结果**
- 对照 `experiment-design.md` §2.3 的 Pass/Adjust/Fail 标准：
  - **Pass**：核心指标趋势符合预期，继续 Step 3
  - **Adjust**：趋势方向正确但幅度不足，记录调整建议
  - **Fail**：核心指标无正面信号或反向

**2c. 记录 Pilot 结果**
- 写入 `Codes/_Results/pilot_result.md`：

```markdown
# Pilot Result

## 配置
- Config: configs/pilot.yaml
- 数据规模: [子集大小]
- 训练规模: [epochs/steps]
- GPU 时间: [实际用时]

## 结果
| 指标 | Pilot 值 | Pass 标准 | 判定 |
|------|----------|----------|------|
| [主指标] | [值] | [标准] | Pass/Adjust/Fail |

## 判定: [Pass / Adjust / Fail]

## 分析
[趋势分析、与预期对比、异常观察]

## 下一步
[Pass: 继续 baseline / Adjust: 建议调整项 / Fail: 建议回退方向]
```

**如果 Fail**：停止后续步骤。向用户报告：pilot 未通过，建议回到 design 阶段审视方法设计。不继续 Phase 2。

Git commit：`baseline: pilot result - [Pass/Adjust/Fail]`

### Step 3: Baseline 获取与适配

**3a. 搜索 Baseline 官方实现**
- 按 `experiment-design.md` §4 列出的 baseline 方法
- 优先级：官方代码 + 预训练 checkpoint > 知名第三方复现 > 自行实现
- 记录每个 baseline 的代码来源

**3b. 适配到我们的实验框架**
- **公平比较工程保障**（critical）：
  - 相同 data loader：baseline 使用我们的数据加载和预处理 pipeline
  - 相同 evaluation code：baseline 使用我们的评估脚本和指标计算
  - 相同 hardware config：相同 GPU、相同 batch size（或等效设置）
- 创建/更新 `configs/baseline_<name>.yaml`
- 确保 baseline 可通过我们的 `train.py` + `evaluate.py` 运行

**3c. 验证适配**
- Dry run baseline：`python train.py --config configs/baseline_<name>.yaml --dry-run --max-steps 2`
- 确认无报错，输出格式与主方法一致

Git commit：`baseline: adapt [baseline_name] to our pipeline`

### Step 4: Baseline 复现（Phase 2）

**4a. 运行 Baseline 训练**
- 按 `experiment-todo.md` Phase 2 执行
- 使用完整训练配置

**4b. 对比论文报告值**
- 复现目标：论文报告值 ±2%
- 如果偏差 > 2%，逐项排查：
  - Data preprocessing 差异（normalization、augmentation、tokenization）
  - Learning rate schedule（warmup、decay type、total steps）
  - Training epochs / steps（是否训练足够长）
  - 隐含 tricks（EMA、gradient clipping、label smoothing、dropout rate）
  - 随机种子影响（跑多个 seed 取均值）

**4c. 记录 Baseline 结果**
- 每个 baseline 写入 `Codes/_Results/baseline_<name>.md`：

```markdown
# Baseline: [Name]

## 来源
- 论文: [引用]
- 代码: [URL / 自行实现]
- Checkpoint: [是否使用预训练 / 从头训练]

## 复现结果
| 指标 | 论文值 | 复现值 | 差异 |
|------|--------|--------|------|
| [主指标] | [值] | [值] | [±%] |

## 复现状态: [成功 ±2% / 偏差较大 / 未完成]

## 复现难点记录
[遇到的问题、发现的隐含超参、与论文不一致之处]

## 公平比较保障
- [x] 相同 data loader
- [x] 相同 evaluation code
- [x] 相同 hardware config
- [ ] [其他需注意项]
```

Git commit：`baseline: reproduce [baseline_name] - [状态]`

### Step 5: 输出完整状态报告

在对话中显示以下格式的状态报告：

```
══════════════════════════════════════════════════════
  代码基线验证完成

  Sanity Checks:
    Overfit check .......... PASS
    Gradient check ......... PASS
    Shape check ............ PASS

  Pilot (Phase 1):
    判定: [Pass / Adjust / Fail]
    主指标: [值] (标准: [标准])

  Baseline 复现 (Phase 2):
    [baseline_1]: [指标] = [值] (论文: [值], 差异: ±[%])
    [baseline_2]: [指标] = [值] (论文: [值], 差异: ±[%])

  实验就绪。按 experiment-todo.md Phase 3+ 运行：
    cd Codes && bash scripts/run_main.sh
══════════════════════════════════════════════════════
```

### Step 6: Git 同步

```bash
cd <project_path>
git add Codes/
git commit -m "baseline: sanity + pilot + baseline reproduction complete"
git push origin main
```

## 验证标准

- [ ] Sanity check 全部通过（overfit / gradient / shape）
- [ ] Pilot 结果已写入 `_Results/pilot_result.md`，含 Pass/Adjust/Fail 判定
- [ ] 如果 Pilot Fail，已停止并报告用户
- [ ] 所有 baseline 适配到相同 data loader + evaluation code + hardware config
- [ ] Baseline 复现到论文值 ±2%（或已记录偏差原因）
- [ ] 所有结果已写入 `_Results/baseline_*.md`
- [ ] 状态报告已显示
- [ ] Git 同步完成

## 禁止事项

- 不修改核心模型代码（除非 sanity check 发现 bug）
- 不修改 `research/` 目录下的文档
- 不跳过 sanity check 直接跑 pilot
- Pilot Fail 时不继续 baseline 复现
- 不为了复现数字而修改 evaluation protocol（公平比较优先）
- 不自行决定跳过某个 baseline（用户决策）
