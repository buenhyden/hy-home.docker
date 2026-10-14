"""Offline trusted installer, receipt and interrupted-write regressions."""

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from .test_openbao_issuance import BASE, REV, WHEN, FakeAPI, M


class TrustedInstallTests(unittest.TestCase):
    def test_exact_committed_blobs_atomically_installed_without_overwrite(self):
        import hashlib

        with tempfile.TemporaryDirectory() as directory:
            parent = Path(directory)
            repo = parent / "repo"
            repo.mkdir()
            source = repo / "infra/03-security/openbao/scripts"
            source.mkdir(parents=True)
            for name in (
                "issue-renderer-secret-id.sh",
                "renderer-issuance.py",
                "renderer-request.sh",
                "install-renderer-issuer.sh",
            ):
                (source / name).write_bytes((BASE / "scripts" / name).read_bytes())

            def git(*args):
                return subprocess.run(
                    ["/usr/bin/git", "-C", str(repo), *args],
                    check=True,
                    capture_output=True,
                    env={
                        "PATH": "/usr/bin:/bin",
                        "GIT_CONFIG_NOSYSTEM": "1",
                        "GIT_CONFIG_GLOBAL": "/dev/null",
                        "GIT_NO_REPLACE_OBJECTS": "1",
                    },
                ).stdout

            git("init", "--quiet")
            git("add", ".")
            git(
                "-c",
                "user.name=SEC01 synthetic fixture",
                "-c",
                "user.email=fixture@example.invalid",
                "commit",
                "--quiet",
                "-m",
                "test: committed public helper fixture",
            )
            revision = git("rev-parse", "HEAD").decode().strip()
            (source / "renderer-request.sh").write_text("exit 99")
            git("add", ".")
            git(
                "-c",
                "user.name=fixture",
                "-c",
                "user.email=fixture@example.invalid",
                "commit",
                "--quiet",
                "-m",
                "test: replacement object",
            )
            replacement = git("rev-parse", "HEAD").decode().strip()
            git("replace", revision, replacement)
            target = parent / "reviewed-install"
            installer = parent / "approved-installer.sh"
            installer.write_bytes(
                git(
                    "show",
                    revision
                    + ":infra/03-security/openbao/scripts/install-renderer-issuer.sh",
                )
            )
            installer.chmod(0o400)
            marker = parent / "malicious-installer-executed"
            (source / "install-renderer-issuer.sh").write_text(
                "#!/bin/sh\ntouch " + str(marker) + "\nexit 1\n"
            )

            def run(target_path, rev=revision):
                return subprocess.run(
                    ["sh", str(installer), str(repo), rev, str(target_path)],
                    capture_output=True,
                    timeout=20,
                    check=False,
                )

            # Dirty source changes are deliberately excluded from the installed artifact.
            (source / "renderer-issuance.py").write_text("unreviewed working tree code")
            with patch.dict(
                os.environ,
                {
                    "GIT_DIR": str(parent / "poisoned-git"),
                    "GIT_CONFIG_COUNT": "1",
                    "GIT_CONFIG_KEY_0": "core.bare",
                    "GIT_CONFIG_VALUE_0": "true",
                },
            ):
                done = run(target)
            self.assertEqual(0, done.returncode)
            self.assertFalse(marker.exists())
            self.assertEqual(b"", done.stdout)
            self.assertEqual(b"", done.stderr)
            receipt = json.loads((target / "source-receipt.json").read_text())
            self.assertEqual(revision, receipt["source_revision"])
            for name, mode in (
                ("issue-renderer-secret-id.sh", 0o500),
                ("renderer-issuance.py", 0o400),
                ("renderer-request.sh", 0o400),
            ):
                blob = git(
                    "show", revision + ":infra/03-security/openbao/scripts/" + name
                )
                self.assertEqual(blob, (target / name).read_bytes())
                self.assertEqual(mode, (target / name).stat().st_mode & 0o777)
                self.assertEqual(
                    hashlib.sha256(blob).hexdigest(), receipt["sha256"][name]
                )
            self.assertNotEqual(0, run(target).returncode)
            unknown = parent / "unknown"
            unknown.mkdir(mode=0o700)
            self.assertNotEqual(0, run(unknown).returncode)
            self.assertEqual([], list(unknown.iterdir()))
            alias = parent / "alias"
            alias.symlink_to(unknown)
            self.assertNotEqual(0, run(alias).returncode)
            self.assertNotEqual(0, run(parent / "bad-revision", "bad").returncode)
            self.assertFalse((parent / "bad-revision").exists())
            public_parent = parent / "public"
            public_parent.mkdir(mode=0o755)
            self.assertNotEqual(0, run(public_parent / "unsafe-install").returncode)
            self.assertFalse((public_parent / "unsafe-install").exists())


