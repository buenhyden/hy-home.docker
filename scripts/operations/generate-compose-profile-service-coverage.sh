#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(git rev-parse --show-toplevel)"
cd "$BASE_DIR"

OUTPUT="docs/90.references/data/docker/compose-profile-service-coverage.md"

usage() {
  cat <<'EOF'
Usage: bash scripts/operations/generate-compose-profile-service-coverage.sh [--check|--dry-run]

Generate the Docker Compose profile-to-service coverage snapshot.

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
import pathlib
import subprocess
import sys

try:
    import yaml
except Exception as exc:
    print(f"FAIL: PyYAML is required for Compose profile coverage generation: {exc}", file=sys.stderr)
    sys.exit(1)

MODE = sys.argv[1]
OUTPUT = pathlib.Path(sys.argv[2])


def git_ls_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def compose_candidates() -> list[pathlib.Path]:
    candidates: list[pathlib.Path] = []
    for raw_path in git_ls_files():
        path = pathlib.Path(raw_path)
        if raw_path == "docker-compose.yml" or (
            raw_path.startswith("infra/")
            and path.name.startswith("docker-compose")
            and path.suffix in {".yml", ".yaml"}
        ):
            candidates.append(path)
    return sorted(candidates)


def read_compose(path: pathlib.Path) -> dict:
    try:
        data = yaml.safe_load(path.read_text(errors="ignore")) or {}
    except Exception as exc:
        raise SystemExit(f"FAIL: {path}: YAML parse failed: {exc}") from exc
    return data if isinstance(data, dict) else {}


def normalize_profiles(value: object) -> list[str]:
    if value is None:
        return ["default"]
    if isinstance(value, str):
        return [value or "default"]
    if isinstance(value, list):
        profiles = [str(item) for item in value if str(item)]
        return profiles or ["default"]
    return ["default"]


def stage_for(path: pathlib.Path) -> str:
    if path.parts and path.parts[0] == "infra" and len(path.parts) > 1:
        return path.parts[1]
    return "root"


compose_files = compose_candidates()
services: list[dict[str, object]] = []
files_with_services: set[str] = set()

for path in compose_files:
    data = read_compose(path)
    raw_services = data.get("services", {})
    if not isinstance(raw_services, dict):
        continue
    for service_name, service_def in sorted(raw_services.items()):
        definition = service_def if isinstance(service_def, dict) else {}
        profiles = normalize_profiles(definition.get("profiles"))
        services.append(
            {
                "service": str(service_name),
                "path": str(path),
                "stage": stage_for(path),
                "profiles": sorted(set(profiles)),
            }
        )
        files_with_services.add(str(path))

profile_services: dict[str, list[dict[str, object]]] = collections.defaultdict(list)
stage_services: dict[str, list[dict[str, object]]] = collections.defaultdict(list)
file_services: dict[str, list[dict[str, object]]] = collections.defaultdict(list)

for item in services:
    for profile in item["profiles"]:  # type: ignore[index]
        profile_services[str(profile)].append(item)
    stage_services[str(item["stage"])].append(item)
    file_services[str(item["path"])].append(item)

profile_names = sorted(profile_services)
default_services = profile_services.get("default", [])
profile_only_services = [item for item in services if "default" not in item["profiles"]]


def service_ref(item: dict[str, object]) -> str:
    return f"`{item['service']}` ({item['path']})"


def compact_refs(items: list[dict[str, object]], limit: int = 18) -> str:
    refs = [service_ref(item) for item in sorted(items, key=lambda x: (str(x["path"]), str(x["service"])))]
    if len(refs) <= limit:
        return ", ".join(refs)
    shown = ", ".join(refs[:limit])
    return f"{shown}, ... +{len(refs) - limit} more"


lines: list[str] = [
    "---",
    "status: active",
    "---",
    "",
    "<!-- Target: docs/90.references/data/docker/compose-profile-service-coverage.md -->",
    "",
    "# Reference: Docker Compose Profile Service Coverage",
    "",
    "## Overview",
    "",
    "This generated reference maps tracked Docker Compose services to declared",
    "Compose profiles and infrastructure stages. It is a static repository",
    "snapshot; runtime truth remains in `infra/**/docker-compose*.yml` and the",
    "root Compose entrypoint.",
    "",
    "## Purpose",
    "",
    "This reference supports audit reports and documentation reviews that need a",
    "quick view of which services are included by default and which services are",
    "gated behind Compose profiles.",
    "",
    "## Repository Role",
    "",
    "Use this document as derived inventory context only. Do not edit it by hand;",
    "regenerate it with `bash scripts/operations/generate-compose-profile-service-coverage.sh`.",
    "It does not replace Compose files, operations runbooks, or runtime validation.",
    "",
    "## Scope",
    "",
    "### In Scope",
    "",
    "- Tracked root and `infra/**/docker-compose*.yml` / `.yaml` files.",
    "- Compose service names, declared `profiles`, source file paths, and top-level",
    "  infrastructure stage folders.",
    "- Services without a `profiles` key, represented as `default`.",
    "",
    "### Out of Scope",
    "",
    "- Running `docker compose config` or resolving profile-specific includes.",
    "- Runtime service health, container state, secrets, or environment values.",
    "- Deployment guidance or rollback procedures.",
    "",
    "## Definitions / Facts",
    "",
    "- **default**: service has no Compose `profiles` key and is active whenever its",
    "  Compose file is included.",
    "- **profile-gated service**: service declares one or more Compose profiles.",
    "- **stage**: first directory under `infra/`, such as `04-data` or `09-tooling`.",
    "- **snapshot**: deterministic parse of tracked Compose files, not live runtime",
    "  evidence.",
    "",
    "## Snapshot Summary",
    "",
    "| Metric | Value |",
    "| --- | ---: |",
    f"| Compose files scanned | {len(compose_files)} |",
    f"| Compose files with services | {len(files_with_services)} |",
    f"| Services discovered | {len(services)} |",
    f"| Distinct profiles including `default` | {len(profile_names)} |",
    f"| Default services | {len(default_services)} |",
    f"| Profile-gated service entries | {len(profile_only_services)} |",
    "",
    "## Profile Coverage",
    "",
    "| Profile | Service Count | Services |",
    "| --- | ---: | --- |",
]

for profile in profile_names:
    items = profile_services[profile]
    lines.append(f"| `{profile}` | {len(items)} | {compact_refs(items)} |")

lines.extend(
    [
        "",
        "## Stage Coverage",
        "",
        "| Stage | Service Count | Profiles Seen |",
        "| --- | ---: | --- |",
    ]
)
for stage, items in sorted(stage_services.items()):
    profiles = sorted({profile for item in items for profile in item["profiles"]})  # type: ignore[index]
    profile_text = ", ".join(f"`{profile}`" for profile in profiles)
    lines.append(f"| `{stage}` | {len(items)} | {profile_text} |")

lines.extend(
    [
        "",
        "## Compose File Coverage",
        "",
        "| Compose File | Service Count | Profiles Seen |",
        "| --- | ---: | --- |",
    ]
)
for path, items in sorted(file_services.items()):
    profiles = sorted({profile for item in items for profile in item["profiles"]})  # type: ignore[index]
    profile_text = ", ".join(f"`{profile}`" for profile in profiles)
    lines.append(f"| `{path}` | {len(items)} | {profile_text} |")

lines.extend(
    [
        "",
        "## Source Rules",
        "",
        "- Regenerate this file after adding, removing, or changing tracked Compose",
        "  services or profiles.",
        "- Treat this reference as advisory inventory; use Compose files for current",
        "  implementation truth.",
        "- Do not include secret values, `.env` values, container logs, or runtime",
        "  inspection output.",
        "",
        "## Sources",
        "",
        "- [root Compose entrypoint](../../../../docker-compose.yml) - root Compose",
        "  include boundary when tracked.",
        "- [infra directory](../../../../infra/) - tracked service-local Compose files.",
        "- [coverage generator](../../../../scripts/operations/generate-compose-profile-service-coverage.sh) - deterministic snapshot generator.",
        "",
        "## Maintenance",
        "",
        "- **Owner**: Infra/DevOps Engineer / Documentation Specialist.",
        "- **Review Cadence**: Review after Compose service/profile changes.",
        "- **Update Trigger**: Run the generator after tracked Compose files change.",
        "",
        "## Related Documents",
        "",
        "- **Docker data index**: [README.md](./README.md)",
        "- **Docker image/version interpretation**: [image-version-interpretation.md](./image-version-interpretation.md)",
        "- **Automation candidates**: [../../audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md](../../audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md)",
        "- **Compose validation script**: [../../../../scripts/validation/validate-docker-compose.sh](../../../../scripts/validation/validate-docker-compose.sh)",
    ]
)

content = "\n".join(lines) + "\n"

if MODE == "dry-run":
    print(content, end="")
elif MODE == "check":
    if not OUTPUT.is_file():
        print(f"FAIL: missing generated Compose coverage snapshot: {OUTPUT}", file=sys.stderr)
        sys.exit(1)
    current = OUTPUT.read_text(errors="ignore")
    if current != content:
        print(f"FAIL: stale generated Compose coverage snapshot: {OUTPUT}", file=sys.stderr)
        print("Run: bash scripts/operations/generate-compose-profile-service-coverage.sh", file=sys.stderr)
        sys.exit(1)
    print(f"PASS: generated Compose coverage snapshot is fresh: {OUTPUT}")
elif MODE == "write":
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(content)
    print(f"Generated {OUTPUT} with {len(services)} services across {len(profile_names)} profiles")
else:
    print(f"FAIL: unsupported mode: {MODE}", file=sys.stderr)
    sys.exit(2)
PY
