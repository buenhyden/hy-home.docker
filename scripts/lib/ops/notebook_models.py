"""Fail-closed local model registration for an owned Open Notebook fixture."""

from __future__ import annotations

import hashlib
import json
import os
import secrets
import stat
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit


class PolicyError(ValueError):
    """A value-free policy or runtime contract failure."""


def _require(condition: bool, message: str = "invalid_model_policy") -> None:
    if not condition:
        raise PolicyError(message)


def _mapping(value: Any) -> Mapping[str, Any]:
    _require(isinstance(value, Mapping))
    return value


def _exact_keys(value: Mapping[str, Any], expected: set[str]) -> None:
    _require(set(value) == expected)


@dataclass(frozen=True)
class ProviderPolicy:
    name: str
    credential_name: str
    base_url: str
    modalities: tuple[str, ...]

    @classmethod
    def from_document(cls, value: Any) -> ProviderPolicy:
        document = _mapping(value)
        _exact_keys(document, {"name", "credential_name", "base_url", "modalities"})
        _require(document["name"] == "ollama")
        _require(
            isinstance(document["credential_name"], str)
            and 1 <= len(document["credential_name"]) <= 80
            and all(
                ord(character) >= 0x20 and ord(character) != 0x7F
                for character in document["credential_name"]
            )
        )
        _require(document["credential_name"].strip() == document["credential_name"])
        modalities = document["modalities"]
        _require(
            isinstance(modalities, list) and modalities == ["language", "embedding"]
        )
        _require(isinstance(document["base_url"], str))
        parsed = urlsplit(document["base_url"])
        try:
            port = parsed.port
        except ValueError as error:
            raise PolicyError("invalid_model_policy") from error
        _require(
            parsed.scheme == "http"
            and parsed.hostname == "ollama"
            and port is not None
            and 1 <= port <= 65535
            and document["base_url"] == f"http://ollama:{port}"
            and not parsed.username
            and not parsed.password
            and parsed.path in {"", "/"}
            and not parsed.query
            and not parsed.fragment
        )
        return cls(
            name="ollama",
            credential_name=document["credential_name"],
            base_url=document["base_url"],
            modalities=tuple(modalities),
        )


@dataclass(frozen=True)
class DesiredModel:
    name: str
    type: str
    default: str
    dimensions: int | None = None

    @classmethod
    def from_document(cls, value: Any) -> DesiredModel:
        document = _mapping(value)
        allowed = {"name", "type", "default"}
        if document.get("type") == "embedding":
            allowed.add("dimensions")
        _exact_keys(document, allowed)
        _require(
            isinstance(document["name"], str)
            and 1 <= len(document["name"]) <= 160
            and document["name"].strip() == document["name"]
        )
        model_type = document["type"]
        default = document["default"]
        _require(
            (model_type, default) in {("language", "chat"), ("embedding", "embedding")}
        )
        dimensions = document.get("dimensions")
        if model_type == "embedding":
            _require(
                document["name"] == "embeddinggemma-2:740m"
                and type(dimensions) is int
                and dimensions == 768
            )
        else:
            _require(document["name"] == "gemma4:e2b" and dimensions is None)
        return cls(document["name"], model_type, default, dimensions)


@dataclass(frozen=True)
class ModelPolicy:
    schema_version: int
    target: str
    provider: ProviderPolicy
    models: tuple[DesiredModel, ...]

    @classmethod
    def from_document(cls, value: Any) -> ModelPolicy:
        document = _mapping(value)
        _exact_keys(document, {"schema_version", "target", "provider", "models"})
        _require(type(document["schema_version"]) is int)
        _require(document["schema_version"] == 1)
        _require(document["target"] == "owned-isolated")
        models_value = document["models"]
        _require(isinstance(models_value, list) and len(models_value) == 2)
        models = tuple(DesiredModel.from_document(item) for item in models_value)
        _require(
            {(item.type, item.default) for item in models}
            == {("language", "chat"), ("embedding", "embedding")}
        )
        _require(len({item.name.casefold() for item in models}) == 2)
        return cls(
            schema_version=1,
            target="owned-isolated",
            provider=ProviderPolicy.from_document(document["provider"]),
            models=models,
        )

    @property
    def chat(self) -> DesiredModel:
        return next(item for item in self.models if item.default == "chat")

    @property
    def embedding(self) -> DesiredModel:
        return next(item for item in self.models if item.default == "embedding")


def strict_json_loads(document: str | bytes) -> Any:
    """Decode JSON while refusing ambiguous duplicate object members."""

    def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate_json_key")
            result[key] = value
        return result

    def reject_constant(_value: str) -> None:
        raise ValueError("non_finite_json_number")

    return json.loads(
        document,
        object_pairs_hook=unique_object,
        parse_constant=reject_constant,
    )


