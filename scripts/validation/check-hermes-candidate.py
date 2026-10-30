#!/usr/bin/env python3
"""Read-only, offline Hermes v1 candidate preflight; never approves publication.

Exit 0: structurally valid non-private candidate (not approval).
Exit 1: invalid candidate or unavailable/mismatched staged bytes.
Exit 2: structurally valid private infra candidate, blocked from publication.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
from datetime import datetime
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit

KINDS = {
    "6eabd835f969": "strategy-news",
    "25674fbc0bf3": "devops-brief",
    "8d0925bc571d": "solo-dev-ideas",
    "3c3f81a925e0": "infra-github-report",
}
HEX32 = re.compile(r"[0-9a-f]{32}\Z")
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
CRON_FILE = re.compile(r"\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}\.md\Z")
UNVERIFIED = re.compile(r"\[(?:출처 확인 불가|Link Unavailable)\]", re.I)
COMMON = {
    "title",
    "summary",
    "region_or_scope",
    "category",
    "source_url",
    "collection_evidence",
    "verification_status",
}
DEVOPS = {"product", "version", "release_date", "impact_scope"}
IDEA = {
    "customer_segment",
    "problem",
    "differentiation",
    "pricing",
    "revenue_model",
    "mvp_duration",
    "competitors",
    "alternatives",
    "uncertainty",
    "market_size_claim",
    "source_ref",
    "source_sha256",
}
TOP = {
    "schema_version",
    "producer",
    "job_id",
    "run_id",
    "report_kind",
    "generated_at",
    "source_ref",
    "source_sha256",
    "items",
    "state",
    "export_status",
    "privacy_classification",
    "warnings",
}
STATE = {"run_completed", "source_file_ready", "email_delivery", "blog_data_ingested"}


class InvalidCandidate(ValueError):
    """A candidate assertion or staged source failed preflight."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise InvalidCandidate(message)


def exact_keys(value: object, keys: set[str], location: str) -> dict:
    if not isinstance(value, dict):
        raise InvalidCandidate(f"{location}: expected object")
    require(set(value) == keys, f"{location}: missing or unexpected fields")
    return value


def digest(value: object, location: str) -> None:
    require(
        isinstance(value, str) and HEX64.fullmatch(value) is not None,
        f"{location}: expected lowercase SHA-256 hex",
    )


def reference(value: object, location: str) -> PurePosixPath:
    if not isinstance(value, str):
        raise InvalidCandidate(f"{location}: invalid relative source reference")
    require(
        bool(value) and "\\" not in value,
        f"{location}: invalid relative source reference",
    )
    path = PurePosixPath(value)
    require(
        not path.is_absolute()
        and all(part not in (".", "..") for part in value.split("/"))
        and all(path.parts)
        and path.as_posix() == value,
        f"{location}: noncanonical or escaping source reference",
    )
    return path


