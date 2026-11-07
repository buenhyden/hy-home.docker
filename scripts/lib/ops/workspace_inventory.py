"""Dated public source census; private entries are metadata only, never opened."""

from __future__ import annotations

import hashlib
import os
import re
import stat
import subprocess
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath

import yaml

STATES = {
    "REUSE_ACCEPTED",
    "SOURCE_READY",
    "IMPLEMENT_GAP",
    "IMPROVEMENT_CANDIDATE",
    "TEST_RESIDUAL",
    "BLOCKED",
    "OUT_OF_SCOPE",
    "NO_CHANGE",
}
GENERATED = {
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    "graphify-out",
    ".worktrees",
    "dist",
    "build",
}
PRIVATE = {
    ".git",
    ".aws",
    ".ssh",
    ".workspace-memory",
    "sessions",
    ".agent-work",
    ".rtk",
    ".history",
}
SHA = re.compile(r"[0-9a-f]{64}")


class InventoryError(ValueError):
    """Safe fixed diagnostic; never contains file values or raw subprocess errors."""


def _require(condition, message="Invalid inventory metadata."):
    if not condition:
        raise InventoryError(message)


def _relative(value):
    _require(isinstance(value, str) and bool(value))
    p = PurePosixPath(value)
    _require(not p.is_absolute() and ".." not in p.parts and p.as_posix() == value)
    return p


def _sensitive(path):
    p = PurePosixPath(path)
    if PRIVATE.intersection(p.parts):
        return True
    if "secrets" in p.parts:
        suffix = PurePosixPath(*p.parts[p.parts.index("secrets") :]).as_posix()
        return (
            suffix not in {"secrets/README.md", "secrets/SENSITIVE_ENV_VARS.md.example"}
            and p.name != ".gitkeep"
        )
    return (
        (p.name.startswith(".env") and not p.name.endswith(".example"))
        or p.name.lower()
        in {
            "credentials",
            "credentials.json",
            "auth.json",
            ".npmrc",
            ".netrc",
            "id_rsa",
            "id_ed25519",
            "claude.local.md",
            "settings.local.json",
        }
        or p.suffix.lower() in {".pem", ".key", ".p12", ".pfx", ".log"}
    )


def _safe_path(root, relative):
    p = _relative(relative)
    current = root
    for part in p.parts:
        current = current / part
        _require(not current.is_symlink(), "Symlink access refused.")
    return current


def _read_public(root, relative):
    from scripts.lib.document_governance.operations_catalog import read_bounded_regular

    _require(not _sensitive(relative), "Private input refused.")
    return read_bounded_regular(root, _relative(relative), max_bytes=64 * 1024 * 1024)


def _git(root, *args):
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            timeout=20,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    return result.stdout if result.returncode == 0 else None


def _git_metadata(root):
    top = _git(root, "rev-parse", "--show-toplevel")
    if top is None:
        return {
            "path": ".",
            "git": False,
            "head": None,
            "branch": None,
            "dirty_paths": [],
        }, set()
    actual = Path(os.fsdecode(top).strip()).resolve()
    inside = actual == root or actual.is_relative_to(root)
    raw = _git(root, "ls-files", "-z") if inside else None
    tracked = {os.fsdecode(p) for p in (raw or b"").split(b"\0") if p}
    status = (
        _git(root, "status", "--porcelain=v1", "-z", "--untracked-files=all")
        if inside
        else None
    )
    fields, dirty, index = (status or b"").split(b"\0"), [], 0
    while index < len(fields) and fields[index]:
        item = fields[index]
        index += 1
        row = {"status": os.fsdecode(item[:2]), "path": os.fsdecode(item[3:])}
        if b"R" in item[:2] or b"C" in item[:2]:
            row["original_path"] = os.fsdecode(fields[index])
            index += 1
        dirty.append(row)
    head, branch = (
        _git(root, "rev-parse", "--verify", "HEAD"),
        _git(root, "symbolic-ref", "--short", "HEAD"),
    )
    worktrees = []
    raw_worktrees = _git(root, "worktree", "list", "--porcelain", "-z") or b""
    for field in raw_worktrees.split(b"\0"):
        if field.startswith(b"worktree "):
            location = os.fsdecode(field[9:])
            worktrees.append(
                {
                    "path": location,
                    "in_boundary": Path(location).is_relative_to(root),
                    "access": "metadata-only",
                }
            )
    staged = _git(root, "ls-files", "--stage", "-z") if inside else None
    submodules = [
        os.fsdecode(row.partition(b"\t")[2])
        for row in (staged or b"").split(b"\0")
        if row.startswith(b"160000 ")
    ]
    return {
        "path": ".",
        "git": True,
        "git_root": str(actual),
        "git_root_in_boundary": inside,
        "head": os.fsdecode(head).strip() if head else None,
        "branch": os.fsdecode(branch).strip() if branch else None,
        "dirty_paths": dirty,
        "worktrees": worktrees,
        "submodules": submodules,
        "tracked_query": "PASS" if raw is not None else "ERROR",
    }, tracked


