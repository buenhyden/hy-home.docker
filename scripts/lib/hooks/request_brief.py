"""Check request and scope consistency for a native session's explicit brief."""

from __future__ import annotations

import contextlib
import fcntl
import hashlib
import json
import os
import re
import secrets
import stat
import subprocess
import sys
from pathlib import Path

from scripts.lib.hooks.tool_payload import PayloadError, _relative_target

CONTRACT_VERSION = "3.0.1"
MAX_BYTES = 1024 * 1024
MAX_MATERIAL_INPUTS = 32
SESSION = re.compile(r"[A-Za-z0-9._-]{1,256}")
REQUEST_REVISION = re.compile(r"[0-9a-f]{32}")
SHA256 = re.compile(r"[0-9a-f]{64}")
MISSING_BRIEF = "Request brief unavailable. Refresh and bind the current scope."
USAGE = "Use status SESSION, bind SESSION, or check SESSION dispatch REQUEST_REVISION BRIEF_REVISION PATH..."
BINDING_FIELDS = {
    "request_ref",
    "request_digest",
    "request_revision",
    "workspace_id",
    "baseline_id",
}
LIST_FIELDS = {
    "in_scope",
    "out_of_scope",
    "constraints",
    "acceptance_criteria",
    "assumptions",
    "expected_checks",
}
BRIEF_FIELDS = (
    BINDING_FIELDS
    | LIST_FIELDS
    | {
        "contract_version",
        "brief_id",
        "revision",
        "goal",
        "known_facts",
        "unresolved_questions",
        "risk",
        "authority_ref",
        "allowed_mutations",
        "material_inputs",
        "state",
    }
)
SOURCE_FIELDS = {
    "source_id",
    "kind",
    "logical_uri",
    "content_digest",
    "revision",
    "observed_at",
    "access_scope",
    "trust",
}
FILE_FLAGS = os.O_NOFOLLOW | os.O_NONBLOCK


class BriefError(ValueError):
    """The brief cannot prove that the proposed scope is current."""


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _strings(value: object) -> bool:
    return isinstance(value, list) and all(_nonempty(item) for item in value)


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result = dict(pairs)
    if len(result) != len(pairs):
        raise BriefError("Brief JSON contains duplicate keys.")
    return result


def _decode(raw: bytes) -> dict:
    if len(raw) > MAX_BYTES:
        raise BriefError("Brief input exceeds its size limit.")
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_object)
    except (ValueError, RecursionError) as error:
        raise BriefError("Brief JSON is invalid.") from error
    if not isinstance(value, dict):
        raise BriefError("Brief JSON must be an object.")
    return value


def _git(root: Path, *arguments: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-c", "core.fsmonitor=false", "--literal-pathspecs", *arguments],
        cwd=root,
        env={
            "PATH": os.defpath,
            "GIT_CONFIG_GLOBAL": "/dev/null",
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_NO_REPLACE_OBJECTS": "1",
            "GIT_OPTIONAL_LOCKS": "0",
        },
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        timeout=2,
        check=False,
    )


def _git_head(root: Path) -> str:
    result = _git(root, "rev-parse", "--show-toplevel", "--verify", "HEAD")
    lines = os.fsdecode(result.stdout).splitlines()
    if (
        result.returncode
        or len(lines) != 2
        or lines[0] != str(root)
        or not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", lines[1])
    ):
        raise BriefError("Exact workspace Git baseline is unavailable.")
    return lines[1]


def _private_file(descriptor: int) -> None:
    metadata = os.fstat(descriptor)
    if (
        not stat.S_ISREG(metadata.st_mode)
        or metadata.st_uid != os.getuid()
        or metadata.st_mode & 0o077
        or metadata.st_nlink != 1
    ):
        raise BriefError("Brief state is not a private regular file.")


