from __future__ import annotations

import datetime
import errno
import hashlib
import importlib.metadata
import json
import os
import pathlib
import re
import stat
import sys
from collections.abc import Mapping, Sequence

OWNER = "SPEC-0211-TSK-0003"
PLAN_NAME = "plan.json"
RESULT_NAME = "result.json"
MANIFEST_NAME = "evidence-manifest.json"
MAX_JSON_BYTES = 262_144

_IDENTITY_FIELDS = frozenset(
    {
        "event_name",
        "profile",
        "execution_context",
        "input_sha",
        "base_sha",
        "head_sha",
        "run_id",
        "run_attempt",
        "job",
    }
)
_ROW_FIELDS = frozenset(
    {
        "gate_id",
        "argv",
        "selection_reason",
        "environment_keys",
        "source",
        "tool_image_digest",
    }
)
_SOURCE_FIELDS = frozenset({"path", "sha256", "git_object", "size_bytes"})
_ARTIFACT_FIELDS = frozenset({"status", "path", "sha256", "size_bytes"})
_TOOLCHAIN_FIELDS = frozenset(
    {
        "status",
        "executables",
        "dependency_inputs",
        "installed_packages",
        "runner_image",
        "node",
    }
)
_EXECUTABLE_FIELDS = frozenset({"name", "version", "sha256"})
_INPUT_FIELDS = frozenset({"path", "sha256"})
_PACKAGE_FIELDS = frozenset({"name", "version"})
_RUNNER_IMAGE_FIELDS = frozenset(
    {"image_os", "image_version", "architecture", "image_digest"}
)
_RUNTIME_FIELDS = frozenset({"node"})
_NODE_FIELDS = frozenset({"status", "version", "sha256"})
_SHA1 = re.compile(r"[0-9a-f]{40}\Z")
_SHA256 = re.compile(r"[0-9a-f]{64}\Z")
# Registered leaves pass explicit test-module lists (80 arguments today).
_MAX_ROW_ARGV = 256
_IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,127}\Z")
_ENV_KEY = re.compile(r"[A-Z_][A-Z0-9_]{0,127}\Z")
_UTC_TIMESTAMP = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?Z\Z")
_TERMINAL_STATUSES = frozenset({"PASS", "FAIL", "ERROR"})
_CLOSED_STATUSES = frozenset({"PASS", "FAIL", "ERROR", "NOT_RUN", "BLOCKED"})
_CONTROLLER_INPUTS = (
    ".github/workflow-contract.yml",
    "scripts/requirements-controller.lock",
    "scripts/requirements-pre-commit.txt",
    "scripts/requirements.txt",
)


class EvidenceError(ValueError):
    """Raised when execution evidence cannot be written without ambiguity."""


def capture_controller_toolchain(
    root: pathlib.Path,
    environ: Mapping[str, str],
    *,
    node_selected: bool,
) -> dict[str, object]:
    """Capture the allowlisted controller identity without serializing paths or env values."""
    dependency_inputs = []
    for relative in _CONTROLLER_INPUTS:
        try:
            payload = (root / relative).read_bytes()
        except OSError as error:
            raise EvidenceError(
                f"controller dependency input is unavailable: {relative}"
            ) from error
        dependency_inputs.append(
            {"path": relative, "sha256": hashlib.sha256(payload).hexdigest()}
        )

    try:
        lock = (root / "scripts/requirements-controller.lock").read_text(
            encoding="utf-8"
        )
    except OSError as error:
        raise EvidenceError("controller lock is unavailable") from error
    locked = _active_locked_packages(lock)
    if not locked or len(locked) != len({name for name, _version in locked}):
        raise EvidenceError("locked dependency inventory is invalid")
    installed_packages = []
    for name, expected_version in locked:
        try:
            actual_version = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError as error:
            raise EvidenceError(
                f"locked dependency is not installed: {name}"
            ) from error
        if actual_version != expected_version:
            raise EvidenceError(f"installed dependency differs from lock: {name}")
        installed_packages.append({"name": name, "version": actual_version})

    runner_image = {
        "image_os": environ.get("TRUSTED_IMAGE_OS", ""),
        "image_version": environ.get("TRUSTED_IMAGE_VERSION", ""),
        "architecture": environ.get("TRUSTED_RUNNER_ARCH", ""),
        "image_digest": "NOT_AVAILABLE",
    }
    if any(not value for key, value in runner_image.items() if key != "image_digest"):
        raise EvidenceError("captured runner image identity is unavailable")
    return {
        "status": "CAPTURED",
        "executables": [
            _capture_executable(environ, name=name) for name in ("git", "python", "uv")
        ],
        "dependency_inputs": dependency_inputs,
        "installed_packages": installed_packages,
        "runner_image": runner_image,
        "node": (
            {
                "status": "SELECTED_NOT_YET_OBSERVED",
                "version": "24.22.0",
                "sha256": None,
            }
            if node_selected
            else {"status": "NOT_SELECTED", "version": None, "sha256": None}
        ),
    }


