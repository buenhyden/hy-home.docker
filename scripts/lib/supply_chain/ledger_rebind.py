"""Re-bind SEC01 ledger Compose file hashes after a hash-only drift.

Dry run by default. A row is re-bound only when its declared image and build
still match Compose; a changed image or build, or any added or removed row,
service or include input, stops the run because those need real update
evidence. Only hashes are written, never review, scan or acceptance fields.
The n8n source binding is rehashed identically in the ledger and
build-inputs.json, and the old binding is appended to its history.

--accept-image-updates is the Renovate post-upgrade mode. It also accepts an
image change when Compose now holds a full name:tag@sha256:<64 hex> reference
of the same repository as the existing row. Such a row is marked unverified:
target digests UNKNOWN, review, scan and acceptance fields NOT_RUN, the
previous values kept in the source_refreshes record. A new or removed service,
a repository change, a reference without a digest and a build change still stop
the run. Nothing here contacts a registry; digests, signatures and provenance
stay unchecked.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

from scripts.lib.supply_chain.latest_version_gate import expected_from_root

LEDGER = "infra/09-platform-ops/security-updates/update-ledger.json"
BUILD_INPUTS = "build-inputs.json"
REVISION = re.compile(r"[0-9a-f]{40}")
PINNED = re.compile(
    r"[a-z0-9][a-z0-9._/:-]*:[A-Za-z0-9_][A-Za-z0-9._-]*@sha256:[0-9a-f]{64}"
)
UNKNOWN_TARGET = (
    "target_index_digest",
    "target_manifest_digest",
    "target_config_digest",
    "target_declared_digest",
    "platform",
    "applicability",
    "upstream_reported_tag",
)
NOT_RUN = (
    "signature",
    "sbom_scan",
    "compatibility",
    "backup",
    "rollback",
    "native_test",
    "deployment",
)
RECEIPTS = (
    "candidate_workflow_receipt",
    "candidate_openbao_receipt",
    "current_candidate_receipt",
)
RENOVATE_NOTE = (
    "Renovate-proposed pin: the digest was not verified against a registry and "
    "no publisher signature, provenance, SBOM, scan, compatibility, native, "
    "deployment or recovery result exists for it"
)


def _dump(document):
    return json.dumps(document, indent=2, ensure_ascii=False) + "\n"


def _repository(ref):
    head, _, last = ref.split("@", 1)[0].rpartition("/")
    return f"{head}/{last.split(':')[0]}" if head else last.split(":")[0]


def _image_refusal(old, new):
    """Why a Compose image is not an acceptable Renovate pin of the row, or None."""
    if not isinstance(new, str) or not PINNED.fullmatch(new):
        return "not a full name:tag@sha256:<64 hex> reference"
    if _repository(old) != _repository(new):
        return "repository differs from the ledger row"
    return None


def rebound_binding(root, binding):
    """Return the n8n source binding rehashed from the files it names."""
    files = [
        {
            **item,
            "sha256": hashlib.sha256((root / item["path"]).read_bytes()).hexdigest(),
        }
        for item in binding["input_files"]
    ]
    aggregate = hashlib.sha256()
    for item in sorted(files, key=lambda item: item["path"]):
        aggregate.update(
            item["path"].encode() + b"\0" + (root / item["path"]).read_bytes()
        )
    return {**binding, "input_files": files, "input_sha256": aggregate.hexdigest()}


def plan_n8n(root, ledger, build):
    """Return (blockers, rehashed binding or None when it is current)."""
    section = ledger.get("n8n_source_preparation")
    if section is None:
        return [], None
    binding = section["source_binding"]
    if build is None or build["n8n_source_preparation"]["source_binding"] != binding:
        return ["n8n source bindings differ between the ledger and build-inputs"], None
    missing = [
        f"n8n source input missing: {item['path']}"
        for item in binding["input_files"]
        if not (root / item["path"]).is_file()
    ]
    if missing:
        return missing, None
    fresh = rebound_binding(root, binding)
    return [], (fresh if fresh != binding else None)


def plan(root, ledger, accept_images=False):
    """Return (drifted rows, changed include paths, blockers, inventory, image updates)."""
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
    drifted, updates = [], {}
    for name, row in sorted(rows.items()):
        if name not in expected:
            continue
        service = _compose_mapping(root, Path(row["compose_file"]))["services"].get(
            name
        )
        if service is None:
            blockers.append(f"service missing from {row['compose_file']}: {name}")
            continue
        image = service.get("image", "UNKNOWN")
        refusal = None
        if image != row["current_declared"]:
            refusal = _image_refusal(row["current_declared"], image)
            if not accept_images or refusal:
                detail = f" ({refusal})" if accept_images else ""
                blockers.append(f"image changed, needs update evidence: {name}{detail}")
                continue
            updates[name] = image
        if service.get("build") != row["build_source"]:
            blockers.append(f"build changed, needs update evidence: {name}")
        elif name in updates or (
            hashlib.sha256((root / row["compose_file"]).read_bytes()).hexdigest()
            != row["source_input_sha256"]
        ):
            drifted.append(name)
    return drifted, changed, blockers, inventory, updates


def _mark_unverified(row, image, stamp):
    """Re-point a row at a Renovate-proposed image; return what it replaced."""
    kept = {
        key: copy.deepcopy(row[key])
        for key in (
            "target_version",
            "target_source_image",
            "target_digest_evidence",
            "candidate_evidence_scope",
            "disposition",
            "blocker",
            "source_refreshed_at",
            *UNKNOWN_TARGET,
            *NOT_RUN,
            *RECEIPTS,
        )
        if key in row
    }
    record = {
        "service": row["service"],
        "current_declared": row["current_declared"],
        "proposed_declared": image,
        "previous_fields": kept,
    }
    for key in RECEIPTS:
        row.pop(key, None)
    tag = image.split("@", 1)[0].rsplit(":", 1)[1]
    version = re.search(r"\d+(?:\.\d+)+", tag)
    version = version.group() if version else "UNKNOWN"
    row.update(dict.fromkeys(UNKNOWN_TARGET, "UNKNOWN"))
    row.update(dict.fromkeys(NOT_RUN, "NOT_RUN"))
    due = datetime.fromisoformat(stamp) + timedelta(days=7)
    row.update(
        current_declared=image,
        target_version=version,
        target_source_image=image,
        target_digest_evidence=f"UNKNOWN: {RENOVATE_NOTE}.",
        candidate_evidence_scope=f"{RENOVATE_NOTE}.",
        disposition="BLOCKED",
        source_refreshed_at=stamp,
        blocker={
            **row.get("blocker", {}),
            "owner": "SEC01",
            "discovered_at": stamp,
            "next_validation_due": due.isoformat(),
            "reason": f"{RENOVATE_NOTE}.",
            "exit_condition": (
                "Verify the registry index, platform and config digests, the "
                "publisher signature and provenance, a scan, compatibility and "
                "recovery for this exact pin, or revert it."
            ),
        },
        current_target_artifact_binding={
            "source_version": version,
            "source_image": image,
            "status": "UNBOUND_CURRENT_TARGET",
            "reason": (
                f"{RENOVATE_NOTE}; do not reuse historical artifact, build or "
                "native results."
            ),
        },
    )
    return record


def apply(
    root,
    ledger,
    drifted,
    changed,
    inventory,
    source_revision,
    refreshed_at,
    updates=None,
    binding=None,
):
    """Return a re-bound copy of the ledger with the previous binding kept."""
    updates = updates or {}
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
    images = [
        _mark_unverified(rows[name], image, refreshed_at)
        for name, image in sorted(updates.items())
    ]
    for name in drifted:
        rows[name]["source_input_sha256"] = hashlib.sha256(
            (root / rows[name]["compose_file"]).read_bytes()
        ).hexdigest()
    if drifted or changed:
        refresh = {
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
        if images:
            refresh.update(
                revision_scope="Renovate-proposed image pins and Compose file hash re-binding",
                updated_services=sorted(updates),
                previous_service_images=images,
                meaning=(
                    f"{len(images)} rows now declare a Renovate-proposed image "
                    "(a full name:tag@sha256 reference of the same repository). "
                    "The digest was not verified against a registry and the "
                    "signature and provenance were not verified: their target "
                    "digests are UNKNOWN, review, scan and acceptance fields are "
                    "NOT_RUN and the previous values are kept in "
                    "previous_service_images. Include hashes and the "
                    f"source_input_sha256 of {len(previous)} rows were re-bound. "
                    "No vendor lookup, SBOM, scan, native, deployment or recovery "
                    "acceptance."
                ),
            )
        result["source_refreshes"].append(refresh)
        result["include_inputs"] = inventory["input_files"]
    if binding:
        _rebind_n8n(
            result["n8n_source_preparation"],
            binding,
            source_revision,
            refreshed_at,
            bool(images),
        )
    return result


def _rebind_n8n(section, binding, source_revision, refreshed_at, renovate):
    old = section["source_binding"]
    section["historical_source_bindings"].append({**old, "archived_at": refreshed_at})
    section["source_binding"] = {
        **binding,
        "checked_at": refreshed_at,
        "source_revision": source_revision,
        "source_state": (
            "SOURCE_REVIEW_ONLY: the n8n input files changed on top of this revision "
            + (
                "and were rehashed after a Renovate-proposed update."
                if renovate
                else "and were rehashed."
            )
        ),
        "meaning": (
            "Same existing n8n source paths rehashed; no custom image build, "
            "signature, scan, native or HOME acceptance, and no earlier native "
            "acceptance applies to the changed source."
        ),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root", type=Path, default=Path(__file__).resolve().parents[3]
    )
    parser.add_argument("--ledger", type=Path, help=f"default: <repo-root>/{LEDGER}")
    parser.add_argument("--write", action="store_true", help="apply the plan")
    parser.add_argument(
        "--accept-image-updates",
        action="store_true",
        help="Renovate post-upgrade mode: accept full name:tag@sha256 pins of "
        "existing rows as unverified",
    )
    parser.add_argument("--source-revision", help="40-hex commit; required by --write")
    parser.add_argument("--refreshed-at", help="ISO timestamp; default: now (UTC)")
    args = parser.parse_args(argv)
    root = args.repo_root.resolve()
    path = args.ledger or root / LEDGER
    try:
        stamp = args.refreshed_at or datetime.now(UTC).isoformat()
        datetime.fromisoformat(stamp)
        ledger = _load(path)
        build = (
            _load(path.with_name(BUILD_INPUTS))
            if "n8n_source_preparation" in ledger
            else None
        )
        drifted, changed, blockers, inventory, updates = plan(
            root, ledger, args.accept_image_updates
        )
        n8n_blockers, binding = plan_n8n(root, ledger, build)
        blockers += n8n_blockers
    except (ValueError, TypeError, OSError, KeyError, AttributeError) as error:
        print(f"Invalid update ledger: {type(error).__name__}", file=sys.stderr)
        return 2
    if blockers:
        print("BLOCKED: these need real update evidence, nothing was written")
        for item in blockers:
            print(f"  {item}")
        return 2
    if not (drifted or changed or updates or binding):
        print("up to date: no hash-only drift")
        return 0
    print(f"{len(drifted)} rows and {len(changed)} include inputs to re-bind")
    for name in drifted:
        print(
            f"  row {name}"
            + (" (Renovate-proposed image, unverified)" if name in updates else "")
        )
    for item in changed:
        print(f"  include {item}")
    if binding:
        print("  n8n source binding")
    if not args.write:
        print("dry run: pass --write with --source-revision to apply")
        return 0
    if not args.source_revision or not REVISION.fullmatch(args.source_revision):
        print("--write needs --source-revision with a 40-hex commit", file=sys.stderr)
        return 2
    result = apply(
        root,
        ledger,
        drifted,
        changed,
        inventory,
        args.source_revision,
        stamp,
        updates,
        binding,
    )
    path.write_text(_dump(result), encoding="utf-8")
    if binding:
        section = build["n8n_source_preparation"]
        _rebind_n8n(section, binding, args.source_revision, stamp, bool(updates))
        path.with_name(BUILD_INPUTS).write_text(_dump(build), encoding="utf-8")
    print(f"re-bound {len(drifted)} rows")
    return 0


def _load(path):
    text = path.read_text(encoding="utf-8")
    document = json.loads(text)
    if _dump(document) != text:
        raise ValueError("ledger formatting is not canonical")
    return document


if __name__ == "__main__":
    sys.exit(main())
