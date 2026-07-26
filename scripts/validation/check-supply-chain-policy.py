#!/usr/bin/env python3
"""Validate the deterministic, redacted local supply-chain fixture contract."""

from __future__ import annotations

import argparse
import datetime as dt
import fnmatch
import hashlib
import io
import json
import os
import pathlib
import re
import secrets
import stat
import subprocess
import sys
import tarfile
from typing import Any
import zlib


ROOT = pathlib.Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "tests/fixtures/supply-chain"
TOOL_REGISTRY_PATH = ROOT / "infra/supply-chain.tool-images.json"
POLICY_PATH = ROOT / "infra/supply-chain.sample-service-policy.json"
EXCEPTIONS_PATH = ROOT / "infra/supply-chain.vulnerability-exceptions.json"
SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
SHA1_RE = re.compile(r"^[0-9a-f]{40}$")
LOCAL_IMAGE_REF_RE = re.compile(
    r"^hyhome\.local/sample-web-service:(baseline|candidate)-([0-9a-f]{64})$"
)
OCI_INDEX_MEDIA_TYPE = "application/vnd.oci.image.index.v1+json"
OCI_MANIFEST_MEDIA_TYPE = "application/vnd.oci.image.manifest.v1+json"
OCI_CONFIG_MEDIA_TYPE = "application/vnd.oci.image.config.v1+json"
OCI_PORTABLE_LAYER_MEDIA_TYPES = {
    "application/vnd.oci.image.layer.v1.tar+gzip",
    "application/vnd.oci.image.layer.nondistributable.v1.tar+gzip",
}
# The local sample-service handoff is intentionally bounded before allocation:
# at most 512 MiB compressed input, 512 MiB per expanded layer, and 1 GiB
# expanded across all layers. Larger images require a separately reviewed path.
OCI_ARCHIVE_MAX_BYTES = 512 * 1024 * 1024
OCI_METADATA_MAX_BYTES = 16 * 1024 * 1024
OCI_LAYER_MAX_UNCOMPRESSED_BYTES = 512 * 1024 * 1024
OCI_LAYERS_MAX_UNCOMPRESSED_BYTES = 1024 * 1024 * 1024
OCI_DECOMPRESSION_CHUNK_BYTES = 64 * 1024
OCI_OUTER_COMPRESSION_MAGICS = (
    b"\x1f\x8b",  # gzip
    b"BZh",  # bzip2
    b"\xfd7zXZ\x00",  # xz
    b"\x28\xb5\x2f\xfd",  # zstd
    b"\x04\x22\x4d\x18",  # lz4
)
VERDICT_IDENTITY_KEYS = (
    "oci_manifest_digest",
    "image_config_digest",
    "oci_archive_sha256",
    "docker_archive_sha256",
    "local_image_ref",
    "runtime_image_id",
    "runtime_identity_kind",
)
VERIFICATION_VERDICT_KEYS = {
    "build_context_sha256",
    "docker_archive_sha256",
    "exception_id",
    "image_config_digest",
    "local_image_ref",
    "oci_archive_sha256",
    "oci_manifest_digest",
    "policy_id",
    "producer_spec",
    "redaction_status",
    "role",
    "runtime_identity_kind",
    "runtime_image_id",
    "schema_version",
    "source_revision",
    "verified_at",
    "verdict",
}
SCORECARD_REPOSITORY = "github.com/buenhyden/hy-home.docker"
SAMPLE_SERVICE_DOCKERIGNORE = (
    "**",
    "!Dockerfile",
    "!.dockerignore",
    "!nginx.conf",
    "!site/",
    "!site/**",
)
TOOL_PINS = {
    "syft": (
        "anchore/syft:v1.48.0",
        "sha256:b4f1df79f97b817682d8b5ff941eb6bfe74f6172553a5e312c75bbc2eabc405c",
        "anchore/syft@sha256:b4f1df79f97b817682d8b5ff941eb6bfe74f6172553a5e312c75bbc2eabc405c",
        "sha256:b4f1df79f97b817682d8b5ff941eb6bfe74f6172553a5e312c75bbc2eabc405c",
        "v1.48.0",
    ),
    "grype": (
        "anchore/grype:v0.116.0",
        "sha256:fd4ab4d1042b522c896e73bdf09ab8bf384fa417df99d6dd0d6e1008c7e7c821",
        "anchore/grype@sha256:fd4ab4d1042b522c896e73bdf09ab8bf384fa417df99d6dd0d6e1008c7e7c821",
        "sha256:fd4ab4d1042b522c896e73bdf09ab8bf384fa417df99d6dd0d6e1008c7e7c821",
        "v0.116.0",
    ),
    "cosign": (
        "gcr.io/projectsigstore/cosign:v3.0.6",
        "sha256:de9c65609e6bde17e6b48de485ee788407c9502fa08b8f4459f595b21f56cd00",
        "gcr.io/projectsigstore/cosign@sha256:de9c65609e6bde17e6b48de485ee788407c9502fa08b8f4459f595b21f56cd00",
        "sha256:de9c65609e6bde17e6b48de485ee788407c9502fa08b8f4459f595b21f56cd00",
        "v3.0.6",
    ),
    "scorecard": (
        "ghcr.io/ossf/scorecard:v5.5.0",
        "sha256:3f24714e9366917adb7a05635382c97dfecb14b21eaef3dfa2ea48c8e23e0795",
        "ghcr.io/ossf/scorecard@sha256:3f24714e9366917adb7a05635382c97dfecb14b21eaef3dfa2ea48c8e23e0795",
        "sha256:3f24714e9366917adb7a05635382c97dfecb14b21eaef3dfa2ea48c8e23e0795",
        "v5.5.0",
    ),
}


class BuildContextError(ValueError):
    """The effective Docker build context is not clean or stable."""


class SecureOutputError(ValueError):
    """A repo-support handoff path violates the no-follow output contract."""


def _dockerignore_rules(context_dir: pathlib.Path) -> list[tuple[bool, str, bool]]:
    path = context_dir / ".dockerignore"
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise BuildContextError("dockerignore-missing") from exc
    if tuple(lines) != SAMPLE_SERVICE_DOCKERIGNORE:
        raise BuildContextError("dockerignore-contract-invalid")
    rules: list[tuple[bool, str, bool]] = []
    for raw in lines:
        line = raw.strip()
        if not line or line.startswith("#") or line == ".":
            continue
        include = line.startswith("!")
        if include:
            line = line[1:]
        line = line.replace("\\", "/").lstrip("/")
        directory_only = line.endswith("/")
        line = line.rstrip("/")
        if line:
            rules.append((include, line, directory_only))
    if not rules:
        raise BuildContextError("dockerignore-empty")
    return rules


def _dockerignore_rule_matches(
    relative: str, is_directory: bool, pattern: str, directory_only: bool
) -> bool:
    if directory_only:
        if relative == pattern:
            return is_directory
        return relative.startswith(pattern + "/")
    if "/" not in pattern:
        return any(fnmatch.fnmatchcase(part, pattern) for part in relative.split("/"))
    return fnmatch.fnmatchcase(relative, pattern)


def _is_effective_context_path(
    relative: str,
    *,
    is_directory: bool,
    rules: list[tuple[bool, str, bool]],
) -> bool:
    if relative in {"Dockerfile", ".dockerignore"}:
        return True
    included = True
    for include, pattern, directory_only in rules:
        if _dockerignore_rule_matches(relative, is_directory, pattern, directory_only):
            included = include
    return included


def _git_lines(repo_root: pathlib.Path, arguments: list[str]) -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(repo_root), *arguments],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise BuildContextError("git-context-inspection-failed")
    return [line for line in result.stdout.splitlines() if line]


def _git_paths(repo_root: pathlib.Path, arguments: list[str]) -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(repo_root), *arguments],
        check=False,
        capture_output=True,
    )
    if result.returncode != 0:
        raise BuildContextError("git-context-inspection-failed")
    try:
        return [
            value.decode("utf-8")
            for value in result.stdout.split(b"\0")
            if value
        ]
    except UnicodeDecodeError as exc:
        raise BuildContextError("git-context-path-encoding-invalid") from exc


def _stable_material_stat(path_stat: os.stat_result) -> tuple[int, ...]:
    return (
        path_stat.st_dev,
        path_stat.st_ino,
        path_stat.st_size,
        path_stat.st_mtime_ns,
        path_stat.st_ctime_ns,
        stat.S_IMODE(path_stat.st_mode),
        path_stat.st_uid,
    )


def _read_regular_material(path: pathlib.Path) -> tuple[bytes, os.stat_result]:
    try:
        path_stat = path.lstat()
    except OSError as exc:
        raise BuildContextError("effective-context-material-missing") from exc
    if stat.S_ISLNK(path_stat.st_mode):
        raise BuildContextError("effective-context-symlink-forbidden")
    if not stat.S_ISREG(path_stat.st_mode):
        raise BuildContextError("effective-context-special-file-forbidden")
    try:
        descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    except OSError as exc:
        raise BuildContextError("effective-context-material-open-failed") from exc
    try:
        opened_stat = os.fstat(descriptor)
        if (
            not stat.S_ISREG(opened_stat.st_mode)
            or _stable_material_stat(opened_stat) != _stable_material_stat(path_stat)
        ):
            raise BuildContextError("effective-context-material-raced")
        chunks: list[bytes] = []
        while True:
            chunk = os.read(descriptor, 65536)
            if not chunk:
                break
            chunks.append(chunk)
        final_stat = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    try:
        current_stat = path.lstat()
    except OSError as exc:
        raise BuildContextError("effective-context-material-raced") from exc
    if (
        _stable_material_stat(opened_stat) != _stable_material_stat(final_stat)
        or _stable_material_stat(opened_stat) != _stable_material_stat(current_stat)
    ):
        raise BuildContextError("effective-context-material-raced")
    body = b"".join(chunks)
    if len(body) != opened_stat.st_size:
        raise BuildContextError("effective-context-material-raced")
    return body, opened_stat


