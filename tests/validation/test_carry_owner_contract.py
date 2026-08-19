"""Regression tests for the Spec 137 carry remediation-owner contract.

Converted 2026-08-19 from bare pytest-style functions to unittest.TestCase.
The repository runs `python3 -m unittest discover -s tests/validation`, and
this was the only file in that directory declaring no TestCase, so none of
these regressions had ever executed under the repository's own runner.

The requirement these cover was measured wrongly seven times before a check
existed. Each test pins one of the failure modes so the eighth cannot land
silently.
"""

from __future__ import annotations

import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "scripts" / "validation"))

import carry_owner_contract as contract  # noqa: E402

OWNERSHIP = {("docs", 59): "doc-writer", ("common", 54): "code-reviewer"}
CODEOWNERS_LINES = {4, 16}


def _record(text: str) -> contract.Record:
    return contract.Record(surface="ledger", where="t.md:1", label="claim", text=text)


def _codes(text: str) -> list[str]:
    return [f.code for f in contract.check_record(_record(text), OWNERSHIP, CODEOWNERS_LINES)]


class CarryOwnerContractTests(unittest.TestCase):
    def test_a_record_with_no_owner_fails(self) -> None:
        assert _codes("Carried because the condition is live.") == ["CARRY-OWNER-MISSING"]



    def test_mentioning_an_owner_without_naming_one_fails(self) -> None:
        """Failure mode 1: counting rows that mention an owner rather than name one."""
        assert _codes("Remediation owner: whichever unit owns the surface.") == [
            "CARRY-OWNER-MISSING"
        ]



    def test_a_role_without_a_scope_citation_fails(self) -> None:
        """Failure modes 2 and 3: a justification asserted, and propagated, uncited."""
        assert _codes("Remediation owner: `doc-writer`.") == ["CARRY-OWNER-UNCITED"]



    def test_a_role_contradicting_its_own_citation_fails(self) -> None:
        """Failure mode 6: presence reported as correctness."""
        codes = _codes("Remediation owner: `code-reviewer`, from `scopes/docs.md:59`.")
        assert "CARRY-OWNER-MISMATCH" in codes



    def test_a_citation_that_is_not_an_ownership_row_fails(self) -> None:
        codes = _codes("Remediation owner: `doc-writer`, from `scopes/docs.md:999`.")
        assert "CARRY-OWNER-CITATION-UNRESOLVED" in codes



    def test_a_repository_owner_without_a_codeowners_citation_fails(self) -> None:
        assert _codes("Remediation owner: `@buenhyden`.") == ["CARRY-OWNER-UNCITED"]



    def test_a_codeowners_citation_at_a_comment_line_fails(self) -> None:
        codes = _codes("Remediation owner: `@buenhyden` under `.github/CODEOWNERS:7`.")
        assert "CARRY-OWNER-CITATION-UNRESOLVED" in codes



    def test_a_correctly_cited_role_passes(self) -> None:
        assert _codes("Remediation owner: `doc-writer`, from `scopes/docs.md:59`.") == []



    def test_a_correctly_cited_repository_owner_passes(self) -> None:
        assert _codes("Remediation owner: `@buenhyden` under `.github/CODEOWNERS:4`.") == []



    def test_a_split_surface_may_name_two_owners_when_both_are_cited(self) -> None:
        """A surface spanning two scope tables is legitimate and must not false-fail."""
        text = (
            "Remediation owner: `doc-writer` from `scopes/docs.md:59`; the other half is "
            "Remediation owner `code-reviewer` from `scopes/common.md:54`."
        )
        assert _codes(text) == []



    def test_a_destination_paragraph_that_declares_no_ledger_row_fails(self) -> None:
        """The join has to be declared; prose titles do not supply it."""
        codes = _pair_codes(_destination(OWNED_BY_DOCS))
        assert "CARRY-PAIR-UNDECLARED" in codes



    def test_a_ledger_row_with_no_destination_paragraph_fails(self) -> None:
        """Gate 2 reads the destination, so an unserved ledger row is a gap."""
        assert _pair_codes(_ledger("`A`", OWNED_BY_DOCS)) == ["CARRY-PAIR-MISSING"]



    def test_a_destination_declaring_an_unknown_ledger_row_fails(self) -> None:
        codes = _pair_codes(_destination(OWNED_BY_DOCS + " {ledger-anchor: `ghost`}"))
        assert "CARRY-PAIR-ORPHAN" in codes



    def test_paired_surfaces_naming_different_owners_fail(self) -> None:
        """The historical defect: both surfaces passed their own citation check."""
        codes = _pair_codes(
            _ledger("`A`", OWNED_BY_DOCS),
            _destination(OWNED_BY_COMMON + " {ledger-anchor: `A`}"),
        )
        assert "CARRY-OWNER-CROSS-SURFACE" in codes



    def test_paired_surfaces_naming_the_same_owner_pass(self) -> None:
        assert (
            _pair_codes(
                _ledger("`A`", OWNED_BY_DOCS),
                _destination(OWNED_BY_DOCS + " {ledger-anchor: `A`}"),
            )
            == []
        )



    def test_an_anchor_containing_a_period_survives_the_marker(self) -> None:
        """A period-terminated marker would truncate this; the braced form does not."""
        key = "`Definitions / Facts` (v1.2 census)"
        assert (
            _pair_codes(
                _ledger(key, OWNED_BY_DOCS),
                _destination(OWNED_BY_DOCS + " {ledger-anchor: " + key + "}"),
            )
            == []
        )



    def test_one_shared_owner_is_enough_when_a_surface_names_two(self) -> None:
        """A split surface may name two owners; agreement on one is agreement."""
        both = (
            "Remediation owner: `doc-writer` from `scopes/docs.md:59`; the other half "
            "is Remediation owner `code-reviewer` from `scopes/common.md:54`."
        )
        assert (
            _pair_codes(
                _ledger("`A`", both),
                _destination(OWNED_BY_COMMON + " {ledger-anchor: `A`}"),
            )
            == []
        )


# Pairing tests. Added 2026-08-19 after an independent seat found that the

# module could not compare what the two surfaces say about the same claim,

# because nothing in the data joined them. Its `failures=0` was true by

# construction: 21 owner disagreements, 17 of them naming a different owner,

# passed because no comparison existed. Each test below pins one way the join

# can fail.



def _ledger(key: str, text: str) -> contract.Record:
    return contract.Record(surface="ledger", where="L", label=key, text=text, key=key)



def _destination(text: str) -> contract.Record:
    declared = contract.LEDGER_ANCHOR_DECLARATION.search(text)
    return contract.Record(
        surface="destination",
        where="D",
        label="paragraph",
        text=text,
        key=declared.group(1).strip() if declared else "",
    )



def _pair_codes(*records: contract.Record) -> list[str]:
    return [finding.code for finding in contract.check_pairing(list(records))]



OWNED_BY_DOCS = "Remediation owner: `doc-writer` from `scopes/docs.md:59`."

OWNED_BY_COMMON = "Remediation owner: `code-reviewer` from `scopes/common.md:54`."


if __name__ == "__main__":
    unittest.main()
