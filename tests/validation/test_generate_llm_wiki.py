from __future__ import annotations

import subprocess
import tempfile
import unittest
import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def load_generator():
    path = ROOT / "scripts/knowledge/generate-llm-wiki.py"
    spec = importlib.util.spec_from_file_location("generate_llm_wiki", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class LlmWikiGeneratorTests(unittest.TestCase):
    def _fixture_repo(self, root: Path) -> None:
        tracked = {
            ".agents/agent.md": "agent\n",
            ".claude/agent.md": "claude\n",
            ".codex/config.toml": "codex\n",
            ".github/workflow.yml": "workflow\n",
            "README.md": "root\n",
            "docs/04.execution/plan.md": "plan\n",
            "docs/90.references/data/knowledge/ref-0076-llm-wiki-stage-category-coverage.md": "coverage\n",
            "docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md": "index\n",
            "docs/한글-경로.md": "unicode\n",
            "scripts/tool.py": "python\n",
            "scripts/tool.sh": "shell\n",
            "scripts/knowledge/generate-llm-wiki.py": "merged\n",
        }
        for relative, content in tracked.items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        (root / "docs/arbitrary-untracked.md").write_text("untracked\n", encoding="utf-8")

    def test_generator_defaults_to_check_without_mutating_git_diff(self) -> None:
        before = subprocess.run(
            ["git", "diff", "--name-only"],
            cwd=ROOT,
            text=True,
            check=True,
            capture_output=True,
        ).stdout
        result = subprocess.run(
            ["python3", "scripts/knowledge/generate-llm-wiki.py"],
            cwd=ROOT,
            text=True,
            check=False,
            capture_output=True,
        )
        after = subprocess.run(
            ["git", "diff", "--name-only"],
            cwd=ROOT,
            text=True,
            check=True,
            capture_output=True,
        ).stdout
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(before, after)

    def test_write_mode_is_explicit_and_invalid_modes_fail_closed(self) -> None:
        generator = load_generator()
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "output.md"
            outputs = {output: "generated\n"}
            self.assertEqual(1, generator.apply_mode(outputs, "check"))
            self.assertFalse(output.exists())
            self.assertEqual(0, generator.apply_mode(outputs, "write"))
            self.assertEqual("generated\n", output.read_text(encoding="utf-8"))
            with self.assertRaises(ValueError):
                generator.apply_mode(outputs, "default-write")

    def test_build_outputs_collects_candidates_once(self) -> None:
        generator = load_generator()
        original = generator.collect_candidates
        calls = 0

        def counted(repo_root: Path):
            nonlocal calls
            calls += 1
            return original(repo_root)

        generator.collect_candidates = counted
        outputs = generator.build_outputs(ROOT)
        self.assertEqual(1, calls)
        self.assertEqual({generator.INDEX_OUTPUT, generator.COVERAGE_OUTPUT}, set(outputs))

    def test_tracked_nul_inventory_excludes_arbitrary_untracked_and_handles_unicode(self) -> None:
        generator = load_generator()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._fixture_repo(root)
            paths = {candidate.path for candidate in generator.collect_candidates(root)}
            self.assertIn("docs/한글-경로.md", paths)
            self.assertNotIn("docs/arbitrary-untracked.md", paths)

    def test_retired_wrapper_selection_and_classification_parity(self) -> None:
        generator = load_generator()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._fixture_repo(root)
            candidates = generator.collect_candidates(root)
            selected = {candidate.path: candidate.category for candidate in candidates}
            # Canonical 4b44cfd8 wrapper allowlist: .sh but not .py; only
            # .github/.claude/.codex hidden surfaces; docs/04 remains active.
            self.assertNotIn("scripts/tool.py", selected)
            self.assertIn("scripts/knowledge/generate-llm-wiki.py", selected)
            self.assertNotIn(".agents/agent.md", selected)
            self.assertEqual("Runtime surfaces", selected[".claude/agent.md"])
            self.assertEqual("Runtime surfaces", selected[".codex/config.toml"])
            self.assertEqual("Active stage docs", selected["docs/04.execution/plan.md"])
            index = generator.render_index(candidates)
            coverage = generator.render_coverage(candidates)
            self.assertIn("ref-0076-llm-wiki-stage-category-coverage.md", index)
            self.assertNotIn("ref-0082-llm-wiki-index.md](", index)
            self.assertNotIn("ref-0076-llm-wiki-stage-category-coverage.md](", coverage)
            self.assertNotIn("ref-0082-llm-wiki-index.md](", coverage)

    def test_exact_script_identity_parity_replaces_two_wrappers_with_one(self) -> None:
        generator = load_generator()
        script_paths = {
            candidate.path
            for candidate in generator.collect_candidates(ROOT)
            if candidate.category == "Scripts and validators"
        }
        self.assertEqual(43, len(script_paths))
        self.assertIn(generator.GENERATOR_PATH, script_paths)
        self.assertNotIn("scripts/knowledge/generate-llm-wiki-index.sh", script_paths)
        self.assertNotIn("scripts/knowledge/generate-llm-wiki-coverage.sh", script_paths)
        self.assertFalse(
            any(path.endswith(".py") for path in script_paths - {generator.GENERATOR_PATH})
        )


if __name__ == "__main__":
    unittest.main()