def _deterministic_context_archive(
    materials: list[dict[str, Any]], bodies: dict[str, bytes]
) -> bytes:
    directory_names: set[str] = set()
    for material in materials:
        parent = pathlib.PurePosixPath(material["path"]).parent
        while parent != pathlib.PurePosixPath("."):
            directory_names.add(parent.as_posix())
            parent = parent.parent
    material_by_path = {material["path"]: material for material in materials}
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w", format=tarfile.USTAR_FORMAT) as bundle:
        entries = [
            *((name, True) for name in directory_names),
            *((material["path"], False) for material in materials),
        ]
        for name, is_directory in sorted(entries, key=lambda row: row[0].encode("utf-8")):
            info = tarfile.TarInfo(name=name)
            info.uid = 0
            info.gid = 0
            info.uname = ""
            info.gname = ""
            info.mtime = 0
            if is_directory:
                info.type = tarfile.DIRTYPE
                info.mode = 0o755
                bundle.addfile(info)
                continue
            material = material_by_path[name]
            body = bodies[name]
            info.mode = material["mode"]
            info.size = len(body)
            bundle.addfile(info, io.BytesIO(body))
    return buffer.getvalue()


def _capture_build_context_bundle(
    repo_root: pathlib.Path | str, context_relative: pathlib.Path | str
) -> tuple[dict[str, Any], bytes]:
    root = pathlib.Path(repo_root)
    relative_root = pathlib.PurePosixPath(str(context_relative).replace("\\", "/"))
    if relative_root.is_absolute() or ".." in relative_root.parts:
        raise BuildContextError("build-context-path-invalid")
    context_dir = root.joinpath(*relative_root.parts)
    try:
        context_stat = context_dir.lstat()
    except OSError as exc:
        raise BuildContextError("build-context-missing") from exc
    if not stat.S_ISDIR(context_stat.st_mode) or context_dir.is_symlink():
        raise BuildContextError("build-context-not-directory")
    rules = _dockerignore_rules(context_dir)

    materials: list[dict[str, Any]] = []
    bodies: dict[str, bytes] = {}
    for current, directories, files in os.walk(context_dir, followlinks=False):
        current_path = pathlib.Path(current)
        for name in sorted([*directories, *files]):
            path = current_path / name
            relative = path.relative_to(context_dir).as_posix()
            path_stat = path.lstat()
            is_directory = stat.S_ISDIR(path_stat.st_mode)
            if not _is_effective_context_path(
                relative, is_directory=is_directory, rules=rules
            ):
                continue
            if stat.S_ISLNK(path_stat.st_mode):
                raise BuildContextError("effective-context-symlink-forbidden")
            if is_directory:
                continue
            if not stat.S_ISREG(path_stat.st_mode):
                raise BuildContextError("effective-context-special-file-forbidden")
            body, opened_stat = _read_regular_material(path)
            bodies[relative] = body
            materials.append(
                {
                    "ctime_ns": opened_stat.st_ctime_ns,
                    "device": opened_stat.st_dev,
                    "inode": opened_stat.st_ino,
                    "mode": stat.S_IMODE(opened_stat.st_mode),
                    "mtime_ns": opened_stat.st_mtime_ns,
                    "path": relative,
                    "sha256": hashlib.sha256(body).hexdigest(),
                    "size": opened_stat.st_size,
                    "uid": opened_stat.st_uid,
                }
            )
    materials.sort(key=lambda row: row["path"].encode("utf-8"))
    if not materials:
        raise BuildContextError("effective-context-empty")

    context_prefix = relative_root.as_posix().rstrip("/") + "/"

    def to_context_path(repo_path: str) -> str | None:
        normalized = repo_path.replace("\\", "/")
        if not normalized.startswith(context_prefix):
            return None
        return normalized[len(context_prefix) :]

    modified = _git_lines(
        root, ["rev-parse", "HEAD"]
    )
    if len(modified) != 1 or not SHA1_RE.fullmatch(modified[0]):
        raise BuildContextError("source-revision-invalid")
    source_revision = modified[0]

    modified_paths = _git_paths(
        root,
        ["diff", "--name-only", "-z", "--diff-filter=ACDMRTUXB", "HEAD", "--", relative_root.as_posix()],
    )
    for repo_path in modified_paths:
        relative = to_context_path(repo_path)
        if relative and _is_effective_context_path(
            relative,
            is_directory=False,
            rules=rules,
        ):
            raise BuildContextError("tracked-effective-material-modified")

    tracked = set(
        _git_paths(
            root,
            ["ls-files", "-z", "--", relative_root.as_posix()],
        )
    )
    for material in materials:
        repo_path = f"{context_prefix}{material['path']}"
        if repo_path not in tracked:
            raise BuildContextError("untracked-effective-material")

    untracked = _git_paths(
        root,
        [
            "ls-files",
            "--others",
            "--ignored",
            "--exclude-standard",
            "-z",
            "--",
            relative_root.as_posix(),
        ],
    )
    for repo_path in untracked:
        relative = to_context_path(repo_path)
        if relative and _is_effective_context_path(
            relative,
            is_directory=False,
            rules=rules,
        ):
            raise BuildContextError("untracked-effective-material")

    archive = _deterministic_context_archive(materials, bodies)
    archive_sha256 = f"sha256:{hashlib.sha256(archive).hexdigest()}"
    return {
        "archive_sha256": archive_sha256,
        "build_context_sha256": archive_sha256,
        "context": relative_root.as_posix(),
        "generation": "hyhome-docker-build-context-v2",
        "materials": materials,
        "schema_version": 2,
        "source_revision": source_revision,
    }, archive


def capture_build_context_snapshot(
    repo_root: pathlib.Path | str, context_relative: pathlib.Path | str
) -> dict[str, Any]:
    snapshot, _ = _capture_build_context_bundle(repo_root, context_relative)
    return snapshot


def verify_build_context_snapshot(
    repo_root: pathlib.Path | str,
    context_relative: pathlib.Path | str,
    snapshot_path: pathlib.Path | str,
    archive_path: pathlib.Path | str | None = None,
) -> dict[str, Any]:
    try:
        expected = load_json(snapshot_path)
    except (OSError, json.JSONDecodeError) as exc:
        raise BuildContextError("build-context-snapshot-invalid") from exc
    actual, actual_archive = _capture_build_context_bundle(repo_root, context_relative)
    if actual != expected:
        raise BuildContextError("build-context-snapshot-mismatch")
    if archive_path is not None:
        archive = read_private_bytes(archive_path)
        if (
            archive != actual_archive
            or f"sha256:{hashlib.sha256(archive).hexdigest()}"
            != expected.get("archive_sha256")
        ):
            raise BuildContextError("build-context-archive-mismatch")
    return actual


def write_private_bytes(path: pathlib.Path | str, body: bytes) -> None:
    target = pathlib.Path(path)
    parent_stat = target.parent.lstat()
    if (
        not stat.S_ISDIR(parent_stat.st_mode)
        or target.parent.is_symlink()
        or parent_stat.st_uid != os.getuid()
        or stat.S_IMODE(parent_stat.st_mode) != 0o700
    ):
        raise SecureOutputError("private-parent-invalid")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW
    parent_fd = os.open(
        target.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    )
    try:
        descriptor = os.open(target.name, flags, 0o600, dir_fd=parent_fd)
        try:
            view = memoryview(body)
            while view:
                view = view[os.write(descriptor, view) :]
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
    finally:
        os.close(parent_fd)


def read_private_bytes(path: pathlib.Path | str) -> bytes:
    source = pathlib.Path(path)
    try:
        parent_stat = source.parent.lstat()
    except OSError as exc:
        raise SecureOutputError("private-parent-invalid") from exc
    if (
        not stat.S_ISDIR(parent_stat.st_mode)
        or source.parent.is_symlink()
        or parent_stat.st_uid != os.getuid()
        or stat.S_IMODE(parent_stat.st_mode) != 0o700
    ):
        raise SecureOutputError("private-parent-invalid")
    parent_fd = os.open(
        source.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    )
    try:
        descriptor = os.open(source.name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=parent_fd)
        try:
            source_stat = os.fstat(descriptor)
            if (
                not stat.S_ISREG(source_stat.st_mode)
                or source_stat.st_uid != os.getuid()
                or stat.S_IMODE(source_stat.st_mode) != 0o600
            ):
                raise SecureOutputError("private-source-invalid")
            chunks: list[bytes] = []
            while True:
                chunk = os.read(descriptor, 65536)
                if not chunk:
                    break
                chunks.append(chunk)
        finally:
            os.close(descriptor)
    except OSError as exc:
        raise SecureOutputError("private-source-invalid") from exc
    finally:
        os.close(parent_fd)
    return b"".join(chunks)


def write_private_json(path: pathlib.Path | str, payload: Any) -> None:
    body = (json.dumps(payload, sort_keys=True) + "\n").encode("utf-8")
    write_private_bytes(path, body)


def write_build_context_bundle(
    repo_root: pathlib.Path | str,
    context_relative: pathlib.Path | str,
    snapshot_path: pathlib.Path | str,
    archive_path: pathlib.Path | str,
) -> dict[str, Any]:
    snapshot, archive = _capture_build_context_bundle(repo_root, context_relative)
    write_private_bytes(archive_path, archive)
    write_private_json(snapshot_path, snapshot)
    return snapshot


def _validate_directory_stat(
    path_stat: os.stat_result, *, final: bool
) -> None:
    if not stat.S_ISDIR(path_stat.st_mode):
        raise SecureOutputError("output-ancestor-not-directory")
    if path_stat.st_uid != os.getuid():
        raise SecureOutputError("output-owner-invalid")
    mode = stat.S_IMODE(path_stat.st_mode)
    if final:
        if mode != 0o700:
            raise SecureOutputError("output-mode-invalid")
    elif mode & 0o022:
        raise SecureOutputError("output-ancestor-writable")


