"""Companion Evidence v1 binding checks on synthetic fixtures only."""

import copy
import hashlib
import json
import sys
import types
import unittest
from pathlib import Path

WORKLOAD = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKLOAD))
from publisher.evidence import EvidenceError, RunTimes, verify  # noqa: E402

FIXTURES = Path(__file__).parent / "fixtures"
CANDIDATE = (FIXTURES / "companion-candidate-v1.json").read_bytes()
EVIDENCE = json.loads((FIXTURES / "companion-evidence-v1.json").read_bytes())
KEY = ("6eabd835f969", "b" * 32)
VALIDATOR = WORKLOAD.parents[4] / "scripts/validation/check-hermes-candidate.py"


def encode(data):
    return json.dumps(data).encode()


class EvidenceTests(unittest.TestCase):
    def check(self, mutate, code):
        data = copy.deepcopy(EVIDENCE)
        mutate(data)
        with self.assertRaises(EvidenceError) as caught:
            verify(*KEY, CANDIDATE, encode(data))
        self.assertEqual(str(caught.exception), code)

    def test_fixture_pair_derives_latest_direct_fetch_time(self):
        self.assertEqual(
            verify(*KEY, CANDIDATE, encode(EVIDENCE)),
            RunTimes("2026-10-30T09:00:00+09:00", "2026-10-30T09:01:10.250+09:00"),
        )

    def test_candidate_fixture_passes_pinned_validator(self):
        module = types.ModuleType("validator")
        exec(compile(VALIDATOR.read_bytes(), str(VALIDATOR), "exec"), module.__dict__)
        self.assertFalse(module.validate(json.loads(CANDIDATE)))

    def test_rejections(self):
        def item(field, value, index=0):
            return lambda d: d["items"][index].__setitem__(field, value)

        cases = [
            ("identity", lambda d: d.__setitem__("run_id", "c" * 32)),
            ("candidate_digest", lambda d: d.__setitem__("candidate_sha256", "0" * 64)),
            ("schema_version", lambda d: d.__setitem__("schema_version", "v2")),
            ("fields", lambda d: d.__setitem__("extra", 1)),
            ("producer", lambda d: d.__setitem__("producer", {"name": "x"})),
            ("coverage", lambda d: d["items"].pop()),
            ("order", item("index", 1)),
            ("source_url", item("source_url", "https://example.com/other")),
            ("fetched_url", item("fetched_url", "https://user:pw@example.com/x")),
            ("fetched_url", item("fetched_url", "https://")),
            ("fetched_url", item("fetched_url", "https://example.com:99999/x")),
            ("http_status", item("http_status", 304)),
            ("body_digest", item("body_sha256", "A" * 64)),
            ("cache", item("cache", {"hit": True, "key_sha256": None})),
            ("tool_call_id", item("tool_call_id", "")),
            ("tool_call_id", item("tool_call_id", "x" * 129)),
            ("tool_call_id", item("tool_call_id", 7)),
            ("fields", lambda d: d["items"][0].pop("status")),
            ("status", item("status", "partial")),
            ("timestamp", item("fetched_at", "2026-10-30T09:01:10")),
            (
                "fetched_after_generation",
                item("fetched_at", "2026-10-30T09:06:00+09:00"),
            ),
            ("fetched_before_run", item("fetched_at", "2026-10-30T08:59:59+09:00")),
            (
                "scheduled_after_generation",
                lambda d: d.__setitem__("scheduled_at", "2026-10-30T09:06:00+09:00"),
            ),
        ]
        for code, mutate in cases:
            with self.subTest(code=code):
                self.check(mutate, code)

    def test_duplicate_keys_and_garbage_fail_closed(self):
        raw = encode(EVIDENCE)[:-1] + b',"job_id":"6eabd835f969"}'
        for value in (raw, b"\xff", b"NaN", b"[]"):
            with self.subTest(value=value[:8]):
                with self.assertRaises(EvidenceError):
                    verify(*KEY, CANDIDATE, value)

    def test_microsecond_generated_at_is_accepted(self):
        report = json.loads(CANDIDATE)
        report["generated_at"] = "2026-10-30T09:05:00.123456+09:00"
        candidate = json.dumps(report).encode()
        data = copy.deepcopy(EVIDENCE)
        data["candidate_sha256"] = hashlib.sha256(candidate).hexdigest()
        self.assertEqual(
            verify(*KEY, candidate, encode(data)).collected_at,
            "2026-10-30T09:01:10.250+09:00",
        )

    def test_item_without_source_url_blocks_the_run(self):
        report = json.loads(CANDIDATE)
        report["items"][1]["source_url"] = None
        with self.assertRaises(EvidenceError):
            verify(*KEY, json.dumps(report).encode(), encode(EVIDENCE))


if __name__ == "__main__":
    unittest.main()
