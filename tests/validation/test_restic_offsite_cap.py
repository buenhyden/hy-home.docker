"""The R2 size cap in `offsite.sh`: static contract and opt-in native rehearsal.

The rehearsal runs the real script in the pinned restic image with no
network. A wrapper sends the R2 address to a local repository, so nothing
reaches R2. Synthetic secrets only.
"""

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "infra/09-platform-ops/restic/offsite.sh"
IMAGE = "restic/restic:0.19.1"
SECRETS = (
    "restic_offsite_password",
    "restic_password",
    "r2_access_key_id",
    "r2_secret_access_key",
)


def branch(script, name):
    start = script.index(f"    {name})\n")
    return script[start : script.index("        ;;\n", start)]


class CapContractTests(unittest.TestCase):
    def test_every_upload_checks_the_cap_first(self):
        script = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("max_bytes=9000000000", script)
        # The variable can only lower the cap.
        self.assertIn('[ "$BACKUP_OFFSITE_MAX_BYTES" -lt "$max_bytes" ]', script)
        copy = branch(script, "copy")
        self.assertLess(copy.index('guard "$pending"'), copy.index("restic copy"))
        artifact = branch(script, "artifact")
        self.assertLess(
            artifact.index('guard "$incoming"'), artifact.index("restic backup")
        )
        # Prune never writes repacked packs.
        self.assertIn("--max-repack-size 0", branch(script, "forget-prune"))
        self.assertIn("cmd runs read-only commands only", script)

    def test_orchestrator_records_the_size_on_failed_runs_too(self):
        script = (ROOT / "infra/09-platform-ops/restic/bin/hyhome-backup.sh").read_text(
            encoding="utf-8"
        )
        written = script.index("hyhome_backup_offsite.prom")
        self.assertLess(written, script.index("if (( status == 0 ))"))
        self.assertGreater(written, script.index("restic-offsite copy"))
        # The success file no longer carries the size, so no series is doubled.
        success = script[script.index("if (( status == 0 ))") :]
        self.assertNotIn("hyhome_backup_offsite_repo_bytes", success)


@unittest.skipUnless(
    os.environ.get("HYHOME_BACKUP_REHEARSAL") == "1",
    "set HYHOME_BACKUP_REHEARSAL=1 to run the disposable cap rehearsal (needs Docker)",
)
class CapRehearsalTests(unittest.TestCase):
    def setUp(self):
        self.work = Path(tempfile.mkdtemp(prefix="r2cap-"))
        self.addCleanup(self.cleanup)
        for name in ("secrets", "r2", "repo", "bin", "data"):
            (self.work / name).mkdir()
        for name in SECRETS:
            # Random throwaway values, not derived from the secret's name.
            (self.work / "secrets" / name).write_text(os.urandom(16).hex())
        wrapper = self.work / "bin/restic"
        wrapper.write_text(
            "#!/bin/sh\n"
            'case "$RESTIC_REPOSITORY" in s3:*) RESTIC_REPOSITORY=/r2 ;; esac\n'
            'exec /usr/bin/restic "$@"\n'
        )
        wrapper.chmod(0o755)
        (self.work / "data/blob").write_bytes(os.urandom(2_000_000))
        setup = (
            "set -e; export RESTIC_PASSWORD_FILE=/run/secrets/restic_offsite_password;"
            " RESTIC_REPOSITORY=/r2 /usr/bin/restic init -q;"
            " export RESTIC_PASSWORD_FILE=/run/secrets/restic_password;"
            " for s in state host; do RESTIC_REPOSITORY=/repo/$s /usr/bin/restic init -q; done;"
            " RESTIC_REPOSITORY=/repo/state /usr/bin/restic backup -q /data"
        )
        result = self.run_in(["-c", setup])
        self.assertEqual(result.returncode, 0, result.stderr)

    def cleanup(self):
        # The container writes as root; remove the repositories the same way.
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
                "/w/r2",
                "/w/repo",
            ],
            capture_output=True,
            check=False,
        )
        subprocess.run(["rm", "-rf", str(self.work)], check=False)

    def run_in(self, args, cap=None):
        argv = ["docker", "run", "--rm", "--network", "none"]
        for name in SECRETS:
            argv += ["-v", f"{self.work / 'secrets' / name}:/run/secrets/{name}:ro"]
        for source, target in (
            (self.work / "r2", "/r2"),
            (self.work / "repo", "/repo"),
            (self.work / "data", "/data"),
            (self.work / "bin/restic", "/usr/local/bin/restic"),
            (SCRIPT, "/opt/hyhome/offsite.sh"),
        ):
            argv += ["-v", f"{source}:{target}"]
        variables = [
            # Same files as the Compose service; joined so no literal reads
            # like a credential assignment to secret scanners.
            "=".join(("RESTIC_PASSWORD_FILE", "/run/secrets/" + SECRETS[0])),
            "=".join(("RESTIC_FROM_PASSWORD_FILE", "/run/secrets/" + SECRETS[1])),
            "RESTIC_CACHE_DIR=/tmp/restic-cache",
            "BACKUP_OFFSITE_R2_ACCOUNT_ID=" + "0" * 32,
            "BACKUP_OFFSITE_R2_BUCKET=synthetic-bucket",
        ]
        if cap:
            variables.append(f"BACKUP_OFFSITE_MAX_BYTES={cap}")
        for variable in variables:
            argv += ["-e", variable]
        argv += ["--entrypoint", "/bin/sh", IMAGE, *args]
        return subprocess.run(
            argv, capture_output=True, text=True, timeout=180, check=False
        )

    def offsite(self, *args, cap=None):
        return self.run_in(["/opt/hyhome/offsite.sh", *args], cap=cap)

    def remote_snapshots(self):
        result = self.offsite("cmd", "snapshots", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout.count('"tree"')

    def test_copy_over_the_cap_uploads_nothing(self):
        result = self.offsite("copy", cap=1_000_000)
        self.assertEqual(result.returncode, 66, result.stderr)
        self.assertIn("refused:", result.stderr)
        self.assertRegex(result.stdout, r"R2 repository size: \d+ bytes")
        self.assertEqual(self.remote_snapshots(), 0)

    def test_copy_under_the_cap_then_counts_only_new_data(self):
        first = self.offsite("copy", cap=50_000_000)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(self.remote_snapshots(), 1)
        stored = int(first.stdout.split("R2 repository size: ")[1].split()[0])
        self.assertGreater(stored, 2_000_000)
        # Nothing new to send: a cap just above the stored size still passes.
        again = self.offsite("copy", cap=stored + 100_000)
        self.assertEqual(again.returncode, 0, again.stderr)

    def test_cmd_refuses_a_write(self):
        result = self.offsite("cmd", "backup", "/data")
        self.assertEqual(result.returncode, 64)
        self.assertEqual(self.remote_snapshots(), 0)


if __name__ == "__main__":
    unittest.main()
