# Skill: Implementation Planning (实验规划) — Phase R8

> **本阶段是纯规划阶段，不编写代码、不运行实验。** 产出 `Codes/` 目录后，进入人工编码阶段。

## 输入

- `research/method-design.md` — 方法的组件结构、核心机制、理论分析
- `research/experiment-design.md` — 实验体系（Dim 0-4）、baselines、metrics、数据集
- （可选）知识库中的 Experimental Patterns — 实验实施的经验模式

## 执行流程

### Step 1: 代码架构拆解

基于 `research/method-design.md` 的组件结构，设计代码模块划分：

1. **模块映射**：research/method-design.md 中的每个组件 → 对应的代码模块/文件
2. **接口定义**：每个模块的输入/输出类型、维度、数据流
3. **依赖分析**：模块间依赖关系、执行顺序
4. **代码起点评估**：
   - 是否有可复用的 baseline 官方代码？
   - 是否有成熟框架可接入（diffusers, timm, transformers 等）？
   - 从零实现 vs 基于现有代码扩展，各自的利弊

**核心原则：代码模块边界 = 方法组件边界。** 这样消融实验只需改配置，不改代码。

### Step 2: 实验方案细化

基于 `research/experiment-design.md`，将每个实验拆解为具体可执行的步骤：

1. **Dim 0 快速验证**：最优先、最小实验，验证核心假设
2. **Dim 1 核心验证**：主实验 + 消融 + 反事实
3. **Dim 2 应用价值**：下游任务实验
4. **Dim 3 效率验证**：计算成本分析
5. **Dim 4 科学发现**：探索性实验（如适用）

每个实验项需明确：
- 实验目的（对应哪个 RQ / 哪个组件）
- 所需代码模块（对应 code-todo.md 中的哪些项）
- 数据集和规模
- 评估指标
- 预期结果和通过标准
- 依赖关系（需要先完成哪些实验）

### Step 3: Baseline 复现方案

规划 baseline 复现策略：
- 哪些 baseline 有官方代码？代码质量如何？
- 复现的预期结果（论文报告的数值）
- 允许的偏差范围
- 复现失败的应对方案

### Step 4: 环境与工具规划

- Python 版本、核心依赖库、硬件需求
- 远程服务器配置（如需 GPU）
- 数据获取和预处理流程
- 版本控制策略（多 Agent 并行实验的分支方案，如需）

### Step 5: 建立 Codes/ 目录

在项目根目录下创建 `Codes/` 文件夹，生成三个核心文件：

#### 5.1 `Codes/code-todo.md`

细粒度的代码实现清单，按优先级排列：

```markdown
# Code TODO

## 阶段一：Dim 0 最小可行实现
- [ ] [模块名] — [功能描述]（对应 method-design 组件 X）
  - 输入：...
  - 输出：...
  - 关键点：...
- [ ] ...

## 阶段二：核心验证补全
- [ ] [消融变体实现]
- [ ] [额外 baseline 对比]
- [ ] ...

## 阶段三：完整实验支持
- [ ] [Dim 2-4 所需的额外代码]
- [ ] ...

## 工具与基础设施
- [ ] [评估 pipeline]
- [ ] [配置系统]
- [ ] [可视化/绘图]
```

#### 5.2 `Codes/experiment-todo.md`

细粒度的实验执行清单，按 Dimension 组织：

```markdown
# Experiment TODO

## Dim 0: 快速验证
- [ ] [实验名] — [目的]
  - 数据：...
  - 指标：...
  - 通过标准：...
  - 预计时间：...

## Dim 1: 核心验证
### 主实验
- [ ] ...
### 消融实验
- [ ] ...

## Dim 2: 应用价值
- [ ] ...

## Dim 3: 效率验证
- [ ] ...

## Dim 4: 科学发现（可选）
- [ ] ...

## Baseline 复现
- [ ] [Baseline 名] — 预期: [论文数值]
```

#### 5.3 `Codes/CLAUDE.md`

代码/实验阶段的专用指导文档，供人类与 AI 协作时使用：

```markdown
# CLAUDE.md — 代码与实验阶段

## 项目概述
[一句话描述本项目的核心方法和目标]

## 代码架构
[模块结构图、组件与 research/method-design.md 的映射]

## 环境配置
[Python 版本、依赖、硬件需求、远程服务器信息]

## 工作流程
1. 按 code-todo.md 顺序实现代码
2. 按 experiment-todo.md 顺序运行实验
3. 先完成 Dim 0 快速验证，通过后再推进后续

## 关键约束
[来自 research/method-design.md 和 research/experiment-design.md 的核心约束]

## 数据
[数据集路径、格式、预处理说明]

## 常用命令
[训练、评估、可视化的命令模板]
```

### Step 6: 更新 research/contribution.md

记录实验规划层面的贡献（如有新发现的实验设计创新）。

## AI Co-Author 关键行为
- code-todo.md 的颗粒度要细到「一个 Agent session 能完成一个 TODO 项」
- experiment-todo.md 的每个实验项必须可独立执行，不依赖于「上下文理解」
- Codes/CLAUDE.md 要写得让一个全新的 AI Agent 能直接上手，无需额外解释
- 主动识别代码实现中的技术风险点，在 code-todo.md 中标注
- 考虑代码复用——如果知识库中有类似实现的经验，引用之

## 输出
- `Codes/` 目录（含以下三个文件）
  - `Codes/code-todo.md`
  - `Codes/experiment-todo.md`
  - `Codes/CLAUDE.md`
- `research/contribution.md`（更新，如有）

## Exit Criteria
- [ ] 代码模块与 research/method-design.md 组件一一对应
- [ ] 每个 code-todo 项有明确的输入/输出定义
- [ ] code-todo 按优先级排列（Dim 0 → Dim 1 → ...）
- [ ] 每个 experiment-todo 项有通过标准和预期结果
- [ ] experiment-todo 项与 code-todo 项有交叉引用（实验需要哪些代码先完成）
- [ ] Baseline 复现方案完整
- [ ] Codes/CLAUDE.md 足以让全新 Agent 上手
- [ ] 环境配置需求已明确

