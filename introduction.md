# Noesis System Manual (v3)

> Complete usage guide and architecture reference for Noesis.
> For a quick product overview, see [README.md](README.md). This document is the full operational manual.

---

## Reading Guide

| You want to... | Read sections |
|----------------|---------------|
| Understand what Noesis is | 1-2 |
| Get started immediately | 3 |
| Learn the Init Module | 4 |
| Learn the Research Module | 5 |
| Learn the Paper Module | 6 |
| Use auxiliary commands | 7 |
| Use knowledge accumulation (Logos) | 8 |
| Understand architecture & file layout | 9-10 |
| Troubleshoot or check FAQ | 11 |

---

## 1. What Is Noesis

**Noesis** (νόησις, cognition & insight) is an AI Agent-driven scientific research system for **AI/ML/DL**, running on local **Claude Code**.

It is not a one-shot prompt tool. It is a long-running operational framework where:

- Knowledge accumulates as structured, searchable assets — not chat history
- Research proceeds through auditable, recoverable, reviewable state machines
- Every completed project feeds lessons back into the system for future projects

**The core philosophy:**

> The researcher commands direction and critical judgment. Agents handle high-intensity execution and structured labor.

In practice, this means:

- **Automated phases**: AI drives execution end-to-end (formalization, review, design, paper writing)
- **Manual phases**: The researcher is in full control (probe experiments, implementation, final experiment execution)
- **Review gates**: Multi-agent debates pressure-test every major decision before proceeding

---

## 2. System Overview

Noesis consists of two **independent** subsystems connected through a shared knowledge base:

```
Logos  ──────────────→  Episteme  ──────────────→  Praxis
knowledge accumulation     knowledge base           research execution

/logos-discover            Methods Bank             /praxis-init-auto
/logos-read                Gaps & Assumptions       /praxis-r-auto
                           Experimental Patterns    /praxis-paper
                           Reusable Resources       /praxis-evolve
```

### Why Two Subsystems

- **Knowledge accumulation** (Logos) is an open-ended loop with no fixed endpoint
- **Research execution** (Praxis) is phased work with clear states and exits

Logos fills the Episteme knowledge base. Praxis consumes it at key decision points. This separation lets you build knowledge continuously while running projects in structured phases.

### Praxis: Three Independent Modules

Praxis contains three modules, each with its own state machine:

| Module | Purpose | State file |
|--------|---------|------------|
| **Init** | From idea to validated direction | `Docs/init-module-status.json` |
| **Research** | From direction to complete experiments | `Docs/research-module-status.json` |
| **Paper** | From results to publication-ready manuscript | `Papers/paper-status.json` |

A lightweight `pipeline-status.json` tracks only which module is currently active.

---

## 3. Quick Start

### 3.1 Environment Setup

Noesis assumes: **macOS + Claude Code + GitHub**

```
~/Research/
├── Noesis/           ← This repo (central methodology library)
├── Episteme/         ← Knowledge base (Logos output)
└── <ProjectName>/    ← Individual research projects (each its own repo)

~/.noesis/lessons/    ← Cross-project lessons (local, auto-injected)
```

Multi-machine sync is handled through `git push` / `git pull`. All paths use `~` to avoid hardcoding usernames.

### 3.2 Initialize Episteme (First Time Only)

```bash
KB="$HOME/Research/Episteme"
cp "$HOME/Research/Noesis/Logos/templates/kb-index.md" "$KB/"
cp "$HOME/Research/Noesis/Logos/templates/reading-queue.md" "$KB/"
cp "$HOME/Research/Noesis/Logos/templates/research-directions.md" "$KB/"
```

Edit `~/Research/Episteme/research-directions.md` with your research directions, core keywords, seed papers, target venues, and authors to follow.

### 3.3 Typical Workflow: New Project from Scratch

