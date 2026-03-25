<div align="center">

# Noesis

### A Research Operating System for the Age of Agents

An AI-driven scientific research framework for **AI/ML/DL** researchers,<br>
running on **Claude Code** with structured state machines, multi-agent review, and cross-project learning.

*noesis (cognition & insight) / logos (knowledge) / praxis (action) / episteme (understanding)*

[![Claude Code](https://img.shields.io/badge/Platform-Claude_Code-blueviolet)](#requirements)
[![Modules](https://img.shields.io/badge/Modules-3_(Init%20%C2%B7%20Research%20%C2%B7%20Paper)-blue)](#modules-overview)
[![Commands](https://img.shields.io/badge/Slash_Commands-28-green)](#command-reference)
[![Reviews](https://img.shields.io/badge/Multi--Agent_Reviews-4%20%26%206%20Agent%20Debates-orange)](#multi-agent-review-system)

</div>

---

## What is Noesis

Noesis is a long-running operational framework that turns AI from a chat assistant into a **structured research system**. It manages the full lifecycle of a research project -- from idea validation through experiments to publication-ready manuscripts -- using auditable state machines, multi-agent debate reviews, and automatic cross-project learning.

The core philosophy: **the researcher commands direction and critical judgment; agents handle high-intensity execution and structured labor.**

---

## System Architecture

```
                          ┌─────────────────────────────────────────────────────────────────┐
                          │                         P R A X I S                              │
                          │                    (Research Execution)                          │
                          │                                                                 │
  L O G O S              │   ┌──────────┐     ┌───────────┐     ┌──────────┐              │
  (Knowledge)    ──────→  │   │   Init   │ ──→ │ Research  │ ──→ │  Paper   │              │
                          │   │ 6 phases │     │ 8 phases  │     │ 7 phases │              │
 /logos-discover          │   └──────────┘     └───────────┘     └──────────┘              │
 /logos-read              │   /praxis-init-auto /praxis-r-auto   /praxis-paper             │
                          └─────────────────────────────────────────────────────────────────┘
       │                                           │
       ▼                                           ▼
  E P I S T E M E                          ~/.noesis/lessons/
  (Knowledge Base)                         (Cross-Project Learning)
```

| Subsystem | Role | Key Fact |
|-----------|------|----------|
| **Logos** | Continuous knowledge accumulation | 5 search strategies, 5 knowledge asset types |
| **Episteme** | Shared knowledge base | Methods Bank, Gaps, Patterns, Connections, Resources |
| **Praxis** | Phased research execution | 3 independent modules, each with its own state machine |

Logos fills Episteme. Praxis consumes it. They run independently -- you can accumulate knowledge while a project is mid-execution.

---

## Quick Start

### 1. Prerequisites

- **Claude Code** (Anthropic CLI)
- **GitHub CLI** (`gh`)
- **Python 3.x**
- macOS recommended (multi-machine sync via git)

### 2. Directory Layout

```
~/Research/
├── Noesis/           ← This repo (central methodology library)
├── Episteme/         ← Knowledge base (Logos output)
└── <ProjectName>/    ← Individual research projects (each its own repo)

~/.noesis/lessons/    ← Cross-project lessons (auto-injected)
```

### 3. Initialize Episteme (first time only)

```bash
KB="$HOME/Research/Episteme"
cp "$HOME/Research/Noesis/Logos/templates/kb-index.md" "$KB/"
cp "$HOME/Research/Noesis/Logos/templates/reading-queue.md" "$KB/"
cp "$HOME/Research/Noesis/Logos/templates/research-directions.md" "$KB/"
# Edit research-directions.md with your directions, keywords, seed papers, venues
```

### 4. Run Your First Project

```bash
# Build knowledge (can run anytime, independently)
/logos-discover
/logos-read 5

# Init: idea → validated direction + probe results
/praxis-init-auto

# Research: direction → complete experiments
/praxis-r-auto ~/Research/MyProject

# Paper: results → publication-ready manuscript
/praxis-paper ~/Research/MyProject

# Evolution: extract lessons for future projects
/praxis-evolve ~/Research/MyProject
```

Already have an in-progress project? Onboard it with:
```bash
/praxis-assimilate ~/Research/ExistingProject
```

---

## Modules Overview

### Init Module -- From Idea to Validated Direction

| Phase | What Happens | Mode |
|-------|-------------|------|
| `init` | Collect idea, papers, notes, or Episteme leads | Auto |
| `start` | Identify seed type, hypothesis, background, SOTA, gaps | Auto |
| `probe_design` | Design minimal probe experiment | Auto |
| `review` | **4-agent debate** pressure test | Auto |
| `probe_impl` | Execute probe experiment | **Manual** |
| `complete` | Direction confirmed, `project.md` finalized | -- |

### Research Module -- From Direction to Complete Experiments

| Phase | What Happens | Mode |
|-------|-------------|------|
| `formalize` | Formal gap, research question, attack angle | Auto |
| `formalize_review` | **4-agent strategic debate**: "Is this worth pursuing?" | Auto |
| `design` | Method + experiment co-design with pilot (Experiment 0) | Auto |
| `design_review` | **6-agent technical debate**: "Is the approach sound?" | Auto |
| `blueprint` | Code architecture + experiment execution checklist | Auto |
| `implement` | Coding + experiments (pilot first, then full) | **Manual** |
| `retrospective` | Knowledge recovery: what worked, failed, and carries forward | Auto |
| `complete` | Module finished | -- |

### Paper Module -- From Results to Manuscript

| Phase | What Happens | Mode |
|-------|-------------|------|
| **P1** Outline | Narrative spine, notation table, section structure | Auto |
| **P2** Sections | Draft each section independently | Auto |
| **P3** Critique | Multi-role critique of the draft | Auto |
| **P4** Integrate | Merge into unified `paper.md` | Auto |
| **P5** Review | Final quality review with scoring (revision loop) | Auto |
| **P6** LaTeX | Generate `main.tex`, `references.bib` | Auto |
| **P7** Project Review | Retrospective review of the entire project | Auto |

P5 scores the manuscript -- if below threshold, it loops back to P4 (max 2 rounds).
Paper can start **before experiments complete** using `{{PENDING:...}}` placeholders, filled later with `/praxis-paper-fill`.

---

## Multi-Agent Review System

Reviews are not advisory -- they **route the state machine**. Outcomes directly determine whether work proceeds, revises, or is abandoned.

### Strategic Review (4 Agents) -- Init & Formalize

| Agent | Perspective |
|-------|------------|
| **Contrarian** | Challenges assumptions, identifies weaknesses |
| **Comparativist** | Compares against alternative approaches |
| **Pragmatist** | Evaluates feasibility and resource constraints |
| **Interdisciplinary** | Cross-field connections and missed angles |

### Technical Review (6 Agents) -- Design

| Agent | Perspective |
|-------|------------|
| **Theorist** | Mathematical and theoretical correctness |
| **Methodologist** | Method design quality |
| **Empiricist** | Experiment design rigor |
| **Skeptic** | Hidden flaws and edge cases |
| **Pragmatist** | Engineering feasibility |
| **Contrarian** | Fundamental objections |

**Review outcomes:** `pass` (proceed) / `revise` (redo current phase) / `fundamental` (escalate rollback) / `abandon` (recover knowledge, then stop)

---

## Command Reference

### Logos (Knowledge Accumulation)

| Command | Description |
|---------|-------------|
| `/logos-discover` | Multi-strategy paper search, update reading queue |
| `/logos-read` | Deep reading + 5-type knowledge asset extraction |

### Praxis -- Init Module

| Command | Description |
|---------|-------------|
| `/praxis-init-auto` | Run full Init flow automatically |
| `/praxis-init` | Manual: init phase |
| `/praxis-start` | Manual: start phase |
| `/praxis-probe-design` | Manual: probe design |
| `/praxis-review` | Manual: run review debate |
| `/praxis-probe-impl` | Manual: execute probe |

### Praxis -- Research Module

| Command | Description |
|---------|-------------|
| `/praxis-r-auto` | Run full Research flow automatically |
| `/praxis-research` | Alias for Research module entry |
| `/praxis-r-formalize` | Manual: formalize phase |
| `/praxis-r-formalize-review` | Manual: formalize review |
| `/praxis-r-design` | Manual: design phase |
| `/praxis-r-design-review` | Manual: design review |
| `/praxis-r-blueprint` | Manual: blueprint phase |
| `/praxis-r-implement` | Manual: implementation |
| `/praxis-r-retrospective` | Manual: retrospective |

### Praxis -- Paper Module

| Command | Description |
|---------|-------------|
| `/praxis-paper` | Run full Paper flow (P1 through P7) |
| `/praxis-paper-fill` | Fill `{{PENDING:...}}` placeholders with real data |

### Praxis -- Code Implementation

| Command | Description |
|---------|-------------|
| `/praxis-code-scaffold` | Generate project code scaffolding |
| `/praxis-code-pipeline` | Build experiment pipeline |
| `/praxis-code-baseline` | Implement baseline methods |
| `/praxis-code-review` | Review code quality |

### Praxis -- Auxiliary

| Command | Description |
|---------|-------------|
| `/praxis-conclude` | Experiment failure diagnosis + layered rollback |
| `/praxis-present` | Generate `presentation.md` for advisor discussions |
| `/praxis-assimilate` | Onboard existing project into Noesis |
| `/praxis-evolve` | Extract cross-project lessons + framework evolution |
| `/praxis-optimize` | Deep prompt/skill optimization |

---

## Project Structure

```
~/Research/<ProjectName>/
├── CLAUDE.md                          ← Project-level guidance
├── project.md                         ← Core project document
├── pipeline-status.json               ← Active module tracker
├── Docs/
│   ├── init-module-status.json        ← Init state machine
│   └── research-module-status.json    ← Research state machine
├── Reviews/
│   ├── init/                          ← Init review debate records
│   ├── research-formalize/            ← Strategic review records
│   └── research-design/               ← Technical review records
├── research/
│   ├── problem-statement.md           ← Gap, RQ, attack angle
│   ├── method-design.md               ← Method specification
│   ├── experiment-design.md           ← Experiment plan
│   ├── contribution.md                ← Contribution summary
│   └── retrospective.md              ← Knowledge recovery
├── Codes/
│   ├── probe/                         ← Probe experiment code
│   ├── core/                          ← Deep kernel (reusable algorithms)
│   ├── experiments/                   ← Shallow wrappers (experiment-specific)
│   ├── _Data/                         ← Generated data (gitignored)
│   └── _Results/                      ← Experiment results (tracked)
└── Papers/
    ├── paper-status.json              ← Paper state machine
    ├── sections/                      ← Individual section drafts
    ├── paper.md                       ← Integrated manuscript
    └── latex/                         ← main.tex, references.bib
```

---

## Design Philosophy

| Principle | What It Means |
|-----------|--------------|
| **Researcher-in-Command** | The researcher defines direction, makes key tradeoffs, and approves critical transitions. AI handles high-intensity execution. Manual phases (probe, implement) keep humans at decision points. |
| **Knowledge-First** | Research knowledge is a persistent system asset, not disposable chat context. Papers read, gaps found, and methods catalogued persist across all projects via Episteme. |
| **Multi-Agent Review Gates** | No major decision passes unchallenged. 4-agent strategic debates test direction viability; 6-agent technical debates test approach soundness. Reviews route state machines, not just generate opinions. |
| **Compute-Resource-Aware** | Probe experiments validate intuition at minimal cost before full investment. Pilot experiments (Experiment 0) run before the full suite. Layered rollback avoids wasting compute on flawed directions. |
| **Recoverable State Machines** | Every module has explicit JSON state. Failures trigger layered rollback to the right level (execution / method / direction). No work is lost -- escalation guards prevent infinite loops. |
| **Cross-Project Compounding** | `/praxis-evolve` extracts lessons tagged by category, frequency, and validity. Runners auto-inject relevant lessons into future projects. Ineffective lessons are filtered out. The framework itself evolves. |

---

## Requirements

| Requirement | Details |
|-------------|---------|
| **Claude Code** | Anthropic's CLI -- the runtime for all Noesis agents |
| **GitHub CLI** | `gh` -- used for repo management and sync |
| **Python 3.x** | Required for orchestrator state machines and runners |
| **macOS** | Recommended; multi-machine sync via git push/pull |

---

## Further Reading

For the complete operational manual -- phase details, orchestrator CLI reference, FAQ, and file conventions -- see **[introduction.md](introduction.md)**.

---

## Acknowledgments

[Sibyl Research System](https://github.com/Sibyl-Research/sibyl-research-system) provided inspiration for parts of the phase design.
