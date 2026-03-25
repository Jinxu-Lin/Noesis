# Code Skills 实施计划

> 目标：为 Research 模块的 implement 阶段设计 3 个编码子 skill + 1 个审查 skill，将"一锅煮"的代码实现拆分为可验证的分步流程。

---

## 1. 设计原则

**不改状态机**：4 个 skill 是 implement 阶段的辅助工具，不是新的 phase。用户可以选择用或不用。

**每步验证**：每个 skill 完成后必须通过验证测试才算成功。验证失败 → 自修复 → 重新验证。

**架构即 ablation**：核心模块边界 = 方法组件边界 = ablation 切割线。Config-driven 实验设计。

**AI 是 junior developer**：严格按 blueprint 的文件映射表实现，不自行发挥架构。

---

## 2. 四个 Skill 概览

```
/praxis-code-scaffold    搭骨架 + 实现核心模型组件
        ↓ 测试通过
/praxis-code-pipeline    实现数据 + 训练 + 评估 + 配置体系
        ↓ dry run 通过
/praxis-code-baseline    复现 baseline + sanity check + pilot
        ↓ 全部验证通过
实验就绪，用户按 experiment-todo.md 跑实验

/praxis-code-review      随时可调用：对照 blueprint 审查代码质量
```

---

## 3. Skill 1: `/praxis-code-scaffold`

### 黑盒定义

- **使命**：按 blueprint 的文件映射表，创建项目代码骨架并实现所有核心模型组件
- **输入**：`Codes/CLAUDE.md`（文件映射表 + 编码指南）、`research/method-design.md`（组件详情）、`Codes/probe/`（可复用代码）、`project.md` §1.4（GPU 约束）
- **输出**：`Codes/core/*.py`（全部核心组件）+ `Codes/tests/test_*.py`（验证测试，全部通过）
- **消费者**：`/praxis-code-pipeline`（在此基础上构建训练/评估）

### 步骤设计

**Step 1: 读取 Blueprint**
- 读 `Codes/CLAUDE.md` 的组件→文件映射表
- 读 `research/method-design.md` 每个组件的 §5（功能、I/O、因果论证、接口规格）
- 构建实现清单：每个文件要实现什么，依赖哪些其他文件

**Step 2: 评估 Probe 代码复用**
- 读 `Codes/probe/`，按 CLAUDE.md 的复用评估（直接复用 / 需重构 / 必须重写）
- 复用代码直接拷贝到 `Codes/core/`，标注来源

**Step 3: 按依赖顺序逐个实现组件**

对每个组件（按依赖拓扑序）：

```
3a. 读 method-design.md 对应 section
3b. 创建文件，顶部注释标注：
    # Component: [组件名]
    # Source: research/method-design.md §5.[N]
    # Ablation config key: model.use_[component_name]
3c. 实现代码（严格按接口规格，不自行发挥）
3d. 创建验证测试 Codes/tests/test_[component].py：
    - test_forward_shape: 输入输出 shape 正确
    - test_gradient_flow: 所有参数有梯度
    - test_output_range: 输出值范围合理（不是 NaN/Inf）
    - test_config_switch: config 关闭该组件后模型仍可运行（ablation 工程保障）
3e. 运行测试
3f. 失败 → 修复 → 重新测试，直到通过
3g. Git commit: "scaffold: implement [component_name]"
```

**Step 4: 集成验证**
- 组装完整模型（所有组件启用）
- 验证完整前向传播 + 反向传播
- 验证 GPU 显存在 §1.4 约束内（估算 vs 实际）

**Step 5: Git 同步**

### 验证标准
- 所有 `Codes/tests/test_*.py` 通过
- 每个组件可通过 config 独立开关（ablation ready）
- 完整模型前向+反向传播无报错
- 显存使用在 GPU 约束内

---

## 4. Skill 2: `/praxis-code-pipeline`

### 黑盒定义

- **使命**：在已实现的核心组件上构建完整的训练、评估和配置体系
- **输入**：`Codes/core/`（已实现）、`research/experiment-design.md`（实验规格）、`Codes/CLAUDE.md`（config 结构、日志系统）
- **输出**：训练脚本 + 评估脚本 + 所有 experiment configs + run scripts（dry run 全部通过）
- **消费者**：`/praxis-code-baseline`（用这些基础设施复现 baseline 和跑 pilot）