@contextlib.contextmanager
def _session_location(root: Path, session: object, *, create: bool = False):
    if not isinstance(session, str) or not SESSION.fullmatch(session):
        raise FileNotFoundError
    base = Path(os.environ.get("XDG_STATE_HOME") or Path.home() / ".local/state")
    directory = base / "hy-home" / "request-brief"
    if not directory.is_absolute() or directory.resolve() != directory:
        raise BriefError("Brief state directory is not canonical.")
    if create:
        directory.mkdir(mode=0o700, parents=True, exist_ok=True)
    name = hashlib.sha256(f"{root}\0{session}".encode()).hexdigest()
    directory_fd = os.open(directory, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        metadata = os.fstat(directory_fd)
        if metadata.st_uid != os.getuid() or metadata.st_mode & 0o077:
            raise BriefError("Brief state directory is not private.")
        yield directory_fd, name
    finally:
        os.close(directory_fd)


@contextlib.contextmanager
def _locked(directory: int, name: str, *, write=False, create=False):
    flags = (os.O_RDWR if write else os.O_RDONLY) | FILE_FLAGS
    if create:
        flags |= os.O_CREAT
    try:
        lock = os.open(f"{name}.lock", flags, 0o600, dir_fd=directory)
    except FileNotFoundError:
        for suffix in ("json", "revision"):
            try:
                os.stat(f"{name}.{suffix}", dir_fd=directory, follow_symlinks=False)
            except FileNotFoundError:
                continue
            raise BriefError("Brief enrollment marker is missing.") from None
        raise
    try:
        _private_file(lock)
        fcntl.flock(lock, (fcntl.LOCK_EX if write else fcntl.LOCK_SH) | fcntl.LOCK_NB)
        enrollment = os.pread(lock, 2, 0)
        if enrollment not in {b"", b"1"}:
            raise BriefError("Brief enrollment marker is invalid.")
        yield lock, enrollment == b"1"
    finally:
        os.close(lock)


def _load(directory: int, name: str) -> dict:
    descriptor = os.open(name, os.O_RDONLY | FILE_FLAGS, dir_fd=directory)
    with os.fdopen(descriptor, "rb") as handle:
        _private_file(handle.fileno())
        return _decode(handle.read(MAX_BYTES + 1))


def _save(directory: int, name: str, state: dict) -> None:
    temporary = f".{secrets.token_hex(16)}.tmp"
    descriptor = os.open(
        temporary,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | FILE_FLAGS,
        0o600,
        dir_fd=directory,
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(state, handle)
        os.replace(temporary, name, src_dir_fd=directory, dst_dir_fd=directory)
    except BaseException:
        os.unlink(temporary, dir_fd=directory)
        raise


def _rotate_revision(
    directory: int, name: str, *, existing: bool = False
) -> tuple[str, dict | None]:
    marker = f"{name}.revision"
    # Invalidate independently of the bind lock, even if that writer is interrupted.
    fcntl.flock(directory, fcntl.LOCK_EX)
    try:
        try:
            previous = _load(directory, marker)
        except (OSError, BriefError):
            if existing:
                raise
            previous = None
        revision = secrets.token_hex(16)
        _save(directory, marker, {"revision": revision})
        return revision, previous
    finally:
        fcntl.flock(directory, fcntl.LOCK_UN)


def _require_revision(directory: int, name: str, revision: str) -> None:
    checkpoint = _load(directory, f"{name}.revision")
    if checkpoint != {"revision": revision}:
        raise BriefError("Request brief revision is stale. Refresh the current scope.")


def _observation(root: Path, digest: str, revision: str) -> dict[str, str]:
    return {
        "request_ref": f"native-request:{revision}",
        "request_digest": digest,
        "request_revision": revision,
        "workspace_id": str(root),
        "baseline_id": _git_head(root),
    }


def _event_in_workspace(root: Path, data: dict) -> bool:
    cwd = data.get("cwd")
    return cwd is None or (
        isinstance(cwd, str)
        and Path(cwd).is_absolute()
        and Path(cwd).resolve().is_relative_to(root)
    )


def _bound_authority(brief: object) -> dict | None:
    if not isinstance(brief, dict) or brief.get("state") not in (
        "ready",
        "needs-clarification",
    ):
        return None
    reference = brief.get("native_reference")
    if (
        not isinstance(reference, str)
        or not re.fullmatch(r"native-request:[0-9a-f]{32}", reference)
        or not _strings(brief.get("allowed"))
        or not _strings(brief.get("held"))
        or not isinstance(brief.get("inputs"), dict)
    ):
        return None
    ceiling = sorted(set(brief["allowed"]).difference(brief["held"]))
    return (
        {"reference": reference, "allowed": ceiling, "inputs": brief["inputs"]}
        if ceiling
        else None
    )


def _prior_authority(
    root: Path,
    state: dict,
    observed: dict,
    previous: dict | None,
    *,
    continue_session: bool = False,
) -> dict | None:
    try:
        request = _request(root, state)
        if previous != {"revision": request["request_revision"]} or (
            request["baseline_id"] != observed["baseline_id"]
        ):
            return None
        recovered = _bound_authority(state.get("brief"))
        # PreCompact and SessionStart can arrive before the planner can rebind.
        if continue_session and state.get("brief") is None:
            recovered = _retained_authority(state, request)
        if recovered:
            _check_inputs(root, recovered["inputs"])
        return recovered
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError):
        return None


def observe_request(root: Path, data: dict) -> str:
    """Record the native prompt fingerprint, without retaining the prompt."""
    if data.get("agent_id") or data.get("hook_event_name") != "UserPromptSubmit":
        return ""
    root = root.resolve()
    session = data.get("session_id")
    prompt = data.get("prompt")
    try:
        with _session_location(root, session, create=True) as (directory, name):
            revision, previous = _rotate_revision(directory, name)
            with _locked(directory, name, write=True, create=previous is None):
                if not _event_in_workspace(root, data) or not _nonempty(prompt):
                    return ""
                raw = prompt.encode("utf-8")
                if len(raw) > MAX_BYTES:
                    return ""
                observed = _observation(root, hashlib.sha256(raw).hexdigest(), revision)
                try:
                    prior = _prior_authority(
                        root, _load(directory, f"{name}.json"), observed, previous
                    )
                except (OSError, BriefError):
                    prior = None
                _require_revision(directory, name, revision)
                _save(
                    directory,
                    f"{name}.json",
                    {"request": observed, "brief": None, "prior_authority": prior},
                )
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError):
        return ""
    return (
        "Request brief consistency is available for this session. After read-only "
        "discovery, use `python3 -m scripts.lib.hooks.request_brief status "
        f"{session}` from the repository root and bind the brief before covered "
        "edits or a mutating worker handoff. Native authorization remains required."
    )