```bash
# 1. Build knowledge (can be done anytime, independently)
/logos-discover
/logos-read 5

# 2. Init: idea → validated direction + probe results
/praxis-init-auto

# 3. Research: direction → complete experiments
/praxis-r-auto ~/Research/MyProject

# 4. Paper: results → publication-ready manuscript
/praxis-paper ~/Research/MyProject

# 5. Evolution: extract lessons for future projects
/praxis-evolve ~/Research/MyProject
```

### 3.4 Onboarding an Existing Project

```bash
/praxis-assimilate ~/Research/ExistingProject
```

This reconstructs missing documents, runs key reviews, and writes state files so the project can continue under Noesis management.

---

## 4. Init Module — From Idea to Validated Direction

The Init module takes a vague research seed and transforms it into a pressure-tested direction with empirical signal from a probe experiment.

### 4.1 Flow

```
init → start → probe_design → review → probe_impl → complete
```

| Phase | What happens |
|-------|-------------|
| **init** | Collect researcher's idea, papers, notes, or Episteme leads |
| **start** | Identify seed type, core hypothesis, background, SOTA, candidate gaps |
| **probe_design** | Design minimal probe experiment to test core intuition |
| **review** | 6-agent debate pressure test |
| **probe_impl** | Execute probe experiment (researcher-driven) |
| **complete** | Direction confirmed, `project.md` finalized |

### 4.2 Commands

| Command | Description |
|---------|-------------|
| `/praxis-init-auto` | Runs the full Init flow automatically |
| `/praxis-init` | Manual: enter the init phase |
| `/praxis-start` | Manual: enter the start phase |
| `/praxis-probe-design` | Manual: enter probe design |
| `/praxis-review` | Manual: run the review debate |
| `/praxis-probe-impl` | Manual: execute the probe |

### 4.3 The 6-Agent Review Debate

Six independent agents evaluate the direction from different angles:

| Agent | Perspective |
|-------|------------|
| **Innovator** | Novelty and potential impact |
| **Pragmatist** | Feasibility and resource constraints |
| **Theorist** | Theoretical soundness |
| **Contrarian** | Weaknesses and failure modes |
| **Interdisciplinary** | Cross-field connections and missed angles |
| **Empiricist** | Experimental viability and evidence strength |

A synthesizer produces a final verdict: **confirmed**, **strengthened**, **revised**, or **HIGH RISK**.

### 4.4 Iteration Paths

- **review** can revise back to **start** (rethink direction)
- **probe_impl** can declare infeasible, returning to **probe_design**

### 4.5 Core Output

`project.md` sections 1-4, plus probe code and probe results.

---

## 5. Research Module — From Direction to Complete Experiments

The Research module takes a validated direction and drives it through formalization, review, design, review, implementation, and knowledge recovery.

### 5.1 Flow

```
formalize → formalize_review → design → design_review → blueprint → implement → retrospective → complete
```

