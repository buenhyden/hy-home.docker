"""Synthetic checks for the SPEC-0246 W7 write-rate comparison."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.lib.ops import storage_write_rate as rate

GB = 10**9
STARTED = "2026-01-01T00:00:00Z"


def _disk(sda_bytes: int, sdb_bytes: int) -> str:
    def line(minor: int, name: str, written: int) -> str:
        fields = [8, minor, name, 1, 0, 8, 1, 1, 0, written // 512, 1, 0, 1, 1]
        return " ".join(str(f) for f in fields)

    return f"{line(0, 'sda', sda_bytes)}\n{line(16, 'sdb', sdb_bytes)}\n"


def _snap(time: str, sda: int, rows: dict[str, tuple[str, int]]) -> dict[str, str]:
    return {
        "time": time + "\n",
        "diskstats": _disk(sda, 0),
        "wbytes": "".join(f"{n}\t{s}\t{b}\n" for n, (s, b) in rows.items()),
    }


def _rows(scale: int) -> dict[str, tuple[str, int]]:
    return {store: (STARTED, scale * GB) for store in rate.STORES}


T0 = "2026-01-01T00:00:00+09:00"
T1 = "2026-01-02T00:00:00+09:00"
# 50% used after 50 TB: the remaining 50% lasts another 50 TB.
SMART = {"smart_used_percent": 50.0, "smart_host_bytes": 50 * 10**12}


class CompareTests(unittest.TestCase):
    def test_full_day_projects_years_and_dispositions(self) -> None:
        later = _rows(1)
        later["alloy"] = (STARTED, 101 * GB)  # +100 GB/day
        result = rate.compare(
            _snap(T0, 0, _rows(1)), _snap(T1, 10 * GB, later), ssd_device="sda", **SMART
        )
        # 50 TB left at 10 GB/day is 5000 days.
        self.assertAlmostEqual(result["ssd_years_baseline"], 5000 / 365.25)
        self.assertEqual(result["stores"]["prometheus"]["disposition"], "ELIGIBLE")
        self.assertEqual(result["stores"]["prometheus"]["bytes"], 0)
        alloy = result["stores"]["alloy"]
        self.assertEqual(alloy["bytes_per_day"], 100 * GB)
        self.assertAlmostEqual(alloy["ssd_years_with_store"], 50_000 / 110 / 365.25)
        self.assertEqual(alloy["disposition"], "KEEP_HDD")

    def test_short_window_defers_every_store(self) -> None:
        result = rate.compare(
            _snap(T0, 0, _rows(1)),
            _snap("2026-01-01T23:59:59+09:00", GB, _rows(2)),
            ssd_device="sda",
            **SMART,
        )
        self.assertIsNone(result["ssd_years_baseline"])
        for store in result["stores"].values():
            self.assertEqual(store["disposition"], "DEFER")
            self.assertEqual(store["reason"], "window shorter than 24 h")

    def test_restart_decrease_and_missing_rows_are_invalid(self) -> None:
        later = _rows(2)
        later["loki"] = ("2026-01-01T12:00:00Z", 3 * GB)
        later["tempo"] = (STARTED, 0)
        del later["pyroscope"]
        result = rate.compare(
            _snap(T0, 0, _rows(1)), _snap(T1, GB, later), ssd_device="sda", **SMART
        )
        reasons = {name: s.get("reason") for name, s in result["stores"].items()}
        self.assertEqual(reasons["loki"], "container restarted (counter reset)")
        self.assertEqual(reasons["tempo"], "counter decreased")
        self.assertEqual(reasons["pyroscope"], "missing from a snapshot")
        self.assertEqual(result["stores"]["alloy"]["status"], "valid")

    def test_reboot_or_missing_smart_defers(self) -> None:
        rebooted = rate.compare(
            _snap(T0, 5 * GB, _rows(1)),
            _snap(T1, GB, _rows(2)),
            ssd_device="sda",
            **SMART,
        )
        self.assertEqual(rebooted["disks"]["sda"]["status"], "invalid")
        self.assertEqual(rebooted["stores"]["alloy"]["reason"], "SSD rate unavailable")
        no_smart = rate.compare(
            _snap(T0, 0, _rows(1)), _snap(T1, GB, _rows(2)), ssd_device="sda"
        )
        self.assertEqual(
            no_smart["stores"]["alloy"]["reason"], "SMART counters not supplied"
        )

    def test_time_reversal_and_naive_time_raise(self) -> None:
        with self.assertRaises(ValueError):
            rate.compare(
                _snap(T1, 0, _rows(1)), _snap(T0, 0, _rows(1)), ssd_device="sda"
            )
        with self.assertRaises(ValueError):
            rate.parse_time("2026-01-01T00:00:00")

    def test_duplicate_row_raises(self) -> None:
        with self.assertRaises(ValueError):
            rate.parse_wbytes(f"alloy\t{STARTED}\t1\nalloy\t{STARTED}\t2\n")


class AccountingTests(unittest.TestCase):
    def test_iostat_sum_counts_every_line_like_t0(self) -> None:
        # The 2026-10-19 t0 recorded 2x the SSD line for an SSD-only writer.
        stat = (
            "8:0 rbytes=1 wbytes=6004736 rios=1 wios=1 dbytes=0 dios=0\n"
            "252:0 rbytes=1 wbytes=6004736 rios=1 wios=1 dbytes=0 dios=0\n"
            "8:16 rbytes=1 wbytes=0 rios=1 wios=0 dbytes=0 dios=0\n"
        )
        self.assertEqual(rate.iostat_wbytes(stat), 12009472)

    def test_diskstats_reads_sectors_written(self) -> None:
        self.assertEqual(
            rate.parse_diskstats(_disk(1024, 512)), {"sda": 1024, "sdb": 512}
        )

    def test_collect_refuses_to_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "t1.time").write_text(T1)
            with self.assertRaises(FileExistsError):
                rate.collect(Path(tmp), "t1", ("sda",))


if __name__ == "__main__":
    unittest.main()
