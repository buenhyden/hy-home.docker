"""Deliver the nearest folder AGENTS.md before a tool touches that folder.

Codex loads AGENTS.md only from the repository root down to its working
directory, and Claude Code skips AGENTS.md wherever a CLAUDE.md is on the
path. Neither reads `infra/AGENTS.md` when a session started at the root edits
`infra/...`. Claude reaches each guide through the folder's generated
`CLAUDE.md` import, so the shared PreToolUse dispatcher hands the full guide
text to Codex only, and to Claude only when a folder's shim is missing or no
longer imports `AGENTS.md`. Every edit also names its guide for both providers.
Full text is delivered once per session; SessionStart clears the record, so a
compacted or resumed session receives it again; a subagent keeps its own
record. Only guides Git tracks are delivered. The record lives in a per-user
state directory that must be owned by this user with mode 0700.
"""

from __future__ import annotations

import json
import os
import re
import stat
import subprocess
import tempfile
import time
from pathlib import Path, PurePosixPath

GUIDE_NAME = "AGENTS.md"
SHIM_NAME = "CLAUDE.md"
SHIM_IMPORT = b"@AGENTS.md"
MAX_GUIDE_BYTES = 16 * 1024
STATE_MAX_AGE_SECONDS = 7 * 24 * 3600
_SESSION_ID = re.compile(r"[A-Za-z0-9._-]{1,256}")


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
    # ponytail: age-based pruning; records are tiny and only one survives per session.
    cutoff = time.time() - STATE_MAX_AGE_SECONDS
    for record in directory.glob("*.json"):
        try:
            if record.lstat().st_mtime < cutoff:
                record.unlink()
        except OSError:
            pass
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


def tracked_guides(root: Path) -> frozenset[str]:
    """Folder guides Git tracks; an ignored or vendored AGENTS.md is data."""
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "ls-files", "-z", "--", ":(glob)**/" + GUIDE_NAME],
            capture_output=True,
            timeout=2,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return frozenset()
    if result.returncode != 0:
        return frozenset()
    names = result.stdout.decode("utf-8", errors="replace").split("\0")
    return frozenset(name for name in names if name and name != GUIDE_NAME)


def nearest_guide(
    root: Path, target: PurePosixPath, tracked: frozenset[str]
) -> str | None:
    """Return the closest tracked folder guide above `target`, never the root shim."""
    for parent in target.parents:
        if not parent.parts:
            return None
        guide = (parent / GUIDE_NAME).as_posix()
        if guide not in tracked:
            continue
        path = root / guide
        try:
            # The root is canonical, so any symlink component changes the path.
            if path.resolve(strict=True) == path and path.is_file():
                return guide
        except OSError:
            continue
    return None


def tool_targets(data: dict[str, object], edits: tuple[str, ...]) -> list[object]:
    """Edit targets plus the file a Read call opens."""
    targets: list[object] = list(edits)
    tool_input = data.get("tool_input")
    if data.get("tool_name") == "Read" and isinstance(tool_input, dict):
        targets.append(tool_input.get("file_path"))
    return targets


def session_key(data: dict[str, object]) -> object:
    """A subagent has its own context, so it gets its own delivery record."""
    session_id = data.get("session_id")
    agent_id = data.get("agent_id")
    if isinstance(session_id, str) and isinstance(agent_id, str) and agent_id:
        return f"{session_id}-{agent_id}"
    return session_id


def _guides_for(root: Path, values: list[object], tracked: frozenset[str]) -> list[str]:
    guides: list[str] = []
    for value in values:
        relative = _relative(root, value)
        guide = nearest_guide(root, relative, tracked) if relative else None
        if guide and guide not in guides:
            guides.append(guide)
    return guides


def pending_messages(
    root: Path,
    targets: list[object],
    session_id: object,
    *,
    edits: tuple[str, ...] = (),
    full: bool = True,
) -> list[str]:
    """Full guide text once per session, and a path reminder on every edit so
    a compacted session that kept only a summary re-reads it. Without `full`
    (Claude), text goes only to a guide whose shim cannot import it."""
    if not full and not edits:
        return []  # A Claude Read needs no reminder, so skip `git ls-files`.
    if not any(_relative(root, value) for value in [*targets, *edits]):
        return []
    tracked = tracked_guides(root)
    delivered = _full_messages(root, targets, session_id, tracked, full=full)
    shown = {guide for guide, _ in delivered}
    reminders = [
        f"Folder guide for this edit: `{guide}`. Re-read it if its text is no "
        "longer in context, for example after compaction."
        for guide in _guides_for(root, list(edits), tracked)
        if guide not in shown
    ]
    return [message for _, message in delivered] + reminders


def has_shim(root: Path, guide: str) -> bool:
    """True when the guide's folder holds a regular CLAUDE.md importing it."""
    shim = root / PurePosixPath(guide).with_name(SHIM_NAME)
    try:
        if not stat.S_ISREG(shim.lstat().st_mode):
            return False
        with open(shim, "rb") as handle:
            lines = handle.read(MAX_GUIDE_BYTES).splitlines()
    except OSError:
        return False
    return any(line.strip() == SHIM_IMPORT for line in lines)


def _full_messages(
    root: Path,
    targets: list[object],
    session_id: object,
    tracked: frozenset[str],
    *,
    full: bool = True,
) -> list[tuple[str, str]]:
    guides = [
        guide
        for guide in _guides_for(root, targets, tracked)
        if full or not has_shim(root, guide)
    ]
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
    # Build every message before recording delivery, so a read failure never
    # marks a guide as seen.
    messages = [(guide, _message(root, guide)) for guide in fresh]
    if messages and state:
        _write_state(state, seen | set(fresh))
    return messages


RESTART_SOURCES = frozenset({"compact", "resume"})


def restart_message(root: Path) -> str:
    """Re-read instruction for a session that resumed or was compacted."""
    guides = sorted(tracked_guides(root))
    listing = "\n".join(f"- `{guide}`" for guide in guides) or "- none tracked"
    return (
        "Folder guides loaded earlier may now survive only as a summary. Before "
        "changing a file, re-read the nearest folder `AGENTS.md` above it:\n"
        f"{listing}\n"
        "Recovery: `git ls-files '*/AGENTS.md'` lists them. Claude reloads a "
        "folder's `CLAUDE.md` import when it next opens a file there, and the "
        "PreToolUse hook delivers the guide to Codex again and names it on "
        "every edit."
    )


def _write_state(state: Path, guides: set[str]) -> None:
    with tempfile.NamedTemporaryFile(
        "w", dir=state.parent, delete=False, encoding="utf-8"
    ) as handle:
        name = handle.name
        try:
            json.dump(sorted(guides), handle)
        except BaseException:
            handle.close()
            os.unlink(name)
            raise
    try:
        os.replace(name, state)
    except BaseException:
        os.unlink(name)
        raise


def _message(root: Path, guide: str) -> str:
    with open(root / guide, "rb") as handle:
        raw = handle.read(MAX_GUIDE_BYTES + 1)
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
