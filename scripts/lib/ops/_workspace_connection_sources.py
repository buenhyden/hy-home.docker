"""Closed source handlers for the public workspace connection census."""

from __future__ import annotations

import json
import re
from collections.abc import Mapping
from pathlib import PurePosixPath
from urllib.parse import urlsplit

import yaml

from scripts.lib.ops._workspace_services import _InventoryLoader

NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,255}\Z")
DEFAULT = re.compile(r"\$\{[A-Za-z_][A-Za-z0-9_]*:-([^{}$]+)\}")
FILE_SECRET = re.compile(r"\$__file\{/run/secrets/([A-Za-z0-9][A-Za-z0-9_.-]{0,255})\}")
PRIVATE_PARTS = {".git", ".aws", ".ssh", "secrets", "sessions", ".agent-work"}
ALLOWED_KINDS = {
    "airflow",
    "compose",
    "grafana",
    "n8n",
    "n8n-node",
    "n8n-policy",
    "n8n-source-url",
}


class ConnectionSourceError(ValueError):
    """Fixed source diagnostic with no source value."""


class DuplicateSourceKey(ConnectionSourceError):
    pass


class _UniqueLoader(yaml.SafeLoader):
    def construct_mapping(self, node, deep=False):
        keys = [key.value for key, _ in node.value]
        if not all(isinstance(key, str) for key in keys) or len(keys) != len(set(keys)):
            raise DuplicateSourceKey("Invalid connection source.")
        return super().construct_mapping(node, deep=deep)


def candidate_kind(path: str) -> str | None:
    if path.startswith(
        "infra/06-observability/grafana/provisioning/datasources/"
    ) and path.endswith((".yml", ".yaml")):
        return "grafana"
    if (
        "/airflow/workloads/" in path
        and "/fixtures/" in path
        and "connection" in PurePosixPath(path).name
        and path.endswith(".json")
    ):
        return "airflow"
    if (
        "/n8n/workloads/" in path
        and path.endswith(".json")
        and (PurePosixPath(path).name == "workflow.json" or "/workflows/" in path)
    ):
        return "n8n"
    if "/n8n/workloads/" in path and path.endswith(".node.ts"):
        return "n8n-node"
    if "/n8n/workloads/" in path and PurePosixPath(path).name == "transport.ts":
        return "n8n-policy"
    if "/n8n/workloads/" in path and path.endswith("/hermes-plugin/tools.py"):
        return "n8n-source-url"
    if re.search(r"(?:^|/)(?:docker-)?compose[^/]*\.ya?ml\Z", path):
        return "compose"
    return None


def public_source_path(relative: str) -> bool:
    if not isinstance(relative, str):
        return False
    path = PurePosixPath(relative)
    return (
        bool(relative)
        and not path.is_absolute()
        and ".." not in path.parts
        and path.as_posix() == relative
        and not PRIVATE_PARTS.intersection(path.parts)
        and not path.name.startswith(".env")
        and path.suffix.lower() not in {".key", ".pem", ".p12", ".pfx", ".log"}
    )


def _json(raw: bytes):
    def unique(pairs):
        if len(pairs) != len({key for key, _ in pairs}):
            raise DuplicateSourceKey("Invalid connection source.")
        return dict(pairs)

    return json.loads(raw, object_pairs_hook=unique)


def _endpoint(value) -> tuple[str | None, int | None, str | None]:
    if (
        not isinstance(value, str)
        or len(value) > 2048
        or any(ord(c) < 32 for c in value)
    ):
        return None, None, "endpoint-unresolved"
    resolved = DEFAULT.sub(lambda match: match.group(1), value)
    if "$" in resolved:
        symbolic_port = re.fullmatch(
            r"(?:[A-Za-z][A-Za-z0-9+.-]*://)?([A-Za-z0-9][A-Za-z0-9_.-]{0,255}):\$\{[^{}]+\}",
            resolved,
        )
        return (
            (symbolic_port.group(1), None, "endpoint-unresolved")
            if symbolic_port
            else (None, None, "endpoint-unresolved")
        )
    parsed = urlsplit(resolved if "://" in resolved else "//" + resolved)
    if parsed.username is not None or parsed.password is not None:
        return None, None, "credential-bearing-endpoint-refused"
    if parsed.query or parsed.fragment:
        return None, None, "endpoint-query-refused"
    try:
        port = parsed.port
    except ValueError:
        return None, None, "endpoint-port-invalid"
    host = parsed.hostname
    return (
        (host, port, None)
        if host and NAME.fullmatch(host)
        else (None, None, "endpoint-unresolved")
    )