def _open_secure_output_directory(
    base: pathlib.Path | str,
    relative: pathlib.Path | str,
    *,
    create: bool,
) -> tuple[int, str]:
    root = pathlib.Path(base)
    relative_path = pathlib.PurePosixPath(str(relative).replace("\\", "/"))
    if (
        relative_path.is_absolute()
        or not relative_path.parts
        or any(part in {"", ".", ".."} for part in relative_path.parts)
    ):
        raise SecureOutputError("output-relative-path-invalid")
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    try:
        current_fd = os.open(root, flags)
    except OSError as exc:
        raise SecureOutputError("output-base-invalid") from exc
    try:
        _validate_directory_stat(os.fstat(current_fd), final=False)
        for index, component in enumerate(relative_path.parts):
            is_final = index == len(relative_path.parts) - 1
            try:
                next_fd = os.open(component, flags, dir_fd=current_fd)
            except FileNotFoundError:
                if not create:
                    raise SecureOutputError("output-directory-missing") from None
                try:
                    os.mkdir(component, 0o700, dir_fd=current_fd)
                    next_fd = os.open(component, flags, dir_fd=current_fd)
                    os.fchmod(next_fd, 0o700)
                except OSError as exc:
                    raise SecureOutputError("output-directory-create-failed") from exc
            except OSError as exc:
                raise SecureOutputError("output-ancestor-symlink-or-invalid") from exc
            os.close(current_fd)
            current_fd = next_fd
            if create and is_final:
                final_stat = os.fstat(current_fd)
                if (
                    stat.S_ISDIR(final_stat.st_mode)
                    and final_stat.st_uid == os.getuid()
                    and stat.S_IMODE(final_stat.st_mode) & 0o022 == 0
                ):
                    os.fchmod(current_fd, 0o700)
            _validate_directory_stat(os.fstat(current_fd), final=is_final)
        output_stat = os.fstat(current_fd)
        return current_fd, f"{output_stat.st_dev}:{output_stat.st_ino}"
    except Exception:
        os.close(current_fd)
        raise


def prepare_secure_output_directory(
    base: pathlib.Path | str, relative: pathlib.Path | str
) -> str:
    descriptor, identity = _open_secure_output_directory(
        base, relative, create=True
    )
    os.close(descriptor)
    return identity


def _validate_output_identity(descriptor: int, expected_identity: str) -> None:
    output_stat = os.fstat(descriptor)
    actual = f"{output_stat.st_dev}:{output_stat.st_ino}"
    if actual != expected_identity:
        raise SecureOutputError("output-identity-mismatch")


def _validate_existing_handoff(
    descriptor: int, name: str, *, require_private_mode: bool = True
) -> None:
    try:
        path_stat = os.stat(name, dir_fd=descriptor, follow_symlinks=False)
    except FileNotFoundError:
        return
    if not stat.S_ISREG(path_stat.st_mode):
        raise SecureOutputError("handoff-symlink-or-type-invalid")
    if path_stat.st_uid != os.getuid():
        raise SecureOutputError("handoff-owner-invalid")
    if require_private_mode and stat.S_IMODE(path_stat.st_mode) != 0o600:
        raise SecureOutputError("handoff-mode-invalid")


PAIR_HANDOFF_NAMES = (
    "verification-verdict.pair.json",
    "verification-verdict.baseline.json",
    "verification-verdict.candidate.json",
)
MINIMIZED_HANDOFF_NAMES = (
    "advisory-summary.baseline.json",
    "advisory-summary.candidate.json",
)


def invalidate_secure_handoffs(
    base: pathlib.Path | str,
    relative: pathlib.Path | str,
    expected_identity: str,
) -> None:
    descriptor, _ = _open_secure_output_directory(base, relative, create=False)
    names = (*PAIR_HANDOFF_NAMES, *MINIMIZED_HANDOFF_NAMES)
    try:
        _validate_output_identity(descriptor, expected_identity)
        for name in names:
            _validate_existing_handoff(
                descriptor, name, require_private_mode=False
            )
        for name in names:
            try:
                os.unlink(name, dir_fd=descriptor)
            except FileNotFoundError:
                pass
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _read_private_handoff(path: pathlib.Path | str) -> tuple[bytes, Any]:
    source = pathlib.Path(path)
    try:
        parent_stat = source.parent.lstat()
    except OSError as exc:
        raise SecureOutputError("private-source-parent-invalid") from exc
    if (
        not stat.S_ISDIR(parent_stat.st_mode)
        or source.parent.is_symlink()
        or parent_stat.st_uid != os.getuid()
        or stat.S_IMODE(parent_stat.st_mode) != 0o700
    ):
        raise SecureOutputError("private-source-parent-invalid")
    parent_fd = os.open(
        source.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    )
    try:
        descriptor = os.open(source.name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=parent_fd)
        try:
            source_stat = os.fstat(descriptor)
            if (
                not stat.S_ISREG(source_stat.st_mode)
                or source_stat.st_uid != os.getuid()
                or stat.S_IMODE(source_stat.st_mode) != 0o600
            ):
                raise SecureOutputError("private-source-invalid")
            chunks: list[bytes] = []
            while True:
                chunk = os.read(descriptor, 65536)
                if not chunk:
                    break
                chunks.append(chunk)
        finally:
            os.close(descriptor)
    except OSError as exc:
        raise SecureOutputError("private-source-invalid") from exc
    finally:
        os.close(parent_fd)
    body = b"".join(chunks)
    try:
        payload = json.loads(body)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SecureOutputError("private-source-json-invalid") from exc
    return body, payload


def _atomic_write_at(descriptor: int, name: str, body: bytes) -> None:
    temporary = f".{name}.{secrets.token_hex(8)}.tmp"
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW
    temporary_fd = os.open(temporary, flags, 0o600, dir_fd=descriptor)
    try:
        os.fchmod(temporary_fd, 0o600)
        view = memoryview(body)
        while view:
            view = view[os.write(temporary_fd, view) :]
        os.fsync(temporary_fd)
    except Exception:
        try:
            os.unlink(temporary, dir_fd=descriptor)
        except FileNotFoundError:
            pass
        raise
    finally:
        os.close(temporary_fd)
    try:
        os.replace(
            temporary,
            name,
            src_dir_fd=descriptor,
            dst_dir_fd=descriptor,
        )
    except Exception:
        try:
            os.unlink(temporary, dir_fd=descriptor)
        except FileNotFoundError:
            pass
        raise


def publish_verdict_pair(
    base: pathlib.Path | str,
    relative: pathlib.Path | str,
    expected_identity: str,
    baseline_path: pathlib.Path | str,
    candidate_path: pathlib.Path | str,
    source_revision: str,
    build_context_sha256: str,
) -> dict[str, Any]:
    if not SHA1_RE.fullmatch(source_revision):
        raise SecureOutputError("pair-source-revision-invalid")
    if not SHA256_RE.fullmatch(build_context_sha256):
        raise SecureOutputError("pair-build-context-invalid")
    sources = {
        "baseline": _read_private_handoff(baseline_path),
        "candidate": _read_private_handoff(candidate_path),
    }
    for role, (_, payload) in sources.items():
        local_ref = payload.get("local_image_ref") if isinstance(payload, dict) else None
        local_match = (
            LOCAL_IMAGE_REF_RE.fullmatch(local_ref)
            if isinstance(local_ref, str)
            else None
        )
        runtime_kind = (
            payload.get("runtime_identity_kind")
            if isinstance(payload, dict)
            else None
        )
        runtime_id = payload.get("runtime_image_id") if isinstance(payload, dict) else None
        config_digest = (
            payload.get("image_config_digest") if isinstance(payload, dict) else None
        )
        if (
            not isinstance(payload, dict)
            or set(payload) != VERIFICATION_VERDICT_KEYS
            or payload.get("schema_version") != 2
            or payload.get("role") != role
            or payload.get("verdict") != "accepted"
            or payload.get("exception_id") is not None
            or payload.get("source_revision") != source_revision
            or payload.get("build_context_sha256") != build_context_sha256
            or payload.get("policy_id") != "sample-service-local-v1"
            or payload.get("producer_spec")
            != "spec:126-security-supply-chain-remediation"
            or payload.get("redaction_status") != "passed"
            or not re.fullmatch(
                r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z",
                str(payload.get("verified_at", "")),
            )
            or not SHA256_RE.fullmatch(
                str(payload.get("oci_manifest_digest", ""))
            )
            or not SHA256_RE.fullmatch(str(payload.get("image_config_digest", "")))
            or not SHA256_RE.fullmatch(str(payload.get("oci_archive_sha256", "")))
            or not SHA256_RE.fullmatch(
                str(payload.get("docker_archive_sha256", ""))
            )
            or not SHA256_RE.fullmatch(str(runtime_id))
            or local_match is None
            or local_match.group(1) != role
            or local_match.group(2)
            != str(config_digest).removeprefix("sha256:")
            or runtime_kind not in {"config-digest", "docker-target-digest"}
            or (runtime_kind == "config-digest" and runtime_id != config_digest)
            or (runtime_kind == "docker-target-digest" and runtime_id == config_digest)
        ):
            raise SecureOutputError("pair-verdict-invalid")
    for field in VERDICT_IDENTITY_KEYS:
        if field == "runtime_identity_kind":
            continue
        if sources["baseline"][1][field] == sources["candidate"][1][field]:
            raise SecureOutputError("pair-subjects-not-distinct")
    manifest = {
        "build_context_sha256": build_context_sha256,
        "generation": "hyhome-verification-verdict-pair-v3",
        "schema_version": 3,
        "source_revision": source_revision,
        "subjects": {
            role: {
                field: sources[role][1][field]
                for field in VERDICT_IDENTITY_KEYS
            }
            for role in ("baseline", "candidate")
        },
        "verdict_sha256": {
            role: f"sha256:{hashlib.sha256(body).hexdigest()}"
            for role, (body, _) in sources.items()
        },
    }
    manifest_body = (json.dumps(manifest, sort_keys=True) + "\n").encode("utf-8")
    descriptor, _ = _open_secure_output_directory(base, relative, create=False)
    try:
        _validate_output_identity(descriptor, expected_identity)
        for name in PAIR_HANDOFF_NAMES:
            _validate_existing_handoff(descriptor, name)
        try:
            try:
                os.unlink("verification-verdict.pair.json", dir_fd=descriptor)
            except FileNotFoundError:
                pass
            os.fsync(descriptor)
            for role in ("baseline", "candidate"):
                _atomic_write_at(
                    descriptor,
                    f"verification-verdict.{role}.json",
                    sources[role][0],
                )
            _atomic_write_at(
                descriptor,
                "verification-verdict.pair.json",
                manifest_body,
            )
            os.fsync(descriptor)
        except Exception:
            for name in PAIR_HANDOFF_NAMES:
                try:
                    os.unlink(name, dir_fd=descriptor)
                except FileNotFoundError:
                    pass
            os.fsync(descriptor)
            raise
    finally:
        os.close(descriptor)
    return manifest


