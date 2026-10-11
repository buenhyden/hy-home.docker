"""Value-free four-location declaration projection; never proves listening/auth."""

from __future__ import annotations

import hashlib
import ipaddress
import json
import os
import re
import selectors
import signal
import subprocess
import tempfile
import time
from collections.abc import Mapping
from pathlib import Path, PurePosixPath

import yaml
from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

NAME = re.compile(r"[a-zA-Z0-9_][a-zA-Z0-9_.-]{0,127}")
VARIABLE = re.compile(r"\$\{[A-Za-z_][A-Za-z0-9_]*(?:(?::?[-+?])[^{}\r\n]*)?\}")
UNKNOWN = "__p03_unresolved__"
ENDPOINT_BUDGET = 16384
SOURCE_PATH = re.compile(
    r"(?:docker-compose\.yml|(?:infra|tests)/(?:[a-zA-Z0-9_-][a-zA-Z0-9_.-]*/)*[a-zA-Z0-9_-][a-zA-Z0-9_.-]*)"
)
BACKEND = re.compile(
    r"traefik\.(http|tcp|udp)\.services\.([a-zA-Z0-9_.-]+)\.loadbalancer\.server\.(port|scheme)"
)


class PortContractError(ValueError):
    """Fixed diagnostics, with no input values or raw configuration."""


def _require(condition, reason):
    if not condition:
        raise PortContractError(reason)


def _name(value):
    _require(
        isinstance(value, str) and bool(NAME.fullmatch(value)), "invalid metadata name"
    )
    return value


def _list(value):
    _require(isinstance(value, list) and len(value) <= 4096, "invalid declaration list")
    return value


def _expression(value):
    if not isinstance(value, str):
        return value
    _require(len(value) <= 4096, "declaration too long")
    result = VARIABLE.sub(UNKNOWN, value)
    _require(
        "$" not in result and "{" not in result and "}" not in result,
        "invalid expression",
    )
    return result


def _resolved_name(value):
    transformed = _expression(value)
    if transformed is None or (isinstance(transformed, str) and UNKNOWN in transformed):
        return None
    return _name(transformed)


def _port(value, automatic=False):
    if isinstance(value, str) and UNKNOWN in value:
        return {"state": "unknown"}
    if automatic and (
        value is None
        or value == ""
        or (type(value) in (int, str) and str(value) == "0")
    ):
        return {"state": "automatic"}
    _require(type(value) in (int, str), "invalid port")
    match = re.fullmatch(r"([0-9]{1,5})(?:-([0-9]{1,5}))?", str(value))
    _require(match is not None, "invalid port")
    start, end = int(match[1]), int(match[2] or match[1])
    _require(1 <= start <= end <= 65535, "invalid port range")
    return {"state": "declared", "start": start, "end": end}


def _ip(value):
    if value is None or (isinstance(value, str) and UNKNOWN in value):
        return None
    _require(isinstance(value, str) and "%" not in value, "invalid IP")
    try:
        return str(ipaddress.ip_address(value))
    except ValueError:
        raise PortContractError("invalid IP") from None


def _split_short(value):
    _require(type(value) in (int, str), "invalid port declaration")
    text = _expression(str(value))
    body, separator, protocol = text.partition("/")
    protocol = protocol if separator else "tcp"
    _require(protocol in {"tcp", "udp"}, "invalid protocol")
    host_ip = None
    if body.startswith("["):
        match = re.fullmatch(r"\[([^\]]+)\]:([^:]*):([^:]+)", body)
        _require(match is not None, "invalid IPv6 publication")
        host_ip, published, target = match.groups()
        _require(":" in host_ip, "invalid IPv6 publication")
    else:
        fields = body.split(":")
        _require(1 <= len(fields) <= 3, "invalid short publication")
        target = fields[-1]
        published = fields[-2] if len(fields) > 1 else None
        host_ip = fields[0] if len(fields) == 3 else None
    return host_ip, published, target, protocol


