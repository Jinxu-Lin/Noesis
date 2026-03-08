"""ResearchFlow Pipeline Runner.

Builds the next action (with full fork-agent prompt) for the main Claude session.
The main session is a pure executor: call runner.py → spawn fork agent → call runner.py.
No loop logic lives in the Skill file.

CLI:
    python runner.py next    <project_path>  → print action JSON (with fork_prompt)
    python runner.py advance <project_path>  → read outcome, advance state, print result
    python runner.py status  <project_path>  → print current status
"""

import json
import sys
from pathlib import Path

# Same package
sys.path.insert(0, str(Path(__file__).parent))
from state_machine import get_next_action, advance, get_status

RESEARCHFLOW_ROOT = Path(__file__).parent.parent
SKILLS_DIR        = RESEARCHFLOW_ROOT / "skills"
LESSONS_DIR       = Path.home() / ".researchflow" / "lessons"


# ─────────────────────────────────────────────────────────────────
# Tier preambles
# ─────────────────────────────────────────────────────────────────

_TIER_PREAMBLE = {
    "heavy": """\
> **Agent 角色定位（Heavy Tier）**：你正在以**独立审稿人 / 综合决策者**身份执行此任务。
> 核心要求：严格、批判、不因礼貌软化判断。主动寻找方案漏洞、隐含假设和潜在风险。
> 研究质量依赖于你的严格把关——宁可多指出问题，不可放水通过。

""",
    "standard": """\
> **Agent 角色定位（Standard Tier）**：你是一位专业的 AI 研究合著者（Co-Author）。
> 深度理解每个步骤背后的研究意图，产出高质量、可发表级别的成果。

""",
}


# ─────────────────────────────────────────────────────────────────
# Cross-project lessons (evolution overlay)
# ─────────────────────────────────────────────────────────────────

def _load_lessons(skill_name: str) -> str:
    """Load cross-project lessons for this skill type from ~/.researchflow/lessons/."""
    lessons_file = LESSONS_DIR / f"{skill_name}.md"
    if not lessons_file.exists():
        return ""
    content = lessons_file.read_text(encoding="utf-8").strip()
    if not content:
        return ""
    return (
        "\n\n---\n\n"
        "## 跨项目经验教训（自动注入）\n\n"
        "> 以下教训来自历史项目的 Phase 11 Retrospective，已验证有效。请在执行中主动参考。\n\n"
        + content
    )


# ─────────────────────────────────────────────────────────────────
# Prompt building
# ─────────────────────────────────────────────────────────────────

def _load_skill_content(skill_name: str, skill_args: str) -> str:
    """Load skill file, prepending review config for review phases."""
    skill_file = SKILLS_DIR / f"{skill_name}-skill.md"
    if not skill_file.exists():
        return f"[ERROR: Skill file not found: {skill_file}]"
    content = skill_file.read_text(encoding="utf-8")

    if skill_name == "review" and skill_args:
        config_file = SKILLS_DIR / "review-configs" / f"{skill_args}-review.yaml"
        if config_file.exists():
            cfg = config_file.read_text(encoding="utf-8")
            content = (
                f"# 审查配置（{skill_args}-review.yaml）\n\n```yaml\n{cfg}\n```\n\n---\n\n"
                + content
            )
    return content


_OUTCOME_GUIDES = {
    "work": (
        '- `"done"` — 正常完成'
    ),
    "review": (
        '- `"pass"` — 审查通过\n'
        '- `"revise"` — 需要修改，回到前序工作阶段\n'
        '- `"continue_P1"` / `"continue_P2"` / `"continue_P4"` '
        '— Block + Exit Gate → Continue，目标 Phase 对应路由\n'
        '- `"abandon"` — Block + Exit Gate → Abandon'
    ),
    "impl_validate": (
        '- `"pass"` — Dim 0 通过\n'
        '- `"L1"` — 调参重试（留在本阶段）\n'
        '- `"continue_P4"` — L2 Swap 或 L3 Redesign\n'
        '- `"continue_P2"` — L4 Pivot\n'
        '- `"abandon"` — Exit Gate → Abandon'
    ),
    "impl_full": (
        '- `"done"` — 所有实验完成，结果满意\n'
        '- `"continue_P4"` — L2/L3 迭代\n'
        '- `"continue_P2"` — L4 Pivot\n'
        '- `"abandon"` — Exit Gate → Abandon'
    ),
}


