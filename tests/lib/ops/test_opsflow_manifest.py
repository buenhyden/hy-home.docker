"""Synthetic independent manifest parser and object-before-database regressions."""

import dataclasses
import hashlib
import importlib
import json
import sys
import traceback
import unittest
from pathlib import Path
from unittest.mock import patch

WORKLOAD = (
    Path(__file__).resolve().parents[3]
    / "infra/07-workflow/airflow/workloads/manifest-pipeline"
)
sys.path.insert(0, str(WORKLOAD))
module = importlib.import_module("workflow_lib.manifest")
ContractError = module.ContractError
ingest = module.ingest
object_key = module.object_key
parse_manifest = module.parse_manifest
run_id = module.run_id


def body(**changes):
    value = {
        "schema_version": 1,
        "source": "hy-home.docker",
        "repository": "buenhyden/hy-home.docker",
        "ref": "main",
        "captured_at": "2026-10-10T00:00:00Z",
        "records": [
            {
                "path": "docs/README.md",
                "revision": "a" * 40,
                "content_sha256": "b" * 64,
                "title": "운영 문서",
            }
        ],
    }
    return json.dumps(dict(value, **changes), ensure_ascii=False).encode()


class SyntheticStore:
    def __init__(self, raw, events):
        self.raw, self.events, self.objects, self.fail = raw, events, {}, None

    def read_input(self, key):
        self.events.append(("read", key))
        if self.fail == "read":
            raise OSError("synthetic-private-payload")
        return self.raw

    def put_verified(self, key, raw):
        self.events.append(("object", key))
        if self.fail == "put":
            raise OSError("synthetic-private-payload")
        self.objects.setdefault(key, raw)
        actual = (
            self.objects.get("wrong", b"")
            if self.fail == "wrong-key"
            else self.objects[key]
        )
        if actual != raw:
            raise ContractError("storage_readback")
        self.events.append(("verified", key))


class SyntheticPublisher:
    def __init__(self, events):
        self.events, self.ledger, self.status = events, {}, "published"

    def publish(self, manifest, identifier, digest, artifact):
        self.events.append(("publish", identifier))
        if self.status == "raise":
            raise OSError("synthetic-private-payload")
        if identifier in self.ledger:
            return "replayed"
        self.ledger[identifier] = (manifest, digest, artifact)
        return self.status