def _active_locked_packages(lock: str) -> tuple[tuple[str, str], ...]:
    packages = []
    pattern = re.compile(
        r"([a-z0-9][a-z0-9._-]*)==([^ ;\\]+)"
        r"(?: ; python_full_version < '([0-9]+(?:\.[0-9]+)+)')? \\"
    )
    for line in lock.splitlines():
        if line.startswith((" ", "#")) or not line.endswith(" \\"):
            continue
        match = pattern.fullmatch(line)
        if match is None:
            raise EvidenceError("locked dependency inventory is invalid")
        marker_version = match.group(3)
        if marker_version is not None:
            limit = tuple(int(part) for part in marker_version.split("."))
            current = tuple(sys.version_info[: len(limit)])
            if current >= limit:
                continue
        packages.append((match.group(1).replace("_", "-").lower(), match.group(2)))
    return tuple(sorted(packages))


def capture_runtime_observation(
    environ: Mapping[str, str], *, node_selected: bool
) -> dict[str, object]:
    if not node_selected:
        return {"node": {"status": "NOT_SELECTED", "version": None, "sha256": None}}
    node = _capture_executable(environ, name="node")
    return {
        "node": {
            "status": "CAPTURED",
            "version": node["version"],
            "sha256": node["sha256"],
        }
    }


def _capture_executable(environ: Mapping[str, str], *, name: str) -> dict[str, str]:
    prefix = f"TRUSTED_{name.upper()}"
    path = pathlib.Path(environ.get(f"{prefix}_PATH", ""))
    version = environ.get(f"{prefix}_VERSION", "")
    expected_sha256 = environ.get(f"{prefix}_SHA256", "")
    if (
        not path.is_absolute()
        or ".." in path.parts
        or not version
        or _SHA256.fullmatch(expected_sha256) is None
    ):
        raise EvidenceError(f"captured executable identity is invalid: {name}")
    descriptor = -1
    try:
        descriptor = os.open(path, os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW)
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode) or metadata.st_mode & (
            stat.S_IWGRP | stat.S_IWOTH
        ):
            raise OSError(
                errno.EPERM,
                f"unsafe executable mode={oct(metadata.st_mode)} "
                f"owner_is_self={metadata.st_uid == os.geteuid()}",
            )
        digest = hashlib.sha256()
        offset = 0
        while offset < metadata.st_size:
            chunk = os.pread(descriptor, min(65536, metadata.st_size - offset), offset)
            if not chunk:
                raise OSError(errno.EIO, "short executable read")
            digest.update(chunk)
            offset += len(chunk)
    except OSError as error:
        raise EvidenceError(
            f"captured executable identity is unavailable: {name} "
            f"({errno.errorcode.get(error.errno, 'unknown')}: {error.strerror})"
        ) from error
    finally:
        if descriptor >= 0:
            os.close(descriptor)
    if digest.hexdigest() != expected_sha256:
        raise EvidenceError(f"captured executable bytes changed after capture: {name}")
    return {"name": name, "version": version, "sha256": expected_sha256}


def canonical_json_bytes(document: object) -> bytes:
    try:
        payload = (
            json.dumps(
                document,
                allow_nan=False,
                ensure_ascii=True,
                separators=(",", ":"),
                sort_keys=True,
            ).encode("utf-8")
            + b"\n"
        )
    except (TypeError, ValueError) as error:
        raise EvidenceError("evidence is not canonical JSON") from error
    if len(payload) > MAX_JSON_BYTES:
        raise EvidenceError("evidence exceeds the JSON size limit")
    return payload


def _require_exact_fields(
    value: object, expected: frozenset[str], label: str
) -> Mapping[str, object]:
    if not isinstance(value, Mapping) or set(value) != expected:
        raise EvidenceError(f"{label} fields must be exactly {sorted(expected)}")
    return value


def _bounded_text(value: object, label: str, *, limit: int = 512) -> str:
    if (
        not isinstance(value, str)
        or not value
        or len(value) > limit
        or any(ord(character) < 32 or ord(character) == 127 for character in value)
    ):
        raise EvidenceError(f"{label} must be bounded printable text")
    return value


def _identifier(value: object, label: str) -> str:
    text = _bounded_text(value, label, limit=128)
    if _IDENTIFIER.fullmatch(text) is None:
        raise EvidenceError(f"{label} must be an identifier")
    return text


