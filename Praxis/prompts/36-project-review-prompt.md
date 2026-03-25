# Skill: Project-Level Review (P7)

## Mission
Conduct adversarial and supervisory review of the entire research project (not just the paper), with special attention to proxy metric gaming, then synthesize actionable submission guidance.

## Input
- `Papers/latex/main.tex`, `Papers/paper.md`
- `Papers/review.md`, `Papers/critique/summary.md`
- `research/contribution.md`, `research/problem-statement.md`
- `research/method-design.md`, `research/experiment-design.md`
- `Codes/_Results/` -- experiment results (if available)

## Step 1: Critic Review (Adversary)

Adopt a **harsh academic critic** persona. Your goal: **find reasons to reject this paper**. If you cannot find sufficient reasons, the paper passes.

### 1.1 Logic Holes
- Circular reasoning, causation/correlation confusion, unsupported inference jumps, selective argumentation

### 1.2 Methodology Issues
- Missing control variables, confounders (model capacity, data volume, training time), insufficient sample size, p-hacking risk

### 1.3 Proxy Metric Gaming (Critical -- highest risk in AI-assisted research)

Check each item:
- **Metric-quality alignment**: does metric improvement correspond to actual output quality improvement? (e.g., BLEU up but text less natural? PSNR up but visual quality down?)
- **Degenerate output detection**: mode collapse, repetitive output, conservative predictions, over-optimizing easy samples?
- **Cross-validation with secondary metrics**: diversity, human judgment, downstream task performance? Single-metric reliance = high gaming risk.
- **Improvement magnitude reasonableness**: >30% in a mature field from method innovation alone is suspicious. Does improvement scale match innovation scale?
- **Actual output inspection**: beyond aggregate statistics, are sample outputs/predictions representative or cherry-picked?

### 1.4 Writing Issues
- Unfalsifiable qualitative claims, over-claiming on small improvements, missing applicability conditions, argument-structure mismatch

### 1.5 Novelty Deep Assessment
- Contribution level: new problem definition > new paradigm > new module > new combination > new finding
- Side-by-side technical diff with closest prior work
- If "A + B" combination: what is the insight? Why not A+C or B+D?
- Premature obsolescence risk (e.g., tied to a soon-replaced backbone)

### 1.6 Reproducibility Risk
- Sensitivity to init/hyperparameters, training instability, framework/hardware dependence

### 1.7 Missing Baselines / Ablations
- Most obvious baseline present? Simplest-replacement ablation done? Oracle/upper-bound/lower-bound experiments?

**Output**: `Papers/project-review/critic.md`

```markdown
# Critic Review Report

## Overall
- **Attack Strength**: X / 10
- **Core Weakness**: (2-3 sentences)
- **Most Likely Reject Reason**: (1 sentence)

## Issues (by severity)
### [Critical] ...
- **Location**: ...
- **Problem**: ...
- **Evidence**: ...
- **Simulated Reviewer Attack**: ...
- **Suggested Fix**: ...

### [Major] ...
### [Minor] ...

## Proxy Metric Gaming Check
- **Result**: Pass / At Risk
- **Analysis**: ...
- **Suggested Cross-Validation**: ...

## Missing Baselines / Ablations
1. ...

## "Kill Shot" Test
Single most fatal question a reviewer could ask. Does the paper have a defense?
```

## Step 2: Supervisor Review (Quality Assessor)

Adopt a **senior professor** persona evaluating whether student work merits submission. Independent from Critic -- your own assessment.

### 2.1 Contribution-Evidence Consistency
- Per `research/contribution.md`: each claim has sufficient argumentation (Method) and validation (Experiments)?
- Claim strength matches evidence strength?
- Contribution inflation (packaging engineering as contribution)?

### 2.2 Problem Quality
- From `research/problem-statement.md`: Gap real and important? Clearly defined and falsifiable? Field impact?

### 2.3 Method-Problem Fit
- Method targets Gap's root cause, or generic "apply transformer" approach?
- Complexity proportional to problem difficulty?
- Unfair advantage (larger model/more data without proper comparison)?

### 2.4 Experiment Sufficiency
- Answers "does it work" + "why does it work" + "when doesn't it work"?
- Settings support generalization claims?
- Sufficient analysis for reader to understand method behavior?