def _kind(path):
    p = PurePosixPath(path)
    if _sensitive(path):
        return "private"
    if GENERATED.intersection(p.parts):
        return "generated"
    if p.suffix.lower() in {
        ".png",
        ".jpg",
        ".jpeg",
        ".ico",
        ".woff",
        ".woff2",
        ".ttf",
        ".otf",
        ".zip",
        ".pdf",
        ".bin",
        ".gz",
        ".bz2",
        ".xz",
        ".7z",
        ".tar",
        ".pyc",
        ".so",
        ".sqlite",
        ".db",
        ".exe",
        ".dll",
        ".mp3",
        ".mp4",
        ".webm",
        ".wav",
        ".webp",
        ".avif",
    }:
        return "binary"
    if p.parts[0] == "tests":
        return "test"
    if p.suffix.lower() in {".md", ".rst", ".txt"}:
        return "document"
    if p.suffix.lower() in {".py", ".sh", ".js", ".ts", ".tsx", ".sql", ".cjs", ".mjs"}:
        return "code"
    return "configuration"


def _review_map(reviews):
    result = {}
    for row in reviews:
        _require(
            isinstance(row, dict)
            and all(
                isinstance(row.get(k), str) and row[k].strip()
                for k in ("path", "sha256", "reviewer", "observed_at", "scope")
            )
        )
        path = _relative(row["path"]).as_posix()
        _require(type(row.get("complete", False)) is bool)
        _require(path not in result and SHA.fullmatch(row["sha256"]))
        try:
            _require(
                datetime.fromisoformat(row["observed_at"].replace("Z", "+00:00")).tzinfo
                is not None
            )
        except ValueError:
            raise InventoryError("Invalid review time.") from None
        result[path] = dict(row)
    return result


def _file_row(root, relative, tracked, public, outputs, reviews):
    path = root / relative
    row = {"path": relative, "tracked": tracked, "kind": _kind(relative)}
    try:
        info = path.lstat()
        row["bytes"] = info.st_size
        if stat.S_ISLNK(info.st_mode):
            return {
                **row,
                **(
                    {
                        "link_identity_sha256": hashlib.sha256(
                            os.fsencode(os.readlink(path))
                        ).hexdigest()
                    }
                    if public
                    else {}
                ),
                "state": "SYMLINK_NOT_FOLLOWED",
                "link_scope": "internal"
                if path.resolve().is_relative_to(root)
                else "external",
            }
        if not stat.S_ISREG(info.st_mode):
            return {**row, "state": "SPECIAL_NOT_OPENED"}
        if not public:
            return {**row, "state": "METADATA_ONLY"}
        if relative in outputs:
            return {**row, "state": "GENERATED_OUTPUT"}
        if row["kind"] == "generated":
            return {**row, "state": "GENERATED_NOT_OPENED"}
        if row["kind"] == "binary":
            return {**row, "state": "BINARY_NOT_OPENED"}
        raw = _read_public(root, relative)
        row.update(state="HASHED", sha256=hashlib.sha256(raw).hexdigest())
    except (OSError, ValueError, RuntimeError):
        return {**row, "state": "UNREADABLE"}
    review = reviews.get(relative)
    row["review"] = (
        {"state": "UNREVIEWED"}
        if review is None
        else {
            **review,
            "state": ("REVIEWED" if review.get("complete", False) else "PARTIAL")
            if review["sha256"] == row["sha256"]
            else "STALE",
        }
    )
    return row


