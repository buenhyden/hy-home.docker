#!/usr/bin/env python3
"""Validate and atomically publish a private, immutable Grype DB seed."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import re
import secrets
import stat
import sys
from typing import Any


SHA256_HEX_RE = re.compile(r"[0-9a-f]{64}")
SHA256_RE = re.compile(r"sha256:[0-9a-f]{64}")
TIMESTAMP_RE = re.compile(r"20[0-9]{2}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z")
STAGE_NAME_RE = re.compile(r"\.stage\.[0-9a-f]{32}")
GENERATION_PATH_RE = re.compile(r"generations/[0-9a-f]{64}")
MAX_STATUS_BYTES = 131_072
MAX_CACHE_FILES = 128
MAX_CACHE_BYTES = 2 * 1024 * 1024 * 1024
GENERATION = "hyhome-grype-db-seed-v1"
EXACT_GRYPE_TOOL = {
    "image_ref": (
        "anchore/grype:v0.116.0@"
        "sha256:fd4ab4d1042b522c896e73bdf09ab8bf384fa417df99d6dd0d6e1008c7e7c821"
    ),
    "repo_digest": (
        "anchore/grype@"
        "sha256:fd4ab4d1042b522c896e73bdf09ab8bf384fa417df99d6dd0d6e1008c7e7c821"
    ),
    "config_id": (
        "sha256:fd4ab4d1042b522c896e73bdf09ab8bf384fa417df99d6dd0d6e1008c7e7c821"
    ),
}
IDENTITY_KEYS = {
    "cache",
    "database",
    "generation",
    "generation_path",
    "redaction_status",
    "schema_version",
    "seeded_at",
    "tool",
}


class SeedContractError(ValueError):
    """Raised when a seed crosses a typed identity or filesystem boundary."""


def _relative_parts(relative: pathlib.Path | str) -> tuple[str, ...]:
    value = pathlib.PurePosixPath(str(relative).replace("\\", "/"))
    if (
        value.is_absolute()
        or not value.parts
        or any(part in {"", ".", ".."} for part in value.parts)
    ):
        raise SeedContractError("seed-output-relative-path-invalid")
    return value.parts


def _validate_directory_stat(value: os.stat_result, *, final: bool) -> None:
    if not stat.S_ISDIR(value.st_mode):
        raise SeedContractError("seed-directory-type-invalid")
    if value.st_uid != os.getuid():
        raise SeedContractError("seed-directory-owner-invalid")
    mode = stat.S_IMODE(value.st_mode)
    if final:
        if mode != 0o700:
            raise SeedContractError("seed-directory-mode-invalid")
    elif mode & 0o022:
        raise SeedContractError("seed-ancestor-writable")


def _open_output_directory(
    base: pathlib.Path | str,
    relative: pathlib.Path | str,
    *,
    create: bool,
) -> tuple[int, str]:
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    try:
        current_fd = os.open(pathlib.Path(base), flags)
    except OSError as exc:
        raise SeedContractError("seed-output-base-invalid") from exc
    try:
        _validate_directory_stat(os.fstat(current_fd), final=False)
        parts = _relative_parts(relative)
        for index, component in enumerate(parts):
            final = index == len(parts) - 1
            try:
                next_fd = os.open(component, flags, dir_fd=current_fd)
            except FileNotFoundError:
                if not create:
                    raise SeedContractError("seed-output-missing") from None
                try:
                    os.mkdir(component, 0o700, dir_fd=current_fd)
                    next_fd = os.open(component, flags, dir_fd=current_fd)
                    os.fchmod(next_fd, 0o700 if final else 0o755)
                except OSError as exc:
                    raise SeedContractError("seed-output-create-failed") from exc
            except OSError as exc:
                raise SeedContractError("seed-output-symlink-or-invalid") from exc
            os.close(current_fd)
            current_fd = next_fd
            if create and final:
                current_stat = os.fstat(current_fd)
                if (
                    stat.S_ISDIR(current_stat.st_mode)
                    and current_stat.st_uid == os.getuid()
                    and stat.S_IMODE(current_stat.st_mode) & 0o022 == 0
                ):
                    os.fchmod(current_fd, 0o700)
            _validate_directory_stat(os.fstat(current_fd), final=final)
        output_stat = os.fstat(current_fd)
        return current_fd, f"{output_stat.st_dev}:{output_stat.st_ino}"
    except Exception:
        os.close(current_fd)
        raise


def _validate_identity(descriptor: int, expected: str, reason: str) -> None:
    current = os.fstat(descriptor)
    if f"{current.st_dev}:{current.st_ino}" != expected:
        raise SeedContractError(reason)


def _open_owned_directory_at(parent_fd: int, name: str) -> int:
    try:
        descriptor = os.open(
            name,
            os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
            dir_fd=parent_fd,
        )
    except OSError as exc:
        raise SeedContractError("seed-directory-open-failed") from exc
    try:
        _validate_directory_stat(os.fstat(descriptor), final=True)
    except Exception:
        os.close(descriptor)
        raise
    return descriptor


def _ensure_owned_directory_at(parent_fd: int, name: str) -> int:
    try:
        os.mkdir(name, 0o700, dir_fd=parent_fd)
    except FileExistsError:
        pass
    except OSError as exc:
        raise SeedContractError("seed-directory-create-failed") from exc
    descriptor = _open_owned_directory_at(parent_fd, name)
    os.fchmod(descriptor, 0o700)
    return descriptor


def _atomic_write_at(parent_fd: int, name: str, body: bytes) -> None:
    temporary = f".{name}.{secrets.token_hex(16)}.tmp"
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW
    try:
        descriptor = os.open(temporary, flags, 0o600, dir_fd=parent_fd)
    except OSError as exc:
        raise SeedContractError("seed-pointer-temporary-create-failed") from exc
    try:
        os.fchmod(descriptor, 0o600)
        view = memoryview(body)
        while view:
            view = view[os.write(descriptor, view) :]
        os.fsync(descriptor)
    except Exception:
        try:
            os.unlink(temporary, dir_fd=parent_fd)
        except FileNotFoundError:
            pass
        raise
    finally:
        os.close(descriptor)
    try:
        os.replace(temporary, name, src_dir_fd=parent_fd, dst_dir_fd=parent_fd)
        os.fsync(parent_fd)
    except Exception:
        try:
            os.unlink(temporary, dir_fd=parent_fd)
        except FileNotFoundError:
            pass
        raise


def _read_private_file_at(parent_fd: int, name: str, *, limit: int) -> bytes:
    try:
        descriptor = os.open(name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=parent_fd)
    except OSError as exc:
        raise SeedContractError("seed-private-file-open-failed") from exc
    try:
        file_stat = os.fstat(descriptor)
        if (
            not stat.S_ISREG(file_stat.st_mode)
            or file_stat.st_uid != os.getuid()
            or stat.S_IMODE(file_stat.st_mode) != 0o600
            or file_stat.st_size > limit
        ):
            raise SeedContractError("seed-private-file-invalid")
        chunks: list[bytes] = []
        remaining = limit + 1
        while remaining > 0:
            chunk = os.read(descriptor, min(65_536, remaining))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        body = b"".join(chunks)
        if len(body) > limit:
            raise SeedContractError("seed-private-file-too-large")
        return body
    finally:
        os.close(descriptor)


def _parse_status(body: bytes) -> dict[str, str]:
    try:
        text = body.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise SeedContractError("seed-status-encoding-invalid") from exc
    fields = dict(
        re.findall(r"^(Schema|Built|Status):[ \t]+([^\r\n]+)$", text, re.MULTILINE)
    )
    checksum = re.search(r"checksum=sha256%3A([0-9a-f]{64})(?:\s|$|&)", text)
    schema = fields.get("Schema", "")
    built = fields.get("Built", "")
    status_value = fields.get("Status", "").lower()
    if (
        not re.fullmatch(r"v6(?:\.[0-9]+){0,2}", schema)
        or not TIMESTAMP_RE.fullmatch(built)
        or status_value not in {"valid", "active"}
        or checksum is None
    ):
        raise SeedContractError("seed-status-identity-invalid")
    return {
        "built": built,
        "package_sha256": checksum.group(1),
        "schema": schema,
        "status": status_value,
    }


def _scan_cache_directory(cache_fd: int) -> dict[str, int | str]:
    digest = hashlib.sha256()
    file_count = 0
    byte_count = 0
    schema_seen = False

    def visit(directory_fd: int, prefix: str) -> None:
        nonlocal file_count, byte_count, schema_seen
        try:
            names = sorted(os.listdir(directory_fd))
        except OSError as exc:
            raise SeedContractError("seed-cache-list-failed") from exc
        for name in names:
            if not name or name in {".", ".."} or "/" in name or "\x00" in name:
                raise SeedContractError("seed-cache-name-invalid")
            relative = f"{prefix}/{name}" if prefix else name
            try:
                value = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
            except OSError as exc:
                raise SeedContractError("seed-cache-stat-failed") from exc
            if value.st_uid != os.getuid():
                raise SeedContractError("seed-cache-owner-invalid")
            if stat.S_ISDIR(value.st_mode):
                child_fd = _open_owned_directory_at(directory_fd, name)
                try:
                    os.fchmod(child_fd, 0o700)
                    if relative == "6":
                        schema_seen = True
                    digest.update(b"D\0" + relative.encode("utf-8") + b"\n")
                    visit(child_fd, relative)
                finally:
                    os.close(child_fd)
                continue
            if not stat.S_ISREG(value.st_mode) or value.st_nlink != 1:
                raise SeedContractError("seed-cache-member-type-invalid")
            try:
                file_fd = os.open(
                    name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=directory_fd
                )
            except OSError as exc:
                raise SeedContractError("seed-cache-file-open-failed") from exc
            try:
                opened = os.fstat(file_fd)
                if (
                    not stat.S_ISREG(opened.st_mode)
                    or opened.st_uid != os.getuid()
                    or opened.st_nlink != 1
                    or (opened.st_dev, opened.st_ino, opened.st_size)
                    != (value.st_dev, value.st_ino, value.st_size)
                ):
                    raise SeedContractError("seed-cache-file-identity-changed")
                os.fchmod(file_fd, 0o600)
                file_digest = hashlib.sha256()
                size = 0
                while True:
                    chunk = os.read(file_fd, 1_048_576)
                    if not chunk:
                        break
                    size += len(chunk)
                    if size > MAX_CACHE_BYTES:
                        raise SeedContractError("seed-cache-size-limit")
                    file_digest.update(chunk)
                if size != opened.st_size:
                    raise SeedContractError("seed-cache-file-size-changed")
            finally:
                os.close(file_fd)
            file_count += 1
            byte_count += size
            if file_count > MAX_CACHE_FILES or byte_count > MAX_CACHE_BYTES:
                raise SeedContractError("seed-cache-size-limit")
            digest.update(
                b"F\0"
                + relative.encode("utf-8")
                + b"\0"
                + str(size).encode("ascii")
                + b"\0"
                + file_digest.hexdigest().encode("ascii")
                + b"\n"
            )

    os.fchmod(cache_fd, 0o700)
    visit(cache_fd, "")
    if not schema_seen or file_count == 0:
        raise SeedContractError("seed-cache-schema-or-content-missing")
    return {
        "byte_count": byte_count,
        "file_count": file_count,
        "tree_sha256": f"sha256:{digest.hexdigest()}",
    }


def _validate_tool(tool: Any) -> dict[str, str]:
    if not isinstance(tool, dict) or tool != EXACT_GRYPE_TOOL:
        raise SeedContractError("seed-tool-identity-invalid")
    return dict(EXACT_GRYPE_TOOL)


def _validate_payload(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict) or set(payload) != IDENTITY_KEYS:
        raise SeedContractError("seed-identity-shape-invalid")
    cache = payload.get("cache")
    database = payload.get("database")
    if (
        payload.get("schema_version") != 1
        or payload.get("generation") != GENERATION
        or payload.get("redaction_status") != "passed"
        or not TIMESTAMP_RE.fullmatch(str(payload.get("seeded_at", "")))
        or not GENERATION_PATH_RE.fullmatch(str(payload.get("generation_path", "")))
        or payload.get("tool") != EXACT_GRYPE_TOOL
        or not isinstance(database, dict)
        or set(database) != {"built", "package_sha256", "schema", "status"}
        or not TIMESTAMP_RE.fullmatch(str(database.get("built", "")))
        or not re.fullmatch(r"v6(?:\.[0-9]+){0,2}", str(database.get("schema", "")))
        or database.get("status") not in {"valid", "active"}
        or not SHA256_HEX_RE.fullmatch(str(database.get("package_sha256", "")))
        or not isinstance(cache, dict)
        or set(cache) != {"byte_count", "file_count", "tree_sha256"}
        or isinstance(cache.get("byte_count"), bool)
        or not isinstance(cache.get("byte_count"), int)
        or cache["byte_count"] <= 0
        or isinstance(cache.get("file_count"), bool)
        or not isinstance(cache.get("file_count"), int)
        or cache["file_count"] <= 0
        or not SHA256_RE.fullmatch(str(cache.get("tree_sha256", "")))
    ):
        raise SeedContractError("seed-identity-invalid")
    expected_generation = hashlib.sha256(
        (
            json.dumps(
                {
                    key: value
                    for key, value in payload.items()
                    if key != "generation_path"
                },
                sort_keys=True,
            )
            + "\n"
        ).encode("utf-8")
    ).hexdigest()
    if payload["generation_path"] != f"generations/{expected_generation}":
        raise SeedContractError("seed-generation-identity-invalid")
    return payload


def _tool_from_registry(repo_root: pathlib.Path | str) -> dict[str, str]:
    path = pathlib.Path(repo_root) / "infra/supply-chain.tool-images.json"
    try:
        registry = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SeedContractError("seed-tool-registry-invalid") from exc
    rows = registry.get("tools") if isinstance(registry, dict) else None
    if not isinstance(rows, list):
        raise SeedContractError("seed-tool-registry-invalid")
    for row in rows:
        if isinstance(row, dict) and row.get("name") == "grype":
            return _validate_tool(
                {
                    "image_ref": f"{row.get('image')}@{row.get('digest')}",
                    "repo_digest": row.get("repo_digest"),
                    "config_id": row.get("config_id"),
                }
            )
    raise SeedContractError("seed-tool-registry-invalid")


def prepare_seed_stage(
    base: pathlib.Path | str, relative: pathlib.Path | str
) -> tuple[str, str, pathlib.Path]:
    output_fd, output_identity = _open_output_directory(base, relative, create=True)
    stage_name = f".stage.{secrets.token_hex(16)}"
    try:
        generations_fd = _ensure_owned_directory_at(output_fd, "generations")
        os.close(generations_fd)
        try:
            os.mkdir(stage_name, 0o700, dir_fd=output_fd)
            stage_fd = _open_owned_directory_at(output_fd, stage_name)
        except OSError as exc:
            raise SeedContractError("seed-stage-create-failed") from exc
        try:
            os.fchmod(stage_fd, 0o700)
            cache_fd = _ensure_owned_directory_at(stage_fd, "cache")
            os.close(cache_fd)
            stage_stat = os.fstat(stage_fd)
            stage_identity = f"{stage_stat.st_dev}:{stage_stat.st_ino}"
        finally:
            os.close(stage_fd)
        os.fsync(output_fd)
    finally:
        os.close(output_fd)
    return (
        output_identity,
        stage_identity,
        pathlib.Path(base) / pathlib.Path(relative) / stage_name,
    )


def finalize_seed_generation(
    base: pathlib.Path | str,
    relative: pathlib.Path | str,
    output_identity: str,
    stage_identity: str,
    stage_path: pathlib.Path | str,
    status_path: pathlib.Path | str,
    tool: Any,
    seeded_at: str,
) -> dict[str, Any]:
    if not TIMESTAMP_RE.fullmatch(seeded_at):
        raise SeedContractError("seeded-at-invalid")
    tool_identity = _validate_tool(tool)
    output_path = pathlib.Path(base) / pathlib.Path(relative)
    stage = pathlib.Path(stage_path)
    if stage.parent != output_path or not STAGE_NAME_RE.fullmatch(stage.name):
        raise SeedContractError("seed-stage-path-invalid")
    if pathlib.Path(status_path) != stage / "db-status.txt":
        raise SeedContractError("seed-status-path-invalid")

    output_fd, _ = _open_output_directory(base, relative, create=False)
    stage_fd = -1
    generations_fd = -1
    try:
        _validate_identity(output_fd, output_identity, "seed-output-identity-mismatch")
        stage_fd = _open_owned_directory_at(output_fd, stage.name)
        _validate_identity(stage_fd, stage_identity, "seed-stage-identity-mismatch")
        status_body = _read_private_file_at(
            stage_fd, "db-status.txt", limit=MAX_STATUS_BYTES
        )
        database = _parse_status(status_body)
        cache_fd = _open_owned_directory_at(stage_fd, "cache")
        try:
            cache = _scan_cache_directory(cache_fd)
            os.fsync(cache_fd)
        finally:
            os.close(cache_fd)
        base_payload = {
            "cache": cache,
            "database": database,
            "generation": GENERATION,
            "redaction_status": "passed",
            "schema_version": 1,
            "seeded_at": seeded_at,
            "tool": tool_identity,
        }
        generation_digest = hashlib.sha256(
            (json.dumps(base_payload, sort_keys=True) + "\n").encode("utf-8")
        ).hexdigest()
        payload = {
            **base_payload,
            "generation_path": f"generations/{generation_digest}",
        }
        _validate_payload(payload)
        body = (json.dumps(payload, sort_keys=True) + "\n").encode("utf-8")
        _atomic_write_at(stage_fd, "identity.json", body)
        try:
            os.unlink("db-status.txt", dir_fd=stage_fd)
        except OSError as exc:
            raise SeedContractError("seed-status-cleanup-failed") from exc
        os.fsync(stage_fd)
        generations_fd = _ensure_owned_directory_at(output_fd, "generations")
        try:
            os.rename(
                stage.name,
                generation_digest,
                src_dir_fd=output_fd,
                dst_dir_fd=generations_fd,
            )
        except FileExistsError as exc:
            raise SeedContractError("seed-generation-already-exists") from exc
        except OSError as exc:
            raise SeedContractError("seed-generation-publication-failed") from exc
        os.fsync(generations_fd)
        _atomic_write_at(output_fd, "current.json", body)
        return payload
    finally:
        if generations_fd >= 0:
            os.close(generations_fd)
        if stage_fd >= 0:
            os.close(stage_fd)
        os.close(output_fd)


def _read_pointer(output_fd: int) -> tuple[bytes, dict[str, Any]]:
    body = _read_private_file_at(output_fd, "current.json", limit=MAX_STATUS_BYTES)
    try:
        payload = json.loads(body)
    except json.JSONDecodeError as exc:
        raise SeedContractError("seed-pointer-json-invalid") from exc
    return body, _validate_payload(payload)


def inspect_current_seed(
    base: pathlib.Path | str, relative: pathlib.Path | str
) -> tuple[pathlib.Path, dict[str, Any]]:
    output_fd, _ = _open_output_directory(base, relative, create=False)
    generations_fd = -1
    generation_fd = -1
    try:
        pointer_body, payload = _read_pointer(output_fd)
        generation_name = payload["generation_path"].split("/", 1)[1]
        generations_fd = _open_owned_directory_at(output_fd, "generations")
        generation_fd = _open_owned_directory_at(generations_fd, generation_name)
        identity_body = _read_private_file_at(
            generation_fd, "identity.json", limit=MAX_STATUS_BYTES
        )
        if identity_body != pointer_body:
            raise SeedContractError("seed-generation-pointer-mismatch")
        cache_fd = _open_owned_directory_at(generation_fd, "cache")
        try:
            actual_cache = _scan_cache_directory(cache_fd)
        finally:
            os.close(cache_fd)
        if actual_cache != payload["cache"]:
            raise SeedContractError("seed-cache-identity-mismatch")
        cache_path = (
            pathlib.Path(base)
            / pathlib.Path(relative)
            / "generations"
            / generation_name
            / "cache"
        )
        return cache_path, payload
    finally:
        if generation_fd >= 0:
            os.close(generation_fd)
        if generations_fd >= 0:
            os.close(generations_fd)
        os.close(output_fd)


def resolve_seed_generation(
    base: pathlib.Path | str, relative: pathlib.Path | str
) -> pathlib.Path:
    return inspect_current_seed(base, relative)[0]


def discard_seed_stage(
    base: pathlib.Path | str,
    relative: pathlib.Path | str,
    output_identity: str,
    stage_identity: str,
    stage_path: pathlib.Path | str,
) -> None:
    output_path = pathlib.Path(base) / pathlib.Path(relative)
    stage = pathlib.Path(stage_path)
    if stage.parent != output_path or not STAGE_NAME_RE.fullmatch(stage.name):
        raise SeedContractError("seed-stage-path-invalid")
    output_fd, _ = _open_output_directory(base, relative, create=False)
    try:
        _validate_identity(output_fd, output_identity, "seed-output-identity-mismatch")
        try:
            stage_fd = _open_owned_directory_at(output_fd, stage.name)
        except SeedContractError:
            return
        try:
            _validate_identity(stage_fd, stage_identity, "seed-stage-identity-mismatch")
        finally:
            os.close(stage_fd)
        # The stage is task-owned and identity-bound. Walk without following
        # links, unlink files/links, then remove directories bottom-up.
        for current, directories, files in os.walk(
            stage, topdown=False, followlinks=False
        ):
            current_path = pathlib.Path(current)
            for name in files:
                (current_path / name).unlink(missing_ok=True)
            for name in directories:
                path = current_path / name
                if path.is_symlink():
                    path.unlink()
                else:
                    path.rmdir()
        stage.rmdir()
        os.fsync(output_fd)
    finally:
        os.close(output_fd)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--prepare-stage",
        nargs=2,
        metavar=("REPO_ROOT", "RELATIVE_OUTPUT"),
    )
    parser.add_argument(
        "--finalize-stage",
        nargs=7,
        metavar=(
            "REPO_ROOT",
            "RELATIVE_OUTPUT",
            "OUTPUT_IDENTITY",
            "STAGE_IDENTITY",
            "STAGE_PATH",
            "STATUS_PATH",
            "SEEDED_AT",
        ),
    )
    parser.add_argument(
        "--discard-stage",
        nargs=5,
        metavar=(
            "REPO_ROOT",
            "RELATIVE_OUTPUT",
            "OUTPUT_IDENTITY",
            "STAGE_IDENTITY",
            "STAGE_PATH",
        ),
    )
    parser.add_argument(
        "--resolve-current",
        nargs=2,
        metavar=("REPO_ROOT", "RELATIVE_OUTPUT"),
    )
    parser.add_argument(
        "--check-current",
        nargs=2,
        metavar=("REPO_ROOT", "RELATIVE_OUTPUT"),
    )
    args = parser.parse_args(argv)
    operations = (
        args.prepare_stage,
        args.finalize_stage,
        args.discard_stage,
        args.resolve_current,
        args.check_current,
    )
    if sum(value is not None for value in operations) != 1:
        parser.print_usage(sys.stderr)
        return 2
    try:
        if args.prepare_stage:
            output_identity, stage_identity, stage = prepare_seed_stage(
                *args.prepare_stage
            )
            print(output_identity)
            print(stage_identity)
            print(stage)
            return 0
        if args.finalize_stage:
            (
                base,
                relative,
                output_identity,
                stage_identity,
                stage,
                status_path,
                seeded_at,
            ) = args.finalize_stage
            payload = finalize_seed_generation(
                base,
                relative,
                output_identity,
                stage_identity,
                stage,
                status_path,
                _tool_from_registry(base),
                seeded_at,
            )
            print(json.dumps(payload, sort_keys=True))
            return 0
        if args.discard_stage:
            discard_seed_stage(*args.discard_stage)
            return 0
        if args.resolve_current:
            print(resolve_seed_generation(*args.resolve_current))
            return 0
        _, payload = inspect_current_seed(*args.check_current)
        print(json.dumps(payload, sort_keys=True))
        return 0
    except (OSError, SeedContractError) as exc:
        print(f"grype_db_seed=fail reason={exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
