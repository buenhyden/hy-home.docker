"""Immutable ownership records for the bounded n8n native fixture."""

from __future__ import annotations

import json
import os
import re
import stat
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path

from tests.validation._opsflow_native_inputs import (
    ATTEMPT_LABEL,
    OWNER,
    OWNER_LABEL,
    ROLE_LABEL,
)

CID = re.compile(r"[0-9a-f]{64}\Z")
STATUS_ERROR_NAMES = {
    "none",
    "Error",
    "TypeError",
    "ReferenceError",
    "EvalError",
    "AbortError",
    "other",
}
STATUS_CODE_SOURCES = {"none", "cause_code", "error_code", "error_name"}
STATUS_ERROR_CODES = {
    "none",
    "connection_refused",
    "connection_reset",
    "timeout",
    "dns",
    "other",
}
STATUS_PROBE_URLS = {
    "http://127.0.0.1:5678/healthz",
    "http://127.0.0.1:5678/healthz/readiness",
    "http://127.0.0.1:5679/healthz",
    "http://mailpit:8025/readyz",
}
NODE_STATUS_PROBE_SCRIPT = r"""
const http = require('node:http');
const names = new Set(['Error', 'TypeError', 'ReferenceError', 'EvalError', 'AbortError']);
const cleanError = {name: 'none', code_source: 'none', code: 'none'};
const classifyCode = value => {
  if (value === 'ECONNREFUSED') return 'connection_refused';
  if (value === 'ECONNRESET' || value === 'UND_ERR_SOCKET') return 'connection_reset';
  if (['ETIMEDOUT', 'TimeoutError', 'AbortError', 'UND_ERR_CONNECT_TIMEOUT'].includes(value)) return 'timeout';
  if (value === 'ENOTFOUND' || value === 'EAI_AGAIN') return 'dns';
  return 'other';
};
const describe = error => {
  const name = names.has(error?.name) ? error.name : 'other';
  if (typeof error?.cause?.code === 'string') {
    return {name, code_source: 'cause_code', code: classifyCode(error.cause.code)};
  }
  if (typeof error?.code === 'string') {
    return {name, code_source: 'error_code', code: classifyCode(error.code)};
  }
  if (typeof error?.name === 'string') {
    return {name, code_source: 'error_name', code: classifyCode(error.name)};
  }
  return {name, code_source: 'none', code: 'other'};
};
const probe = url => new Promise(resolve => {
  let request;
  let settled = false;
  const finish = value => {
    if (settled) return;
    settled = true;
    clearTimeout(timer);
    resolve(value);
  };
  const timer = setTimeout(() => {
    const error = Object.assign(new Error(), {code: 'ETIMEDOUT'});
    if (request) request.destroy(error);
    finish({status: null, error: describe(error)});
  }, 2000);
  try {
    request = http.get(url, response => {
      const status = response.statusCode;
      response.destroy();
      finish({status, error: cleanError});
    });
    request.once('error', error => {
      finish({status: null, error: describe(error)});
    });
  } catch (error) {
    finish({status: null, error: describe(error)});
  }
});
Promise.all(process.argv.slice(1).map(probe))
  .then(results => process.stdout.write(JSON.stringify({results})))
  .catch(() => process.exit(3));
""".strip()


@dataclass(frozen=True)
class Container:
    cid: str
    name: str
    role: str
    generation: int
    image_id: str
    image_ref: str
    user: str
    networks: tuple[str, ...]
    mounts: tuple[str, ...]
    cap_add: tuple[str, ...]


@dataclass(frozen=True)
class Network:
    network_id: str
    name: str


@dataclass(frozen=True)
class PendingContainer:
    name: str
    role: str
    generation: int
    image_id: str
    image_ref: str
    user: str
    networks: tuple[str, ...]
    mounts: tuple[str, ...]
    cap_add: tuple[str, ...]


@dataclass(frozen=True)
class PendingNetwork:
    name: str
    role: str


@dataclass(frozen=True)
class ContainerAbsenceObservation:
    absent: bool
    present: int
    exact_absent: int
    unknown: int


def unique_identity(values: list[str]) -> str | None:
    """Return one exact full identity, rejecting ambiguity and malformed output."""
    candidates = [value for value in values if value]
    if any(not CID.fullmatch(value) for value in candidates):
        return None
    identities = set(candidates)
    return identities.pop() if len(identities) == 1 else None


