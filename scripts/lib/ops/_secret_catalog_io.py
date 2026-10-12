"""Private P02 fixed-public-input and staging I/O; no credential discovery."""

from __future__ import annotations

import os
import re
import stat
import subprocess
from contextlib import ExitStack
from pathlib import Path, PurePosixPath

from scripts.lib.ops.smtp_contract import ContractError, root_identity

CATALOG_PATH = "infra/03-security/openbao/secret-catalog.json"


SCHEMA_PATH = "infra/03-security/openbao/secret-catalog.schema.json"


METADATA_PATH = "secrets/SENSITIVE_ENV_VARS.md.example"


SUPPORT_PATH = "infra/secret-file-support.json"


OUTPUT_PATH = ".agent-work/p02-views"


MAX_BYTES = 2 * 1024 * 1024


DIR_FLAGS = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC


FILE_FLAGS = os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC | os.O_NONBLOCK


class CatalogError(ValueError):
    """Only a fixed code is safe to report; never interpolate input."""


def _borrowed_root_fd(root):
    raw = os.fspath(root)
    held = os.environ.get("HYHOME_GENERATOR_HELD_ROOT")
    match = re.fullmatch(r"/proc/self/fd/([0-9]+)", raw)
    held_match = re.fullmatch(r"/proc/self/fd/([0-9]+)", held or "")
    if match is None or held_match is None:
        return None
    fd = int(match.group(1))
    held_fd = int(held_match.group(1))
    info = os.fstat(fd)
    held_info = os.fstat(held_fd)
    if not stat.S_ISDIR(info.st_mode) or (info.st_dev, info.st_ino) != (
        held_info.st_dev,
        held_info.st_ino,
    ):
        raise CatalogError("unsafe_repository_root")
    return os.dup(fd)


def _is_borrowed_root(root):
    fd = _borrowed_root_fd(root)
    if fd is None:
        return False
    os.close(fd)
    return True


def _root(root):
    raw = os.fspath(root)
    path = Path(raw)
    if path.anchor != "/" or raw != str(path) or ".." in path.parts:
        raise CatalogError("unsafe_repository_root")
    try:
        expected = root_identity(path)
    except ContractError as exc:
        raise CatalogError("unsafe_repository_root") from exc
    environment = {
        key: value for key, value in os.environ.items() if not key.startswith("GIT_")
    }
    if not _is_borrowed_root(path):
        result = subprocess.run(
            ["git", "-C", str(path), "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=False,
            env=environment,
        )
        if result.returncode != 0 or Path(result.stdout.strip()) != path:
            raise CatalogError("repository_root_mismatch")
    return path, expected, environment


def _directory(root, relative, stack):
    allowed = {
        "",
        *(
            str(PurePosixPath(path).parent)
            for path in (CATALOG_PATH, SCHEMA_PATH, METADATA_PATH, SUPPORT_PATH)
        ),
    }
    if relative not in allowed:
        raise CatalogError("unapproved_public_directory")
    borrowed = _borrowed_root_fd(root)
    fd = borrowed if borrowed is not None else os.open(root, DIR_FLAGS)
    stack.callback(os.close, fd)
    for part in PurePosixPath(relative).parts:
        fd = os.open(part, DIR_FLAGS, dir_fd=fd)
        stack.callback(os.close, fd)
    return fd


def _read_file(fd, name):
    opened = os.open(name, FILE_FLAGS, dir_fd=fd)
    try:
        before = os.fstat(opened)
        if (
            not stat.S_ISREG(before.st_mode)
            or before.st_nlink != 1
            or before.st_size > MAX_BYTES
        ):
            raise CatalogError("unsafe_public_metadata_file")
        chunks, remaining = [], before.st_size + 1
        while remaining:
            chunk = os.read(opened, min(remaining, 65_536))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        data = b"".join(chunks)
        after = os.fstat(opened)
        if len(data) != before.st_size or (
            before.st_dev,
            before.st_ino,
            before.st_size,
            before.st_mtime_ns,
            before.st_ctime_ns,
        ) != (
            after.st_dev,
            after.st_ino,
            after.st_size,
            after.st_mtime_ns,
            after.st_ctime_ns,
        ):
            raise CatalogError("metadata_changed_during_read")
        return data
    finally:
        os.close(opened)


def _public_bytes(root, relative, environment):
    if relative not in {CATALOG_PATH, SCHEMA_PATH, METADATA_PATH, SUPPORT_PATH}:
        raise CatalogError("unapproved_public_input")
    borrowed = _borrowed_root_fd(root)
    try:
        git_root = str(root)
        pass_fds = ()
        if borrowed is not None:
            git_root = f"/proc/self/fd/{borrowed}"
            pass_fds = (borrowed,)
        tracked = subprocess.run(
            ["git", "-C", git_root, "ls-files", "--error-unmatch", "--", relative],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
            env=environment,
            pass_fds=pass_fds,
        )
        if tracked.returncode != 0:
            raise CatalogError("public_input_not_tracked")
    finally:
        if borrowed is not None:
            os.close(borrowed)
    with ExitStack() as stack:
        path = PurePosixPath(relative)
        fd = _directory(root, str(path.parent), stack)
        return _read_file(fd, path.name)


def _unique_object(pairs):
    result = {}
    for name, value in pairs:
        if name in result:
            raise CatalogError("duplicate_json_field")
        result[name] = value
    return result


def _output(root, output):
    expected = root / OUTPUT_PATH
    if output is not None and os.fspath(output) != str(expected):
        raise CatalogError("output_must_be_staging_only")
    return expected


def _staging_fd(root, stack, create):
    fd = _directory(root, "", stack)
    for index, part in enumerate(PurePosixPath(OUTPUT_PATH).parts):
        if create and index:
            try:
                os.mkdir(part, mode=0o700, dir_fd=fd)
            except FileExistsError:
                pass
        fd = os.open(part, DIR_FLAGS, dir_fd=fd)
        stack.callback(os.close, fd)
        if os.fstat(fd).st_uid != os.getuid():
            raise CatalogError("unsafe_staging_owner")
        if index == 0:
            _target_safe(fd, "README.md")
            os.stat("README.md", dir_fd=fd, follow_symlinks=False)
    return fd


def _target_safe(fd, name, *, required_mode=None):
    try:
        info = os.stat(name, dir_fd=fd, follow_symlinks=False)
    except FileNotFoundError:
        return
    if (
        not stat.S_ISREG(info.st_mode)
        or info.st_nlink != 1
        or info.st_uid != os.getuid()
        or (required_mode is not None and stat.S_IMODE(info.st_mode) != required_mode)
    ):
        raise CatalogError("unsafe_staging_target")