def _request(root: Path, state: dict) -> dict[str, str]:
    request = state.get("request")
    if (
        not isinstance(request, dict)
        or request.keys() != BINDING_FIELDS
        or not all(_nonempty(value) for value in request.values())
        or request["workspace_id"] != str(root)
        or not REQUEST_REVISION.fullmatch(request["request_revision"])
        or request["request_ref"] != f"native-request:{request['request_revision']}"
        or not SHA256.fullmatch(request["request_digest"])
    ):
        raise BriefError(MISSING_BRIEF)
    return request


def _current(root: Path, state: dict, directory: int, name: str) -> dict[str, str]:
    request = _request(root, state)
    _require_revision(directory, name, request["request_revision"])
    return {**request, "baseline_id": _git_head(root)}


def invalidate_request(root: Path, data: dict) -> None:
    """Rotate freshness on resume/compact without retaining scope or approval."""
    if data.get("agent_id") or data.get("source") not in {"compact", "resume"}:
        return
    root = root.resolve()
    try:
        with _session_location(root, data.get("session_id")) as (
            directory,
            name,
        ):
            revision, previous = _rotate_revision(directory, name, existing=True)
            with _locked(directory, name, write=True):
                state = _load(directory, f"{name}.json")
                brief = state.get("brief")
                if not _event_in_workspace(root, data) or (
                    isinstance(brief, dict) and brief.get("state") == "withdrawn"
                ):
                    return
                current = _request(root, state)
                if previous != {"revision": current["request_revision"]}:
                    return
                refreshed = _observation(root, current["request_digest"], revision)
                prior = _prior_authority(
                    root, state, refreshed, previous, continue_session=True
                )
                _require_revision(directory, name, revision)
                _save(
                    directory,
                    f"{name}.json",
                    {"request": refreshed, "brief": None, "prior_authority": prior},
                )
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError):
        return