def adopt_container(pending: PendingContainer, cid: str) -> Container:
    if not CID.fullmatch(cid):
        raise ValueError("invalid container identity")
    return Container(
        cid,
        pending.name,
        pending.role,
        pending.generation,
        pending.image_id,
        pending.image_ref,
        pending.user,
        pending.networks,
        pending.mounts,
        pending.cap_add,
    )


def adopt_network(pending: PendingNetwork, network_id: str) -> Network:
    if not CID.fullmatch(network_id):
        raise ValueError("invalid network identity")
    return Network(network_id, pending.name)


def discover_container(
    client, pending: PendingContainer, attempt: str
) -> Container | None:
    found = client.run(
        "ps",
        "-aq",
        "--no-trunc",
        "--filter",
        f"name=^/{pending.name}$",
        "--filter",
        f"label={OWNER_LABEL}={OWNER}",
        "--filter",
        f"label={ATTEMPT_LABEL}={attempt}",
        "--filter",
        f"label={ROLE_LABEL}={pending.role}",
    ).split()
    if not found:
        return None
    identity = unique_identity(found)
    if identity is None:
        raise ValueError("ambiguous pending container")
    return adopt_container(pending, identity)


def discover_network(client, pending: PendingNetwork, attempt: str) -> Network | None:
    found = client.run(
        "network",
        "ls",
        "-q",
        "--no-trunc",
        "--filter",
        f"name=^{pending.name}$",
        "--filter",
        f"label={OWNER_LABEL}={OWNER}",
        "--filter",
        f"label={ATTEMPT_LABEL}={attempt}",
        "--filter",
        f"label={ROLE_LABEL}={pending.role}",
    ).split()
    if not found:
        return None
    identity = unique_identity(found)
    if identity is None:
        raise ValueError("ambiguous pending network")
    return adopt_network(pending, identity)


def network_identity_matches(
    item: dict, record: Network, role: str, attempt: str
) -> bool:
    labels = item.get("Labels") or {}
    return bool(
        item.get("Id") == record.network_id
        and item.get("Name") == record.name
        and item.get("Internal")
        and labels.get(OWNER_LABEL) == OWNER
        and labels.get(ATTEMPT_LABEL) == attempt
        and labels.get(ROLE_LABEL) == role
    )


def network_attachment_matches(
    item: dict,
    record: Container,
    networks: dict[str, Network],
    aliases: dict[str, str],
    none_network_id: str,
) -> bool:
    actual = item.get("NetworkSettings", {}).get("Networks") or {}
    network_mode = (item.get("HostConfig") or {}).get("NetworkMode")
    if record.networks:
        expected = {
            networks[role].name: networks[role].network_id for role in record.networks
        }
        if set(actual) != set(expected) or any(
            not isinstance(actual[name], dict) for name in expected
        ):
            return False
        status = (item.get("State") or {}).get("Status")
        for name, network_id in expected.items():
            endpoint = actual[name]
            if endpoint.get("Aliases") != [aliases[record.role]]:
                return False
            if status == "created":
                identity_ok = (
                    endpoint.get("NetworkID") == "" and endpoint.get("EndpointID") == ""
                )
            elif status == "running":
                identity_ok = endpoint.get("NetworkID") == network_id and bool(
                    CID.fullmatch(endpoint.get("EndpointID", ""))
                )
            elif status == "exited":
                identity_ok = (
                    endpoint.get("NetworkID") == network_id
                    and endpoint.get("EndpointID") == ""
                )
            else:
                identity_ok = False
            if not identity_ok:
                return False
        return True
    if network_mode != "none" or set(actual) != {"none"}:
        return False
    endpoint = actual["none"]
    status = (item.get("State") or {}).get("Status")
    if status == "created":
        identity_ok = (
            endpoint.get("NetworkID") == "" and endpoint.get("EndpointID") == ""
        )
    elif status == "running":
        identity_ok = endpoint.get("NetworkID") == none_network_id and bool(
            CID.fullmatch(endpoint.get("EndpointID", ""))
        )
    elif status == "exited":
        identity_ok = (
            endpoint.get("NetworkID") == none_network_id
            and endpoint.get("EndpointID") == ""
        )
    else:
        identity_ok = False
    return bool(
        CID.fullmatch(none_network_id)
        and status in {"created", "running", "exited"}
        and identity_ok
        and endpoint.get("IPAMConfig") is None
        and endpoint.get("Links") is None
        and endpoint.get("Aliases") is None
        and endpoint.get("DriverOpts") is None
        and endpoint.get("DNSNames") is None
        and endpoint.get("GwPriority") == 0
        and endpoint.get("IPPrefixLen") == 0
        and endpoint.get("GlobalIPv6PrefixLen") == 0
        and all(
            endpoint.get(key) == ""
            for key in (
                "Gateway",
                "IPAddress",
                "MacAddress",
                "IPv6Gateway",
                "GlobalIPv6Address",
            )
        )
    )