### 步骤设计

**Step 1: 实现数据 Pipeline**
- 读 experiment-design.md §9（数据集与计算规划）
- 实现 `Codes/core/data/` 或 `Codes/experiments/data/`：
  - 数据加载 + 预处理
  - Train/val/test split（如适用）
  - Data augmentation（如适用）
- 验证：加载一个 batch，打印 shape + 值范围 + 数据类型

**Step 2: 实现训练循环**
- 读 Codes/CLAUDE.md 的可复现性 checklist
- 实现 `train.py`（或 `Codes/experiments/<exp>/train.py`）：
  - Seed 全链路管理（torch/numpy/random/CUDA/dataloader worker）
  - Loss 计算（按 method-design.md 的 loss function 设计）
  - Optimizer + scheduler
  - Logging（wandb 或 tensorboard：loss, gradient norm, lr, GPU utilization）
  - Checkpointing（按 epoch / validation metric / 最多保留 N 个）
  - 支持 `--dry-run --max-steps 2`
  - 支持 `--resume` 从 checkpoint 恢复
- 验证：dry run 2 steps，loss 非 NaN，梯度非零

**Step 3: 实现评估脚本**
- 读 experiment-design.md §5（指标定义）
- 实现 `evaluate.py`：
  - 所有指标计算（主指标 + 辅助指标 + 效率指标）
  - 结果输出到 `Codes/_Results/<experiment_name>.md`
  - 自动对比表格生成（方法 vs baseline）
  - 支持 `--dry-run`（用 dummy 数据验证输出格式）
- 验证：dry run 输出格式正确

**Step 4: 创建 Config 体系**
- 读 experiment-design.md 的实验矩阵
- 创建 `Codes/configs/`:
  - `base.yaml`：默认配置（所有组件启用）
  - `ablation_no_<component>.yaml`：继承 base，关闭特定组件
  - `baseline_<name>.yaml`：baseline 配置
  - `pilot.yaml`：pilot 快速验证配置（小数据/少 epoch）
- 验证：每个 config 加载不报错 + dry run 不报错

**Step 5: 创建 Run Scripts**
- `Codes/scripts/run_pilot.sh`：运行 pilot 实验
- `Codes/scripts/run_baseline.sh`：运行所有 baseline
- `Codes/scripts/run_main.sh`：运行主实验
- `Codes/scripts/run_ablation.sh`：运行所有 ablation
- `Codes/scripts/run_all.sh`：按 experiment-todo.md 顺序全跑

**Step 6: Full Dry Run**
```bash
# 验证全链路
python train.py --config configs/base.yaml --dry-run --max-steps 2
python evaluate.py --config configs/base.yaml --dry-run
python train.py --config configs/ablation_no_X.yaml --dry-run --max-steps 2
python train.py --config configs/pilot.yaml --dry-run --max-steps 2
```

**Step 7: Git 同步**

### 验证标准
- 所有 config 加载无报错
- 所有 dry run 通过（训练 + 评估 + ablation configs）
- 评估输出格式正确（md 文件，含标准表格）
- ablation = 改 config 不改代码

---

## 5. Skill 3: `/praxis-code-baseline`

### 黑盒定义

- **使命**：复现 baseline 并运行集成测试（sanity check + pilot），确保实验基础设施可靠
- **输入**：`Codes/`（已实现）、`research/experiment-design.md` §4（baseline 规格）+ §2（pilot 规格）、`Codes/experiment-todo.md`（Phase 0-1）
- **输出**：baseline 实现 + sanity check 通过 + pilot 结果 + baseline 复现结果（全部写入 `_Results/`）
- **消费者**：用户（在此基础上按 experiment-todo.md Phase 2+ 跑实验）

### 步骤设计

**Step 1: Sanity Checks（Phase 0）**
- 按 experiment-todo.md Phase 0 逐项执行：
  - Overfit check：极小 batch → loss 接近 0
  - Gradient check：所有参数梯度非零
  - Shape check：无 shape mismatch
- 失败 → 定位 bug → 修复 → 重跑（这是代码 bug，不是方法问题）

