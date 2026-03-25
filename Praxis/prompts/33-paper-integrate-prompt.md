# Skill: Paper Integration & Editing (P4)

## Mission
Address all critique issues, edit sections, and assemble the complete paper with narrative consistency.

## Input

Determine mode first:

| Mode | Condition | Extra Input |
|------|-----------|-------------|
| First Integration | `Papers/review.md` does not exist | P3 critique reports |
| P5 Revise Return | `Papers/review.md` exists | P5 final review |

**Base input (all modes)**:
- `Papers/sections/` -- section files
- `Papers/critique/summary.md`
- `Papers/outline.md`, `Papers/notation.md`

## Step 1: Create Edit Plan

**1.1 Classify and Prioritize Issues**

| Priority | Category | Description | Approach |
|----------|----------|-------------|----------|
| P0 | Fatal | Logic errors, math errors, data errors | Immediate fix; may require paragraph rewrite |
| P1 | Structural | Narrative breaks, weak argumentation, contribution-experiment misalignment | Significant edits, possibly cross-section |
| P2 | Expression | Imprecise language, notation inconsistency, redundancy/brevity | Local edits, no argument structure change |
| P3 | Polish | Grammar, formatting, caption improvement | Batch at end |

**1.2 Cross-Section Impact Analysis**

For each P0/P1 issue, trace cascading effects:
- Method formula change -> update notation.md + Experiments references
- Introduction contribution wording change -> update Abstract + Conclusion
- Experiment analysis change -> verify Introduction claims still hold
- New baseline/experiment needed -> tag "cannot resolve by editing alone"

**1.3 "Do Not Edit" Judgment**

Not all critique items need action. Skip with documented rationale when:
- Critique is based on misunderstanding (clarify if it is expression vs critique error)
- Critique requests out-of-scope experiments (record as future work)
- Different roles contradict each other (choose the more justified side with reasoning)

## Step 2: Edit Sections

Edit `Papers/sections/` files per the plan.

**Principles**:
- **Minimal invasion**: change only what needs changing. Broad rewrites introduce new problems.
- **Maintain narrative flow**: after editing a paragraph, verify transitions to preceding and following paragraphs.
- **Edit tracking**: every edit maps to a specific critique item. If an edit does not correspond to any critique, reconsider whether it is necessary.
- **Notation sync**: new symbols -> update `Papers/notation.md`
- **Do not skip Minor issues** -- they accumulate and erode professionalism.

**Section-specific notes**:
- **Method**: formula edits must not break derivation chains; new motivation aligns with Introduction gap
- **Experiments**: supplement analysis with "why" not "what"; if cherry-picking flagged, add comprehensive results
- **Introduction**: contribution wording changes must sync with Method/Experiments
- **Related Work**: integrate new citations into existing thematic groups, do not just append
- **Abstract**: almost always needs re-check after edits for consistency with revised body

## Step 3: Assemble Full Paper

Merge edited sections into `Papers/paper.md`:

```markdown
# [Title]

## Abstract
[from sections/abstract.md]

## 1. Introduction
[from sections/intro.md]

## 2. Related Work
[from sections/related_work.md]

## 3. Method
[from sections/method.md]

## 4. Experiments
[from sections/experiments.md]

## 5. Conclusion
[from sections/conclusion.md]

## References
[reference list]
```

## Step 4: Refine Abstract

With full paper finalized, re-examine Abstract:
- Consistent with revised body content
- Contains core numerical results
- 150-250 words
- Remove any claims deleted or modified in body

## Step 5: Full Self-Check

| Check | Method |
|-------|--------|
| Narrative consistency | Every Introduction claim covered by Experiments? |
| Contribution completeness | Every contribution.md item fully argued? |
| No fabricated content | Any new content not in research documents? |
| Figure/table self-contained | Every caption independently understandable? |
| Logic coherent | Intro -> Method -> Experiments -> Conclusion chain smooth? |
| Notation consistent | All symbols match notation.md? |
| Critique coverage | All Critical/Major issues addressed? |
| Number consistency | Same numbers in Abstract/Intro/Experiments/Conclusion? |
| Cross-references | All "Table X" / "Figure Y" references correct? |

## P5 Revise Mode (Additional Steps)

When returning from P5:
1. **Prioritize P5 review issues** over re-doing full edits
2. Read `Papers/review.md`, locate each issue
3. **Targeted fixes only -- keep stable content unchanged**. Excessive edits risk infinite revision loops.
4. If P5 flags "need additional experiments", tag as "cannot resolve this round" but mitigate through improved analysis/discussion
5. Update `Papers/paper.md`

## Key Behaviors
- Edits **precisely map** to critique items; no unrelated changes
- Maintain cross-section narrative consistency
- Academic language: precise, objective, concise
- Do not skip Minor issues
- Revise mode: minimal edit principle
- **Re-read after editing**: read the full section after changes to verify edits did not break flow
- **Do not introduce new problems**: for each edit, ask "would the next review round flag this?"

## Output
- `Papers/sections/*.md` -- updated section files
- `Papers/paper.md` -- complete paper
- `Papers/notation.md` -- updated notation table

## Exit Criteria
- [ ] All Critical and Major issues addressed (or tagged "cannot resolve by editing" with rationale)
- [ ] Complete paper `paper.md` generated
- [ ] Abstract refined, contains core numbers, consistent with revised body
- [ ] Full self-check passed
- [ ] Notation table updated
- [ ] Edits did not introduce new narrative breaks or logic contradictions
