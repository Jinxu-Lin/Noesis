"""Init Module Runner — v1.

Builds the next action (with full fork-agent prompt) for the init module.
init → start → probe_design → review → probe_impl → complete

CLI:
    python init_runner.py next    <project_path>  → print action JSON (with fork_prompt)
    python init_runner.py advance <project_path>  → read outcome, advance state, print result
    python init_runner.py advance <project_path> --outcome <outcome>  → manual advance
    python init_runner.py rollback <project_path> --phase <phase> --mode <mode> [--context <file>]
    python init_runner.py status  <project_path>  → print current status
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from init_state_machine import (
    get_next_action, advance, get_status, rollback, PHASES,
    save_status, _status_path,
)

PRAXIS_ROOT = Path(__file__).parent.parent
PROMPTS_DIR = PRAXIS_ROOT / "prompts"
LESSONS_DIR = Path.home() / ".noesis" / "lessons"

_TIER_MODEL = {"heavy": "opus", "standard": "sonnet"}

_TIER_PREAMBLE = """\
> **Agent 角色定位**：你是一位资深深度学习研究科学家（NeurIPS/ICML/ICLR 级别），
> 正在协助完成研究项目的初始化分析。核心要求：严格、批判、不因礼貌软化判断。
> 主动寻找方案漏洞、隐含假设和潜在风险。

"""


# ─────────────────────────────────────────────────────────────────
# Prompt loading
# ─────────────────────────────────────────────────────────────────

def _load_prompt_content(prompt_name: str) -> str:
    """Load prompt file content. For review phases, prepend review config YAML."""
    prompt_file = PROMPTS_DIR / f"{prompt_name}-prompt.md"
    if not prompt_file.exists():
        return f"[ERROR: Prompt file not found: {prompt_file}]"
    content = prompt_file.read_text(encoding="utf-8")

    # For review phases, prepend the review config
    if prompt_name == "init-review":
        config_file = PROMPTS_DIR / "review-configs" / f"{prompt_name}.yaml"
        if config_file.exists():
            cfg = config_file.read_text(encoding="utf-8")
            content = (
                f"# 审查配置（{prompt_name}.yaml）\n\n```yaml\n{cfg}\n```\n\n---\n\n"
                + content
            )
    return content


def _load_lessons(skill_name: str) -> str:
    """Load cross-project lessons for this skill type."""
    lessons_file = LESSONS_DIR / f"{skill_name}.md"
    if not lessons_file.exists():
        return ""
    content = lessons_file.read_text(encoding="utf-8").strip()
    if not content:
        return ""

    recurring: list[str] = []
    normal: list[str] = []
    result_lines: list[str] = []

    def flush():
        result_lines.extend(recurring)
        result_lines.extend(normal)
        recurring.clear()
        normal.clear()

    for line in content.splitlines():
        if line.startswith("- "):
            if "[✗ ineffective]" in line:
                continue
            elif "[RECURRING]" in line:
                recurring.append(line)
            else:
                normal.append(line)
        else:
            flush()
            result_lines.append(line)
    flush()

    filtered = "\n".join(result_lines).strip()
    if not filtered:
        return ""
    return (
        "\n\n---\n\n"
        "## 跨项目经验教训（自动注入）\n\n"
        "> 以下教训来自历史项目。[RECURRING] 为跨项目反复出现的高优先级问题。\n\n"
        + filtered
    )


# ─────────────────────────────────────────────────────────────────
# Entry context → iteration injection
# ─────────────────────────────────────────────────────────────────

def _build_iteration_context(project_path: Path, phase: str,
                              entry_context: dict | None) -> str:
    """Build iteration context injection block."""
    if not entry_context:
        return ""

    mode = entry_context.get("mode", "first")

    if mode == "first":
        return ""

    if mode == "review_revise":
        review_round = entry_context.get("review_round", 1)
        synthesis_file = project_path / "Reviews" / "init" / f"round-{review_round}" / "synthesis.md"
        return (
            f"\n## 迭代模式：Review-Revise（基于 review 意见修改）\n\n"
            f"Review 已完成，综合意见文件：`{synthesis_file}`（必须全文读取）\n\n"
            f"执行要点：\n"
            f"- 逐条理解 review 意见中的 '必须修改的内容'\n"
            f"- 保留 '可以保留的内容'，只修改被质疑的部分\n"
            f"- 更新 project.md frontmatter version（minor +1）\n"
        )

    if mode == "probe_failure":
        ctx_file = entry_context.get("context_file", "")
        return (
            f"\n## 迭代模式：Probe-Failure（后续模块 probe 失败回退）\n\n"
            f"Probe 实验未获正面信号，需要重新审视问题定义和方法。\n"
            f"- Probe 结果文件：`{ctx_file}`（如存在，必须全文读取）\n\n"
            f"执行要点：\n"
            f"- 分析 probe 失败的根因：是方向问题还是实现问题\n"
            f"- 如果方向有问题 → 重新设计 §2.2 问题定义 和 §2.4 方法\n"
            f"- 如果只是实现问题 → 微调 §2.4 和 §2.5\n"
            f"- 充分利用失败中的洞察\n"
            f"- 更新 project.md frontmatter version（major +1）\n"
        )

    return ""


# ─────────────────────────────────────────────────────────────────
# Outcome guides
# ─────────────────────────────────────────────────────────────────

_OUTCOME_GUIDES = {
    "work": '- `"done"` — 正常完成',
    "review": (
        '- `"pass"` — 审查通过，进入 probe 代码实现\n'
        '- `"revise"` — 需要修改，回到 start 子模块\n'
        '- `"hold"` — 信息不足，暂停等待补充\n'
        '- `"stop"` — 方向有硬伤，终止'
    ),
    "probe_impl": (
        '- `"done"` — 代码就绪，dry run 通过\n'
        '- `"infeasible"` — 实现中发现设计不可行，回到 probe_design 重新设计'
    ),
}


# ─────────────────────────────────────────────────────────────────
# Fork prompt building
# ─────────────────────────────────────────────────────────────────

def _build_fork_prompt(action: dict, project_path: Path) -> str:
    """Assemble the complete, self-contained prompt for the fork subagent."""
    phase = action["phase"]
    skill_name = action["skill_name"]
    description = action["description"]
    outcome_type = action["outcome_type"]
    entry_ctx = action.get("entry_context")

    skill_content = _load_prompt_content(skill_name)
    lessons_overlay = _load_lessons(skill_name)
    outcome_guide = _OUTCOME_GUIDES.get(outcome_type, '- `"done"`')
    outcome_file = project_path / "phase-outcomes" / f"{phase}.json"

    iter_context = _build_iteration_context(project_path, phase, entry_ctx)

    return f"""{_TIER_PREAMBLE}# 项目上下文