def _normalize_identity(identity: Mapping[str, object]) -> dict[str, str]:
    source = _require_exact_fields(identity, _IDENTITY_FIELDS, "identity")
    normalized = {
        field: _identifier(source[field], f"identity.{field}")
        for field in (
            "event_name",
            "profile",
            "execution_context",
            "run_id",
            "run_attempt",
            "job",
        )
    }
    for field in ("run_id", "run_attempt"):
        if not normalized[field].isdigit():
            raise EvidenceError(f"identity.{field} must contain digits only")
    for field in ("input_sha", "base_sha", "head_sha"):
        value = source[field]
        if field in {"base_sha", "head_sha"} and value == "NOT_AVAILABLE":
            normalized[field] = value
            continue
        if not isinstance(value, str) or _SHA1.fullmatch(value) is None:
            raise EvidenceError(f"identity.{field} must be a lowercase 40-hex digest")
        normalized[field] = value
    return {field: normalized[field] for field in sorted(normalized)}


def _empty_artifact() -> dict[str, object]:
    return {
        "path": None,
        "sha256": None,
        "size_bytes": None,
        "status": "NOT_APPLICABLE",
    }


def _normalize_artifact(artifact: object) -> dict[str, object]:
    value = _require_exact_fields(artifact, _ARTIFACT_FIELDS, "artifact")
    status_value = value["status"]
    if status_value != "CAPTURED":
        raise EvidenceError("artifact.status must be CAPTURED")
    path_text = _bounded_text(value["path"], "artifact.path", limit=512)
    path = pathlib.PurePosixPath(path_text)
    if path.is_absolute() or ".." in path.parts or path.as_posix() != path_text:
        raise EvidenceError("artifact.path must be repository-relative")
    digest = value["sha256"]
    if not isinstance(digest, str) or _SHA256.fullmatch(digest) is None:
        raise EvidenceError("artifact.sha256 must be a lowercase 64-hex digest")
    size = value["size_bytes"]
    if (
        isinstance(size, bool)
        or not isinstance(size, int)
        or not 0 <= size <= 1_073_741_824
    ):
        raise EvidenceError("artifact.size_bytes must be a bounded integer")
    return {
        "path": path_text,
        "sha256": digest,
        "size_bytes": size,
        "status": "CAPTURED",
    }


def _sha256_value(value: object, label: str) -> str:
    if not isinstance(value, str) or _SHA256.fullmatch(value) is None:
        raise EvidenceError(f"{label} must be a lowercase 64-hex digest")
    return value


def _normalize_toolchain(toolchain: Mapping[str, object] | None) -> dict[str, object]:
    if toolchain is None:
        return {"status": "NOT_CAPTURED"}
    value = _require_exact_fields(toolchain, _TOOLCHAIN_FIELDS, "toolchain")
    if value["status"] != "CAPTURED":
        raise EvidenceError("toolchain.status must be CAPTURED")
    executables = value["executables"]
    if isinstance(executables, (str, bytes)) or not isinstance(executables, Sequence):
        raise EvidenceError("toolchain.executables must be a sequence")
    normalized_executables = []
    for index, candidate in enumerate(executables):
        item = _require_exact_fields(
            candidate, _EXECUTABLE_FIELDS, f"toolchain.executables[{index}]"
        )
        normalized_executables.append(
            {
                "name": _identifier(item["name"], "toolchain executable name"),
                "sha256": _sha256_value(item["sha256"], "toolchain executable sha256"),
                "version": _bounded_text(
                    item["version"], "toolchain executable version", limit=128
                ),
            }
        )
    names = [item["name"] for item in normalized_executables]
    if names != sorted(names) or len(names) != len(set(names)):
        raise EvidenceError("toolchain executables must be sorted and unique")

    normalized_inputs = _normalize_named_hashes(
        value["dependency_inputs"], _INPUT_FIELDS, "dependency_inputs"
    )
    packages = value["installed_packages"]
    if isinstance(packages, (str, bytes)) or not isinstance(packages, Sequence):
        raise EvidenceError("toolchain.installed_packages must be a sequence")
    normalized_packages = []
    for index, candidate in enumerate(packages):
        item = _require_exact_fields(
            candidate, _PACKAGE_FIELDS, f"toolchain.installed_packages[{index}]"
        )
        normalized_packages.append(
            {
                "name": _identifier(item["name"], "installed package name"),
                "version": _bounded_text(
                    item["version"], "installed package version", limit=128
                ),
            }
        )
    package_names = [item["name"] for item in normalized_packages]
    if package_names != sorted(package_names) or len(package_names) != len(
        set(package_names)
    ):
        raise EvidenceError("installed packages must be sorted and unique")

    image = _require_exact_fields(
        value["runner_image"], _RUNNER_IMAGE_FIELDS, "toolchain.runner_image"
    )
    if image["image_digest"] != "NOT_AVAILABLE":
        raise EvidenceError("runner image digest must be NOT_AVAILABLE")
    normalized_image = {
        field: _bounded_text(image[field], f"runner_image.{field}", limit=128)
        for field in ("architecture", "image_os", "image_version")
    }
    normalized_image["image_digest"] = "NOT_AVAILABLE"
    declared_node = _require_exact_fields(value["node"], _NODE_FIELDS, "toolchain.node")
    node_status = declared_node["status"]
    if node_status == "NOT_SELECTED":
        if declared_node["version"] is not None or declared_node["sha256"] is not None:
            raise EvidenceError("unselected declared Node identity must be null")
        normalized_node = {"status": "NOT_SELECTED", "version": None, "sha256": None}
    elif node_status == "SELECTED_NOT_YET_OBSERVED":
        if declared_node["sha256"] is not None:
            raise EvidenceError("unobserved declared Node sha256 must be null")
        normalized_node = {
            "status": "SELECTED_NOT_YET_OBSERVED",
            "version": _bounded_text(
                declared_node["version"], "toolchain.node.version", limit=128
            ),
            "sha256": None,
        }
    else:
        raise EvidenceError("declared Node status is invalid")
    return {
        "dependency_inputs": normalized_inputs,
        "executables": normalized_executables,
        "installed_packages": normalized_packages,
        "runner_image": normalized_image,
        "node": normalized_node,
        "status": "CAPTURED",
    }


