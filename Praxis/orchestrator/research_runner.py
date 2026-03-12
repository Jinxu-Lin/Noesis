"""Research Pipeline Runner.

Builds the next action (with full fork-agent prompt) for the research pipeline (R1→R11).
Independent from the paper writing pipeline.

CLI:
    python research_runner.py next    <project_path>  → print action JSON (with fork_prompt)
    python research_runner.py advance <project_path>  → read outcome, advance state, print result
    python research_runner.py status  <project_path>  → print current status
"""

import json
import sys
from pathlib import Path

# Same package
sys.path.insert(0, str(Path(__file__).parent))
from research_state_machine import get_next_action, advance, get_status

PRAXIS_ROOT  = Path(__file__).parent.parent
PROMPTS_DIR  = PRAXIS_ROOT / "prompts"
LESSONS_DIR  = Path.home() / ".noesis" / "lessons"


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
    """Load cross-project lessons for this skill type from ~/.noesis/lessons/.

    Filters out [✗ ineffective] entries (injected before but didn't help).
    Promotes [RECURRING] bullet points to the top of each section.
    """
    lessons_file = LESSONS_DIR / f"{skill_name}.md"
    if not lessons_file.exists():
        return ""
    content = lessons_file.read_text(encoding="utf-8").strip()
    if not content:
        return ""

    # Process line by line: filter ineffective, sort recurring first within sections
    recurring: list[str] = []  # bullet lines with [RECURRING]
    normal: list[str] = []     # other bullet lines (not ineffective, not recurring)
    result_lines: list[str] = []

    def flush_bullets() -> None:
        result_lines.extend(recurring)
        result_lines.extend(normal)
        recurring.clear()
        normal.clear()

    for line in content.splitlines():
        if line.startswith("- "):
            if "[✗ ineffective]" in line:
                continue  # drop ineffective lessons entirely
            elif "[RECURRING]" in line:
                recurring.append(line)
            else:
                normal.append(line)
        else:
            # Non-bullet line: flush pending bullets first, then add this line
            flush_bullets()
            result_lines.append(line)

    flush_bullets()  # flush any remaining bullets at end of file

    filtered = "\n".join(result_lines).strip()
    if not filtered:
        return ""

    return (
        "\n\n---\n\n"
        "## 跨项目经验教训（自动注入）\n\n"
        "> 以下教训来自历史项目的 Phase 11 Retrospective。[RECURRING] 为跨项目反复出现的高优先级问题。\n\n"
        + filtered
    )


# ─────────────────────────────────────────────────────────────────
# Prompt building
# ─────────────────────────────────────────────────────────────────

def _load_prompt_content(prompt_name: str, skill_args: str) -> str:
    """Load prompt file, prepending review config for review phases."""
    prompt_file = PROMPTS_DIR / f"{prompt_name}-prompt.md"
    if not prompt_file.exists():
        return f"[ERROR: Prompt file not found: {prompt_file}]"
    content = prompt_file.read_text(encoding="utf-8")

    if prompt_name == "1X-review" and skill_args:
        config_file = PROMPTS_DIR / "review-configs" / f"{skill_args}-review.yaml"
        if config_file.exists():
            cfg = config_file.read_text(encoding="utf-8")
            content = (
                f"# 审查配置（{skill_args}-review.yaml）\n\n```yaml\n{cfg}\n```\n\n---\n\n"
                + content
            )
    return content


def _load_reflect_prompt() -> str:
    """Load the phase reflection prompt (injected after every non-manual phase)."""
    reflect_file = PROMPTS_DIR / "X-reflect-pipeline-prompt.md"
    if not reflect_file.exists():
        return ""
    return reflect_file.read_text(encoding="utf-8")


# ─────────────────────────────────────────────────────────────────
# Iteration context detection
# ─────────────────────────────────────────────────────────────────

# Maps work phases to the review file produced by the preceding review phase.
# Presence of this file → Revise mode.
_PHASE_REVIEW_FILES: dict[str, str] = {
    "R1": "inner-reviews/gap-review.md",
    "R3": "inner-reviews/method-review.md",
    "R5": "inner-reviews/experiment-review.md",
}

# Maps work phases to downstream documents produced in later phases.
# On Pivot restart, agent should read these for full iteration context.
_PHASE_DOWNSTREAM_DOCS: dict[str, list[str]] = {
    "R1": ["research/method-design.md", "research/experiment-design.md", "research/result.md"],
    "R3": ["research/experiment-design.md", "research/result.md"],
    "R5": ["research/result.md"],
}