def _environment(service) -> dict[str, object]:
    environment = service.get("environment", {}) if isinstance(service, Mapping) else {}
    if isinstance(environment, Mapping):
        return {
            key: value for key, value in environment.items() if isinstance(key, str)
        }
    if isinstance(environment, list):
        result = {}
        for item in environment:
            if isinstance(item, str) and "=" in item:
                key, value = item.split("=", 1)
                if NAME.fullmatch(key):
                    result[key] = value
        return result
    return {}


def _secret_names(service) -> list[str]:
    values = service.get("secrets", []) if isinstance(service, Mapping) else []
    result = []
    for value in values if isinstance(values, list) else []:
        name = value.get("source") if isinstance(value, Mapping) else value
        if isinstance(name, str) and NAME.fullmatch(name):
            result.append(name)
    return sorted(set(result))


def _port(state="unknown", port=None):
    return {"state": state, "port": port}


def _location_state(value):
    if value == "declared":
        return "declared"
    return "absent" if value in {"absent", "unpublished", "disabled"} else "unknown"


def _declared_port(endpoint, field="port"):
    if not isinstance(endpoint, Mapping):
        return None
    port = endpoint.get(field)
    if (
        isinstance(port, Mapping)
        and port.get("state") == "declared"
        and port.get("start") == port.get("end")
    ):
        return port["start"]
    return None


def _port_contract(provider, service_port, services):
    matches = [row for row in services if row.get("service") == provider]
    match = matches[0] if len(matches) == 1 else None
    projected = match.get("ports", {}) if isinstance(match, Mapping) else {}
    result = {
        "listener": _port(_location_state(projected.get("listener", {}).get("state"))),
        "service_dns": _port("declared", service_port)
        if type(service_port) is int and 1 <= service_port <= 65535
        else _port(),
        "host_publication": _port(
            _location_state(projected.get("host_publication", {}).get("state"))
        ),
        "gateway_backend": _port(
            _location_state(projected.get("traefik_backend", {}).get("state"))
        ),
    }
    for location, source, field in (
        ("listener", "listener", "port"),
        ("host_publication", "host_publication", "published"),
        ("gateway_backend", "traefik_backend", "port"),
    ):
        endpoints = projected.get(source, {}).get("endpoints", [])
        ports = sorted(
            {
                port
                for port in (_declared_port(item, field) for item in endpoints)
                if port is not None
            }
        )
        if len(ports) == 1:
            result[location]["port"] = ports[0]
    return result


def _row(
    source,
    caller,
    provider,
    port,
    auth,
    secrets,
    disposition,
    reason,
    owner,
    level,
    services,
    suffix,
):
    return {
        "id": f"{source['path']}::{suffix}",
        "source": {"path": source["path"], "sha256": source["sha256"]},
        "caller_roles": sorted(set(caller)),
        "provider": provider,
        "port_contract": _port_contract(provider, port, services),
        "auth_kind": auth,
        "secret_refs": sorted(set(secrets)),
        "disposition": disposition,
        "reason": reason,
        "owner": owner,
        "registration": {"level": level, "actual_state": "UNKNOWN"},
    }


