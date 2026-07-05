#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(git rev-parse --show-toplevel)"
cd "$BASE_DIR"

OUTPUT="docs/90.references/data/docker/tech-stack-version-provenance.md"

usage() {
  cat <<'EOF'
Usage: bash scripts/operations/generate-tech-stack-version-provenance.sh [--check|--dry-run]

Generate the tech-stack version drift severity and source provenance snapshot.

Options:
  --check    Fail when the generated snapshot is stale.
  --dry-run  Print the generated snapshot to stdout without writing it.
  -h, --help Show this help.
EOF
}

mode="write"
case "${1:-}" in
  "")
    ;;
  --check)
    mode="check"
    ;;
  --dry-run)
    mode="dry-run"
    ;;
  -h|--help)
    usage
    exit 0
    ;;
  *)
    usage >&2
    exit 2
    ;;
esac

python3 - "$mode" "$OUTPUT" <<'PY'
from __future__ import annotations

import collections
import json
import pathlib
import re
import sys
from dataclasses import dataclass

MODE = sys.argv[1]
OUTPUT = pathlib.Path(sys.argv[2])
REGISTRY_PATH = pathlib.Path("infra/tech-stack.versions.json")
EXCEPTIONS_PATH = pathlib.Path("infra/image-tag-policy.exceptions.json")


@dataclass(frozen=True)
class ImageRecord:
    path: pathlib.Path
    line_no: int
    raw: str
    default: str | None


