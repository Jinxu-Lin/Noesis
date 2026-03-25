---
description: "Praxis Code：Sanity check + Pilot 验证 + Baseline 复现"
---

# /praxis-code-baseline <project_path>

实现阶段的第三个编码子 skill：执行 sanity check（Phase 0）、pilot 快速验证（Phase 1）、baseline 复现（Phase 2），确保实验基础设施可靠。

## 变量

```
PROJECT_PATH = $ARGUMENTS
```

## 前提检查

1. 确认 `$PROJECT_PATH/Codes/` 存在且包含已实现的代码（core/、configs/、train.py 等）
2. 确认 `$PROJECT_PATH/Codes/experiment-todo.md` 存在
3. 确认 `$PROJECT_PATH/research/experiment-design.md` 存在

如果缺少前提文件，提示用户先完成前序步骤（`/praxis-code-scaffold` + `/praxis-code-pipeline`）。

## 执行

1. 运行 `echo $HOME` 确定 `HOME_DIR`，推导 `noesis_root = HOME_DIR/Research/Noesis`。
2. 读取 `<noesis_root>/Praxis/prompts/code-baseline-prompt.md`。
3. **按照该 prompt 的完整指令执行**，将 `<project_path>` 替换为 `$PROJECT_PATH`。
4. 完成后，显示状态报告：

```
══════════════════════════════════════════════════════
  代码基线验证完成

  Sanity Checks:
    Overfit check .......... [PASS/FAIL]
    Gradient check ......... [PASS/FAIL]
    Shape check ............ [PASS/FAIL]

  Pilot (Phase 1):
    判定: [Pass / Adjust / Fail]
    主指标: [值] (标准: [标准])

  Baseline 复现 (Phase 2):
    [baseline]: [指标] = [值] (论文: [值], 差异: ±[%])

  实验就绪。按 experiment-todo.md Phase 3+ 运行：
    cd Codes && bash scripts/run_main.sh
══════════════════════════════════════════════════════
```
