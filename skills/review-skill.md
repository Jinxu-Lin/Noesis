# Skill: Review (通用审查框架)

> 本 Skill 是 Phase 3/5/7 的通用框架。具体审查维度和路由由配置文件决定。
> 核心原则：审查由**独立 SubAgent** 执行，消除确认偏误。

## 触发场景

前序工作 Phase 完成后，用户调用 `/review` 并指定审查类型：
- `/review gap` → 加载 `review-configs/gap-review.yaml`
- `/review method` → 加载 `review-configs/method-review.yaml`
- `/review experiment` → 加载 `review-configs/experiment-review.yaml`

## 执行流程

### Step 1: 加载配置

读取对应的配置文件，获取：
- `review_type`: 审查类型名称
- `phase_id`: 对应 Phase 编号
- `input_docs`: 需要传入 SubAgent 的文档列表
- `review_dimensions`: 审查维度及其核心问题与判定标准
- `output_doc`: 审查报告文件名
- `routing`: Pass/Revise/Block 的流向定义

### Step 2: 准备 SubAgent 输入

按配置的 `input_docs` 列表，读取项目目录中对应文档的完整内容。
将文档内容组装为 SubAgent 的输入上下文。

### Step 3: 生成 Review SubAgent

使用 Agent tool 生成独立子代理，传入：
1. **角色设定**（来自 `subagents/review-subagent.md` 模板）
2. **审查维度**（来自配置文件的 `review_dimensions`）
3. **待审查文档**（Step 2 收集的文档内容）
4. **输出格式要求**（审查报告结构）

关键：SubAgent 只接收文档内容，**不接收任何项目工作过程的记忆**。

### Step 4: 接收审查结果

SubAgent 返回审查报告，包含：
- 各维度判定 (Pass / Revise / Block)
- 逐条问题清单
- 贡献价值评估
- **整体判定: Pass / Revise / Block**

将审查报告写入项目目录的 `output_doc` 文件。

### Step 5: 根据判定路由

读取配置的 `routing`，根据整体判定执行：

**Pass**:
- 通知用户审查通过
- 提示下一步 Skill：`routing.pass.next_skill`

**Revise**:
- 通知用户需要修改
- 展示审查报告中的问题清单
- 提示用户调用：`routing.revise.next_skill`（迭代模式）

**Block**:
- 通知用户审查判定为 Block（方向性问题）
- 触发 Exit Assessment Gate SubAgent（传入 `subagents/exit-assessment-subagent.md`）
  - SubAgent 输入：当前所有项目文档 + 迭代历史
  - SubAgent 输出：Continue / Abandon + 理由
- 根据 Exit Assessment 结果：
  - **Continue** → 提示用户调用 `routing.block.continue_skill`
  - **Abandon** → 提示用户调用 `/retrospective`

## 输出
- 审查报告文档（文件名由配置决定）
- 审查判定 (Pass / Revise / Block)
- (Block 时) Exit Assessment Gate 的判定结果

## 注意事项
- **绝对禁止**主 Agent 直接执行审查——必须通过 SubAgent
- SubAgent 的角色是"Reviewer 2"——严格、挑剔、以审稿人视角
- 审查报告必须有具体问题，不能只给判定没有理由
- Block 判定必须经过 Exit Assessment Gate，不能直接跳到 Abandon