class ManifestTests(unittest.TestCase):
    def test_invalid_input_rejected(self):
        with self.assertRaises(ValueError):
            parse_manifest(b"not-json")

    def test_four_pairs_and_immutability(self):
        for source, (repository, ref) in module.SOURCES.items():
            parsed = parse_manifest(body(source=source, repository=repository, ref=ref))
            self.assertEqual(parsed.source, source)
            with self.assertRaises(TypeError):
                parsed.records[0]["title"] = "changed"
            with self.assertRaises(dataclasses.FrozenInstanceError):
                parsed.source = "changed"
        with self.assertRaises(TypeError):
            module.SOURCES["extra"] = ("other", "main")

    def test_sorting_preserves_input(self):
        row = json.loads(body())["records"][0]
        raw = body(records=[dict(row, path="z.md"), dict(row, path="a.md")])
        original = bytes(raw)
        self.assertEqual(
            [r["path"] for r in parse_manifest(raw).records], ["a.md", "z.md"]
        )
        self.assertEqual(raw, original)

    def test_closed_fields_and_types(self):
        for changes in (
            {"schema_version": 2},
            {"schema_version": True},
            {"schema_version": 1.0},
            {"source": []},
            {"source": "unknown"},
            {"repository": "other"},
            {"ref": "dev"},
            {"extra": "synthetic-private-payload"},
            {"records": []},
            {"records": {}},
            {"records": [None]},
            {"records": [{"path": "x"}]},
        ):
            with self.subTest(changes=changes), self.assertRaises(ContractError):
                parse_manifest(body(**changes))
        for raw in (b"[]", b"null", b"1", b'"x"'):
            with self.assertRaises(ContractError):
                parse_manifest(raw)

    def test_paths(self):
        row = json.loads(body())["records"][0]
        for path in (
            "",
            "/x",
            "../x",
            "docs//x",
            "docs/./x",
            "docs/../x",
            "docs\\x",
            ".env",
            "x/.git/config",
            "SECRETS/x",
            "x/SeCrEtS/y",
            "x/\x00",
            "x/\x1f",
            "x/\x7f",
            "x" * 513,
        ):
            with self.subTest(path=path), self.assertRaises(ContractError):
                parse_manifest(body(records=[dict(row, path=path)]))
        parsed = parse_manifest(body(records=[dict(row, path="docs/한국어.md")]))
        self.assertEqual(parsed.records[0]["path"], "docs/한국어.md")

    def test_sensitive_segments_case_insensitive(self):
        row = json.loads(body())["records"][0]
        for segment in (
            "SECRET",
            "PASSWORDS",
            "credentials",
            "tokens",
            "Password",
            "Secrets",
        ):
            with (
                self.subTest(segment=segment),
                self.assertRaisesRegex(ContractError, "record_path"),
            ):
                parse_manifest(body(records=[dict(row, path=f"docs/{segment}/x.md")]))

    def test_unicode_control_characters_in_path_and_title(self):
        row = json.loads(body())["records"][0]
        for control in ("\u0080", "\u0085", "\u009f"):
            for field in ("path", "title"):
                with (
                    self.subTest(control=ord(control), field=field),
                    self.assertRaises(ContractError),
                ):
                    parse_manifest(
                        body(records=[dict(row, **{field: f"docs/{control}x"})])
                    )

    def test_row_hash_title_and_duplicates(self):
        row = json.loads(body())["records"][0]
        for changes in (
            {"title": ""},
            {"title": "x" * 257},
            {"title": "x\x7f"},
            {"title": "x\n"},
            {"title": 1},
            {"path": None},
            {"revision": "A" * 40},
            {"revision": "a" * 39},
            {"content_sha256": "b" * 63},
            {"content_sha256": "G" * 64},
            {"extra": "x"},
        ):
            with self.assertRaises(ContractError):
                parse_manifest(body(records=[dict(row, **changes)]))
        for rows in ([row, row], [row] * (module.MAX_RECORDS + 1)):
            with self.assertRaises(ContractError):
                parse_manifest(body(records=rows))

    def test_utc_timestamp_and_invalid_dates(self):
        parsed = parse_manifest(body(captured_at="2026-10-10T09:30:01+09:00"))
        self.assertEqual(parsed.captured_at.isoformat(), "2026-10-10T00:30:01+00:00")
        for captured in (
            None,
            10,
            "",
            "2026-10-10",
            "2026-10-10T00:00:00",
            "2026-10-10 00:00:00Z",
            "20261010T000000Z",
            "2026-02-30T00:00:00Z",
            "2026-10-10T00:00:00+00:00:01",
        ):
            with self.assertRaises(ContractError):
                parse_manifest(body(captured_at=captured))

    def test_json_bounds_duplicates_nonfinite_depth(self):
        for raw in (
            None,
            "{}",
            bytearray(b"{}"),
            b"",
            b"\xff",
            b"x" * (module.MAX_BYTES + 1),
            b'{"x":1,"x":2}',
            b'{"x":NaN}',
            b'{"x":Infinity}',
            b'{"x":-Infinity}',
            b'{"x":1e999}',
            b"[" * 40 + b"0" + b"]" * 40,
            b'{"x":"unfinished}',
        ):
            with self.assertRaises(ContractError):
                parse_manifest(raw)
        row = json.loads(body())["records"][0]
        parse_manifest(body(records=[dict(row, title='[{}]\\"')]))
        with patch.object(module.json, "loads", side_effect=RecursionError):
            with self.assertRaises(ContractError):
                parse_manifest(body())

    def test_maximum_allowed_boundaries(self):
        raw = body() + b" " * (module.MAX_BYTES - len(body()))
        self.assertEqual(len(raw), module.MAX_BYTES)
        parse_manifest(raw)
        row = json.loads(body())["records"][0]
        parsed = parse_manifest(
            body(
                records=[
                    dict(row, path=f"docs/{n}.md") for n in range(module.MAX_RECORDS)
                ]
            )
        )
        self.assertEqual(len(parsed.records), module.MAX_RECORDS)

    def test_key_identity_and_bad_arguments(self):
        self.assertEqual(
            object_key("hy-home.docker", "2026-10-10"),
            "manifest-input/hy-home.docker/2026-10-10.json",
        )
        for source, day in (
            ([], "2026-10-10"),
            ("unknown", "x"),
            ("hy-home.docker", None),
            ("hy-home.docker", "20261010"),
            ("hy-home.docker", "2026-02-30"),
        ):
            with self.assertRaises(ContractError):
                object_key(source, day)
        raw = body()
        expected = hashlib.sha256(
            f"hy-home.docker:{hashlib.sha256(raw).hexdigest()}".encode()
        ).hexdigest()
        self.assertEqual(run_id("hy-home.docker", raw), expected)
        self.assertNotEqual(
            run_id("hy-home.docker", raw), run_id("hy-home.docker", raw + b" ")
        )
        self.assertNotEqual(run_id("hy-home.docker", raw), run_id("hy-home.k8s", raw))
        for source, raw in (
            ("unknown", body()),
            ([], body()),
            ("hy-home.docker", "{}"),
        ):
            with self.assertRaises(ContractError):
                run_id(source, raw)

    def test_verified_object_before_db_replay_and_result(self):
        events = []
        store, db = SyntheticStore(body(), events), SyntheticPublisher(events)
        result = ingest(store, db, "hy-home.docker", "2026-10-10")
        self.assertEqual(set(result), {"run_id", "status", "records"})
        self.assertEqual(result["records"], 1)
        self.assertEqual(result["status"], "published")
        self.assertEqual(
            [e[0] for e in events], ["read", "object", "verified", "publish"]
        )
        _, digest, artifact = db.ledger[result["run_id"]]
        self.assertEqual(digest, hashlib.sha256(body()).hexdigest())
        self.assertEqual(
            artifact, f"manifest-validated/hy-home.docker/{result['run_id']}.json"
        )
        self.assertEqual(
            ingest(store, db, "hy-home.docker", "2026-10-10")["status"], "replayed"
        )
        self.assertEqual(len(db.ledger), 1)
        self.assertEqual(len(store.objects), 1)
        db = SyntheticPublisher([])
        db.status = "historical"
        self.assertEqual(
            ingest(store, db, "hy-home.docker", "2026-10-10")["status"], "historical"
        )

    def test_invalid_input_storage_failures_do_not_publish(self):
        cases = (
            (b"invalid", "2026-10-10", None),
            (
                body(source="hy-home.k8s", repository="buenhyden/hy-home.k8s"),
                "2026-10-10",
                None,
            ),
            (body(), "2026-10-11", None),
            (body(), "2026-10-10", "read"),
            (body(), "2026-10-10", "put"),
            (body(), "2026-10-10", "wrong-key"),
        )
        for raw, day, failure in cases:
            events = []
            store, db = SyntheticStore(raw, events), SyntheticPublisher(events)
            store.fail = failure
            with self.assertRaises(ContractError) as error:
                ingest(store, db, "hy-home.docker", day)
            self.assertFalse(db.ledger)
            self.assertNotIn("publish", [e[0] for e in events])
            self.assertNotIn(
                "synthetic-private-payload",
                "".join(traceback.format_exception(error.exception)),
            )

    def test_failed_db_keeps_verified_artifact_and_invalid_status_rejected(self):
        store, db = SyntheticStore(body(), []), SyntheticPublisher([])
        db.status = "raise"
        with self.assertRaisesRegex(ContractError, "publication_failed") as error:
            ingest(store, db, "hy-home.docker", "2026-10-10")
        self.assertNotIn(
            "synthetic-private-payload",
            "".join(traceback.format_exception(error.exception)),
        )
        self.assertEqual(len(store.objects), 1)
        db.status = "published"
        self.assertEqual(
            ingest(store, db, "hy-home.docker", "2026-10-10")["status"], "published"
        )
        for status in (None, [], "synthetic-private-payload"):
            db = SyntheticPublisher([])
            db.status = status
            with self.assertRaisesRegex(ContractError, "publication_status"):
                ingest(store, db, "hy-home.docker", "2026-10-10")
