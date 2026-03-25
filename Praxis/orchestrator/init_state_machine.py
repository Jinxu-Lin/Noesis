"""Init Module State Machine — v2

Tracks init module phase state: init → start → probe_design → review → probe_impl → complete
Does NOT execute anything — init_runner.py calls this and executes.

State file: Docs/init-module-status.json
Outcomes: phase-outcomes/<phase>.json (written by fork agents)

CLI:
    python init_state_machine.py next       <project_path>
    python init_state_machine.py advance    <project_path> [--outcome <outcome>]
    python init_state_machine.py status     <project_path>
    python init_state_machine.py init       <project_path>
    python init_state_machine.py init-phase <project_path> <phase>
    python init_state_machine.py rollback   <project_path> --phase <phase> --mode <mode> [--context <file>]
    python init_state_machine.py phases
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# ─────────────────────────────────────────────────────────────────
# Phase configuration table
# ─────────────────────────────────────────────────────────────────

PHASES = {
    "init": {
        "skill": "init-setup",
        "description": "项目初始化 — 目录结构 + 上下文提取 + Git",
        "output_doc": "project.md",
        "outcome_type": "work",
        "next": {
            "done": "start",
        },
    },
    "start": {
        "skill": "start-analysis",
        "description": "核心分析 — Baseline + 问题定义 + Root Cause + 方法",
        "output_doc": "project.md",
        "outcome_type": "work",
        "next": {
            "done": "probe_design",
        },
    },
    "probe_design": {
        "skill": "probe-design",
        "description": "验证策略设计 — Probe 实验方案",
        "output_doc": "project.md",
        "outcome_type": "work",
        "next": {
            "done": "review",
        },
    },
    "review": {
        "skill": "init-review",
        "description": "多视角压力测试 — 6 Agent 辩论 + 综合判定",
        "output_doc": None,
        "outcome_type": "review",
        "debate_agents": [
            "innovator", "pragmatist", "theorist",
            "contrarian", "interdisciplinary", "empiricist",
        ],
        "next": {
            "pass": "probe_impl",   # review 通过 → 实现 probe 代码
            "revise": "start",      # entry_context: review_revise
            "hold": "hold",
            "stop": "complete",
        },
    },
    "probe_impl": {
        "skill": "probe-impl",
        "description": "探针实验实现 — 编写 Probe 代码 + Dry Run 验证",
        "output_doc": None,
        "outcome_type": "probe_impl",
        "next": {
            "done": "complete",
            "infeasible": "probe_design",  # 实现中发现设计不可行 → 重新设计
        },
    },
    "hold": {
        "skill": None,             # manual: waiting for user input
        "description": "暂停 — 等待补充关键信息",
        "output_doc": None,
        "outcome_type": "manual",
        "next": {
            "resume": "review",
        },
    },
    "complete": {
        "skill": None,
        "description": "Init Module 完成",
        "outcome_type": "terminal",
        "next": {},
    },
}


# ─────────────────────────────────────────────────────────────────
# Status I/O
# ─────────────────────────────────────────────────────────────────

STATUS_DIR = "Docs"
STATUS_FILE = "init-module-status.json"
PIPELINE_STATUS_FILE = "pipeline-status.json"


def _status_path(project_path: Path) -> Path:
    return project_path / STATUS_DIR / STATUS_FILE


def get_status(project_path: Path) -> dict:
    f = _status_path(project_path)
    if f.exists():
        return json.loads(f.read_text(encoding="utf-8"))
    return {"phase": "init", "initialized": False}


def save_status(project_path: Path, status: dict) -> None:
    status["last_updated"] = datetime.now().isoformat()
    f = _status_path(project_path)
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(status, indent=2, ensure_ascii=False), encoding="utf-8")


def _update_pipeline_status(project_path: Path, module: str = "init") -> None:
    """Update top-level pipeline-status.json."""
    f = project_path / PIPELINE_STATUS_FILE
    if f.exists():
        pipeline = json.loads(f.read_text(encoding="utf-8"))
    else:
        pipeline = {"active_module": module, "module_history": []}

    pipeline["active_module"] = module
    pipeline["last_updated"] = datetime.now().isoformat()
    f.write_text(json.dumps(pipeline, indent=2, ensure_ascii=False), encoding="utf-8")


# ─────────────────────────────────────────────────────────────────
# Entry context computation
# ─────────────────────────────────────────────────────────────────

def _compute_entry_context(phase: str, outcome: str, status: dict) -> dict | None:
    """Compute entry_context for the target phase based on transition."""
    history = status.get("history", [])
    review_count = sum(1 for h in history if h.get("phase") == "review")

    # review → start (revise)
    if phase == "review" and outcome == "revise":
        return {
            "mode": "review_revise",
            "source": "review",
            "review_round": review_count + 1,
        }

    return None


# ─────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────

def get_next_action(project_path_str: str) -> dict:
    """Return the next action for the runner to execute."""
    path = Path(project_path_str)
    status = get_status(path)
    phase = status.get("phase", "init")
    cfg = PHASES.get(phase)

    if not cfg:
        return {"action_type": "error", "message": f"Unknown phase: {phase}",
                "status": status}

    if cfg["outcome_type"] == "terminal":
        decision = status.get("decision", "unknown")
        return {"action_type": "done",
                "description": f"Init Module 完成 — 判定: {decision}",
                "phase": phase, "decision": decision}

    if cfg["outcome_type"] == "manual":
        return {
            "action_type": "manual",
            "phase": phase,
            "description": cfg["description"],
            "message": f"当前处于 {phase} 阶段（手动）。",
        }

    # Compute iteration count from history
    history = status.get("history", [])
    iter_count = sum(1 for h in history if h.get("phase") == phase)

    result = {
        "action_type": "skill",
        "phase": phase,
        "skill_name": cfg["skill"],
        "description": cfg["description"],
        "output_doc": cfg.get("output_doc"),
        "outcome_type": cfg["outcome_type"],
        "debate_agents": cfg.get("debate_agents"),
        "iteration_count": iter_count,
        "entry_context": status.get("entry_context"),
    }
    return result


def advance(project_path_str: str, phase: str, outcome: str) -> dict:
    """Advance state machine: record outcome and set next phase."""
    path = Path(project_path_str)
    status = get_status(path)
    cfg = PHASES.get(phase, {})
    transitions = cfg.get("next", {})

    outcome_key = outcome.strip()
    next_phase = transitions.get(outcome_key)

    if next_phase is None:
        return {
            "error": f"No transition from {phase} on outcome '{outcome}'",
            "valid_outcomes": list(transitions.keys()),
            "phase_unchanged": phase,
        }

    # Compute entry_context for target phase
    entry_context = _compute_entry_context(phase, outcome_key, status)

    # Record history
    history_entry = {
        "phase": phase,
        "outcome": outcome_key,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "timestamp": datetime.now().isoformat(),
    }
    if entry_context and entry_context.get("mode"):
        history_entry["mode"] = entry_context["mode"]
    if phase == "review":
        review_count = sum(1 for h in status.get("history", []) if h.get("phase") == "review")
        history_entry["review_round"] = review_count + 1

    status.setdefault("history", []).append(history_entry)

    # Update status
    status["phase"] = next_phase
    if entry_context:
        status["entry_context"] = entry_context
    else:
        status.pop("entry_context", None)

    # Record decision for terminal transitions
    if phase == "review" and outcome_key == "stop":
        status["decision"] = "Stop"
    if phase == "probe_impl" and outcome_key == "done":
        status["decision"] = "Pass"

    save_status(path, status)

    return {
        "from_phase": phase,
        "outcome": outcome_key,
        "next_phase": next_phase,
        "entry_context": entry_context,
    }


def rollback(project_path_str: str, target_phase: str, mode: str,
             context_file: str | None = None) -> dict:
    """Rollback to a specific phase with context (e.g., probe failure from later module)."""
    path = Path(project_path_str)
    status = get_status(path)

    if target_phase not in PHASES:
        return {"error": f"Unknown phase: {target_phase}"}

    prev_phase = status.get("phase", "?")

    # Record rollback in history
    status.setdefault("history", []).append({
        "phase": prev_phase,
        "outcome": f"rollback:{target_phase}",
        "mode": mode,
        "timestamp": datetime.now().isoformat(),
    })

    # Set new phase and entry_context
    status["phase"] = target_phase
    status["entry_context"] = {
        "mode": mode,
        "source": "external_rollback",
        "context_file": context_file,
    }

    save_status(path, status)

    # Update pipeline-status to point back to init module
    _update_pipeline_status(path, "init")

    return {
        "rollback_to": target_phase,
        "mode": mode,
        "previous_phase": prev_phase,
    }


# ─────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────

def _cli():
    args = sys.argv[1:]
    if not args:
        print(json.dumps({"error": "Usage: init_state_machine.py <cmd> <project_path> [args]"}))
        sys.exit(1)

    cmd = args[0]

    if cmd == "next" and len(args) >= 2:
        result = get_next_action(args[1])

    elif cmd == "advance" and len(args) >= 2:
        path = Path(args[1])
        status = get_status(path)
        phase = status.get("phase", "init")
        # Check for --outcome flag
        manual_outcome = None
        if "--outcome" in args:
            idx = args.index("--outcome")
            if idx + 1 < len(args):
                manual_outcome = args[idx + 1]
        if manual_outcome:
            result = advance(args[1], phase, manual_outcome)
        else:
            # Read from outcome file
            outcome_file = path / "phase-outcomes" / f"{phase}.json"
            if not outcome_file.exists():
                result = {"error": "outcome_file_missing", "phase": phase}
            else:
                try:
                    data = json.loads(outcome_file.read_text(encoding="utf-8"))
                    outcome = data.get("outcome", "unknown")
                    if outcome == "unknown":
                        result = {"error": "outcome_unknown", "phase": phase}
                    else:
                        result = advance(args[1], phase, outcome)
                        result["notes"] = data.get("notes", "")
                except Exception as e:
                    result = {"error": str(e), "phase": phase}

    elif cmd == "status" and len(args) >= 2:
        result = get_status(Path(args[1]))

    elif cmd == "init" and len(args) >= 2:
        path = Path(args[1])
        status = {"phase": "init", "initialized": True,
                  "notes": "init module initialized", "history": []}
        save_status(path, status)
        _update_pipeline_status(path, "init")
        result = {"initialized": True, "phase": "init"}

    elif cmd == "init-phase" and len(args) >= 3:
        path = Path(args[1])
        target = args[2]
        if target not in PHASES:
            result = {"error": f"Unknown phase: {target}", "valid": list(PHASES.keys())}
        else:
            status = get_status(path)
            prev = status.get("phase", "?")
            status["phase"] = target
            status.pop("entry_context", None)
            if prev != target:
                status.setdefault("history", []).append({
                    "phase": prev, "outcome": f"goto:{target}",
                    "timestamp": datetime.now().isoformat(),
                })
            save_status(path, status)
            result = {"forced_phase": target, "previous": prev}

    elif cmd == "rollback" and len(args) >= 2:
        path_str = args[1]
        phase = None
        mode = None
        ctx_file = None
        if "--phase" in args:
            phase = args[args.index("--phase") + 1]
        if "--mode" in args:
            mode = args[args.index("--mode") + 1]
        if "--context" in args:
            ctx_file = args[args.index("--context") + 1]
        if not phase or not mode:
            result = {"error": "rollback requires --phase and --mode"}
        else:
            result = rollback(path_str, phase, mode, ctx_file)

    elif cmd == "phases":
        result = {
            p: {"description": c["description"], "outcome_type": c["outcome_type"]}
            for p, c in PHASES.items()
        }

    else:
        result = {"error": f"Unknown command: {cmd}"}
        sys.exit(1)

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    _cli()