def publish_minimized_handoff(
    base: pathlib.Path | str,
    relative: pathlib.Path | str,
    expected_identity: str,
    name: str,
    source_path: pathlib.Path | str,
) -> None:
    if name not in MINIMIZED_HANDOFF_NAMES:
        raise SecureOutputError("minimized-handoff-name-invalid")
    body, payload = _read_private_handoff(source_path)
    expected_role = name.removeprefix("advisory-summary.").removesuffix(".json")
    allowed_keys = {
        "build_context_sha256",
        "database",
        "exception_id",
        "image_config_digest",
        "oci_archive_sha256",
        "policy_id",
        "reason",
        "redaction_status",
        "role",
        "schema_version",
        "source_revision",
        "verdict",
        "vulnerability_counts",
    }
    allowed_database_keys = {
        "built",
        "database_package_sha256",
        "schema",
        "schema_version",
        "status",
    }
    database = payload.get("database") if isinstance(payload, dict) else None
    counts = payload.get("vulnerability_counts") if isinstance(payload, dict) else None
    if (
        not isinstance(payload, dict)
        or set(payload) != allowed_keys
        or payload.get("schema_version") != 1
        or payload.get("redaction_status") != "passed"
        or payload.get("role") != expected_role
        or payload.get("verdict") not in {"accepted", "rejected"}
        or not SHA1_RE.fullmatch(str(payload.get("source_revision", "")))
        or not SHA256_RE.fullmatch(str(payload.get("build_context_sha256", "")))
        or not SHA256_RE.fullmatch(str(payload.get("image_config_digest", "")))
        or not SHA256_RE.fullmatch(str(payload.get("oci_archive_sha256", "")))
        or not isinstance(database, dict)
        or set(database) != allowed_database_keys
        or not isinstance(counts, dict)
        or any(
            severity not in {"negligible", "unknown", "low", "medium", "high", "critical"}
            or isinstance(count, bool)
            or not isinstance(count, int)
            or count < 0
            for severity, count in counts.items()
        )
    ):
        raise SecureOutputError("minimized-handoff-invalid")
    descriptor, _ = _open_secure_output_directory(base, relative, create=False)
    try:
        _validate_output_identity(descriptor, expected_identity)
        _validate_existing_handoff(descriptor, name)
        _atomic_write_at(descriptor, name, body)
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def load_json(path: pathlib.Path | str) -> Any:
    with pathlib.Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def _is_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _valid_date(value: Any) -> bool:
    if not _is_text(value):
        return False
    try:
        dt.date.fromisoformat(value)
    except ValueError:
        return False
    return True


def _exception_errors(exception: Any) -> list[str]:
    if not isinstance(exception, dict):
        return ["exception-row-invalid"]
    required = (
        "id",
        "subject_digest",
        "package",
        "vulnerability_id",
        "severity",
        "owner_role",
        "reason",
        "expires_on",
        "compensating_control",
        "approval_reference",
    )
    errors = ["exception-field-missing" for key in required if not _is_text(exception.get(key))]
    if not SHA256_RE.fullmatch(str(exception.get("subject_digest", ""))):
        errors.append("exception-subject-digest-invalid")
    if not _is_text(exception.get("owner_role")):
        errors.append("exception-owner-invalid")
    if not _is_text(exception.get("approval_reference")):
        errors.append("exception-approval-invalid")
    if not _valid_date(exception.get("expires_on")):
        errors.append("exception-expiry-invalid")
    elif dt.date.fromisoformat(exception["expires_on"]) < dt.date.today():
        errors.append("exception-expired")
    return sorted(set(errors))


def validate_tool_registry(registry: Any) -> list[str]:
    if not isinstance(registry, dict):
        return ["tool-registry-invalid"]
    errors: list[str] = []
    if registry.get("schema_version") != 2:
        errors.append("tool-schema-version-invalid")
    for field in ("policy_id", "effective_date", "owner_role"):
        if not _is_text(registry.get(field)):
            errors.append(f"tool-registry-{field}-invalid")
    if not _valid_date(registry.get("effective_date")):
        errors.append("tool-registry-effective-date-invalid")
    tools = registry.get("tools")
    if not isinstance(tools, list) or len(tools) != len(TOOL_PINS):
        return sorted(set(errors + ["tool-registry-tool-set-invalid"]))
    by_name = {row.get("name"): row for row in tools if isinstance(row, dict)}
    if set(by_name) != set(TOOL_PINS):
        errors.append("tool-registry-tool-set-invalid")
    for name, expected in TOOL_PINS.items():
        row = by_name.get(name)
        if not isinstance(row, dict):
            continue
        image, digest, repo_digest, config_id, version = expected
        if row.get("image") != image:
            errors.append("tool-image-pin-invalid")
        if row.get("digest") != digest or not SHA256_RE.fullmatch(str(row.get("digest", ""))):
            errors.append("tool-digest-invalid")
        if row.get("repo_digest") != repo_digest:
            errors.append("tool-repo-digest-invalid")
        if row.get("config_id") != config_id or not SHA256_RE.fullmatch(
            str(row.get("config_id", ""))
        ):
            errors.append("tool-config-id-invalid")
        if row.get("expected_version") != version:
            errors.append("tool-version-invalid")
        for field in ("command_contract", "network_mode"):
            if not _is_text(row.get(field)):
                errors.append(f"tool-{field}-invalid")
    return sorted(set(errors))


def validate_policy(policy: Any) -> list[str]:
    if not isinstance(policy, dict):
        return ["policy-invalid"]
    errors: list[str] = []
    if policy.get("schema_version") != 1:
        errors.append("policy-schema-version-invalid")
    if policy.get("policy_id") != "sample-service-local-v1":
        errors.append("policy-id-invalid")
    subject = policy.get("subject")
    if not isinstance(subject, dict) or subject.get("service") != "examples/sample-web-service":
        errors.append("policy-subject-service-invalid")
    elif subject.get("roles") != ["baseline", "candidate"]:
        errors.append("policy-subject-roles-invalid")
    if policy.get("sbom") != {"format": "cyclonedx-json"}:
        errors.append("policy-sbom-invalid")
    vulnerability = policy.get("vulnerability")
    if not isinstance(vulnerability, dict):
        errors.append("policy-vulnerability-invalid")
    else:
        if vulnerability.get("blocking_severities") != ["critical"]:
            errors.append("policy-blocking-severities-invalid")
        if vulnerability.get("review_severities") != ["high"]:
            errors.append("policy-review-severities-invalid")
        if vulnerability.get("exception_registry") != "infra/supply-chain.vulnerability-exceptions.json":
            errors.append("policy-exception-registry-invalid")
    if policy.get("provenance") != {"predicate_type": "https://slsa.dev/provenance/v1"}:
        errors.append("policy-provenance-invalid")
    if policy.get("signature") != {"mode": "cosign-sign-blob", "key_lifetime": "process"}:
        errors.append("policy-signature-invalid")
    if policy.get("scorecard") != {"mode": "read-only-advisory"}:
        errors.append("policy-scorecard-invalid")
    if policy.get("ci_enforcement") != "fixture-policy-only":
        errors.append("policy-ci-enforcement-invalid")
    return sorted(set(errors))


def validate_exceptions(
    registry: Any, policy: Any, expected_subject_digest: str | None = None
) -> list[str]:
    if not isinstance(registry, dict) or registry.get("schema_version") != 1:
        return ["exception-registry-invalid"]
    if validate_policy(policy):
        return ["exception-policy-invalid"]
    rows = registry.get("exceptions")
    if not isinstance(rows, list):
        return ["exception-rows-invalid"]
    errors: list[str] = []
    ids: set[str] = set()
    for row in rows:
        errors.extend(_exception_errors(row))
        if isinstance(row, dict):
            identifier = row.get("id")
            if identifier in ids:
                errors.append("exception-id-duplicate")
            if isinstance(identifier, str):
                ids.add(identifier)
    if expected_subject_digest is not None and not SHA256_RE.fullmatch(expected_subject_digest):
        errors.append("exception-expected-subject-invalid")
    return sorted(set(errors))


def validate_subject_tuples(subjects: Any) -> list[str]:
    if not isinstance(subjects, list) or len(subjects) != 2:
        return ["subject-tuples-cardinality-invalid"]
    errors: list[str] = []
    roles: set[str] = set()
    pairs: set[tuple[str, str]] = set()
    revisions: set[str] = set()
    for subject in subjects:
        if not isinstance(subject, dict):
            errors.append("subject-tuple-invalid")
            continue
        role = subject.get("role")
        image = subject.get("image_config_digest")
        archive = subject.get("oci_archive_sha256")
        revision = subject.get("source_revision")
        if role not in {"baseline", "candidate"}:
            errors.append("subject-role-invalid")
        else:
            roles.add(role)
        if not SHA256_RE.fullmatch(str(image)):
            errors.append("subject-image-config-digest-invalid")
        if not SHA256_RE.fullmatch(str(archive)):
            errors.append("subject-oci-archive-digest-invalid")
        if not SHA1_RE.fullmatch(str(revision)):
            errors.append("subject-source-revision-invalid")
        else:
            revisions.add(revision)
        pairs.add((str(image), str(archive)))
    if roles != {"baseline", "candidate"}:
        errors.append("subject-roles-invalid")
    if len(pairs) != 2:
        errors.append("subject-tuples-not-distinct")
    if len(revisions) != 1:
        errors.append("subject-source-revision-mismatch")
    return sorted(set(errors))


def _properties(component: Any) -> dict[str, Any]:
    if not isinstance(component, dict):
        return {}
    rows = component.get("properties")
    if not isinstance(rows, list):
        return {}
    return {
        row.get("name"): row.get("value")
        for row in rows
        if isinstance(row, dict) and isinstance(row.get("name"), str)
    }


def _unique_json_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("json-key-duplicate")
        result[key] = value
    return result


def _parse_json_object(content: bytes, reason: str) -> dict[str, Any]:
    try:
        value = json.loads(content, object_pairs_hook=_unique_json_object)
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise ValueError(reason) from exc
    if not isinstance(value, dict):
        raise ValueError(reason)
    return value


