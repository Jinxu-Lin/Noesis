# Skill: Paper Sections Writing (P2)

## Mission
Write all paper sections following the outline, extracting and transforming content from research documents into academic prose.

## Placeholder Mode

When paper starts before experiments complete, use unified placeholder format for experiment-dependent content:

```
{{PENDING: <id> | <description> | <expected_range>}}
```

**Detection**: check `Codes/_Results/experiment_result.md`:
- **Exists** -> Full Mode: use real data
- **Missing** -> Placeholder Mode: experiment content uses `{{PENDING:...}}`

**Unaffected sections**: Method, Introduction (except key numbers), Related Work.
**Affected sections**: Experiments (tables/values/analysis), Abstract (key numbers), Conclusion (result references).

## Input
- `Papers/outline.md`, `Papers/notation.md`
- `research/problem-statement.md`, `research/method-design.md`, `research/experiment-design.md`
- `research/contribution.md`
- `project.md`
- `Codes/_Results/`

## Writing Mode Selection

Before starting, check if Codex MCP is available by attempting `codex-cli`:

**Mode A (Codex available)**: delegate drafts per `Praxis/prompts/codex-writer-prompt.md`, save to `Papers/sections/<section_id>-codex-draft.md`, then refine each (fix symbols, delete fabrications, fill `[RESULT:...]` from real data), save refined to `Papers/sections/<section_id>.md`. Proceed to Step 7.

**Mode B (Codex unavailable, non-blocking)**: write directly via Steps 1-6 below.

---

**Write strictly in the following order.** Each chapter produces a separate file in `Papers/sections/`.

## Step 1: Method (`Papers/sections/method.md`)

Write first because Method is the factual foundation. Introduction and Experiments depend on knowing exactly what we did.

- **Source**: `research/method-design.md` direct transformation
- **Structure**:
  1. **Overview / Problem Formulation** (0.5-1 page): big picture first. Define input/output, formalize the problem ($\text{Given } X, \text{find } Y \text{such that } Z$).
  2. **Component Details** (logical order, not code structure): each subsection = one component. Pattern: **Motivation** (1-2 sentences: why needed) -> **Design** (intuitive explanation) -> **Formulation** (math). Never drop a formula without explaining motivation first.
  3. **Training / Inference** (0.5 page): complete loss function, training procedure, inference procedure. Explicitly state training-inference differences (dropout, teacher forcing, etc.).
- **Math writing**:
  - Every formula has lead-in text ("We define the attention score as:")
  - Important formulas: numbered `\begin{equation}`; auxiliary: inline or `align`
  - Complex formulas followed by intuition ("Intuitively, this measures...")
  - Symbols defined at first use per `notation.md`
- Include Framework Figure description (elements and layout)
- **Do not invent methods** -- all content from `research/method-design.md`

## Step 2: Experiments (`Papers/sections/experiments.md`)

- **Source**: `research/experiment-design.md` + `Codes/_Results/`
- **Placeholder Mode** (`experiment_result.md` missing): Experimental Setup written normally. Remaining sections use table skeletons + `{{PENDING:...}}` values. Analysis sections use conditional frameworks ("If results match expectations, this indicates...").

**Structure** (argument order, not execution order):

1. **Experimental Setup** (0.5-1 page):
   - Datasets: name, scale, splits, preprocessing. Standard benchmarks: cite original + version.
   - Baselines: one sentence each with citation. Justify selection. Include recent 1-2 year SOTA.
   - Metrics: definition or citation. Explain non-standard metrics.
   - Implementation: key hyperparameters, hardware, training time. Details may go to appendix but main paper lists critical ones.

2. **Main Results** (1-1.5 pages):
   - Main table/figure for core comparison. Bold best, underline second-best.
   - Analyze patterns, not restate numbers ("The improvement is more pronounced on X, suggesting...")
   - Honestly discuss settings with no/weak improvement.

3. **Ablation Study** (0.5-1 page):
   - Each ablation validates one design choice. Order = importance order.
   - Analyze "why removing X causes Y% drop", not just report numbers.

4. **Analysis / Case Study** (0.5-1 page):
   - Visualization, error analysis, sensitivity analysis as space permits.
   - Show deep understanding of method behavior, not just "it works."

- **Principles**: every experiment states which claim it validates (per contribution.md); table/figure captions are self-contained; fair baseline comparison; no cherry-picking; report variance/std for stochastic experiments.

## Step 3: Introduction (`Papers/sections/intro.md`)

- **Source**: `research/problem-statement.md` + `research/contribution.md` + `project.md`
- **Paragraph structure** (~4-5 paragraphs, 1.5-2 pages with Figure 1):

  **P1: Define field and establish importance** (3-5 sentences). Define the task so non-experts understand. Establish importance. Do not start too broad ("Deep learning has transformed..."); cut directly to the specific area.

  **P2: Existing methods and their limitations -- Gap Setup** (4-6 sentences). Outline mainstream paradigms. Point out shared limitation = the Gap. Be specific ("existing methods assume X, but actually Y"). Use a concrete example if possible. Gap wording should naturally lead toward your method.

  **P3: "In this paper, we..." -- Contribution Statement** (3-5 sentences). One sentence for core idea (key insight). 1-2 sentences for high-level method description. Reference Figure 1 if appropriate.

  **P4: Contribution list**. Bullet points from `research/contribution.md`. Each: what was done + effect/significance. Every claim must have Experiments validation. Typically 3-4 items.

  **P5 (optional): Paper organization** (1-2 sentences).

