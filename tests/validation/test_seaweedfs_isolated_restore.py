"""Contract of the SeaweedFS isolated restore (RUN-0024, SPEC-0212 TSK-0128)."""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/operations/seaweedfs-isolated-restore.py"
COMPOSE = ROOT / "infra/04-data/seaweedfs/docker-compose.yml"


def load():
    spec = importlib.util.spec_from_file_location("swfs_restore", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def state_tree(root: Path) -> Path:
    state = root / "state"
    volume = state / "volumes/data/seaweedfs/volume"
    volume.mkdir(parents=True)
    (volume / "opsflow-dev_1.dat").write_bytes(b"x" * 8)
    (volume / "opsflow-dev_1.idx").write_bytes(b"i")
    exports = state / "exports"
    exports.mkdir()
    (exports / "seaweedfs-filer.meta").write_bytes(b"meta")
    return state


LIST = (
    '<ListBucketResult xmlns="http://s3.amazonaws.com/doc/2006-03-01/">'
    "<IsTruncated>false</IsTruncated>"
    "<Contents><Key>a/b.json</Key><Size>5</Size></Contents>"
    "<Contents><Key>c d.json</Key><Size>7</Size></Contents>"
    "</ListBucketResult>"
)


class FakeDocker:
    """Answers the docker calls of one restore run."""

    def __init__(
        self,
        fsck="13,4ef5 /buckets/loki-bucket/seed.json volume not found\ntotal 3 directories, 9 files\n",
        read="2 12",
        du_bytes=12,
    ):
        self.calls = []
        self.fsck, self.read, self.du_bytes = fsck, read, du_bytes

    def __call__(self, argv, *, timeout, stdin=None):
        self.calls.append(argv)
        text = " ".join(argv)
        if argv[:3] == ["docker", "run", "-d"] or argv[:3] == ["docker", "rm", "-f"]:
            return 0, b""
        if "weed shell" in text:
            script = (stdin or b"").decode()
            if "fs.ls /buckets" in script:
                return 0, b"opsflow-dev/\nloki-bucket/\n"
            if "volume.fsck" in script:
                return 0, self.fsck.encode()
            if "fs.du" in script:
                return (
                    0,
                    f"block:   3\tbyte:{self.du_bytes:>10}\t/buckets/opsflow-dev\n".encode(),
                )
            return 0, b"loaded\n"
        if "8080/status" in text:
            return 0, json.dumps({"Volumes": [{"Id": 1}]}).encode()
        if "list-type=2" in text:
            return 0, LIST.encode()
        if argv[-2:-1] == ["-c"]:
            return 0, self.read.encode()
        return 0, b"ok"


class SeaweedfsIsolatedRestoreTests(unittest.TestCase):
    def setUp(self):
        self.mod = load()

    def test_image_is_the_compose_pin(self):
        self.assertIn(f"image: {self.mod.IMAGE}", COMPOSE.read_text())

    def test_parsers(self):
        self.assertEqual(
            (12, 3456), self.mod.parse_du("block:  12\tbyte:      3456\t/buckets/x\n")
        )
        self.assertEqual(
            (2, 10),
            self.mod.parse_du("block:   2\tlogical size:  10\tphysical size: 11\t/b\n"),
        )
        self.assertIsNone(self.mod.parse_du("nothing"))
        self.assertEqual(
            ["lakehouse", "opsflow-dev"],
            self.mod.parse_buckets("> \nopsflow-dev/\n/buckets/lakehouse\nREADME\n"),
        )
        # The real 4.54 output: one "<fid> <path> <reason>" line per missing chunk.
        summary = self.mod.parse_fsck(
            "13,4ef58b8f6e2 /buckets/loki-bucket/seed.json volume not found\n"
            "9,1705f9 /buckets/loki-bucket/fake/a volume not found\n"
            "21,1752 /buckets/tempo-bucket/work.json volume not found\n"
            "total 2060 directories, 6373 files\n"
        )
        self.assertEqual(
            {"loki-bucket": 2, "tempo-bucket": 1}, summary["missing_by_bucket"]
        )
        self.assertEqual([], summary["unparsed"])
        odd = self.mod.parse_fsck("unexpected text from the shell\n")
        self.assertEqual(["unexpected text from the shell"], odd["unparsed"])

    def test_bad_input_is_refused_before_docker(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fake = FakeDocker()
            with self.assertRaises(self.mod.RestoreError):
                self.mod.restore(
                    state_dir=root / "none", workdir=root / "w", keep=False, run=fake
                )
            state = state_tree(root)
            (root / "w").mkdir()
            with self.assertRaises(self.mod.RestoreError):
                self.mod.restore(
                    state_dir=state, workdir=root / "w", keep=False, run=fake
                )
            self.assertEqual([], fake.calls)

    def run_restore(self, fake):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            state = state_tree(root)
            work = root / "work"
            receipt = self.mod.restore(
                state_dir=state, workdir=work, keep=False, run=fake,
                sleep=lambda _: None,
            )  # fmt: skip
            self.assertFalse(work.exists(), "work directory removed")
            self.assertTrue((state / "exports/seaweedfs-filer.meta").is_file())
            return receipt

    def test_isolated_run_passes_and_always_cleans_up(self):
        fake = FakeDocker()
        receipt = self.run_restore(fake)
        self.assertEqual("PASS", receipt["result"], receipt)
        self.assertEqual(["loki-bucket"], receipt["excluded_buckets"])
        bucket = receipt["buckets"]["opsflow-dev"]
        self.assertEqual(
            (2, 12, 2, 12),
            (
                bucket["s3_objects"],
                bucket["s3_listed_bytes"],
                bucket["objects_read"],
                bucket["bytes_read"],
            ),
        )
        start = next(c for c in fake.calls if c[:3] == ["docker", "run", "-d"])
        self.assertIn("--network=none", start)
        self.assertIn("--cap-drop=ALL", start)
        self.assertEqual(["docker", "rm", "-f"], fake.calls[-1][:3])

    def test_missing_chunks_or_short_reads_fail(self):
        missing = self.run_restore(
            FakeDocker(fsck="1,ab /buckets/opsflow-dev/a volume not found\n")
        )
        self.assertEqual("FAIL", missing["result"])
        self.assertEqual(["opsflow-dev"], missing["fsck"]["unexpected_missing_buckets"])
        odd = self.run_restore(FakeDocker(fsck="panic: lost the filer\n"))
        self.assertEqual("FAIL", odd["result"])
        short = self.run_restore(FakeDocker(read="1 5"))
        self.assertEqual("FAIL", short["result"])
        self.assertFalse(short["buckets"]["opsflow-dev"]["match"])


if __name__ == "__main__":
    unittest.main()
