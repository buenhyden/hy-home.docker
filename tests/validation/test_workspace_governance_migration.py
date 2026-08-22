from __future__ import annotations

from collections import Counter
from datetime import date
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import tarfile
import unittest

import yaml

from scripts.lib.document_governance.frontmatter import read_frontmatter_values
from scripts.lib.document_governance.links import parse_local_markdown_links


ROOT = Path(__file__).resolve().parents[2]
ADR = ROOT / "docs/02.architecture/decisions/0029-workspace-governance-authority.md"
MIGRATION = (
    ROOT
    / "docs/98.archive/migrations/mig-0003-workspace-governance-simplification.md"
)
CANONICAL_PACKAGE = (
    ROOT / "docs/03.specs/0153-workspace-governance-simplification"
)
LEGACY_PACKAGE = (
    ROOT / "docs/03.specs/spec-0153-workspace-governance-simplification"
)
EXPECTED_TASK_FILES = (
    "tsk-0001-control-plane.md",
    "tsk-0002-stage99.md",
    "tsk-0003-bootstrap.md",
    "tsk-0004-stage00.md",
    "tsk-0005-requirements.md",
    "tsk-0006-architecture.md",
    "tsk-0007-spec-lifecycle.md",
    "tsk-0008-operations.md",
    "tsk-0009-references.md",
    "tsk-0010-archive.md",
    "tsk-0011-script-tests.md",
    "tsk-0012-gates.md",
    "tsk-0013-closure.md",
)
BOOTSTRAP_EVIDENCE_BLOB = "f271bcf127e2ad766b6006210e9cba1d41176887"
BOOTSTRAP_EVIDENCE_SHA256 = (
    "1fc246c7b23a9d998939d1f40ae1af82fc41f7aed151ae3a1b162bbb9d2010ba"
)
EXPECTED_SELECTION_SHA256 = (
    "9328d04dc01ad60faa9be3f805eaa9414af1bacfe4751c61ef133749390e30e1"
)
EXPECTED_BASELINE_COMMIT = "889d3868ecd0913cddac79a718584a54a8453525"
EXPECTED_CONSUMER_POLICY = {
    "version": 1,
    "literal_references": "exact-repository-relative-path",
    "markdown_links": "shared-local-relative-parser",
    "delete_consumers": "inactive-when-delete-owner-task-lte-source-owner-task",
    "excluded_noncurrent": [
        "docs/98.archive/",
        "graphify-out/",
        "docs/90.references/research/",
        "docs/90.references/audits/",
        "docs/90.references/llm-wiki/",
        "docs/90.references/data/knowledge/",
        "docs/90.references/data/security/",
        "docs/90.references/data/governance/document-corpus-lifecycle/",
        "docs/90.references/*[generated_by]",
    ],
}
EXPECTED_OWNER_COUNTS = {
    3: 3,
    4: 128,
    5: 25,
    6: 51,
    7: 49,
    8: 193,
    9: 116,
    10: 275,
    11: 4,
    12: 8,
    13: 51,
}
EXPECTED_ACTION_COUNTS = {"delete": 356, "rename": 547}
EXPECTED_SOURCE_KIND_COUNTS = {"planned-output": 19, "tracked": 884}
REQUIRED_CREATION_KEYS = frozenset({"path", "artifact_id", "owner_task"})
REQUIRED_ROW_KEYS = frozenset(
    {
        "row_id",
        "source_path",
        "target_path",
        "artifact_id",
        "action",
        "owner_task",
        "source_kind",
        "source_owner_task",
        "active_consumers",
        "recovery_commit",
        "status",
    }
)


def _run_git(*args: str) -> bytes:
    return subprocess.run(
        ("git", *args), cwd=ROOT, check=True, capture_output=True
    ).stdout


def _level_two_section(text: str, heading: str) -> str:
    match = re.search(
        rf"^## {re.escape(heading)}\s*$\n(?P<body>.*?)(?=^## |\Z)",
        text,
        flags=re.DOTALL | re.MULTILINE,
    )
    if match is None:
        raise AssertionError(f"missing level-two section: {heading}")
    return match.group("body")


def _markdown_table_data_rows(section: str) -> tuple[tuple[str, ...], ...]:
    rows: list[tuple[str, ...]] = []
    after_separator = False
    for line in section.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or not stripped.endswith("|"):
            if stripped:
                after_separator = False
            continue
        cells = tuple(cell.strip() for cell in stripped[1:-1].split("|"))
        if cells and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            after_separator = True
        elif after_separator:
            rows.append(cells)
    return tuple(rows)


def _level_three_sections(section: str) -> dict[str, str]:
    matches = tuple(re.finditer(r"^### (?P<heading>.+?)\s*$", section, re.MULTILINE))
    return {
        match.group("heading"): section[
            match.end() : matches[index + 1].start()
            if index + 1 < len(matches)
            else len(section)
        ].strip()
        for index, match in enumerate(matches)
    }


