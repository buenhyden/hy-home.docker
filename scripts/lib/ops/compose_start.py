"""Source-bound, value-free selection for explicit Compose starts."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
from pathlib import Path, PurePosixPath

import yaml

from scripts.lib.document_governance.operations_catalog import (
    _compose_mapping,
    _ComposeLoader,
    _read_text,
    _required_compose_dependencies,
    read_bounded_regular,
)
from scripts.lib.supply_chain.latest_version_gate import expected_from_root

POLICY = "docs/05.operations/policies/01-common/0078-compose-profile-vocabulary.md"
COMMON = "infra/common-optimizations.yml"
OBSERVABILITY_INPUTS = (
    "infra/06-observability/prometheus/config/prometheus.yml",
    "infra/06-observability/prometheus/config/prometheus.dev.yml",
    "infra/06-observability/prometheus/scripts/start.sh",
)
NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,127}\Z")


def _root(root):
    value = Path(root)
    if not value.is_absolute() or value.resolve(strict=True) != value:
        raise ValueError("unsafe_root")
    return value


def _text(root, path):
    return _read_text(root, PurePosixPath(path))


def _digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _policy(text):
    rows = re.findall(r"^\| HOME \|([^\n]+)\|$", text, re.MULTILINE)
    if len(rows) != 1:
        raise ValueError("invalid_home_policy")
    home = re.findall(r"`([A-Za-z0-9][A-Za-z0-9_.-]*)`", rows[0].split("|")[0])
    if not home or len(home) != len(set(home)):
        raise ValueError("invalid_home_policy")
    try:
        section = text.split("### Companion, exclusion and side effects", 1)[1]
    except IndexError:
        raise ValueError("missing_companion_policy") from None
    section = section.split("\n### ", 1)[0]
    companions = {}
    for producer, values in re.findall(
        r"^\| `([A-Za-z0-9][A-Za-z0-9_.-]*)` \| `([^`]+)` \|$",
        section,
        re.MULTILINE,
    ):
        names = values.split()
        if (
            producer in companions
            or producer not in names
            or len(names) != len(set(names))
            or any(not NAME.fullmatch(name) for name in names)
        ):
            raise ValueError("invalid_companion_policy")
        companions[producer] = tuple(name for name in names if name != producer)
    if not companions:
        raise ValueError("missing_companion_policy")
    return tuple(home), companions


def _inspect_targets(root, selected):
    from scripts.lib.ops.compose_observation import inspect_targets

    return inspect_targets(root, selected)


def _unique_mapping(node):
    if not isinstance(node, yaml.MappingNode):
        raise ValueError("invalid_selection_mapping")
    result = {}
    for key, value in node.value:
        if key.tag == "tag:yaml.org,2002:merge":
            continue
        if not isinstance(key, yaml.ScalarNode) or key.value in result:
            raise ValueError("duplicate_selection_key")
        result[key.value] = value
    return result


def _selection_nodes(text):
    try:
        root = yaml.compose(text, Loader=_ComposeLoader)
        top = _unique_mapping(root)
        service_node = top.get("services")
        if service_node is None:
            return
        for service in _unique_mapping(service_node).values():
            items = _unique_mapping(service)
            for name in ("profiles", "depends_on", "extends"):
                value = items.get(name)
                if value is None:
                    continue
                if value.tag in {"!reset", "!override"}:
                    raise ValueError("unsupported_selection_tag")
                if name == "depends_on" and isinstance(value, yaml.MappingNode):
                    for rule in _unique_mapping(value).values():
                        if isinstance(rule, yaml.MappingNode):
                            _unique_mapping(rule)
    except yaml.YAMLError:
        raise ValueError("invalid_compose_yaml") from None


def _dependencies(service):
    value = service.get("depends_on", {})
    if isinstance(value, list):
        if any(
            not isinstance(name, str) or not NAME.fullmatch(name) for name in value
        ) or len(value) != len(set(value)):
            raise ValueError("invalid_dependencies")
    elif isinstance(value, dict):
        for name, rule in value.items():
            if (
                not isinstance(name, str)
                or not NAME.fullmatch(name)
                or not isinstance(rule, dict)
            ):
                raise ValueError("invalid_dependencies")
            if set(rule) - {"condition", "required", "restart"}:
                raise ValueError("invalid_dependencies")
            if rule.get("condition", "service_started") not in {
                "service_started",
                "service_healthy",
                "service_completed_successfully",
            }:
                raise ValueError("invalid_dependencies")
            if any(
                key in rule and type(rule[key]) is not bool
                for key in ("required", "restart")
            ):
                raise ValueError("invalid_dependencies")
    else:
        raise ValueError("invalid_dependencies")
    return _required_compose_dependencies(service)


def _sources(root):
    names, binding = expected_from_root(root)
    inputs = {item["path"]: item["sha256"] for item in binding["input_files"]}
    services = {}
    extends = []
    for item in binding["input_files"]:
        path = item["path"]
        _selection_nodes(_text(root, path))
        document = _compose_mapping(root, PurePosixPath(path))
        if _digest(_text(root, path)) != item["sha256"]:
            raise ValueError("source_changed")
        for name, service in document.get("services", {}).items():
            if (
                not isinstance(name, str)
                or not NAME.fullmatch(name)
                or not isinstance(service, dict)
            ):
                raise ValueError("invalid_service")
            if name in services:
                raise ValueError("duplicate_service")
            _dependencies(service)
            services[name] = service
            if "extends" in service:
                extends.append((path, service["extends"]))
    if sorted(services) != names:
        raise ValueError("source_changed")
    if extends:
        templates = _compose_mapping(root, PurePosixPath(COMMON)).get("services", {})
        if not isinstance(templates, dict):
            raise ValueError("unsupported_extends")
        for source, extension in extends:
            if not isinstance(extension, dict) or set(extension) != {"file", "service"}:
                raise ValueError("unsupported_extends")
            target = PurePosixPath(source).parent.joinpath(extension["file"])
            import posixpath

            if posixpath.normpath(str(target)) != COMMON:
                raise ValueError("unsupported_extends")
            template = templates.get(extension["service"])
            if not isinstance(template, dict) or any(
                key in template for key in ("profiles", "depends_on", "extends")
            ):
                raise ValueError("unsupported_extends")
        inputs[COMMON] = _digest(_text(root, COMMON))
    for path in (POLICY, *OBSERVABILITY_INPUTS):
        inputs[path] = _digest(_text(root, path))
    home, companions = _policy(_text(root, POLICY))
    if any(
        name not in services
        for producer, items in companions.items()
        for name in (producer, *items)
    ):
        raise ValueError("missing_companion")
    return services, home, companions, inputs


def _profiles(services):
    result = set()
    for service in services.values():
        profiles = service.get("profiles", [])
        if (
            not isinstance(profiles, list)
            or any(not isinstance(p, str) or not NAME.fullmatch(p) for p in profiles)
            or len(profiles) != len(set(profiles))
        ):
            raise ValueError("invalid_profiles")
        result.update(profiles)
    return result


def _closure(services, initial, companions, mode):
    reasons = {name: {f"selected:{mode}"} for name in initial}
    while True:
        before = set(reasons)
        active_profiles = {
            profile
            for name in reasons
            for profile in services[name].get("profiles", [])
        }
        for name in sorted(before):
            dependencies = _dependencies(services[name])
            value = services[name].get("depends_on", {})
            optional = (
                (item for item, rule in value.items() if rule.get("required") is False)
                if isinstance(value, dict)
                else ()
            )
            for target, reason in (
                *((item, f"dependency:{name}") for item in dependencies),
                *((item, f"companion:{name}") for item in companions.get(name, ())),
                *(
                    (item, f"optional-dependency:{name}")
                    for item in optional
                    if item in services
                    and (
                        not services[item].get("profiles")
                        or set(services[item]["profiles"]) & active_profiles
                    )
                ),
            ):
                if target not in services:
                    raise ValueError("missing_dependency")
                reasons.setdefault(target, set()).add(reason)
        if set(reasons) == before:
            break
    selected = set(reasons)
    done, visiting = set(), set()

    def visit(name):
        if name in visiting:
            raise ValueError("dependency_cycle")
        if name in done:
            return
        visiting.add(name)
        value = services[name].get("depends_on", {})
        optional = (
            (item for item, rule in value.items() if rule.get("required") is False)
            if isinstance(value, dict)
            else ()
        )
        for target in (*_dependencies(services[name]), *optional):
            if target in selected:
                visit(target)
        visiting.remove(name)
        done.add(name)

    for name in sorted(selected):
        visit(name)
    return {name: sorted(reasons[name]) for name in sorted(reasons)}


def _host_bindings(service):
    """Yield (host_ip, host_port, protocol) source expressions a service publishes."""
    for item in service.get("ports") or ():
        if isinstance(item, dict):
            if item.get("published") is not None:
                yield (
                    str(item.get("host_ip", "")),
                    str(item["published"]),
                    str(item.get("protocol", "tcp")),
                )
            continue
        text, protocol = str(item), "tcp"
        if text.endswith(("/tcp", "/udp", "/sctp")):
            text, protocol = text.rsplit("/", 1)
        parts, depth, current = [], 0, ""
        for char in text:  # split on ':' outside ${...}
            depth += (char == "{") - (char == "}")
            if char == ":" and depth == 0:
                parts.append(current)
                current = ""
            else:
                current += char
        parts.append(current)
        if len(parts) >= 2:
            yield (":".join(parts[:-2]), parts[-2], protocol)


def _reject_host_port_conflicts(services, selected):
    # ponytail: compares unrendered source expressions, so two different
    # variables that resolve to the same value are not caught; render the
    # selection first if that matters.
    owners = {}
    for name in sorted(selected):
        for binding in set(_host_bindings(services[name])):
            if owners.setdefault(binding, name) != name:
                raise ValueError("host_port_conflict")


def create_plan(root, *, mode, values, dev_data_expected=None):
    root = _root(root)
    if mode not in {"home", "profile", "target"} or not isinstance(
        values, (list, tuple)
    ):
        raise ValueError("invalid_selection")
    if any(not isinstance(item, str) or not NAME.fullmatch(item) for item in values):
        raise ValueError("invalid_selection")
    selection = sorted(set(values))
    if (mode == "home") != (not selection):
        raise ValueError("invalid_selection")
    if (mode == "target" and dev_data_expected is not None) or (
        mode != "target" and dev_data_expected not in {"on", "off"}
    ):
        raise ValueError("invalid_dev_state")
    services, home, companions, inputs = _sources(root)
    available = _profiles(services)
    profiles = sorted(
        home if mode == "home" else selection if mode == "profile" else ()
    )
    if set(profiles) - available:
        raise ValueError("unknown_profile")
    if mode == "target":
        if set(selection) - services.keys():
            raise ValueError("unknown_target")
        initial = set(selection)
    else:
        initial = {
            name
            for name, service in services.items()
            if not service.get("profiles") or set(service["profiles"]) & set(profiles)
        }
    if not initial:
        raise ValueError("empty_selection")
    reasons = _closure(services, initial, companions, mode)
    _reject_host_port_conflicts(services, reasons)
    if mode != "target":
        selected_dev = bool({"dev-pg", "dev-valkey"} & reasons.keys())
        if dev_data_expected != ("on" if selected_dev else "off"):
            raise ValueError("dev_state_conflict")
    observations = _inspect_targets(root, tuple(reasons))
    if not isinstance(observations, list):
        raise ValueError("invalid_observations")
    project = _compose_mapping(root, PurePosixPath("docker-compose.yml")).get("name")
    if not isinstance(project, str) or not re.fullmatch(
        r"[a-z0-9][a-z0-9_-]*", project
    ):
        raise ValueError("invalid_project")
    if any(_digest(_text(root, name)) != digest for name, digest in inputs.items()):
        raise ValueError("source_changed")
    document = {
        "version": 1,
        "project": project,
        "effect": "explicit up may recreate containers and may partially succeed",
        "mode": mode,
        "selection": selection,
        "profiles": profiles,
        "targets": sorted(reasons),
        "reasons": reasons,
        "provision_jobs": sorted(
            name for name in reasons if re.search(r"(?:-init|-provision)$", name)
        ),
        "dev_data_expected": dev_data_expected,
        "observations": observations,
        "inputs": [
            {"path": name, "sha256": digest} for name, digest in sorted(inputs.items())
        ],
    }
    document["fingerprint"] = hashlib.sha256(
        json.dumps(
            document, sort_keys=True, separators=(",", ":"), ensure_ascii=True
        ).encode()
    ).hexdigest()
    return document


def validate_plan(root, document):
    if not isinstance(document, dict) or type(document.get("version")) is not int:
        raise ValueError("invalid_plan")
    try:
        expected = create_plan(
            root,
            mode=document["mode"],
            values=document["selection"],
            dev_data_expected=document["dev_data_expected"],
        )
    except (KeyError, TypeError):
        raise ValueError("invalid_plan") from None
    if document != expected:
        raise ValueError("plan_mismatch")
    return expected


def execute_plan(root, document, *, runner=None):
    """Recompute the plan; failures can leave containers partially changed."""
    root = _root(root)
    plan = validate_plan(root, document)
    overlay = None
    if plan["mode"] == "target" and "prometheus" in plan["targets"]:
        raise ValueError("partial_prometheus_forbidden")
    if plan["mode"] != "target" and "prometheus" in plan["targets"]:
        from scripts.lib.ops.compose_observation import (
            materialize,
            validate_materialized,
        )

        directory = Path("/tmp") / f"hyhome-p07-{os.geteuid()}" / plan["fingerprint"]
        overlay = materialize(root, plan, directory)
        validate_plan(root, plan)
        validate_materialized(root, plan, overlay)
    argv = [
        "/usr/bin/docker",
        "--host",
        "unix:///var/run/docker.sock",
        "compose",
        "--project-name",
        plan["project"],
        "--project-directory",
        str(root),
        "-f",
        str(root / "docker-compose.yml"),
    ]
    if overlay is not None:
        argv += ["-f", str(overlay)]
    argv += ["up", "-d", "--no-build", "--pull", "never", *plan["targets"]]
    environment = {"PATH": "/usr/bin:/bin", "HOME": "/nonexistent"}
    try:
        result = (runner or subprocess.run)(
            argv,
            cwd=root,
            env=environment,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
            timeout=300,
        )
        if result.returncode == 0:
            return {"result": "STARTED", "recovery_required": False}
    except (OSError, subprocess.TimeoutExpired):
        pass
    return {"result": "START_FAILED", "recovery_required": True}


def load_plan(root, path):
    root = _root(root)
    value = Path(path)
    if not value.is_absolute():
        value = root / value
    try:
        relative = value.relative_to(root)
    except ValueError:
        raise ValueError("unsafe_plan_path") from None
    prefix = ("_workspace", "repo-support", "analysis", "p07", "plans")
    if relative.parts[: len(prefix)] != prefix or ".." in relative.parts:
        raise ValueError("unsafe_plan_path")

    def unique(pairs):
        result = {}
        for key, item in pairs:
            if key in result:
                raise ValueError("duplicate_json_key")
            result[key] = item
        return result

    data = read_bounded_regular(
        root, PurePosixPath(relative), max_bytes=2 * 1024 * 1024
    )
    try:
        return json.loads(
            data,
            object_pairs_hook=unique,
            parse_constant=lambda _: (_ for _ in ()).throw(ValueError("invalid_json")),
        )
    except (UnicodeError, json.JSONDecodeError):
        raise ValueError("invalid_json") from None
