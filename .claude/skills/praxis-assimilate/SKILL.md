---
description: "现有项目同化：将任意状态的科研项目纳入 Noesis 框架统一管理"
model: sonnet
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
---

# Skill: Praxis Assimilate

## 触发

```
/praxis-assimilate <project_path>
```

`<project_path>` 是现有研究项目的绝对路径。

---

## 说明

这是一个**交互式**工具。你将直接与研究者协作，不需要启动 fork agent。

现有项目可能处于任何状态：有论文无代码、有代码无方法文档、已发表、搁置中途……
本工具负责扫描分析、推断状态、与研究者确认，然后创建 Noesis 框架所需的结构文件，
使项目可以通过 `/praxis-research`、`/praxis-paper` 等命令统一管理。

---

## 执行

1. 运行 `echo $HOME` 确定 `HOME_DIR`，推导 `noesis_root = HOME_DIR/Research/Noesis`。
2. 读取 `<noesis_root>/Praxis/skills/assimilate-skill.md`。
3. **按照该 skill 文件的完整指令，逐步与研究者交互执行**，将 `<project_path>` 和 `<noesis_root>` 替换为实际路径。

---

## 完成后

告知研究者：

```
同化完成。项目已纳入 Noesis 框架。
查看当前状态：/praxis-status <project_path>
继续研究流程：/praxis-research <project_path>
```
