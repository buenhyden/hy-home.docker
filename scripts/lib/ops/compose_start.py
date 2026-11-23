"""Source-bound, value-free selection for explicit Compose starts."""

from __future__ import annotations

import hashlib
import json
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

POLICY = "docs/05.operations/02.policies/01.common/0078-compose-profile-vocabulary.md"
COMMON = "infra/common-optimizations.yml"
OBSERVABILITY_INPUTS = (
    "infra/06-observability/prometheus/config/prometheus.yml",
    "infra/06-observability/prometheus/config/prometheus.dev.yml",
    "infra/06-observability/prometheus/scripts/start.sh",
)
NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,127}\Z")


class _OperatingSetupError(Exception):
    def __init__(self, token, released, cleanup_pending):
        self.token = token
        self.released = released
        self.cleanup_pending = cleanup_pending


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


COMPOSE_FILE_LINE = re.compile(r"[ \t]*(?:export[ \t]+)?COMPOSE_FILE[ \t]*=(.*)")


def _compose_files(root):
    """Compose files named by the root .env COMPOSE_FILE, as `docker compose` reads them.

    Only the root .env counts; a process COMPOSE_FILE stays untrusted. Other .env
    lines are never kept or reported.
    """
    try:
        data = read_bounded_regular(root, PurePosixPath(".env"))
    except Exception:
        if (root / ".env").exists() or (root / ".env").is_symlink():
            raise ValueError("invalid_compose_file") from None
        return ("docker-compose.yml",)
    values = [
        match.group(1).strip()
        for line in data.decode("utf-8", "replace").splitlines()
        if (match := COMPOSE_FILE_LINE.fullmatch(line))
    ]
    if not values:
        return ("docker-compose.yml",)
    if len(values) != 1:
        raise ValueError("invalid_compose_file")
    value = values[0]
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1]
    # POL-0078: no overlay is applied through COMPOSE_FILE; maintenance overlays
    # use an explicit -f in their runbook. Anything but the root file is refused.
    if value != "docker-compose.yml":
        raise ValueError("compose_file_overlay_forbidden")
    files = ("docker-compose.yml",)
    return files


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
    for path in (POLICY, *OBSERVABILITY_INPUTS, *_compose_files(root)[1:]):
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
    if mode == "home" and dev_data_expected == "on":
        profiles = sorted({*profiles, "dev-data"})  # POL-0078 HOME activation
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
        "compose_files": list(_compose_files(root)),
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