class _StrictLedgerLoader(yaml.SafeLoader):
    def compose_node(self, parent: object, index: object) -> yaml.Node:
        event = self.peek_event()
        if isinstance(event, yaml.events.AliasEvent):
            raise AssertionError("YAML aliases are unsupported")
        if getattr(event, "anchor", None) is not None:
            raise AssertionError("YAML anchors are unsupported")
        if getattr(event, "tag", None) is not None:
            raise AssertionError("explicit YAML tags are unsupported")
        return super().compose_node(parent, index)

    def construct_mapping(
        self, node: yaml.MappingNode, deep: bool = False
    ) -> dict[object, object]:
        seen: set[object] = set()
        for key_node, _ in node.value:
            if key_node.tag == "tag:yaml.org,2002:merge":
                raise AssertionError("YAML merge aliases are unsupported")
            key = self.construct_object(key_node, deep=False)
            if key in seen:
                raise AssertionError(f"duplicate YAML key: {key!r}")
            seen.add(key)
        return super().construct_mapping(node, deep=deep)


def _load_ledger_text(text: str) -> dict[str, object]:
    matches = re.findall(
        r"^```(?:yaml|yml)[ \t]*\r?\n(.*?)^```[ \t]*$",
        text,
        flags=re.DOTALL | re.MULTILINE,
    )
    if len(matches) != 1:
        raise AssertionError("Migration must contain exactly one fenced YAML ledger")
    raw = yaml.load(matches[0], Loader=_StrictLedgerLoader)
    if not isinstance(raw, dict):
        raise AssertionError("Migration ledger must be a mapping")
    return raw


def _load_ledger() -> dict[str, object]:
    return _load_ledger_text(MIGRATION.read_text(encoding="utf-8"))


def _safe_path(value: object, *, nullable: bool = False) -> str | None:
    if value is None and nullable:
        return None
    if not isinstance(value, str) or not value:
        raise AssertionError(f"expected non-empty path, got {value!r}")
    if any(ord(character) < 32 or ord(character) == 127 for character in value):
        raise AssertionError(f"control character in path: {value!r}")
    path = PurePosixPath(value)
    if (
        path.is_absolute()
        or not path.parts
        or ".." in path.parts
        or value.startswith("-")
        or "\\" in value
        or value != path.as_posix()
    ):
        raise AssertionError(f"unsafe path: {value!r}")
    return value


def _safe_artifact_id(value: object) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not value:
        raise AssertionError(f"expected artifact_id string or null, got {value!r}")
    if value.startswith("<") and value.endswith(">"):
        raise AssertionError(f"placeholder artifact_id is not stable: {value!r}")
    return value


def _baseline_files(commit: str) -> dict[str, bytes]:
    archive = _run_git("archive", "--format=tar", commit)
    result: dict[str, bytes] = {}
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as tar:
        for member in tar.getmembers():
            if not member.isfile():
                continue
            extracted = tar.extractfile(member)
            if extracted is None:
                continue
            result[member.name] = extracted.read()
    return result


def _baseline_tree(commit: str) -> dict[str, tuple[str, str, str]]:
    result: dict[str, tuple[str, str, str]] = {}
    for record in _run_git("ls-tree", "-rz", "--full-tree", commit).split(b"\0"):
        if not record:
            continue
        metadata, encoded_path = record.split(b"\t", 1)
        mode, object_type, object_id = metadata.decode("ascii").split()
        path = encoded_path.decode("utf-8")
        _safe_path(path)
        result[path] = (mode, object_type, object_id)
    return result


def _inactive_consumer(
    path: str,
    content: bytes,
    source_owner_task: int,
    delete_owners: dict[str, int],
) -> bool:
    delete_owner = delete_owners.get(path)
    if delete_owner is not None and delete_owner <= source_owner_task:
        return True
    if path.startswith(("docs/98.archive/", "graphify-out/")):
        return True
    if path.startswith(
        (
            "docs/90.references/research/",
            "docs/90.references/audits/",
            "docs/90.references/llm-wiki/",
            "docs/90.references/data/knowledge/",
            "docs/90.references/data/security/",
            "docs/90.references/data/governance/document-corpus-lifecycle/",
        )
    ):
        return True
    return path.startswith("docs/90.references/") and b"generated_by:" in content[:2048]


def _markdown_targets(baseline: dict[str, bytes]) -> dict[str, frozenset[str]]:
    result: dict[str, frozenset[str]] = {}
    for candidate, content in baseline.items():
        if not candidate.endswith(".md"):
            continue
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError:
            continue
        links = parse_local_markdown_links(PurePosixPath(candidate), text)
        result[candidate] = frozenset(
            link.target.as_posix() for link in links if not link.has_unsafe_target
        )
    return result


