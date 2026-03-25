---
description: "Praxis Probe Impl：探针实验代码实现 + Dry Run 验证"
---

# /praxis-probe-impl <project_path>

运行 Init Module 的 probe_impl 子模块：编写探针实验代码并通过 dry run 验证。

## 变量

```
PROJECT_PATH = $ARGUMENTS
RUNNER = ~/Research/Noesis/Praxis/orchestrator/init_runner.py
SM = ~/Research/Noesis/Praxis/orchestrator/init_state_machine.py
```

## 前提检查

当前阶段必须是 `probe_impl`。检查：

```bash
python3 $RUNNER status $PROJECT_PATH
```

如果当前 phase 不是 `probe_impl`，使用 `init-phase` 强制设置：
```bash
python3 $SM init-phase $PROJECT_PATH probe_impl
```

## 执行

### Step 1: 获取动作

```bash
python3 $RUNNER next $PROJECT_PATH
```

### Step 2: 执行 Fork Agent

使用 Agent tool：
- `description`: JSON 中的 `description`
- `prompt`: JSON 中的 `fork_prompt`
- `model`: `opus`

### Step 3: 推进状态机

```bash
python3 $RUNNER advance $PROJECT_PATH
```

解析结果并显示：

- 如果 `outcome == "done"`：

  ```
  ✓ Probe 代码就绪，dry run 通过。Init Module 完成。

  下一步：运行探针实验
    cd $PROJECT_PATH/Codes/probe
    bash run_probe.sh

  结果将输出到：
    Codes/_Results/probe_result.md   （报告）
    Codes/_Results/probe_result.json （数据）
  结果解读：参考 project.md §3.4（Pass/Marginal/Fail 标准）
  ```

- 如果 `outcome == "infeasible"`：

  ```
  ⚠ Probe 设计不可行，回到 probe_design 重新设计。
  原因: {notes}

  运行 /praxis-probe-design $PROJECT_PATH 重新设计验证方案
  或运行 /praxis-init-auto $PROJECT_PATH 自动继续流程
  ```