def _walk(root):
    errors = []
    entries, git_roots, opaque = [], [], []

    def onerror(_error):
        errors.append("DIRECTORY_UNREADABLE")

    for base, directories, files in os.walk(root, followlinks=False, onerror=onerror):
        relative_base = Path(base).relative_to(root)
        if ".git" in directories or ".git" in files:
            git_roots.append(relative_base.as_posix())
        if ".git" in directories:
            directories.remove(".git")
            opaque.append((relative_base / ".git").as_posix())
        for directory in list(directories):
            target = Path(base) / directory
            if target.is_symlink():
                directories.remove(directory)
                entries.append((relative_base / directory).as_posix())
        entries.extend((relative_base / name).as_posix() for name in files)
    return sorted(entries), sorted(git_roots), opaque, errors


def scan(root, *, public_paths=(), excluded_outputs=(), reviews=(), connections=False):
    """Enumerate all accessible entries; open only selected, nonprivate sources."""
    root = Path(root).absolute()
    _require(root.is_dir() and root.resolve() == root, "Workspace boundary refused.")
    explicit = {_relative(p).as_posix() for p in public_paths}
    _require(not any(_sensitive(p) for p in explicit), "Private input refused.")
    outputs = {_relative(p).as_posix() for p in excluded_outputs}
    review_map = _review_map(reviews)
    workspace, tracked = _git_metadata(root)
    entries, roots, opaque, errors = _walk(root)
    _require(explicit <= set(entries) | outputs, "Public input does not exist.")
    root_rows = []
    public_roots = set()
    for relative in sorted(set([".", *roots])):
        directory = root if relative == "." else _safe_path(root, relative)
        metadata, local_tracked = _git_metadata(directory)
        root_rows.append({**metadata, "path": relative, "write_boundary": str(root)})
        selected_root = (
            relative == "."
            or relative in workspace.get("submodules", [])
            or any(p.startswith(relative + "/") for p in explicit)
        )
        if selected_root and not _sensitive(relative):
            public_roots.add(relative)
            tracked.update(
                (PurePosixPath(relative) / p).as_posix() for p in local_tracked
            )
    public, private = [], []
    for relative in entries:
        selected = (relative in tracked or relative in explicit) and not _sensitive(
            relative
        )
        row = _file_row(
            root, relative, relative in tracked, selected, outputs, review_map
        )
        (public if selected else private).append(row)
    # Do not expose untracked/ignored/private names through public Git status.
    public_workspace = {
        **workspace,
        "dirty_paths": [
            r
            for r in workspace["dirty_paths"]
            if (r["path"] in tracked or r["path"] in explicit)
            and not _sensitive(r["path"])
        ],
    }
    public_workspace.update(
        root=str(root),
        writable_boundary=str(root),
        private_dirty_count=len(workspace["dirty_paths"])
        - len(public_workspace["dirty_paths"]),
    )
    public_workspace = {
        **public_workspace,
        "worktrees": [
            {k: v for k, v in item.items() if k != "path"}
            for item in workspace.get("worktrees", [])
        ],
    }
    from scripts.lib.ops._workspace_services import inspect_services

    inspection = inspect_services(
        root, [r["path"] for r in public if r["state"] == "HASHED"]
    )
    services = inspection["services"]
    service_data = {k: v for k, v in inspection.items() if k != "services"}
    fingerprints = {row["path"]: row.get("sha256") for row in public}
    _require(
        all(
            fingerprints.get(row["path"]) == row["sha256"]
            for row in service_data["sources"]
        ),
        "Compose input changed during collection.",
    )
    timestamp = datetime.now(UTC).isoformat().replace("+00:00", "Z")
    doc = {
        "schema_version": 1,
        "observed_at": timestamp,
        "workspace": public_workspace,
        "roots": [
            {
                **r,
                "dirty_paths": [],
                "dirty_count": len(r["dirty_paths"]),
                "worktrees": [
                    {k: v for k, v in item.items() if k != "path"}
                    for item in r.get("worktrees", [])
                ],
            }
            for r in root_rows
            if r["path"] in public_roots
        ],
        "files": public,
        "excluded": dict(sorted(Counter(r["kind"] for r in private).items())),
        "opaque": {
            "git_directories": len(opaque),
            "private_git_roots": len(root_rows) - len(public_roots),
            "directory_errors": errors,
        },
        "services": services,
        "compose": service_data,
        "coverage": {
            "files": {
                "numerator": len(public) + len(private),
                "denominator": len(entries),
            },
            "body_review": {
                "numerator": sum(
                    r.get("review", {}).get("state") == "REVIEWED" for r in public
                ),
                "denominator": sum(
                    "sha256" in r and r["kind"] != "binary" for r in public
                ),
            },
            "body_review_partial": {
                "numerator": sum(
                    r.get("review", {}).get("state") == "PARTIAL" for r in public
                ),
                "denominator": sum(
                    "sha256" in r and r["kind"] != "binary" for r in public
                ),
            },
            "render": {"numerator": 0, "denominator": len(service_data["entrypoints"])},
            "runtime": {
                "numerator": 0,
                "denominator": len(service_data["root_services"]),
            },
            "restore": {
                "numerator": 0,
                "denominator": len(service_data["root_services"]),
            },
        },
    }
    if connections:
        from scripts.lib.ops._workspace_connections import (
            ConnectionInventoryError,
            inspect_connections,
        )

        try:
            doc.update(inspect_connections(root, public, services=services))
        except ConnectionInventoryError:
            raise InventoryError("Connection inventory failed.") from None
    validate(doc)
    return doc, {
        "schema_version": 1,
        "observed_at": timestamp,
        "files": private,
        "roots": root_rows,
        "opaque_git_paths": opaque,
        "workspace": workspace,
    }