def _normalize_named_hashes(
    values: object,
    fields: frozenset[str],
    label: str,
) -> list[dict[str, str]]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence):
        raise EvidenceError(f"toolchain.{label} must be a sequence")
    normalized = []
    for index, candidate in enumerate(values):
        item = _require_exact_fields(candidate, fields, f"toolchain.{label}[{index}]")
        path_text = _bounded_text(item["path"], f"toolchain.{label}.path", limit=512)
        path = pathlib.PurePosixPath(path_text)
        if path.is_absolute() or ".." in path.parts or path.as_posix() != path_text:
            raise EvidenceError(f"toolchain.{label}.path must be repository-relative")
        normalized.append(
            {
                "path": path_text,
                "sha256": _sha256_value(item["sha256"], f"toolchain.{label}.sha256"),
            }
        )
    paths = [item["path"] for item in normalized]
    if paths != sorted(paths) or len(paths) != len(set(paths)):
        raise EvidenceError(f"toolchain.{label} must be sorted and unique")
    return normalized


def _normalize_runtime_observation(
    observation: Mapping[str, object] | None,
) -> dict[str, object]:
    if observation is None:
        return {"status": "NOT_CAPTURED"}
    value = _require_exact_fields(observation, _RUNTIME_FIELDS, "runtime_observation")
    node = _require_exact_fields(
        value["node"], _NODE_FIELDS, "runtime_observation.node"
    )
    status_value = node["status"]
    if status_value == "NOT_SELECTED":
        if node["version"] is not None or node["sha256"] is not None:
            raise EvidenceError("unselected Node identity must be null")
        normalized_node = {"status": "NOT_SELECTED", "version": None, "sha256": None}
    elif status_value == "CAPTURED":
        normalized_node = {
            "status": "CAPTURED",
            "version": _bounded_text(node["version"], "node.version", limit=128),
            "sha256": _sha256_value(node["sha256"], "node.sha256"),
        }
    else:
        raise EvidenceError("node status must be CAPTURED or NOT_SELECTED")
    return {"node": normalized_node, "status": "CAPTURED"}


def _normalize_source(source: object) -> dict[str, object]:
    value = _require_exact_fields(source, _SOURCE_FIELDS, "source")
    path_text = _bounded_text(value["path"], "source.path", limit=512)
    path = pathlib.PurePosixPath(path_text)
    if path.is_absolute() or ".." in path.parts or path.as_posix() != path_text:
        raise EvidenceError("source.path must be a normalized repository-relative path")
    sha256 = value["sha256"]
    git_object = value["git_object"]
    size_bytes = value["size_bytes"]
    if not isinstance(sha256, str) or _SHA256.fullmatch(sha256) is None:
        raise EvidenceError("source.sha256 must be a lowercase 64-hex digest")
    if not isinstance(git_object, str) or _SHA1.fullmatch(git_object) is None:
        raise EvidenceError("source.git_object must be a lowercase 40-hex digest")
    if (
        isinstance(size_bytes, bool)
        or not isinstance(size_bytes, int)
        or not 0 <= size_bytes <= 1_073_741_824
    ):
        raise EvidenceError("source.size_bytes must be a bounded non-negative integer")
    return {
        "git_object": git_object,
        "path": path_text,
        "sha256": sha256,
        "size_bytes": size_bytes,
    }


