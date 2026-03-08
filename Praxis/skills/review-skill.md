# Skill: Review (通用审查框架)

> 本 Skill 是 Phase 3/5/7 的通用框架。具体审查维度和路由由配置文件决定。
> 核心原则：审查由**独立 SubAgent** 执行，消除确认偏误。
>
> **2026-03 更新**：借鉴 Sibyl System 的多视角辩论机制，引入可选的"挑战者"并行 SubAgent，
> 以及 Comparativist 的竞争工作在线核查能力。P7 默认启用双 SubAgent 结构。

## 触发场景

前序工作 Phase 完成后，用户调用 `/review` 并指定审查类型：
- `/review gap` → 加载 `review-configs/gap-review.yaml`
- `/review method` → 加载 `review-configs/method-review.yaml`
- `/review experiment` → 加载 `review-configs/experiment-review.yaml`

## 配置字段说明

配置文件除原有字段外，新增可选字段：
- `challenger_enabled`: true/false — 是否启用并行"挑战者" SubAgent（P7 默认 true）
- `comparativist_search`: true/false — 是否在审查前执行竞争工作在线核查（P3 默认 true）

## 执行流程

### Step 1: 加载配置

读取对应的配置文件，获取所有字段，包括：
- `challenger_enabled`: 是否启用挑战者 SubAgent
- `comparativist_search`: 是否执行竞争工作搜索
- 其余原有字段（见各 yaml 配置）

---

### Step 2: 准备 SubAgent 输入

按配置的 `input_docs` 列表，读取项目目录中对应文档的完整内容。
将文档内容组装为 SubAgent 的输入上下文。

**2a. 竞争工作核查（当 `comparativist_search: true`）**

在组装文档之前，执行一次在线文献搜索：

1. 提取审查文档中的研究方向关键词（2-3个最具代表性的术语）
2. 使用 WebSearch 搜索：`"[关键词] arxiv 2024 2025"` + `"[关键词] site:arxiv.org"`
3. 扫描搜索结果，寻找**直接竞争工作**（解决同一问题的）：
   - 如发现，记录：标题、发表时间、核心方法、与本项目的关键差异
   - 如未发现，记录搜索范围和结论
4. 将竞争工作核查结果作为额外上下文注入 SubAgent 输入，格式：
   ```
   ## 竞争工作核查（Comparativist 视角）
   搜索范围：[搜索词]
   发现：[无竞争工作 / 发现以下工作：...]
   ```

**注意**：搜索结论由 SubAgent 自己分析判断，主 Agent 只负责提供原始搜索结果。

---

### Step 3: 生成审查 SubAgent

**3a. 主审查 SubAgent（所有配置均执行）**

使用 Agent tool 生成独立子代理，传入：
1. **角色设定**（来自 `subagents/review-subagent.md` 模板）
2. **审查维度**（来自配置文件的 `review_dimensions`）
3. **待审查文档**（Step 2 收集的文档内容）
4. **竞争工作核查结果**（如 Step 2a 执行，则包含）
5. **输出格式要求**（见 review-subagent.md）

关键：SubAgent 只接收文档内容，**不接收任何项目工作过程的记忆**。

**3b. 挑战者 SubAgent（当 `challenger_enabled: true`）**

与 3a **并行启动**（同一个 Agent tool 调用中的第二个 SubAgent）。

使用 Agent tool 生成第二个独立子代理，传入：
1. **角色设定**（来自 `subagents/challenger-subagent.md` 模板）
2. **待审查文档**（与 3a 相同的文档内容）
3. **特殊指令**：专注寻找 Block 级别问题，不负责综合判定

两个 SubAgent 互不知晓对方的存在。

---

### Step 4: 接收审查结果并合并

**4a. 仅主审查 SubAgent（`challenger_enabled: false`）**

主审查 SubAgent 返回审查报告，包含：
- 各维度判定 (Pass / Revise / Block)
- 逐条问题清单
- 战略预判（新增）
- **整体判定: Pass / Revise / Block**

将审查报告写入项目目录的 `output_doc` 文件。

**4b. 双 SubAgent 合并（`challenger_enabled: true`）**

等待两个 SubAgent 均完成后，由**主 Agent**（非新 SubAgent）执行以下合并逻辑：

1. 读取主审查报告和挑战者报告
2. 执行合并决策（下方逻辑）
3. 生成最终审查报告写入 `output_doc`

**合并决策逻辑：**

```
整体判定 = MAX(主审查整体判定, 挑战者最严重发现的对应判定)

合并规则：
- 挑战者提出 Block 级问题 → 整体至少 Block（即使主审查判 Pass/Revise）
- 挑战者提出 Revise 级问题（主审查判 Pass）→ 整体升级为 Revise，将挑战者问题纳入问题清单
- 主审查判 Block、挑战者未发现 Block 问题 → 整体仍为 Block（主审查优先，挑战者负责发现额外问题）
- 两者均 Pass → 整体 Pass，在报告中注明"挑战者未发现额外 Block 级问题"
```

**最终报告结构**（双 SubAgent 模式）：
```markdown
## 主审查报告（摘要）
[主审查维度判定摘要]

## 挑战者报告（摘要）
[挑战者发现的问题列表]

## 综合判定
[合并后的最终判定和理由]

[完整的各维度分析、问题清单、战略预判]
```

---

### Step 5: 根据判定路由

读取配置的 `routing`，根据整体判定执行：

**Pass**:
- 通知用户审查通过
- 提示下一步 Skill：`routing.pass.next_skill`
- 展示战略预判中的"风险预警"（即使 Pass，也让研究者知道潜在风险）

**Revise**:
- 通知用户需要修改
- 展示审查报告中的问题清单（区分来自主审查 vs 挑战者）
- 提示用户调用：`routing.revise.next_skill`（迭代模式）

**Block**:
- 通知用户审查判定为 Block（方向性问题）
- 触发 Exit Assessment Gate SubAgent（传入 `subagents/exit-assessment-subagent.md`）
  - SubAgent 输入：当前所有项目文档 + 迭代历史 + **战略预判中的候选方向**
  - SubAgent 输出：Continue / Abandon + 理由
- 根据 Exit Assessment 结果：
  - **Continue** → 提示用户调用 `routing.block.continue_skill`
  - **Abandon** → 提示用户调用 `/retrospective`

## 输出
- 审查报告文档（文件名由配置决定，含战略预判章节）
- 审查判定 (Pass / Revise / Block)
- (Block 时) Exit Assessment Gate 的判定结果

## 注意事项
- **绝对禁止**主 Agent 直接执行审查——必须通过 SubAgent
- 双 SubAgent 模式下，**合并决策由主 Agent 执行**，不需要第三个 SubAgent
- 挑战者 SubAgent 的角色是"专职刁难者"——只找 Block，不综合判定
- 竞争工作核查的搜索应聚焦于直接竞争（解决同一问题），不是泛泛的相关工作
- Block 判定必须经过 Exit Assessment Gate，不能直接跳到 Abandon
- **Pass 不等于完美**——战略预判章节在 Pass 情况下同样重要

## 完成后
执行 `/reflect-pipeline` 对本阶段的流程进行反思，记录改进观察。