def validate(doc):
    """Validate evidence structure, not natural-language meaning or live acceptance."""
    _require(isinstance(doc, dict) and doc.get("schema_version") == 1)
    _require(
        isinstance(doc.get("files"), list) and isinstance(doc.get("coverage"), dict)
    )
    paths = set()
    for row in doc["files"]:
        _require(isinstance(row, dict))
        path = _relative(row.get("path")).as_posix()
        _require(path not in paths and not _sensitive(path))
        paths.add(path)
        if "sha256" in row:
            _require(isinstance(row["sha256"], str) and SHA.fullmatch(row["sha256"]))
        if row.get("review", {}).get("state") in {"REVIEWED", "PARTIAL"}:
            record = _review_map([row["review"]])[path]
            _require(record["sha256"] == row.get("sha256"))
            _require(
                (row["review"]["state"] == "REVIEWED") == record.get("complete", False)
            )
    expected = sum(r.get("review", {}).get("state") == "REVIEWED" for r in doc["files"])
    _require(doc["coverage"].get("body_review", {}).get("numerator") == expected)
    _require(
        doc["coverage"].get("body_review", {}).get("denominator")
        == sum("sha256" in r and r["kind"] != "binary" for r in doc["files"])
    )
    files = doc["coverage"].get("files", {})
    _require(
        files.get("numerator")
        == files.get("denominator")
        == len(doc["files"]) + sum(doc.get("excluded", {}).values())
    )
    _require(
        doc["coverage"].get("render", {}).get("numerator")
        == sum(
            row.get("result") == "PASS"
            for row in doc.get("compose", {}).get("render_cases", [])
        )
    )
    for level in ("runtime", "restore"):
        for observation in doc.get("observations", []):
            _require(
                isinstance(observation, dict)
                and all(
                    isinstance(observation.get(k), str) and observation[k].strip()
                    for k in (
                        "level",
                        "result",
                        "actor",
                        "environment",
                        "target",
                        "observed_at",
                        "evidence",
                    )
                )
            )
        _require(
            doc["coverage"].get(level, {}).get("numerator")
            == sum(
                row.get("result") == "PASS" and row.get("level") == level
                for row in doc.get("observations", [])
            )
        )
    for count in doc["coverage"].values():
        _require(
            isinstance(count, dict)
            and all(type(count.get(k)) is int for k in ("numerator", "denominator"))
        )
        _require(0 <= count["numerator"] <= count["denominator"])
    leases = set()
    for row in doc.get("ownership", []):
        _require(
            isinstance(row, dict)
            and isinstance(row.get("writer"), str)
            and row["writer"]
        )
        scope = (row.get("path"), row.get("section", "whole-file"))
        _require(
            not any(
                p == scope[0] and (s == "whole-file" or scope[1] == "whole-file")
                for p, s in leases
            ),
            "Overlapping writer lease.",
        )
        _require(scope not in leases, "Conflicting writer lease.")
        leases.add(scope)
    for row in doc.get("requirements", []):
        _require(row.get("state") in STATES)
        subject = row.get("subject")
        _require(isinstance(subject, str) and subject.strip(), "Requirement subject.")
    # Tier rows claim current membership, so they must resolve against this payload.
    service_ids = {s.get("id") for s in doc.get("services", [])}
    root_names = set(doc.get("compose", {}).get("root_services", []))
    digests = {r["path"]: r.get("sha256") for r in doc["files"]}
    for tier in doc.get("coverage_tiers", []):
        ids = tier.get("service_ids", [])
        _require(set(ids) <= service_ids, "Stale tier service.")
        _require(set(tier.get("root_service_names", [])) <= root_names)
        _require(tier.get("declared_service_rows", len(ids)) == len(ids))
        for source in tier.get("source_files", []):
            digest = source.get("sha256")
            _require(
                isinstance(digest, str) and digests.get(source.get("path")) == digest
            )
    connection_keys = {
        "connections",
        "connection_sources",
        "connection_gaps",
        "connection_coverage",
    }
    _require(not (connection_keys & set(doc)) or connection_keys <= set(doc))
    if connection_keys <= set(doc):
        from scripts.lib.ops._workspace_connections import (
            ConnectionInventoryError,
            validate_connections,
        )

        try:
            validate_connections(
                {key: doc[key] for key in connection_keys}, public_files=doc["files"]
            )
        except ConnectionInventoryError:
            raise InventoryError("Invalid connection metadata.") from None
    return True


