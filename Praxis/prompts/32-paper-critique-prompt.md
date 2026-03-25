# Skill: Paper Cross-Review Critique (P3)

## Mission
Independently critique the full paper draft from 5 reviewer perspectives, producing actionable issue lists and a prioritized summary for P4 editing.

## Input
- `Papers/sections/` -- all section files
- `Papers/outline.md`, `Papers/notation.md`
- `research/contribution.md`, `research/method-design.md`, `research/experiment-design.md`

## Step 1: Assemble Full Paper

Concatenate sections in order from `Papers/sections/`. Read and understand the complete draft.

## Step 2: Execute 5-Role Review

Review the full paper independently from each role below. Use `Praxis/subagents/paper-critic-subagent.md` as the review template.

### Role 1: Novelty Critic

**Persona**: senior researcher with 20+ publications, deep knowledge of the field's technical lineage. Novelty = "provides new understanding or capability", not just "nobody did this exact thing."

**Dimensions**:
- **Incremental vs fundamental**: simple combination (A+B) or insight-driven innovation? If combination, what insight justifies it?
- **Differentiation from closest prior work**: identify 1-3 most similar published works. Is the difference technically substantial and empirically meaningful?
- **Related Work completeness**: missing competitors (especially recent 6 months)? Missing technique origins? Selective citation?
- **Honesty of novelty claims**: "first to..." -- really first? Claim strength matches actual innovation?

### Role 2: Soundness Critic

**Persona**: theory-oriented researcher who finds holes in logic chains and math derivations.

**Dimensions**:
- **Reproducibility from description alone**: can a PhD student reimplement without seeing code? Any hand-waved steps?
- **Math correctness**: derivation gaps? Hidden assumptions? Gradient flow through non-differentiable ops addressed?
- **Causal reasoning chain**: Gap -> Insight -> Method -> Experiments chain intact? Logic jumps?
- **DL-specific unsoundness patterns**: train/test leakage, unfair comparison (different backbone/pretraining/augmentation), missing variance reports, hyperparameter overfitting on test set, missing statistical tests for <1% differences.

### Role 3: Experiment Critic

**Persona**: ablation expert who cares about "do experiments actually prove the claims."

**Dimensions**:
- **Claim-Evidence alignment**: per `research/contribution.md`, every claim has experimental validation? Correlation != causation addressed? Ablation proves improvement source?
- **Baseline fairness and sufficiency**: strong enough? Recent enough? Same backbone/pretraining/augmentation/training budget? Extra parameters/FLOPs accounted for?
- **Ablation coverage**: all key design choices covered? Reasonable ablation baselines? Any hidden "remove-and-it-goes-up" ablations?
- **Cherry-picking detection**: selective metrics/datasets/visualizations? Failure cases shown?
- **Generalizability support**: dataset diversity sufficient? Multiple domains/scales/settings?

### Role 4: Presentation Critic

**Persona**: Area Chair who knows reviewer time is limited and readability directly affects scores.

**Dimensions**:
- **Narrative flow**: can reader follow the logic chain naturally? Information gaps? Redundancies?
- **Figure quality**: Figure 1 effective? Architecture diagram clear? Experiment figures professional? Captions self-contained?
- **Space allocation**: Method/Experiments ratio matches paper type? Over-verbose or under-developed sections?
- **Language quality**: consistent terminology? Notation matches notation.md? Grammar/spelling? Sentence clarity? Passive voice overuse?
- **First impression**: title accurate and attractive? Abstract makes reader want to continue? Core contribution graspable in 10-minute skim?

### Role 5: Reproducibility Critic

**Persona**: researcher who has tried reproducing many papers and knows the gap between "what papers say" and "what was actually done."

**Dimensions**:
- **Hidden hyperparameters**: weight init, gradient clipping, warmup, EMA, label smoothing, mixup?
- **Hardware dependence**: large batch requiring multi-GPU sync? TPU/GPU behavior differences?
- **Data preprocessing completeness**: every step specified? Tokenization, normalization, augmentation parameters?
- **Implementation details**: optimizer, LR schedule, total steps/epochs, early stopping, eval settings (beam size, temperature)?
- **Code/data availability**: open-source commitment? Public datasets? Private data statistics?
- **Reproduction cost**: GPU hours / cost? Feasible for a 1-2 GPU PhD student?

### Role 6: External Perspective (Optional)

If Codex MCP available, invoke for independent third-party review. Focus: overlooked risks, assumption holes, methodology flaws, novelty assessment. Save to `Papers/critique/external.md`. Non-blocking on failure.

## Step 3: Write Review Reports

Each role produces an independent report in `Papers/critique/`:
- `novelty.md`, `soundness.md`, `experiment.md`, `presentation.md`, `reproducibility.md`

Report format:
```markdown
# [Role] Critique Report

## Overall Assessment
- **Score**: X / 10
- **Core Assessment**: (2-3 sentences)
- **Would this dimension cause reject at a top venue?**: Yes/No + reasoning

## Issues (by severity)

### [Critical] Issue Title
- **Location**: section + specific paragraph
- **Problem**: concrete description
- **Simulated reviewer phrasing**: (how a real reviewer would word this)
- **Suggested fix**: specific solution

### [Major] Issue Title
...

### [Minor] Issue Title
...

## Strengths
(genuine positives in this dimension)

## Summary Recommendations
(1-2 paragraphs)
```

## Step 4: Generate Summary

Produce `Papers/critique/summary.md`:
- Aggregate all Critical and Major issues (include External findings marked `[External]`)
- Group by section for P4 editing convenience
- Tag each issue: **rewrite-fixable** vs **needs-additional-experiments**
- If External review available, add "Unique External Findings" section
- **Reject risk assessment**: based on 5 role scores, preliminary judgment on "would this be rejected?"

## Key Behaviors
- Each role reviews **independently** -- not influenced by other roles' conclusions
- **Cite original text** for every issue
- **Concrete fix suggestions**, not vague "needs strengthening"
- Strict but fair -- acknowledge strengths too
- Distinguish **presentation problems** from **research problems** (latter tagged as needing code-stage work)
- Simulate real reviewer reading pattern: quick scan (Abstract -> Figure -> Tables -> Conclusion) then detailed read
- **No false-positive criticism**: every critique has specific evidence. Do not criticize just to appear strict.

## Output
- `Papers/critique/novelty.md`
- `Papers/critique/soundness.md`
- `Papers/critique/experiment.md`
- `Papers/critique/presentation.md`
- `Papers/critique/reproducibility.md`
- `Papers/critique/external.md` (optional)
- `Papers/critique/summary.md`

## Exit Criteria
- [ ] 5 independent review reports generated (+ external if MCP available)
- [ ] Each report has score and issue list
- [ ] Summary groups all Critical/Major issues by section
- [ ] Issues have specific text citations and fix suggestions
- [ ] Presentation vs research problems distinguished
- [ ] Every Critical issue has simulated reviewer phrasing
- [ ] Reject risk assessed