def parse_port(value):
    """Preserve short paired ranges vs long available host pools/ephemeral ports."""
    long = isinstance(value, Mapping)
    mode = None
    if long:
        allowed = {
            "target",
            "published",
            "host_ip",
            "protocol",
            "mode",
            "name",
            "app_protocol",
        }
        _require(
            set(value) <= allowed and "target" in value, "invalid long publication"
        )
        for key in ("name", "app_protocol"):
            if key in value:
                _require(
                    isinstance(value[key], str) and len(value[key]) <= 4096,
                    "invalid port description",
                )
        target, published = (_expression(value.get(k)) for k in ("target", "published"))
        host_ip = _expression(value.get("host_ip"))
        protocol, mode = value.get("protocol", "tcp"), value.get("mode")
        _require(mode in {None, "host", "ingress"}, "invalid publication mode")
    else:
        host_ip, published, target, protocol = _split_short(value)
    _require(protocol in {"tcp", "udp"}, "invalid protocol")
    target, published = _port(target), _port(published, automatic=True)
    allocation = "single"
    if published["state"] == "automatic":
        allocation = "automatic"
    elif target["state"] == "unknown" or published["state"] == "unknown":
        allocation = "unknown"
    elif long and published["end"] > published["start"]:
        allocation = "pool"
    elif not long:
        _require(
            target["end"] - target["start"] == published["end"] - published["start"],
            "unequal short ranges",
        )
        if target["end"] > target["start"]:
            allocation = "paired-range"
    return {
        "host_ip": _ip(host_ip),
        "host_ip_state": "absent"
        if host_ip is None
        else ("unknown" if UNKNOWN in str(host_ip) else "declared"),
        "published": published,
        "target": target,
        "protocol": protocol,
        "mode": mode,
        "allocation": allocation,
    }


def _expose(value):
    _require(type(value) in (int, str), "invalid exposed port")
    body, separator, protocol = str(_expression(value)).partition("/")
    protocol = protocol if separator else "tcp"
    _require(protocol in {"tcp", "udp"}, "invalid protocol")
    return {"port": _port(body), "protocol": protocol}


def _unique(rows):
    # Fresh objects; no caller-owned input is mutated.
    return [
        json.loads(value)
        for value in sorted({json.dumps(r, sort_keys=True) for r in rows})
    ]


def _networks(service, definitions):
    mode = service.get("network_mode")
    if mode is not None:
        _require(isinstance(mode, str), "invalid network mode")
        _require(not service.get("networks"), "mixed network modes")
        if mode in {"host", "none"}:
            _require(
                mode != "host" or not service.get("ports"), "host network publication"
            )
            return "absent", []
        _require(
            mode.startswith(("service:", "container:")) or _expression(mode) == UNKNOWN,
            "unsupported network mode",
        )
        return "unknown", []
    networks = service.get("networks", {"default": None})
    if isinstance(networks, list):
        networks = dict.fromkeys(_list(networks))
    _require(
        isinstance(networks, Mapping) and len(networks) <= 4096, "invalid networks"
    )
    result = []
    for logical, config in networks.items():
        _name(logical)
        _require(
            config is None or isinstance(config, Mapping), "invalid network attachment"
        )
        definition = definitions.get(logical)
        definition = {} if definition is None else definition
        _require(isinstance(definition, Mapping), "invalid network definition")
        actual = _resolved_name(
            definition.get(
                "name", logical if definition.get("external") is True else None
            )
        )
        raw_aliases = _list((config or {}).get("aliases", []))
        _require(all(isinstance(a, str) for a in raw_aliases), "invalid alias")
        aliases = [_resolved_name(alias) for alias in raw_aliases]
        result.append({"logical": logical, "name": actual, "aliases": aliases})
    state = "declared" if result else "absent"
    if any(n["name"] is None or None in n["aliases"] for n in result):
        state = "unknown"
    return state, result


def _labels(value):
    if isinstance(value, list):
        pairs = []
        for item in _list(value):
            _require(isinstance(item, str) and "=" in item, "invalid label list")
            pairs.append(item.split("=", 1))
        _require(len({k for k, _ in pairs}) == len(pairs), "duplicate label")
        value = dict(pairs)
    _require(
        isinstance(value, Mapping)
        and len(value) <= 4096
        and all(isinstance(k, str) for k in value),
        "invalid labels",
    )
    return value


