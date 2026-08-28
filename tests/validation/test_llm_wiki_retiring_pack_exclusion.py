from __future__ import annotations

import pathlib
import subprocess
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]
GENERATOR = ROOT / "scripts/knowledge/generate-llm-wiki.py"
OUTPUTS = {
    "index": ROOT / "docs/90.references/data/0082-llm-wiki-index/README.md",
    "coverage": ROOT
    / "docs/90.references/data/0076-llm-wiki-stage-category-coverage/README.md",
}
RETIRED_WRAPPERS = (
    ROOT / "scripts/knowledge/generate-llm-wiki-index.sh",
    ROOT / "scripts/knowledge/generate-llm-wiki-coverage.sh",
)
RETIRING_PREFIX = "docs/90.references/research/0001-agentic-research-pack-refresh/"


class LlmWikiRetiringPackExclusionTest(unittest.TestCase):
    def test_retired_wrappers_are_absent_and_canonical_generator_is_current(self) -> None:
        self.assertTrue(GENERATOR.is_file())
        for wrapper in RETIRED_WRAPPERS:
            with self.subTest(wrapper=wrapper):
                self.assertFalse(wrapper.exists())

    def test_canonical_stdout_is_byte_exact_and_write_free_for_both_outputs(
        self,
    ) -> None:
        for artifact, output in OUTPUTS.items():
            with self.subTest(artifact=artifact):
                before = output.read_bytes()
                result = subprocess.run(
                    [
                        "python3",
                        str(GENERATOR),
                        "--stdout",
                        "--artifact",
                        artifact,
                    ],
                    cwd=ROOT,
                    capture_output=True,
                    check=False,
                    timeout=30,
                )
                self.assertEqual(0, result.returncode, result.stderr.decode())
                self.assertEqual(before, result.stdout)
                self.assertEqual(before, output.read_bytes())

    def test_canonical_generator_rejects_conflicting_or_incomplete_modes(self) -> None:
        invalid = (
            ("--check", "--write"),
            ("--stdout",),
            ("--artifact", "unknown"),
            ("--unknown",),
        )
        before = {path: path.read_bytes() for path in OUTPUTS.values()}
        for arguments in invalid:
            with self.subTest(arguments=arguments):
                result = subprocess.run(
                    ["python3", str(GENERATOR), *arguments],
                    cwd=ROOT,
                    capture_output=True,
                    check=False,
                    timeout=10,
                )
                self.assertNotEqual(0, result.returncode)
        self.assertEqual(before, {path: path.read_bytes() for path in OUTPUTS.values()})

    def test_retiring_pack_paths_are_excluded_from_both_projections(self) -> None:
        for output in OUTPUTS.values():
            with self.subTest(output=output):
                self.assertNotIn(
                    RETIRING_PREFIX,
                    output.read_text(encoding="utf-8"),
                )


if __name__ == "__main__":
    unittest.main()