class InterruptedAtomicUpdateTests(unittest.TestCase):
    def test_partial_write_blocks_even_with_an_older_valid_journal(self):
        with (
            tempfile.TemporaryDirectory() as directory,
            M.Journal(directory) as journal,
        ):
            journal.save(M.Record("1" * 32, M.utc(WHEN), M.ROLE, REV, M.MANIFEST))
            (Path(directory) / "issuance.json.pending").write_text("{")
            api = FakeAPI()
            with self.assertRaises(M.Blocked):
                M.run_issuance(api, journal, revision=REV)
            self.assertNotIn("issue", api.calls)
            self.assertTrue((Path(directory) / "issuance.json").exists())
            self.assertTrue((Path(directory) / "issuance.json.pending").exists())


class JournalVersionCompatibilityTests(unittest.TestCase):
    @staticmethod
    def record(version, nonce="1" * 32):
        return M.Record(
            nonce,
            M.utc(WHEN),
            M.ROLE,
            REV,
            M.MANIFEST,
            schema_version=version,
        )

    @staticmethod
    def accessor(metadata):
        return {"metadata": metadata, "creation_time": M.utc(WHEN + 1)}

    def test_versioned_documents_anchors_and_metadata_are_exact(self):
        legacy = self.record(1)
        current = self.record(2)
        self.assertEqual(legacy.nonce, legacy.issuance_id)
        self.assertEqual(current.nonce, current.issuance_id)
        self.assertEqual(
            {
                "nonce": legacy.nonce,
                "started_at": legacy.started_at,
                "role": M.ROLE,
                "source_revision": REV,
                "image_manifest": M.MANIFEST,
                "state": "issuing",
                "agent_started_at": None,
            },
            legacy.document(),
        )
        self.assertEqual(
            {
                **legacy.document(),
                "schema_version": 2,
                "issuance_id": current.nonce,
            },
            current.document(),
        )
        self.assertEqual(
            {"nonce": legacy.nonce, "state": "active"},
            legacy.anchor("active"),
        )
        self.assertEqual(
            {
                "nonce": current.nonce,
                "state": "active",
                "schema_version": 2,
                "issuance_id": current.nonce,
            },
            current.anchor("active"),
        )
        self.assertEqual(
            {
                "sec01_nonce": legacy.nonce,
                "sec01_role": M.ROLE,
                "sec01_issued_at": legacy.started_at,
            },
            legacy.metadata(),
        )
        self.assertEqual(
            {
                **legacy.metadata(),
                "issuance_schema": "2",
                "issuance_id": current.nonce,
            },
            current.metadata(),
        )

    def test_both_journal_versions_roundtrip_without_rewriting_active_bytes(self):
        for version in (1, 2):
            with self.subTest(version=version), tempfile.TemporaryDirectory() as path:
                with M.Journal(path) as journal:
                    record = self.record(version)
                    journal.save(record)
                    root = Path(path)
                    before = {
                        name: (root / name).read_bytes()
                        for name in ("issuance.json", "issuance.anchor")
                    }
                    self.assertEqual(record, journal.load())
                    self.assertEqual(
                        before,
                        {name: (root / name).read_bytes() for name in before},
                    )

    def test_preexisting_unversioned_journal_reconciles_before_new_issue(self):
        with tempfile.TemporaryDirectory() as path:
            legacy = self.record(1)
            root = Path(path)
            (root / "issuance.json").write_text(json.dumps(legacy.document()))
            (root / "issuance.json").chmod(0o600)
            (root / "issuance.anchor").write_text(
                json.dumps({"nonce": legacy.nonce, "state": "active"})
            )
            (root / "issuance.anchor").chmod(0o600)
            with M.Journal(path) as journal:
                api = FakeAPI()
                api.journal = journal
                api.data["legacy"] = self.accessor(legacy.metadata())
                self.assertEqual(
                    "reconciled", M.run_issuance(api, journal, revision=REV)
                )
                self.assertEqual(["legacy"], api.destroyed)
                self.assertNotIn("issue", api.calls)
                self.assertIsNone(journal.load())

    def test_interrupted_complete_witness_finishes_both_versions(self):
        for version in (1, 2):
            with self.subTest(version=version), tempfile.TemporaryDirectory() as path:
                record = self.record(version)
                root = Path(path)
                (root / "issuance.json").write_text(json.dumps(record.document()))
                (root / "issuance.json").chmod(0o600)
                anchor = json.dumps(record.anchor("complete")).encode()
                (root / "issuance.anchor").write_bytes(anchor)
                (root / "issuance.anchor").chmod(0o600)
                with M.Journal(path) as journal:
                    self.assertIsNone(journal.load())
                self.assertFalse((root / "issuance.json").exists())
                self.assertEqual(anchor, (root / "issuance.anchor").read_bytes())

    def test_legacy_recovery_generation_save_stays_unversioned(self):
        class CapturingJournal(M.Journal):
            def __init__(self, directory):
                super().__init__(directory)
                self.saved = []

            def save(self, record):
                self.saved.append(record.document())
                super().save(record)

        with tempfile.TemporaryDirectory() as path, CapturingJournal(path) as journal:
            legacy = M.Record(
                "1" * 32,
                M.utc(WHEN),
                M.ROLE,
                REV,
                M.MANIFEST,
                state="delivered",
            )
            journal.save(legacy)
            api = FakeAPI()
            api.journal = journal
            api.running = True
            self.assertEqual("reconciled", M.run_issuance(api, journal, revision=REV))
            self.assertEqual(2, len(journal.saved))
            self.assertNotIn("schema_version", journal.saved[-1])
            self.assertNotIn("issuance_id", journal.saved[-1])
            self.assertEqual(api.generation, journal.saved[-1]["agent_started_at"])

    def test_version_two_response_loss_restarts_without_second_issue(self):
        with tempfile.TemporaryDirectory() as path, M.Journal(path) as journal:
            api = FakeAPI("kill")
            api.journal = journal
            with self.assertRaises(SystemExit):
                M.run_issuance(
                    api,
                    journal,
                    revision=REV,
                    clock=lambda: WHEN,
                    nonce=lambda _: "1" * 32,
                )
            active = journal.load()
            self.assertEqual(2, active.schema_version)
            self.assertEqual(active.issuance_id, active.nonce)
            self.assertEqual(
                active.metadata(), api.data["synthetic-accessor"]["metadata"]
            )
            api.failure = None
            self.assertEqual("reconciled", M.run_issuance(api, journal, revision=REV))
            self.assertEqual(1, api.calls.count("issue"))
            self.assertEqual(["synthetic-accessor"], api.destroyed)

    def test_malformed_or_mixed_journals_block_without_mutation(self):
        legacy = self.record(1)
        current = self.record(2)
        cases = {
            "v1-record-v2-anchor": (legacy.document(), current.anchor("active")),
            "v2-record-v1-anchor": (current.document(), legacy.anchor("active")),
            "v2-alias-mismatch": (
                {**current.document(), "issuance_id": "2" * 32},
                current.anchor("active"),
            ),
            "explicit-v1-version": (
                {**legacy.document(), "schema_version": 1},
                legacy.anchor("active"),
            ),
            "v1-missing-field": (
                {k: v for k, v in legacy.document().items() if k != "agent_started_at"},
                legacy.anchor("active"),
            ),
            "v2-string-version": (
                {**current.document(), "schema_version": "2"},
                current.anchor("active"),
            ),
            "v2-boolean-version": (
                {**current.document(), "schema_version": True},
                current.anchor("active"),
            ),
            "v2-unknown-version": (
                {**current.document(), "schema_version": 3},
                current.anchor("active"),
            ),
            "numeric-complete-anchor": (
                None,
                {"nonce": int("1" * 32), "state": "complete"},
            ),
        }
        for case, (document, anchor) in cases.items():
            with self.subTest(case=case), tempfile.TemporaryDirectory() as path:
                root = Path(path)
                if document is not None:
                    (root / "issuance.json").write_text(json.dumps(document))
                    (root / "issuance.json").chmod(0o600)
                (root / "issuance.anchor").write_text(json.dumps(anchor))
                (root / "issuance.anchor").chmod(0o600)
                before = {item.name: item.read_bytes() for item in root.iterdir()}
                with M.Journal(path) as journal, self.assertRaises(M.Blocked):
                    journal.load()
                self.assertEqual(
                    before,
                    {
                        item.name: item.read_bytes()
                        for item in root.iterdir()
                        if item.name != "issuance.lock"
                    },
                )

    def test_repeated_json_fields_block_and_preserve_bytes(self):
        current = self.record(2)
        needle = f'"issuance_id": "{current.nonce}"'
        repeated = json.dumps(current.document()).replace(
            needle, f"{needle}, {needle}", 1
        )
        with tempfile.TemporaryDirectory() as path:
            root = Path(path)
            (root / "issuance.json").write_text(repeated)
            (root / "issuance.json").chmod(0o600)
            (root / "issuance.anchor").write_text(json.dumps(current.anchor("active")))
            (root / "issuance.anchor").chmod(0o600)
            before = (root / "issuance.json").read_bytes()
            with M.Journal(path) as journal, self.assertRaises(M.Blocked):
                journal.load()
            self.assertEqual(before, (root / "issuance.json").read_bytes())

    def test_accessor_identity_is_version_bound_and_alias_conflicts_block(self):
        legacy = self.record(1)
        current = self.record(2)
        other_legacy = self.record(1, "2" * 32)
        other_current = self.record(2, "2" * 32)
        accepted = (
            (legacy, legacy.metadata(), other_current.metadata()),
            (current, current.metadata(), other_legacy.metadata()),
        )
        for record, ours, unrelated in accepted:
            with self.subTest(version=record.schema_version):
                api = FakeAPI()
                api.data = {
                    "ours": self.accessor(ours),
                    "unrelated": self.accessor(unrelated),
                }
                self.assertEqual(["ours"], M.matching_accessors(api, record))

        invalid = {
            "v1-target-v2-metadata": (legacy, current.metadata()),
            "v2-target-v1-metadata": (current, legacy.metadata()),
            "v2-missing-id": (
                current,
                {k: v for k, v in current.metadata().items() if k != "issuance_id"},
            ),
            "v2-missing-version": (
                current,
                {k: v for k, v in current.metadata().items() if k != "issuance_schema"},
            ),
            "v2-conflicting-id": (
                current,
                {**current.metadata(), "issuance_id": "2" * 32},
            ),
            "v2-conflicting-legacy-alias": (
                current,
                {**current.metadata(), "sec01_nonce": "2" * 32},
            ),
            "v2-unknown-version": (
                current,
                {**current.metadata(), "issuance_schema": "3"},
            ),
        }
        for case, (record, metadata) in invalid.items():
            with self.subTest(case=case):
                api = FakeAPI()
                api.data["target"] = self.accessor(metadata)
                with self.assertRaises(M.Blocked):
                    M.matching_accessors(api, record)
                self.assertEqual([], api.destroyed)

    def test_duplicate_targets_block_before_destroying_or_rewriting(self):
        current = self.record(2)
        cases = {
            "same-version": (current.metadata(), current.metadata()),
            "cross-version": (current.metadata(), self.record(1).metadata()),
        }
        for case, metadata in cases.items():
            with self.subTest(case=case), tempfile.TemporaryDirectory() as path:
                with M.Journal(path) as journal:
                    journal.save(current)
                    root = Path(path)
                    before = {
                        name: (root / name).read_bytes()
                        for name in ("issuance.json", "issuance.anchor")
                    }
                    api = FakeAPI()
                    api.data = {
                        str(index): self.accessor(document)
                        for index, document in enumerate(metadata)
                    }
                    with self.assertRaises(M.Blocked):
                        M.reconcile(api, journal, current)
                    self.assertEqual([], api.destroyed)
                    self.assertEqual(
                        before,
                        {name: (root / name).read_bytes() for name in before},
                    )