def _backends(service, networks):
    labels = _labels(service.get("labels", {}))
    enabled = labels.get("traefik.enable")
    enabled = str(enabled).lower() if enabled is not None else None
    _require(
        enabled in {None, "true", "false"} or _expression(enabled) == UNKNOWN,
        "invalid gateway enablement",
    )
    selected = _resolved_name(labels.get("traefik.docker.network"))
    attached = {n["name"] for n in networks if n["name"] is not None}
    mismatch = selected is not None and selected not in attached
    unresolved = mismatch and any(n["name"] is None for n in networks)
    endpoints = []
    for key, value in labels.items():
        match = BACKEND.fullmatch(key)
        if not match or match[3] != "port":
            continue
        kind, name, _ = match.groups()
        scheme = labels.get(key.removesuffix("port") + "scheme")
        _require(scheme in {None, "http", "https", "h2c"}, "invalid backend scheme")
        endpoints.append(
            {
                "kind": kind,
                "name": _name(name),
                "network": selected,
                "network_state": "absent"
                if labels.get("traefik.docker.network") is None
                else ("unknown" if selected is None else "declared"),
                "port": _port(_expression(value)),
                "scheme": scheme,
            }
        )
    state = "disabled" if enabled == "false" else "unknown"
    if enabled == "true" and endpoints and selected and not mismatch:
        state = "declared"
    gaps = (
        ["backend-network-unresolved" if unresolved else "backend-network-unattached"]
        if mismatch
        else []
    )
    return {"state": state, "endpoints": _unique(endpoints)}, gaps


def project(document, *, source=None, mode="source"):
    """Project only allowed endpoint metadata from a parsed Compose document.

    Configured ports are declarations, not observations. No filesystem,
    environment, network, Docker or secret access occurs in this function.
    """
    _require(isinstance(document, Mapping), "invalid document")
    services, definitions = document.get("services"), document.get("networks", {})
    _require(
        isinstance(services, Mapping) and len(services) <= 4096, "invalid services"
    )
    _require(
        isinstance(definitions, Mapping) and len(definitions) <= 4096,
        "invalid networks",
    )
    _require(mode in {"source", "synthetic-render"}, "invalid source mode")
    for name in services:
        _name(name)
    rows = []
    endpoint_count = 0
    for name, service in sorted(services.items()):
        _name(name)
        _require(isinstance(service, Mapping), "invalid service")
        publications = _unique([parse_port(p) for p in _list(service.get("ports", []))])
        exposed = _unique(
            [_expose(p) for p in _list(service.get("expose", []))]
            + [{"port": p["target"], "protocol": p["protocol"]} for p in publications]
        )
        if not exposed:
            exposed = [{"port": {"state": "unknown"}, "protocol": "tcp"}]
        network_state, networks = _networks(service, definitions)
        _require(
            sum(1 + len(n["aliases"]) for n in networks) * len(exposed) <= 4096,
            "DNS endpoint bound",
        )
        gateway, gaps = _backends(service, networks)
        endpoint_count += (
            len(publications)
            + len(gateway["endpoints"])
            + sum(1 + len(n["aliases"]) for n in networks) * len(exposed)
        )
        _require(endpoint_count <= ENDPOINT_BUDGET, "document endpoint bound")
        dns = [
            {
                "network_key": n["logical"],
                "network": n["name"],
                "name": alias,
                "alias_index": index,
                **p,
            }
            for n in networks
            for alias, index in [
                (name, None),
                *[(a, i) for i, a in enumerate(n["aliases"])],
            ]
            for p in exposed
        ]
        rows.append(
            {
                "service": name,
                "listener": {"state": "unknown", "endpoints": []},
                "internal_dns": {"state": network_state, "endpoints": _unique(dns)},
                "host_publication": {
                    "state": "declared" if publications else "unpublished",
                    "endpoints": publications,
                },
                "traefik_backend": gateway,
                "gaps": gaps,
                "runtime": dict.fromkeys(
                    ("running", "healthy", "used", "recovered"), "unknown"
                ),
            }
        )
    # The CLI supplies only bounded public path/hash inputs; do not echo supplied metadata.
    if source is not None:
        _list(source)
    evidence = []
    for item in source or []:
        _require(
            isinstance(item, Mapping) and set(item) == {"path", "sha256"},
            "invalid source evidence",
        )
        _require(
            isinstance(item["path"], str)
            and SOURCE_PATH.fullmatch(item["path"]) is not None,
            "invalid source path",
        )
        path = PurePosixPath(item["path"])
        _require(
            not path.is_absolute()
            and ".." not in path.parts
            and path.parts
            and path.parts[0] in {"infra", "tests", "docker-compose.yml"},
            "invalid source path",
        )
        _require(
            re.fullmatch(r"[0-9a-f]{64}", str(item["sha256"])) is not None,
            "invalid source hash",
        )
        evidence.append({"path": path.as_posix(), "sha256": item["sha256"]})
    _require(
        len({e["path"] for e in evidence}) == len(evidence), "duplicate source evidence"
    )
    return {
        "schema_version": "1.0.0",
        "scope": "root",
        "mode": mode,
        "source": _unique(evidence),
        "services": rows,
    }


