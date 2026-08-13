from __future__ import annotations

import collections
import dataclasses
import hashlib
import pathlib
import re
import shutil
import subprocess
import tempfile
import unittest

from scripts.lib.document_governance.operations_catalog import (
    ManifestError,
    OperationFileRecord,
    OperationSubjectRecord,
    find_operations_merge_candidates,
    load_operations_catalog_manifest,
    validate_operations_catalog_manifest,
    validate_subject_disposition,
)


ROOT = pathlib.Path(__file__).resolve().parents[2]
MANIFEST = (
    ROOT
    / "docs/98.archive/migrations/mig-0002-operations-catalog-convergence.md"
)
CLI = ROOT / "scripts/validation/check-operations-catalog.py"
BASELINE = "6f2703d8d245cf4e3576bece0bf247dd516b2bf3"
EXPECTED_DOMAINS = {
    "00-workspace",
    "01-gateway",
    "02-auth",
    "03-security",
    "04-data",
    "05-messaging",
    "06-observability",
    "07-workflow",
    "08-ai",
    "09-tooling",
    "10-communication",
    "11-laboratory",
    "12-infra-net",
}


def finding_codes(findings: object) -> set[str]:
    return {finding.code for finding in findings}


def remove_markdown_section(text: str, heading: str) -> str:
    pattern = re.compile(
        rf"(?ms)^## {re.escape(heading)}\s*$.*?(?=^## |\Z)"
    )
    mutated, count = pattern.subn("", text, count=1)
    if count != 1:
        raise AssertionError(f"missing section: {heading}")
    return mutated


def valid_subject_record(**overrides: object) -> OperationSubjectRecord:
    values: dict[str, object] = {
        "legacy_subject_path": pathlib.PurePosixPath(
            "docs/05.operations/00-workspace/ops-0001-common-optimizations-template-exceptions"
        ),
        "source_commit": BASELINE,
        "source_tree": "f" * 40,
        "current_ops_id": "ops-0001",
        "catalog_domain": "00-workspace",
        "catalog_path": pathlib.PurePosixPath(
            "docs/05.operations/catalog/00-workspace/ops-0001-common-optimizations-template-exceptions"
        ),
        "canonical_ops_id": "ops-0001",
        "canonical_slug": "common-optimizations-template-exceptions",
        "final_path": pathlib.PurePosixPath(
            "docs/05.operations/catalog/00-workspace/ops-0001-common-optimizations-template-exceptions"
        ),
        "semantic_action": "retain",
        "merge_into": None,
        "owner_match": False,
        "control_boundary_match": False,
        "trigger_and_recovery_match": False,
        "independent_evidence_boundary": True,
        "reason": "The policy owns an independent workspace-wide exception boundary.",
    }
    values.update(overrides)
    return OperationSubjectRecord(**values)  # type: ignore[arg-type]