- **Anti-patterns**: overly grand opening; vague gap ("have limitations"); over-promising ("we solve"); unverifiable contributions ("we provide insights").

## Step 4: Related Work (`Papers/sections/related_work.md`)

- **Source**: `project.md` + knowledge base (if available)
- **Function**: position our work in the landscape of existing research -- prove field awareness, prove novelty, help readers understand technical context.
- **Structure**: group by topic/technique, not chronology. Each group: arrange by technical evolution logic; end with 1-2 sentences on difference from our work.
- **Writing**: each cited work gets: what it did (1 sentence) + relation to ours (1 sentence). Do not over-disparage prior work. Address concurrent work explicitly. Final paragraph converges to "none addressed X, which is our entry point."
- **Completeness check**: recent 1-2 year coverage? Technique sources covered? Same-benchmark works covered?
- If material insufficient, annotate "directions needing supplementary reading" at file end.

## Step 5: Conclusion (`Papers/sections/conclusion.md`)

Structure (0.5-0.75 pages):

**Placeholder Mode**: key result numbers use `{{PENDING:...}}`; Limitations and Future Work unaffected.

**Summary** (3-5 sentences): not a repeat of Abstract. Pattern: what we did -> core finding/insight -> what experiments validated -> significance. Rephrase, do not copy Abstract.

**Limitations**: 2-3 honest limitations. Frame as conscious trade-offs ("We trade X for Y, which may limit..."). Common valid ones: compute cost, domain-specific assumptions, scaling behavior, edge cases.

**Future Work**: 1-3 concrete directions naturally extending limitations. Each 1-2 sentences.

## Step 6: Abstract (`Papers/sections/abstract.md`)

Written last -- full paper is now stable.

**Structure** (4-6 sentences, 150-250 words):
1. Problem (1 sentence): task + key limitation of existing methods
2. Method (1-2 sentences): what we propose + core idea
3. Results (1-2 sentences): key quantitative results
4. Significance (0-1 sentence): broader impact (optional)

**Placeholder Mode**: "achieves {{PENDING: main_acc | ...}} accuracy, outperforming the best baseline by {{PENDING: main_delta | ...}}"

Self-contained: no citations, no figure/table references. Use specific numbers, not "significantly improves."

## Step 7 (Optional): Cross-Section Consistency Review

If external AI MCP available, pass all 6 sections for cross-check: terminology consistency, narrative coherence, logic gaps, contribution alignment. Save to `Papers/sections/external-review.md`. Failure is non-blocking.

## Anti-Pattern Checklist (check after each section)

| Anti-Pattern | Fix |
|-------------|-----|
| Over-claiming ("significantly outperforms" but <2% gain) | Use specific numbers |
| Vague contribution ("a novel method" but no specifics) | State exact novelty |
| Missing limitations | Add Limitations subsection |
| Contribution inflation (listing "we ran experiments on X") | Only genuine innovations |
| Notation inconsistency | Strict adherence to notation.md |
| Broken logic chain (gap vs method motivation mismatch) | Verify Gap -> Method causality |
| Number recitation ("we achieve X%") | Analyze patterns and reasons |
| Over-disparaging prior work | Use neutral language |
| Missing variance reports | Report mean +/- std |

## Key Behaviors
- **Extract and transform** from research documents; do not create new content
- Cross-section **terminology consistency** (per notation.md)
- **Narrative consistency**: Introduction claims = Method content = Experiments validation
- Academic language: precise, concise, objective. No exaggeration.
- After each section, quick check against outline.md
- Each paragraph: topic sentence, argument development, transition. One topic per paragraph.
- Active voice preferred: "We propose" over "A method is proposed"

## Output

**Required (both modes)**:
- `Papers/sections/method.md`
- `Papers/sections/experiments.md`
- `Papers/sections/intro.md`
- `Papers/sections/related_work.md`
- `Papers/sections/conclusion.md`
- `Papers/sections/abstract.md`

**Mode A additional**: `Papers/sections/<section_id>-codex-draft.md` (6 drafts), `Papers/sections/codex-writer-summary.md`

**Optional (Step 7)**: `Papers/sections/external-review.md`

## Exit Criteria
- [ ] All 6 section files generated
- [ ] Symbols consistent with notation.md
- [ ] Every Introduction contribution has Experiments validation
- [ ] No fabricated content (all traceable to research documents)
- [ ] Section lengths roughly match outline.md plan
- [ ] Academic language; no exaggeration or subjective claims
- [ ] Anti-pattern checklist passed
- [ ] Every math formula has lead-in text and intuition
- [ ] Experiment analysis explains patterns, not restates numbers
