"""Behavior of the repository-docs retrieval evaluation (SPEC-0212 TSK-0119)."""

from __future__ import annotations

import unittest

from scripts.lib.ops import docs_retrieval_eval as ev


def raw(title: str, body: str) -> str:
    return f'---\ntitle: "{title}"\nversion: "1.0.0"\n---\n\n# {title}\n\n{body}\n'


class DocsRetrievalEvalTests(unittest.TestCase):
    def test_embedding_inputs_carry_the_model_task_prompts(self):
        # Ollama sends text as is, so the client adds each model's prompts.
        model = "embeddinggemma-2:740m"
        self.assertEqual(
            ["task: search result | query: valkey"],
            ev.prompted(model, ["valkey"], True),
        )
        self.assertEqual(
            ["title: none | text: cache"], ev.prompted(model, ["cache"], False)
        )
        self.assertEqual(["cache"], ev.prompted("bge-m3", ["cache"], False))

    def test_parse_drops_frontmatter_and_title_heading(self):
        title, body = ev.parse_document(raw("Ollama Runbook", "Restart the model."))
        self.assertEqual("Ollama Runbook", title)
        self.assertNotIn("Ollama Runbook", body)
        self.assertIn("Restart the model.", body)
        self.assertIsNone(ev.parse_document("# no frontmatter\n"))
        self.assertIsNone(ev.parse_document('---\ntitle: ""\n---\nx\n'))

    def test_boilerplate_shared_by_many_documents_is_removed(self):
        bodies = [f"Readers use the payload below.\nunique line {i}" for i in range(10)]
        stripped = ev.strip_boilerplate(bodies, share=0.2)
        self.assertTrue(all("Readers use" not in b for b in stripped))
        self.assertEqual("unique line 3", stripped[3])

    def test_assemble_drops_ambiguous_titles_and_keeps_created(self):
        rows = ev.assemble(
            [
                ("docs/a.md", "2026-01-01T00:00:00+09:00", raw("Same", "alpha")),
                ("docs/b.md", "2026-01-02T00:00:00+09:00", raw("Same", "beta")),
                (
                    "docs/c.md",
                    "2026-01-03T00:00:00+09:00",
                    raw("Valkey Guide", "cache"),
                ),
            ]
        )
        self.assertEqual(["docs/c.md"], [r["path"] for r in rows])
        self.assertEqual("2026-01-03T00:00:00+09:00", rows[0]["created"])
        self.assertEqual({"path", "title", "created", "text"}, set(rows[0]))

    def test_time_split_puts_the_latest_documents_in_test(self):
        docs = [{"path": f"d{i}", "created": f"2026-01-{i + 1:02d}"} for i in range(10)]
        tune, test = ev.time_split(list(reversed(docs)), share=0.8)
        self.assertEqual(8, len(tune))
        self.assertEqual(["d8", "d9"], [d["path"] for d in test])
        self.assertLess(
            max(d["created"] for d in tune), min(d["created"] for d in test)
        )

    def test_bm25_ranks_the_matching_document_first_with_korean_tokens(self):
        corpus = [
            ev.tokenize("valkey cache cluster replication"),
            ev.tokenize("올라마 로컬 모델 추론 경로"),
            ev.tokenize("traefik gateway route middleware"),
        ]
        self.assertEqual(1, ev.BM25(corpus).rank(ev.tokenize("로컬 추론"))[0])
        self.assertEqual([], ev.BM25(corpus).rank(ev.tokenize("absent")))

    def test_rrf_rewards_agreement_between_rankings(self):
        self.assertEqual(2, ev.rrf([[1, 2, 3], [2, 3, 1]], k=60)[0])

    def test_metrics_recall_and_mrr(self):
        m = ev.metrics([(1, [1, 2]), (2, [5, 2]), (3, [4, 5])])
        self.assertAlmostEqual(1 / 3, m["recall_at_1"])
        self.assertAlmostEqual(2 / 3, m["recall_at_5"])
        self.assertAlmostEqual((1 + 0.5) / 3, m["mrr_at_10"])
        self.assertEqual(3.0, m["queries"])

    def test_chunks_are_bounded(self):
        parts = ev.chunks("word " * 2000, size=100, limit=4)
        self.assertEqual(4, len(parts))
        self.assertEqual([""], ev.chunks(""))


if __name__ == "__main__":
    unittest.main()
