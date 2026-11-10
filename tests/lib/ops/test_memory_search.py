"""Bounded lexical memory search without persistent fixture data."""

from __future__ import annotations

import unittest

from scripts.lib.ops.memory_search import search_records


def record(memory_id, body, **changes):
    return {
        "memory_id": memory_id,
        "revision": 2,
        "body": body,
        "source_refs": [{"path": "source.md"}],
        "eligibility": "eligible",
        "provenance": {"reuse_state": "current"},
        **changes,
    }


class SearchTests(unittest.TestCase):
    def test_search_is_casefolded_deterministic_and_returns_snippets(self):
        rows = [
            record("b", "Find SQLite details"),
            record("a", "SQLite journal " + "x" * 500),
        ]
        result = search_records(rows, "sqlite", 10)
        self.assertEqual(["a", "b"], [row["memory_id"] for row in result])
        self.assertNotIn("body", result[0])
        self.assertLessEqual(len(result[0]["snippet"]), 240)
        self.assertEqual(2, result[0]["revision"])
        self.assertEqual([{"path": "source.md"}], result[0]["source_refs"])
        result[0]["source_refs"][0]["path"] = "changed.md"
        self.assertEqual("source.md", rows[1]["source_refs"][0]["path"])

    def test_noncurrent_ineligible_and_nonmatching_rows_are_excluded(self):
        rows = [
            record("a", "needle", eligibility="ineligible"),
            record("b", "needle", provenance={"reuse_state": "needs-review"}),
            record("c", "different"),
        ]
        self.assertEqual([], search_records(rows, "needle", 10))

    def test_unicode_casefold_expansion_keeps_the_matching_snippet(self):
        result = search_records([record("a", "ß" * 300 + "needle")], "needle")
        self.assertIn("needle", result[0]["snippet"])

    def test_limit_and_input_boundaries_are_explicit(self):
        rows = [record(str(i), "needle") for i in range(60)]
        self.assertEqual(10, len(search_records(rows, "needle")))
        self.assertEqual(50, len(search_records(rows, "needle", 50)))
        for query, limit in (
            ("", 10),
            ("  ", 10),
            ("x" * 1025, 10),
            ("needle", 0),
            ("needle", 51),
        ):
            with self.subTest(query=query, limit=limit), self.assertRaises(ValueError):
                search_records(rows, query, limit)


if __name__ == "__main__":
    unittest.main()
