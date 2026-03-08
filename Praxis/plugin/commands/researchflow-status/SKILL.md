# Skill: ResearchFlow 项目状态查看器

## 触发

```
/researchflow:status <project_path>
```

---

## 执行步骤

### Step 1: 读取状态

```bash
python3 <researchflow_path>/orchestrator/state_machine.py status <project_path>
```

若 `pipeline-status.json` 不存在，改为：

```bash
python3 <researchflow_path>/orchestrator/state_machine.py next <project_path>
```

（会自动推断当前阶段）

### Step 2: 格式化输出

以清晰的 Markdown 表格展示以下信息：

```
## ResearchFlow 项目状态

**项目路径**：<project_path>
**当前阶段**：<phase> — <description>
**最后更新**：<last_updated>

### 阶段历史

| # | 阶段 | 结果 | 时间 |
|---|------|------|------|
| 1 | P1 — Project Startup | done | ... |
| 2 | P2 — Gap Discovery   | done | ... |
| ... |

### 各阶段迭代次数

| 阶段 | 迭代次数 |
|------|---------|
| P2   | 2       |
| P4   | 1       |

### 下一步

运行 `/researchflow:run <project_path>` 继续自动化流程。
或手动执行当前阶段的 Skill。
```

### Step 3: 补充文档检查

扫描项目目录，列出已存在的关键文档：

```
### 已产出文档

- [x] project-startup.md
- [x] gap-analysis.md
- [x] gap-review.md (Pass)
- [ ] method-design.md
- [ ] ...
```

对于审查文档，尝试读取其 `整体判定` 并标注 (Pass/Revise/Block)。