class OperationsCatalogManifestTests(unittest.TestCase):
    def _approved_manifest(self):
        manifest = load_operations_catalog_manifest(MANIFEST)
        return dataclasses.replace(
            manifest,
            approval=dataclasses.replace(
                manifest.approval,
                status="approved",
                approved_at="2026-08-13",
                approved_by="user",
            ),
        )

    def _execution_tree(self, root: pathlib.Path, manifest, domain: str) -> None:
        for subject in manifest.subjects:
            if subject.catalog_domain == domain:
                (root / subject.final_path).mkdir(parents=True, exist_ok=True)
        for row in manifest.files:
            if row.legacy_path.parts[2] != domain or row.final_path is None:
                continue
            target = root / row.final_path
            target.parent.mkdir(parents=True, exist_ok=True)
            if not target.exists():
                shutil.copy2(ROOT / row.catalog_path, target)
        selected_rows = [
            row for row in manifest.files if row.legacy_path.parts[2] == domain
        ]
        for row in selected_rows:
            for source_path, final_path in zip(
                row.active_consumers, row.final_consumers, strict=True
            ):
                target = root / final_path
                if target.exists():
                    continue
                target.parent.mkdir(parents=True, exist_ok=True)
                source = ROOT / source_path
                if (
                    source_path.parts[:2] == ("docs", "05.operations")
                    and source_path.parts[2] in EXPECTED_DOMAINS
                ):
                    source = (
                        ROOT
                        / "docs/05.operations/catalog"
                        / pathlib.Path(*source_path.parts[2:])
                    )
                shutil.copy2(source, target)
        for row in selected_rows:
            if row.final_path is None:
                continue
            replacements = (
                (row.legacy_path.as_posix(), row.final_path.as_posix()),
                (row.legacy_path.parent.as_posix(), row.final_path.parent.as_posix()),
                (row.legacy_path.parent.name, row.final_path.parent.name),
            )
            for final_path in row.final_consumers:
                target = root / final_path
                text = target.read_text(encoding="utf-8")
                for old, new in replacements:
                    text = text.replace(old, new)
                target.write_text(text, encoding="utf-8")

    def _structure_tree(self, root: pathlib.Path, manifest) -> None:
        for subject in manifest.subjects:
            (root / subject.catalog_path).mkdir(parents=True, exist_ok=True)
        for row in manifest.files:
            target = root / row.catalog_path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / row.catalog_path, target)

    def _complete_tree(self, root: pathlib.Path, manifest) -> None:
        for domain in sorted({row.catalog_domain for row in manifest.subjects}):
            self._execution_tree(root, manifest, domain)
        operations_root = root / "docs/05.operations"
        (operations_root / "README.md").write_text(
            "# Operations\n\n"
            "- [Catalog](catalog/)\n"
            "- [Incidents](incidents/)\n"
            "- [Releases](releases/)\n",
            encoding="utf-8",
        )
        (operations_root / "catalog/README.md").write_text(
            "# Operations Catalog\n\n"
            + "".join(
                f"- [{domain}]({domain}/)\n"
                for domain in sorted(
                    {row.catalog_domain for row in manifest.subjects}
                )
            ),
            encoding="utf-8",
        )
        incident_packet = operations_root / "incidents/2026/inc-0001-control-plane-outage"
        incident_packet.mkdir(parents=True)
        (operations_root / "incidents/README.md").write_text(
            "# Incidents\n",
            encoding="utf-8",
        )
        (incident_packet / "incident.md").write_text(
            "# Incident: Control Plane Outage\n",
            encoding="utf-8",
        )
        (incident_packet / "postmortem.md").write_text(
            "# Postmortem: Control Plane Outage\n",
            encoding="utf-8",
        )
        release_packet = operations_root / "releases/rel-0001-initial-release"
        release_packet.mkdir(parents=True)
        (operations_root / "releases/README.md").write_text(
            "# Releases\n",
            encoding="utf-8",
        )
        (release_packet / "release.md").write_text(
            "# Release: Initial Release\n",
            encoding="utf-8",
        )

    def test_dataclass_interfaces_are_exact_and_frozen(self) -> None:
        self.assertEqual(
            (
                "legacy_subject_path",
                "source_commit",
                "source_tree",
                "current_ops_id",
                "catalog_domain",
                "catalog_path",
                "canonical_ops_id",
                "canonical_slug",
                "final_path",
                "semantic_action",
                "merge_into",
                "owner_match",
                "control_boundary_match",
                "trigger_and_recovery_match",
                "independent_evidence_boundary",
                "reason",
            ),
            tuple(field.name for field in dataclasses.fields(OperationSubjectRecord)),
        )
        self.assertEqual(
            (
                "legacy_path",
                "source_commit",
                "source_blob",
                "role",
                "catalog_path",
                "final_path",
                "semantic_action",
                "canonical_role_owner",
                "preserved_semantics",
                "removed_semantics",
                "active_consumers",
                "final_consumers",
            ),
            tuple(field.name for field in dataclasses.fields(OperationFileRecord)),
        )
        with self.assertRaises(dataclasses.FrozenInstanceError):
            valid_subject_record().reason = "changed"  # type: ignore[misc]

    def test_manifest_covers_exact_current_inventory(self) -> None:
        manifest = load_operations_catalog_manifest(MANIFEST)
        self.assertEqual(BASELINE, manifest.baseline_commit)
        self.assertEqual("approved", manifest.approval.status)
        self.assertEqual("2026-08-13", manifest.approval.approved_at)
        self.assertEqual("user", manifest.approval.approved_by)
        self.assertEqual(77, len(manifest.subjects))
        self.assertEqual(
            {
                "guide": 66,
                "policy": 64,
                "runbook": 62,
                "domain-readme": 13,
            },
            dict(collections.Counter(row.role for row in manifest.files)),
        )
        self.assertEqual((), validate_operations_catalog_manifest(ROOT, manifest))

    def test_displayed_approval_table_is_exactly_bound_to_machine_rows(self) -> None:
        manifest = load_operations_catalog_manifest(MANIFEST)
        text = MANIFEST.read_text(encoding="utf-8")
        mutations = (
            text.replace("| `ops-0001` |", "| `ops-9999` |", 1),
            text.replace("retain policy | Retain managed", "retain guide | Retain managed", 1),
            text.replace("independent operational boundary.", "different rationale.", 1),
        )
        self.assertEqual((), validate_operations_catalog_manifest(ROOT, manifest))
        for index, mutated in enumerate(mutations):
            with self.subTest(index=index), tempfile.TemporaryDirectory() as directory:
                path = pathlib.Path(directory) / "manifest.md"
                path.write_text(mutated, encoding="utf-8")
                loaded = load_operations_catalog_manifest(path)
                self.assertIn(
                    "approval-table-mismatch",
                    finding_codes(validate_operations_catalog_manifest(ROOT, loaded)),
                )

    def test_text_witness_must_derive_from_pinned_role_body(self) -> None:
        manifest = load_operations_catalog_manifest(MANIFEST)
        index = next(
            index
            for index, row in enumerate(manifest.files)
            if row.semantic_action == "rewrite"
        )
        row = manifest.files[index]
        files = list(manifest.files)
        files[index] = dataclasses.replace(
            row,
            preserved_semantics=("text:baseline-body:fabricated semantic evidence that is not in source",),
        )
        self.assertIn(
            "text-witness-source-mismatch",
            finding_codes(
                validate_operations_catalog_manifest(
                    ROOT, dataclasses.replace(manifest, files=tuple(files))
                )
            ),
        )

    def test_active_consumers_must_equal_derived_current_consumers(self) -> None:
        manifest = load_operations_catalog_manifest(MANIFEST)
        index = next(
            index
            for index, row in enumerate(manifest.files)
            if row.active_consumers
        )
        row = manifest.files[index]
        for consumers in (
            row.active_consumers[1:],
            (*row.active_consumers, pathlib.PurePosixPath("README.md")),
        ):
            with self.subTest(consumers=consumers):
                files = list(manifest.files)
                files[index] = dataclasses.replace(row, active_consumers=consumers)
                self.assertIn(
                    "active-consumers-mismatch",
                    finding_codes(
                        validate_operations_catalog_manifest(
                            ROOT, dataclasses.replace(manifest, files=tuple(files))
                        )
                    ),
                )

    def test_structure_mode_validates_only_catalog_paths(self) -> None:
        manifest = self._approved_manifest()
        with tempfile.TemporaryDirectory() as directory:
            execution_root = pathlib.Path(directory)
            self._structure_tree(execution_root, manifest)
            self.assertEqual(
                (),
                validate_operations_catalog_manifest(
                    ROOT,
                    manifest,
                    mode="structure",
                    execution_root=execution_root,
                ),
            )

    def test_structure_mode_rejects_any_role_body_addition_removal_or_rewrite(self) -> None:
        manifest = self._approved_manifest()
        row = next(
            item
            for item in manifest.files
            if item.catalog_path.as_posix().endswith(
                "ops-0003-env-key-comparison/guide.md"
            )
        )
        mutations = {
            "addition": lambda text: text + "\nUnauthorized structural addition.\n",
            "removal": lambda text: text.replace("## Usage", "", 1),
            "rewrite": lambda text: text.replace("## Usage", "## Structural Rewrite", 1),
        }
        for label, mutate in mutations.items():
            with self.subTest(mutation=label), tempfile.TemporaryDirectory() as directory:
                execution_root = pathlib.Path(directory)
                self._structure_tree(execution_root, manifest)
                target = execution_root / row.catalog_path
                target.write_text(
                    mutate(target.read_text(encoding="utf-8")),
                    encoding="utf-8",
                )
                self.assertIn(
                    "structural-body-mismatch",
                    finding_codes(
                        validate_operations_catalog_manifest(
                            ROOT,
                            manifest,
                            mode="structure",
                            execution_root=execution_root,
                        )
                    ),
                )

    def test_structure_semantic_normalization_rejects_unsafe_markdown_targets(self) -> None:
        manifest = self._approved_manifest()
        row = next(
            item
            for item in manifest.files
            if item.catalog_path.as_posix().endswith(
                "ops-0003-env-key-comparison/guide.md"
            )
        )
        unsafe_targets = (
            "/docs/05.operations/catalog/00-workspace/README.md",
            "../../../../../../escape.md",
            "..\\escape.md",
            "../%00escape.md",
        )
        for unsafe_target in unsafe_targets:
            with self.subTest(target=unsafe_target), tempfile.TemporaryDirectory() as directory:
                execution_root = pathlib.Path(directory)
                self._structure_tree(execution_root, manifest)
                target = execution_root / row.catalog_path
                target.write_text(
                    target.read_text(encoding="utf-8")
                    + f"\n[Unsafe structural target]({unsafe_target})\n",
                    encoding="utf-8",
                )
                self.assertIn(
                    "structural-link-target-unsafe",
                    finding_codes(
                        validate_operations_catalog_manifest(
                            ROOT,
                            manifest,
                            mode="structure",
                            execution_root=execution_root,
                        )
                    ),
                )

    def test_active_repository_has_no_legacy_operations_domain_publications(self) -> None:
        pattern = re.compile(
            r"docs/05\.operations/(?:"
            + "|".join(re.escape(domain) for domain in sorted(EXPECTED_DOMAINS))
            + r")(?:/|`|\*|$)"
        )
        excluded_prefixes = (
            "docs/90.references/",
            "docs/98.archive/",
            "graphify-out/",
            "tests/",
        )
        excluded_exact = {
            "docs/00.agent-governance/memory/progress.md",
            "docs/03.specs/spec-0136-sdlc-taxonomy-convergence/plan.md",
        }
        candidates = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.splitlines()
        findings: list[str] = []
        for path_text in candidates:
            if path_text in excluded_exact or path_text.startswith(excluded_prefixes):
                continue
            path = ROOT / path_text
            if not path.is_file():
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeError):
                continue
            if pattern.search(text):
                findings.append(path_text)
        self.assertEqual([], sorted(findings))

    def test_catalog_root_exists_with_exact_domain_set(self) -> None:
        catalog_root = ROOT / "docs/05.operations/catalog"
        self.assertTrue(catalog_root.is_dir())
        self.assertEqual(
            EXPECTED_DOMAINS,
            {path.name for path in catalog_root.iterdir() if path.is_dir()},
        )

    def test_legacy_domain_roots_are_absent(self) -> None:
        operations_root = ROOT / "docs/05.operations"
        for domain in EXPECTED_DOMAINS:
            with self.subTest(domain=domain):
                self.assertFalse((operations_root / domain).exists())

    def test_event_roots_remain_outside_catalog(self) -> None:
        operations_root = ROOT / "docs/05.operations"
        catalog_root = operations_root / "catalog"
        for event_root in ("incidents", "releases"):
            with self.subTest(event_root=event_root):
                self.assertTrue((operations_root / event_root).is_dir())
                self.assertFalse((catalog_root / event_root).exists())

    def test_file_consumers_include_current_scripts_tests_and_exclude_history(self) -> None:
        manifest = load_operations_catalog_manifest(MANIFEST)
        declared = {
            consumer.as_posix()
            for row in manifest.files
            for consumer in row.active_consumers
        }
        self.assertIn("scripts/manifest.yaml", declared)
        self.assertIn("tests/validation/test_script_manifest.py", declared)
        self.assertIn("scripts/validation/check-repo-contracts.sh", declared)
        self.assertFalse(any(path.startswith("docs/98.archive/") for path in declared))
        allowed_stage90 = {
            "docs/90.references/data/knowledge/ref-0076-llm-wiki-stage-category-coverage.md",
            "docs/90.references/llm-wiki/ref-0082-llm-wiki-index.md",
        }
        self.assertEqual(
            set(),
            {path for path in declared if path.startswith("docs/90.references/")}
            - allowed_stage90,
        )

    def test_manifest_freezes_every_source_git_object(self) -> None:
        manifest = load_operations_catalog_manifest(MANIFEST)
        for subject in manifest.subjects:
            with self.subTest(subject=subject.current_ops_id):
                actual = subprocess.run(
                    [
                        "git",
                        "rev-parse",
                        f"{subject.source_commit}:{subject.legacy_subject_path.as_posix()}",
                    ],
                    cwd=ROOT,
                    check=True,
                    capture_output=True,
                    text=True,
                ).stdout.strip()
                self.assertEqual(subject.source_tree, actual)
        for row in manifest.files:
            with self.subTest(path=row.legacy_path):
                actual = subprocess.run(
                    [
                        "git",
                        "rev-parse",
                        f"{row.source_commit}:{row.legacy_path.as_posix()}",
                    ],
                    cwd=ROOT,
                    check=True,
                    capture_output=True,
                    text=True,
                ).stdout.strip()
                self.assertEqual(row.source_blob, actual)

    def test_similarity_cannot_authorize_merge(self) -> None:
        base = valid_subject_record(
            semantic_action="merge",
            merge_into="ops-0050",
            canonical_ops_id="ops-0050",
            canonical_slug="airflow",
            final_path=pathlib.PurePosixPath(
                "docs/05.operations/catalog/07-workflow/ops-0050-airflow"
            ),
            owner_match=True,
            control_boundary_match=True,
            trigger_and_recovery_match=True,
            independent_evidence_boundary=False,
        )
        mutations = {
            "owner_match": "merge-owner-boundary-unproven",
            "control_boundary_match": "merge-control-boundary-unproven",
            "trigger_and_recovery_match": "merge-trigger-recovery-unproven",
            "independent_evidence_boundary": "merge-independent-evidence-boundary",
        }
        for field, code in mutations.items():
            value = True if field == "independent_evidence_boundary" else False
            with self.subTest(field=field):
                findings = validate_subject_disposition(
                    dataclasses.replace(base, **{field: value})
                )
                self.assertIn(code, finding_codes(findings))
        self.assertEqual((), validate_subject_disposition(base))

    def test_merge_candidates_are_only_fully_proven_rows(self) -> None:
        approved = dataclasses.replace(
            valid_subject_record(),
            semantic_action="merge",
            merge_into="ops-0050",
            canonical_ops_id="ops-0050",
            canonical_slug="airflow",
            final_path=pathlib.PurePosixPath(
                "docs/05.operations/catalog/07-workflow/ops-0050-airflow"
            ),
            owner_match=True,
            control_boundary_match=True,
            trigger_and_recovery_match=True,
            independent_evidence_boundary=False,
        )
        unproved = dataclasses.replace(approved, current_ops_id="ops-0051", owner_match=False)
        self.assertEqual((approved,), find_operations_merge_candidates((approved, unproved)))

    def test_parser_rejects_unknown_and_duplicate_keys(self) -> None:
        text = MANIFEST.read_text(encoding="utf-8")
        mutations = (
            text.replace("schema_version: 1", "schema_version: 1\nunknown: true", 1),
            text.replace("schema_version: 1", "schema_version: 1\nschema_version: 1", 1),
            text.replace("  status: approved", "  status: approved\n  unknown: true", 1),
        )
        for index, body in enumerate(mutations):
            with self.subTest(index=index), tempfile.TemporaryDirectory() as directory:
                path = pathlib.Path(directory) / "manifest.md"
                path.write_text(body, encoding="utf-8")
                with self.assertRaises(ManifestError):
                    load_operations_catalog_manifest(path)

    def test_validator_rejects_unsafe_duplicate_and_git_object_mutations(self) -> None:
        manifest = load_operations_catalog_manifest(MANIFEST)
        first = manifest.subjects[0]
        second = manifest.subjects[1]
        cases = {
            "unsafe-path": dataclasses.replace(
                manifest,
                subjects=(
                    dataclasses.replace(
                        first,
                        legacy_subject_path=pathlib.PurePosixPath("../escape"),
                    ),
                    *manifest.subjects[1:],
                ),
            ),
            "duplicate-subject-source": dataclasses.replace(
                manifest,
                subjects=(first, dataclasses.replace(second, legacy_subject_path=first.legacy_subject_path), *manifest.subjects[2:]),
            ),
            "source-tree-mismatch": dataclasses.replace(
                manifest,
                subjects=(dataclasses.replace(first, source_tree="0" * 40), *manifest.subjects[1:]),
            ),
            "source-blob-mismatch": dataclasses.replace(
                manifest,
                files=(dataclasses.replace(manifest.files[0], source_blob="0" * 40), *manifest.files[1:]),
            ),
        }
        for expected, mutated in cases.items():
            with self.subTest(expected=expected):
                self.assertIn(
                    expected,
                    finding_codes(validate_operations_catalog_manifest(ROOT, mutated)),
                )

    def test_historical_evidence_cannot_be_declared_an_active_consumer(self) -> None:
        manifest = load_operations_catalog_manifest(MANIFEST)
        first = manifest.files[0]
        mutated = dataclasses.replace(
            manifest,
            files=(
                dataclasses.replace(
                    first,
                    active_consumers=(
                        pathlib.PurePosixPath("docs/98.archive/README.md"),
                    ),
                ),
                *manifest.files[1:],
            ),
        )
        self.assertIn(
            "active-consumer-historical",
            finding_codes(validate_operations_catalog_manifest(ROOT, mutated)),
        )

    def test_merge_file_requires_concrete_unique_and_removed_semantics(self) -> None:
        manifest = load_operations_catalog_manifest(MANIFEST)
        merge_index = next(
            index
            for index, row in enumerate(manifest.files)
            if row.semantic_action == "merge"
        )
        row = manifest.files[merge_index]
        mutated_files = list(manifest.files)
        mutated_files[merge_index] = dataclasses.replace(
            row,
            preserved_semantics=("section:overview:000000000000",),
            removed_semantics=(),
        )
        self.assertEqual(
            {
                "merge-preserved-semantics-unproven",
                "merge-removed-semantics-unproven",
            },
            finding_codes(
                validate_operations_catalog_manifest(
                    ROOT,
                    dataclasses.replace(manifest, files=tuple(mutated_files)),
                )
            )
            & {
                "merge-preserved-semantics-unproven",
                "merge-removed-semantics-unproven",
            },
        )

    def test_retain_subject_allows_evidence_bounded_role_rewrite(self) -> None:
        manifest = load_operations_catalog_manifest(MANIFEST)
        rewritten = next(
            row
            for row in manifest.files
            if row.legacy_path.as_posix().endswith("ops-0003-env-key-comparison/guide.md")
        )
        self.assertEqual("rewrite", rewritten.semantic_action)
        self.assertTrue(rewritten.preserved_semantics)
        self.assertEqual(("contradiction:env-key-diff-count",), rewritten.removed_semantics)

    def test_section_preservation_tokens_are_body_sensitive(self) -> None:
        manifest = load_operations_catalog_manifest(MANIFEST)
        row = next(
            item
            for item in manifest.files
            if item.legacy_path.as_posix().endswith("ops-0003-env-key-comparison/guide.md")
        )
        text = subprocess.run(
            ["git", "show", f"{BASELINE}:{row.legacy_path.as_posix()}"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        matches = list(__import__("re").finditer(r"(?m)^#{1,6}\s+(.+?)\s*$", text))
        expected: set[str] = set()
        for index, match in enumerate(matches):
            slug = __import__("re").sub(
                r"[^a-z0-9]+", "-", match.group(1).lower()
            ).strip("-")
            section = text[
                match.start() : (
                    matches[index + 1].start() if index + 1 < len(matches) else len(text)
                )
            ].strip()
            expected.add(f"section:{slug}:{hashlib.sha256(section.encode()).hexdigest()[:12]}")
        self.assertEqual(
            expected,
            {token for token in row.preserved_semantics if token.startswith("section:")},
        )
        mutated = text.replace("## Overview", "## Overview\nmutated body", 1)
        self.assertNotEqual(
            hashlib.sha256(text.encode()).hexdigest(),
            hashlib.sha256(mutated.encode()).hexdigest(),
        )

    def test_executed_rewrite_requires_every_text_witness(self) -> None:
        manifest = self._approved_manifest()
        row = next(
            item
            for item in manifest.files
            if item.legacy_path.as_posix().endswith("ops-0003-env-key-comparison/guide.md")
        )
        witness = next(
            item.split(":", 2)[2]
            for item in row.preserved_semantics
            if item.startswith("text:")
        )
        with tempfile.TemporaryDirectory() as directory:
            execution_root = pathlib.Path(directory)
            self._execution_tree(execution_root, manifest, "00-workspace")
            self.assertEqual(
                (),
                validate_operations_catalog_manifest(
                    ROOT,
                    manifest,
                    mode="executed",
                    domains=("00-workspace",),
                    execution_root=execution_root,
                ),
            )
            target = execution_root / row.final_path
            target.write_text(
                target.read_text(encoding="utf-8").replace(witness, "", 1),
                encoding="utf-8",
            )
            self.assertIn(
                "preserved-semantics-mismatch",
                finding_codes(
                    validate_operations_catalog_manifest(
                        ROOT,
                        manifest,
                        mode="executed",
                        domains=("00-workspace",),
                        execution_root=execution_root,
                    )
                ),
            )

    def test_executed_semantic_normalization_rejects_unsafe_link_targets(self) -> None:
        manifest = self._approved_manifest()
        row = next(
            item
            for item in manifest.files
            if item.legacy_path.as_posix().endswith(
                "ops-0007-llm-wiki-maintenance/guide.md"
            )
        )
        valid_relative = "../../../README.md"
        unsafe_targets = (
            "/docs/05.operations/README.md",
            "../../../../../../escape.md",
            "..\\escape.md",
            "../%00escape.md",
        )
        for unsafe_target in unsafe_targets:
            with self.subTest(target=unsafe_target), tempfile.TemporaryDirectory() as directory:
                execution_root = pathlib.Path(directory)
                self._execution_tree(execution_root, manifest, "00-workspace")
                self.assertEqual(
                    (),
                    validate_operations_catalog_manifest(
                        ROOT,
                        manifest,
                        mode="executed",
                        domains=("00-workspace",),
                        execution_root=execution_root,
                    ),
                )
                target = execution_root / row.final_path
                original = target.read_text(encoding="utf-8")
                self.assertIn(f"]({valid_relative})", original)
                target.write_text(
                    original.replace(valid_relative, unsafe_target, 1),
                    encoding="utf-8",
                )
                self.assertIn(
                    "semantic-link-invalid",
                    finding_codes(
                        validate_operations_catalog_manifest(
                            ROOT,
                            manifest,
                            mode="executed",
                            domains=("00-workspace",),
                            execution_root=execution_root,
                        )
                    ),
                )

    def test_executed_merge_requires_every_text_witness(self) -> None:
        manifest = self._approved_manifest()
        row = next(
            item
            for item in manifest.files
            if item.legacy_path.as_posix().endswith("ops-0052-dag-deployment/policy.md")
        )
        witness = next(
            item.split(":", 2)[2]
            for item in row.preserved_semantics
            if item.startswith("text:")
        )
        with tempfile.TemporaryDirectory() as directory:
            execution_root = pathlib.Path(directory)
            self._execution_tree(execution_root, manifest, "07-workflow")
            self.assertEqual(
                (),
                validate_operations_catalog_manifest(
                    ROOT,
                    manifest,
                    mode="executed",
                    domains=("07-workflow",),
                    execution_root=execution_root,
                ),
            )
            target = execution_root / row.final_path
            target.write_text(
                target.read_text(encoding="utf-8").replace(witness, "", 1),
                encoding="utf-8",
            )
            self.assertIn(
                "preserved-semantics-mismatch",
                finding_codes(
                    validate_operations_catalog_manifest(
                        ROOT,
                        manifest,
                        mode="executed",
                        domains=("07-workflow",),
                        execution_root=execution_root,
                    )
                ),
            )

    def test_execution_accounts_for_every_non_removed_source_section(self) -> None:
        manifest = self._approved_manifest()
        cases = (
            (
                "00-workspace",
                "ops-0002-developer-setup/guide.md",
                "Common Checks",
            ),
            (
                "07-workflow",
                "ops-0052-dag-deployment/policy.md",
                "Review Cadence",
            ),
        )
        for domain, suffix, deleted_heading in cases:
            with self.subTest(suffix=suffix), tempfile.TemporaryDirectory() as directory:
                execution_root = pathlib.Path(directory)
                self._execution_tree(execution_root, manifest, domain)
                row = next(
                    item
                    for item in manifest.files
                    if item.legacy_path.as_posix().endswith(suffix)
                )
                target = execution_root / row.final_path
                original = target.read_text(encoding="utf-8")
                transformed = original.replace(
                    row.legacy_path.as_posix(),
                    row.final_path.as_posix(),
                ).replace(
                    row.legacy_path.parent.name,
                    row.final_path.parent.name,
                )
                target.write_text(transformed, encoding="utf-8")
                self.assertEqual(
                    (),
                    validate_operations_catalog_manifest(
                        ROOT,
                        manifest,
                        mode="executed",
                        domains=(domain,),
                        execution_root=execution_root,
                    ),
                )
                target.write_text(
                    remove_markdown_section(transformed, deleted_heading),
                    encoding="utf-8",
                )
                witnesses = [
                    item.split(":", 2)[2]
                    for item in row.preserved_semantics
                    if item.startswith("text:")
                ]
                self.assertTrue(all(item in target.read_text() for item in witnesses))
                self.assertIn(
                    "preserved-semantics-mismatch",
                    finding_codes(
                        validate_operations_catalog_manifest(
                            ROOT,
                            manifest,
                            mode="executed",
                            domains=(domain,),
                            execution_root=execution_root,
                        )
                    ),
                )

    def test_active_consumers_require_explicit_exact_final_routes(self) -> None:
        manifest = load_operations_catalog_manifest(MANIFEST)
        row = next(item for item in manifest.files if item.active_consumers)
        self.assertEqual(len(row.active_consumers), len(row.final_consumers))
        index = manifest.files.index(row)
        for routes in (
            row.final_consumers[1:],
            (*row.final_consumers, pathlib.PurePosixPath("README.md")),
        ):
            with self.subTest(routes=routes):
                files = list(manifest.files)
                files[index] = dataclasses.replace(row, final_consumers=routes)
                self.assertIn(
                    "active-consumer-routes-mismatch",
                    finding_codes(
                        validate_operations_catalog_manifest(
                            ROOT, dataclasses.replace(manifest, files=tuple(files))
                        )
                    ),
                )

    def test_executed_consumer_must_exist_at_declared_regular_final_path(self) -> None:
        manifest = self._approved_manifest()
        domain = "00-workspace"
        with tempfile.TemporaryDirectory() as directory:
            execution_root = pathlib.Path(directory)
            self._execution_tree(execution_root, manifest, domain)
            row = next(
                item
                for item in manifest.files
                if item.legacy_path.parts[2] == domain and item.final_consumers
            )
            consumer = execution_root / row.final_consumers[0]
            consumer.unlink()
            self.assertIn(
                "executed-consumer-missing",
                finding_codes(
                    validate_operations_catalog_manifest(
                        ROOT,
                        manifest,
                        mode="executed",
                        domains=(domain,),
                        execution_root=execution_root,
                    )
                ),
            )
            consumer.symlink_to(ROOT / row.active_consumers[0])
            self.assertIn(
                "executed-consumer-symlink-invalid",
                finding_codes(
                    validate_operations_catalog_manifest(
                        ROOT,
                        manifest,
                        mode="executed",
                        domains=(domain,),
                        execution_root=execution_root,
                    )
                ),
            )

    def test_executed_rejects_symlink_predecessor_and_stale_consumer(self) -> None:
        manifest = self._approved_manifest()
        domain = "00-workspace"
        with tempfile.TemporaryDirectory() as directory:
            execution_root = pathlib.Path(directory)
            self._execution_tree(execution_root, manifest, domain)
            subject = next(
                row
                for row in manifest.subjects
                if row.catalog_domain == domain and row.semantic_action == "rename"
            )
            predecessor = execution_root / subject.legacy_subject_path
            predecessor.parent.mkdir(parents=True, exist_ok=True)
            predecessor.symlink_to(execution_root / subject.final_path, target_is_directory=True)
            self.assertTrue(
                {
                    "executed-predecessor-present",
                    "executed-symlink-invalid",
                }
                & finding_codes(
                    validate_operations_catalog_manifest(
                        ROOT,
                        manifest,
                        mode="executed",
                        domains=(domain,),
                        execution_root=execution_root,
                    )
                )
            )

        with tempfile.TemporaryDirectory() as directory:
            execution_root = pathlib.Path(directory)
            self._execution_tree(execution_root, manifest, domain)
            row = next(
                item
                for item in manifest.files
                if item.legacy_path.parts[2] == domain
                and item.active_consumers
                and item.final_path != item.catalog_path
            )
            consumer = execution_root / row.final_consumers[0]
            consumer.parent.mkdir(parents=True, exist_ok=True)
            consumer.write_text(row.legacy_path.as_posix(), encoding="utf-8")
            self.assertIn(
                "executed-stale-consumer",
                finding_codes(
                    validate_operations_catalog_manifest(
                        ROOT,
                        manifest,
                        mode="executed",
                        domains=(domain,),
                        execution_root=execution_root,
                    )
                ),
            )

    def test_complete_mode_accepts_full_typed_operations_tree(self) -> None:
        manifest = self._approved_manifest()
        with tempfile.TemporaryDirectory() as directory:
            execution_root = pathlib.Path(directory)
            self._complete_tree(execution_root, manifest)
            self.assertEqual(
                (),
                validate_operations_catalog_manifest(
                    ROOT,
                    manifest,
                    mode="complete",
                    execution_root=execution_root,
                ),
            )

    def test_complete_mode_requires_every_operations_index(self) -> None:
        manifest = self._approved_manifest()
        indexes = (
            "docs/05.operations/catalog/README.md",
            "docs/05.operations/incidents/README.md",
            "docs/05.operations/releases/README.md",
        )
        for index in indexes:
            with self.subTest(index=index), tempfile.TemporaryDirectory() as directory:
                execution_root = pathlib.Path(directory)
                self._complete_tree(execution_root, manifest)
                (execution_root / index).unlink()
                self.assertIn(
                    "complete-index-invalid",
                    finding_codes(
                        validate_operations_catalog_manifest(
                            ROOT,
                            manifest,
                            mode="complete",
                            execution_root=execution_root,
                        )
                    ),
                )

    def test_complete_mode_requires_exact_root_and_catalog_index_routes(self) -> None:
        manifest = self._approved_manifest()
        mutations = (
            (
                "docs/05.operations/README.md",
                "- [Releases](releases/)\n",
                "",
            ),
            (
                "docs/05.operations/README.md",
                "- [Releases](releases/)\n",
                "- [Release history](releases.md)\n",
            ),
            (
                "docs/05.operations/README.md",
                "- [Releases](releases/)\n",
                "- [Release section](#releases)\n",
            ),
            (
                "docs/05.operations/README.md",
                "- [Releases](releases/)\n",
                "- [Releases](releases/)\n- [Extra](extra/)\n",
            ),
            (
                "docs/05.operations/catalog/README.md",
                "- [00-workspace](00-workspace/)\n",
                "",
            ),
            (
                "docs/05.operations/catalog/README.md",
                "- [00-workspace](00-workspace/)\n",
                "- [00-workspace](00-workspace/)\n- [Extra](99-extra/)\n",
            ),
        )
        for index, old, new in mutations:
            with self.subTest(index=index, replacement=new), tempfile.TemporaryDirectory() as directory:
                execution_root = pathlib.Path(directory)
                self._complete_tree(execution_root, manifest)
                target = execution_root / index
                target.write_text(
                    target.read_text(encoding="utf-8").replace(old, new, 1),
                    encoding="utf-8",
                )
                self.assertIn(
                    "complete-index-routes-mismatch",
                    finding_codes(
                        validate_operations_catalog_manifest(
                            ROOT,
                            manifest,
                            mode="complete",
                            execution_root=execution_root,
                        )
                    ),
                )

    def test_complete_mode_parses_only_safe_direct_directory_routes(self) -> None:
        manifest = self._approved_manifest()
        with tempfile.TemporaryDirectory() as directory:
            execution_root = pathlib.Path(directory)
            self._complete_tree(execution_root, manifest)
            operations_root = execution_root / "docs/05.operations"
            (operations_root / "README.md").write_text(
                """# Operations

- [Catalog](<./catalog/?view=all#catalog>)
- [Incidents](%69ncidents/#current)
- [Releases](releases/(current)/../)
- [Same document](#operations)
- [Historical file](history.md)

Historical context mentions `guides/`, while this deeper
[catalog example](catalog/00-workspace/) and [Spec](../../03.specs/spec-0136-sdlc-taxonomy-convergence/spec.md)
are not direct root routes.

`[Inline fake](extra-inline/)`

```markdown
[Fenced fake](extra-fenced/)
```
""",
                encoding="utf-8",
            )
            catalog_index = operations_root / "catalog/README.md"
            catalog_text = catalog_index.read_text(encoding="utf-8")
            catalog_text = catalog_text.replace(
                "[00-workspace](00-workspace/)",
                "[Workspace](<./00-workspace/?view=all#workspace>)",
            ).replace(
                "[01-gateway](01-gateway/)",
                "[Gateway](%30%31-gateway/#current)",
            ).replace(
                "[02-auth](02-auth/)",
                "[Auth](02-auth/(history)/../)",
            )
            catalog_index.write_text(
                catalog_text
                + "\nHistorical context points to a deeper "
                "[subject](00-workspace/ops-0001-common-optimizations-template-exceptions/).\n"
                "[Same document](#operations-catalog) and [historical file](history.md).\n"
                "`[Inline fake](99-inline/)`\n"
                "```markdown\n[Fenced fake](99-fenced/)\n```\n",
                encoding="utf-8",
            )

            self.assertEqual(
                (),
                validate_operations_catalog_manifest(
                    ROOT,
                    manifest,
                    mode="complete",
                    execution_root=execution_root,
                ),
            )

        unsafe_routes = (
            "[Absolute](/docs/05.operations/catalog/)",
            "[Outside](../../../escape/)",
            "[Backslash](catalog\\legacy/)",
            "[NUL](catalog/%00/)",
            "[Query C0](catalog/?bad=%00)",
            "[Fragment C0](catalog/#bad=%1F)",
        )
        for unsafe_route in unsafe_routes:
            with (
                self.subTest(route=unsafe_route),
                tempfile.TemporaryDirectory() as directory,
            ):
                execution_root = pathlib.Path(directory)
                self._complete_tree(execution_root, manifest)
                index = execution_root / "docs/05.operations/README.md"
                index.write_text(
                    index.read_text(encoding="utf-8") + f"\n- {unsafe_route}\n",
                    encoding="utf-8",
                )
                self.assertIn(
                    "complete-index-route-invalid",
                    finding_codes(
                        validate_operations_catalog_manifest(
                            ROOT,
                            manifest,
                            mode="complete",
                            execution_root=execution_root,
                        )
                    ),
                )

    def test_complete_mode_rejects_invalid_utf8_index_explicitly(self) -> None:
        manifest = self._approved_manifest()
        with tempfile.TemporaryDirectory() as directory:
            execution_root = pathlib.Path(directory)
            self._complete_tree(execution_root, manifest)
            (execution_root / "docs/05.operations/README.md").write_bytes(b"\xff")
            self.assertIn(
                "complete-index-unreadable",
                finding_codes(
                    validate_operations_catalog_manifest(
                        ROOT,
                        manifest,
                        mode="complete",
                        execution_root=execution_root,
                    )
                ),
            )

    def test_complete_mode_rejects_extra_catalog_root_file(self) -> None:
        manifest = self._approved_manifest()
        with tempfile.TemporaryDirectory() as directory:
            execution_root = pathlib.Path(directory)
            self._complete_tree(execution_root, manifest)
            (execution_root / "docs/05.operations/catalog/notes.md").write_text(
                "unregistered",
                encoding="utf-8",
            )
            self.assertIn(
                "complete-catalog-contents-mismatch",
                finding_codes(
                    validate_operations_catalog_manifest(
                        ROOT,
                        manifest,
                        mode="complete",
                        execution_root=execution_root,
                    )
                ),
            )

    def test_complete_mode_rejects_malformed_incident_and_release_contents(self) -> None:
        manifest = self._approved_manifest()
        mutations = (
            ("docs/05.operations/incidents/incident-notes.md", "complete-incident-contents-invalid"),
            ("docs/05.operations/incidents/current/inc-0002-bad-year/incident.md", "complete-incident-contents-invalid"),
            ("docs/05.operations/incidents/2026/inc-2-bad-id/incident.md", "complete-incident-contents-invalid"),
            ("docs/05.operations/incidents/2026/inc-0002-bad-role/timeline.md", "complete-incident-contents-invalid"),
            ("docs/05.operations/releases/2026-08-13-release.md", "complete-release-contents-invalid"),
            ("docs/05.operations/releases/release-0002-bad-id/release.md", "complete-release-contents-invalid"),
            ("docs/05.operations/releases/rel-0002-bad-role/notes.md", "complete-release-contents-invalid"),
        )
        for relative_path, expected_code in mutations:
            with self.subTest(path=relative_path), tempfile.TemporaryDirectory() as directory:
                execution_root = pathlib.Path(directory)
                self._complete_tree(execution_root, manifest)
                target = execution_root / relative_path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("malformed", encoding="utf-8")
                self.assertIn(
                    expected_code,
                    finding_codes(
                        validate_operations_catalog_manifest(
                            ROOT,
                            manifest,
                            mode="complete",
                            execution_root=execution_root,
                        )
                    ),
                )

    def test_complete_mode_rejects_nested_subject_readme(self) -> None:
        manifest = self._approved_manifest()
        with tempfile.TemporaryDirectory() as directory:
            execution_root = pathlib.Path(directory)
            self._complete_tree(execution_root, manifest)
            subject = next(iter(manifest.subjects))
            nested = execution_root / subject.final_path / "attachments/README.md"
            nested.parent.mkdir()
            nested.write_text("# Forbidden nested index\n", encoding="utf-8")
            self.assertIn(
                "complete-subject-readme-invalid",
                finding_codes(
                    validate_operations_catalog_manifest(
                        ROOT,
                        manifest,
                        mode="complete",
                        execution_root=execution_root,
                    )
                ),
            )

    def test_complete_mode_requires_exact_catalog_topology_and_index(self) -> None:
        manifest = self._approved_manifest()
        with tempfile.TemporaryDirectory() as directory:
            execution_root = pathlib.Path(directory)
            self._complete_tree(execution_root, manifest)
            extra = execution_root / "docs/05.operations/catalog/00-workspace/unregistered"
            extra.mkdir()
            self.assertIn(
                "complete-domain-contents-mismatch",
                finding_codes(
                    validate_operations_catalog_manifest(
                        ROOT,
                        manifest,
                        mode="complete",
                        execution_root=execution_root,
                    )
                ),
            )
            extra.rmdir()
            extra_root = execution_root / "docs/05.operations/guides"
            extra_root.mkdir()
            self.assertIn(
                "complete-root-contents-mismatch",
                finding_codes(
                    validate_operations_catalog_manifest(
                        ROOT,
                        manifest,
                        mode="complete",
                        execution_root=execution_root,
                    )
                ),
            )
            extra_root.rmdir()
            subject = next(iter(manifest.subjects))
            subject_readme = execution_root / subject.final_path / "README.md"
            subject_readme.write_text("# Forbidden\n", encoding="utf-8")
            self.assertIn(
                "complete-subject-readme-invalid",
                finding_codes(
                    validate_operations_catalog_manifest(
                        ROOT,
                        manifest,
                        mode="complete",
                        execution_root=execution_root,
                    )
                ),
            )


    def test_validator_rejects_merge_cycles_and_self_merge(self) -> None:
        manifest = load_operations_catalog_manifest(MANIFEST)
        first, second = manifest.subjects[:2]
        common = {
            "semantic_action": "merge",
            "owner_match": True,
            "control_boundary_match": True,
            "trigger_and_recovery_match": True,
            "independent_evidence_boundary": False,
        }
        self_merge = dataclasses.replace(first, merge_into=first.current_ops_id, **common)
        self.assertIn(
            "merge-self",
            finding_codes(
                validate_operations_catalog_manifest(
                    ROOT,
                    dataclasses.replace(manifest, subjects=(self_merge, *manifest.subjects[1:])),
                )
            ),
        )
        one = dataclasses.replace(
            first,
            merge_into=second.current_ops_id,
            canonical_ops_id=second.current_ops_id,
            canonical_slug=second.canonical_slug,
            final_path=second.final_path,
            **common,
        )
        two = dataclasses.replace(
            second,
            merge_into=first.current_ops_id,
            canonical_ops_id=first.current_ops_id,
            canonical_slug=first.canonical_slug,
            final_path=first.final_path,
            **common,
        )
        self.assertIn(
            "merge-cycle",
            finding_codes(
                validate_operations_catalog_manifest(
                    ROOT,
                    dataclasses.replace(manifest, subjects=(one, two, *manifest.subjects[2:])),
                )
            ),
        )

    def test_pending_approval_is_non_executable(self) -> None:
        approved = load_operations_catalog_manifest(MANIFEST)
        manifest = dataclasses.replace(
            approved,
            approval=dataclasses.replace(
                approved.approval,
                status="pending",
                approved_at=None,
                approved_by=None,
            ),
        )
        for mode in ("structure", "executed", "complete"):
            with self.subTest(mode=mode):
                self.assertIn(
                    "approval-pending",
                    finding_codes(
                        validate_operations_catalog_manifest(
                            ROOT,
                            manifest,
                            mode=mode,
                            domains=("00-workspace",) if mode == "executed" else (),
                        )
                    ),
                )

    def test_cli_mode_and_domain_contract_is_fail_closed(self) -> None:
        good = subprocess.run(
            [str(CLI), "--mode", "manifest"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(0, good.returncode, good.stdout + good.stderr)
        self.assertIn("subjects=77 files=205 approval=approved", good.stdout)
        for args in (
            ["--mode", "manifest", "--domains", "00-workspace"],
            ["--mode", "structure", "--domains", "00-workspace"],
            ["--mode", "complete", "--domains", "00-workspace"],
            ["--mode", "executed"],
            ["--mode", "executed", "--domains", "unknown"],
        ):
            with self.subTest(args=args):
                result = subprocess.run(
                    [str(CLI), *args],
                    cwd=ROOT,
                    text=True,
                    capture_output=True,
                )
                self.assertNotEqual(0, result.returncode)


if __name__ == "__main__":
    unittest.main()