def _path(root: Path, value: str) -> str:
    try:
        return _relative_target(root, value)
    except (OSError, PayloadError, UnicodeError) as error:
        raise BriefError("Brief action contains an unsafe workspace path.") from error


def _action_set(root: Path, values: object, scope: set[str]) -> set[str]:
    if not _strings(values):
        raise BriefError(
            "Brief actions must be a list of exact edit or dispatch paths."
        )
    for value in values:
        action, separator, path = value.partition(":")
        if (
            not separator
            or action not in {"edit", "dispatch"}
            or _path(root, path) not in scope
            or Path(path).is_absolute()
        ):
            raise BriefError("Brief action exceeds its declared workspace scope.")
    return set(values)


def _validate_facts(facts: object) -> None:
    if not isinstance(facts, list):
        raise BriefError("Brief facts require distinct sourced observations.")
    for fact in facts:
        if (
            not isinstance(fact, dict)
            or fact.keys() != {"claim", "source_refs"}
            or not _nonempty(fact["claim"])
            or not isinstance(fact["source_refs"], list)
            or not fact["source_refs"]
        ):
            raise BriefError("Brief fact sources are missing.")
        for source in fact["source_refs"]:
            if (
                not isinstance(source, dict)
                or source.keys() != SOURCE_FIELDS
                or not all(_nonempty(value) for value in source.values())
                or source["kind"] not in {"document", "code", "session", "observation"}
                or source["trust"] not in {"untrusted", "reviewed-source"}
            ):
                raise BriefError("Brief fact source metadata is invalid.")


def _check_inputs(root: Path, inputs: dict) -> None:
    if not inputs:
        return
    if len(inputs) > MAX_MATERIAL_INPUTS:
        raise BriefError("Brief material inputs exceed their count limit.")
    for path, digest in inputs.items():
        if (
            _path(root, path) != path
            or ".git" in Path(path).parts
            or not isinstance(digest, str)
            or not SHA256.fullmatch(digest)
        ):
            raise BriefError(
                "Brief material inputs require relative paths and SHA-256."
            )
    result = _git(root, "ls-files", "--stage", "-z", "--", *inputs)
    tracked = set()
    for entry in result.stdout.split(b"\0"):
        header, separator, path = entry.partition(b"\t")
        mode, _, stage = header.partition(b" ")
        if separator and mode in {b"100644", b"100755"} and stage.endswith(b" 0"):
            tracked.add(os.fsdecode(path))
    if result.returncode or not set(inputs).issubset(tracked):
        raise BriefError("Brief material inputs must be tracked regular files.")
    for path, digest in inputs.items():
        descriptor = os.open(root / path, os.O_RDONLY | FILE_FLAGS)
        with os.fdopen(descriptor, "rb") as handle:
            metadata = os.fstat(handle.fileno())
            if not stat.S_ISREG(metadata.st_mode) or metadata.st_size > MAX_BYTES:
                raise BriefError("Brief material input is not a bounded regular file.")
            content = handle.read(MAX_BYTES + 1)
        if len(content) > MAX_BYTES or hashlib.sha256(content).hexdigest() != digest:
            raise BriefError("A brief material input changed. Refresh the brief.")


def _retained_authority(state: dict, current: dict) -> dict | None:
    prior = state.get("prior_authority")
    if state["request"] != current or not isinstance(prior, dict):
        return None
    reference = prior.get("reference")
    if (
        not isinstance(reference, str)
        or not re.fullmatch(r"native-request:[0-9a-f]{32}", reference)
        or not _strings(prior.get("allowed"))
        or not prior["allowed"]
        or not isinstance(prior.get("inputs"), dict)
    ):
        return None
    return prior


