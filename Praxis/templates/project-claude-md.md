# [项目名称]

> 项目入口文档。自动化运行器通过 Noesis 路径定位 Praxis orchestrator。

## 项目概览

- **一句话描述**: [本项目做什么]
- **目标会议/期刊**: [如有]
- **Noesis 路径**: `~/Research/Noesis`（跨机器自动适配，勿硬编码用户名）

## 当前状态

- **当前阶段**: [C/RS/P/D/RT/I/E/W/R] ([阶段名称])
- **执行模式**: 首次 / RS-Revise / Probe-Pivot / RT-Revise / Execute-Iterate / Execute-Pivot
- **下一步**: 运行 `/praxis-research <项目路径>` 继续自动化流程
- **阶段历史**: C ✓ → RS Pass → P signal → D ✓ → ...

> 阶段状态由 `pipeline-status.json` 权威记录，本节仅供人类快速查阅。

## 关键文档

按阅读优先级排列（AI 进入项目时按此顺序阅读）：

| 文档 | 状态 | 说明 |
|------|------|------|
| `project-startup.md` | | S — 项目知识基础 |
| `research/problem-statement.md` | | C — Gap + 攻击角度 + 探针方案 |
| `research/probe-results.md` | | P — 探针实验结果 |
| `research/method-design.md` | | D — 方法设计（含实验交叉引用） |
| `research/experiment-design.md` | | D — 实验设计（含方法交叉引用） |
| `research/contribution.md` | | 跨阶段 — 贡献跟踪 |
| `research/result.md` | | E — 实验结果与洞察（如有） |
| `iteration-log.md` | | 版本变更历史（如有） |

## 迭代记录

<!-- 由 iteration-log.md 记录完整历史，此处仅简要概览 -->
| 版本 | 触发 | 变更 | 日期 |
|------|------|------|------|
| | | | |

---

## Codes/ 子目录

> 以下内容在 I（实现规划）时填写。I 之前本节可留空。

### 代码架构

```
Codes/
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

| research/method-design.md 中的组件 | 代码文件 | 说明 |
|--------------------------|---------|------|
| Component A | `src/methods/xxx.py` | |
| Component B | `src/methods/yyy.py` | |

### 环境配置

**本地**：
```bash
# 依赖安装
# 数据准备
```

**远程服务器**（E 实验执行）：
```yaml
# 在项目根目录创建 env.json（已加入 .gitignore，每台机器独立配置）
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
- **重要**: 修改核心方法代码前，先读 research/method-design.md 中对应的理论部分

---

## Papers/ 子目录

> 以下内容在 W（论文写作）时填写。W 之前本节可留空。

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
