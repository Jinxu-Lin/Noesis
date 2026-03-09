"""Paper Writing Pipeline Runner.

Builds the next action (with full fork-agent prompt) for paper writing phases.
Independent from the main research pipeline runner.

CLI:
    python paper_runner.py next    <project_path>  → print action JSON (with fork_prompt)
    python paper_runner.py advance <project_path>  → read outcome, advance state, print result
    python paper_runner.py status  <project_path>  → print current paper status
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from paper_state_machine import get_next_action, advance, get_status, save_status

PRAXIS_ROOT  = Path(__file__).parent.parent
PROMPTS_DIR  = PRAXIS_ROOT / "prompts"
LESSONS_DIR  = Path.home() / ".noesis" / "lessons"


# ─────────────────────────────────────────────────────────────────
# Tier preambles
# ─────────────────────────────────────────────────────────────────

_TIER_PREAMBLE = {
    "heavy": """\
> **Agent 角色定位（Heavy Tier）**：你正在以**资深编辑 / 独立审稿人**身份执行此任务。
> 核心要求：严格把控论文质量，确保每个章节的论证严密、表达清晰、数据准确。
> 论文质量直接决定能否被顶会接收——宁可多次修订，不可降低标准。

""",
    "standard": """\
> **Agent 角色定位（Standard Tier）**：你是一位专业的学术论文写作者。
> 深度理解研究内容，用精确、简洁、学术规范的语言表达。产出可发表级别的论文内容。

""",
}


# ─────────────────────────────────────────────────────────────────
# Cross-project lessons
# ─────────────────────────────────────────────────────────────────

def _load_lessons(skill_name: str) -> str:
    lessons_file = LESSONS_DIR / f"{skill_name}.md"
    if not lessons_file.exists():
        return ""
    content = lessons_file.read_text(encoding="utf-8").strip()
    if not content:
        return ""
    return (
        "\n\n---\n\n"
        "## 跨项目经验教训（自动注入）\n\n"
        "> 以下教训来自历史项目，已验证有效。请在执行中主动参考。\n\n"
        + content
    )


# ─────────────────────────────────────────────────────────────────
# Prompt building
# ─────────────────────────────────────────────────────────────────

def _load_prompt_content(prompt_name: str) -> str:
    prompt_file = PROMPTS_DIR / f"{prompt_name}-prompt.md"
    if not prompt_file.exists():
        return f"[ERROR: Prompt file not found: {prompt_file}]"
    return prompt_file.read_text(encoding="utf-8")


def _load_reflect_prompt() -> str:
    """Load the phase reflection prompt (injected after every non-manual phase)."""
    reflect_file = PROMPTS_DIR / "X-reflect-pipeline-prompt.md"
    if not reflect_file.exists():
        return ""
    return reflect_file.read_text(encoding="utf-8")


_OUTCOME_GUIDES = {
    "work": (
        '- `"done"` — 正常完成'
    ),
    "paper_review": (
        '- `"pass"` — 终审通过（评分 ≥ 7.0）\n'
        '- `"revise"` — 需要修订，回到 P4 编辑整合阶段'
    ),
}


def _build_fork_prompt(action: dict, project_path: Path) -> str:
    phase = action["phase"]
    skill_name = action["skill_name"]
    description = action["description"]
    outcome_type = action["outcome_type"]
    tier = action.get("tier", "standard")
    iter_count = action.get("iteration_count", 0)
    revision_rounds = action.get("revision_rounds", 0)

    tier_preamble = _TIER_PREAMBLE.get(tier, "")
    skill_content = _load_prompt_content(skill_name)
    lessons_overlay = _load_lessons(skill_name)
    reflect_content = _load_reflect_prompt()
    outcome_guide = _OUTCOME_GUIDES.get(outcome_type, '- `"done"`')
    outcome_file = project_path / "Papers" / "phase-outcomes" / f"{phase}.json"

    iter_note = ""
    if iter_count > 0:
        iter_note = f"\n> **注意**：本阶段已执行 {iter_count} 次，这是第 {iter_count + 1} 次。\n"

    revision_note = ""
    if revision_rounds > 0:
        revision_note = f"\n> **修订轮次**：当前为第 {revision_rounds} 轮修订。请重点关注上一轮 review 中指出的问题。\n"

    revision_warning = action.get("revision_warning", "")
    if revision_warning:
        revision_note += f"\n> {revision_warning}\n"

    reflect_section = ""
    if reflect_content:
        reflect_section = f"\n\n---\n\n{reflect_content}"

    return f"""{tier_preamble}# 项目上下文