def _require_oci_descriptor(
    value: Any, *, prefix: str
) -> tuple[str, int, str]:
    if not isinstance(value, dict):
        raise ValueError(f"{prefix}-descriptor-invalid")
    digest = value.get("digest")
    size = value.get("size")
    media_type = value.get("mediaType")
    if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
        raise ValueError(f"{prefix}-digest-invalid")
    if isinstance(size, bool) or not isinstance(size, int) or size < 0:
        raise ValueError(f"{prefix}-size-invalid")
    if not isinstance(media_type, str) or not media_type:
        raise ValueError(f"{prefix}-media-type-invalid")
    return digest, size, media_type


def _verify_oci_gzip_layer_diff_id(
    blob: bytes,
    expected_diff_id: str,
    *,
    prior_uncompressed_bytes: int,
) -> int:
    """Stream one strict gzip member and verify its uncompressed DiffID."""

    decompressor = zlib.decompressobj(16 + zlib.MAX_WBITS)
    digest = hashlib.sha256()
    uncompressed_bytes = 0

    def consume(output: bytes) -> None:
        nonlocal uncompressed_bytes
        uncompressed_bytes += len(output)
        if uncompressed_bytes > OCI_LAYER_MAX_UNCOMPRESSED_BYTES:
            raise ValueError("oci-layer-uncompressed-size-limit-exceeded")
        if (
            prior_uncompressed_bytes + uncompressed_bytes
            > OCI_LAYERS_MAX_UNCOMPRESSED_BYTES
        ):
            raise ValueError("oci-layers-uncompressed-size-limit-exceeded")
        digest.update(output)

    offset = 0
    while offset < len(blob) and not decompressor.eof:
        pending = blob[offset : offset + OCI_DECOMPRESSION_CHUNK_BYTES]
        offset += len(pending)
        while pending and not decompressor.eof:
            previous_size = len(pending)
            try:
                output = decompressor.decompress(
                    pending, OCI_DECOMPRESSION_CHUNK_BYTES
                )
            except zlib.error as exc:
                raise ValueError("oci-layer-gzip-invalid") from exc
            pending = decompressor.unconsumed_tail
            consume(output)
            if decompressor.eof:
                if decompressor.unused_data or pending or offset < len(blob):
                    raise ValueError("oci-layer-gzip-trailing-data")
                break
            if pending and len(pending) == previous_size and not output:
                raise ValueError("oci-layer-gzip-invalid")

    if not decompressor.eof:
        raise ValueError("oci-layer-gzip-invalid")
    actual_diff_id = f"sha256:{digest.hexdigest()}"
    if actual_diff_id != expected_diff_id:
        raise ValueError("oci-layer-diff-id-mismatch")
    return uncompressed_bytes


def _parse_bounded_pax_decimal(
    content: bytes,
    start: int,
    end: int,
    *,
    maximum: int,
    invalid_reason: str,
    limit_reason: str,
) -> int:
    """Parse a bounded unsigned PAX decimal without a large temporary int."""

    if start >= end:
        raise ValueError(invalid_reason)
    value = 0
    for index in range(start, end):
        byte = content[index]
        if byte < ord("0") or byte > ord("9"):
            raise ValueError(invalid_reason)
        digit = byte - ord("0")
        if value > (maximum - digit) // 10:
            raise ValueError(limit_reason)
        value = value * 10 + digit
    return value


def _preflight_pax_payload(
    content: bytes, payload_start: int, payload_size: int
) -> None:
    """Validate bounded PAX framing and allocation-relevant keys."""

    invalid_reason = "oci-archive-pax-header-invalid"
    payload_end = payload_start + payload_size
    record_start = payload_start
    sparse_prefix = b"GNU.sparse"
    size_key = b"size"
    length_digits_max = len(str(payload_size))

    while record_start < payload_end:
        length_end = content.find(b" ", record_start, payload_end)
        if length_end <= record_start:
            raise ValueError(invalid_reason)
        remaining = payload_end - record_start
        if length_end - record_start > length_digits_max:
            raise ValueError(invalid_reason)
        record_size = _parse_bounded_pax_decimal(
            content,
            record_start,
            length_end,
            maximum=remaining,
            invalid_reason=invalid_reason,
            limit_reason=invalid_reason,
        )
        if record_size < 5:
            raise ValueError(invalid_reason)
        record_end = record_start + record_size
        if record_end > payload_end or content[record_end - 1] != ord("\n"):
            raise ValueError(invalid_reason)

        key_start = length_end + 1
        value_end = record_end - 1
        equals = content.find(b"=", key_start, value_end)
        if equals <= key_start:
            raise ValueError(invalid_reason)

        key_size = equals - key_start
        if (
            key_size == len(sparse_prefix)
            and content.startswith(sparse_prefix, key_start, equals)
        ) or (
            key_size > len(sparse_prefix)
            and content.startswith(sparse_prefix, key_start, equals)
            and content[key_start + len(sparse_prefix)] == ord(".")
        ):
            raise ValueError("oci-archive-sparse-type-invalid")

        if key_size == len(size_key) and content.startswith(
            size_key, key_start, equals
        ):
            _parse_bounded_pax_decimal(
                content,
                equals + 1,
                value_end,
                maximum=OCI_ARCHIVE_MAX_BYTES,
                invalid_reason=invalid_reason,
                limit_reason="oci-archive-member-size-limit-exceeded",
            )

        record_start = record_end


