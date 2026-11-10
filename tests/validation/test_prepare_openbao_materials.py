"""Synthetic guards for the OpenBao material preparation script; no network."""

import base64
import hashlib
import importlib.util
import json
import subprocess
import sys
import tarfile
import tempfile
import unittest
import zlib
from io import BytesIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location(
    "prepare_openbao_materials",
    ROOT / "scripts/operations/prepare-openbao-materials.py",
)
prep = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = prep
spec.loader.exec_module(prep)


def tar_member(name, payload: bytes) -> bytes:
    stream = BytesIO()
    with tarfile.open(fileobj=stream, mode="w") as out:
        item = tarfile.TarInfo(name)
        item.size = len(payload)
        out.addfile(item, BytesIO(payload))
    return zlib.compress(stream.getvalue(), wbits=31)


class Signed(unittest.TestCase):
    """A synthetic Alpine-style key signing a gzip segment (sha1 RSA)."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.dir = Path(self.temp.name)
        private = self.dir / "private.pem"
        subprocess.run(
            ["openssl", "genrsa", "-out", str(private), "2048"],
            check=True,
            capture_output=True,
        )
        self.key = self.dir / "test.rsa.pub"
        subprocess.run(
            ["openssl", "rsa", "-in", str(private), "-pubout", "-out", str(self.key)],
            check=True,
            capture_output=True,
        )
        self.private = private

    def package(self, control=b"control", data=b"data", tamper=False):
        control_member = tar_member(".PKGINFO", control)
        sig = subprocess.run(
            ["openssl", "dgst", "-sha1", "-sign", str(self.private)],
            input=control_member,
            capture_output=True,
            check=True,
        ).stdout
        raw = (
            tar_member(".SIGN.RSA.test.rsa.pub", sig)
            + control_member
            + tar_member("f", data)
        )
        if tamper:
            raw = (
                tar_member(".SIGN.RSA.test.rsa.pub", sig)
                + tar_member(".PKGINFO", b"other")
                + tar_member("f", data)
            )
        return raw

    def test_valid_apk_signature_and_control_checksum_pass(self):
        raw = self.package()
        segments = prep.gzip_members(raw)
        self.assertEqual(3, len(segments))
        prep.verify_rsa(self.dir, self.key, "test.rsa.pub", segments, 1)
        checksum = (
            "Q1" + base64.b64encode(hashlib.sha1(segments[1][0]).digest()).decode()
        )
        row = {
            "P": "pkg",
            "V": "1-r0",
            "A": "noarch",
            "S": str(len(raw)),
            "C": checksum,
            "repository": "main",
        }
        result = prep.closure_row(row, raw, segments)
        self.assertEqual("pkg-1-r0.apk", result["filename"])
        self.assertEqual(hashlib.sha256(raw).hexdigest(), result["sha256"])
        self.assertEqual(checksum, result["index_control_checksum"])

    def test_tampered_control_segment_is_rejected(self):
        segments = prep.gzip_members(self.package(tamper=True))
        with self.assertRaises(prep.Blocked):
            prep.verify_rsa(self.dir, self.key, "test.rsa.pub", segments, 1)

    def test_signature_naming_another_key_is_rejected(self):
        segments = prep.gzip_members(self.package())
        with self.assertRaises(prep.Blocked):
            prep.verify_rsa(self.dir, self.key, "other.rsa.pub", segments, 1)

    def test_index_checksum_or_size_mismatch_is_rejected(self):
        raw = self.package()
        segments = prep.gzip_members(raw)
        row = {
            "P": "pkg",
            "V": "1-r0",
            "A": "x86_64",
            "S": str(len(raw)),
            "C": "Q1wrong",
            "repository": "main",
        }
        with self.assertRaises(prep.Blocked):
            prep.closure_row(row, raw, segments)

    def test_truncated_gzip_member_is_rejected(self):
        with self.assertRaises((prep.Blocked, zlib.error)):
            prep.gzip_members(self.package()[:-8])


INDEX = """\
C:Q1a
P:app
V:1-r0
A:x86_64
S:1
D:so:libc.musl-x86_64.so.1 /bin/sh !conflicting libx=2
p:cmd:app=1-r0

C:Q1b
P:musl
V:1-r3
A:x86_64
S:1
p:so:libc.musl-x86_64.so.1=1

