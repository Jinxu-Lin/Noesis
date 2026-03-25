"""Paper Writing State Machine

Tracks paper writing phase state (P1-P7), independent from the main pipeline.
State stored in: <project>/Papers/paper-status.json

P1 Outline → P2 Sections → P3 Critique → P4 Integrate → P5 Review → P6 LaTeX → P7 Project Review
                                           ↑                │
                                           └── revise ──────┘ (max 2 rounds)

CLI:
    python paper_state_machine.py next    <project_path>
    python paper_state_machine.py advance <project_path> <phase> <outcome>
    python paper_state_machine.py status  <project_path>
    python paper_state_machine.py init    <project_path>
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# ─────────────────────────────────────────────────────────────────
# Phase configuration table
# ─────────────────────────────────────────────────────────────────

PHASES = {
    "P1": {
        "skill": "30-paper-outline",
        "skill_args": "",
        "description": "P1: Paper Outline — 论文大纲生成",
        "outcome_type": "work",
        "tier": "heavy",
        "next": {"done": "P2"},
    },
    "P2": {
        "skill": "31-paper-sections",
        "skill_args": "",
        "description": "P2: Section Writing — 章节顺序写作",
        "outcome_type": "work",
        "tier": "standard",
        "next": {"done": "P3"},
    },
    "P3": {
        "skill": "32-paper-critique",
        "skill_args": "",
        "codex_agent": "codex-reviewer",
        "description": "P3: Cross-Review Critique — 多角色并行审查 🔒",
        "outcome_type": "work",
        "tier": "heavy",
        "next": {"done": "P4"},
    },
    "P4": {
        "skill": "33-paper-integrate",
        "skill_args": "",
        "description": "P4: Integration & Editing — 编辑整合",
        "outcome_type": "work",
        "tier": "standard",
        "next": {"done": "P5"},
    },
    "P5": {
        "skill": "34-paper-review",
        "skill_args": "",
        "description": "P5: Final Review — 会议级终审 🔒",
        "outcome_type": "paper_review",
        "tier": "heavy",
        "next": {
            "pass": "P6",
            "revise": "P4",
        },
    },
    "P6": {
        "skill": "35-paper-latex",
        "skill_args": "",
        "description": "P6: LaTeX Compilation — LaTeX 编译",
        "outcome_type": "work",
        "tier": "standard",
        "next": {"done": "P7"},
    },
    "P7": {
        "skill": "36-project-review",
        "skill_args": "",
        "codex_agent": "codex-reviewer",
        "description": "P7: Project-Level Review — 项目级多视角审查 🔒",
        "outcome_type": "work",
        "tier": "heavy",
        "next": {"done": "complete"},
    },
    "complete": {
        "skill": None,
        "skill_args": "",
        "description": "Paper writing complete — 论文写作完成",
        "outcome_type": "terminal",
        "next": {},
    },
}

MAX_REVISION_ROUNDS = 2

# ─────────────────────────────────────────────────────────────────
# Status I/O
# ─────────────────────────────────────────────────────────────────

STATUS_FILE = "Papers/paper-status.json"


def get_status(project_path: Path) -> dict:
    f = project_path / STATUS_FILE
    if f.exists():
        return json.loads(f.read_text(encoding="utf-8"))
    return {"phase": "P1", "initialized": False}


def save_status(project_path: Path, status: dict) -> None:
    status["last_updated"] = datetime.now().isoformat()
    f = project_path / STATUS_FILE
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(status, indent=2, ensure_ascii=False), encoding="utf-8")


# ─────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────

def get_next_action(project_path_str: str) -> dict:
    """Return the next action for the paper runner to execute."""
    path = Path(project_path_str)
    status = get_status(path)
    phase = status.get("phase", "P1")
    cfg = PHASES.get(phase)

    if not cfg:
        return {"action_type": "error", "message": f"Unknown paper phase: {phase}",
                "status": status}

    if cfg["outcome_type"] == "terminal":
        return {"action_type": "done",
                "description": "Paper writing complete — 论文写作完成 ✓",
                "phase": phase}

    # Revision guard for P5
    revision_count = status.get("revision_rounds", 0)
    revision_warning = None
    if phase == "P5" and revision_count >= MAX_REVISION_ROUNDS:
        revision_warning = (
            f"⚠️  已达到最大修订轮数 ({MAX_REVISION_ROUNDS})。"
            f"本轮 Final Review 将强制通过，不再回退修订。"
        )

    return {
        "action_type": "skill",
        "phase": phase,
        "skill_name": cfg["skill"],
        "skill_args": cfg.get("skill_args", ""),
        "codex_agent": cfg.get("codex_agent"),
        "description": cfg["description"],
        "outcome_type": cfg["outcome_type"],
        "tier": cfg.get("tier", "standard"),
        "iteration_count": status.get(f"iter_{phase}", 0),
        "revision_rounds": revision_count,
        "revision_warning": revision_warning,
    }


def advance(project_path_str: str, phase: str, outcome: str) -> dict:
    """Advance paper state machine: record outcome and set next phase."""
    path = Path(project_path_str)
    status = get_status(path)
    cfg = PHASES.get(phase, {})
    transitions = cfg.get("next", {})

    outcome_key = outcome.strip()

    # Revision guard: force pass if max rounds reached
    if phase == "P5" and outcome_key == "revise":
        revision_count = status.get("revision_rounds", 0)
        if revision_count >= MAX_REVISION_ROUNDS:
            outcome_key = "pass"

    next_phase = transitions.get(outcome_key)

    if next_phase is None:
        return {
            "error": f"No transition from {phase} on outcome '{outcome}'",
            "valid_outcomes": list(transitions.keys()),
            "phase_unchanged": phase,
        }

    # Track revision rounds
    if phase == "P5" and outcome_key == "revise":
        status["revision_rounds"] = status.get("revision_rounds", 0) + 1

    # Update status
    iter_key = f"iter_{phase}"
    status[iter_key] = status.get(iter_key, 0) + 1
    status.setdefault("history", []).append({
        "phase": phase,
        "outcome": outcome_key,
        "timestamp": datetime.now().isoformat(),
    })
    status["phase"] = next_phase
    save_status(path, status)

    return {
        "from_phase": phase,
        "outcome": outcome_key,
        "next_phase": next_phase,
        "iteration_count": status[iter_key],
        "revision_rounds": status.get("revision_rounds", 0),
    }


# ─────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────

def _cli():
    args = sys.argv[1:]
    if not args:
        print(json.dumps({"error": "Usage: paper_machine.py <cmd> <project_path> [args]"}))
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
        status = {"phase": "P1", "revision_rounds": 0}
        save_status(path, status)
        # Update top-level pipeline-status.json
        pipeline_file = path / "pipeline-status.json"
        if pipeline_file.exists():
            pipeline = json.loads(pipeline_file.read_text(encoding="utf-8"))
        else:
            pipeline = {"module_history": []}
        pipeline["active_module"] = "paper"
        pipeline["last_updated"] = datetime.now().isoformat()
        pipeline_file.write_text(json.dumps(pipeline, indent=2, ensure_ascii=False), encoding="utf-8")
        result = {"initialized": True, "phase": "P1", "project": str(path)}

    elif cmd == "init-phase" and len(args) >= 3:
        path = Path(args[1])
        target_phase = args[2]
        if target_phase not in PHASES:
            result = {"error": f"Unknown paper phase: {target_phase}",
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

    elif cmd == "phases":
        result = {
            phase: {"description": cfg["description"], "outcome_type": cfg["outcome_type"]}
            for phase, cfg in PHASES.items()
        }

    else:
        result = {"error": f"Unknown command: {cmd}",
                  "usage": "next|advance|status|init|init-phase|phases"}
        sys.exit(1)

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    _cli()