def _operating_admission(root, plan):
    from scripts.lib.ops.dispatch_process import (
        CONTROLLER_CPUS,
        CONTROLLER_DISK_BYTES,
        CONTROLLER_MEMORY_BYTES,
    )
    from scripts.operations import lab

    admission = lab.execution_admission(root)
    model = lab.render("/usr/bin/docker", root / ".env", None)
    selected = {name: model["services"][name] for name in plan["targets"]}
    footprint = lab.footprint({**model, "services": selected})
    failed, unmeasured = lab.candidate_problems(footprint)
    if failed or unmeasured:
        raise ValueError("selected_resource_accounting_incomplete")
    # No per-service lifetime disk estimate exists for the operating stack.
    # Serialize its short startup conservatively with all admissible disk;
    # successful handoff below accounts its live containers instead.
    claimed = admission.admit(
        services=plan["targets"],
        kind="compose-start",
        project=plan["project"],
        budget={
            "cpus": footprint["reserved_cpus"] + CONTROLLER_CPUS,
            "memory_bytes": footprint["reserved_memory"] + CONTROLLER_MEMORY_BYTES,
            "disk_bytes": CONTROLLER_DISK_BYTES,
            "runtime_seconds": 300,
        },
        resources=[f"start:{plan['project']}:{name}" for name in plan["targets"]],
        fill_disk=True,
    )
    from scripts.lib.ops.dispatch_process import (
        cleanup_unstarted_registered_docker,
        prepare_registered_docker,
        verify_registered_docker_absent,
    )

    try:
        admission.update(
            claimed["token"],
            one_shot_services=sorted(
                name
                for name, service in selected.items()
                if service.get("restart") == "no"
            ),
        )
        prepare_registered_docker(admission, claimed["token"])
        # Inside the setup guard: the fill-disk claim already exists, so a
        # failed state read must still return its token for recovery.
        claimed = next(r for r in admission.records() if r["token"] == claimed["token"])
    except (OSError, ValueError, lab.LabError, StopIteration) as error:
        released = False
        cleanup_pending = False
        try:
            current = next(
                row for row in admission.records() if row["token"] == claimed["token"]
            )
            cleanup_pending = not cleanup_unstarted_registered_docker(
                current, owner_may_be_live=True
            )
            if not cleanup_pending:
                released = admission.release(
                    claimed["token"],
                    verify=lambda row: (
                        row["owner"] == claimed["owner"]
                        and row["identity"] is None
                        and row["kind"] == "compose-start"
                    ),
                )
        except (OSError, ValueError, lab.LabError, StopIteration):
            pass
        raise _OperatingSetupError(
            claimed["token"], released, cleanup_pending
        ) from error

    def accounted(record):
        if not verify_registered_docker_absent(record):
            return False
        current = lab.running_containers("/usr/bin/docker")
        present = {
            c["service"]
            for c in current
            if c["project"] == plan["project"]
            and c["service"] in selected
            and (
                c["running"]
                or (
                    c.get("status") == "exited"
                    and c.get("exit_code") == 0
                    and selected[c["service"]].get("restart") == "no"
                )
            )
        }
        if not set(plan["targets"]) <= present:
            return False
        observed = admission.observe()
        running = {
            c["service"]
            for c in current
            if c["project"] == plan["project"] and c["running"]
        }
        return set(plan["targets"]) & running <= set(observed["services"])

    return admission, claimed, accounted


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
            overlay_root,
            validate_materialized,
        )

        directory = overlay_root() / plan["fingerprint"]
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
    ]
    for name in plan["compose_files"]:
        argv += ["-f", str(root / name)]
    if overlay is not None:
        argv += ["-f", str(overlay)]
    argv += ["up", "-d", "--no-build", "--pull", "never", *plan["targets"]]
    environment = {"PATH": "/usr/bin:/bin", "HOME": "/nonexistent"}
    try:
        admission, claimed, accounted = _operating_admission(root, plan)
    except _OperatingSetupError as error:
        result = {
            "result": "START_FAILED",
            "recovery_required": not error.released,
            "cleanup_pending": error.cleanup_pending,
        }
        if not error.released:
            result["recovery_token"] = error.token
        return result
    from scripts.operations.lab import LabError

    try:
        admission.attach(
            claimed["token"], identity=None, resource_type="operating-start"
        )
        failure = None
        if runner is None:
            from scripts.lib.ops.dispatch_process import run_registered_docker

            result = run_registered_docker(
                argv,
                cwd=root,
                timeout=300,
                admission=admission,
                token=claimed["token"],
                env=environment,
            )
        else:
            result = runner(
                argv,
                cwd=root,
                env=environment,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
                timeout=300,
            )
        if result.returncode != 0:
            code = result.returncode
            failure = (
                f"controller_exit_{code}"
                if isinstance(code, int) and 0 <= code <= 255
                else "controller_failed"
            )
        if result.returncode == 0 and admission.release(
            claimed["token"], verify=accounted
        ):
            if runner is None:
                from scripts.lib.ops.dispatch_process import cleanup_registered_docker

                cleanup_pending = not cleanup_registered_docker(claimed)
            else:
                cleanup_pending = False
            return {
                "result": "STARTED",
                "recovery_required": False,
                "cleanup_pending": cleanup_pending,
            }
    except (OSError, subprocess.TimeoutExpired, ValueError, LabError):
        failure = "controller_error"
    failed = {
        "result": "START_FAILED",
        "recovery_required": True,
        "recovery_token": claimed["token"],
    }
    if failure:
        failed["failure"] = failure[:64]
    return failed