def none_network_facts(item: dict, none_network_id: str) -> dict[str, bool]:
    actual = item.get("NetworkSettings", {}).get("Networks") or {}
    endpoint = actual.get("none") or {}
    return {
        "mode_none": (item.get("HostConfig") or {}).get("NetworkMode") == "none",
        "sole_none_attachment": set(actual) == {"none"},
        "state_created": (item.get("State") or {}).get("Status") == "created",
        "state_running": (item.get("State") or {}).get("Status") == "running",
        "state_exited": (item.get("State") or {}).get("Status") == "exited",
        "state_running_or_exited": (item.get("State") or {}).get("Status")
        in {"running", "exited"},
        "network_id_empty": endpoint.get("NetworkID") == "",
        "network_id_matches_builtin": endpoint.get("NetworkID") == none_network_id,
        "endpoint_id_empty": endpoint.get("EndpointID") == "",
        "endpoint_id_valid": bool(CID.fullmatch(endpoint.get("EndpointID", ""))),
        "address_fields_empty": all(
            endpoint.get(key) == ""
            for key in (
                "Gateway",
                "IPAddress",
                "MacAddress",
                "IPv6Gateway",
                "GlobalIPv6Address",
            )
        ),
        "optional_fields_null": all(
            endpoint.get(key) is None
            for key in ("IPAMConfig", "Links", "Aliases", "DriverOpts", "DNSNames")
        ),
    }


def ordinary_network_facts(
    item: dict,
    record: Container,
    networks: dict[str, Network],
    aliases: dict[str, str],
) -> dict[str, bool]:
    raw = (item.get("NetworkSettings") or {}).get("Networks")
    actual = raw if isinstance(raw, dict) else {}
    expected = {
        networks[role].name: networks[role].network_id for role in record.networks
    }
    endpoints = (
        [actual[name] for name in expected]
        if set(actual) == set(expected)
        and all(isinstance(actual[name], dict) for name in expected)
        else []
    )
    status = (item.get("State") or {}).get("Status")
    return {
        "state_created": status == "created",
        "state_running": status == "running",
        "state_exited": status == "exited",
        "expected_keyset": set(actual) == set(expected),
        "network_ids_empty": bool(endpoints)
        and all(endpoint.get("NetworkID") == "" for endpoint in endpoints),
        "network_ids_match": bool(endpoints)
        and all(
            endpoint.get("NetworkID") == expected[name]
            for name, endpoint in zip(expected, endpoints, strict=True)
        ),
        "endpoint_ids_empty": bool(endpoints)
        and all(endpoint.get("EndpointID") == "" for endpoint in endpoints),
        "endpoint_ids_valid": bool(endpoints)
        and all(
            bool(CID.fullmatch(endpoint.get("EndpointID", "")))
            for endpoint in endpoints
        ),
        "required_aliases_present": bool(endpoints)
        and all(
            aliases[record.role] in (endpoint.get("Aliases") or [])
            for endpoint in endpoints
        ),
        "aliases_exact": bool(endpoints)
        and all(
            endpoint.get("Aliases") == [aliases[record.role]] for endpoint in endpoints
        ),
    }


def mismatch_receipt(
    failures: list[str],
    item: dict,
    record: Container,
    networks: dict[str, Network],
    aliases: dict[str, str],
    none_network_id: str,
) -> dict[str, object]:
    result: dict[str, object] = {"last_contract_mismatch": failures}
    if "network" in failures:
        if record.networks:
            result["ordinary_network_facts"] = ordinary_network_facts(
                item, record, networks, aliases
            )
        else:
            result["none_network_facts"] = none_network_facts(item, none_network_id)
    if "security" in failures:
        result["security_facts"] = security_contract_facts(
            item.get("HostConfig") or {}, record.cap_add
        )
    return result


