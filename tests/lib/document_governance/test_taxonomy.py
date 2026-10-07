import unittest
from pathlib import Path, PurePosixPath

from scripts.lib.document_governance.taxonomy import (
    architecture_identity,
    find_dated_identity_parts,
    validate_stable_identity,
)

ROOT = Path(__file__).resolve().parents[3]


class StableDocumentTaxonomyTests(unittest.TestCase):
    def test_rejects_date_prefix_and_year_partition(self):
        self.assertEqual(
            ("2026", "2026-08-09-audit.md"),
            find_dated_identity_parts(
                PurePosixPath("docs/90.references/research/2026/2026-08-09-audit.md")
            ),
        )

    def test_incident_year_navigation_uses_its_distinct_path_profile(self):
        findings = validate_stable_identity(
            PurePosixPath("docs/05.operations/incidents/2026/README.md"),
            {"type": "common/readme"},
            {
                "incident-year-readme": {
                    "type": "common/readme",
                    "artifact_id_pattern": None,
                    "identity_relation": "none",
                },
                "readme": {
                    "type": "common/readme",
                    "artifact_id_pattern": None,
                    "identity_relation": "none",
                },
            },
            profile_id="incident-year-readme",
        )
        self.assertEqual([], findings)

    def test_accepts_architecture_description_identity(self):
        path = PurePosixPath("docs/02.architecture/descriptions/0001-gateway.md")
        self.assertEqual(
            ("architecture-description", "AD-0001"),
            architecture_identity(path),
        )
        findings = validate_stable_identity(
            path,
            {
                "artifact_id": "AD-0001",
                "type": "architecture-description",
            },
            {
                "architecture-description": {
                    "path_pattern": "docs/02.architecture/descriptions/{number:4}-{slug}.md",
                    "artifact_id_pattern": "AD-{number:4}",
                    "identity_relation": "direct",
                }
            },
        )
        self.assertEqual([], findings)

    def test_accepts_inherited_task_role_identity(self):
        findings = validate_stable_identity(
            PurePosixPath("docs/03.specs/spec-0999-example-change/task.md"),
            {
                "artifact_id": "task-0999-01",
                "type": "task",
            },
            {
                "task": {
                    "id_pattern": r"task-[0-9]{4}-[0-9]{2}",
                    "path_identity": "inherited",
                    "parent_id_pattern": (r"spec-(?P<identity>[0-9]{4})-[a-z0-9-]+"),
                    "artifact_id_identity_pattern": (
                        r"task-(?P<identity>[0-9]{4})-[0-9]{2}"
                    ),
                    "identity_capture": "identity",
                }
            },
        )
        self.assertEqual([], findings)

    def test_rejects_inherited_task_role_with_mismatched_identity(self):
        findings = validate_stable_identity(
            PurePosixPath("docs/03.specs/spec-0999-example-change/task.md"),
            {
                "artifact_id": "task-9999-01",
                "type": "task",
            },
            {
                "task": {
                    "id_pattern": r"task-[0-9]{4}-[0-9]{2}",
                    "path_identity": "inherited",
                    "parent_id_pattern": (r"spec-(?P<identity>[0-9]{4})-[a-z0-9-]+"),
                    "artifact_id_identity_pattern": (
                        r"task-(?P<identity>[0-9]{4})-[0-9]{2}"
                    ),
                    "identity_capture": "identity",
                }
            },
        )
        self.assertEqual(
            ["path-id-mismatch"],
            [finding.code for finding in findings],
        )

    def test_rejects_inherited_task_role_without_stable_parent(self):
        findings = validate_stable_identity(
            PurePosixPath("docs/03.specs/temporary-task/task.md"),
            {
                "artifact_id": "task-0136-01",
                "type": "task",
            },
            {
                "task": {
                    "id_pattern": r"task-[0-9]{4}-[0-9]{2}",
                    "path_identity": "inherited",
                    "parent_id_pattern": (r"spec-(?P<identity>[0-9]{4})-[a-z0-9-]+"),
                    "artifact_id_identity_pattern": (
                        r"task-(?P<identity>[0-9]{4})-[0-9]{2}"
                    ),
                    "identity_capture": "identity",
                }
            },
        )
        self.assertEqual(
            [
                "path-id-mismatch",
            ],
            [finding.code for finding in findings],
        )


if __name__ == "__main__":
    unittest.main()


class ActiveStageScopeTests(unittest.TestCase):
    """Current scan scopes and native provider paths name existing surfaces."""

    def active_scopes(self) -> tuple[tuple[str, tuple[str, ...]], ...]:
        from scripts.lib.document_governance import links, metadata_validator

        return (
            ("links._ACTIVE_STAGE_PREFIXES", links._ACTIVE_STAGE_PREFIXES),
            (
                "metadata_validator.TARGET_MARKDOWN_PREFIXES",
                metadata_validator.TARGET_MARKDOWN_PREFIXES,
            ),
        )

    def test_native_provider_files_are_exact_paths_not_directory_prefixes(self) -> None:
        from scripts.lib.document_governance.metadata.profile import (
            TARGET_MARKDOWN_FILES,
            _normalized_target_path,
        )

        self.assertEqual(
            {".claude/provider.md", ".codex/provider.md"}, set(TARGET_MARKDOWN_FILES)
        )
        for relative in TARGET_MARKDOWN_FILES:
            self.assertTrue((ROOT / relative).is_file())
            self.assertEqual(Path(relative), _normalized_target_path(relative))
            self.assertIsNone(_normalized_target_path(relative + "/private.md"))

    def test_every_active_stage_prefix_names_a_directory_that_exists(self) -> None:
        for name, prefixes in self.active_scopes():
            for prefix in prefixes:
                with self.subTest(scope=name, prefix=prefix):
                    self.assertTrue(
                        (ROOT / prefix.rstrip("/")).is_dir(),
                        f"{name} names {prefix}, which is not a directory",
                    )
