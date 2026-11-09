"""Re-bind SEC01 ledger Compose file hashes after a hash-only drift.

Dry run by default. A row is re-bound only when its declared image and build
still match Compose; a changed image or build, or any added or removed row,
service or include input, stops the run because those need real update
evidence. Only hashes are written, never review, scan or acceptance fields.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

from scripts.lib.supply_chain.latest_version_gate import expected_from_root

LEDGER = "infra/09-platform-ops/security-updates/update-ledger.json"
REVISION = re.compile(r"[0-9a-f]{40}")


def _dump(document):
    return json.dumps(document, indent=2, ensure_ascii=False) + "\n"


def plan(root, ledger):
    """Return (drifted rows, changed include paths, blockers, inventory)."""
    from scripts.lib.document_governance.operations_catalog import _compose_mapping

    expected, inventory = expected_from_root(root)
    blockers = []
    rows = {row["service"]: row for row in ledger["entries"]}
    for name in sorted(set(expected) - set(rows)):
        blockers.append(f"service without a ledger row: {name}")
    for name in sorted(set(rows) - set(expected)):
        blockers.append(f"ledger row without a Compose service: {name}")
    if set(ledger["expected_services"]) != set(rows):
        blockers.append("expected_services differs from the ledger rows")
    current = {item["path"]: item["sha256"] for item in inventory["input_files"]}
    recorded = {item["path"]: item["sha256"] for item in ledger["include_inputs"]}
    for path in sorted(set(current) ^ set(recorded)):
        blockers.append(f"include input added or removed: {path}")
    changed = sorted(p for p in current if p in recorded and current[p] != recorded[p])
    drifted = []
    for name, row in sorted(rows.items()):
        if name not in expected:
            continue
        service = _compose_mapping(root, Path(row["compose_file"]))["services"].get(
            name
        )
        if service is None:
            blockers.append(f"service missing from {row['compose_file']}: {name}")
            continue
        if service.get("image", "UNKNOWN") != row["current_declared"]:
            blockers.append(f"image changed, needs update evidence: {name}")
        elif service.get("build") != row["build_source"]:
            blockers.append(f"build changed, needs update evidence: {name}")
        elif (
            hashlib.sha256((root / row["compose_file"]).read_bytes()).hexdigest()
            != row["source_input_sha256"]
        ):
            drifted.append(name)
    return drifted, changed, blockers, inventory


def apply(root, ledger, drifted, changed, inventory, source_revision, refreshed_at):
    """Return a re-bound copy of the ledger with the previous binding kept."""
    result = copy.deepcopy(ledger)
    rows = {row["service"]: row for row in result["entries"]}
    previous = [
        {
            "service": name,
            "source_input_sha256": rows[name]["source_input_sha256"],
            "source_refreshed_at": rows[name]["source_refreshed_at"],
        }
        for name in drifted
    ]
    for name in drifted:
        rows[name]["source_input_sha256"] = hashlib.sha256(
            (root / rows[name]["compose_file"]).read_bytes()
        ).hexdigest()
    result["source_refreshes"].append(
        {
            "source_revision": source_revision,
            "refreshed_at": refreshed_at,
            "revision_scope": "Compose file hash re-binding only",
            "input_manifest_sha256": inventory["input_manifest_sha256"],
            "previous_include_inputs": ledger["include_inputs"],
            "changed_inputs": changed,
            "previous_service_source_bindings": previous,
            "meaning": (
                f"{len(changed)} root Compose inputs changed after their rows were "
                "last bound. Declared image and build fields are unchanged, so only "
                f"include hashes and the source_input_sha256 of {len(previous)} rows "
                "were re-bound; their source_refreshed_at is unchanged. No vendor "
                "lookup, signature, SBOM, scan, native, deployment or recovery "
                "acceptance."
            ),
        }
    )
    result["include_inputs"] = inventory["input_files"]
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root", type=Path, default=Path(__file__).resolve().parents[3]
    )
    parser.add_argument("--ledger", type=Path, help=f"default: <repo-root>/{LEDGER}")
    parser.add_argument("--write", action="store_true", help="apply the plan")
    parser.add_argument("--source-revision", help="40-hex commit; required by --write")
    parser.add_argument("--refreshed-at", help="ISO timestamp; default: now (UTC)")
    args = parser.parse_args(argv)
    root = args.repo_root.resolve()
    path = args.ledger or root / LEDGER
    try:
        text = path.read_text(encoding="utf-8")
        ledger = json.loads(text)
        if _dump(ledger) != text:
            raise ValueError("ledger formatting is not canonical")
        drifted, changed, blockers, inventory = plan(root, ledger)
    except (ValueError, TypeError, OSError, KeyError, AttributeError) as error:
        print(f"Invalid update ledger: {type(error).__name__}", file=sys.stderr)
        return 2
    if blockers:
        print("BLOCKED: these need real update evidence, nothing was written")
        for item in blockers:
            print(f"  {item}")
        return 2
    if not drifted and not changed:
        print("up to date: no hash-only drift")
        return 0
    print(f"{len(drifted)} rows and {len(changed)} include inputs to re-bind")
    for name in drifted:
        print(f"  row {name}")
    for item in changed:
        print(f"  include {item}")
    if not args.write:
        print("dry run: pass --write with --source-revision to apply")
        return 0
    if not args.source_revision or not REVISION.fullmatch(args.source_revision):
        print("--write needs --source-revision with a 40-hex commit", file=sys.stderr)
        return 2
    stamp = args.refreshed_at or datetime.now(UTC).isoformat()
    result = apply(
        root, ledger, drifted, changed, inventory, args.source_revision, stamp
    )
    path.write_text(_dump(result), encoding="utf-8")
    print(f"re-bound {len(drifted)} rows")
    return 0


if __name__ == "__main__":
    sys.exit(main())
