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
import hashlib
import json
import math
import os
import pathlib
import posixpath
import re
import subprocess
import sys
import tempfile

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
REGISTRY = "infra/common-optimizations.exceptions.json"
# Synthetic, non-HOME inputs: only enough to render each LAB model.
LAB_INPUTS = {
    "LAB_DATA_DIR": "/nonexistent/lab-data",
    "LAB_SECRET_DIR": "/nonexistent/lab-secrets",
    "LAB_KAFKA_CLUSTER_ID": "synthetic-lab-cluster",
    "LAB_LOCUST_SCENARIO_DIR": "/nonexistent/locust-scenario",
    "LAB_LOCUST_RESULT_DIR": "/nonexistent/locust-results",
    "LAB_OPENSEARCH_CERT_DIR": "/nonexistent/opensearch-certs",
    # Required HOME endpoints of the SPEC-0262 LABs; same synthetic values as
    # tests/validation/test_lab_isolation.py.
    "LAB_LAKEHOUSE_S3_ENDPOINT": "http://lab-endpoint.invalid:8333",
    "LAB_LAKEHOUSE_CATALOG_URI": "http://lab-endpoint.invalid:8181",
    "LAB_DBT_DB_HOST": "lab-endpoint.invalid",
    "LAB_SUPERSET_DB_HOST": "lab-endpoint.invalid",
    "LAB_SUPERSET_DEFAULT_URL": "lab.invalid",
    "LAB_SUPERSET_CA_FILE": "/nonexistent/lab-ca/rootCA.pem",
    "LAB_SONARQUBE_DB_HOST": "lab-endpoint.invalid",
    "LAB_STALWART_DEFAULT_URL": "lab.invalid",
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
REGISTRY_FIELDS = frozenset(
    {
        "schema_version",
        "policy_id",
        "template_source",
        "owner_role",
        "review_cadence",
        "description",
        "controls",
        "exceptions",
        "naming_exceptions",
    }
)
SUPPORTED_CONTROLS = frozenset(
    {
        "no_new_privileges",
        "cap_drop_all",
        "cap_add",
        "privileged",
        "init",
        "restart",
        "healthcheck",
        "cpus",
        "mem_limit",
        "pids_limit",
        "secrets_group",
        "gpu",
    }
)


def _unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate_registry_key")
        result[key] = value
    return result


def validate_registry(registry: dict) -> dict:
    """Validate the canonical shape after a caller's bounded duplicate-safe read."""
    if not isinstance(registry, dict) or set(registry) != REGISTRY_FIELDS:
        raise ValueError("invalid_registry_shape")
    if (
        type(registry["schema_version"]) is not int
        or registry["schema_version"] != 2
        or registry["policy_id"] != "OPS-TPL-EXCEPTIONS-001"
        or registry["template_source"] != "infra/common-optimizations.yml"
    ):
        raise ValueError("invalid_registry_identity")
    if any(
        not isinstance(registry[k], str) or not registry[k].strip()
        for k in ("owner_role", "review_cadence", "description")
    ):
        raise ValueError("invalid_registry_metadata")
    registered = registry["controls"]
    if (
        not isinstance(registered, dict)
        or set(registered) != SUPPORTED_CONTROLS
        or any(not isinstance(v, str) or not v.strip() for v in registered.values())
    ):
        raise ValueError("invalid_registry_controls")
    if (
        not isinstance(registry["exceptions"], list)
        or any(
            not isinstance(row, dict)
            or set(row) != set(FIELDS)
            or any(
                not isinstance(row[field], str) or not row[field].strip()
                for field in FIELDS
                if field != "allowed_value"
            )
            for row in registry["exceptions"]
        )
        or not isinstance(registry["naming_exceptions"], list)
        or any(
            not isinstance(row, dict)
            or set(row) != {"service", "container_name", "reason"}
            or any(not isinstance(v, str) or not v.strip() for v in row.values())
            for row in registry["naming_exceptions"]
        )
    ):
        raise ValueError("invalid_registry_entries")
    names = [
        (row["service"], row["container_name"]) for row in registry["naming_exceptions"]
    ]
    if len({service for service, _ in names}) != len(names) or len(
        {container for _, container in names}
    ) != len(names):
        raise ValueError("duplicate_naming_exception")
    return registry


def load_registry(path: pathlib.Path) -> dict:
    """Load the exact canonical registry shape without losing duplicate keys."""
    from scripts.lib.document_governance.operations_catalog import read_bounded_regular

    path = pathlib.Path(path)
    try:
        relative = pathlib.PurePosixPath(path.relative_to(ROOT).as_posix())
        root = ROOT
    except ValueError:
        root, relative = path.parent, pathlib.PurePosixPath(path.name)
    raw = read_bounded_regular(root, relative)
    registry = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_pairs)
    return validate_registry(registry)


