"""Small deterministic lexical search over already reviewed current records."""

from __future__ import annotations

from copy import deepcopy


def _source_position(body: str, folded_position: int) -> int:
    offset = 0
    for index, character in enumerate(body):
        following = offset + len(character.casefold())
        if following > folded_position:
            return index
        offset = following
    return len(body)


def search_records(records: list[dict], query: str, limit: int = 10) -> list[dict]:
    if (
        not isinstance(query, str)
        or not query.strip()
        or len(query) > 1024
        or type(limit) is not int
        or not 1 <= limit <= 50
    ):
        raise ValueError("Invalid memory search query or limit")
    needle = query.strip().casefold()
    matches = []
    for record in sorted(records, key=lambda row: row["memory_id"]):
        if (
            record["eligibility"] != "eligible"
            or record["provenance"]["reuse_state"] != "current"
        ):
            continue
        body = record["body"]
        position = body.casefold().find(needle)
        if position < 0:
            continue
        start = max(0, _source_position(body, position) - 60)
        snippet = body[start : start + 240]
        matches.append(
            {
                "memory_id": record["memory_id"],
                "revision": record["revision"],
                "source_refs": deepcopy(record["source_refs"]),
                "provenance": deepcopy(record["provenance"]),
                "snippet": snippet,
            }
        )
        if len(matches) == limit:
            break
    return matches