def recover_start(root, token):
    """Stop only the token-owned controller and reconcile its exact project."""
    root = _root(root)
    if not isinstance(token, str) or not re.fullmatch(r"[0-9a-f]{32}", token):
        raise ValueError("invalid_recovery_token")
    from scripts.lib.ops.dispatch_process import (
        cleanup_registered_docker,
        cleanup_unstarted_registered_docker,
        verify_registered_docker_absent,
    )
    from scripts.lib.ops.environment_admission import process_status
    from scripts.operations import lab

    try:
        admission = lab.execution_admission(root)
        matches = [row for row in admission.records() if row["token"] == token]
    except (OSError, subprocess.SubprocessError, ValueError, lab.LabError):
        return {"result": "RECOVERY_BLOCKED", "reason": "environment_unavailable"}
    if len(matches) != 1:
        return {"result": "RECOVERY_BLOCKED", "reason": "unknown_token"}
    record = matches[0]
    if (
        record["kind"] != "compose-start"
        or record["workspace_id"] != admission.workspace_id
        or record["binding_id"] != admission.binding_id
        or record["daemon_id"] != admission.daemon_id
        or not record["project"]
        or not record["services"]
    ):
        return {"result": "RECOVERY_BLOCKED", "reason": "ownership_mismatch"}
    one_shot_services = record["metadata"].get("one_shot_services")
    if (
        not isinstance(one_shot_services, list)
        or any(not isinstance(name, str) for name in one_shot_services)
        or not set(one_shot_services) <= set(record["services"])
    ):
        return {"result": "RECOVERY_BLOCKED", "reason": "service_policy_unavailable"}
    operation_dir = record["metadata"].get("docker_operation_dir")
    controller_started = bool(
        operation_dir and record["metadata"].get("docker_operation_token")
    )
    if controller_started:
        try:
            controller_stopped = verify_registered_docker_absent(record, stop=True)
        except (OSError, subprocess.SubprocessError, ValueError):
            controller_stopped = False
    else:
        # A pre-spawn failure has no controller token and can only be removed
        # after the exact owning process has exited.
        controller_stopped = process_status(record["owner"]) == "absent"
    if not controller_stopped:
        return {"result": "RECOVERY_BLOCKED", "reason": "controller_live_or_unknown"}
    if not controller_started and not cleanup_unstarted_registered_docker(record):
        return {
            "result": "RECOVERY_BLOCKED",
            "reason": "pre_controller_cleanup_unverified",
        }

    def accounted(_record):
        if controller_started and not verify_registered_docker_absent(record):
            return False
        if not controller_started and process_status(record["owner"]) != "absent":
            return False
        containers = lab.running_containers("/usr/bin/docker")
        selected = [
            item
            for item in containers
            if item["project"] == record["project"]
            and item["service"] in record["services"]
        ]
        if not selected:
            return True
        if {item["service"] for item in selected} != set(record["services"]):
            return False
        for item in selected:
            if item["running"]:
                continue
            if not (
                item.get("status") == "exited"
                and item.get("exit_code") == 0
                and item["service"] in one_shot_services
            ):
                return False
        observed = admission.observe()
        running_services = {item["service"] for item in selected if item["running"]}
        return running_services <= set(observed["services"])

    try:
        released = admission.release(token, verify=accounted)
    except (OSError, subprocess.SubprocessError, ValueError, lab.LabError):
        released = False
    if not released:
        return {"result": "RECOVERY_BLOCKED", "reason": "resources_partial_or_unknown"}
    if controller_started and not cleanup_registered_docker(record):
        return {"result": "RECOVERED", "cleanup_pending": True}
    return {"result": "RECOVERED", "cleanup_pending": False}


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
