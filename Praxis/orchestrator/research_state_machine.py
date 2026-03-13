"""Research Pipeline State Machine — v2

Tracks project phase state and computes next actions.
Does NOT execute anything — research_runner.py calls this and executes.

v2 Phase flow:
  S (Startup, independent) → C (Crystallize) → RS (Strategic Review)
  → P (Probe, manual) → D (Joint Design) → RT (Technical Review)
  → I (Implementation) → E (Execution, manual) → W (Paper Writing, manual)
  → R (Retrospective) → complete

Single source of truth: pipeline-status.json
Outcomes: phase-outcomes/<phase>.json (written by fork agents)

CLI:
    python research_state_machine.py next       <project_path>
    python research_state_machine.py advance    <project_path> [--outcome <outcome>]
    python research_state_machine.py status     <project_path>
    python research_state_machine.py init       <project_path>
    python research_state_machine.py init-phase <project_path> <phase>
    python research_state_machine.py phases
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# ─────────────────────────────────────────────────────────────────
# Phase configuration table (v2)
# ─────────────────────────────────────────────────────────────────

PHASES = {
    "C": {
        "skill": "crystallize",
        "skill_args": "",
        "description": "问题锐化 — Gap + 攻击角度 + 探针方案",
        "output_doc": "research/problem-statement.md",
        "outcome_type": "work",
        "tier": "heavy",
        "next": {
            "done": "RS",
            "abandon": "R",       # iteration guard: C ≥ 3 次 → 用户选择放弃
        },
    },
    "RS": {
        "skill": "strategic-review",
        "skill_args": "",
        "codex_agent": "codex-reviewer",
        "debate_agents": ["contrarian", "comparativist", "pragmatist", "interdisciplinary"],
        "description": "战略审查 — 方向+攻击角度+探针审查 🔒",
        "output_doc": "inner-reviews/strategic-review.md",
        "outcome_type": "strategic_review",
        "tier": "heavy",
        "next": {
            "pass": "P",
            "revise": "C",        # entry_context: rs_revise
            "abandon": "R",
        },
    },
    "P": {
        "skill": None,            # manual phase
        "skill_args": "",
        "description": "探针实验 — 用最小成本验证核心直觉 🔧",
        "output_doc": "research/probe-results.md",
        "outcome_type": "manual",
        "tier": None,
        "next": {
            "signal": "D",
            "pivot": "C",         # entry_context: probe_pivot
            "abandon": "R",
        },
    },
    "D": {
        "skill": "joint-design",
        "skill_args": "",
        "description": "联合设计 — 方法+实验同步设计",
        "output_doc": ["research/method-design.md", "research/experiment-design.md"],
        "outcome_type": "work",
        "tier": "heavy",
        "next": {
            "done": "RT",
            "escalate": "C",      # iteration guard: D ≥ 2 次 → 强制升级到 C
        },
    },
    "RT": {
        "skill": "technical-review",
        "skill_args": "",
        "codex_agent": "codex-reviewer",
        "debate_agents": ["theorist", "methodologist", "empiricist", "skeptic", "pragmatist", "contrarian"],
        "description": "技术审查 — 方法逻辑+实验有效性 🔒",
        "output_doc": "inner-reviews/technical-review.md",
        "outcome_type": "technical_review",
        "tier": "heavy",
        "next": {
            "pass": "I",
            "revise": "D",        # entry_context: rt_revise
            "fundamental": "C",   # entry_context: execute_pivot (direction)
            "abandon": "R",
        },
    },
    "I": {
        "skill": "implementation",
        "skill_args": "",
        "description": "实现规划 — 代码架构+实验方案",
        "output_doc": ["Codes/code-todo.md", "Codes/experiment-todo.md", "Codes/CLAUDE.md"],
        "outcome_type": "work",
        "tier": "standard",
        "next": {"done": "E"},
    },
    "E": {
        "skill": None,            # manual phase
        "skill_args": "",
        "description": "实验执行 — 编码与实验 🔧",
        "output_doc": "research/result.md",
        "outcome_type": "manual",
        "tier": None,
        "next": {
            "success": "W",
            "iterate_method": "D",      # entry_context: execute_iterate
            "iterate_direction": "C",   # entry_context: execute_pivot
            "abandon": "R",
        },
    },
    "W": {
        "skill": None,            # independent paper pipeline
        "skill_args": "",
        "description": "论文写作 — 独立 Paper Pipeline 🔧",
        "output_doc": None,
        "outcome_type": "manual",
        "tier": None,
        "next": {"done": "R"},
    },
    "R": {
        "skill": "retrospective",
        "skill_args": "",
        "description": "知识回收 — 项目生命周期知识提取",
        "output_doc": "research/retrospective.md",
        "outcome_type": "work",
        "tier": "heavy",
        "next": {"done": "complete"},
    },
    "complete": {
        "skill": None,
        "skill_args": "",
        "description": "Pipeline complete — 研究全流程已完成",
        "outcome_type": "terminal",
        "next": {},
    },
}

# Phases that require human confirmation before auto-proceeding
HUMAN_CHECKPOINT_PHASES = set()


# ─────────────────────────────────────────────────────────────────
# Status I/O
# ─────────────────────────────────────────────────────────────────

STATUS_FILE = "pipeline-status.json"


def get_status(project_path: Path) -> dict:
    f = project_path / STATUS_FILE
    if f.exists():
        return json.loads(f.read_text(encoding="utf-8"))
    # No status file → fresh project, start at C
    return {"phase": "C", "initialized": False}


def save_status(project_path: Path, status: dict) -> None:
    status["last_updated"] = datetime.now().isoformat()
    f = project_path / STATUS_FILE
    f.write_text(json.dumps(status, indent=2, ensure_ascii=False), encoding="utf-8")


# ─────────────────────────────────────────────────────────────────
# Entry context computation
# ─────────────────────────────────────────────────────────────────

def _compute_entry_context(phase: str, outcome: str, status: dict) -> dict | None:
    """Compute entry_context for the target phase based on current transition.

    Returns a dict to be stored in pipeline-status.json, or None if no special context.
    """
    # Count iterations for iteration guards
    history = status.get("history", [])
    d_count = sum(1 for h in history if h.get("phase") == "D")
    c_count = sum(1 for h in history if h.get("phase") == "C")

    # RS → C (revise)
    if phase == "RS" and outcome == "revise":
        return {
            "mode": "rs_revise",
            "source_phase": "RS",
            "c_iteration_count": c_count,
        }

    # P → C (pivot)
    if phase == "P" and outcome == "pivot":
        return {
            "mode": "probe_pivot",
            "source_phase": "P",
            "c_iteration_count": c_count,
        }

    # RT → D (revise)
    if phase == "RT" and outcome == "revise":
        return {
            "mode": "rt_revise",
            "source_phase": "RT",
            "d_iteration_count": d_count,
        }

    # RT → C (fundamental)
    if phase == "RT" and outcome == "fundamental":
        return {
            "mode": "execute_pivot",
            "source_phase": "RT",
            "diagnosis": "direction_level",
            "c_iteration_count": c_count,
        }

    # D → C (escalate, iteration guard)
    if phase == "D" and outcome == "escalate":
        return {
            "mode": "execute_pivot",
            "source_phase": "D",
            "diagnosis": "direction_level",
            "reason": "iteration_guard_escalate",
            "d_iteration_count": d_count,
            "c_iteration_count": c_count,
        }

    # E → D (iterate_method)
    if phase == "E" and outcome == "iterate_method":
        return {
            "mode": "execute_iterate",
            "source_phase": "E",
            "diagnosis": "method_level",
            "d_iteration_count": d_count,
            "c_iteration_count": c_count,
        }

    # E → C (iterate_direction)
    if phase == "E" and outcome == "iterate_direction":
        return {
            "mode": "execute_pivot",
            "source_phase": "E",
            "diagnosis": "direction_level",
            "c_iteration_count": c_count,
        }

    return None


# ─────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────

def get_next_action(project_path_str: str) -> dict:
    """Return the next action for the runner to execute."""
    path = Path(project_path_str)
    status = get_status(path)
    phase = status.get("phase", "C")
    cfg = PHASES.get(phase)

    if not cfg:
        return {"action_type": "error", "message": f"Unknown phase: {phase}",
                "status": status}

    if cfg["outcome_type"] == "terminal":
        return {"action_type": "done",
                "description": "Pipeline complete — 研究全流程已完成 ✓",
                "phase": phase}

    if cfg["outcome_type"] == "manual":
        runner = str(Path(__file__).parent / "research_runner.py")
        p = project_path_str
        messages = {
            "P": (
                f"当前处于探针实验阶段（手动）。\n"
                f"请阅读 research/problem-statement.md §3 探针方案，执行最小验证实验。\n"
                f"完成后将结果写入 research/probe-results.md，然后推进状态：\n"
                f"  - 有信号 → python3 {runner} advance {p} --outcome signal\n"
                f"  - 换攻击角度 → python3 {runner} advance {p} --outcome pivot\n"
                f"  - 放弃 → python3 {runner} advance {p} --outcome abandon"
            ),
            "E": (
                f"当前处于实验执行阶段（手动）。\n"
                f"请与 AI 协作完成代码编写和实验运行（参考 Codes/ 目录）。\n"
                f"完成后：\n"
                f"  - 验证通过 → python3 {runner} advance {p} --outcome success\n"
                f"  - 方法层失败 → /praxis-conclude {p}（诊断后选择 iterate_method）\n"
                f"  - 方向层失败 → /praxis-conclude {p}（诊断后选择 iterate_direction）\n"
                f"  - 放弃 → /praxis-conclude {p}（诊断后选择 abandon）"
            ),
            "W": (
                f"当前处于论文写作阶段。\n"
                f"请运行 /praxis-paper {p} 启动论文写作模块（P1→P7）。\n"
                f"完成后运行：python3 {runner} advance {p} --outcome done\n"
                f"然后继续运行 /praxis-research {p} 进入 R（知识回收）。"
            ),
        }
        return {
            "action_type": "manual",
            "phase": phase,
            "description": cfg["description"],
            "message": messages.get(phase, f"当前处于 {phase} 阶段。"),
        }

    requires_human = phase in HUMAN_CHECKPOINT_PHASES

    # Compute iteration count from history
    history = status.get("history", [])
    iter_count = sum(1 for h in history if h.get("phase") == phase)

    result = {
        "action_type": "skill",
        "phase": phase,
        "skill_name": cfg["skill"],
        "skill_args": cfg.get("skill_args", ""),
        "codex_agent": cfg.get("codex_agent"),
        "debate_agents": cfg.get("debate_agents"),
        "description": cfg["description"],
        "output_doc": cfg.get("output_doc"),
        "outcome_type": cfg["outcome_type"],
        "tier": cfg.get("tier", "standard"),
        "requires_human_checkpoint": requires_human,
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

    # Append to history
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

    status.setdefault("history", []).append(history_entry)

    # Update status
    status["phase"] = next_phase
    if entry_context:
        status["entry_context"] = entry_context
    else:
        status.pop("entry_context", None)  # clear stale context

    save_status(path, status)

    return {
        "from_phase": phase,
        "outcome": outcome_key,
        "next_phase": next_phase,
        "entry_context": entry_context,
    }


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
        status = {"phase": "C", "notes": "manually initialized"}
        save_status(path, status)
        result = {"initialized": True, "phase": "C", "project": str(path)}

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
            status.pop("entry_context", None)  # clear context on manual override
            # Only record history if actually changing phase (avoid polluting
            # iteration count when e.g. startup calls init-phase C on a fresh
            # project whose default phase is already C)
            if prev != target_phase:
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