def _require_no_symlink_parent(path: Path, message: str) -> None:
    absolute = Path(os.path.abspath(path))
    current = Path(absolute.anchor)
    for part in absolute.parent.parts[1:]:
        current = current / part
        _require(not current.is_symlink(), message)


def _file_identity(metadata: os.stat_result) -> tuple[int, ...]:
    return (
        metadata.st_dev,
        metadata.st_ino,
        metadata.st_uid,
        metadata.st_gid,
        metadata.st_nlink,
        metadata.st_mode,
        metadata.st_size,
        metadata.st_mtime_ns,
        metadata.st_ctime_ns,
    )


def load_policy(path: Path) -> tuple[ModelPolicy, str]:
    """Load one bounded regular JSON policy without following a symlink."""
    try:
        _require_no_symlink_parent(path, "policy_file_refused")
        before = path.lstat()
        _require(stat.S_ISREG(before.st_mode), "policy_file_refused")
        _require(before.st_size <= 64 * 1024, "policy_file_refused")
        flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
        descriptor = os.open(path, flags)
        try:
            after = os.fstat(descriptor)
            _require(
                _file_identity(before) == _file_identity(after),
                "policy_file_changed",
            )
            body = os.read(descriptor, 64 * 1024 + 1)
            final = os.fstat(descriptor)
            _require(
                _file_identity(after) == _file_identity(final)
                and len(body) == final.st_size,
                "policy_file_changed",
            )
        finally:
            os.close(descriptor)
        _require(len(body) <= 64 * 1024, "policy_file_refused")
        document = strict_json_loads(body.decode("utf-8"))
    except PolicyError:
        raise
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as error:
        raise PolicyError("policy_file_invalid") from error
    return ModelPolicy.from_document(document), hashlib.sha256(body).hexdigest()


def read_password_file(path: Path) -> str:
    """Read one owner-only password; its value is never fingerprinted or returned in evidence."""

    try:
        _require_no_symlink_parent(path, "password_file_refused")
        before = path.lstat()
        _require(stat.S_ISREG(before.st_mode), "password_file_refused")
        _require(
            before.st_uid == os.getuid() and before.st_nlink == 1,
            "password_file_refused",
        )
        _require(before.st_mode & 0o077 == 0, "password_file_refused")
        _require(0 < before.st_size <= 4096, "password_file_refused")
        flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
        descriptor = os.open(path, flags)
        try:
            after = os.fstat(descriptor)
            _require(
                _file_identity(before) == _file_identity(after),
                "password_file_changed",
            )
            body = os.read(descriptor, 4097)
            final = os.fstat(descriptor)
            _require(
                _file_identity(after) == _file_identity(final)
                and final.st_nlink == 1
                and len(body) == final.st_size,
                "password_file_changed",
            )
        finally:
            os.close(descriptor)
        _require(len(body) <= 4096, "password_file_refused")
        value = body.decode("utf-8")
    except PolicyError:
        raise
    except (OSError, UnicodeError) as error:
        raise PolicyError("password_file_invalid") from error
    if value.endswith("\n"):
        value = value[:-1]
    _require(
        1 <= len(value) <= 512
        and "\n" not in value
        and "\r" not in value
        and "\x00" not in value
        and value.strip() == value,
        "password_file_invalid",
    )
    return value


def atomic_write_receipt(path: Path, document: Mapping[str, Any]) -> None:
    """Publish one value-free JSON receipt without following path symlinks."""
    temporary: Path | None = None
    try:
        parent = path.parent
        _require(path.name not in {"", ".", ".."}, "receipt_path_refused")
        _require(parent.is_dir() and not parent.is_symlink(), "receipt_path_refused")
        current = Path(path.anchor) if path.is_absolute() else Path(".")
        parent_parts = parent.parts[1:] if path.is_absolute() else parent.parts
        for part in parent_parts:
            current = current / part
            _require(not current.is_symlink(), "receipt_path_refused")
        if path.exists() or path.is_symlink():
            current_state = path.lstat()
            _require(stat.S_ISREG(current_state.st_mode), "receipt_path_refused")
        body = (
            json.dumps(document, ensure_ascii=True, indent=2, sort_keys=True).encode(
                "utf-8"
            )
            + b"\n"
        )
        _require(len(body) <= 1024 * 1024, "receipt_too_large")
        temporary = parent / f".{path.name}.{os.getpid()}.{secrets.token_hex(8)}.tmp"
        descriptor = os.open(
            temporary,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
            0o600,
        )
        try:
            offset = 0
            while offset < len(body):
                written = os.write(descriptor, body[offset:])
                _require(written > 0, "receipt_write_failed")
                offset += written
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
        os.replace(temporary, path)
        temporary = None
    except PolicyError:
        raise
    except (OSError, TypeError, ValueError) as error:
        raise PolicyError("receipt_write_failed") from error
    finally:
        if temporary is not None:
            try:
                temporary.unlink(missing_ok=True)
            except OSError:
                pass


