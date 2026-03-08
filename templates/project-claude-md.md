# [项目名称]

> AI Co-Author 进入项目时的第一份文档。读完本文件后，再读 `pipeline.md` 了解完整方法论。

## 项目概览

- **一句话描述**: [本项目做什么]
- **目标会议/期刊**: [如有]
- **ResearchFlow 路径**: `[ResearchFlow 中央仓库的绝对路径]`

## 当前状态

- **当前阶段**: Phase [X] ([阶段名称])
- **执行模式**: 首次 / P[Y] Revise 迭代 / P8 L[N] 迭代
- **下一步 Skill**: `/[skill-name]`
- **阶段历史**: P1 ✓ → P2 ✓ → P3 Pass → P4 ✓ → ...

> 每次阶段转换时更新本节。如果本节信息缺失，参照 `pipeline.md` "阶段判断：快速定位表"，根据已存在的文档推断当前阶段。

## 关键文档

按阅读优先级排列（AI 进入项目时按此顺序阅读）：

| 文档 | 状态 | 说明 |
|------|------|------|
| `pipeline.md` | ✓ | 方法论参考（完整 Pipeline 定义） |
| `project-startup.md` | | Phase 1 — 项目知识基础 |
| `gap-analysis.md` | | Phase 2 — 研究空白与研究问题 |
| `method-design.md` | | Phase 4 — 方法设计与理论 |
| `experiment-design.md` | | Phase 6 — 实验方案（含结果） |
| `contribution.md` | | 跨阶段 — 贡献跟踪 |
| `iteration-log.md` | | 迭代历史（如有） |

## 迭代记录

<!-- 如果项目经历了迭代，在此简要记录 -->
| 轮次 | 级别 | 原因摘要 | 结果 |
|------|------|---------|------|
| | | | |

---

## Code/ 子目录

> 以下内容在 Phase 8 (`/impl-setup`) 时填写。Phase 8 之前本节可留空。

### 代码架构

```
Code/
├── configs/           ← 实验配置（配置驱动实验）
├── src/
│   ├── methods/       ← 核心方法实现
│   ├── evaluation/    ← 评估 pipeline
│   ├── data/          ← 数据处理
│   └── utils/         ← 工具函数
├── scripts/           ← 运行脚本
└── experiments/       ← 实验结果
```

### 方法组件 → 代码映射

| method-design.md 中的组件 | 代码文件 | 说明 |
|--------------------------|---------|------|
| Component A | `src/methods/xxx.py` | |
| Component B | `src/methods/yyy.py` | |
| 整体 Pipeline | `src/methods/pipeline.py` | 组装各组件 |

### 环境配置

```bash
# 依赖安装
# 数据准备
```

### 运行命令

```bash
# 训练
# 评估
# 消融
```

### 开发约定

- **配置管理**: [yaml / hydra / argparse]
- **实验结果**: 存储在 `experiments/[实验名]/[日期]/`
- **重要**: 修改核心方法代码前，先读 method-design.md 中对应的理论部分

### 关键实现决策记录

| 决策 | 原因 | 对应 method-design.md 章节 |
|------|------|--------------------------|
| | | |

---

## Papers/ 子目录

> 以下内容在 Phase 9 (`/paper-writing`) 时填写。Phase 9 之前本节可留空。

### 论文结构

```
Papers/
├── main.tex
├── figures/
└── ...
```

### 写作约定

- **目标格式**: [会议/期刊模板]
- **参考文献管理**: [BibTeX 文件路径]
- **图表编号约定**: [如有]
