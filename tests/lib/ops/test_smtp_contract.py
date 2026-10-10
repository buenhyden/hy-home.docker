"""Synthetic SMTP source and retirement regressions; unittest CI compatible."""

import io
import json
import os
import socket
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import yaml

from scripts.lib.ops import smtp_contract as module
from scripts.lib.ops.smtp_contract import (
    ALIAS_ROW,
    CANONICAL_PATH,
    LOCK_PATH,
    OLD_PATH,
    ContractError,
    main,
    metadata_retired,
    retire,
    retirement_lock,
    root_identity,
    source_hashes,
    summarize,
    unify,
)


def model():
    return {
        "secrets": {
            "smtp_password": {"file": "./" + CANONICAL_PATH},
            "supabase_smtp_password": {"file": "./" + OLD_PATH},
        },
        "services": {
            "auth": {
                "secrets": ["supabase_smtp_password", "other"],
                "environment": {
                    "GOTRUE_SMTP_PASS_FILE": "/run/secrets/supabase_smtp_password"
                },
            },
            "n8n": {"secrets": ["smtp_password"]},
        },
    }


def tree(tmp_path):
    for relative in (CANONICAL_PATH, OLD_PATH):
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"synthetic-password\n")
    metadata = tmp_path / "secrets/SENSITIVE_ENV_VARS.md"
    metadata.write_bytes(
        b"prefix unchanged\r\n"
        + b"| **COMM-002** | `X` | `PW` | `synthetic-password` | `-` | `"
        + CANONICAL_PATH.encode()
        + b"` | date | canonical |\r\n"
        + b"| **COMM-003** | `X` | `PW` | `synthetic-password` | `-` | `"
        + OLD_PATH.encode()
        + b"` | date | retired |\r\n"
        + b"| **OTHER-001** | `X` | `PW` | `synthetic-untouched` | `-` | `secrets/other.txt` | date | untouched |\r\n"
    )
    return tmp_path


def apply(tree, **kwargs):
    return retire(
        tree,
        apply=True,
        proof="synthetic-proof",
        verifier=lambda root, proof: None,
        **kwargs,
    )


def public_source(tree):

    root = unify(model())
    root["include"] = ["infra/auth.yml"]
    root.pop("services")
    (tree / "docker-compose.yml").write_text(yaml.safe_dump(root))
    (tree / "infra").mkdir()
    (tree / "infra/auth.yml").write_text(
        yaml.safe_dump({"services": unify(model())["services"]})
    )
    return tree