def load_json(path: pathlib.Path) -> dict:
    if not path.is_file():
        raise SystemExit(f"FAIL: missing required JSON file: {path}")
    try:
        data = json.loads(path.read_text())
    except Exception as exc:  # noqa: BLE001
        raise SystemExit(f"FAIL: invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"FAIL: {path} must contain a JSON object")
    return data


registry = load_json(REGISTRY_PATH)
exceptions_data = load_json(EXCEPTIONS_PATH)

entries = registry.get("entries")
if not isinstance(entries, list) or not entries:
    raise SystemExit(f"FAIL: {REGISTRY_PATH} must define a non-empty entries list")

exception_items = exceptions_data.get("floating_image_exceptions", [])
if not isinstance(exception_items, list):
    raise SystemExit(f"FAIL: {EXCEPTIONS_PATH} must define floating_image_exceptions as a list")

exceptions: dict[str, dict[str, str]] = {}
for item in exception_items:
    if not isinstance(item, dict) or not item.get("image"):
        continue
    exceptions[str(item["image"])] = {
        "owner": str(item.get("owner", "")),
        "reason": str(item.get("reason", "")),
        "review_cadence": str(item.get("review_cadence", "")),
    }

image_line_re = re.compile(r"^\s*image:\s*['\"]?([^'\"\s#]+)")
default_image_re = re.compile(r"\$\{[^}:]+:-([^}]+)\}")
floating_suffixes = (":main", ":latest", ":stable", ":edge", ":nightly", ":dev", ":sts", ":alpine")


def markdown_escape(value: object) -> str:
    text = str(value)
    return text.replace("|", "\\|").replace("\n", " ")


def split_repo_tag(image: str) -> tuple[str, str]:
    last_segment = image.rsplit("/", 1)[-1]
    if ":" not in last_segment:
        return image, ""
    repo, tag = image.rsplit(":", 1)
    return repo, tag


def is_floating(image: str) -> bool:
    _repo, tag = split_repo_tag(image)
    if not tag:
        return True
    return image.endswith(floating_suffixes) or "latest" in tag


def parse_image_records(path: pathlib.Path) -> list[ImageRecord]:
    records: list[ImageRecord] = []
    for line_no, line in enumerate(path.read_text(errors="ignore").splitlines(), start=1):
        match = image_line_re.match(line)
        if not match:
            continue
        raw = match.group(1)
        default_match = default_image_re.search(raw)
        records.append(
            ImageRecord(
                path=path,
                line_no=line_no,
                raw=raw,
                default=default_match.group(1) if default_match else None,
            )
        )
    return records


def record_values(record: ImageRecord) -> set[str]:
    values = {record.raw}
    if record.default:
        values.add(record.default)
    return values


def source_text(records: list[ImageRecord], image: str) -> str:
    if not records:
        return "Not declared in listed Compose files"
    parts: list[str] = []
    for record in sorted(records, key=lambda item: (str(item.path), item.line_no)):
        if record.raw == image:
            mode = "direct"
        elif record.default == image:
            mode = "env-default"
        else:
            mode = "declared"
        parts.append(f"`{record.path}:{record.line_no}` ({mode})")
    return "<br>".join(parts)


def severity_for(image: str, records: list[ImageRecord], missing_files: list[str]) -> tuple[str, str]:
    if missing_files:
        return "critical", "missing-compose-file"
    if not records:
        return "high", "registry-image-not-declared"
    if is_floating(image):
        if image in exceptions:
            return "advisory", "floating-exception"
        return "high", "floating-without-exception"
    return "none", "declared-pinned"


component_rows: list[dict[str, object]] = []
image_rows: list[dict[str, object]] = []
missing_file_refs: list[str] = []

for index, entry in enumerate(entries, start=1):
    if not isinstance(entry, dict):
        raise SystemExit(f"FAIL: {REGISTRY_PATH}: entry #{index} must be an object")
    component = str(entry.get("component", f"entry-{index}"))
    tier = str(entry.get("tier", "unspecified"))
    images = entry.get("images")
    compose_files = entry.get("compose_files")
    if not isinstance(images, list) or not images or not isinstance(compose_files, list) or not compose_files:
        raise SystemExit(
            f"FAIL: {REGISTRY_PATH}: {component} must include non-empty images and compose_files lists"
        )

    records_by_value: dict[str, list[ImageRecord]] = collections.defaultdict(list)
    missing_files: list[str] = []
    compose_record_count = 0
    for compose_file in compose_files:
        compose_path = pathlib.Path(str(compose_file))
        if not compose_path.is_file():
            missing_files.append(str(compose_path))
            missing_file_refs.append(f"{component}: {compose_path}")
            continue
        records = parse_image_records(compose_path)
        compose_record_count += len(records)
        for record in records:
            for value in record_values(record):
                records_by_value[value].append(record)

    severities: list[str] = []
    statuses: list[str] = []
    declared_count = 0
    for image in [str(item) for item in images]:
        records = records_by_value.get(image, [])
        if records:
            declared_count += 1
        severity, status = severity_for(image, records, missing_files)
        severities.append(severity)
        statuses.append(status)
        exception = exceptions.get(image)
        image_rows.append(
            {
                "component": component,
                "tier": tier,
                "image": image,
                "status": status,
                "severity": severity,
                "sources": source_text(records, image),
                "exception_owner": exception["owner"] if exception else "",
                "exception_cadence": exception["review_cadence"] if exception else "",
            }
        )

    severity_rank = {"none": 0, "advisory": 1, "high": 2, "critical": 3}
    max_severity = max(severities, key=lambda item: severity_rank[item])
    component_rows.append(
        {
            "component": component,
            "tier": tier,
            "registry_images": len(images),
            "declared_images": declared_count,
            "compose_files": len(compose_files),
            "compose_image_lines": compose_record_count,
            "max_severity": max_severity,
            "statuses": ", ".join(sorted(set(statuses))),
        }
    )

severity_counts = collections.Counter(str(row["severity"]) for row in image_rows)
status_counts = collections.Counter(str(row["status"]) for row in image_rows)
tier_counts = collections.Counter(str(row["tier"]) for row in image_rows)
floating_rows = [row for row in image_rows if row["status"] in {"floating-exception", "floating-without-exception"}]

lines: list[str] = [
    "---",
    "status: active",
    "generated_by: scripts/operations/generate-tech-stack-version-provenance.sh",
    "---",
    "",
    "<!-- Target: docs/90.references/data/docker/tech-stack-version-provenance.md -->",
    "",
    "# Reference: Tech-Stack Version Provenance",
    "",
    "## Overview",
    "",
    "This generated reference summarizes drift severity and source provenance for",
    "`infra/tech-stack.versions.json`. It maps each curated registry image to the",
    "tracked Docker Compose image declaration that currently proves it.",
    "",
    "## Purpose",
    "",
    "The snapshot lets reviewers see whether important runtime images are declared",
    "as pinned, exception-approved floating, missing, or blocked by source drift",
    "without re-reading every Compose file by hand.",
    "",
    "## Repository Role",
    "",
    "Use this document as generated audit context only. Runtime truth remains in",
    "`infra/**/docker-compose*.yml`, `infra/tech-stack.versions.json`, and",
    "`infra/image-tag-policy.exceptions.json`. Do not edit this file by hand;",
    "regenerate it with `bash scripts/operations/generate-tech-stack-version-provenance.sh`.",
    "",
    "## Scope",
    "",
    "### In Scope",
    "",
    "- Curated entries from `infra/tech-stack.versions.json`.",
    "- Listed Compose files for each curated entry.",
    "- Direct image declarations and `${VAR:-image:tag}` default declarations.",
    "- Floating-image exception metadata from `infra/image-tag-policy.exceptions.json`.",
    "",
    "### Out of Scope",
    "",
    "- Live container state, registry network lookups, vulnerability scanning, or SBOM generation.",
    "- Docker Compose interpolation from local `.env` files.",
    "- Deployment, rollback, or image-upgrade procedures.",
    "- Secret values, credentials, container logs, shell history, or runtime inspection output.",
    "",
    "## Definitions / Facts",
    "",
    "- **none**: registry image is declared in a listed Compose file and is pinned.",
    "- **advisory**: registry image is declared, but its tag is floating and covered by an approved exception.",
    "- **high**: registry image is missing from listed Compose files or uses an unapproved floating tag.",
    "- **critical**: registry entry points to a missing Compose file.",
    "- **env-default**: image is the default inside a Compose expression such as `${VAR:-image:tag}`.",
    "",
    "## Snapshot Summary",
    "",
    "| Metric | Value |",
    "| --- | ---: |",
    f"| Registry policy | `{markdown_escape(registry.get('policy_id', 'unknown'))}` |",
    f"| Registry effective date | `{markdown_escape(registry.get('effective_date', 'unknown'))}` |",
    f"| Registry review cadence | `{markdown_escape(registry.get('review_cadence', 'unknown'))}` |",
    f"| Registry source of truth | `{markdown_escape(registry.get('source_of_truth', 'unknown'))}` |",
    f"| Components | {len(component_rows)} |",
    f"| Registry images | {len(image_rows)} |",
    f"| Floating exception images in registry | {len(floating_rows)} |",
    f"| Missing compose file references | {len(missing_file_refs)} |",
    "",
    "## Severity Coverage",
    "",
    "| Severity | Image Count |",
    "| --- | ---: |",
]

for severity in ["none", "advisory", "high", "critical"]:
    lines.append(f"| `{severity}` | {severity_counts.get(severity, 0)} |")

lines.extend(
    [
        "",
        "## Status Coverage",
        "",
        "| Status | Image Count |",
        "| --- | ---: |",
    ]
)
for status, count in sorted(status_counts.items()):
    lines.append(f"| `{status}` | {count} |")

lines.extend(
    [
        "",
        "## Tier Coverage",
        "",
        "| Tier | Registry Image Count |",
        "| --- | ---: |",
    ]
)
for tier, count in sorted(tier_counts.items()):
    lines.append(f"| `{markdown_escape(tier)}` | {count} |")

lines.extend(
    [
        "",
        "## Component Summary",
        "",
        "| Component | Tier | Registry Images | Declared Images | Compose Files | Compose Image Lines | Max Severity | Statuses |",
        "| --- | --- | ---: | ---: | ---: | ---: | --- | --- |",
    ]
)
for row in sorted(component_rows, key=lambda item: (str(item["tier"]), str(item["component"]))):
    lines.append(
        "| {component} | `{tier}` | {registry_images} | {declared_images} | {compose_files} | {compose_image_lines} | `{max_severity}` | {statuses} |".format(
            component=markdown_escape(row["component"]),
            tier=markdown_escape(row["tier"]),
            registry_images=row["registry_images"],
            declared_images=row["declared_images"],
            compose_files=row["compose_files"],
            compose_image_lines=row["compose_image_lines"],
            max_severity=markdown_escape(row["max_severity"]),
            statuses=markdown_escape(row["statuses"]),
        )
    )

lines.extend(
    [
        "",
        "## Image Provenance",
        "",
        "| Component | Image | Status | Severity | Source Provenance | Exception |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
)
for row in sorted(image_rows, key=lambda item: (str(item["tier"]), str(item["component"]), str(item["image"]))):
    exception_text = "N/A"
    if row["exception_owner"]:
        exception_text = f"{row['exception_owner']} / {row['exception_cadence']}"
    lines.append(
        "| {component} | `{image}` | `{status}` | `{severity}` | {sources} | {exception} |".format(
            component=markdown_escape(row["component"]),
            image=markdown_escape(row["image"]),
            status=markdown_escape(row["status"]),
            severity=markdown_escape(row["severity"]),
            sources=markdown_escape(row["sources"]),
            exception=markdown_escape(exception_text),
        )
    )

lines.extend(
    [
        "",
        "## Floating Exception Detail",
        "",
        "| Image | Owner | Review Cadence | Reason |",
        "| --- | --- | --- | --- |",
    ]
)
if floating_rows:
    for row in sorted(floating_rows, key=lambda item: str(item["image"])):
        image = str(row["image"])
        exception = exceptions.get(image, {})
        lines.append(
            f"| `{markdown_escape(image)}` | {markdown_escape(exception.get('owner', 'N/A'))} | {markdown_escape(exception.get('review_cadence', 'N/A'))} | {markdown_escape(exception.get('reason', 'N/A'))} |"
        )
else:
    lines.append("| N/A | N/A | N/A | No floating registry images are present. |")

lines.extend(
    [
        "",
        "## Source Rules",
        "",
        "- Regenerate this file after changing `infra/tech-stack.versions.json`,",
        "  `infra/image-tag-policy.exceptions.json`, or listed Compose image lines.",
        "- Treat `none` severity as current declaration parity, not a security or",
        "  vulnerability statement.",
        "- Treat `advisory` severity as an accepted review obligation, not an error.",
        "- Use `scripts/operations/sync-tech-stack-versions.sh --check` for registry",
        "  tag drift and this generator for human-readable provenance.",
        "- Do not include `.env` values, secret files, live container state, or registry",
        "  network lookup output.",
        "",
        "## Sources",
        "",
        "- [tech-stack registry](../../../../infra/tech-stack.versions.json) - curated image registry and listed Compose sources.",
        "- [floating image exceptions](../../../../infra/image-tag-policy.exceptions.json) - approved floating-tag review obligations.",
        "- [sync script](../../../../scripts/operations/sync-tech-stack-versions.sh) - registry-to-Compose drift synchronization rules.",
        "- [repo contract checker](../../../../scripts/validation/check-repo-contracts.sh) - freshness and drift validation boundary.",
        "",
        "## Maintenance",
        "",
        "- **Owner**: Infra/DevOps Engineer / Documentation Specialist.",
        "- **Review Cadence**: Review after curated registry, Compose image, or floating exception changes.",
        "- **Update Trigger**: Run the generator after tracked registry or listed Compose image changes.",
        "",
        "## Related Documents",
        "",
        "- **Docker data index**: [README.md](./README.md)",
        "- **Docker image/version interpretation**: [image-version-interpretation.md](./image-version-interpretation.md)",
        "- **Compose profile coverage**: [compose-profile-service-coverage.md](./compose-profile-service-coverage.md)",
        "- **Automation candidates**: [../../audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md](../../audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md)",
    ]
)

content = "\n".join(lines) + "\n"

if MODE == "dry-run":
    print(content, end="")
elif MODE == "check":
    if not OUTPUT.is_file():
        print(f"FAIL: missing generated tech-stack provenance snapshot: {OUTPUT}", file=sys.stderr)
        sys.exit(1)
    current = OUTPUT.read_text(errors="ignore")
    if current != content:
        print(f"FAIL: stale generated tech-stack provenance snapshot: {OUTPUT}", file=sys.stderr)
        print("Run: bash scripts/operations/generate-tech-stack-version-provenance.sh", file=sys.stderr)
        sys.exit(1)
    print(f"PASS: generated tech-stack provenance snapshot is fresh: {OUTPUT}")
elif MODE == "write":
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(content)
    print(
        f"Generated {OUTPUT} with {len(image_rows)} images; severity_counts="
        + ",".join(f"{key}:{severity_counts.get(key, 0)}" for key in ["none", "advisory", "high", "critical"])
    )
else:
    print(f"FAIL: unsupported mode: {MODE}", file=sys.stderr)
    sys.exit(2)
PY