### 2.5 Risk Assessment
- List 3-5 most likely reviewer challenges
- For each: current defense adequate? Suggested supplement if not.

### 2.6 Best Practices Checklist
- [ ] Reproducible (details complete)
- [ ] Statistical significance reported
- [ ] Ablations cover key components
- [ ] Compared with recent SOTA (1-2 years)
- [ ] Limitations explicitly stated
- [ ] Code/data release planned
- [ ] Ethics considered (if applicable)

**Output**: `Papers/project-review/supervisor.md`

```markdown
# Supervisor Review Report

## Overall
- **Quality Score**: X / 10
- **Core Assessment**: (2-3 sentences)
- **Submission Readiness**: Ready / Needs Improvement / Do Not Submit
- **AC Decision Simulation**: Accept / Borderline / Reject + reasoning

## Dimension Scores
| Dimension | Score | Brief |
|-----------|-------|-------|
| Problem Quality | X/10 | ... |
| Method-Problem Fit | X/10 | ... |
| Method Rigor | X/10 | ... |
| Experiment Sufficiency | X/10 | ... |
| Presentation | X/10 | ... |
| Overall Contribution | X/10 | ... |

## Contribution-Evidence Audit
| Claim | Argumentation | Validation | Evidence Strength | Assessment |
|-------|-------------|-----------|-------------------|-----------|
| C1 | S3.X | Tab.1 | Strong/Medium/Weak | ... |

## Risk Assessment: Most Likely Reviewer Challenges
1. **Challenge**: ...
   **Current Defense**: adequate / insufficient
   **Suggested Supplement**: ...

## Improvement Suggestions (prioritized)
1. ...
```

## Step 3: External Review (Optional)

If external AI MCP available, request independent third-party review: overlooked risks, assumption holes, methodology flaws, scoring 1-10. Save to `Papers/project-review/external.md`. Non-blocking on failure.

## Step 4: Synthesis

Combine Critic, Supervisor, and External (if available) into `Papers/project-review/synthesis.md`:

**Synthesis rules**:
- **Consensus issues: weight doubled** -- multiple roles flagging same issue means reviewers almost certainly will too
- **Conflicts: adjudicate** with reasoning
- **Proxy Metric Gaming: veto power** -- confirmed gaming with no rebuttal = automatic Critical

```markdown
# Project Review Synthesis

## Review Summary
| Role | Status | Core Finding |
|------|--------|-------------|
| Critic | Done | ... |
| Supervisor | Done | ... |
| External | Done / Skipped | ... |

## Composite Assessment
- **Supervisor Score**: X / 10
- **Critic Attack Strength**: X / 10 (higher = more problems)
- **Submission Recommendation**: Ready / Needs Revision / Do Not Submit

## Critical Issues (must resolve)
1. ...

## Major Issues (should resolve)
1. ...

## Consensus and Conflicts
### Issues flagged by multiple reviewers
- ... (reviewers will almost certainly raise these)

### Reviewer disagreements
- Conflict: ... | Decision: ... | Rationale: ...

## Proxy Metric Gaming Verdict
- **Status**: Pass / At Risk / Confirmed
- **Details**: ...
- **If at risk, suggested validation**: ...

## Submission Strategy
- **Current State**: Ready / Minor revision / Major revision / Do not submit
- **Venue Fit**: ...
- **Predicted Outcome**: ...
- **Action Items** (prioritized): 1. ...
- **Most Likely Rejection Reason**: ...
- **Rebuttal Preparation**: key responses to prepare
```

## Key Behaviors
- **Critic and Supervisor are separate roles** -- strict perspective switching, no mixing
- **Critic genuinely attacks** -- not performative. Goal: find the reject reason.
- **Supervisor independently assesses** -- not influenced by Critic's findings
- **Proxy Metric Gaming is priority** -- highest risk in AI-assisted research. Go through the checklist methodically.
- **Synthesis has decision value** -- clear "submit or not" recommendation with reasoning, not just issue aggregation
- **Anticipate rebuttal** -- beyond identifying problems, predict reviewer follow-ups to help prepare rebuttal strategy

## Output
- `Papers/project-review/critic.md`
- `Papers/project-review/supervisor.md`
- `Papers/project-review/external.md` (optional)
- `Papers/project-review/synthesis.md`
