from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
INDEX_GENERATOR = Path("scripts/knowledge/generate-llm-wiki-index.sh")
COVERAGE_GENERATOR = Path("scripts/knowledge/generate-llm-wiki-coverage.sh")
INDEX_OUTPUT = Path("docs/90.references/llm-wiki/llm-wiki-index.md")
COVERAGE_OUTPUT = Path(
    "docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md"
)
RETIRING_PREFIX = (
    "docs/90.references/research/2026-07-05-agentic-research-pack-refresh/"
)
NEW_PREFIX = (
    "docs/90.references/research/"
    "2026-08-08-agentic-engineering-research-pack/"
)
SIBLING_PATH = (
    "docs/90.references/research/"
    "2026-07-05-agentic-research-pack-refresh-notes/README.md"
)
PLAN_PATH = "docs/04.execution/plans/2026-07-05-agentic-research-pack-refresh.md"
TASK_PATH = "docs/04.execution/tasks/2026-07-05-agentic-research-pack-refresh.md"

PACK_FILES = (
    "README.md",
    "agent-instructions-vibe-coding.md",
    "agent-model-selection.md",
    "ai-agent-catalogs.md",
    "automation-pipeline-workflow.md",
    "docker-compose-infrastructure.md",
    "document-metadata-lifecycle.md",
    "documentation-architecture.md",
    "harness-engineering.md",
    "llm-wiki-system.md",
    "loop-engineering.md",
    "memory-hierarchy.md",
    "provider-implementation-comparison.md",
    "provider-model-landscape.md",
    "quality-ci-formatting.md",
    "scope-application-matrix.md",
    "sdlc-document-roles.md",
    "security-governance.md",
    "spec-driven-sdlc.md",
    "workspace-baseline.md",
)


def run(command: list[str], *, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    )


def write_fixture_file(root: Path, relative_path: str) -> None:
    target = root / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(f"# Fixture: {relative_path}\n")


def coverage_metrics(content: str) -> dict[str, int]:
    patterns = {
        "safe paths": r"^- Safe tracked source paths: `(\d+)`$",
        "docs/90.references": r"^\| `docs/90\.references` \| (\d+) \|",
        "Reference and template docs": (
            r"^\| Reference and template docs \| (\d+) \|"
        ),
        "folder index": r"^\| folder index \| (\d+) \|",
        "Markdown reference": r"^\| Markdown reference \| (\d+) \|",
    }
    metrics: dict[str, int] = {}
    for label, pattern in patterns.items():
        match = re.search(pattern, content, re.MULTILINE)
        if match is None:
            raise AssertionError(f"coverage metric is missing: {label}")
        metrics[label] = int(match.group(1))
    return metrics


class LlmWikiRetiringPackExclusionTest(unittest.TestCase):
    def create_repository(self, root: Path) -> None:
        run(["git", "init", "--quiet"], cwd=root)

        for generator in (INDEX_GENERATOR, COVERAGE_GENERATOR):
            target = root / generator
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(REPOSITORY_ROOT / generator, target)

        for filename in PACK_FILES:
            write_fixture_file(root, f"{RETIRING_PREFIX}{filename}")
            write_fixture_file(root, f"{NEW_PREFIX}{filename}")

        for retained_path in (SIBLING_PATH, PLAN_PATH, TASK_PATH):
            write_fixture_file(root, retained_path)

        run(["git", "add", "."], cwd=root)

    def generate(self, root: Path) -> tuple[bytes, bytes]:
        run(["bash", str(INDEX_GENERATOR)], cwd=root)
        run(["bash", str(COVERAGE_GENERATOR)], cwd=root)
        return (
            (root / INDEX_OUTPUT).read_bytes(),
            (root / COVERAGE_OUTPUT).read_bytes(),
        )

    def test_retiring_pack_is_projection_invariant_until_deletion(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.create_repository(root)

            coexisting_index, coexisting_coverage = self.generate(root)

            run(
                ["git", "rm", "--cached", "--quiet", "-r", RETIRING_PREFIX],
                cwd=root,
            )
            post_delete_index, post_delete_coverage = self.generate(root)

            coexisting_metrics = coverage_metrics(coexisting_coverage.decode())
            post_delete_metrics = coverage_metrics(post_delete_coverage.decode())
            observed_deltas = {
                label: post_delete_metrics[label] - coexisting_metrics[label]
                for label in coexisting_metrics
            }
            if coexisting_coverage != post_delete_coverage:
                self.assertEqual(
                    observed_deltas,
                    {
                        "safe paths": -20,
                        "docs/90.references": -20,
                        "Reference and template docs": -20,
                        "folder index": -1,
                        "Markdown reference": -19,
                    },
                )

            delta_evidence = f"temporary-index deletion deltas: {observed_deltas}"
            self.assertEqual(
                coexisting_index,
                post_delete_index,
                msg=delta_evidence,
            )
            self.assertEqual(
                coexisting_coverage,
                post_delete_coverage,
                msg=delta_evidence,
            )

            decoded_index = coexisting_index.decode()
            decoded_coverage = coexisting_coverage.decode()
            for filename in PACK_FILES:
                self.assertNotIn(f"{RETIRING_PREFIX}{filename}", decoded_index)
                self.assertNotIn(f"{RETIRING_PREFIX}{filename}", decoded_coverage)
                self.assertIn(f"{NEW_PREFIX}{filename}", decoded_index)

            for retained_path in (SIBLING_PATH, PLAN_PATH, TASK_PATH):
                self.assertIn(retained_path, decoded_index)
                self.assertIn(retained_path, decoded_coverage)

            for filename in PACK_FILES:
                retained_path = f"{NEW_PREFIX}{filename}"
                run(
                    ["git", "rm", "--cached", "--quiet", retained_path],
                    cwd=root,
                )
                run(["bash", str(COVERAGE_GENERATOR)], cwd=root)
                without_path_metrics = coverage_metrics(
                    (root / COVERAGE_OUTPUT).read_text(encoding="utf-8")
                )
                expected_delta = {
                    "safe paths": -1,
                    "docs/90.references": -1,
                    "Reference and template docs": -1,
                    "folder index": -1 if filename == "README.md" else 0,
                    "Markdown reference": 0 if filename == "README.md" else -1,
                }
                self.assertEqual(
                    expected_delta,
                    {
                        label: without_path_metrics[label] - coexisting_metrics[label]
                        for label in coexisting_metrics
                    },
                    msg=f"new-pack coverage projection omitted {retained_path}",
                )
                run(["git", "add", retained_path], cwd=root)


if __name__ == "__main__":
    unittest.main()