def _chown_capabilities(values: object) -> tuple[str, ...] | None:
    if values is None:
        return ()
    if not isinstance(values, (list, tuple)) or not all(
        isinstance(value, str) for value in values
    ):
        return None
    normalized = tuple(
        "CHOWN" if value in {"CHOWN", "CAP_CHOWN"} else "" for value in values
    )
    if "" in normalized or len(normalized) != len(set(normalized)):
        return None
    return normalized


def security_contract_matches(host: dict, cap_add: tuple[str, ...]) -> bool:
    actual_caps = host.get("CapAdd")
    actual = _chown_capabilities(actual_caps)
    expected = _chown_capabilities(cap_add)
    return bool(
        host.get("CapDrop") == ["ALL"]
        and actual is not None
        and expected is not None
        and actual == expected
        and host.get("SecurityOpt") == ["no-new-privileges=true"]
    )


def security_contract_facts(host: dict, cap_add: tuple[str, ...]) -> dict[str, bool]:
    prefixed = {
        value if value.startswith("CAP_") else "CAP_" + value for value in cap_add
    }
    declared = set(cap_add)
    raw_cap_add = host.get("CapAdd")
    actual_semantic = _chown_capabilities(raw_cap_add)
    expected_semantic = _chown_capabilities(cap_add)
    return {
        "cap_drop_all_exact": host.get("CapDrop") == ["ALL"],
        "cap_add_prefixed_exact": raw_cap_add == sorted(prefixed),
        "cap_add_declared_exact": raw_cap_add == sorted(declared),
        "cap_add_semantic_exact": actual_semantic is not None
        and expected_semantic is not None
        and actual_semantic == expected_semantic,
        "security_opt_equals_exact": host.get("SecurityOpt")
        == ["no-new-privileges=true"],
        "security_opt_colon_exact": host.get("SecurityOpt")
        == ["no-new-privileges:true"],
    }


def _object(payload: str) -> dict:
    value = json.loads(payload)
    if isinstance(value, list) and len(value) == 1:
        value = value[0]
    if not isinstance(value, dict):
        raise ValueError("invalid Docker metadata")
    return value


def inspect_container_identity(client, record: Container, attempt: str) -> dict:
    result = client.run_result("inspect", record.cid)
    if result.returncode:
        raise ValueError("owned container disappeared")
    item = _object(result.stdout)
    labels = (item.get("Config") or {}).get("Labels") or {}
    if not (
        item.get("Id") == record.cid
        and item.get("Name") == "/" + record.name
        and labels.get(OWNER_LABEL) == OWNER
        and labels.get(ATTEMPT_LABEL) == attempt
        and labels.get(ROLE_LABEL) == record.role
        and labels.get("hyhome.opsflow.native-generation") == str(record.generation)
        and labels.get("hyhome.opsflow.native-image-ref") == record.image_ref
    ):
        raise ValueError("owned container metadata changed")
    return item


def exact_container_absent(result, cid: str) -> bool:
    if result.returncode == 0 and result.stdout.strip() == cid and not result.stderr:
        return False
    if (
        result.returncode == 1
        and not result.stdout.strip(" \t\r\n\v\f")
        and result.stderr.strip().casefold() == "error: no such object: " + cid
    ):
        return True
    raise ValueError("exact container absence unknown")


def wait_container_absent(
    client, cid: str, deadline: float
) -> ContainerAbsenceObservation:
    if not CID.fullmatch(cid):
        return ContainerAbsenceObservation(False, 0, 0, 0)
    field = "cleanup_deadline" if client.cleanup_deadline is not None else "deadline"
    previous = getattr(client, field)
    if type(previous) not in (int, float) or type(deadline) not in (int, float):
        return ContainerAbsenceObservation(False, 0, 0, 0)
    limit = min(previous, deadline, time.monotonic() + 5.0)
    setattr(client, field, limit)
    present = exact_absent = unknown = 0
    try:
        while time.monotonic() < limit:
            try:
                result = client.run_result("inspect", "--format", "{{.Id}}", cid)
            except subprocess.TimeoutExpired:
                unknown += 1
                return ContainerAbsenceObservation(
                    False, present, exact_absent, unknown
                )
            try:
                if exact_container_absent(result, cid):
                    exact_absent += 1
                    return ContainerAbsenceObservation(
                        True, present, exact_absent, unknown
                    )
                present += 1
            except ValueError:
                unknown += 1
            time.sleep(min(0.1, max(0.0, limit - time.monotonic())))
        return ContainerAbsenceObservation(False, present, exact_absent, unknown)
    finally:
        setattr(client, field, previous)