def _build_iteration_context(project_path: Path, phase: str, iter_count: int) -> str:
    """Detect execution mode from project state and return an injection block.

    Three modes:
      Revise    — review file present AND newer than iteration-log (fresh review feedback)
      Pivot     — iteration-log.md present AND iter_count > 0 (hot-restart after coding failure)
      首次执行  — neither condition met → empty string

    When both files exist, the newer one wins: a fresh review file (written by R2/R4/R6)
    means Revise mode; a newer iteration-log (written by /praxis-conclude) means Pivot mode.
    """
    review_file_name = _PHASE_REVIEW_FILES.get(phase)
    if not review_file_name:
        return ""

    review_file = project_path / review_file_name
    iter_log    = project_path / "iteration-log.md"

    # When both files exist, compare modification times to determine which is more recent
    if review_file.exists() and iter_count > 0 and iter_log.exists():
        if review_file.stat().st_mtime > iter_log.stat().st_mtime:
            # Review file is newer → came from a fresh review cycle → Revise mode
            return (
                f"\n## 迭代模式：Revise（基于审查意见修改）\n\n"
                f"前序审查已完成，意见文件：`{review_file}`（必须全文读取）\n\n"
                f"执行要点：\n"
                f"- 逐条理解每个 Revise / Block 级问题，定位对应段落，针对性修改\n"
                f"- **不从零开始**——保留已通过审查的内容\n"
                f"- Pass 级建议可选择性采纳\n"
            )
        # else: iteration-log is newer → /praxis-conclude hot-restart → fall through to Pivot

    # Pivot mode: iteration-log exists and is the most recent context source
    if iter_count > 0 and iter_log.exists():
        # Build downstream docs reference
        downstream_lines = ""
        downstream_docs = _PHASE_DOWNSTREAM_DOCS.get(phase, [])
        existing_docs = [d for d in downstream_docs if (project_path / d).exists()]
        if existing_docs:
            doc_list = "\n".join(f"  - `{d}`" for d in existing_docs)
            downstream_lines = (
                f"\n前序迭代产出文档（必须阅读以获取完整失败上下文）：\n{doc_list}\n"
                f"\n> 这些文档记录了上一轮迭代的完整设计细节，"
                f"比 iteration-log 摘要更详尽——优先从中理解失败全貌。\n"
            )

        return (
            f"\n## 迭代模式：Pivot（第 {iter_count + 1} 轮热重启）\n\n"
            f"前序方向已排除，迭代日志：`{iter_log}`（必须全文读取）\n"
            f"{downstream_lines}\n"
            f"执行要点：\n"
            f"- 理解所有已排除方向、失败层级（L2/L3/L4）和根因\n"
            f"- **严禁**重复 iteration-log.md 中已排除的方向\n"
            f"- 根据失败层级决定改动范围（见 prompt 中的层级说明）\n"
        )

    # Revise mode: review file present from a fresh review cycle (not stale)
    if review_file.exists():
        return (
            f"\n## 迭代模式：Revise（基于审查意见修改）\n\n"
            f"前序审查已完成，意见文件：`{review_file}`（必须全文读取）\n\n"
            f"执行要点：\n"
            f"- 逐条理解每个 Revise / Block 级问题，定位对应段落，针对性修改\n"
            f"- **不从零开始**——保留已通过审查的内容\n"
            f"- Pass 级建议可选择性采纳\n"
        )

    return ""  # 首次执行 — no special context needed


_OUTCOME_GUIDES = {
    "work": (
        '- `"done"` — 正常完成'
    ),
    "review": (
        '- `"pass"` — 审查通过\n'
        '- `"revise"` — 需要修改，回到前序工作阶段\n'
        '- `"continue_R1"` / `"continue_R3"` '
        '— Block + Exit Gate → Continue，目标 Phase 对应路由（R4 review 可用 continue_R1，R6 review 可用 continue_R3）\n'
        '- `"abandon"` — Block + Exit Gate → Abandon，进入 R8 Retrospective'
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
    skill_content   = _load_prompt_content(skill_name, skill_args)
    lessons_overlay = _load_lessons(skill_name)
    reflect_content = _load_reflect_prompt()
    outcome_guide   = _OUTCOME_GUIDES.get(outcome_type, '- `"done"`')
    outcome_file    = project_path / "phase-outcomes" / f"{phase}.json"

    iter_context = _build_iteration_context(project_path, phase, iter_count)

    reflect_section = ""
    if reflect_content:
        reflect_section = f"\n\n---\n\n{reflect_content}"

    return f"""{tier_preamble}# 项目上下文

**项目路径**：`{project_path}`
**当前阶段**：{description}
**Praxis 仓库**：`{PRAXIS_ROOT}`
{iter_context}
所有文档的读写均使用绝对路径（以 `{project_path}/` 为前缀）。

---

# Skill 执行指令

{skill_content}{lessons_overlay}{reflect_section}

---

# 完成后的强制步骤：写入 Outcome

完成上方所有步骤（包括阶段反思和 Exit Assessment Gate（如果触发））之后，
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
# Codex parallel agent support
# ─────────────────────────────────────────────────────────────────

def _build_codex_prompt(codex_agent: str, action: dict, project_path: Path) -> str:
    """Build the fork prompt for an optional parallel Codex/external-AI agent.

    The Codex agent is informational only — it does NOT write to phase-outcomes/.
    It writes its review to <project>/codex-reviews/<phase>-review.md.
    """
    phase       = action["phase"]
    description = action["description"]
    skill_args  = action.get("skill_args", "")

    prompt_content = _load_prompt_content(codex_agent, skill_args)
    output_file = project_path / "codex-reviews" / f"{phase}-review.md"

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
    """Return next action with fully assembled fork_prompt."""
    project_path = Path(project_path_str).resolve()
    (project_path / "phase-outcomes").mkdir(exist_ok=True)

    action = get_next_action(str(project_path))

    if action["action_type"] != "skill":
        return action  # "done", "error", or "manual" — pass through as-is

    main_fork_prompt = _build_fork_prompt(action, project_path)
    codex_agent = action.get("codex_agent")  # optional field from PHASES config

    if codex_agent:
        # Return parallel action: main agent + codex reviewer
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

    # Human checkpoint
    if action.get("requires_human_checkpoint"):
        action["checkpoint_message"] = (
            f"⏸️  即将进入 {action['phase']}（{action['description']}）\n"
            f"   请确认准备就绪后继续。\n"
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
    phase = status.get("phase", "R1")

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