class SMTPContractTests(unittest.TestCase):
    def _prepare(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.tree = tree(self.root)
        public_source(self.tree)
        self.monkeypatch = self
        self.capture = self
        self._output = io.StringIO()
        self.setattr(__import__("sys"), "stdout", self._output)

    def setattr(self, target, name, value):
        replacement = patch.object(target, name, value)
        replacement.start()
        self.addCleanup(replacement.stop)

    def readouterr(self):
        text = self._output.getvalue()
        self._output.seek(0)
        self._output.truncate(0)
        return SimpleNamespace(out=text)

    def test_unify_preserves_mount_and_input(self):
        self._prepare()
        original = model()
        untouched = deepcopy(original)
        output = unify(original)
        assert list(output["secrets"]) == ["smtp_password"]
        assert output["services"]["auth"]["secrets"][0] == {
            "source": "smtp_password",
            "target": "supabase_smtp_password",
        }
        assert original == untouched
        assert unify(output) == output

    def test_duplicate_targets_rejected(self):
        self._prepare()
        original = model()
        original["services"]["auth"]["secrets"].append(
            {"source": "smtp_password", "target": "supabase_smtp_password"}
        )
        with self.assertRaises(ContractError):
            unify(original)

    def test_long_syntax_preserves_fields(self):
        for item, expected in [
            (
                {"source": "supabase_smtp_password", "target": "custom", "mode": 288},
                {"source": "smtp_password", "target": "custom", "mode": 288},
            ),
            (
                {"source": "supabase_smtp_password"},
                {"source": "smtp_password", "target": "supabase_smtp_password"},
            ),
        ]:
            with self.subTest():
                self._prepare()
                original = model()
                original["services"]["auth"]["secrets"][0] = item
                assert unify(original)["services"]["auth"]["secrets"][0] == expected

    def test_model_drift_rejected(self):
        for mutation in [
            lambda m: m["secrets"].pop("smtp_password"),
            lambda m: m["secrets"]["smtp_password"].update(file="wrong"),
            lambda m: m["secrets"]["supabase_smtp_password"].update(file="wrong"),
            lambda m: m.update(secrets=[]),
            lambda m: m.update(services=[]),
            lambda m: m["services"].update(auth=42),
            lambda m: m["services"]["auth"].update(secrets=[42]),
            lambda m: m["services"]["auth"].update(secrets=[{}]),
            lambda m: m["services"]["auth"].update(
                secrets=[{"source": "x", "target": 42}]
            ),
            lambda m: m["services"]["auth"].update(secrets=None),
            lambda m: m["services"]["auth"].update(
                secrets=["supabase_smtp_password", "smtp_password"]
            ),
        ]:
            with self.subTest():
                self._prepare()
                original = model()
                mutation(original)
                with self.assertRaises(ContractError):
                    unify(original)

    def test_summary_is_value_free(self):
        self._prepare()
        original = model()
        original["services"]["auth"]["environment"]["X"] = "synthetic-private-probe"
        assert "synthetic-private-probe" not in json.dumps(summarize(original))
        original["services"]["other"] = {}
        assert "other" not in summarize(original)["changed_services"]

    def test_duplicate_definition_path_rejected(self):
        for relative in (CANONICAL_PATH, OLD_PATH):
            with self.subTest(relative=relative):
                original = model()
                original["secrets"]["unexpected_duplicate"] = {"file": relative}
                with self.assertRaises(ContractError):
                    unify(original)

    def test_retirement_equal_and_idempotent_preserves_bytes(self):
        self._prepare()
        metadata = self.tree / "secrets/SENSITIVE_ENV_VARS.md"
        original = metadata.read_bytes()
        canonical = (self.tree / CANONICAL_PATH).read_bytes()
        status, summary = retire(self.tree)
        assert status == 1 and summary == {
            "status": "pending",
            "equal": True,
            "applied": False,
        }
        assert metadata.read_bytes() == original
        assert apply(self.tree) == (
            0,
            {"status": "retired", "equal": True, "applied": True},
        )
        assert not (self.tree / OLD_PATH).exists()
        assert not (self.tree / OLD_PATH).parent.exists()
        assert (self.tree / CANONICAL_PATH).read_bytes() == canonical
        assert metadata.read_bytes() == metadata_retired(original)
        assert metadata.stat().st_mode & 511 == 384
        assert ALIAS_ROW in metadata.read_bytes()
        assert b"synthetic-untouched" in metadata.read_bytes()
        assert not list((self.tree / "secrets").glob(".smtp-retirement-*"))
        assert retire(self.tree) == (
            0,
            {"status": "already_retired", "equal": None, "applied": False},
        )

    def test_apply_needs_receipt(self):
        self._prepare()
        with self.assertRaisesRegex(ContractError, "audit_receipt_required"):
            retire(self.tree, apply=True)
        assert (self.tree / OLD_PATH).exists()

    def test_unsafe_private_input_rejected(self):
        for unsafe in [
            "mismatch",
            "empty",
            "symlink",
            "parent_symlink",
            "hardlink",
            "fifo",
            "missing_canonical",
            "missing_metadata",
        ]:
            with self.subTest():
                self._prepare()
                old = self.tree / OLD_PATH
                canonical = self.tree / CANONICAL_PATH
                if unsafe == "mismatch":
                    old.write_bytes(b"synthetic-mismatch")
                elif unsafe == "empty":
                    canonical.write_bytes(b"")
                elif unsafe == "symlink":
                    old.unlink()
                    old.symlink_to(canonical)
                elif unsafe == "parent_symlink":
                    moved = old.parent.with_name("moved")
                    old.parent.rename(moved)
                    old.parent.symlink_to(moved, target_is_directory=True)
                elif unsafe == "hardlink":
                    old.unlink()
                    os.link(canonical, old)
                elif unsafe == "fifo":
                    old.unlink()
                    os.mkfifo(old)
                elif unsafe == "missing_canonical":
                    canonical.unlink()
                else:
                    (self.tree / "secrets/SENSITIVE_ENV_VARS.md").unlink()
                with self.assertRaises((ContractError, OSError)):
                    apply(self.tree)

    def test_missing_old_retires_metadata_and_keeps_unknown_entry(self):
        self._prepare()
        old = self.tree / OLD_PATH
        old.unlink()
        extra = old.parent / "preserved.txt"
        extra.write_bytes(b"synthetic-unknown")
        assert apply(self.tree)[0] == 0
        assert extra.read_bytes() == b"synthetic-unknown"

    def test_concurrent_change_preserves_duplicate(self):
        for phase in ["before", "after_metadata"]:
            with self.subTest():
                self._prepare()
                old = self.tree / OLD_PATH
                metadata = self.tree / "secrets/SENSITIVE_ENV_VARS.md"
                original = metadata.read_bytes()
                if phase == "before":

                    def hook(old=old):
                        old.write_bytes(b"synthetic-concurrent-change")

                    with self.assertRaisesRegex(
                        ContractError, "concurrent_file_change"
                    ):
                        apply(self.tree, before_commit=hook)
                    assert metadata.read_bytes() == original
                else:
                    rename = module._rename_noreplace

                    def race(parent, source, target, old=old, rename=rename):
                        rename(parent, source, target)
                        if target == "SENSITIVE_ENV_VARS.md":
                            old.write_bytes(b"synthetic-concurrent-change")

                    self.setattr(module, "_rename_noreplace", race)
                    with self.assertRaisesRegex(
                        ContractError, "concurrent_file_change"
                    ):
                        apply(self.tree)
                assert old.read_bytes() == b"synthetic-concurrent-change"
                assert (
                    self.tree / CANONICAL_PATH
                ).read_bytes() == b"synthetic-password\n"

    def test_metadata_failure_keeps_duplicate_and_cleans_temporary(self):
        self._prepare()

        def fail(*args, **kwargs):
            raise OSError("synthetic-failure")

        self.setattr(module, "_rename_noreplace", fail)
        with self.assertRaises(OSError):
            apply(self.tree)
        assert (self.tree / OLD_PATH).exists()
        assert not list((self.tree / "secrets").glob(".smtp-retirement-*"))

    def test_metadata_drift_rejected(self):
        for data in [
            b"no canonical\n",
            b"| COMM-002 | x | x | x | x | wrong | x | x |\n",
            b"| COMM-003 | WRONG-002 |\n",
            b"| COMM-003 | COMM-002 | path |\n",
        ]:
            with self.subTest():
                self._prepare()
                with self.assertRaises(ContractError):
                    metadata_retired(data)

    def test_source_mapping_and_proof(self):
        self._prepare()
        public_source = self.tree
        tmp_path = self.root
        hashes = module.source_hashes(public_source)
        assert set(hashes) == {"docker-compose.yml", "infra/auth.yml"}
        proof = tmp_path / "proof.json"
        receipt = {
            "host": socket.gethostname(),
            "git_sha": "synthetic-sha",
            "source_sha256": hashes,
            "old_mount_consumers": [],
            "job_backup_external_verified": True,
            "canonical_restore_mapping_verified": True,
            "consumer_creation_quiesced": True,
            "source_private_mutation_quiesced": True,
            "root_identity": {
                "st_dev": public_source.stat().st_dev,
                "st_ino": public_source.stat().st_ino,
            },
        }
        proof.write_text(json.dumps(receipt))
        self.setattr(
            module,
            "_run",
            lambda argv, root=None: b"synthetic-sha\n" if argv[0] == "git" else b"",
        )
        module.verify_proof(public_source, proof)
        for field in receipt:
            changed = dict(receipt)
            changed[field] = None
            proof.write_text(json.dumps(changed))
            with self.assertRaisesRegex(ContractError, "audit_receipt_stale"):
                module.verify_proof(public_source, proof)

    def test_live_mount_verification(self):
        for mount, rejected in [
            (
                {
                    "Type": "bind",
                    "Source": "OLD",
                    "Destination": "/run/secrets/x",
                    "RW": False,
                },
                True,
            ),
            (
                {"Type": "bind", "Source": "PARENT", "Destination": "/x", "RW": False},
                True,
            ),
            (
                {
                    "Type": "bind",
                    "Source": "SECRETS",
                    "Destination": "/src/host/secrets",
                    "RW": False,
                },
                False,
            ),
            (
                {
                    "Type": "bind",
                    "Source": "SECRETS",
                    "Destination": "/src/host/secrets",
                    "RW": True,
                },
                True,
            ),
            (
                {"Type": "volume", "Source": "OLD", "Destination": "/x", "RW": False},
                False,
            ),
            (
                {
                    "Type": "bind",
                    "Source": "/unrelated",
                    "Destination": "/x",
                    "RW": False,
                },
                False,
            ),
        ]:
            with self.subTest():
                self._prepare()
                public_source = self.tree
                proof = public_source / "proof.json"
                proof.write_text(
                    json.dumps(
                        {
                            "host": socket.gethostname(),
                            "git_sha": "sha",
                            "source_sha256": module.source_hashes(public_source),
                            "old_mount_consumers": [],
                            "job_backup_external_verified": True,
                            "canonical_restore_mapping_verified": True,
                            "consumer_creation_quiesced": True,
                            "source_private_mutation_quiesced": True,
                            "root_identity": {
                                "st_dev": public_source.stat().st_dev,
                                "st_ino": public_source.stat().st_ino,
                            },
                        }
                    )
                )
                mounted = dict(mount)
                mounted["Source"] = {
                    "OLD": str(public_source / OLD_PATH),
                    "PARENT": str((public_source / OLD_PATH).parent),
                    "SECRETS": str(public_source / "secrets"),
                }.get(mount["Source"], mount["Source"])

                def command(argv, root=None, mounted=mounted):
                    if argv[0] == "git":
                        return b"sha"
                    if argv[1] == "ps":
                        return b"synthetic-container"
                    return json.dumps([mounted]).encode()

                self.setattr(module, "_run", command)
                if rejected:
                    with self.assertRaises(ContractError):
                        module.verify_proof(public_source, proof)
                else:
                    module.verify_proof(public_source, proof)

    def test_source_cutover_guard(self):
        for change in [
            "root_old",
            "include_old",
            "missing_alias",
            "old_path",
            "include_symlink",
            "include_escape",
            "invalid_document",
            "bad_include",
        ]:
            with self.subTest():
                self._prepare()
                public_source = self.tree
                root_path = public_source / "docker-compose.yml"
                include = public_source / "infra/auth.yml"
                root = yaml.safe_load(root_path.read_text())
                if change == "root_old":
                    root["secrets"]["supabase_smtp_password"] = {"file": OLD_PATH}
                elif change == "include_old":
                    include.write_text(
                        yaml.safe_dump(
                            {"secrets": {"supabase_smtp_password": {"file": OLD_PATH}}}
                        )
                    )
                elif change == "missing_alias":
                    include.write_text("services: {}\n")
                elif change == "old_path":
                    include.write_text(yaml.safe_dump({"x-legacy": OLD_PATH}))
                elif change == "include_symlink":
                    include.unlink()
                    include.symlink_to(root_path)
                elif change == "include_escape":
                    root["include"] = ["../escape.yml"]
                elif change == "bad_include":
                    root["include"] = [{}]
                else:
                    include.write_text("[]\n")
                root_path.write_text(yaml.safe_dump(root))
                with self.assertRaises((ContractError, ValueError)):
                    source_hashes(public_source)

    def test_service_less_include_old_path_is_rejected(self):
        self._prepare()
        rootfile = self.root / "docker-compose.yml"
        document = yaml.safe_load(rootfile.read_text())
        document["include"].append("infra/legacy.yml")
        rootfile.write_text(yaml.safe_dump(document))
        (self.root / "infra/legacy.yml").write_text(
            yaml.safe_dump({"x-legacy": OLD_PATH})
        )
        with self.assertRaises(ContractError):
            source_hashes(self.root)

    def test_final_name_race_is_preserved(self):
        self._prepare()
        old = self.tree / OLD_PATH
        original_unchanged = module._unchanged
        checks = 0

        def race(parent, name, snapshot):
            nonlocal checks
            original_unchanged(parent, name, snapshot)
            if name == old.name:
                checks += 1
                if checks == 3:
                    os.rename(old, old.with_suffix(".saved"))
                    old.write_bytes(b"synthetic-raced-new-file")

        self.setattr(module, "_unchanged", race)
        with self.assertRaises(ContractError):
            apply(self.tree)
        assert old.read_bytes() == b"synthetic-raced-new-file"
        assert old.with_suffix(".saved").read_bytes() == b"synthetic-password\n"

    def test_mounts_rechecked_before_and_after_deletion(self):
        self._prepare()
        checks = []

        def verifier(root, proof):
            checks.append((self.tree / OLD_PATH).exists())

        retire(self.tree, apply=True, proof="synthetic-proof", verifier=verifier)
        assert checks == [True, True, False]

    def test_mount_scan_race_fails_before_or_after_deletion(self):
        for failure in (2, 3):
            with self.subTest(failure=failure):
                self._prepare()
                scans = 0

                def verifier(root, proof, failure=failure):
                    nonlocal scans
                    scans += 1
                    if scans == failure:
                        raise ContractError("old_runtime_mount")

                with self.assertRaisesRegex(ContractError, "old_runtime_mount"):
                    retire(
                        self.tree,
                        apply=True,
                        proof="synthetic-proof",
                        verifier=verifier,
                    )
                assert (self.tree / OLD_PATH).exists() is (failure == 2)
                assert (
                    self.tree / CANONICAL_PATH
                ).read_bytes() == b"synthetic-password\n"

    def test_quarantine_restore_never_overwrites_new_original(self):
        self._prepare()
        old = self.tree / OLD_PATH
        original_unchanged = module._unchanged

        def conflict(parent, name, snapshot):
            if name.startswith(".smtp-quarantine-"):
                old.write_bytes(b"synthetic-new-original")
                raise ContractError("concurrent_file_change")
            original_unchanged(parent, name, snapshot)

        self.setattr(module, "_unchanged", conflict)
        with self.assertRaisesRegex(ContractError, "quarantine_restore_conflict"):
            apply(self.tree)
        assert old.read_bytes() == b"synthetic-new-original"
        preserved = list(old.parent.glob(".smtp-quarantine-*"))
        assert len(preserved) == 1
        assert preserved[0].read_bytes() == b"synthetic-password\n"

    def test_quarantine_destination_collision_never_overwrites(self):
        self._prepare()
        old = self.tree / OLD_PATH
        existing = old.parent / ".smtp-quarantine-fixed"
        existing.write_bytes(b"synthetic-unrelated")
        self.setattr(module.secrets, "token_hex", lambda size: "fixed")
        with self.assertRaises(OSError):
            apply(self.tree)
        assert existing.read_bytes() == b"synthetic-unrelated"
        assert old.read_bytes() == b"synthetic-password\n"

    def test_directory_identity_swap_is_preserved(self):
        self._prepare()
        old = (self.tree / OLD_PATH).parent
        fd = os.open(old, os.O_RDONLY | os.O_DIRECTORY)
        parent = os.open(old.parent, os.O_RDONLY | os.O_DIRECTORY)
        self.addCleanup(os.close, fd)
        self.addCleanup(os.close, parent)
        old.rename(old.with_name("preserved-directory"))
        old.mkdir()
        with self.assertRaisesRegex(ContractError, "concurrent_directory_change"):
            module._remove_empty_directory(parent, old.name, fd)
        assert old.is_dir()
        assert (
            old.with_name("preserved-directory") / "supabase_smtp_password.txt"
        ).exists()

    def test_atomic_rename_unavailable_preserves_original(self):
        self._prepare()
        self.setattr(module.ctypes, "CDLL", lambda *args, **kwargs: object())
        with self.assertRaisesRegex(ContractError, "atomic_restore_unavailable"):
            apply(self.tree)
        assert (self.tree / OLD_PATH).read_bytes() == b"synthetic-password\n"

    def test_old_name_created_after_quarantine_is_preserved_and_unsafe(self):
        self._prepare()
        old = self.tree / OLD_PATH
        rename = module._rename_noreplace

        def create_after_move(parent, source, target):
            rename(parent, source, target)
            if source == old.name:
                old.write_bytes(b"synthetic-recreated-old")

        self.setattr(module, "_rename_noreplace", create_after_move)
        with self.assertRaises(ContractError):
            apply(self.tree)
        assert old.read_bytes() == b"synthetic-recreated-old"

    def test_metadata_replacement_after_commit_is_unsafe(self):
        self._prepare()
        metadata = self.tree / "secrets/SENSITIVE_ENV_VARS.md"
        rename = module._rename_noreplace

        def overwrite_after_commit(parent, source, target):
            rename(parent, source, target)
            if source.startswith(".smtp-retirement-"):
                metadata.write_bytes(b"synthetic-raced-metadata")

        self.setattr(module, "_rename_noreplace", overwrite_after_commit)
        with self.assertRaises(ContractError):
            apply(self.tree)
        assert metadata.read_bytes() == b"synthetic-raced-metadata"

    def test_cli_failure_after_mutation_reports_partial_truthfully(self):
        for failure in (2, 3):
            with self.subTest(failure=failure):
                self._prepare()
                original_retire = module.retire
                scans = 0

                def verifier(root, proof, failure=failure):
                    nonlocal scans
                    scans += 1
                    if scans == failure:
                        raise ContractError("old_runtime_mount")

                def synthetic_retire(
                    *args, original_retire=original_retire, verifier=verifier, **kwargs
                ):
                    return original_retire(*args, verifier=verifier, **kwargs)

                self.setattr(module, "retire", synthetic_retire)
                result = module.main(
                    ["--retire", "--root", str(self.tree), "--proof", "synthetic-proof"]
                )
                assert result == 2
                assert json.loads(self.readouterr().out) == {
                    "status": "unsafe_after_mutation",
                    "applied": True,
                    "completed": False,
                }
                assert (self.tree / OLD_PATH).exists() is (failure == 2)

    def test_every_include_rejects_canonical_redefinitions(self):
        for name, relative in (
            ("smtp_password", CANONICAL_PATH),
            ("alias", CANONICAL_PATH),
            ("alias", OLD_PATH),
            ("alias", "../" + CANONICAL_PATH),
            ("alias", "../" + OLD_PATH),
        ):
            with self.subTest(name=name, relative=relative):
                self._prepare()
                rootfile = self.root / "docker-compose.yml"
                document = yaml.safe_load(rootfile.read_text())
                document["include"].append("infra/redefinition.yml")
                rootfile.write_text(yaml.safe_dump(document))
                (self.root / "infra/redefinition.yml").write_text(
                    yaml.safe_dump({"secrets": {name: {"file": relative}}})
                )
                with self.assertRaises(ContractError):
                    source_hashes(self.root)

    def test_metadata_race_before_publication_is_preserved(self):
        self._prepare()
        metadata = self.tree / "secrets/SENSITIVE_ENV_VARS.md"
        rename = module._rename_noreplace
        raced = metadata.read_bytes().replace(
            b"synthetic-untouched", b"synthetic-concurrent-private-row"
        )

        def change_before_move(parent, source, target):
            if source == "SENSITIVE_ENV_VARS.md":
                metadata.write_bytes(raced)
            return rename(parent, source, target)

        self.setattr(module, "_rename_noreplace", change_before_move)
        with self.assertRaises(ContractError):
            apply(self.tree)
        assert metadata.read_bytes() == raced
        assert (self.tree / OLD_PATH).read_bytes() == b"synthetic-password\n"
        assert not list(metadata.parent.glob(".smtp-metadata-quarantine-*"))

    def test_readonly_check_does_not_create_lock(self):
        self._prepare()
        assert retire(self.tree)[0] == 1
        assert not (self.tree / LOCK_PATH).exists()

    def test_shared_lock_is_persistent_exclusive_and_identity_bound(self):
        self._prepare()
        identity = root_identity(self.tree)
        with retirement_lock(self.tree, identity) as actual:
            assert actual == identity
            with self.assertRaisesRegex(ContractError, "retirement_lock_busy"):
                with retirement_lock(self.tree, identity):
                    self.fail("lock must be exclusive")
            with self.assertRaisesRegex(ContractError, "retirement_lock_busy"):
                apply(self.tree)
        lock = self.tree / LOCK_PATH
        assert lock.is_file() and lock.stat().st_mode & 0o777 == 0o600
        with retirement_lock(self.tree, identity):
            pass
        with self.assertRaisesRegex(ContractError, "root_identity_mismatch"):
            with retirement_lock(
                self.tree, dict(identity, st_ino=identity["st_ino"] + 1)
            ):
                self.fail("wrong root identity must fail")

    def test_shared_lock_rejects_symlink_hardlink_and_wrong_mode(self):
        for unsafe in ("symlink", "hardlink", "mode"):
            with self.subTest(unsafe=unsafe):
                self._prepare()
                lock = self.tree / LOCK_PATH
                if unsafe == "symlink":
                    lock.symlink_to(self.tree / CANONICAL_PATH)
                elif unsafe == "hardlink":
                    os.link(self.tree / CANONICAL_PATH, lock)
                else:
                    lock.write_bytes(b"")
                    lock.chmod(0o644)
                with self.assertRaises((OSError, ContractError)):
                    with retirement_lock(self.tree):
                        self.fail("unsafe lock must fail")

    def test_metadata_create_race_preserves_both_private_records(self):
        self._prepare()
        metadata = self.tree / "secrets/SENSITIVE_ENV_VARS.md"
        original = metadata.read_bytes()
        rename = module._rename_noreplace

        def create_during_gap(parent, source, target):
            rename(parent, source, target)
            if source == "SENSITIVE_ENV_VARS.md":
                metadata.write_bytes(b"synthetic-new-private-record")

        self.setattr(module, "_rename_noreplace", create_during_gap)
        with self.assertRaisesRegex(ContractError, "metadata_restore_conflict"):
            apply(self.tree)
        assert metadata.read_bytes() == b"synthetic-new-private-record"
        displaced = list(metadata.parent.glob(".smtp-metadata-quarantine-*"))
        assert len(displaced) == 1 and displaced[0].read_bytes() == original
        assert not list(metadata.parent.glob(".smtp-retirement-*"))
        assert (self.tree / OLD_PATH).read_bytes() == b"synthetic-password\n"

    def test_cli_public_summary_and_unsafe_redaction(self):
        self._prepare()
        capsys = self.capture
        assert main(["--retire-check", "--root", str(self.tree)]) == 1
        assert "synthetic-password" not in capsys.readouterr().out
        (self.tree / OLD_PATH).write_bytes(b"synthetic-mismatch")
        assert main(["--retire", "--root", str(self.tree)]) == 2
        output = capsys.readouterr().out
        assert "synthetic" not in output
        assert '"unsafe"' in output


if __name__ == "__main__":
    unittest.main()