def request_container_removal(client, cid: str) -> None:
    try:
        client.run_result("rm", "-f", "-v", cid)
    except Exception:
        pass


def main_readiness_failure_facts(
    client, record: Container, attempt: str, retain=None
) -> dict[str, bool]:
    item: dict = {}
    try:
        item = inspect_container_identity(client, record, attempt)
        inspect_available = True
    except (ValueError, TypeError, json.JSONDecodeError):
        inspect_available = False
    try:
        result = client.run_result("logs", "--tail", "200", record.cid)
        logs_available = result.returncode == 0
        logs = result.stdout + result.stderr if logs_available else ""
        if retain is not None:
            retain(result)
    except Exception:
        logs_available, logs = False, ""
    state = item.get("State") if isinstance(item.get("State"), dict) else {}
    status, exit_code = state.get("Status"), state.get("ExitCode")
    folded_logs = logs.casefold()
    return {
        "inspect_available": inspect_available,
        "state_created": status == "created",
        "state_running": status == "running",
        "state_exited": status == "exited",
        "state_restarting": status == "restarting",
        "exit_zero": type(exit_code) is int and exit_code == 0,
        "exit_nonzero": type(exit_code) is int and exit_code != 0,
        "oom_killed": state.get("OOMKilled") is True,
        "logs_available": logs_available,
        "log_ready": "n8n ready on" in folded_logs,
        "log_migration_started": "starting migration" in folded_logs,
        "log_migration_finished": "finished migration" in folded_logs,
        "log_db_init_error": "there was an error initializing db" in folded_logs,
        "log_db_auth_error": "password authentication failed" in folded_logs,
        "log_encryption_error": any(
            text in folded_logs
            for text in ("missing encryption key", "no encryption key found")
        ),
        "log_permission_error": any(
            text in folded_logs
            for text in (
                "permission denied",
                "eacces",
                "read-only file system",
                "erofs",
            )
        ),
    }


def _strict_probe_object(pairs):
    result = {}
    for key, value in pairs:
        if not isinstance(key, str) or key in result:
            raise ValueError("duplicate or non-string probe key")
        result[key] = value
    return result


def _status_error(value) -> dict[str, str]:
    if not isinstance(value, dict) or set(value) != {"name", "code_source", "code"}:
        raise ValueError("status error shape rejected")
    name, source, code = value["name"], value["code_source"], value["code"]
    if (
        name not in STATUS_ERROR_NAMES
        or source not in STATUS_CODE_SOURCES
        or code not in STATUS_ERROR_CODES
        or (name == "none") != (source == "none" and code == "none")
    ):
        raise ValueError("status error values rejected")
    return {"name": name, "code_source": source, "code": code}


def _status_result(value) -> dict[str, object]:
    if not isinstance(value, dict) or set(value) != {"status", "error"}:
        raise ValueError("status result shape rejected")
    status, error = value["status"], _status_error(value["error"])
    if (
        status is not None and (type(status) is not int or not 100 <= status <= 599)
    ) or (status is None) == (error["code"] == "none"):
        raise ValueError("status result values rejected")
    return {"status": status, "error": error}


def _failed_status_facts(category: str, *, timed_out: bool = False) -> dict:
    return {
        "exec_exit_zero": False,
        "exec_timed_out": timed_out,
        "output_valid": False,
        "probe_error": category,
        "results": [],
    }


