"""Executable evidence that prompt routing owns keywords and nothing else.

The dispatcher used to carry a `label`, `path`, and `desc` for each routed
skill, which made it a second, hand-maintained copy of the canonical skill
inventory: sixteen of twenty-three skills had drifted out of it entirely, and
the seven that remained described themselves in words their own `SKILL.md` no
longer used. These tests hold the corrected shape — a route is a keyword list,
the path is derived from the skill id, and the summary is read back from the
skill's own frontmatter at match time.
"""

from __future__ import annotations

import ast
import json
import pathlib
import subprocess
import unittest

from scripts.lib.document_governance.frontmatter import parse_frontmatter_text

ROOT = pathlib.Path(__file__).resolve().parents[2]
DISPATCHER = ROOT / "scripts/hooks/agent-event-hook.sh"
SKILL_ROOT = ROOT / ".agents/skills"


def routing_source() -> str:
    """Return the Python body the `UserPromptSubmit` branch executes."""
    lines = DISPATCHER.read_text(encoding="utf-8").splitlines()
    start = next(
        index
        for index, line in enumerate(lines)
        if line.strip() == "user_prompt_submit() {"
    )
    opening = next(
        index for index in range(start, len(lines)) if lines[index].endswith("<<'PY'")
    )
    closing = next(
        index for index in range(opening + 1, len(lines)) if lines[index] == "PY"
    )
    return "\n".join(lines[opening + 1 : closing])


def routes() -> dict[str, list[str]]:
    tree = ast.parse(routing_source())
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "ROUTES"
            for target in node.targets
        ):
            return ast.literal_eval(node.value)
    raise AssertionError("the routing branch declares no ROUTES table")


def canonical_skill_ids() -> set[str]:
    return {
        path.parent.name for path in SKILL_ROOT.glob("*/SKILL.md") if path.is_file()
    }


def canonical_description(skill_id: str) -> str:
    text = (SKILL_ROOT / skill_id / "SKILL.md").read_text(encoding="utf-8")
    metadata = parse_frontmatter_text(text)
    return str(metadata.get("description", ""))


def run_dispatcher(prompt: str) -> str:
    result = subprocess.run(
        ["bash", str(DISPATCHER), "UserPromptSubmit"],
        cwd=ROOT,
        input=json.dumps({"prompt": prompt}),
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
        env={"PATH": "/usr/bin:/bin", "CLAUDE_PROJECT_DIR": str(ROOT)},
    )
    if result.returncode != 0:
        raise AssertionError(f"dispatcher failed: {result.stderr}")
    if not result.stdout.strip():
        return ""
    payload = json.loads(result.stdout)
    return payload["hookSpecificOutput"]["additionalContext"]


class AgentFunctionRoutesTest(unittest.TestCase):
    def test_every_canonical_skill_is_reachable_from_a_prompt(self) -> None:
        """A skill nothing routes to is a skill callers keep re-deriving."""
        unrouted = canonical_skill_ids() - set(routes())
        self.assertEqual(set(), unrouted)

    def test_no_route_names_a_skill_that_does_not_exist(self) -> None:
        dangling = set(routes()) - canonical_skill_ids()
        self.assertEqual(set(), dangling)

    def test_a_route_declares_keywords_and_no_second_identity(self) -> None:
        """Re-adding a path or summary here would restore the drift."""
        source = routing_source()
        for key in ('"path"', '"desc"', '"label"'):
            self.assertNotIn(key, source)
        for skill_id, keywords in routes().items():
            self.assertTrue(keywords, f"{skill_id} routes on no keyword")
            for keyword in keywords:
                self.assertEqual(
                    keyword,
                    keyword.lower(),
                    f"{skill_id} keyword {keyword!r} can never match a lowered prompt",
                )

    def test_a_matched_route_reports_the_skill_s_own_description(self) -> None:
        context = run_dispatcher("please run a security audit")
        self.assertIn(".agents/skills/security-audit/SKILL.md", context)
        self.assertIn(canonical_description("security-audit"), context)

    def test_an_unmatched_prompt_adds_no_context(self) -> None:
        self.assertEqual("", run_dispatcher("good morning"))


if __name__ == "__main__":
    unittest.main()