def _normalize_rows(rows: Sequence[Mapping[str, object]]) -> list[dict[str, object]]:
    if isinstance(rows, (str, bytes)) or not isinstance(rows, Sequence):
        raise EvidenceError("rows must be a sequence")
    if not rows or len(rows) > 2048:
        raise EvidenceError("rows must contain between 1 and 2048 gates")
    normalized: list[dict[str, object]] = []
    gate_ids: set[str] = set()
    for index, candidate in enumerate(rows):
        row = _require_exact_fields(candidate, _ROW_FIELDS, f"row[{index}]")
        gate_id = _identifier(row["gate_id"], f"row[{index}].gate_id")
        if gate_id in gate_ids:
            raise EvidenceError(f"duplicate gate id: {gate_id}")
        gate_ids.add(gate_id)

        argv = row["argv"]
        if (
            isinstance(argv, (str, bytes))
            or not isinstance(argv, Sequence)
            or not 1 <= len(argv) <= _MAX_ROW_ARGV
        ):
            observed = (
                len(argv)
                if isinstance(argv, Sequence) and not isinstance(argv, (str, bytes))
                else type(argv).__name__
            )
            raise EvidenceError(
                f"row[{index}].argv must contain 1 to {_MAX_ROW_ARGV} arguments "
                f"(gate {gate_id}: {observed})"
            )
        normalized_argv = [
            _bounded_text(argument, f"row[{index}].argv", limit=4096)
            for argument in argv
        ]

        env_keys = row["environment_keys"]
        if isinstance(env_keys, (str, bytes)) or not isinstance(env_keys, Sequence):
            raise EvidenceError(f"row[{index}].environment_keys must be a sequence")
        normalized_env: list[str] = []
        for key in env_keys:
            if not isinstance(key, str) or _ENV_KEY.fullmatch(key) is None:
                raise EvidenceError(
                    f"row[{index}].environment_keys contains an invalid key"
                )
            normalized_env.append(key)
        if len(normalized_env) != len(set(normalized_env)):
            raise EvidenceError(f"row[{index}].environment_keys contains duplicates")

        digest = row["tool_image_digest"]
        if digest != "NOT_AVAILABLE" and (
            not isinstance(digest, str)
            or not digest.startswith("sha256:")
            or _SHA256.fullmatch(digest.removeprefix("sha256:")) is None
        ):
            raise EvidenceError(
                f"row[{index}].tool_image_digest must be NOT_AVAILABLE or sha256"
            )
        normalized.append(
            {
                "argv": normalized_argv,
                "environment_keys": sorted(normalized_env),
                "gate_id": gate_id,
                "selected": True,
                "selection_reason": _bounded_text(
                    row["selection_reason"],
                    f"row[{index}].selection_reason",
                    limit=256,
                ),
                "source": _normalize_source(row["source"]),
                "status": "NOT_RUN",
                "tool_image_digest": digest,
            }
        )
    return normalized


def _expected_plan(
    identity: Mapping[str, object],
    rows: Sequence[Mapping[str, object]],
    retention_days: int,
    toolchain: Mapping[str, object] | None,
) -> dict[str, object]:
    if (
        isinstance(retention_days, bool)
        or not isinstance(retention_days, int)
        or not 1 <= retention_days <= 90
    ):
        raise EvidenceError("retention_days must be an integer from 1 through 90")
    return {
        "identity": _normalize_identity(identity),
        "owner": OWNER,
        "retention_days": retention_days,
        "rows": _normalize_rows(rows),
        "schema_version": 1,
        "toolchain": _normalize_toolchain(toolchain),
    }