**项目路径**：`{project_path}`
**当前阶段**：{description}
**Praxis 仓库**：`{PRAXIS_ROOT}`
{iter_note}{revision_note}
所有文档的读写均使用绝对路径（以 `{project_path}/` 为前缀）。
论文相关文件位于 `{project_path}/Papers/` 目录下。

---

# Skill 执行指令

{skill_content}{lessons_overlay}{reflect_section}

---

# 完成后的强制步骤：写入 Outcome

完成上方所有步骤（包括阶段反思）之后，将本阶段的最终结果写入：

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
# Codex parallel agent support
# ─────────────────────────────────────────────────────────────────

def _build_codex_prompt(codex_agent: str, action: dict, project_path: Path) -> str:
    """Build fork prompt for a parallel Codex/external-AI reviewer (informational only)."""
    phase       = action["phase"]
    description = action["description"]
    prompt_content = _load_prompt_content(codex_agent)
    output_file = project_path / "Papers" / "codex-reviews" / f"{phase}-review.md"

    return f"""> **Agent 角色定位（External AI Reviewer）**：你是一个独立的外部 AI 审查者（非 Claude 生态），
> 负责提供差异化的第三方视角。你的审查结果为**参考信息**，不参与流程判定。

# 项目上下文

**项目路径**：`{project_path}`
**当前阶段**：{description}（外部审查视角）

---

# 审查指令

{prompt_content}

---

# 完成后的强制步骤：写入审查结果

将你的审查结果写入（**不要**写入 phase-outcomes/）：

`{output_file}`

格式：Markdown，包含评分（1-10）、核心发现、具体改进建议。
"""


# ─────────────────────────────────────────────────────────────────
# CLI commands
# ─────────────────────────────────────────────────────────────────

def cmd_next(project_path_str: str) -> dict:
    project_path = Path(project_path_str).resolve()
    papers_dir = project_path / "Papers"
    papers_dir.mkdir(exist_ok=True)
    (papers_dir / "phase-outcomes").mkdir(exist_ok=True)

    action = get_next_action(str(project_path))

    if action["action_type"] != "skill":
        return action

    main_fork_prompt = _build_fork_prompt(action, project_path)
    codex_agent = action.get("codex_agent")

    if codex_agent:
        action["action_type"] = "skills_parallel"
        action["skills"] = [
            {
                "role": "main",
                "description": action["description"],
                "fork_prompt": main_fork_prompt,
            },
            {
                "role": "codex",
                "description": f"Codex 外部审查: {action['description']}",
                "fork_prompt": _build_codex_prompt(codex_agent, action, project_path),
            },
        ]
    else:
        action["action_type"] = "skill"
        action["fork_prompt"] = main_fork_prompt

    action["project_path"] = str(project_path)

    # Iteration guard
    if action.get("iteration_count", 0) >= 5:
        action["iteration_warning"] = (
            f"⚠️  阶段 {action['phase']} 已迭代 {action['iteration_count']} 次，"
            f"可能陷入循环。请检查论文状态后决定是否继续。"
        )

    return action


def cmd_advance(project_path_str: str) -> dict:
    project_path = Path(project_path_str).resolve()
    status = get_status(project_path)
    phase = status.get("phase", "P1")

    outcome_file = project_path / "Papers" / "phase-outcomes" / f"{phase}.json"

    if not outcome_file.exists():
        return {
            "error": "outcome_file_missing",
            "message": f"Fork agent did not write outcome to {outcome_file}",
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
            "message": "Fork agent wrote outcome='unknown'.",
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
            "error": "Usage: paper_runner.py <next|advance|status> <project_path>"
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
