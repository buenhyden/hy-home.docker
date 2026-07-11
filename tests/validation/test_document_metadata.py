from __future__ import annotations

import importlib.util
import pathlib
import subprocess
import sys
import tempfile
import unittest

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[2]
CHECKER = ROOT / "scripts" / "validation" / "check-document-metadata.py"
PROFILES = ROOT / "docs" / "99.templates" / "support" / "document-metadata-profiles.yaml"

spec = importlib.util.spec_from_file_location("check_document_metadata", CHECKER)
if spec is None or spec.loader is None:
    raise RuntimeError(f"unable to load checker module: {CHECKER}")
metadata = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = metadata
spec.loader.exec_module(metadata)


def write_doc(path: pathlib.Path, frontmatter: dict[str, object] | None, body: str = "# Fixture\n") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if frontmatter is None:
        path.write_text(body, encoding="utf-8")
        return
    rendered = yaml.safe_dump(frontmatter, sort_keys=False).rstrip()
    path.write_text(f"---\n{rendered}\n---\n\n{body}", encoding="utf-8")


def run_checker(root: pathlib.Path, mode: str = "report", *extra: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(CHECKER),
            "--root",
            str(root),
            "--profiles",
            str(PROFILES),
            "--mode",
            mode,
            *extra,
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


class FrontmatterParsingTests(unittest.TestCase):
    def test_valid_yaml_frontmatter_is_parsed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "valid.md"
            write_doc(path, {"status": "active", "parent_ids": ["PRD-001"]})
            self.assertEqual(
                {"status": "active", "parent_ids": ["PRD-001"]},
                metadata.parse_frontmatter(path),
            )

    def test_missing_frontmatter_returns_empty_mapping(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "README.md"
            write_doc(path, None)
            self.assertEqual({}, metadata.parse_frontmatter(path))

    def test_invalid_yaml_frontmatter_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "invalid.md"
            path.write_text("---\nstatus: [active\n---\n# Invalid\n", encoding="utf-8")
            with self.assertRaises(metadata.FrontmatterError):
                metadata.parse_frontmatter(path)

    def test_duplicate_yaml_key_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "duplicate.md"
            path.write_text("---\nstatus: active\nstatus: completed\n---\n", encoding="utf-8")
            with self.assertRaises(metadata.FrontmatterError):
                metadata.parse_frontmatter(path)


class ArtifactInferenceTests(unittest.TestCase):
    def test_supported_paths_infer_explicit_profiles(self) -> None:
        cases = {
            "docs/01.requirements/123-example.md": "prd",
            "docs/02.architecture/requirements/0123-example.md": "ard",
            "docs/02.architecture/decisions/0123-example.md": "adr",
            "docs/03.specs/123-example/spec.md": "spec",
            "docs/04.execution/plans/2026-07-11-example.md": "plan",
            "docs/04.execution/tasks/2026-07-11-example.md": "task",
            "docs/05.operations/guides/00-workspace/example.md": "guide",
            "docs/05.operations/policies/00-workspace/example.md": "policy",
            "docs/05.operations/runbooks/00-workspace/example.md": "runbook",
            "docs/05.operations/incidents/2026/INC-001-example/INC-001-example.md": "incident",
            "docs/05.operations/incidents/2026/INC-001-example/postmortem.md": "postmortem",
            "docs/05.operations/releases/2026-07-11.md": "release",
            "docs/90.references/research/example.md": "reference",
            "docs/90.references/audits/example.md": "audit",
            "docs/98.archive/04.execution/example.md": "archive",
            "docs/99.templates/templates/sdlc/spec.template.md": "template-source",
            "docs/00.agent-governance/rules/example.md": "governance",
            "README.md": "readme",
            "misc/example.md": "unsupported",
        }
        for path, expected in cases.items():
            with self.subTest(path=path):
                self.assertEqual(expected, metadata.infer_artifact_type(pathlib.Path(path)))


class MetadataValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profiles = metadata.load_profiles(PROFILES)

    def record(
        self,
        path: str,
        values: dict[str, object],
        artifact_type: str,
        previous_status: str | None = None,
    ):
        return metadata.Record(
            pathlib.Path(path),
            values,
            artifact_type,
            previous_status=previous_status,
        )

    def codes(self, record, records=()) -> list[str]:
        all_records = [*records, record]
        manifest = metadata.build_manifest(all_records)
        return [finding.code for finding in metadata.validate_record(record, self.profiles, manifest)]

    def test_valid_spec_metadata_passes(self) -> None:
        parent = self.record(
            "docs/01.requirements/123-parent.md",
            {"status": "active", "artifact_id": "PRD-123", "artifact_type": "prd", "parent_ids": []},
            "prd",
        )
        spec_record = self.record(
            "docs/03.specs/123-example/spec.md",
            {
                "status": "active",
                "artifact_id": "SPEC-123",
                "artifact_type": "spec",
                "parent_ids": ["PRD-123"],
            },
            "spec",
        )
        self.assertEqual([], self.codes(spec_record, [parent]))

    def test_readme_without_frontmatter_is_an_explicit_exception(self) -> None:
        record = self.record("docs/03.specs/README.md", {}, "readme")
        self.assertEqual([], self.codes(record))

    def test_readme_rejects_copied_template_draft_status(self) -> None:
        record = self.record("docs/03.specs/README.md", {"status": "draft"}, "readme")
        self.assertIn("invalid-status", self.codes(record))

    def test_unresolved_parent_is_reported(self) -> None:
        record = self.record(
            "docs/03.specs/123-example/spec.md",
            {
                "status": "active",
                "artifact_id": "SPEC-123",
                "artifact_type": "spec",
                "parent_ids": ["PRD-MISSING"],
            },
            "spec",
        )
        self.assertIn("unresolved-parent", self.codes(record))

    def test_wrong_parent_type_and_parent_cycle_are_reported(self) -> None:
        parent = self.record(
            "docs/04.execution/tasks/2026-07-11-parent.md",
            {
                "status": "active",
                "artifact_id": "TASK-PARENT",
                "artifact_type": "task",
                "parent_ids": ["SPEC-CHILD"],
            },
            "task",
        )
        child = self.record(
            "docs/03.specs/123-example/spec.md",
            {
                "status": "active",
                "artifact_id": "SPEC-CHILD",
                "artifact_type": "spec",
                "parent_ids": ["TASK-PARENT"],
            },
            "spec",
        )
        codes = self.codes(child, [parent])
        self.assertIn("invalid-parent-type", codes)
        self.assertIn("parent-cycle", codes)

    def test_declared_type_must_match_inferred_profile(self) -> None:
        record = self.record(
            "docs/03.specs/123-example/spec.md",
            {
                "status": "active",
                "artifact_id": "SPEC-123",
                "artifact_type": "plan",
                "parent_ids": [],
            },
            "spec",
        )
        self.assertIn("artifact-type-mismatch", self.codes(record))

    def test_forbidden_and_type_inappropriate_keys_are_reported(self) -> None:
        record = self.record(
            "docs/03.specs/123-example/spec.md",
            {
                "status": "active",
                "artifact_id": "SPEC-123",
                "artifact_type": "spec",
                "parent_ids": [],
                "type": "spec",
                "archived_from": "docs/03.specs/old/spec.md",
            },
            "spec",
        )
        codes = self.codes(record)
        self.assertIn("forbidden-key", codes)
        self.assertIn("type-inappropriate-key", codes)

    def test_valid_forward_lifecycle_transition_passes(self) -> None:
        record = self.record(
            "docs/04.execution/tasks/2026-07-11-example.md",
            {
                "status": "completed",
                "artifact_id": "TASK-2026-07-11-EXAMPLE",
                "artifact_type": "task",
                "parent_ids": [],
            },
            "task",
            previous_status="active",
        )
        self.assertNotIn("invalid-transition", self.codes(record))

    def test_reverse_lifecycle_transition_is_reported(self) -> None:
        record = self.record(
            "docs/04.execution/tasks/2026-07-11-example.md",
            {
                "status": "active",
                "artifact_id": "TASK-2026-07-11-EXAMPLE",
                "artifact_type": "task",
                "parent_ids": [],
            },
            "task",
            previous_status="completed",
        )
        self.assertIn("invalid-transition", self.codes(record))

    def test_superseded_artifact_requires_resolvable_replacement(self) -> None:
        record = self.record(
            "docs/03.specs/123-example/spec.md",
            {
                "status": "superseded",
                "artifact_id": "SPEC-OLD",
                "artifact_type": "spec",
                "parent_ids": [],
            },
            "spec",
        )
        self.assertIn("replacement-free-supersession", self.codes(record))

    def test_replacement_requires_superseded_target_state(self) -> None:
        old = self.record(
            "docs/03.specs/122-old/spec.md",
            {
                "status": "active",
                "artifact_id": "SPEC-OLD",
                "artifact_type": "spec",
                "parent_ids": [],
            },
            "spec",
        )
        new = self.record(
            "docs/03.specs/123-new/spec.md",
            {
                "status": "active",
                "artifact_id": "SPEC-NEW",
                "artifact_type": "spec",
                "parent_ids": [],
                "supersedes": ["SPEC-OLD"],
            },
            "spec",
        )
        self.assertIn("invalid-supersession-state", self.codes(new, [old]))

    def test_generated_document_uses_generator_profile(self) -> None:
        record = self.record(
            "docs/90.references/data/example.md",
            {"status": "active", "generated_by": "scripts/example.py"},
            "generated",
        )
        self.assertEqual([], self.codes(record))

    def test_generated_document_rejects_human_typed_identity(self) -> None:
        record = self.record(
            "docs/90.references/data/example.md",
            {
                "status": "active",
                "generated_by": "scripts/example.py",
                "artifact_id": "REF-GENERATED",
            },
            "generated",
        )
        self.assertIn("type-inappropriate-key", self.codes(record))


class CheckerCliTests(unittest.TestCase):
    def test_duplicate_artifact_id_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            values = {
                "status": "active",
                "artifact_id": "SPEC-123",
                "artifact_type": "spec",
                "parent_ids": [],
            }
            write_doc(root / "docs/03.specs/123-a/spec.md", values)
            write_doc(root / "docs/03.specs/123-b/spec.md", values)
            result = run_checker(root, "report")
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn("duplicate-artifact-id", result.stdout)

    def test_report_returns_nonzero_for_parser_failure_but_renders_inventory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            path = root / "docs/03.specs/123-example/spec.md"
            path.parent.mkdir(parents=True)
            path.write_text("---\nstatus: [active\n---\n", encoding="utf-8")
            result = run_checker(root, "report")
            self.assertNotEqual(0, result.returncode)
            self.assertIn("frontmatter-parse-error", result.stdout)
            self.assertIn(path.relative_to(root).as_posix(), result.stdout)

    def test_changed_mode_fails_only_selected_violations(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            invalid = root / "docs/03.specs/123-example/spec.md"
            valid = root / "docs/03.specs/README.md"
            write_doc(invalid, {"status": "active"})
            write_doc(valid, None)
            passing = run_checker(root, "check-changed", "--changed-path", "docs/03.specs/README.md")
            failing = run_checker(
                root,
                "check-changed",
                "--changed-path",
                "docs/03.specs/123-example/spec.md",
            )
            self.assertEqual(0, passing.returncode, passing.stdout + passing.stderr)
            self.assertNotEqual(0, failing.returncode)
            self.assertIn("missing-required-key", failing.stdout)

    def test_report_order_is_deterministic_and_sorted_by_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            write_doc(root / "docs/03.specs/200-z/spec.md", {"status": "active"})
            write_doc(root / "docs/01.requirements/100-a.md", {"status": "active"})
            first = run_checker(root, "report")
            second = run_checker(root, "report")
            self.assertEqual(first.stdout, second.stdout)
            self.assertLess(
                first.stdout.index("docs/01.requirements/100-a.md"),
                first.stdout.index("docs/03.specs/200-z/spec.md"),
            )

    def test_report_output_check_detects_staleness(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            write_doc(root / "docs/03.specs/README.md", None)
            output = root / "inventory.md"
            generated = run_checker(root, "report", "--output", str(output))
            fresh = run_checker(root, "report", "--output", str(output), "--check")
            output.write_text("stale\n", encoding="utf-8")
            stale = run_checker(root, "report", "--output", str(output), "--check")
            self.assertEqual(0, generated.returncode, generated.stderr)
            self.assertEqual(0, fresh.returncode, fresh.stderr)
            self.assertNotEqual(0, stale.returncode)
            self.assertIn("metadata inventory is stale", stale.stderr)

    def test_active_mode_is_available_but_semantic_gate_is_not_auto_invoked(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            write_doc(root / "docs/03.specs/123-example/spec.md", {"status": "active"})
            result = run_checker(root, "check-active")
            self.assertNotEqual(0, result.returncode)
            self.assertIn("metadata check-active", result.stdout)


if __name__ == "__main__":
    unittest.main()
