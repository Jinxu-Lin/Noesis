# Skill: Paper LaTeX Compilation (P6)

## Mission
Convert the complete paper to LaTeX, compile PDF, and pass all format checks for the target venue.

## Input
- `Papers/paper.md` -- complete paper (Markdown)
- `Papers/notation.md` -- notation table
- `Papers/outline.md` -- target venue info
- `Codes/_Results/` -- experiment figures and tables

## Step 1: Select LaTeX Template

Per `outline.md` target venue:
- NeurIPS -> `neurips_YYYY.sty`
- ICML -> `icml_YYYY.sty`
- ICLR -> `iclr_YYYY.sty`
- ACL/EMNLP -> `acl_YYYY.sty`
- Unspecified -> generic `article` class

Prompt user to download venue template to `Papers/latex/`. Fall back to basic article format if not provided.

## Step 2: Markdown to LaTeX Conversion

Convert `Papers/paper.md` to `Papers/latex/main.tex`.

Conversion mapping: sections -> `\section{}`/`\subsection{}`; math -> `\begin{equation}`/inline `$...$`; tables -> `\begin{table}`/`tabular`; figures -> `\begin{figure}`/`\includegraphics`; citations -> `\cite{}`; lists -> `\begin{itemize}`/`\begin{enumerate}`.

**Rules**: symbols per `notation.md`; figure/table numbers per `outline.md` plan; captions from section files; cross-references via `\label{}`+`\ref{}`.

### 2.1 Math Typesetting
- Inline for brief variable references (`$x$`); numbered `equation` for formulas referenced later
- Multi-line alignment with `align` at `=` or key operators
- Conditional definitions with `cases`
- Vectors: `\mathbf{x}` (lowercase bold); matrices: `\mathbf{W}` (uppercase bold) -- consistent throughout
- Custom operators via `\operatorname{}` (e.g., `\operatorname{softmax}`)
- Multi-character subscripts: `\text{}` (e.g., `x_{\text{query}}`); single-char: italic (`x_i`)

### 2.2 Algorithm Pseudocode
- Use `algorithm2e` or `algorithmic` package
- Balance abstraction and detail -- understandable flow, not a code listing
- Variable names match body formulas
- Place in Method section, not Appendix (reviewers may skip Appendix)

### 2.3 Tables
- `booktabs` package (`\toprule`, `\midrule`, `\bottomrule`); no `\hline`
- Best result **bold**, second-best underlined
- Numbers aligned (decimal point); methods left-aligned, numbers right-aligned/centered
- Group methods with `\midrule` separators
- Captions self-contained: include experiment setting, dataset, metric, direction (higher/lower is better)
- Use `\resizebox` or `\small`/`\footnotesize` for wide tables

### 2.4 Figures
- Format priority: PDF > EPS > PNG (vector preserves quality)
- Figure 1 on page 1 or 2; use `\begin{figure*}` for two-column templates
- Subfigures via `subfigure`/`subcaption` package
- Placement: `[t]` or `[t!]`; avoid `[h]`. Reference before or on same page as figure.
- Text in figures >= 80% of body font size
- Colorblind-friendly palette (ColorBrewer). Differentiate with line styles + markers, not color alone.

### 2.5 Citations
- Inline: `\citet{smith2023}` or `Smith et al.~\cite{smith2023}`
- Parenthetical: `\citep{smith2023}` or `\cite{smith2023}`
- Multiple citations sorted by year ascending
- Double-blind: use third person for self-citations

### 2.6 Page Space Management
- 8-page body is a hard limit (excluding references). Space-saving techniques:
  - `\small`/`\footnotesize` for tables/long equations
  - Move non-critical figures/tables to Appendix
  - `\vspace{-Xmm}` for fine-tuning (use sparingly)
- Never delete important content for space -- move to Appendix instead

## Step 3: Generate Bibliography

Produce `Papers/latex/references.bib`:
- Extract all citations from paper
- BibTeX format with complete author, title, venue, year
- Conference: `@inproceedings{}` with `booktitle` (full name)
- Journal: `@article{}` with `journal`, `volume`, `pages`
- Preprint: `@article{}` with `journal = {arXiv preprint arXiv:XXXX.XXXXX}`
- Key format: `{surname}{year}{title_keyword}` (e.g., `vaswani2017attention`)
- Common errors to avoid: inconsistent venue abbreviations, missing pages, wrong years, inconsistent author name format

## Step 4: Figure Processing

- Copy/link experiment figures from `Codes/_Results/` to `Papers/latex/figures/`
- Verify format compatibility (PDF/EPS/PNG)
- Fit figure dimensions to template column width
- Quality checks: axis labels clear with units? Legend complete and not occluding data? Font size consistent with body? Resolution >= 300 DPI for raster images?

## Step 5: Compile (if environment supports)

```bash
cd Papers/latex && pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
```

If compilation environment unavailable, note in output and suggest Overleaf.

**Common fixes**: `Undefined control sequence` -> missing package; `Missing $ inserted` -> unescaped special chars; `Float too large` -> resize figure; `Citation undefined` -> rerun bibtex; `Overfull hbox` -> manual line break in long formula/word.

## Step 6: Format Check

| Check | Target |
|-------|--------|
| Page count | Within venue limit (body <= 8/10 pages, references excluded) |
| Font size | Template default; no manual shrinking to fit content |
| Margins | Template default; no manual margin changes |
| Figure placement | Near referencing text; no 3-page gap |
| Reference format | Matches venue style |
| Anonymization | Double-blind: author info removed? Code links anonymized? Self-citations in third person? |
| Appendix | Correct position (after references) |
| Hyperlinks | `\url{}` and `\href{}` functional |

## Step 7: Pre-Submission Checklist

| Check | Status |
|-------|--------|
| All formulas render correctly in PDF | |
| All figures readable (100% zoom) | |
| All cross-references (`\ref`) correct | |
| All citations appear in bibliography | |
| No orphan bibliography entries | |
| Anonymization check passed | |
| Page count compliant | |
| Abstract numbers match body | |

## Key Behaviors
- **Exact** LaTeX conversion -- zero math formula errors
- Figure layout considers reviewer experience: Figure 1 on first two pages, result tables near analysis text
- **Complete and consistent** bibliography
- Diagnose and fix compilation failures
- Remind user to check: anonymization, supplementary material, code/data links
- **Typographic quality**: table alignment, formula spacing, text-figure balance
- **Never sacrifice content for space** -- move to Appendix if over page limit

## Output
- `Papers/latex/main.tex`
- `Papers/latex/references.bib`
- `Papers/latex/figures/` -- figure files
- `Papers/latex/main.pdf` (if compilation succeeds)

## Exit Criteria
- [ ] `main.tex` correct and matches target template
- [ ] All math formulas correctly converted (notation.md consistent)
- [ ] Algorithm pseudocode (if any) properly formatted
- [ ] Tables use booktabs; best results bolded
- [ ] Bibliography complete in BibTeX format; no format errors
- [ ] Figures included and positioned properly (Figure 1 on first two pages)
- [ ] Compilation successful (or issues documented)
- [ ] Format check passed (pages, margins, anonymization)
- [ ] Pre-submission checklist all passed
