from __future__ import annotations

import importlib.util
import pathlib
import subprocess
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]
CHECKER = ROOT / "scripts/validation/check-document-metadata.py"
PROFILES = ROOT / "docs/99.templates/support/document-metadata-profiles.yaml"
SERVICE_EXAMPLE = ROOT / "examples/sample-web-service/service.md"
TARGET_MANIFEST = (
    ROOT
    / "docs/90.references/data/governance/document-corpus-lifecycle/target-surface-convergence.yaml"
)
TARGET_ROOTS = (".github", "archive", "examples", "infra", "projects", "scripts", "secrets", "tests")

spec = importlib.util.spec_from_file_location("target_surface_metadata", CHECKER)
if spec is None or spec.loader is None:
    raise RuntimeError(f"unable to load checker module: {CHECKER}")
metadata = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = metadata
spec.loader.exec_module(metadata)


def tracked_paths(*pathspecs: str) -> list[pathlib.Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z", "--", *pathspecs],
        cwd=ROOT,
        capture_output=True,
        check=True,
    )
    return [pathlib.Path(raw.decode("utf-8")) for raw in result.stdout.split(b"\0") if raw]


class SampleServiceContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profiles = metadata.load_profiles(PROFILES)
        cls.text = SERVICE_EXAMPLE.read_text(encoding="utf-8")

    def test_sample_service_uses_canonical_metadata_in_canonical_order(self) -> None:
        self.assertEqual(
            {
                "status": "active",
                "artifact_id": "spec:sample-web-service",
                "artifact_type": "spec",
                "parent_ids": ["spec:133-target-surface-contract-convergence"],
            },
            metadata.parse_frontmatter(SERVICE_EXAMPLE),
        )
        frontmatter = self.text.split("---", 2)[1]
        keys = [
            line.split(":", 1)[0]
            for line in frontmatter.splitlines()
            if line and not line.startswith(" ")
        ]
        self.assertEqual(
            self.profiles["common"]["frontmatter_order"][:4],
            keys,
        )

    def test_sample_service_sections_follow_the_registered_service_role(self) -> None:
        role = self.profiles["template_roles"]["service"]
        headings = [line for line in self.text.splitlines() if line.startswith("## ")]
        self.assertEqual(role["required_headings"], headings)
        self.assertNotIn("## Template Usage", headings)

    def test_sample_service_contains_no_template_instruction_or_placeholder(self) -> None:
        for forbidden in (
            "<artifact-id>",
            "<parent-artifact-id>",
            "{{",
            "}}",
            "When authoring a real service",
            "copy the template",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, self.text)

    def test_migrated_typed_example_manifest_target_matches_document(self) -> None:
        document = metadata._safe_load_unique(  # noqa: SLF001
            TARGET_MANIFEST.read_text(encoding="utf-8")
        )
        row = next(
            entry
            for entry in document["entries"]
            if entry["source_path"] == "examples/sample-web-service/service.md"
        )
        frontmatter = metadata.parse_frontmatter(SERVICE_EXAMPLE)

        self.assertEqual("typed-example", row["surface_class"])
        self.assertEqual("migrate", row["disposition"])
        self.assertEqual(
            {
                "artifact_id": frontmatter["artifact_id"],
                "artifact_type_after": frontmatter["artifact_type"],
                "parent_ids": frontmatter["parent_ids"],
            },
            {
                "artifact_id": row["artifact_id"],
                "artifact_type_after": row["artifact_type_after"],
                "parent_ids": row["parent_ids"],
            },
        )


class TargetReadmeProfileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profiles = metadata.load_profiles(PROFILES)

    def test_all_75_target_readmes_match_exactly_one_profile(self) -> None:
        readmes = [
            path
            for path in tracked_paths(*TARGET_ROOTS)
            if path.name == "README.md"
        ]
        self.assertEqual(75, len(readmes))
        for path in readmes:
            with self.subTest(path=path.as_posix()):
                self.assertEqual(
                    1,
                    len(metadata.matching_readme_profiles(path, self.profiles)),
                )

    def test_native_markdown_and_typed_example_do_not_inherit_readme_profiles(self) -> None:
        native_or_typed_paths = (
            pathlib.Path(".github/PULL_REQUEST_TEMPLATE.md"),
            pathlib.Path(".github/SECURITY.md"),
            pathlib.Path("examples/sample-web-service/service.md"),
        )
        for path in native_or_typed_paths:
            with self.subTest(path=path.as_posix()):
                self.assertEqual(
                    [], metadata.matching_readme_profiles(path, self.profiles)
                )


class StorybookPhantomContractTests(unittest.TestCase):
    def test_active_surfaces_have_no_storybook_mcp_phantom_reference(self) -> None:
        active_paths = (
            ROOT / ".prettierignore",
            ROOT / "projects/storybook/README.md",
            ROOT / "projects/storybook/nextjs/README.md",
            ROOT / "scripts/knowledge/report-graphify-health.sh",
            ROOT / "scripts/hooks/agent-event-hook.sh",
        )
        for path in active_paths:
            with self.subTest(path=path.relative_to(ROOT).as_posix()):
                self.assertNotIn(
                    "projects/storybook/mcp", path.read_text(encoding="utf-8")
                )

    def test_storybook_has_no_tracked_gitlink(self) -> None:
        result = subprocess.run(
            ["git", "ls-files", "--stage", "--", "projects/storybook"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertFalse(
            any(line.startswith("160000 ") for line in result.stdout.splitlines())
        )

    def test_historical_spec_and_plan_evidence_remains_allowed(self) -> None:
        historical_owners = (
            ROOT / "docs/03.specs/133-target-surface-contract-convergence/spec.md",
            ROOT / "docs/04.execution/plans/2026-07-18-target-surface-contract-convergence.md",
        )
        for path in historical_owners:
            with self.subTest(path=path.relative_to(ROOT).as_posix()):
                self.assertIn(
                    "projects/storybook/mcp", path.read_text(encoding="utf-8")
                )


if __name__ == "__main__":
    unittest.main()
