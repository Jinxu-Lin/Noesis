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

**DL 论文 LaTeX 最佳实践**：

#### 2.1 数学排版

- **行内公式 vs 独立公式**：简短变量引用用行内（`$x$`），重要公式用独立编号（`\begin{equation}`）。判断标准：如果后文需要引用这个公式，就用编号
- **多行公式对齐**：使用 `align` 环境，在 `=` 或关键运算符处对齐
  ```latex
  \begin{align}
    \mathcal{L} &= \mathcal{L}_{\text{task}} + \lambda \mathcal{L}_{\text{reg}} \\
                &= -\sum_{i} y_i \log \hat{y}_i + \lambda \|\theta\|_2^2
  \end{align}
  ```
- **条件定义**：使用 `cases` 环境
- **矩阵和向量**：向量用 `\mathbf{x}`（小写粗体），矩阵用 `\mathbf{W}`（大写粗体）。保持全文一致
- **常用数学算子**：使用 `\operatorname{}` 定义自定义算子（如 `\operatorname{softmax}`），避免斜体
- **上下标**：多字符下标用 `\text{}`（如 `x_{\text{query}}`），单字符用斜体（如 `x_i`）

#### 2.2 算法伪代码

- 使用 `algorithm2e` 或 `algorithmic` 包
- 伪代码应该在 abstraction level 和 detail level 之间取平衡——既能理解算法流程，又不至于变成代码列表
- **推荐格式**：
  ```latex
  \begin{algorithm}[t]
    \caption{Method Name}
    \label{alg:method}
    \KwIn{Input description}
    \KwOut{Output description}
    \For{each iteration $t = 1, \ldots, T$}{
      Step 1: Description\;
      $z \gets f_\theta(x)$\;
    }
  \end{algorithm}
  ```
- 算法中的变量名与正文公式保持一致
- 复杂方法建议放在 Method 节而非 Appendix——审稿人可能不看 Appendix

#### 2.3 表格规范

- **主结果表**：
  - 使用 `booktabs` 包（`\toprule`, `\midrule`, `\bottomrule`），不用 `\hline`
  - 最好结果**加粗**（`\textbf{}`），次好结果**下划线**（`\underline{}`）
  - 数字对齐（使用 `S` 列格式或手动保持小数点对齐）
  - 方法名左对齐，数字右对齐或居中
  - 如果表格太宽，使用 `\resizebox` 或 `\small`/`\footnotesize`
  - 分组：用 `\midrule` 分隔不同类别的方法（如 CNN-based / Transformer-based / Ours）
- **表格 caption 要自包含**：包含实验设置的关键信息（数据集、metric、是否 higher-is-better）
- **示例**：
  ```latex
  \begin{table}[t]
    \centering
    \caption{Main results on Dataset-X. Best in \textbf{bold}, second-best \underline{underlined}. $\uparrow$ means higher is better.}
    \label{tab:main}
    \begin{tabular}{l cc cc}
      \toprule
      Method & Metric-A $\uparrow$ & Metric-B $\uparrow$ \\
      \midrule
      Baseline-1 & 85.2 & 72.1 \\
      Baseline-2 & 86.7 & 73.5 \\
      \midrule
      \textbf{Ours} & \textbf{89.3} & \textbf{76.8} \\
      \bottomrule
    \end{tabular}
  \end{table}
  ```

#### 2.4 图表规范

- **图片格式优先级**：PDF > EPS > PNG（PDF 保留矢量，缩放不失真）
- **Figure 1 通常放在第一页或第二页**，使用 `\begin{figure*}` 双栏展示（如果是双栏模板）
- **子图使用 `subfigure` 或 `subcaption`**：
  ```latex
  \begin{figure}[t]
    \centering
    \begin{subfigure}[b]{0.48\linewidth}
      \includegraphics[width=\linewidth]{figures/fig_a.pdf}
      \caption{Description of (a)}
    \end{subfigure}
    \hfill
    \begin{subfigure}[b]{0.48\linewidth}
      \includegraphics[width=\linewidth]{figures/fig_b.pdf}
      \caption{Description of (b)}
    \end{subfigure}
    \caption{Overall description. (a) shows X. (b) shows Y.}
    \label{fig:example}
  \end{figure}
  ```
- **图表位置**：使用 `[t]`（top）或 `[t!]`，避免 `[h]`（容易导致排版混乱）。在正文中引用图表时，确保引用位置在图表出现之前或同一页
- **图中文字**：字体大小不小于正文字体的 80%，确保打印后仍可读
- **配色**：使用色盲友好的配色方案（如 ColorBrewer）。避免仅靠颜色区分——同时使用线型（实线/虚线/点线）或标记（圆/方/三角）

#### 2.5 引用格式

- **行内引用 vs 括号引用**：
  - "As shown by Smith et al. (2023)" → `\citet{smith2023}` 或 `Smith et al.~\cite{smith2023}`
  - "(Smith et al., 2023)" → `\citep{smith2023}` 或 `\cite{smith2023}`
