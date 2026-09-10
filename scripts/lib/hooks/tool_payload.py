"""Normalize native edit payloads for both policy and post-edit checks."""

from __future__ import annotations

import json
import stat
from pathlib import Path, PurePosixPath

EDIT_TOOLS = frozenset({"Write", "Edit", "MultiEdit", "apply_patch", "ApplyPatch"})
MAX_PAYLOAD_BYTES = 1024 * 1024
MAX_TARGETS = 256


class PayloadError(ValueError):
    """An edit cannot safely be mapped to repository targets."""


def decode_payload(raw: str) -> dict[str, object]:
    if len(raw.encode("utf-8")) > MAX_PAYLOAD_BYTES:
        raise PayloadError("hook payload exceeds byte limit")
    try:
        data = json.loads(raw)
    except (ValueError, RecursionError) as error:
        raise PayloadError("hook payload is invalid JSON") from error
    if not isinstance(data, dict):
        raise PayloadError("hook payload must be an object")
    return data


def _relative_target(root: Path, value: str) -> str:
    if (
        not value
        or len(value.encode("utf-8")) > 4096
        or "\\" in value
        or any(ord(c) < 32 or ord(c) == 127 for c in value)
    ):
        raise PayloadError("unsafe changed path: invalid path bytes")
    candidate = PurePosixPath(value)
    if candidate.as_posix() != value or ".." in candidate.parts:
        raise PayloadError("unsafe changed path: noncanonical path")
    if candidate.is_absolute():
        try:
            candidate = candidate.relative_to(root)
        except ValueError as error:
            raise PayloadError("unsafe changed path: outside project root") from error
    if not candidate.parts:
        raise PayloadError("unsafe changed path: target is project root")
    current = root
    for index, part in enumerate(candidate.parts):
        current = current / part
        try:
            metadata = current.lstat()
        except FileNotFoundError:
            break
        if stat.S_ISLNK(metadata.st_mode):
            raise PayloadError("unsafe changed path: symlink component")
        final = index == len(candidate.parts) - 1
        if not final and not stat.S_ISDIR(metadata.st_mode):
            raise PayloadError("unsafe changed path: non-directory parent")
        if final and (not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1):
            raise PayloadError("unsafe changed path: non-regular or hardlinked target")
    return candidate.as_posix()


def _patch_edits(command: object) -> list[tuple[str, str]]:
    if not isinstance(command, str):
        raise PayloadError("patch input must contain a command string")
    # Native patch records use LF; Unicode separators remain filename/content bytes.
    # Rust trim uses Unicode White_Space; Python also strips C0 U+001C–001F.
    native_whitespace = (
        "\t\n\v\f\r \x85\xa0\u1680"
        "\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200a"
        "\u2028\u2029\u202f\u205f\u3000"
    )
    lines = command.replace("\r\n", "\n").strip(native_whitespace).split("\n")
    if not lines or lines[0] != "*** Begin Patch" or lines[-1] != "*** End Patch":
        raise PayloadError("patch envelope is invalid")
    edits: list[tuple[str, str]] = []
    targets: list[str] = []
    added: list[str] = []
    operation = ""
    body_started = False
    has_content = False
    end_of_file = False

    def finish() -> None:
        if operation == "*** Update File: " and not has_content:
            raise PayloadError("patch update has no body")
        if len(edits) + len(targets) > MAX_TARGETS:
            raise PayloadError("too many edit targets")
        replacement = "\n".join(added)
        edits.extend((path, replacement) for path in targets)

    for line in lines[1:-1]:
        header = next(
            (
                prefix
                for prefix in (
                    "*** Add File: ",
                    "*** Update File: ",
                    "*** Delete File: ",
                )
                if line.startswith(prefix)
            ),
            None,
        )
        if header:
            finish()
            targets = [line[len(header) :]]
            added = []
            operation = header
            body_started = False
            has_content = False
            end_of_file = False
        elif (
            line.startswith("*** Move to: ")
            and len(targets) == 1
            and operation == "*** Update File: "
            and not body_started
        ):
            targets.append(line[len("*** Move to: ") :])
        elif targets and operation != "*** Delete File: " and line.startswith("+"):
            if end_of_file:
                raise PayloadError("patch body follows end-of-file marker")
            added.append(line[1:])
            body_started = has_content = True
        elif operation == "*** Update File: " and (
            line == "@@" or line.startswith("@@ ")
        ):
            if body_started and not has_content:
                raise PayloadError("patch contains an empty hunk")
            body_started = True
            has_content = end_of_file = False
        elif operation == "*** Update File: " and line == "*** End of File":
            if not has_content or end_of_file:
                raise PayloadError("patch has a misplaced end-of-file marker")
            end_of_file = True
        elif operation == "*** Update File: " and (
            not line or line.startswith(("-", " "))
        ):
            if end_of_file:
                raise PayloadError("patch body follows end-of-file marker")
            body_started = has_content = True
        else:
            raise PayloadError("patch contains an unsupported or misplaced record")
    finish()
    return edits


def edit_targets(root: Path, data: dict[str, object]) -> tuple[tuple[str, str], ...]:
    """Return relative path/replacement pairs, preserving all edits to each file."""
    root = root.absolute()
    if root.resolve(strict=True) != root or not root.is_dir():
        raise PayloadError("project root must be a canonical physical directory")
    tool = data.get("tool_name", "")
    if not isinstance(tool, str):
        raise PayloadError("tool name must be a string")
    if tool and tool not in EDIT_TOOLS:
        return ()
    source = data.get("tool_input", {})
    if not isinstance(source, dict):
        raise PayloadError("edit input must be an object")
    edits: list[tuple[str, str]] = []

    def add(
        record: object, default_path: object = None, *, optional: bool = False
    ) -> None:
        if isinstance(record, str):
            edits.append((record, ""))
        elif isinstance(record, dict):
            for key in ("file_path", "path", "content", "new_string", "new_text"):
                if key in record and not isinstance(record[key], str):
                    raise PayloadError(
                        "edit path and replacement fields must be strings"
                    )
                if key in {"file_path", "path"} and key in record and not record[key]:
                    raise PayloadError("explicit edit path must not be empty")
            path = record.get("file_path") or record.get("path") or default_path
            if isinstance(path, str):
                text = next(
                    (
                        record[k]
                        for k in ("content", "new_string", "new_text")
                        if isinstance(record.get(k), str)
                    ),
                    "",
                )
                edits.append((path, text))
            elif not optional:
                raise PayloadError("edit record has no valid target")
        else:
            raise PayloadError("edit record must be a path or object")
        if len(edits) > MAX_TARGETS:
            raise PayloadError("too many edit targets")

    if tool in {"apply_patch", "ApplyPatch"}:
        edits = _patch_edits(source.get("command"))
    else:
        add(source, optional=True)
        for key in ("files", "paths", "edits"):
            records = source.get(key, [])
            if not isinstance(records, list):
                raise PayloadError("edit target collection must be a list")
            for record in records:
                add(record, source.get("file_path") or source.get("path"))
    if tool in EDIT_TOOLS and not edits:
        raise PayloadError("matched edit tool has no valid targets")
    return tuple(
        dict.fromkeys((_relative_target(root, path), text) for path, text in edits)
    )
