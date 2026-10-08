#!/usr/bin/env python3
"""Effective Compose controls for every root and LAB service (SPEC-0218).

Renders the root with every profile and each LAB entrypoint, reads each
service's final controls after extends and merge, and checks them against
infra/common-optimizations.exceptions.json. A deviation passes only through an
exception naming its exact scope, Compose file, service, control and value;
a job's missing healthcheck and a secret-free service's missing secret are
lifecycle facts, not exceptions.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import pathlib
import subprocess
import sys
import tempfile

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
REGISTRY = "infra/common-optimizations.exceptions.json"
# Synthetic, non-HOME inputs: only enough to render each LAB model.
LAB_INPUTS = {
    "LAB_DATA_DIR": "/nonexistent/lab-data",
    "LAB_SECRET_DIR": "/nonexistent/lab-secrets",
    "LAB_KAFKA_CLUSTER_ID": "synthetic-lab-cluster",
    "LAB_LOCUST_SCENARIO_DIR": "/nonexistent/locust-scenario",
    "LAB_LOCUST_RESULT_DIR": "/nonexistent/locust-results",
    "LAB_OPENSEARCH_CERT_DIR": "/nonexistent/opensearch-certs",
}
SECRETS_GID = "1000"
DAEMON_RESTART = {"unless-stopped", "always"}
KINDS = {"weakening", "compatibility"}
FIELDS = (
    "scope", "compose_file", "service", "control", "allowed_value", "kind",
    "owner", "reason", "impact", "mitigation", "verification", "reviewed",
    "review_by", "release_condition",
)  # fmt: skip
MAX_REVIEW_DAYS = 366


def _limits(service: dict) -> dict:
    return ((service.get("deploy") or {}).get("resources") or {}).get("limits") or {}


def is_job(service: dict) -> bool:
    return str(service.get("restart", "")) == "no"


def needs_secret_group(service: dict, secret_roots: tuple[str, ...]) -> bool:
    if service.get("secrets"):
        return True
    for volume in service.get("volumes") or []:
        source = str(volume.get("source", "")) if isinstance(volume, dict) else ""
        if volume.get("type") == "bind" and source.startswith(secret_roots):
            return True
    return False


def deviations(service: dict, secret_roots: tuple[str, ...]) -> dict[str, object]:
    """Return {control: actual value} for every control the service misses."""
    found: dict[str, object] = {}
    security = [str(item) for item in service.get("security_opt") or []]
    if not any("no-new-privileges:true" in item for item in security):
        found["no_new_privileges"] = False
    cap_drop = sorted(str(item) for item in service.get("cap_drop") or [])
    if "ALL" not in cap_drop:
        found["cap_drop_all"] = cap_drop
    if service.get("cap_add"):
        found["cap_add"] = sorted(str(item) for item in service["cap_add"])
    if service.get("privileged"):
        found["privileged"] = True
    if service.get("init") is not True:
        found["init"] = False
    has_group = SECRETS_GID in {str(item) for item in service.get("group_add") or []}
    needs_group = needs_secret_group(service, secret_roots)
    if has_group and not needs_group:
        found["secrets_group"] = "unneeded"
    elif needs_group and not has_group:
        found["secrets_group"] = "missing"
    restart = str(service.get("restart", ""))
    if not is_job(service):
        if restart not in DAEMON_RESTART:
            found["restart"] = restart or None
        check = service.get("healthcheck") or {}
        if not check or check.get("disable"):
            found["healthcheck"] = "absent"
    if not (service.get("cpus") or _limits(service).get("cpus")):
        found["cpus"] = None
    if not (service.get("mem_limit") or _limits(service).get("memory")):
        found["mem_limit"] = None
    if not (service.get("pids_limit") or _limits(service).get("pids")):
        found["pids_limit"] = None
    devices = ((service.get("deploy") or {}).get("resources") or {}).get(
        "reservations", {}
    ).get("devices") or []
    if any("gpu" in (device.get("capabilities") or []) for device in devices):
        found["gpu"] = "reserved"
    return found


def _compose(args: list[str], extra_env: dict[str, str]) -> dict:
    with tempfile.TemporaryDirectory() as home:
        result = subprocess.run(
            ["docker", "compose", *args, "config", "--format", "json"],
            cwd=ROOT,
            env={"PATH": os.environ.get("PATH", os.defpath), "HOME": home, **extra_env},
            capture_output=True,
            text=True,
            check=False,
            timeout=120,
        )
    if result.returncode != 0:
        raise SystemExit(f"render failed: {' '.join(args)}\n{result.stderr[-2000:]}")
    return json.loads(result.stdout)


class _ComposeLoader(yaml.SafeLoader):
    """Accepts Compose merge tags such as !override and !reset."""


# Only service names are read, so a tagged value can stay unconstructed.
_ComposeLoader.add_multi_constructor("!", lambda loader, suffix, node: None)


def _service_files(paths: list[pathlib.Path]) -> dict[str, str]:
    owners: dict[str, str] = {}
    for path in paths:
        text = path.read_text(encoding="utf-8")
        document = yaml.load(text, Loader=_ComposeLoader) or {}
        for name in document.get("services") or {}:
            owners[name] = path.relative_to(ROOT).as_posix()
    return owners


def render_models() -> dict[str, tuple[dict, dict[str, str], tuple[str, ...]]]:
    """Return {scope: (rendered model, service->file, secret roots)}."""
    infra = sorted((ROOT / "infra").rglob("docker-compose*.yml"))
    models = {
        "root": (
            _compose(["--env-file", ".env.example", "--profile", "*"], {}),
            _service_files(infra),
            (str(ROOT / "secrets") + "/",),
        )
    }
    for lab in sorted((ROOT / "labs").glob("*.yml")):
        relative = lab.relative_to(ROOT).as_posix()
        models[f"lab:{lab.stem}"] = (
            _compose(
                ["--env-file", "labs/.env.example", "-f", relative, "--profile", "*"],
                LAB_INPUTS,
            ),
            _service_files([lab]),
            (LAB_INPUTS["LAB_SECRET_DIR"] + "/", str(ROOT / "secrets") + "/"),
        )
    return models


def _date(value: object) -> dt.date | None:
    try:
        return dt.date.fromisoformat(str(value))
    except ValueError:
        return None


def check(
    registry: dict,
    models: dict[str, tuple[dict, dict[str, str], tuple[str, ...]]],
    today: dt.date,
) -> list[str]:
    findings: list[str] = []
    controls = set(registry.get("controls") or {})
    actual: dict[tuple[str, str], dict[str, object]] = {}
    files: dict[tuple[str, str], str] = {}
    for scope, (model, owners, roots) in models.items():
        for name, service in model["services"].items():
            # Only registered controls are enforced; the report shows the rest.
            found = deviations(service, roots)
            actual[(scope, name)] = {k: v for k, v in found.items() if k in controls}
            files[(scope, name)] = owners.get(name, "")
    seen: set[tuple[str, str, str]] = set()
    excepted: set[tuple[str, str, str]] = set()
    for index, row in enumerate(registry.get("exceptions") or []):
        label = f"exception {index} ({row.get('scope')}/{row.get('service')}/{row.get('control')})"
        missing = [
            field for field in FIELDS
            if field not in row or (field != "allowed_value" and row[field] in ("", None))
        ]  # fmt: skip
        if missing:
            findings.append(f"{label}: missing {', '.join(missing)}")
            continue
        if set(row) - set(FIELDS):
            findings.append(f"{label}: unknown fields {sorted(set(row) - set(FIELDS))}")
        key = (row["scope"], row["service"], row["control"])
        if "*" in row["service"] or "*" in row["compose_file"] or "*" in row["scope"]:
            findings.append(f"{label}: wildcards are not allowed")
            continue
        if row["control"] not in controls:
            findings.append(f"{label}: unregistered control")
            continue
        if row["kind"] not in KINDS:
            findings.append(f"{label}: kind must be one of {sorted(KINDS)}")
        if key in seen:
            findings.append(f"{label}: duplicate")
        seen.add(key)
        reviewed, review_by = _date(row["reviewed"]), _date(row["review_by"])
        if not reviewed or not review_by:
            findings.append(f"{label}: reviewed and review_by must be ISO dates")
        elif review_by < today:
            findings.append(f"{label}: expired on {review_by}")
        elif (review_by - reviewed).days > MAX_REVIEW_DAYS:
            findings.append(f"{label}: review_by is more than a year after reviewed")
        service_key = (row["scope"], row["service"])
        if service_key not in actual:
            findings.append(f"{label}: no such service in {row['scope']}")
            continue
        if files[service_key] != row["compose_file"]:
            findings.append(f"{label}: service is declared in {files[service_key]}")
        current = actual[service_key].get(row["control"], "conforms")
        if current == "conforms":
            findings.append(f"{label}: the service conforms; retire the exception")
        elif current != row["allowed_value"]:
            findings.append(
                f"{label}: actual value {current!r} differs from {row['allowed_value']!r}"
            )
        else:
            excepted.add(key)
    for (scope, name), found in sorted(actual.items()):
        for control, value in found.items():
            if (scope, name, control) not in excepted:
                findings.append(
                    f"{scope}/{name}: {control} is {value!r} without an exception"
                )
    return findings


def main(argv: list[str]) -> int:
    registry = json.loads((ROOT / REGISTRY).read_text(encoding="utf-8"))
    models = render_models()
    if "--report" in argv:
        for scope, (model, owners, roots) in models.items():
            for name, service in sorted(model["services"].items()):
                found = deviations(service, roots)
                if found:
                    print(json.dumps({"scope": scope, "service": name,
                                      "compose_file": owners.get(name, ""),
                                      "job": is_job(service), "deviations": found}))  # fmt: skip
        return 0
    findings = check(registry, models, dt.date.today())
    # Every Compose leaf builds on the shared templates (template adoption).
    for path in sorted(
        [*(ROOT / "infra").rglob("docker-compose*.yml"), *(ROOT / "labs").glob("*.yml")]
    ):
        if "common-optimizations.yml" not in path.read_text(encoding="utf-8"):
            findings.append(
                f"{path.relative_to(ROOT)}: does not extend common-optimizations.yml"
            )
    total = sum(len(model["services"]) for model, _, _ in models.values())
    for finding in findings:
        print(f"FAIL {finding}")
    print(
        f"compose-controls: scopes={len(models)} services={total} findings={len(findings)}"
    )
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
