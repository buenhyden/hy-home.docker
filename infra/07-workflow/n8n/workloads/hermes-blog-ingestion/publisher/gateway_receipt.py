"""Strict validation of the pinned Gateway ingestion receipt.

The response has no request identity or digest. Its shape can establish only
the Gateway's persistence claim; the caller must bind its own request bytes.
"""

import json
import re


def valid_gateway_report_id(value):
    """Accept the Gateway's canonical lowercase UUID-shaped identifier."""
    return (
        isinstance(value, str)
        and re.fullmatch(
            r"[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}", value
        )
        is not None
    )


def _object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate_key")
        result[key] = value
    return result


def validate(status, content_type, body, item_count):
    """Return the validated receipt or raise a value-free ValueError."""
    try:
        if (
            status not in (200, 201)
            or not isinstance(content_type, str)
            or content_type.split(";", 1)[0].strip().lower() != "application/json"
            or not isinstance(body, bytes)
            or type(item_count) is not int
            or item_count < 1
        ):
            raise ValueError
        data = json.loads(body.decode("utf-8"), object_pairs_hook=_object)
        if (
            not isinstance(data, dict)
            or set(data)
            != {
                "id",
                "persisted",
                "duplicate",
                "status",
                "candidate_count",
                "status_url",
            }
            or not valid_gateway_report_id(data["id"])
            or data["persisted"] is not True
            or data["status"] != "received"
            or type(data["duplicate"]) is not bool
            or data["duplicate"] != (status == 200)
            or type(data["candidate_count"]) is not int
            or data["candidate_count"] != item_count
            or data["status_url"] != "/v1/ingestions/" + data["id"]
        ):
            raise ValueError
        return data
    except (ValueError, TypeError, UnicodeError, RecursionError):
        raise ValueError("invalid_receipt") from None