def _validate_brief(
    root: Path, record: dict, current: dict, prior: dict | None
) -> dict:
    if (
        record.keys() != BRIEF_FIELDS
        or record["contract_version"] != CONTRACT_VERSION
        or not _nonempty(record["brief_id"])
        or type(record["revision"]) is not int
        or record["revision"] < 1
        or not _nonempty(record["goal"])
        or not isinstance(record["risk"], str)
        or record["risk"] not in {"low", "medium", "high"}
        or not all(_strings(record[field]) for field in LIST_FIELDS)
        or not record["in_scope"]
        or not record["acceptance_criteria"]
    ):
        raise BriefError("BriefRecord goal, acceptance, or metadata is invalid.")
    if any(record[key] != current[key] for key in BINDING_FIELDS):
        raise BriefError(
            "Brief request revision or baseline is stale. Refresh the brief."
        )
    authority = record["authority_ref"]
    if authority is not None and not _nonempty(authority):
        raise BriefError("Brief authority reference is invalid.")
    scope = set(record["in_scope"])
    if any(_path(root, path) != path for path in scope) or scope.intersection(
        record["out_of_scope"]
    ):
        raise BriefError("Brief scope paths are invalid or contradictory.")
    _validate_facts(record["known_facts"])
    allowed = _action_set(root, record["allowed_mutations"], scope)
    questions = record["unresolved_questions"]
    if not isinstance(questions, list):
        raise BriefError("Brief questions must identify their affected actions.")
    held: set[str] = set()
    for question in questions:
        if (
            not isinstance(question, dict)
            or question.keys() != {"question", "affected_actions", "recommendation"}
            or not _nonempty(question["question"])
            or not _nonempty(question["recommendation"])
            or not question["affected_actions"]
        ):
            raise BriefError("Brief questions must identify their affected actions.")
        held.update(_action_set(root, question["affected_actions"], scope))
    expected = "needs-clarification" if held else "ready"
    state = record["state"]
    if not isinstance(state, str) or (
        state != expected
        and (state not in {"discovered", "stale", "withdrawn"} or allowed)
    ):
        raise BriefError("Brief state and held actions are inconsistent.")
    inputs = record["material_inputs"]
    if not isinstance(inputs, dict):
        raise BriefError("Brief material inputs must be an object.")
    _check_inputs(root, inputs)
    native_reference = None
    if authority == current["request_ref"]:
        native_reference = authority
    elif prior and authority == prior["reference"]:
        if not allowed.issubset(prior["allowed"]) or inputs != prior["inputs"]:
            raise BriefError(
                "Brief reuse exceeds the prior scope or changes its inputs."
            )
        native_reference = authority
    return {
        "revision": record["revision"],
        "state": state,
        "native_reference": native_reference,
        "allowed": sorted(allowed),
        "held": sorted(held),
        "inputs": inputs,
    }


def _check_scope(
    root: Path,
    state: dict,
    actions: set[str],
    directory: int,
    name: str,
    *,
    prepared_revisions: tuple[str, str] | None = None,
) -> None:
    current = _current(root, state, directory, name)
    brief = state.get("brief")
    if (
        not isinstance(brief, dict)
        or brief.get("state") not in ("ready", "needs-clarification")
        or state["request"] != current
        or type(brief.get("revision")) is not int
        or brief["revision"] < 1
        or not _strings(brief.get("allowed"))
        or not _strings(brief.get("held"))
        or not isinstance(brief.get("inputs"), dict)
    ):
        raise BriefError(MISSING_BRIEF)
    if prepared_revisions is not None and prepared_revisions != (
        current["request_revision"],
        str(brief["revision"]),
    ):
        raise BriefError(
            "Prepared handoff revisions are stale. Reconcile the envelope."
        )
    prior = _retained_authority(state, current)
    reference = brief.get("native_reference")
    if reference != current["request_ref"] and (
        not prior or reference != prior["reference"]
    ):
        raise BriefError("Brief has no locally corroborated native request reference.")
    if actions.intersection(brief["held"]):
        raise BriefError("A material question holds this brief action.")
    if not actions.issubset(brief["allowed"]):
        raise BriefError("This action exceeds the bound request brief scope.")
    _check_inputs(root, brief["inputs"])
    _require_revision(directory, name, current["request_revision"])