| Phase | What happens | Mode |
|-------|-------------|------|
| **formalize** | Formal Gap + Research Question + attack angle (deeper than Init's start) | Auto |
| **formalize_review** | 4-agent strategic debate: "Is this direction worth pursuing?" | Auto |
| **design** | Method + experiment co-design, with pilot experiment (Experiment 0) | Auto |
| **design_review** | 6-agent technical debate: "Is this approach sound?" | Auto |
| **blueprint** | Code architecture + experiment execution checklist | Auto |
| **implement** | Coding + experiments — pilot first, then full | **Manual** |
| **retrospective** | Knowledge recovery: what worked, what failed, what to carry forward | Auto |
| **complete** | Module finished | — |

### 5.2 Commands

| Command | Description |
|---------|-------------|
| `/praxis-r-auto` | Runs the full Research flow automatically |
| `/praxis-r-formalize` | Manual: run formalize phase |
| `/praxis-r-formalize-review` | Manual: run formalize review |
| `/praxis-r-design` | Manual: run design phase |
| `/praxis-r-design-review` | Manual: run design review |
| `/praxis-r-blueprint` | Manual: run blueprint phase |
| `/praxis-r-implement` | Manual: implementation (always manual) |
| `/praxis-r-retrospective` | Manual: run retrospective |

### 5.3 Formalize Review (4-Agent Strategic Debate)

| Agent | Focus |
|-------|-------|
| **Contrarian** | Challenges assumptions and identifies weaknesses |
| **Comparativist** | Compares against alternative approaches |
| **Pragmatist** | Evaluates feasibility and practical constraints |
| **Interdisciplinary** | Identifies cross-field insights |

Outcomes: **pass** → design | **revise** → formalize | **abandon** → complete

### 5.4 Design Review (6-Agent Technical Debate)

| Agent | Focus |
|-------|-------|
| **Theorist** | Mathematical and theoretical correctness |
| **Methodologist** | Method design quality |
| **Empiricist** | Experiment design rigor |
| **Skeptic** | Hidden flaws and edge cases |
| **Pragmatist** | Engineering feasibility |
| **Contrarian** | Fundamental objections |

Outcomes: **pass** → blueprint | **revise** → design | **fundamental** → formalize | **abandon** → complete

### 5.5 The Implement Phase (Manual)

This is where the researcher takes over. Refer to the blueprint output for code architecture and experiment checklists.

**Code organization follows deep/shallow separation:**
- `Codes/core/` — reusable deep kernel (algorithms, models)
- `Codes/experiments/` — shallow wrappers (experiment-specific scripts)
- `Codes/_Data/` — generated data (gitignored)
- `Codes/_Results/` — results (tracked in git)

Run the pilot experiment (Experiment 0) first, then proceed to full experiments.

### 5.6 Iteration and Rollback

The Research module does not blindly restart on failure. It routes rollbacks to the appropriate level:

| Trigger | Rollback target | Rationale |
|---------|----------------|-----------|
| formalize_review **revise** | formalize | Strategic framing needs adjustment |
| design_review **revise** | design | Technical approach needs revision |
| design_review **fundamental** | formalize | Direction itself is flawed |
| implement **iterate_method** | design | Method component has issues |
| implement **iterate_direction** | formalize | Attack angle or gap definition is wrong |

**Escalation guards:**
- design receives ≥2 rollbacks → escalate to formalize
- formalize receives ≥3 rollbacks → trigger abandon evaluation

**Cross-module rollback:** Research can roll back to Init's start phase (probe_failure) if fundamental issues surface.

### 5.7 Core Output Files

| File | Content |
|------|---------|
| `research/problem-statement.md` | Formal gap, research question, attack angle |
| `research/method-design.md` | Method specification |
| `research/experiment-design.md` | Experiment plan (cross-referenced with method) |
| `research/contribution.md` | Contribution summary |
| `research/retrospective.md` | Knowledge recovery |
| `Reviews/research-formalize/` | Formalize review debate records |
| `Reviews/research-design/` | Design review debate records |

---

## 6. Paper Module — From Results to Manuscript

The Paper module has its own independent state machine. It can start before experiments are fully complete — use `{{PENDING:...}}` placeholders for missing data and fill them later.

### 6.1 Flow

```
P1(outline) → P2(sections) → P3(critique) → P4(integrate) → P5(review) → P6(latex) → P7(project-review)
```

| Phase | What happens |
|-------|-------------|
| **P1 Outline** | Narrative spine, notation table, section structure |
| **P2 Sections** | Draft each section independently |
| **P3 Critique** | Multi-role critique of the draft |
| **P4 Integrate** | Merge sections into unified `paper.md` |
| **P5 Review** | Final quality review with scoring |
| **P6 LaTeX** | Generate `main.tex`, `references.bib`, optional PDF |
| **P7 Project Review** | Retrospective review of the entire project |

### 6.2 Commands

| Command | Description |
|---------|-------------|
| `/praxis-paper` | Runs the full Paper flow (P1 through P7) |
| `/praxis-paper-fill` | Fill `{{PENDING:...}}` placeholders with real experiment data |

### 6.3 Revision Loop

P5 scores the manuscript. If the score falls below threshold, it loops back to P4 for revision. Maximum 2 revision rounds — after that, it forces through to prevent infinite loops.

### 6.4 Key Principle

The Paper module does not reinvent the research. It faithfully maps from `research/problem-statement.md`, `research/method-design.md`, `research/experiment-design.md`, and `Codes/_Results/` into a coherent narrative:

**Gap → Root Cause → Method → Validation → Contribution**

No new research claims are invented during paper writing.

### 6.5 Output Files

```
Papers/
├── paper-status.json
├── outline.md, notation.md
├── sections/*.md
├── paper.md
├── latex/main.tex, references.bib
└── project-review/
```

---

## 7. Auxiliary Commands

### 7.1 `/praxis-conclude` — Experiment Failure Diagnosis

```bash
/praxis-conclude ~/Research/MyProject
```

When experiments fail, this command:
1. Diagnoses the failure level (execution / method / direction)
2. Appends to `iteration-log.md` and updates result files
3. Routes rollback to the appropriate phase

| Failure level | Meaning | Rollback to |
|---------------|---------|-------------|
| Execution | Bugs, hyperparameters — method is fine | Stay in implement |
| Method | Method component is flawed | design |
| Direction | Gap or attack angle is wrong | formalize |

After rollback, re-run `/praxis-r-auto` to continue from the new position.

### 7.2 `/praxis-present` — Progress Presentation

```bash
/praxis-present ~/Research/MyProject
```

Generates `presentation.md` designed for a **15-minute research discussion** with an advisor or collaborator. Prioritizes:
- Current progress and key claims
- Open questions
- Decisions that need human judgment

Supports hot restart — will not overwrite manual edits you have made.

### 7.3 `/praxis-assimilate` — Onboard External Projects

```bash
/praxis-assimilate ~/Research/ExistingProject
```

Takes any in-progress research project and brings it into Noesis:
- Reconstructs missing phase documents
- Runs key reviews
- Writes `pipeline-status.json` and module status files

### 7.4 `/praxis-evolve` — Cross-Project Learning

```bash
/praxis-evolve ~/Research/MyProject
```

Extracts two types of output:

**1. Cross-project lessons** → `~/.noesis/lessons/<skill_name>.md`

Each lesson is tagged:
- Category: `[SYSTEM]`, `[EXPERIMENT]`, `[WRITING]`, etc.
- Frequency: `[RECURRING]`, `[NEW]`
- Validity: `[✓ verified]`, `[✗ ineffective]`, `[? unverified]`

Runners automatically inject relevant lessons into future projects at matching phases. Lessons tagged `[✗ ineffective]` are filtered out.

**2. Framework self-evolution** → reads `pipeline-evolution-log.md` and may update Noesis prompts, skills, or templates. This means Noesis improves at the framework level, not just the project level.

### 7.5 `/praxis-optimize` — Deep Prompt/Skill Optimization

```bash
/praxis-optimize
```

Performs deep optimization of Noesis prompts and skills based on accumulated experience and evolution logs.

---

## 8. Logos — Continuous Knowledge Accumulation

Logos runs an open-ended loop: **Discover → Read → Extract → Discover again**.

Its purpose is to convert "having read many papers" into "owning a long-term searchable, composable, reusable research knowledge base."

### 8.1 Commands

| Command | Description |
|---------|-------------|
| `/logos-discover [kb_path]` | Multi-strategy paper search, update reading queue |
| `/logos-read [arg]` | Deep reading + knowledge asset extraction |

Default knowledge base path: `~/Research/Episteme`.

### 8.2 `/logos-discover` — Paper Discovery

Executes 5 search strategies:

| Strategy | Description |
|----------|-------------|
| **Keyword search** | arXiv + Semantic Scholar, core × extended keywords |
| **Citation tracking** | Forward/backward citation networks from seed papers |
| **Author tracking** | Latest publications from target researchers |
| **Venue tracking** | Latest papers from target conferences/journals |
| **Controversy search** | Negative results, criticisms, replication failures |

Candidates undergo **Quick Scan** scoring on 4 dimensions: relevance, reusability, complementarity, and hidden-assumption potential. Results update `reading-queue.md`.

### 8.3 `/logos-read` — Deep Reading

Accepts four input modes:

```bash
/logos-read          # Read highest-priority paper from queue
/logos-read 3        # Read top 3 papers from queue
/logos-read 2405.12186  # Read specific arXiv paper
/logos-read attention   # Search queue by keyword
```

### 8.4 Five Knowledge Asset Types

| Asset | Content |
|-------|---------|
| **Methods Bank** | Mechanisms, formulas, applicability conditions, decomposable components |
| **Gaps & Assumptions** | Explicit limitations + implicit attackable assumptions |
| **Experimental Patterns** | Baselines, metrics, ablation designs, datasets, validation logic |
| **Cross-Paper Connections** | Complementary, contradictory, extending, combinable relationships |
| **Reusable Resources** | Code, datasets, models, engineering assets |

### 8.5 Episteme File Structure

```
~/Research/Episteme/
├── research-directions.md    ← Your research configuration
├── reading-queue.md          ← discover writes, read consumes
├── kb-index.md               ← Master index of all knowledge
├── domain-landscape.md       ← Generated after threshold of papers read
└── [arxiv-id].md             ← Structured note per paper
```

### 8.6 How Logos Feeds Praxis

Praxis consumes Episteme assets at specific phases:

| Praxis phase | Consumed assets |
|-------------|-----------------|
| formalize | Gaps & Assumptions + Cross-Paper Connections |
| design | Methods Bank + Experimental Patterns + Reusable Resources |

---

## 9. Architecture

### 9.1 Independent State Machines

Each Praxis module has its own state machine. They do not share state:

- Init: `Docs/init-module-status.json`
- Research: `Docs/research-module-status.json`
- Paper: `Papers/paper-status.json`

`pipeline-status.json` only records which module is currently active. State is never inferred from directory structure — only from these JSON files.

### 9.2 Three-Layer Separation

| Layer | Responsibility |
|-------|---------------|
| **Runner** (`*_runner.py`) | Decides what/when, builds fork prompts, injects lessons |
| **Prompts** (`prompts/*.md`) | Pure agent instructions, no state logic |
| **State Machine** (`*_state_machine.py`) | Pure state transitions + I/O, no prompt logic |

### 9.3 Model Configuration

All phases use **opus**.

### 9.4 Git Sync

Git commit + push after every phase completion. This ensures multi-machine collaboration stays in sync and provides full audit trail.

### 9.5 Cross-Project Lessons Pipeline

```
Project completes → /praxis-evolve extracts lessons
                  → ~/.noesis/lessons/<skill_name>.md
                  → Runner auto-injects at matching phases in future projects
                  → [✗ ineffective] filtered, [RECURRING] prioritized
```

### 9.6 X-Reflect

After every non-manual phase, the runner automatically injects a reflection prompt. The agent appends observations about the process itself to `pipeline-evolution-log.md`. These observations are later consumed by `/praxis-evolve` to decide whether framework-level changes are warranted.

---

## 10. Project Directory Structure

### 10.1 Noesis System Repository

```
~/Research/Noesis/
├── Logos/               ← Knowledge accumulation subsystem
│   ├── skills/          ← discover + read skill definitions
│   └── templates/       ← Episteme templates
├── Praxis/              ← Research execution subsystem
│   ├── orchestrator/    ← State machines + runners
│   ├── prompts/         ← Phase-specific agent instructions
│   ├── skills/          ← Non-automated module instructions
│   ├── subagents/       ← Debate agent prompt templates
│   └── templates/       ← Project document templates
├── .claude/skills/      ← Slash command registrations
├── introduction.md      ← This file
├── CLAUDE.md            ← System development guidance
└── README.md
```

### 10.2 Individual Research Project

```
~/Research/<ProjectName>/
├── CLAUDE.md                          ← Project-level Claude guidance
├── project.md                         ← Core project document (§1-§4)
├── pipeline-status.json               ← Active module tracker
├── Docs/
│   ├── init-module-status.json        ← Init state machine
│   └── research-module-status.json    ← Research state machine
├── Reviews/
│   ├── init/                          ← Init review debate records
│   ├── research-formalize/            ← Formalize review records
│   └── research-design/               ← Design review records
├── Codes/
│   ├── probe/                         ← Probe experiment code
│   ├── core/                          ← Deep kernel (reusable algorithms)
│   ├── experiments/                   ← Shallow wrappers (experiment-specific)
│   ├── configs/                       ← Configuration files
│   ├── scripts/                       ← Utility scripts
│   ├── _Data/                         ← Generated data (gitignored)
│   └── _Results/                      ← Experiment results (tracked)
├── Papers/
│   ├── paper-status.json              ← Paper state machine
│   ├── sections/                      ← Individual section drafts
│   └── latex/                         ← LaTeX output
├── research/
│   ├── problem-statement.md
│   ├── method-design.md
│   ├── experiment-design.md
│   ├── contribution.md
│   └── retrospective.md
└── phase-outcomes/                    ← Phase result JSONs
```

### 10.3 Orchestrator CLI Reference

For debugging, recovery, or scripted invocation, you can use the runner CLI directly:

```bash
# Research module
python3 ~/Research/Noesis/Praxis/orchestrator/research_runner.py status  <project_path>
python3 ~/Research/Noesis/Praxis/orchestrator/research_runner.py next    <project_path>
python3 ~/Research/Noesis/Praxis/orchestrator/research_runner.py advance <project_path>
python3 ~/Research/Noesis/Praxis/orchestrator/research_runner.py advance <project_path> --outcome <outcome>

# Paper module
python3 ~/Research/Noesis/Praxis/orchestrator/paper_runner.py status  <project_path>
python3 ~/Research/Noesis/Praxis/orchestrator/paper_runner.py next    <project_path>
python3 ~/Research/Noesis/Praxis/orchestrator/paper_runner.py advance <project_path>

# Force-set phase (recovery)
python3 ~/Research/Noesis/Praxis/orchestrator/research_state_machine.py init-phase <project_path> <phase>
python3 ~/Research/Noesis/Praxis/orchestrator/paper_state_machine.py init-phase <project_path> <phase>
```

Phase outcome files use a minimal format:
```json
{
  "outcome": "<outcome_key>",
  "notes": "Brief human-readable explanation"
}
```

---

## 11. FAQ

### How do I recover from a stuck state?

Use `init-phase` to force-set the state machine to any phase:
```bash
python3 ~/Research/Noesis/Praxis/orchestrator/research_state_machine.py init-phase ~/Research/MyProject formalize
```

### Can I skip phases?

Yes, using `init-phase`. But skipping review phases means losing the multi-agent pressure testing that catches problems early. Not recommended unless you have a specific reason.

### What if my experiments fail?

Run `/praxis-conclude`. It will diagnose whether the failure is at the execution, method, or direction level, and route the rollback accordingly. Then re-run `/praxis-r-auto` to continue from the corrected position.

### Can I run Logos and Praxis simultaneously?

Yes. They are fully independent. You can accumulate knowledge with Logos while a project is mid-execution in Praxis.

### Can I start writing the paper before experiments are done?

Yes. The Paper module is independent. Use `{{PENDING:...}}` placeholders for missing data, then run `/praxis-paper-fill` once results are available.

### How do lessons transfer between projects?

`/praxis-evolve` extracts lessons to `~/.noesis/lessons/`. Runners automatically inject relevant lessons at matching phases in subsequent projects. Ineffective lessons are filtered out automatically.

### What happens when a review says "abandon"?

The system moves to retrospective to recover whatever knowledge is possible, then marks the module complete. No work is wasted — lessons and partial insights are preserved.

### Who is Noesis for?

- PhD students and independent researchers maintaining long-term knowledge bases
- Labs that want research projects to be more institutionalized and trackable
- Individuals or teams running multiple projects who want cross-project learning
- Anyone who wants AI to function as a research system, not just a chat assistant

If you need a one-shot document generator, Noesis is overkill. If you care about **research capability compounding over time**, it was built for that.
