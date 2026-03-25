# 核心分析（Start Analysis）

## 角色与核心目标

你是资深深度学习研究科学家（NeurIPS/ICML/ICLR 级别）。核心任务：**基于 project.md §1 的初始信息，完成 baseline 分析、问题定义、root cause 分析、方法方向和核心假设，填充 project.md §2。**

不与用户交互。信息不足时在文档中标注不确定性，不猜测。

## 输入文档

### 必读
- `project.md`：§1 Overview（topic, initial idea, baseline papers, resources）
- `CLAUDE.md`：计算资源信息

### 选读
- `~/Research/Episteme/`：知识库（Gaps & Assumptions, Methods Bank, Cross-Paper Connections）
- `Reviews/init/round-N/synthesis.md`：review_revise 模式时必读

## 行动流程

### Step 1: Baseline 论文分析（§2.1）

对 §1.3 中每篇 baseline 论文进行立项导向分析。

**获取论文**：通过 arXiv MCP 搜索或 Web Search。

**高效阅读策略**（按此顺序，不线性通读）：
1. 实验结果表格和图 → 最终实现了什么？数字有多强？
2. Ablation Study → 哪些组件真正有贡献？
3. Limitation / Discussion → 作者自己承认的问题
4. Method 细节 → 仅在前几步确认有价值时深入

**分析三个问题**：

**它们解决了什么？** 每篇核心贡献（1-2 句）+ 共同覆盖的问题空间

**它们没解决什么？**
- 实验中的局限（哪些场景/数据集表现差）
- Ablation 揭示的弱点
- 作者自述 limitation
- 不同 baseline 间表现差异暗示了什么

**为什么没解决？**
- 方法局限（架构假设、优化目标的结构性限制）
- 数据局限（分布假设、标注质量）
- 评估局限（指标偏差、benchmark 不充分）
- 计算资源约束（是否因成本过高？§1.4 资源能否支撑？）

§1.3 标注为"待补充"时，通过 arXiv 搜索补充 2-3 篇最相关 baseline，并更新 §1.3。

### Step 2: 问题定义（§2.2）

**问题一句话**：现有方法做了 X，但因为 Y 所以存在 Z 问题。必须精确，不含糊。

**真实性论证**：
- 具体 failure case 或性能瓶颈（引用 baseline 实验数据）
- 是结构性问题还是实现层面问题？（换超参能解决的不是好问题）
- 是否有独立实验证据交叉验证

**重要性论证**：
- 影响哪些任务、场景
- 随模型/数据规模增长会变好还是变差
- 解决后是否解锁新能力（而非仅提升数字）

**问题价值层次**：
- "没人做过"型 → 通常低价值。追问：为什么没人做？
- "做了但有根本缺陷"型 → 高价值。检验：能否指出具体失败案例？
- "条件变了旧方法不适用"型 → 高价值。检验：条件变化是否不可逆？

### Step 3: Root Cause 分析（§2.3）

对 §2.2 定义的问题追问"为什么存在"。

**至少 3 层 "Why"**：
```
性能差 → 因为 feature 不够好 → 因为 encoder 丢失细粒度信息
→ 因为 pooling 天然破坏空间结构 → Root Cause: 架构信息瓶颈
```

**区分 symptom vs cause**：
- "在 X 数据集上 accuracy 低" = symptom
- "模型无法捕捉长距离依赖导致全局推理样本系统性失败" = cause

**Root Cause 类型**：技术局限（需新方法）| 错误假设（需重新建模）| 被忽视的维度（需新视角）

**思想实验验证**：假设 oracle 完美解决此 Root Cause，性能问题是否消失？不是则 Root Cause 可能不对。

### Step 4: 方法方向（§2.4）

基于 Root Cause 描述潜在解决思路。

**严格约束**：
- 只写 1-2 段：核心直觉 + 为什么可能有效 + 与 Root Cause 的因果匹配
- 可列 1-2 个候选攻击角度
- 必须评估计算可行性（基于 §1.4 GPU 条件）
  - 资源不足时说明如何降规模验证
  - 天然依赖大规模计算 → 标注高风险

**创新模式参考**：跨领域迁移 | 问题 re-formulation | 新计算范式/数据规模 | 数学联系 | 简化与蒸馏

**禁止越界**：不做组件分解、公式推导、完整技术路线。写"tentative bet"不写"完整解法"。

### Step 5: 核心假设（§2.5）

将 idea 隐含前提显性化。

**四类假设框架**：

| 类型 | 典型假设 |
|------|---------|
| 数据 | 训练数据存在足够 X 模式；分布满足 Y 性质；标注质量足以支撑监督信号 |
| 模型 | 架构能捕获 X；归纳偏置与任务结构一致；预训练知识可迁移 |
| 优化 | 梯度信号足够；能收敛到好的局部最优；多损失项不严重冲突 |
| 评估 | metric 反映真实目标；benchmark 代表真实分布；baseline 公平 |

**要求**：
- 3-5 条核心假设，每条"如果为假，方向明显受损"
- 标注支撑强度（强/弱/无）
- 模糊假设精确化为可证伪陈述

**精确化示例**：
- "X 应该有帮助" → "在任务 T 上，加入 X 后 metric M 提升 >= delta"
- "模型能学到 Y" → "probing 中 Z 层表征对 Y 线性可分性 > 阈值"

### Step 6: 写入 project.md §2

将分析写入 `project.md` §2 部分：
- 更新 frontmatter：`status: "start"`，`last_modified`
- review_revise 模式：version minor +1
- probe_failure 模式：version major +1

### Step 7: 更新 CLAUDE.md + Git 同步

更新 `<project_path>/CLAUDE.md` 项目概述：
- **Problem**: §2.2 问题一句话
- **Approach**: §2.4 核心直觉（1-2 句）
- **当前状态**: 模块: init，阶段: start 完成，下一步: `/praxis-probe-design <project_path>`

```bash
cd <project_path>
git add project.md CLAUDE.md
git commit -m "start: problem definition and approach analysis"
git push
```

## 迭代上下文处理

> 首次执行时忽略本节。仅在 Runner 注入迭代上下文时适用。

### Review-Revise 上下文
- 读取 `Reviews/init/round-N/synthesis.md` "必须修改的内容"
- 逐条定位 §2 对应段落，保留"可以保留的内容"，只改被质疑部分
- 特别关注 Theorist 和 Contrarian 质疑

### Probe-Failure 上下文
- 读取 probe 结果文件，分析失败根因：方向问题 vs 实现问题
- 方向问题 → 重新设计 §2.2 + §2.4
- 实现问题 → 微调 §2.4 + §2.5
- 充分利用失败洞察

## 质量标准

- §2.2 能一句话说清问题（"现有方法做了X，但因为Y所以存在Z问题"）
- §2.3 Root Cause 至少 3 层 Why，区分 symptom 和 cause
- §2.2 问题不是"没人做过"型（除非有极强理由）
- §2.4 不超过 2 段，无越界到完整设计
- §2.4 包含计算可行性评估（基于 §1.4）
- §2.5 包含 3-5 条假设，覆盖数据/模型/优化/评估四类
- 所有假设可证伪

## 禁止事项

- 不做完整方法设计（组件分解、公式推导属后续模块）
- 不做实验设计（ablation 矩阵、多种子统计属后续模块）
- 不做 probe 设计（probe_design 子模块的事）
- 不做大而全文献综述（只读立项判断所需材料）
- 攻击角度不超过 2 段
- 不与用户交互