def _limits(service: dict) -> dict:
    return ((service.get("deploy") or {}).get("resources") or {}).get("limits") or {}


def is_job(service: dict) -> bool:
    return str(service.get("restart", "")) == "no"


def _positive_limit(value: object, kind: str) -> bool:
    if isinstance(value, bool):
        return False
    if isinstance(value, (int, float)):
        try:
            return (
                math.isfinite(value)
                and value > 0
                and (kind != "pids" or int(value) == value)
            )
        except (OverflowError, ValueError):
            return False
    if not isinstance(value, str) or len(value) > 64:
        return False
    pattern = {
        "cpus": r"[0-9]+(?:\.[0-9]+)?",
        "memory": r"[0-9]+(?:\.[0-9]+)?(?:[bkmg](?:i?b)?)?",
        "pids": r"[0-9]+",
    }[kind]
    if re.fullmatch(pattern, value, re.IGNORECASE) is None:
        return False
    number = re.match(r"[0-9]+(?:\.[0-9]+)?", value)
    return (
        number is not None
        and math.isfinite(float(number.group()))
        and float(number.group()) > 0
    )


def _has_positive_limit(service: dict, field: str, nested: str) -> bool:
    values = [
        value
        for value in (service.get(field), _limits(service).get(nested))
        if value is not None
    ]
    return bool(values) and all(_positive_limit(value, nested) for value in values)


def _no_new_privileges_enabled(service: dict) -> bool:
    options = [str(value) for value in service.get("security_opt") or []]
    relevant = [
        value
        for value in options
        if value == "no-new-privileges"
        or value.startswith(("no-new-privileges:", "no-new-privileges="))
    ]
    return relevant == ["no-new-privileges:true"]


def needs_secret_group(service: dict, secret_roots: tuple[str, ...]) -> bool:
    if service.get("secrets"):
        return True
    for volume in service.get("volumes") or []:
        source = str(volume.get("source", "")) if isinstance(volume, dict) else ""
        if isinstance(volume, dict) and volume.get("type") == "bind" and source:
            normalized = posixpath.normpath(source)
            for root in secret_roots:
                if root:
                    boundary = posixpath.normpath(root)
                    if normalized == boundary or normalized.startswith(
                        boundary.rstrip("/") + "/"
                    ):
                        return True
    return False


def deviations(service: dict, secret_roots: tuple[str, ...]) -> dict[str, object]:
    """Return {control: actual value} for every control the service misses."""
    found: dict[str, object] = {}
    if not _no_new_privileges_enabled(service):
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
    if not _has_positive_limit(service, "cpus", "cpus"):
        found["cpus"] = None
    if not _has_positive_limit(service, "mem_limit", "memory"):
        found["mem_limit"] = None
    if not _has_positive_limit(service, "pids_limit", "pids"):
        found["pids_limit"] = None
    devices = ((service.get("deploy") or {}).get("resources") or {}).get(
        "reservations", {}
    ).get("devices") or []
    if (
        any("gpu" in (device.get("capabilities") or []) for device in devices)
        or service.get("gpus")
        or service.get("runtime") == "nvidia"
    ):
        found["gpu"] = "reserved"
    return found