**Step 2: Pilot 快速验证（Phase 1）**
- 按 experiment-todo.md Phase 1 执行：
  - 用 `configs/pilot.yaml` 运行
  - 对照 experiment-design.md §2.3 的 Pass/Adjust/Fail 标准
- 结果写入 `Codes/_Results/pilot_result.md`
- **如果 Fail**：报告给用户，建议回到 design 阶段。不继续 Phase 2

**Step 3: Baseline 获取与适配**
- 搜索/下载 baseline 官方代码
- 适配到我们的数据 pipeline 和评估协议（公平比较的工程保障）
- 确保与我们的方法共享：相同 data loader、相同 evaluation code、相同 hardware config

**Step 4: Baseline 复现（Phase 2）**
- 按 experiment-todo.md Phase 2 执行
- 复现目标：论文报告值 ±2%
- 如果复现困难，检查并记录：data preprocessing 差异、learning rate schedule、training epochs、tricks（EMA、gradient clipping）
- 结果写入 `Codes/_Results/baseline_<name>.md`

**Step 5: 输出完整状态报告**

```
══════════════════════════════════════════
  代码实现 + 集成验证完成

  Sanity checks: 全部通过 ✓
  Pilot: Pass / Adjust / Fail
  Baseline 复现: X / Y ±Z%

  实验就绪。按 experiment-todo.md Phase 3+ 运行：
    cd Codes && bash scripts/run_main.sh
══════════════════════════════════════════
```

**Step 6: Git 同步**

### 验证标准
- Sanity check 全通过
- Pilot 趋势符合预期
- Baseline 复现 ±2%
- 所有结果已写入 `_Results/`

---

## 6. Skill 4: `/praxis-code-review`

### 黑盒定义

- **使命**：对照 blueprint 和 method-design 审查代码实现的忠实度和质量
- **输入**：`Codes/`（当前代码）、`Codes/CLAUDE.md`（文件映射表）、`research/method-design.md`（组件规格）
- **输出**：审查报告（打印到对话 + 写入 `Codes/_Results/code_review.md`）
- **可随时调用**：不依赖特定阶段

### 审查维度

| 维度 | 检查内容 |
|------|---------|
| **架构忠实度** | 代码文件结构是否匹配 CLAUDE.md 的映射表？是否遵循深内核+浅包装？ |
| **组件忠实度** | 每个 core/ 文件是否忠实实现 method-design.md 的对应 section？ |
| **Ablation 工程** | 所有可 ablate 组件是否 config-driven？能否只改 config 跑 ablation？ |
| **DL 常见 Bug** | 数据泄漏？Shape broadcasting 异常？Loss reduction 模式错误？随机 seed 遗漏？ |
| **可复现性** | Seed 全链路管理？环境锁定？结果记录格式？ |
| **计算效率** | 有无不必要的 GPU 显存浪费？数据加载是否有 bottleneck？ |

---

## 7. 文件清单

### 新建

| 文件 | 类型 |
|------|------|
| `Praxis/prompts/code-scaffold-prompt.md` | Prompt |
| `Praxis/prompts/code-pipeline-prompt.md` | Prompt |
| `Praxis/prompts/code-baseline-prompt.md` | Prompt |
| `Praxis/prompts/code-review-prompt.md` | Prompt |
| `.claude/skills/praxis-code-scaffold/SKILL.md` | Skill |
| `.claude/skills/praxis-code-pipeline/SKILL.md` | Skill |
| `.claude/skills/praxis-code-baseline/SKILL.md` | Skill |
| `.claude/skills/praxis-code-review/SKILL.md` | Skill |

### 修改

| 文件 | 变更 |
|------|------|
| `Praxis/prompts/implement-prompt.md` | 在手动阶段指引中加入 3 个编码 skill 的用法说明 |
| `Praxis/prompts/blueprint-prompt.md` | 在 Codes/CLAUDE.md 产出规格中加入"编码 skill 将按此映射表实现" |

---

## 8. 实施顺序

```
1. 4 个 Prompt（核心内容，并行编写）
2. 4 个 Skill（薄 wrapper，并行创建）
3. 更新 implement-prompt 和 blueprint-prompt
4. Dry run 验证
```
