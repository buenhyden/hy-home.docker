from __future__ import annotations

import copy
import collections
import contextlib
import dataclasses
import datetime
import hashlib
import io
import importlib.util
import inspect
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import yaml

from scripts.lib.document_governance.spec_packages import load_spec_packages
from scripts.lib.document_governance import archive as archive_authority


ROOT = pathlib.Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/validation/check-document-corpus-lifecycle.py"
METADATA_SCRIPT = ROOT / "scripts/validation/check-document-metadata.py"
REGISTRY = ROOT / "docs/99.templates/registry.json"
PROFILES = ROOT / "docs/99.templates/support/document-metadata-profiles.yaml"
CONTRACT = ROOT / "docs/99.templates/support/document-corpus-migration-contract.yaml"
CORPUS_HUMAN_CONTRACT = ROOT / "docs/99.templates/support/corpus-migration-contract.md"
ARCHIVE_HUMAN_CONTRACT = ROOT / "docs/99.templates/support/archive-retention-contract.md"
TASK7_LEDGER = ROOT / "docs/98.archive/migrations/0001-sdlc-taxonomy-convergence.md"
TARGET_WAVE = "target-surface-convergence"
TARGET_BASELINE = "32c40e11747bc0bd03789c24861d2e5d60c0e999"
SUCCESSOR_MANIFEST = (
    "docs/90.references/data/0073-target-surface-delta-manifest/data.yaml"
)
SAMPLE_FIXTURE_PATH = "examples/sample-web-service/service.md"
SAMPLE_PREDECESSOR_EQUALITY_CODES = {
    "manifest-target-parent-ids-mismatch",
    "manifest-target-profile-invalid",
    "manifest-target-status-mismatch",
}