def _superset_database_rows(service_name, environment, secrets, source, services, gaps):
    if not service_name.startswith("superset"):
        return []
    rows = []
    declarations = (
        (
            "SUPERSET_DB_HOST",
            "SUPERSET_DB_PORT",
            "superset_db_password",
            "superset-metadata-database-source",
        ),
        (
            "PGHOST",
            "PGPORT",
            "mng_postgres_password",
            "superset-provision-database-source",
        ),
    )
    for host_key, port_key, secret_name, reason in declarations:
        if host_key not in environment and port_key not in environment:
            continue
        provider, port, error = _endpoint(
            f"{environment.get(host_key, '')}:{environment.get(port_key, '')}"
        )
        if error:
            gaps.append({"source": source["path"], "code": error})
        if provider is None:
            continue
        refs = [secret_name] if secret_name in secrets else []
        rows.append(
            _row(
                source,
                [service_name],
                provider,
                port,
                "credential-reference" if refs else "unknown",
                refs,
                "adopted",
                reason,
                "P02",
                "source-declared",
                services,
                f"{service_name}:postgres:{host_key}",
            )
        )
    return rows


def _superset_datasource_rows(service_name, service, source, services, gaps):
    if not service_name.startswith("superset"):
        return []
    command = service.get("command", []) if isinstance(service, Mapping) else []
    commands = [command] if isinstance(command, str) else command
    if not isinstance(commands, list):
        return []
    rows = []
    pattern = re.compile(
        r"\bsuperset\s+set-database-uri\s+--database_name\s+"
        r"[A-Za-z0-9_.-]+\s+--uri\s+(['\"])([^'\"\r\n]{1,2048})\1"
    )
    for index, text in enumerate(commands):
        if not isinstance(text, str) or "superset set-database-uri" not in text:
            continue
        match = pattern.search(text)
        if match is None:
            gaps.append({"source": source["path"], "code": "endpoint-unresolved"})
            continue
        parsed = urlsplit(match.group(2))
        if parsed.password is not None:
            gaps.append(
                {
                    "source": source["path"],
                    "code": "credential-bearing-endpoint-refused",
                }
            )
            continue
        if parsed.query or parsed.fragment:
            gaps.append({"source": source["path"], "code": "endpoint-query-refused"})
            continue
        try:
            port = parsed.port
        except ValueError:
            gaps.append({"source": source["path"], "code": "endpoint-port-invalid"})
            continue
        provider = parsed.hostname
        if provider is None or not NAME.fullmatch(provider):
            gaps.append({"source": source["path"], "code": "endpoint-unresolved"})
            continue
        rows.append(
            _row(
                source,
                [service_name],
                provider,
                port,
                "unknown",
                [],
                "adopted",
                "superset-datasource-registration-source",
                "P02",
                "source-declared",
                services,
                f"{service_name}:datasource:{index}",
            )
        )
    return rows


def _compose(doc, source, services, gaps):
    rows = []
    definitions = doc.get("services", {}) if isinstance(doc, Mapping) else {}
    if not isinstance(definitions, Mapping):
        return rows
    for service_name, service in sorted(definitions.items()):
        if not isinstance(service_name, str) or not isinstance(service, Mapping):
            continue
        env, secrets = _environment(service), _secret_names(service)
        for key, value in sorted(env.items()):
            match = re.fullmatch(r"RI_REDIS_HOST([0-9]+)", key)
            if match:
                index = match.group(1)
                provider, _, error = _endpoint(value)
                _, port, port_error = _endpoint(
                    f"x:{env.get('RI_REDIS_PORT' + index, '')}"
                )
                if error or port_error:
                    gaps.append({"source": source["path"], "code": error or port_error})
                if provider is None:
                    continue
                scope = provider.split("-", 1)[0]
                connection_secrets = [
                    name
                    for name in secrets
                    if scope in name and name.endswith("inspector_password")
                ]
                auth = (
                    "named-user-secret-reference"
                    if f"RI_REDIS_USERNAME{index}" in env and connection_secrets
                    else "unknown"
                )
                rows.append(
                    _row(
                        source,
                        [service_name],
                        provider,
                        port,
                        auth,
                        connection_secrets,
                        "adopted",
                        "compose-preconfigured-connection",
                        "P02",
                        "source-declared",
                        services,
                        f"{service_name}:redis:{index}",
                    )
                )
        kafka_keys = {
            "BOOTSTRAPSERVERS": "kafka",
            "SCHEMAREGISTRY": "schema-registry",
            "ADDRESS": "kafka-connect",
        }
        for key, value in sorted(env.items()):
            kind = next(
                (
                    label
                    for suffix, label in kafka_keys.items()
                    if key.startswith("KAFKA_CLUSTERS_") and key.endswith(suffix)
                ),
                None,
            )
            if kind is None:
                continue
            provider, port, error = _endpoint(value)
            if error:
                gaps.append({"source": source["path"], "code": error})
            if provider is not None:
                rows.append(
                    _row(
                        source,
                        [service_name],
                        provider,
                        port,
                        "unknown",
                        [],
                        "adopted",
                        "compose-ui-provider-declaration",
                        "P02",
                        "source-declared",
                        services,
                        f"{service_name}:{kind}:{key}",
                    )
                )
        rows.extend(
            _superset_database_rows(service_name, env, secrets, source, services, gaps)
        )
        rows.extend(
            _superset_datasource_rows(service_name, service, source, services, gaps)
        )
    return rows


