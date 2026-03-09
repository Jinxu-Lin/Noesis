# Skill: Paper LaTeX Compilation (LaTeX 编译) — Phase P6

## 触发场景
P5 终审通过（评分 ≥ 7.0），需要将论文转换为 LaTeX 格式并编译 PDF。

## 输入
- `Papers/paper.md` — 完整论文（Markdown）
- `Papers/notation.md` — 符号表
- `Papers/outline.md` — 目标会议/期刊信息
- `Codes/` — 实验图表

## 执行流程

### Step 1: 确定 LaTeX 模板

根据 `outline.md` 中的目标会议/期刊，选择对应的 LaTeX 模板：
- NeurIPS → `neurips_YYYY.sty`
- ICML → `icml_YYYY.sty`
- ICLR → `iclr_YYYY.sty`
- ACL/EMNLP → `acl_YYYY.sty`
- 未指定 → 使用通用 `article` 模板

**模板获取**：提示用户下载目标会议的模板文件到 `Papers/latex/` 目录。如果用户未提供，使用最基础的 LaTeX article 格式。

### Step 2: Markdown → LaTeX 转换

将 `Papers/paper.md` 转换为 `Papers/latex/main.tex`：

- 章节标题 → `\section{}`, `\subsection{}`
- 数学公式 → `\begin{equation}`, 行内 `$...$`
- 表格 → `\begin{table}`, `tabular`
- 图片 → `\begin{figure}`, `\includegraphics`
- 引用 → `\cite{}`
- 列表 → `\begin{itemize}` / `\begin{enumerate}`

**关键转换规则**：
- 所有符号按 `notation.md` 统一
- 图表编号与 `outline.md` 中的图表规划一致
- Caption 从 sections 文件中提取
- 交叉引用使用 `\label{}` + `\ref{}`

### Step 3: 生成参考文献

产出 `Papers/latex/references.bib`：
- 从论文中提取所有引用
- 生成 BibTeX 格式
- 确保每个引用都有完整的作者、标题、会议/期刊、年份

### Step 4: 图表处理

- 将 `Codes/` 中的实验图表复制或链接到 `Papers/latex/figures/`
- 确保图片格式兼容（PDF/EPS/PNG）
- 图表尺寸适配模板的 column width

### Step 5: 编译（如环境支持）

尝试编译 LaTeX：
```bash
cd Papers/latex && pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
```

如果编译环境不可用，标注在输出中，提示用户手动编译或使用 Overleaf。

### Step 6: 格式检查

| 检查项 | 方法 |
|--------|------|
| 页数 | 是否符合目标会议要求？ |
| 字体大小 | 模板默认字体是否正确？ |
| 边距 | 是否符合模板要求？ |
| 图表位置 | 是否在引用它们的文字附近？ |
| 参考文献格式 | 是否符合目标会议风格？ |
| 匿名化 | 如果双盲审稿，是否已去除作者信息？ |

## AI Co-Author 关键行为
- LaTeX 转换要**精确**——数学公式不能有任何错误
- 图表排版要考虑审稿人的阅读体验
- 参考文献格式要**完整且一致**
- 如果编译失败，诊断错误并修复
- 提醒用户检查：匿名化、补充材料、代码/数据链接

## 输出
- `Papers/latex/main.tex` — LaTeX 源文件
- `Papers/latex/references.bib` — 参考文献
- `Papers/latex/figures/` — 图表文件
- `Papers/latex/main.pdf` — 编译后的 PDF（如编译成功）

## Exit Criteria
- [ ] `main.tex` 格式正确，符合目标模板
- [ ] 所有数学公式正确转换
- [ ] 参考文献完整（BibTeX 格式）
- [ ] 图表已包含且位置合理
- [ ] 编译成功（或标注了编译问题）
- [ ] 格式检查通过