def guard_edits(root: Path, data: dict, edits: tuple[str, ...]) -> str | None:
    """Deny known edit targets for an enrolled session if consistency fails."""
    if not edits:
        return None
    root = root.resolve()
    enrolled = False
    try:
        with (
            _session_location(root, data.get("session_id")) as (directory, name),
            _locked(directory, name) as (_, enrolled),
        ):
            if not enrolled:
                return None
            if not _event_in_workspace(root, data):
                return MISSING_BRIEF
            paths = {_path(root, path) for path in edits}
            actions = {f"edit:{path}" for path in paths}
            if data.get("agent_id"):
                actions.update(f"dispatch:{path}" for path in paths)
            state = _load(directory, f"{name}.json")
            _check_scope(root, state, actions, directory, name)
    except FileNotFoundError:
        return MISSING_BRIEF if enrolled else None
    except BriefError as error:
        return str(error)
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError):
        return MISSING_BRIEF
    return None


def main(argv: list[str] | None = None) -> int:
    arguments = sys.argv[1:] if argv is None else argv
    if len(arguments) < 2:
        print(USAGE, file=sys.stderr)
        return 2
    command, session, *extra = arguments
    if not (
        (command in {"status", "bind"} and not extra)
        or (
            command == "check"
            and len(extra) >= 4
            and extra[0] == "dispatch"
            and REQUEST_REVISION.fullmatch(extra[1])
            and re.fullmatch(r"[1-9][0-9]*", extra[2])
        )
    ):
        print(USAGE, file=sys.stderr)
        return 2
    try:
        record = (
            _decode(sys.stdin.buffer.read(MAX_BYTES + 1)) if command == "bind" else None
        )
        root = Path.cwd().resolve()
        with (
            _session_location(root, session) as (directory, name),
            _locked(directory, name, write=command == "bind") as (lock, enrolled),
        ):
            state = _load(directory, f"{name}.json")
            if command == "status":
                current = _current(root, state, directory, name)
                prior = _retained_authority(state, current)
                _require_revision(directory, name, current["request_revision"])
                fields = (
                    {**current, "prior_authority_ref": prior["reference"]}
                    if prior
                    else current
                )
                print(json.dumps(fields, sort_keys=True))
                return 0
            if command == "bind":
                current = _current(root, state, directory, name)
                prior = _retained_authority(state, current)
                brief = _validate_brief(root, record, current, prior)
                previous = state.get("brief")
                if previous is not None and (
                    not isinstance(previous, dict)
                    or previous.get("state") == "withdrawn"
                    or type(previous.get("revision")) is not int
                    or brief["revision"] <= previous["revision"]
                ):
                    raise BriefError(
                        "Brief was withdrawn or its revision did not advance."
                    )
                revision = current["request_revision"]
                _require_revision(directory, name, revision)
                os.pwrite(lock, b"1", 0)
                retained = (
                    _bound_authority(brief)
                    if prior and brief["native_reference"] == prior["reference"]
                    else None
                )
                _save(
                    directory,
                    f"{name}.json",
                    {"request": current, "brief": brief, "prior_authority": retained},
                )
                _require_revision(directory, name, revision)
                print(
                    "Brief consistency recorded. Native permission is still required."
                )
            else:
                if not enrolled:
                    raise BriefError(MISSING_BRIEF)
                paths = {_path(root, path) for path in extra[3:]}
                _check_scope(
                    root,
                    state,
                    {
                        f"{action}:{path}"
                        for path in paths
                        for action in ("edit", "dispatch")
                    },
                    directory,
                    name,
                    prepared_revisions=(extra[1], extra[2]),
                )
                print("Brief consistency checked. Native permission is still required.")
    except BriefError as error:
        print(str(error), file=sys.stderr)
        return 1
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError):
        print(MISSING_BRIEF, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