def node_status_probe(execute, *urls: str) -> tuple[bool, dict[str, object]]:
    if (
        not urls
        or len(urls) > 2
        or len(set(urls)) != len(urls)
        or any(url not in STATUS_PROBE_URLS for url in urls)
    ):
        return False, _failed_status_facts("target_rejected")
    try:
        result = execute("node", "-e", NODE_STATUS_PROBE_SCRIPT, *urls)
    except subprocess.TimeoutExpired:
        return False, _failed_status_facts("exec_timeout", timed_out=True)
    failed = _failed_status_facts("exec_failed")
    if (
        type(result.returncode) is not int
        or result.returncode != 0
        or not isinstance(result.stdout, str)
        or not isinstance(result.stderr, str)
        or result.stderr
        or not 0 < len(result.stdout) <= 4096
    ):
        return False, failed
    try:
        value = json.loads(result.stdout, object_pairs_hook=_strict_probe_object)
        if not isinstance(value, dict) or set(value) != {"results"}:
            raise ValueError("status probe shape rejected")
        results = value["results"]
        if not isinstance(results, list) or len(results) != len(urls):
            raise ValueError("status result count rejected")
        closed_results = [_status_result(item) for item in results]
    except (json.JSONDecodeError, TypeError, ValueError):
        return False, {
            **failed,
            "exec_exit_zero": True,
            "probe_error": "invalid_output",
        }
    facts = {
        "exec_exit_zero": True,
        "exec_timed_out": False,
        "output_valid": True,
        "probe_error": "none",
        "results": closed_results,
    }
    ready = all(
        type(item["status"]) is int
        and 200 <= item["status"] <= 299
        and item["error"]["code"] == "none"
        for item in closed_results
    )
    return ready, facts


def n8n_health_probe(execute) -> tuple[bool, dict[str, object]]:
    ready, status_facts = node_status_probe(
        execute,
        "http://127.0.0.1:5678/healthz",
        "http://127.0.0.1:5678/healthz/readiness",
    )
    results = status_facts["results"]

    def projection(index: int, prefix: str) -> dict:
        if len(results) != 2:
            return {
                f"{prefix}_status": None,
                f"{prefix}_error": status_facts["probe_error"],
                f"{prefix}_error_name": "none",
                f"{prefix}_error_source": "none",
            }
        item = results[index]
        return {
            f"{prefix}_status": item["status"],
            f"{prefix}_error": item["error"]["code"],
            f"{prefix}_error_name": item["error"]["name"],
            f"{prefix}_error_source": item["error"]["code_source"],
        }

    facts = {key: value for key, value in status_facts.items() if key != "results"}
    facts.update(projection(0, "liveness"))
    facts.update(projection(1, "readiness"))
    return ready, facts


def inspect_network_identity(client, record: Network, role: str, attempt: str) -> dict:
    result = client.run_result("network", "inspect", record.network_id)
    if result.returncode:
        raise ValueError("owned network disappeared")
    item = _object(result.stdout)
    if not network_identity_matches(item, record, role, attempt):
        raise ValueError("owned network metadata changed")
    return item


def inspect_none_network(client) -> str:
    item = _object(client.run("network", "inspect", "none"))
    network_id = item.get("Id", "")
    if not (
        CID.fullmatch(network_id)
        and item.get("Name") == "none"
        and item.get("Driver") == "null"
        and item.get("Scope") == "local"
        and item.get("Internal") is False
        and item.get("Attachable") is False
        and item.get("Ingress") is False
        and not (item.get("Labels") or {})
        and not (item.get("Options") or {})
    ):
        raise ValueError("built-in none network identity changed")
    return network_id


def sweep_attempt(client, attempt: str) -> tuple[set[str], set[str]]:
    container_ids = client.run(
        "ps", "-aq", "--no-trunc", "--filter", f"label={ATTEMPT_LABEL}={attempt}"
    ).split()
    network_ids = client.run(
        "network",
        "ls",
        "-q",
        "--no-trunc",
        "--filter",
        f"label={ATTEMPT_LABEL}={attempt}",
    ).split()
    if any(not CID.fullmatch(value) for value in container_ids + network_ids):
        raise ValueError("residual resource identity rejected")
    return set(container_ids), set(network_ids)


def consume_cidfile(path: Path, expected_uid: int) -> str | None:
    try:
        fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW)
    except FileNotFoundError:
        return None
    try:
        metadata = os.fstat(fd)
        if (
            not stat.S_ISREG(metadata.st_mode)
            or metadata.st_uid != expected_uid
            or metadata.st_nlink != 1
            or metadata.st_size > 129
        ):
            raise ValueError("container identity file metadata rejected")
        value = os.read(fd, 130).decode("ascii").strip()
    finally:
        os.close(fd)
    path.unlink()
    return value