def _local_schema(schema):
    """Allow only bounded in-document references; no schema retrieval is possible."""
    _require(isinstance(schema, dict), "invalid contract schema")
    stack = [(schema, True)]
    budget = 10000
    while stack:
        node, root = stack.pop()
        budget -= 1
        _require(budget >= 0, "schema size bound")
        if isinstance(node, dict):
            if "$id" in node:
                _require(
                    root and node["$id"] == "urn:hy-home:port-contract:1.0.0",
                    "external schema identity",
                )
            for key in ("$ref", "$dynamicRef"):
                if key in node:
                    reference = node[key]
                    _require(
                        isinstance(reference, str)
                        and reference.startswith("#/")
                        and "%" not in reference,
                        "external schema reference",
                    )
                    target = schema
                    try:
                        for part in reference[2:].split("/"):
                            target = target[part.replace("~1", "/").replace("~0", "~")]
                    except (KeyError, TypeError):
                        raise PortContractError(
                            "invalid local schema reference"
                        ) from None
            stack.extend((v, False) for v in node.values())
        elif isinstance(node, list):
            stack.extend((v, False) for v in node)


def _contract_port(port, *, automatic=False):
    _require(automatic or port["state"] != "automatic", "invalid automatic endpoint")
    if port["state"] == "declared":
        _require(port["start"] <= port["end"], "invalid endpoint range")


