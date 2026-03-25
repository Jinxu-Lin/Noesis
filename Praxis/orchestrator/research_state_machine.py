"""Research Module State Machine — v3

Tracks research module phase state:
  formalize → formalize_review → design → design_review → blueprint → implement → retrospective → complete

Does NOT execute anything — research_runner.py calls this and executes.

State file: Docs/research-module-status.json
Pipeline tracker: pipeline-status.json (active_module field)
Outcomes: phase-outcomes/<phase>.json (written by fork agents)

CLI:
    python research_state_machine.py next       <project_path>
    python research_state_machine.py advance    <project_path> [--outcome <outcome>]
    python research_state_machine.py status     <project_path>
    python research_state_machine.py init       <project_path>
    python research_state_machine.py init-phase <project_path> <phase>
    python research_state_machine.py rollback   <project_path> --phase <phase> --mode <mode> [--context <file>]
    python research_state_machine.py phases
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# ─────────────────────────────────────────────────────────────────
# Phase configuration table
# ─────────────────────────────────────────────────────────────────

PHASES = {
    "formalize": {
        "skill": "formalize",
        "description": "问题锐化 — 将直觉方向精炼为正式 Gap + RQ + 攻击角度",
        "output_doc": "research/problem-statement.md",
        "outcome_type": "work",
        "next": {"done": "formalize_review", "abandon": "complete"},
    },
    "formalize_review": {
        "skill": "formalize-review",
        "description": "问题锐化审查 — 4 Agent 战略辩论",
        "output_doc": None,
        "outcome_type": "formalize_review",
        "debate_agents": ["contrarian", "comparativist", "pragmatist", "interdisciplinary"],
        "next": {"pass": "design", "revise": "formalize", "abandon": "complete"},
    },
    "design": {
        "skill": "design",
        "description": "联合设计 — 方法 + 实验同步设计",
        "output_doc": ["research/method-design.md", "research/experiment-design.md"],
        "outcome_type": "work",
        "next": {"done": "design_review", "escalate": "formalize"},
    },
    "design_review": {
        "skill": "design-review",
        "description": "设计审查 — 6 Agent 技术辩论",
        "output_doc": None,
        "outcome_type": "design_review",
        "debate_agents": ["theorist", "methodologist", "empiricist", "skeptic", "pragmatist", "contrarian"],
        "next": {"pass": "blueprint", "revise": "design", "fundamental": "formalize", "abandon": "complete"},
    },
    "blueprint": {
        "skill": "blueprint",
        "description": "实现蓝图 — 代码架构 + 实验执行清单",
        "output_doc": ["Codes/experiment-todo.md"],
        "outcome_type": "work",
        "next": {"done": "implement"},
    },
    "implement": {
        "skill": None,  # manual phase - coding + experiments
        "description": "编码实验 — 编写代码 + 执行实验 + 记录结果",
        "output_doc": "Codes/_Results/experiment_result.md",
        "outcome_type": "manual",
        "next": {
            "success": "retrospective",
            "iterate_method": "design",
            "iterate_direction": "formalize",
            "abandon": "complete",
        },
    },
    "retrospective": {
        "skill": "retrospective",
        "description": "知识回收 — 提取知识资产 + 标记验证状态",
        "output_doc": "research/retrospective.md",
        "outcome_type": "work",
        "next": {"done": "complete"},
    },
    "complete": {
        "skill": None,
        "description": "Research Module 完成",
        "outcome_type": "terminal",
        "next": {},
    },
}


# ─────────────────────────────────────────────────────────────────
# Status I/O
# ─────────────────────────────────────────────────────────────────

STATUS_DIR = "Docs"
STATUS_FILE = "research-module-status.json"
PIPELINE_STATUS_FILE = "pipeline-status.json"


def _status_path(project_path: Path) -> Path:
    return project_path / STATUS_DIR / STATUS_FILE


def get_status(project_path: Path) -> dict:
    f = _status_path(project_path)
    if f.exists():
        return json.loads(f.read_text(encoding="utf-8"))
    return {"phase": "formalize", "initialized": False}


def save_status(project_path: Path, status: dict) -> None:
    status["last_updated"] = datetime.now().isoformat()
    f = _status_path(project_path)
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(status, indent=2, ensure_ascii=False), encoding="utf-8")


def _update_pipeline_status(project_path: Path, module: str = "research") -> None:
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
    """Compute entry_context for the target phase based on transition.

    Returns a dict stored in research-module-status.json, or None if no special context.
    """
    history = status.get("history", [])
    formalize_count = sum(1 for h in history if h.get("phase") == "formalize")
    design_count = sum(1 for h in history if h.get("phase") == "design")

    # formalize_review → formalize (revise)
    if phase == "formalize_review" and outcome == "revise":
        # Find the latest formalize_review round number
        fr_count = sum(1 for h in history if h.get("phase") == "formalize_review")
        review_file = f"Reviews/research-formalize/round-{fr_count + 1}/synthesis.md"
        return {
            "mode": "fr_revise",
            "source_phase": "formalize_review",
            "review_file": review_file,
            "formalize_iteration_count": formalize_count,
        }

    # design_review → design (revise)
    if phase == "design_review" and outcome == "revise":
        dr_count = sum(1 for h in history if h.get("phase") == "design_review")
        review_file = f"Reviews/research-design/round-{dr_count + 1}/synthesis.md"
        return {
            "mode": "dr_revise",
            "source_phase": "design_review",
            "review_file": review_file,
            "design_iteration_count": design_count,
        }

    # design_review → formalize (fundamental)
    if phase == "design_review" and outcome == "fundamental":
        return {
            "mode": "direction_pivot",
            "source_phase": "design_review",
            "diagnosis": "direction_level",
            "formalize_iteration_count": formalize_count,
        }

    # implement → design (iterate_method)
    if phase == "implement" and outcome == "iterate_method":
        result_file = "Codes/_Results/experiment_result.md"
        return {
            "mode": "method_iterate",
            "source_phase": "implement",
            "result_file": result_file,
            "design_iteration_count": design_count,
            "formalize_iteration_count": formalize_count,
        }

    # implement → formalize (iterate_direction)
    if phase == "implement" and outcome == "iterate_direction":
        result_file = "Codes/_Results/experiment_result.md"
        return {
            "mode": "direction_pivot",
            "source_phase": "implement",
            "result_file": result_file,
            "formalize_iteration_count": formalize_count,
        }

    # design → formalize (escalate, iteration guard)
    if phase == "design" and outcome == "escalate":
        return {
            "mode": "direction_pivot",
            "source_phase": "design",
            "reason": "iteration_guard",
            "design_iteration_count": design_count,
            "formalize_iteration_count": formalize_count,
        }

    return None


# ─────────────────────────────────────────────────────────────────
# Document version reader
# ─────────────────────────────────────────────────────────────────

def _read_doc_version(project_path: Path, output_doc) -> str | None:
    """Try to read version from document frontmatter."""
    if not output_doc:
        return None
    if isinstance(output_doc, list):
        output_doc = output_doc[0]
    doc_path = project_path / output_doc
    if not doc_path.exists():
        return None
    try:
        content = doc_path.read_text(encoding="utf-8")
        if content.startswith("---"):
            end = content.find("---", 3)
            if end > 0:
                frontmatter = content[3:end]
                for line in frontmatter.splitlines():
                    if line.strip().startswith("version:"):
                        return line.split(":", 1)[1].strip().strip('"\'')
    except Exception:
        pass
    return None


# ─────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────

def get_next_action(project_path_str: str) -> dict:
    """Return the next action for the runner to execute."""
    path = Path(project_path_str)
    status = get_status(path)
    phase = status.get("phase", "formalize")
    cfg = PHASES.get(phase)

    if not cfg:
        return {"action_type": "error", "message": f"Unknown phase: {phase}",
                "status": status}

    if cfg["outcome_type"] == "terminal":
        decision = status.get("decision", "unknown")
        return {"action_type": "done",
                "description": f"Research Module 完成 — 判定: {decision}",
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

    # Read document version if available
    version = _read_doc_version(path, cfg.get("output_doc"))

    # Record history
    history_entry = {
        "phase": phase,
        "outcome": outcome_key,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "timestamp": datetime.now().isoformat(),
    }
    if entry_context and entry_context.get("mode"):
        history_entry["mode"] = entry_context["mode"]
    if version:
        history_entry["version"] = version

    # Track review round numbers
    if phase == "formalize_review":
        fr_count = sum(1 for h in status.get("history", []) if h.get("phase") == "formalize_review")
        history_entry["review_round"] = fr_count + 1
    if phase == "design_review":
        dr_count = sum(1 for h in status.get("history", []) if h.get("phase") == "design_review")
        history_entry["review_round"] = dr_count + 1

    status.setdefault("history", []).append(history_entry)

    # Update status
    status["phase"] = next_phase
    if entry_context:
        status["entry_context"] = entry_context
    else:
        status.pop("entry_context", None)

    # Record decision for terminal transitions
    if outcome_key == "abandon":
        status["decision"] = "Abandon"
    if phase == "retrospective" and outcome_key == "done":
        status["decision"] = "Complete"

    save_status(path, status)

    return {
        "from_phase": phase,
        "outcome": outcome_key,
        "next_phase": next_phase,
        "entry_context": entry_context,
    }


def rollback(project_path_str: str, target_phase: str, mode: str,
             context_file: str | None = None) -> dict:
    """Rollback to a specific phase with context (e.g., from later module)."""
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

    # Update pipeline-status to point back to research module
    _update_pipeline_status(path, "research")

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
        print(json.dumps({"error": "Usage: research_state_machine.py <cmd> <project_path> [args]"}))
        sys.exit(1)

    cmd = args[0]

    if cmd == "next" and len(args) >= 2:
        result = get_next_action(args[1])

    elif cmd == "advance" and len(args) >= 2:
        path = Path(args[1])
        status = get_status(path)
        phase = status.get("phase", "formalize")
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
        status = {"phase": "formalize", "initialized": True,
                  "notes": "research module initialized", "history": []}
        save_status(path, status)
        _update_pipeline_status(path, "research")
        result = {"initialized": True, "phase": "formalize"}

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
