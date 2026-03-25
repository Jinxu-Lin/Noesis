# [项目名称]

> Claude 进入项目时先读本文件，再按需查阅具体文档。

## 项目概述

- **Topic**: [一句话：这个项目研究什么]
- **Problem**: [现有方法做了X，但因为Y所以存在Z问题 — init/start 完成后填入]
- **Approach**: [核心直觉，1-2 句 — init/start 完成后填入]
- **Target**: [目标会议/期刊 + DDL]

## 资源约束

- **GPU**: [类型 × 数量]
- **远程服务器**: [如有]
- **Timeline**: [DDL / 可用时间窗口]

> 所有分析、设计和实验规划必须在上述约束内。

## 当前状态

- **模块**: [init / research / paper]
- **阶段**: [当前阶段名]（[一句话描述]）
- **下一步**: [具体命令]

> 权威状态由 `Docs/*-module-status.json` 记录。本节仅供快速查阅。

## 关键文档

| 文档 | 说明 | 产出阶段 |
|------|------|---------|
| `project.md` | 项目介绍书（idea、问题、方法、假设、probe 设计、review） | Init |
| `Codes/_Results/probe_result.md` | 探针实验结果 | Init / probe_impl |
| `research/problem-statement.md` | 正式 Gap + RQ + 攻击角度 | Research / formalize |
| `research/method-design.md` | 方法设计（组件、公式、因果论证） | Research / design |
| `research/experiment-design.md` | 实验设计（baselines、ablations、metrics） | Research / design |
| `Codes/experiment-todo.md` | 实验执行清单（blueprint 产出） | Research / blueprint |
| `Codes/_Results/experiment_result.md` | 正式实验结果 | Research / implement |
| `research/retrospective.md` | 知识回收 | Research / retrospective |
| `Papers/` | 论文写作 | Paper module |

## Noesis 系统

- **路径**: `~/Research/Noesis`
- **状态文件**: `Docs/init-module-status.json`、`Docs/research-module-status.json`、`Papers/paper-status.json`
- **CLI 参考**: `~/Research/Noesis/Praxis/CLAUDE.md`

## 代码约束

- `Codes/core/` 深内核（可复用） | `Codes/experiments/` 浅包装（按实验）
- `Codes/_Data/` 生成数据（gitignore） | `Codes/_Results/` 实验结果（md，提交 Git）
- 外部数据: `~/Resources/Datasets/` 或 `~/Resources/Models/`
- **每次修改后 commit + push**
