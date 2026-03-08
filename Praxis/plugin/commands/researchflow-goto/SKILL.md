# Skill: ResearchFlow 强制跳转

> 强制将状态机设置到指定阶段。用于：outcome 判断出错需手动纠正、人工决定回退或跳过某阶段。

## 触发

```
/researchflow:goto <project_path> <phase>
```

有效的 phase 值：`P1` `P2` `P3` `P4` `P5` `P6` `P7` `P8a` `P8a_validate` `P8b` `P9` `P11`

## 执行

```bash
python3 <researchflow_path>/orchestrator/state_machine.py init-phase <project_path> <phase>
```

若 `state_machine.py` 不支持 `init-phase` 命令，直接读取并修改
`<project_path>/pipeline-status.json` 的 `"phase"` 字段为目标 phase，保存文件。

输出确认：
```
✓ 强制跳转：当前阶段已设置为 <phase>
   运行 /researchflow:run <project_path> 继续。
```