def _grafana(doc, source, services, gaps):
    rows = []
    datasources = doc.get("datasources", []) if isinstance(doc, Mapping) else []
    for index, datasource in enumerate(
        datasources if isinstance(datasources, list) else []
    ):
        if not isinstance(datasource, Mapping):
            continue
        provider, port, error = _endpoint(datasource.get("url"))
        if error:
            gaps.append({"source": source["path"], "code": error})
        if provider is None:
            continue
        secure = datasource.get("secureJsonData", {})
        refs = (
            sorted(
                {
                    match.group(1)
                    for value in secure.values()
                    if isinstance(secure, Mapping) and isinstance(value, str)
                    for match in FILE_SECRET.finditer(value)
                }
            )
            if isinstance(secure, Mapping)
            else []
        )
        identity = (
            datasource.get("uid")
            if isinstance(datasource.get("uid"), str)
            and NAME.fullmatch(datasource["uid"])
            else str(index)
        )
        rows.append(
            _row(
                source,
                ["grafana"],
                provider,
                port,
                "credential-reference" if refs else "none",
                refs,
                "adopted",
                "grafana-provisioning-source",
                "P07",
                "provisioned-source",
                services,
                f"grafana:{identity}",
            )
        )
    return rows


def _airflow(doc, source, services, gaps):
    endpoint_value = (
        doc.get("endpoint_url")
        if isinstance(doc, Mapping) and "endpoint_url" in doc
        else doc.get("host")
        if isinstance(doc, Mapping)
        else None
    )
    if isinstance(doc, Mapping) and "host" in doc:
        endpoint_value = f"{endpoint_value}:{doc.get('port', '')}"
    provider, port, error = _endpoint(endpoint_value)
    if error:
        gaps.append({"source": source["path"], "code": error})
    return (
        []
        if provider is None
        else [
            _row(
                source,
                ["airflow-dag"],
                provider,
                port,
                "credential-reference",
                [],
                "deferred",
                "fixture-not-stored-registration",
                "P04",
                "fixture",
                services,
                "airflow:fixture",
            )
        ]
    )


def _n8n(doc, source, services, gaps):
    if not isinstance(doc, Mapping) or not isinstance(doc.get("nodes", []), list):
        return []
    rows = []
    for index, node in enumerate(doc["nodes"]):
        if (
            not isinstance(node, Mapping)
            or node.get("type") != "n8n-nodes-base.httpRequest"
        ):
            continue
        parameters = node.get("parameters", {})
        provider, port, error = _endpoint(
            parameters.get("url") if isinstance(parameters, Mapping) else None
        )
        if error:
            gaps.append({"source": source["path"], "code": error})
        if provider is None:
            continue
        credentials = node.get("credentials", {})
        refs = sorted(
            key
            for key in credentials
            if isinstance(credentials, Mapping)
            and isinstance(key, str)
            and NAME.fullmatch(key)
        )
        node_id = (
            node.get("id")
            if isinstance(node.get("id"), str) and NAME.fullmatch(node["id"])
            else str(index)
        )
        inactive = doc.get("active") is False
        rows.append(
            _row(
                source,
                ["n8n-workflow"],
                provider,
                port,
                "credential-reference" if refs else "unknown",
                refs,
                "deferred",
                "inactive-source-is-not-product-registration"
                if inactive
                else "workflow-source-is-not-stored-state",
                "P05",
                "inactive-workflow-source" if inactive else "source-declared",
                services,
                f"n8n:{node_id}",
            )
        )
    return rows