def _compose(
    args: list[str], extra_env: dict[str, str], *, cwd: pathlib.Path = ROOT
) -> dict:
    with tempfile.TemporaryDirectory() as home:
        try:
            result = subprocess.run(
                [
                    "docker",
                    "compose",
                    *args,
                    "config",
                    "--no-env-resolution",
                    "--format",
                    "json",
                ],
                cwd=cwd,
                env={
                    "PATH": os.environ.get("PATH", os.defpath),
                    "HOME": home,
                    "DOCKER_CONFIG": home,
                    **extra_env,
                },
                capture_output=True,
                text=True,
                check=False,
                timeout=120,
            )
        except (OSError, subprocess.TimeoutExpired):
            raise ValueError("compose_render_unavailable") from None
    if result.returncode != 0:
        raise ValueError("compose_render_failed")
    try:
        model = json.loads(result.stdout)
    except (ValueError, TypeError):
        raise ValueError("compose_render_invalid") from None
    if not isinstance(model, dict) or not isinstance(model.get("services"), dict):
        raise ValueError("compose_render_invalid")
    return model


class _ComposeLoader(yaml.SafeLoader):
    """Accepts Compose merge tags such as !override and !reset."""

    def construct_mapping(self, node, deep=False):
        explicit = set()
        for key, _ in node.value:
            if key.tag == "tag:yaml.org,2002:merge":
                continue
            name = self.construct_object(key, deep=deep)
            if name in explicit:
                raise ValueError("duplicate_compose_key")
            explicit.add(name)
        return super().construct_mapping(node, deep=deep)


# Only service names are read, so a tagged value can stay unconstructed.
_ComposeLoader.add_multi_constructor("!", lambda loader, suffix, node: None)


def _service_files(paths: list[pathlib.Path]) -> dict[str, str]:
    from scripts.lib.ops.workspace_inventory import _read_public

    owners: dict[str, str] = {}
    for path in paths:
        text = _read_public(ROOT, path.relative_to(ROOT).as_posix()).decode("utf-8")
        document = yaml.load(text, Loader=_ComposeLoader) or {}
        for name in document.get("services") or {}:
            if name in owners:
                raise ValueError(f"duplicate_service_owner: {name}")
            owners[name] = path.relative_to(ROOT).as_posix()
    return owners


def template_findings(paths: list[pathlib.Path]) -> list[str]:
    """Require each regular service to actually extend the canonical template."""
    from scripts.lib.ops.workspace_inventory import _read_public

    findings = []
    for path in paths:
        text = _read_public(ROOT, path.relative_to(ROOT).as_posix()).decode("utf-8")
        document = yaml.load(text, Loader=_ComposeLoader) or {}
        for name, service in (document.get("services") or {}).items():
            extends = service.get("extends") if isinstance(service, dict) else None
            file = extends.get("file") if isinstance(extends, dict) else None
            template = extends.get("service") if isinstance(extends, dict) else None
            target = (
                posixpath.normpath(
                    posixpath.join(path.parent.relative_to(ROOT).as_posix(), file)
                )
                if isinstance(file, str)
                else None
            )
            if (
                target != "infra/common-optimizations.yml"
                or not isinstance(template, str)
                or not template.startswith("template-")
            ):
                findings.append(
                    f"{path.relative_to(ROOT)}/{name}: does not extend common-optimizations.yml"
                )
    return findings


def _control_identity(service: dict, control: str, roots: tuple[str, ...]):
    """Compare determining fields rather than only the reported deviation."""
    if control == "no_new_privileges":
        return _no_new_privileges_enabled(service)
    if control == "cap_drop_all":
        return "ALL" in [str(x) for x in service.get("cap_drop") or []]
    if control == "init":
        return service.get("init") is True
    if control == "healthcheck":
        check = service.get("healthcheck") or {}
        return (is_job(service), bool(check) and not check.get("disable"))
    if control in {"cpus", "mem_limit", "pids_limit"}:
        nested = {"cpus": "cpus", "mem_limit": "memory", "pids_limit": "pids"}[control]
        return (service.get(control), _limits(service).get(nested))
    if control == "secrets_group":
        return (
            SECRETS_GID in {str(x) for x in service.get("group_add") or []},
            needs_secret_group(service, roots),
        )
    if control == "gpu":
        devices = (
            ((service.get("deploy") or {}).get("resources") or {}).get("reservations")
            or {}
        ).get("devices")
        return (service.get("gpus"), service.get("runtime"), devices)
    fields = {
        "cap_add": ("cap_add",),
        "privileged": ("privileged",),
        "restart": ("restart",),
    }
    return tuple((key, service.get(key)) for key in fields[control])