def staged_digest(root: Path, ref: PurePosixPath, claimed: str) -> None:
    """Read only a regular file within a staged root; hash actual bytes."""
    require(root.is_dir() and not root.is_symlink(), "staged root missing or symlinked")
    target = root.joinpath(*ref.parts)
    base = root.resolve(strict=True)
    # Reject symlinked ancestors as well as leaf files (including dangling links).
    cursor = root
    for part in ref.parts:
        cursor = cursor / part
        require(not cursor.is_symlink(), f"staged source symlink: {ref}")
    require(
        target.is_file() and target.resolve(strict=True).is_relative_to(base),
        f"staged source missing or outside root: {ref}",
    )
    try:
        fd = os.open(target, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
        with os.fdopen(fd, "rb") as stream:
            require(
                stat.S_ISREG(os.fstat(stream.fileno()).st_mode),
                f"staged source is not a regular file: {ref}",
            )
            hasher = hashlib.sha256()
            for block in iter(lambda: stream.read(65536), b""):
                hasher.update(block)
    except OSError as exc:
        raise InvalidCandidate(f"staged source unreadable: {ref}") from exc
    require(hasher.hexdigest() == claimed, f"staged source SHA-256 mismatch: {ref}")


def valid_url(value: object, location: str) -> None:
    if not isinstance(value, str):
        raise InvalidCandidate(f"{location}: invalid URL")
    require(
        value == value.strip() and not any(c.isspace() for c in value),
        f"{location}: invalid URL",
    )
    try:
        url = urlsplit(value)
        require(
            url.scheme in ("http", "https") and bool(url.hostname) and url.port != 0,
            f"{location}: expected HTTP(S) URL with host",
        )
    except ValueError as exc:
        raise InvalidCandidate(f"{location}: invalid URL") from exc


def check_item(item: object, kind: str, index: int, item_root: Path | None) -> None:
    location = f"items[{index}]"
    fields = COMMON | (
        IDEA
        if kind == "solo-dev-ideas"
        else DEVOPS
        if kind == "devops-brief"
        else set()
    )
    data = exact_keys(item, fields, location)
    for field in ("title", "summary", "region_or_scope", "category"):
        require(
            isinstance(data[field], str) and bool(data[field].strip()),
            f"{location}.{field}: expected nonempty text",
        )
    evidence = data["collection_evidence"]
    require(
        evidence is None or isinstance(evidence, str),
        f"{location}.collection_evidence: invalid text",
    )
    url = data["source_url"]
    require(url is None or isinstance(url, str), f"{location}.source_url: invalid type")
    if url is not None:
        valid_url(url, f"{location}.source_url")
        require(
            isinstance(evidence, str) and url in evidence,
            f"{location}: source URL is not in collection evidence",
        )
    if kind == "devops-brief":
        require(
            isinstance(data["product"], str) and bool(data["product"]),
            f"{location}.product: invalid value",
        )
        require(
            isinstance(data["impact_scope"], str) and bool(data["impact_scope"]),
            f"{location}.impact_scope: invalid value",
        )
        for field in ("version", "release_date"):
            require(
                data[field] is None or isinstance(data[field], str),
                f"{location}.{field}: invalid value",
            )
    if kind == "solo-dev-ideas":
        for field in IDEA - {"uncertainty", "source_ref", "source_sha256"}:
            require(
                data[field] is None or isinstance(data[field], str),
                f"{location}.{field}: invalid value",
            )
        uncertainty = data["uncertainty"]
        require(
            isinstance(uncertainty, list)
            and all(isinstance(v, str) for v in uncertainty),
            f"{location}.uncertainty: invalid list",
        )
        ref = reference(data["source_ref"], f"{location}.source_ref")
        require(
            len(ref.parts) >= 6
            and ref.parts[:3] == ("storage", "research", "solo-dev-ideas")
            and ref.parts[4] in ("kr", "global")
            and ref.name.endswith(".md"),
            f"{location}.source_ref: unexpected idea path",
        )
        digest(data["source_sha256"], f"{location}.source_sha256")
        if item_root is not None:
            staged_digest(item_root, ref, data["source_sha256"])
    flagged = bool(UNVERIFIED.search(evidence or ""))
    if kind == "solo-dev-ideas":
        flagged = flagged or any(UNVERIFIED.search(v) for v in data["uncertainty"])
    expected = (
        "source_cited_unverified" if url is not None and not flagged else "unverified"
    )
    require(
        data["verification_status"] == expected,
        f"{location}.verification_status: URL/unverified evidence mismatch",
    )


def validate(
    document: object, source_root: Path | None = None, item_root: Path | None = None
) -> bool:
    """Return True only for a valid but private, blocked infra candidate."""
    data = exact_keys(document, TOP, "candidate")
    require(
        data["schema_version"] == "1.0.0" and data["producer"] == "hermes",
        "unsupported producer/schema version",
    )
    job = data["job_id"]
    require(
        isinstance(job, str) and job in KINDS and data["report_kind"] == KINDS[job],
        "job-id/report-kind mismatch",
    )
    require(
        isinstance(data["run_id"], str) and HEX32.fullmatch(data["run_id"]) is not None,
        "run_id must be lowercase 32-hex",
    )
    try:
        timestamp = datetime.fromisoformat(data["generated_at"])
        require(
            timestamp.tzinfo is not None and timestamp.utcoffset() is not None,
            "generated_at must include timezone offset",
        )
    except (TypeError, ValueError) as exc:
        raise InvalidCandidate("generated_at must be timezone-aware ISO 8601") from exc
    ref = reference(data["source_ref"], "source_ref")
    require(
        len(ref.parts) == 4
        and ref.parts[:3] == ("cron", "output", job)
        and CRON_FILE.fullmatch(ref.name) is not None,
        "unexpected Cron source reference",
    )
    digest(data["source_sha256"], "source_sha256")
    if source_root is not None:
        staged_digest(source_root, ref, data["source_sha256"])
    state = exact_keys(data["state"], STATE, "state")
    require(
        state["run_completed"] is True and state["source_file_ready"] is True,
        "unready execution/source",
    )
    require(
        state["email_delivery"] in ("reported_sent", "reported_failed", "unknown")
        and state["blog_data_ingested"] == "unknown",
        "unearned delivery/ingestion claim",
    )
    require(
        isinstance(data["warnings"], list)
        and all(isinstance(v, str) for v in data["warnings"]),
        "warnings must be strings",
    )
    items = data["items"]
    require(isinstance(items, list), "items must be a list")
    private = data["report_kind"] == "infra-github-report"
    if private:
        require(
            not items
            and data["export_status"] == "blocked_private_source"
            and data["privacy_classification"] == "internal_restricted",
            "private infra must have no items and remain blocked",
        )
    else:
        require(
            bool(items)
            and data["export_status"] == "ready_for_review"
            and data["privacy_classification"] == "unreviewed",
            "candidate must remain unreviewed and have items",
        )
        for index, item in enumerate(items):
            check_item(item, data["report_kind"], index, item_root)
    return private


def unique_object(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", type=Path, help="single local candidate JSON")
    parser.add_argument(
        "--source-root", type=Path, help="staged Hermes home containing cron/output"
    )
    parser.add_argument(
        "--item-root", type=Path, help="staged user home containing storage/research"
    )
    args = parser.parse_args(argv)
    try:
        with args.candidate.open("r", encoding="utf-8") as stream:
            document = json.load(stream, object_pairs_hook=unique_object)
        private = validate(document, args.source_root, args.item_root)
    except (OSError, UnicodeError, ValueError, RecursionError) as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        return 1
    checked = "checked" if args.source_root is not None else "not checked"
    ideas = "checked" if args.item_root is not None else "not checked"
    if private:
        print(
            f"BLOCKED: private infra source; Cron bytes {checked}; idea bytes {ideas}; no publication approval"
        )
        return 2
    print(
        f"VALID: offline preflight only; Cron bytes {checked}; idea bytes {ideas}; no publication approval"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
