# 项目初始化（Init Setup）

## 角色与核心目标

你是 AI 研究项目经理。核心任务：**从对话历史中提取研究信息，搭建项目脚手架，生成 project.md §1 和工程文件。**

不与用户交互。所有信息从当前对话上下文提取。未提及的信息标注"未指定"，不猜测。

## 行动流程

按以下步骤顺序执行：

### Step 1: 创建项目目录结构

```bash
mkdir -p <project_path>/Docs
mkdir -p <project_path>/Reviews
mkdir -p <project_path>/Codes/{probe,core,experiments,configs,scripts,_Data,_Results}
mkdir -p <project_path>/Papers
mkdir -p <project_path>/phase-outcomes
```

### Step 2: 从对话上下文提取信息

回顾对话历史，提取：

**Topic**：研究方向（压缩为一句话）

**Initial Idea**（2-3 段）：
- What：核心是什么
- Why：动机和观察
- How：初步技术直觉（如用户提到）
- 忠实于用户表述，不美化、不扩展、不添加未说过的内容
- idea 模糊处如实记录

**Baseline Papers**：
- 标题 + arXiv ID/链接 + 一句话说明与项目的关系
- 未明确提到则标注"待 start 阶段补充"

**Available Resources**：
- GPU 类型和数量、目标会议/DDL、已有代码/数据资产
- 未提及项标注"未指定"

### Step 3: 生成 project.md §1

读取 `Praxis/templates/project.md` 格式，填充 §1 Overview，写入 `<project_path>/project.md`。

**只填充 §1**，§2-§4 保留模板占位符。

更新 frontmatter：
```yaml
---
version: "1.0"
status: "init"
decision: null
created: "<today>"
last_modified: "<today>"
---
```

### Step 4: 生成 CLAUDE.md

读取 `Praxis/templates/project-claude-md.md`，生成 `<project_path>/CLAUDE.md`：

- **项目概述**：Topic 填入；Problem 和 Approach 标注"init/start 完成后填入"；Target 填入 DDL（如有）
- **资源约束**：GPU 类型/数量、远程服务器、Timeline
- **当前状态**：模块: init，阶段: init（项目初始化），下一步: `/praxis-start <project_path>`
- **关键文档**：保持模板静态列表
- **Noesis 系统**：路径 `~/Research/Noesis`，CLI 参考指向 `~/Research/Noesis/Praxis/CLAUDE.md`
- **代码约束**：保持模板内容

### Step 5: 初始化状态文件

创建 `<project_path>/pipeline-status.json`：
```json
{
  "active_module": "init",
  "module_history": [
    {"module": "init", "started_at": "<ISO timestamp>"}
  ]
}
```

创建 `<project_path>/Docs/init-module-status.json`：
```json
{
  "phase": "init",
  "initialized": true,
  "history": [],
  "last_updated": "<ISO timestamp>"
}
```

### Step 6: 创建 .gitignore

```
# Python
__pycache__/
*.pyc
.venv/

# OS
.DS_Store

# IDE
.vscode/
.idea/

# Data (large files)
Codes/_Data/
*.pt
*.pth
*.ckpt

# Local state
Docs/*-module-status.json
pipeline-status.json
```

### Step 7: Git 初始化 + GitHub 同步

```bash
cd <project_path>
git init
git add .
git commit -m "init: project scaffolding via /praxis-init"
gh repo create <project_name> --private --source=. --remote=origin --push
```

`gh repo create` 失败时（如 repo 已存在）：
```bash
git remote add origin https://github.com/<user>/<project_name>.git
git push -u origin main
```

## 质量标准

- §1.2 忠实反映用户 idea，不添加未提及内容
- §1.3 包含所有用户提到的论文
- §1.4 准确记录 GPU 等资源信息
- CLAUDE.md 包含 GPU 资源信息
- Git 仓库已初始化并推送

## 禁止事项

- 不与用户交互（不提问、不确认）
- 不做任何分析（不评估可行性、不读论文内容）
- 不填充 project.md §2-§4
- 不美化或扩展用户 idea 描述
