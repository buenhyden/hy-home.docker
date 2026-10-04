"""Native k6 raw distribution is bounded, immutable and safe before handoff."""

import json
import unittest
from unittest import mock

from tests.validation import test_k6_results as fixtures


class QualityRawPointTests(unittest.TestCase):
    def setUp(self):
        self.fixture = fixtures.K6ResultContractTests()
        self.fixture.setUp()
        self.attempt = self.fixture.prepare()
        self.fixture.write_execution(self.attempt)
        exit_path = self.attempt / "exit.json"
        exit_record = json.loads(exit_path.read_bytes())
        exit_record.update(
            schema_version="hyhome.quality-exit/v2", raw_points_required=True
        )
        exit_path.write_text(json.dumps(exit_record))
        self.metric = {
            "type": "Metric",
            "metric": "http_req_duration",
            "data": {
                "name": "http_req_duration",
                "type": "trend",
                "contains": "time",
                "thresholds": [],
                "submetrics": [],
            },
        }
        self.point = {
            "type": "Point",
            "metric": "http_req_duration",
            "data": {
                "time": "2026-10-03T00:00:00.123456789Z",
                "value": 12.5,
                "tags": {
                    name: str(self.fixture.manifest[name])
                    for name in ("project_id", "environment", "run_id", "attempt")
                },
            },
        }
        self.point["data"]["tags"]["testid"] = self.fixture.manifest["run_id"]

    def tearDown(self):
        self.fixture.tearDown()

    def points(self, point=None):
        path = self.attempt / "raw-points.json"
        path.write_text(
            json.dumps(self.metric)
            + "\n"
            + json.dumps(self.point if point is None else point)
            + "\n"
        )
        return path

    def test_native_points_preserve_distribution_time_bytes_and_digest(self):
        from tests.validation.test_k6_results import quality_run

        path = self.points()
        raw = path.read_bytes()
        final = quality_run.finalize(self.attempt)
        self.assertEqual(final["verdict"], "passed")
        self.assertTrue(final["import_allowed"])
        self.assertEqual(path.read_bytes(), raw)
        artifacts = json.loads((self.attempt / "checksums.json").read_bytes())[
            "artifacts"
        ]
        self.assertIn("raw-points.json", {item["name"] for item in artifacts})
        self.assertEqual(path.stat().st_mode & 0o222, 0)
        envelope = quality_run.prepare_import(
            self.attempt, self.fixture.root / "import.json"
        )
        self.assertIn("raw-points.json", {a["name"] for a in envelope["artifacts"]})

    def test_missing_or_truncated_native_distribution_cannot_import(self):
        from tests.validation.test_k6_results import quality_run

        final = quality_run.finalize(self.attempt)
        self.assertEqual(final["verdict"], "incomplete")
        self.assertFalse(final["import_allowed"])
        with self.assertRaises(quality_run.ContractError):
            quality_run.prepare_import(self.attempt, self.fixture.root / "import.json")

    def test_native_points_reject_unsafe_tags_nonfinite_and_invalid_time(self):
        from result_inspection import inspect_raw_points

        cases = []
        for key, value in (
            ("url", "http://wiremock:8080/health?token=synthetic"),
            ("authorization", "synthetic"),
            ("custom", "unapproved"),
        ):
            point = json.loads(json.dumps(self.point))
            point["data"]["tags"][key] = value
            cases.append(point)
        for value in (float("nan"), float("inf")):
            point = json.loads(json.dumps(self.point))
            point["data"]["value"] = value
            cases.append(point)
        point = json.loads(json.dumps(self.point))
        point["data"]["time"] = "invalid"
        cases.append(point)
        for point in cases:
            with self.subTest(point=point):
                self.points(point)
                _, issues = inspect_raw_points(self.attempt, self.fixture.manifest)
                self.assertTrue(issues)
        self.points().write_bytes(b'{"type":"Point"')
        _, issues = inspect_raw_points(self.attempt, self.fixture.manifest)
        self.assertTrue(issues)

    def test_concurrently_growing_native_stream_is_rejected(self):
        import result_inspection

        path = self.points()
        original = json.loads
        changed = False

        def append_during_parse(*args, **kwargs):
            nonlocal changed
            if not changed:
                changed = True
                with path.open("a") as stream:
                    stream.write(json.dumps(self.point) + "\n")
            return original(*args, **kwargs)

        with mock.patch.object(result_inspection.json, "loads", append_during_parse):
            _, issues = result_inspection.inspect_raw_points(
                self.attempt, self.fixture.manifest
            )
        self.assertTrue(issues)
