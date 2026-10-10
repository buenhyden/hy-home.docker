"""Check submitted stable-version evidence; never queries vendors or deploys images."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from urllib.parse import urlsplit

NAME = re.compile(r"[a-zA-Z0-9_.-]+")


def _https(value):
    try:
        parsed = urlsplit(value) if isinstance(value, str) else None
        return bool(
            parsed
            and parsed.scheme == "https"
            and parsed.hostname
            and not parsed.username
            and not parsed.password
        )
    except ValueError:
        return False


def _fresh(value, now, window):
    try:
        timestamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return (
            timestamp.tzinfo is not None and timedelta(0) <= now - timestamp <= window
        )
    except (TypeError, AttributeError, ValueError):
        return False


def _version(value):
    if not isinstance(value, str) or not value or value != value.strip():
        return False
    if value.lower() in {
        "latest",
        "stable",
        "edge",
        "main",
        "master",
        "unknown",
        "not_run",
        "none",
    }:
        return False
    return not re.search(
        r"(?:^|[-_.])(?:alpha|beta|rc|test|nightly|snapshot)(?:[0-9_.-]|$)",
        value,
        re.IGNORECASE,
    )


def _names(values):
    if not isinstance(values, list) or not values:
        raise ValueError("invalid_expected_services")
    if any(not isinstance(item, str) or not NAME.fullmatch(item) for item in values):
        raise ValueError("invalid_expected_services")
    if len(set(values)) != len(values):
        raise ValueError("duplicate_expected")
    return set(values)


def evaluate(rows, expected_services, now=None):
    """Compare evidence with an independently collected, nonempty expected set."""
    now = now or datetime.now(UTC)
    expected = _names(expected_services)
    if (
        not isinstance(rows, list)
        or not isinstance(now, datetime)
        or now.tzinfo is None
    ):
        raise ValueError("invalid_input")
    seen = set()
    entries = []
    for row in rows:
        if not isinstance(row, dict) or row.get("scope") != "root":
            raise ValueError("invalid_scope")
        name = row.get("service")
        if not isinstance(name, str) or not NAME.fullmatch(name) or name in seen:
            raise ValueError("invalid_or_duplicate_service")
        seen.add(name)
        missing = []
        target, latest = row.get("target_version"), row.get("latest_version")
        if not _version(target) or not _version(latest):
            missing.append("latest_unresolved")
        elif target != latest:
            missing.append("latest_mismatch")
        if row.get("channel") != "stable":
            missing.append("stable_channel")
        if not _fresh(row.get("checked_at"), now, timedelta(hours=24)):
            missing.append("fresh_lookup")
        if not _https(row.get("release_url")):
            missing.append("primary_release_reference")
        entries.append(
            {
                "service": name,
                "missing": missing,
                "matches_declared_latest": not missing,
            }
        )
    absent, unexpected = sorted(expected - seen), sorted(seen - expected)
    return {
        "ready": not absent
        and not unexpected
        and all(not r["missing"] for r in entries),
        "missing_services": absent,
        "unexpected_services": unexpected,
        "entries": entries,
        "deployed": False,
        "verified_external_facts": False,
        "meaning": "Submitted ledger completeness only; vendor facts, scans and deployment require separate verification.",
    }


def expected_from_root(root):
    """Read public source closure using the existing inventory authority parser.

    No Compose interpolation, environment rendering or Docker invocation occurs.
    The independently read inputs are hashed; submitted ledger sets are ignored.
    """
    from scripts.lib.document_governance.operations_catalog import (
        _compose_mapping,
        _include_paths,
        _read_text,
    )

    root = Path(root).resolve()
    pending, visited, names, inputs = [Path("docker-compose.yml")], set(), [], []
    while pending:
        path = pending.pop()
        if path in visited:
            continue
        if len(visited) >= 1000:
            raise ValueError("include_limit")
        if (
            path.is_absolute()
            or ".." in path.parts
            or (
                path != Path("docker-compose.yml")
                and (not path.parts or path.parts[0] != "infra")
            )
        ):
            raise ValueError("invalid_include_scope")
        visited.add(path)
        document = _compose_mapping(root, path)
        text = _read_text(root, path)
        inputs.append(
            {
                "path": path.as_posix(),
                "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            }
        )
        services = document.get("services", {})
        if not isinstance(services, dict):
            raise ValueError("invalid_services")
        names.extend(services)
        pending.extend(
            Path(path.parent / child)
            for child in _include_paths(document.get("include"))
        )
    _names(names)
    inputs.sort(key=lambda item: item["path"])
    manifest = hashlib.sha256(json.dumps(inputs, sort_keys=True).encode()).hexdigest()
    return sorted(names), {
        "input_files": inputs,
        "input_manifest_sha256": manifest,
        "meaning": "Public root Compose source set only; runtime set and active profiles require independent observation.",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument(
        "--repo-root", type=Path, default=Path(__file__).resolve().parents[3]
    )
    args = parser.parse_args(argv)
    try:
        document = json.loads(args.input.read_text(encoding="utf-8"))
        expected, inventory = expected_from_root(args.repo_root)
        result = {
            **evaluate(document["entries"], expected),
            "expected_source": inventory,
        }
    except (ValueError, TypeError, OSError, KeyError, AttributeError):
        print("Invalid update ledger; input contents are not printed.", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 0 if result["ready"] else 2


if __name__ == "__main__":
    sys.exit(main())
