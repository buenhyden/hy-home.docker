"""Pure redaction for private OpsFlow native failure evidence."""

from __future__ import annotations

import base64
import json
import re
import urllib.parse


def _variants(values: tuple[str, ...]) -> tuple[str, ...]:
    if type(values) is not tuple or any(type(value) is not str for value in values):
        raise TypeError("secret values must be a tuple of text")
    if any(not value for value in values):
        raise ValueError("secret values must not be empty")
    variants = set()
    for value in values:
        raw = value.encode("utf-8")
        variants.update(
            {
                value,
                urllib.parse.quote(value, safe=""),
                urllib.parse.quote_plus(value),
                base64.b64encode(raw).decode("ascii"),
                base64.urlsafe_b64encode(raw).decode("ascii"),
                json.dumps(value)[1:-1],
            }
        )
    return tuple(sorted(variants, key=len, reverse=True))


def redact_text(text: str, secret_values: tuple[str, ...]) -> str:
    """Return text with known fixture secrets and generic credentials removed."""
    if type(text) is not str:
        raise TypeError("failure output must be text")
    for value in _variants(secret_values):
        text = text.replace(value, "[REDACTED]")
    text = re.sub(
        r"(?i)(\b[a-z][a-z0-9+.-]*://[^:/\s]+:)[^@\s]+@",
        r"\1[REDACTED]@",
        text,
    )
    text = re.sub(r"(?i)\b(bearer\s+)[^\s,;]+", r"\1[REDACTED]", text)
    text = re.sub(
        r"""(?i)((?:"|')(?:authorization|password|passwd|token|secret|api[_-]?key)"""
        r"""(?:"|')\s*:\s*(?:"|'))[^"']+((?:"|'))""",
        r"\1[REDACTED]\2",
        text,
    )
    text = re.sub(
        r"(?i)\b(authorization|password|passwd|token|secret|api[_-]?key)"
        r"(\s*[:=]\s*)([^\s,;]+)",
        r"\1\2[REDACTED]",
        text,
    )
    text = re.sub(
        r"\b[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}"
        r"(?:\.[A-Za-z0-9_-]{8,})?\b",
        "[TOKEN]",
        text,
    )
    return re.sub(r"\b[A-Za-z0-9_-]{32,}\b", "[OPAQUE]", text)
