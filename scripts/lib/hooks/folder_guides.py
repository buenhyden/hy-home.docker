"""Deliver the nearest folder AGENTS.md before a tool touches that folder.

Codex loads AGENTS.md only from the repository root down to its working
directory, and Claude Code skips AGENTS.md wherever a CLAUDE.md is on the
path. Neither reads `infra/AGENTS.md` when a session started at the root edits
`infra/...`, so the shared PreToolUse dispatcher hands the guide to the model.
Each guide is delivered once per session; SessionStart clears the record, so a
compacted or resumed session receives it again. The record lives in a
per-user state directory that must be owned by this user with mode 0700.
"""

from __future__ import annotations

import json
import os
import re
import stat
import tempfile
from pathlib import Path, PurePosixPath

GUIDE_NAME = "AGENTS.md"
MAX_GUIDE_BYTES = 16 * 1024
_SESSION_ID = re.compile(r"[A-Za-z0-9._-]{1,128}")


def _state_directory() -> Path | None:
    """A per-user state directory this user owns, never a shared /tmp name."""
    base = os.environ.get("XDG_STATE_HOME") or str(Path.home() / ".local/state")
    directory = Path(base) / "hy-home" / "folder-guides"
    try:
        directory.mkdir(mode=0o700, parents=True, exist_ok=True)
        info = directory.lstat()
    except OSError:
        return None
    if (
        not stat.S_ISDIR(info.st_mode)
        or info.st_uid != os.getuid()
        or info.st_mode & 0o077
    ):
        return None
    return directory


def _state_file(session_id: object) -> Path | None:
    if not isinstance(session_id, str) or not _SESSION_ID.fullmatch(session_id):
        return None
    directory = _state_directory()
    return directory / f"{session_id}.json" if directory else None


def _relative(root: Path, value: object) -> PurePosixPath | None:
    if not isinstance(value, str) or not value or "\x00" in value:
        return None
    candidate = PurePosixPath(value)
    if ".." in candidate.parts:
        return None
    if candidate.is_absolute():
        try:
            candidate = candidate.relative_to(root.as_posix())
        except ValueError:
            return None
    return candidate if candidate.parts else None


def nearest_guide(root: Path, target: PurePosixPath) -> str | None:
    """Return the closest folder guide above `target`, never the root shim."""
    for parent in target.parents:
        if not parent.parts:
            return None
        path = root / parent / GUIDE_NAME
        if path.is_file() and not path.is_symlink():
            return (parent / GUIDE_NAME).as_posix()
    return None


def tool_targets(data: dict[str, object], edits: tuple[str, ...]) -> list[object]:
    """Edit targets plus the file a Read call opens."""
    targets: list[object] = list(edits)
    tool_input = data.get("tool_input")
    if data.get("tool_name") == "Read" and isinstance(tool_input, dict):
        targets.append(tool_input.get("file_path"))
    return targets


def pending_messages(
    root: Path, targets: list[object], session_id: object
) -> list[str]:
    guides: list[str] = []
    for value in targets:
        relative = _relative(root, value)
        guide = nearest_guide(root, relative) if relative else None
        if guide and guide not in guides:
            guides.append(guide)
    if not guides:
        return []
    state = _state_file(session_id)
    seen: set[str] = set()
    if state and state.is_file():
        try:
            seen = set(json.loads(state.read_text(encoding="utf-8")))
        except (OSError, ValueError, TypeError):
            seen = set()
    fresh = [guide for guide in guides if guide not in seen]
    if not fresh:
        return []
    if state:
        with tempfile.NamedTemporaryFile(
            "w", dir=state.parent, delete=False, encoding="utf-8"
        ) as handle:
            json.dump(sorted(seen | set(fresh)), handle)
        os.replace(handle.name, state)
    return [_message(root, guide) for guide in fresh]


def _message(root: Path, guide: str) -> str:
    raw = (root / guide).read_bytes()
    text = raw[:MAX_GUIDE_BYTES].decode("utf-8", errors="replace")
    if len(raw) > MAX_GUIDE_BYTES:
        text += f"\n\n[truncated at {MAX_GUIDE_BYTES} bytes; read `{guide}` in full]"
    folder = PurePosixPath(guide).parent.as_posix()
    return (
        f"Folder guide `{guide}` applies to files under `{folder}/`. "
        "Bootstrap step 4 requires it before changing a file there:\n\n"
        f"{text.strip()}"
    )


def reset(session_id: object) -> None:
    state = _state_file(session_id)
    if state:
        state.unlink(missing_ok=True)
