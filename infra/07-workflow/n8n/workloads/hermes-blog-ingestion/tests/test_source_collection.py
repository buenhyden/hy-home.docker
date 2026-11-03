"""Run-bound source receipts and private record boundary tests."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from unittest import mock

WORKLOAD = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKLOAD))

from publisher import private_records, source_collection  # noqa: E402
from publisher.source_fetch import FetchResult  # noqa: E402

JOB = "25674fbc0bf3"
RUN = "0123456789abcdef"
SCHEDULED = "2026-11-01T00:00:00Z"
URL = "https://example.org/original"
FINAL_URL = "https://example.org/final"
SENTENCE = "Example released version 2.1 of its build tool on 31 October."


def fetched(body=None, *, fetched_at="2026-11-01T00:00:01.123Z"):
    body = body or f"<html><body><p>{SENTENCE}</p></body></html>".encode()
    return FetchResult(
        final_url=FINAL_URL,
        status=200,
        sha256=hashlib.sha256(body).hexdigest(),
        fetched_at=fetched_at,
        content_type="text/html; charset=utf-8",
        body=body,
    )


def item(item_id="item-1", *, source_url=FINAL_URL):
    return {
        "item_id": item_id,
        "kind": "devops",
        "title": "Example ships version 2.1",
        "body": SENTENCE,
        "source_url": source_url,
        "source_quotes": [SENTENCE],
    }


class SourceCollectionTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name) / "receipts"

    def collect(self, **overrides):
        values = {
            "root": self.root,
            "job": JOB,
            "run": RUN,
            "scheduled": SCHEDULED,
            "item": "item-1",
            "url": URL,
            "fetcher": mock.Mock(return_value=fetched()),
        }
        values.update(overrides)
        return source_collection.collect(**values), values["fetcher"]

    def test_collect_persists_actual_bytes_before_returning_receipt(self):
        result, fetcher = self.collect()
        self.assertTrue(result["ok"])
        self.assertEqual(result["source_url"], FINAL_URL)
        self.assertEqual(result["normalized_text"], SENTENCE)
        self.assertRegex(result["collection_call_id"], r"^[a-f0-9]{32}$")
        self.assertNotEqual(result["collection_call_id"], result["receipt_id"])
        records = list(self.root.glob("*.json"))
        self.assertEqual(len(records), 1)
        record = json.loads(records[0].read_bytes())
        self.assertEqual(record["body_sha256"], result["body_sha256"])
        self.assertEqual(record["collection_call_id"], result["collection_call_id"])
        self.assertEqual(fetcher.call_args.args, (URL,))

    def test_same_run_and_item_is_idempotent_but_url_replacement_conflicts(self):
        first, first_fetcher = self.collect()
        second_fetcher = mock.Mock(side_effect=AssertionError("must not refetch"))
        second, _ = self.collect(fetcher=second_fetcher)
        self.assertEqual(first, second)
        self.assertEqual(first_fetcher.call_count, 1)
        second_fetcher.assert_not_called()
        with self.assertRaisesRegex(ValueError, "source_conflict"):
            self.collect(url="https://example.org/replacement")

    def test_other_execution_cannot_reuse_receipt(self):
        receipt, _ = self.collect()
        with self.assertRaisesRegex(ValueError, "source_missing"):
            source_collection.resolve(
                self.root,
                JOB,
                "another-execution",
                SCHEDULED,
                [item()],
                [receipt["receipt_id"]],
            )

    def test_ordered_receipts_are_bound_to_matching_items(self):
        first, _ = self.collect(item="item-1")
        second, _ = self.collect(item="item-2", url="https://example.org/second")
        with self.assertRaisesRegex(ValueError, "source_mismatch"):
            source_collection.resolve(
                self.root,
                JOB,
                RUN,
                SCHEDULED,
                [item("item-1"), item("item-2")],
                [second["receipt_id"], first["receipt_id"]],
            )

    def test_complete_item_receipt_pairs_may_be_reordered_together(self):
        first, _ = self.collect(item="item-1")
        second, _ = self.collect(item="item-2", url="https://example.org/second")
        rows = source_collection.resolve(
            self.root,
            JOB,
            RUN,
            SCHEDULED,
            [item("item-2"), item("item-1")],
            [second["receipt_id"], first["receipt_id"]],
        )
        self.assertEqual([row["item_id"] for row in rows], ["item-2", "item-1"])

    def test_tampered_source_bytes_are_rejected(self):
        receipt, _ = self.collect()
        path = next(self.root.glob("*.json"))
        record = json.loads(path.read_bytes())
        record["body_b64"] = "dGFtcGVyZWQ="
        path.write_text(json.dumps(record), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "invalid_record"):
            source_collection.resolve(
                self.root, JOB, RUN, SCHEDULED, [item()], [receipt["receipt_id"]]
            )

    def test_receipt_is_not_returned_when_atomic_write_fails(self):
        with mock.patch.object(
            private_records.PrivateRecords,
            "write",
            side_effect=private_records.RecordError("write_failed"),
        ):
            with self.assertRaisesRegex(private_records.RecordError, "write_failed"):
                self.collect()
        self.assertEqual(list(self.root.glob("*.json")), [])

    def test_fetch_before_scheduled_instant_is_rejected(self):
        early = fetched(fetched_at="2026-10-31T23:59:59Z")
        with self.assertRaisesRegex(ValueError, "invalid_record"):
            self.collect(fetcher=mock.Mock(return_value=early))

    def test_run_rejects_the_101st_item_before_fetch(self):
        shared_fetcher = mock.Mock(return_value=fetched())
        for index in range(source_collection.MAX_RUN_ITEMS):
            self.collect(
                item=f"item-{index}",
                url=f"https://example.org/{index}",
                fetcher=shared_fetcher,
            )
        denied = mock.Mock(side_effect=AssertionError("must not fetch item 101"))
        with self.assertRaisesRegex(ValueError, "source_item_limit"):
            self.collect(item="item-101", url="https://example.org/101", fetcher=denied)
        denied.assert_not_called()

    def test_failed_fetch_budget_is_persisted_before_network(self):
        fetcher = mock.Mock(side_effect=RuntimeError("synthetic fetch failure"))
        for _ in range(source_collection.MAX_ITEM_FETCH_ATTEMPTS):
            with self.assertRaisesRegex(RuntimeError, "synthetic fetch failure"):
                self.collect(fetcher=fetcher)
        with self.assertRaisesRegex(ValueError, "source_attempt_limit"):
            self.collect(fetcher=fetcher)
        self.assertEqual(fetcher.call_count, source_collection.MAX_ITEM_FETCH_ATTEMPTS)

    def test_concurrent_same_item_fetches_once_and_returns_one_receipt(self):
        entered = threading.Event()
        release = threading.Event()
        results = []
        errors = []

        def fetcher(_url):
            entered.set()
            self.assertTrue(release.wait(timeout=2))
            return fetched()

        def invoke():
            try:
                results.append(self.collect(fetcher=fetcher)[0])
            except BaseException as error:
                errors.append(error)

        first = threading.Thread(target=invoke)
        second = threading.Thread(target=invoke)
        first.start()
        self.assertTrue(entered.wait(timeout=2))
        second.start()
        release.set()
        first.join(timeout=5)
        second.join(timeout=5)
        self.assertEqual(errors, [])
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["receipt_id"], results[1]["receipt_id"])


class PrivateRecordsTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name) / "private"
        self.store = private_records.PrivateRecords(self.root)
        self.addCleanup(self.store.close)

    def test_written_records_are_private_single_link_files(self):
        self.store.write("state.json", b"payload")
        info = (self.root / "state.json").stat()
        self.assertEqual(stat.S_IMODE(info.st_mode), 0o600)
        self.assertEqual(info.st_nlink, 1)
        self.assertEqual(self.store.read("state.json"), b"payload")

    def test_symlink_hardlink_fifo_and_unsafe_mode_are_rejected(self):
        outside = self.root.parent / "outside"
        outside.write_bytes(b"outside")
        os.chmod(outside, 0o600)
        (self.root / "link.json").symlink_to(outside)
        with self.assertRaises((OSError, private_records.RecordError)):
            self.store.read("link.json")
        os.link(outside, self.root / "hard.json")
        with self.assertRaisesRegex(private_records.RecordError, "unsafe_record"):
            self.store.read("hard.json")
        os.mkfifo(self.root / "fifo.json", 0o600)
        with self.assertRaisesRegex(private_records.RecordError, "unsafe_record"):
            self.store.read("fifo.json")
        unsafe = self.root / "unsafe.json"
        unsafe.write_bytes(b"unsafe")
        unsafe.chmod(0o644)
        with self.assertRaisesRegex(private_records.RecordError, "unsafe_record"):
            self.store.read("unsafe.json")

    def test_oversized_record_is_rejected_without_content_in_error(self):
        path = self.root / "large.json"
        path.write_bytes(b"synthetic-secret" * 32)
        path.chmod(0o600)
        with self.assertRaisesRegex(
            private_records.RecordError, "record_too_large"
        ) as caught:
            self.store.read("large.json", limit=16)
        self.assertNotIn("synthetic-secret", str(caught.exception))

    def test_failed_replace_preserves_previous_record(self):
        self.store.write("state.json", b"old")
        with mock.patch.object(
            private_records.os, "replace", side_effect=OSError("synthetic failure")
        ):
            with self.assertRaises(OSError):
                self.store.write("state.json", b"new")
        self.assertEqual(self.store.read("state.json"), b"old")
        self.assertEqual(list(self.root.glob(".tmp-*")), [])

    def test_lock_path_rebinding_is_rejected_before_critical_section(self):
        key = "report-1"
        lock_name = ".lock-" + hashlib.sha256(key.encode()).hexdigest()
        opened = threading.Event()
        entered = []
        failures = []
        original_open = private_records.os.open

        def observed_open(path, *args, **kwargs):
            descriptor = original_open(path, *args, **kwargs)
            if path == lock_name and threading.current_thread().name == "contender":
                opened.set()
            return descriptor

        def contend():
            other = private_records.PrivateRecords(self.root)
            try:
                with other.lock(key):
                    entered.append(True)
            except BaseException as error:
                failures.append(error)
            finally:
                other.close()

        with self.store.lock(key):
            with mock.patch.object(
                private_records.os, "open", side_effect=observed_open
            ):
                thread = threading.Thread(target=contend, name="contender")
                thread.start()
                self.assertTrue(opened.wait(timeout=2))
                (self.root / lock_name).unlink()
                descriptor = original_open(
                    self.root / lock_name,
                    os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                    0o600,
                )
                os.close(descriptor)
        thread.join(timeout=5)
        self.assertEqual(entered, [])
        self.assertEqual(len(failures), 1)
        self.assertIsInstance(failures[0], private_records.RecordError)


if __name__ == "__main__":
    unittest.main()
