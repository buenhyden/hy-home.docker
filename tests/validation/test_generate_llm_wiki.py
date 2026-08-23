from __future__ import annotations

import subprocess
import tempfile
import time
import unittest
import importlib.util
import os
import sys
from pathlib import Path
from unittest import mock


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
            "docs/90.references/data/0076-llm-wiki-stage-category-coverage/README.md": "coverage\n",
            "docs/90.references/data/0082-llm-wiki-index/README.md": "index\n",
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
            self.assertIn("data/0076-llm-wiki-stage-category-coverage/README.md", index)
            self.assertNotIn("data/0082-llm-wiki-index/README.md](", index)
            self.assertNotIn("data/0076-llm-wiki-stage-category-coverage/README.md](", coverage)
            self.assertNotIn("data/0082-llm-wiki-index/README.md](", coverage)

    def test_exact_script_identity_excludes_transition_wrappers(self) -> None:
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

    def test_git_process_deadline_terminates_a_stalled_process_group(self) -> None:
        generator = load_generator()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            started = time.monotonic()
            with self.assertRaisesRegex(generator.GeneratorError, "deadline"):
                generator._run_git_bounded(
                    root,
                    ["-c", "alias.wait=!sleep 2", "wait"],
                    timeout_seconds=0.05,
                )
            self.assertLess(time.monotonic() - started, 1.0)

    def test_git_process_rejects_stdout_stderr_and_total_overflow(self) -> None:
        generator = load_generator()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            cases = (
                (
                    "stdout",
                    "alias.noisy=!python3 -c 'import sys;sys.stdout.write(\"o\"*64)'",
                    {"max_stdout": 16, "max_stderr": 128, "max_total": 128},
                ),
                (
                    "stderr",
                    "alias.noisy=!python3 -c 'import sys;sys.stderr.write(\"e\"*64)'",
                    {"max_stdout": 128, "max_stderr": 16, "max_total": 128},
                ),
                (
                    "total",
                    "alias.noisy=!python3 -c 'import sys;sys.stdout.write(\"o\"*16);sys.stderr.write(\"e\"*16)'",
                    {"max_stdout": 64, "max_stderr": 64, "max_total": 20},
                ),
            )
            for label, alias, bounds in cases:
                with self.subTest(label=label), self.assertRaisesRegex(
                    generator.GeneratorError, label
                ):
                    generator._run_git_bounded(
                        root,
                        ["-c", alias, "noisy"],
                        timeout_seconds=2,
                        **bounds,
                    )

    def test_tracked_path_count_is_bounded(self) -> None:
        generator = load_generator()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._fixture_repo(root)
            original = generator.MAX_TRACKED_PATHS
            generator.MAX_TRACKED_PATHS = 2
            try:
                with self.assertRaisesRegex(generator.GeneratorError, "path count"):
                    generator.collect_candidates(root)
            finally:
                generator.MAX_TRACKED_PATHS = original

    def test_candidate_validation_rejects_symlink_fifo_and_symlink_parent(self) -> None:
        generator = load_generator()
        for mutation in ("live-symlink", "broken-symlink", "fifo", "symlink-parent"):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                self._fixture_repo(root)
                candidate = root / "docs/한글-경로.md"
                if mutation == "symlink-parent":
                    real_parent = root / "docs-real"
                    (root / "docs").rename(real_parent)
                    (root / "docs").symlink_to(real_parent, target_is_directory=True)
                else:
                    candidate.unlink()
                    if mutation == "live-symlink":
                        victim = root / "victim.md"
                        victim.write_text("victim\n", encoding="utf-8")
                        candidate.symlink_to(victim)
                    elif mutation == "broken-symlink":
                        candidate.symlink_to(root / "missing.md")
                    else:
                        os.mkfifo(candidate)
                with self.assertRaisesRegex(
                    generator.GeneratorError, "symlink|regular|directory"
                ):
                    generator.collect_candidates(root)

    def test_candidate_validation_enforces_per_file_and_aggregate_bounds(self) -> None:
        generator = load_generator()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._fixture_repo(root)
            original_file = generator.MAX_CANDIDATE_FILE_BYTES
            original_total = generator.MAX_CANDIDATE_TOTAL_BYTES
            try:
                generator.MAX_CANDIDATE_FILE_BYTES = 3
                with self.assertRaisesRegex(generator.GeneratorError, "file.*bound"):
                    generator.collect_candidates(root)
                generator.MAX_CANDIDATE_FILE_BYTES = original_file
                generator.MAX_CANDIDATE_TOTAL_BYTES = 10
                with self.assertRaisesRegex(generator.GeneratorError, "aggregate"):
                    generator.collect_candidates(root)
            finally:
                generator.MAX_CANDIDATE_FILE_BYTES = original_file
                generator.MAX_CANDIDATE_TOTAL_BYTES = original_total

    def test_bounded_read_detects_a_leaf_swap_race(self) -> None:
        generator = load_generator()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "candidate.md"
            path.write_text("original", encoding="utf-8")
            replacement = Path(directory) / "replacement.md"
            replacement.write_text("replacement", encoding="utf-8")
            original_read = os.read
            swapped = False

            def swap_after_read(descriptor: int, size: int) -> bytes:
                nonlocal swapped
                chunk = original_read(descriptor, size)
                if chunk and not swapped:
                    swapped = True
                    os.replace(replacement, path)
                return chunk

            with mock.patch.object(generator.os, "read", side_effect=swap_after_read):
                with self.assertRaisesRegex(generator.GeneratorError, "changed during read"):
                    generator._read_bounded_regular_path(path, max_bytes=128)

    def test_candidate_read_rejects_immediate_and_partial_premature_eof(self) -> None:
        generator = load_generator()
        for mutation in ("immediate", "partial"):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                self._fixture_repo(root)
                candidate = root / "docs/한글-경로.md"
                identity = (candidate.stat().st_dev, candidate.stat().st_ino)
                original_read = os.read
                candidate_reads = 0

                def premature_eof(descriptor: int, size: int) -> bytes:
                    nonlocal candidate_reads
                    opened = os.fstat(descriptor)
                    if (opened.st_dev, opened.st_ino) != identity:
                        return original_read(descriptor, size)
                    candidate_reads += 1
                    if mutation == "partial" and candidate_reads == 1:
                        return original_read(descriptor, min(size, 3))
                    return b""

                with mock.patch.object(generator.os, "read", side_effect=premature_eof):
                    with self.assertRaisesRegex(generator.GeneratorError, "premature EOF"):
                        generator.collect_candidates(root)

    def test_current_output_read_rejects_immediate_and_partial_premature_eof(self) -> None:
        generator = load_generator()
        for mutation in ("immediate", "partial"):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as directory:
                output = Path(directory) / "generated.md"
                output.write_text("expected\n", encoding="utf-8")
                identity = (output.stat().st_dev, output.stat().st_ino)
                original_read = os.read
                output_reads = 0

                def premature_eof(descriptor: int, size: int) -> bytes:
                    nonlocal output_reads
                    opened = os.fstat(descriptor)
                    if (opened.st_dev, opened.st_ino) != identity:
                        return original_read(descriptor, size)
                    output_reads += 1
                    if mutation == "partial" and output_reads == 1:
                        return original_read(descriptor, min(size, 3))
                    return b""

                with mock.patch.object(generator.os, "read", side_effect=premature_eof):
                    with self.assertRaisesRegex(generator.GeneratorError, "premature EOF"):
                        generator.check_outputs({output: "expected\n"})

    def test_output_operations_reject_symlink_fifo_oversize_and_unsafe_parent(self) -> None:
        generator = load_generator()
        for mutation in ("symlink", "fifo", "oversize", "symlink-parent"):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                parent = root / "output"
                parent.mkdir()
                output = parent / "generated.md"
                victim = root / "victim.md"
                victim.write_text("victim\n", encoding="utf-8")
                if mutation == "symlink":
                    output.symlink_to(victim)
                elif mutation == "fifo":
                    os.mkfifo(output)
                elif mutation == "oversize":
                    output.write_text("x" * 64, encoding="utf-8")
                else:
                    real_parent = root / "real-output"
                    parent.rename(real_parent)
                    parent.symlink_to(real_parent, target_is_directory=True)
                original_bound = generator.MAX_OUTPUT_BYTES
                generator.MAX_OUTPUT_BYTES = 16
                try:
                    with self.assertRaises(generator.GeneratorError):
                        generator.apply_mode({output: "generated\n"}, "write" if mutation != "oversize" else "check")
                finally:
                    generator.MAX_OUTPUT_BYTES = original_bound
                self.assertEqual("victim\n", victim.read_text(encoding="utf-8"))

    def test_atomic_write_replaces_regular_leaf_without_temporary_residue(self) -> None:
        generator = load_generator()
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "generated.md"
            output.write_text("old\n", encoding="utf-8")
            previous_inode = output.stat().st_ino
            self.assertEqual(0, generator.apply_mode({output: "new\n"}, "write"))
            self.assertEqual("new\n", output.read_text(encoding="utf-8"))
            self.assertNotEqual(previous_inode, output.stat().st_ino)
            self.assertEqual(["generated.md"], sorted(path.name for path in output.parent.iterdir()))


if __name__ == "__main__":
    unittest.main()