def _parse_canonical(raw: bytes, label: str) -> dict[str, object]:
    def reject_duplicate(pairs: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise EvidenceError(f"{label} contains duplicate JSON keys")
            result[key] = value
        return result

    try:
        document = json.loads(raw, object_pairs_hook=reject_duplicate)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise EvidenceError(f"{label} is not valid JSON") from error
    if not isinstance(document, dict) or canonical_json_bytes(document) != raw:
        raise EvidenceError(f"{label} is not canonical JSON")
    return document


def _validate_timestamp(value: object) -> str:
    if not isinstance(value, str) or _UTC_TIMESTAMP.fullmatch(value) is None:
        raise EvidenceError("timestamp must be an RFC3339 UTC timestamp")
    try:
        datetime.datetime.fromisoformat(value.removesuffix("Z") + "+00:00")
    except ValueError as error:
        raise EvidenceError("timestamp must be an RFC3339 UTC timestamp") from error
    return value


def _validate_reason(value: object, label: str) -> str:
    return _identifier(value, label)


class EvidenceStore:
    def __init__(
        self,
        directory: pathlib.Path,
        directory_fd: int,
        plan: dict[str, object],
        plan_sha256: str,
    ) -> None:
        self.directory = directory
        self._directory_fd = directory_fd
        self._plan = plan
        self.plan_sha256 = plan_sha256
        metadata = os.fstat(directory_fd)
        self._directory_identity = (metadata.st_dev, metadata.st_ino)
        self._result_snapshot: tuple[int, int, int, int, str] | None = None
        self._result: dict[str, object] | None = None

    @classmethod
    def create(
        cls,
        directory: pathlib.Path,
        *,
        identity: Mapping[str, object],
        rows: Sequence[Mapping[str, object]],
        retention_days: int,
        toolchain: Mapping[str, object] | None = None,
    ) -> EvidenceStore:
        path = pathlib.Path(directory)
        if path.name.startswith("."):
            raise EvidenceError("evidence output directory must have a visible name")
        plan = _expected_plan(identity, rows, retention_days, toolchain)
        plan_bytes = canonical_json_bytes(plan)
        try:
            os.mkdir(path, 0o700)
        except FileExistsError as error:
            raise EvidenceError("evidence output directory already exists") from error
        except OSError as error:
            raise EvidenceError(
                f"cannot create evidence output directory: {error}"
            ) from error
        directory_fd = cls._open_directory(path)
        store = cls(path, directory_fd, plan, hashlib.sha256(plan_bytes).hexdigest())
        try:
            store._write_new(PLAN_NAME, plan_bytes)
        except BaseException:
            store.close()
            raise
        return store

    @classmethod
    def open(
        cls,
        directory: pathlib.Path,
        *,
        identity: Mapping[str, object],
        rows: Sequence[Mapping[str, object]],
        retention_days: int,
        toolchain: Mapping[str, object] | None = None,
    ) -> EvidenceStore:
        path = pathlib.Path(directory)
        expected = _expected_plan(identity, rows, retention_days, toolchain)
        directory_fd = cls._open_directory(path)
        store = cls(path, directory_fd, expected, "")
        try:
            raw, _ = store._read_file(PLAN_NAME)
            actual = _parse_canonical(raw, "execution plan")
            if actual != expected:
                raise EvidenceError(
                    "execution plan does not match the authenticated input"
                )
            store.plan_sha256 = hashlib.sha256(raw).hexdigest()
        except BaseException:
            store.close()
            raise
        return store

    @staticmethod
    def _open_directory(path: pathlib.Path) -> int:
        flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC
        try:
            descriptor = os.open(path, flags)
        except OSError as error:
            raise EvidenceError(
                "evidence output must be a private regular directory"
            ) from error
        info = os.fstat(descriptor)
        if (
            not stat.S_ISDIR(info.st_mode)
            or info.st_uid != os.geteuid()
            or stat.S_IMODE(info.st_mode) != 0o700
        ):
            os.close(descriptor)
            raise EvidenceError("evidence output directory must be owned and mode 0700")
        return descriptor

    def close(self) -> None:
        if self._directory_fd >= 0:
            os.close(self._directory_fd)
            self._directory_fd = -1

    def __enter__(self) -> EvidenceStore:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def __del__(self) -> None:
        try:
            self.close()
        except OSError:
            pass

    def _write_all(self, descriptor: int, payload: bytes) -> None:
        offset = 0
        while offset < len(payload):
            written = os.write(descriptor, payload[offset:])
            if written <= 0:
                raise EvidenceError("short evidence write")
            offset += written

    def _assert_directory_identity(self) -> None:
        try:
            path_info = self.directory.stat(follow_symlinks=False)
            descriptor_info = os.fstat(self._directory_fd)
        except OSError as error:
            raise EvidenceError("evidence directory identity changed") from error
        if (
            not stat.S_ISDIR(path_info.st_mode)
            or (path_info.st_dev, path_info.st_ino) != self._directory_identity
            or (descriptor_info.st_dev, descriptor_info.st_ino)
            != self._directory_identity
        ):
            raise EvidenceError("evidence directory identity changed")

    def _write_new(self, name: str, payload: bytes) -> None:
        self._assert_directory_identity()
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC
        try:
            descriptor = os.open(name, flags, 0o600, dir_fd=self._directory_fd)
        except FileExistsError as error:
            raise EvidenceError(f"{name} already exists") from error
        except OSError as error:
            raise EvidenceError(f"cannot create {name}: {error}") from error
        try:
            os.fchmod(descriptor, 0o600)
            self._write_all(descriptor, payload)
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
        os.fsync(self._directory_fd)

    def _read_file(self, name: str) -> tuple[bytes, tuple[int, int, int, int, str]]:
        self._assert_directory_identity()
        flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC | os.O_NONBLOCK
        try:
            descriptor = os.open(name, flags, dir_fd=self._directory_fd)
        except OSError as error:
            if error.errno in {errno.ELOOP, errno.ENOENT}:
                raise EvidenceError(f"{name} must be a regular file") from error
            raise EvidenceError(f"cannot open {name}: {error}") from error
        try:
            before = os.fstat(descriptor)
            if not stat.S_ISREG(before.st_mode):
                raise EvidenceError(f"{name} must be a regular file")
            if before.st_uid != os.geteuid():
                raise EvidenceError(f"{name} must be owned by the current user")
            if before.st_nlink != 1:
                raise EvidenceError(f"{name} must have a single link")
            if stat.S_IMODE(before.st_mode) != 0o600:
                raise EvidenceError(f"{name} must have mode 0600")
            if not 0 <= before.st_size <= MAX_JSON_BYTES:
                raise EvidenceError(f"{name} exceeds the JSON size limit")
            chunks: list[bytes] = []
            remaining = before.st_size + 1
            while remaining:
                chunk = os.read(descriptor, min(65536, remaining))
                if not chunk:
                    break
                chunks.append(chunk)
                remaining -= len(chunk)
            raw = b"".join(chunks)
            after = os.fstat(descriptor)
            if len(raw) != before.st_size or (
                before.st_dev,
                before.st_ino,
                before.st_size,
                before.st_mtime_ns,
            ) != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns):
                raise EvidenceError(f"{name} changed while it was read")
            digest = hashlib.sha256(raw).hexdigest()
            return raw, (
                after.st_dev,
                after.st_ino,
                after.st_size,
                after.st_mtime_ns,
                digest,
            )
        finally:
            os.close(descriptor)

    def _current_result(self) -> dict[str, object]:
        if self._result_snapshot is None or self._result is None:
            raise EvidenceError("execution result has not been initialized")
        raw, snapshot = self._read_file(RESULT_NAME)
        if snapshot != self._result_snapshot:
            raise EvidenceError("execution result changed since the prior update")
        document = _parse_canonical(raw, "execution result")
        if document != self._result:
            raise EvidenceError("execution result changed since the prior update")
        return document

    def initialize_result(
        self,
        *,
        runtime_observation: Mapping[str, object] | None = None,
    ) -> None:
        if self._result_snapshot is not None:
            raise EvidenceError("execution result is already initialized")
        document: dict[str, object] = {
            "complete": False,
            "owner": OWNER,
            "plan_sha256": self.plan_sha256,
            "retention_days": self._plan["retention_days"],
            "runtime_observation": _normalize_runtime_observation(runtime_observation),
            "rows": [
                {
                    "artifact": _empty_artifact(),
                    "duration_ms": None,
                    "ended_at_utc": None,
                    "exit_code": None,
                    "gate_id": row["gate_id"],
                    "reason": None,
                    "started_at_utc": None,
                    "status": "NOT_RUN",
                }
                for row in self._plan["rows"]
            ],
            "schema_version": 1,
        }
        planned_toolchain = self._plan["toolchain"]
        observed_runtime = document["runtime_observation"]
        if planned_toolchain.get("status") == "CAPTURED":
            selected = (
                planned_toolchain["node"]["status"] == "SELECTED_NOT_YET_OBSERVED"
            )
            captured = observed_runtime.get("node", {}).get("status") == "CAPTURED"
            if selected != captured:
                raise EvidenceError(
                    "Node runtime observation does not match the selected prerequisite"
                )
        self._write_new(RESULT_NAME, canonical_json_bytes(document))
        _, self._result_snapshot = self._read_file(RESULT_NAME)
        self._result = document

    def _replace_result(self, document: dict[str, object]) -> None:
        self._current_result()
        payload = canonical_json_bytes(document)
        temporary = RESULT_NAME + ".tmp"
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC
        try:
            descriptor = os.open(temporary, flags, 0o600, dir_fd=self._directory_fd)
        except FileExistsError as error:
            raise EvidenceError(
                "execution result temporary file already exists"
            ) from error
        try:
            os.fchmod(descriptor, 0o600)
            self._write_all(descriptor, payload)
            os.fsync(descriptor)
        except BaseException:
            try:
                os.unlink(temporary, dir_fd=self._directory_fd)
            except OSError:
                pass
            raise
        finally:
            os.close(descriptor)

        try:
            self._assert_directory_identity()
            _, current = self._read_file(RESULT_NAME)
            if current != self._result_snapshot:
                raise EvidenceError("execution result changed since the prior update")
            os.replace(
                temporary,
                RESULT_NAME,
                src_dir_fd=self._directory_fd,
                dst_dir_fd=self._directory_fd,
            )
            os.fsync(self._directory_fd)
        except BaseException:
            try:
                os.unlink(temporary, dir_fd=self._directory_fd)
            except OSError:
                pass
            raise
        _, self._result_snapshot = self._read_file(RESULT_NAME)
        self._result = document

    @staticmethod
    def _row(document: dict[str, object], gate_id: str) -> dict[str, object]:
        gate = _identifier(gate_id, "gate_id")
        for row in document["rows"]:
            if row["gate_id"] == gate:
                return row
        raise EvidenceError(f"gate is absent from the execution plan: {gate}")

    def mark_started(self, gate_id: str, *, started_at_utc: str) -> None:
        document = self._current_result()
        row = self._row(document, gate_id)
        if row["status"] != "NOT_RUN":
            raise EvidenceError(f"{gate_id} must be NOT_RUN before it can start")
        replacement = {
            **document,
            "rows": [
                (
                    {
                        **candidate,
                        "started_at_utc": _validate_timestamp(started_at_utc),
                        "status": "STARTED",
                    }
                    if candidate["gate_id"] == gate_id
                    else candidate
                )
                for candidate in document["rows"]
            ],
        }
        self._replace_result(replacement)

    def mark_terminal(
        self,
        gate_id: str,
        *,
        status: str,
        exit_code: int,
        ended_at_utc: str,
        duration_ms: int,
        reason: str | None = None,
        artifact: Mapping[str, object] | None = None,
    ) -> None:
        if status not in _TERMINAL_STATUSES:
            raise EvidenceError("terminal status must be PASS, FAIL, or ERROR")
        if isinstance(exit_code, bool) or not isinstance(exit_code, int):
            raise EvidenceError("exit_code must be an integer")
        if status == "PASS" and exit_code != 0:
            raise EvidenceError("PASS requires exit_code 0")
        if (
            isinstance(duration_ms, bool)
            or not isinstance(duration_ms, int)
            or duration_ms < 0
        ):
            raise EvidenceError("duration_ms must be a non-negative integer")
        normalized_reason = (
            None if reason is None else _validate_reason(reason, "reason")
        )
        document = self._current_result()
        row = self._row(document, gate_id)
        if row["status"] != "STARTED":
            raise EvidenceError(f"{gate_id} must be STARTED before it can finish")
        replacement = {
            **document,
            "rows": [
                (
                    {
                        **candidate,
                        "artifact": (
                            _empty_artifact()
                            if artifact is None
                            else _normalize_artifact(artifact)
                        ),
                        "duration_ms": duration_ms,
                        "ended_at_utc": _validate_timestamp(ended_at_utc),
                        "exit_code": exit_code,
                        "reason": normalized_reason,
                        "status": status,
                    }
                    if candidate["gate_id"] == gate_id
                    else candidate
                )
                for candidate in document["rows"]
            ],
        }
        self._replace_result(replacement)

    def finalize(self, *, blocked_reason: str) -> dict[str, str]:
        reason = _validate_reason(blocked_reason, "blocked_reason")
        document = self._current_result()
        statuses = {row["status"] for row in document["rows"]}
        if "STARTED" in statuses:
            raise EvidenceError("cannot finalize while a gate is STARTED")
        if not statuses <= _CLOSED_STATUSES:
            raise EvidenceError("execution result contains an unknown status")
        replacement = {
            **document,
            "complete": True,
            "rows": [
                (
                    {
                        **row,
                        "reason": reason,
                    }
                    if row["status"] == "NOT_RUN"
                    else row
                )
                for row in document["rows"]
            ],
        }
        self._replace_result(replacement)
        result_raw, result_snapshot = self._read_file(RESULT_NAME)
        if result_snapshot != self._result_snapshot:
            raise EvidenceError("execution result changed before manifest creation")
        result_sha256 = hashlib.sha256(result_raw).hexdigest()
        manifest = {
            "owner": OWNER,
            "plan_sha256": self.plan_sha256,
            "result_sha256": result_sha256,
            "retention_days": self._plan["retention_days"],
            "schema_version": 1,
        }
        manifest_raw = canonical_json_bytes(manifest)
        self._write_new(MANIFEST_NAME, manifest_raw)
        return {
            "manifest_sha256": hashlib.sha256(manifest_raw).hexdigest(),
            "plan_sha256": self.plan_sha256,
            "result_sha256": result_sha256,
        }
