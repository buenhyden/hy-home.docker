from __future__ import annotations

import importlib.util
import os
import pathlib
import shutil
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


def run_checker(
    root: pathlib.Path,
    mode: str = "report",
    *extra: str,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
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
        env={**os.environ, **(env or {})},
        capture_output=True,
        text=True,
        check=False,
    )


def git(root: pathlib.Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        text=True,
        check=False,
    )


def failing_git_probe_env(directory: pathlib.Path, probe_name: str) -> dict[str, str]:
    """Return an environment whose Git delegates except for one discovery probe."""

    real_git = shutil.which("git")
    if real_git is None:
        raise RuntimeError("Git is required for metadata fixtures")
    bin_dir = directory / "bin"
    bin_dir.mkdir()
    wrapper = bin_dir / "git"
    wrapper.write_text(
        f"""#!{sys.executable}
import subprocess
import sys

args = sys.argv[1:]
probe = args[2:] if len(args) >= 2 and args[0] == "-C" else args
probe_name = {probe_name!r}
should_fail = (
    probe_name == "tracked"
    and probe[:2] == ["ls-files", "-z"]
    and "--others" not in probe
) or (
    probe_name == "unstaged"
    and probe[:1] == ["diff"]
    and "--cached" not in probe
    and not any(item.endswith("...HEAD") for item in probe)
) or (
    probe_name == "staged"
    and probe[:1] == ["diff"]
    and "--cached" in probe
) or (
    probe_name == "untracked"
    and probe[:1] == ["ls-files"]
    and "--others" in probe
)
if should_fail:
    raise SystemExit(73)
raise SystemExit(subprocess.run([{real_git!r}, *args], check=False).returncode)
""",
        encoding="utf-8",
    )
    wrapper.chmod(0o755)
    return {"PATH": f"{bin_dir}{os.pathsep}{os.environ.get('PATH', '')}"}


def init_git(root: pathlib.Path) -> None:
    self_check = git(root, "init", "-q")
    if self_check.returncode != 0:
        raise RuntimeError(self_check.stderr)
    git(root, "config", "user.name", "Metadata Fixture")
    git(root, "config", "user.email", "metadata@example.invalid")


