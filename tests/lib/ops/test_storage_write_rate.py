"""Synthetic checks for the SPEC-0246 W7 write-rate comparison."""

from __future__ import annotations

import json
import subprocess
import sys
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

    def test_changed_device_numbers_defer_the_stores(self) -> None:
        later = _snap(T1, GB, _rows(2))
        later["diskstats"] = later["diskstats"].replace("8 0 sda", "259 7 sda")
        result = rate.compare(_snap(T0, 0, _rows(1)), later, ssd_device="sda", **SMART)
        self.assertEqual(result["disks"]["sda"]["status"], "invalid")
        self.assertIsNone(result["ssd_years_baseline"])
        self.assertTrue(
            all(s["disposition"] == "DEFER" for s in result["stores"].values())
        )

    def test_invalid_smart_values_are_rejected(self) -> None:
        invalid = [
            {"smart_used_percent": value, "smart_host_bytes": 50 * 10**12}
            for value in (-1, 101, float("nan"), float("inf"), True, "50")
        ] + [
            {"smart_used_percent": 50, "smart_host_bytes": value}
            for value in (-1, 0, True, 1.5, float("inf"), 10**400)
        ]
        for arguments in invalid:
            with self.subTest(arguments=arguments), self.assertRaises(ValueError):
                rate.compare(
                    _snap(T0, 0, _rows(1)),
                    _snap(T1, GB, _rows(2)),
                    ssd_device="sda",
                    **arguments,
                )

    def test_zero_missing_and_exhausted_smart_boundaries(self) -> None:
        for percent, written in ((0, 50 * 10**12), (None, None), (50, None)):
            with self.subTest(percent=percent, written=written):
                result = rate.compare(
                    _snap(T0, 0, _rows(1)),
                    _snap(T1, GB, _rows(2)),
                    ssd_device="sda",
                    smart_used_percent=percent,
                    smart_host_bytes=written,
                )
                self.assertTrue(
                    all(s["disposition"] == "DEFER" for s in result["stores"].values())
                )
        result = rate.compare(
            _snap(T0, 0, _rows(1)),
            _snap(T1, GB, _rows(2)),
            ssd_device="sda",
            smart_used_percent=100,
            smart_host_bytes=50 * 10**12,
        )
        self.assertEqual(result["ssd_years_baseline"], 0)
        self.assertTrue(
            all(s["disposition"] == "KEEP_HDD" for s in result["stores"].values())
        )

    def test_zero_ssd_delta_remains_deferred(self) -> None:
        result = rate.compare(
            _snap(T0, 0, _rows(1)), _snap(T1, 0, _rows(2)), ssd_device="sda", **SMART
        )
        self.assertTrue(
            all(s["disposition"] == "DEFER" for s in result["stores"].values())
        )

    def test_unrepresentable_rates_and_lifetime_are_rejected(self) -> None:
        for later, smart in (
            (_snap(T1, 10**310, _rows(2)), SMART),
            (_snap(T1, GB, _rows(2)), {**SMART, "smart_used_percent": 1e-320}),
        ):
            with self.subTest(smart=smart), self.assertRaises(ValueError):
                rate.compare(_snap(T0, 0, _rows(1)), later, ssd_device="sda", **smart)


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

    def test_invalid_disk_and_container_counters_are_rejected(self) -> None:
        for text in (_disk(-512, 0), _disk(0, 0) + _disk(0, 0), "malformed\n"):
            with self.subTest(text=text), self.assertRaises(ValueError):
                rate.parse_diskstats(text)
        for text in (f"alloy\t{STARTED}\t-1\n", f"alloy\t{STARTED}\t{'1' * 400}\n"):
            with self.subTest(text=text), self.assertRaises(ValueError):
                rate.parse_wbytes(text)
        with self.assertRaises(ValueError):
            rate.iostat_wbytes("8:0 wbytes=-1\n")

    def test_collect_refuses_to_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "t1.time").write_text(T1)
            with self.assertRaises(FileExistsError):
                rate.collect(Path(tmp), "t1", ("sda",))


class CliTests(unittest.TestCase):
    def _run(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "scripts/operations/storage-write-rate.py", *args],
            cwd=Path(__file__).resolve().parents[3],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_compare_prints_json_and_exit_codes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            for label, snap in (
                ("t0", _snap(T0, 0, _rows(1))),
                ("t1", _snap(T1, GB, _rows(2))),
            ):
                for key, suffix in rate.SUFFIXES.items():
                    Path(tmp, label + suffix).write_text(snap[key])
            smart = [
                "--smart-used-percent",
                "50",
                "--smart-host-bytes",
                str(50 * 10**12),
            ]
            done = self._run("compare", tmp, *smart)
            self.assertEqual(done.returncode, 0, done.stderr)
            self.assertEqual(
                json.loads(done.stdout)["stores"]["alloy"]["status"], "valid"
            )
            self.assertEqual(self._run("compare", tmp).returncode, 1)
            self.assertEqual(self._run("compare", tmp, "--t1", "absent").returncode, 2)

    def test_cli_rejects_nonfinite_smart_without_json_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            for label, snap in (
                ("t0", _snap(T0, 0, _rows(1))),
                ("t1", _snap(T1, GB, _rows(2))),
            ):
                for key, suffix in rate.SUFFIXES.items():
                    Path(tmp, label + suffix).write_text(snap[key])
            for value in ("nan", "inf", "-1", "101"):
                with self.subTest(value=value):
                    result = self._run(
                        "compare",
                        tmp,
                        "--smart-used-percent",
                        value,
                        "--smart-host-bytes",
                        str(50 * 10**12),
                    )
                    self.assertEqual(result.returncode, 2, result.stderr)
                    self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
