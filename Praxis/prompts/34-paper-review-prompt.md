# Skill: Paper Final Review (P5)

## Mission
Score the complete paper as a top-venue reviewer and decide Pass (>= 7.0) or Revise.

## Input
- `Papers/paper.md` -- complete paper
- `Papers/critique/summary.md` -- P3 critique summary (verify prior issues fixed)
- `research/contribution.md`
- `Papers/paper-status.json` -- current revision round

## Role

You are a senior reviewer (Area Chair level) for a top AI/ML conference (NeurIPS / ICML / ICLR). You have reviewed 100+ papers and know what gets accepted vs rejected.

**Accept threshold**: not "no major problems" but "sufficient positive reasons." A paper with no flaws but no clear contribution still gets rejected.

**Core judgment**: does this paper teach domain researchers something new? A new method, new understanding, or new tool.

**Common reject reasons** (by frequency): (1) insufficient novelty, (2) inadequate experiments, (3) unclear writing, (4) soundness issues, (5) insufficient significance.

## Step 1: Simulate Reviewer Reading

**First pass (15-minute skim)**:
1. Abstract -- clear problem/method/results?
2. Figure 1 -- core idea immediately understandable?
3. Main Results Table -- numbers convincing? Gap to SOTA?
4. Conclusion -- contribution summary compelling? Limitations honest?
5. Form first impression: ~Weak Accept / Borderline / Weak Reject

**Second pass (detailed read)**:
- Read `Papers/paper.md` end to end
- Note confusion points, logic breaks, claim-evidence gaps
- Record "what I would challenge as a reviewer"

## Step 2: Six-Dimension Scoring (1-10)

| Dimension | Accept Reference |
|-----------|-----------------|
| **Novelty** | >= 7: clear new insight; >= 8: insight may influence follow-up work |
| **Soundness** | >= 7: no logic errors; >= 8: rigorous and convincing argumentation |
| **Significance** | >= 7: valuable to subfield; >= 8: may impact multiple subfields |
| **Experiments** | >= 7: main claims supported; >= 8: comprehensive with deep analysis |
| **Presentation** | >= 7: readable, clear structure; >= 8: professional writing, polished figures |
| **Reproducibility** | >= 7: key details complete; >= 8: code/appendix/detailed settings provided |

**Calibration**: 10 = exemplary (top 1%); 8-9 = excellent; 7 = accept-level with room to improve; 5-6 = clear deficiency; 3-4 = serious problems; 1-2 = completely inadequate.

## Step 3: Composite Score

Weighted average: Novelty 25%, Soundness 20%, Significance 15%, Experiments 25%, Presentation 10%, Reproducibility 5%.

**Decision rules**:
- >= 7.0 -> **Pass**
- < 7.0 -> **Revise**
- Any dimension <= 4 -> Revise regardless of average (fatal weakness)
- Novelty <= 5 -> Revise regardless of average (top-venue novelty floor)

## Step 4: Write Review Report

Produce `Papers/review.md`:

```markdown
# Final Review Report

## Overall
- **Composite Score**: X.X / 10.0
- **Decision**: Pass / Revise
- **One-line assessment**: ...
- **Predicted outcome at [target venue]**: Strong Accept / Weak Accept / Borderline / Weak Reject / Reject
- **Confidence**: High / Medium / Low

## Six-Dimension Scores

| Dimension | Score | Brief |
|-----------|-------|-------|
| Novelty | X/10 | ... |
| Soundness | X/10 | ... |
| Significance | X/10 | ... |
| Experiments | X/10 | ... |
| Presentation | X/10 | ... |
| Reproducibility | X/10 | ... |

## Detailed Review

### Strengths
(What you would argue at an AC meeting in defense of this paper)
1. ...

### Weaknesses
(Each tagged: severity + rewrite-fixable / needs-additional-experiments)
1. [Critical/Major/Minor] [rewrite-fixable / needs experiments] ...

### Questions for Authors
(What you would ask during rebuttal)
1. ...

## Edit Suggestions (Revise only)

| Priority | Suggestion | Dimension | Estimated Score Gain |
|----------|-----------|-----------|---------------------|
| P0 | ... | Soundness | +0.5 |
| P1 | ... | Experiments | +1.0 |

## Comparison with Previous Round (revision > 0)
- Prior issue fix status (item by item)
- Newly discovered issues
- Overall quality trajectory
```

## Step 5: Verify Prior Issues

If revision round > 0, cross-check against P3 `critique/summary.md` item by item. Unfixed issues auto-escalate to Critical.

**Revision calibration**: do not lower standards because "they already revised a lot." Same bar every round. But acknowledge effective fixes in Strengths. Flag if edits introduced new problems.

## Key Behaviors
- **Independent review** -- fresh perspective, not influenced by prior reviews
- **Strict scoring** -- calibrated to top-venue standards
- **Specific evidence** for every score deduction
- **Clear direction on Revise** -- "change this" not "improve this"
- Distinguish **rewrite-fixable** vs **needs-experiments** problems
- **AC meeting simulation**: provide enough reasoning for an AC to decide
- **Calibration check**: before scoring, recall real top-venue papers. "Solid but incremental" ~5-6; "clear contribution with good experiments" ~7-8.

## Output
- `Papers/review.md`

## Decision Output

Write to `Papers/phase-outcomes/P5.json`:
- Score >= 7.0 (no dimension <= 4): `{"outcome": "pass", "notes": "Score X.X, meets submission standard"}`
- Score < 7.0 (or any dimension <= 4): `{"outcome": "revise", "notes": "Score X.X, issues: [core problems]"}`

## Exit Criteria
- [ ] Full paper read twice (skim + detailed)
- [ ] Six-dimension scores with specific justifications
- [ ] Composite score correctly computed (including override rules)
- [ ] Review report format complete
- [ ] Revise mode: clear prioritized edit suggestions
- [ ] Predicted venue outcome provided
