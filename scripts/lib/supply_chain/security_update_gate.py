"""Check reviewed security evidence; never scans, proves advisory facts or deploys."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path, PurePosixPath

from scripts.lib.supply_chain.latest_version_gate import (
    NAME,
    _fresh,
    _https,
    _names,
    expected_from_root,
)

DIGEST = re.compile(r"sha256:[0-9a-f]{64}")
VERSION = re.compile(r"(\d+)\.(\d+)\.(\d+)")
IMAGE = re.compile(r"[a-z0-9][a-z0-9._:/-]*(?::[A-Za-z0-9_.-]+)?@sha256:[0-9a-f]{64}")


def _root_service(row, seen):
    if not isinstance(row, dict):
        raise ValueError("invalid_row")
    service, raw_path = row.get("service"), row.get("compose_file")
    if not isinstance(raw_path, str):
        raise ValueError("invalid_root_scope")
    path = PurePosixPath(raw_path)
    if (
        not isinstance(service, str)
        or not NAME.fullmatch(service)
        or row.get("scope") != "root"
        or path.is_absolute()
        or ".." in path.parts
        or "\\" in raw_path
        or not path.parts
        or path.parts[0] != "infra"
        or path.suffix not in {".yml", ".yaml"}
    ):
        raise ValueError("invalid_root_scope")
    if service in seen:
        raise ValueError("duplicate_service")
    return service


def _patch_missing(row, now, window):
    missing = []
    if row.get("affected_confirmed") is not True:
        missing.append("affectedness")
    image = row.get("candidate_image")
    digest = image.rsplit("@", 1)[-1] if isinstance(image, str) else ""
    if (
        not isinstance(image, str)
        or not IMAGE.fullmatch(image)
        or not DIGEST.fullmatch(digest)
    ):
        missing.append("candidate_digest")
    if row.get("scan_digest") != digest or not DIGEST.fullmatch(digest):
        missing.append("matching_scan_digest")
    if not _fresh(row.get("scan_at"), now, window):
        missing.append("fresh_scan")
    missing.extend(
        field for field in ("compatibility", "recovery") if row.get(field) != "pass"
    )
    if row.get("residual_disposition") != "approved":
        missing.append("residual_disposition")
    old, new = (
        VERSION.fullmatch(str(row.get("current_version", ""))),
        VERSION.fullmatch(str(row.get("candidate_version", ""))),
    )
    if not old or not new:
        missing.append("explicit_upstream_version")
    elif tuple(map(int, new.groups())) < tuple(map(int, old.groups())):
        missing.append("downgrade")
    return missing


def assess(rows, now=None, freshness_days=7, expected_services=None):
    now = now or datetime.now(UTC)
    if (
        not isinstance(rows, list)
        or not rows
        or not isinstance(now, datetime)
        or now.tzinfo is None
        or not isinstance(freshness_days, int)
        or isinstance(freshness_days, bool)
        or freshness_days < 1
    ):
        raise ValueError("invalid_input")
    expected = _names(expected_services) if expected_services is not None else None
    window, seen, entries = timedelta(days=freshness_days), set(), []
    for row in rows:
        service = _root_service(row, seen)
        seen.add(service)
        missing = []
        if not _fresh(row.get("reviewed_at"), now, window):
            missing.append("fresh_review")
        urls = row.get("advisory_urls")
        if (
            not isinstance(urls, list)
            or not urls
            or not all(_https(url) for url in urls)
        ):
            missing.append("primary_advisory")
        decision = row.get("decision")
        if decision == "not-affected":
            reason = row.get("reason")
            if (
                row.get("affected_confirmed") is not False
                or not isinstance(reason, str)
                or not reason.strip()
            ):
                missing.append("applicability_reason")
            status = (
                "blocked-evidence"
                if missing
                else "ledger-complete-pending-independent-verification"
            )
        elif decision == "no-fix":
            status = "blocked-no-fix"
        elif decision == "patch":
            missing.extend(_patch_missing(row, now, window))
            status = (
                "blocked-evidence"
                if missing
                else "ledger-complete-pending-independent-verification"
            )
        else:
            missing.append("reviewed_decision")
            status = "blocked-evidence"
        entries.append({"service": service, "status": status, "missing": missing})
    absent = sorted(expected - seen) if expected is not None else []
    unexpected = sorted(seen - expected) if expected is not None else []
    return {
        "ledger_complete": expected is not None
        and not absent
        and not unexpected
        and all(not row["status"].startswith("blocked") for row in entries),
        "coverage_checked": expected is not None,
        "missing_services": absent,
        "unexpected_services": unexpected,
        "schema_version": 1,
        "evaluated_at": now.isoformat(),
        "entries": entries,
        "deployed": False,
        "verified_external_facts": False,
        "meaning": "Submitted reviewed ledger completeness only; no advisory, scan or deployment verification.",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--freshness-days", type=int, default=7)
    parser.add_argument(
        "--repo-root", type=Path, default=Path(__file__).resolve().parents[3]
    )
    args = parser.parse_args(argv)
    try:
        raw = json.loads(args.input.read_text(encoding="utf-8"))
        expected, inventory = expected_from_root(args.repo_root)
        result = {
            **assess(
                raw["entries"],
                freshness_days=args.freshness_days,
                expected_services=expected,
            ),
            "expected_source": inventory,
        }
    except (KeyError, ValueError, OSError, TypeError, AttributeError):
        print(
            "Invalid security ledger; input contents are not printed.", file=sys.stderr
        )
        return 2
    print(json.dumps(result, indent=2))
    return 0 if result["ledger_complete"] else 2


if __name__ == "__main__":
    sys.exit(main())
