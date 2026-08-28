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
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "scripts" / "validation"))

import carry_owner_contract as contract  # noqa: E402

OWNERSHIP = {
    ("docs", 59): "doc-writer",
    ("common", 54): "code-reviewer",
    ("security", 69): "security-auditor",
}
CODEOWNERS_LINES = {4, 16}


class EvidenceTimeBoundaryTests(unittest.TestCase):
    def test_complete_scope_citation_resolves_exact_historical_git_path(self) -> None:
        root = pathlib.Path(__file__).resolve().parents[2]
        with mock.patch.object(contract, "HistoricalDocument", wraps=contract.HistoricalDocument) as historical:
            ownership = contract.load_ownership_table(root, {"`scopes/docs.md:59`", "`scopes/docs.md:62`"})
        historical.assert_called_once_with(
            root, contract.OWNERSHIP_AS_OF, "docs/00.agent-governance/scopes/docs.md"
        )
        self.assertEqual("doc-writer", ownership[("docs", 59)])
        for citation in (
            "docs", "`scopes/../docs.md:59`", "`/scopes/docs.md:59`",
            "`scopes/docs.md:59/extra`", "`scopes/docs.md:not-a-line`",
            "`scopes/docs.md:59` trailing", "`roles/docs.md:59`",
        ):
            with self.subTest(citation=citation), mock.patch.object(contract, "HistoricalDocument") as historical:
                with self.assertRaises(ValueError):
                    contract.load_ownership_table(root, {citation})
                historical.assert_not_called()

    def test_historical_scope_uses_the_regular_ownership_baseline(self) -> None:
        root = pathlib.Path(__file__).resolve().parents[2]
        ownership = contract.load_ownership_table(root, {"`scopes/docs.md:59`"})
        self.assertEqual("doc-writer", ownership[("docs", 59)])
        with mock.patch.object(contract, "OWNERSHIP_AS_OF", "9917fcdadf700e7f68541e73188620e133485470"):
            wrong = contract.load_ownership_table(root, {"`scopes/docs.md:59`"})
        codes = [item.code for item in contract.check_record(_record(OWNED_BY_DOCS), wrong, CODEOWNERS_LINES)]
        self.assertIn("CARRY-OWNER-CITATION-UNRESOLVED", codes)

    def test_historical_scope_rejects_missing_and_nonregular_git_proof(self) -> None:
        root = pathlib.Path(__file__).resolve().parents[2]
        with mock.patch.object(contract, "OWNERSHIP_AS_OF", "0" * 40):
            with self.assertRaises(ValueError):
                contract.load_ownership_table(root, {"`scopes/docs.md:59`"})
        with self.assertRaises(ValueError):
            contract.load_ownership_table(root, {"`scopes/missing.md:1`"})
        with tempfile.TemporaryDirectory() as directory:
            fixture = pathlib.Path(directory)
            scope = fixture / "docs/00.agent-governance/scopes/docs.md"
            scope.parent.mkdir(parents=True)
            scope.symlink_to("missing.md")
            for command in (("init", "-q"), ("add", "."), ("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "scope")):
                subprocess.run(["git", *command], cwd=fixture, check=True, capture_output=True)
            commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=fixture, text=True).strip()
            with mock.patch.object(contract, "OWNERSHIP_AS_OF", commit):
                with self.assertRaises(ValueError):
                    contract.load_ownership_table(fixture, {"`scopes/docs.md:59`"})

    def test_current_role_requires_its_active_canonical_identity(self) -> None:
        root = pathlib.Path(__file__).resolve().parents[2]
        cite = "`docs/00.agent-governance/roles/doc-writer.md`"
        record = _destination(OWNED_BY_DOCS + " Current role accountability: " + cite)
        self.assertEqual([], contract.check_current_role(record, root))
        for text in (
            OWNED_BY_DOCS,
            OWNED_BY_DOCS + " `docs/00.agent-governance/roles/missing.md`",
            OWNED_BY_DOCS + " `docs/00.agent-governance/roles/code-reviewer.md`",
            OWNED_BY_DOCS + " `docs/00.agent-governance/roles/doc-writer.md:4`",
        ):
            with self.subTest(text=text):
                self.assertTrue(contract.check_current_role(_destination(text), root))
        with tempfile.TemporaryDirectory() as directory:
            fixture = pathlib.Path(directory)
            role = fixture / "docs/00.agent-governance/roles/doc-writer.md"
            role.parent.mkdir(parents=True)
            for metadata in (
                "profile_id: governance-role\nagent_id: doc-writer\nstatus: retired",
                "profile_id: governance-role\nagent_id: other\nstatus: active",
                "profile_id: governance-policy\nagent_id: doc-writer\nstatus: active",
                "profile_id: governance-role\nagent_id: doc-writer\nagent_id: other\nstatus: active",
            ):
                with self.subTest(metadata=metadata):
                    role.write_text("---\n" + metadata + "\n---\n", encoding="utf-8")
                    self.assertTrue(contract.check_current_role(record, fixture))

    def test_readonly_identity_proof_does_not_grant_implementation_permission(self) -> None:
        root = pathlib.Path(__file__).resolve().parents[2]
        task = "docs/03.specs/0137-agentic-research-pack-rebuild/tasks/tsk-0001-rebuild.md"
        for owner in ("code-reviewer", "security-auditor"):
            relative = f"docs/00.agent-governance/roles/{owner}.md"
            before = (root / relative).read_bytes()
            record = _destination(f"Remediation owner: `{owner}`. Current role accountability: `{relative}`.")
            self.assertEqual([], contract.check_current_role(record, root))
            self.assertEqual(before, (root / relative).read_bytes())
            self.assertIn(b"permission_profile: read-only", before)
        for record in contract.collect_destination_records(root, task):
            if not record.historical and record.operative_owner() in {"code-reviewer", "security-auditor"}:
                self.assertIn("not a write grant", record.text)
                self.assertIn("separately approved implementation assignee", record.text)

    def test_only_exact_marked_historical_quotes_preserve_pairing(self) -> None:
        marker = "> Historical evidence (not current authority; source: Git history):"
        body = "**Claim.** " + OWNED_BY_DOCS + " {ledger-anchor: `A`} {survival: UNIQUE}"
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            task = root / "task.md"
            task.write_text(contract.DESTINATION_HEADING + "\n\n" + marker + "\n> " + body + "\n\n**Current.** " + OWNED_BY_DOCS + "\n", encoding="utf-8")
            records = contract.collect_destination_records(root, "task.md")
            self.assertEqual([True, False], [record.historical for record in records])
            self.assertEqual([], _pair_codes(_ledger("`A`", OWNED_BY_DOCS), records[0]))
            self.assertTrue(contract.check_current_role(records[1], root))
            for prefix in ("", marker + ".\n", marker + "\n\n", marker.replace("not current authority", "historical") + "\n"):
                with self.subTest(prefix=prefix):
                    task.write_text(contract.DESTINATION_HEADING + "\n\n" + prefix + "> " + body + "\n", encoding="utf-8")
                    self.assertEqual([], contract.collect_destination_records(root, "task.md"))
                    self.assertEqual(["CARRY-PAIR-MISSING"], _pair_codes(_ledger("`A`", OWNED_BY_DOCS)))


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
                _destination(OWNED_BY_DOCS + " {ledger-anchor: `A`} {survival: UNIQUE}"),
            )
            == []
        )



    def test_an_anchor_containing_a_period_survives_the_marker(self) -> None:
        """A period-terminated marker would truncate this; the braced form does not."""
        key = "`Definitions / Facts` (v1.2 census)"
        assert (
            _pair_codes(
                _ledger(key, OWNED_BY_DOCS),
                _destination(OWNED_BY_DOCS + " {ledger-anchor: " + key + "} {survival: UNIQUE}"),
            )
            == []
        )



    def test_a_destination_stating_no_survival_verdict_fails(self) -> None:
        """Gate 2 reads the destination, so the survival verdict belongs there."""
        codes = _pair_codes(
            _ledger_s("`A`", OWNED_BY_DOCS + " survival predicate: PARTIAL", "PARTIAL"),
            _destination(OWNED_BY_DOCS + " {ledger-anchor: `A`}"),
        )
        assert "CARRY-SURVIVAL-UNSTATED" in codes

    def test_a_destination_verdict_contradicting_the_ledger_fails(self) -> None:
        """Two surfaces stated contradictory verdicts on 35 of 47 claims."""
        codes = _pair_codes(
            _ledger_s("`A`", OWNED_BY_DOCS + " survival predicate: PARTIAL", "PARTIAL"),
            _destination(OWNED_BY_DOCS + " {ledger-anchor: `A`} {survival: UNIQUE}"),
        )
        assert "CARRY-SURVIVAL-MISMATCH" in codes

    def test_the_voided_intra_document_test_fails_when_it_is_the_basis(self) -> None:
        """The amendment voids it: intra-document duplication does not bear on the gate."""
        codes = _pair_codes(
            _ledger_s("`A`", OWNED_BY_DOCS + " survival predicate: UNIQUE", "UNIQUE"),
            _destination(
                OWNED_BY_DOCS
                + " UNIQUE - no other paragraph in this section carries this claim."
                + " {ledger-anchor: `A`}"
            ),
        )
        assert "CARRY-SURVIVAL-VOIDED-TEST" in codes

    def test_a_retained_intra_document_sentence_passes_beside_a_survival_verdict(
        self,
    ) -> None:
        """Once the verdict is stated, the old sentence is provenance, not the basis."""
        assert (
            _pair_codes(
                _ledger_s("`A`", OWNED_BY_DOCS + " survival predicate: UNIQUE", "UNIQUE"),
                _destination(
                    OWNED_BY_DOCS
                    + " UNIQUE - no other ledger row carries it."
                    + " {ledger-anchor: `A`} {survival: UNIQUE}"
                ),
            )
            == []
        )

    def test_a_disagreeing_owner_appended_last_fails(self) -> None:
        """The accumulation defect: set intersection went blind here.

        These cells append corrections rather than editing, so a synchronised
        cell names two owners. Under an intersection test a third, disagreeing
        owner appended afterwards produced no finding at all. The operative owner
        is the last one stated.
        """
        accumulated = (
            OWNED_BY_DOCS
            + " Owner re-resolved; the earlier statement is withdrawn. "
            + OWNED_BY_COMMON
            + " Remediation owner `security-auditor` from `scopes/security.md:69`."
        )
        codes = _pair_codes(
            _ledger("`A`", accumulated),
            _destination(OWNED_BY_COMMON + " {ledger-anchor: `A`}"),
        )
        assert "CARRY-OWNER-CROSS-SURFACE" in codes

    def test_a_withdrawn_owner_before_the_operative_one_passes(self) -> None:
        """The corpus convention: a later statement supersedes an earlier one."""
        corrected = (
            "Remediation owner: `security-auditor` from `scopes/security.md:69`. "
            "Owner re-resolved; the earlier statement is withdrawn. " + OWNED_BY_COMMON
        )
        assert (
            _pair_codes(
                _ledger("`A`", corrected),
                _destination(OWNED_BY_COMMON + " {ledger-anchor: `A`} {survival: UNIQUE}"),
            )
            == []
        )

    def test_a_surface_naming_two_owners_is_judged_on_its_operative_one(self) -> None:
        """A split surface may name two owners; only the last one is operative.

        Renamed and re-premised 2026-08-20. It previously read "agreement on one
        is agreement", which was the defect an independent seat found: the check
        compared one surface's operative owner against the OTHER surface's whole
        set, so a cell that ever named the right owner satisfied the test forever,
        even in a withdrawn statement. Here the operative owners agree, so the
        pair passes for the reason the contract intends.
        """
        both = (
            "Remediation owner: `doc-writer` from `scopes/docs.md:59`; the other half "
            "is Remediation owner `code-reviewer` from `scopes/common.md:54`."
        )
        assert (
            _pair_codes(
                _ledger("`A`", both),
                _destination(OWNED_BY_COMMON + " {ledger-anchor: `A`} {survival: UNIQUE}"),
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
    return contract.Record(surface="ledger", where="L", label=key, text=text, keys=(key,))


def _ledger_s(key: str, text: str, survival: str) -> contract.Record:
    return contract.Record(
        surface="ledger", where="L", label=key, text=text, keys=(key,), survival=survival
    )



def _destination(text: str) -> contract.Record:
    declared = tuple(
        match.strip() for match in contract.LEDGER_ANCHOR_DECLARATION.findall(text)
    )
    return contract.Record(
        surface="destination",
        where="D",
        label="paragraph",
        text=text,
        keys=declared,
        survival=(
            match.group(1)
            if (match := contract.DESTINATION_SURVIVAL.search(text))
            else ""
        ),
    )



def _pair_codes(*records: contract.Record) -> list[str]:
    return [finding.code for finding in contract.check_pairing(list(records))]



OWNED_BY_DOCS = "Remediation owner: `doc-writer` from `scopes/docs.md:59`."

OWNED_BY_COMMON = "Remediation owner: `code-reviewer` from `scopes/common.md:54`."


class OperativeOwnerComparisonTests(unittest.TestCase):
    """Pins the two defects an independent seat found on 2026-08-20.

    Both made `failures=0` true by construction for a fourth time, so both are
    pinned rather than merely fixed.
    """

    def test_operative_owners_are_compared_against_each_other(self) -> None:
        """A withdrawn owner on one surface must not satisfy the other's operative.

        The ledger withdraws `code-reviewer` for `@buenhyden`; the destination
        withdraws `@buenhyden` for `code-reviewer`. Every owner each surface names
        appears on the other, so a set-membership test finds no disagreement. The
        operative owners are opposite and it is a disagreement.
        """

        ledger = (
            "Remediation owner: `code-reviewer` from `scopes/common.md:54`. "
            "Withdrawn; Owner is `@buenhyden` under `.github/CODEOWNERS:16`."
        )
        destination = (
            "Remediation owner: `@buenhyden` under `.github/CODEOWNERS:16`. "
            "Withdrawn; Owner is `code-reviewer` from `scopes/common.md:54`. "
            "{ledger-anchor: `A`} {survival: UNIQUE}"
        )
        assert "CARRY-OWNER-CROSS-SURFACE" in _pair_codes(
            _ledger("`A`", ledger), _destination(destination)
        )

    def test_a_superseding_owner_not_phrased_as_remediation_owner_is_read(
        self,
    ) -> None:
        """`Owner is X` supersedes an earlier `Remediation owner: Y`.

        The owner pattern matched only the phrase "Remediation owner", so every
        correction written as "Owner is `X` under the ... rule" was invisible and
        `operative_owner()` returned the withdrawn owner instead.
        """

        ledger = (
            "Remediation owner: `code-reviewer` from `scopes/common.md:54`. "
            "Owner is `@buenhyden` under the `scripts/**` rule at "
            "`.github/CODEOWNERS:16`."
        )
        assert "CARRY-OWNER-CROSS-SURFACE" in _pair_codes(
            _ledger("`A`", ledger),
            _destination(OWNED_BY_COMMON + " {ledger-anchor: `A`} {survival: UNIQUE}"),
        )


if __name__ == "__main__":
    unittest.main()