@dataclass(frozen=True)
class _Snapshot:
    credentials: tuple[Mapping[str, Any], ...]
    models: tuple[Mapping[str, Any], ...]
    defaults: Mapping[str, str | None]


@dataclass(frozen=True)
class _Analysis:
    actions: tuple[str, ...]
    credential_id: str | None
    chat_id: str | None
    embedding_id: str | None


def _safe_id(value: Any, prefix: str) -> str:
    _require(
        isinstance(value, str) and value.startswith(prefix + ":"), "api_shape_invalid"
    )
    suffix = value[len(prefix) + 1 :]
    _require(
        1 <= len(suffix) <= 160
        and all(
            character.isascii() and (character.isalnum() or character in "_-")
            for character in suffix
        ),
        "api_shape_invalid",
    )
    return value


def _snapshot(client: Any) -> _Snapshot:
    credentials = client.get("/api/credentials?provider=ollama")
    models = client.get("/api/models")
    defaults = client.get("/api/models/defaults")
    _require(isinstance(credentials, list), "api_shape_invalid")
    _require(isinstance(models, list), "api_shape_invalid")
    _require(isinstance(defaults, Mapping), "api_shape_invalid")
    checked_credentials = []
    for row in credentials:
        _require(isinstance(row, Mapping), "api_shape_invalid")
        _safe_id(row.get("id"), "credential")
        _require(
            isinstance(row.get("name"), str)
            and isinstance(row.get("provider"), str)
            and isinstance(row.get("modalities"), list)
            and all(isinstance(item, str) for item in row["modalities"])
            and (row.get("base_url") is None or isinstance(row.get("base_url"), str)),
            "api_shape_invalid",
        )
        checked_credentials.append(dict(row))
    checked_models = []
    for row in models:
        _require(isinstance(row, Mapping), "api_shape_invalid")
        _safe_id(row.get("id"), "model")
        _require(
            isinstance(row.get("name"), str)
            and isinstance(row.get("provider"), str)
            and isinstance(row.get("type"), str)
            and (
                row.get("credential") is None or isinstance(row.get("credential"), str)
            ),
            "api_shape_invalid",
        )
        checked_models.append(dict(row))
    checked_defaults: dict[str, str | None] = {}
    for key, value in defaults.items():
        _require(isinstance(key, str), "api_shape_invalid")
        _require(value is None or isinstance(value, str), "api_shape_invalid")
        checked_defaults[key] = value
    return _Snapshot(
        credentials=tuple(checked_credentials),
        models=tuple(checked_models),
        defaults=checked_defaults,
    )


def _analyze(policy: ModelPolicy, state: _Snapshot) -> _Analysis:
    named = [
        row
        for row in state.credentials
        if row["provider"].casefold() == policy.provider.name
        and row["name"] == policy.provider.credential_name
    ]
    _require(
        all(row["provider"] == policy.provider.name for row in named),
        "credential_conflict",
    )
    exact = [
        row
        for row in named
        if row.get("base_url") == policy.provider.base_url
        and len(row["modalities"]) == len(policy.provider.modalities)
        and set(row["modalities"]) == set(policy.provider.modalities)
    ]
    _require(len(named) == len(exact), "credential_conflict")
    _require(len(exact) <= 1, "credential_duplicate")
    credential_id = _safe_id(exact[0]["id"], "credential") if exact else None

    model_ids: dict[str, str | None] = {"chat": None, "embedding": None}
    for desired in policy.models:
        matches = [
            row
            for row in state.models
            if row["provider"].casefold() == policy.provider.name
            and row["name"].casefold() == desired.name.casefold()
            and row["type"].casefold() == desired.type
        ]
        _require(
            all(
                row["provider"] == policy.provider.name
                and row["name"] == desired.name
                and row["type"] == desired.type
                for row in matches
            ),
            "model_conflict",
        )
        _require(len(matches) <= 1, "model_duplicate")
        if matches:
            _require(
                credential_id is not None
                and matches[0].get("credential") == credential_id,
                "model_credential_conflict",
            )
            model_ids[desired.default] = _safe_id(matches[0]["id"], "model")

    actions: list[str] = []
    if credential_id is None:
        _require(not any(model_ids.values()), "model_credential_conflict")
        actions.append("create_credential")
    if any(value is None for value in model_ids.values()):
        actions.append("register_models")
    if (
        model_ids["chat"] is None
        or model_ids["embedding"] is None
        or state.defaults.get("default_chat_model") != model_ids["chat"]
        or state.defaults.get("default_embedding_model") != model_ids["embedding"]
    ):
        actions.append("set_defaults")
    return _Analysis(
        actions=tuple(actions),
        credential_id=credential_id,
        chat_id=model_ids["chat"],
        embedding_id=model_ids["embedding"],
    )