def _build_fork_prompt(action: dict, project_path: Path) -> str:
    """Assemble the complete, self-contained prompt for the fork subagent."""
    phase        = action["phase"]
    skill_name   = action["skill_name"]
    skill_args   = action.get("skill_args", "")
    description  = action["description"]
    outcome_type = action["outcome_type"]
    tier         = action.get("tier", "standard")
    iter_count   = action.get("iteration_count", 0)

    tier_preamble   = _TIER_PREAMBLE.get(tier, "")
    skill_content   = _load_skill_content(skill_name, skill_args)
    lessons_overlay = _load_lessons(skill_name)
    outcome_guide   = _OUTCOME_GUIDES.get(outcome_type, '- `"done"`')
    outcome_file    = project_path / "phase-outcomes" / f"{phase}.json"

    iter_note = ""
    if iter_count > 0:
        iter_note = f"\n> **注意**：本阶段已执行 {iter_count} 次，这是第 {iter_count + 1} 次。迭代上下文见 `iteration-log.md`（如有）。\n"

    return f"""{tier_preamble}# 项目上下文

**项目路径**：`{project_path}`
**当前阶段**：{description}
**ResearchFlow 仓库**：`{RESEARCHFLOW_ROOT}`
{iter_note}
所有文档的读写均使用绝对路径（以 `{project_path}/` 为前缀）。

---

# Skill 执行指令

{skill_content}{lessons_overlay}

---

# 完成后的强制步骤：写入 Outcome

完成上方 Skill 的**所有步骤**（包括 `/reflect-pipeline` 流程反思，以及 Exit Assessment Gate（如果触发））之后，
将本阶段的最终结果写入：

`{outcome_file}`

格式（JSON）：
```json
{{
  "outcome": "<outcome_key>",
  "notes": "<1-2 句简短说明>"
}}
```

有效的 `outcome_key`：
{outcome_guide}

**这是强制步骤，必须最后执行，不得省略。写入成功后方可结束。**
"""


# ─────────────────────────────────────────────────────────────────
# CLI commands
# ─────────────────────────────────────────────────────────────────

def cmd_next(project_path_str: str) -> dict:
    """Return next action with fully assembled fork_prompt."""
    project_path = Path(project_path_str).resolve()
    (project_path / "phase-outcomes").mkdir(exist_ok=True)

    action = get_next_action(str(project_path))

    if action["action_type"] != "skill":
        return action  # "done" or "error" — pass through as-is

    action["fork_prompt"] = _build_fork_prompt(action, project_path)
    action["project_path"] = str(project_path)

    # Human checkpoint
    if action.get("requires_human_checkpoint"):
        action["checkpoint_message"] = (
            f"⏸️  即将进入 {action['phase']}（{action['description']}）\n"
            f"   此阶段涉及代码执行 / 实验运行，请确认环境就绪后继续。\n"
            f"   回复 yes 继续，skip 跳过（标记为已完成），stop 退出。"
        )

    # Iteration guard
    if action.get("iteration_count", 0) >= 3:
        action["iteration_warning"] = (
            f"⚠️  阶段 {action['phase']} 已迭代 {action['iteration_count']} 次，"
            f"可能陷入循环。请检查项目状态后决定是否继续。"
        )

    return action


def cmd_advance(project_path_str: str) -> dict:
    """Read phase-outcomes/<phase>.json, advance state machine, return result."""
    project_path = Path(project_path_str).resolve()
    status = get_status(project_path)
    phase = status.get("phase", "P1")

    outcome_file = project_path / "phase-outcomes" / f"{phase}.json"

    if not outcome_file.exists():
        return {
            "error": "outcome_file_missing",
            "message": f"Fork agent did not write outcome to {outcome_file}",
            "hint": "Check if the fork agent completed the mandatory 'Write Outcome' step.",
            "phase": phase,
        }

    try:
        outcome_data = json.loads(outcome_file.read_text(encoding="utf-8"))
    except Exception as e:
        return {"error": "outcome_parse_failed", "message": str(e), "phase": phase}

    outcome = outcome_data.get("outcome", "unknown")
    if outcome == "unknown":
        return {
            "error": "outcome_unknown",
            "message": "Fork agent wrote outcome='unknown'. Phase may not have completed.",
            "raw": outcome_data,
            "phase": phase,
        }

    result = advance(str(project_path), phase, outcome)
    if "error" in result:
        return result

    result["notes"] = outcome_data.get("notes", "")
    return result


def _cli():
    args = sys.argv[1:]
    if len(args) < 2:
        print(json.dumps({
            "error": "Usage: runner.py <next|advance|status> <project_path>"
        }))
        sys.exit(1)

    cmd, project_path = args[0], args[1]

    if cmd == "next":
        result = cmd_next(project_path)
    elif cmd == "advance":
        result = cmd_advance(project_path)
    elif cmd == "status":
        result = get_status(Path(project_path).resolve())
    else:
        result = {"error": f"Unknown command: {cmd}"}
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    _cli()
