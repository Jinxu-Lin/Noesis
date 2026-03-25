---
description: "Praxis Paper Fill：将实验结果填入论文占位符"
---

# Skill: Praxis Paper Fill

## 触发

```
/praxis-paper-fill <project_path>
```

`<project_path>` 是研究项目的绝对路径。

---

## 说明

这是一个**独立工具命令**，不属于论文写作状态机（P1→P7）的任何阶段。可在以下场景使用：

- 论文用占位符模式写完（P2 阶段），实验结果后续产出，需要回填数据
- 实验迭代后结果更新，需要刷新论文中的数字和分析
- 多次增量运行：每次只填充新增的可用数据，已填充的不受影响

---

## 执行

1. 运行 `echo $HOME` 确定 `HOME_DIR`，推导 `NOESIS_ROOT = $HOME_DIR/Research/Noesis`。

2. 设置变量：
   ```
   PROMPT_FILE = $NOESIS_ROOT/Praxis/prompts/paper-fill-prompt.md
   PROJECT_PATH = <project_path>
   ```

3. 前置检查：
   - 确认 `$PROJECT_PATH/Papers/sections/` 目录存在且包含 `.md` 文件
   - 确认 `$PROJECT_PATH/Codes/_Results/` 目录存在且包含 `.md` 文件
   - 如果任一目录缺失或为空，向用户报告并退出：
     ```
     ⚠ Papers/sections/ 或 Codes/_Results/ 为空，无法执行 paper-fill。
     请确保论文章节和实验结果文件已就绪。
     ```

4. 读取 `$PROMPT_FILE` 的完整内容。

5. 构建 fork prompt：
   ```
   将 prompt 文件内容中所有 `<project_path>` 替换为实际的 $PROJECT_PATH。

   在 prompt 末尾追加实际的文件清单：

   ---
   ## 实际文件清单

   ### 论文章节
   {列出 $PROJECT_PATH/Papers/sections/ 下所有 .md 文件}

   ### 实验结果
   {列出 $PROJECT_PATH/Codes/_Results/ 下所有 .md 文件}

   ### 实验设计
   $PROJECT_PATH/research/experiment-design.md

   ### 论文大纲
   $PROJECT_PATH/Papers/outline.md
   ```

6. 使用 **Agent tool** 启动 fork agent：
   - `description`: `Paper Fill: 扫描占位符并填入实验结果 — {PROJECT_PATH}`
   - `prompt`: 上述构建的 fork prompt
   - `model`: `opus`

7. 等待 fork agent 完成。

---

## 完成后输出

读取 `$PROJECT_PATH/Papers/fill-report.md`，向用户展示总览部分：

```
✓ Paper Fill 完成！

📊 填充报告：
  - 占位符总数：N
  - 已填充：M
  - 仍待填充：K
  - 需人工审查：J

详细报告：$PROJECT_PATH/Papers/fill-report.md
```

根据结果给出建议：

- **全部填充完成**（K=0, J=0）：
  ```
  所有占位符已填充。建议运行 /praxis-paper 从 P3 开始审查完整论文：
    python3 $NOESIS_ROOT/Praxis/orchestrator/paper_state_machine.py init-phase <project_path> P3
    /praxis-paper <project_path>
  ```

- **有待填充项**（K>0）：
  ```
  仍有 K 个占位符未填充（缺少对应实验结果）。
  完成相关实验后，可再次运行 /praxis-paper-fill <project_path> 增量填充。
  ```

- **有审查项**（J>0）：
  ```
  有 J 个填充项需要人工审查（标记为 <!-- REVIEW -->）。
  请在论文中搜索 "REVIEW" 标记，逐一确认后删除标记。
  ```