def _n8n_node(text, source, services, gaps):
    del gaps
    matches = sorted(
        set(
            re.findall(
                r"credentials\s*:\s*\[\{\s*name\s*:\s*['\"]([A-Za-z0-9][A-Za-z0-9_.-]{0,255})['\"]\s*,\s*required\s*:\s*true",
                text,
            )
        )
    )
    return [
        _row(
            source,
            ["n8n-custom-node"],
            None,
            None,
            "credential-reference",
            [credential],
            "deferred",
            "sdk-source-is-not-product-registration",
            "P05",
            "sdk-only",
            services,
            f"n8n-sdk:{credential}",
        )
        for credential in matches
    ]


def _n8n_policy(text, source, services, gaps):
    match = re.search(
        r"POLICY\s*=\s*Object\.freeze\(\{\s*host\s*:\s*['\"]([A-Za-z0-9][A-Za-z0-9_.-]{0,255})['\"]\s*,\s*port\s*:\s*([0-9]{1,5})",
        text,
    )
    if not match or not 1 <= int(match.group(2)) <= 65535:
        gaps.append({"source": source["path"], "code": "endpoint-unresolved"})
        return []
    return [
        _row(
            source,
            ["n8n-custom-node"],
            match.group(1),
            int(match.group(2)),
            "credential-reference",
            [],
            "deferred",
            "sdk-source-is-not-product-registration",
            "P05",
            "sdk-only",
            services,
            "n8n-sdk:policy",
        )
    ]


def _n8n_source_url(text, source, services, gaps):
    match = re.search(
        r"^WEBHOOK_URL_DEFAULT\s*=\s*['\"]([^'\"\r\n]{1,2048})['\"]\s*$",
        text,
        re.MULTILINE,
    )
    provider, port, error = _endpoint(match.group(1) if match else None)
    if error:
        gaps.append({"source": source["path"], "code": error})
    return (
        []
        if provider is None
        else [
            _row(
                source,
                ["n8n-workload-client"],
                provider,
                port,
                "unknown",
                [],
                "deferred",
                "sdk-source-is-not-product-registration",
                "P05",
                "sdk-only",
                services,
                "n8n-sdk:source-url",
            )
        ]
    )


def extract_source(kind, raw, source, services, gaps):
    try:
        if kind.startswith("n8n-"):
            return {
                "n8n-node": _n8n_node,
                "n8n-policy": _n8n_policy,
                "n8n-source-url": _n8n_source_url,
            }[kind](raw.decode("utf-8"), source, services, gaps)
        doc = (
            _json(raw)
            if source["path"].endswith(".json")
            else yaml.load(
                raw, Loader=_InventoryLoader if kind == "compose" else _UniqueLoader
            )
        )
        if not isinstance(doc, Mapping):
            raise ConnectionSourceError("Invalid connection source.")
        return {
            "compose": _compose,
            "grafana": _grafana,
            "airflow": _airflow,
            "n8n": _n8n,
        }[kind](doc, source, services, gaps)
    except DuplicateSourceKey:
        raise
    except (
        ConnectionSourceError,
        json.JSONDecodeError,
        yaml.YAMLError,
        UnicodeError,
        RecursionError,
        ValueError,
    ) as error:
        if isinstance(error, ValueError) and str(error) == "duplicate_yaml_key":
            raise DuplicateSourceKey("Invalid connection source.") from None
        raise ConnectionSourceError("Invalid connection source.") from None
