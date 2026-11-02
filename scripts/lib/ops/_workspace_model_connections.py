"""Closed P03 model and runner connection extractors.

The caller supplies the shared endpoint and row builders so this module can stay
focused on exact, public source shapes without creating a second inventory
schema.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any
from urllib.parse import urlsplit

MODEL_POLICY_PATH = "tests/fixtures/p03_models/notebook-model-policy.json"


def _networks(service: object) -> set[str]:
    if not isinstance(service, Mapping):
        return set()
    networks = service.get("networks", {})
    if isinstance(networks, Mapping):
        return {name for name in networks if isinstance(name, str)}
    if isinstance(networks, list):
        return {name for name in networks if isinstance(name, str)}
    return set()


def _endpoint_row(
    *,
    service_name: str,
    provider_value: object,
    source: dict[str, str],
    services: list[dict[str, Any]],
    gaps: list[dict[str, str]],
    endpoint: Callable[[object], tuple[str | None, int | None, str | None]],
    row: Callable[..., dict[str, Any]],
    auth: str,
    secrets: list[str],
    disposition: str,
    reason: str,
    owner: str,
    level: str,
    suffix: str,
) -> list[dict[str, Any]]:
    provider, port, error = endpoint(provider_value)
    if error:
        gaps.append({"source": source["path"], "code": error})
    if provider is None:
        return []
    return [
        row(
            source,
            [service_name],
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
        )
    ]


def compose_rows(
    doc: Mapping[str, Any],
    source: dict[str, str],
    services: list[dict[str, Any]],
    gaps: list[dict[str, str]],
    *,
    endpoint: Callable[[object], tuple[str | None, int | None, str | None]],
    environment: Callable[[object], dict[str, object]],
    secret_names: Callable[[object], list[str]],
    row: Callable[..., dict[str, Any]],
) -> list[dict[str, Any]]:
    """Extract P03 rows only from the exact tracked public source locations."""
    definitions = doc.get("services", {})
    if not isinstance(definitions, Mapping):
        return []
    path = source["path"]
    rows: list[dict[str, Any]] = []

    if path == "infra/08-ai/open-webui/docker-compose.yml":
        service = definitions.get("open-webui")
        env = environment(service)
        if "OLLAMA_BASE_URL" in env:
            rows.extend(
                _endpoint_row(
                    service_name="open-webui",
                    provider_value=env["OLLAMA_BASE_URL"],
                    source=source,
                    services=services,
                    gaps=gaps,
                    endpoint=endpoint,
                    row=row,
                    auth="none",
                    secrets=[],
                    disposition="adopted",
                    reason="local-model-provider-source",
                    owner="P03",
                    level="source-declared",
                    suffix="p03:open-webui:ollama",
                )
            )

    if path == "infra/08-ai/open-notebook/docker-compose.yml":
        service = definitions.get("open_notebook")
        env = environment(service)
        refs = secret_names(service)
        for key, auth, secret_refs, disposition, reason, suffix in (
            (
                "SURREAL_URL",
                "credential-reference",
                ["surreal_db_password"] if "surreal_db_password" in refs else [],
                "adopted",
                "notebook-state-provider-source",
                "p03:open-notebook:surrealdb",
            ),
            (
                "OLLAMA_API_BASE",
                "none",
                [],
                "deferred",
                "environment-fallback-not-registration",
                "p03:open-notebook:ollama-fallback",
            ),
        ):
            if key not in env:
                continue
            rows.extend(
                _endpoint_row(
                    service_name="open_notebook",
                    provider_value=env[key],
                    source=source,
                    services=services,
                    gaps=gaps,
                    endpoint=endpoint,
                    row=row,
                    auth=auth,
                    secrets=secret_refs,
                    disposition=disposition,
                    reason=reason,
                    owner="P03",
                    level="source-declared",
                    suffix=suffix,
                )
            )

    if path == "infra/08-ai/ollama/docker-compose.yml":
        service = definitions.get("ollama-exporter")
        env = environment(service)
        if "OLLAMA_HOST" in env:
            rows.extend(
                _endpoint_row(
                    service_name="ollama-exporter",
                    provider_value=env["OLLAMA_HOST"],
                    source=source,
                    services=services,
                    gaps=gaps,
                    endpoint=endpoint,
                    row=row,
                    auth="none",
                    secrets=[],
                    disposition="adopted",
                    reason="model-observability-source",
                    owner="P07",
                    level="source-declared",
                    suffix="p03:ollama-exporter:ollama",
                )
            )

    if path == "infra/07-workflow/n8n/docker-compose.yml":
        for service_name in ("n8n-task-runner", "n8n-task-runner-worker"):
            service = definitions.get(service_name)
            env = environment(service)
            if "N8N_RUNNERS_TASK_BROKER_URI" not in env:
                continue
            refs = secret_names(service)
            rows.extend(
                _endpoint_row(
                    service_name=service_name,
                    provider_value=env["N8N_RUNNERS_TASK_BROKER_URI"],
                    source=source,
                    services=services,
                    gaps=gaps,
                    endpoint=endpoint,
                    row=row,
                    auth="credential-reference",
                    secrets=["n8n_runner_auth_token"]
                    if "n8n_runner_auth_token" in refs
                    else [],
                    disposition="adopted",
                    reason="external-runner-broker-source",
                    owner="P03",
                    level="source-declared",
                    suffix=f"p03:{service_name}:broker",
                )
            )

    if path == "infra/07-workflow/n8n/docker-compose.ollama-local.yml":
        worker = definitions.get("n8n-worker")
        ollama = definitions.get("ollama")
        networks = doc.get("networks", {})
        network = (
            networks.get("n8n_ollama_net") if isinstance(networks, Mapping) else None
        )
        if (
            "n8n_ollama_net" in _networks(worker)
            and "n8n_ollama_net" in _networks(ollama)
            and isinstance(network, Mapping)
            and network.get("internal") is True
        ):
            rows.append(
                row(
                    source,
                    ["n8n-worker"],
                    "ollama",
                    None,
                    "none",
                    [],
                    "deferred",
                    "network-reachability-not-registration",
                    "P03",
                    "source-declared",
                    services,
                    "p03:n8n-worker:ollama-overlay",
                )
            )
    return rows


def policy_rows(
    doc: Mapping[str, Any],
    source: dict[str, str],
    services: list[dict[str, Any]],
    gaps: list[dict[str, str]],
    *,
    endpoint: Callable[[object], tuple[str | None, int | None, str | None]],
    row: Callable[..., dict[str, Any]],
) -> list[dict[str, Any]]:
    """Project the owned isolated model policy without claiming registration."""
    if set(doc) != {"schema_version", "target", "provider", "models"}:
        raise ValueError("invalid model policy")
    if (
        type(doc["schema_version"]) is not int
        or doc["schema_version"] != 1
        or doc["target"] != "owned-isolated"
    ):
        raise ValueError("invalid model policy")
    provider_doc = doc["provider"]
    if not isinstance(provider_doc, Mapping) or set(provider_doc) != {
        "name",
        "credential_name",
        "base_url",
        "modalities",
    }:
        raise ValueError("invalid model policy")
    if provider_doc["name"] != "ollama" or provider_doc["modalities"] != [
        "language",
        "embedding",
    ]:
        raise ValueError("invalid model policy")
    credential_name = provider_doc["credential_name"]
    if not (
        isinstance(credential_name, str)
        and 1 <= len(credential_name) <= 80
        and credential_name.strip() == credential_name
        and all(ord(char) >= 32 and ord(char) != 127 for char in credential_name)
    ):
        raise ValueError("invalid model policy")
    base_url = provider_doc["base_url"]
    provider, port, error = endpoint(base_url)
    if error:
        gaps.append({"source": source["path"], "code": error})
    if provider is None:
        return []
    if not isinstance(base_url, str):
        raise ValueError("invalid model policy")
    parsed = urlsplit(base_url)
    try:
        parsed_port = parsed.port
    except ValueError as error:
        raise ValueError("invalid model policy") from error
    if (
        provider != provider_doc["name"]
        or parsed.scheme != "http"
        or parsed.hostname != "ollama"
        or parsed_port is None
        or not 1 <= parsed_port <= 65535
        or base_url != f"http://ollama:{parsed_port}"
        or parsed.username is not None
        or parsed.password is not None
        or parsed.path != ""
        or parsed.query
        or parsed.fragment
        or port != parsed_port
    ):
        raise ValueError("invalid model policy")
    models = doc["models"]
    if not isinstance(models, list) or len(models) != 2:
        raise ValueError("invalid model policy")
    expected = {
        ("gemma4:e2b", "language", "chat", None),
        ("embeddinggemma-2:740m", "embedding", "embedding", 768),
    }
    actual: set[tuple[object, object, object, object]] = set()
    for model in models:
        if not isinstance(model, Mapping):
            raise ValueError("invalid model policy")
        allowed = {"name", "type", "default"}
        if model.get("type") == "embedding":
            allowed.add("dimensions")
            if type(model.get("dimensions")) is not int:
                raise ValueError("invalid model policy")
        if set(model) != allowed:
            raise ValueError("invalid model policy")
        actual.add(
            (
                model.get("name"),
                model.get("type"),
                model.get("default"),
                model.get("dimensions"),
            )
        )
    if actual != expected:
        raise ValueError("invalid model policy")
    return [
        row(
            source,
            ["open-notebook"],
            provider,
            port,
            "credential-reference",
            [],
            "deferred",
            f"owned-isolated-{default}-model-policy",
            "P03",
            "fixture",
            services,
            f"p03:model-policy:{name}",
        )
        for name, _, default, _ in sorted(expected)
    ]
