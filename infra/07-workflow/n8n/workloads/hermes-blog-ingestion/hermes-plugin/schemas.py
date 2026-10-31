"""Research report submission tool schema."""

from __future__ import annotations

REPORT_SCHEMA = {
    "type": "object",
    "properties": {
        "schema_version": {"type": "string"},
        "producer": {"type": "object"},
        "job_id": {"type": "string"},
        "run_id": {"type": "string"},
        "fire_id": {"type": "string"},
        "report_kind": {"type": "string"},
        "scheduled_at": {"type": "string"},
        "generated_at": {"type": "string"},
        "collected_at": {"type": "string"},
        "source_ref": {"type": "string"},
        "source_text": {"type": "string"},
        "source_sha256": {"type": "string"},
        "idempotency_key": {"type": "string"},
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "source_quotes": {
                        "type": "array",
                        "minItems": 1,
                        "maxItems": 3,
                        "items": {"type": "string", "minLength": 1, "maxLength": 500},
                    }
                },
            },
        },
        "companion_evidence": {"type": "object"},
    },
    "required": [
        "schema_version",
        "producer",
        "job_id",
        "run_id",
        "report_kind",
        "scheduled_at",
        "generated_at",
        "collected_at",
        "source_ref",
        "idempotency_key",
        "items",
    ],
}

ALLOWED_JOBS = {
    "6eabd835f969": "strategy-news",
    "25674fbc0bf3": "devops-brief",
    "8d0925bc571d": "solo-dev-ideas",
}

ALLOWED_REPORT_KINDS = {
    "6eabd835f969": "news",
    "25674fbc0bf3": "devops",
    "8d0925bc571d": "business_ideas",
}
