"""Synthetic protected Raft snapshot tests; HOME and real credentials are excluded."""

from __future__ import annotations

import gzip
import hashlib
import http.server
import importlib.util
import io
import json
import os
import ssl
import stat
import subprocess
import sys
import tarfile
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "infra/03-security/openbao/scripts/protected-raft-snapshot.py"
PARENT = ROOT / "infra/03-security/openbao/scripts/protected-maintenance.py"
TOKEN = "synthetic-snapshot-token"
CLUSTER = "12345678-1234-1234-1234-123456789abc"
PERIOD = 720 * 60 * 60


def load_source():
    spec = importlib.util.spec_from_file_location("protected_raft_snapshot", SOURCE)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


S = load_source()


def lookup(**delta):
    value = {
        "policies": ["backup-snapshot"],
        "token_policies": ["backup-snapshot"],
        "identity_policies": [],
        "entity_id": "",
        "renewable": True,
        "orphan": True,
        "type": "service",
        "ttl": PERIOD,
        "creation_ttl": PERIOD,
        "period": PERIOD,
        "explicit_max_ttl": 0,
    }
    value.update(delta)
    return {"data": value}


def renewal(**delta):
    value = {
        "client_token": TOKEN,
        "policies": ["backup-snapshot"],
        "token_policies": ["backup-snapshot"],
        "renewable": True,
        "orphan": True,
        "token_type": "service",
        "lease_duration": PERIOD,
    }
    value.update(delta)
    return {"auth": value}


def seal(**delta):
    value = {
        "initialized": True,
        "sealed": False,
        "type": "shamir",
        "storage_type": "raft",
        "cluster_id": CLUSTER,
        "version": "2.6.2",
    }
    value.update(delta)
    return value


def native_meta(state=b"barrier-encrypted-state", **delta):
    value = {
        "Version": 1,
        "ID": "synthetic-snapshot",
        "Index": 42,
        "Term": 3,
        "Peers": None,
        "Configuration": {
            "Servers": [
                {
                    "Suffrage": 0,
                    "ID": "openbao-1",
                    "Address": "openbao-1:8201",
                }
            ]
        },
        "ConfigurationIndex": 41,
        "Size": len(state),
    }
    value.update(delta)
    return value


def raft_archive(
    *,
    names=None,
    state=b"barrier-encrypted-state",
    meta=None,
    meta_raw=None,
    corrupt_hash=False,
):
    metadata = native_meta(state) if meta is None else meta
    encoded_meta = json.dumps(metadata).encode() if meta_raw is None else meta_raw
    members = {
        "meta.json": encoded_meta,
        "state.bin": state,
        "SHA256SUMS": (
            f"{hashlib.sha256(encoded_meta).hexdigest()}  meta.json\n"
            f"{hashlib.sha256(state).hexdigest()}  state.bin\n"
        ).encode(),
        "SHA256SUMS.sealed": b"synthetic-sealed-hashes",
    }
    if corrupt_hash:
        checksum = members["SHA256SUMS"]
        members["SHA256SUMS"] = (b"0" if checksum[:1] != b"0" else b"1") + checksum[1:]
    if names is not None:
        members = {name: members.get(name, b"x") for name in names}
    output = io.BytesIO()
    # A zero gzip mtime keeps two calls byte-identical across a second boundary.
    with (
        gzip.GzipFile(fileobj=output, mode="wb", mtime=0) as compressed,
        tarfile.open(fileobj=compressed, mode="w") as archive,
    ):
        for name, body in members.items():
            info = tarfile.TarInfo(name)
            info.size = len(body)
            info.mode = 0o600
            info.mtime = 0
            archive.addfile(info, io.BytesIO(body))
    return output.getvalue()


class Response:
    def __init__(self, headers, *, status=200):
        self.status = status
        self._headers = headers

    def getheaders(self):
        return list(self._headers)


