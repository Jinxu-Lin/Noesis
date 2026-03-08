# Skill: Implementation Setup (代码环境搭建) — Phase 8 环境

## 触发场景
Phase 7 Experiment Review 判定 Pass，开始代码实现阶段的第一步：环境搭建。

## 输入
- `method-design.md` — 方法的组件结构
- `experiment-design.md` — 实验需求（数据集、baselines、metrics）
- （可选）知识库中的代码模式经验

## 执行流程

### Step 1: 选择代码起点

**不要从零开始写。** 按优先级搜索：

1. **Baseline 方法的官方代码** — 最优先
   - 保证评估公平（同一评估 pipeline）
   - 评估代码已就绪
   - 检查：代码质量、依赖完整性、文档

2. **同领域成熟框架** — 如 diffusers, timm, transformers 等
   - 社区维护、接口规范
   - 检查：方法实现是否适配框架的抽象

3. **相关方法的开源实现** — 最后选项
   - 检查：代码质量、star 数、最近维护时间

**选择标准**：
| 维度 | 检查项 |
|------|--------|
| 评估 pipeline | 是否完整？能否直接用于对比？ |
| 模块化 | 代码是否可扩展？能否方便地插入新组件？ |
| 文档 | 是否有清晰的使用说明和 API 文档？ |
| 社区 | 是否活跃维护？issue 响应速度？ |

### Step 2: 复现 Baseline（必须）

在写任何新代码之前，先用选定的代码库复现 baseline 的论文结果。
这一步验证了：
- 环境配置正确
- 数据处理正确
- 评估代码正确
- 训练流程正确

**如果连 baseline 都复现不了，后续所有实验结果都不可信。**

记录复现结果，与论文报告的数值对比。允许合理的偏差（不同硬件/随机种子），但大幅偏差必须排查。

### Step 3: 建立项目代码结构

```
[项目名]/
├── Code/
│   ├── CLAUDE.md                    ← 代码域入职手册
│   ├── code-todo.md                 ← 代码实现清单
│   ├── experiment-todo.md           ← 实验执行清单
│   ├── configs/                     ← 配置驱动实验
│   │   ├── method_full.yaml
│   │   ├── baseline_Y.yaml
│   │   └── ...
│   ├── src/
│   │   ├── methods/
│   │   │   ├── component_a.py       ← 对应 method-design.md 组件 A
│   │   │   ├── component_b.py       ← 对应 method-design.md 组件 B
│   │   │   └── pipeline.py          ← 组装各组件
│   │   ├── evaluation/              ← 评估 pipeline（尽量复用 baseline 的）
│   │   ├── data/                    ← 数据处理
│   │   └── utils/
│   ├── scripts/                     ← 运行脚本
│   └── experiments/                 ← 实验结果存储
```

**核心原则：代码模块边界 = 方法组件边界。**
这样消融实验就是改配置文件，而非改代码。

### Step 4: 填写 CLAUDE.md 的 Code/ 子节

项目 CLAUDE.md 中有一个 Code/ 子节，是 AI Co-Author 在代码域的入职手册。按 `templates/project-claude-md.md` 的结构填写，包含：
- 代码架构概览
- 组件与 method-design.md 的映射关系
- 环境配置（Python 版本、依赖、硬件需求）
- 常用运行命令
- 数据路径和格式说明

### Step 4.5: Git 多 Agent 并行实验准备（如需）

如果计划让多个 Agent 并行运行不同实验，在进入 Step 5 之前设置分支结构：

**同一机器多 Agent（Worktree）**:
```bash
# 主工作树负责 main 分支和协调
# 为每个并行实验 Agent 创建独立 worktree
git worktree add ../[项目名]-wt/exp-[名称] -b exp/[名称]
# 例如：
git worktree add ../my-paper-wt/exp-ablation-A -b exp/ablation-A
git worktree add ../my-paper-wt/exp-baseline-full -b exp/baseline-full
```

**跨服务器（Branch + Push）**:
```bash
# 各服务器分别 checkout 独立分支
git checkout -b exp/[名称] && git push -u origin exp/[名称]
```

**合并约定**：每个实验 Agent 只写 `experiments/[自己的目录]/` 和 `experiment-todo.md` 中对应的条目。合并时冲突仅在 `experiment-todo.md` 中出现，逐条 review 即可。

### Step 5: 初始化 code-todo.md 和 experiment-todo.md

**code-todo.md 第一轮**（仅 Dim 0 所需的最少代码）：
- [ ] 核心方法各组件实现
- [ ] 端到端 pipeline 组装
- [ ] 一个核心 baseline 的对比实现
- [ ] 基本评估（Dim 0 指定的 metrics）

**不写**：消融变体、完整评估 pipeline、额外 baseline

**experiment-todo.md 第一轮**（Dim 0 快速验证）：
- 按 experiment-design.md Dim 0 的 spec 生成具体实验项
- 每项包含：实验目的、运行命令、预期结果、通过标准

## 输出
- Code/ 目录结构（含基础代码）
- CLAUDE.md 的 Code/ 子节
- code-todo.md（第一轮，仅 Dim 0 所需）
- experiment-todo.md（第一轮，Dim 0 实验项）
- Baseline 复现结果记录

## Exit Criteria
- [ ] 代码起点已选定并记录选择理由
- [ ] Baseline 已复现，结果与论文接近
- [ ] CLAUDE.md 的 Code/ 子节 已建立
- [ ] 代码目录结构已搭建，组件边界清晰
- [ ] code-todo.md 第一轮已生成
- [ ] experiment-todo.md 第一轮已生成
- [ ] 如需多 Agent 并行：worktree 或分支结构已配置
- [ ] 初始代码结构已 commit + push

## 完成后
提交初始代码结构：
```bash
git add Code/ CLAUDE.md
git commit -m "phase/8: impl-setup — baseline reproduced, code scaffold ready"
git push origin main
```
提示用户：环境搭建完成，Baseline 已复现，建议进入 `/impl-validate` 开始核心实现与快速验证。
然后执行 `/reflect-pipeline` 对本阶段的流程进行反思，记录改进观察。