def _active_consumers(
    source: str,
    source_owner_task: int,
    baseline: dict[str, bytes],
    delete_owners: dict[str, int],
    markdown_targets: dict[str, frozenset[str]],
) -> list[str]:
    needle = source.encode()
    return sorted(
        candidate
        for candidate, content in baseline.items()
        if candidate != source
        and not _inactive_consumer(
            candidate, content, source_owner_task, delete_owners
        )
        and (needle in content or source in markdown_targets.get(candidate, ()))
    )


def _validate_namespace(
    creations: list[dict[str, object]],
    rows: list[dict[str, object]],
    baseline_paths: set[str],
) -> None:
    creation_paths = [_safe_path(creation["path"]) for creation in creations]
    if len(creation_paths) != len(set(creation_paths)):
        raise AssertionError("planned creation collision")
    if set(creation_paths) & baseline_paths:
        raise AssertionError("planned creation collides with baseline")

    targets: dict[str, list[str]] = {}
    for row in rows:
        target = _safe_path(row["target_path"], nullable=True)
        if target is None:
            continue
        if target in baseline_paths or target in creation_paths:
            raise AssertionError(f"target namespace collision: {target}")
        targets.setdefault(target, []).append(str(row["action"]))
    for target, actions in targets.items():
        if len(actions) > 1 and set(actions) != {"merge"}:
            raise AssertionError(f"target collision without merge lineage: {target}")


def _selection_digest(ledger: dict[str, object]) -> str:
    payload = {
        key: ledger[key]
        for key in (
            "schema_version",
            "migration_id",
            "baseline_commit",
            "consumer_policy",
            "final_compaction",
            "planned_creations",
            "rows",
        )
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode()).hexdigest()


