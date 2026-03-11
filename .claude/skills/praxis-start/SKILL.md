---
description: "Praxis 项目启动：交互式研究种子孵化"
model: opus
---

# Skill: Praxis 项目启动

## 触发

```
/praxis-start <project_name>
```

---

## 执行

1. 运行 `echo $HOME` 确定 `HOME_DIR`，推导 `noesis_root = HOME_DIR/Research/Noesis`。
2. 读取 `<noesis_root>/Praxis/skills/startup-skill.md`。
3. **按照该 skill 文件的指令，在当前对话中直接与研究者交互执行**（无需 fork agent），将 `<project_name>` 和 `<noesis_root>` 替换为实际值。

关键点：
- 项目将创建在 `~/Research/<project_name>/`
- 整个过程是对话式的——需要研究者的输入和确认
- 如果研究者说"一起看 Episteme"，先读取 `~/Research/Episteme/kb-index.md` 了解知识库全貌

## 完成后

告知研究者：
```
Phase 1 完成。后续阶段由自动化运行器推进。
运行：/praxis-research ~/Research/<project_name>
```