C:Q1c
P:busybox-binsh
V:1-r0
A:noarch
S:1
D:busybox=1-r0
p:/bin/sh

C:Q1d
P:busybox
V:1-r0
A:x86_64
S:1

C:Q1e
P:ssl_client
V:1-r0
A:x86_64
S:1
i:busybox=1-r0

C:Q1f
P:busybox-doc
V:1-r0
A:noarch
S:1
i:docs busybox=1-r0

C:Q1g
P:libx
V:2-r0
A:x86_64
S:1
"""


class Closure(unittest.TestCase):
    def packages(self, text=INDEX):
        return prep.parse_index(text, "main")

    def test_dependencies_providers_and_install_if_resolve_like_apk(self):
        names = [row["P"] for row in prep.resolve_closure(self.packages(), ["app"])]
        self.assertEqual(
            ["app", "busybox", "busybox-binsh", "libx", "musl", "ssl_client"],
            sorted(names),
        )

    def test_conflict_tokens_and_unmet_install_if_pull_nothing(self):
        names = {row["P"] for row in prep.resolve_closure(self.packages(), ["app"])}
        self.assertNotIn("busybox-doc", names)
        self.assertNotIn("conflicting", names)

    def test_two_equal_priority_providers_are_ambiguous(self):
        text = INDEX + "\nC:Q1h\nP:alt\nV:1\nA:noarch\nS:1\np:/bin/sh\n"
        with self.assertRaises(prep.Blocked):
            prep.resolve_closure(self.packages(text), ["app"])

    def test_duplicate_versions_matter_only_when_selected(self):
        text = INDEX + "\nC:Q1i\nP:libx\nV:3-r0\nA:x86_64\nS:1\n"
        with self.assertRaises(prep.Blocked):
            prep.resolve_closure(self.packages(text), ["app"])
        names = {
            row["P"] for row in prep.resolve_closure(self.packages(text), ["musl"])
        }
        self.assertEqual({"musl"}, names)


class Boundaries(unittest.TestCase):
    def test_only_approved_https_hosts_and_github_cdn_redirects(self):
        prep.check_url("https://github.com/openbao/openbao/releases/download/v2.7.1/x")
        prep.check_url(
            "https://dl-cdn.alpinelinux.org/alpine/v3.24/main/x86_64/APKINDEX.tar.gz"
        )
        prep.check_url("https://release-assets.githubusercontent.com/x", redirect=True)
        for url, redirect in (
            ("http://github.com/x", False),
            ("https://proxy.golang.org/x", False),
            ("https://release-assets.githubusercontent.com/x", False),
            ("https://evil.example/x", True),
            ("https://user:pass@github.com/x", False),
        ):
            with self.assertRaises(prep.Blocked):
                prep.check_url(url, redirect=redirect)

    def test_approval_line_must_be_on_a_line_of_its_own(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "approvals.md"
            path.write_text(f"intro {prep.APPROVAL_LINE}\n")
            with self.assertRaises(prep.Blocked):
                prep.require_approval(path)
            path.write_text(f"x\n{prep.APPROVAL_LINE}\n")
            prep.require_approval(path)
        prep.require_approval()  # the tracked approval entry is present

    def test_existing_or_foreign_root_is_refused_before_any_fetch(self):
        with self.assertRaises(prep.Blocked):
            prep.prepare(Path("/tmp/not-owned-build-root"), allow_go_proxy=False)
        with tempfile.TemporaryDirectory(prefix="hyhome-p01-owned-build-") as existing:
            with self.assertRaises(FileExistsError):
                prep.prepare(Path(existing), allow_go_proxy=False)

    def test_cosign_contract_has_no_host_mounts_and_bounded_limits(self):
        limits = prep.COSIGN_LIMITS
        for flag, value in (
            ("--memory", "512m"),
            ("--pids-limit", "32"),
            ("--cpus", "1"),
            ("--cap-drop", "ALL"),
        ):
            self.assertEqual(value, limits[limits.index(flag) + 1])
        self.assertIn("--read-only", limits)
        self.assertIn("no-new-privileges", limits)
        self.assertNotIn("docker.sock", " ".join(limits))
        self.assertTrue(prep.COSIGN.startswith("gcr.io/projectsigstore/cosign@sha256:"))

    def test_receipt_records_pass_exit_and_exact_command(self):
        with tempfile.TemporaryDirectory() as directory:
            digest = prep.write_receipt(
                Path(directory), "x", {"command": ["cosign", "verify"], "identity": "i"}
            )
            raw = (Path(directory) / "x-receipt.json").read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), digest)
        document = json.loads(raw)
        self.assertEqual(
            ("PASS", 0, ["cosign", "verify"]),
            (document["status"], document["exit"], document["command"]),
        )

    def test_documented_identities_are_pinned_strings(self):
        self.assertTrue(
            prep.OPENBAO_IDENTITY_REGEXP.startswith(
                "^https://github.com/openbao/openbao/.github/workflows/release.yml@"
            )
        )
        self.assertEqual(
            "https://github.com/chainguard-images/images/.github/workflows/release.yaml@refs/heads/main",
            prep.CHAINGUARD_IDENTITY,
        )


class SourceAndMaterials(unittest.TestCase):
    def test_source_extraction_drops_symlinks_applies_patch_and_materials_accept(self):
        builder = prep.load_builder()
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            archive, patch = work / "source.tar", work / "go.patch"
            with tarfile.open(archive, "w") as out:
                for name, payload in (
                    ("dist/go.mod", b"module x\n\ngo 1.27\n"),
                    ("dist/go.sum", b"a 1\n"),
                ):
                    item = tarfile.TarInfo(name)
                    item.size = len(payload)
                    out.addfile(item, BytesIO(payload))
                link = tarfile.TarInfo("dist/CLAUDE.md")
                link.type, link.linkname = tarfile.SYMTYPE, "AGENTS.md"
                out.addfile(link)
            patch.write_text(
                "--- a/go.mod\n+++ b/go.mod\n@@ -1,3 +1,3 @@\n module x\n \n-go 1.27\n+go 1.28\n"
            )
            target = work / "source"
            extra = prep.extract_source(archive, target, patch)
            self.assertEqual({"omitted_symlinks": ["CLAUDE.md"]}, extra)
            self.assertIn(b"go 1.28", (target / "go.mod").read_bytes())
            self.assertFalse((target / "CLAUDE.md").exists())

        material_root = Path(tempfile.mkdtemp(prefix="hyhome-p01-owned-build-"))
        self.addCleanup(lambda: __import__("shutil").rmtree(material_root))
        material = material_root / "materials"
        material.mkdir(mode=0o700)
        for name in ("source", "modules", "apks", "keys", "proof"):
            (material / name).mkdir()
        (material / "source/go.mod").write_bytes(b"module x\n")
        (material / "source/go.sum").write_bytes(b"sum\n")
        (material / "modules/m").write_bytes(b"m")
        (material / "keys/k.pub").write_bytes(b"key")
        (material / "apks/a.apk").write_bytes(b"apk")
        (material / "proof/source.tar.xz").write_bytes(b"src")
        receipts = {}
        for label in ("builder", "source_checksums"):
            raw = json.dumps({"status": "PASS", "exit": 0}).encode()
            (material / f"proof/{label}-receipt.json").write_bytes(raw)
            receipts[label] = hashlib.sha256(raw).hexdigest()
        indexes = {}
        for label in ("main", "community"):
            (material / f"proof/{label}-APKINDEX.tar.gz").write_bytes(label.encode())
            indexes[label] = hashlib.sha256(label.encode()).hexdigest()
        inputs = {
            "source_archive_sha256": hashlib.sha256(b"src").hexdigest(),
            "go_patch_sha256": "p" * 64,
            "alpine_key_sha256": hashlib.sha256(b"key").hexdigest(),
            "publisher_receipts": receipts,
            "apk_indexes": indexes,
            "apk_closure": [
                {
                    "filename": "a.apk",
                    "size": 3,
                    "sha256": hashlib.sha256(b"apk").hexdigest(),
                }
            ],
        }
        sha = prep.write_materials(builder, material, inputs, {})
        self.assertEqual(
            sha, hashlib.sha256((material / "materials.json").read_bytes()).hexdigest()
        )
        document = builder.materials(material, sha, inputs)
        self.assertEqual("PASS", document["offline_module_verification"])
        self.assertEqual("PASS", document["signed_apk_verification"])


if __name__ == "__main__":
    unittest.main()
