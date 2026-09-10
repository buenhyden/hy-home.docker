from __future__ import annotations

import importlib.util
import pathlib
import sys
import tomllib
import unittest

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
RENDERER = ROOT / "scripts/operations/provider_surface_renderer.py"


def load_renderer():
    spec = importlib.util.spec_from_file_location("provider_surface_renderer", RENDERER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load {RENDERER}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ProviderNativeSurfaceTests(unittest.TestCase):
    def test_render_all_supports_exactly_claude_and_codex(self) -> None:
        renderer = load_renderer()
        records = renderer.render_all(ROOT, providers=("claude", "codex"))
        self.assertIsInstance(records, tuple)
        self.assertEqual({"claude", "codex"}, {item.provider for item in records})
        self.assertTrue(
            all(item.path.parts[0] in {".claude", ".codex"} for item in records)
        )

    def test_native_agents_preserve_provider_controls(self) -> None:
        renderer = load_renderer()
        projection = renderer.expected_native_projection(ROOT)
        claude = yaml.safe_load(
            projection[pathlib.Path(".claude/agents/code-reviewer.md")]
            .decode()
            .split("---\n", 2)[1]
        )
        codex = tomllib.loads(
            projection[pathlib.Path(".codex/agents/code-reviewer.toml")].decode()
        )
        self.assertEqual("claude-opus-5", claude["model"])
        self.assertEqual("high", claude["effort"])
        self.assertEqual("gpt-5.6-sol", codex["model"])
        self.assertEqual("xhigh", codex["model_reasoning_effort"])

    def test_claude_skills_have_exact_canonical_name_set(self) -> None:
        renderer = load_renderer()
        catalog = renderer.load_catalog(ROOT)
        projection = renderer.expected_native_projection(ROOT)
        expected = {item.skill_id for item in catalog.skills}
        actual = {
            path.parent.name
            for path in projection
            if path.parts[:2] == (".claude", "skills") and path.name == "SKILL.md"
        }
        self.assertEqual(expected, actual)

    def test_codex_roles_load_canonical_procedures_without_shared_projection(
        self,
    ) -> None:
        renderer = load_renderer()
        catalog = renderer.load_catalog(ROOT)
        projection = renderer.expected_native_projection(ROOT)
        self.assertFalse(any(path.parts[0] == ".agents" for path in projection))
        for role in catalog.roles:
            payload = tomllib.loads(
                projection[pathlib.Path(f".codex/agents/{role.agent_id}.toml")].decode()
            )
            for skill_id in role.skill_ids:
                self.assertIn(
                    f".agents/skills/{skill_id}/SKILL.md",
                    payload["developer_instructions"],
                )

    def test_all_skills_are_explicit_without_added_tool_grants(self) -> None:
        renderer = load_renderer()
        state = renderer.load_agent_governance(ROOT)
        self.assertEqual(14, len(state.roles))
        self.assertEqual(23, len(state.skills))
        for provider in state.provider_records:
            self.assertEqual(
                ".agents/skills/{skill_id}/SKILL.md", provider.canonical_skill_pattern
            )
        self.assertIsNone(state.provider_records[1].skill_pattern)
        projection = renderer.expected_native_projection(ROOT)
        for skill in state.skills:
            controls = yaml.safe_load(
                (ROOT / skill.source_path.parent / "agents/openai.yaml").read_text()
            )
            self.assertEqual({"policy": {"allow_implicit_invocation": False}}, controls)
            payload = projection[
                pathlib.Path(f".claude/skills/{skill.skill_id}/SKILL.md")
            ].decode()
            native = yaml.safe_load(payload.split("---\n", 2)[1])
            self.assertEqual(
                {"name", "description", "disable-model-invocation"}, set(native)
            )
            self.assertIs(native["disable-model-invocation"], True)
            self.assertEqual(skill.description, native["description"])
            self.assertNotIn("## Procedure", payload)

    def test_unknown_provider_fails_closed(self) -> None:
        renderer = load_renderer()
        with self.assertRaisesRegex(ValueError, "unsupported provider"):
            renderer.render_all(ROOT, providers=("claude", "unsupported"))


if __name__ == "__main__":
    unittest.main()