def overlay_findings(
    registry: dict, base: dict, overlay: dict, path: str, roots: tuple[str, ...]
) -> list[str]:
    """Reject changed or new deviations in an explicitly selected overlay.

    The registry has no overlay selection key: a changed deviation cannot
    borrow the base exception. The base itself is checked separately.
    """
    base_services = base.get("services", {})
    services = overlay.get("services", {})
    if set(services) != set(base_services):
        raise ValueError("overlay_service_set_changed")
    findings = []
    for name, service in sorted(services.items()):
        before = base_services[name]
        base_deviations = deviations(before, roots)
        for control, value in deviations(service, roots).items():
            if control not in registry["controls"]:
                continue
            if base_deviations.get(control, "conforms") != value or _control_identity(
                before, control, roots
            ) != _control_identity(service, control, roots):
                findings.append(
                    f"overlay:{path}/{name}: {control} is {value!r} without a selection-specific exception"
                )
    return findings


def _public_hashes(paths: set[str]) -> dict[str, str]:
    from scripts.lib.ops.workspace_inventory import _read_public

    return {
        path: hashlib.sha256(_read_public(ROOT, path)).hexdigest() for path in paths
    }


class RenderedModels(dict):
    """The rendered models and exact public inputs used to produce them."""

    def __init__(self, initial: dict, fingerprints: dict[str, str]):
        super().__init__(initial)
        self.fingerprints = fingerprints.copy()


def _copy_public_render_sources(
    copied: pathlib.Path, sources: set[str], *, expected: dict[str, str] | None = None
) -> None:
    """Copy only approved public Compose inputs and neutralize file reads."""
    from scripts.lib.ops._workspace_render import _prepare_sources
    from scripts.lib.ops.workspace_inventory import _read_public

    for source in sorted(sources | {".env.example", "labs/.env.example"}):
        raw = _read_public(ROOT, source)
        if expected is not None and hashlib.sha256(raw).hexdigest() != expected.get(
            source
        ):
            raise ValueError("compose_source_changed")
        target = copied / source
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
    _, blocked = _prepare_sources(copied, [{"path": path} for path in sorted(sources)])
    if blocked:
        raise ValueError("unsafe_compose_source")


def _source_inventory():
    """Identify candidate sources, refusing untracked configuration inputs."""
    from scripts.lib.document_governance.operations_catalog import (
        MAX_TRACKED_FILES,
        _conftest_untracked_candidates,
        _is_infra_compose_file,
        _tracked_paths,
    )

    _conftest_untracked_candidates(ROOT)
    tracked = _tracked_paths(ROOT, MAX_TRACKED_FILES)
    labs = sorted((ROOT / "labs").glob("*.yml"))
    snapshot_paths = (
        {path.as_posix() for path in tracked if _is_infra_compose_file(path)}
        | {p.relative_to(ROOT).as_posix() for p in labs}
        | {
            "docker-compose.yml",
            "infra/common-optimizations.yml",
            ".env.example",
            "labs/.env.example",
            REGISTRY,
        }
    )
    return tracked, labs, snapshot_paths


def _validate_source_snapshot(fingerprints: dict[str, str]) -> None:
    _, _, current = _source_inventory()
    if current != set(fingerprints) or _public_hashes(current) != fingerprints:
        raise ValueError("compose_source_changed")


