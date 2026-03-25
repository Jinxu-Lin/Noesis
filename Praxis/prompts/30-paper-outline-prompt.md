# Skill: Paper Outline (P1)

## Mission
Map research documents to a paper structure with narrative spine, chapter plan, and figure/table layout.

## Input
- `project.md` -- background, motivation, target venue
- `research/problem-statement.md` -- Gap, RQ, root cause
- `research/method-design.md` -- method framework, causal reasoning
- `research/experiment-design.md` -- experiment plan
- `research/contribution.md` -- contribution list
- `Codes/_Results/` -- experiment results, figures

## Step 1: Audit Research Materials

Read all inputs. Build the following mappings before any planning.

**1.1 Result Availability Check**

Check `Codes/_Results/experiment_result.md`:
- **Exists (Full Mode)**: reference real data and numbers throughout
- **Missing (Placeholder Mode)**: paper started before experiments complete
  - Figure/Table plans define skeleton only (column/row names, expected trends), no values
  - Data source column in figure/table plan marked `{{PENDING}}`
  - Method, Introduction, Related Work unaffected
  - Experiments outline planned normally; material mapping annotated "data pending"

Also check `Codes/_Results/probe_result.md` -- probe results always available (Init Module complete); reference freely.

**1.2 Narrative Spine**

Build four tension nodes:
- **Gap**: an overlooked or unsolved fundamental problem
- **Insight**: a unique angle -- not brute force, but deep understanding of the problem essence
- **Method**: an elegant, self-consistent solution grounded in the insight
- **Validation**: experiments confirm both effectiveness and the core insight

Guiding question: **"If the reviewer remembers only one thing, what should it be?"** That is the key insight; the entire narrative orbits it.

**1.3 Material Inventory**: which content from each document maps to which paper section.

**1.4 Figure/Table Inventory**: existing figures in `Codes/_Results/` plus new figures needed.

## Step 2: Determine Venue and Paper Type

**2.1 Target Venue**

Check `project.md` for specified venue. If absent, mark TBD and plan for generic ML conference format (8-10 pages).

**2.2 Paper Type**

| Type | Method % | Experiments % | Core Selling Point |
|------|----------|--------------|-------------------|
| Method-Heavy | 40-45 | 30-35 | Novel method / theory elegance |
| Experiment-Heavy | 20-25 | 45-50 | Insights from large-scale experiments |
| Analysis Paper | 15-20 | 50-55 | Deep understanding of existing methods/phenomena |
| System Paper | 30-35 | 35-40 | System design + engineering contribution |

This determines space allocation and narrative emphasis in Step 3.

## Step 3: Writing Order and Narrative Strategy

**Writing order**: Method -> Experiments -> Introduction -> Related Work -> Conclusion -> Abstract

Rationale: Method is factual ground truth. Writing it first prevents Introduction from over-promising or under-setting-up.

**Narrative strategy** (choose one, state rationale in outline):
- **Contrastive**: show existing methods' shortcomings, then our solution. Best when clear baseline improvement exists.
- **Insight-driven**: present an overlooked observation, then build method on it. Best when a novel insight drives the work.
- **Problem-driven**: show failure cases, analyze root cause, propose solution. Best when addressing specific failure modes.

## Step 4: Generate Outline

Produce `Papers/outline.md` containing:

**4.1 Metadata**
- 2-3 candidate titles (strategy: method name + one-sentence core idea; <= 12 words; DL convention: verb phrase or "X: A Y for Z")
- Target venue, paper type, page limit, narrative strategy

**4.2 Chapter Outline**

For each section (Abstract, Introduction, Related Work, Method, Experiments, Conclusion):
- **Core argument**: 1-2 key messages
- **Material mapping**: source documents and specific sections
- **Space estimate**: percentage of total (per paper type from Step 2)
- **Subsection structure**: level-2 headings
- **Transition logic**: one sentence on how previous section leads into this one

Chapter-specific guidance:

- **Abstract**: written last. Note which sections supply its key numbers.
- **Introduction**: plan paragraph-level structure (typically 4-5 paragraphs), each with a clear function. Contribution list from `research/contribution.md`. Decide whether Figure 1 appears here.
- **Related Work**: group by topic (not chronology). Each group ends with differentiation from our work. May follow Method if method has high comprehension barrier.
- **Method**: decide if Preliminary/Background subsection is needed. Structure: Overview -> component details -> training/inference. Each design choice pairs with a motivation.
- **Experiments**: presentation order = argument order (main claim -> component validation -> deep analysis). Decide table vs figure for each experiment. Consider Case Study / Visualization / Error Analysis subsections.
- **Conclusion**: include Limitations (reviewers always check; honesty > avoidance) and Future Work (natural extension of limitations).

**4.3 Figure and Table Plan**

Principles:
- **Figure 1 (visual abstract)**: first thing reviewers see. Convey core idea in one figure -- method overview + key insight, or existing vs. ours comparison. High info density, not crowded.
- **Method figure**: all necessary components, color-coded modules, uniform data flow direction, loss attachment points annotated.
- **Experiment figures/tables**: tables for precise comparisons (main results); line/bar charts for trends (ablation, scaling); heatmaps/visualizations for qualitative analysis. Each has a clear takeaway.
- **Count guideline**: 8-page paper typically has 4-6 figures + 2-4 tables.

Plan table:

| ID | Type | Content | Takeaway | Data Source | Section |
|----|------|---------|----------|-------------|---------|
| Fig.1 | Concept | Visual abstract of core idea | ... | method-design.md | Intro/Method |
| Fig.2 | Framework | Architecture diagram | ... | method-design.md | Method |
| Tab.1 | Results | Main comparison | ... | `Codes/_Results/` or `{{PENDING}}` | Experiments |

**4.4 Narrative Consistency Check**

Build Contribution-Evidence alignment matrix:

| Contribution | Method Location | Experiment Location | Evidence Strength |
|-------------|----------------|--------------------|--------------------|
| C1: ... | S3.2 | Tab.1, Fig.4 | Quantitative + Qualitative |
| C2: ... | S3.3 | Tab.2 (ablation) | Quantitative |

Verify: no dangling contributions (claim without validation) and no dangling experiments (validation without claim).

## Step 5: Generate Notation Table

Produce `Papers/notation.md`:
- Unify all mathematical symbols and abbreviations across the paper
- Follow domain conventions: $\theta$ for parameters, $\mathcal{L}$ for loss, $\mathcal{D}$ for dataset; $x, y$ for input/output; $h, z$ for intermediate representations; script letters for sets; bold uppercase for matrices; bold lowercase for vectors
- Format: `| Symbol | Meaning | First Appearance |`

## Key Behaviors
- **Map** from research documents to paper structure; do not create from scratch
- Narrative spine must align with problem-statement -> method-design -> experiments logic chain
- Outline stage produces structure and material mapping only -- no prose
- Plan figures considering reviewer reading pattern: Abstract -> Figure 1 -> experiment tables -> decide whether to read carefully
- One insight permeates the entire paper: from Introduction motivation through every Method design choice to every Experiment validation
- Reference a comparable published top-venue paper for narrative strategy and space allocation

## Output
- `Papers/outline.md`
- `Papers/notation.md`

## Exit Criteria
- [ ] Narrative spine complete (Gap -> Insight -> Method -> Validation -> Contributions); core insight explicit
- [ ] Paper type determined; space allocation matches type
- [ ] Narrative strategy chosen with rationale
- [ ] Every contribution has argumentation and validation paths (Contribution-Evidence matrix done)
- [ ] Figure plan covers key results; Figure 1 function defined
- [ ] Notation table unified, unambiguous, follows domain conventions
- [ ] Chapter space allocation reasonable; inter-chapter transitions explicit
- [ ] Writing order planned (Method -> Experiments -> Introduction -> ...)
