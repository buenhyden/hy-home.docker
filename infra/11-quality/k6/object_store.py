"""Approved object handoff via the existing AWS CLI; no implicit runtime approval.

Only an explicitly supplied endpoint allowlist and file credentials permit calls.
Synthetic tests do not establish SeaweedFS conditional/checksum compatibility.
Upload receipts must be bound BEFORE the first immutable perf_db import.
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
import re
import resource
import stat
import subprocess
import tempfile
import uuid
from pathlib import Path
from urllib.parse import urlsplit

from quality_run import ContractError, _canonical, _write_once

CONTRACT_SCHEMA = "hyhome.quality-object-contract/v1"
RECEIPT_SCHEMA = "hyhome.quality-object-receipt/v1"
SLUG = re.compile(r"[a-z0-9][a-z0-9-]{0,62}")
NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,254}")
SHA = re.compile(r"[0-9a-f]{64}")


class ObjectStoreError(ValueError):
    """Redacted failure class, with a stable process exit recommendation."""

    def __init__(self, message: str, exit_code: int = 2):
        super().__init__(message)
        self.exit_code = exit_code


def _regular(path: Path, limit: int) -> bytes:
    try:
        absolute = path.absolute()
        if any(parent.is_symlink() for parent in (absolute, *absolute.parents)):
            raise ObjectStoreError("unsafe_file")
        fd = os.open(absolute, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
        with os.fdopen(fd, "rb") as stream:
            info = os.fstat(stream.fileno())
            if not stat.S_ISREG(info.st_mode) or info.st_size > limit:
                raise ObjectStoreError("file_quota_or_type_invalid")
            data = stream.read(limit + 1)
            if len(data) > limit:
                raise ObjectStoreError("file_quota_exceeded")
            return data
    except OSError:
        raise ObjectStoreError("file_unavailable") from None


def _json_bytes(data: bytes) -> dict:
    from result_import import _pairs

    try:
        value = json.loads(data, object_pairs_hook=_pairs)
        if not isinstance(value, dict):
            raise ValueError()
        return value
    except (ValueError, UnicodeError):
        raise ObjectStoreError("invalid_json") from None


def _json_file(path: Path) -> dict:
    return _json_bytes(_regular(path, 1024 * 1024))


def _contract(contract: dict) -> None:
    if not isinstance(contract, dict) or set(contract) != {
        "schema_version",
        "project_id",
        "endpoint",
        "region",
        "bucket",
        "prefix",
        "max_file_bytes",
        "max_total_bytes",
    }:
        raise ObjectStoreError("invalid_contract")
    if contract["schema_version"] != CONTRACT_SCHEMA:
        raise ObjectStoreError("invalid_contract_schema")
    for name in ("project_id", "region", "bucket"):
        if not isinstance(contract[name], str) or not SLUG.fullmatch(contract[name]):
            raise ObjectStoreError("invalid_contract_identifier")
    prefix = contract["prefix"]
    if (
        not isinstance(prefix, str)
        or not prefix
        or not all(SLUG.fullmatch(part) for part in prefix.split("/"))
        or len(prefix) > 512
    ):
        raise ObjectStoreError("invalid_object_prefix")
    try:
        endpoint = urlsplit(contract["endpoint"])
        if (
            endpoint.scheme not in ("http", "https")
            or not endpoint.hostname
            or endpoint.username
            or endpoint.password
            or endpoint.query
            or endpoint.fragment
            or endpoint.path not in ("", "/")
            or endpoint.port == 0
        ):
            raise ValueError()
    except (ValueError, TypeError, AttributeError):
        raise ObjectStoreError("invalid_endpoint") from None
    for key, ceiling in (
        ("max_file_bytes", 64 * 1024 * 1024),
        ("max_total_bytes", 256 * 1024 * 1024),
    ):
        value = contract[key]
        if type(value) is not int or not 1 <= value <= ceiling:
            raise ObjectStoreError("invalid_quota")


def _identity(identity: dict, contract: dict) -> None:
    if not isinstance(identity, dict) or set(identity) != {
        "project_id",
        "run_id",
        "attempt",
    }:
        raise ObjectStoreError("invalid_identity")
    try:
        if str(uuid.UUID(identity["run_id"])) != identity["run_id"]:
            raise ValueError()
    except (ValueError, TypeError, AttributeError):
        raise ObjectStoreError("invalid_run_id") from None
    if (
        identity["project_id"] != contract["project_id"]
        or type(identity["attempt"]) is not int
        or not 1 <= identity["attempt"] <= 999
    ):
        raise ObjectStoreError("invalid_project_or_attempt")


def _key(contract: dict, identity: dict, artifact: dict) -> str:
    return "/".join(
        (
            contract["prefix"],
            identity["project_id"],
            identity["run_id"],
            str(identity["attempt"]),
            artifact["sha256"],
            artifact["name"],
        )
    )


def validate_object_ref(ref: object, identity: dict, artifact: dict) -> None:
    """Validate a normalized reference without implying upload verification."""
    if (
        not isinstance(ref, str)
        or not isinstance(artifact.get("name"), str)
        or not NAME.fullmatch(artifact["name"])
        or not isinstance(artifact.get("sha256"), str)
        or not SHA.fullmatch(artifact["sha256"])
    ):
        raise ObjectStoreError("invalid_object_reference")
    parsed = urlsplit(ref)
    suffix = "/".join(
        (
            identity["project_id"],
            identity["run_id"],
            str(identity["attempt"]),
            artifact["sha256"],
            artifact["name"],
        )
    )
    prefix = parsed.path[1 : -(len(suffix) + 1)]
    if (
        parsed.scheme != "s3"
        or not SLUG.fullmatch(parsed.netloc)
        or parsed.query
        or parsed.fragment
        or not prefix
        or not all(SLUG.fullmatch(part) for part in prefix.split("/"))
        or parsed.path != "/" + prefix + "/" + suffix
    ):
        raise ObjectStoreError("invalid_object_reference")


def validate_receipt(receipt: dict) -> dict:
    if (
        not isinstance(receipt, dict)
        or set(receipt)
        != {
            "schema_version",
            "identity",
            "final_sha256",
            "contract",
            "artifacts",
        }
        or receipt["schema_version"] != RECEIPT_SCHEMA
    ):
        raise ObjectStoreError("invalid_object_receipt")
    _contract(receipt["contract"])
    _identity(receipt["identity"], receipt["contract"])
    if not isinstance(receipt["final_sha256"], str) or not SHA.fullmatch(
        receipt["final_sha256"]
    ):
        raise ObjectStoreError("invalid_final_digest")
    artifacts = receipt["artifacts"]
    if not isinstance(artifacts, list) or not 1 <= len(artifacts) <= 64:
        raise ObjectStoreError("invalid_artifacts")
    names, total = set(), 0
    for item in artifacts:
        if not isinstance(item, dict) or set(item) != {
            "name",
            "sha256",
            "bytes",
            "object_ref",
        }:
            raise ObjectStoreError("invalid_artifact")
        if (
            not isinstance(item["name"], str)
            or not NAME.fullmatch(item["name"])
            or item["name"] in names
            or item["name"] == "restore-receipt.json"
            or not isinstance(item["sha256"], str)
            or not SHA.fullmatch(item["sha256"])
            or type(item["bytes"]) is not int
            or not 0 <= item["bytes"] <= receipt["contract"]["max_file_bytes"]
        ):
            raise ObjectStoreError("invalid_artifact_identity_or_quota")
        expected = (
            "s3://"
            + receipt["contract"]["bucket"]
            + "/"
            + _key(receipt["contract"], receipt["identity"], item)
        )
        validate_object_ref(item["object_ref"], receipt["identity"], item)
        if item["object_ref"] != expected:
            raise ObjectStoreError("invalid_object_reference")
        names.add(item["name"])
        total += item["bytes"]
    if total > receipt["contract"]["max_total_bytes"]:
        raise ObjectStoreError("total_quota_exceeded")
    return receipt


def validate_object_binding(
    ref: object,
    identity: dict,
    artifact: dict,
    contract: dict,
    approved_endpoints: tuple[str, ...],
) -> None:
    _contract(contract)
    _identity(identity, contract)
    validate_object_ref(ref, identity, artifact)
    if (
        contract["endpoint"] not in approved_endpoints
        or ref
        != "s3://" + contract["bucket"] + "/" + _key(contract, identity, artifact)
        or type(artifact.get("bytes")) is not int
        or not 0 <= artifact["bytes"] <= contract["max_file_bytes"]
    ):
        raise ObjectStoreError("object_binding_not_approved")


def _binary(binary: str) -> None:
    path = Path(binary)
    if not path.is_absolute():
        raise ObjectStoreError("unsafe_object_client")
    try:
        info = path.lstat()
        if (
            not path.is_absolute()
            or any(p.is_symlink() for p in (path, *path.parents))
            or not stat.S_ISREG(info.st_mode)
            or info.st_uid not in (0, os.getuid())
            or info.st_mode & 0o022
            or not os.access(path, os.X_OK)
        ):
            raise ObjectStoreError("unsafe_object_client")
    except OSError:
        raise ObjectStoreError("object_client_unavailable", 127) from None


def _environment(
    contract: dict,
    approved_endpoints: tuple[str, ...],
    access_key_file: Path,
    secret_key_file: Path,
) -> dict:
    if not approved_endpoints or contract["endpoint"] not in approved_endpoints:
        raise ObjectStoreError("endpoint_not_approved")
    credentials = []
    for path in (access_key_file, secret_key_file):
        try:
            info = path.lstat()
            if info.st_uid not in (0, os.getuid()) or stat.S_IMODE(
                info.st_mode
            ) not in (0o600, 0o640):
                raise ObjectStoreError("unsafe_credential_permissions")
            value = _regular(path, 4096).decode("utf-8").rstrip("\r\n")
        except (OSError, UnicodeError):
            raise ObjectStoreError("invalid_credential_file") from None
        if not value or any(ord(c) < 33 or ord(c) > 126 for c in value):
            raise ObjectStoreError("invalid_credential_file")
        credentials.append(value)
    return dict(
        {
            key: value
            for key, value in os.environ.items()
            if key in ("LANG", "LC_ALL", "TZ")
        },
        PATH="/usr/bin:/bin",
        AWS_ACCESS_KEY_ID=credentials[0],
        AWS_SECRET_ACCESS_KEY=credentials[1],
        AWS_DEFAULT_REGION=contract["region"],
        AWS_EC2_METADATA_DISABLED="true",
        AWS_CONFIG_FILE="/dev/null",
        AWS_SHARED_CREDENTIALS_FILE="/dev/null",
        AWS_MAX_ATTEMPTS="2",
    )


def _client(
    binary: str,
    contract: dict,
    env: dict,
    operation: str,
    args: list[str],
    file_limit: int | None = None,
) -> dict | None:
    def limit_file():
        resource.setrlimit(resource.RLIMIT_FSIZE, (file_limit, file_limit))

    try:
        result = subprocess.run(
            [
                binary,
                "--endpoint-url",
                contract["endpoint"],
                "--no-cli-pager",
                "--cli-connect-timeout",
                "5",
                "--cli-read-timeout",
                "20",
                "s3api",
                operation,
                *args,
            ],
            env=env,
            capture_output=True,
            timeout=30,
            check=False,
            preexec_fn=limit_file if file_limit is not None else None,
        )
    except subprocess.TimeoutExpired:
        raise ObjectStoreError("object_client_timeout", 124) from None
    except (OSError, subprocess.SubprocessError):
        raise ObjectStoreError("object_client_unavailable", 127) from None
    if result.returncode != 0:
        if operation == "put-object" and b"(PreconditionFailed)" in result.stderr:
            return None
        raise ObjectStoreError("object_client_failed")
    try:
        if len(result.stdout) > 1024 * 1024:
            raise ValueError()
        value = json.loads(result.stdout)
        if not isinstance(value, dict):
            raise ValueError()
        return value
    except (ValueError, UnicodeError):
        raise ObjectStoreError("invalid_object_client_response") from None


def _head(binary: str, receipt: dict, item: dict, env: dict) -> dict:
    value = _client(
        binary,
        receipt["contract"],
        env,
        "head-object",
        [
            "--bucket",
            receipt["contract"]["bucket"],
            "--key",
            _key(receipt["contract"], receipt["identity"], item),
            "--checksum-mode",
            "ENABLED",
        ],
    )
    expected = base64.b64encode(bytes.fromhex(item["sha256"])).decode()
    if (
        value is None
        or type(value.get("ContentLength")) is not int
        or value.get("ContentLength") != item["bytes"]
        or value.get("ChecksumSHA256") != expected
    ):
        raise ObjectStoreError("object_verification_failed")
    return value


def upload(
    attempt_dir: Path,
    contract: dict,
    receipt_path: Path,
    *,
    approved_endpoints: tuple[str, ...],
    access_key_file: Path,
    secret_key_file: Path,
    aws_binary: str,
) -> dict:
    _binary(aws_binary)
    _contract(contract)
    for name in ("final.json", "checksums.json"):
        try:
            if (attempt_dir / name).lstat().st_mode & 0o222:
                raise ObjectStoreError("artifact_not_finalized")
        except OSError:
            raise ObjectStoreError("file_unavailable") from None
    final_bytes = _regular(attempt_dir / "final.json", 1024 * 1024)
    final = _json_bytes(final_bytes)
    checksums_bytes = _regular(attempt_dir / "checksums.json", 1024 * 1024)
    if (
        final.get("import_allowed") is not True
        or final.get("checksums_sha256") != hashlib.sha256(checksums_bytes).hexdigest()
    ):
        raise ObjectStoreError("quarantined_or_invalid_final")
    identity = {name: final.get(name) for name in ("project_id", "run_id", "attempt")}
    _identity(identity, contract)
    artifacts = _json_bytes(checksums_bytes).get("artifacts")
    if not isinstance(artifacts, list) or any(
        not isinstance(a, dict) or set(a) != {"name", "sha256", "bytes"}
        for a in artifacts
    ):
        raise ObjectStoreError("invalid_checksum_artifacts")
    for a in artifacts:
        if (
            not isinstance(a["name"], str)
            or not NAME.fullmatch(a["name"])
            or not isinstance(a["sha256"], str)
            or not SHA.fullmatch(a["sha256"])
        ):
            raise ObjectStoreError("invalid_artifact_identity")
    receipt = {
        "schema_version": RECEIPT_SCHEMA,
        "identity": identity,
        "final_sha256": hashlib.sha256(final_bytes).hexdigest(),
        "contract": dict(contract),
        "artifacts": [
            dict(
                a,
                object_ref="s3://"
                + contract["bucket"]
                + "/"
                + _key(contract, identity, a),
            )
            for a in artifacts
        ],
    }
    validate_receipt(receipt)
    if any(parent.is_symlink() for parent in receipt_path.absolute().parents):
        raise ObjectStoreError("unsafe_receipt_parent")
    if receipt_path.exists() or receipt_path.is_symlink():
        if _regular(receipt_path, 1024 * 1024) != _canonical(receipt):
            raise ObjectStoreError("immutable_receipt_conflict")
    # Validate every local file before any network request, then use owned snapshots.
    with tempfile.TemporaryDirectory(prefix="quality-object-upload-") as temporary:
        snapshots = []
        for item in receipt["artifacts"]:
            source = attempt_dir / item["name"]
            try:
                mode = source.lstat().st_mode
            except OSError:
                raise ObjectStoreError("file_unavailable") from None
            if mode & 0o222:
                raise ObjectStoreError("artifact_not_finalized")
            data = _regular(source, contract["max_file_bytes"])
            if (
                len(data) != item["bytes"]
                or hashlib.sha256(data).hexdigest() != item["sha256"]
            ):
                raise ObjectStoreError("local_artifact_mismatch")
            path = Path(temporary) / item["name"]
            path.write_bytes(data)
            path.chmod(0o400)
            snapshots.append((item, path))
        env = _environment(
            contract, approved_endpoints, access_key_file, secret_key_file
        )
        for item, path in snapshots:
            _client(
                aws_binary,
                contract,
                env,
                "put-object",
                [
                    "--bucket",
                    contract["bucket"],
                    "--key",
                    _key(contract, identity, item),
                    "--body",
                    str(path),
                    "--if-none-match",
                    "*",
                    "--checksum-sha256",
                    base64.b64encode(bytes.fromhex(item["sha256"])).decode(),
                ],
            )
            _head(aws_binary, receipt, item, env)
    try:
        _write_once(receipt_path, receipt)
    except (ContractError, OSError):
        raise ObjectStoreError("immutable_receipt_conflict") from None
    return receipt


def restore(
    receipt: dict,
    contract: dict,
    scratch: Path,
    *,
    approved_endpoints: tuple[str, ...],
    access_key_file: Path,
    secret_key_file: Path,
    aws_binary: str,
) -> dict:
    _binary(aws_binary)
    validate_receipt(receipt)
    if contract != receipt["contract"]:
        raise ObjectStoreError("restore_contract_mismatch")
    if (
        any(p.is_symlink() for p in (scratch.absolute(), *scratch.absolute().parents))
        or not scratch.is_dir()
        or any(scratch.iterdir())
    ):
        raise ObjectStoreError("restore_requires_empty_owned_scratch")
    env = _environment(contract, approved_endpoints, access_key_file, secret_key_file)
    with tempfile.TemporaryDirectory(
        prefix=".object-restore-", dir=scratch
    ) as temporary:
        paths = []
        for item in receipt["artifacts"]:
            head = _head(aws_binary, receipt, item, env)
            etag = head.get("ETag")
            if not isinstance(etag, str) or not etag or "\n" in etag:
                raise ObjectStoreError("restore_etag_missing")
            path = Path(temporary) / item["name"]
            value = _client(
                aws_binary,
                contract,
                env,
                "get-object",
                [
                    "--bucket",
                    contract["bucket"],
                    "--key",
                    _key(contract, receipt["identity"], item),
                    "--if-match",
                    etag,
                    str(path),
                ],
                file_limit=max(item["bytes"], 1),
            )
            if value is None:
                raise ObjectStoreError("object_restore_failed")
            data = _regular(path, item["bytes"])
            if (
                len(data) != item["bytes"]
                or hashlib.sha256(data).hexdigest() != item["sha256"]
            ):
                raise ObjectStoreError("restored_artifact_mismatch")
            path.chmod(0o440)
            paths.append(path)
        linked = []
        try:
            for path in paths:
                info = path.lstat()
                target = scratch / path.name
                os.link(path, target, follow_symlinks=False)
                linked.append((target, info.st_dev, info.st_ino))
            receipt_source = Path(temporary) / "restore-receipt.json"
            _write_once(receipt_source, receipt)
            info = receipt_source.lstat()
            target = scratch / receipt_source.name
            os.link(receipt_source, target, follow_symlinks=False)
            linked.append((target, info.st_dev, info.st_ino))
        except (OSError, ContractError):
            for target, device, inode in reversed(linked):
                try:
                    info = target.lstat()
                    if (info.st_dev, info.st_ino) == (device, inode):
                        target.unlink()
                except FileNotFoundError:
                    pass
            raise ObjectStoreError("restore_publication_failed") from None
    return receipt