class ContractTests(unittest.TestCase):
    def test_verified_parent_source_is_loaded_from_exact_public_bytes(self):
        parent = S.load_parent()
        self.assertEqual(parent.HOST, "openbao.hy.home.arpa")
        self.assertEqual(
            hashlib.sha256(PARENT.read_bytes()).hexdigest(), S.PARENT_SHA256
        )

    def test_wrong_parent_hash_fails_before_execution(self):
        with mock.patch.object(S, "PARENT_SHA256", "0" * 64):
            with self.assertRaises(S.Blocked):
                S.load_parent()

    def test_parent_failures_are_translated_to_redacted_local_errors(self):
        parent = S.load_parent()
        with self.assertRaises(S.Blocked) as error:
            S._trusted(parent, "validate_secret", "not a secret with spaces")
        self.assertEqual(str(error.exception), "")

    def test_lookup_identity_is_exact(self):
        S.check_lookup(lookup())
        for delta in (
            {"policies": ["default", "backup-snapshot"]},
            {"token_policies": []},
            {"identity_policies": ["foreign"]},
            {"renewable": False},
            {"orphan": False},
            {"type": "batch"},
            {"ttl": 0},
            {"ttl": PERIOD + 1},
            {"period": PERIOD - 1},
            {"creation_ttl": 0},
            {"explicit_max_ttl": PERIOD},
        ):
            with self.subTest(delta=delta), self.assertRaises(S.Blocked):
                S.check_lookup(lookup(**delta))

    def test_lookup_accepts_the_real_shape_without_token_or_identity_policies(self):
        # 2.6.2 and 2.7.1 lookup-self omit both fields (observed 2026-10-22, W3 BLOCKED).
        response = lookup()
        del response["data"]["token_policies"], response["data"]["identity_policies"]
        S.check_lookup(response)
        for key, value in (("token_policies", None), ("identity_policies", None)):
            with self.subTest(key=key), self.assertRaises(S.Blocked):
                S.check_lookup(lookup(**{key: value}))

    def test_snapshot_lookup_requires_an_explicit_unlinked_entity(self):
        for value in (None, "foreign-entity", 0, False, [], {}):
            with self.subTest(value=value), self.assertRaises(S.Blocked):
                S.check_lookup(lookup(entity_id=value))
        response = lookup()
        del response["data"]["entity_id"]
        with self.assertRaises(S.Blocked):
            S.check_lookup(response)

    def test_renewal_response_binds_same_token_and_identity(self):
        S.check_renewal(renewal(), TOKEN)
        for delta in (
            {"client_token": "other"},
            {"policies": ["default"]},
            {"token_policies": []},
            {"renewable": False},
            {"orphan": False},
            {"token_type": "batch"},
            {"lease_duration": 0},
        ):
            with self.subTest(delta=delta), self.assertRaises(S.Blocked):
                S.check_renewal(renewal(**delta), TOKEN)

    def test_seal_status_requires_exact_unsealed_raft_cluster_and_version(self):
        S.check_seal(seal(), CLUSTER, "2.6.2")
        for delta in (
            {"initialized": False},
            {"sealed": True},
            {"storage_type": "file"},
            {"cluster_id": "foreign"},
            {"version": "2.7.1"},
        ):
            with self.subTest(delta=delta), self.assertRaises(S.Blocked):
                S.check_seal(seal(**delta), CLUSTER, "2.6.2")

    def test_only_current_or_owned_fixed_version_is_admitted(self):
        for version in ("2.6.2", "2.7.1+hyhome.go1.27.3.net0.60.0.r1"):
            S.validate_version(version)
        for version in ("2.7.1", "latest", "", "2.7.1+hyhome.go1.27.2.net0.60.0.r1"):
            with self.assertRaises(S.Blocked):
                S.validate_version(version)

    def test_header_framing_accepts_one_length_or_chunked(self):
        self.assertEqual(S.validate_headers(Response([("Content-Length", "12")])), 12)
        self.assertIsNone(
            S.validate_headers(Response([("Transfer-Encoding", "chunked")]))
        )

    def test_header_framing_rejects_duplicates_conflicts_and_redirects(self):
        cases = (
            Response([]),
            Response([("Content-Length", "1"), ("Content-Length", "1")]),
            Response([("Content-Length", "1"), ("Transfer-Encoding", "chunked")]),
            Response([("Transfer-Encoding", "gzip")]),
            Response([("Content-Length", "-1")]),
            Response([("Content-Length", str(S.MAX_COMPRESSED + 1))]),
            Response([("Content-Length", "1")], status=302),
        )
        for response in cases:
            with (
                self.subTest(headers=response.getheaders()),
                self.assertRaises(S.Blocked),
            ):
                S.validate_headers(response)
        with self.assertRaises(S.Blocked):
            S.validate_headers(Response([("X-Pad", "x")] * 65))

    def test_archive_validation_accepts_native_shape_without_extraction(self):
        with tempfile.TemporaryFile() as stream:
            stream.write(raft_archive())
            stream.flush()
            S.validate_archive(stream.fileno())

    def test_archive_rejects_json_error_malformed_gzip_and_missing_members(self):
        for body in (
            b'{"errors":["synthetic"]}',
            b"not-gzip",
            raft_archive(names=("meta.json", "state.bin")),
            raft_archive(meta=[]),
            raft_archive(corrupt_hash=True),
        ):
            with self.subTest(prefix=body[:10]), tempfile.TemporaryFile() as stream:
                stream.write(body)
                stream.flush()
                with self.assertRaises(S.Blocked):
                    S.validate_archive(stream.fileno())

    def test_archive_rejects_traversal_links_duplicates_and_member_cap(self):
        variants = []
        variants.append(raft_archive(names=("../state.bin", "meta.json")))
        duplicate = io.BytesIO()
        with tarfile.open(fileobj=duplicate, mode="w:gz") as archive:
            for name in ("meta.json", "meta.json"):
                info = tarfile.TarInfo(name)
                info.size = 2
                archive.addfile(info, io.BytesIO(b"{}"))
        variants.append(duplicate.getvalue())
        linked = io.BytesIO()
        with tarfile.open(fileobj=linked, mode="w:gz") as archive:
            info = tarfile.TarInfo("state.bin")
            info.type = tarfile.SYMTYPE
            info.linkname = "/etc/passwd"
            archive.addfile(info)
        variants.append(linked.getvalue())
        for body in variants:
            with tempfile.TemporaryFile() as stream:
                stream.write(body)
                with self.assertRaises(S.Blocked):
                    S.validate_archive(stream.fileno())
        with tempfile.TemporaryFile() as stream:
            stream.write(raft_archive())
            archive = S.load_archive()
            with (
                mock.patch.object(archive, "MAX_UNPACKED", 10),
                self.assertRaises(S.Blocked),
            ):
                S.validate_archive(stream.fileno(), archive)


class ArtifactTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.root.chmod(0o700)

    def stage_snapshot(self, artifacts, body):
        artifacts.reserve_attempt("raft.snap")
        os.write(artifacts.snapshot_fd, body)
        os.fsync(artifacts.snapshot_fd)
        validation = S.validate_archive(artifacts.snapshot_fd, artifacts.archive)
        return artifacts.publish_snapshot(validation, validation["sha256"])

    def test_private_directory_and_nofollow_are_required(self):
        with S.ArtifactDirectory(self.root):
            pass
        self.root.chmod(0o750)
        with self.assertRaises(S.Blocked):
            S.ArtifactDirectory(self.root)
        self.root.chmod(0o700)
        alias = self.root.with_name(self.root.name + "-alias")
        alias.symlink_to(self.root, target_is_directory=True)
        self.addCleanup(alias.unlink)
        with self.assertRaises(S.Blocked):
            S.ArtifactDirectory(alias)

    def test_o_excl_staging_retains_failure_and_refuses_retry(self):
        with S.ArtifactDirectory(self.root) as artifacts:
            artifacts.reserve_attempt("raft.snap")
            os.write(artifacts.snapshot_fd, b"partial")
        self.assertEqual((self.root / ".raft.snap.partial").read_bytes(), b"partial")
        self.assertEqual(len(list(self.root.iterdir())), 3)
        with S.ArtifactDirectory(self.root) as artifacts:
            with self.assertRaises(FileExistsError):
                artifacts.reserve_attempt("raft.snap")

    def test_atomic_publish_is_no_overwrite_single_link_and_fsynced(self):
        body = raft_archive()
        with S.ArtifactDirectory(self.root) as artifacts:
            record = self.stage_snapshot(artifacts, body)
        info = (self.root / "raft.snap").stat()
        self.assertEqual(info.st_nlink, 1)
        self.assertEqual(stat.S_IMODE(info.st_mode), 0o600)
        self.assertEqual(record["size"], len(body))
        self.assertFalse((self.root / ".raft.snap.partial").exists())
        with S.ArtifactDirectory(self.root) as artifacts:
            with self.assertRaises(S.Blocked):
                artifacts.reserve_attempt("raft.snap")

    def test_publish_failure_keeps_all_reserved_names(self):
        body = raft_archive()
        with S.ArtifactDirectory(self.root) as artifacts:
            artifacts.reserve_attempt("raft.snap")
            os.write(artifacts.snapshot_fd, body)
            validation = S.validate_archive(artifacts.snapshot_fd, artifacts.archive)

            with (
                mock.patch.object(artifacts, "rename_noreplace", side_effect=OSError),
                self.assertRaises(S.Indeterminate),
            ):
                artifacts.publish_snapshot(validation, validation["sha256"])
        self.assertEqual(
            {path.name for path in self.root.iterdir()},
            {
                ".raft.snap.attempt",
                ".raft.snap.partial",
                ".raft.snap.receipt.json.partial",
            },
        )

    def test_secret_free_receipt_has_only_opaque_artifact_evidence(self):
        body = raft_archive()
        with S.ArtifactDirectory(self.root) as artifacts:
            record = self.stage_snapshot(artifacts, body)
            receipt = S.receipt_document(
                record,
                cluster=CLUSTER,
                version="2.6.2",
                digest=hashlib.sha256(body).hexdigest(),
                when=0,
            )
            artifacts.publish_receipt(receipt)
        parsed = json.loads((self.root / "raft.snap.receipt.json").read_text())
        self.assertEqual(parsed["sha256"], hashlib.sha256(body).hexdigest())
        self.assertEqual(parsed["http_status"], 200)
        text = json.dumps(parsed)
        for forbidden in (TOKEN, "quies", "offsite", "restore", "payload"):
            self.assertNotIn(forbidden, text.lower())

    def test_token_ca_and_output_cross_role_aliases_are_rejected(self):
        token = self.root / "token"
        token.write_text(TOKEN)
        token.chmod(0o600)
        with token.open("rb") as stream, S.ArtifactDirectory(self.root) as artifacts:
            with self.assertRaises(S.Blocked):
                S.check_role_aliases(artifacts, stream.fileno(), (99, 99), (88, 88))

    def test_directory_close_failure_is_never_reported_as_safe_completion(self):
        artifacts = S.ArtifactDirectory(self.root)
        with mock.patch.object(artifacts, "close", side_effect=OSError):
            with self.assertRaises(S.Indeterminate):
                artifacts.__exit__(None, None, None)
        artifacts.close()