class RuntimeReceiptTests(unittest.TestCase):
    def test_wrong_revision_or_tampered_snapshot_refused_before_token_read(self):
        import hashlib
        import io

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            helper = root / "renderer-issuance.py"
            wrapper = root / "issue-renderer-secret-id.sh"
            request = root / "renderer-request.sh"
            request.write_text('printf "{}"')
            request.chmod(0o400)
            helper.write_text("approved helper")
            wrapper.write_text("approved wrapper")
            helper.chmod(0o400)
            wrapper.chmod(0o500)
            receipt = root / "source-receipt.json"

            def write_receipt():
                receipt.chmod(0o600) if receipt.exists() else None
                receipt.write_text(
                    json.dumps(
                        {
                            "source_revision": REV,
                            "sha256": {
                                p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                for p in (helper, wrapper, request)
                            },
                        }
                    )
                )
                receipt.chmod(0o400)

            write_receipt()
            with patch.object(M, "__file__", str(helper)):
                held = M.validate_receipt(REV)
                for replace_peer in (False, True):
                    request.chmod(0o600)
                    if replace_peer:
                        request.unlink()
                    request.write_text("exit 99")
                    api = M.DockerAPI(
                        "server",
                        "volume",
                        "agent",
                        "issuer",
                        "cleanup",
                        request_script=held,
                    )

                    def execute(argv, **kwargs):
                        return subprocess.run(
                            argv[4:],
                            input=kwargs["payload"],
                            capture_output=True,
                            check=True,
                        ).stdout

                    with patch.object(api, "command", side_effect=execute):
                        self.assertEqual(
                            {}, api.request("read", "auth/token/lookup-self")
                        )
                request.write_text('printf "{}"')
                request.chmod(0o400)
                stdin = io.StringIO("synthetic-issuer\nsynthetic-cleanup\n")
                args = ["server", "volume", M.IMAGE, "agent", directory, "b" * 40]
                with patch.object(M.sys, "stdin", stdin), self.assertRaises(M.Blocked):
                    M.main(args)
                self.assertEqual(0, stdin.tell())
                helper.chmod(0o600)
                helper.write_text("tampered helper")
                helper.chmod(0o400)
                with self.assertRaises(M.Blocked):
                    M.validate_receipt(REV)
                write_receipt()
                receipt.chmod(0o600)
                with self.assertRaises(M.Blocked):
                    M.validate_receipt(REV)
                receipt.unlink()
                receipt.symlink_to(wrapper)
                with self.assertRaises(M.Blocked):
                    M.validate_receipt(REV)


