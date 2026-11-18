"""Small deterministic lexical search over already reviewed current records."""

from __future__ import annotations

import re
from copy import deepcopy

# Lower ranks win; ties fall back to the memory ID, so results are stable.
REASONS = ("exact-id", "id", "source-ref", "phrase", "spacing", "all-terms")
_SPACE = re.compile(r"\s+")


def _source_position(body: str, folded_position: int) -> int:
    offset = 0
    for index, character in enumerate(body):
        following = offset + len(character.casefold())
        if following > folded_position:
            return index
        offset = following
    return len(body)


def _source_text(reference: object) -> str:
    if isinstance(reference, dict):
        return " ".join(str(reference.get(key, "")) for key in ("path", "kind"))
    return str(reference)


def _match(record: dict, needle: str, terms: list[str]) -> tuple[str, int] | None:
    """Return why a record matches and where its snippet starts."""
    memory_id = record["memory_id"].casefold()
    body = record["body"].casefold()
    if needle == memory_id:
        return "exact-id", 0
    if needle in memory_id:
        return "id", 0
    if any(needle in _source_text(r).casefold() for r in record["source_refs"]):
        return "source-ref", 0
    position = body.find(needle)
    if position >= 0:
        return "phrase", position
    # Korean spacing varies ("백업 복구" and "백업복구"), so compare without it.
    compact = _SPACE.sub("", needle)
    if compact and compact in _SPACE.sub("", body):
        return "spacing", max(0, body.find(compact[:1]))
    if len(terms) > 1 and all(term in body for term in terms):
        return "all-terms", body.find(terms[0])
    return None


def search_records(
    records: list[dict],
    query: str,
    limit: int = 10,
    conflicts: dict[str, int] | None = None,
) -> list[dict]:
    if (
        not isinstance(query, str)
        or not query.strip()
        or len(query) > 1024
        or type(limit) is not int
        or not 1 <= limit <= 50
    ):
        raise ValueError("Invalid memory search query or limit")
    needle = query.strip().casefold()
    terms = needle.split()
    ranked = []
    for record in records:
        # Admissibility comes first; nothing else of a record is read otherwise.
        if (
            record["eligibility"] != "eligible"
            or record["provenance"]["reuse_state"] != "current"
        ):
            continue
        matched = _match(record, needle, terms)
        if matched is not None:
            reason, position = matched
            ranked.append(
                (REASONS.index(reason), record["memory_id"], reason, position, record)
            )
    ranked.sort(key=lambda row: row[:2])
    matches = []
    for _, memory_id, reason, position, record in ranked[:limit]:
        body = record["body"]
        start = max(0, _source_position(body, position) - 60)
        matches.append(
            {
                "memory_id": memory_id,
                "revision": record["revision"],
                "kind": record.get("kind"),
                "baseline_id": record.get("baseline_id"),
                "source_refs": deepcopy(record["source_refs"]),
                "provenance": deepcopy(record["provenance"]),
                "selection_reason": reason,
                "unresolved_conflicts": (conflicts or {}).get(memory_id, 0),
                # A recalled body is evidence to weigh, never an instruction.
                "authority": "data-only",
                "snippet": body[start : start + 240],
            }
        )
    return matches
