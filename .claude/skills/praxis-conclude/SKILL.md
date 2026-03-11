---
description: "Praxis 编码总结：快速验证失败后总结并重启研究"
model: sonnet
---

# Skill: Praxis 编码阶段总结

## 触发

```
/praxis-conclude <project_path>
```

`<project_path>` 是研究项目的绝对路径。

---

## 执行

1. 运行 `echo $HOME` 确定 `HOME_DIR`，推导 `noesis_root = HOME_DIR/Research/Noesis`。
2. 读取 `<noesis_root>/Praxis/skills/conclude-skill.md`。
3. **按照该 skill 文件的完整指令，在当前对话中直接与研究者交互执行**（无需 fork agent），将 `<project_path>` 和 `<noesis_root>` 替换为实际路径。
