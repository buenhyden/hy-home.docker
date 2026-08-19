"""Regression tests for the Spec 137 carry remediation-owner contract.

The requirement these cover was measured wrongly seven times before a check
existed. Each test pins one of the failure modes so the eighth cannot land
silently.
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "scripts" / "validation"))

import carry_owner_contract as contract  # noqa: E402

OWNERSHIP = {("docs", 59): "doc-writer", ("common", 54): "code-reviewer"}
CODEOWNERS_LINES = {4, 16}


def _record(text: str) -> contract.Record:
    return contract.Record(surface="ledger", where="t.md:1", label="claim", text=text)


def _codes(text: str) -> list[str]:
    return [f.code for f in contract.check_record(_record(text), OWNERSHIP, CODEOWNERS_LINES)]


def test_a_record_with_no_owner_fails() -> None:
    assert _codes("Carried because the condition is live.") == ["CARRY-OWNER-MISSING"]


def test_mentioning_an_owner_without_naming_one_fails() -> None:
    """Failure mode 1: counting rows that mention an owner rather than name one."""
    assert _codes("Remediation owner: whichever unit owns the surface.") == [
        "CARRY-OWNER-MISSING"
    ]


def test_a_role_without_a_scope_citation_fails() -> None:
    """Failure modes 2 and 3: a justification asserted, and propagated, uncited."""
    assert _codes("Remediation owner: `doc-writer`.") == ["CARRY-OWNER-UNCITED"]


def test_a_role_contradicting_its_own_citation_fails() -> None:
    """Failure mode 6: presence reported as correctness."""
    codes = _codes("Remediation owner: `code-reviewer`, from `scopes/docs.md:59`.")
    assert "CARRY-OWNER-MISMATCH" in codes


def test_a_citation_that_is_not_an_ownership_row_fails() -> None:
    codes = _codes("Remediation owner: `doc-writer`, from `scopes/docs.md:999`.")
    assert "CARRY-OWNER-CITATION-UNRESOLVED" in codes


def test_a_repository_owner_without_a_codeowners_citation_fails() -> None:
    assert _codes("Remediation owner: `@buenhyden`.") == ["CARRY-OWNER-UNCITED"]


def test_a_codeowners_citation_at_a_comment_line_fails() -> None:
    codes = _codes("Remediation owner: `@buenhyden` under `.github/CODEOWNERS:7`.")
    assert "CARRY-OWNER-CITATION-UNRESOLVED" in codes


def test_a_correctly_cited_role_passes() -> None:
    assert _codes("Remediation owner: `doc-writer`, from `scopes/docs.md:59`.") == []


def test_a_correctly_cited_repository_owner_passes() -> None:
    assert _codes("Remediation owner: `@buenhyden` under `.github/CODEOWNERS:4`.") == []


def test_a_split_surface_may_name_two_owners_when_both_are_cited() -> None:
    """A surface spanning two scope tables is legitimate and must not false-fail."""
    text = (
        "Remediation owner: `doc-writer` from `scopes/docs.md:59`; the other half is "
        "Remediation owner `code-reviewer` from `scopes/common.md:54`."
    )
    assert _codes(text) == []