def load_script(path: pathlib.Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


lifecycle = load_script(SCRIPT, "document_corpus_lifecycle")
metadata = load_script(METADATA_SCRIPT, "document_metadata_for_lifecycle_tests")


class SharedProvenanceExtractionTests(unittest.TestCase):
    def test_lifecycle_uses_shared_git_provenance_without_file_loading_metadata(self) -> None:
        source = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("scripts.lib.document_governance.git_provenance", source)
        self.assertNotIn("METADATA_SCRIPT", source)
        self.assertNotIn(
            'spec_from_file_location(\n        "document_metadata',
            source,
        )


def task7_ledger_payload() -> dict[str, object]:
    text = TASK7_LEDGER.read_text(encoding="utf-8")
    yaml_text = text.split("```yaml\n", 1)[1].split("```", 1)[0]
    payload = yaml.safe_load(yaml_text)
    if not isinstance(payload, dict):
        raise AssertionError("mig-0001 YAML block must be a mapping")
    return payload


def task7_rows(payload: dict[str, object]) -> list[dict[str, object]]:
    baseline = payload.get("records")
    extension = payload.get("post_baseline_records")
    if not isinstance(baseline, list) or not isinstance(extension, list):
        raise AssertionError("mig-0001 baseline and extension records must be lists")
    return [
        row
        for row in [*baseline, *extension]
        if isinstance(row, dict)
        and (
            str(row.get("legacy_path", "")).startswith(
                ("docs/90.references/", "docs/98.archive/")
            )
            or row.get("legacy_path") == "archive/Windows-Network-IP.md"
        )
    ]


def is_typed_task7_target(target: str) -> bool:
    patterns = (
        r"docs/01\.requirements/prd-[0-9]{4}-[^/]+\.md",
        r"docs/02\.architecture/descriptions/ad-[0-9]{4}-[^/]+\.md",
        r"docs/02\.architecture/decisions/adr-[0-9]{4}-[^/]+\.md",
        r"docs/03\.specs/spec-[0-9]{4}-[^/]+/(?:spec|plan|task)\.md",
        r"docs/05\.operations/[0-9]{2}-[^/]+/ops-[0-9]{4}-[^/]+/(?:guide|policy|runbook)\.md",
        r"docs/05\.operations/incidents/[0-9]{4}/inc-[0-9]{4}-[^/]+/(?:incident|postmortem)\.md",
        r"docs/05\.operations/releases/rel-[0-9]{4}-[^/]+/release\.md",
        r"docs/90\.references/(?:.+/)?(?:ref|audit)-[0-9]{4}-[^/]+(?:\.(?:md|yaml|yml|json)|/README\.md)",
        r"docs/98\.archive/changes/chg-[0-9]{4}-[^/]+/(?:plan|task)\.md",
        r"docs/98\.archive/tombstones/(?:01\.requirements|02\.architecture|03\.specs|05\.operations)/[^/]+\.md",
        r"docs/98\.archive/migrations/mig-[0-9]{4}-[^/]+\.md",
    )
    return target.endswith("/README.md") or any(
        re.fullmatch(pattern, target) for pattern in patterns
    )


class Task7LedgerRepairTests(unittest.TestCase):
    ROW_FIELDS = {
        "legacy_path",
        "stable_path",
        "artifact_id",
        "action",
        "replacement",
        "source_commit",
        "reason",
    }
    EXTENSION = (
        (
            "archive/Windows-Network-IP.md",
            "docs/98.archive/tombstones/05.operations/ref-0095-windows-network-ip.md",
            "ref-0095",
            "archive",
            "32c40e11747bc0bd03789c24861d2e5d60c0e999",
        ),
        (
            "docs/90.references/research/0001-agentic-research-pack-refresh/github-actions-platform.md",
            "docs/90.references/research/0084-github-actions-platform/README.md",
            "ref-0084",
            "move",
            "f2f8f8a441b5977d55e516ba59ea7865c06d6c55",
        ),
        (
            "docs/90.references/research/0001-agentic-research-pack-refresh/verification-validation.md",
            "docs/90.references/research/ref-0085-verification-validation.md",
            "ref-0085",
            "move",
            "9c927a0e187a4214358453f4826dc758a72611b5",
        ),
    )
    CHANGE_PACKET_REPAIR = {
        "docs/98.archive/04.execution/plans/2026-05-30-ai-governance-reorg.md": (
            "docs/98.archive/changes/chg-0143-ai-governance-reorg/plan.md",
            "plan-0143",
        ),
        "docs/98.archive/04.execution/plans/2026-05-30-standardizing-agent-governance.md": (
            "docs/98.archive/changes/chg-0144-standardizing-agent-governance/plan.md",
            "plan-0144",
        ),
        "docs/98.archive/04.execution/tasks/2026-05-30-standardizing-agent-governance.md": (
            "docs/98.archive/changes/chg-0144-standardizing-agent-governance/task.md",
            "task-0144-01",
        ),
        "docs/98.archive/04.execution/plans/2026-06-01-agent-governance-phase1-diagnostic.md": (
            "docs/98.archive/changes/chg-0145-agent-governance-phase1-diagnostic/plan.md",
            "plan-0145",
        ),
        "docs/98.archive/04.execution/tasks/2026-06-01-agent-governance-phase1-diagnostic.md": (
            "docs/98.archive/changes/chg-0145-agent-governance-phase1-diagnostic/task.md",
            "task-0145-01",
        ),
        "docs/98.archive/04.execution/plans/2026-06-01-agent-governance-phase2-alignment.md": (
            "docs/98.archive/changes/chg-0146-agent-governance-phase2-alignment/plan.md",
            "plan-0146",
        ),
        "docs/98.archive/04.execution/tasks/2026-06-01-agent-governance-phase3-implementation.md": (
            "docs/98.archive/changes/chg-0147-agent-governance-phase3-implementation/task.md",
            "task-0147-01",
        ),
        "docs/98.archive/04.execution/tasks/2026-06-01-agent-governance-phase3-stage01-02-continuation.md": (
            "docs/98.archive/changes/chg-0148-agent-governance-phase3-stage01-02-continuation/task.md",
            "task-0148-01",
        ),
        "docs/98.archive/04.execution/tasks/2026-06-01-agent-governance-phase3-strategy-integration.md": (
            "docs/98.archive/changes/chg-0149-agent-governance-phase3-strategy-integration/task.md",
            "task-0149-01",
        ),
        "docs/98.archive/04.execution/tasks/2026-06-01-agent-governance-phase4-closure.md": (
            "docs/98.archive/changes/chg-0150-agent-governance-phase4-closure/task.md",
            "task-0150-01",
        ),
        "docs/98.archive/04.execution/tasks/2026-06-01-agent-governance-stage01-02-alignment.md": (
            "docs/98.archive/changes/chg-0151-agent-governance-stage01-02-alignment/task.md",
            "task-0151-01",
        ),
    }

    def setUp(self) -> None:
        self.payload = task7_ledger_payload()
        self.baseline = self.payload["records"]
        self.extension = self.payload["post_baseline_records"]
        self.rows = task7_rows(self.payload)

    def test_extension_is_exact_without_mutating_the_baseline_contract(self) -> None:
        self.assertEqual(796, len(self.baseline))
        self.assertEqual(3, len(self.extension))
        self.assertEqual(
            self.EXTENSION,
            tuple(
                (
                    row["legacy_path"],
                    row["stable_path"],
                    row["artifact_id"],
                    row["action"],
                    row["source_commit"],
                )
                for row in self.extension
            ),
        )
        for row in [*self.baseline, *self.extension]:
            self.assertEqual(self.ROW_FIELDS, set(row))
        self.assertEqual(
            [row["legacy_path"] for row in self.extension],
            sorted(row["legacy_path"] for row in self.extension),
        )

    def test_task7_union_has_unique_sources_targets_and_artifact_ids(self) -> None:
        self.assertEqual(169, len(self.rows))
        for key in ("legacy_path", "stable_path", "artifact_id"):
            values = [row[key] for row in self.rows if row[key] is not None]
            self.assertEqual(len(values), len(set(values)), key)
        self.assertEqual(
            {"move": 75, "archive": 38, "rewrite": 40, "delete": 16},
            dict(collections.Counter(row["action"] for row in self.rows)),
        )

    def test_task7_targets_are_globally_typed_and_collision_free(self) -> None:
        targets = [row["stable_path"] for row in self.rows if row["stable_path"]]
        self.assertEqual([], [target for target in targets if not is_typed_task7_target(target)])
        extension_targets = {
            str(row["stable_path"]): str(row["artifact_id"])
            for row in self.extension
        }
        self.assertEqual(
            extension_targets,
            {
                target: str(metadata.parse_frontmatter(ROOT / target).get("artifact_id"))
                for target in extension_targets
                if (ROOT / target).is_file()
            },
        )

    def test_task7_source_commits_resolve_every_legacy_path_to_a_blob(self) -> None:
        object_names = [
            f"{row['source_commit']}:{row['legacy_path']}" for row in self.rows
        ]
        result = subprocess.run(
            ["git", "cat-file", "--batch-check"],
            cwd=ROOT,
            input="\n".join(object_names) + "\n",
            text=True,
            capture_output=True,
            check=True,
        )
        results = result.stdout.splitlines()
        self.assertEqual(len(object_names), len(results))
        failures = [
            f"{object_name} -> {resolved}"
            for object_name, resolved in zip(object_names, results, strict=True)
            if not re.fullmatch(r"[0-9a-f]{40} blob [0-9]+", resolved)
        ]
        self.assertEqual([], failures)

    def test_operations_tombstone_repair_owns_ref_0086_through_ref_0094(self) -> None:
        operations = [
            row
            for row in self.rows
            if str(row["legacy_path"]).startswith("docs/98.archive/05.operations/")
        ]
        self.assertEqual(
            [f"ref-{number:04d}" for number in range(86, 95)],
            [row["artifact_id"] for row in operations],
        )
        self.assertEqual(
            [f"ref-{number:04d}-" for number in range(86, 95)],
            [pathlib.PurePosixPath(str(row["stable_path"])).name[:9] for row in operations],
        )

    def test_change_packet_repair_uses_the_exact_next_free_namespace(self) -> None:
        by_source = {row["legacy_path"]: row for row in self.rows}
        self.assertEqual(
            self.CHANGE_PACKET_REPAIR,
            {
                source: (by_source[source]["stable_path"], by_source[source]["artifact_id"])
                for source in self.CHANGE_PACKET_REPAIR
            },
        )

    def test_same_initiative_plan_and_task_are_co_located(self) -> None:
        by_source = {row["legacy_path"]: row for row in self.rows}
        for slug, plan_source, task_source, packet in (
            (
                "standardizing-agent-governance",
                "docs/98.archive/04.execution/plans/2026-05-30-standardizing-agent-governance.md",
                "docs/98.archive/04.execution/tasks/2026-05-30-standardizing-agent-governance.md",
                "chg-0144-standardizing-agent-governance",
            ),
            (
                "agent-governance-phase1-diagnostic",
                "docs/98.archive/04.execution/plans/2026-06-01-agent-governance-phase1-diagnostic.md",
                "docs/98.archive/04.execution/tasks/2026-06-01-agent-governance-phase1-diagnostic.md",
                "chg-0145-agent-governance-phase1-diagnostic",
            ),
        ):
            with self.subTest(slug=slug):
                parents = {
                    pathlib.PurePosixPath(str(by_source[source]["stable_path"])).parent.name
                    for source in (plan_source, task_source)
                }
                self.assertEqual({packet}, parents)

    def test_change_packet_and_artifact_identities_are_globally_unique(self) -> None:
        packet_ids: list[str] = []
        artifact_ids: list[str] = []
        for packet in sorted((ROOT / "docs/98.archive/changes").glob("chg-*")):
            match = re.match(r"chg-(\d{4})-", packet.name)
            if match:
                packet_ids.append(match.group(1))
            for document in sorted(packet.glob("*.md")):
                value = metadata.parse_frontmatter(document).get("artifact_id")
                if isinstance(value, str):
                    artifact_ids.append(value)
        expected_ids = [artifact_id for _, artifact_id in self.CHANGE_PACKET_REPAIR.values()]
        self.assertEqual(len(packet_ids), len(set(packet_ids)))
        self.assertEqual(len(artifact_ids), len(set(artifact_ids)))
        self.assertLessEqual(set(expected_ids), set(artifact_ids))


class Task7CorpusConvergenceTests(unittest.TestCase):
    DATE_COMPONENT = re.compile(r"^\d{4}-\d{2}-\d{2}(?:-|$)")
    YEAR_COMPONENT = re.compile(r"^\d{4}$")
    DATE_VALUE_FIELDS = {
        "created",
        "updated",
        "observed_at",
        "completed_at",
        "released_at",
        "occurred_at",
        "archived_at",
    }
    PACK_INDEX_ROLES = {
        "docs/90.references/audits/0001-readme/README.md": "audit",
        "docs/90.references/audits/0012-readme/README.md": "audit",
        "docs/90.references/audits/0019-readme/README.md": "audit",
        "docs/90.references/audits/0033-readme/README.md": "audit",
        "docs/90.references/research/ref-0039-readme.md": "reference",
    }

    def setUp(self) -> None:
        self.payload = task7_ledger_payload()
        self.rows = task7_rows(self.payload)

    def test_task7_executes_every_frozen_disposition(self) -> None:
        failures: list[str] = []
        for row in self.rows:
            source = ROOT / str(row["legacy_path"])
            target_value = row["stable_path"]
            action = row["action"]
            if action == "delete":
                if source.exists():
                    failures.append(f"delete-source-present:{row['legacy_path']}")
                continue
            if not isinstance(target_value, str):
                failures.append(f"target-invalid:{row['legacy_path']}")
                continue
            target = ROOT / target_value
            if not target.is_file():
                failures.append(f"target-missing:{target_value}")
            if source != target and source.exists():
                failures.append(f"source-present:{row['legacy_path']}")
        self.assertEqual([], failures)

    def test_stage90_and_stage98_have_no_date_identity_or_root_archive(self) -> None:
        result = subprocess.run(
            ["git", "ls-files", "--", "docs/90.references", "docs/98.archive", "archive"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        tracked = result.stdout.splitlines()
        dated = [
            path
            for path in tracked
            if any(
                self.YEAR_COMPONENT.fullmatch(component)
                or self.DATE_COMPONENT.match(component)
                for component in pathlib.PurePosixPath(path).parts
            )
        ]
        root_archive = [path for path in tracked if path.startswith("archive/")]
        self.assertEqual([], dated)
        self.assertEqual([], root_archive)
        self.assertFalse((ROOT / "archive").exists())

    def test_identity_dates_move_to_typed_frontmatter(self) -> None:
        failures: list[str] = []
        for row in self.rows:
            legacy = str(row["legacy_path"])
            dates = set(re.findall(r"\d{4}-\d{2}-\d{2}", legacy))
            target_value = row["stable_path"]
            if not dates or not isinstance(target_value, str):
                continue
            target = ROOT / target_value
            if not target.is_file():
                failures.append(f"target-missing:{target_value}")
                continue
            values = metadata.parse_frontmatter(target)
            serialized_dates = {
                value[:10] if isinstance(value, str) else value.isoformat()[:10]
                for key, value in values.items()
                if key in self.DATE_VALUE_FIELDS
                and isinstance(value, (str, datetime.date, datetime.datetime))
            }
            if not dates <= serialized_dates:
                failures.append(
                    f"date-missing:{target_value}:{','.join(sorted(dates - serialized_dates))}"
                )
        self.assertEqual([], failures)

    def test_every_tombstone_has_exact_git_provenance(self) -> None:
        inventory = archive_authority.load_archive(ROOT / "docs/98.archive")
        rows = tuple(item.recovery for item in inventory.tombstones)
        self.assertEqual(38, len(rows))
        self.assertTrue(all(item.is_minimal for item in inventory.tombstones))
        self.assertEqual((), archive_authority.validate_recovery_rows(rows, ROOT))

    def test_check_recovery_mode_uses_minimal_archive_authority(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "scripts/validation/check-document-corpus-lifecycle.py",
                "--mode",
                "check-recovery",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("migrations=3", result.stdout)
        self.assertIn("tombstones=38", result.stdout)
        self.assertIn("decisions=184", result.stdout)
        self.assertIn("recovery_rows=272 violations=0", result.stdout)

    def test_current_links_resolve_without_active_archive_consumers(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "scripts/validation/check-document-links.py",
                "--mode",
                "alignment",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("archive_direct_links_total=0", result.stdout)
        self.assertIn("failures=0", result.stdout)

    def test_renamed_pack_indexes_use_their_typed_leaf_body_contracts(self) -> None:
        profiles = metadata.load_profiles(PROFILES)
        for relative, role_name in self.PACK_INDEX_ROLES.items():
            with self.subTest(path=relative):
                text = (ROOT / relative).read_text(encoding="utf-8")
                record = metadata._record_from_text(
                    pathlib.Path(relative),
                    text,
                    profiles=profiles,
                )
                self.assertEqual(role_name, record.artifact_type)
                h1, h2 = metadata.extract_markdown_headings(text)
                expected_h2 = [
                    "## Overview",
                    "## Purpose",
                    "## Repository Role",
                    "## Scope",
                    "## Definitions / Facts",
                    "## Sources",
                    "## Maintenance",
                    "## Related Documents",
                ]
                self.assertEqual(1, len(h1))
                self.assertTrue(h1[0].startswith("# Reference: "), h1[0])
                self.assertEqual(expected_h2, h2)
                codes = {
                    finding.code
                    for finding in metadata.validate_body_contract(
                        record,
                        text,
                        profiles,
                        changed_boundary=True,
                    )
                }
                self.assertNotIn("body-heading-missing", codes)
                self.assertNotIn("body-heading-forbidden", codes)
                self.assertNotIn("template-instruction-in-target", codes)

    def test_immutable_target_surface_evidence_is_not_blindly_translated(self) -> None:
        manifest_path = (
            ROOT
            / "docs/90.references/data/0069-target-surface-convergence/data.yaml"
        )
        summary_path = (
            ROOT
            / "docs/90.references/data/0068-target-surface-convergence-summary/README.md"
        )
        self.assertTrue(manifest_path.is_file())
        self.assertTrue(summary_path.is_file())
        document = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
        windows = next(
            row
            for row in document["entries"]
            if row["source_path"] == "archive/Windows-Network-IP.md"
        )
        self.assertEqual("archive/Windows-Network-IP.md", windows["target_path"])
        self.assertEqual("preserve", windows["disposition"])
        self.assertIn(
            "| archive/Windows-Network-IP.md | archive/Windows-Network-IP.md | preserve |",
            summary_path.read_text(encoding="utf-8"),
        )


class CoLocatedExecutionTests(unittest.TestCase):
    TASK5_LINK_CONSUMERS = (
        ROOT / "_workspace/README.md",
        ROOT / "_workspace/repo-support/README.md",
        ROOT / "archive/Windows-Network-IP.md",
        ROOT / "examples/sample-web-service/service.md",
        ROOT
        / "docs/05.operations/catalog/00-workspace/0006-infrastructure-optimization-governance/policy.md",
    )

    def test_all_capability_directories_use_stable_identity(self) -> None:
        packages = load_spec_packages(ROOT / "docs/03.specs")
        self.assertEqual(34, len(packages))
        self.assertTrue(
            all(re.fullmatch(r"\d{4}-[a-z0-9]+(?:-[a-z0-9]+)*", package.path.name)
                for package in packages)
        )

    def test_registered_package_readme_exception_is_exact(self) -> None:
        readmes = sorted((ROOT / "docs/03.specs").glob("[0-9][0-9][0-9][0-9]-*/README.md"))
        self.assertEqual(
            [
                ROOT
                / "docs/03.specs/0153-workspace-governance-simplification/README.md"
            ],
            readmes,
        )

    def test_stage_04_is_absent(self) -> None:
        self.assertFalse((ROOT / "docs/04.execution").exists())

    def test_task5_moved_documents_publish_no_broken_relative_links(self) -> None:
        documents = sorted((ROOT / "docs/98.archive/changes").glob("chg-*/*.md"))
        documents.extend(path for path in self.TASK5_LINK_CONSUMERS if path.is_file())
        link_pattern = re.compile(r"(?<!!)(?<!\\)\[[^\]\n]+\]\(([^)\n]+)\)")
        violations: list[str] = []
        for document in documents:
            in_fence = False
            for line_number, line in enumerate(
                document.read_text(encoding="utf-8").splitlines(), start=1
            ):
                stripped = line.lstrip()
                if stripped.startswith(("```", "~~~")):
                    in_fence = not in_fence
                    continue
                if in_fence:
                    continue
                for match in link_pattern.finditer(line):
                    raw = match.group(1).strip()
                    href = (
                        raw[1 : raw.index(">")] if raw.startswith("<") and ">" in raw
                        else raw.split()[0]
                    )
                    if (
                        not href
                        or href.startswith("#")
                        or re.match(r"^[a-z][a-z0-9+.-]*:", href, flags=re.I)
                    ):
                        continue
                    target = (document.parent / href.split("#", 1)[0]).resolve()
                    try:
                        target.relative_to(ROOT.resolve())
                    except ValueError:
                        violations.append(f"{document.relative_to(ROOT)}:{line_number}: {href}")
                        continue
                    if not target.exists():
                        violations.append(f"{document.relative_to(ROOT)}:{line_number}: {href}")
        self.assertEqual([], violations)

    def test_active_change_uses_only_canonical_role_names(self) -> None:
        for capability in sorted(
            (ROOT / "docs/03.specs").glob("[0-9][0-9][0-9][0-9]-*")
        ):
            with self.subTest(capability=capability.name):
                self.assertFalse((capability / "design.md").exists())
                self.assertFalse((capability / "tests.md").exists())
                self.assertFalse((capability / "task.md").exists())
                task_paths = sorted((capability / "tasks").glob("*.md"))
                self.assertTrue(
                    all(
                        re.fullmatch(
                            r"tsk-\d{4}-[a-z0-9]+(?:-[a-z0-9]+)*\.md",
                            task.name,
                        )
                        for task in task_paths
                    )
                )

    def test_task7_promoted_reconciliation_is_exactly_bounded(self) -> None:
        profiles = metadata.load_profiles(PROFILES)
        contract = lifecycle.load_migration_contract(CONTRACT)
        _, findings = lifecycle._load_declared_manifests(
            ROOT,
            profiles,
            contract,
            promoted_only=True,
        )
        task7_sources = set(lifecycle._task7_migration_rows(ROOT))
        task7_residual = [
            finding
            for finding in findings
            if finding.path in task7_sources
            and finding.code
            in {"manifest-target-missing", "manifest-transition-invalid"}
        ]
        self.assertEqual([], task7_residual)
        self.assertEqual(
            {
                "manifest-consumer-evidence-mismatch": 23,
                "manifest-target-missing": 21,
                "manifest-target-parent-ids-mismatch": 1,
                "manifest-target-profile-invalid": 1,
                "manifest-target-status-mismatch": 1,
            },
            dict(collections.Counter(finding.code for finding in findings)),
        )

    def test_task7_reconciliation_requires_exact_ledger_and_current_topology(self) -> None:
        contract = lifecycle.load_migration_contract(CONTRACT)
        rows = lifecycle._task7_migration_rows(ROOT)
        self.assertEqual(169, len(rows))
        self.assertEqual(
            {"archive": 38, "delete": 16, "move": 75, "rewrite": 40},
            dict(collections.Counter(row["action"] for row in rows.values())),
        )
        self.assertTrue(lifecycle._task7_reconciliation_ready(ROOT, contract))

        incomplete = dict(rows)
        incomplete.pop(next(iter(incomplete)))
        with mock.patch.object(
            lifecycle, "_task7_migration_rows", return_value=incomplete
        ):
            self.assertFalse(lifecycle._task7_reconciliation_ready(ROOT, contract))

    def test_task7_consumer_reconciliation_rejects_unrelated_drift(self) -> None:
        document = lifecycle.load_migration_manifest(
            ROOT
            / "docs/90.references/data/0069-target-surface-convergence/data.yaml"
        )
        rows = lifecycle._task7_migration_rows(ROOT)
        legacy, ledger_row = next(
            (legacy, row)
            for legacy, row in rows.items()
            if isinstance(row.get("stable_path"), str)
            and row["stable_path"] != legacy
        )
        stable = str(ledger_row["stable_path"])
        first = dataclasses.replace(
            document.entries[0],
            active_consumers=(pathlib.PurePosixPath(legacy),),
        )
        candidate = dataclasses.replace(
            document,
            entries=(first, *document.entries[1:]),
        )
        with mock.patch.object(
            lifecycle,
            "_tracked_active_consumers",
            return_value=(pathlib.PurePosixPath(stable),),
        ):
            self.assertTrue(
                lifecycle._task7_consumer_evidence_is_reconciled(
                    ROOT, candidate, first.source_path.as_posix(), rows
                )
            )
        with mock.patch.object(
            lifecycle,
            "_tracked_active_consumers",
            return_value=(
                pathlib.PurePosixPath(stable),
                pathlib.PurePosixPath("docs/unrelated-consumer.md"),
            ),
        ):
            self.assertFalse(
                lifecycle._task7_consumer_evidence_is_reconciled(
                    ROOT, candidate, first.source_path.as_posix(), rows
                )
            )

    def test_task7_reconciliation_requires_exact_registered_immutable_bytes(self) -> None:
        contract = lifecycle.load_migration_contract(CONTRACT)
        document = lifecycle.load_migration_manifest(
            ROOT
            / "docs/90.references/data/0069-target-surface-convergence/data.yaml"
        )
        self.assertTrue(
            lifecycle._task7_registered_manifest_matches(
                ROOT,
                contract,
                document,
                lifecycle.TASK7_IMMUTABLE_MANIFEST,
            )
        )
        self.assertFalse(
            lifecycle._task7_registered_manifest_matches(
                ROOT,
                contract,
                document,
                None,
            )
        )

        first = document.entries[0]
        consumer_drift = dataclasses.replace(
            first,
            active_consumers=tuple(
                sorted(
                    {
                        *first.active_consumers,
                        pathlib.PurePosixPath("docs/unrelated-consumer.md"),
                    }
                )
            ),
        )
        target_drift = dataclasses.replace(
            first,
            target_path=pathlib.PurePosixPath("docs/unrelated-target.md"),
        )
        for mutated in (consumer_drift, target_drift):
            candidate = dataclasses.replace(
                document,
                entries=(mutated, *document.entries[1:]),
            )
            with self.subTest(mutated=mutated):
                self.assertFalse(
                    lifecycle._task7_registered_manifest_matches(
                        ROOT,
                        contract,
                        candidate,
                        lifecycle.TASK7_IMMUTABLE_MANIFEST,
                    )
                )

        original_reader = lifecycle._read_regular_repo_bytes

        def corrupted_reader(
            root: pathlib.Path, relative_path: str, *, require_tracked: bool
        ) -> bytes | None:
            payload = original_reader(
                root, relative_path, require_tracked=require_tracked
            )
            if relative_path == lifecycle.TASK7_IMMUTABLE_MANIFEST and payload is not None:
                return payload + b"\n"
            return payload

        with mock.patch.object(
            lifecycle, "_read_regular_repo_bytes", side_effect=corrupted_reader
        ):
            self.assertFalse(
                lifecycle._task7_registered_manifest_matches(
                    ROOT,
                    contract,
                    document,
                    lifecycle.TASK7_IMMUTABLE_MANIFEST,
                )
            )

        with tempfile.TemporaryDirectory() as directory:
            copied_root = pathlib.Path(directory)
            init_repo(copied_root)
            copied = copied_root / lifecycle.TASK7_IMMUTABLE_MANIFEST
            copied.parent.mkdir(parents=True)
            copied.write_bytes(
                (ROOT / lifecycle.TASK7_IMMUTABLE_MANIFEST).read_bytes()
            )
            commit_all(copied_root, "copy immutable manifest only")
            self.assertFalse(
                lifecycle._task7_registered_manifest_matches(
                    copied_root,
                    contract,
                    document,
                    lifecycle.TASK7_IMMUTABLE_MANIFEST,
                )
            )

    def test_task7_reconciliation_rejects_an_exact_copy_at_a_candidate_path(self) -> None:
        profiles = metadata.load_profiles(PROFILES, CONTRACT)
        contract = lifecycle.load_migration_contract(CONTRACT)
        canonical_relative = lifecycle.TASK7_IMMUTABLE_MANIFEST
        canonical = ROOT / canonical_relative
        document = lifecycle.load_migration_manifest(canonical)
        task7_sources = set(lifecycle._task7_migration_rows(ROOT))

        def task7_reconcilable_findings(
            findings: list[lifecycle.Finding],
        ) -> set[tuple[str, str]]:
            return {
                (finding.path, finding.code)
                for finding in findings
                if finding.path in task7_sources
                or (
                    finding.path == "manifest"
                    and finding.code == "manifest-baseline-commit-invalid"
                )
            }

        raw_task7_findings = task7_reconcilable_findings(
            lifecycle._validate_surface_manifest(
                ROOT,
                profiles,
                contract,
                document,
            )
        )

        canonical_findings = lifecycle.validate_migration_manifest(
            ROOT,
            profiles,
            contract,
            document,
            manifest_path=canonical_relative,
        )
        self.assertFalse(
            any(
                finding.path in task7_sources
                and finding.code
                in {"manifest-target-missing", "manifest-transition-invalid"}
                for finding in canonical_findings
            )
        )

        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            candidate = pathlib.Path(directory) / "ref-0069-copy.yaml"
            candidate.write_bytes(canonical.read_bytes())
            candidate_relative = candidate.relative_to(ROOT).as_posix()
            copied_document = lifecycle.load_migration_manifest(candidate)
            copied_findings = lifecycle.validate_migration_manifest(
                ROOT,
                profiles,
                contract,
                copied_document,
                manifest_path=candidate_relative,
            )
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                return_code = lifecycle.main(
                    (
                        "--root",
                        str(ROOT),
                        "--mode",
                        "check-manifest",
                        "--wave",
                        TARGET_WAVE,
                        "--manifest",
                        candidate_relative,
                    )
                )

        self.assertEqual(1, return_code)
        self.assertIn("manifest-target-missing:", output.getvalue())
        self.assertIn("manifest-transition-invalid:", output.getvalue())

        self.assertEqual(
            raw_task7_findings,
            task7_reconcilable_findings(copied_findings),
        )

        copied_task7 = {
            finding.code
            for finding in copied_findings
            if finding.path in task7_sources
        }
        self.assertIn("manifest-target-missing", copied_task7)
        self.assertIn("manifest-transition-invalid", copied_task7)

        unbound_findings = lifecycle.validate_migration_manifest(
            ROOT,
            profiles,
            contract,
            document,
        )
        self.assertEqual(
            raw_task7_findings,
            task7_reconcilable_findings(unbound_findings),
        )
        unbound_task7 = {
            finding.code
            for finding in unbound_findings
            if finding.path in task7_sources
        }
        self.assertIn("manifest-target-missing", unbound_task7)
        self.assertIn("manifest-transition-invalid", unbound_task7)

    def test_task5_reconciliation_requires_every_exact_ledger_disposition(self) -> None:
        rows = lifecycle._task5_migration_rows(ROOT)
        selected = lifecycle._task5_selected_rows(rows)

        self.assertEqual(337, len(selected))
        self.assertEqual(
            {
                "archive": 28,
                "delete": 38,
                "merge": 8,
                "move": 262,
                "rewrite": 1,
            },
            dict(collections.Counter(row["action"] for row in selected.values())),
        )
        self.assertTrue(lifecycle._task5_dispositions_executed(ROOT, selected))

    def test_task5_reconciliation_requires_a_resolvable_legacy_source_blob(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            init_repo(root)
            legacy = root / "docs/04.execution/plan.md"
            legacy.parent.mkdir(parents=True)
            legacy.write_text("legacy\n", encoding="utf-8")
            non_blob = root / "docs/04.execution/non-blob"
            non_blob.mkdir()
            (non_blob / "child.md").write_text("child\n", encoding="utf-8")
            source_commit = commit_all(root, "record legacy sources")

            legacy.unlink()
            shutil.rmtree(non_blob)
            target = root / "docs/03.specs/spec-0001-example/plan.md"
            target.parent.mkdir(parents=True)
            target.write_text("moved\n", encoding="utf-8")
            destination_commit = commit_all(root, "move disposition target")

            def row(
                source_commit: str,
                legacy_path: str = "docs/04.execution/plan.md",
            ) -> dict[str, dict[str, object]]:
                return {
                    legacy_path: {
                        "action": "move",
                        "stable_path": "docs/03.specs/spec-0001-example/plan.md",
                        "source_commit": source_commit,
                    }
                }

            self.assertFalse(
                lifecycle._task5_dispositions_executed(root, row("0" * 40))
            )
            self.assertFalse(
                lifecycle._task5_dispositions_executed(
                    root,
                    row(destination_commit, "docs/04.execution/missing.md"),
                )
            )
            self.assertFalse(
                lifecycle._task5_dispositions_executed(
                    root,
                    row(source_commit, "docs/04.execution/non-blob"),
                )
            )
            self.assertTrue(lifecycle._task5_dispositions_executed(root, row(source_commit)))

    def test_task5_promoted_reconciliation_stays_disabled_without_source_proof(self) -> None:
        contract = lifecycle.load_migration_contract(CONTRACT)
        rows = lifecycle._task5_migration_rows(ROOT)
        selected = lifecycle._task5_selected_rows(rows)
        corrupted = copy.deepcopy(selected)
        _, first_row = next(iter(corrupted.items()))
        first_row["source_commit"] = "0" * 40

        with mock.patch.object(
            lifecycle, "_task5_migration_rows", return_value=corrupted
        ):
            self.assertFalse(lifecycle._task5_reconciliation_ready(ROOT, contract))

    def test_task5_reconciliation_rejects_a_stale_current_consumer(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            init_repo(root)
            consumer = root / "docs/active.md"
            consumer.parent.mkdir(parents=True)
            consumer.write_text("[stale](missing.md)\n", encoding="utf-8")
            commit_all(root)

            self.assertFalse(lifecycle._task5_current_links_resolve(root))
            (root / "docs/missing.md").write_text("# Target\n", encoding="utf-8")
            commit_all(root, "add target")
            self.assertTrue(lifecycle._task5_current_links_resolve(root))

    def test_task5_promoted_mismatch_is_not_hidden_when_link_proof_fails(self) -> None:
        contract = lifecycle.load_migration_contract(CONTRACT)
        with mock.patch.object(
            lifecycle, "_task5_current_links_resolve", return_value=False
        ):
            self.assertFalse(lifecycle._task5_reconciliation_ready(ROOT, contract))


def run(*args: str, cwd: pathlib.Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args),
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )


def git(root: pathlib.Path, *args: str) -> str:
    result = run("git", *args, cwd=root)
    if result.returncode != 0:
        raise AssertionError(result.stderr)
    return result.stdout.strip()


def init_repo(root: pathlib.Path) -> str:
    git(root, "init", "-q")
    git(root, "config", "user.email", "test@example.invalid")
    git(root, "config", "user.name", "Lifecycle Test")
    return ""


def commit_all(root: pathlib.Path, message: str = "fixture") -> str:
    git(root, "add", ".")
    git(root, "commit", "-q", "-m", message)
    return git(root, "rev-parse", "HEAD")


def archive_command_body_findings(text: str) -> list[str]:
    for line in text.splitlines():
        stripped = line.lstrip()
        parts = stripped.split(maxsplit=1)
        if len(parts) == 2:
            marker = parts[0]
            if marker in {"-", "+", "*"} or (
                marker[-1:] in {".", ")"} and marker[:-1].isdigit()
            ):
                stripped = parts[1].lstrip()
        if stripped and stripped.split(maxsplit=1)[0].casefold() == "netsh":
            return ["stale-command-body"]
    return []


class LifecycleTestCase(unittest.TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.profiles = metadata.load_profiles(PROFILES)
        cls.contract = lifecycle.load_migration_contract(CONTRACT)

    def valid_row(self, **overrides: object) -> lifecycle.MigrationManifestRow:
        values: dict[str, object] = {
            "source_path": pathlib.PurePosixPath("docs/03.specs/source.md"),
            "target_path": pathlib.PurePosixPath("docs/03.specs/source.md"),
            "artifact_id": "spec:source",
            "artifact_type": "spec",
            "status_before": "active",
            "status_after": "active",
            "parent_ids": (),
            "disposition": "preserve",
            "canonical_replacement": None,
            "active_consumers": (),
            "partition_plan": None,
            "preservation_class": None,
            "evidence": lifecycle.ManifestEvidence((), (), (), (), ()),
            "review_verdict": lifecycle.ReviewVerdict("pending", "pending"),
        }
        values.update(overrides)
        return lifecycle.MigrationManifestRow(**values)

    def document(
        self,
        baseline_commit: str,
        *,
        entries: tuple[lifecycle.MigrationManifestRow, ...] | None = None,
        wave: str = "fixture",
        enforcement: str = "advisory",
    ) -> lifecycle.MigrationManifestDocument:
        return lifecycle.MigrationManifestDocument(
            schema_version=1,
            wave=wave,
            baseline_commit=baseline_commit,
            generated_by="check-document-corpus-lifecycle.py",
            enforcement=enforcement,
            entries=entries if entries is not None else (self.valid_row(),),
        )

    def fixture_contract(
        self,
        source_paths: list[str],
        *,
        wave: str = "fixture",
        enforcement: str = "advisory",
        manifest_path: str | None = None,
    ) -> dict[str, object]:
        contract = copy.deepcopy(self.contract)
        contract["waves"] = {
            wave: {
                "enforcement": enforcement,
                "manifest_path": manifest_path,
                "scope_state": "approved",
                "source_paths": source_paths,
                "declared_outputs": [],
            }
        }
        return contract

    def run_isolated_impacted_cli(
        self,
        root: pathlib.Path,
        *,
        base_ref: str,
    ) -> subprocess.CompletedProcess[str]:
        """Run check-impacted without repository-owned wave manifests."""
        contract = copy.deepcopy(self.contract)
        for wave in contract["waves"].values():
            wave["enforcement"] = "advisory"
            wave["manifest_path"] = None
        arguments = [
            "--root",
            str(root),
            "--mode",
            "check-impacted",
            "--base-ref",
            base_ref,
        ]
        stdout = io.StringIO()
        stderr = io.StringIO()
        with (
            mock.patch.object(
                lifecycle,
                "load_migration_contract",
                return_value=contract,
            ),
            mock.patch.object(
                lifecycle.metadata,
                "load_profiles",
                return_value=self.profiles,
            ),
            contextlib.redirect_stdout(stdout),
            contextlib.redirect_stderr(stderr),
        ):
            returncode = lifecycle.main(arguments)
        return subprocess.CompletedProcess(
            [sys.executable, str(SCRIPT), *arguments],
            returncode,
            stdout.getvalue(),
            stderr.getvalue(),
        )


class PublicContractTests(LifecycleTestCase):
    def test_cli_defaults_to_registry_and_keeps_profiles_as_transition_alias(self) -> None:
        parser = lifecycle._parser()
        current = parser.parse_args(["--mode", "check-contract"])
        transitional = parser.parse_args(
            ["--mode", "check-contract", "--profiles", str(PROFILES)]
        )

        self.assertEqual(REGISTRY, current.profiles)
        self.assertEqual(PROFILES, transitional.profiles)

    def test_modes_are_the_exact_fixed_tuple(self) -> None:
        self.assertEqual(
            lifecycle.MODES,
            (
                "check-contract",
                "generate-manifest",
                "check-manifest",
                "check-promoted",
                "generate-summary",
                "check-summary",
                "check-impacted",
                "report-duplicates",
                "report-full",
                "check-full",
                "check-archive",
                "check-directory-budget",
                "generate-archive-ledger",
                "check-archive-ledger",
                "generate-snapshot-manifest",
                "check-snapshot-manifest",
            ),
        )

    def test_public_dataclasses_are_frozen_and_tuple_backed(self) -> None:
        row = self.valid_row()
        with self.assertRaises(dataclasses.FrozenInstanceError):
            row.disposition = "delete"  # type: ignore[misc]
        self.assertIsInstance(row.parent_ids, tuple)
        self.assertIsInstance(row.evidence.commands, tuple)

    def test_manifest_skeleton_public_signature_is_exactly_plan_bound(self) -> None:
        self.assertEqual(
            str(inspect.signature(lifecycle.generate_manifest_skeleton)),
            "(root: 'pathlib.Path', contract: 'dict[str, object]', *, "
            "wave: 'str', baseline_ref: 'str') -> 'MigrationManifestDocument'",
        )

    def test_cli_misuse_returns_two_before_opening_repository_files(self) -> None:
        result = run(
            sys.executable,
            str(SCRIPT),
            "--mode",
            "generate-manifest",
            "--profiles",
            "/missing/profiles.yaml",
            "--contract",
            "/missing/contract.yaml",
            cwd=ROOT,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("--wave", result.stderr)
        self.assertNotIn("configuration-error", result.stderr)

    def test_loader_rejects_unknown_and_missing_manifest_keys(self) -> None:
        valid = lifecycle.render_migration_manifest(
            self.document("a" * 40, entries=(self.valid_row(),))
        )
        loaded = yaml.safe_load(valid)
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "manifest.yaml"
            for mutation in ("unknown-top", "missing-entry"):
                candidate = copy.deepcopy(loaded)
                if mutation == "unknown-top":
                    candidate["unexpected"] = True
                else:
                    del candidate["entries"][0]["status_after"]
                path.write_text(yaml.safe_dump(candidate, sort_keys=False), encoding="utf-8")
                with self.subTest(mutation=mutation), self.assertRaises(lifecycle.ProfileError):
                    lifecycle.load_migration_manifest(path)

    def test_manifest_serialization_is_canonical_deterministic_and_lf_only(self) -> None:
        row = self.valid_row(
            parent_ids=("spec:z", "spec:a"),
            active_consumers=(
                pathlib.PurePosixPath("docs/z.md"),
                pathlib.PurePosixPath("docs/a.md"),
            ),
            evidence=lifecycle.ManifestEvidence(
                ("z", "a"),
                ("z", "a"),
                (pathlib.PurePosixPath("docs/z.md"), pathlib.PurePosixPath("docs/a.md")),
                ("z", "a"),
                ("z", "a"),
            ),
        )
        rendered = lifecycle.render_migration_manifest(
            self.document("a" * 40, entries=(row,))
        )
        self.assertTrue(rendered.endswith("\n"))
        self.assertNotIn("\r", rendered)
        reloaded = lifecycle.load_migration_manifest(self.write_temp(rendered))
        rerendered = lifecycle.render_migration_manifest(reloaded)
        self.assertEqual(rendered, rerendered)
        self.assertEqual(reloaded.entries[0].parent_ids, ("spec:a", "spec:z"))

    def test_manifest_v2_loader_keeps_v1_and_exposes_surface_transition_fields(self) -> None:
        loaded = yaml.safe_load(
            lifecycle.render_migration_manifest(
                self.document("a" * 40, entries=(self.valid_row(),))
            )
        )
        loaded["schema_version"] = 2
        row = loaded["entries"][0]
        row["artifact_type_before"] = row.pop("artifact_type")
        row["artifact_type_after"] = row["artifact_type_before"]
        row["surface_class"] = "typed-example"
        manifest = lifecycle.load_migration_manifest(
            self.write_temp(yaml.safe_dump(loaded, sort_keys=False))
        )
        self.assertEqual(2, manifest.schema_version)
        self.assertEqual("spec", manifest.entries[0].artifact_type_before)
        self.assertEqual("spec", manifest.entries[0].artifact_type_after)
        self.assertEqual("typed-example", manifest.entries[0].surface_class)

    def write_temp(self, text: str) -> pathlib.Path:
        directory = tempfile.mkdtemp()
        self.addCleanup(lambda: __import__("shutil").rmtree(directory))
        path = pathlib.Path(directory) / "value.yaml"
        path.write_text(text, encoding="utf-8")
        return path


class HumanContractRoutingTests(LifecycleTestCase):
    def test_stage90_routers_match_blocking_foundation_state(self) -> None:
        routers = (
            ROOT / "docs/90.references" / "README.md",
            ROOT / "docs/90.references" / "data/README.md",
            ROOT / "docs/90.references" / "data/governance/README.md",
            ROOT / "docs/90.references"
            / "data/governance/document-corpus-lifecycle/README.md",
        )
        for path in routers:
            text = path.read_text(encoding="utf-8").lower()
            with self.subTest(path=path.relative_to(ROOT).as_posix()):
                self.assertNotIn("reviewed advisory foundation", text)
                self.assertIn("reviewed blocking foundation", text)

    def test_lifecycle_human_owners_are_unique(self) -> None:
        support = ROOT / "docs/99.templates/support"
        texts = {
            path: path.read_text(encoding="utf-8")
            for path in support.glob("*.md")
        }
        expected = {
            "sole human owner for corpus migration": CORPUS_HUMAN_CONTRACT,
            "sole human owner for archive and retention": ARCHIVE_HUMAN_CONTRACT,
        }
        for marker, owner in expected.items():
            with self.subTest(marker=marker):
                self.assertEqual(
                    [owner],
                    [path for path, text in texts.items() if marker in text],
                )

    def test_corpus_contract_owns_reviewed_evidence_and_confidentiality_semantics(
        self,
    ) -> None:
        contract = CORPUS_HUMAN_CONTRACT.read_text(encoding="utf-8")
        for required in (
            "enforcement is `blocking` or either",
            "row source, the Foundation",
            "empty list only when the immutable range proves an unchanged",
            "`commands`, `sources`, `repository_paths`, `consumer_scan`, and `rollback`",
            "Findings remain value-free and never echo rejected data",
        ):
            with self.subTest(required=required):
                self.assertIn(required, contract)

    def test_template_governance_routes_algorithms_to_human_owners(self) -> None:
        path = ROOT / "docs/99.templates/support/template-governance.md"
        text = path.read_text(encoding="utf-8")
        self.assertIn("corpus-migration-contract.md", text)
        self.assertIn("archive-retention-contract.md", text)
        for copied_algorithm_literal in (
            "`active-canonical`",
            "`historical-archive`",
            "`duplicate-remove`",
            "`conflict-remove-or-archive`",
            "`evidence-preserve`",
            "record replacement or `N/A`",
        ):
            with self.subTest(literal=copied_algorithm_literal):
                self.assertNotIn(copied_algorithm_literal, text)
        for approval_boundary in (
            "approved scope",
            "exact paths",
            "validation commands",
            "rollback or recovery",
            "redaction boundary",
            "independent specification",
            "quality review",
        ):
            with self.subTest(boundary=approval_boundary):
                self.assertIn(approval_boundary, text)

    def test_non_owner_support_contracts_do_not_publish_legacy_dispositions(self) -> None:
        support = ROOT / "docs/99.templates/support"
        owners = {CORPUS_HUMAN_CONTRACT, ARCHIVE_HUMAN_CONTRACT}
        legacy_literals = (
            "`active-canonical`",
            "`historical-archive`",
            "`duplicate-remove`",
            "`conflict-remove-or-archive`",
            "`evidence-preserve`",
        )
        for path in support.glob("*.md"):
            if path in owners:
                continue
            text = path.read_text(encoding="utf-8")
            for literal in legacy_literals:
                with self.subTest(path=path.name, literal=literal):
                    self.assertNotIn(literal, text)

    def test_support_catalog_roles_match_canonical_owner_boundaries(self) -> None:
        catalog = (ROOT / "docs/99.templates/support/README.md").read_text(
            encoding="utf-8"
        )
        for role_description in (
            "Owns only template-change workflow, protected surfaces, migration/archive approval boundaries, and commit boundaries; disposition semantics route to the sole human owners.",
            "Owns only the human lifecycle status vocabulary and interpretation boundary; disposition/archive semantics route to the sole human owners, and transition semantics route to the metadata registry and checker.",
        ):
            with self.subTest(role=role_description):
                self.assertIn(role_description, catalog)
        for owner_route in (
            "[corpus-migration-contract.md](./corpus-migration-contract.md)",
            "[archive-retention-contract.md](./archive-retention-contract.md)",
            "[document-metadata-profiles.yaml](./document-metadata-profiles.yaml)",
        ):
            with self.subTest(owner=owner_route):
                self.assertIn(owner_route, catalog)
        for stale_role in (
            "archive/remove dispositions",
            "lifecycle status values, transition rules",
        ):
            self.assertNotIn(stale_role, catalog)

    def test_docs_parent_router_matches_stage98_contract(self) -> None:
        parent = (ROOT / "docs/README.md").read_text(encoding="utf-8")
        for required_route in (
            "manifest-first validated tombstone result",
            "full typed provenance and preservation",
            "`current_replacement` is disposition-conditional",
            "safe provenance",
            "confidentiality",
            "preservation",
            "rollback",
            "independent specification and quality review",
            "[corpus migration contract](99.templates/support/corpus-migration-contract.md)",
            "[archive and retention contract](99.templates/support/archive-retention-contract.md)",
        ):
            with self.subTest(route=required_route):
                self.assertIn(required_route, parent)
        for stale_stage98_route in (
            "active chain에서 제거된 old 문서 tombstone",
            "trace removed old documents",
            "original path/date/title/replacement 원문 보존",
            "오래된 문서를 archive/reference로 옮기거나 삭제하려면",
            "현재 구현과 상충하는 whole-document old 문서",
        ):
            with self.subTest(stale=stale_stage98_route):
                self.assertNotIn(stale_stage98_route, parent)

    def test_stage00_and_stage98_route_without_redefining_semantics(self) -> None:
        archive_readme = (ROOT / "docs/98.archive/README.md").read_text(
            encoding="utf-8"
        )
        for literal in (
            "hand-maintained",
            "non-authoritative compatibility section",
            "archive-retention-contract.md",
            "corpus-migration-contract.md",
            "authoritative `mig-0001` ledger",
            "`archived_at`",
        ):
            self.assertIn(literal, archive_readme)
        for contradictory_synopsis in (
            "현재 구현과 상충",
            "원래 문서 경로, archive 사유, 현재 대체 문서만",
            "원래 경로와 대체 문서 추적",
        ):
            self.assertNotIn(contradictory_synopsis, archive_readme)

        stage00_paths = (
            ROOT / "docs/00.agent-governance/policies/documentation-protocol.md",
            ROOT / "docs/00.agent-governance/policies/stage-authoring-matrix.md",
            ROOT / "docs/00.agent-governance/policies/task-checklists.md",
        )
        combined = "\n".join(path.read_text(encoding="utf-8") for path in stage00_paths)
        for literal in (
            "corpus-migration-contract.md",
            "archive-retention-contract.md",
            "manifest-first",
            "safe provenance",
            "independent specification and quality review",
            "canonical generator",
            "controlled-wrapper evidence",
        ):
            with self.subTest(literal=literal):
                self.assertIn(literal, combined)

    def test_approved_external_sources_are_local_consequences_only(self) -> None:
        rationale = (
            ROOT / "docs/99.templates/support/external-source-rationale.md"
        ).read_text(encoding="utf-8")
        for source in (
            "https://yaml.org/spec/1.2.2/",
            "https://docs.github.com/en/contributing/writing-for-github-docs/using-yaml-frontmatter",
            "https://spec.commonmark.org/0.31.2/",
            "https://github.github.com/gfm/",
            "https://diataxis.fr/",
            "https://swehb.nasa.gov/spaces/7150/pages/16450285/SWE-052%2B-%2BBidirectional%2BTraceability%2BBetween%2BHigher%2BLevel%2BRequirements%2Band%2BSoftware%2BRequirements",
            "https://adr.github.io/madr/",
            "https://github.com/github/spec-kit",
            "https://sre.google/workbook/postmortem-culture/",
            "https://www.w3.org/TR/prov-o/",
            "https://git-scm.com/docs/git-log",
            "https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax",
            "https://pre-commit.com/",
        ):
            with self.subTest(source=source):
                self.assertIn(source, rationale)
        self.assertIn("repository-local decisions", rationale)
        self.assertIn("do not define repository approval authority", rationale)

    def test_human_contracts_route_v2_surfaces_and_archive_split(self) -> None:
        corpus = CORPUS_HUMAN_CONTRACT.read_text(encoding="utf-8")
        archive = ARCHIVE_HUMAN_CONTRACT.read_text(encoding="utf-8")
        for literal in (
            "schema version 2",
            "`artifact_type_before`",
            "`artifact_type_after`",
            "`surface_class`",
            "source roots",
            "direct source paths",
        ):
            with self.subTest(owner="corpus", literal=literal):
                self.assertIn(literal, corpus)
        for literal in (
            "`docs/98.archive` is the sole documentation archive",
            "### `change-plan`",
            "### `change-task`",
            "### `tombstone`",
            "### `migration`",
            "retired top-level",
            "all current archive records remain beneath\n`docs/98.archive`",
        ):
            with self.subTest(owner="archive", literal=literal):
                self.assertIn(literal, archive)

    def test_human_contract_separates_v1_and_v2_entry_fields_and_domains(self) -> None:
        corpus = CORPUS_HUMAN_CONTRACT.read_text(encoding="utf-8")
        for literal in (
            "Schema version 1 entries use",
            "Schema version 2 entries instead use",
            "Field domains are schema-specific",
        ):
            with self.subTest(literal=literal):
                self.assertIn(literal, corpus)
        self.assertNotIn(
            "Each entry uses `source_path`, `target_path`, `artifact_id`, `artifact_type`",
            corpus,
        )

    def test_human_contract_separates_v2_baseline_and_target_metadata_truth(self) -> None:
        corpus = CORPUS_HUMAN_CONTRACT.read_text(encoding="utf-8")
        for literal in (
            "pinned baseline",
            "`artifact_type_before` and `status_before`",
            "`artifact_id`, `artifact_type_after`, `status_after`, and `parent_ids`",
            "current canonical target metadata",
            "non-document surfaces",
        ):
            with self.subTest(literal=literal):
                self.assertIn(literal, corpus)

    def test_v2_native_replacement_contract_keeps_native_bodies_opaque(self) -> None:
        machine_contract = " ".join(CONTRACT.read_text(encoding="utf-8").split())
        human_contract = " ".join(
            CORPUS_HUMAN_CONTRACT.read_text(encoding="utf-8").split()
        )
        for literal in (
            "schema-v2 native runtime/configuration replacement",
            "selected manifest row",
            "tracked regular current result",
        ):
            with self.subTest(owner="machine", literal=literal):
                self.assertIn(literal, machine_contract)
        for literal in (
            "Schema version 2 native `runtime` and `configuration` replacements",
            "same selected manifest",
            "without reading or decoding the native body",
        ):
            with self.subTest(owner="human", literal=literal):
                self.assertIn(literal, human_contract)


class ManifestValidationTests(LifecycleTestCase):
    def target_manifest(self) -> lifecycle.MigrationManifestDocument:
        return lifecycle.load_migration_manifest(
            ROOT
            / "docs/90.references/data/0069-target-surface-convergence/data.yaml"
        )

    def target_row(
        self,
        document: lifecycle.MigrationManifestDocument,
        source_path: str,
    ) -> lifecycle.MigrationManifestRow:
        return next(
            row
            for row in document.entries
            if row.source_path.as_posix() == source_path
        )

    def target_codes(
        self,
        document: lifecycle.MigrationManifestDocument,
    ) -> set[str]:
        return {
            finding.code
            for finding in lifecycle.validate_migration_manifest(
                ROOT,
                self.profiles,
                self.contract,
                document,
            )
        }

    def replace_target_row(
        self,
        document: lifecycle.MigrationManifestDocument,
        replacement: lifecycle.MigrationManifestRow,
    ) -> lifecycle.MigrationManifestDocument:
        source = replacement.source_path
        return dataclasses.replace(
            document,
            entries=tuple(
                replacement if row.source_path == source else row
                for row in document.entries
            ),
        )

    def target_codes_with_result_payload(
        self,
        document: lifecycle.MigrationManifestDocument,
        target_path: str,
        payload: bytes | None,
    ) -> set[str]:
        original_read = lifecycle._read_regular_repo_bytes

        def read_result(
            root: pathlib.Path,
            relative_path: str,
            *,
            require_tracked: bool,
        ) -> bytes | None:
            if relative_path == target_path and not require_tracked:
                return payload
            return original_read(
                root,
                relative_path,
                require_tracked=require_tracked,
            )

        with mock.patch.object(
            lifecycle,
            "_read_regular_repo_bytes",
            side_effect=read_result,
        ):
            return self.target_codes(document)

    def target_codes_with_successor_payload(
        self,
        document: lifecycle.MigrationManifestDocument,
        payload: bytes | None,
    ) -> set[str]:
        delta = lifecycle._ensure_target_surface_delta_loaded()
        original_read = delta._read_contract_text

        def read_result(
            root: pathlib.Path,
            relative_path: str,
        ) -> str:
            if relative_path == SUCCESSOR_MANIFEST:
                if payload is None:
                    raise delta.ContractInputError
                try:
                    return payload.decode("utf-8")
                except UnicodeDecodeError:
                    raise delta.ContractInputError from None
            return original_read(root, relative_path)

        with mock.patch.object(
            delta,
            "_read_contract_text",
            side_effect=read_result,
        ):
            return self.target_codes(document)

    def make_repo(self) -> tuple[tempfile.TemporaryDirectory[str], pathlib.Path, str]:
        temporary = tempfile.TemporaryDirectory()
        root = pathlib.Path(temporary.name)
        init_repo(root)
        source = root / "docs/03.specs/source.md"
        source.parent.mkdir(parents=True)
        source.write_text(
            "---\nstatus: active\nartifact_id: spec:source\nartifact_type: spec\nparent_ids: []\n---\n\n# Source\n",
            encoding="utf-8",
        )
        baseline = commit_all(root)
        return temporary, root, baseline

    def validate(
        self,
        root: pathlib.Path,
        baseline: str,
        entries: tuple[lifecycle.MigrationManifestRow, ...],
        *,
        enforcement: str = "advisory",
    ) -> set[str]:
        document = self.document(
            baseline,
            entries=entries,
            enforcement=enforcement,
        )
        contract = self.fixture_contract(["docs/03.specs/source.md"])
        return {
            finding.code
            for finding in lifecycle.validate_migration_manifest(
                root, self.profiles, contract, document
            )
        }

    def test_skeleton_has_one_pending_semantically_empty_row_per_baseline_path(self) -> None:
        temporary, root, baseline = self.make_repo()
        self.addCleanup(temporary.cleanup)
        contract = self.fixture_contract(["docs/03.specs/source.md"])
        document = lifecycle.generate_manifest_skeleton(
            root,
            contract,
            wave="fixture",
            baseline_ref=baseline,
        )
        self.assertEqual(document.baseline_commit, baseline)
        self.assertEqual(len(document.entries), 1)
        row = document.entries[0]
        self.assertEqual(row.source_path.as_posix(), "docs/03.specs/source.md")
        self.assertEqual(row.review_verdict, lifecycle.ReviewVerdict("pending", "pending"))
        self.assertEqual(row.parent_ids, ())
        self.assertIsNone(row.canonical_replacement)
        self.assertEqual(row.active_consumers, ())
        self.assertEqual(row.evidence, lifecycle.ManifestEvidence((), (), (), (), ()))
        self.assertIsNone(row.preservation_class)

    def test_public_skeleton_uses_registry_profiles_for_canonical_spec(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = pathlib.Path(temporary.name)
        init_repo(root)
        source = root / "docs/03.specs/0001-example/spec.md"
        source.parent.mkdir(parents=True)
        source.write_text(
            "---\nprofile_id: spec\nstatus: draft\nartifact_id: SPEC-0001\n"
            "artifact_type: spec\nparent_ids: []\ncreated: 2026-08-20\n"
            "updated: 2026-08-20\n---\n\n# Example\n",
            encoding="utf-8",
        )
        baseline = commit_all(root)
        contract = self.fixture_contract([source.relative_to(root).as_posix()])

        document = lifecycle.generate_manifest_skeleton(
            root,
            contract,
            wave="fixture",
            baseline_ref=baseline,
        )

        self.assertEqual(1, len(document.entries))
        self.assertEqual("spec", document.entries[0].artifact_type_before)
        self.assertEqual("spec", document.entries[0].artifact_type_after)

    def test_target_wave_expands_exact_roots_and_direct_paths(self) -> None:
        document = lifecycle._task7_immutable_expected_document(
            ROOT,
            self.contract,
            TARGET_WAVE,
        )
        self.assertIsNotNone(document)
        assert document is not None
        wave = self.contract["waves"][TARGET_WAVE]
        selected = [row.source_path.as_posix() for row in document.entries]
        root_selected = [
            path
            for path in selected
            if path.split("/", 1)[0] in set(wave["source_roots"])
        ]
        self.assertEqual(422, len(root_selected))
        self.assertEqual(
            len(selected),
            422 + len(wave["direct_source_paths"]),
        )
        self.assertEqual(selected, sorted(set(selected)))
        self.assertEqual(TARGET_BASELINE, document.baseline_commit)

        windows = next(
            row
            for row in document.entries
            if row.source_path.as_posix() == "archive/Windows-Network-IP.md"
        )
        self.assertEqual("content-archive", windows.surface_class)
        self.assertIsNone(windows.artifact_type_before)
        self.assertEqual("archive", windows.artifact_type_after)
        self.assertEqual("pass", windows.review_verdict.specification)
        self.assertEqual("pass", windows.review_verdict.quality)

    def test_v2_sample_fixture_successor_owns_current_metadata_truth(self) -> None:
        document = self.target_manifest()
        row = self.target_row(document, SAMPLE_FIXTURE_PATH)
        self.assertIsNone(row.artifact_type_before)
        self.assertEqual("spec", row.artifact_type_after)
        self.assertEqual("spec:sample-web-service", row.artifact_id)
        self.assertEqual(
            ("spec:133-target-surface-contract-convergence",), row.parent_ids
        )
        self.assertTrue(
            SAMPLE_PREDECESSOR_EQUALITY_CODES.isdisjoint(
                self.target_codes(document)
            )
        )

    def test_v2_sample_fixture_handoff_requires_exact_successor_update_row(
        self,
    ) -> None:
        document = self.target_manifest()
        successor = yaml.safe_load((ROOT / SUCCESSOR_MANIFEST).read_text(encoding="utf-8"))
        sample_row = next(
            row for row in successor["entries"] if row["path"] == SAMPLE_FIXTURE_PATH
        )
        sample_row["disposition"] = "preserve"

        cases = {
            "missing-successor": None,
            "preserved-successor-row": yaml.safe_dump(
                successor,
                sort_keys=False,
            ).encode(),
        }
        for name, payload in cases.items():
            with self.subTest(case=name):
                self.assertTrue(
                    SAMPLE_PREDECESSOR_EQUALITY_CODES
                    <= self.target_codes_with_successor_payload(document, payload)
                )

    def test_v2_sample_fixture_handoff_requires_complete_successor_evidence(
        self,
    ) -> None:
        document = self.target_manifest()
        valid = yaml.safe_load(
            (ROOT / SUCCESSOR_MANIFEST).read_text(encoding="utf-8")
        )

        def payload(
            *,
            top_updates: dict[str, object] | None = None,
            top_delete: str | None = None,
            row_updates: dict[str, object] | None = None,
            row_delete: str | None = None,
        ) -> bytes:
            candidate = copy.deepcopy(valid)
            if top_updates:
                candidate.update(top_updates)
            if top_delete:
                candidate.pop(top_delete)
            sample_row = next(
                row
                for row in candidate["entries"]
                if row["path"] == SAMPLE_FIXTURE_PATH
            )
            if row_updates:
                sample_row.update(row_updates)
            if row_delete:
                sample_row.pop(row_delete)
            return yaml.safe_dump(candidate, sort_keys=False).encode()

        cases = {
            "failed-specification-verdict": payload(
                row_updates={"spec_verdict": "fail"}
            ),
            "failed-quality-verdict": payload(
                row_updates={"quality_verdict": "fail"}
            ),
            "wrong-implementation-base": payload(
                top_updates={"implementation_base": "0" * 40}
            ),
            "wrong-enforcement": payload(
                top_updates={"enforcement": "blocking"}
            ),
            "wrong-target-roots": payload(
                top_updates={"target_roots": list(reversed(valid["target_roots"]))}
            ),
            "missing-direct-consumers": payload(
                row_updates={"direct_consumers": []}
            ),
            "wrong-direct-consumers": payload(
                row_updates={"direct_consumers": [SAMPLE_FIXTURE_PATH]}
            ),
            "missing-finding": payload(row_updates={"finding": ""}),
            "wrong-finding": payload(
                row_updates={"finding": "Incomplete sample evidence."}
            ),
            "missing-validators": payload(row_updates={"validators": []}),
            "wrong-validators": payload(
                row_updates={"validators": ["scripts/validation/check-json.py"]}
            ),
            "missing-tests": payload(row_updates={"tests": []}),
            "wrong-tests": payload(
                row_updates={"tests": ["tests/validation/test_json.py"]}
            ),
            "extra-destructive-provenance": payload(
                row_updates={
                    "provenance": [
                        *next(
                            row
                            for row in valid["entries"]
                            if row["path"] == SAMPLE_FIXTURE_PATH
                        )["provenance"],
                        (
                            "git:19ee47270e3897073ab9a3f86dfd4cce0f4b2e74:"
                            f"{SAMPLE_FIXTURE_PATH}"
                        ),
                    ]
                }
            ),
            "extra-destructive-rollback": payload(
                row_updates={
                    "rollback": [
                        *next(
                            row
                            for row in valid["entries"]
                            if row["path"] == SAMPLE_FIXTURE_PATH
                        )["rollback"],
                        (
                            "git-revert:"
                            "63039b5b0b20c99a10aae7162627afefcd7a1d8b:"
                            f"{SAMPLE_FIXTURE_PATH}"
                        ),
                    ]
                }
            ),
            "extra-top-level-key": payload(top_updates={"unexpected": True}),
            "missing-top-level-key": payload(top_delete="implementation_base"),
            "extra-row-key": payload(row_updates={"unexpected": True}),
            "missing-row-key": payload(row_delete="finding"),
        }
        for name, candidate_payload in cases.items():
            with self.subTest(case=name):
                self.assertTrue(
                    SAMPLE_PREDECESSOR_EQUALITY_CODES
                    <= self.target_codes_with_successor_payload(
                        document,
                        candidate_payload,
                    )
                )

    def test_v2_sample_fixture_handoff_accepts_nonfailed_review_states(
        self,
    ) -> None:
        document = self.target_manifest()
        valid = yaml.safe_load(
            (ROOT / SUCCESSOR_MANIFEST).read_text(encoding="utf-8")
        )
        for spec_verdict, quality_verdict in (
            ("pass", "pass"),
            ("pass", "pending"),
            ("pending", "pass"),
        ):
            with self.subTest(
                spec_verdict=spec_verdict,
                quality_verdict=quality_verdict,
            ):
                candidate = copy.deepcopy(valid)
                sample_row = next(
                    row
                    for row in candidate["entries"]
                    if row["path"] == SAMPLE_FIXTURE_PATH
                )
                sample_row["spec_verdict"] = spec_verdict
                sample_row["quality_verdict"] = quality_verdict
                candidate_payload = yaml.safe_dump(
                    candidate,
                    sort_keys=False,
                ).encode()
                self.assertTrue(
                    SAMPLE_PREDECESSOR_EQUALITY_CODES.isdisjoint(
                        self.target_codes_with_successor_payload(
                            document,
                            candidate_payload,
                        )
                    )
                )

    def test_v2_sample_fixture_handoff_rejects_wrong_current_metadata(self) -> None:
        document = self.target_manifest()
        payload = (ROOT / SAMPLE_FIXTURE_PATH).read_text(encoding="utf-8").replace(
            "artifact_id: spec:sample-web-service",
            "artifact_id: spec:wrong-sample-web-service",
            1,
        ).encode()

        self.assertTrue(
            SAMPLE_PREDECESSOR_EQUALITY_CODES
            <= self.target_codes_with_result_payload(
                document,
                SAMPLE_FIXTURE_PATH,
                payload,
            )
        )

    def test_promoted_status_witness_is_bounded_to_exact_blocking_chain(self) -> None:
        document = self.target_manifest()
        path = "docs/03.specs/133-target-surface-contract-convergence/spec.md"
        row = self.target_row(document, path)
        self.assertEqual(("draft", "active"), (row.status_before, row.status_after))
        self.assertEqual(lifecycle.ReviewVerdict("pass", "pass"), row.review_verdict)
        self.assertNotIn("manifest-target-status-mismatch", self.target_codes(document))

        invalid_documents = {
            "advisory": (
                dataclasses.replace(document, enforcement="advisory"),
                "manifest-target-status-mismatch",
            ),
            "pending-review": (
                self.replace_target_row(
                    document,
                    dataclasses.replace(
                        row,
                        review_verdict=lifecycle.ReviewVerdict("pending", "pass"),
                    ),
                ),
                "manifest-target-status-mismatch",
            ),
            "wrong-baseline": (
                dataclasses.replace(document, baseline_commit="0" * 40),
                "manifest-baseline-commit-invalid",
            ),
            "skipped-first-hop": (
                self.replace_target_row(
                    document,
                    dataclasses.replace(row, status_after="completed"),
                ),
                "manifest-transition-invalid",
            ),
        }
        for name, (candidate, expected_code) in invalid_documents.items():
            with self.subTest(case=name):
                self.assertIn(expected_code, self.target_codes(candidate))

        for terminal_status in ("archived", "superseded"):
            with self.subTest(terminal_status=terminal_status):
                payload = (ROOT / path).read_text(encoding="utf-8").replace(
                    "status: completed", f"status: {terminal_status}", 1
                ).encode()
                self.assertIn(
                    "manifest-target-status-mismatch",
                    self.target_codes_with_result_payload(document, path, payload),
                )

        coordinated_row = dataclasses.replace(
            row,
            parent_ids=("spec:coordinated",),
        )
        coordinated_document = self.replace_target_row(document, coordinated_row)
        coordinated_payload = (ROOT / path).read_text(encoding="utf-8").replace(
            "spec:131-document-corpus-lifecycle-migration-foundation",
            "spec:coordinated",
            1,
        ).encode()
        self.assertIn(
            "manifest-target-status-mismatch",
            self.target_codes_with_result_payload(
                coordinated_document,
                path,
                coordinated_payload,
            ),
        )

    def test_v2_migrated_typed_target_rejects_false_current_metadata(self) -> None:
        document = self.target_manifest()
        row = self.target_row(
            document, "examples/sample-web-service/service.md"
        )
        cases = (
            (
                "artifact-id",
                dataclasses.replace(row, artifact_id="spec:false-service"),
                "manifest-target-artifact-id-mismatch",
            ),
            (
                "artifact-type",
                dataclasses.replace(row, artifact_type_after="reference"),
                "manifest-target-artifact-type-mismatch",
            ),
            (
                "artifact-type-null",
                dataclasses.replace(row, artifact_type_after=None),
                "manifest-target-artifact-type-mismatch",
            ),
            (
                "parents",
                dataclasses.replace(row, parent_ids=()),
                "manifest-target-parent-ids-mismatch",
            ),
            (
                "status",
                dataclasses.replace(row, status_after="draft"),
                "manifest-target-status-mismatch",
            ),
        )
        for name, candidate_row, expected_code in cases:
            with self.subTest(case=name):
                candidate = self.replace_target_row(document, candidate_row)
                self.assertIn(expected_code, self.target_codes(candidate))

    def test_v2_migrated_typed_target_requires_canonical_profile_fields(self) -> None:
        document = self.target_manifest()
        row = self.target_row(
            document, "examples/sample-web-service/service.md"
        )
        candidate = self.replace_target_row(
            document,
            dataclasses.replace(row, artifact_id=None, parent_ids=()),
        )
        payload = (
            "---\n"
            "status: active\n"
            "artifact_type: spec\n"
            "---\n\n"
            "# Sample Web Service\n"
        ).encode()

        self.assertIn(
            "manifest-target-profile-invalid",
            self.target_codes_with_result_payload(
                candidate,
                "examples/sample-web-service/service.md",
                payload,
            ),
        )

    def test_v2_migrated_readme_rejects_malformed_frontmatter(self) -> None:
        document = self.target_manifest()
        target = "projects/storybook/README.md"
        malformed = b"---\nstatus: [\n---\n\n# Storybook\n"

        self.assertIn(
            "manifest-target-file-invalid",
            self.target_codes_with_result_payload(document, target, malformed),
        )

    def test_v2_migrated_readme_rejects_profile_forbidden_metadata(self) -> None:
        document = self.target_manifest()
        target = "projects/storybook/README.md"
        forbidden = b"---\nartifact_type: readme\n---\n\n# Storybook\n"

        self.assertIn(
            "manifest-target-profile-invalid",
            self.target_codes_with_result_payload(document, target, forbidden),
        )

    def test_v2_migrated_target_read_failure_is_not_an_empty_document(self) -> None:
        document = self.target_manifest()
        target = "projects/storybook/README.md"

        self.assertIn(
            "manifest-target-file-invalid",
            self.target_codes_with_result_payload(document, target, None),
        )

    def test_v2_non_document_target_metadata_is_rejected_without_body_read(self) -> None:
        document = self.target_manifest()
        target = (
            "infra/05-messaging/kafka/jmx-exporter/"
            "jmx_prometheus_javaagent-1.5.0.jar"
        )
        row = self.target_row(document, target)
        candidate = self.replace_target_row(
            document,
            dataclasses.replace(
                row,
                artifact_type_after="spec",
                disposition="migrate",
            ),
        )
        original_read = lifecycle._read_regular_repo_bytes
        result_reads: list[str] = []

        def observe_read(
            root: pathlib.Path,
            relative_path: str,
            *,
            require_tracked: bool,
        ) -> bytes | None:
            if relative_path == target and not require_tracked:
                result_reads.append(relative_path)
                return b"\xff"
            return original_read(
                root,
                relative_path,
                require_tracked=require_tracked,
            )

        with mock.patch.object(
            lifecycle,
            "_read_regular_repo_bytes",
            side_effect=observe_read,
        ):
            codes = self.target_codes(candidate)

        self.assertIn("manifest-target-metadata-forbidden", codes)
        self.assertEqual([], result_reads)

    def test_v2_delete_rejects_a_source_that_remains_in_the_result(self) -> None:
        document = self.target_manifest()
        source = self.target_row(document, ".env.example")
        destructive = dataclasses.replace(
            source,
            target_path=None,
            artifact_type_after=None,
            disposition="delete",
            preservation_class="git-history",
            evidence=lifecycle.ManifestEvidence(
                ("git diff --name-status 32c40e11747bc0bd03789c24861d2e5d60c0e999..6e87a97977c2de48c1c89a278b159f956825fdd1 -- .env.example",),
                (".env.example",),
                (pathlib.PurePosixPath(".env.example"),),
                ("git grep -l --fixed-strings -- .env.example",),
                ("git revert --no-commit 6e87a97977c2de48c1c89a278b159f956825fdd1",),
            ),
            review_verdict=lifecycle.ReviewVerdict("pass", "pass"),
        )
        candidate = self.replace_target_row(document, destructive)

        self.assertIn("manifest-source-result-present", self.target_codes(candidate))

    def test_v2_rejects_invalid_transition_rollback_and_replacement(self) -> None:
        document = self.target_manifest()
        source = self.target_row(document, ".env.example")
        destructive = dataclasses.replace(
            source,
            target_path=None,
            artifact_type_after=None,
            status_after="draft",
            disposition="delete",
            canonical_replacement="spec:missing-replacement",
            preservation_class="git-history",
            evidence=lifecycle.ManifestEvidence(
                ("git diff --name-status 32c40e11747bc0bd03789c24861d2e5d60c0e999..6e87a97977c2de48c1c89a278b159f956825fdd1 -- .env.example",),
                (".env.example",),
                (pathlib.PurePosixPath(".env.example"),),
                ("git grep -l --fixed-strings -- .env.example",),
                ("git revert --no-commit HEAD",),
            ),
            review_verdict=lifecycle.ReviewVerdict("pass", "pass"),
        )
        codes = self.target_codes(self.replace_target_row(document, destructive))

        self.assertIn("manifest-transition-invalid", codes)
        self.assertIn("manifest-rollback-invalid", codes)
        self.assertIn("manifest-replacement-invalid", codes)

    def test_v2_replacement_resolution_accepts_one_current_path_or_identity(self) -> None:
        expected = "docs/03.specs/133-target-surface-contract-convergence/spec.md"
        for replacement in (
            expected,
            "spec:133-target-surface-contract-convergence",
        ):
            with self.subTest(replacement=replacement):
                record = lifecycle._surface_replacement_record(
                    ROOT, self.profiles, replacement
                )
                self.assertIsNotNone(record)
                self.assertEqual(expected, record.path.as_posix())
        self.assertIsNone(
            lifecycle._surface_replacement_record(
                ROOT, self.profiles, "spec:missing-replacement"
            )
        )

    def test_v2_native_replacement_accepts_selected_current_runtime_without_body_read(
        self,
    ) -> None:
        document = self.target_manifest()
        source_path = "infra/04-data/analytics/influxdb/docker-compose.v2.yml"
        replacement_path = "infra/04-data/analytics/influxdb/docker-compose.yml"
        source = self.target_row(document, source_path)
        destructive = dataclasses.replace(
            source,
            target_path=None,
            disposition="delete",
            canonical_replacement=replacement_path,
        )
        candidate = self.replace_target_row(document, destructive)
        original_read = lifecycle._read_regular_repo_bytes

        def reject_native_body_read(
            root: pathlib.Path,
            relative_path: str,
            *,
            require_tracked: bool,
        ) -> bytes | None:
            if relative_path == replacement_path:
                raise AssertionError("native replacement body must remain opaque")
            return original_read(
                root,
                relative_path,
                require_tracked=require_tracked,
            )

        with (
            mock.patch.object(
                lifecycle,
                "_read_regular_repo_bytes",
                side_effect=reject_native_body_read,
            ),
            mock.patch.object(
                lifecycle.metadata,
                "_record_from_text",
                wraps=lifecycle.metadata._record_from_text,
            ) as record_from_text,
        ):
            findings = lifecycle._surface_replacement_findings(
                ROOT,
                self.profiles,
                candidate,
                destructive,
            )

        self.assertEqual([], findings)
        self.assertEqual([], record_from_text.call_args_list)

    def test_v2_native_replacement_rejects_unsafe_result_mutations(self) -> None:
        document = self.target_manifest()
        source_path = "infra/04-data/analytics/influxdb/docker-compose.v2.yml"
        replacement_path = "infra/04-data/analytics/influxdb/docker-compose.yml"
        source = self.target_row(document, source_path)
        replacement = self.target_row(document, replacement_path)
        env_row = self.target_row(document, ".env.example")
        destructive = dataclasses.replace(
            source,
            target_path=None,
            disposition="delete",
            canonical_replacement=replacement_path,
        )
        base_candidate = self.replace_target_row(document, destructive)
        cases = (
            (
                "missing",
                dataclasses.replace(
                    destructive,
                    canonical_replacement="infra/04-data/analytics/influxdb/missing.yml",
                ),
                base_candidate,
            ),
            (
                "self",
                dataclasses.replace(
                    destructive,
                    canonical_replacement=source_path,
                ),
                base_candidate,
            ),
            (
                "target",
                dataclasses.replace(
                    destructive,
                    target_path=pathlib.PurePosixPath(replacement_path),
                    disposition="archive",
                ),
                base_candidate,
            ),
            (
                "incompatible",
                dataclasses.replace(
                    destructive,
                    canonical_replacement=".env.example",
                ),
                base_candidate,
            ),
            (
                "deleted",
                destructive,
                dataclasses.replace(
                    base_candidate,
                    entries=tuple(
                        dataclasses.replace(
                            row,
                            target_path=None,
                            disposition="delete",
                        )
                        if row.source_path == replacement.source_path
                        else row
                        for row in base_candidate.entries
                    ),
                ),
            ),
            (
                "ambiguous",
                destructive,
                dataclasses.replace(
                    base_candidate,
                    entries=base_candidate.entries + (replacement,),
                ),
            ),
            (
                "forged-class",
                dataclasses.replace(
                    destructive,
                    canonical_replacement=".env.example",
                ),
                dataclasses.replace(
                    base_candidate,
                    entries=tuple(
                        dataclasses.replace(row, surface_class="runtime")
                        if row.source_path == env_row.source_path
                        else row
                        for row in base_candidate.entries
                    ),
                ),
            ),
        )
        for name, candidate_row, candidate_document in cases:
            with self.subTest(case=name):
                findings = lifecycle._surface_replacement_findings(
                    ROOT,
                    self.profiles,
                    candidate_document,
                    candidate_row,
                )
                self.assertEqual(
                    {"manifest-replacement-invalid"},
                    {finding.code for finding in findings},
                )

        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = pathlib.Path(temporary.name)
        init_repo(root)
        tracked_source = root / source_path
        tracked_source.parent.mkdir(parents=True)
        tracked_source.write_text("services: {}\n", encoding="utf-8")
        commit_all(root)
        untracked_replacement = root / replacement_path
        untracked_replacement.write_text("services: {}\n", encoding="utf-8")
        untracked_source_row = dataclasses.replace(
            destructive,
            source_path=pathlib.PurePosixPath(source_path),
        )
        untracked_replacement_row = dataclasses.replace(
            replacement,
            source_path=pathlib.PurePosixPath(replacement_path),
            target_path=pathlib.PurePosixPath(replacement_path),
        )
        untracked_document = dataclasses.replace(
            document,
            entries=(untracked_source_row, untracked_replacement_row),
        )
        findings = lifecycle._surface_replacement_findings(
            root,
            self.profiles,
            untracked_document,
            untracked_source_row,
        )
        self.assertEqual(
            {"manifest-replacement-invalid"},
            {finding.code for finding in findings},
        )

    def test_v2_rejects_sensitive_evidence_without_echoing_the_value(self) -> None:
        marker = "token=target-wave-secret-sentinel"
        document = self.target_manifest()
        source = self.target_row(document, ".env.example")
        candidate = self.replace_target_row(
            document,
            dataclasses.replace(
                source,
                evidence=dataclasses.replace(source.evidence, commands=(marker,)),
            ),
        )

        findings = lifecycle.validate_migration_manifest(
            ROOT,
            self.profiles,
            self.contract,
            candidate,
        )
        self.assertIn("manifest-evidence-confidential", {item.code for item in findings})
        self.assertNotIn(marker, "\n".join(map(str, findings)))

    def test_v2_partition_plan_must_resolve_to_a_tracked_canonical_plan(self) -> None:
        document = self.target_manifest()
        source = self.target_row(document, ".env.example")
        candidate = self.replace_target_row(
            document,
            dataclasses.replace(
                source,
                partition_plan=pathlib.PurePosixPath(
                    "docs/04.execution/plans/missing-target-wave-plan.md"
                ),
            ),
        )

        self.assertIn("manifest-partition-plan-invalid", self.target_codes(candidate))

    def test_v2_archive_transition_uses_the_validated_result_like_v1(self) -> None:
        row = self.valid_row(
            target_path=pathlib.PurePosixPath("docs/98.archive/source.md"),
            artifact_type="spec",
            artifact_type_before="spec",
            artifact_type_after="archive",
            surface_class="typed-example",
            status_after="archived",
            disposition="archive",
            preservation_class="git-history",
            evidence=lifecycle.ManifestEvidence(
                ("git diff --name-status",),
                ("docs/03.specs/source.md",),
                (pathlib.PurePosixPath("docs/03.specs/source.md"),),
                ("git grep -l --fixed-strings",),
                ("git revert --no-commit",),
            ),
            review_verdict=lifecycle.ReviewVerdict("pass", "pass"),
        )
        document = dataclasses.replace(
            self.document("a" * 40, entries=(row,)), schema_version=2
        )
        with (
            mock.patch.object(
                lifecycle, "_surface_result_state_findings", return_value=([], True)
            ),
            mock.patch.object(
                lifecycle, "_surface_rollback_valid", return_value=True
            ),
        ):
            codes = {
                finding.code
                for finding in lifecycle._validate_surface_manifest_semantics(
                    ROOT, self.profiles, self.contract, document
                )
            }

        self.assertNotIn("manifest-transition-invalid", codes)

    def test_native_binary_generation_does_not_decode_blob_body(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = pathlib.Path(temporary.name)
        init_repo(root)
        asset = root / "assets/native.bin"
        asset.parent.mkdir(parents=True)
        asset.write_bytes(b"\xff\xfe\x00\x80")
        baseline = commit_all(root)
        contract = copy.deepcopy(self.contract)
        contract["waves"]["binary-fixture"] = {
            "baseline_commit": baseline,
            "enforcement": "advisory",
            "manifest_path": "docs/manifest.yaml",
            "summary_path": "docs/manifest-summary.md",
            "scope_state": "approved",
            "source_roots": ["assets"],
            "direct_source_paths": [],
            "declared_outputs": [],
        }
        document = lifecycle.generate_manifest_skeleton(
            root,
            contract,
            wave="binary-fixture",
            baseline_ref=baseline,
        )
        self.assertEqual(1, len(document.entries))
        row = document.entries[0]
        self.assertEqual("unsupported-static", row.surface_class)
        self.assertIsNone(row.artifact_type_before)
        self.assertIsNone(row.artifact_type_after)

    def test_wave_archive_selection_is_focused_to_after_archive_rows(self) -> None:
        selected = self.valid_row(
            source_path=pathlib.PurePosixPath("archive/Windows-Network-IP.md"),
            target_path=pathlib.PurePosixPath("archive/Windows-Network-IP.md"),
            artifact_type=None,
            artifact_type_before=None,
            artifact_type_after="archive",
            surface_class="content-archive",
        )
        document = dataclasses.replace(
            self.document("a" * 40, entries=(selected,), wave=TARGET_WAVE),
            schema_version=2,
        )
        records = (
            metadata.Record(pathlib.Path("archive/Windows-Network-IP.md"), {}, "archive"),
            metadata.Record(pathlib.Path("docs/98.archive/legacy.md"), {}, "archive"),
        )
        focused = lifecycle.archive_records_for_wave(records, document)
        self.assertEqual(
            ["archive/Windows-Network-IP.md"],
            [record.path.as_posix() for record in focused],
        )

    def test_template_source_placeholder_identity_is_null_but_real_identity_is_enforced(
        self,
    ) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = pathlib.Path(temporary.name)
        init_repo(root)
        source_path = "docs/99.templates/templates/common/archive.template.md"
        source = root / source_path
        source.parent.mkdir(parents=True)

        def write_template(artifact_id: str) -> None:
            source.write_text(
                "---\n"
                "status: draft\n"
                f"artifact_id: {artifact_id}\n"
                "artifact_type: archive\n"
                "parent_ids: []\n"
                "---\n\n"
                "# Archive\n",
                encoding="utf-8",
            )

        contract = self.fixture_contract([source_path])
        write_template("<artifact-id>")
        placeholder_baseline = commit_all(root, "template placeholder baseline")
        placeholder_document = lifecycle.generate_manifest_skeleton(
            root,
            contract,
            wave="fixture",
            baseline_ref=placeholder_baseline,
        )
        placeholder_row = placeholder_document.entries[0]
        self.assertEqual(placeholder_row.artifact_type, "template-source")
        self.assertIsNone(placeholder_row.artifact_id)
        placeholder_codes = {
            finding.code
            for finding in lifecycle.validate_migration_manifest(
                root,
                self.profiles,
                contract,
                placeholder_document,
            )
        }
        self.assertTrue(
            {
                "manifest-static-invalid",
                "manifest-baseline-artifact-id-mismatch",
                "manifest-target-artifact-id-mismatch",
            }.isdisjoint(placeholder_codes)
        )

        write_template("template-source:rogue")
        real_id_baseline = commit_all(root, "template real identity baseline")
        real_id_document = lifecycle.generate_manifest_skeleton(
            root,
            contract,
            wave="fixture",
            baseline_ref=real_id_baseline,
        )
        real_id_row = real_id_document.entries[0]
        self.assertEqual(real_id_row.artifact_id, "template-source:rogue")
        real_id_codes = {
            finding.code
            for finding in lifecycle.validate_migration_manifest(
                root,
                self.profiles,
                contract,
                real_id_document,
            )
        }
        self.assertIn("manifest-static-invalid", real_id_codes)

        hidden_real_id = dataclasses.replace(real_id_row, artifact_id=None)
        hidden_real_id_codes = {
            finding.code
            for finding in lifecycle.validate_migration_manifest(
                root,
                self.profiles,
                contract,
                self.document(
                    real_id_baseline,
                    entries=(hidden_real_id,),
                ),
            )
        }
        self.assertTrue(
            {
                "manifest-baseline-artifact-id-mismatch",
                "manifest-target-artifact-id-mismatch",
            }.issubset(hidden_real_id_codes)
        )

        write_template("<noncanonical-artifact-id>")
        noncanonical_placeholder_baseline = commit_all(
            root, "template noncanonical placeholder baseline"
        )
        noncanonical_placeholder_document = lifecycle.generate_manifest_skeleton(
            root,
            contract,
            wave="fixture",
            baseline_ref=noncanonical_placeholder_baseline,
        )
        noncanonical_placeholder_row = noncanonical_placeholder_document.entries[0]
        self.assertEqual(
            noncanonical_placeholder_row.artifact_id,
            "<noncanonical-artifact-id>",
        )
        noncanonical_placeholder_codes = {
            finding.code
            for finding in lifecycle.validate_migration_manifest(
                root,
                self.profiles,
                contract,
                noncanonical_placeholder_document,
            )
        }
        self.assertIn("manifest-static-invalid", noncanonical_placeholder_codes)

        non_template_path = "docs/03.specs/non-template.md"
        non_template_source = root / non_template_path
        non_template_source.parent.mkdir(parents=True, exist_ok=True)
        non_template_source.write_text(
            "---\n"
            "status: active\n"
            "artifact_id: <artifact-id>\n"
            "artifact_type: spec\n"
            "parent_ids: []\n"
            "---\n\n"
            "# Non-template\n",
            encoding="utf-8",
        )
        non_template_baseline = commit_all(root, "non-template placeholder baseline")
        non_template_document = lifecycle.generate_manifest_skeleton(
            root,
            self.fixture_contract([non_template_path]),
            wave="fixture",
            baseline_ref=non_template_baseline,
        )
        non_template_row = non_template_document.entries[0]
        self.assertEqual(non_template_row.artifact_type, "spec")
        self.assertEqual(non_template_row.artifact_id, "<artifact-id>")

    def test_manifest_coverage_path_type_and_target_conditions(self) -> None:
        temporary, root, baseline = self.make_repo()
        self.addCleanup(temporary.cleanup)
        valid = self.valid_row()
        cases = {
            "missing": ((), "manifest-source-missing"),
            "duplicate": ((valid, valid), "manifest-source-duplicate"),
            "delete-target": (
                (dataclasses.replace(valid, disposition="delete"),),
                "manifest-delete-target-invalid",
            ),
            "move-null": (
                (dataclasses.replace(valid, disposition="move", target_path=None),),
                "manifest-move-target-required",
            ),
            "preserve-distinct": (
                (
                    dataclasses.replace(
                        valid,
                        target_path=pathlib.PurePosixPath("docs/03.specs/other.md"),
                    ),
                ),
                "manifest-preserve-target-invalid",
            ),
            "absolute-source": (
                (dataclasses.replace(valid, source_path=pathlib.PurePosixPath("/tmp/source.md")),),
                "manifest-source-path-invalid",
            ),
            "unknown-type": (
                (dataclasses.replace(valid, artifact_type="mystery"),),
                "manifest-artifact-type-invalid",
            ),
        }
        for name, (entries, expected) in cases.items():
            with self.subTest(case=name):
                self.assertIn(expected, self.validate(root, baseline, entries))

    def test_baseline_must_resolve_to_the_exact_commit(self) -> None:
        temporary, root, baseline = self.make_repo()
        self.addCleanup(temporary.cleanup)
        document = self.document("f" * 40)
        findings = lifecycle.validate_migration_manifest(
            root,
            self.profiles,
            self.fixture_contract(["docs/03.specs/source.md"]),
            document,
        )
        self.assertIn("manifest-baseline-commit-invalid", {item.code for item in findings})
        self.assertNotEqual(baseline, document.baseline_commit)

    def test_destructive_pending_row_is_rejected(self) -> None:
        temporary, root, baseline = self.make_repo()
        self.addCleanup(temporary.cleanup)
        row = self.valid_row(
            disposition="delete",
            target_path=None,
            preservation_class="git-history",
            active_consumers=(pathlib.PurePosixPath("docs/consumer.md"),),
            evidence=lifecycle.ManifestEvidence(
                ("git show BASE:docs/source.md",),
                ("docs/source.md",),
                (pathlib.PurePosixPath("docs/source.md"),),
                ("rg --fixed-strings docs/source.md",),
                ("revert logical task commit",),
            ),
            review_verdict=lifecycle.ReviewVerdict("pending", "pending"),
        )
        self.assertIn(
            "manifest-destructive-review-required",
            self.validate(root, baseline, (row,), enforcement="blocking"),
        )

    def test_reviewed_evidence_rejects_broad_consumers_and_floating_rollback(
        self,
    ) -> None:
        temporary, root, baseline = self.make_repo()
        self.addCleanup(temporary.cleanup)
        consumer = root / "docs/00.agent-governance/consumer.md"
        consumer.parent.mkdir(parents=True, exist_ok=True)
        consumer.write_text(
            "# Consumer\n\nUses docs/03.specs/source.md.\n",
            encoding="utf-8",
        )
        source = root / "docs/03.specs/source.md"
        source.write_text(
            source.read_text(encoding="utf-8") + "\nChanged.\n",
            encoding="utf-8",
        )
        changed_commit = commit_all(root, "change source and add consumer")
        row = self.valid_row(
            disposition="migrate",
            active_consumers=(),
            evidence=lifecycle.ManifestEvidence(
                (
                    f"git diff --name-status {baseline}..{changed_commit} -- docs/03.specs/source.md",
                    f"git log --format=%H {baseline}..{changed_commit} -- docs/03.specs/source.md",
                ),
                ("docs/03.specs/source.md",),
                (pathlib.PurePosixPath("docs/03.specs/source.md"),),
                ("git grep -l --fixed-strings -- 'docs/03.specs/source.md'",),
                (f"git revert --no-commit {baseline}..HEAD",),
            ),
        )

        codes = {
            finding.code
            for finding in lifecycle.validate_migration_manifest(
                root,
                self.profiles,
                self.fixture_contract(
                    ["docs/03.specs/source.md"],
                    wave="foundation",
                ),
                self.document(
                    baseline,
                    entries=(row,),
                    wave="foundation",
                ),
            )
        }

        self.assertIn("manifest-consumer-scan-invalid", codes)
        self.assertIn("manifest-consumer-evidence-mismatch", codes)
        self.assertIn("manifest-rollback-invalid", codes)

        exact_row = dataclasses.replace(
            row,
            active_consumers=(
                pathlib.PurePosixPath("docs/00.agent-governance/consumer.md"),
            ),
            evidence=dataclasses.replace(
                row.evidence,
                consumer_scan=(
                    lifecycle._active_consumer_scan_command(
                        "docs/03.specs/source.md"
                    ),
                ),
                rollback=(f"git revert --no-commit {changed_commit}",),
            ),
        )
        exact_codes = {
            finding.code
            for finding in lifecycle.validate_migration_manifest(
                root,
                self.profiles,
                self.fixture_contract(
                    ["docs/03.specs/source.md"],
                    wave="foundation",
                ),
                self.document(
                    baseline,
                    entries=(exact_row,),
                    wave="foundation",
                ),
            )
        }
        self.assertTrue(
            {
                "manifest-consumer-scan-invalid",
                "manifest-consumer-evidence-mismatch",
                "manifest-rollback-invalid",
            }.isdisjoint(exact_codes)
        )

    def _foundation_reviewed_row(
        self,
        baseline: str,
        *,
        disposition: str = "preserve",
    ) -> lifecycle.MigrationManifestRow:
        source = "docs/03.specs/source.md"
        evidence_paths = tuple(
            sorted(
                (
                    source,
                    "docs/03.specs/131-document-corpus-lifecycle-migration-foundation/spec.md",
                    "docs/04.execution/plans/2026-07-14-document-corpus-lifecycle-migration-foundation.md",
                )
            )
        )
        return self.valid_row(
            disposition=disposition,
            evidence=lifecycle.ManifestEvidence(
                commands=(
                    f"git diff --name-status {baseline}..{baseline} -- {source}",
                    f"git log --format=%H {baseline}..{baseline} -- {source}",
                ),
                sources=evidence_paths,
                repository_paths=tuple(
                    pathlib.PurePosixPath(path) for path in evidence_paths
                ),
                consumer_scan=(lifecycle._active_consumer_scan_command(source),),
                rollback=(),
            ),
            review_verdict=lifecycle.ReviewVerdict("pass", "pass"),
        )

    def _foundation_codes(
        self,
        root: pathlib.Path,
        baseline: str,
        row: lifecycle.MigrationManifestRow,
        *,
        enforcement: str = "blocking",
    ) -> set[str]:
        contract = self.fixture_contract(
            ["docs/03.specs/source.md"],
            wave="foundation",
            enforcement=enforcement,
        )
        return {
            finding.code
            for finding in lifecycle.validate_migration_manifest(
                root,
                self.profiles,
                contract,
                self.document(
                    baseline,
                    entries=(row,),
                    wave="foundation",
                    enforcement=enforcement,
                ),
            )
        }

    def test_promoted_foundation_requires_complete_reviewed_evidence(self) -> None:
        temporary, root, baseline = self.make_repo()
        self.addCleanup(temporary.cleanup)
        valid = self._foundation_reviewed_row(baseline)

        all_empty = dataclasses.replace(
            valid,
            evidence=lifecycle.ManifestEvidence((), (), (), (), ()),
        )
        self.assertIn(
            "manifest-reviewed-evidence-required",
            self._foundation_codes(root, baseline, all_empty),
        )

        for field in ("sources", "repository_paths"):
            with self.subTest(field=field):
                candidate = dataclasses.replace(
                    valid,
                    evidence=dataclasses.replace(valid.evidence, **{field: ()}),
                )
                self.assertIn(
                    "manifest-reviewed-evidence-required",
                    self._foundation_codes(root, baseline, candidate),
                )

        wrong_sources = dataclasses.replace(
            valid,
            evidence=dataclasses.replace(
                valid.evidence,
                sources=("docs/03.specs/source.md",),
            ),
        )
        self.assertIn(
            "manifest-reviewed-source-evidence-invalid",
            self._foundation_codes(root, baseline, wrong_sources),
        )
        wrong_repository_paths = dataclasses.replace(
            valid,
            evidence=dataclasses.replace(
                valid.evidence,
                repository_paths=(
                    pathlib.PurePosixPath("docs/03.specs/source.md"),
                ),
            ),
        )
        self.assertIn(
            "manifest-reviewed-repository-evidence-invalid",
            self._foundation_codes(root, baseline, wrong_repository_paths),
        )

        self.assertNotIn(
            "manifest-reviewed-evidence-required",
            self._foundation_codes(root, baseline, valid),
        )
        self.assertNotIn(
            "manifest-rollback-invalid",
            self._foundation_codes(root, baseline, valid),
        )

    def test_empty_rollback_is_only_valid_for_unchanged_preserve(self) -> None:
        temporary, root, baseline = self.make_repo()
        self.addCleanup(temporary.cleanup)
        unchanged_migrate = self._foundation_reviewed_row(
            baseline,
            disposition="migrate",
        )
        self.assertIn(
            "manifest-rollback-invalid",
            self._foundation_codes(root, baseline, unchanged_migrate),
        )

    def test_pending_advisory_foundation_skeleton_allows_empty_evidence(self) -> None:
        temporary, root, baseline = self.make_repo()
        self.addCleanup(temporary.cleanup)
        contract = self.fixture_contract(
            ["docs/03.specs/source.md"],
            wave="foundation",
            enforcement="advisory",
        )
        document = lifecycle.generate_manifest_skeleton(
            root,
            contract,
            wave="foundation",
            baseline_ref=baseline,
        )
        codes = {
            finding.code
            for finding in lifecycle.validate_migration_manifest(
                root,
                self.profiles,
                contract,
                document,
            )
        }
        self.assertNotIn("manifest-reviewed-evidence-required", codes)
        self.assertNotIn("manifest-rollback-invalid", codes)

    def test_advisory_foundation_with_one_passing_review_requires_evidence(self) -> None:
        temporary, root, baseline = self.make_repo()
        self.addCleanup(temporary.cleanup)
        row = dataclasses.replace(
            self.valid_row(),
            evidence=lifecycle.ManifestEvidence((), (), (), (), ()),
            review_verdict=lifecycle.ReviewVerdict("pass", "pending"),
        )
        self.assertIn(
            "manifest-reviewed-evidence-required",
            self._foundation_codes(
                root,
                baseline,
                row,
                enforcement="advisory",
            ),
        )

    def test_manifest_evidence_rejects_sensitive_values_without_echoing_them(self) -> None:
        temporary, root, baseline = self.make_repo()
        self.addCleanup(temporary.cleanup)
        valid = self._foundation_reviewed_row(baseline)
        sensitive_values = (
            "token=supersecretvalue",
            "password: supersecretvalue",
            "secret=supersecretvalue",
            "api_key=supersecretvalue",
            "-----BEGIN PRIVATE KEY----- supersecretvalue",
            ".netrc supersecretvalue",
            ".docker/config.json supersecretvalue",
            "auth.json supersecretvalue",
            ".aws/credentials supersecretvalue",
            ".bash_history supersecretvalue",
            "2026-07-15T10:00:00Z ERROR supersecretvalue",
        )
        fields = ("commands", "sources", "repository_paths", "consumer_scan", "rollback")
        for field in fields:
            for marker in sensitive_values:
                with self.subTest(field=field, payload_class=marker.split("=")[0]):
                    value: object = (
                        pathlib.PurePosixPath(marker)
                        if field == "repository_paths"
                        else marker
                    )
                    current = getattr(valid.evidence, field)
                    candidate = dataclasses.replace(
                        valid,
                        evidence=dataclasses.replace(
                            valid.evidence,
                            **{field: tuple(sorted((*current, value)))},
                        ),
                    )
                    findings = lifecycle.validate_migration_manifest(
                        root,
                        self.profiles,
                        self.fixture_contract(
                            ["docs/03.specs/source.md"],
                            wave="foundation",
                            enforcement="blocking",
                        ),
                        self.document(
                            baseline,
                            entries=(candidate,),
                            wave="foundation",
                            enforcement="blocking",
                        ),
                    )
                    self.assertIn(
                        "manifest-evidence-confidential",
                        {finding.code for finding in findings},
                    )
                    rendered = io.StringIO()
                    with contextlib.redirect_stdout(rendered):
                        lifecycle._print_findings(findings)
                    self.assertNotIn("supersecretvalue", rendered.getvalue())

    def test_manifest_evidence_allows_safe_credential_option_names(self) -> None:
        temporary, root, baseline = self.make_repo()
        self.addCleanup(temporary.cleanup)
        valid = self._foundation_reviewed_row(baseline)
        safe_values = (
            "tool --token-file config/token-path",
            "tool --password-stdin",
            "git config credential.helper",
            "docs/auth.md",
            "secrets/README.md",
        )
        for value in safe_values:
            with self.subTest(value=value):
                candidate = dataclasses.replace(
                    valid,
                    evidence=dataclasses.replace(
                        valid.evidence,
                        commands=tuple(sorted((*valid.evidence.commands, value))),
                    ),
                )
                self.assertNotIn(
                    "manifest-evidence-confidential",
                    self._foundation_codes(root, baseline, candidate),
                )

        for value in ("docs/auth.md", "secrets/README.md"):
            with self.subTest(repository_path=value):
                candidate = dataclasses.replace(
                    valid,
                    evidence=dataclasses.replace(
                        valid.evidence,
                        repository_paths=tuple(
                            sorted(
                                (
                                    *valid.evidence.repository_paths,
                                    pathlib.PurePosixPath(value),
                                )
                            )
                        ),
                    ),
                )
                self.assertNotIn(
                    "manifest-evidence-confidential",
                    self._foundation_codes(root, baseline, candidate),
                )

    def test_check_manifest_cli_rejects_evidence_secret_without_echo(self) -> None:
        temporary, root, baseline = self.make_repo()
        self.addCleanup(temporary.cleanup)
        marker = "token=supersecretvalue"
        valid = self._foundation_reviewed_row(baseline)
        candidate = dataclasses.replace(
            valid,
            evidence=dataclasses.replace(
                valid.evidence,
                sources=tuple(sorted((*valid.evidence.sources, marker))),
            ),
        )
        document = self.document(
            baseline,
            entries=(candidate,),
            wave="foundation",
            enforcement="blocking",
        )
        manifest = root / "docs/manifest.yaml"
        manifest.write_text(
            lifecycle.render_migration_manifest(document),
            encoding="utf-8",
        )
        contract = self.fixture_contract(
            ["docs/03.specs/source.md"],
            wave="foundation",
            enforcement="blocking",
        )
        stdout = io.StringIO()
        stderr = io.StringIO()
        with (
            mock.patch.object(
                lifecycle,
                "load_migration_contract",
                return_value=contract,
            ),
            mock.patch.object(
                lifecycle.metadata,
                "load_profiles",
                return_value=self.profiles,
            ),
            contextlib.redirect_stdout(stdout),
            contextlib.redirect_stderr(stderr),
        ):
            result = lifecycle.main(
                [
                    "--root",
                    str(root),
                    "--mode",
                    "check-manifest",
                    "--wave",
                    "foundation",
                    "--manifest",
                    "docs/manifest.yaml",
                ]
            )
        rendered = stdout.getvalue() + stderr.getvalue()
        self.assertEqual(result, 3)
        self.assertIn("manifest-evidence-confidential", rendered)
        self.assertNotIn("supersecretvalue", rendered)
class PromotedManifestCliTests(LifecycleTestCase):
    def canonical_contract(
        self,
        *,
        enforcement: str = "advisory",
        manifest_path: str | None = None,
    ) -> dict[str, object]:
        contract = copy.deepcopy(self.contract)
        contract["waves"]["foundation"]["enforcement"] = enforcement
        contract["waves"]["foundation"]["manifest_path"] = manifest_path
        return contract

    def write_config(self, root: pathlib.Path, contract: dict[str, object]) -> tuple[pathlib.Path, pathlib.Path]:
        profiles = root / "profiles.yaml"
        profiles.write_text(PROFILES.read_text(encoding="utf-8"), encoding="utf-8")
        contract_path = root / "contract.yaml"
        contract_path.write_text(yaml.safe_dump(contract, sort_keys=False), encoding="utf-8")
        return profiles, contract_path

    def invoke(self, root: pathlib.Path, profiles: pathlib.Path, contract: pathlib.Path) -> subprocess.CompletedProcess[str]:
        return run(
            sys.executable,
            str(SCRIPT),
            "--root",
            str(root),
            "--profiles",
            str(profiles),
            "--contract",
            str(contract),
            "--mode",
            "check-promoted",
            cwd=ROOT,
        )

    def test_advisory_null_is_skipped_but_blocking_null_fails(self) -> None:
        canonical_foundation = self.contract["waves"]["foundation"]
        self.assertEqual(canonical_foundation["enforcement"], "blocking")
        self.assertEqual(
            canonical_foundation["manifest_path"],
            "docs/90.references/data/governance/"
            "document-corpus-lifecycle/ref-0067-foundation.yaml",
        )
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            advisory = self.canonical_contract()
            self.assertEqual(advisory["waves"]["foundation"]["enforcement"], "advisory")
            self.assertIsNone(advisory["waves"]["foundation"]["manifest_path"])
            profiles, contract_path = self.write_config(root, advisory)
            advisory_result = self.invoke(ROOT, profiles, contract_path)
            self.assertEqual(advisory_result.returncode, 1)
            self.assertNotIn("promoted-manifest-path-required: foundation", advisory_result.stdout)
            self.assertNotIn("promoted-manifest-missing: foundation", advisory_result.stdout)

            blocking = self.canonical_contract(enforcement="blocking")
            _, contract_path = self.write_config(root, blocking)
            result = self.invoke(ROOT, profiles, contract_path)
            self.assertEqual(result.returncode, 1)
            self.assertIn("promoted-manifest-path-required", result.stdout)

    def test_blocking_manifest_requires_existing_path_and_matching_enforcement(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            init_repo(root)
            contract = self.canonical_contract(
                enforcement="blocking",
                manifest_path=(
                    "docs/90.references/data/governance/"
                    "document-corpus-lifecycle/fixture.yaml"
                ),
            )
            source_paths = contract["waves"]["foundation"]["source_paths"]
            for path_text in source_paths:
                source = root / path_text
                source.parent.mkdir(parents=True, exist_ok=True)
                body = "---\nstatus: draft\n---\n\n# Fixture\n" if path_text.endswith("archive.template.md") else "# Fixture\n"
                source.write_text(body, encoding="utf-8")
            baseline = commit_all(root)
            profiles, contract_path = self.write_config(root, contract)
            missing = self.invoke(root, profiles, contract_path)
            self.assertEqual(missing.returncode, 1)
            self.assertIn("promoted-manifest-missing", missing.stdout)

            manifest = lifecycle.generate_manifest_skeleton(
                root,
                contract,
                wave="foundation",
                baseline_ref=baseline,
            )
            manifest = dataclasses.replace(manifest, enforcement="advisory")
            manifest_path = root / contract["waves"]["foundation"]["manifest_path"]
            manifest_path.parent.mkdir(parents=True, exist_ok=True)
            manifest_path.write_text(
                lifecycle.render_migration_manifest(manifest), encoding="utf-8"
            )
            commit_all(root, "track promoted manifest")
            mismatch = self.invoke(root, profiles, contract_path)
            self.assertEqual(mismatch.returncode, 1)
            self.assertIn("promoted-enforcement-mismatch", mismatch.stdout)


class CandidateManifestCliTests(LifecycleTestCase):
    def write_config(
        self,
        root: pathlib.Path,
        contract: dict[str, object],
    ) -> tuple[pathlib.Path, pathlib.Path]:
        profiles = root / "profiles.yaml"
        profiles.write_text(PROFILES.read_text(encoding="utf-8"), encoding="utf-8")
        contract_path = root / "contract.yaml"
        contract_path.write_text(
            yaml.safe_dump(contract, sort_keys=False),
            encoding="utf-8",
        )
        return profiles, contract_path

    def invoke(
        self,
        root: pathlib.Path,
        profiles: pathlib.Path,
        contract: pathlib.Path,
        mode: str,
        manifest: pathlib.Path | str,
        *,
        output: pathlib.Path | None = None,
    ) -> subprocess.CompletedProcess[str]:
        arguments = [
            sys.executable,
            str(SCRIPT),
            "--root",
            str(root),
            "--profiles",
            str(profiles),
            "--contract",
            str(contract),
            "--mode",
            mode,
            "--manifest",
            str(manifest),
        ]
        if mode == "check-manifest":
            arguments.extend(("--wave", "foundation"))
        else:
            if output is None:
                raise AssertionError("summary modes require an output fixture")
            arguments.extend(("--output", str(output)))
        return run(*arguments, cwd=ROOT)

    def make_fixture(
        self,
        root: pathlib.Path,
    ) -> tuple[pathlib.Path, pathlib.Path, pathlib.Path]:
        init_repo(root)
        contract = copy.deepcopy(self.contract)
        contract["waves"]["foundation"]["enforcement"] = "advisory"
        contract["waves"]["foundation"]["manifest_path"] = None
        source_paths = contract["waves"]["foundation"]["source_paths"]
        foundation_manifest = yaml.safe_load(
            (
                ROOT
                / self.contract["waves"]["foundation"]["manifest_path"]
            ).read_text(encoding="utf-8")
        )
        baseline_commit = foundation_manifest["baseline_commit"]
        for source_path in source_paths:
            source = root / source_path
            source.parent.mkdir(parents=True, exist_ok=True)
            if source_path.endswith("archive.template.md"):
                source.write_text(
                    "---\nstatus: draft\n---\n\n# Archive fixture\n",
                    encoding="utf-8",
                )
            else:
                current_source = ROOT / source_path
                if current_source.is_file():
                    source.write_bytes(current_source.read_bytes())
                    continue
                historical_source = run(
                    "git",
                    "show",
                    f"{baseline_commit}:{source_path}",
                    cwd=ROOT,
                )
                if historical_source.returncode != 0:
                    raise AssertionError(historical_source.stderr)
                source.write_text(historical_source.stdout, encoding="utf-8")
        baseline = commit_all(root, "candidate baseline")
        document = lifecycle.generate_manifest_skeleton(
            root,
            contract,
            wave="foundation",
            baseline_ref=baseline,
        )
        candidate = root / "docs/90.references/data/fixture.yaml"
        candidate.parent.mkdir(parents=True, exist_ok=True)
        candidate.write_text(
            lifecycle.render_migration_manifest(document),
            encoding="utf-8",
        )
        profiles, contract_path = self.write_config(root, contract)
        return candidate, profiles, contract_path

    def test_explicit_modes_accept_safe_untracked_candidate_before_staging(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            candidate, profiles, contract = self.make_fixture(root)
            self.assertEqual(git(root, "ls-files", "--", candidate.relative_to(root)), "")

            checked = self.invoke(
                root,
                profiles,
                contract,
                "check-manifest",
                candidate.relative_to(root),
            )
            self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)

            summary = root / "docs/90.references/data/fixture-summary.md"
            generated = self.invoke(
                root,
                profiles,
                contract,
                "generate-summary",
                candidate.relative_to(root),
                output=summary,
            )
            self.assertEqual(generated.returncode, 0, generated.stdout + generated.stderr)
            self.assertTrue(summary.is_file())

            summary_checked = self.invoke(
                root,
                profiles,
                contract,
                "check-summary",
                candidate.relative_to(root),
                output=summary,
            )
            self.assertEqual(
                summary_checked.returncode,
                0,
                summary_checked.stdout + summary_checked.stderr,
            )

    def test_explicit_modes_reject_unsafe_candidate_paths_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            candidate, profiles, contract = self.make_fixture(root)
            outside = root.parent / f"{root.name}-outside-candidate.yaml"
            outside.write_bytes(candidate.read_bytes())
            self.addCleanup(lambda: outside.unlink(missing_ok=True))
            symlink = root / "docs/90.references/data/symlink.yaml"
            symlink.symlink_to(outside)
            unsafe_candidates: tuple[pathlib.Path | str, ...] = (
                symlink.relative_to(root),
                pathlib.Path("../escape.yaml"),
                outside,
            )

            for mode in ("check-manifest", "generate-summary", "check-summary"):
                for index, unsafe in enumerate(unsafe_candidates):
                    with self.subTest(mode=mode, candidate=unsafe):
                        output = root / f"unsafe-{mode}-{index}.md"
                        result = self.invoke(
                            root,
                            profiles,
                            contract,
                            mode,
                            unsafe,
                            output=output if mode != "check-manifest" else None,
                        )
                        self.assertEqual(result.returncode, 3)
                        self.assertFalse(output.exists())
                        self.assertNotIn("Traceback", result.stderr)

    def test_wave_archive_check_validates_candidate_before_archive_selection(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            init_repo(root)
            source = root / "archive/item.md"
            source.parent.mkdir(parents=True)
            source.write_text("# Archive candidate\n", encoding="utf-8")
            baseline = commit_all(root, "archive candidate baseline")
            contract = copy.deepcopy(self.contract)
            contract["waves"] = {
                "fixture": {
                    "baseline_commit": baseline,
                    "enforcement": "advisory",
                    "manifest_path": "docs/manifest.yaml",
                    "summary_path": "docs/manifest-summary.md",
                    "scope_state": "approved",
                    "source_roots": ["archive"],
                    "direct_source_paths": [],
                    "declared_outputs": [],
                }
            }
            canonical = lifecycle._generate_manifest_skeleton(
                root,
                contract,
                wave="fixture",
                baseline_ref=baseline,
                profiles=self.profiles,
            )
            archive_row = canonical.entries[0]
            cases = {
                "removed-selector": (
                    dataclasses.replace(canonical, entries=()),
                    False,
                    "manifest-source-missing",
                ),
                "altered-selector": (
                    dataclasses.replace(
                        canonical,
                        entries=(
                            dataclasses.replace(
                                archive_row,
                                artifact_type_after=None,
                            ),
                        ),
                    ),
                    False,
                    "manifest-artifact-transition-invalid",
                ),
                "noncanonical-bytes": (
                    canonical,
                    True,
                    "manifest-serialization-stale",
                ),
            }
            manifest = root / "docs/manifest.yaml"
            manifest.parent.mkdir(parents=True)
            records = (
                metadata.Record(pathlib.Path("archive/item.md"), {}, "archive"),
            )
            for name, (candidate, tamper_bytes, expected_code) in cases.items():
                with self.subTest(case=name):
                    rendered = lifecycle.render_migration_manifest(candidate)
                    if tamper_bytes:
                        rendered += "# noncanonical archive selector bytes\n"
                    manifest.write_text(rendered, encoding="utf-8")
                    stdout = io.StringIO()
                    stderr = io.StringIO()
                    with (
                        mock.patch.object(
                            lifecycle,
                            "load_migration_contract",
                            return_value=contract,
                        ),
                        mock.patch.object(
                            lifecycle.metadata,
                            "load_profiles",
                            return_value=self.profiles,
                        ),
                        mock.patch.object(
                            lifecycle,
                            "_full_findings",
                            return_value=(records, []),
                        ),
                        mock.patch.object(
                            lifecycle,
                            "validate_archive_provenance",
                            return_value=[],
                        ),
                        contextlib.redirect_stdout(stdout),
                        contextlib.redirect_stderr(stderr),
                    ):
                        result = lifecycle.main(
                            [
                                "--root",
                                str(root),
                                "--mode",
                                "check-archive",
                                "--wave",
                                "fixture",
                            ]
                        )
                    diagnostics = stdout.getvalue() + stderr.getvalue()
                    self.assertNotEqual(result, 0, diagnostics)
                    self.assertIn(expected_code, diagnostics)
                    self.assertNotIn("Archive candidate", diagnostics)
                    self.assertNotIn("noncanonical archive selector bytes", diagnostics)


class ArchiveProvenanceTests(LifecycleTestCase):
    def test_command_body_scan_rejects_markdown_list_commands(self) -> None:
        synthetic_mutations = {
            "unordered": "- NeTsH i i synthetic-static-address\n",
            "ordered": "1. nEtSh wlan synthetic-profile\n",
        }
        for kind, mutation in synthetic_mutations.items():
            with self.subTest(kind=kind):
                self.assertEqual(
                    ["stale-command-body"], archive_command_body_findings(mutation)
                )

    def test_command_body_scan_rejects_abbreviated_case_varied_netsh_line(self) -> None:
        synthetic_mutation = "  NeTsH i i synthetic-static-address\n"
        self.assertEqual(
            ["stale-command-body"],
            archive_command_body_findings(synthetic_mutation),
        )
        for non_command in (
            "The netsh utility is named only as historical context.\n",
            "netsh_command = disabled_identifier\n",
        ):
            with self.subTest(non_command=non_command):
                self.assertEqual([], archive_command_body_findings(non_command))

    def test_windows_network_note_is_a_provenance_only_content_tombstone(self) -> None:
        path = pathlib.Path(
            "docs/98.archive/tombstones/05.operations/ref-0095-windows-network-ip.md"
        )
        source_path = pathlib.PurePosixPath("archive/Windows-Network-IP.md")
        text = (ROOT / path).read_text(encoding="utf-8")
        record = metadata._record_from_text(path, text, profiles=self.profiles)
        manifest = metadata.build_manifest([record])
        failures: list[str] = []

        expected_metadata: dict[str, object] = {
            "status": "archived",
            "artifact_id": "ref-0095",
            "artifact_type": "archive",
            "parent_ids": [],
            "archived_from": source_path.as_posix(),
            "archived_at": "2026-07-18",
            "archive_disposition": "withdrawn",
            "archived_commit": TARGET_BASELINE,
            "archived_blob": "b1faa418b9e0bb91bc93137e6e97236e75967f21",
            "preservation_class": "git-history",
        }
        for key, expected in expected_metadata.items():
            if record.metadata.get(key) != expected:
                failures.append(f"metadata:{key}")
        if not isinstance(record.metadata.get("archive_reason"), str):
            failures.append("metadata:archive_reason")

        for key in (
            "supersedes",
            "archived_on",
            "current_replacement",
            "snapshot_path",
            "content_sha256",
            "snapshot_reason",
        ):
            if key in record.metadata:
                failures.append(f"forbidden:{key}")

        failures.extend(archive_command_body_findings(text))
        for heading in (
            "## Overview",
            "## Current-use Warning",
            "## Archive Metadata",
            "## Archive Ledger",
            "## Historical Retrieval",
            "## Related Documents",
        ):
            if heading not in text:
                failures.append(f"heading:{heading}")

        failures.extend(
            f"metadata-finding:{finding.code}"
            for finding in metadata.validate_record(record, self.profiles, manifest)
            if finding.severity == "error"
        )
        failures.extend(
            f"provenance-finding:{finding.code}"
            for finding in lifecycle.validate_archive_provenance(ROOT, record)
        )

        document = lifecycle.load_migration_manifest(
            ROOT
            / "docs/90.references/data/0069-target-surface-convergence/data.yaml"
        )
        row = next(
            item
            for item in document.entries
            if item.source_path == source_path
        )
        expected_row = {
            "target_path": source_path,
            "artifact_id": "archive:windows-network-ip",
            "artifact_type_before": None,
            "artifact_type_after": "archive",
            "surface_class": "content-archive",
            "status_before": None,
            "status_after": "archived",
            "parent_ids": (),
            "disposition": "preserve",
            "canonical_replacement": None,
            "active_consumers": (),
            "partition_plan": None,
            "preservation_class": "git-history",
            "review_verdict": lifecycle.ReviewVerdict("pass", "pass"),
        }
        for field, expected in expected_row.items():
            if getattr(row, field) != expected:
                failures.append(f"manifest:{field}")

        self.assertEqual([], failures)

    def archive_fixture(
        self, preservation_class: str = "git-history"
    ) -> tuple[tempfile.TemporaryDirectory[str], pathlib.Path, metadata.Record, bytes]:
        temporary = tempfile.TemporaryDirectory()
        root = pathlib.Path(temporary.name)
        init_repo(root)
        payload = b"historical evidence\n"
        source = root / "docs/source.md"
        source.parent.mkdir()
        source.write_bytes(payload)
        commit = commit_all(root)
        blob = git(root, "rev-parse", f"{commit}:docs/source.md")
        sha256 = hashlib.sha256(payload).hexdigest()
        tombstone_relative = pathlib.Path(
            "docs/98.archive/tombstones/05.operations/ref-9999-source.md"
        )
        tombstone = root / tombstone_relative
        tombstone.parent.mkdir(parents=True)
        metadata_values: dict[str, object] = {
            "status": "archived",
            "artifact_id": "ref-9999",
            "artifact_type": "archive",
            "parent_ids": [],
            "archived_from": "docs/source.md",
            "archived_at": "2026-07-14",
            "archive_reason": "Fixture.",
            "archive_disposition": "evidence-preserve",
            "archived_commit": commit,
            "archived_blob": blob,
            "preservation_class": preservation_class,
        }
        if preservation_class == "immutable-snapshot":
            snapshot = pathlib.PurePosixPath(
                f"docs/98.archive/evidence/{sha256}.md.snapshot"
            )
            (root / snapshot).parent.mkdir(parents=True)
            (root / snapshot).write_bytes(payload)
            metadata_values.update(
                snapshot_path=snapshot.as_posix(),
                content_sha256=sha256,
                snapshot_reason="Approved audit evidence.",
            )
        tombstone.write_text("# Tombstone\n", encoding="utf-8")
        commit_all(root, "track archive fixture")
        record = metadata.Record(
            tombstone_relative, metadata_values, "archive"
        )
        return temporary, root, record, payload

    def test_commit_blob_path_and_snapshot_hashes_are_verified(self) -> None:
        temporary, root, record, _ = self.archive_fixture("immutable-snapshot")
        self.addCleanup(temporary.cleanup)
        self.assertEqual(lifecycle.validate_archive_provenance(root, record), [])

        mutations = {
            "commit": ({"archived_commit": "f" * 40}, "archive-commit-invalid"),
            "blob": ({"archived_blob": "f" * 40}, "archive-blob-invalid"),
            "path-equality": ({"archived_blob": git(root, "hash-object", "-w", str(root / record.path))}, "archive-blob-mismatch"),
            "snapshot-path": ({"snapshot_path": "docs/98.archive/evidence/wrong.md.snapshot"}, "archive-snapshot-path-mismatch"),
        }
        for name, (changes, expected) in mutations.items():
            with self.subTest(case=name):
                changed = dataclasses.replace(record, metadata={**record.metadata, **changes})
                self.assertIn(
                    expected,
                    {item.code for item in lifecycle.validate_archive_provenance(root, changed)},
                )
        snapshot_path = root / record.metadata["snapshot_path"]
        snapshot_path.write_bytes(b"changed evidence\n")
        self.assertIn(
            "archive-content-sha256-mismatch",
            {item.code for item in lifecycle.validate_archive_provenance(root, record)},
        )

    def test_git_history_forbids_snapshot_bytes(self) -> None:
        temporary, root, record, payload = self.archive_fixture("git-history")
        self.addCleanup(temporary.cleanup)
        sha256 = hashlib.sha256(payload).hexdigest()
        snapshot = root / f"docs/98.archive/evidence/{sha256}.md.snapshot"
        snapshot.parent.mkdir(parents=True)
        snapshot.write_bytes(payload)
        changed = dataclasses.replace(
            record,
            metadata={
                **record.metadata,
                "snapshot_path": snapshot.relative_to(root).as_posix(),
                "content_sha256": sha256,
                "snapshot_reason": "Not admitted.",
            },
        )
        self.assertIn(
            "archive-snapshot-forbidden",
            {item.code for item in lifecycle.validate_archive_provenance(root, changed)},
        )

    def test_sensitive_snapshot_classes_are_rejected_without_payload_leakage(self) -> None:
        samples = (
            b"password=ultra-sensitive-value\n",
            b"credential: ultra-sensitive-value\n",
            b"token=ultra-sensitive-value\n",
            b"-----BEGIN PRIVATE KEY-----\nultra-sensitive-value\n",
            b".bash_history\nultra-sensitive-value\n",
            b"2026-07-14 ERROR ultra-sensitive-value\n",
        )
        for sample in samples:
            temporary, root, record, _ = self.archive_fixture("immutable-snapshot")
            try:
                sha256 = hashlib.sha256(sample).hexdigest()
                snapshot_path = pathlib.PurePosixPath(
                    f"docs/98.archive/evidence/{sha256}.md.snapshot"
                )
                (root / snapshot_path).write_bytes(sample)
                commit_all(root, "track confidentiality fixture")
                changed = dataclasses.replace(
                    record,
                    metadata={
                        **record.metadata,
                        "snapshot_path": snapshot_path.as_posix(),
                        "content_sha256": sha256,
                    },
                )
                findings = lifecycle.validate_archive_provenance(root, changed)
                self.assertIn("archive-snapshot-confidential", {item.code for item in findings})
                rendered = "\n".join(item.message for item in findings)
                self.assertNotIn("ultra-sensitive-value", rendered)
            finally:
                temporary.cleanup()

    def test_ledgers_are_deterministic_and_snapshot_manifest_excludes_git_history(self) -> None:
        first_tmp, first_root, first, _ = self.archive_fixture("immutable-snapshot")
        second_tmp, _, second, _ = self.archive_fixture("git-history")
        self.addCleanup(first_tmp.cleanup)
        self.addCleanup(second_tmp.cleanup)
        records = (dataclasses.replace(second, path=pathlib.Path("docs/98.archive/z.md")), first)
        ledger = lifecycle.render_archive_ledger(records)
        snapshot = lifecycle.render_snapshot_manifest(records)
        self.assertEqual(ledger, lifecycle.render_archive_ledger(tuple(reversed(records))))
        self.assertIn(first.path.as_posix(), snapshot)
        self.assertNotIn("docs/98.archive/z.md", snapshot)
        self.assertNotIn((first_root / "docs/source.md").read_text(), ledger)

    def test_ledger_and_snapshot_generate_check_modes_are_byte_equal(self) -> None:
        temporary, root, record, payload = self.archive_fixture("immutable-snapshot")
        self.addCleanup(temporary.cleanup)
        frontmatter = yaml.safe_dump(record.metadata, sort_keys=False)
        (root / record.path).write_text(
            f"---\n{frontmatter}---\n\n# Archived Source\n",
            encoding="utf-8",
        )
        commit_all(root, "archive fixture")
        with tempfile.TemporaryDirectory() as output_directory:
            for generate_mode, check_mode, name in (
                ("generate-archive-ledger", "check-archive-ledger", "ledger.md"),
                (
                    "generate-snapshot-manifest",
                    "check-snapshot-manifest",
                    "snapshots.md",
                ),
            ):
                output = pathlib.Path(output_directory) / name
                generated = run(
                    sys.executable,
                    str(SCRIPT),
                    "--root",
                    str(root),
                    "--mode",
                    generate_mode,
                    "--output",
                    str(output),
                    cwd=ROOT,
                )
                self.assertEqual(generated.returncode, 0, generated.stdout + generated.stderr)
                before = output.read_bytes()
                checked = run(
                    sys.executable,
                    str(SCRIPT),
                    "--root",
                    str(root),
                    "--mode",
                    check_mode,
                    "--output",
                    str(output),
                    cwd=ROOT,
                )
                self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
                self.assertEqual(output.read_bytes(), before)
                self.assertNotIn(payload.decode().strip(), output.read_text(encoding="utf-8"))


class DuplicateBudgetAndImpactTests(LifecycleTestCase):
    def record(
        self,
        path: str,
        artifact_type: str = "spec",
        **metadata_values: object,
    ) -> metadata.Record:
        values = {
            "status": "active",
            "artifact_id": f"{artifact_type}:{pathlib.PurePosixPath(path).stem}",
            "artifact_type": artifact_type,
            "parent_ids": [],
        }
        values.update(metadata_values)
        return metadata.Record(pathlib.Path(path), values, artifact_type)

    def test_duplicate_candidates_are_same_type_advisory_and_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            paths = {
                "docs/03.specs/a.md": "# Shared Title\n\nSame body.\n",
                "docs/03.specs/b.md": "# Shared Title\n\nSame body.\n",
                "docs/03.specs/c.md": "# shared-title\n\nDifferent.\n",
                "docs/04.execution/plans/d.md": "# Shared Title\n\nSame body.\n",
            }
            for path, body in paths.items():
                target = root / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(body, encoding="utf-8")
            records = (
                self.record("docs/03.specs/c.md"),
                self.record("docs/04.execution/plans/d.md", "plan"),
                self.record("docs/03.specs/b.md"),
                self.record("docs/03.specs/a.md"),
            )
            candidates = lifecycle.find_duplicate_candidates(root, records)
            self.assertEqual(candidates, tuple(sorted(candidates)))
            pairs = {(item.left_path.as_posix(), item.right_path.as_posix()): item for item in candidates}
            self.assertIn(("docs/03.specs/a.md", "docs/03.specs/b.md"), pairs)
            self.assertIn("exact-content", pairs[("docs/03.specs/a.md", "docs/03.specs/b.md")].signals)
            self.assertIn("normalized-title", pairs[("docs/03.specs/a.md", "docs/03.specs/c.md")].signals)
            self.assertFalse(any("d.md" in left or "d.md" in right for left, right in pairs))
            self.assertFalse(hasattr(candidates[0], "disposition"))

    def test_immediate_leaf_budget_boundaries_and_added_only_blocking(self) -> None:
        records_99 = tuple(
            self.record(f"docs/04.execution/tasks/{index:03}.md", "task")
            for index in range(99)
        )
        below_warning = lifecycle.validate_directory_budgets(
            records_99,
            added_paths=frozenset(),
            warning_at=100,
            block_new_leaf_at=150,
            enforce_all=False,
        )
        self.assertNotIn("directory-budget-warning", {item.code for item in below_warning})

        records_100 = tuple(
            self.record(f"docs/04.execution/tasks/{index:03}.md", "task")
            for index in range(100)
        )
        findings = lifecycle.validate_directory_budgets(
            records_100,
            added_paths=frozenset(),
            warning_at=100,
            block_new_leaf_at=150,
            enforce_all=False,
        )
        self.assertIn("directory-budget-warning", {item.code for item in findings})
        self.assertNotIn("directory-budget-blocked", {item.code for item in findings})

        records_150 = tuple(
            self.record(f"docs/04.execution/tasks/{index:03}.md", "task")
            for index in range(150)
        )
        added = pathlib.PurePosixPath("docs/04.execution/tasks/149.md")
        blocked = lifecycle.validate_directory_budgets(
            records_150,
            added_paths=frozenset({added}),
            warning_at=100,
            block_new_leaf_at=150,
            enforce_all=False,
        )
        self.assertIn("directory-budget-blocked", {item.code for item in blocked})
        edited = lifecycle.validate_directory_budgets(
            records_150,
            added_paths=frozenset(),
            warning_at=100,
            block_new_leaf_at=150,
            enforce_all=False,
        )
        self.assertNotIn("directory-budget-blocked", {item.code for item in edited})

        records_149 = records_150[:-1]
        below_block = lifecycle.validate_directory_budgets(
            records_149,
            added_paths=frozenset({pathlib.PurePosixPath("docs/04.execution/tasks/148.md")}),
            warning_at=100,
            block_new_leaf_at=150,
            enforce_all=False,
        )
        self.assertNotIn("directory-budget-blocked", {item.code for item in below_block})

        approved_records = tuple(
            dataclasses.replace(
                record,
                metadata={
                    **record.metadata,
                    "partition_plan": "docs/04.execution/plans/2026-partition.md",
                    "review_verdict": {"specification": "pass", "quality": "pass"},
                },
            )
            if record.path.as_posix() == added.as_posix()
            else record
            for record in records_150
        )
        approved = lifecycle.validate_directory_budgets(
            approved_records,
            added_paths=frozenset({added}),
            warning_at=100,
            block_new_leaf_at=150,
            enforce_all=False,
        )
        self.assertNotIn("directory-budget-blocked", {item.code for item in approved})

    def test_review_age_unavailable_is_advisory_and_does_not_mutate_status(self) -> None:
        record = self.record("docs/03.specs/source.md", status="active")
        original = copy.deepcopy(record.metadata)
        findings = lifecycle._review_findings(
            (record,), self.contract, today=datetime.date(2026, 7, 14)
        )
        self.assertIn("review-age-unavailable", {item.code for item in findings})
        self.assertTrue(all(item.severity == "warning" for item in findings))
        self.assertEqual(record.metadata, original)

    def test_impacted_records_include_declared_consumer_and_links_not_title_similarity(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            init_repo(root)
            bodies = {
                "docs/03.specs/source.md": "# Shared Title\n\nInitial.\n",
                "docs/03.specs/consumer.md": "# Consumer\n\n[Source](./source.md)\n",
                "docs/03.specs/similar.md": "# Shared Title\n\nUnlinked.\n",
            }
            for path, body in bodies.items():
                target = root / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(body, encoding="utf-8")
            baseline = commit_all(root)
            (root / "docs/03.specs/source.md").write_text(
                "# Shared Title\n\nChanged.\n", encoding="utf-8"
            )
            records = (
                self.record("docs/03.specs/source.md"),
                self.record("docs/03.specs/consumer.md"),
                self.record("docs/03.specs/similar.md"),
            )
            row = self.valid_row(
                source_path=pathlib.PurePosixPath("docs/03.specs/source.md"),
                target_path=pathlib.PurePosixPath("docs/03.specs/source.md"),
                active_consumers=(pathlib.PurePosixPath("docs/03.specs/consumer.md"),),
            )
            document = self.document(baseline, entries=(row,))
            selected = lifecycle.collect_impacted_records(
                root,
                records,
                self.profiles,
                self.fixture_contract(["docs/03.specs/source.md"]),
                (document,),
                base_ref=baseline,
            )
            paths = {item.path.as_posix() for item in selected}
            self.assertIn("docs/03.specs/source.md", paths)
            self.assertIn("docs/03.specs/consumer.md", paths)
            self.assertNotIn("docs/03.specs/similar.md", paths)


class ExceptionValidationTests(LifecycleTestCase):
    def write(self, exceptions: list[dict[str, object]]) -> pathlib.Path:
        directory = tempfile.mkdtemp()
        self.addCleanup(lambda: __import__("shutil").rmtree(directory))
        path = pathlib.Path(directory) / "exceptions.yaml"
        path.write_text(
            yaml.safe_dump({"schema_version": 1, "exceptions": exceptions}, sort_keys=False),
            encoding="utf-8",
        )
        return path

    def valid(self) -> dict[str, object]:
        return {
            "finding_code": "directory-budget-warning",
            "scope_paths": ["docs/04.execution/tasks/example.md"],
            "owner": "docs-platform",
            "reason": "Bounded migration debt.",
            "approved_at": "2026-07-01",
            "expires_on": "2026-08-01",
            "exit_condition": "Partition the directory.",
            "evidence": ["docs/04.execution/tasks/evidence.md"],
        }

    def codes(self, value: dict[str, object]) -> set[str]:
        return {
            item.code
            for item in lifecycle.validate_exceptions(
                self.write([value]),
                known_codes=frozenset({"directory-budget-warning"}),
                today=datetime.date(2026, 7, 14),
            )
        }

    def test_bounded_exception_schema_cases(self) -> None:
        valid = self.valid()
        cases = {
            "unknown-code": ({**valid, "finding_code": "unknown"}, "exception-code-unknown"),
            "wildcard": ({**valid, "scope_paths": ["docs/**"]}, "exception-scope-invalid"),
            "owner": ({**valid, "owner": ""}, "exception-owner-required"),
            "reason": ({**valid, "reason": ""}, "exception-reason-required"),
            "exit": ({**valid, "exit_condition": ""}, "exception-exit-condition-required"),
            "expired": ({**valid, "expires_on": "2026-07-14"}, "exception-expired"),
        }
        for name, (value, expected) in cases.items():
            with self.subTest(case=name):
                self.assertIn(expected, self.codes(value))
        self.assertEqual(self.codes(valid), set())

    def test_omitted_owner_uses_the_specific_required_code(self) -> None:
        value = self.valid()
        del value["owner"]
        self.assertIn("exception-owner-required", self.codes(value))


class ReviewRemediationTests(LifecycleTestCase):
    def record(
        self,
        path: str,
        artifact_type: str = "spec",
        **metadata_values: object,
    ) -> metadata.Record:
        values: dict[str, object] = {
            "status": "active",
            "artifact_id": f"{artifact_type}:{pathlib.PurePosixPath(path).stem}",
            "artifact_type": artifact_type,
            "parent_ids": [],
        }
        values.update(metadata_values)
        return metadata.Record(pathlib.Path(path), values, artifact_type)

    def test_cli_misuse_does_not_execute_repository_metadata_module(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            validation = root / "scripts/validation"
            validation.mkdir(parents=True)
            shutil.copy2(SCRIPT, validation / SCRIPT.name)
            marker = root / "metadata-loaded"
            (validation / "check-document-metadata.py").write_text(
                "import pathlib\n"
                f"pathlib.Path({str(marker)!r}).write_text('loaded')\n"
                "raise RuntimeError('metadata module executed')\n",
                encoding="utf-8",
            )
            result = run(
                sys.executable,
                str(validation / SCRIPT.name),
                "--mode",
                "generate-manifest",
                cwd=root,
            )
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertFalse(marker.exists())
            self.assertNotIn("metadata module executed", result.stderr)
            self.assertNotIn("Traceback", result.stderr)

    def test_companion_reuses_canonical_static_manifest_and_exception_grammar(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            init_repo(root)
            readme = root / "README.md"
            readme.write_text("# Fixture\n", encoding="utf-8")
            baseline = commit_all(root)
            row = self.valid_row(
                source_path=pathlib.PurePosixPath("README.md"),
                target_path=pathlib.PurePosixPath("README.md"),
                artifact_id="readme:forbidden",
                artifact_type="readme",
                status_before=None,
                status_after=None,
            )
            document = self.document(baseline, entries=(row,))
            contract = self.fixture_contract(["README.md"])
            with self.assertRaises(metadata.ProfileError):
                metadata.validate_static_migration_manifest(
                    lifecycle._manifest_mapping(document), contract, self.profiles
                )
            findings = lifecycle.validate_migration_manifest(
                root, self.profiles, contract, document
            )
            self.assertIn("manifest-static-invalid", {item.code for item in findings})

        invalid_scope = ExceptionValidationTests.valid(self)
        invalid_scope["scope_paths"] = ["ALL"]
        codes = {
            item.code
            for item in lifecycle.validate_exceptions(
                ExceptionValidationTests.write(self, [invalid_scope]),
                known_codes=frozenset({"directory-budget-warning"}),
                today=datetime.date(2026, 7, 14),
            )
        }
        self.assertIn("exception-scope-invalid", codes)

    def test_exception_nested_types_fail_closed_without_traceback_or_payload(self) -> None:
        marker = "do-not-echo-nested-payload"
        cases: tuple[object, ...] = (
            {marker: "value"},
            [marker],
            True,
            None,
            7,
        )
        for value in cases:
            with self.subTest(value_type=type(value).__name__):
                entry = ExceptionValidationTests.valid(self)
                entry["evidence"] = [value]
                path = ExceptionValidationTests.write(self, [entry])
                findings = lifecycle.validate_exceptions(
                    path,
                    known_codes=frozenset({"directory-budget-warning"}),
                    today=datetime.date(2026, 7, 14),
                )
                rendered = "\n".join(
                    f"{item.code}:{item.path}:{item.message}" for item in findings
                )
                self.assertIn("exception-evidence-invalid", rendered)
                self.assertNotIn(marker, rendered)

    def _impact_fixture(
        self,
    ) -> tuple[tempfile.TemporaryDirectory[str], pathlib.Path, str, tuple[metadata.Record, ...]]:
        temporary = tempfile.TemporaryDirectory()
        root = pathlib.Path(temporary.name)
        init_repo(root)
        bodies = {
            "docs/03.specs/source.md": (
                "---\nstatus: active\nartifact_id: spec:source\n"
                "artifact_type: spec\nparent_ids: [spec:parent]\n---\n\n# Source\n"
            ),
            "docs/03.specs/parent.md": "# Parent\n",
            "docs/03.specs/dependent.md": "# Dependent\n",
            "docs/03.specs/superseder.md": "# Superseder\n",
            "docs/03.specs/link.md": "# Link\n\n[Source](./source.md)\n",
            "docs/03.specs/consumer.md": "# Consumer\n",
            "docs/03.specs/replacement.md": "# Replacement\n",
        }
        for path_text, body in bodies.items():
            target = root / path_text
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(body, encoding="utf-8")
        baseline = commit_all(root)
        records = (
            self.record("docs/03.specs/parent.md", artifact_id="spec:parent"),
            self.record(
                "docs/03.specs/dependent.md", parent_ids=["spec:source"]
            ),
            self.record(
                "docs/03.specs/superseder.md", supersedes="spec:source"
            ),
            self.record("docs/03.specs/link.md"),
            self.record("docs/03.specs/consumer.md"),
            self.record(
                "docs/03.specs/replacement.md", artifact_id="spec:replacement"
            ),
        )
        return temporary, root, baseline, records

    def test_deletion_selects_old_path_and_every_direct_relation_class(self) -> None:
        temporary, root, baseline, records = self._impact_fixture()
        self.addCleanup(temporary.cleanup)
        (root / "docs/03.specs/source.md").unlink()
        row = self.valid_row(
            source_path=pathlib.PurePosixPath("docs/03.specs/source.md"),
            target_path=None,
            artifact_id="spec:source",
            parent_ids=("spec:parent",),
            disposition="delete",
            canonical_replacement="spec:replacement",
            active_consumers=(
                pathlib.PurePosixPath("docs/03.specs/consumer.md"),
            ),
        )
        selected = lifecycle.collect_impacted_records(
            root,
            records,
            self.profiles,
            self.fixture_contract(["docs/03.specs/source.md"]),
            (self.document(baseline, entries=(row,)),),
            base_ref=baseline,
        )
        self.assertEqual(
            {item.path.as_posix() for item in selected},
            {
                "docs/03.specs/parent.md",
                "docs/03.specs/dependent.md",
                "docs/03.specs/superseder.md",
                "docs/03.specs/link.md",
                "docs/03.specs/consumer.md",
                "docs/03.specs/replacement.md",
            },
        )

    def test_rename_diff_is_nul_safe_and_retains_both_paths(self) -> None:
        temporary, root, baseline, records = self._impact_fixture()
        self.addCleanup(temporary.cleanup)
        old = root / "docs/03.specs/source.md"
        new = root / "docs/03.specs/renamed.md"
        old.rename(new)
        current, triggers = lifecycle._changed_path_sets(root, baseline)
        self.assertIn("docs/03.specs/renamed.md", current)
        self.assertIn("docs/03.specs/source.md", triggers)
        self.assertIn("docs/03.specs/renamed.md", triggers)

        renamed = self.record(
            "docs/03.specs/renamed.md",
            artifact_id="spec:source",
            parent_ids=["spec:parent"],
        )
        row = self.valid_row(
            source_path=pathlib.PurePosixPath("docs/03.specs/source.md"),
            target_path=pathlib.PurePosixPath("docs/03.specs/renamed.md"),
            artifact_id="spec:source",
            parent_ids=("spec:parent",),
            disposition="move",
            active_consumers=(
                pathlib.PurePosixPath("docs/03.specs/consumer.md"),
            ),
        )
        selected = lifecycle.collect_impacted_records(
            root,
            (*records, renamed),
            self.profiles,
            self.fixture_contract(["docs/03.specs/source.md"]),
            (self.document(baseline, entries=(row,)),),
            base_ref=baseline,
        )
        paths = {item.path.as_posix() for item in selected}
        self.assertIn("docs/03.specs/renamed.md", paths)
        self.assertIn("docs/03.specs/link.md", paths)
        self.assertIn("docs/03.specs/parent.md", paths)
        self.assertIn("docs/03.specs/consumer.md", paths)

    def test_introduced_findings_subtract_identical_base_debt(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            init_repo(root)
            target = root / "docs/90.references/debt.md"
            target.parent.mkdir(parents=True)
            target.write_text("# Existing debt\n", encoding="utf-8")
            baseline = commit_all(root)
            records = tuple(metadata.collect_records(root, self.profiles, require_git=True))
            findings = lifecycle._introduced_metadata_findings(
                root, records, records, self.profiles, base_ref=baseline
            )
            self.assertEqual(findings, [])

    def test_manifest_attestation_binds_baseline_transition_and_result_truth(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = pathlib.Path(temporary.name)
        init_repo(root)
        source = root / "docs/90.references/source.md"
        source.parent.mkdir(parents=True)
        source.write_text(
            "---\nstatus: active\nartifact_id: reference:source\n"
            "artifact_type: reference\nparent_ids: []\n---\n\n# Source\n",
            encoding="utf-8",
        )
        baseline = commit_all(root)
        source.write_text(
            "---\nstatus: completed\nartifact_id: reference:source\n"
            "artifact_type: reference\nparent_ids: []\n---\n\n# Source\n",
            encoding="utf-8",
        )
        row = self.valid_row(
            source_path=pathlib.PurePosixPath("docs/90.references/source.md"),
            target_path=pathlib.PurePosixPath("docs/90.references/source.md"),
            artifact_id="reference:source",
            artifact_type="reference",
            status_before="active",
            status_after="completed",
        )
        contract = self.fixture_contract(["docs/90.references/source.md"])

        valid = lifecycle.validate_migration_manifest(
            root, self.profiles, contract, self.document(baseline, entries=(row,))
        )
        binding_codes = {item.code for item in valid}
        self.assertFalse(any("mismatch" in code or "transition" in code for code in binding_codes))

        cases = {
            "baseline-id": (
                dataclasses.replace(row, artifact_id="reference:other"),
                "manifest-baseline-artifact-id-mismatch",
            ),
            "baseline-status": (
                dataclasses.replace(row, status_before="draft"),
                "manifest-baseline-status-mismatch",
            ),
            "reverse-transition": (
                dataclasses.replace(row, status_before="completed", status_after="active"),
                "manifest-transition-invalid",
            ),
            "result-id": (
                row,
                "manifest-target-artifact-id-mismatch",
            ),
        }
        for name, (candidate, expected) in cases.items():
            with self.subTest(case=name):
                if name == "result-id":
                    source.write_text(
                        source.read_text(encoding="utf-8").replace(
                            "reference:source", "reference:other"
                        ),
                        encoding="utf-8",
                    )
                findings = lifecycle.validate_migration_manifest(
                    root,
                    self.profiles,
                    contract,
                    self.document(baseline, entries=(candidate,)),
                )
                self.assertIn(expected, {item.code for item in findings})
                if name == "result-id":
                    source.write_text(
                        source.read_text(encoding="utf-8").replace(
                            "reference:other", "reference:source"
                        ),
                        encoding="utf-8",
                    )

        missing_target = dataclasses.replace(
            row,
            target_path=pathlib.PurePosixPath("docs/90.references/moved.md"),
            disposition="move",
        )
        self.assertIn(
            "manifest-target-missing",
            {
                item.code
                for item in lifecycle.validate_migration_manifest(
                    root,
                    self.profiles,
                    contract,
                    self.document(baseline, entries=(missing_target,)),
                )
            },
        )

        delete = dataclasses.replace(row, target_path=None, disposition="delete")
        self.assertIn(
            "manifest-source-result-present",
            {
                item.code
                for item in lifecycle.validate_migration_manifest(
                    root,
                    self.profiles,
                    contract,
                    self.document(baseline, entries=(delete,)),
                )
            },
        )

    def test_manifest_attestation_allows_legitimate_nullable_readme_profile(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            init_repo(root)
            (root / "README.md").write_text("# Readme\n", encoding="utf-8")
            baseline = commit_all(root)
            row = self.valid_row(
                source_path=pathlib.PurePosixPath("README.md"),
                target_path=pathlib.PurePosixPath("README.md"),
                artifact_id=None,
                artifact_type="readme",
                status_before=None,
                status_after=None,
            )
            findings = lifecycle.validate_migration_manifest(
                root,
                self.profiles,
                self.fixture_contract(["README.md"]),
                self.document(baseline, entries=(row,)),
            )
            self.assertNotIn("manifest-static-invalid", {item.code for item in findings})
            self.assertFalse(any("mismatch" in item.code for item in findings))

    def test_check_full_blocks_warnings_and_safety_is_unsuppressible(self) -> None:
        warning = lifecycle._finding(
            "docs/90.references/debt.md",
            "review-age-unavailable",
            "review evidence is unavailable",
            "warning",
        )
        safety = lifecycle._finding(
            "docs/98.archive/value.md",
            "archive-snapshot-path-mismatch",
            "snapshot path is invalid",
        )
        with mock.patch.object(lifecycle, "_full_findings", return_value=((), [warning])):
            self.assertEqual(lifecycle.main(["--mode", "report-full"]), 0)
            self.assertEqual(lifecycle.main(["--mode", "check-full"]), 1)

        with tempfile.TemporaryDirectory() as directory:
            exceptions = pathlib.Path(directory) / "exceptions.yaml"
            entry = ExceptionValidationTests.valid(self)
            entry["finding_code"] = "archive-snapshot-path-mismatch"
            entry["scope_paths"] = ["docs/98.archive/value.md"]
            exceptions.write_text(
                yaml.safe_dump(
                    {"schema_version": 1, "exceptions": [entry]}, sort_keys=False
                ),
                encoding="utf-8",
            )
            with mock.patch.object(
                lifecycle, "_full_findings", return_value=((), [safety])
            ):
                self.assertEqual(
                    lifecycle.main(
                        [
                            "--mode",
                            "check-full",
                            "--exceptions",
                            str(exceptions),
                        ]
                    ),
                    3,
                )
            self.assertTrue(lifecycle._is_safety_finding(safety))

    def test_redaction_covers_all_contract_payload_classes_and_parser_errors(self) -> None:
        samples = (
            b"machine host.example login user password do-not-echo-auth\n",
            b'{"auths":{"registry":{"auth":"do-not-echo-auth"}}}\n',
            b"-----BEGIN ENCRYPTED PRIVATE KEY-----\ndo-not-echo-key\n",
            b"-----BEGIN DSA PRIVATE KEY-----\ndo-not-echo-key\n",
            b"-----BEGIN PGP PRIVATE KEY BLOCK-----\ndo-not-echo-key\n",
            b"sk-do-not-echo-token-1234567890\n",
            b"ghp_do_not_echo_token_1234567890\n",
            b'{"timestamp":"2026-07-14T10:00:00Z","level":"error","message":"do-not-echo-log"}\n',
            b'{"level":"error","message":"do-not-echo-log","timestamp":"2026-07-14T10:00:00Z"}\n',
        )
        for sample in samples:
            with self.subTest(sample=sample.splitlines()[0][:24]):
                self.assertTrue(
                    any(pattern.search(sample) for pattern in lifecycle.SENSITIVE_PAYLOAD_PATTERNS)
                )

        marker = "do-not-echo-yaml-payload"
        with tempfile.TemporaryDirectory() as directory:
            contract = pathlib.Path(directory) / "contract.yaml"
            contract.write_text(f"schema_version: [{marker}\n", encoding="utf-8")
            result = run(
                sys.executable,
                str(SCRIPT),
                "--mode",
                "check-contract",
                "--contract",
                str(contract),
                cwd=ROOT,
            )
            self.assertEqual(result.returncode, 3)
            self.assertNotIn(marker, result.stdout + result.stderr)
            self.assertNotIn("Traceback", result.stderr)
            self.assertIn("configuration-error", result.stderr)

    def test_snapshot_and_manifest_symlinks_cannot_escape_repository(self) -> None:
        temporary, root, record, payload = ArchiveProvenanceTests.archive_fixture(
            self, "immutable-snapshot"
        )
        self.addCleanup(temporary.cleanup)
        snapshot = root / str(record.metadata["snapshot_path"])
        outside = root.parent / f"{root.name}-outside-snapshot"
        outside.write_bytes(payload)
        self.addCleanup(lambda: outside.unlink(missing_ok=True))
        snapshot.unlink()
        snapshot.symlink_to(outside)
        self.assertIn(
            "archive-snapshot-file-invalid",
            {item.code for item in lifecycle.validate_archive_provenance(root, record)},
        )

        manifest_root = root / "manifest-fixture"
        manifest_root.mkdir()
        init_repo(manifest_root)
        source = manifest_root / "docs/03.specs/source.md"
        source.parent.mkdir(parents=True)
        source.write_text(
            "---\nstatus: active\nartifact_id: spec:source\n"
            "artifact_type: spec\nparent_ids: []\n---\n\n# Source\n",
            encoding="utf-8",
        )
        baseline = commit_all(manifest_root, "manifest baseline")
        manifest_relative = "docs/90.references/manifests/foundation.yaml"
        manifest = manifest_root / manifest_relative
        manifest.parent.mkdir(parents=True)
        manifest.write_text(
            lifecycle.render_migration_manifest(
                self.document(baseline, entries=(self.valid_row(),))
            ),
            encoding="utf-8",
        )
        commit_all(manifest_root, "track manifest fixture")
        outside_manifest = root.parent / f"{root.name}-outside-manifest"
        outside_manifest.write_bytes(manifest.read_bytes())
        self.addCleanup(lambda: outside_manifest.unlink(missing_ok=True))
        manifest.unlink()
        manifest.symlink_to(outside_manifest)
        with self.assertRaises(lifecycle.ProfileError):
            lifecycle._load_repo_migration_manifest(manifest_root, manifest_relative)
        with self.assertRaises(lifecycle.ProfileError):
            lifecycle._repo_manifest_path(manifest_root, outside_manifest)
        with self.assertRaises(lifecycle.ProfileError):
            lifecycle._repo_manifest_path(
                manifest_root,
                pathlib.Path("../escape.yaml"),
            )
        self.assertIsNone(
            lifecycle._read_regular_repo_bytes(
                manifest_root,
                "../escape.yaml",
                require_tracked=False,
            )
        )

        manifest.unlink()
        manifest_directory = manifest.parent
        manifest_directory.rmdir()
        outside_manifest_directory = root.parent / f"{root.name}-outside-manifest-dir"
        outside_manifest_directory.mkdir()
        self.addCleanup(
            lambda: shutil.rmtree(outside_manifest_directory, ignore_errors=True)
        )
        (outside_manifest_directory / manifest.name).write_bytes(
            outside_manifest.read_bytes()
        )
        manifest_directory.symlink_to(
            outside_manifest_directory,
            target_is_directory=True,
        )
        with self.assertRaises(lifecycle.ProfileError):
            lifecycle._load_repo_migration_manifest(manifest_root, manifest_relative)

        snapshot.unlink()
        evidence_dir = snapshot.parent
        evidence_dir.rmdir()
        outside_dir = root.parent / f"{root.name}-outside-dir"
        outside_dir.mkdir()
        self.addCleanup(lambda: shutil.rmtree(outside_dir, ignore_errors=True))
        (outside_dir / snapshot.name).write_bytes(payload)
        evidence_dir.symlink_to(outside_dir, target_is_directory=True)
        self.assertIn(
            "archive-snapshot-file-invalid",
            {item.code for item in lifecycle.validate_archive_provenance(root, record)},
        )

    def test_unicode_title_normalization_preserves_multilingual_alphanumerics(self) -> None:
        pairs = (
            ("# 운영 가이드\n", "# 운영-가이드\n"),
            ("# Café Guide\n", "# CAFE\u0301-guide\n"),
        )
        for index, (left_body, right_body) in enumerate(pairs):
            with self.subTest(index=index), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                left = root / f"docs/90.references/{index}-left.md"
                right = root / f"docs/90.references/{index}-right.md"
                left.parent.mkdir(parents=True)
                left.write_text(left_body, encoding="utf-8")
                right.write_text(right_body, encoding="utf-8")
                records = (
                    self.record(left.relative_to(root).as_posix(), "reference"),
                    self.record(right.relative_to(root).as_posix(), "reference"),
                )
                candidates = lifecycle.find_duplicate_candidates(root, records)
                self.assertEqual(len(candidates), 1)
                self.assertIn("normalized-title", candidates[0].signals)

    def test_declared_manifests_load_in_registry_order_and_fail_before_use(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            first_path = "docs/90.references/manifests/zeta.yaml"
            second_path = "docs/90.references/manifests/alpha.yaml"
            for path_text in (first_path, second_path):
                target = root / path_text
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("fixture\n", encoding="utf-8")
            contract = self.fixture_contract(
                ["docs/03.specs/source.md"],
                wave="zeta",
                manifest_path=first_path,
            )
            contract["waves"]["alpha"] = {
                "enforcement": "advisory",
                "manifest_path": second_path,
                "scope_state": "approved",
                "source_paths": ["docs/03.specs/source.md"],
                "declared_outputs": [],
            }
            first = self.document("a" * 40, wave="zeta")
            calls: list[str] = []

            def load_declared(
                _root: pathlib.Path,
                relative_path: str,
            ) -> lifecycle.MigrationManifestDocument:
                calls.append(relative_path)
                if relative_path == second_path:
                    raise lifecycle.ProfileError("invalid declared manifest")
                return first

            with (
                mock.patch.object(
                    lifecycle,
                    "_load_repo_migration_manifest",
                    side_effect=load_declared,
                ),
                mock.patch.object(
                    lifecycle,
                    "validate_migration_manifest",
                    return_value=[],
                ),
                mock.patch.object(
                    lifecycle,
                    "_repo_manifest_matches",
                    return_value=True,
                ),
            ):
                documents, findings = lifecycle._load_declared_manifests(
                    root,
                    self.profiles,
                    contract,
                    promoted_only=False,
                )
            self.assertEqual(calls, [first_path, second_path])
            self.assertEqual(documents, (first,))
            self.assertIn(
                "promoted-manifest-file-invalid",
                {item.code for item in findings},
            )

        safety = lifecycle._finding(
            second_path,
            "promoted-manifest-file-invalid",
            "declared manifest is invalid",
        )
        with (
            mock.patch.object(
                lifecycle,
                "_load_declared_manifests",
                return_value=((), [safety]),
            ),
            mock.patch.object(lifecycle, "_collect_records") as collect_records,
            contextlib.redirect_stdout(io.StringIO()),
        ):
            self.assertEqual(
                lifecycle.main(["--mode", "check-impacted", "--base-ref", "HEAD"]),
                3,
            )
        collect_records.assert_not_called()

    def test_all_sixteen_modes_have_table_driven_shape_contracts(self) -> None:
        valid_arguments: dict[str, list[str]] = {
            "check-contract": [],
            "generate-manifest": ["--wave", "foundation", "--base-ref", "HEAD", "--output", "out"],
            "check-manifest": ["--wave", "foundation", "--manifest", "manifest"],
            "check-promoted": [],
            "generate-summary": ["--manifest", "manifest", "--output", "out"],
            "check-summary": ["--manifest", "manifest", "--output", "out"],
            "check-impacted": ["--base-ref", "HEAD"],
            "report-duplicates": ["--output", "out"],
            "report-full": [],
            "check-full": [],
            "check-archive": [],
            "check-directory-budget": [],
            "generate-archive-ledger": ["--output", "out"],
            "check-archive-ledger": ["--output", "out"],
            "generate-snapshot-manifest": ["--output", "out"],
            "check-snapshot-manifest": ["--output", "out"],
        }
        self.assertEqual(tuple(valid_arguments), lifecycle.MODES)
        for mode, extra in valid_arguments.items():
            with self.subTest(mode=mode):
                parser = lifecycle._parser()
                args = parser.parse_args(["--mode", mode, *extra])
                lifecycle._validate_cli_shape(parser, args)
                if extra:
                    broken = ["--mode", mode, *extra[2:]]
                elif mode in {"check-promoted", "check-archive"}:
                    broken = ["--mode", mode, "--base-ref", "HEAD"]
                else:
                    broken = ["--mode", mode, "--wave", "forbidden"]
                with self.assertRaises(SystemExit) as raised:
                    parser = lifecycle._parser()
                    with contextlib.redirect_stderr(io.StringIO()):
                        lifecycle._validate_cli_shape(parser, parser.parse_args(broken))
                self.assertEqual(raised.exception.code, 2)

    def test_all_sixteen_modes_have_success_and_write_boundary_matrix(self) -> None:
        mode_contracts: dict[str, tuple[list[str], bool]] = {
            "check-contract": ([], False),
            "generate-manifest": (
                ["--wave", "fixture", "--base-ref", "HEAD", "--output", "{output}"],
                True,
            ),
            "check-manifest": (
                ["--wave", "fixture", "--manifest", "docs/manifest.yaml"],
                False,
            ),
            "check-promoted": ([], False),
            "generate-summary": (
                ["--manifest", "docs/manifest.yaml", "--output", "{output}"],
                True,
            ),
            "check-summary": (
                ["--manifest", "docs/manifest.yaml", "--output", "{output}"],
                False,
            ),
            "check-impacted": (["--base-ref", "HEAD"], False),
            "report-duplicates": (["--output", "{output}"], True),
            "report-full": ([], False),
            "check-full": ([], False),
            "check-archive": ([], False),
            "check-directory-budget": ([], False),
            "generate-archive-ledger": (["--output", "{output}"], True),
            "check-archive-ledger": (["--output", "{output}"], False),
            "generate-snapshot-manifest": (["--output", "{output}"], True),
            "check-snapshot-manifest": (["--output", "{output}"], False),
        }
        self.assertEqual(tuple(mode_contracts), lifecycle.MODES)
        write_modes = {mode for mode, (_, writes) in mode_contracts.items() if writes}
        self.assertEqual(
            write_modes,
            {
                "generate-manifest",
                "generate-summary",
                "report-duplicates",
                "generate-archive-ledger",
                "generate-snapshot-manifest",
            },
        )
        contract = copy.deepcopy(self.contract)
        document = self.document("a" * 40)
        for mode, (raw_extra, writes) in mode_contracts.items():
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                output = root / f"{mode}.out"
                extra = [value.format(output=output) for value in raw_extra]
                if "--output" in extra and not writes:
                    output.write_bytes(b"sentinel")
                with (
                    mock.patch.object(
                        lifecycle,
                        "load_migration_contract",
                        return_value=contract,
                    ),
                    mock.patch.object(
                        lifecycle.metadata,
                        "load_profiles",
                        return_value=self.profiles,
                    ),
                    mock.patch.object(
                        lifecycle,
                        "_generate_manifest_skeleton",
                        return_value=document,
                    ),
                    mock.patch.object(
                        lifecycle,
                        "_load_candidate_migration_manifest",
                        return_value=document,
                    ),
                    mock.patch.object(
                        lifecycle,
                        "validate_migration_manifest",
                        return_value=[],
                    ),
                    mock.patch.object(
                        lifecycle,
                        "_candidate_manifest_matches",
                        return_value=True,
                    ),
                    mock.patch.object(
                        lifecycle,
                        "_load_declared_manifests",
                        return_value=((), []),
                    ),
                    mock.patch.object(lifecycle, "_collect_records", return_value=()),
                    mock.patch.object(
                        lifecycle,
                        "collect_impacted_records",
                        return_value=(),
                    ),
                    mock.patch.object(
                        lifecycle,
                        "_introduced_metadata_findings",
                        return_value=[],
                    ),
                    mock.patch.object(
                        lifecycle,
                        "_added_record_paths",
                        return_value=frozenset(),
                    ),
                    mock.patch.object(
                        lifecycle,
                        "_full_findings",
                        return_value=((), []),
                    ),
                    mock.patch.object(
                        lifecycle,
                        "validate_directory_budgets",
                        return_value=[],
                    ),
                    mock.patch.object(
                        lifecycle,
                        "find_duplicate_candidates",
                        return_value=(),
                    ),
                    mock.patch.object(lifecycle, "_check_output", return_value=True),
                    contextlib.redirect_stdout(io.StringIO()),
                    contextlib.redirect_stderr(io.StringIO()),
                ):
                    result = lifecycle.main(
                        ["--root", str(root), "--mode", mode, *extra]
                    )
                self.assertEqual(result, 0)
                if writes:
                    self.assertTrue(output.is_file())
                elif "--output" in extra:
                    self.assertEqual(output.read_bytes(), b"sentinel")
                else:
                    self.assertFalse(output.exists())

    def test_all_sixteen_modes_have_explicit_exit_class_matrix(self) -> None:
        arguments = {
            "check-contract": [],
            "generate-manifest": [
                "--wave",
                "fixture",
                "--base-ref",
                "HEAD",
                "--output",
                "{output}",
            ],
            "check-manifest": [
                "--wave",
                "fixture",
                "--manifest",
                "docs/manifest.yaml",
            ],
            "check-promoted": [],
            "generate-summary": [
                "--manifest",
                "docs/manifest.yaml",
                "--output",
                "{output}",
            ],
            "check-summary": [
                "--manifest",
                "docs/manifest.yaml",
                "--output",
                "{output}",
            ],
            "check-impacted": ["--base-ref", "HEAD"],
            "report-duplicates": ["--output", "{output}"],
            "report-full": [],
            "check-full": [],
            "check-archive": [],
            "check-directory-budget": [],
            "generate-archive-ledger": ["--output", "{output}"],
            "check-archive-ledger": ["--output", "{output}"],
            "generate-snapshot-manifest": ["--output", "{output}"],
            "check-snapshot-manifest": ["--output", "{output}"],
        }
        ordinary_exits = {
            "check-contract": 0,
            "generate-manifest": 0,
            "check-manifest": 1,
            "check-promoted": 1,
            "generate-summary": 1,
            "check-summary": 1,
            "check-impacted": 1,
            "report-duplicates": 0,
            "report-full": 0,
            "check-full": 1,
            "check-archive": 1,
            "check-directory-budget": 1,
            "generate-archive-ledger": 1,
            "check-archive-ledger": 1,
            "generate-snapshot-manifest": 1,
            "check-snapshot-manifest": 1,
        }
        self.assertEqual(tuple(arguments), lifecycle.MODES)
        self.assertEqual(tuple(ordinary_exits), lifecycle.MODES)
        contract = copy.deepcopy(self.contract)
        document = self.document("a" * 40)
        archive = self.record("docs/98.archive/item.md", "archive")

        for mode in lifecycle.MODES:
            for safety_case in (False, True):
                with (
                    self.subTest(mode=mode, safety=safety_case),
                    tempfile.TemporaryDirectory() as directory,
                    contextlib.ExitStack() as stack,
                ):
                    root = pathlib.Path(directory)
                    output = root / f"{mode}.out"
                    extra = [
                        value.format(output=output) for value in arguments[mode]
                    ]
                    finding = (
                        lifecycle._finding(
                            archive.path.as_posix(),
                            "archive-snapshot-file-invalid",
                            "safety failure",
                        )
                        if safety_case
                        else lifecycle._finding(
                            archive.path.as_posix(),
                            "directory-budget-blocked",
                            "ordinary blocking finding",
                        )
                    )
                    if mode == "check-contract" and safety_case:
                        stack.enter_context(
                            mock.patch.object(
                                lifecycle,
                                "load_migration_contract",
                                side_effect=lifecycle.ProfileError("invalid contract"),
                            )
                        )
                    else:
                        stack.enter_context(
                            mock.patch.object(
                                lifecycle,
                                "load_migration_contract",
                                return_value=contract,
                            )
                        )
                    stack.enter_context(
                        mock.patch.object(
                            lifecycle.metadata,
                            "load_profiles",
                            return_value=self.profiles,
                        )
                    )
                    if mode == "generate-manifest" and safety_case:
                        stack.enter_context(
                            mock.patch.object(
                                lifecycle,
                                "_generate_manifest_skeleton",
                                side_effect=lifecycle.ProfileError("unsafe baseline"),
                            )
                        )
                    else:
                        stack.enter_context(
                            mock.patch.object(
                                lifecycle,
                                "_generate_manifest_skeleton",
                                return_value=document,
                            )
                        )
                    stack.enter_context(
                        mock.patch.object(
                            lifecycle,
                            "_load_candidate_migration_manifest",
                            return_value=document,
                        )
                    )
                    stack.enter_context(
                        mock.patch.object(
                            lifecycle,
                            "validate_migration_manifest",
                            return_value=[finding],
                        )
                    )
                    stack.enter_context(
                        mock.patch.object(
                            lifecycle,
                            "_candidate_manifest_matches",
                            return_value=True,
                        )
                    )
                    stack.enter_context(
                        mock.patch.object(
                            lifecycle,
                            "_load_declared_manifests",
                            return_value=((), [finding]),
                        )
                    )
                    stack.enter_context(
                        mock.patch.object(
                            lifecycle,
                            "_full_findings",
                            return_value=((archive,), [finding]),
                        )
                    )
                    stack.enter_context(
                        mock.patch.object(
                            lifecycle,
                            "validate_archive_provenance",
                            return_value=[finding],
                        )
                    )
                    stack.enter_context(
                        mock.patch.object(
                            lifecycle,
                            "validate_directory_budgets",
                            return_value=[finding],
                        )
                    )
                    stack.enter_context(
                        mock.patch.object(lifecycle, "_check_output", return_value=True)
                    )
                    stack.enter_context(contextlib.redirect_stdout(io.StringIO()))
                    stack.enter_context(contextlib.redirect_stderr(io.StringIO()))
                    result = lifecycle.main(
                        ["--root", str(root), "--mode", mode, *extra]
                    )
                    expected = 3 if safety_case else ordinary_exits[mode]
                    self.assertEqual(result, expected)


class FinalReviewRemediationTests(LifecycleTestCase):
    def record(
        self,
        path: str,
        artifact_type: str = "task",
        **metadata_values: object,
    ) -> metadata.Record:
        values: dict[str, object] = {
            "status": "active",
            "artifact_id": f"{artifact_type}:{pathlib.PurePosixPath(path).stem}",
            "artifact_type": artifact_type,
            "parent_ids": [],
        }
        values.update(metadata_values)
        return metadata.Record(pathlib.Path(path), values, artifact_type)

    def _invoke_corpus_mode(
        self,
        root: pathlib.Path,
        mode: str,
        output: pathlib.Path,
    ) -> subprocess.CompletedProcess[str]:
        if mode == "check-impacted":
            return self.run_isolated_impacted_cli(root, base_ref="HEAD")
        arguments = [
            sys.executable,
            str(SCRIPT),
            "--root",
            str(root),
            "--mode",
            mode,
        ]
        if mode in {
            "report-duplicates",
            "generate-archive-ledger",
            "check-archive-ledger",
            "generate-snapshot-manifest",
            "check-snapshot-manifest",
        }:
            arguments.extend(("--output", str(output)))
        return run(*arguments, cwd=ROOT)

    def test_corpus_modes_reject_final_and_intermediate_markdown_symlinks_without_leakage(
        self,
    ) -> None:
        marker = "outside-corpus-payload-marker"
        modes = (
            "report-full",
            "check-full",
            "report-duplicates",
            "check-impacted",
            "check-archive",
            "generate-archive-ledger",
            "check-archive-ledger",
            "generate-snapshot-manifest",
            "check-snapshot-manifest",
        )
        for attack in ("final", "intermediate"):
            with self.subTest(attack=attack), tempfile.TemporaryDirectory() as directory:
                fixture = pathlib.Path(directory)
                root = fixture / "repository"
                outside = fixture / "outside"
                root.mkdir()
                outside.mkdir()
                init_repo(root)
                outside_body = (
                    "---\nstatus: active\nartifact_id: reference:outside\n"
                    f"artifact_type: reference\nparent_ids: [{marker}]\n---\n\n# Outside\n"
                )
                relative = pathlib.PurePosixPath(
                    "docs/90.references/link.md"
                    if attack == "final"
                    else "docs/90.references/nested/link.md"
                )
                target = root / relative
                target.parent.mkdir(parents=True)
                if attack == "final":
                    outside_file = outside / "link.md"
                    outside_file.write_text(outside_body, encoding="utf-8")
                    target.symlink_to(outside_file)
                    commit_all(root, "track final symlink")
                else:
                    target.write_text("# Safe baseline\n", encoding="utf-8")
                    commit_all(root, "track regular file")
                    shutil.rmtree(target.parent)
                    (outside / "link.md").write_text(outside_body, encoding="utf-8")
                    target.parent.symlink_to(outside, target_is_directory=True)

                for mode in modes:
                    with self.subTest(attack=attack, mode=mode):
                        output = fixture / f"{attack}-{mode}.out"
                        check_mode = mode.startswith("check-") and mode.endswith(
                            ("ledger", "manifest")
                        )
                        if check_mode:
                            output.write_bytes(b"sentinel")
                        result = self._invoke_corpus_mode(root, mode, output)
                        rendered = result.stdout + result.stderr
                        self.assertEqual(result.returncode, 3, rendered)
                        self.assertNotIn(marker, rendered)
                        self.assertNotIn("Traceback", rendered)
                        if check_mode:
                            self.assertEqual(output.read_bytes(), b"sentinel")
                        else:
                            self.assertFalse(output.exists())

    def _archive_fixture(
        self,
    ) -> tuple[
        tempfile.TemporaryDirectory[str],
        pathlib.Path,
        str,
        lifecycle.MigrationManifestRow,
        pathlib.Path,
    ]:
        temporary = tempfile.TemporaryDirectory()
        root = pathlib.Path(temporary.name)
        init_repo(root)
        source_relative = pathlib.PurePosixPath(
            "docs/90.references/ref-9999-source.md"
        )
        source = root / source_relative
        source.parent.mkdir(parents=True)
        source.write_text(
            "---\nstatus: active\nartifact_id: ref-9999\n"
            "artifact_type: reference\nparent_ids: []\n---\n\n# Source\n",
            encoding="utf-8",
        )
        baseline = commit_all(root, "archive source baseline")
        blob = git(root, "rev-parse", f"{baseline}:{source_relative.as_posix()}")
        source.unlink()
        replacement = root / "docs/90.references/data/replacement.md"
        replacement.parent.mkdir(parents=True, exist_ok=True)
        replacement.write_text(
            "---\nstatus: active\nartifact_id: reference:replacement\n"
            "artifact_type: reference\nparent_ids: []\n---\n\n"
            "# Replacement\n\n## Overview\nCurrent replacement.\n\n"
            "## Purpose\nCanonical replacement.\n\n## Scope\nCurrent scope.\n\n"
            "## Definitions / Facts\nReplacement truth.\n\n"
            "## Sources\nRepository evidence.\n\n## Maintenance\nActive.\n\n"
            "## Related Documents\nNone.\n",
            encoding="utf-8",
        )
        commit_all(root, "track canonical replacement")
        target_relative = pathlib.PurePosixPath(
            "docs/98.archive/tombstones/05.operations/ref-9999-source.md"
        )
        target = root / target_relative
        target.parent.mkdir(parents=True)
        archive_metadata: dict[str, object] = {
            "status": "archived",
            "artifact_id": "ref-9999",
            "artifact_type": "archive",
            "parent_ids": [],
            "archived_from": source_relative.as_posix(),
            "archived_at": "2026-07-14",
            "archive_reason": "Superseded by the canonical replacement.",
            "archive_disposition": "superseded",
            "archived_commit": baseline,
            "archived_blob": blob,
            "preservation_class": "git-history",
            "current_replacement": "docs/90.references/data/replacement.md",
        }
        target.write_text(
            "---\n"
            + yaml.safe_dump(archive_metadata, sort_keys=False)
            + "---\n\n# Archived Source\n",
            encoding="utf-8",
        )
        row = self.valid_row(
            source_path=source_relative,
            target_path=target_relative,
            artifact_id="ref-9999",
            artifact_type="reference",
            status_before="active",
            status_after="archived",
            parent_ids=(),
            disposition="archive",
            canonical_replacement="docs/90.references/data/replacement.md",
            active_consumers=(),
            preservation_class="git-history",
            evidence=lifecycle.ManifestEvidence(
                ("git show baseline source",),
                (source_relative.as_posix(),),
                (source_relative,),
                ("verified no active consumers",),
                ("revert archive commit",),
            ),
            review_verdict=lifecycle.ReviewVerdict("pass", "pass"),
        )
        return temporary, root, baseline, row, target

    def _archive_codes(
        self,
        root: pathlib.Path,
        baseline: str,
        row: lifecycle.MigrationManifestRow,
    ) -> set[str]:
        return {
            item.code
            for item in lifecycle.validate_migration_manifest(
                root,
                self.profiles,
                self.fixture_contract([row.source_path.as_posix()]),
                self.document(baseline, entries=(row,)),
            )
        }

    def test_archive_disposition_binds_source_to_canonical_validated_tombstone(
        self,
    ) -> None:
        temporary, root, baseline, row, target = self._archive_fixture()
        self.addCleanup(temporary.cleanup)
        self.assertEqual(self._archive_codes(root, baseline, row), set())

        original = yaml.safe_load(target.read_text(encoding="utf-8").split("---", 2)[1])
        cases: dict[str, tuple[dict[str, object], lifecycle.MigrationManifestRow, str]] = {
            "source": (
                {"archived_from": "docs/90.references/other.md"},
                row,
                "manifest-archive-source-mismatch",
            ),
            "type": (
                {"artifact_type": "reference"},
                row,
                "manifest-archive-target-profile-invalid",
            ),
            "status": (
                {"status": "active"},
                dataclasses.replace(row, status_after="active"),
                "manifest-archive-status-invalid",
            ),
            "parents": (
                {"parent_ids": ["reference:parent"]},
                row,
                "manifest-target-parent-ids-mismatch",
            ),
            "replacement": (
                {"current_replacement": "docs/90.references/other.md"},
                row,
                "manifest-archive-replacement-mismatch",
            ),
            "preservation": (
                {"preservation_class": "immutable-snapshot"},
                row,
                "manifest-archive-preservation-mismatch",
            ),
            "reviews": (
                {},
                dataclasses.replace(
                    row,
                    review_verdict=lifecycle.ReviewVerdict("pending", "pending"),
                ),
                "manifest-destructive-review-required",
            ),
        }
        for name, (changes, candidate, expected) in cases.items():
            with self.subTest(case=name):
                target_metadata = {**original, **changes}
                target.write_text(
                    "---\n"
                    + yaml.safe_dump(target_metadata, sort_keys=False)
                    + "---\n\n# Archived Source\n",
                    encoding="utf-8",
                )
                codes = self._archive_codes(root, baseline, candidate)
                self.assertIn(expected, codes)
                if name != "reviews":
                    self.assertIn("manifest-transition-invalid", codes)
        target.write_text(
            "---\n" + yaml.safe_dump(original, sort_keys=False) + "---\n",
            encoding="utf-8",
        )
        non_archive = dataclasses.replace(
            row,
            source_path=row.target_path,
            target_path=row.target_path,
            artifact_type="archive",
            status_before="archived",
            status_after="active",
            disposition="preserve",
            canonical_replacement=None,
            preservation_class=None,
            evidence=lifecycle.ManifestEvidence((), (), (), (), ()),
            review_verdict=lifecycle.ReviewVerdict("pending", "pending"),
        )
        reverse_contract = self.fixture_contract([non_archive.source_path.as_posix()])
        reverse_document = self.document(
            baseline,
            entries=(non_archive,),
        )
        reverse_contract["waves"]["fixture"]["source_paths"] = [
            non_archive.source_path.as_posix()
        ]
        reverse_codes = {
            item.code
            for item in lifecycle.validate_migration_manifest(
                root, self.profiles, reverse_contract, reverse_document
            )
        }
        self.assertIn("manifest-transition-invalid", reverse_codes)

    def test_archive_binds_manifest_baseline_blob_and_dynamic_replacement_truth(self) -> None:
        temporary, root, baseline, row, target = self._archive_fixture()
        self.addCleanup(temporary.cleanup)
        original_text = target.read_text(encoding="utf-8")
        original = yaml.safe_load(original_text.split("---", 2)[1])

        archived_bytes = run(
            "git",
            "cat-file",
            "blob",
            str(original["archived_blob"]),
            cwd=root,
        ).stdout.encode("utf-8")
        digest = hashlib.sha256(archived_bytes).hexdigest()
        snapshot_relative = pathlib.PurePosixPath(
            f"docs/98.archive/evidence/{digest}.md.snapshot"
        )
        snapshot = root / snapshot_relative
        snapshot.parent.mkdir(parents=True, exist_ok=True)
        snapshot.write_bytes(archived_bytes)
        immutable_values = {
            **original,
            "archive_disposition": "evidence-preserve",
            "preservation_class": "immutable-snapshot",
            "snapshot_path": snapshot_relative.as_posix(),
            "content_sha256": digest,
            "snapshot_reason": "Preserve exact evidence bytes.",
        }
        target.write_text(
            "---\n"
            + yaml.safe_dump(immutable_values, sort_keys=False)
            + "---\n\n# Archived Source\n",
            encoding="utf-8",
        )
        commit_all(root, "track immutable archive snapshot")
        immutable_row = dataclasses.replace(
            row, preservation_class="immutable-snapshot"
        )
        self.assertEqual(self._archive_codes(root, baseline, immutable_row), set())
        target.write_text(original_text, encoding="utf-8")

        source_path = row.source_path.as_posix()
        newer_source = root / source_path
        newer_source.parent.mkdir(parents=True, exist_ok=True)
        newer_source.write_text(
            "---\nstatus: active\nartifact_id: ref-9999\n"
            "artifact_type: reference\nparent_ids: []\n---\n\n"
            "# Source\n\nUnique newer baseline evidence.\n",
            encoding="utf-8",
        )
        newer_baseline = commit_all(root, "newer source boundary")
        newer_source.unlink()
        git(root, "add", "-u")
        self.assertIn(
            "manifest-archive-baseline-blob-mismatch",
            self._archive_codes(root, newer_baseline, row),
        )
        self.assertNotIn(
            "manifest-archive-baseline-blob-mismatch",
            self._archive_codes(root, baseline, row),
        )

        variants = {
            "superseded": "docs/90.references/data/replacement.md",
            "duplicate": "docs/90.references/data/replacement.md",
            "conflict": "docs/90.references/data/replacement.md",
            "withdrawn": None,
            "evidence-preserve": None,
        }
        for disposition, replacement in variants.items():
            with self.subTest(disposition=disposition):
                values = {
                    **original,
                    "archive_disposition": disposition,
                }
                if replacement is None:
                    values.pop("current_replacement", None)
                else:
                    values["current_replacement"] = replacement
                target.write_text(
                    "---\n" + yaml.safe_dump(values, sort_keys=False) + "---\n\n# Archived Source\n",
                    encoding="utf-8",
                )
                candidate = dataclasses.replace(row, canonical_replacement=replacement)
                self.assertEqual(self._archive_codes(root, baseline, candidate), set())

        invalid = {
            "superseded": None,
            "duplicate": None,
            "conflict": None,
            "withdrawn": "docs/90.references/data/replacement.md",
        }
        for disposition, replacement in invalid.items():
            with self.subTest(invalid_disposition=disposition):
                values = {**original, "archive_disposition": disposition}
                if replacement is None:
                    values.pop("current_replacement", None)
                else:
                    values["current_replacement"] = replacement
                target.write_text(
                    "---\n" + yaml.safe_dump(values, sort_keys=False) + "---\n\n# Archived Source\n",
                    encoding="utf-8",
                )
                candidate = dataclasses.replace(row, canonical_replacement=replacement)
                codes = self._archive_codes(root, baseline, candidate)
                self.assertTrue(
                    {"manifest-replacement-required", "manifest-replacement-forbidden"}
                    & codes,
                    (disposition, codes),
                )

    def test_archive_replacement_resolves_unique_current_canonical_document(self) -> None:
        temporary, root, baseline, row, target = self._archive_fixture()
        self.addCleanup(temporary.cleanup)
        values = yaml.safe_load(target.read_text(encoding="utf-8").split("---", 2)[1])

        self.assertEqual(self._archive_codes(root, baseline, row), set())

        cases = {
            "missing": "docs/90.references/missing.md",
            "untracked": "docs/90.references/untracked.md",
            "self": row.source_path.as_posix(),
            "target": row.target_path.as_posix(),
        }
        (root / "docs/90.references/untracked.md").write_text(
            (root / "docs/90.references/data/replacement.md").read_text(encoding="utf-8")
            .replace("reference:replacement", "reference:untracked"),
            encoding="utf-8",
        )
        for name, replacement in cases.items():
            with self.subTest(case=name):
                values["current_replacement"] = replacement
                target.write_text(
                    "---\n" + yaml.safe_dump(values, sort_keys=False) + "---\n\n# Archived Source\n",
                    encoding="utf-8",
                )
                codes = self._archive_codes(
                    root,
                    baseline,
                    dataclasses.replace(row, canonical_replacement=replacement),
                )
                self.assertIn("manifest-replacement-invalid", codes)

        replacement_path = root / "docs/90.references/data/replacement.md"
        canonical = replacement_path.read_text(encoding="utf-8")
        outside = pathlib.Path(temporary.name).parent / (
            pathlib.Path(temporary.name).name + "-outside-replacement"
        )
        outside.write_text(canonical, encoding="utf-8")
        self.addCleanup(lambda: outside.unlink(missing_ok=True))
        replacement_path.unlink()
        replacement_path.symlink_to(outside)
        values["current_replacement"] = "docs/90.references/data/replacement.md"
        target.write_text(
            "---\n" + yaml.safe_dump(values, sort_keys=False) + "---\n\n# Archived Source\n",
            encoding="utf-8",
        )
        with self.assertRaises(lifecycle._CorpusSafetyError):
            self._archive_codes(root, baseline, row)
        replacement_path.unlink()
        replacement_path.write_text(canonical, encoding="utf-8")
        for name, mutation in {
            "wrong-profile": canonical.replace(
                "artifact_type: reference", "artifact_type: archive"
            ),
            "wrong-status": canonical.replace("status: active", "status: draft"),
            "wrong-body": canonical.replace("## Sources", "### Sources"),
        }.items():
            with self.subTest(case=name):
                replacement_path.write_text(mutation, encoding="utf-8")
                values["current_replacement"] = "docs/90.references/data/replacement.md"
                target.write_text(
                    "---\n" + yaml.safe_dump(values, sort_keys=False) + "---\n\n# Archived Source\n",
                    encoding="utf-8",
                )
                self.assertIn(
                    "manifest-replacement-invalid",
                    self._archive_codes(root, baseline, row),
                )
        replacement_path.write_text(canonical, encoding="utf-8")
        duplicate = root / "docs/90.references/data/duplicate.md"
        duplicate.parent.mkdir(parents=True, exist_ok=True)
        duplicate.write_text(canonical, encoding="utf-8")
        commit_all(root, "duplicate replacement identity")
        values["current_replacement"] = "reference:replacement"
        target.write_text(
            "---\n" + yaml.safe_dump(values, sort_keys=False) + "---\n\n# Archived Source\n",
            encoding="utf-8",
        )
        self.assertIn(
            "manifest-replacement-invalid",
            self._archive_codes(
                root,
                baseline,
                dataclasses.replace(
                    row, canonical_replacement="reference:replacement"
                ),
            ),
        )

    def _partition_fixture(
        self,
        *,
        plan_state: str,
        reviews: lifecycle.ReviewVerdict = lifecycle.ReviewVerdict("pass", "pass"),
    ) -> tuple[
        tempfile.TemporaryDirectory[str],
        pathlib.Path,
        str,
        lifecycle.MigrationManifestRow,
        tuple[metadata.Record, ...],
    ]:
        temporary = tempfile.TemporaryDirectory()
        root = pathlib.Path(temporary.name)
        init_repo(root)
        source_relative = pathlib.PurePosixPath(
            "docs/04.execution/tasks/149.md"
        )
        source = root / source_relative
        source.parent.mkdir(parents=True)
        source.write_text(
            "---\nstatus: active\nartifact_id: task:149\nartifact_type: task\n"
            "parent_ids: [plan:partition]\n---\n\n# Task: New Leaf\n",
            encoding="utf-8",
        )
        baseline = commit_all(root, "partition baseline")
        plan_relative = pathlib.PurePosixPath(
            "docs/04.execution/plans/2026-partition.md"
        )
        plan = root / plan_relative
        plan.parent.mkdir(parents=True, exist_ok=True)
        parent = root / "docs/03.specs/partition/spec.md"
        parent.parent.mkdir(parents=True, exist_ok=True)
        parent.write_text(
            "---\nstatus: active\nartifact_id: spec:partition\n"
            "artifact_type: spec\nparent_ids: [spec:root]\n---\n\n# Partition Spec\n",
            encoding="utf-8",
        )
        valid_plan = (
            "---\nstatus: active\nartifact_id: plan:partition\n"
            "artifact_type: plan\nparent_ids: [spec:partition]\n---\n\n"
            "# Document Partition Plan\n\n"
            "## Overview\nPartition approval.\n\n"
            "## Context and Inputs\nValidated corpus.\n\n"
            "## Goals and Non-goals\nBounded partition.\n\n"
            "## Work Breakdown\nApply the partition.\n\n"
            "## Verification Plan\nRun lifecycle validation.\n\n"
            "## Risks and Rollback\nRevert the migration commit.\n\n"
            "## Completion Criteria\nAll budgets pass.\n\n"
            "## Related Documents\nParent Spec.\n"
        )
        if plan_state == "missing":
            pass
        elif plan_state == "untracked":
            plan.write_text(valid_plan, encoding="utf-8")
        elif plan_state == "wrong-profile":
            plan.write_text(
                valid_plan.replace("artifact_type: plan", "artifact_type: spec"),
                encoding="utf-8",
            )
            commit_all(root, "track wrong-profile plan")
        elif plan_state == "draft":
            plan.write_text(
                valid_plan.replace("status: active", "status: draft"),
                encoding="utf-8",
            )
            commit_all(root, "track draft plan")
        elif plan_state in {"tracked", "symlink"}:
            plan.write_text(valid_plan, encoding="utf-8")
            commit_all(root, "track partition plan")
            if plan_state == "symlink":
                outside = pathlib.Path(temporary.name).parent / (
                    pathlib.Path(temporary.name).name + "-outside-plan"
                )
                outside.write_text("outside-plan-marker\n", encoding="utf-8")
                self.addCleanup(lambda: outside.unlink(missing_ok=True))
                plan.unlink()
                plan.symlink_to(outside)
        else:
            raise AssertionError(plan_state)
        row = self.valid_row(
            source_path=source_relative,
            target_path=source_relative,
            artifact_id="task:149",
            artifact_type="task",
            status_before="active",
            status_after="active",
            parent_ids=("plan:partition",),
            partition_plan=plan_relative,
            review_verdict=reviews,
        )
        records = tuple(
            self.record(
                f"docs/04.execution/tasks/{index:03}.md",
                "task",
                artifact_id=f"task:{index:03}",
            )
            for index in range(150)
        )
        return temporary, root, baseline, row, records

    def test_partition_approval_requires_tracked_canonical_reviewed_plan(self) -> None:
        cases = {
            "missing": "manifest-partition-plan-invalid",
            "untracked": "manifest-partition-plan-invalid",
            "symlink": "manifest-partition-plan-invalid",
            "wrong-profile": "manifest-partition-plan-profile-invalid",
            "draft": "manifest-partition-plan-status-invalid",
            "unreviewed": "manifest-partition-plan-review-required",
        }
        for name, expected in cases.items():
            state = "tracked" if name == "unreviewed" else name
            reviews = (
                lifecycle.ReviewVerdict("pending", "pending")
                if name == "unreviewed"
                else lifecycle.ReviewVerdict("pass", "pass")
            )
            temporary, root, baseline, row, records = self._partition_fixture(
                plan_state=state,
                reviews=reviews,
            )
            try:
                contract = self.fixture_contract([row.source_path.as_posix()])
                document = self.document(baseline, entries=(row,))
                codes = {
                    item.code
                    for item in lifecycle.validate_migration_manifest(
                        root, self.profiles, contract, document
                    )
                }
                self.assertIn(expected, codes, name)
                applied = lifecycle._apply_partition_approvals(
                    records,
                    (document,),
                    root=root,
                    profiles=self.profiles,
                )
                findings = lifecycle.validate_directory_budgets(
                    applied,
                    added_paths=frozenset(
                        {pathlib.PurePosixPath("docs/04.execution/tasks/149.md")}
                    ),
                    warning_at=100,
                    block_new_leaf_at=150,
                    enforce_all=False,
                )
                self.assertIn("directory-budget-blocked", {item.code for item in findings})
            finally:
                temporary.cleanup()

        temporary, root, baseline, row, records = self._partition_fixture(
            plan_state="tracked"
        )
        self.addCleanup(temporary.cleanup)
        contract = self.fixture_contract([row.source_path.as_posix()])
        document = self.document(baseline, entries=(row,))
        self.assertFalse(
            any(
                item.code.startswith("manifest-partition-plan-")
                for item in lifecycle.validate_migration_manifest(
                    root, self.profiles, contract, document
                )
            )
        )
        applied = lifecycle._apply_partition_approvals(
            records,
            (document,),
            root=root,
            profiles=self.profiles,
        )
        approved = lifecycle.validate_directory_budgets(
            applied,
            added_paths=frozenset(
                {pathlib.PurePosixPath("docs/04.execution/tasks/149.md")}
            ),
            warning_at=100,
            block_new_leaf_at=150,
            enforce_all=False,
        )
        self.assertNotIn("directory-budget-blocked", {item.code for item in approved})

    def test_partition_plan_uses_canonical_metadata_relations_and_body_role(self) -> None:
        temporary, root, _baseline, row, _records = self._partition_fixture(
            plan_state="tracked"
        )
        self.addCleanup(temporary.cleanup)
        plan = root / row.partition_plan.as_posix()
        canonical = plan.read_text(encoding="utf-8")
        wrong_parent = root / "docs/90.references/data/wrong-parent.md"
        wrong_parent.parent.mkdir(parents=True, exist_ok=True)
        wrong_parent.write_text(
            "---\nstatus: active\nartifact_id: reference:wrong-parent\n"
            "artifact_type: reference\nparent_ids: []\n---\n\n# Wrong Parent\n",
            encoding="utf-8",
        )
        commit_all(root, "track wrong parent type")
        cases = {
            "invalid-optional": canonical.replace(
                "parent_ids: [spec:partition]",
                "parent_ids: [spec:partition]\nsupersedes: invalid-scalar",
            ),
            "unresolved-parent": canonical.replace(
                "parent_ids: [spec:partition]", "parent_ids: [spec:missing]"
            ),
            "self-parent": canonical.replace(
                "parent_ids: [spec:partition]", "parent_ids: [plan:partition]"
            ),
            "wrong-parent-type": canonical.replace(
                "parent_ids: [spec:partition]",
                "parent_ids: [reference:wrong-parent]",
            ),
            "frontmatter-order": canonical.replace(
                "status: active\nartifact_id: plan:partition\nartifact_type: plan",
                "artifact_type: plan\nstatus: active\nartifact_id: plan:partition",
            ),
            "placeholder": canonical.replace(
                "Partition approval.", "{{overview}}"
            ),
            "missing-heading": canonical.replace("## Work Breakdown", "### Work Breakdown"),
            "forbidden-heading": canonical + "\n## Verification Evidence\nNot permitted.\n",
        }
        for name, candidate in cases.items():
            with self.subTest(case=name):
                plan.write_text(candidate, encoding="utf-8")
                codes = {
                    item.code
                    for item in lifecycle._partition_plan_findings(
                        root, self.profiles, row
                    )
                }
                self.assertIn("manifest-partition-plan-profile-invalid", codes)
        plan.write_text(canonical, encoding="utf-8")
        self.assertEqual(
            lifecycle._partition_plan_findings(root, self.profiles, row), []
        )

    def test_v2_partition_plan_requires_canonical_identity_and_parent_relations(
        self,
    ) -> None:
        temporary, root, _baseline, row, _records = self._partition_fixture(
            plan_state="tracked"
        )
        self.addCleanup(temporary.cleanup)
        plan = root / row.partition_plan.as_posix()
        canonical = plan.read_text(encoding="utf-8")
        cases = {
            "missing-identity": canonical.replace(
                "artifact_id: plan:partition\n", ""
            ),
            "unresolved-parent": canonical.replace(
                "parent_ids: [spec:partition]", "parent_ids: [spec:missing]"
            ),
        }
        for name, candidate in cases.items():
            with self.subTest(case=name):
                plan.write_text(candidate, encoding="utf-8")
                codes = {
                    item.code
                    for item in lifecycle._surface_partition_plan_findings(
                        root, self.profiles, row
                    )
                }
                self.assertIn("manifest-partition-plan-profile-invalid", codes)

    def test_directory_budget_counts_only_immediate_eligible_markdown_leaves(self) -> None:
        records = tuple(
            self.record(f"docs/04.execution/tasks/{index:03}.md")
            for index in range(99)
        ) + (
            self.record("docs/04.execution/tasks/README.md", "readme"),
            self.record("docs/04.execution/tasks/generated.md", "generated"),
            self.record("docs/04.execution/tasks/repo-support.md", "repo-support"),
            self.record("docs/04.execution/tasks/unsupported.md", "unsupported"),
            self.record("docs/04.execution/tasks/not-markdown.txt", "task"),
            self.record("docs/04.execution/tasks/2026/nested.md", "task"),
        )
        findings = lifecycle.validate_directory_budgets(
            records,
            added_paths=frozenset(),
            warning_at=100,
            block_new_leaf_at=150,
            enforce_all=False,
        )
        self.assertFalse(
            any(
                item.path == "docs/04.execution/tasks"
                and item.code == "directory-budget-warning"
                for item in findings
            )
        )

    def test_impacted_cli_snapshots_safe_untracked_records_and_blocks_150th_leaf(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            init_repo(root)
            git(root, "commit", "--allow-empty", "-q", "-m", "empty baseline")
            baseline = git(root, "rev-parse", "HEAD")
            candidate = root / "docs/90.references/data/new.md"
            candidate.parent.mkdir(parents=True)
            valid = (
                "---\nstatus: active\nartifact_id: reference:new\n"
                "artifact_type: reference\nparent_ids: []\n---\n\n# New Reference\n"
            )
            candidate.write_text(valid, encoding="utf-8")
            accepted = self.run_isolated_impacted_cli(root, base_ref=baseline)
            self.assertEqual(accepted.returncode, 0, accepted.stdout + accepted.stderr)
            self.assertIn("selected=1 violations=0", accepted.stdout)
            candidate.write_text(
                valid.replace("status: active", "status: invalid-status"),
                encoding="utf-8",
            )
            rejected = self.run_isolated_impacted_cli(root, base_ref=baseline)
            self.assertEqual(rejected.returncode, 1, rejected.stdout + rejected.stderr)
            self.assertIn("selected=1 violations=", rejected.stdout)

        for attack in ("final", "intermediate"):
            with self.subTest(attack=attack), tempfile.TemporaryDirectory() as directory:
                fixture = pathlib.Path(directory)
                root = fixture / "repository"
                outside = fixture / "outside"
                root.mkdir()
                outside.mkdir()
                init_repo(root)
                git(root, "commit", "--allow-empty", "-q", "-m", "empty baseline")
                marker = "outside-untracked-marker"
                (outside / "leak.md").write_text(marker, encoding="utf-8")
                target = root / "docs/90.references/data/leak.md"
                target.parent.mkdir(parents=True)
                if attack == "final":
                    target.symlink_to(outside / "leak.md")
                else:
                    target.parent.joinpath("nested").symlink_to(
                        outside, target_is_directory=True
                    )
                result = self.run_isolated_impacted_cli(root, base_ref="HEAD")
                rendered = result.stdout + result.stderr
                self.assertEqual(result.returncode, 3, rendered)
                self.assertNotIn(marker, rendered)

        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            init_repo(root)
            budget = root / "docs/90.references/data/budget"
            budget.mkdir(parents=True)
            for index in range(148):
                (budget / f"{index:03}.md").write_text(
                    "---\nstatus: active\n"
                    f"artifact_id: reference:budget-{index:03}\n"
                    "artifact_type: reference\nparent_ids: []\n---\n\n# Budget\n",
                    encoding="utf-8",
                )
            base_148 = commit_all(root, "148 leaves")
            leaf_149 = budget / "148.md"
            leaf_149.write_text(
                "---\nstatus: active\nartifact_id: reference:budget-148\n"
                "artifact_type: reference\nparent_ids: []\n---\n\n# Budget\n",
                encoding="utf-8",
            )
            before_limit = self.run_isolated_impacted_cli(root, base_ref=base_148)
            self.assertEqual(before_limit.returncode, 0, before_limit.stdout + before_limit.stderr)
            base_149 = commit_all(root, "149 leaves")
            (budget / "149.md").write_text(
                "---\nstatus: active\nartifact_id: reference:budget-149\n"
                "artifact_type: reference\nparent_ids: []\n---\n\n# Budget\n",
                encoding="utf-8",
            )
            at_limit = self.run_isolated_impacted_cli(root, base_ref=base_149)
            self.assertEqual(at_limit.returncode, 1, at_limit.stdout + at_limit.stderr)
            self.assertIn("directory-budget-blocked", at_limit.stdout)

    def test_cli_diagnostics_never_emit_metadata_payloads_across_modes(self) -> None:
        cases = (
            ("report-full", "sk-do-not-echo-1234567890"),
            ("check-full", "password=do-not-echo"),
            ("check-impacted", "credential=do-not-echo"),
            ("check-archive", "-----BEGIN PRIVATE KEY-----"),
            ("generate-archive-ledger", "authorization: Bearer do-not-echo-value"),
            ("check-archive-ledger", ".zsh_history"),
            ("generate-snapshot-manifest", "2026-07-14T10:00:00 ERROR do-not-echo"),
            ("check-snapshot-manifest", "token=do-not-echo"),
        )
        for mode, marker in cases:
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                init_repo(root)
                git(root, "commit", "--allow-empty", "-q", "-m", "empty baseline")
                baseline = git(root, "rev-parse", "HEAD")
                path = root / "docs/90.references/data/diagnostic.md"
                path.parent.mkdir(parents=True)
                path.write_text(
                    "---\n"
                    + yaml.safe_dump(
                        {
                            "status": "active",
                            "artifact_id": "reference:diagnostic",
                            "artifact_type": "reference",
                            "parent_ids": [marker],
                        },
                        sort_keys=False,
                    )
                    + "---\n\n# Diagnostic\n",
                    encoding="utf-8",
                )
                commit_all(root, "track diagnostic")
                output = root / "output.md"
                arguments = [
                    sys.executable,
                    str(SCRIPT),
                    "--root",
                    str(root),
                    "--mode",
                    mode,
                ]
                if mode in {
                    "generate-archive-ledger",
                    "check-archive-ledger",
                    "generate-snapshot-manifest",
                    "check-snapshot-manifest",
                }:
                    arguments.extend(("--output", str(output)))
                    if mode.startswith("check-"):
                        output.write_text("sentinel\n", encoding="utf-8")
                result = (
                    self.run_isolated_impacted_cli(root, base_ref=baseline)
                    if mode == "check-impacted"
                    else run(*arguments, cwd=ROOT)
                )
                rendered = result.stdout + result.stderr
                self.assertNotIn(marker, rendered)
                self.assertNotIn(marker, output.read_text(encoding="utf-8") if output.exists() else "")
                if mode in {"report-full", "check-full", "check-impacted"}:
                    self.assertEqual(result.returncode, 3, rendered)

        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            init_repo(root)
            path = root / "docs/90.references/data/ordinary.md"
            path.parent.mkdir(parents=True)
            missing_id = "reference:ordinary-unresolved-id"
            path.write_text(
                "---\nstatus: active\nartifact_id: reference:ordinary\n"
                f"artifact_type: reference\nparent_ids: [{missing_id}]\n---\n\n# Ordinary\n",
                encoding="utf-8",
            )
            commit_all(root)
            result = run(
                sys.executable,
                str(SCRIPT),
                "--root",
                str(root),
                "--mode",
                "report-full",
                cwd=ROOT,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("unresolved-parent", result.stdout)
            self.assertNotIn(missing_id, result.stdout + result.stderr)

    def test_generated_markdown_table_cells_escape_pipe_and_control_characters(self) -> None:
        record = self.record(
            "docs/98.archive/a|b.md",
            "archive",
            archived_from="docs/source|name.md\nnext-row",
            archive_disposition="withdrawn",
            preservation_class="git-history",
            archived_commit="a" * 40,
            archived_blob="b" * 40,
        )
        ledger = lifecycle.render_archive_ledger((record,))
        self.assertIn("docs/98.archive/a\\|b.md", ledger)
        self.assertIn("docs/source\\|name.md next-row", ledger)
        self.assertNotIn("docs/source|name.md\nnext-row", ledger)


class AcceptanceFindingRemediationTests(LifecycleTestCase):
    _archive_fixture = FinalReviewRemediationTests._archive_fixture
    _archive_codes = FinalReviewRemediationTests._archive_codes

    @staticmethod
    def _reference_text(
        artifact_id: str,
        title: str,
        *,
        parent_ids: tuple[str, ...] = (),
        status: str = "active",
    ) -> str:
        metadata_values = {
            "status": status,
            "artifact_id": artifact_id,
            "artifact_type": "reference",
            "parent_ids": list(parent_ids),
        }
        return (
            "---\n"
            + yaml.safe_dump(metadata_values, sort_keys=False)
            + f"---\n\n# {title}\n\n"
            "## Overview\nCurrent reference.\n\n"
            "## Purpose\nCanonical purpose.\n\n"
            "## Scope\nCurrent scope.\n\n"
            "## Facts and Definitions\nCanonical facts.\n\n"
            "## Sources\nRepository evidence.\n\n"
            "## Maintenance\nActive.\n\n"
            "## Related Documents\nNone.\n"
        )

    @staticmethod
    def _destructive_evidence() -> lifecycle.ManifestEvidence:
        return lifecycle.ManifestEvidence(
            ("git show baseline source",),
            ("docs/90.references/source.md",),
            (pathlib.PurePosixPath("docs/90.references/source.md"),),
            ("verified active consumers",),
            ("revert destructive commit",),
        )

    def _invoke_corpus_mode(
        self,
        root: pathlib.Path,
        mode: str,
        output: pathlib.Path,
        *,
        base_ref: str = "HEAD",
    ) -> subprocess.CompletedProcess[str]:
        if mode == "check-impacted":
            return self.run_isolated_impacted_cli(root, base_ref=base_ref)
        arguments = [
            sys.executable,
            str(SCRIPT),
            "--root",
            str(root),
            "--mode",
            mode,
        ]
        if mode in {
            "report-duplicates",
            "generate-archive-ledger",
            "check-archive-ledger",
            "generate-snapshot-manifest",
            "check-snapshot-manifest",
        }:
            arguments.extend(("--output", str(output)))
        return run(*arguments, cwd=ROOT)

    def test_real_impacted_cli_accepts_unstaged_delete_and_rename_snapshots(self) -> None:
        for operation in ("delete", "rename"):
            with self.subTest(operation=operation), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                init_repo(root)
                source = root / "docs/90.references/source.md"
                consumer = root / "docs/90.references/consumer.md"
                source.parent.mkdir(parents=True)
                source.write_text(
                    self._reference_text("reference:source", "Source"),
                    encoding="utf-8",
                )
                consumer.write_text(
                    self._reference_text("reference:consumer", "Consumer")
                    + "\n[Source](./source.md)\n",
                    encoding="utf-8",
                )
                baseline = commit_all(root, "impacted baseline")
                if operation == "delete":
                    source.unlink()
                    expected_selected = 1
                else:
                    source.rename(root / "docs/90.references/renamed.md")
                    expected_selected = 2

                result = self._invoke_corpus_mode(
                    root,
                    "check-impacted",
                    root / "unused",
                    base_ref=baseline,
                )
                rendered = result.stdout + result.stderr
                self.assertEqual(result.returncode, 0, rendered)
                self.assertIn(
                    f"selected={expected_selected} violations=0",
                    result.stdout,
                )
                self.assertNotIn("corpus-markdown-file-invalid", rendered)

    def test_safety_exception_paths_are_redacted_across_corpus_reading_modes(self) -> None:
        marker = "token=do-not-echo-1234567890"
        modes = (
            "report-full",
            "check-full",
            "report-duplicates",
            "check-impacted",
            "check-archive",
            "check-directory-budget",
            "generate-archive-ledger",
            "check-archive-ledger",
            "generate-snapshot-manifest",
            "check-snapshot-manifest",
        )
        with tempfile.TemporaryDirectory() as directory:
            fixture = pathlib.Path(directory)
            root = fixture / "repository"
            outside = fixture / "outside.md"
            root.mkdir()
            init_repo(root)
            outside.write_text("outside payload", encoding="utf-8")
            unsafe = root / f"docs/90.references/{marker}.md"
            unsafe.parent.mkdir(parents=True)
            unsafe.symlink_to(outside)
            commit_all(root, "track unsafe token-shaped path")

            for mode in modes:
                with self.subTest(mode=mode):
                    output = fixture / f"{mode}.out"
                    if mode in {"check-archive-ledger", "check-snapshot-manifest"}:
                        output.write_bytes(b"existing-output")
                    result = self._invoke_corpus_mode(root, mode, output)
                    rendered = result.stdout + result.stderr
                    self.assertEqual(result.returncode, 3, rendered)
                    self.assertNotIn(marker, rendered)
                    self.assertNotIn("Traceback", rendered)
                    if mode in {"check-archive-ledger", "check-snapshot-manifest"}:
                        self.assertEqual(output.read_bytes(), b"existing-output")
                    else:
                        self.assertFalse(output.exists())

    def _merge_fixture(
        self,
        *,
        track_target: bool = True,
        baseline_target_artifact_type: str = "reference",
        baseline_target_status: str = "active",
        duplicate_baseline_owner: bool = False,
    ) -> tuple[tempfile.TemporaryDirectory[str], pathlib.Path, str, lifecycle.MigrationManifestRow]:
        temporary = tempfile.TemporaryDirectory()
        root = pathlib.Path(temporary.name)
        init_repo(root)
        source_relative = pathlib.PurePosixPath("docs/90.references/source.md")
        source = root / source_relative
        source.parent.mkdir(parents=True)
        source.write_text(
            self._reference_text("reference:duplicate", "Duplicate Source"),
            encoding="utf-8",
        )
        target_relative = pathlib.PurePosixPath(
            "docs/90.references/data/canonical.md"
        )
        target = root / target_relative
        canonical_target = self._reference_text(
            "reference:canonical",
            "Canonical Owner",
            status=baseline_target_status,
        )
        if track_target:
            target.parent.mkdir(parents=True)
            target.write_text(
                canonical_target.replace(
                    "artifact_type: reference",
                    f"artifact_type: {baseline_target_artifact_type}",
                ),
                encoding="utf-8",
            )
        duplicate_owner = root / "docs/90.references/data/duplicate-owner.md"
        if duplicate_baseline_owner:
            duplicate_owner.write_text(canonical_target, encoding="utf-8")
        baseline = commit_all(root, "merge baseline")
        source.unlink()
        if track_target and baseline_target_artifact_type != "reference":
            target.write_text(canonical_target, encoding="utf-8")
        if duplicate_baseline_owner:
            duplicate_owner.unlink()
        git(root, "add", "-A")
        git(root, "commit", "-q", "-m", "remove merged source")
        if not track_target:
            target.parent.mkdir(parents=True)
            target.write_text(canonical_target, encoding="utf-8")
        row = self.valid_row(
            source_path=source_relative,
            target_path=target_relative,
            artifact_id="reference:duplicate",
            artifact_type="reference",
            status_before="active",
            status_after="active",
            parent_ids=(),
            disposition="merge",
            canonical_replacement=target_relative.as_posix(),
            active_consumers=(),
            preservation_class="git-history",
            evidence=self._destructive_evidence(),
            review_verdict=lifecycle.ReviewVerdict("pass", "pass"),
        )
        return temporary, root, baseline, row

    def _manifest_codes(
        self,
        root: pathlib.Path,
        baseline: str,
        rows: tuple[lifecycle.MigrationManifestRow, ...],
    ) -> set[str]:
        return {
            finding.code
            for finding in lifecycle.validate_migration_manifest(
                root,
                self.profiles,
                self.fixture_contract(
                    [row.source_path.as_posix() for row in rows]
                ),
                self.document(baseline, entries=rows),
            )
        }

    def test_merge_and_delete_replacements_resolve_and_bind_to_canonical_results(self) -> None:
        temporary, root, baseline, row = self._merge_fixture()
        self.addCleanup(temporary.cleanup)
        self.assertEqual(self._manifest_codes(root, baseline, (row,)), set())
        self.assertEqual(
            self._manifest_codes(
                root,
                baseline,
                (
                    dataclasses.replace(
                        row,
                        canonical_replacement="reference:canonical",
                    ),
                ),
            ),
            set(),
        )

        other = root / "docs/90.references/data/other.md"
        other.write_text(
            self._reference_text("reference:other", "Other"),
            encoding="utf-8",
        )
        commit_all(root, "track mismatched replacement")
        invalid_replacements = (
            "docs/90.references/data/missing.md",
            "reference:missing",
            "docs/90.references/data/other.md",
            "reference:other",
        )
        for replacement in invalid_replacements:
            with self.subTest(replacement=replacement):
                self.assertIn(
                    "manifest-replacement-invalid",
                    self._manifest_codes(
                        root,
                        baseline,
                        (dataclasses.replace(row, canonical_replacement=replacement),),
                    ),
                )

        target = root / row.target_path
        canonical = target.read_text(encoding="utf-8")
        for name, mutation in {
            "invalid-profile": canonical.replace(
                "artifact_type: reference", "artifact_type: archive"
            ),
            "invalid-body": canonical.replace("## Sources", "### Sources"),
        }.items():
            with self.subTest(target_mutation=name):
                target.write_text(mutation, encoding="utf-8")
                self.assertIn(
                    "manifest-replacement-invalid",
                    self._manifest_codes(root, baseline, (row,)),
                )
        target.write_text(canonical, encoding="utf-8")

        outside = pathlib.Path(temporary.name).parent / (
            pathlib.Path(temporary.name).name + "-merge-outside.md"
        )
        outside.write_text(canonical, encoding="utf-8")
        self.addCleanup(lambda: outside.unlink(missing_ok=True))
        target.unlink()
        target.symlink_to(outside)
        with self.assertRaises(lifecycle._CorpusSafetyError):
            self._manifest_codes(root, baseline, (row,))
        target.unlink()
        target.write_text(canonical, encoding="utf-8")

        duplicate = root / "docs/90.references/data/duplicate.md"
        duplicate.write_text(canonical, encoding="utf-8")
        commit_all(root, "duplicate merged identity")
        self.assertIn(
            "manifest-replacement-invalid",
            self._manifest_codes(
                root,
                baseline,
                (
                    dataclasses.replace(
                        row,
                        canonical_replacement="reference:canonical",
                    ),
                ),
            ),
        )

        untracked_temporary, untracked_root, untracked_baseline, untracked_row = (
            self._merge_fixture(track_target=False)
        )
        self.addCleanup(untracked_temporary.cleanup)
        self.assertIn(
            "manifest-replacement-invalid",
            self._manifest_codes(
                untracked_root, untracked_baseline, (untracked_row,)
            ),
        )

        delete_source = root / "docs/90.references/delete-source.md"
        delete_source.write_text(
            self._reference_text("reference:delete-source", "Delete Source"),
            encoding="utf-8",
        )
        delete_baseline = commit_all(root, "delete baseline")
        delete_source.unlink()
        commit_all(root, "remove delete source")
        delete_row = dataclasses.replace(
            row,
            source_path=pathlib.PurePosixPath("docs/90.references/delete-source.md"),
            target_path=None,
            artifact_id="reference:delete-source",
            disposition="delete",
            canonical_replacement="docs/90.references/data/other.md",
        )
        self.assertEqual(
            self._manifest_codes(root, delete_baseline, (delete_row,)),
            set(),
        )
        self.assertIn(
            "manifest-replacement-invalid",
            self._manifest_codes(
                root,
                delete_baseline,
                (
                    dataclasses.replace(
                        delete_row,
                        canonical_replacement="docs/90.references/data/missing.md",
                    ),
                ),
            ),
        )

    def test_distinct_identity_merge_rejects_owner_target_and_identity_mutations(
        self,
    ) -> None:
        temporary, root, baseline, row = self._merge_fixture()
        self.addCleanup(temporary.cleanup)

        other = root / "docs/90.references/data/other.md"
        other.write_text(
            self._reference_text("reference:other", "Other Owner"),
            encoding="utf-8",
        )
        commit_all(root, "track other owner")

        wrong_owner = dataclasses.replace(
            row,
            canonical_replacement="reference:other",
        )
        wrong_target = dataclasses.replace(
            row,
            target_path=pathlib.PurePosixPath("docs/90.references/data/other.md"),
            canonical_replacement="reference:canonical",
        )
        baseline_identity_mutation = dataclasses.replace(
            row,
            artifact_id="reference:canonical",
        )
        for name, mutated, expected in (
            ("wrong-owner", wrong_owner, "manifest-replacement-invalid"),
            ("wrong-target", wrong_target, "manifest-replacement-invalid"),
            (
                "baseline-row-identity",
                baseline_identity_mutation,
                "manifest-baseline-artifact-id-mismatch",
            ),
        ):
            with self.subTest(name=name):
                self.assertIn(
                    expected,
                    self._manifest_codes(root, baseline, (mutated,)),
                )

        target = root / row.target_path
        canonical = target.read_text(encoding="utf-8")
        target.write_text(
            canonical.replace("reference:canonical", "reference:mutated"),
            encoding="utf-8",
        )
        self.assertIn(
            "manifest-replacement-invalid",
            self._manifest_codes(root, baseline, (row,)),
        )

    def test_merge_can_preserve_source_identity_when_the_target_is_new(self) -> None:
        temporary, root, baseline, row = self._merge_fixture(track_target=False)
        self.addCleanup(temporary.cleanup)
        target = root / row.target_path
        target.write_text(
            self._reference_text("reference:duplicate", "Consolidated Result"),
            encoding="utf-8",
        )
        commit_all(root, "track consolidated result")

        self.assertEqual(self._manifest_codes(root, baseline, (row,)), set())
        self.assertEqual(
            self._manifest_codes(
                root,
                baseline,
                (
                    dataclasses.replace(
                        row,
                        canonical_replacement="reference:duplicate",
                    ),
                ),
            ),
            set(),
        )

    def test_merge_rejects_distinct_identity_created_after_the_baseline(self) -> None:
        temporary, root, baseline, row = self._merge_fixture(track_target=False)
        self.addCleanup(temporary.cleanup)
        commit_all(root, "track post-baseline canonical identity")

        for replacement in (
            row.target_path.as_posix(),
            "reference:canonical",
        ):
            with self.subTest(replacement=replacement):
                self.assertIn(
                    "manifest-replacement-invalid",
                    self._manifest_codes(
                        root,
                        baseline,
                        (
                            dataclasses.replace(
                                row,
                                canonical_replacement=replacement,
                            ),
                        ),
                    ),
                )

    def test_merge_rejects_ambiguous_or_wrong_profile_baseline_owner(self) -> None:
        fixtures = (
            ("ambiguous-owner", {"duplicate_baseline_owner": True}),
            ("wrong-profile", {"baseline_target_artifact_type": "archive"}),
        )
        for name, options in fixtures:
            with self.subTest(name=name):
                temporary, root, baseline, row = self._merge_fixture(**options)
                self.addCleanup(temporary.cleanup)
                self.assertIn(
                    "manifest-replacement-invalid",
                    self._manifest_codes(root, baseline, (row,)),
                )

    def test_merge_accepts_preexisting_distinct_owner_moved_by_the_same_wave(
        self,
    ) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = pathlib.Path(temporary.name)
        init_repo(root)
        source_relative = pathlib.PurePosixPath("docs/90.references/source.md")
        owner_relative = pathlib.PurePosixPath(
            "docs/90.references/data/old-owner.md"
        )
        target_relative = pathlib.PurePosixPath(
            "docs/90.references/data/canonical.md"
        )
        source = root / source_relative
        owner = root / owner_relative
        source.parent.mkdir(parents=True)
        owner.parent.mkdir(parents=True)
        source.write_text(
            self._reference_text("reference:duplicate", "Duplicate Source"),
            encoding="utf-8",
        )
        owner.write_text(
            self._reference_text("reference:canonical", "Canonical Owner"),
            encoding="utf-8",
        )
        baseline = commit_all(root, "moving merge-owner baseline")
        source.unlink()
        owner.unlink()
        target = root / target_relative
        target.write_text(
            self._reference_text("reference:canonical", "Moved Canonical Owner"),
            encoding="utf-8",
        )
        commit_all(root, "move canonical owner and merge duplicate")

        def evidence(path: pathlib.PurePosixPath) -> lifecycle.ManifestEvidence:
            return lifecycle.ManifestEvidence(
                (f"git show baseline:{path.as_posix()}",),
                (path.as_posix(),),
                (path,),
                ("verified active consumers",),
                ("revert destructive commit",),
            )

        owner_row = self.valid_row(
            source_path=owner_relative,
            target_path=target_relative,
            artifact_id="reference:canonical",
            artifact_type="reference",
            status_before="active",
            status_after="active",
            parent_ids=(),
            disposition="move",
            canonical_replacement=None,
            active_consumers=(),
            preservation_class="git-history",
            evidence=evidence(owner_relative),
            review_verdict=lifecycle.ReviewVerdict("pass", "pass"),
        )
        merge_row = dataclasses.replace(
            owner_row,
            source_path=source_relative,
            artifact_id="reference:duplicate",
            disposition="merge",
            canonical_replacement=target_relative.as_posix(),
            evidence=evidence(source_relative),
        )
        for replacement in (target_relative.as_posix(), "reference:canonical"):
            with self.subTest(replacement=replacement):
                candidate = dataclasses.replace(
                    merge_row,
                    canonical_replacement=replacement,
                )
                self.assertEqual(
                    self._manifest_codes(root, baseline, (owner_row, candidate)),
                    set(),
                )

    def test_merge_owner_requires_a_regular_baseline_git_blob(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = pathlib.Path(temporary.name)
        init_repo(root)
        source_relative = pathlib.PurePosixPath("docs/90.references/source.md")
        target_relative = pathlib.PurePosixPath(
            "docs/90.references/data/canonical.md"
        )
        source = root / source_relative
        target = root / target_relative
        source.parent.mkdir(parents=True)
        target.parent.mkdir(parents=True)
        source.write_text(
            self._reference_text("reference:duplicate", "Duplicate Source"),
            encoding="utf-8",
        )
        canonical_text = self._reference_text(
            "reference:canonical", "Canonical Owner"
        )
        target.symlink_to(canonical_text)
        baseline = commit_all(root, "symlink merge-owner baseline")

        baseline_owners = metadata.collect_records_at_ref(
            root, self.profiles, baseline
        )
        self.assertIn(
            "reference:canonical",
            {
                record.metadata.get("artifact_id")
                for record in baseline_owners
            },
            "the fixture must prove that parseable symlink bytes reach metadata discovery",
        )
        self.assertTrue(
            git(root, "ls-tree", baseline, "--", target_relative.as_posix()).startswith(
                "120000 blob "
            )
        )

        source.unlink()
        target.unlink()
        target.write_text(canonical_text, encoding="utf-8")
        commit_all(root, "replace symlink owner with regular result")
        row = self.valid_row(
            source_path=source_relative,
            target_path=target_relative,
            artifact_id="reference:duplicate",
            artifact_type="reference",
            status_before="active",
            status_after="active",
            parent_ids=(),
            disposition="merge",
            canonical_replacement=target_relative.as_posix(),
            active_consumers=(),
            preservation_class="git-history",
            evidence=self._destructive_evidence(),
            review_verdict=lifecycle.ReviewVerdict("pass", "pass"),
        )

        for replacement in (target_relative.as_posix(), "reference:canonical"):
            with self.subTest(replacement=replacement):
                codes = self._manifest_codes(
                    root,
                    baseline,
                    (
                        dataclasses.replace(
                            row,
                            canonical_replacement=replacement,
                        ),
                    ),
                )
                self.assertIn("manifest-replacement-invalid", codes)

    def test_baseline_regular_blob_rejects_nonregular_git_entries(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            init_repo(root)
            regular = root / "docs/regular.md"
            executable = root / "docs/executable.md"
            symlink = root / "docs/symlink.md"
            regular.parent.mkdir(parents=True)
            regular.write_text("regular\n", encoding="utf-8")
            executable.write_text("executable\n", encoding="utf-8")
            executable.chmod(0o755)
            symlink.symlink_to("regular.md")
            baseline = commit_all(root, "regular and nonregular modes")
            git(
                root,
                "update-index",
                "--add",
                "--cacheinfo",
                f"160000,{baseline},docs/gitlink.md",
            )
            git(root, "commit", "-q", "-m", "add synthetic gitlink")
            checked = git(root, "rev-parse", "HEAD")

            self.assertTrue(
                lifecycle._baseline_regular_blob(root, checked, "docs/regular.md")
            )
            self.assertTrue(
                lifecycle._baseline_regular_blob(root, checked, "docs/executable.md")
            )
            self.assertFalse(
                lifecycle._baseline_regular_blob(root, checked, "docs/symlink.md")
            )
            self.assertFalse(
                lifecycle._baseline_regular_blob(root, checked, "docs/gitlink.md")
            )
            self.assertFalse(lifecycle._baseline_regular_blob(root, checked, "docs"))
            self.assertFalse(
                lifecycle._baseline_regular_blob(root, checked, "docs/missing.md")
            )

    def _same_path_owner_transition_fixture(
        self,
        *,
        baseline_owner_status: str = "active",
        current_owner_status: str = "completed",
    ) -> tuple[
        tempfile.TemporaryDirectory[str],
        pathlib.Path,
        str,
        lifecycle.MigrationManifestRow,
        lifecycle.MigrationManifestRow,
    ]:
        temporary, root, baseline, merge_row = self._merge_fixture(
            baseline_target_status=baseline_owner_status,
        )
        target = root / merge_row.target_path
        target.write_text(
            self._reference_text(
                "reference:canonical",
                "Canonical Owner",
                status=current_owner_status,
            ),
            encoding="utf-8",
        )
        commit_all(root, "transition canonical owner")

        evidence = lifecycle.ManifestEvidence(
            ("git show baseline owner",),
            (merge_row.target_path.as_posix(),),
            (merge_row.target_path,),
            ("verified active consumers",),
            ("revert lifecycle transition",),
        )
        owner_row = self.valid_row(
            source_path=merge_row.target_path,
            target_path=merge_row.target_path,
            artifact_id="reference:canonical",
            artifact_type="reference",
            status_before=baseline_owner_status,
            status_after=current_owner_status,
            parent_ids=(),
            disposition="migrate",
            canonical_replacement=None,
            active_consumers=(),
            preservation_class=None,
            evidence=evidence,
            review_verdict=lifecycle.ReviewVerdict("pass", "pass"),
        )
        merge_row = dataclasses.replace(
            merge_row,
            status_after=current_owner_status,
        )
        return temporary, root, baseline, owner_row, merge_row

    def test_merge_accepts_exact_same_path_owner_lifecycle_attestation(self) -> None:
        temporary, root, baseline, owner_row, merge_row = (
            self._same_path_owner_transition_fixture()
        )
        self.addCleanup(temporary.cleanup)

        for replacement in (
            merge_row.target_path.as_posix(),
            "reference:canonical",
        ):
            with self.subTest(replacement=replacement):
                candidate = dataclasses.replace(
                    merge_row,
                    canonical_replacement=replacement,
                )
                self.assertEqual(
                    self._manifest_codes(root, baseline, (owner_row, candidate)),
                    set(),
                )

    def test_merge_rejects_missing_ambiguous_or_invalid_same_path_owner_peer(
        self,
    ) -> None:
        temporary, root, baseline, owner_row, merge_row = (
            self._same_path_owner_transition_fixture()
        )
        self.addCleanup(temporary.cleanup)
        empty_evidence = lifecycle.ManifestEvidence((), (), (), (), ())
        cases: tuple[
            tuple[str, tuple[lifecycle.MigrationManifestRow, ...]], ...
        ] = (
            ("missing", (merge_row,)),
            (
                "duplicate",
                (owner_row, dataclasses.replace(owner_row), merge_row),
            ),
            (
                "wrong-status-before",
                (dataclasses.replace(owner_row, status_before="draft"), merge_row),
            ),
            (
                "wrong-status-after",
                (dataclasses.replace(owner_row, status_after="superseded"), merge_row),
            ),
            (
                "wrong-id",
                (
                    dataclasses.replace(owner_row, artifact_id="reference:other"),
                    merge_row,
                ),
            ),
            (
                "wrong-type",
                (dataclasses.replace(owner_row, artifact_type="guide"), merge_row),
            ),
            (
                "wrong-disposition",
                (dataclasses.replace(owner_row, disposition="preserve"), merge_row),
            ),
            (
                "review-not-passing",
                (
                    dataclasses.replace(
                        owner_row,
                        review_verdict=lifecycle.ReviewVerdict("pending", "pending"),
                    ),
                    merge_row,
                ),
            ),
            (
                "evidence-incomplete",
                (dataclasses.replace(owner_row, evidence=empty_evidence), merge_row),
            ),
        )
        for name, rows in cases:
            with self.subTest(name=name):
                self.assertIn(
                    "manifest-replacement-invalid",
                    self._manifest_codes(root, baseline, rows),
                )

    def test_merge_rejects_reverse_same_path_owner_transition(self) -> None:
        temporary, root, baseline, owner_row, merge_row = (
            self._same_path_owner_transition_fixture(
                baseline_owner_status="completed",
                current_owner_status="active",
            )
        )
        self.addCleanup(temporary.cleanup)
        codes = self._manifest_codes(root, baseline, (owner_row, merge_row))
        self.assertIn("manifest-transition-invalid", codes)
        self.assertIn("manifest-replacement-invalid", codes)

    WRITE_MODES = (
        "generate-manifest",
        "generate-summary",
        "report-duplicates",
        "generate-archive-ledger",
        "generate-snapshot-manifest",
    )
    CHECK_MODES = (
        "check-summary",
        "check-archive-ledger",
        "check-snapshot-manifest",
    )

    def _mode_fixture(
        self,
        mode: str,
        output: pathlib.Path,
    ) -> tuple[list[str], str, lifecycle.MigrationManifestDocument]:
        document = self.document("a" * 40)
        arguments = ["--mode", mode]
        if mode == "generate-manifest":
            arguments.extend(
                (
                    "--wave",
                    "fixture",
                    "--base-ref",
                    "HEAD",
                    "--output",
                    str(output),
                )
            )
            rendered = lifecycle.render_migration_manifest(document)
        elif mode in {"generate-summary", "check-summary"}:
            arguments.extend(
                ("--manifest", "docs/manifest.yaml", "--output", str(output))
            )
            rendered = lifecycle._render_summary(document)
        elif mode == "report-duplicates":
            arguments.extend(("--output", str(output)))
            rendered = yaml.safe_dump(
                {"schema_version": 1, "candidates": []},
                sort_keys=False,
                width=1000,
            )
        elif mode in {"generate-archive-ledger", "check-archive-ledger"}:
            arguments.extend(("--output", str(output)))
            rendered = lifecycle.render_archive_ledger(())
        elif mode in {"generate-snapshot-manifest", "check-snapshot-manifest"}:
            arguments.extend(("--output", str(output)))
            rendered = lifecycle.render_snapshot_manifest(())
        else:
            raise AssertionError(f"unsupported output mode: {mode}")
        return arguments, rendered, document

    def _invoke_output_mode(
        self,
        root: pathlib.Path,
        mode: str,
        output: pathlib.Path,
    ) -> tuple[int, str, str]:
        arguments, _, document = self._mode_fixture(mode, output)
        stdout = io.StringIO()
        stderr = io.StringIO()
        with (
            mock.patch.object(
                lifecycle,
                "load_migration_contract",
                return_value=copy.deepcopy(self.contract),
            ),
            mock.patch.object(
                lifecycle.metadata,
                "load_profiles",
                return_value=self.profiles,
            ),
            mock.patch.object(
                lifecycle,
                "_generate_manifest_skeleton",
                return_value=document,
            ),
            mock.patch.object(
                lifecycle,
                "_load_candidate_migration_manifest",
                return_value=document,
            ),
            mock.patch.object(
                lifecycle,
                "validate_migration_manifest",
                return_value=[],
            ),
            mock.patch.object(
                lifecycle,
                "_candidate_manifest_matches",
                return_value=True,
            ),
            mock.patch.object(lifecycle, "_full_findings", return_value=((), [])),
            mock.patch.object(
                lifecycle,
                "find_duplicate_candidates",
                return_value=(),
            ),
            contextlib.redirect_stdout(stdout),
            contextlib.redirect_stderr(stderr),
        ):
            result = lifecycle.main(["--root", str(root), *arguments])
        return result, stdout.getvalue(), stderr.getvalue()

    def test_all_output_modes_reject_final_and_intermediate_symlinks(self) -> None:
        modes = self.WRITE_MODES + self.CHECK_MODES
        for attack in ("final", "intermediate"):
            for mode in modes:
                with (
                    self.subTest(attack=attack, mode=mode),
                    tempfile.TemporaryDirectory() as directory,
                ):
                    fixture = pathlib.Path(directory)
                    root = fixture / "repository"
                    root.mkdir()
                    outside = fixture / "outside"
                    outside.mkdir()
                    output_parent = fixture / "selected"
                    output_parent.mkdir()
                    _, rendered, _ = self._mode_fixture(
                        mode,
                        output_parent / "placeholder",
                    )
                    expected = rendered.encode("utf-8")
                    if attack == "final":
                        victim = outside / "victim"
                        original = expected if mode in self.CHECK_MODES else b"victim-sentinel"
                        victim.write_bytes(original)
                        output = output_parent / "result"
                        output.symlink_to(victim)
                    else:
                        alias = output_parent / "alias"
                        alias.symlink_to(outside, target_is_directory=True)
                        output = alias / "result"
                        victim = outside / "result"
                        original = expected if mode in self.CHECK_MODES else None
                        if original is not None:
                            victim.write_bytes(original)

                    result, stdout, stderr = self._invoke_output_mode(
                        root,
                        mode,
                        output,
                    )
                    rendered_diagnostic = stdout + stderr
                    self.assertEqual(result, 3, rendered_diagnostic)
                    self.assertNotIn("Traceback", rendered_diagnostic)
                    self.assertNotIn("victim-sentinel", rendered_diagnostic)
                    if original is None:
                        self.assertFalse(victim.exists())
                    else:
                        self.assertEqual(victim.read_bytes(), original)
                    self.assertFalse(
                        any("lifecycle-output" in path.name for path in fixture.rglob("*"))
                    )

    def test_all_output_modes_reject_nonregular_final_entries(self) -> None:
        for mode in self.WRITE_MODES + self.CHECK_MODES:
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as directory:
                fixture = pathlib.Path(directory)
                root = fixture / "repository"
                root.mkdir()
                output = fixture / "selected-output"
                output.mkdir()
                result, stdout, stderr = self._invoke_output_mode(root, mode, output)
                self.assertEqual(result, 3, stdout + stderr)
                self.assertTrue(output.is_dir())
                self.assertNotIn("Traceback", stdout + stderr)

    def test_all_output_modes_accept_regular_absolute_paths(self) -> None:
        for mode in self.WRITE_MODES + self.CHECK_MODES:
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as directory:
                fixture = pathlib.Path(directory)
                root = fixture / "repository"
                root.mkdir()
                output = fixture / "nested" / "result"
                _, rendered, _ = self._mode_fixture(mode, output)
                if mode in self.CHECK_MODES:
                    output.parent.mkdir()
                    output.write_bytes(rendered.encode("utf-8"))
                result, stdout, stderr = self._invoke_output_mode(root, mode, output)
                self.assertEqual(result, 0, stdout + stderr)
                self.assertEqual(output.read_bytes(), rendered.encode("utf-8"))

    def test_atomic_publication_cannot_redirect_a_concurrent_final_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = pathlib.Path(directory)
            output = fixture / "result"
            victim = fixture / "victim"
            victim.write_bytes(b"victim-sentinel")
            original_replace = os.replace

            def swap_then_replace(
                source: str,
                target: str,
                *,
                src_dir_fd: int | None = None,
                dst_dir_fd: int | None = None,
            ) -> None:
                os.symlink(victim, target, dir_fd=dst_dir_fd)
                original_replace(
                    source,
                    target,
                    src_dir_fd=src_dir_fd,
                    dst_dir_fd=dst_dir_fd,
                )

            with mock.patch.object(
                lifecycle.os,
                "replace",
                side_effect=swap_then_replace,
            ) as replaced:
                lifecycle._write_output(output, "complete\n")

            replaced.assert_called_once()
            self.assertEqual(victim.read_bytes(), b"victim-sentinel")
            self.assertEqual(output.read_bytes(), b"complete\n")
            self.assertFalse(
                any("lifecycle-output" in path.name for path in fixture.iterdir())
            )

    def test_interrupted_publication_preserves_existing_output_and_cleans_temp(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = pathlib.Path(directory)
            output = fixture / "result"
            output.write_bytes(b"existing-output")
            original_write = os.write
            calls = 0

            def partial_then_fail(descriptor: int, payload: bytes) -> int:
                nonlocal calls
                calls += 1
                if calls == 1:
                    original_write(descriptor, payload[: max(1, len(payload) // 2)])
                    raise OSError("simulated interrupted publication")
                return original_write(descriptor, payload)

            with mock.patch.object(
                lifecycle.os,
                "write",
                side_effect=partial_then_fail,
            ):
                with self.assertRaises((OSError, lifecycle._CorpusSafetyError)):
                    lifecycle._write_output(output, "complete-output\n")

            self.assertGreater(calls, 0)
            self.assertEqual(output.read_bytes(), b"existing-output")
            self.assertFalse(
                any("lifecycle-output" in path.name for path in fixture.iterdir())
            )

    def test_archive_result_relations_use_the_held_full_result_manifest(self) -> None:
        temporary, root, baseline, row, target = self._archive_fixture()
        self.addCleanup(temporary.cleanup)
        original = yaml.safe_load(target.read_text(encoding="utf-8").split("---", 2)[1])

        other = root / "docs/90.references/data/other.md"
        other.write_text(
            self._reference_text(
                "reference:other",
                "Other",
                parent_ids=("ref-9999",),
            ),
            encoding="utf-8",
        )
        spec_parent = root / "docs/03.specs/parent.md"
        spec_parent.parent.mkdir(parents=True)
        spec_parent.write_text(
            "---\nstatus: active\nartifact_id: spec:parent\n"
            "artifact_type: spec\nparent_ids: []\n---\n\n# Parent Spec\n",
            encoding="utf-8",
        )
        archive_parent = root / (
            "docs/98.archive/tombstones/05.operations/"
            "ref-9996-archive-parent.md"
        )
        archive_parent.parent.mkdir(parents=True, exist_ok=True)
        archive_parent.write_text(
            "---\nstatus: archived\nartifact_id: ref-9996\n"
            "artifact_type: archive\nparent_ids: []\n---\n\n# Other Archive\n",
            encoding="utf-8",
        )
        commit_all(root, "track archive relation graph")

        cases: tuple[
            tuple[str, dict[str, object], tuple[str, ...], str | None], ...
        ] = (
            ("unresolved-parent", {"parent_ids": ["reference:missing"]}, ("reference:missing",), "unresolved-parent"),
            ("self-parent", {"parent_ids": ["ref-9999"]}, ("ref-9999",), "self-parent"),
            ("archive-parent", {"parent_ids": ["ref-9996"]}, ("ref-9996",), None),
            ("parent-order", {"parent_ids": ["reference:replacement", "spec:parent"]}, ("reference:replacement", "spec:parent"), "parent-order"),
            ("parent-cycle", {"parent_ids": ["reference:other"]}, ("reference:other",), "parent-cycle"),
            ("unresolved-supersedes", {"supersedes": ["reference:missing"]}, (), "unresolved-supersedes"),
            ("self-supersession", {"supersedes": ["ref-9999"]}, (), "self-supersession"),
            ("invalid-supersession-state", {"supersedes": ["reference:replacement"]}, (), "invalid-supersession-state"),
        )
        for name, mutation, parents, expected in cases:
            with self.subTest(case=name):
                values = {**original, **mutation}
                target.write_text(
                    "---\n"
                    + yaml.safe_dump(values, sort_keys=False)
                    + "---\n\n# Archived Source\n",
                    encoding="utf-8",
                )
                candidate = dataclasses.replace(row, parent_ids=parents)
                codes = self._archive_codes(root, baseline, candidate)
                if expected is None:
                    self.assertNotIn("invalid-parent-type", codes)
                else:
                    self.assertIn(expected, codes)

    def test_multi_row_archive_relations_resolve_against_untracked_result_targets(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            init_repo(root)
            archive_source_path = pathlib.PurePosixPath(
                "docs/90.references/ref-9998-archive-source.md"
            )
            parent_source_path = pathlib.PurePosixPath(
                "docs/90.references/ref-9997-parent.md"
            )
            for path, artifact_id, title in (
                (archive_source_path, "ref-9998", "Archive Source"),
                (parent_source_path, "ref-9997", "Parent Source"),
            ):
                target = root / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(self._reference_text(artifact_id, title), encoding="utf-8")
            baseline = commit_all(root, "multi-row baseline")
            archived_blob = git(root, "rev-parse", f"{baseline}:{archive_source_path.as_posix()}")
            (root / archive_source_path).unlink()
            (root / parent_source_path).unlink()
            commit_all(root, "remove multi-row sources")

            archive_target_path = pathlib.PurePosixPath(
                "docs/98.archive/tombstones/05.operations/ref-9998-archive-source.md"
            )
            archive_target = root / archive_target_path
            archive_target.parent.mkdir(parents=True)
            archive_target.write_text(
                "---\n"
                + yaml.safe_dump(
                    {
                        "status": "archived",
                        "artifact_id": "ref-9998",
                        "artifact_type": "archive",
                        "parent_ids": ["ref-9997"],
                        "archived_from": archive_source_path.as_posix(),
                        "archived_at": "2026-07-14",
                        "archive_reason": "Withdrawn with preserved provenance.",
                        "archive_disposition": "withdrawn",
                        "archived_commit": baseline,
                        "archived_blob": archived_blob,
                        "preservation_class": "git-history",
                    },
                    sort_keys=False,
                )
                + "---\n\n# Archived Source\n",
                encoding="utf-8",
            )
            parent_target_path = pathlib.PurePosixPath(
                "docs/90.references/data/ref-9997-parent.md"
            )
            parent_target = root / parent_target_path
            parent_target.parent.mkdir(parents=True)
            parent_target.write_text(
                self._reference_text("ref-9997", "Moved Parent"),
                encoding="utf-8",
            )
            archive_row = self.valid_row(
                source_path=archive_source_path,
                target_path=archive_target_path,
                artifact_id="ref-9998",
                artifact_type="reference",
                status_before="active",
                status_after="archived",
                parent_ids=("ref-9997",),
                disposition="archive",
                canonical_replacement=None,
                active_consumers=(),
                preservation_class="git-history",
                evidence=self._destructive_evidence(),
                review_verdict=lifecycle.ReviewVerdict("pass", "pass"),
            )
            parent_row = self.valid_row(
                source_path=parent_source_path,
                target_path=parent_target_path,
                artifact_id="ref-9997",
                artifact_type="reference",
                status_before="active",
                status_after="active",
                parent_ids=(),
                disposition="move",
            )
            self.assertEqual(
                self._manifest_codes(root, baseline, (parent_row, archive_row)),
                set(),
            )


if __name__ == "__main__":
    unittest.main()