class FakeAPI:
    def __init__(self, body=None):
        self.body = body or raft_archive()
        self.calls = []

    def lookup(self):
        self.calls.append(("GET", "auth/token/lookup-self"))
        return lookup()

    def renew(self):
        self.calls.append(("POST", "auth/token/renew-self"))
        return renewal()

    def seal(self):
        self.calls.append(("GET", "sys/seal-status"))
        return seal()

    def snapshot(self, descriptor):
        self.calls.append(("GET", "sys/storage/raft/snapshot"))
        os.write(descriptor, self.body)
        return 200, len(self.body), hashlib.sha256(self.body).hexdigest()


class FlowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.root.chmod(0o700)

    def test_lookup_renew_lookup_seal_precede_single_snapshot_get(self):
        api = FakeAPI()
        with S.ArtifactDirectory(self.root) as artifacts:
            S.save_snapshot(
                api,
                artifacts,
                "raft.snap",
                TOKEN,
                CLUSTER,
                "2.6.2",
                clock=lambda: 0,
            )
        self.assertEqual(
            api.calls,
            [
                ("GET", "auth/token/lookup-self"),
                ("POST", "auth/token/renew-self"),
                ("GET", "auth/token/lookup-self"),
                ("GET", "sys/seal-status"),
                ("GET", "sys/storage/raft/snapshot"),
            ],
        )

    def test_malformed_archive_keeps_partial_and_publishes_no_receipt(self):
        with S.ArtifactDirectory(self.root) as artifacts:
            with self.assertRaises(S.Indeterminate):
                S.save_snapshot(
                    FakeAPI(b'{"errors":["denied"]}'),
                    artifacts,
                    "raft.snap",
                    TOKEN,
                    CLUSTER,
                    "2.6.2",
                )
        self.assertTrue((self.root / ".raft.snap.partial").exists())
        self.assertEqual(len(list(self.root.iterdir())), 3)

    def test_invalid_renewal_identity_stops_before_artifact_intent(self):
        api = FakeAPI()
        api.renew = lambda: renewal(client_token="other")
        with (
            S.ArtifactDirectory(self.root) as artifacts,
            self.assertRaises(S.Indeterminate),
        ):
            S.save_snapshot(api, artifacts, "raft.snap", TOKEN, CLUSTER, "2.6.2")
        self.assertEqual(len(list(self.root.iterdir())), 3)
        self.assertTrue(all(path.stat().st_size == 0 for path in self.root.iterdir()))

    def test_stream_digest_mismatch_retains_partial_as_indeterminate(self):
        api = FakeAPI()
        original_snapshot = api.snapshot

        def mismatched_snapshot(descriptor):
            status, size, _digest = original_snapshot(descriptor)
            return status, size, "0" * 64

        api.snapshot = mismatched_snapshot
        with (
            S.ArtifactDirectory(self.root) as artifacts,
            self.assertRaises(S.Indeterminate),
        ):
            S.save_snapshot(api, artifacts, "raft.snap", TOKEN, CLUSTER, "2.6.2")
        self.assertTrue((self.root / ".raft.snap.partial").exists())
        self.assertEqual(len(list(self.root.iterdir())), 3)

    def test_api_deadline_covers_the_whole_preflight_sequence(self):
        parent = S.load_parent()
        api = S.SnapshotAPI(parent, TOKEN, object(), "127.0.0.1", timeout=1)
        api.deadline = time.monotonic() - 1
        with self.assertRaises(S.Indeterminate):
            api.lookup()

    def test_secret_argv_is_rejected_without_echo(self):
        stderr = io.StringIO()
        with mock.patch("sys.stderr", stderr):
            status = S.main(["--token", TOKEN])
        self.assertEqual(status, 1)
        self.assertNotIn(TOKEN, stderr.getvalue())
        self.assertIn("BLOCKED", stderr.getvalue())

    def test_token_fd_change_after_request_is_indeterminate_and_redacted(self):
        parent = S.load_parent()
        ca = self.root.parent / (self.root.name + "-ca.pem")
        ca.write_text("public placeholder")
        ca.chmod(0o644)
        self.addCleanup(ca.unlink)
        token_path = self.root.parent / (self.root.name + "-token")
        token_path.write_text(TOKEN)
        token_path.chmod(0o600)
        self.addCleanup(token_path.unlink)
        stderr = io.StringIO()

        def mutate_token(*_args, **_options):
            token_path.write_text("changed-snapshot-token")

        with (
            token_path.open("rb") as token_stream,
            mock.patch.object(S, "load_parent", return_value=parent),
            mock.patch.object(parent, "ca_context", return_value=object()),
            mock.patch.object(S, "save_snapshot", side_effect=mutate_token),
            mock.patch("sys.stderr", stderr),
        ):
            status = S.main(
                [
                    "--ca",
                    str(ca),
                    "--ca-sha256",
                    "0" * 64,
                    "--output-directory",
                    str(self.root),
                    "--artifact-name",
                    "raft.snap",
                    "--expected-cluster-id",
                    CLUSTER,
                    "--expected-version",
                    "2.6.2",
                    "--connect-ip",
                    "127.0.0.1",
                    "--token-fd",
                    str(token_stream.fileno()),
                ]
            )
        self.assertEqual(status, 2)
        self.assertNotIn(TOKEN, stderr.getvalue())
        self.assertIn("INDETERMINATE", stderr.getvalue())


class TLSFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.temp.name)
        for label, host in (("valid", S.HOST), ("wrong", "wrong.invalid")):
            subprocess.run(
                [
                    "openssl",
                    "req",
                    "-x509",
                    "-newkey",
                    "rsa:2048",
                    "-nodes",
                    "-keyout",
                    str(cls.root / f"{label}.key"),
                    "-out",
                    str(cls.root / f"{label}.pem"),
                    "-days",
                    "1",
                    "-subj",
                    f"/CN={host}",
                    "-addext",
                    f"subjectAltName=DNS:{host}",
                ],
                check=True,
                capture_output=True,
            )
            (cls.root / f"{label}.pem").chmod(0o644)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def serve(self, parent, *, certificate="valid", chunked=False, slow=False):
        calls = []
        snapshot = raft_archive()

        class Handler(http.server.BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def log_message(self, *_):
                pass

            def _send(self, body, *, as_chunks=False):
                self.send_response(200)
                if as_chunks:
                    self.send_header("Transfer-Encoding", "chunked")
                else:
                    self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                pieces = [body] if not slow else [bytes([byte]) for byte in body]
                for piece in pieces:
                    try:
                        if as_chunks:
                            self.wfile.write(f"{len(piece):x}\r\n".encode())
                            self.wfile.write(piece + b"\r\n")
                        else:
                            self.wfile.write(piece)
                        self.wfile.flush()
                    except (OSError, ssl.SSLError):
                        return
                    if slow:
                        time.sleep(0.05)
                if as_chunks:
                    self.wfile.write(b"0\r\n\r\n")
                    self.wfile.flush()

            def do_GET(self):
                calls.append(("GET", self.path))
                documents = {
                    "/v1/auth/token/lookup-self": lookup(),
                    "/v1/sys/seal-status": seal(),
                }
                if self.path == "/v1/sys/storage/raft/snapshot":
                    self._send(snapshot, as_chunks=chunked)
                elif self.path in documents:
                    self._send(json.dumps(documents[self.path]).encode())
                else:
                    self.send_error(404)

            def do_POST(self):
                calls.append(("POST", self.path))
                length = int(self.headers.get("Content-Length", "0"))
                body = self.rfile.read(length)
                if self.path != "/v1/auth/token/renew-self" or json.loads(body) != {
                    "increment": "720h"
                }:
                    self.send_error(404)
                    return
                self._send(json.dumps(renewal()).encode())

        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        server.daemon_threads = True
        server.handle_error = lambda *_: None
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        context.load_cert_chain(
            self.root / f"{certificate}.pem", self.root / f"{certificate}.key"
        )
        server.socket = context.wrap_socket(server.socket, server_side=True)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        original = parent.PinnedConnection

        def connection(host, _port, **options):
            return original(host, server.server_port, **options)

        patch = mock.patch.object(parent, "PinnedConnection", connection)
        patch.start()
        self.addCleanup(patch.stop)
        return calls, snapshot

    def context(self, parent, label):
        ca = self.root / f"{label}.pem"
        return parent.ca_context(ca, hashlib.sha256(ca.read_bytes()).hexdigest())

    def test_fixed_tls_origin_ignores_proxy_and_streams_chunked_binary(self):
        parent = S.load_parent()
        calls, snapshot = self.serve(parent, chunked=True)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            root.chmod(0o700)
            api = S.SnapshotAPI(
                parent, TOKEN, self.context(parent, "valid"), "127.0.0.1", timeout=3
            )
            with (
                mock.patch.dict(
                    os.environ,
                    {
                        "HTTPS_PROXY": "http://127.0.0.1:1",
                        "https_proxy": "http://127.0.0.1:1",
                        "NO_PROXY": "",
                    },
                ),
                S.ArtifactDirectory(root) as artifacts,
            ):
                receipt = S.save_snapshot(
                    api,
                    artifacts,
                    "raft.snap",
                    TOKEN,
                    CLUSTER,
                    "2.6.2",
                    clock=lambda: 0,
                )
            self.assertEqual((root / "raft.snap").read_bytes(), snapshot)
            self.assertEqual(receipt["sha256"], hashlib.sha256(snapshot).hexdigest())
        self.assertEqual(
            calls,
            [
                ("GET", "/v1/auth/token/lookup-self"),
                ("POST", "/v1/auth/token/renew-self"),
                ("GET", "/v1/auth/token/lookup-self"),
                ("GET", "/v1/sys/seal-status"),
                ("GET", "/v1/sys/storage/raft/snapshot"),
            ],
        )

    def test_wrong_hostname_and_ca_fail_closed(self):
        for certificate, trust in (("valid", "wrong"), ("wrong", "wrong")):
            with self.subTest(certificate=certificate):
                parent = S.load_parent()
                self.serve(parent, certificate=certificate)
                api = S.SnapshotAPI(
                    parent,
                    TOKEN,
                    self.context(parent, trust),
                    "127.0.0.1",
                    timeout=1,
                )
                with self.assertRaises(S.Indeterminate):
                    api.lookup()
                self.doCleanups()

    def test_trickle_response_obeys_one_total_deadline(self):
        parent = S.load_parent()
        self.serve(parent, slow=True)
        api = S.SnapshotAPI(
            parent, TOKEN, self.context(parent, "valid"), "127.0.0.1", timeout=0.2
        )
        started = time.monotonic()
        with self.assertRaises(S.Indeterminate):
            api.lookup()
        self.assertLess(time.monotonic() - started, 1.0)


if __name__ == "__main__":
    unittest.main()