def _receipt(
    policy: ModelPolicy,
    mode: str,
    result: str,
    policy_sha256: str,
    actions: tuple[str, ...],
) -> dict[str, Any]:
    _require(
        len(policy_sha256) == 64
        and all(character in "0123456789abcdef" for character in policy_sha256),
        "policy_fingerprint_invalid",
    )
    return {
        "schema_version": 1,
        "result": result,
        "mode": mode,
        "target": "owned-isolated",
        "target_api_contract_version": "1.15.0",
        "api_version_observed": False,
        "policy_sha256": policy_sha256,
        "credential_input": {"kind": "protected_file", "hashed": False},
        "actions": list(actions),
        "evidence": {
            "provider": "ollama",
            "provider_base_url": policy.provider.base_url,
            "chat_model": policy.chat.name,
            "embedding_model": policy.embedding.name,
            "embedding_dimensions_policy": policy.embedding.dimensions,
            "association_read_back": not actions,
            "optional_defaults_preserved": True,
            "live_inference_claimed": False,
            "caller_asserted_owned_isolated": mode == "apply",
            "authorization_proven": False,
        },
    }


def plan_policy(policy: ModelPolicy, client: Any, policy_sha256: str) -> dict[str, Any]:
    analysis = _analyze(policy, _snapshot(client))
    result = "NO_CHANGE" if not analysis.actions else "CHANGE_REQUIRED"
    return _receipt(policy, "plan", result, policy_sha256, analysis.actions)


def verify_policy(
    policy: ModelPolicy, client: Any, policy_sha256: str
) -> dict[str, Any]:
    analysis = _analyze(policy, _snapshot(client))
    _require(not analysis.actions, "verification_failed")
    return _receipt(policy, "verify", "PASS", policy_sha256, analysis.actions)


def apply_policy(
    policy: ModelPolicy,
    client: Any,
    policy_sha256: str,
    *,
    owned_isolated: bool,
) -> dict[str, Any]:
    _require(
        owned_isolated and policy.target == "owned-isolated", "apply_boundary_refused"
    )
    initial_state = _snapshot(client)
    initial = _analyze(policy, initial_state)
    if "create_credential" in initial.actions:
        response = client.post(
            "/api/credentials",
            {
                "name": policy.provider.credential_name,
                "provider": policy.provider.name,
                "modalities": list(policy.provider.modalities),
                "base_url": policy.provider.base_url,
            },
        )
        _require(isinstance(response, Mapping), "api_shape_invalid")
    after_credential = _analyze(policy, _snapshot(client))
    if "register_models" in after_credential.actions:
        _require(after_credential.credential_id is not None, "credential_missing")
        response = client.post(
            f"/api/credentials/{after_credential.credential_id}/register-models",
            {
                "models": [
                    {
                        "name": model.name,
                        "provider": policy.provider.name,
                        "model_type": model.type,
                    }
                    for model in policy.models
                ]
            },
        )
        _require(isinstance(response, Mapping), "api_shape_invalid")
    after_models = _analyze(policy, _snapshot(client))
    if "set_defaults" in after_models.actions:
        _require(
            after_models.chat_id is not None and after_models.embedding_id is not None,
            "model_registration_unverified",
        )
        response = client.put(
            "/api/models/defaults",
            {
                "default_chat_model": after_models.chat_id,
                "default_embedding_model": after_models.embedding_id,
            },
        )
        _require(isinstance(response, Mapping), "api_shape_invalid")
    final_state = _snapshot(client)
    final = _analyze(policy, final_state)
    _require(not final.actions, "verification_failed")
    managed_defaults = {"default_chat_model", "default_embedding_model"}
    initial_optional = {
        key: value
        for key, value in initial_state.defaults.items()
        if key not in managed_defaults
    }
    final_optional = {
        key: value
        for key, value in final_state.defaults.items()
        if key not in managed_defaults
    }
    _require(initial_optional == final_optional, "optional_defaults_changed")
    receipt = _receipt(policy, "apply", "PASS", policy_sha256, initial.actions)
    receipt["evidence"] = {**receipt["evidence"], "association_read_back": True}
    return receipt
