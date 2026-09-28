"""Judge whether a document's prose matches its declared language."""

from __future__ import annotations

import re

LANGUAGES = ("ko", "en")
# ponytail: character-ratio heuristic; it sees script, not meaning. Calibrated
# against the tracked corpus in SPEC-0184 TSK-0001; recalibrate there, never
# with a per-path allowlist.
KO_MIN_RATIO = 0.12
EN_MAX_RATIO = 0.02
MIN_LETTERS = 40

_FRONTMATTER = re.compile(r"\A---\n.*?\n---\n", re.S)
_FENCE = re.compile(r"^(```|~~~)[^\n]*\n.*?^\1[^\n]*$", re.S | re.M)
_COMMENT = re.compile(r"<!--.*?-->", re.S)
_HEADING = re.compile(r"^#{1,6} [^\n]*$", re.M)
_INLINE_CODE = re.compile(r"`[^`\n]*`")
_LINK_TARGET = re.compile(r"\]\([^)]*\)")
_URL = re.compile(r"https?://\S+")
_TOKEN = re.compile(r"\b[A-Za-z0-9_.-]+/[A-Za-z0-9_./-]*|\b[A-Z]{2,}-\d+\b")
_HANGUL = re.compile(r"[가-힣]")
_LATIN = re.compile(r"[A-Za-z]")


def prose(text: str) -> str:
    """Remove structure tokens that keep their form in every language."""

    for pattern in (
        _FRONTMATTER,
        _FENCE,
        _COMMENT,
        _HEADING,
        _INLINE_CODE,
        _LINK_TARGET,
        _URL,
        _TOKEN,
    ):
        text = pattern.sub(" ", text)
    return text


def hangul_ratio(text: str) -> float | None:
    """Return Hangul / (Hangul + Latin) over prose, or None when too short."""

    body = prose(text)
    hangul = len(_HANGUL.findall(body))
    latin = len(_LATIN.findall(body))
    if hangul + latin < MIN_LETTERS:
        return None
    return hangul / (hangul + latin)


def language_mismatch(text: str, declared: str) -> str | None:
    """Return a reason when prose does not read as the declared language."""

    ratio = hangul_ratio(text)
    if ratio is None:
        return None
    if declared == "ko" and ratio < KO_MIN_RATIO:
        return f"declared ko, Hangul ratio {ratio:.2f} < {KO_MIN_RATIO}"
    if declared == "en" and ratio > EN_MAX_RATIO:
        return f"declared en, Hangul ratio {ratio:.2f} > {EN_MAX_RATIO}"
    return None