def compare(before, after):
    validate(before)
    validate(after)
    old = {r["path"]: r for r in before["files"]}
    new = {r["path"]: r for r in after["files"]}

    def identity(row):
        return (
            row.get("sha256"),
            row.get("state"),
            row.get("bytes"),
            row.get("link_identity_sha256"),
            row.get("link_scope"),
        )

    changed = sorted(
        p for p in old.keys() & new.keys() if identity(old[p]) != identity(new[p])
    )
    removed = sorted(old.keys() - new.keys())
    old_connections = {row["id"]: row for row in before.get("connections", [])}
    new_connections = {row["id"]: row for row in after.get("connections", [])}
    changed_connections = sorted(
        identity
        for identity in old_connections.keys() & new_connections.keys()
        if old_connections[identity] != new_connections[identity]
    )
    removed_connections = sorted(old_connections.keys() - new_connections.keys())
    return {
        "added": sorted(new.keys() - old.keys()),
        "removed": removed,
        "changed": changed,
        "invalidated_reviews": sorted(set(changed + removed)),
        "added_connections": sorted(new_connections.keys() - old_connections.keys()),
        "removed_connections": removed_connections,
        "changed_connections": changed_connections,
        "invalidated_connections": sorted(
            set(changed_connections + removed_connections)
        ),
        "head_changed": before.get("workspace", {}).get("head")
        != after.get("workspace", {}).get("head"),
    }


def atomic_write(root, relative, document):
    """Write one validated caller-selected payload; never replace through links."""
    root = Path(root).resolve()
    _require(not _sensitive(relative), "Private output refused.")
    _safe_path(root, relative)
    parts = _relative(relative).parts
    directory_fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    temporary = None
    try:
        for part in parts[:-1]:
            try:
                os.mkdir(part, mode=0o700, dir_fd=directory_fd)
            except FileExistsError:
                pass
            next_fd = os.open(
                part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=directory_fd
            )
            os.close(directory_fd)
            directory_fd = next_fd
        try:
            _require(
                not stat.S_ISLNK(
                    os.stat(
                        parts[-1], dir_fd=directory_fd, follow_symlinks=False
                    ).st_mode
                ),
                "Symlink output refused.",
            )
        except FileNotFoundError:
            pass
        raw = yaml.safe_dump(document, allow_unicode=True, sort_keys=False)
        temporary = ".p01-" + os.urandom(16).hex()
        descriptor = os.open(
            temporary,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
            0o600,
            dir_fd=directory_fd,
        )
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        _safe_path(root, relative)
        os.replace(
            temporary, parts[-1], src_dir_fd=directory_fd, dst_dir_fd=directory_fd
        )
    except (OSError, ValueError):
        raise InventoryError(
            "Inventory output failed; previous output preserved."
        ) from None
    finally:
        if temporary is not None:
            try:
                os.unlink(temporary, dir_fd=directory_fd)
            except FileNotFoundError:
                pass
        os.close(directory_fd)


def load_public(root, relative):
    """Load a bounded public YAML/JSON document without arbitrary constructors."""
    try:
        return yaml.safe_load(_read_public(Path(root).resolve(), relative))
    except (OSError, ValueError, yaml.YAMLError):
        raise InventoryError("Inventory input failed.") from None


def render_inventory(root, document, **kwargs):
    from scripts.lib.ops._workspace_render import render_inventory as render

    return render(root, document, **kwargs)
