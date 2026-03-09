---
description: "从已完成项目提取经验教训，注入全局 lessons"
model: opus
---

# Skill: Praxis 跨项目进化（Evolution）

## 触发

```
/praxis-evolve <project_path>
```

`<project_path>` 是已完成研究项目的绝对路径。通常在 Phase R11 Retrospective 完成后运行。

---

## 执行

1. 运行 `echo $HOME` 确定 `HOME_DIR`，推导 `noesis_root = HOME_DIR/Documents/Noesis`。
2. 读取 `<noesis_root>/Praxis/skills/evolve-skill.md`。
3. **按照该 skill 文件的完整指令，在当前对话中直接执行**，将 `<project_path>` 和 `<noesis_root>` 替换为实际路径。