**项目路径**：`{project_path}`
**当前阶段**：{description}
**Praxis 仓库**：`{PRAXIS_ROOT}`
{iter_context}
所有文档的读写均使用绝对路径（以 `{project_path}/` 为前缀）。

---

# Skill 执行指令

{skill_content}{lessons_overlay}

---

# 完成后的强制步骤：写入 Outcome

完成上方所有步骤之后，将本阶段的最终结果写入：

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

    if not project_path.is_dir():
        return {"action_type": "error",
                "message": f"Project path does not exist: {project_path}"}

    (project_path / "phase-outcomes").mkdir(exist_ok=True)

    action = get_next_action(str(project_path))

    if action["action_type"] != "skill":
        return action

    # Clear stale outcome file
    phase = action["phase"]
    stale = project_path / "phase-outcomes" / f"{phase}.json"
    if stale.exists():
        stale.unlink()

    fork_prompt = _build_fork_prompt(action, project_path)
    action["action_type"] = "skill"
    action["fork_prompt"] = fork_prompt
    action["model"] = "opus"
    action["project_path"] = str(project_path)

    return action


def cmd_advance(project_path_str: str, manual_outcome: str | None = None) -> dict:
    """Read outcome, advance state machine, return result."""
    project_path = Path(project_path_str).resolve()
    status = get_status(project_path)
    phase = status.get("phase", "init")

    if manual_outcome:
        result = advance(str(project_path), phase, manual_outcome)
        if "error" in result:
            return result
        result["notes"] = f"manual advance: {manual_outcome}"
        return result

    outcome_file = project_path / "phase-outcomes" / f"{phase}.json"
    if not outcome_file.exists():
        return {"error": "outcome_file_missing",
                "message": f"Fork agent did not write outcome to {outcome_file}",
                "phase": phase}

    try:
        data = json.loads(outcome_file.read_text(encoding="utf-8"))
    except Exception as e:
        return {"error": "outcome_parse_failed", "message": str(e), "phase": phase}

    outcome = data.get("outcome", "unknown")
    if outcome == "unknown":
        return {"error": "outcome_unknown", "phase": phase}

    result = advance(str(project_path), phase, outcome)
    if "error" in result:
        return result
    result["notes"] = data.get("notes", "")
    return result


def _cli():
    args = sys.argv[1:]
    if len(args) < 2:
        print(json.dumps({"error": "Usage: init_runner.py <next|advance|status|rollback> <project_path> [args]"}))
        sys.exit(1)

    cmd, project_path = args[0], args[1]

    if cmd == "next":
        result = cmd_next(project_path)
    elif cmd == "advance":
        manual_outcome = None
        if "--outcome" in args:
            idx = args.index("--outcome")
            if idx + 1 < len(args):
                manual_outcome = args[idx + 1]
        result = cmd_advance(project_path, manual_outcome)
    elif cmd == "status":
        result = get_status(Path(project_path).resolve())
    elif cmd == "rollback":
        # Delegate to state machine rollback
        phase = mode = ctx_file = None
        if "--phase" in args:
            phase = args[args.index("--phase") + 1]
        if "--mode" in args:
            mode = args[args.index("--mode") + 1]
        if "--context" in args:
            ctx_file = args[args.index("--context") + 1]
        if not phase or not mode:
            result = {"error": "rollback requires --phase and --mode"}
        else:
            result = rollback(project_path, phase, mode, ctx_file)
    else:
        result = {"error": f"Unknown command: {cmd}"}
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    _cli()
