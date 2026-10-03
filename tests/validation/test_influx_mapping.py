"""Synthetic contract checks for a future Influx logical migration."""

import importlib.util
import unittest
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[2] / "infra/04-data/influxdb/migration/validate_mapping.py"
SPEC = importlib.util.spec_from_file_location("influx_mapping", SOURCE)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def mapping():
    return {
        "schema_version": 1,
        "measurement": "synthetic_temperature",
        "tags": ["device_id"],
        "fields": [{"name": "value", "type": "float", "unit": "celsius"}],
        "source_precision": "ns",
        "target_timestamp": "observed_at",
        "retain_source_ns": True,
        "retention": "source-unchanged",
        "query": "approved-query-reference",
        "writers": ["synthetic-writer"],
    }


class InfluxMappingTests(unittest.TestCase):
    def test_complete_mapping_and_explicit_empty_source(self):
        self.assertEqual(MODULE.validate(mapping())["source_precision"], "ns")
        self.assertEqual(MODULE.empty_source_result(mapping(), 0)["status"], "NO_DATA")
        with self.assertRaises(ValueError):
            MODULE.empty_source_result(mapping(), 1)

    def test_ambiguous_or_unsafe_mapping_fails(self):
        bad = (
            {"source_precision": "auto"},
            {"fields": [{"name": "value", "type": "unknown", "unit": "celsius"}]},
            {"fields": [{"name": "value", "type": "float"}]},
            {"tags": ["value"]},
            {"writers": []},
            {"extra": "ignored"},
        )
        for change in bad:
            with self.subTest(change=change), self.assertRaises(ValueError):
                MODULE.validate({**mapping(), **change})


if __name__ == "__main__":
    unittest.main()