def validate_contract(document, schema):
    """Pure schema plus semantic admission; no runtime/source truth is asserted."""
    _local_schema(schema)
    try:
        Draft202012Validator.check_schema(schema)
        valid = Draft202012Validator(schema).is_valid(document)
    except (ValueError, TypeError, RecursionError, SchemaError):
        raise PortContractError("invalid contract schema") from None
    _require(valid, "invalid port contract")
    rows = document["services"]
    _require(
        sum(
            len(r[k]["endpoints"])
            for r in rows
            for k in ("internal_dns", "host_publication", "traefik_backend")
        )
        <= ENDPOINT_BUDGET,
        "document endpoint bound",
    )
    _require(
        len({r["service"] for r in rows}) == len(rows), "duplicate contract service"
    )
    sources = document["source"]
    _require(len({s["path"] for s in sources}) == len(sources), "duplicate source path")
    for row in rows:
        for key in ("internal_dns", "host_publication", "traefik_backend"):
            endpoints = row[key]["endpoints"]
            _require(
                len({json.dumps(e, sort_keys=True) for e in endpoints})
                == len(endpoints),
                "duplicate endpoint",
            )
        dns, backend = row["internal_dns"], row["traefik_backend"]
        _require(dns["state"] != "absent" or not dns["endpoints"], "invalid DNS state")
        _require(
            dns["state"] != "declared"
            or (
                bool(dns["endpoints"])
                and all(
                    e["network"] is not None and e["name"] is not None
                    for e in dns["endpoints"]
                )
            ),
            "invalid DNS state",
        )
        _require(
            backend["state"] != "declared"
            or (
                bool(backend["endpoints"])
                and all(e["network_state"] == "declared" for e in backend["endpoints"])
            ),
            "invalid backend state",
        )
        for endpoint in (
            row["internal_dns"]["endpoints"] + row["traefik_backend"]["endpoints"]
        ):
            _contract_port(endpoint["port"])
        for endpoint in row["traefik_backend"]["endpoints"]:
            _require(
                (endpoint["network_state"] == "declared")
                == (endpoint["network"] is not None),
                "invalid backend network state",
            )
        publications = row["host_publication"]
        _require(
            (publications["state"] == "declared") == bool(publications["endpoints"]),
            "invalid publication state",
        )
        for endpoint in publications["endpoints"]:
            target, published = endpoint["target"], endpoint["published"]
            _contract_port(target)
            _contract_port(published, automatic=True)
            _ip(endpoint["host_ip"])
            _require(
                (endpoint["host_ip_state"] == "declared")
                == (endpoint["host_ip"] is not None),
                "invalid bind state",
            )
            allocation = endpoint["allocation"]
            if published["state"] == "automatic":
                valid = allocation == "automatic"
            elif "unknown" in {target["state"], published["state"]}:
                valid = allocation == "unknown"
            else:
                width = published["end"] - published["start"]
                target_width = target["end"] - target["start"]
                valid = (
                    (allocation == "single" and width == target_width == 0)
                    or (allocation == "pool" and width > 0)
                    or (allocation == "paired-range" and width == target_width > 0)
                )
            _require(valid, "invalid allocation")


def project_root(root):
    """Reuse the existing root include closure and bounded source parser."""
    from scripts.lib.document_governance.operations_catalog import (
        _ComposeLoader,
        read_bounded_regular,
    )
    from scripts.lib.supply_chain.latest_version_gate import expected_from_root

    root = Path(root)
    expected, evidence = expected_from_root(root)
    services, networks = {}, {}
    for item in evidence["input_files"]:
        raw = read_bounded_regular(root, PurePosixPath(item["path"]))
        _require(
            hashlib.sha256(raw).hexdigest() == item["sha256"], "source input changed"
        )
        doc = yaml.load(raw, Loader=_ComposeLoader) or {}
        _require(isinstance(doc, Mapping), "invalid source document")
        services.update(doc.get("services", {}))
        for name, config in doc.get("networks", {}).items():
            if name in networks:
                _require(networks[name] == config, "network source conflict")
            networks[name] = config
    _require(set(services) == set(expected), "source membership mismatch")
    return project(
        {"services": services, "networks": networks}, source=evidence["input_files"]
    )


class _SyntheticLoader(yaml.SafeLoader):
    """Synthetic inputs reject duplicate keys and all custom tags."""


def _mapping(loader, node, deep=False):
    keys = [loader.construct_object(key, deep=deep) for key, _ in node.value]
    _require(all(isinstance(k, str) for k in keys), "invalid synthetic key")
    _require(len(keys) == len(set(keys)), "duplicate synthetic key")
    return loader.construct_mapping(node, deep=deep)


_SyntheticLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _mapping
)


def _synthetic_document(raw):
    _require(isinstance(raw, bytes) and len(raw) <= 65536, "invalid synthetic bytes")
    try:
        document = yaml.load(raw, Loader=_SyntheticLoader)
    except (yaml.YAMLError, UnicodeError, RecursionError):
        raise PortContractError("invalid synthetic document") from None
    _require(
        isinstance(document, Mapping) and set(document) <= {"services", "networks"},
        "unsupported synthetic root",
    )
    _require(
        isinstance(document.get("services"), Mapping), "invalid synthetic services"
    )
    allowed = {
        "image",
        "ports",
        "expose",
        "networks",
        "network_mode",
        "labels",
        "environment",
        "profiles",
        "command",
    }
    for name, service in document["services"].items():
        _name(name)
        _require(
            isinstance(service, Mapping) and set(service) <= allowed,
            "external synthetic edge",
        )
    _require(
        isinstance(document.get("networks", {}), Mapping), "invalid synthetic networks"
    )
    for config in document.get("networks", {}).values():
        _require(
            config is None
            or (isinstance(config, Mapping) and set(config) <= {"name", "driver"}),
            "external synthetic network",
        )
    return document