class TransportTests(unittest.TestCase):
    def test_tokens_metadata_and_accessors_never_appear_in_argv(self):
        api = M.DockerAPI(
            "server",
            "volume",
            "agent",
            "synthetic-issuer",
            "synthetic-cleanup",
            request_script=":",
        )
        responses = [
            json.dumps({"wrap_info": {"token": "synthetic-wrap"}}).encode(),
            b"",
            b"{}",
        ]
        observed = []

        def command(argv, **kwargs):
            observed.append((argv, kwargs.get("payload")))
            return responses.pop(0)

        with patch.object(api, "command", side_effect=command):
            api.issue({"nonce": "synthetic-nonce"})
            api.destroy("synthetic-accessor")
            api.lookup("synthetic-accessor")
        for argv, body in observed:
            for sensitive in (
                "synthetic-issuer",
                "synthetic-cleanup",
                "synthetic-accessor",
                "synthetic-nonce",
            ):
                self.assertNotIn(sensitive, " ".join(argv))
            self.assertIsInstance(body, bytes)

    def test_transport_failure_never_includes_original_stderr(self):
        response = subprocess.CompletedProcess(
            [], 2, b"", b"synthetic-sensitive-server-error"
        )
        with patch.object(M.subprocess, "run", return_value=response):
            with self.assertRaises(M.Blocked) as caught:
                M.DockerAPI.command(["docker"])
            self.assertEqual("", str(caught.exception))

    def test_empty_list_not_confused_with_permission_failure(self):
        responses = [
            subprocess.CompletedProcess(
                [], 2, b"", ("No value found at " + M.PREFIX + "/secret-id\n").encode()
            ),
            subprocess.CompletedProcess(
                [], 2, b"", b"Error making API request: permission denied"
            ),
        ]
        with patch.object(M.subprocess, "run", side_effect=responses):
            value = M.DockerAPI.command(
                ["docker"], empty_list_path=M.PREFIX + "/secret-id"
            )
            self.assertEqual([], json.loads(value)["data"]["keys"])
            with self.assertRaises(M.Blocked):
                M.DockerAPI.command(["docker"], empty_list_path=M.PREFIX + "/secret-id")

    def test_native_json_empty_list_sentinel_is_not_permission_success(self):
        for stderr in (b"", b"permission denied"):
            response = subprocess.CompletedProcess([], 2, b"{}\n", stderr)
            with patch.object(M.subprocess, "run", return_value=response):
                if stderr:
                    with self.assertRaises(M.Blocked):
                        M.DockerAPI.command(
                            ["docker"], empty_list_path=M.PREFIX + "/secret-id"
                        )
                else:
                    value = M.DockerAPI.command(
                        ["docker"], empty_list_path=M.PREFIX + "/secret-id"
                    )
                    self.assertEqual([], json.loads(value)["data"]["keys"])
        for raw in (b"null", b"[]", b'{"errors":[]}', b'{"unexpected":true}'):
            response = subprocess.CompletedProcess([], 2, raw, b"")
            with patch.object(M.subprocess, "run", return_value=response):
                with self.assertRaises(M.Blocked):
                    M.DockerAPI.command(
                        ["docker"], empty_list_path=M.PREFIX + "/secret-id"
                    )

    def test_native_cli_accessor_array_validated_without_api_envelope(self):
        api = M.DockerAPI(
            "server", "volume", "agent", "issuer", "cleanup", request_script=":"
        )
        with patch.object(api, "request", return_value=["synthetic-accessor"]):
            self.assertEqual(["synthetic-accessor"], api.accessors())
        for response in (
            ["same", "same"],
            ["../escape"],
            [3],
            {"unexpected": []},
            None,
        ):
            with patch.object(api, "request", return_value=response):
                with self.assertRaises(M.Blocked):
                    api.accessors()

    def test_exact_cleanup_policy_and_short_roles(self):
        policy = (BASE / "config/policies/renderer-cleanup.hcl").read_text()
        self.assertNotIn("*", policy)
        resource = policy.split("# Self-identity")[0]
        self.assertNotIn('"read"', resource)
        self.assertNotIn('"create"', policy)
        self.assertNotIn("secret/data", policy)
        self.assertEqual(3, policy.count('path "' + M.PREFIX))
        for name in ("renderer-issuer", "renderer-cleanup"):
            role = json.loads(
                (BASE / "config" / (name + "-token-role.json")).read_text()
            )
            self.assertEqual([name], role["allowed_policies"])
            self.assertFalse(role["renewable"])
            self.assertTrue(role["token_no_default_policy"])
            self.assertEqual("5m", role["token_explicit_max_ttl"])


if __name__ == "__main__":
    unittest.main()