- **多引用排序**：按年份升序 `\cite{a2020,b2021,c2023}`
- **自引**：如果双盲审稿，自引使用第三人称（"Previous work [X] showed..."而非"In our previous work [X]"）

#### 2.6 页面空间管理

- 8 页正文是硬限制（不含 references）。常用节省空间的技巧：
  - 表格使用 `\small` 或 `\footnotesize`
  - 长 equation 使用 `\small` 包裹
  - 非关键图表移到 Appendix（Supplementary Material）
  - 使用 `\vspace{-Xmm}` 微调垂直间距（谨慎使用）
- 不要为了省空间而删除重要内容——宁可移到 Appendix

### Step 3: 生成参考文献

产出 `Papers/latex/references.bib`：
- 从论文中提取所有引用
- 生成 BibTeX 格式
- 确保每个引用都有完整的作者、标题、会议/期刊、年份
- **引用格式注意**：
  - 会议论文：`@inproceedings{}`，包含 booktitle（会议全名）
  - 期刊论文：`@article{}`，包含 journal、volume、pages
  - 预印本：`@article{}`，journal 填 `arXiv preprint arXiv:XXXX.XXXXX`
  - BibTeX key 格式建议：`{作者姓}+{年份}+{标题首词}`（如 `vaswani2017attention`）
- **常见错误**：会议名缩写不一致、缺少页码、年份错误、作者名格式不统一

### Step 4: 图表处理

- 将 `Codes/` 中的实验图表复制或链接到 `Papers/latex/figures/`
- 确保图片格式兼容（PDF/EPS/PNG）
- 图表尺寸适配模板的 column width
- **实验图表质量检查**：
  - 坐标轴标签是否清晰且有单位？
  - Legend 是否完整？位置是否遮挡数据？
  - 字体大小是否与正文协调？
  - 分辨率是否足够（至少 300 DPI for raster images）？

### Step 5: 编译（如环境支持）

尝试编译 LaTeX：
```bash
cd Papers/latex && pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
```

如果编译环境不可用，标注在输出中，提示用户手动编译或使用 Overleaf。

**常见编译问题及修复**：
- `Undefined control sequence` → 检查是否缺少 package
- `Missing $ inserted` → 正文中的下划线或特殊字符需要转义
- `Float too large` → 图表超出页面，调整尺寸
- `Citation undefined` → 重新运行 bibtex
- `Overfull hbox` → 长公式或长单词导致溢出，手动断行

### Step 6: 格式检查

| 检查项 | 方法 |
|--------|------|
| 页数 | 是否符合目标会议要求？（正文 ≤ 8/10 页，references 不算） |
| 字体大小 | 模板默认字体是否正确？（不要手动改小字体来塞内容） |
| 边距 | 是否符合模板要求？（不要手动改边距） |
| 图表位置 | 是否在引用它们的文字附近？（不要出现"see Figure 3"但 Figure 3 在 3 页之后） |
| 参考文献格式 | 是否符合目标会议风格？ |
| 匿名化 | 如果双盲审稿，是否已去除作者信息？代码链接是否匿名化？是否有自引暴露身份？ |
| Appendix | 补充材料是否在正确的位置？（通常在 references 之后） |
| 超链接 | `\url{}` 和 `\href{}` 是否正常工作？ |

### Step 7: 提交前最终检查清单

| 检查项 | 状态 |
|--------|------|
| PDF 中所有公式正确渲染 | |
| 所有图表清晰可读（zoom 到 100% 检查） | |
| 所有交叉引用（\ref）正确 | |
| 所有引用（\cite）出现在参考文献中 | |
| 参考文献中无多余条目 | |
| 双盲审稿匿名化检查通过 | |
| 页数符合要求 | |
| Abstract 与正文数字一致 | |

## AI Co-Author 关键行为
- LaTeX 转换要**精确**——数学公式不能有任何错误
- 图表排版要考虑审稿人的阅读体验——Figure 1 在前两页，结果表紧跟分析文字
- 参考文献格式要**完整且一致**
- 如果编译失败，诊断错误并修复
- 提醒用户检查：匿名化、补充材料、代码/数据链接
- **排版美感**：好的排版让论文看起来更专业。注意表格对齐、公式间距、图文搭配
- **不牺牲内容换空间**：如果正文超页数，优先将非关键内容移到 Appendix，而非删除

## 输出
- `Papers/latex/main.tex` — LaTeX 源文件
- `Papers/latex/references.bib` — 参考文献
- `Papers/latex/figures/` — 图表文件
- `Papers/latex/main.pdf` — 编译后的 PDF（如编译成功）

## Exit Criteria
- [ ] `main.tex` 格式正确，符合目标模板
- [ ] 所有数学公式正确转换（符号与 notation.md 一致）
- [ ] 算法伪代码（如有）格式规范
- [ ] 表格使用 booktabs 风格，最佳结果加粗
- [ ] 参考文献完整（BibTeX 格式），无格式错误
- [ ] 图表已包含且位置合理（Figure 1 在前两页）
- [ ] 编译成功（或标注了编译问题）
- [ ] 格式检查通过（页数、边距、匿名化）
- [ ] 提交前最终检查清单全部通过