def _run_config(argv, *, env, cwd):
    # Only config runs. Timeout kills the invocation-owned process group including plugin.
    process = subprocess.Popen(
        argv,
        cwd=cwd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        start_new_session=True,
    )
    try:
        stdout = bytearray()
        sizes = {process.stdout: 0, process.stderr: 0}
        deadline = time.monotonic() + 30
        with selectors.DefaultSelector() as selector:
            for pipe in sizes:
                selector.register(pipe, selectors.EVENT_READ)
            while selector.get_map():
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise subprocess.TimeoutExpired(argv, 30)
                for key, _ in selector.select(remaining):
                    chunk = os.read(key.fileobj.fileno(), 65536)
                    sizes[key.fileobj] += len(chunk)
                    _require(sizes[key.fileobj] <= 1024 * 1024, "config output bound")
                    if not chunk:
                        selector.unregister(key.fileobj)
                    elif key.fileobj is process.stdout:
                        stdout.extend(chunk)
        process.wait(timeout=max(0.001, deadline - time.monotonic()))
        return subprocess.CompletedProcess(argv, process.returncode, bytes(stdout), b"")
    finally:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.wait()
        process.stdout.close()
        process.stderr.close()


def render_synthetic(documents, environment, *, source=None):
    """Render selected public synthetic bytes in a private temporary config directory.

    No repo dotenv, mount, env_file, include, build or credential path is admitted.
    Docker Compose config is daemonless. Raw output/stderr is never returned.
    """
    _require(
        isinstance(documents, list) and 1 <= len(documents) <= 8,
        "invalid synthetic input set",
    )
    _require(
        all(isinstance(raw, bytes) for raw in documents)
        and sum(map(len, documents)) <= 65536,
        "synthetic size bound",
    )
    for raw in documents:
        _synthetic_document(raw)
    _require(
        isinstance(environment, Mapping) and len(environment) <= 64,
        "invalid synthetic environment",
    )
    for key, value in environment.items():
        _require(
            isinstance(key, str)
            and re.fullmatch(r"[A-Z][A-Z0-9_]{0,63}", key) is not None
            and not key.startswith(("COMPOSE_", "DOCKER_"))
            and key not in {"HOME", "PATH"},
            "reserved synthetic environment key",
        )
        _require(
            isinstance(value, str)
            and len(value) <= 256
            and re.fullmatch(r"[A-Za-z0-9_.:/-]*", value) is not None,
            "invalid synthetic environment value",
        )
    with tempfile.TemporaryDirectory(prefix="hy-home-p03-config-") as temp:
        directory = Path(temp)
        env_path = directory / "public.env"
        env_path.write_text(
            "".join(f"{k}={v}\n" for k, v in sorted(environment.items()))
        )
        argv = [
            "/usr/bin/docker",
            "compose",
            "--project-directory",
            temp,
            "--project-name",
            "p03-synthetic",
            "--env-file",
            str(env_path),
        ]
        for index, raw in enumerate(documents):
            path = directory / f"input-{index}.yml"
            path.write_bytes(raw)
            argv.extend(["-f", str(path)])
        argv.extend(["config", "--format", "json"])
        child_env = {
            "PATH": "/usr/bin:/bin",
            "HOME": temp,
            "DOCKER_CONFIG": str(directory / "docker-config"),
            "COMPOSE_DISABLE_ENV_FILE": "1",
        }
        try:
            result = _run_config(argv, cwd=temp, env=child_env)
            _require(
                result.returncode == 0 and len(result.stdout) <= 1024 * 1024,
                "synthetic config failed",
            )
            document = json.loads(result.stdout)
            return project(document, mode="synthetic-render", source=source)
        except (
            OSError,
            subprocess.TimeoutExpired,
            ValueError,
            TypeError,
            RecursionError,
        ):
            raise PortContractError("synthetic config failed") from None
