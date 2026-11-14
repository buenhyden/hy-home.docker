"""The one SemVer parser, comparator and version-change rule every consumer reuses."""

from __future__ import annotations

import itertools
import unittest

from scripts.lib.document_governance import semver
from scripts.lib.document_governance.semver import SemVerError, VersionChangeError


class ParseAndPrecedenceTests(unittest.TestCase):
    def test_precedence_orders_numbers_and_prerelease_not_text(self) -> None:
        ordered = (
            ["1.9.0", "1.10.0"],
            ["1.0.0-rc.2", "1.0.0-rc.10", "1.0.0"],
            ["1.0.0-alpha", "1.0.0-alpha.1", "1.0.0-alpha.beta", "1.0.0-beta"],
            ["1.0.0-beta.2", "1.0.0-beta.11", "1.0.0-rc.1", "1.0.0"],
            ["1.0.0-9", "1.0.0-alpha"],
            ["0.9.9", "1.0.0-0", "1.0.0"],
        )
        for chain in ordered:
            for low, high in itertools.pairwise(chain):
                with self.subTest(low=low, high=high):
                    self.assertEqual(-1, semver.compare_semver(low, high))
                    self.assertEqual(1, semver.compare_semver(high, low))

    def test_build_metadata_is_ignored_for_precedence(self) -> None:
        self.assertEqual(0, semver.compare_semver("1.2.3+build.1", "1.2.3+build.2"))
        self.assertEqual(0, semver.compare_semver("1.2.3", "1.2.3+build.2"))
        self.assertEqual(0, semver.compare_semver("1.2.3-rc.1+a", "1.2.3-rc.1+b"))
        self.assertEqual(-1, semver.compare_semver("1.2.3-rc.1+z", "1.2.3-rc.2+a"))

    def test_malformed_and_non_string_versions_are_refused(self) -> None:
        for bad in (
            "v1.2.3",
            "1.2",
            "01.2.3",
            "1.2.3-01",
            "1.2.3-rc..1",
            "-1.2.3",
            "",
            None,
            1.2,
            12,
        ):
            with self.subTest(bad=bad):
                self.assertFalse(semver.is_semver(bad))
                with self.assertRaises(SemVerError):
                    semver.compare_semver(bad, "1.0.0")
                with self.assertRaises(SemVerError):
                    semver.compare_semver("1.0.0", bad)

    def test_artifact_numbers_and_input_labels_are_not_versions(self) -> None:
        # Q-07 numbering, a baseline reset and input-package labels never parse
        # as a version, so a renumbering cannot reorder or reset one.
        for not_version in ("SPEC-0064", "TSK-0001", "v14.7", "0064", "14.7", 14.7):
            with self.subTest(value=not_version):
                self.assertFalse(semver.is_semver(not_version))
                with self.assertRaises(SemVerError):
                    semver.compare_semver(not_version, "1.0.0")
        self.assertEqual(1, semver.compare_semver("1.10.0", "1.9.0"))


class VersionChangeTests(unittest.TestCase):
    def code(self, old: object, new: object) -> str | None:
        return semver.version_change_code(old, new)

    def test_a_raised_precedence_passes(self) -> None:
        for old, new in (
            ("1.9.0", "1.10.0"),
            ("1.0.0-rc.2", "1.0.0-rc.10"),
            ("1.0.0-rc.10", "1.0.0"),
            ("0.1.0", "0.1.1"),
        ):
            with self.subTest(old=old, new=new):
                self.assertIsNone(self.code(old, new))
                semver.check_version_change(old, new)

    def test_unchanged_downgrade_and_missing_are_distinct_codes(self) -> None:
        for old, new, code in (
            ("1.2.3", "1.2.3", "version-unchanged"),
            ("1.2.3+build.1", "1.2.3+build.2", "version-unchanged"),
            ("1.10.0", "1.9.0", "version-downgrade"),
            ("1.0.0", "1.0.0-rc.10", "version-downgrade"),
            ("1.2.3", None, "version-missing"),
            (None, "1.2.3", "version-missing"),
            ("1.2.3", "", "version-missing"),
        ):
            with self.subTest(old=old, new=new):
                self.assertEqual(code, self.code(old, new))
                with self.assertRaises(VersionChangeError) as raised:
                    semver.check_version_change(old, new)
                self.assertEqual(code, raised.exception.code)
                self.assertIsInstance(raised.exception, SemVerError)
                self.assertIn(code.removeprefix("version-"), str(raised.exception))

    def test_a_malformed_value_is_refused_not_classified(self) -> None:
        for old, new in (("v1.2.3", "1.2.4"), ("1.2.3", "1.2"), ("SPEC-0064", "1.0.0")):
            with self.subTest(old=old, new=new), self.assertRaises(SemVerError):
                semver.version_change_code(old, new)

    def test_old_and_new_producer_against_old_and_new_consumer(self) -> None:
        """Old and new producer values, each read as the base and as the head."""

        old_producer, new_producer = "1.2.0", "1.3.0-rc.1+build.7"
        expected = {
            (old_producer, old_producer): "version-unchanged",
            (old_producer, new_producer): None,
            (new_producer, old_producer): "version-downgrade",
            (new_producer, new_producer): "version-unchanged",
        }
        for (base, head), code in expected.items():
            with self.subTest(base=base, head=head):
                self.assertEqual(code, self.code(base, head))


if __name__ == "__main__":
    unittest.main()