def _validate_execution_ledger_state(ledger: dict[str, object]) -> None:
    required = {
        "schema_version",
        "migration_id",
        "baseline_commit",
        "approval",
        "consumer_policy",
        "final_compaction",
        "planned_creations",
        "rows",
    }
    if frozenset(ledger) != required or ledger.get("schema_version") != 2:
        raise AssertionError("execution Migration schema is invalid")
    approval = ledger.get("approval")
    if not isinstance(approval, dict) or frozenset(approval) != {
        "status",
        "approved_by",
        "approved_at",
    }:
        raise AssertionError("execution Migration approval fields are invalid")
    status = approval["status"]
    if status == "pending":
        if approval["approved_by"] is not None or approval["approved_at"] is not None:
            raise AssertionError("pending approval identity and date must be null")
        return
    if status != "approved":
        raise AssertionError("execution Migration status must be pending or approved")
    approved_by = approval["approved_by"]
    approved_at = approval["approved_at"]
    if not isinstance(approved_by, str) or not approved_by.strip():
        raise AssertionError("approved Migration requires approved_by")
    if not isinstance(approved_at, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", approved_at):
        raise AssertionError("approved Migration requires YYYY-MM-DD approved_at")
    try:
        parsed = date.fromisoformat(approved_at)
    except ValueError as error:
        raise AssertionError("approved_at must be a real calendar date") from error
    if parsed.isoformat() != approved_at:
        raise AssertionError("approved_at must be canonical YYYY-MM-DD")


def _validate_final_compaction(compacted: dict[str, object]) -> None:
    if frozenset(compacted) != {"schema_version", "migration_id", "rows"}:
        raise AssertionError("final Migration top-level fields are not minimal")
    if compacted["schema_version"] != 3:
        raise AssertionError("final Migration schema must be version 3")
    if compacted["migration_id"] != "mig-0003":
        raise AssertionError("final Migration identity is invalid")
    rows = compacted["rows"]
    if not isinstance(rows, list):
        raise AssertionError("final Migration rows must be a list")
    required = {
        "source_path",
        "target_path",
        "artifact_id",
        "action",
        "recovery_commit",
    }
    for row in rows:
        if not isinstance(row, dict) or frozenset(row) != required:
            raise AssertionError("final Migration row fields are not minimal")
        _safe_path(row["source_path"])
        _safe_path(row["target_path"], nullable=True)
        _safe_artifact_id(row["artifact_id"])
        if row["action"] not in {"rename", "merge", "delete"}:
            raise AssertionError("final Migration action is invalid")
        if row["action"] == "delete" and row["target_path"] is not None:
            raise AssertionError("final delete mapping target must be null")
        if row["action"] != "delete" and row["target_path"] is None:
            raise AssertionError("final move mapping target is required")
        recovery = row["recovery_commit"]
        if not isinstance(recovery, str) or not re.fullmatch(r"[0-9a-f]{40}", recovery):
            raise AssertionError("final Migration recovery commit is required")


class WorkspaceGovernanceMigrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.ledger = _load_ledger()
        commit = cls.ledger.get("baseline_commit")
        if not isinstance(commit, str) or not re.fullmatch(r"[0-9a-f]{40}", commit):
            raise AssertionError("baseline_commit must be a full Git object ID")
        if commit != EXPECTED_BASELINE_COMMIT:
            raise AssertionError("baseline_commit does not match the reviewed commit")
        object_type = _run_git("cat-file", "-t", commit).decode().strip()
        if object_type != "commit":
            raise AssertionError("baseline_commit must identify a Git commit")
        cls.baseline = _baseline_files(commit)
        cls.baseline_tree = _baseline_tree(commit)
        cls.markdown_targets = _markdown_targets(cls.baseline)
        cls.creations = cls.ledger.get("planned_creations")
        cls.rows = cls.ledger.get("rows")
        if not isinstance(cls.creations, list) or not isinstance(cls.rows, list):
            raise AssertionError("planned_creations and rows must be lists")

    def test_governance_migration_control_plane_exists(self) -> None:
        self.assertTrue(ADR.is_file())
        self.assertTrue(MIGRATION.is_file())

    def test_spec_0153_uses_canonical_package(self) -> None:
        self.assertFalse(LEGACY_PACKAGE.exists())
        self.assertTrue(CANONICAL_PACKAGE.joinpath("README.md").is_file())
        self.assertTrue(CANONICAL_PACKAGE.joinpath("spec.md").is_file())
        self.assertTrue(CANONICAL_PACKAGE.joinpath("plan.md").is_file())
        self.assertFalse(CANONICAL_PACKAGE.joinpath("task.md").exists())
        self.assertEqual(
            EXPECTED_TASK_FILES,
            tuple(
                path.name
                for path in sorted(CANONICAL_PACKAGE.joinpath("tasks").glob("tsk-*.md"))
            ),
        )

    def test_spec_0153_supersedes_spec_0136_reciprocally(self) -> None:
        self.assertTrue(CANONICAL_PACKAGE.joinpath("spec.md").is_file())
        current = read_frontmatter_values(CANONICAL_PACKAGE / "spec.md")
        predecessor = read_frontmatter_values(
            ROOT / "docs/03.specs/0136-sdlc-taxonomy-convergence/spec.md"
        )

        self.assertEqual("SPEC-0153", current["artifact_id"])
        self.assertIn("SPEC-0136", current["supersedes"])
        self.assertEqual("SPEC-0153", predecessor["superseded_by"])

    def test_spec_0153_task_evidence_is_complete_and_nonprospective(self) -> None:
        tasks = CANONICAL_PACKAGE / "tasks"
        self.assertTrue(tasks.joinpath("tsk-0001-control-plane.md").is_file())
        self.assertTrue(tasks.joinpath("tsk-0002-stage99.md").is_file())
        control_plane = tasks.joinpath("tsk-0001-control-plane.md").read_text(
            encoding="utf-8"
        )
        stage99 = tasks.joinpath("tsk-0002-stage99.md").read_text(encoding="utf-8")
        bootstrap = tasks.joinpath("tsk-0003-bootstrap.md").read_text(
            encoding="utf-8"
        )
        self.assertIn(EXPECTED_SELECTION_SHA256, control_plane)
        self.assertIn("e58d91796409fd562a8b395293942c0f73949c24", control_plane)
        self.assertIn("71f89ba1", control_plane)
        self.assertIn("Task 2 Registry RED", stage99)
        self.assertIn("APPROVED C0/I0/M0", stage99)
        self.assertIn("c891118e736ee46c709b22de459c20858467ddd3", stage99)
        self.assertIn("8cc65475", stage99)
        self.assertGreater(
            len(
                _markdown_table_data_rows(
                    _level_two_section(bootstrap, "Work Log")
                )
            ),
            0,
        )
        self.assertGreater(
            len(
                _markdown_table_data_rows(
                    _level_two_section(bootstrap, "Verification Evidence")
                )
            ),
            0,
        )
        self.assertGreater(
            len(
                _markdown_table_data_rows(
                    _level_two_section(bootstrap, "Review Evidence")
                )
            ),
            0,
        )
        self.assertEqual(
            (),
            _markdown_table_data_rows(
                _level_two_section(bootstrap, "Commit Ledger")
            ),
        )

        for index, filename in enumerate(EXPECTED_TASK_FILES, start=1):
            values = read_frontmatter_values(tasks / filename)
            self.assertEqual("task", values["profile_id"])
            self.assertEqual(f"task-0153-{index:04d}", values["artifact_id"])
            self.assertEqual(["SPEC-0153", "plan-0153"], values["parent_ids"])
            if index <= 3:
                self.assertEqual("completed", values["status"])
            else:
                self.assertEqual("draft", values["status"])

    def test_spec_0153_completed_task_evidence_partitions_source_blob(self) -> None:
        source_bytes = _run_git("cat-file", "blob", BOOTSTRAP_EVIDENCE_BLOB)
        self.assertEqual(
            BOOTSTRAP_EVIDENCE_SHA256,
            hashlib.sha256(source_bytes).hexdigest(),
        )
        source = source_bytes.decode("utf-8")
        tasks = CANONICAL_PACKAGE / "tasks"
        task1 = tasks.joinpath("tsk-0001-control-plane.md").read_text(
            encoding="utf-8"
        )
        task2 = tasks.joinpath("tsk-0002-stage99.md").read_text(encoding="utf-8")

        source_work_rows = _markdown_table_data_rows(
            _level_two_section(source, "Work Log")
        )
        source_task2_work = tuple(
            row for row in source_work_rows if row[0].startswith("Task 2")
        )
        source_task1_work = tuple(
            row for row in source_work_rows if not row[0].startswith("Task 2")
        )
        self.assertEqual(
            source_task1_work,
            _markdown_table_data_rows(_level_two_section(task1, "Work Log")),
        )
        self.assertEqual(
            source_task2_work,
            _markdown_table_data_rows(_level_two_section(task2, "Work Log")),
        )

        source_review_rows = _markdown_table_data_rows(
            _level_two_section(source, "Review Evidence")
        )
        source_task2_reviews = {
            row for row in source_review_rows if row[0].startswith("Task 2")
        }
        source_task1_reviews = tuple(
            row for row in source_review_rows if not row[0].startswith("Task 2")
        )
        task2_reviews = set(
            _markdown_table_data_rows(_level_two_section(task2, "Review Evidence"))
        )
        self.assertEqual(
            source_task1_reviews,
            _markdown_table_data_rows(_level_two_section(task1, "Review Evidence")),
        )
        self.assertTrue(source_task2_reviews <= task2_reviews)

        source_commits = tuple(
            re.findall(
                r"`([0-9a-f]{40})`",
                _level_two_section(source, "Commit Ledger"),
            )
        )
        self.assertEqual(
            (
                "e58d91796409fd562a8b395293942c0f73949c24",
                "c891118e736ee46c709b22de459c20858467ddd3",
            ),
            source_commits,
        )
        self.assertIn(source_commits[0], _level_two_section(task1, "Commit Ledger"))
        self.assertIn(source_commits[1], _level_two_section(task2, "Commit Ledger"))

    def test_spec_0153_verification_evidence_partitions_source_blob(self) -> None:
        source = _run_git("cat-file", "blob", BOOTSTRAP_EVIDENCE_BLOB).decode(
            "utf-8"
        )
        tasks = CANONICAL_PACKAGE / "tasks"
        task1 = tasks.joinpath("tsk-0001-control-plane.md").read_text(
            encoding="utf-8"
        )
        task2 = tasks.joinpath("tsk-0002-stage99.md").read_text(encoding="utf-8")
        source_sections = _level_three_sections(
            _level_two_section(source, "Verification Evidence")
        )
        task1_sections = _level_three_sections(
            _level_two_section(task1, "Verification Evidence")
        )
        task2_sections = _level_three_sections(
            _level_two_section(task2, "Verification Evidence")
        )
        task1_headings = (
            "Initial RED",
            "Focused GREEN",
            "Quality Remediation RED",
            "Lifecycle Remediation RED",
            "Initial Review Remediation Probe",
        )
        self.assertEqual(
            {*task1_headings, "Task 2 Registry RED and GREEN"},
            set(source_sections),
        )
        for heading in task1_headings:
            with self.subTest(task="tsk-0001", section=heading):
                self.assertEqual(source_sections[heading], task1_sections[heading])
        self.assertIn("Task 2 Registry RED and GREEN", task2_sections)
        self.assertEqual(
            source_sections["Task 2 Registry RED and GREEN"],
            task2_sections["Task 2 Registry RED and GREEN"],
        )

    def test_spec_0153_draft_tasks_have_no_evidence_rows(self) -> None:
        tasks = CANONICAL_PACKAGE / "tasks"
        evidence_sections = (
            "Work Log",
            "Verification Evidence",
            "Review Evidence",
            "Commit Ledger",
        )

        for filename in EXPECTED_TASK_FILES[3:]:
            text = tasks.joinpath(filename).read_text(encoding="utf-8")
            for heading in evidence_sections:
                with self.subTest(task=filename, section=heading):
                    self.assertEqual(
                        (),
                        _markdown_table_data_rows(_level_two_section(text, heading)),
                    )

    def test_approved_selection_is_exact_and_reviewable(self) -> None:
        _validate_execution_ledger_state(self.ledger)
        self.assertEqual(self.ledger.get("schema_version"), 2)
        self.assertEqual(self.ledger.get("migration_id"), "mig-0003")
        self.assertEqual(
            self.ledger.get("approval"),
            {
                "status": "approved",
                "approved_by": "user",
                "approved_at": "2026-08-20",
            },
        )
        self.assertEqual(len(self.creations), 17)
        self.assertEqual(len(self.rows), 903)
        self.assertEqual(self.ledger.get("baseline_commit"), EXPECTED_BASELINE_COMMIT)
        self.assertEqual(
            frozenset(self.ledger),
            frozenset(
                {
                    "schema_version",
                    "migration_id",
                    "baseline_commit",
                    "approval",
                    "consumer_policy",
                    "final_compaction",
                    "planned_creations",
                    "rows",
                }
            ),
        )
        consumer_policy = self.ledger.get("consumer_policy")
        self.assertIsInstance(consumer_policy, dict)
        self.assertEqual(
            {key: value for key, value in consumer_policy.items() if key != "derived_edges_sha256"},
            EXPECTED_CONSUMER_POLICY,
        )
        self.assertRegex(consumer_policy["derived_edges_sha256"], r"^[0-9a-f]{64}$")
        final_compaction = self.ledger.get("final_compaction")
        self.assertEqual(
            final_compaction,
            {
                "owner_task": 13,
                "schema_version": 3,
                "top_level_keys": ["schema_version", "migration_id", "rows"],
                "row_keys": [
                    "source_path",
                    "target_path",
                    "artifact_id",
                    "action",
                    "recovery_commit",
                ],
            },
        )
        self.assertEqual(
            Counter(row["owner_task"] for row in self.rows),
            Counter(EXPECTED_OWNER_COUNTS),
        )
        self.assertEqual(
            Counter(row["action"] for row in self.rows),
            Counter(EXPECTED_ACTION_COUNTS),
        )
        self.assertEqual(
            Counter(row["source_kind"] for row in self.rows),
            Counter(EXPECTED_SOURCE_KIND_COUNTS),
        )

        self.assertEqual(_selection_digest(self.ledger), EXPECTED_SELECTION_SHA256)

        changed_baseline = dict(self.ledger)
        changed_baseline["baseline_commit"] = "0" * 40
        self.assertNotEqual(_selection_digest(changed_baseline), EXPECTED_SELECTION_SHA256)
        changed_policy = dict(self.ledger)
        changed_policy["consumer_policy"] = {
            **consumer_policy,
            "markdown_links": "disabled",
        }
        self.assertNotEqual(_selection_digest(changed_policy), EXPECTED_SELECTION_SHA256)

    def test_execution_ledger_lifecycle_mutations(self) -> None:
        _validate_execution_ledger_state(self.ledger)

        pending = dict(self.ledger)
        pending["approval"] = {
            "status": "pending",
            "approved_by": None,
            "approved_at": None,
        }
        _validate_execution_ledger_state(pending)
        self.assertEqual(_selection_digest(pending), EXPECTED_SELECTION_SHA256)

        invalid_approvals = (
            {"status": "pending", "approved_by": "owner", "approved_at": None},
            {"status": "pending", "approved_by": None, "approved_at": "2026-08-20"},
            {"status": "approved", "approved_by": None, "approved_at": "2026-08-20"},
            {"status": "approved", "approved_by": "owner", "approved_at": None},
            {"status": "approved", "approved_by": "owner", "approved_at": "20-08-2026"},
            {"status": "completed", "approved_by": "owner", "approved_at": "2026-08-20"},
        )
        for approval in invalid_approvals:
            with self.subTest(approval=approval):
                mutated = dict(self.ledger)
                mutated["approval"] = approval
                with self.assertRaises(AssertionError):
                    _validate_execution_ledger_state(mutated)

    def test_planned_creations_are_unique_and_typed(self) -> None:
        paths: list[str] = []
        for creation in self.creations:
            self.assertIsInstance(creation, dict)
            self.assertEqual(frozenset(creation), REQUIRED_CREATION_KEYS)
            path = _safe_path(creation["path"])
            assert path is not None
            paths.append(path)
            self.assertNotIn(path, self.baseline)
            _safe_artifact_id(creation["artifact_id"])
            self.assertIsInstance(creation["owner_task"], int)
            self.assertGreaterEqual(creation["owner_task"], 1)
            self.assertLessEqual(creation["owner_task"], 13)
        self.assertEqual(len(paths), len(set(paths)))
        targets = {
            row["target_path"] for row in self.rows if row["target_path"] is not None
        }
        self.assertFalse(set(paths) & targets)
        _validate_namespace(self.creations, self.rows, set(self.baseline))
        creation_identities = {
            (creation["path"], creation["artifact_id"]) for creation in self.creations
        }
        planned_sources = {
            (row["source_path"], row["artifact_id"])
            for row in self.rows
            if row["source_kind"] == "planned-output"
        }
        self.assertTrue(creation_identities.issubset(planned_sources))

    def test_final_compaction_contract_is_minimal(self) -> None:
        compacted = {
            "schema_version": 3,
            "migration_id": "mig-0003",
            "rows": [
                {
                    "source_path": "docs/legacy.md",
                    "target_path": "docs/current.md",
                    "artifact_id": "EXAMPLE-0001",
                    "action": "rename",
                    "recovery_commit": EXPECTED_BASELINE_COMMIT,
                }
            ],
        }
        _validate_final_compaction(compacted)

        extra_field = {**compacted, "approval": {"status": "approved"}}
        with self.assertRaisesRegex(AssertionError, "top-level"):
            _validate_final_compaction(extra_field)
        null_recovery = {
            **compacted,
            "rows": [{**compacted["rows"][0], "recovery_commit": None}],
        }
        with self.assertRaisesRegex(AssertionError, "recovery"):
            _validate_final_compaction(null_recovery)
        execution_schema = {**compacted, "schema_version": 2}
        with self.assertRaisesRegex(AssertionError, "schema"):
            _validate_final_compaction(execution_schema)

    def test_namespace_mutations_fail_closed(self) -> None:
        colliding_creation = [dict(item) for item in self.creations]
        colliding_creation[0]["path"] = next(iter(self.baseline))
        with self.assertRaisesRegex(AssertionError, "baseline"):
            _validate_namespace(colliding_creation, self.rows, set(self.baseline))

        colliding_target = [dict(item) for item in self.rows]
        colliding_target[0]["target_path"] = self.creations[0]["path"]
        with self.assertRaisesRegex(AssertionError, "target namespace"):
            _validate_namespace(self.creations, colliding_target, set(self.baseline))

    def test_yaml_contract_rejects_ambiguity(self) -> None:
        source = MIGRATION.read_text(encoding="utf-8")
        with self.assertRaisesRegex(AssertionError, "exactly one"):
            _load_ledger_text(source + "\n```yaml\nextra: true\n```\n")
        with self.assertRaisesRegex(AssertionError, "duplicate"):
            _load_ledger_text("```yaml\nschema_version: 2\nschema_version: 3\n```")
        with self.assertRaisesRegex(AssertionError, "alias|anchor"):
            _load_ledger_text("```yaml\nvalue: &shared []\nalias: *shared\n```")
        with self.assertRaisesRegex(AssertionError, "tag"):
            _load_ledger_text("```yaml\nvalue: !!str tagged\n```")
        with self.assertRaisesRegex(AssertionError, "merge"):
            _load_ledger_text("```yaml\nvalue:\n  <<: {nested: true}\n```")

    def test_paths_are_canonical_posix(self) -> None:
        for invalid in (
            "docs//source.md",
            "docs/./source.md",
            "docs\\source.md",
            "docs/source.md\x7f",
            ".",
        ):
            with self.subTest(invalid=invalid):
                with self.assertRaises(AssertionError):
                    _safe_path(invalid)

    def test_consumer_policy_covers_ordered_and_relative_edges(self) -> None:
        rows = {row["source_path"]: row for row in self.rows}
        self.assertIn(
            "scripts/validation/check-repo-contracts.sh",
            rows["docs/00.agent-governance/rules/agentic.md"]["active_consumers"],
        )
        self.assertIn(
            "docs/02.architecture/decisions/README.md",
            rows[
                "docs/02.architecture/decisions/adr-0027-stage-00-canonical-adapter-model.md"
            ]["active_consumers"],
        )

        edge_payload = [
            {
                "row_id": row["row_id"],
                "active_consumers": row["active_consumers"],
            }
            for row in self.rows
        ]
        edge_digest = hashlib.sha256(
            json.dumps(edge_payload, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        self.assertEqual(
            self.ledger["consumer_policy"]["derived_edges_sha256"], edge_digest
        )

    def test_transition_rows_fail_closed(self) -> None:
        row_ids: list[str] = []
        source_identities: list[tuple[str, int]] = []
        target_owners: dict[str, list[str]] = {}
        delete_owners = {
            row["source_path"]: row["owner_task"]
            for row in self.rows
            if row["action"] == "delete"
        }
        creations = {
            (creation["path"], creation["artifact_id"]): creation["owner_task"]
            for creation in self.creations
        }
        earlier_targets: dict[tuple[str, object], int] = {}

        for row in self.rows:
            self.assertIsInstance(row, dict)
            self.assertEqual(frozenset(row), REQUIRED_ROW_KEYS)
            self.assertRegex(row["row_id"], r"^mig-0003-r\d{4}$")
            row_ids.append(row["row_id"])
            source = _safe_path(row["source_path"])
            assert source is not None
            target = _safe_path(row["target_path"], nullable=True)
            _safe_artifact_id(row["artifact_id"])
            self.assertIn(row["action"], {"rename", "merge", "delete"})
            self.assertNotEqual(row["action"], "create")
            self.assertIn(row["owner_task"], range(3, 14))
            self.assertIn(row["source_kind"], {"tracked", "planned-output"})
            self.assertEqual(row["status"], "planned")
            self.assertIsNone(row["recovery_commit"])
            self.assertIsInstance(row["active_consumers"], list)
            self.assertEqual(
                row["active_consumers"], sorted(set(row["active_consumers"]))
            )
            for consumer in row["active_consumers"]:
                _safe_path(consumer)
            source_identities.append((source, row["owner_task"]))

            if row["action"] == "delete":
                self.assertIsNone(target)
            else:
                self.assertIsNotNone(target)
            if target is not None:
                target_owners.setdefault(target, []).append(row["action"])
                if row["action"] != "merge":
                    self.assertNotIn(
                        target,
                        self.baseline,
                        msg=f"target already exists at baseline: {row['row_id']}",
                    )

            if row["source_kind"] == "tracked":
                self.assertIsNone(row["source_owner_task"])
                self.assertIn(source, self.baseline)
                mode, object_type, object_id = self.baseline_tree[source]
                self.assertIn(mode, {"100644", "100755"})
                self.assertEqual(object_type, "blob")
                self.assertRegex(object_id, r"^[0-9a-f]{40}$")
                self.assertEqual(
                    row["active_consumers"],
                    _active_consumers(
                        source,
                        row["owner_task"],
                        self.baseline,
                        delete_owners,
                        self.markdown_targets,
                    ),
                )
            else:
                self.assertIsInstance(row["source_owner_task"], int)
                self.assertLess(row["source_owner_task"], row["owner_task"])
                self.assertEqual(row["active_consumers"], [])
                creation_owner = creations.get((source, row["artifact_id"]))
                transition_owner = earlier_targets.get(
                    (source, row["artifact_id"])
                )
                self.assertIn(
                    row["source_owner_task"],
                    {creation_owner, transition_owner},
                    msg=f"unresolved planned output: {row['row_id']}",
                )

            if target is not None:
                earlier_targets[(target, row["artifact_id"])] = row["owner_task"]

            lowered_target = (target or "").lower()
            self.assertNotIn("docs/05.operations/releases/", lowered_target)
            self.assertNotIn("gemini", lowered_target)
            self.assertNotIn("antigravity", lowered_target)

        self.assertEqual(len(row_ids), len(set(row_ids)))
        self.assertEqual(len(source_identities), len(set(source_identities)))
        for target, actions in target_owners.items():
            if len(actions) > 1:
                self.assertEqual(
                    set(actions), {"merge"}, msg=f"target collision: {target}"
                )

    def test_structural_source_families_are_complete(self) -> None:
        sources = {row["source_path"] for row in self.rows}
        baseline_paths = set(self.baseline)

        selected_families = {
            "requirements": {
                path
                for path in baseline_paths
                if re.fullmatch(r"docs/01\.requirements/prd-\d{4}-.+\.md", path)
            },
            "architecture": {
                path
                for path in baseline_paths
                if re.fullmatch(
                    r"docs/02\.architecture/(?:descriptions/ad|decisions/adr)-\d{4}-.+\.md",
                    path,
                )
            },
            "stage04": {
                path
                for path in baseline_paths
                if path.startswith("docs/04.execution/")
            },
            "operations-subjects": {
                path
                for path in baseline_paths
                if re.fullmatch(
                    r"docs/05\.operations/catalog/[^/]+/ops-\d{4}-[^/]+/(?:guide|policy|runbook)\.md",
                    path,
                )
            },
            "archive-changes": {
                path
                for path in baseline_paths
                if path.startswith("docs/98.archive/changes/")
            },
            "archive-tombstones": {
                path
                for path in baseline_paths
                if path.startswith("docs/98.archive/tombstones/")
            },
            "stage99-support": {
                path
                for path in baseline_paths
                if path.startswith("docs/99.templates/support/")
            },
        }
        expected_sizes = {
            "requirements": 25,
            "architecture": 50,
            "stage04": 7,
            "operations-subjects": 192,
            "archive-changes": 234,
            "archive-tombstones": 38,
            "stage99-support": 14,
        }
        for family, selected in selected_families.items():
            self.assertEqual(len(selected), expected_sizes[family], family)
            self.assertTrue(selected.issubset(sources), family)


if __name__ == "__main__":
    unittest.main()
