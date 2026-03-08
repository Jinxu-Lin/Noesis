"""ResearchFlow Pipeline State Machine

Tracks project phase state and computes next actions.
Does NOT execute anything — the runner Skill calls this and executes.

CLI:
    python state_machine.py next   <project_path>
    python state_machine.py advance <project_path> <phase> <outcome>
    python state_machine.py status  <project_path>
    python state_machine.py init    <project_path>
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path

# ─────────────────────────────────────────────────────────────────
# Phase configuration table
# ─────────────────────────────────────────────────────────────────

PHASES = {
    "P1": {
        "skill": "project-startup",
        "skill_args": "",
        "description": "Phase 1: Project Startup — 项目启动",
        "output_doc": "project-startup.md",
        "outcome_type": "work",
        "tier": "standard",
        "next": {"done": "P2"},
    },
    "P2": {
        "skill": "gap-discovery",
        "skill_args": "",
        "description": "Phase 2: Gap Discovery — 研究空白发现",
        "output_doc": "gap-analysis.md",
        "outcome_type": "work",
        "tier": "standard",
        "next": {"done": "P3"},
    },
    "P3": {
        "skill": "review",
        "skill_args": "gap",
        "description": "Phase 3: Gap Review — 研究空白审查 🔒",
        "output_doc": "gap-review.md",
        "outcome_type": "review",
        "tier": "heavy",
        "next": {
            "pass": "P4",
            "revise": "P2",
            "continue_P1": "P1",
            "abandon": "P11",
        },
    },
    "P4": {
        "skill": "method-design",
        "skill_args": "",
        "description": "Phase 4: Method Design — 方法设计",
        "output_doc": "method-design.md",
        "outcome_type": "work",
        "tier": "standard",
        "next": {"done": "P5"},
    },
    "P5": {
        "skill": "review",
        "skill_args": "method",
        "description": "Phase 5: Method Review — 方法审查 🔒",
        "output_doc": "method-review.md",
        "outcome_type": "review",
        "tier": "heavy",
        "next": {
            "pass": "P6",
            "revise": "P4",
            "continue_P2": "P2",
            "abandon": "P11",
        },
    },
    "P6": {
        "skill": "experiment-design",
        "skill_args": "",
        "description": "Phase 6: Experiment Design — 实验设计",
        "output_doc": "experiment-design.md",
        "outcome_type": "work",
        "tier": "standard",
        "next": {"done": "P7"},
    },
    "P7": {
        "skill": "review",
        "skill_args": "experiment",
        "description": "Phase 7: Experiment Review — 实验审查 🔒",
        "output_doc": "experiment-review.md",
        "outcome_type": "review",
        "tier": "heavy",
        "next": {
            "pass": "P8a",
            "revise": "P6",
            "continue_P4": "P4",
            "abandon": "P11",
        },
    },
    "P8a": {
        "skill": "impl-setup",
        "skill_args": "",
        "description": "Phase 8a: Implementation Setup — 环境搭建与 baseline 复现",
        "output_doc": None,
        "outcome_type": "work",
        "tier": "standard",
        "next": {"done": "P8a_validate"},
    },
    "P8a_validate": {
        "skill": "impl-validate",
        "skill_args": "",
        "description": "Phase 8a: Core Implementation & Dim 0 Validation — 核心实现与快速验证",
        "output_doc": None,
        "outcome_type": "impl_validate",
        "tier": "standard",
        "next": {
            "pass": "P8b",
            "L1": "P8a_validate",
            "continue_P4": "P4",
            "continue_P2": "P2",
            "abandon": "P11",
        },
    },
    "P8b": {
        "skill": "impl-full",
        "skill_args": "",
        "description": "Phase 8b: Full Experiments — 完整实验 (Dim 1-4)",
        "output_doc": None,
        "outcome_type": "impl_full",
        "tier": "standard",
        "next": {
            "done": "P9",
            "continue_P4": "P4",
            "continue_P2": "P2",
            "abandon": "P11",
        },
    },
    "P9": {
        "skill": "paper-writing",
        "skill_args": "",
        "description": "Phase 9: Paper Writing — 论文撰写",
        "output_doc": "Papers/",
        "outcome_type": "work",
        "tier": "standard",
        "next": {"done": "P11"},
    },
    "P11": {
        "skill": "retrospective",
        "skill_args": "",
        "description": "Phase 11: Project Retrospective — 项目回顾与知识回收",
        "output_doc": "retrospective.md",
        "outcome_type": "work",
        "tier": "heavy",      # needs synthesis across the whole project
        "next": {"done": "complete"},
    },
    "complete": {
        "skill": None,
        "description": "Pipeline complete — 研究流程已完成",
        "outcome_type": "terminal",
        "next": {},
    },
}

# Phases that require human confirmation before auto-proceeding
# (runner will pause and ask user before spawning the next fork agent)
HUMAN_CHECKPOINT_PHASES = {
    "P8a",          # involves code execution, environment setup
    "P8a_validate", # involves actual model training/experimentation
    "P8b",          # full GPU experiments
}


# ─────────────────────────────────────────────────────────────────
# Status I/O
# ─────────────────────────────────────────────────────────────────

STATUS_FILE = "pipeline-status.json"


def get_status(project_path: Path) -> dict:
    f = project_path / STATUS_FILE
    if f.exists():
        return json.loads(f.read_text(encoding="utf-8"))
    return _auto_detect(project_path)


def save_status(project_path: Path, status: dict) -> None:
    status["last_updated"] = datetime.now().isoformat()
    f = project_path / STATUS_FILE
    f.write_text(json.dumps(status, indent=2, ensure_ascii=False), encoding="utf-8")


def _auto_detect(project_path: Path) -> dict:
    """Infer current phase by scanning existing output documents."""
    checks = [
        ("retrospective.md",    "complete"),
        ("Papers/",             "P11"),
        ("experiment-review.md","_review_P7"),
        ("experiment-design.md","P7"),
        ("method-review.md",    "_review_P5"),
        ("method-design.md",    "P5"),
        ("gap-review.md",       "_review_P3"),
        ("gap-analysis.md",     "P3"),
        ("project-startup.md",  "P2"),
    ]
    for doc, phase_hint in checks:
        p = project_path / doc
        if p.exists():
            if phase_hint.startswith("_review_"):
                src_phase = phase_hint[8:]   # e.g. "P7"
                verdict = _parse_review_verdict(p)
                if verdict == "pass":
                    # Map review phase to the next work phase
                    nxt = PHASES[src_phase]["next"].get("pass", src_phase)
                    return {"phase": nxt, "auto_detected": True}
                elif verdict == "revise":
                    nxt = PHASES[src_phase]["next"].get("revise", src_phase)
                    return {"phase": nxt, "auto_detected": True}
                elif verdict in ("block", "unknown"):
                    # Stay at review phase for human to inspect
                    return {"phase": src_phase, "auto_detected": True,
                            "warning": f"Review verdict unclear in {doc}"}
                return {"phase": src_phase, "auto_detected": True}
            else:
                return {"phase": phase_hint, "auto_detected": True}
    return {"phase": "P1", "auto_detected": True, "notes": "no documents found"}


# ─────────────────────────────────────────────────────────────────
# Verdict / outcome detection
# ─────────────────────────────────────────────────────────────────

def _parse_review_verdict(doc: Path) -> str:
    """Extract Pass/Revise/Block from a review document."""
    if not doc.exists():
        return "unknown"
    txt = doc.read_text(encoding="utf-8")
    for pattern, verdict in [
        (r'整体判定\s*[：:]\s*\*?\s*Pass',   "pass"),
        (r'整体判定\s*[：:]\s*\*?\s*Revise', "revise"),
        (r'整体判定\s*[：:]\s*\*?\s*Block',  "block"),
        (r'\*\*整体判定\*\*\s*[：:]\s*Pass',   "pass"),
        (r'\*\*整体判定\*\*\s*[：:]\s*Revise', "revise"),
        (r'\*\*整体判定\*\*\s*[：:]\s*Block',  "block"),
        (r'判定\s*[：:]\s*Pass\b',  "pass"),
        (r'判定\s*[：:]\s*Revise\b', "revise"),
        (r'判定\s*[：:]\s*Block\b',  "block"),
        (r'\bPass\b',   "pass"),
        (r'\bRevise\b', "revise"),
        (r'\bBlock\b',  "block"),
    ]:
        if re.search(pattern, txt, re.IGNORECASE):
            return verdict
    return "unknown"


def read_phase_outcome(project_path: Path, phase: str) -> dict:
    """Read the outcome written by the fork agent after phase completion.

    Fork agents write to: phase-outcomes/<phase>.json
    Format: {"outcome": "pass|revise|done|...", "notes": "..."}
    """
    outcome_dir = project_path / "phase-outcomes"
    outcome_file = outcome_dir / f"{phase}.json"
    if outcome_file.exists():
        try:
            return json.loads(outcome_file.read_text(encoding="utf-8"))
        except Exception:
            pass
    # Fallback: try to infer from review documents
    phase_cfg = PHASES.get(phase, {})
    output_doc = phase_cfg.get("output_doc")
    outcome_type = phase_cfg.get("outcome_type", "work")

    if outcome_type == "review" and output_doc:
        verdict = _parse_review_verdict(project_path / output_doc)
        return {"outcome": verdict, "inferred": True}
    elif outcome_type == "work":
        # Check if output doc exists
        if output_doc and (project_path / output_doc).exists():
            return {"outcome": "done", "inferred": True}
    return {"outcome": "unknown", "inferred": True}


# ─────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────

def get_next_action(project_path_str: str) -> dict:
    """Return the next action for the runner to execute."""
    path = Path(project_path_str)
    status = get_status(path)
    phase = status.get("phase", "P1")
    cfg = PHASES.get(phase)

    if not cfg:
        return {"action_type": "error", "message": f"Unknown phase: {phase}",
                "status": status}

    if cfg["outcome_type"] == "terminal":
        return {"action_type": "done",
                "description": "Pipeline complete — 研究全流程已完成 ✓",
                "phase": phase}

    requires_human = phase in HUMAN_CHECKPOINT_PHASES
    return {
        "action_type": "skill",
        "phase": phase,
        "skill_name": cfg["skill"],
        "skill_args": cfg.get("skill_args", ""),
        "description": cfg["description"],
        "output_doc": cfg.get("output_doc"),
        "outcome_type": cfg["outcome_type"],
        "tier": cfg.get("tier", "standard"),
        "requires_human_checkpoint": requires_human,
        "iteration_count": status.get(f"iter_{phase}", 0),
    }


def advance(project_path_str: str, phase: str, outcome: str) -> dict:
    """Advance state machine: record outcome and set next phase."""
    path = Path(project_path_str)
    status = get_status(path)
    cfg = PHASES.get(phase, {})
    transitions = cfg.get("next", {})

    outcome_key = outcome.lower().strip()
    next_phase = transitions.get(outcome_key)

    if next_phase is None:
        # Unknown outcome — stay in place and flag it
        return {
            "error": f"No transition from {phase} on outcome '{outcome}'",
            "valid_outcomes": list(transitions.keys()),
            "phase_unchanged": phase,
        }

    # Update status
    iter_key = f"iter_{phase}"
    status[iter_key] = status.get(iter_key, 0) + 1
    status.setdefault("history", []).append({
        "phase": phase,
        "outcome": outcome,
        "timestamp": datetime.now().isoformat(),
    })
    status["phase"] = next_phase
    save_status(path, status)

    return {
        "from_phase": phase,
        "outcome": outcome,
        "next_phase": next_phase,
        "iteration_count": status[iter_key],
    }


# ─────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────

def _cli():
    args = sys.argv[1:]
    if not args:
        print(json.dumps({"error": "Usage: state_machine.py <cmd> <project_path> [args]"}))
        sys.exit(1)

    cmd = args[0]

    if cmd == "next" and len(args) >= 2:
        result = get_next_action(args[1])

    elif cmd == "advance" and len(args) >= 4:
        result = advance(args[1], args[2], args[3])

    elif cmd == "status" and len(args) >= 2:
        result = get_status(Path(args[1]))

    elif cmd == "init" and len(args) >= 2:
        path = Path(args[1])
        status = {"phase": "P1", "notes": "manually initialized"}
        save_status(path, status)
        result = {"initialized": True, "phase": "P1", "project": str(path)}

    elif cmd == "init-phase" and len(args) >= 3:
        path = Path(args[1])
        target_phase = args[2]
        if target_phase not in PHASES:
            result = {"error": f"Unknown phase: {target_phase}",
                      "valid": list(PHASES.keys())}
        else:
            status = get_status(path)
            prev = status.get("phase", "?")
            status["phase"] = target_phase
            status.setdefault("history", []).append({
                "phase": prev, "outcome": f"goto:{target_phase}",
                "timestamp": datetime.now().isoformat(),
            })
            save_status(path, status)
            result = {"forced_phase": target_phase, "previous": prev}

    elif cmd == "detect-outcome" and len(args) >= 3:
        path = Path(args[1])
        phase = args[2]
        result = read_phase_outcome(path, phase)

    elif cmd == "phases":
        result = {
            phase: {"description": cfg["description"], "outcome_type": cfg["outcome_type"]}
            for phase, cfg in PHASES.items()
        }

    else:
        result = {"error": f"Unknown command: {cmd}",
                  "usage": "next|advance|status|init|detect-outcome|phases"}
        sys.exit(1)

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    _cli()
