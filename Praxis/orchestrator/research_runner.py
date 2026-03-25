"""Research Module Runner — v3.

Builds the next action (with full fork-agent prompt) for the research module.
formalize → formalize_review → design → design_review → blueprint → implement → retrospective → complete

All phases use opus model (no standard tier).

CLI:
    python research_runner.py next    <project_path>  → print action JSON (with fork_prompt)
    python research_runner.py advance <project_path>  → read outcome, advance state, print result
    python research_runner.py advance <project_path> --outcome <outcome>  → manual advance
    python research_runner.py rollback <project_path> --phase <phase> --mode <mode> [--context <file>]
    python research_runner.py status  <project_path>  → print current status
"""

import json
import sys
from pathlib import Path

# Same package
sys.path.insert(0, str(Path(__file__).parent))
from research_state_machine import (
    get_next_action, advance, get_status, rollback, PHASES,
    save_status, _status_path,
)

PRAXIS_ROOT = Path(__file__).parent.parent
PROMPTS_DIR = PRAXIS_ROOT / "prompts"
LESSONS_DIR = Path.home() / ".noesis" / "lessons"

# Single opus-level preamble for all phases
_TIER_PREAMBLE = """\
> **Agent 角色定位**：你正在以**独立审稿人 / 综合决策者**身份执行此任务。
> 核心要求：严格、批判、不因礼貌软化判断。主动寻找方案漏洞、隐含假设和潜在风险。
> 研究质量依赖于你的严格把关——宁可多指出问题，不可放水通过。

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
    if prompt_name in ("formalize-review", "design-review"):
        config_file = PROMPTS_DIR / "review-configs" / f"{prompt_name}.yaml"
        if config_file.exists():
            cfg = config_file.read_text(encoding="utf-8")
            content = (
                f"# 审查配置（{prompt_name}.yaml）\n\n```yaml\n{cfg}\n```\n\n---\n\n"
                + content
            )
    return content


def _load_lessons(skill_name: str) -> str:
    """Load cross-project lessons for this skill type from ~/.noesis/lessons/.

    Filters out [ineffective] entries. Promotes [RECURRING] bullets to top.
    """
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
        "> 以下教训来自历史项目的 Retrospective。[RECURRING] 为跨项目反复出现的高优先级问题。\n\n"
        + filtered
    )


def _load_reflect_prompt() -> str:
    """Load the phase reflection prompt (injected after every non-manual phase)."""
    reflect_file = PROMPTS_DIR / "X-reflect-pipeline-prompt.md"
    if not reflect_file.exists():
        return ""
    return reflect_file.read_text(encoding="utf-8")


# ─────────────────────────────────────────────────────────────────
# Entry context → iteration injection
# ─────────────────────────────────────────────────────────────────

def _build_iteration_context(project_path: Path, phase: str,
                              entry_context: dict | None, iter_count: int) -> str:
    """Build iteration context injection block based on entry_context."""
    if not entry_context:
        if iter_count > 0:
            iter_log = project_path / "iteration-log.md"
            if iter_log.exists():
                return (
                    f"\n## 迭代模式：Pivot（第 {iter_count + 1} 轮）\n\n"
                    f"前序方向已排除，迭代日志：`{iter_log}`（必须全文读取）\n\n"
                    f"执行要点：\n"
                    f"- 理解所有已排除方向和根因\n"
                    f"- **严禁**重复 iteration-log.md 中已排除的方向\n"
                )
        return ""

    mode = entry_context.get("mode", "first")

    if mode == "first":
        return ""

    # formalize_review revise → formalize
    if mode == "fr_revise":
        review_file = entry_context.get("review_file", "")
        full_path = project_path / review_file if review_file else ""
        return (
            f"\n## 迭代模式：FR-Revise（基于问题锐化审查意见修改）\n\n"
            f"审查已完成，综合意见文件：`{full_path}`（必须全文读取）\n\n"
            f"执行要点：\n"
            f"- 逐条理解审查意见中的 '必须修改的内容'\n"
            f"- **不从零开始**——保留已通过审查的内容\n"
            f"- 更新文档 frontmatter 版本号（minor +1）\n"
        )

    # design_review revise → design
    if mode == "dr_revise":
        review_file = entry_context.get("review_file", "")
        full_path = project_path / review_file if review_file else ""
        return (
            f"\n## 迭代模式：DR-Revise（基于设计审查意见修改）\n\n"
            f"设计审查已完成，综合意见文件：`{full_path}`（必须全文读取）\n\n"
            f"执行要点：\n"
            f"- 读设计审查意见，定位需要修改的组件/实验\n"
            f"- 保留未被质疑的部分，针对性修改\n"
            f"- 确保方法-实验交叉引用保持一致\n"
            f"- 更新文档 frontmatter 版本号（minor +1）\n"
        )

    # direction_pivot (from design_review fundamental, implement iterate_direction, design escalate)
    if mode == "direction_pivot":
        result_file = entry_context.get("result_file", "")
        reason = entry_context.get("reason", "")
        iter_log = project_path / "iteration-log.md"

        result_line = ""
        if result_file:
            result_line = f"- 实验结果：`{project_path / result_file}`（如存在，必须全文读取）\n"

        reason_line = ""
        if reason == "iteration_guard":
            reason_line = (
                f"- **触发原因**：设计阶段迭代守卫（design 迭代次数过多，强制升级）\n"
            )

        # Reference downstream docs for context
        downstream = []
        for doc in ["research/method-design.md", "research/experiment-design.md",
                     "Codes/_Results/experiment_result.md"]:
            if (project_path / doc).exists():
                downstream.append(doc)

        downstream_lines = ""
        if downstream:
            doc_list = "\n".join(f"  - `{d}`" for d in downstream)
            downstream_lines = (
                f"\n前序迭代产出文档（参考，获取完整失败上下文）：\n{doc_list}\n"
            )

        return (
            f"\n## 迭代模式：Direction-Pivot（方向层问题，重新审视 Gap 和攻击角度）\n\n"
            f"核心假设或攻击方向需要重新审视。\n"
            f"{result_line}"
            f"{reason_line}"
            f"- 迭代日志：`{iter_log}`（必须全文读取）\n"
            f"{downstream_lines}\n"
            f"执行要点：\n"
            f"- Gap 定义和攻击角度都需要重新审视\n"
            f"- 从失败中获得的关键洞察是最有价值的资产\n"
            f"- **严禁**重复 iteration-log.md 中已排除的方向\n"
            f"- 更新文档 frontmatter 版本号（major +1）\n"
        )

    # method_iterate (from implement iterate_method)
    if mode == "method_iterate":
        result_file = entry_context.get("result_file", "")
        iter_log = project_path / "iteration-log.md"

        result_line = ""
        if result_file:
            result_line = f"- 实验结果：`{project_path / result_file}`（必须全文读取）\n"

        return (
            f"\n## 迭代模式：Method-Iterate（方法层问题，修改失败组件）\n\n"
            f"实验执行发现方法层问题。\n"
            f"{result_line}"
            f"- 迭代日志：`{iter_log}`（必须全文读取）\n\n"
            f"执行要点：\n"
            f"- 理解哪些组件有问题，保留已验证有效的组件\n"
            f"- 只重新设计失败组件及其对应实验\n"
            f"- 读 iteration-log.md 确认已排除的替代方案\n"
            f"- 更新文档 frontmatter 版本号（major +1）\n"
        )

    return ""


# ─────────────────────────────────────────────────────────────────
# Outcome guides
# ─────────────────────────────────────────────────────────────────

_OUTCOME_GUIDES = {
    "work": '- `"done"` — 正常完成',
    "formalize_review": (
        '- `"pass"` — 审查通过，进入联合设计\n'
        '- `"revise"` — 需要修改，回到 formalize 问题锐化\n'
        '- `"abandon"` — 放弃，进入 complete'
    ),
    "design_review": (
        '- `"pass"` — 审查通过，进入实现蓝图\n'
        '- `"revise"` — 技术问题，回到 design 联合设计\n'
        '- `"fundamental"` — 问题定义层面有误，回到 formalize 问题锐化\n'
        '- `"abandon"` — 放弃，进入 complete'
    ),
    "manual": (
        '手动阶段 — 无需写入 outcome 文件。\n'
        '完成后通过 CLI 推进：\n'
        '  - `--outcome success` — 验证通过，进入知识回收\n'
        '  - `--outcome iterate_method` — 方法层失败，回到 design\n'
        '  - `--outcome iterate_direction` — 方向层失败，回到 formalize\n'
        '  - `--outcome abandon` — 放弃，进入 complete'
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
    iter_count = action.get("iteration_count", 0)
    entry_ctx = action.get("entry_context")

    skill_content = _load_prompt_content(skill_name)
    lessons_overlay = _load_lessons(skill_name)
    reflect_content = _load_reflect_prompt()
    outcome_guide = _OUTCOME_GUIDES.get(outcome_type, '- `"done"`')
    outcome_file = project_path / "phase-outcomes" / f"{phase}.json"

    iter_context = _build_iteration_context(project_path, phase, entry_ctx, iter_count)

    reflect_section = ""
    if reflect_content:
        reflect_section = f"\n\n---\n\n{reflect_content}"

    return f"""{_TIER_PREAMBLE}# 项目上下文

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
    """Build the fork prompt for an optional parallel Codex/external-AI agent."""
    phase = action["phase"]
    description = action["description"]

    prompt_content = _load_prompt_content(codex_agent)
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

    if not project_path.is_dir():
        return {
            "action_type": "error",
            "message": f"Project path does not exist: {project_path}",
        }

    (project_path / "phase-outcomes").mkdir(exist_ok=True)
    (project_path / "codex-reviews").mkdir(exist_ok=True)

    action = get_next_action(str(project_path))

    if action["action_type"] == "manual":
        # Enrich manual phase with specific messages
        phase = action["phase"]
        runner = str(Path(__file__).parent / "research_runner.py")
        p = project_path_str

        if phase == "implement":
            action["message"] = (
                f"当前处于编码实验阶段（手动）。\n"
                f"请与 AI 协作完成代码编写和实验运行（参考 Codes/ 目录）。\n"
                f"完成后：\n"
                f"  - 验证通过 → python3 {runner} advance {p} --outcome success\n"
                f"  - 方法层失败 → python3 {runner} advance {p} --outcome iterate_method\n"
                f"  - 方向层失败 → python3 {runner} advance {p} --outcome iterate_direction\n"
                f"  - 放弃 → python3 {runner} advance {p} --outcome abandon"
            )
        return action

    if action["action_type"] != "skill":
        return action  # "done" or "error" — pass through

    # Clear stale outcome file
    phase = action["phase"]
    stale_outcome = project_path / "phase-outcomes" / f"{phase}.json"
    if stale_outcome.exists():
        stale_outcome.unlink()

    main_fork_prompt = _build_fork_prompt(action, project_path)

    # Check for codex agent support (formalize_review and design_review)
    codex_agent = None
    if phase in ("formalize_review", "design_review"):
        codex_agent = "codex-reviewer"

    if codex_agent:
        action["action_type"] = "skills_parallel"
        action["skills"] = [
            {
                "role": "main",
                "description": action["description"],
                "fork_prompt": main_fork_prompt,
                "model": "opus",
            },
            {
                "role": "codex",
                "description": f"Codex 外部审查: {action['description']}",
                "fork_prompt": _build_codex_prompt(codex_agent, action, project_path),
                "model": "sonnet",  # codex agent is just MCP dispatch
            },
        ]
    else:
        action["action_type"] = "skill"
        action["fork_prompt"] = main_fork_prompt
        action["model"] = "opus"

    action["project_path"] = str(project_path)

    # Iteration guards
    entry_ctx = action.get("entry_context") or {}

    # design >= 2 iterations → escalate warning
    if phase == "design" and entry_ctx.get("design_iteration_count", 0) >= 2:
        action["iteration_warning"] = (
            f"⚠️  design（联合设计）已迭代 {entry_ctx['design_iteration_count']} 次。\n"
            f"   根据迭代守卫规则，建议升级到 formalize（问题锐化）重新审视方向。\n"
            f"   继续 design 迭代？回复 yes 继续，escalate 升级到 formalize，stop 退出。"
        )

    # formalize >= 3 iterations → abandon warning
    if phase == "formalize" and entry_ctx.get("formalize_iteration_count", 0) >= 3:
        action["iteration_warning"] = (
            f"⚠️  formalize（问题锐化）已迭代 {entry_ctx['formalize_iteration_count']} 次。\n"
            f"   根据迭代守卫规则，建议评估是否 abandon 项目。\n"
            f"   回复 yes 继续迭代，abandon 放弃进入 complete，stop 退出。"
        )

    # General iteration warning
    iter_count = action.get("iteration_count", 0)
    if iter_count >= 3 and "iteration_warning" not in action:
        action["iteration_warning"] = (
            f"⚠️  阶段 {phase} 已迭代 {iter_count} 次，"
            f"可能陷入循环。请检查项目状态后决定是否继续。"
        )

    return action


def cmd_advance(project_path_str: str, manual_outcome: str | None = None) -> dict:
    """Read outcome, advance state machine, return result."""
    project_path = Path(project_path_str).resolve()
    status = get_status(project_path)
    phase = status.get("phase", "formalize")

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
    if len(args) < 2 and (not args or args[0] != "phases"):
        print(json.dumps({"error": "Usage: research_runner.py <next|advance|status|rollback> <project_path> [args]"}))
        sys.exit(1)

    cmd = args[0]

    if cmd == "next":
        result = cmd_next(args[1])
    elif cmd == "advance":
        manual_outcome = None
        if "--outcome" in args:
            idx = args.index("--outcome")
            if idx + 1 < len(args):
                manual_outcome = args[idx + 1]
        result = cmd_advance(args[1], manual_outcome)
    elif cmd == "status":
        result = get_status(Path(args[1]).resolve())
    elif cmd == "rollback":
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
            result = rollback(args[1], phase, mode, ctx_file)
    else:
        result = {"error": f"Unknown command: {cmd}"}
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    _cli()
