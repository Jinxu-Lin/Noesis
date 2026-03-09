"""Research Pipeline State Machine

Tracks project phase state (R1→R8 + coding/paper_writing) and computes next actions.
Does NOT execute anything — research_runner.py calls this and executes.

Phase numbering (Startup is independent via /praxis-start):
  R1 Gap Discovery → R2 Gap Review → R3 Method Design → R4 Method Review
  → R5 Experiment Design → R6 Experiment Review → R7 Impl Planning
  → R8 Retrospective → coding → paper_writing → complete

Single source of truth: pipeline-status.json
Outcomes: phase-outcomes/<phase>.json (written by fork agents)

CLI:
    python research_state_machine.py next      <project_path>
    python research_state_machine.py advance   <project_path> <phase> <outcome>
    python research_state_machine.py status    <project_path>
    python research_state_machine.py init      <project_path>
    python research_state_machine.py init-phase <project_path> <phase>
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# ─────────────────────────────────────────────────────────────────
# Phase configuration table
# ─────────────────────────────────────────────────────────────────

PHASES = {
    "R1": {
        "skill": "10-gap-discovery",
        "skill_args": "",
        "description": "Phase 1: Gap Discovery — 研究空白发现",
        "output_doc": "gap-analysis.md",
        "outcome_type": "work",
        "tier": "heavy",
        "next": {"done": "R2"},
    },
    "R2": {
        "skill": "1X-review",
        "skill_args": "gap",
        "codex_agent": "codex-reviewer",
        "description": "Phase 2: Gap Review — 研究空白审查 🔒",
        "output_doc": "gap-review.md",
        "outcome_type": "review",
        "tier": "heavy",
        "next": {
            "pass": "R3",
            "revise": "R1",
            "abandon": "R8",
        },
    },
    "R3": {
        "skill": "11-method-design",
        "skill_args": "",
        "description": "Phase 3: Method Design — 方法设计",
        "output_doc": "method-design.md",
        "outcome_type": "work",
        "tier": "heavy",
        "next": {"done": "R4"},
    },
    "R4": {
        "skill": "1X-review",
        "skill_args": "method",
        "codex_agent": "codex-reviewer",
        "description": "Phase 4: Method Review — 方法审查 🔒",
        "output_doc": "method-review.md",
        "outcome_type": "review",
        "tier": "heavy",
        "next": {
            "pass": "R5",
            "revise": "R3",
            "continue_R1": "R1",
            "abandon": "R8",
        },
    },
    "R5": {
        "skill": "12-experiment-design",
        "skill_args": "",
        "description": "Phase 5: Experiment Design — 实验设计",
        "output_doc": "experiment-design.md",
        "outcome_type": "work",
        "tier": "heavy",
        "next": {"done": "R6"},
    },
    "R6": {
        "skill": "1X-review",
        "skill_args": "experiment",
        "codex_agent": "codex-reviewer",
        "description": "Phase 6: Experiment Review — 实验审查 🔒",
        "output_doc": "experiment-review.md",
        "outcome_type": "review",
        "tier": "heavy",
        "next": {
            "pass": "R7",
            "revise": "R5",
            "continue_R3": "R3",
            "abandon": "R8",
        },
    },
    "R7": {
        "skill": "13-impl-planning",
        "skill_args": "",
        "description": "Phase 7: Implementation Planning — 实验规划",
        "output_doc": None,
        "outcome_type": "work",
        "tier": "standard",
        "next": {"done": "R8"},
    },
    "R8": {
        "skill": "14-retrospective",
        "skill_args": "",
        "description": "Phase 8: Research Retrospective — 研究设计回顾与知识回收",
        "output_doc": "retrospective.md",
        "outcome_type": "work",
        "tier": "heavy",
        "next": {"done": "coding"},
    },
    "coding": {
        "skill": None,
        "skill_args": "",
        "description": "Code & Experiment — 人工编码与实验阶段",
        "output_doc": None,
        "outcome_type": "manual",
        "tier": None,
        "next": {
            "success": "paper_writing",
            "iterate_R3": "R3",
            "iterate_R1": "R1",
            "abandon": "complete",
        },
    },
    "paper_writing": {
        "skill": None,
        "skill_args": "",
        "description": "Paper Writing — 论文写作阶段",
        "output_doc": None,
        "outcome_type": "manual",
        "tier": None,
        "next": {
            "done": "complete",
        },
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
HUMAN_CHECKPOINT_PHASES = set()  # no auto-checkpoint phases currently


# ─────────────────────────────────────────────────────────────────
# Status I/O
# ─────────────────────────────────────────────────────────────────

STATUS_FILE = "pipeline-status.json"


def get_status(project_path: Path) -> dict:
    f = project_path / STATUS_FILE
    if f.exists():
        return json.loads(f.read_text(encoding="utf-8"))
    # No status file → fresh project, start at R1
    return {"phase": "R1", "initialized": False}


def save_status(project_path: Path, status: dict) -> None:
    status["last_updated"] = datetime.now().isoformat()
    f = project_path / STATUS_FILE
    f.write_text(json.dumps(status, indent=2, ensure_ascii=False), encoding="utf-8")


# ─────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────

def get_next_action(project_path_str: str) -> dict:
    """Return the next action for the runner to execute."""
    path = Path(project_path_str)
    status = get_status(path)
    phase = status.get("phase", "R1")
    cfg = PHASES.get(phase)

    if not cfg:
        return {"action_type": "error", "message": f"Unknown phase: {phase}",
                "status": status}

    if cfg["outcome_type"] == "terminal":
        return {"action_type": "done",
                "description": "Pipeline complete — 研究全流程已完成 ✓",
                "phase": phase}

    if cfg["outcome_type"] == "manual":
        messages = {
            "coding": (
                "当前处于人工编码与实验阶段。\n"
                "请与 AI 协作完成代码编写和实验运行（参考 Codes/ 目录）。\n"
                "完成后：\n"
                "  - 验证通过 → 运行 /praxis-paper <path> 启动论文写作\n"
                "  - 验证失败 → 运行 /praxis-conclude <path> 进行总结并重启研究"
            ),
            "paper_writing": (
                "当前处于论文写作阶段。\n"
                "请运行 /praxis-paper <path> 启动论文写作模块（P1→P7）。\n"
                "完成后：\n"
                "  - 运行 /praxis-evolve <path> 提取跨项目经验教训"
            ),
        }
        return {
            "action_type": "manual",
            "phase": phase,
            "description": cfg["description"],
            "message": messages.get(phase, f"当前处于 {phase} 阶段。"),
        }

    requires_human = phase in HUMAN_CHECKPOINT_PHASES
    return {
        "action_type": "skill",
        "phase": phase,
        "skill_name": cfg["skill"],
        "skill_args": cfg.get("skill_args", ""),
        "codex_agent": cfg.get("codex_agent"),  # optional: triggers skills_parallel in runner
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

    outcome_key = outcome.strip()
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
        status = {"phase": "R1", "notes": "manually initialized"}
        save_status(path, status)
        result = {"initialized": True, "phase": "R1", "project": str(path)}

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