def _preflight_uncompressed_oci_tar(content: bytes) -> None:
    """Bound raw tar records before tarfile can consume hidden metadata."""

    block_size = tarfile.BLOCKSIZE
    zero_block = b"\0" * block_size
    if len(content) < block_size * 2 or len(content) % block_size != 0:
        raise ValueError("oci-archive-truncated-or-misaligned")

    allowed_member_types = {
        tarfile.REGTYPE,
        tarfile.AREGTYPE,
        tarfile.DIRTYPE,
    }
    pax_types = {
        tarfile.XHDTYPE,
        tarfile.XGLTYPE,
        tarfile.SOLARIS_XHDTYPE,
    }
    longname_types = {tarfile.GNUTYPE_LONGNAME, tarfile.GNUTYPE_LONGLINK}
    hidden_metadata_bytes = 0
    offset = 0

    while offset < len(content):
        header = content[offset : offset + block_size]
        if header == zero_block:
            second_end = offset + 2 * block_size
            if (
                second_end > len(content)
                or content[offset + block_size : second_end] != zero_block
            ):
                raise ValueError("oci-archive-termination-invalid")
            if content.count(b"\0", second_end) != len(content) - second_end:
                raise ValueError("oci-archive-trailing-data-invalid")
            return

        try:
            member = tarfile.TarInfo.frombuf(
                header, encoding="utf-8", errors="surrogateescape"
            )
        except tarfile.HeaderError as exc:
            raise ValueError("oci-archive-header-invalid") from exc

        if (
            isinstance(member.size, bool)
            or not isinstance(member.size, int)
            or member.size < 0
        ):
            raise ValueError("oci-archive-member-size-invalid")
        if member.size > OCI_ARCHIVE_MAX_BYTES:
            raise ValueError("oci-archive-member-size-limit-exceeded")

        payload_start = offset + block_size
        payload_end = payload_start + member.size
        padded_size = ((member.size + block_size - 1) // block_size) * block_size
        next_offset = payload_start + padded_size

        if member.type in pax_types:
            if (
                member.size > OCI_METADATA_MAX_BYTES
                or hidden_metadata_bytes + member.size
                > OCI_METADATA_MAX_BYTES
            ):
                raise ValueError(
                    "oci-archive-pax-metadata-size-limit-exceeded"
                )
            if next_offset > len(content):
                raise ValueError("oci-archive-truncated")
            _preflight_pax_payload(content, payload_start, member.size)
            hidden_metadata_bytes += member.size
        elif member.type in longname_types:
            raise ValueError("oci-archive-longname-type-invalid")
        elif member.type == tarfile.GNUTYPE_SPARSE:
            raise ValueError("oci-archive-sparse-type-invalid")
        elif member.type not in allowed_member_types:
            raise ValueError("oci-archive-member-type-invalid")

        if next_offset > len(content):
            raise ValueError("oci-archive-truncated")
        if (
            content.count(b"\0", payload_end, next_offset)
            != next_offset - payload_end
        ):
            raise ValueError("oci-archive-padding-invalid")
        offset = next_offset

    raise ValueError("oci-archive-termination-invalid")


def _inspect_oci_archive_bytes(content: bytes) -> dict[str, Any]:
    if len(content) > OCI_ARCHIVE_MAX_BYTES:
        raise ValueError("oci-archive-size-limit-exceeded")
    if any(content.startswith(magic) for magic in OCI_OUTER_COMPRESSION_MAGICS):
        raise ValueError("oci-archive-outer-compression-invalid")
    _preflight_uncompressed_oci_tar(content)
    try:
        archive = tarfile.open(fileobj=io.BytesIO(content), mode="r:")
    except (OSError, tarfile.TarError) as exc:
        raise ValueError("oci-archive-invalid") from exc
    with archive:
        members: dict[str, tarfile.TarInfo] = {}
        try:
            for member in archive:
                if member.size < 0 or member.size > OCI_ARCHIVE_MAX_BYTES:
                    raise ValueError(
                        "oci-archive-member-size-limit-exceeded"
                    )
                name = member.name
                path = pathlib.PurePosixPath(name)
                if (
                    not name
                    or name.startswith("/")
                    or "\\" in name
                    or path.is_absolute()
                    or path.as_posix() != name.rstrip("/")
                    or any(part in {"", ".", ".."} for part in path.parts)
                ):
                    raise ValueError("oci-archive-member-path-invalid")
                if name in members:
                    raise ValueError("oci-archive-member-duplicate")
                if not member.isfile() and not member.isdir():
                    raise ValueError("oci-archive-member-type-invalid")
                members[name] = member
        except ValueError:
            raise
        except (OSError, tarfile.TarError) as exc:
            raise ValueError("oci-archive-invalid") from exc

        def read_member(
            name: str,
            reason: str,
            *,
            max_bytes: int = OCI_ARCHIVE_MAX_BYTES,
        ) -> bytes:
            member = members.get(name)
            if member is None or not member.isfile():
                raise ValueError(reason)
            if member.size < 0 or member.size > max_bytes:
                raise ValueError("oci-archive-member-size-limit-exceeded")
            try:
                handle = archive.extractfile(member)
            except (OSError, tarfile.TarError) as exc:
                raise ValueError(reason) from exc
            if handle is None:
                raise ValueError(reason)
            chunks: list[bytes] = []
            remaining = member.size
            try:
                while remaining:
                    chunk = handle.read(min(remaining, 1024 * 1024))
                    if not chunk:
                        raise ValueError(reason)
                    remaining -= len(chunk)
                    chunks.append(chunk)
            except (OSError, tarfile.TarError) as exc:
                raise ValueError(reason) from exc
            return b"".join(chunks)

        index = _parse_json_object(
            read_member(
                "index.json",
                "oci-index-missing",
                max_bytes=OCI_METADATA_MAX_BYTES,
            ),
            "oci-index-invalid",
        )
        if (
            index.get("schemaVersion") != 2
            or index.get("mediaType") != OCI_INDEX_MEDIA_TYPE
        ):
            raise ValueError("oci-index-schema-or-media-type-invalid")
        manifests = index.get("manifests")
        if (
            not isinstance(manifests, list)
            or len(manifests) != 1
            or not isinstance(manifests[0], dict)
        ):
            raise ValueError("oci-index-manifest-cardinality-invalid")
        manifest_digest, manifest_size, manifest_media_type = _require_oci_descriptor(
            manifests[0], prefix="oci-index-manifest"
        )
        if manifest_media_type != OCI_MANIFEST_MEDIA_TYPE:
            raise ValueError("oci-index-manifest-media-type-invalid")
        manifest_blob = read_member(
            f"blobs/sha256/{manifest_digest.removeprefix('sha256:')}",
            "oci-manifest-blob-missing",
            max_bytes=OCI_METADATA_MAX_BYTES,
        )
        if len(manifest_blob) != manifest_size:
            raise ValueError("oci-manifest-blob-size-mismatch")
        if (
            hashlib.sha256(manifest_blob).hexdigest()
            != manifest_digest.removeprefix("sha256:")
        ):
            raise ValueError("oci-manifest-blob-digest-mismatch")
        manifest = _parse_json_object(manifest_blob, "oci-manifest-invalid")
        if (
            manifest.get("schemaVersion") != 2
            or manifest.get("mediaType") != OCI_MANIFEST_MEDIA_TYPE
        ):
            raise ValueError("oci-manifest-schema-or-media-type-invalid")

        config_digest, config_size, config_media_type = _require_oci_descriptor(
            manifest.get("config"), prefix="oci-config"
        )
        if config_media_type != OCI_CONFIG_MEDIA_TYPE:
            raise ValueError("oci-config-media-type-invalid")
        config_blob = read_member(
            f"blobs/sha256/{config_digest.removeprefix('sha256:')}",
            "oci-config-blob-missing",
            max_bytes=OCI_METADATA_MAX_BYTES,
        )
        if len(config_blob) != config_size:
            raise ValueError("oci-config-blob-size-mismatch")
        if (
            hashlib.sha256(config_blob).hexdigest()
            != config_digest.removeprefix("sha256:")
        ):
            raise ValueError("oci-config-blob-digest-mismatch")
        config = _parse_json_object(config_blob, "oci-config-blob-invalid")
        rootfs = config.get("rootfs")
        diff_ids = rootfs.get("diff_ids") if isinstance(rootfs, dict) else None
        if (
            not isinstance(config.get("architecture"), str)
            or not config["architecture"]
            or not isinstance(config.get("os"), str)
            or not config["os"]
            or not isinstance(rootfs, dict)
            or rootfs.get("type") != "layers"
            or not isinstance(diff_ids, list)
            or any(
                not isinstance(diff_id, str) or not SHA256_RE.fullmatch(diff_id)
                for diff_id in diff_ids
            )
        ):
            raise ValueError("oci-config-rootfs-invalid")

        raw_layers = manifest.get("layers")
        if not isinstance(raw_layers, list):
            raise ValueError("oci-layers-invalid")
        if len(raw_layers) != len(diff_ids):
            raise ValueError("oci-rootfs-layer-cardinality-mismatch")
        layers: list[dict[str, Any]] = []
        total_uncompressed_bytes = 0
        for index, raw_layer in enumerate(raw_layers):
            layer_digest, layer_size, media_type = _require_oci_descriptor(
                raw_layer, prefix="oci-layer"
            )
            if media_type not in OCI_PORTABLE_LAYER_MEDIA_TYPES:
                raise ValueError("oci-layer-media-type-not-portable")
            layer_blob = read_member(
                f"blobs/sha256/{layer_digest.removeprefix('sha256:')}",
                "oci-layer-blob-missing",
            )
            if len(layer_blob) != layer_size:
                raise ValueError("oci-layer-blob-size-mismatch")
            if (
                hashlib.sha256(layer_blob).hexdigest()
                != layer_digest.removeprefix("sha256:")
            ):
                raise ValueError("oci-layer-blob-digest-mismatch")
            uncompressed_bytes = _verify_oci_gzip_layer_diff_id(
                layer_blob,
                diff_ids[index],
                prior_uncompressed_bytes=total_uncompressed_bytes,
            )
            total_uncompressed_bytes += uncompressed_bytes
            layers.append(
                {
                    "blob": layer_blob,
                    "digest": layer_digest,
                    "media_type": media_type,
                    "uncompressed_size": uncompressed_bytes,
                }
            )
    return {
        "config_blob": config_blob,
        "image_config_digest": config_digest,
        "layers": layers,
        "oci_manifest_digest": manifest_digest,
    }


def inspect_oci_archive_config_digest(archive_path: pathlib.Path | str) -> str:
    """Return the config digest cryptographically bound by an OCI archive index."""

    try:
        content = _read_stable_private_bytes(
            pathlib.Path(archive_path), max_bytes=OCI_ARCHIVE_MAX_BYTES
        )
    except SecureOutputError as exc:
        if str(exc) == "private-source-size-limit-exceeded":
            raise ValueError("oci-archive-size-limit-exceeded") from exc
        raise ValueError("oci-archive-private-input-invalid") from exc
    return str(_inspect_oci_archive_bytes(content)["image_config_digest"])


def _read_stable_private_bytes(
    path: pathlib.Path, *, max_bytes: int | None = None
) -> bytes:
    try:
        parent_stat = path.parent.lstat()
    except OSError as exc:
        raise SecureOutputError("private-parent-invalid") from exc
    if (
        not stat.S_ISDIR(parent_stat.st_mode)
        or path.parent.is_symlink()
        or parent_stat.st_uid != os.getuid()
        or stat.S_IMODE(parent_stat.st_mode) != 0o700
    ):
        raise SecureOutputError("private-parent-invalid")
    parent_fd = os.open(
        path.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    )
    try:
        opened_parent = os.fstat(parent_fd)
        if (opened_parent.st_dev, opened_parent.st_ino) != (
            parent_stat.st_dev,
            parent_stat.st_ino,
        ):
            raise SecureOutputError("private-parent-raced")
        descriptor = os.open(
            path.name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=parent_fd
        )
        try:
            before = os.fstat(descriptor)
            if (
                not stat.S_ISREG(before.st_mode)
                or before.st_uid != os.getuid()
                or stat.S_IMODE(before.st_mode) != 0o600
            ):
                raise SecureOutputError("private-source-invalid")
            if max_bytes is not None and before.st_size > max_bytes:
                raise SecureOutputError("private-source-size-limit-exceeded")
            chunks: list[bytes] = []
            bytes_read = 0
            while True:
                chunk = os.read(descriptor, 1024 * 1024)
                if not chunk:
                    break
                bytes_read += len(chunk)
                if max_bytes is not None and bytes_read > max_bytes:
                    raise SecureOutputError(
                        "private-source-size-limit-exceeded"
                    )
                chunks.append(chunk)
            after = os.fstat(descriptor)
            current = os.stat(path.name, dir_fd=parent_fd, follow_symlinks=False)
            fields = (
                "st_dev",
                "st_ino",
                "st_size",
                "st_mtime_ns",
                "st_ctime_ns",
                "st_mode",
                "st_uid",
            )
            if any(
                getattr(before, field) != getattr(after, field)
                or getattr(before, field) != getattr(current, field)
                for field in fields
            ):
                raise SecureOutputError("private-source-raced")
        finally:
            os.close(descriptor)
    except OSError as exc:
        raise SecureOutputError("private-source-invalid") from exc
    finally:
        os.close(parent_fd)
    body = b"".join(chunks)
    if len(body) != before.st_size:
        raise SecureOutputError("private-source-raced")
    return body


def _atomic_replace_private_bytes(path: pathlib.Path, body: bytes) -> None:
    try:
        parent_stat = path.parent.lstat()
    except OSError as exc:
        raise SecureOutputError("private-parent-invalid") from exc
    if (
        not stat.S_ISDIR(parent_stat.st_mode)
        or path.parent.is_symlink()
        or parent_stat.st_uid != os.getuid()
        or stat.S_IMODE(parent_stat.st_mode) != 0o700
    ):
        raise SecureOutputError("private-parent-invalid")
    parent_fd = os.open(
        path.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    )
    temporary = f".{path.name}.{secrets.token_hex(8)}.tmp"
    try:
        try:
            existing = os.stat(path.name, dir_fd=parent_fd, follow_symlinks=False)
        except FileNotFoundError:
            pass
        else:
            if (
                not stat.S_ISREG(existing.st_mode)
                or existing.st_uid != os.getuid()
                or stat.S_IMODE(existing.st_mode) != 0o600
            ):
                raise SecureOutputError("private-target-invalid")
        opened_parent = os.fstat(parent_fd)
        if (opened_parent.st_dev, opened_parent.st_ino) != (
            parent_stat.st_dev,
            parent_stat.st_ino,
        ):
            raise SecureOutputError("private-parent-raced")
        descriptor = os.open(
            temporary,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
            0o600,
            dir_fd=parent_fd,
        )
        try:
            os.fchmod(descriptor, 0o600)
            view = memoryview(body)
            while view:
                view = view[os.write(descriptor, view) :]
            os.fsync(descriptor)
        except BaseException:
            try:
                os.unlink(temporary, dir_fd=parent_fd)
            except FileNotFoundError:
                pass
            raise
        finally:
            os.close(descriptor)
        current_parent = path.parent.lstat()
        if (current_parent.st_dev, current_parent.st_ino) != (
            opened_parent.st_dev,
            opened_parent.st_ino,
        ):
            raise SecureOutputError("private-parent-raced")
        os.replace(
            temporary,
            path.name,
            src_dir_fd=parent_fd,
            dst_dir_fd=parent_fd,
        )
        os.fsync(parent_fd)
        result = os.stat(path.name, dir_fd=parent_fd, follow_symlinks=False)
        final_parent = path.parent.lstat()
        if (
            not stat.S_ISREG(result.st_mode)
            or result.st_uid != os.getuid()
            or stat.S_IMODE(result.st_mode) != 0o600
            or (final_parent.st_dev, final_parent.st_ino)
            != (opened_parent.st_dev, opened_parent.st_ino)
        ):
            raise SecureOutputError("private-target-invalid")
    finally:
        try:
            os.unlink(temporary, dir_fd=parent_fd)
        except FileNotFoundError:
            pass
        os.close(parent_fd)


def convert_oci_archive_to_docker_load_archive(
    source_path: pathlib.Path | str,
    destination_path: pathlib.Path | str,
    role: str,
) -> dict[str, str]:
    """Validate one OCI layout and emit a deterministic Docker load archive."""

    if role not in {"baseline", "candidate"}:
        raise ValueError("local-image-role-invalid")
    source = pathlib.Path(source_path)
    destination = pathlib.Path(destination_path)
    if source == destination or source.parent != destination.parent:
        raise ValueError("docker-archive-target-invalid")
    try:
        content = _read_stable_private_bytes(
            source, max_bytes=OCI_ARCHIVE_MAX_BYTES
        )
    except SecureOutputError as exc:
        if str(exc) == "private-source-size-limit-exceeded":
            raise ValueError("oci-archive-size-limit-exceeded") from exc
        raise ValueError("oci-archive-private-input-invalid") from exc
    inspected = _inspect_oci_archive_bytes(content)
    config_digest = str(inspected["image_config_digest"])
    config_hex = config_digest.removeprefix("sha256:")
    local_ref = f"hyhome.local/sample-web-service:{role}-{config_hex}"
    if not re.fullmatch(
        rf"hyhome\.local/sample-web-service:{role}-[0-9a-f]{{64}}", local_ref
    ):
        raise ValueError("local-image-ref-invalid")

    layer_names: list[str] = []
    payloads: dict[str, bytes] = {f"{config_hex}.json": inspected["config_blob"]}
    for layer in inspected["layers"]:
        layer_hex = str(layer["digest"]).removeprefix("sha256:")
        layer_name = f"{layer_hex}.tar"
        layer_names.append(layer_name)
        payloads[layer_name] = layer["blob"]
    payloads["manifest.json"] = json.dumps(
        [
            {
                "Config": f"{config_hex}.json",
                "Layers": layer_names,
                "RepoTags": [local_ref],
            }
        ],
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    output = io.BytesIO()
    with tarfile.open(
        fileobj=output, mode="w", format=tarfile.USTAR_FORMAT
    ) as archive:
        for name in sorted(payloads):
            body = payloads[name]
            member = tarfile.TarInfo(name)
            member.type = tarfile.REGTYPE
            member.mode = 0o600
            member.uid = 0
            member.gid = 0
            member.uname = ""
            member.gname = ""
            member.mtime = 0
            member.size = len(body)
            archive.addfile(member, io.BytesIO(body))
    docker_archive = output.getvalue()
    _atomic_replace_private_bytes(destination, docker_archive)
    return {
        "docker_archive_sha256": f"sha256:{hashlib.sha256(docker_archive).hexdigest()}",
        "image_config_digest": config_digest,
        "local_image_ref": local_ref,
        "oci_archive_sha256": f"sha256:{hashlib.sha256(content).hexdigest()}",
        "oci_manifest_digest": str(inspected["oci_manifest_digest"]),
    }


def validate_sbom_subject(sbom: Any, subject: Any) -> list[str]:
    if not isinstance(sbom, dict) or not isinstance(subject, dict):
        return ["sbom-subject-invalid"]
    errors: list[str] = []
    if sbom.get("bomFormat") != "CycloneDX" or not _is_text(sbom.get("specVersion")):
        errors.append("sbom-format-invalid")
    component = (sbom.get("metadata") or {}).get("component") if isinstance(sbom.get("metadata"), dict) else None
    if not isinstance(component, dict) or component.get("name") != "examples/sample-web-service":
        errors.append("sbom-component-invalid")
        return errors
    properties = _properties(component)
    if properties.get("org.hyhome.delivery.image_config_digest") != subject.get("image_config_digest"):
        errors.append("sbom-image-config-subject-mismatch")
    if properties.get("org.hyhome.delivery.oci_archive_sha256") != subject.get("oci_archive_sha256"):
        errors.append("sbom-oci-archive-subject-mismatch")
    if properties.get("org.hyhome.delivery.rehearsal.role") != subject.get("role"):
        errors.append("sbom-role-subject-mismatch")
    return sorted(set(errors))


def _find_exception(
    fixture: dict[str, Any], registry: dict[str, Any], match: dict[str, str], subject_digest: str
) -> tuple[dict[str, Any] | None, str | None]:
    embedded = fixture.get("exception")
    if isinstance(embedded, dict):
        if (
            embedded.get("subject_digest") == subject_digest
            and embedded.get("package") == match["package"]
            and embedded.get("vulnerability_id") == match["vulnerability_id"]
            and str(embedded.get("severity", "")).lower() == match["severity"]
        ):
            return embedded, embedded.get("id") if isinstance(embedded.get("id"), str) else None
        return None, None
    requested_id = fixture.get("exception_id")
    if not isinstance(requested_id, str) or not requested_id:
        return None, None
    rows = registry.get("exceptions") if isinstance(registry.get("exceptions"), list) else []
    for row in rows:
        if not isinstance(row, dict):
            continue
        if requested_id and row.get("id") != requested_id:
            continue
        if (
            row.get("subject_digest") == subject_digest
            and row.get("package") == match["package"]
            and row.get("vulnerability_id") == match["vulnerability_id"]
            and str(row.get("severity", "")).lower() == match["severity"]
        ):
            return row, row.get("id") if isinstance(row.get("id"), str) else None
    return None, None


def evaluate_grype_fixture(
    fixture: Any, policy: Any, registry: Any, subject: Any
) -> dict[str, str | None]:
    if not isinstance(fixture, dict) or not isinstance(policy, dict) or not isinstance(registry, dict) or not isinstance(subject, dict):
        return {"verdict": "rejected", "exception_id": None, "reason": "grype-fixture-invalid"}
    if fixture.get("schema_version") != 1 or fixture.get("subject_digest") != subject.get("image_config_digest"):
        return {"verdict": "rejected", "exception_id": None, "reason": "grype-subject-mismatch"}
    matches = fixture.get("matches")
    if not isinstance(matches, list):
        return {"verdict": "rejected", "exception_id": None, "reason": "grype-matches-invalid"}
    if not matches:
        return {"verdict": "accepted", "exception_id": None, "reason": "clean"}
    vulnerability = policy.get("vulnerability", {})
    blocking = set(vulnerability.get("blocking_severities", []))
    review = set(vulnerability.get("review_severities", []))
    approved_exception_ids: list[str] = []
    has_outside_policy_match = False
    for match in matches:
        if not isinstance(match, dict):
            return {"verdict": "rejected", "exception_id": None, "reason": "grype-match-invalid"}
        artifact = match.get("artifact")
        finding = match.get("vulnerability")
        if not isinstance(artifact, dict) or not isinstance(finding, dict):
            return {"verdict": "rejected", "exception_id": None, "reason": "grype-match-invalid"}
        if any(key in finding for key in ("description", "urls", "locations", "relatedVulnerabilities")):
            return {"verdict": "rejected", "exception_id": None, "reason": "raw-finding-leakage"}
        severity = str(finding.get("severity", "")).lower()
        finding_key = {
            "package": str(artifact.get("name", "")),
            "vulnerability_id": str(finding.get("id", "")),
            "severity": severity,
        }
        if not all(finding_key.values()):
            return {"verdict": "rejected", "exception_id": None, "reason": "grype-finding-invalid"}
        exception, exception_id = _find_exception(
            fixture, registry, finding_key, str(subject.get("image_config_digest", ""))
        )
        if exception is not None:
            exception_errors = _exception_errors(exception)
            if "exception-expired" in exception_errors:
                return {"verdict": "rejected", "exception_id": exception_id, "reason": "exception-expired"}
            if exception_errors:
                return {"verdict": "rejected", "exception_id": exception_id, "reason": exception_errors[0]}
            if severity in blocking or severity in review:
                if exception_id is None:
                    return {"verdict": "rejected", "exception_id": None, "reason": "exception-id-invalid"}
                approved_exception_ids.append(exception_id)
            continue
        if severity in blocking:
            return {"verdict": "rejected", "exception_id": None, "reason": "blocking-finding-without-exception"}
        if severity in review:
            return {"verdict": "rejected", "exception_id": None, "reason": "review-finding-without-exception"}
        has_outside_policy_match = True
    if approved_exception_ids:
        unique_ids = sorted(set(approved_exception_ids))
        return {
            "verdict": "accepted",
            "exception_id": unique_ids[0] if len(unique_ids) == 1 else None,
            "reason": "all-policy-findings-exception-approved",
        }
    return {"verdict": "accepted", "exception_id": None, "reason": "outside-policy" if has_outside_policy_match else "clean"}


def validate_provenance_subject(provenance: Any, subject: Any) -> list[str]:
    if not isinstance(provenance, dict) or not isinstance(subject, dict):
        return ["provenance-invalid"]
    errors: list[str] = []
    if provenance.get("_type") != "https://in-toto.io/Statement/v1":
        errors.append("provenance-statement-type-invalid")
    if provenance.get("predicateType") != "https://slsa.dev/provenance/v1":
        errors.append("provenance-predicate-type-invalid")
    subjects = provenance.get("subject")
    expected_sha = str(subject.get("oci_archive_sha256", "")).removeprefix("sha256:")
    if not isinstance(subjects, list) or not any(
        isinstance(item, dict)
        and item.get("name") == "examples/sample-web-service"
        and isinstance(item.get("digest"), dict)
        and item["digest"].get("sha256") == expected_sha
        for item in subjects
    ):
        errors.append("provenance-archive-subject-mismatch")
    predicate = provenance.get("predicate")
    if not isinstance(predicate, dict):
        return sorted(set(errors + ["provenance-predicate-invalid"]))
    build_definition = predicate.get("buildDefinition")
    run_details = predicate.get("runDetails")
    if not isinstance(build_definition, dict) or not isinstance(run_details, dict):
        return sorted(set(errors + ["provenance-build-definition-invalid"]))
    params = build_definition.get("externalParameters")
    dependencies = build_definition.get("resolvedDependencies")
    builder = run_details.get("builder")
    if not isinstance(params, dict) or params.get("role") != subject.get("role"):
        errors.append("provenance-role-invalid")
    if not isinstance(params, dict) or params.get("source_revision") != subject.get("source_revision"):
        errors.append("provenance-source-revision-mismatch")
    expected_context = subject.get("build_context_sha256")
    if (
        not isinstance(params, dict)
        or params.get("build_context_sha256") != expected_context
    ):
        errors.append("provenance-build-context-mismatch")
    expected_context_sha = str(expected_context or "").removeprefix("sha256:")
    if not isinstance(dependencies, list) or not any(
        isinstance(item, dict)
        and item.get("uri") == "git+local://examples/sample-web-service"
        and isinstance(item.get("digest"), dict)
        and item["digest"].get("sha256") == expected_context_sha
        for item in dependencies
    ):
        errors.append("provenance-materials-invalid")
    if not isinstance(builder, dict) or not _is_text(builder.get("id")):
        errors.append("provenance-builder-invalid")
    return sorted(set(errors))


def validate_signature_fixture(fixture: Any, subject: Any) -> list[str]:
    if not isinstance(fixture, dict) or not isinstance(subject, dict):
        return ["signature-fixture-invalid"]
    errors: list[str] = []
    if fixture.get("schema_version") != 1 or fixture.get("mode") != "cosign-sign-blob":
        errors.append("signature-fixture-invalid")
    if fixture.get("role") != subject.get("role"):
        errors.append("signature-role-mismatch")
    if fixture.get("oci_archive_sha256") != subject.get("oci_archive_sha256"):
        errors.append("signature-subject-mismatch")
    if fixture.get("verified") is not True:
        errors.append("signature-verification-rejected")
    return sorted(set(errors))


def validate_scorecard_advisory(scorecard: Any) -> list[str]:
    if not isinstance(scorecard, dict):
        return ["scorecard-fixture-invalid"]
    errors: list[str] = []
    if scorecard.get("schema_version") != 1:
        errors.append("scorecard-schema-version-invalid")
    if scorecard.get("mode") != "read-only-advisory" or scorecard.get("observation") != "read-only":
        errors.append("scorecard-advisory-mode-invalid")
    if scorecard.get("ci_enforcement") != "fixture-policy-only":
        errors.append("scorecard-blocking-forbidden")
    if scorecard.get("repository") != SCORECARD_REPOSITORY:
        errors.append("scorecard-repository-invalid")
    return sorted(set(errors))


def _fixture_subject() -> dict[str, str]:
    return {
        "role": "candidate",
        "source_revision": "0123456789abcdef0123456789abcdef01234567",
        "image_config_digest": "sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc",
        "oci_archive_sha256": "sha256:dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd",
        "build_context_sha256": "sha256:eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
    }


def check() -> list[str]:
    registry = load_json(TOOL_REGISTRY_PATH)
    policy = load_json(POLICY_PATH)
    exceptions = load_json(EXCEPTIONS_PATH)
    subject = _fixture_subject()
    errors = [*validate_tool_registry(registry), *validate_policy(policy)]
    errors.extend(validate_exceptions(exceptions, policy, subject["image_config_digest"]))
    errors.extend(
        validate_subject_tuples(
            [
                {
                    **subject,
                    "role": "baseline",
                    "image_config_digest": "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                    "oci_archive_sha256": "sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
                },
                subject,
            ]
        )
    )
    errors.extend(validate_sbom_subject(load_json(FIXTURES / "sample-service-sbom.valid.cdx.json"), subject))
    if not validate_sbom_subject(load_json(FIXTURES / "sample-service-sbom.subject-mismatch.cdx.json"), subject):
        errors.append("negative-sbom-fixture-not-rejected")
    for name, expected in (
        ("grype.clean.json", "accepted"),
        ("grype.high-without-exception.json", "rejected"),
        ("grype.high-with-valid-exception.json", "accepted"),
        ("grype.expired-exception.json", "rejected"),
        ("grype.valid-exception-then-critical.json", "rejected"),
    ):
        result = evaluate_grype_fixture(load_json(FIXTURES / name), policy, exceptions, subject)
        if result["verdict"] != expected:
            errors.append("grype-fixture-verdict-invalid")
    errors.extend(validate_provenance_subject(load_json(FIXTURES / "provenance.valid.intoto.json"), subject))
    if not validate_provenance_subject(load_json(FIXTURES / "provenance.subject-mismatch.intoto.json"), subject):
        errors.append("negative-provenance-fixture-not-rejected")
    errors.extend(validate_signature_fixture(load_json(FIXTURES / "cosign.verify.valid.json"), subject))
    for name in ("cosign.verify.tampered.json", "cosign.verify.wrong-subject.json"):
        if not validate_signature_fixture(load_json(FIXTURES / name), subject):
            errors.append("negative-signature-fixture-not-rejected")
    errors.extend(validate_scorecard_advisory(load_json(FIXTURES / "scorecard.advisory.json")))
    return sorted(set(errors))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate policy and deterministic fixtures")
    parser.add_argument(
        "--oci-archive-config-digest",
        metavar="ARCHIVE",
        help="print the SHA-256 config digest cryptographically bound by an OCI archive",
    )
    parser.add_argument(
        "--convert-oci-to-docker-load",
        nargs=3,
        metavar=("OCI_ARCHIVE", "DOCKER_ARCHIVE", "ROLE"),
        help="validate one private OCI archive and atomically emit a deterministic Docker load archive",
    )
    parser.add_argument(
        "--capture-build-context",
        nargs=4,
        metavar=("REPO_ROOT", "CONTEXT", "SNAPSHOT", "ARCHIVE"),
        help="capture a clean, deterministic effective Docker context snapshot and tar",
    )
    parser.add_argument(
        "--verify-build-context",
        nargs=4,
        metavar=("REPO_ROOT", "CONTEXT", "SNAPSHOT", "ARCHIVE"),
        help="fail unless the effective Docker context and tar still match a snapshot",
    )
    parser.add_argument(
        "--prepare-secure-output",
        nargs=2,
        metavar=("REPO_ROOT", "RELATIVE_OUTPUT"),
        help="create and validate the private handoff directory, then print its identity",
    )
    parser.add_argument(
        "--invalidate-secure-handoffs",
        nargs=3,
        metavar=("REPO_ROOT", "RELATIVE_OUTPUT", "IDENTITY"),
        help="remove only the fixed consumer handoffs from a validated directory",
    )
    parser.add_argument(
        "--publish-verdict-pair",
        nargs=7,
        metavar=(
            "REPO_ROOT",
            "RELATIVE_OUTPUT",
            "IDENTITY",
            "BASELINE",
            "CANDIDATE",
            "SOURCE_REVISION",
            "BUILD_CONTEXT_SHA256",
        ),
        help="atomically publish the two accepted verdicts and commit manifest",
    )
    parser.add_argument(
        "--publish-minimized-handoff",
        nargs=5,
        metavar=("REPO_ROOT", "RELATIVE_OUTPUT", "IDENTITY", "NAME", "SOURCE"),
        help="atomically publish one allowlisted redacted advisory summary",
    )
    args = parser.parse_args(argv)
    operation_count = sum(
        bool(value)
        for value in (
            args.check,
            args.oci_archive_config_digest,
            args.convert_oci_to_docker_load,
            args.capture_build_context,
            args.verify_build_context,
            args.prepare_secure_output,
            args.invalidate_secure_handoffs,
            args.publish_verdict_pair,
            args.publish_minimized_handoff,
        )
    )
    if operation_count != 1:
        parser.print_usage(sys.stderr)
        return 2
    if args.oci_archive_config_digest:
        try:
            print(inspect_oci_archive_config_digest(args.oci_archive_config_digest))
        except ValueError as exc:
            print(f"oci_archive_config_digest=fail reason={exc}", file=sys.stderr)
            return 1
        return 0
    try:
        if args.convert_oci_to_docker_load:
            result = convert_oci_archive_to_docker_load_archive(
                *args.convert_oci_to_docker_load
            )
            print(json.dumps(result, sort_keys=True, separators=(",", ":")))
            return 0
        if args.capture_build_context:
            root, context, snapshot_path, archive_path = args.capture_build_context
            snapshot = write_build_context_bundle(
                root, context, snapshot_path, archive_path
            )
            print(snapshot["build_context_sha256"])
            return 0
        if args.verify_build_context:
            root, context, snapshot, archive = args.verify_build_context
            verified = verify_build_context_snapshot(root, context, snapshot, archive)
            print(verified["build_context_sha256"])
            return 0
        if args.prepare_secure_output:
            print(prepare_secure_output_directory(*args.prepare_secure_output))
            return 0
        if args.invalidate_secure_handoffs:
            invalidate_secure_handoffs(*args.invalidate_secure_handoffs)
            return 0
        if args.publish_verdict_pair:
            publish_verdict_pair(*args.publish_verdict_pair)
            return 0
        if args.publish_minimized_handoff:
            publish_minimized_handoff(*args.publish_minimized_handoff)
            return 0
    except (
        BuildContextError,
        SecureOutputError,
        OSError,
        ValueError,
        json.JSONDecodeError,
    ) as exc:
        print(f"supply_chain_operation=fail reason={exc}", file=sys.stderr)
        return 1
    try:
        errors = check()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"supply_chain_policy=fail reason={exc.__class__.__name__}", file=sys.stderr)
        return 1
    if errors:
        print(f"supply_chain_policy=fail errors={','.join(errors)}", file=sys.stderr)
        return 1
    print("supply_chain_policy=pass fixtures=13")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
