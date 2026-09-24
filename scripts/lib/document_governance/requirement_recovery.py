"""Task-owned evidence for the single REQ-0012 stable-identity restoration.

This is not an alternate base selector. The ordinary loader remains strict, and
all unaffected allocations are parsed again against the requested comparison base.
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import re
import stat

from scripts.lib.document_governance.frontmatter import parse_frontmatter_text
from scripts.lib.document_governance.identity_history import (
    IdentityHistoryError,
    _run_git,
)

FIELD = "requirement_allocation_recovery_decisions"
REQUIREMENT_PATH = "docs/01.requirements/0012-laboratory.md"
REGISTRY_PATH = "docs/99.templates/registry.json"
ALLOCATION = "REQ-0012.FR"
# The owning package may sit in Stage 03 or, once completed, in the archive.
TASK_PATH = re.compile(
    r"docs/(?:98\.archive/completed/)?03\.specs/(?P<spec>[0-9]{4})-[a-z0-9][a-z0-9-]*/tasks/tsk-(?P<task>[0-9]{4})-[a-z0-9][a-z0-9-]*\.md"
)
EXPECTED_PINS = {
    "comparison_base_commit": "d1e6ded52808b02392c52472d5416518a3b959d6",
    "defect_commit": "70aaeffb84e8f6bc537241615d4743b79ccac079",
    "valid_predecessor_commit": "b66da447f68993dd9bddfd100bdd4c4b90d19be4",
}
EXPECTED_TASK = (
    "docs/98.archive/completed/03.specs/0180-home-dev-convergence/tasks/"
    "tsk-0001-home-dev-convergence.md"
)
PIN_FIELDS = tuple(EXPECTED_PINS)
FIXED = {
    "requirement_path": REQUIREMENT_PATH,
    "allocation_name": ALLOCATION,
    "predecessor_current_issued": [1, 2, 3, 4],
    "corrupt_declared": [1, 2, 3],
    "repaired_current_issued": [1, 2, 4],
    "repaired_reserved_history": [3],
    "disposition": "stable-identity-restoration",
}
LIMIT = 4 * 1024 * 1024


def _git(root, *args):
    return _run_git(root, tuple(args), max_output_bytes=LIMIT).text


def _regular_text(root, path):
    candidate = root
    for part in pathlib.PurePosixPath(path).parts:
        candidate = candidate / part
        if candidate.is_symlink():
            raise ValueError("recovery source is a symlink")
    info = candidate.stat()
    if not stat.S_ISREG(info.st_mode) or info.st_size > LIMIT:
        raise ValueError("recovery source is not a bounded regular file")
    with candidate.open("rb") as stream:
        data = stream.read(LIMIT + 1)
    if len(data) > LIMIT:
        raise ValueError("recovery source exceeded its byte bound")
    return data.decode("utf-8")


def _decision(root):
    rows = []
    total = 0
    paths = _git(
        root,
        "ls-files",
        "-z",
        "--",
        "docs/03.specs",
        "docs/98.archive/completed/03.specs",
    ).split("\0")
    for path in filter(None, paths):
        match = TASK_PATH.fullmatch(path)
        if match is None:
            continue
        text = _regular_text(root, path)
        total += len(text.encode("utf-8"))
        if total > LIMIT:
            raise ValueError("recovery Task scan exceeded its byte bound")
        metadata = parse_frontmatter_text(text)
        if FIELD not in metadata:
            continue
        if (
            path != EXPECTED_TASK
            or metadata.get("type") != "sdlc/task"
            or metadata.get("status") not in {"draft", "active", "completed"}
            or metadata.get("artifact_id")
            != f"SPEC-{match['spec']}-TSK-{match['task']}"
        ):
            raise ValueError("recovery decision has no current Task owner")
        decisions = metadata[FIELD]
        if not isinstance(decisions, list) or len(decisions) != 1:
            raise ValueError("recovery decision must contain one row")
        rows.extend(decisions)
    if len(rows) != 1 or not isinstance(rows[0], dict):
        raise ValueError("recovery requires exactly one tracked Task decision")
    row = rows[0]
    if set(row) != set(FIXED) | set(PIN_FIELDS) | {"repaired_requirement_sha256"}:
        raise ValueError("recovery decision keys are invalid")
    # JSON equality distinguishes booleans from integer allocation numbers.
    if any(json.dumps(row[key]) != json.dumps(value) for key, value in FIXED.items()):
        raise ValueError("unsupported recovery disposition")
    if any(row[field] != value for field, value in EXPECTED_PINS.items()):
        raise ValueError("recovery commit differs from the registered incident")
    for field in (*PIN_FIELDS, "repaired_requirement_sha256"):
        size = 64 if field == "repaired_requirement_sha256" else 40
        if (
            not isinstance(row[field], str)
            or re.fullmatch(rf"[0-9a-f]{{{size}}}", row[field]) is None
        ):
            raise ValueError("recovery commit or content pin is invalid")
    return row


def _state(registry_text):
    from scripts.lib.document_governance.registry import _unique_object

    value = json.loads(registry_text, object_pairs_hook=_unique_object)[
        "identity_spaces"
    ]["requirement"]["child_spaces"][ALLOCATION]
    numbers = [
        value["high_water"],
        value["next_number"],
        *value["current_issued"],
        *value["reserved_history"],
    ]
    if any(type(number) is not int for number in numbers):
        raise ValueError("recovery allocation numbers must be integers")
    return value


def _declared(text):
    section = re.search(r"(?ms)^## Functional Requirements\n(.*?)(?=^## |\Z)", text)
    if section is None:
        raise ValueError("recovery requirement section is missing")
    return sorted(
        set(int(n) for n in re.findall(r"REQ-0012-FR-([0-9]{4})", section[1]))
    )


def recover_pinned_requirement_baseline(revision, *, root):
    """Verify evidence, then return only the original FR allocation declaration."""
    from scripts.lib.document_governance.registry import (
        RegistryError,
        _trusted_blob_snapshot,
        load_trusted_requirement_allocation_baseline,
    )

    try:
        row = _decision(root)
        base = _git(root, "rev-parse", "--verify", f"{revision}^{{commit}}").strip()
        if base != row["comparison_base_commit"]:
            raise ValueError("recovery comparison base does not match")
        defect, predecessor = row["defect_commit"], row["valid_predecessor_commit"]
        if _git(root, "rev-parse", f"{defect}^").strip() != predecessor:
            raise ValueError("recovery predecessor is not the defect parent")
        for before, after in ((predecessor, defect), (defect, base), (base, "HEAD")):
            _git(root, "merge-base", "--is-ancestor", before, after)
        prior = load_trusted_requirement_allocation_baseline(predecessor, root=root)
        state = prior.child_spaces[ALLOCATION]
        if (
            state.high_water,
            state.next_number,
            state.current_issued,
            state.reserved_history,
        ) != (4, 5, (1, 2, 3, 4), ()):
            raise ValueError("recovery predecessor allocation differs")
        snapshots = [
            _trusted_blob_snapshot(commit, root=root)
            for commit in (predecessor, defect, base)
        ]
        old, broken, comparison = [texts[REQUIREMENT_PATH] for _, _, texts in snapshots]
        original_state = {
            "prefix": "REQ-0012-FR-",
            "width": 4,
            "child_spaces": {},
            "high_water": 4,
            "next_number": 5,
            "current_issued": [1, 2, 3, 4],
            "reserved_history": [],
        }
        for _, registry_text, _ in snapshots:
            if _state(registry_text) != original_state:
                raise ValueError("recovery historical registry differs")
        if (
            _declared(old) != [1, 2, 3, 4]
            or _declared(broken) != [1, 2, 3]
            or broken != comparison
        ):
            raise ValueError("recovery historical declarations differ")
        current = _regular_text(root, REQUIREMENT_PATH)
        if (
            hashlib.sha256(current.encode("utf-8")).hexdigest()
            != row["repaired_requirement_sha256"]
        ):
            raise ValueError("recovery candidate content pin differs")
        needle = "- **REQ-0012-FR-0003**:"
        if comparison.count(needle) != 1 or current != comparison.replace(
            needle, "- **REQ-0012-FR-0004**:"
        ):
            raise ValueError("recovery candidate changes more than the stable identity")
        if _declared(current) != [1, 2, 4] or "REQ-0012-FR-0003" in current:
            raise ValueError("recovery candidate reissues withdrawn identity")
        repaired_state = {
            **original_state,
            "current_issued": [1, 2, 4],
            "reserved_history": [3],
        }
        if _state(_regular_text(root, REGISTRY_PATH)) != repaired_state:
            raise ValueError("recovery candidate allocation differs")
        return {ALLOCATION: (1, 2, 3, 4)}
    except (
        ValueError,
        OSError,
        KeyError,
        TypeError,
        IdentityHistoryError,
        RegistryError,
    ) as error:
        raise RegistryError(
            f"pinned Requirement allocation recovery rejected: {error}"
        ) from error