def render_models() -> dict[str, tuple[dict, dict[str, str], tuple[str, ...]]]:
    """Return {scope: (rendered model, service->file, secret roots)}."""
    from scripts.lib.document_governance.operations_catalog import _compose_sources
    from scripts.lib.supply_chain.latest_version_gate import expected_from_root

    tracked, labs, snapshot_paths = _source_inventory()
    fingerprints = _public_hashes(snapshot_paths)
    _, census = expected_from_root(ROOT)
    infra = [ROOT / item["path"] for item in census["input_files"]]
    sources = _compose_sources(ROOT, tracked)
    # An unannotated overlay must not silently steal an existing owner's name.
    _service_files([ROOT / path for path in sources.regular])
    owners = _service_files(infra)
    public_sources = {p.relative_to(ROOT).as_posix() for p in infra + labs}
    public_sources.update(
        path.as_posix() for path in (*sources.regular, *sources.overlays)
    )
    public_sources.add("infra/common-optimizations.yml")
    synthetic = {
        "OPSFLOW_CODE_DIR": "/nonexistent/p09-code",
        "OPSFLOW_SECRET_DIR": "/nonexistent/p09-secrets",
        "OPSFLOW_AIRFLOW_IMAGE": "example.invalid/p09/airflow:synthetic",
    }
    with tempfile.TemporaryDirectory(prefix="p09-compose-") as tmp:
        copied = pathlib.Path(tmp)
        _copy_public_render_sources(copied, public_sources, expected=fingerprints)
        roots = (str(copied / "secrets") + "/", synthetic["OPSFLOW_SECRET_DIR"] + "/")
        root_model = _compose(
            ["--env-file", ".env.example", "--profile", "*"], {}, cwd=copied
        )
        if set(owners) != set(root_model["services"]):
            raise ValueError("root_service_ownership_mismatch")
        models = RenderedModels({"root": (root_model, owners, roots)}, fingerprints)
        for overlay in sources.overlays:
            relative = overlay.as_posix()
            try:
                selected = _compose(
                    [
                        "--env-file",
                        ".env.example",
                        "-f",
                        "docker-compose.yml",
                        "-f",
                        relative,
                        "--profile",
                        "*",
                    ],
                    synthetic,
                    cwd=copied,
                )
            except ValueError:
                raise ValueError(f"overlay_render_failed: {relative}") from None
            models[f"overlay:{relative}"] = (selected, owners, roots)
        for lab in labs:
            relative = lab.relative_to(ROOT).as_posix()
            models[f"lab:{lab.stem}"] = (
                _compose(
                    [
                        "--env-file",
                        "labs/.env.example",
                        "-f",
                        relative,
                        "--profile",
                        "*",
                    ],
                    LAB_INPUTS,
                    cwd=copied,
                ),
                _service_files([lab]),
                (LAB_INPUTS["LAB_SECRET_DIR"] + "/", str(copied / "secrets") + "/"),
            )
    _validate_source_snapshot(fingerprints)
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
        if scope.startswith("overlay:"):
            continue
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
        else:
            if reviewed > today:
                findings.append(f"{label}: reviewed is in the future")
            if review_by < reviewed:
                findings.append(f"{label}: review_by is before reviewed")
            if review_by < today:
                findings.append(f"{label}: expired on {review_by}")
            elif (review_by - reviewed).days > MAX_REVIEW_DAYS:
                findings.append(
                    f"{label}: review_by is more than a year after reviewed"
                )
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
    for scope, (model, _, roots) in models.items():
        if scope.startswith("overlay:"):
            findings.extend(
                overlay_findings(registry, models["root"][0], model, scope[8:], roots)
            )
    return findings


def main(argv: list[str]) -> int:
    try:
        registry_hash = _public_hashes({REGISTRY})
        registry = load_registry(ROOT / REGISTRY)
        models = render_models()
        if _public_hashes({REGISTRY}) != registry_hash:
            raise ValueError("registry_changed")
    except (ValueError, OSError, yaml.YAMLError) as error:
        print(f"FAIL invalid control inputs: {type(error).__name__}")
        return 1
    if "--report" in argv:
        for scope, (model, owners, roots) in models.items():
            for name, service in sorted(model["services"].items()):
                found = deviations(service, roots)
                if found:
                    print(json.dumps({"scope": scope, "service": name,
                                      "compose_file": owners.get(name, ""),
                                      "job": is_job(service), "deviations": found}))  # fmt: skip
        return 0
    try:
        findings = check(registry, models, dt.date.today())
        # Evaluate actual source relations, never comments claiming an extends.
        from scripts.lib.supply_chain.latest_version_gate import expected_from_root

        _, census = expected_from_root(ROOT)
        source_paths = [ROOT / row["path"] for row in census["input_files"]]
        findings.extend(
            template_findings([*source_paths, *(ROOT / "labs").glob("*.yml")])
        )
        _validate_source_snapshot(models.fingerprints)
    except (ValueError, OSError, yaml.YAMLError, TypeError) as error:
        print(f"FAIL invalid control inputs: {type(error).__name__}")
        return 1
    total = sum(len(model["services"]) for model, _, _ in models.values())
    for finding in findings:
        print(f"FAIL {finding}")
    print(
        f"compose-controls: scopes={len(models)} services={total} findings={len(findings)}"
    )
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