def commit_all(root: pathlib.Path, message: str = "fixture") -> None:
    staged = git(root, "add", ".")
    if staged.returncode != 0:
        raise RuntimeError(staged.stderr)
    committed = git(root, "commit", "-qm", message)
    if committed.returncode != 0:
        raise RuntimeError(committed.stderr)


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

    def test_unhashable_yaml_mapping_key_is_normalized(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "unhashable.md"
            path.write_text("---\n? [a, b]: c\n---\n", encoding="utf-8")
            with self.assertRaises(metadata.FrontmatterError) as context:
                metadata.parse_frontmatter(path)
            self.assertEqual("malformed-yaml", context.exception.code)


class ProfileSchemaTests(unittest.TestCase):
    def mutate_and_load(self, mutate) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = pathlib.Path(directory) / "profiles.yaml"
            values = yaml.safe_load(PROFILES.read_text(encoding="utf-8"))
            mutate(values)
            target.write_text(yaml.safe_dump(values, sort_keys=False), encoding="utf-8")
            with self.assertRaises(metadata.ProfileError):
                metadata.load_profiles(target)

    def test_schema_version_rejects_boolean(self) -> None:
        self.mutate_and_load(lambda values: values.__setitem__("schema_version", True))

    def test_profile_lists_reject_non_string_members(self) -> None:
        self.mutate_and_load(lambda values: values["profiles"]["spec"]["required"].append(7))

    def test_transitions_reject_unknown_statuses(self) -> None:
        self.mutate_and_load(lambda values: values["common"]["transitions"]["active"].append("retired"))


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

    def test_approved_crosscutting_spec_root_is_explicitly_permitted(self) -> None:
        record = self.record(
            "docs/03.specs/123-agentic-engineering-audit-remediation/spec.md",
            {
                "status": "active",
                "artifact_id": "spec:123-agentic-engineering-audit-remediation",
                "artifact_type": "spec",
                "parent_ids": [],
            },
            "spec",
        )
        self.assertNotIn("missing-parent", self.codes(record))

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

    def test_freshness_requires_strict_iso_date_or_datetime(self) -> None:
        record = self.record(
            "docs/05.operations/policies/00-workspace/example.md",
            {
                "status": "active",
                "artifact_id": "POLICY-EXAMPLE",
                "artifact_type": "policy",
                "parent_ids": [],
                "reviewed_at": "yesterday",
                "review_cycle": "annual",
            },
            "policy",
        )
        self.assertIn("invalid-reviewed-at", self.codes(record))

    def test_generator_owner_rejects_absolute_and_traversal_paths(self) -> None:
        for generated_by in ("/tmp/generator.py", "scripts/../generator.py", "scripts\\generator.py"):
            with self.subTest(generated_by=generated_by):
                record = self.record(
                    "docs/90.references/data/example.md",
                    {"status": "active", "generated_by": generated_by},
                    "generated",
                )
                self.assertIn("invalid-generator", self.codes(record))

    def test_archive_provenance_types_are_validated(self) -> None:
        record = self.record(
            "docs/98.archive/04.execution/example.md",
            {
                "status": "archived",
                "archived_from": ["docs/04.execution/example.md"],
                "archived_on": "not-a-date",
                "archive_reason": 7,
                "current_replacement": "/absolute.md",
            },
            "archive",
        )
        codes = self.codes(record)
        self.assertIn("invalid-archived-from", codes)
        self.assertIn("invalid-archived-on", codes)
        self.assertIn("invalid-archive-reason", codes)
        self.assertIn("invalid-current-replacement", codes)

    def test_instantiated_document_rejects_template_placeholders(self) -> None:
        record = self.record(
            "docs/03.specs/124-example/spec.md",
            {
                "status": "draft",
                "artifact_id": "<artifact-id>",
                "artifact_type": "spec",
                "parent_ids": ["<parent-artifact-id>"],
            },
            "spec",
        )
        self.assertIn("template-placeholder-in-target", self.codes(record))

    def test_instantiated_document_rejects_composed_angle_bracket_placeholders(self) -> None:
        cases = (
            {
                "status": "draft",
                "artifact_id": "spec:<artifact-id>",
                "artifact_type": "spec",
                "parent_ids": ["prd:real-parent"],
            },
            {
                "status": "draft",
                "artifact_id": "spec:real-child",
                "artifact_type": "spec",
                "parent_ids": ["prefix:<parent-artifact-id>"],
            },
            {
                "status": "active",
                "artifact_id": "policy:real",
                "artifact_type": "policy",
                "parent_ids": ["spec:real-parent"],
                "reviewed_at": "reviewed-<reviewed-at>",
                "review_cycle": "annual",
            },
        )
        paths = (
            "docs/03.specs/124-example/spec.md",
            "docs/03.specs/124-example/spec.md",
            "docs/05.operations/policies/00-workspace/example.md",
        )
        types = ("spec", "spec", "policy")
        for values, path, artifact_type in zip(cases, paths, types, strict=True):
            with self.subTest(values=values):
                record = self.record(path, values, artifact_type)
                self.assertIn("template-placeholder-in-target", self.codes(record))

    def test_non_angle_date_marker_is_not_a_global_placeholder_token(self) -> None:
        record = self.record(
            "docs/01.requirements/124-example.md",
            {
                "status": "active",
                "artifact_id": "prd:release-YYYY-MM-DD",
                "artifact_type": "prd",
                "parent_ids": [],
            },
            "prd",
        )
        self.assertNotIn("template-placeholder-in-target", self.codes(record))


class TemplateMetadataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profiles = metadata.load_profiles(PROFILES)

    def test_leaf_templates_declare_valid_target_profiles_with_safe_placeholders(self) -> None:
        expected = {
            "docs/99.templates/templates/sdlc/prd.template.md": "prd",
            "docs/99.templates/templates/sdlc/ard.template.md": "ard",
            "docs/99.templates/templates/sdlc/adr.template.md": "adr",
            "docs/99.templates/templates/sdlc/spec.template.md": "spec",
            "docs/99.templates/templates/sdlc/plan.template.md": "plan",
            "docs/99.templates/templates/sdlc/task.template.md": "task",
            "docs/99.templates/templates/operations/guide.template.md": "guide",
            "docs/99.templates/templates/operations/policy.template.md": "policy",
            "docs/99.templates/templates/operations/runbook.template.md": "runbook",
            "docs/99.templates/templates/operations/incident.template.md": "incident",
            "docs/99.templates/templates/operations/postmortem.template.md": "postmortem",
            "docs/99.templates/templates/common/reference.template.md": "reference",
            "docs/99.templates/templates/common/archive.template.md": "archive",
        }
        for path_text, target_profile in expected.items():
            with self.subTest(path=path_text):
                values = metadata.parse_frontmatter(ROOT / path_text)
                self.assertEqual("draft", values.get("status"))
                self.assertEqual(target_profile, values.get("artifact_type"))
                self.assertEqual("<artifact-id>", values.get("artifact_id"))
                record = metadata.Record(
                    pathlib.Path(path_text),
                    values,
                    "template-source",
                    frontmatter_present=True,
                )
                self.assertEqual(
                    [],
                    metadata.validate_record(record, self.profiles, metadata.build_manifest([record])),
                )

    def test_readme_template_remains_a_readme_exception_source(self) -> None:
        path_text = "docs/99.templates/templates/common/readme.template.md"
        values = metadata.parse_frontmatter(ROOT / path_text)
        self.assertEqual({"status": "draft"}, values)

    def test_unmapped_template_source_rejects_typed_leaf_metadata(self) -> None:
        record = metadata.Record(
            pathlib.Path("docs/99.templates/templates/governance/memory.template.md"),
            {
                "status": "draft",
                "artifact_id": "template-source:invalid",
                "artifact_type": "template-source",
                "parent_ids": [],
            },
            "template-source",
            frontmatter_present=True,
        )
        codes = {
            finding.code
            for finding in metadata.validate_record(
                record,
                self.profiles,
                metadata.build_manifest([record]),
            )
        }
        self.assertIn("type-inappropriate-key", codes)


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
            self.assertIn("| duplicate |", result.stdout)

    def test_duplicate_yaml_key_has_distinct_inventory_state(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            path = root / "docs/03.specs/123-example/spec.md"
            path.parent.mkdir(parents=True)
            path.write_text("---\nstatus: active\nstatus: completed\n---\n", encoding="utf-8")
            result = run_checker(root, "report")
            self.assertEqual(2, result.returncode)
            self.assertIn("frontmatter-duplicate-key", result.stdout)
            self.assertIn("| duplicate-key |", result.stdout)

    def test_report_returns_nonzero_for_parser_failure_but_renders_inventory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            path = root / "docs/03.specs/123-example/spec.md"
            path.parent.mkdir(parents=True)
            path.write_text("---\nstatus: [active\n---\n", encoding="utf-8")
            result = run_checker(root, "report")
            self.assertNotEqual(0, result.returncode)
            self.assertIn("frontmatter-malformed-yaml", result.stdout)
            self.assertIn(path.relative_to(root).as_posix(), result.stdout)

    def test_unhashable_mapping_key_has_no_traceback_and_writes_inventory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            path = root / "docs/03.specs/123-example/spec.md"
            path.parent.mkdir(parents=True)
            path.write_text("---\n? [a, b]: c\n---\n", encoding="utf-8")
            output = root / "inventory.md"
            result = run_checker(root, "report", "--output", str(output))
            self.assertEqual(2, result.returncode)
            self.assertNotIn("Traceback", result.stderr)
            rendered = output.read_text(encoding="utf-8")
            self.assertIn("frontmatter-malformed-yaml", rendered)
            self.assertIn("malformed-yaml", rendered)

    def test_changed_mode_fails_only_selected_violations(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            init_git(root)
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

    def test_inventory_exposes_all_semantic_state_columns(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            write_doc(root / "docs/03.specs/README.md", None)
            write_doc(
                root / "docs/90.references/data/generated.md",
                {"status": "active", "generated_by": "scripts/example.py"},
            )
            result = run_checker(root, "report")
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn(
                "| Path | Profile | Frontmatter | Identity | Relations | Lifecycle | Transition Evidence | Freshness | Exception Context | Findings | Disposition |",
                result.stdout,
            )
            self.assertIn("missing-fence", result.stdout)
            self.assertIn("README profile; consumer=not-declared; role=folder-index", result.stdout)
            self.assertIn("generated profile; owner=scripts/example.py", result.stdout)
            self.assertIn("reviewed_at=forbidden:not-applicable", result.stdout)

    def test_inventory_records_identity_relations_and_transition_evidence(self) -> None:
        profiles = metadata.load_profiles(PROFILES)
        parent = metadata.Record(
            pathlib.Path("docs/01.requirements/123-parent.md"),
            {"status": "active", "artifact_id": "PRD-123", "artifact_type": "prd", "parent_ids": []},
            "prd",
            frontmatter_present=True,
        )
        child = metadata.Record(
            pathlib.Path("docs/03.specs/123-child/spec.md"),
            {
                "status": "completed",
                "artifact_id": "SPEC-123",
                "artifact_type": "spec",
                "parent_ids": ["PRD-123"],
            },
            "spec",
            previous_status="active",
            frontmatter_present=True,
        )
        records = [parent, child]
        manifest = metadata.build_manifest(records)
        findings = {
            record.path.as_posix(): metadata.validate_record(record, profiles, manifest) for record in records
        }
        report = metadata.render_report(records, profiles, findings)
        child_row = next(line for line in report.splitlines() if "docs/03.specs/123-child/spec.md" in line)
        self.assertIn("| valid | parents=resolved:1; order=declared-list; supersedes=not-provided |", child_row)
        self.assertIn("available:active->completed; valid", child_row)


class ChangedPathGitTests(unittest.TestCase):
    def new_repo(self) -> tuple[tempfile.TemporaryDirectory[str], pathlib.Path]:
        directory = tempfile.TemporaryDirectory()
        root = pathlib.Path(directory.name)
        init_git(root)
        write_doc(root / "docs/03.specs/README.md", None)
        commit_all(root)
        return directory, root

    def assert_changed_failure(self, root: pathlib.Path, *extra: str) -> None:
        result = run_checker(root, "check-changed", *extra)
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("missing-required-key", result.stdout)

    def assert_git_probe_failure(self, probe_name: str, expected_label: str) -> None:
        directory, root = self.new_repo()
        with directory:
            result = run_checker(
                root,
                "check-changed",
                env=failing_git_probe_env(root, probe_name),
            )
            combined = result.stdout + result.stderr
            self.assertEqual(2, result.returncode, combined)
            self.assertIn("configuration-error:", result.stderr)
            self.assertIn(expected_label, result.stderr)
            self.assertNotIn("metadata check-changed:", result.stdout)
            self.assertNotIn("Traceback", combined)

    def write_parent_relation_fixture(self, root: pathlib.Path) -> pathlib.Path:
        parent = root / "docs/01.requirements/123-parent.md"
        write_doc(
            parent,
            {
                "status": "active",
                "artifact_id": "prd:123-parent",
                "artifact_type": "prd",
                "parent_ids": [],
            },
        )
        write_doc(
            root / "docs/03.specs/123-child/spec.md",
            {
                "status": "active",
                "artifact_id": "spec:123-child",
                "artifact_type": "spec",
                "parent_ids": ["prd:123-parent"],
                "reviewed_at": "preexisting-invalid-date",
            },
        )
        commit_all(root, "typed parent relation")
        return parent

    def write_supersedes_relation_fixture(self, root: pathlib.Path) -> pathlib.Path:
        write_doc(
            root / "docs/01.requirements/123-root.md",
            {
                "status": "active",
                "artifact_id": "prd:123-root",
                "artifact_type": "prd",
                "parent_ids": [],
            },
        )
        replaced = root / "docs/03.specs/123-replaced/spec.md"
        write_doc(
            replaced,
            {
                "status": "superseded",
                "artifact_id": "spec:123-replaced",
                "artifact_type": "spec",
                "parent_ids": ["prd:123-root"],
            },
        )
        write_doc(
            root / "docs/03.specs/123-replacement/spec.md",
            {
                "status": "active",
                "artifact_id": "spec:123-replacement",
                "artifact_type": "spec",
                "parent_ids": ["prd:123-root"],
                "supersedes": ["spec:123-replaced"],
                "reviewed_at": "preexisting-invalid-date",
            },
        )
        commit_all(root, "typed supersedes relation")
        return replaced

    def write_identity_change_supersedes_fixture(self, root: pathlib.Path) -> pathlib.Path:
        write_doc(
            root / "docs/01.requirements/123-identity-root.md",
            {
                "status": "active",
                "artifact_id": "prd:123-identity-root",
                "artifact_type": "prd",
                "parent_ids": [],
            },
        )
        target = root / "docs/03.specs/123-identity-target/spec.md"
        write_doc(
            target,
            {
                "status": "superseded",
                "artifact_id": "spec:123-identity-old",
                "artifact_type": "spec",
                "parent_ids": ["prd:123-identity-root"],
            },
        )
        write_doc(
            root / "docs/03.specs/123-old-id-dependent/spec.md",
            {
                "status": "active",
                "artifact_id": "spec:123-old-id-dependent",
                "artifact_type": "spec",
                "parent_ids": ["prd:123-identity-root"],
                "supersedes": ["spec:123-identity-old"],
                "reviewed_at": "preexisting-invalid-date",
            },
        )
        write_doc(
            root / "docs/03.specs/123-new-id-replacement/spec.md",
            {
                "status": "active",
                "artifact_id": "spec:123-new-id-replacement",
                "artifact_type": "spec",
                "parent_ids": ["prd:123-identity-root"],
                "supersedes": ["spec:123-identity-new"],
            },
        )
        commit_all(root, "typed identity-change supersedes relation")
        return target

    def rewrite_artifact_identity(
        self,
        root: pathlib.Path,
        target: pathlib.Path,
        *,
        staged: bool,
    ) -> None:
        if target.as_posix().endswith("docs/01.requirements/123-parent.md"):
            values = {
                "status": "active",
                "artifact_id": "prd:123-parent-new",
                "artifact_type": "prd",
                "parent_ids": [],
            }
        else:
            values = {
                "status": "superseded",
                "artifact_id": "spec:123-identity-new",
                "artifact_type": "spec",
                "parent_ids": ["prd:123-identity-root"],
            }
        write_doc(target, values)
        if staged:
            self.assertEqual(0, git(root, "add", target.relative_to(root).as_posix()).returncode)

    def assert_identity_change_failure(
        self,
        root: pathlib.Path,
        target: pathlib.Path,
        dependent: str,
        finding_code: str,
        *,
        staged: bool,
    ) -> None:
        self.rewrite_artifact_identity(root, target, staged=staged)
        result = run_checker(root, "check-changed")
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn(f"{dependent}: {finding_code}", result.stdout)
        self.assertNotIn("invalid-reviewed-at", result.stdout)
        self.assertIn("selected=2 violations=1", result.stdout)

    def assert_relation_deletion_failure(
        self,
        root: pathlib.Path,
        deleted: pathlib.Path,
        dependent: str,
        finding_code: str,
        *,
        staged: bool,
    ) -> None:
        relative = deleted.relative_to(root).as_posix()
        if staged:
            self.assertEqual(0, git(root, "rm", relative).returncode)
        else:
            deleted.unlink()
        result = run_checker(root, "check-changed")
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn(f"{dependent}: {finding_code}", result.stdout)
        self.assertNotIn("invalid-reviewed-at", result.stdout)
        self.assertIn("selected=2 violations=1", result.stdout)

    def test_untracked_invalid_document_fails(self) -> None:
        directory, root = self.new_repo()
        with directory:
            write_doc(root / "docs/03.specs/123-new/spec.md", {"status": "active"})
            self.assert_changed_failure(root)

    def test_failed_tracked_file_discovery_fails_closed(self) -> None:
        self.assert_git_probe_failure("tracked", "tracked Markdown")

    def test_failed_unstaged_diff_discovery_fails_closed(self) -> None:
        self.assert_git_probe_failure("unstaged", "unstaged Markdown")

    def test_failed_staged_diff_discovery_fails_closed(self) -> None:
        self.assert_git_probe_failure("staged", "staged Markdown")

    def test_failed_untracked_file_discovery_fails_closed(self) -> None:
        self.assert_git_probe_failure("untracked", "untracked Markdown")

    def test_non_git_root_fails_closed_without_success_summary(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            write_doc(root / "docs/03.specs/123-new/spec.md", {"status": "active"})
            result = run_checker(root, "check-changed")
            combined = result.stdout + result.stderr
            self.assertEqual(2, result.returncode, combined)
            self.assertIn("configuration-error:", result.stderr)
            self.assertIn("Git worktree", result.stderr)
            self.assertNotIn("metadata check-changed:", result.stdout)
            self.assertNotIn("Traceback", combined)

    def test_missing_git_executable_fails_closed_without_traceback(self) -> None:
        directory, root = self.new_repo()
        with directory:
            result = run_checker(root, "check-changed", env={"PATH": ""})
            combined = result.stdout + result.stderr
            self.assertEqual(2, result.returncode, combined)
            self.assertIn("configuration-error:", result.stderr)
            self.assertIn("Git executable", result.stderr)
            self.assertNotIn("metadata check-changed:", result.stdout)
            self.assertNotIn("Traceback", combined)

    def test_non_utf8_markdown_path_in_explicit_base_is_sanitized(self) -> None:
        directory, root = self.new_repo()
        with directory:
            raw_directory = os.fsencode(root / "docs/03.specs")
            raw_path = raw_directory + b"/private-base-path-\xff.md"
            descriptor = os.open(raw_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(b"private-base-body\n")
            commit_all(root, "non-UTF-8 base path")
            base = git(root, "rev-parse", "HEAD").stdout.strip()

            readme = root / "docs/03.specs/README.md"
            readme.write_text("# Specifications\n\nOrdinary current change.\n", encoding="utf-8")
            commit_all(root, "ordinary current change")

            result = run_checker(root, "check-changed", "--base-ref", base)
            combined = result.stdout + result.stderr
            self.assertEqual(2, result.returncode, combined)
            self.assertIn("configuration-error:", result.stderr)
            self.assertIn("base Markdown discovery returned a non-UTF-8 path", result.stderr)
            self.assertNotIn("metadata check-changed:", result.stdout)
            self.assertNotIn("Traceback", combined)
            self.assertNotIn("private-base-path", combined)
            self.assertNotIn("private-base-body", combined)
            self.assertNotIn("fatal:", combined)

    def test_staged_invalid_document_fails(self) -> None:
        directory, root = self.new_repo()
        with directory:
            path = root / "docs/03.specs/123-new/spec.md"
            write_doc(path, {"status": "active"})
            self.assertEqual(0, git(root, "add", path.relative_to(root).as_posix()).returncode)
            self.assert_changed_failure(root)

    def test_modified_invalid_document_fails(self) -> None:
        directory, root = self.new_repo()
        with directory:
            path = root / "docs/03.specs/123-existing/spec.md"
            write_doc(
                path,
                {"status": "active", "artifact_id": "SPEC-123", "artifact_type": "spec", "parent_ids": []},
            )
            commit_all(root)
            write_doc(path, {"status": "active"})
            self.assert_changed_failure(root)

    def test_renamed_invalid_document_fails_at_new_path(self) -> None:
        directory, root = self.new_repo()
        with directory:
            source = root / "docs/03.specs/README.md"
            target = root / "docs/03.specs/123-renamed/spec.md"
            target.parent.mkdir(parents=True)
            self.assertEqual(0, git(root, "mv", source.relative_to(root).as_posix(), target.relative_to(root).as_posix()).returncode)
            self.assert_changed_failure(root)

    def test_deleted_document_is_not_parsed_as_violation(self) -> None:
        directory, root = self.new_repo()
        with directory:
            path = root / "docs/01.requirements/123-deleted.md"
            write_doc(
                path,
                {
                    "status": "active",
                    "artifact_id": "prd:123-deleted",
                    "artifact_type": "prd",
                    "parent_ids": [],
                },
            )
            commit_all(root)
            path.unlink()
            result = run_checker(root, "check-changed")
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn("selected=1 violations=0", result.stdout)

    def test_staged_deleted_document_is_retained_as_nonviolating_evidence(self) -> None:
        directory, root = self.new_repo()
        with directory:
            path = root / "docs/01.requirements/123-staged-deleted.md"
            write_doc(
                path,
                {
                    "status": "active",
                    "artifact_id": "prd:123-staged-deleted",
                    "artifact_type": "prd",
                    "parent_ids": [],
                },
            )
            commit_all(root)
            self.assertEqual(0, git(root, "rm", path.relative_to(root).as_posix()).returncode)
            result = run_checker(root, "check-changed")
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn("selected=1 violations=0", result.stdout)

    def test_unstaged_parent_deletion_blocks_unchanged_dependent(self) -> None:
        directory, root = self.new_repo()
        with directory:
            deleted = self.write_parent_relation_fixture(root)
            self.assert_relation_deletion_failure(
                root,
                deleted,
                "docs/03.specs/123-child/spec.md",
                "unresolved-parent",
                staged=False,
            )

    def test_staged_parent_deletion_blocks_unchanged_dependent(self) -> None:
        directory, root = self.new_repo()
        with directory:
            deleted = self.write_parent_relation_fixture(root)
            self.assert_relation_deletion_failure(
                root,
                deleted,
                "docs/03.specs/123-child/spec.md",
                "unresolved-parent",
                staged=True,
            )

    def test_unstaged_supersedes_deletion_blocks_unchanged_dependent(self) -> None:
        directory, root = self.new_repo()
        with directory:
            deleted = self.write_supersedes_relation_fixture(root)
            self.assert_relation_deletion_failure(
                root,
                deleted,
                "docs/03.specs/123-replacement/spec.md",
                "unresolved-supersedes",
                staged=False,
            )

    def test_staged_supersedes_deletion_blocks_unchanged_dependent(self) -> None:
        directory, root = self.new_repo()
        with directory:
            deleted = self.write_supersedes_relation_fixture(root)
            self.assert_relation_deletion_failure(
                root,
                deleted,
                "docs/03.specs/123-replacement/spec.md",
                "unresolved-supersedes",
                staged=True,
            )

    def test_staged_typed_parent_rename_keeps_relation_resolved(self) -> None:
        directory, root = self.new_repo()
        with directory:
            source = self.write_parent_relation_fixture(root)
            target = root / "docs/01.requirements/123-parent-renamed.md"
            self.assertEqual(
                0,
                git(root, "mv", source.relative_to(root).as_posix(), target.relative_to(root).as_posix()).returncode,
            )
            result = run_checker(root, "check-changed")
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn("violations=0", result.stdout)

    def test_unstaged_parent_id_change_blocks_unchanged_dependent(self) -> None:
        directory, root = self.new_repo()
        with directory:
            target = self.write_parent_relation_fixture(root)
            self.assert_identity_change_failure(
                root,
                target,
                "docs/03.specs/123-child/spec.md",
                "unresolved-parent",
                staged=False,
            )

    def test_staged_parent_id_change_blocks_unchanged_dependent(self) -> None:
        directory, root = self.new_repo()
        with directory:
            target = self.write_parent_relation_fixture(root)
            self.assert_identity_change_failure(
                root,
                target,
                "docs/03.specs/123-child/spec.md",
                "unresolved-parent",
                staged=True,
            )

    def test_unstaged_supersedes_target_id_change_blocks_unchanged_dependent(self) -> None:
        directory, root = self.new_repo()
        with directory:
            target = self.write_identity_change_supersedes_fixture(root)
            self.assert_identity_change_failure(
                root,
                target,
                "docs/03.specs/123-old-id-dependent/spec.md",
                "unresolved-supersedes",
                staged=False,
            )

    def test_staged_supersedes_target_id_change_blocks_unchanged_dependent(self) -> None:
        directory, root = self.new_repo()
        with directory:
            target = self.write_identity_change_supersedes_fixture(root)
            self.assert_identity_change_failure(
                root,
                target,
                "docs/03.specs/123-old-id-dependent/spec.md",
                "unresolved-supersedes",
                staged=True,
            )

    def test_coherent_parent_id_change_updates_dependent_relation(self) -> None:
        directory, root = self.new_repo()
        with directory:
            target = self.write_parent_relation_fixture(root)
            self.rewrite_artifact_identity(root, target, staged=False)
            write_doc(
                root / "docs/03.specs/123-child/spec.md",
                {
                    "status": "active",
                    "artifact_id": "spec:123-child",
                    "artifact_type": "spec",
                    "parent_ids": ["prd:123-parent-new"],
                },
            )
            result = run_checker(root, "check-changed")
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn("selected=2 violations=0", result.stdout)

    def test_explicit_untracked_path_is_parsed(self) -> None:
        directory, root = self.new_repo()
        with directory:
            relative = "docs/03.specs/123-explicit/spec.md"
            write_doc(root / relative, {"status": "active"})
            self.assert_changed_failure(root, "--changed-path", relative)


class ChangedModeRolloutTests(unittest.TestCase):
    def new_repo(self) -> tuple[tempfile.TemporaryDirectory[str], pathlib.Path]:
        directory = tempfile.TemporaryDirectory()
        root = pathlib.Path(directory.name)
        init_git(root)
        self.assertEqual(0, git(root, "branch", "-M", "main").returncode)
        write_doc(root / "docs/03.specs/README.md", None)
        commit_all(root, "base")
        return directory, root

    def test_committed_new_invalid_document_is_blocked_from_explicit_base(self) -> None:
        directory, root = self.new_repo()
        with directory:
            base = git(root, "rev-parse", "HEAD").stdout.strip()
            write_doc(root / "docs/03.specs/124-new/spec.md", {"status": "active"})
            commit_all(root, "invalid new doc")
            result = run_checker(root, "check-changed", "--base-ref", base)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn("missing-required-key", result.stdout)
            self.assertIn(f"metadata base: source=explicit ref={base}", result.stderr)

    def test_changed_legacy_document_outside_migration_scope_is_explicitly_excepted(self) -> None:
        directory, root = self.new_repo()
        with directory:
            path = root / "docs/03.specs/122-legacy/spec.md"
            write_doc(path, {"status": "active"}, "# Legacy\n")
            commit_all(root, "legacy baseline")
            base = git(root, "rev-parse", "HEAD").stdout.strip()
            write_doc(path, {"status": "active"}, "# Legacy\n\nEditorial correction.\n")
            commit_all(root, "edit legacy doc")
            result = run_checker(root, "check-changed", "--base-ref", base)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn("legacy_exceptions=1", result.stdout)
            self.assertIn("legacy metadata exception", result.stderr)

    def test_partial_typed_migration_cannot_use_legacy_exception(self) -> None:
        directory, root = self.new_repo()
        with directory:
            path = root / "docs/03.specs/122-legacy/spec.md"
            write_doc(path, {"status": "active"})
            commit_all(root, "legacy baseline")
            base = git(root, "rev-parse", "HEAD").stdout.strip()
            write_doc(path, {"status": "active", "artifact_id": "spec:partial"})
            commit_all(root, "partial migration")
            result = run_checker(root, "check-changed", "--base-ref", base)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn("legacy_exceptions=0", result.stdout)
            self.assertIn("missing-required-key", result.stdout)

    def test_new_stale_active_deficit_cannot_use_legacy_exception(self) -> None:
        directory, root = self.new_repo()
        with directory:
            path = root / "docs/05.operations/policies/00-workspace/legacy.md"
            write_doc(path, {"status": "draft"})
            commit_all(root, "legacy draft policy")
            base = git(root, "rev-parse", "HEAD").stdout.strip()
            write_doc(path, {"status": "active"})
            commit_all(root, "activate legacy policy")
            result = run_checker(root, "check-changed", "--base-ref", base)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn("legacy_exceptions=0", result.stdout)
            self.assertIn("stale-active", result.stdout)

    def test_new_replacement_free_deficit_cannot_use_legacy_exception(self) -> None:
        directory, root = self.new_repo()
        with directory:
            path = root / "docs/03.specs/122-legacy/spec.md"
            write_doc(path, {"status": "active"})
            commit_all(root, "legacy active spec")
            base = git(root, "rev-parse", "HEAD").stdout.strip()
            write_doc(path, {"status": "superseded"})
            commit_all(root, "supersede without replacement")
            result = run_checker(root, "check-changed", "--base-ref", base)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn("legacy_exceptions=0", result.stdout)
            self.assertIn("replacement-free-supersession", result.stdout)

    def test_disappearing_legacy_deficit_remains_eligible(self) -> None:
        directory, root = self.new_repo()
        with directory:
            path = root / "docs/05.operations/policies/00-workspace/legacy.md"
            write_doc(path, {"status": "active"})
            commit_all(root, "legacy active policy")
            base = git(root, "rev-parse", "HEAD").stdout.strip()
            write_doc(path, {"status": "completed"})
            commit_all(root, "complete legacy policy")
            result = run_checker(root, "check-changed", "--base-ref", base)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn("legacy_exceptions=1", result.stdout)

    def test_committed_valid_parent_chain_passes_and_is_selected(self) -> None:
        directory, root = self.new_repo()
        with directory:
            base = git(root, "rev-parse", "HEAD").stdout.strip()
            write_doc(
                root / "docs/01.requirements/124-parent.md",
                {
                    "status": "active",
                    "artifact_id": "prd:124-parent",
                    "artifact_type": "prd",
                    "parent_ids": [],
                },
            )
            write_doc(
                root / "docs/03.specs/124-child/spec.md",
                {
                    "status": "active",
                    "artifact_id": "spec:124-child",
                    "artifact_type": "spec",
                    "parent_ids": ["prd:124-parent"],
                },
            )
            commit_all(root, "valid typed chain")
            result = run_checker(root, "check-changed", "--base-ref", base)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn("selected=2", result.stdout)
            self.assertIn("violations=0", result.stdout)

    def test_committed_parent_deletion_blocks_dependent_from_explicit_base(self) -> None:
        directory, root = self.new_repo()
        with directory:
            parent = root / "docs/01.requirements/124-parent.md"
            write_doc(
                parent,
                {
                    "status": "active",
                    "artifact_id": "prd:124-parent",
                    "artifact_type": "prd",
                    "parent_ids": [],
                },
            )
            write_doc(
                root / "docs/03.specs/124-child/spec.md",
                {
                    "status": "active",
                    "artifact_id": "spec:124-child",
                    "artifact_type": "spec",
                    "parent_ids": ["prd:124-parent"],
                    "reviewed_at": "preexisting-invalid-date",
                },
            )
            commit_all(root, "typed parent chain")
            base = git(root, "rev-parse", "HEAD").stdout.strip()
            self.assertEqual(0, git(root, "rm", parent.relative_to(root).as_posix()).returncode)
            commit_all(root, "delete typed parent")
            result = run_checker(root, "check-changed", "--base-ref", base)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn(
                "docs/03.specs/124-child/spec.md: unresolved-parent",
                result.stdout,
            )
            self.assertNotIn("invalid-reviewed-at", result.stdout)
            self.assertIn("selected=2 violations=1", result.stdout)

    def test_committed_parent_id_change_blocks_dependent_from_explicit_base(self) -> None:
        directory, root = self.new_repo()
        with directory:
            parent = root / "docs/01.requirements/124-identity-parent.md"
            write_doc(
                parent,
                {
                    "status": "active",
                    "artifact_id": "prd:124-identity-old",
                    "artifact_type": "prd",
                    "parent_ids": [],
                },
            )
            write_doc(
                root / "docs/03.specs/124-identity-child/spec.md",
                {
                    "status": "active",
                    "artifact_id": "spec:124-identity-child",
                    "artifact_type": "spec",
                    "parent_ids": ["prd:124-identity-old"],
                    "reviewed_at": "preexisting-invalid-date",
                },
            )
            commit_all(root, "typed parent identity baseline")
            base = git(root, "rev-parse", "HEAD").stdout.strip()
            write_doc(
                parent,
                {
                    "status": "active",
                    "artifact_id": "prd:124-identity-new",
                    "artifact_type": "prd",
                    "parent_ids": [],
                },
            )
            commit_all(root, "change typed parent identity")
            result = run_checker(root, "check-changed", "--base-ref", base)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn(
                "docs/03.specs/124-identity-child/spec.md: unresolved-parent",
                result.stdout,
            )
            self.assertNotIn("invalid-reviewed-at", result.stdout)
            self.assertIn("selected=2 violations=1", result.stdout)

    def test_committed_supersedes_target_id_change_blocks_dependent_from_explicit_base(self) -> None:
        directory, root = self.new_repo()
        with directory:
            write_doc(
                root / "docs/01.requirements/124-identity-root.md",
                {
                    "status": "active",
                    "artifact_id": "prd:124-identity-root",
                    "artifact_type": "prd",
                    "parent_ids": [],
                },
            )
            target = root / "docs/03.specs/124-identity-target/spec.md"
            write_doc(
                target,
                {
                    "status": "superseded",
                    "artifact_id": "spec:124-identity-old",
                    "artifact_type": "spec",
                    "parent_ids": ["prd:124-identity-root"],
                },
            )
            write_doc(
                root / "docs/03.specs/124-old-id-dependent/spec.md",
                {
                    "status": "active",
                    "artifact_id": "spec:124-old-id-dependent",
                    "artifact_type": "spec",
                    "parent_ids": ["prd:124-identity-root"],
                    "supersedes": ["spec:124-identity-old"],
                    "reviewed_at": "preexisting-invalid-date",
                },
            )
            write_doc(
                root / "docs/03.specs/124-new-id-replacement/spec.md",
                {
                    "status": "active",
                    "artifact_id": "spec:124-new-id-replacement",
                    "artifact_type": "spec",
                    "parent_ids": ["prd:124-identity-root"],
                    "supersedes": ["spec:124-identity-new"],
                },
            )
            commit_all(root, "typed supersedes identity baseline")
            base = git(root, "rev-parse", "HEAD").stdout.strip()
            write_doc(
                target,
                {
                    "status": "superseded",
                    "artifact_id": "spec:124-identity-new",
                    "artifact_type": "spec",
                    "parent_ids": ["prd:124-identity-root"],
                },
            )
            commit_all(root, "change typed supersedes target identity")
            result = run_checker(root, "check-changed", "--base-ref", base)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn(
                "docs/03.specs/124-old-id-dependent/spec.md: unresolved-supersedes",
                result.stdout,
            )
            self.assertNotIn("invalid-reviewed-at", result.stdout)
            self.assertIn("selected=2 violations=1", result.stdout)

    def test_committed_replacement_free_superseded_document_is_blocked(self) -> None:
        directory, root = self.new_repo()
        with directory:
            base = git(root, "rev-parse", "HEAD").stdout.strip()
            write_doc(
                root / "docs/01.requirements/124-parent.md",
                {
                    "status": "active",
                    "artifact_id": "prd:124-parent",
                    "artifact_type": "prd",
                    "parent_ids": [],
                },
            )
            write_doc(
                root / "docs/03.specs/124-old/spec.md",
                {
                    "status": "superseded",
                    "artifact_id": "spec:124-old",
                    "artifact_type": "spec",
                    "parent_ids": ["prd:124-parent"],
                },
            )
            commit_all(root, "replacement-free supersession")
            result = run_checker(root, "check-changed", "--base-ref", base)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn("replacement-free-supersession", result.stdout)

    def test_reverse_transition_without_override_is_blocked(self) -> None:
        directory, root = self.new_repo()
        with directory:
            write_doc(
                root / "docs/03.specs/124-parent/spec.md",
                {
                    "status": "active",
                    "artifact_id": "spec:124-parent",
                    "artifact_type": "spec",
                    "parent_ids": ["spec:124-parent-root"],
                },
            )
            write_doc(
                root / "docs/03.specs/124-parent-root/spec.md",
                {
                    "status": "active",
                    "artifact_id": "spec:124-parent-root",
                    "artifact_type": "spec",
                    "parent_ids": ["spec:124-parent-root"],
                },
            )
            task = root / "docs/04.execution/tasks/2026-07-11-transition.md"
            write_doc(
                task,
                {
                    "status": "completed",
                    "artifact_id": "task:transition",
                    "artifact_type": "task",
                    "parent_ids": ["spec:124-parent"],
                },
            )
            commit_all(root, "completed task")
            base = git(root, "rev-parse", "HEAD").stdout.strip()
            write_doc(
                task,
                {
                    "status": "active",
                    "artifact_id": "task:transition",
                    "artifact_type": "task",
                    "parent_ids": ["spec:124-parent"],
                },
            )
            commit_all(root, "reverse task transition")
            result = run_checker(root, "check-changed", "--base-ref", base)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn("invalid-transition", result.stdout)

    def test_scoped_transition_override_requires_complete_stage04_evidence(self) -> None:
        directory, root = self.new_repo()
        with directory:
            parent = root / "docs/03.specs/124-parent/spec.md"
            write_doc(
                parent,
                {
                    "status": "active",
                    "artifact_id": "spec:124-parent",
                    "artifact_type": "spec",
                    "parent_ids": ["spec:124-parent"],
                },
            )
            task = root / "docs/04.execution/tasks/2026-07-11-transition.md"
            values = {
                "status": "completed",
                "artifact_id": "task:transition",
                "artifact_type": "task",
                "parent_ids": ["spec:124-parent"],
            }
            write_doc(task, values)
            evidence = root / "docs/04.execution/tasks/2026-07-11-transition-approval.md"
            write_doc(evidence, {"status": "active"}, "# Task: Transition Approval\n")
            commit_all(root, "completed task and evidence")
            base = git(root, "rev-parse", "HEAD").stdout.strip()
            write_doc(task, {**values, "status": "active"})
            commit_all(root, "approved reverse transition")
            override = root / "override.yaml"
            override.write_text(
                yaml.safe_dump(
                    {
                        "transition_overrides": [
                            {
                                "path": task.relative_to(root).as_posix(),
                                "previous_status": "completed",
                                "new_status": "active",
                                "evidence_task": evidence.relative_to(root).as_posix(),
                                "approval": "Spec 123 Task 8 fixture approval",
                                "reason": "Reopened to correct incomplete evidence",
                            }
                        ]
                    },
                    sort_keys=False,
                ),
                encoding="utf-8",
            )
            result = run_checker(
                root,
                "check-changed",
                "--base-ref",
                base,
                "--transition-override-file",
                str(override),
            )
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn("transition_overrides=1", result.stdout)

    def test_environment_base_is_used_before_local_candidates(self) -> None:
        directory, root = self.new_repo()
        with directory:
            base = git(root, "rev-parse", "HEAD").stdout.strip()
            write_doc(root / "docs/03.specs/124-new/spec.md", {"status": "active"})
            commit_all(root, "invalid branch doc")
            result = run_checker(
                root,
                "check-changed",
                env={"TEMPLATE_GATE_BASE": base, "GITHUB_BASE_REF": "does-not-exist"},
            )
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn("source=env:TEMPLATE_GATE_BASE", result.stderr)

    def test_invalid_explicit_base_is_a_configuration_error_without_fallback(self) -> None:
        directory, root = self.new_repo()
        with directory:
            write_doc(root / "docs/03.specs/124-new/spec.md", {"status": "active"})
            result = run_checker(root, "check-changed", "--base-ref", "missing-ref")
            self.assertEqual(2, result.returncode, result.stdout + result.stderr)
            self.assertIn("explicit --base-ref is not a commit", result.stderr)
            self.assertNotIn("fallback=working-tree-only", result.stderr)

    def test_local_main_base_selects_committed_branch_delta(self) -> None:
        directory, root = self.new_repo()
        with directory:
            self.assertEqual(0, git(root, "switch", "-qc", "feature").returncode)
            write_doc(root / "docs/03.specs/124-new/spec.md", {"status": "active"})
            commit_all(root, "invalid branch doc")
            result = run_checker(
                root,
                "check-changed",
                env={"TEMPLATE_GATE_BASE": "", "GITHUB_BASE_REF": ""},
            )
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn("source=local:main", result.stderr)

    def test_missing_base_falls_back_to_local_delta_without_whole_repo_gate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            init_git(root)
            write_doc(root / "docs/03.specs/README.md", None)
            write_doc(root / "docs/03.specs/124-new/spec.md", {"status": "active"})
            result = run_checker(
                root,
                "check-changed",
                env={"TEMPLATE_GATE_BASE": "", "GITHUB_BASE_REF": ""},
            )
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn("metadata base: fallback=working-tree-only", result.stderr)
            self.assertIn("selected=2", result.stdout)


if __name__ == "__main__":
    unittest.main()
