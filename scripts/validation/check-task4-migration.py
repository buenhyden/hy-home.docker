#!/usr/bin/env python3
"""Verify the exact approved Task 4 subset of Migration mig-0003."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
import pathlib
import re
import sys

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[2]
MIGRATION = ROOT / "docs/98.archive/migrations/0003-workspace-governance-simplification.md"
EXPECTED_SELECTION_SHA256 = "9328d04dc01ad60faa9be3f805eaa9414af1bacfe4751c61ef133749390e30e1"
EXPECTED_EDGES_SHA256 = "2f1840983d98ed93ffdc183305c49b389b17e5c8362538e5df97d451be2b9139"
EXPECTED_TASK4_ROWS_SHA256 = "2fd01449c78581374d37153175455ca0d08e2ca05e36812dcab8189a97208f95"
EXPECTED_ROW_IDS = tuple(f"mig-0003-r{value:04d}" for value in range(4, 132))
ROW_KEYS = {
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


class VerificationError(ValueError):
    """Raised when the frozen migration selection differs."""


class _StrictLoader(yaml.SafeLoader):
    def compose_node(self, parent: object, index: object) -> yaml.Node:
        event = self.peek_event()
        if isinstance(event, yaml.events.AliasEvent):
            raise VerificationError("YAML aliases are unsupported")
        if getattr(event, "anchor", None) is not None:
            raise VerificationError("YAML anchors are unsupported")
        if getattr(event, "tag", None) is not None:
            raise VerificationError("explicit YAML tags are unsupported")
        return super().compose_node(parent, index)

    def construct_mapping(
        self, node: yaml.MappingNode, deep: bool = False
    ) -> dict[object, object]:
        seen: set[object] = set()
        for key_node, _ in node.value:
            if key_node.tag == "tag:yaml.org,2002:merge":
                raise VerificationError("YAML merge aliases are unsupported")
            key = self.construct_object(key_node, deep=False)
            if key in seen:
                raise VerificationError(f"duplicate YAML key: {key!r}")
            seen.add(key)
        return super().construct_mapping(node, deep=deep)


def _load_ledger() -> dict[str, object]:
    try:
        text = MIGRATION.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise VerificationError("migration is unreadable") from error
    matches = re.findall(
        r"^```(?:yaml|yml)[ \t]*\r?\n(.*?)^```[ \t]*$",
        text,
        flags=re.DOTALL | re.MULTILINE,
    )
    if len(matches) != 1:
        raise VerificationError("migration must contain exactly one YAML ledger")
    try:
        value = yaml.load(matches[0], Loader=_StrictLoader)
    except yaml.YAMLError as error:
        raise VerificationError("migration YAML is invalid") from error
    if not isinstance(value, dict):
        raise VerificationError("migration ledger must be a mapping")
    return value


def _digest(value: object, *, sort_keys: bool = True) -> str:
    payload = json.dumps(
        value, sort_keys=sort_keys, separators=(",", ":"), ensure_ascii=False
    ).encode()
    return hashlib.sha256(payload).hexdigest()


def _verify() -> tuple[int, int, int, int]:
    ledger = _load_ledger()
    selection = {
        key: ledger.get(key)
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
    rows = ledger.get("rows")
    if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
        raise VerificationError("migration rows are invalid")
    task_rows = [row for row in rows if row.get("owner_task") == 4]
    if len(task_rows) != 128:
        raise VerificationError("Task 4 totals changed")
    if tuple(row.get("row_id") for row in task_rows) != EXPECTED_ROW_IDS:
        raise VerificationError("Task 4 row identities changed")
    if any(set(row) != ROW_KEYS for row in task_rows):
        raise VerificationError("Task 4 row schema changed")
    actions = Counter(row.get("action") for row in task_rows)
    if actions != Counter({"rename": 81, "delete": 47}):
        raise VerificationError("Task 4 action counts changed")
    for row in task_rows:
        if row["action"] == "delete" and row["target_path"] is not None:
            raise VerificationError(f"delete row has target: {row['row_id']}")
        if row["action"] == "rename" and not isinstance(row["target_path"], str):
            raise VerificationError(f"rename row lacks target: {row['row_id']}")
        if not isinstance(row["source_path"], str) or not row["source_path"]:
            raise VerificationError(f"row lacks source: {row['row_id']}")
        if not isinstance(row["active_consumers"], list):
            raise VerificationError(f"row has invalid consumers: {row['row_id']}")
    tuple_payload = [
        [row["row_id"], row["source_path"], row["target_path"], row["action"]]
        for row in task_rows
    ]
    if _digest(tuple_payload, sort_keys=False) != EXPECTED_TASK4_ROWS_SHA256:
        raise VerificationError("Task 4 source/target/action mapping changed")
    edge_payload = [
        {"row_id": row.get("row_id"), "active_consumers": row.get("active_consumers")}
        for row in rows
    ]
    edge_digest = _digest(edge_payload)
    policy = ledger.get("consumer_policy")
    if (
        not isinstance(policy, dict)
        or policy.get("derived_edges_sha256") != EXPECTED_EDGES_SHA256
        or edge_digest != EXPECTED_EDGES_SHA256
    ):
        raise VerificationError("derived consumer-edge digest changed")
    edges = sum(len(row["active_consumers"]) for row in task_rows)
    if edges != 1134:
        raise VerificationError("Task 4 active-consumer edge count changed")
    if _digest(selection) != EXPECTED_SELECTION_SHA256:
        raise VerificationError("approved selection digest changed")
    return len(task_rows), actions["rename"], actions["delete"], edges


def main() -> int:
    try:
        rows, renames, deletes, edges = _verify()
    except VerificationError as error:
        print(f"task4_migration: FAIL {error}", file=sys.stderr)
        return 1
    print(
        "task4_migration: PASS "
        f"rows={rows} rename={renames} delete={deletes} edges={edges}"
    )
    print(f"selection_sha256={EXPECTED_SELECTION_SHA256}")
    print(f"edges_sha256={EXPECTED_EDGES_SHA256}")
    print(f"task4_rows_sha256={EXPECTED_TASK4_ROWS_SHA256}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
