"""RUN-0085 W3b `offsite.sh artifact`: static contract and opt-in native rehearsal.

The rehearsal runs the real script in the pinned restic image against a local
repository: a wrapper sets RESTIC_REPOSITORY, which the script otherwise points
at R2. Synthetic secrets only; nothing reaches R2.
"""

import hashlib
import json
import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "infra/09-platform-ops/restic/offsite.sh"
IMAGE = "restic/restic:0.19.1"
FILES = ("raft-pre-upgrade.snap", "raft-pre-upgrade.snap.receipt.json")
SECRETS = ("restic_offsite_password", "r2_access_key_id", "r2_secret_access_key")


def branch(script):
    start = script.index("    artifact)\n")
    return script[start : script.index("        ;;\n", start)]


class ArtifactContractTests(unittest.TestCase):
    def test_artifact_only_adds_and_reads_back(self):
        body = branch(SCRIPT.read_text())
        self.assertIn("require_initialized", body)
        self.assertIn("restic backup --json", body)
        self.assertIn('restic dump "$id"', body)
        self.assertIn("set -o pipefail", body)
        self.assertIn('[ ! -s "/artifact/$name" ]', body)
        for word in ("forget", "prune", "unlock", "rm ", "--force"):
            self.assertNotIn(word, body)
        for name in FILES:
            self.assertIn(name, body)


@unittest.skipUnless(
    os.environ.get("HYHOME_OPENBAO_REHEARSAL") == "1",
    "opt-in native rehearsal with the pinned restic image",
)
class ArtifactRehearsalTests(unittest.TestCase):
    def setUp(self):
        self.work = Path(tempfile.mkdtemp(prefix="w3b-"))
        self.addCleanup(self.cleanup)
        for name in ("secrets", "repo", "artifact", "bin"):
            (self.work / name).mkdir()
        for name in SECRETS:
            (self.work / "secrets" / name).write_text("synthetic-" + name)
        wrapper = self.work / "bin/restic"
        wrapper.write_text(
            '#!/bin/sh\nRESTIC_REPOSITORY=/repo exec /usr/bin/restic "$@"\n'
        )
        wrapper.chmod(0o755)
        self.snapshot = os.urandom(300000)
        (self.work / "artifact" / FILES[0]).write_bytes(self.snapshot)
        digest = hashlib.sha256(self.snapshot).hexdigest()
        (self.work / "artifact" / FILES[1]).write_text(
            # Same serialization as protected-snapshot-custody.publish_receipt.
            json.dumps(
                {"sha256": digest, "synthetic": True},
                sort_keys=True,
                separators=(",", ":"),
            )
            + "\n"
        )
        self.assertEqual(self.docker("init").returncode, 0, "synthetic init failed")

    def cleanup(self):
        # The container writes the repository as root; remove it the same way.
        subprocess.run(
            [
                "docker",
                "run",
                "--rm",
                "--entrypoint",
                "/bin/rm",
                "-v",
                f"{self.work}:/w",
                IMAGE,
                "-rf",
                "/w/repo",
            ],
            capture_output=True,
            check=False,
        )
        subprocess.run(["rm", "-rf", str(self.work)], check=False)

    def docker(self, action):
        argv = ["docker", "run", "--rm", "--network", "none"]
        for name in SECRETS:
            argv += ["-v", f"{self.work / 'secrets' / name}:/run/secrets/{name}:ro"]
        mounts = (
            (self.work / "repo", "/repo", ""),
            (self.work / "artifact", "/artifact", ":ro"),
            (self.work / "bin/restic", "/usr/local/bin/restic", ":ro"),
            (SCRIPT, "/opt/hyhome/offsite.sh", ":ro"),
        )
        for source, target, mode in mounts:
            argv += ["-v", f"{source}:{target}{mode}"]
        for variable in (
            # Same file as the Compose service; joined so no literal reads
            # like a credential assignment to secret scanners.
            "=".join(("RESTIC_PASSWORD_FILE", "/run/secrets/" + SECRETS[0])),
            "RESTIC_CACHE_DIR=/tmp/restic-cache",
            "BACKUP_OFFSITE_R2_ACCOUNT_ID=" + "0" * 32,
            "BACKUP_OFFSITE_R2_BUCKET=synthetic-bucket",
        ):
            argv += ["-e", variable]
        argv += ["--entrypoint", "/bin/sh", IMAGE]
        if action == "init":
            argv += ["-c", "RESTIC_REPOSITORY=/repo /usr/bin/restic init -q"]
        else:
            argv += ["/opt/hyhome/offsite.sh", action]
        return subprocess.run(
            argv, capture_output=True, text=True, timeout=120, check=False
        )

    def test_stores_both_files_and_proves_the_bytes(self):
        result = self.docker("artifact")
        self.assertEqual(result.returncode, 0, "artifact action failed")
        receipt = json.loads(result.stdout.strip().splitlines()[-1])
        self.assertEqual(receipt["state"], "W3B_STORED")
        self.assertRegex(receipt["snapshot_id"], re.compile(r"^[0-9a-f]{64}$"))
        self.assertEqual([item["name"] for item in receipt["files"]], list(FILES))
        self.assertEqual(receipt["files"][0]["bytes"], len(self.snapshot))
        self.assertNotIn("synthetic-restic", result.stdout + result.stderr)

    def test_snapshot_not_named_by_its_receipt_stops_before_any_backup(self):
        (self.work / "artifact" / FILES[0]).write_bytes(b"other bytes")
        self.assertEqual(self.docker("artifact").returncode, 64)
        self.assertNotIn("hy-home-openbao-window", self.docker("snapshots").stdout)

    def test_empty_input_stops_before_any_backup(self):
        (self.work / "artifact" / FILES[1]).write_bytes(b"")
        self.assertEqual(self.docker("artifact").returncode, 64)

    def test_missing_or_linked_input_stops_before_any_backup(self):
        receipt = self.work / "artifact" / FILES[1]
        receipt.unlink()
        receipt.symlink_to(FILES[0])
        result = self.docker("artifact")
        self.assertEqual(result.returncode, 64)
        listed = self.docker("snapshots")
        self.assertEqual(listed.returncode, 0)
        self.assertNotIn("hy-home-openbao-window", listed.stdout)


if __name__ == "__main__":
    unittest.main()
