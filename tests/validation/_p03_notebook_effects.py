"""Exact, value-free effect validation for the isolated Notebook rehearsal."""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from typing import Any

from tests.validation._p03_owned_docker import NativeFixtureError


def contains_exact(value: Any, expected: str) -> bool:
    if value == expected:
        return True
    if isinstance(value, Mapping):
        return any(contains_exact(item, expected) for item in value.values())
    if isinstance(value, list):
        return any(contains_exact(item, expected) for item in value)
    return False


def validate_completed_job(value: Any, job_id: str, source_id: str) -> None:
    if not isinstance(value, Mapping) or value.get("status") != "completed":
        raise NativeFixtureError("job_shape_invalid")
    identity = value.get("id", value.get("job_id"))
    commands = [
        item
        for key, item in value.items()
        if key in {"command", "command_name", "name", "type"} and isinstance(item, str)
    ]
    if (
        identity != job_id
        or not any("embed" in item.casefold() for item in commands)
        or not contains_exact(value, source_id)
    ):
        raise NativeFixtureError("job_binding_invalid")


def validate_search(result: Any, source_id: str) -> int:
    if not isinstance(result, Mapping):
        raise NativeFixtureError("search_shape_invalid")
    total = result.get("total_count")
    rows = result.get("results")
    if (
        not isinstance(total, int)
        or total < 1
        or not isinstance(rows, list)
        or not rows
        or any(
            not isinstance(row, Mapping)
            or not isinstance(row.get("id"), str)
            or not contains_exact(row, source_id)
            for row in rows
        )
    ):
        raise NativeFixtureError("search_provenance_invalid")
    return total


def validate_embedding_events(lines: Sequence[str], offset: int = 0) -> int:
    try:
        rows = [json.loads(line) for line in lines[offset:]]
    except (TypeError, ValueError, json.JSONDecodeError) as error:
        raise NativeFixtureError("embedding_event_shape_invalid") from error
    embeddings = [
        row
        for row in rows
        if isinstance(row, Mapping) and row.get("kind") == "embedding"
    ]
    if not embeddings or any(
        set(row) != {"kind", "model", "dimension"}
        or row.get("model") != "embeddinggemma-2:740m"
        or row.get("dimension") != 768
        for row in embeddings
    ):
        raise NativeFixtureError("embedding_event_binding_invalid")
    return 768


def validate_chat_session(
    session: Any,
    session_id: str,
    expected_tail: Sequence[tuple[str, str]],
) -> int:
    messages = session.get("messages") if isinstance(session, Mapping) else None
    if (
        not isinstance(session, Mapping)
        or session.get("id") != session_id
        or not isinstance(messages, list)
    ):
        raise NativeFixtureError("chat_readback_missing")
    persisted = [
        (row.get("role"), row.get("content"))
        for row in messages
        if isinstance(row, Mapping) and row.get("role") in {"user", "assistant"}
    ]
    if persisted[-len(expected_tail) :] != list(expected_tail):
        raise NativeFixtureError("chat_content_readback_invalid")
    return len(messages)


def measured_restore_counts(
    notebooks: Any,
    sources: Any,
    session: Any,
    *,
    session_id: str,
    expected_chat_tail: Sequence[tuple[str, str]],
    text_results: int,
    vector_results: int,
    embedding_dimensions: int,
) -> dict[str, int]:
    if not isinstance(notebooks, list) or not isinstance(sources, list):
        raise NativeFixtureError("restore_dataset_shape_invalid")
    chat_messages = validate_chat_session(session, session_id, expected_chat_tail)
    if (
        not isinstance(text_results, int)
        or text_results < 1
        or not isinstance(vector_results, int)
        or vector_results < 1
        or embedding_dimensions != 768
    ):
        raise NativeFixtureError("restore_dataset_shape_invalid")
    return {
        "notebooks": len(notebooks),
        "sources": len(sources),
        "sessions": int(session.get("id") == session_id),
        "chat_messages": chat_messages,
        "text_results": text_results,
        "vector_results": vector_results,
        "embedding_dimensions": embedding_dimensions,
    }
