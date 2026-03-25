# Skill: Paper Fill

## Mission
Replace `{{PENDING:...}}` placeholders in paper sections with real experiment data from `Codes/_Results/`, supplement result-dependent analysis, and produce a fill report. **Never fabricate data.**

## Input

| File | Purpose |
|------|---------|
| `Papers/sections/*.md` | Sections containing `{{PENDING:...}}` placeholders |
| `Codes/_Results/*.md` | All experiment result files |
| `research/experiment-design.md` | Metric ID to actual metric name mapping |
| `Papers/outline.md` | Figure/table plan (section assignments) |

## Step 1: Scan Placeholders

Read all `Papers/sections/*.md`. Extract every `{{PENDING: id | description | expected}}` pattern.

Build **placeholder registry**:
```
{ id -> { description, expected, file, line, context } }
```

Report to user: total count, breakdown by type (table / numeric / analysis).

## Step 2: Read All Results

Read every `.md` file in `Codes/_Results/`. Parse: numeric results (percentages, metric values), table data (columns, rows, values), analysis conclusions, figure paths.

Build **result registry**:
```
{ metric_name -> { value, context, source_file, related_metrics } }
```

Also read `research/experiment-design.md` for metric ID to actual metric name mapping.

## Step 3: Match and Replace

For each placeholder, find matching data in result registry. Three cases:

**Case A -- Exact Match**: replace placeholder with formatted real data.
- `{{PENDING: main_acc | ... | ~85%}}` -> `87.3%`

**Case B -- Partial Match** (related but not exact): insert best available data with review tag:
```markdown
87.3% <!-- REVIEW: auto-filled from probe_result.md preliminary data; confirm if final -->
```

**Case C -- No Match**: keep original placeholder, add missing tag:
```markdown
{{PENDING: main_acc | ... | ~85%}} <!-- MISSING: no matching result in Codes/_Results/ -->
```

## Step 4: Fill Tables

For placeholders with "table" in the id:
1. Extract complete table data from result registry
2. Generate formatted Markdown table: **bold** best results, `<u>underline</u>` second-best, aligned decimal places, `**Ours**` row label
3. Incomplete tables: fill available cells, `--` for missing, add `<!-- INCOMPLETE: missing X, Y data -->`

## Step 5: Supplement Analysis Paragraphs

After filling tables/numbers, check if analysis text needs updating:

**5.1 Main Results**: overall trend, significance analysis (which datasets/metrics show largest improvement and why), comparison with expected values (flag significant deviations).

**5.2 Ablation**: per-component analysis (performance drop when removed), component interactions, key component identification.

**5.3 Writing Rules**: match paper language (English analysis for English paper), analysis grounded in data only, tag gaps: `<!-- ANALYSIS-GAP: need X experiment data -->`

## Step 6: Update Abstract and Conclusion

**Abstract**: fill key numbers only; do not add length.

**Conclusion**: update result summary with actual numbers. If results diverge from Introduction claims, add `<!-- REVIEW: conclusion-introduction claim mismatch, please check -->`.

## Step 7: Generate Fill Report

Write `Papers/fill-report.md`:

```markdown
# Paper Fill Report

> Generated: {timestamp}
> Sources: {list of result files read}

## Summary

| Item | Count |
|------|-------|
| Total placeholders | N |
| Filled | M |
| Still pending | K |
| Needs human review | J |

## Filled Placeholders

| ID | Value | Source File | Location |
|----|-------|------------|----------|
| ... | ... | ... | sections/X.md:Lxx |

## Still Pending

| ID | Description | Reason |
|----|------------|--------|
| ... | ... | No matching result / experiment not yet run |

## Needs Human Review

| ID | Issue | Suggestion |
|----|-------|-----------|
| ... | Data from probe, not final experiment | Confirm then remove REVIEW tag |

## Expected vs Actual

| ID | Expected | Actual | Notes |
|----|----------|--------|-------|
| ... | ~85% | 91.2% | Significantly above expectation; consider updating Introduction motivation |
```

## Step 8: Git Sync

```bash
cd <project_path>
git add Papers/sections/ Papers/fill-report.md
git commit -m "paper-fill: filled M/N placeholders (K pending, J need review)"
git push
```

## Quality Standards
1. **Data accuracy**: every filled number traceable to `Codes/_Results/`
2. **Format consistency**: decimal places, units, percentage signs match existing paper content
3. **Table formatting**: best bold, second-best underlined, aligned, our method highlighted
4. **Evidence-based analysis**: no unsupported inferences
5. **Complete tagging**: every unfilled or partial-match placeholder has clear tag and reason
6. **Idempotent**: multiple runs do not duplicate tags or corrupt already-filled data

## Prohibitions
- **No data fabrication**: missing result = keep placeholder; never invent numbers
- **No placeholder deletion without filling**: either fill with real data or keep original with tag
- **No non-placeholder content changes**: aside from supplementary analysis, do not modify existing method descriptions, narrative, etc.
- **No ignoring expected field**: always compare expected vs actual in report; flag significant differences
- **No skipping fill-report**: generate complete report even if all placeholders filled
