"""Synthetic periodic issuance/revocation; never use HOME credentials or endpoints."""

from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

from tests.validation import test_openbao_protected_maintenance as fixtures

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "infra/03-security/openbao/scripts/protected-token-operations.py"
SPEC = importlib.util.spec_from_file_location("protected_token_operations", SOURCE)
M = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = M
SPEC.loader.exec_module(M)

TOKEN = "synthetic-periodic-backup"
CLUSTER = fixtures.CLUSTER


def auth():
    return {
        "auth": {
            "client_token": TOKEN,
            "policies": ["backup-snapshot"],
            "token_policies": ["backup-snapshot"],
            "orphan": True,
            "renewable": True,
            "entity_id": "",
            "token_type": "service",
            "lease_duration": 2592000,
        }
    }


def backup():
    return {
        "data": {
            "id": "synthetic-internal-id",
            "policies": ["backup-snapshot"],
            "path": "auth/token/create-orphan",
            "entity_id": "",
            "orphan": True,
            "renewable": True,
            "type": "service",
            "ttl": 2591999,
            "creation_ttl": 2592000,
            "period": 2592000,
            "num_uses": 0,
            "explicit_max_ttl": 0,
        }
    }


class FakeAPI:
    def __init__(self, mode="issue", responses=None):
        self.mode = mode
        self.token = fixtures.ROOT_TOKEN
        self.context = mock.sentinel.context
        self.connect_ip = "127.0.0.1"
        self.calls = []
        policy = (ROOT / M.POLICY_FILE).read_text()
        self.responses = responses or [
            fixtures.FakeAPI().root_response,
            fixtures.seal(),
            None,
            None,
            {"data": {"policy": policy}},
            auth(),
            {
                "data": {
                    path: capabilities for path, capabilities in M.CAPABILITIES.items()
                }
            },
        ]
        self.backup_api = FakeBackup()

    def request(self, method, path, document=None, *, deny=False):
        self.calls.append((method, path, document, deny))
        value = self.responses.pop(0)
        if isinstance(value, BaseException):
            raise value
        return value

    def for_backup(self, token):
        if token != TOKEN:
            raise M.Blocked()
        return self.backup_api


class FakeBackup(FakeAPI):
    def __init__(self):
        self.calls = []
        self.responses = [backup(), True, auth(), backup()]


class IssuanceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = Path(self.tmp.name) / "home"
        self.output = self.home / "secrets/backup/openbao"
        self.output.mkdir(parents=True, mode=0o700)
        self.directory = Path(self.tmp.name) / "operation"
        self.directory.mkdir(mode=0o700)
        self.home_identity = (self.home.stat().st_dev, self.home.stat().st_ino)
        canonical = mock.patch.object(M, "CANONICAL_HOME_ROOT", self.home)
        canonical.start()
        self.addCleanup(canonical.stop)
        self.policy = (ROOT / M.POLICY_FILE).read_text()
        self.api = FakeAPI()

    def tearDown(self):
        self.tmp.cleanup()

    def issue(self):
        with (
            M.Destination(self.home, *self.home_identity) as destination,
            M.OperationCustody(self.directory) as custody,
        ):
            return M.issue_snapshot(
                self.api, custody, destination, CLUSTER, self.policy
            )

    def test_success_has_no_default_policy_one_create_durable_response_and_output(self):
        self.assertEqual(self.issue(), "SNAPSHOT_TOKEN_DELIVERED")
        self.assertEqual((self.output / "snapshot_token.txt").read_text(), TOKEN)
        self.assertEqual((self.output / "snapshot_token.txt").stat().st_nlink, 1)
        self.assertEqual(
            (self.output / "snapshot_token.txt").stat().st_mode & 0o777, 0o600
        )
        self.assertEqual(
            json.loads((self.directory / "issuance-response.json").read_text()), auth()
        )
        create = [call for call in self.api.calls if call[1] == M.CREATE]
        self.assertEqual(len(create), 1)
        self.assertEqual(create[0][2], M.CREATE_PAYLOAD)
        self.assertTrue(create[0][2]["no_default_policy"])
        self.assertEqual(create[0][2]["period"], "720h")
        self.assertEqual(create[0][2]["policies"], ["backup-snapshot"])

    def test_default_or_root_policies_in_issued_response_are_indeterminate(self):
        self.api.responses[5]["auth"]["policies"] = ["default", "backup-snapshot"]
        with self.assertRaises(M.Indeterminate):
            self.issue()
        self.assertTrue((self.directory / "issuance-response.json").exists())
        self.assertFalse((self.output / "snapshot_token.txt").exists())
        self.assertEqual(sum(call[1] == M.CREATE for call in self.api.calls), 1)

    def test_existing_output_symlink_or_operation_is_not_overwritten(self):
        target = self.output / "snapshot_token.txt"
        target.write_text("preserved")
        with self.assertRaises(M.Blocked):
            self.issue()
        self.assertEqual(target.read_text(), "preserved")
        self.assertEqual(self.api.calls, [])

    def test_unexpected_existing_acl_blocks_before_any_post(self):
        self.api.responses[2] = {"data": {"policy": "custom ACL"}}
        with self.assertRaises(M.Blocked):
            self.issue()
        self.assertFalse(any(call[0] == "POST" for call in self.api.calls))

    def test_readback_difference_retains_intent_and_blocks_token_create(self):
        self.api.responses[4] = {"data": {"policy": "changed after upload"}}
        with self.assertRaises(M.Indeterminate):
            self.issue()
        self.assertTrue((self.directory / "operation-intent.json").exists())
        self.assertFalse(any(call[1] == M.CREATE for call in self.api.calls))

    def test_create_response_loss_never_retries_or_revokes(self):
        self.api.responses[5] = M.Indeterminate()
        with self.assertRaises(M.Indeterminate):
            self.issue()
        self.assertEqual(sum(call[1] == M.CREATE for call in self.api.calls), 1)
        self.assertFalse(any(call[1] == M.REVOKE for call in self.api.calls))
        self.assertTrue((self.output / ".snapshot_token.txt.issuance-lock").exists())

    def test_denial_renewal_or_capability_failure_retains_issued_response(self):
        self.api.backup_api.responses[1] = M.Blocked()
        with self.assertRaises(M.Indeterminate):
            self.issue()
        self.assertTrue((self.directory / "issuance-response.json").exists())
        self.assertFalse((self.output / "snapshot_token.txt").exists())

    def test_response_must_be_durable_before_token_is_interpreted(self):
        original = M.OperationCustody.write

        def fail(custody, descriptor, value):
            if value == auth():
                raise OSError("synthetic fsync fault")
            return original(custody, descriptor, value)

        with (
            mock.patch.object(M.OperationCustody, "write", fail),
            self.assertRaises(M.Indeterminate),
        ):
            self.issue()
        self.assertEqual(self.api.backup_api.calls, [])

    def test_destination_alias_wrong_mode_or_retained_lock_blocks_before_credentials(
        self,
    ):
        self.output.chmod(0o755)
        with self.assertRaises(M.Blocked):
            M.Destination(self.home, *self.home_identity)
        self.output.chmod(0o700)
        self.output.rename(self.output.with_name("preserved"))
        self.output.symlink_to(self.output.with_name("preserved"))
        with self.assertRaises(M.Blocked):
            M.Destination(self.home, *self.home_identity)

    def test_destination_path_replacement_never_delivers_into_changed_canonical_target(
        self,
    ):
        with M.Destination(self.home, *self.home_identity) as destination:
            destination.reserve()
            self.output.rename(self.output.with_name("preserved"))
            self.output.mkdir(mode=0o700)
            with self.assertRaises(M.Blocked):
                destination.deliver(TOKEN)
        self.assertFalse((self.output / "snapshot_token.txt").exists())

    def test_concurrent_target_creation_does_not_overwrite_existing_value(self):
        with M.Destination(self.home, *self.home_identity) as destination:
            destination.reserve()
            target = self.output / "snapshot_token.txt"
            target.write_text("preserved")
            with self.assertRaises(FileExistsError):
                destination.deliver(TOKEN)
        self.assertEqual(target.read_text(), "preserved")

    def test_prior_policy_and_exact_new_policy_are_the_only_replaceable_acl_values(
        self,
    ):
        self.api.responses[2] = {"data": {"policy": self.policy}}
        self.assertEqual(self.issue(), "SNAPSHOT_TOKEN_DELIVERED")

    def test_periodic_lookup_wrong_ttl_policy_or_entity_cannot_pass(self):
        self.api.backup_api.responses[0]["data"]["period"] = 0
        with self.assertRaises(M.Indeterminate):
            self.issue()
        self.assertFalse((self.output / "snapshot_token.txt").exists())

    def test_capabilities_or_renewal_identity_mismatch_never_delivers(self):
        self.api.responses[6] = {"data": {**M.CAPABILITIES, M.DENY_SECRET: ["read"]}}
        with self.assertRaises(M.Indeterminate):
            self.issue()
        self.assertFalse((self.output / "snapshot_token.txt").exists())

    def test_renewal_response_is_preserved_even_when_identity_is_wrong(self):
        self.api.backup_api.responses[2]["auth"]["client_token"] = "another-token"
        with self.assertRaises(M.Indeterminate):
            self.issue()
        self.assertTrue((self.directory / "renewal-response.json").exists())
        self.assertFalse((self.output / "snapshot_token.txt").exists())


class RevocationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.directory = Path(self.tmp.name)
        self.directory.chmod(0o700)
        self.api = FakeAPI(
            "revoke", [fixtures.FakeAPI().root_response, fixtures.seal(), None, True]
        )

    def tearDown(self):
        self.tmp.cleanup()

    def revoke(self, operator=None):
        if operator is None:
            operator = mock.Mock(token="independent-operator")
            original = fixtures.operator()
            operator.request.return_value = {
                "data": {**original["data"], "type": "service"}
            }
        with M.OperationCustody(self.directory) as custody:
            return M.revoke_root(self.api, custody, CLUSTER, operator)

    def test_revoke_root_requires_preflight_root_and_post_denial(self):
        self.assertEqual(self.revoke(), "ROOT_REVOKED_OPERATOR_HEALTHY")
        self.assertEqual(sum(call[1] == M.REVOKE for call in self.api.calls), 1)
        self.assertTrue(self.api.calls[-1][3])

    def test_operator_controls_before_and_after_and_never_receives_root(self):
        operator = mock.Mock(token="independent-operator")
        original = fixtures.operator()
        operator.request.return_value = {
            "data": {**original["data"], "type": "service"}
        }
        self.assertEqual(self.revoke(operator), "ROOT_REVOKED_OPERATOR_HEALTHY")
        self.assertEqual(operator.request.call_count, 2)
        for call in operator.request.call_args_list:
            self.assertEqual(call.args, ("GET", M.BASE.LOOKUP))

    def test_root_lookup_denial_before_revoke_never_mutates(self):
        self.api.responses[0] = M.Blocked()
        with self.assertRaises(M.Blocked):
            self.revoke()
        self.assertFalse(any(call[0] == "POST" for call in self.api.calls))

    def test_lost_revoke_response_is_indeterminate_and_never_retried(self):
        self.api.responses[2] = M.Indeterminate()
        with self.assertRaises(M.Indeterminate):
            self.revoke()
        self.assertEqual(sum(call[1] == M.REVOKE for call in self.api.calls), 1)

    def test_successful_post_without_confirmed403_is_not_revocation(self):
        self.api.responses[3] = M.Blocked()
        with self.assertRaises(M.Indeterminate):
            self.revoke()


class BindingAndTransportTests(unittest.TestCase):
    def test_public_source_binding_refuses_different_approved_client_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "public.py"
            path.write_text("raise AssertionError('must not execute')")
            with self.assertRaises(M.BindingBlocked):
                M.read_public(path, M.MAINTENANCE_SHA256)

    def test_canonical_policy_owns_only_snapshot_and_self_lifecycle_permissions(self):
        policy = (ROOT / M.POLICY_FILE).read_text()
        for path in (
            "sys/storage/raft/snapshot",
            "auth/token/lookup-self",
            "auth/token/renew-self",
            "auth/token/revoke-self",
        ):
            self.assertIn('path "' + path + '"', policy)
        self.assertNotIn("*", policy)
        self.assertNotIn("secret/", policy)
        self.assertNotIn("sudo", policy)

    def test_unknown_cli_argument_never_echoes_secret(self):
        output = io.StringIO()
        with mock.patch.object(sys, "stderr", output):
            self.assertEqual(M.main(["--token", TOKEN]), 1)
        self.assertNotIn(TOKEN, output.getvalue())
        self.assertNotIn("Traceback", output.getvalue())

    def test_routes_reject_generic_token_or_policy_operations_before_network(self):
        api = M.TokenAPI(
            fixtures.ROOT_TOKEN, mock.sentinel.context, "127.0.0.1", "revoke"
        )
        with mock.patch.object(M.BASE, "PinnedConnection") as connection:
            with self.assertRaises(M.Blocked):
                api.request("POST", "auth/token/create", {"policies": ["root"]})
            with self.assertRaises(M.Blocked):
                api.request("POST", M.CREATE, M.CREATE_PAYLOAD)
            connection.assert_not_called()

    def test_denial_probes_read_status_only_never_raw_body(self):
        response = mock.Mock(status=403)
        connection = mock.Mock()
        connection.getresponse.return_value = response
        with mock.patch.object(M.BASE, "PinnedConnection", return_value=connection):
            self.assertTrue(
                M.TokenAPI(TOKEN, mock.sentinel.context, "127.0.0.1", "backup").request(
                    "GET", M.DENY_SECRET, deny=True
                )
            )
        response.read.assert_not_called()

    def test_malformed_or_redirected_response_is_secret_free_and_never_followed(self):
        for mode, method, path, payload in (
            ("backup", "GET", M.BASE.LOOKUP, None),
            ("revoke", "POST", M.REVOKE, {}),
        ):
            response = mock.Mock(status=302)
            response.read.return_value = TOKEN.encode()
            connection = mock.Mock()
            connection.getresponse.return_value = response
            with mock.patch.object(M.BASE, "PinnedConnection", return_value=connection):
                with self.assertRaises(M.Blocked) as caught:
                    M.TokenAPI(TOKEN, mock.sentinel.context, "127.0.0.1", mode).request(
                        method, path, payload
                    )
            self.assertNotIn(TOKEN, str(caught.exception))
            response.read.assert_not_called()
            connection.close.assert_called_once()

    def test_issue_routes_refuse_arbitrary_payload_policy_or_caps_paths(self):
        policy = (ROOT / M.POLICY_FILE).read_text()
        api = M.TokenAPI(
            fixtures.ROOT_TOKEN, mock.sentinel.context, "127.0.0.1", "issue", policy
        )
        for path, document in (
            (M.CREATE, {**M.CREATE_PAYLOAD, "policies": ["root"]}),
            (M.POLICY, {"policy": "arbitrary policy"}),
            (M.CAPS, {"token": TOKEN, "paths": ["secret/*"]}),
        ):
            with self.subTest(path=path), self.assertRaises(M.Blocked):
                api.request("POST", path, document)

    def test_root_fd_must_match_private_w1_token_inode_and_delivered_state(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            token = root / "root.token"
            token.write_text(fixtures.ROOT_TOKEN)
            token.chmod(0o600)
            state = root / "state.json"
            state.write_text(
                json.dumps({"state": "DELIVERED", "operator_healthy": True})
            )
            state.chmod(0o600)
            with token.open("rb") as stream:
                self.assertEqual(
                    M.root_input(stream.fileno(), root), fixtures.ROOT_TOKEN
                )
            state.write_text(json.dumps({"state": "INDETERMINATE"}))
            with token.open("rb") as stream, self.assertRaises(M.Blocked):
                M.root_input(stream.fileno(), root)
            other = root / "other"
            other.write_text(fixtures.ROOT_TOKEN)
            other.chmod(0o600)
            with other.open("rb") as stream, self.assertRaises(M.Blocked):
                M.root_input(stream.fileno(), root)

    def test_successful_http_policy404_and_revoke204_are_method_bound(self):
        for mode, method, path, payload, status, raw, expected in (
            (
                "backup",
                "GET",
                M.BASE.LOOKUP,
                None,
                200,
                json.dumps(backup()).encode(),
                backup(),
            ),
            ("issue", "GET", M.POLICY, None, 404, b"untrusted", None),
            ("revoke", "POST", M.REVOKE, {}, 204, b"", None),
        ):
            response = mock.Mock(status=status)
            response.read.return_value = raw
            connection = mock.Mock()
            connection.getresponse.return_value = response
            policy = (ROOT / M.POLICY_FILE).read_text() if mode == "issue" else None
            with mock.patch.object(M.BASE, "PinnedConnection", return_value=connection):
                self.assertEqual(
                    M.TokenAPI(
                        TOKEN, mock.sentinel.context, "127.0.0.1", mode, policy
                    ).request(method, path, payload),
                    expected,
                )
            if status == 404:
                response.read.assert_not_called()

    def test_http_invalid_json_or_transport_loss_is_sanitized(self):
        response = mock.Mock(status=200)
        response.read.return_value = b'{"value":NaN}'
        connection = mock.Mock()
        connection.getresponse.return_value = response
        with mock.patch.object(M.BASE, "PinnedConnection", return_value=connection):
            with self.assertRaises(M.Blocked):
                M.TokenAPI(TOKEN, mock.sentinel.context, "127.0.0.1", "backup").request(
                    "GET", M.BASE.LOOKUP
                )
        connection.request.side_effect = OSError("synthetic secret " + TOKEN)
        with mock.patch.object(M.BASE, "PinnedConnection", return_value=connection):
            with self.assertRaises(M.Indeterminate) as caught:
                M.TokenAPI(TOKEN, mock.sentinel.context, "127.0.0.1", "backup").request(
                    "GET", M.BASE.LOOKUP
                )
        self.assertNotIn(TOKEN, str(caught.exception))


class CLITests(unittest.TestCase):
    setUp = IssuanceTests.setUp
    tearDown = IssuanceTests.tearDown

    def prepare_w1(self):
        w1 = Path(self.tmp.name) / "w1"
        w1.mkdir(mode=0o700)
        root = w1 / "root.token"
        root.write_text(fixtures.ROOT_TOKEN)
        root.chmod(0o600)
        state = w1 / "state.json"
        state.write_text(json.dumps({"state": "DELIVERED", "operator_healthy": True}))
        state.chmod(0o600)
        return w1, root

    def arguments(self, operation, w1, descriptor):
        arguments = [
            operation,
            "--ca",
            str(Path(self.tmp.name) / "ca.pem"),
            "--ca-sha256",
            "0" * 64,
            "--connect-ip",
            "127.0.0.1",
            "--expected-cluster-id",
            CLUSTER,
            "--custody-directory",
            str(self.directory),
            "--w1-custody-directory",
            str(w1),
            "--root-fd",
            str(descriptor),
        ]
        if operation == "issue-snapshot-token":
            return [
                *arguments,
                "--home-root",
                str(self.home),
                "--policy-sha256",
                M.POLICY_SHA256,
                "--expected-home-device",
                str(self.home_identity[0]),
                "--expected-home-inode",
                str(self.home_identity[1]),
            ]
        return arguments

    def run_main(self, arguments, api, broken_output=False, operator=None):
        output, error = io.StringIO(), io.StringIO()
        if broken_output:
            output.write = mock.Mock(side_effect=OSError("synthetic"))
        with (
            mock.patch.object(sys, "stdout", output),
            mock.patch.object(sys, "stderr", error),
        ):
            with mock.patch.object(
                M.BASE, "ca_context", return_value=mock.sentinel.context
            ):

                def factory(_token, _context, _ip, mode, _policy=None):
                    return operator if mode == "operator" else api

                with mock.patch.object(M, "TokenAPI", side_effect=factory):
                    result = M.main(arguments)
        for secret in (TOKEN, fixtures.ROOT_TOKEN):
            self.assertNotIn(secret, output.getvalue() + error.getvalue())
        self.assertNotIn("Traceback", output.getvalue() + error.getvalue())
        return result

    def test_cli_issue_uses_exact_selected_source_policy_and_private_fd(self):
        w1, root = self.prepare_w1()
        with root.open("rb") as stream:
            self.assertEqual(
                self.run_main(
                    self.arguments("issue-snapshot-token", w1, stream.fileno()),
                    self.api,
                ),
                0,
            )
        self.assertEqual((self.output / "snapshot_token.txt").read_text(), TOKEN)

    def test_cli_revoke_without_operator_preserves_root_and_never_posts(self):
        w1, root = self.prepare_w1()
        api = FakeAPI(
            "revoke", [fixtures.FakeAPI().root_response, fixtures.seal(), None, True]
        )
        with root.open("rb") as stream:
            self.assertEqual(
                self.run_main(self.arguments("revoke-root", w1, stream.fileno()), api),
                1,
            )
        self.assertEqual(root.read_text(), fixtures.ROOT_TOKEN)
        self.assertFalse((self.directory / "state.json").exists())
        self.assertEqual(api.calls, [])

    def test_cli_response_loss_and_stdout_fault_after_delivery_are_indeterminate(self):
        w1, root = self.prepare_w1()
        with root.open("rb") as stream:
            self.assertEqual(
                self.run_main(
                    self.arguments("issue-snapshot-token", w1, stream.fileno()),
                    self.api,
                    True,
                ),
                2,
            )
        self.assertEqual((self.output / "snapshot_token.txt").read_text(), TOKEN)

    def test_cli_wrong_selected_policy_version_or_stdio_root_fails_without_post(self):
        w1, root = self.prepare_w1()
        with root.open("rb") as stream:
            arguments = self.arguments("issue-snapshot-token", w1, stream.fileno())
            for suffix in (
                ["--policy-sha256", "f" * 64],
                ["--root-fd", "0"],
                ["--expected-cluster-id", "wrong"],
            ):
                self.assertEqual(self.run_main([*arguments, *suffix], self.api), 1)
        self.assertEqual(self.api.calls, [])

    def test_source_binding_unavailable_is_blocked_without_echoing_unknown_argv(self):
        error = io.StringIO()
        with (
            mock.patch.object(M, "BASE", None),
            mock.patch.object(sys, "stderr", error),
        ):
            self.assertEqual(M.main(["--token", TOKEN]), 1)
        self.assertNotIn(TOKEN, error.getvalue())


class TokenTLSTests(unittest.TestCase):
    setUpClass = classmethod(fixtures.TLSFixtureTests.setUpClass.__func__)
    tearDownClass = classmethod(fixtures.TLSFixtureTests.tearDownClass.__func__)
    serve = fixtures.TLSFixtureTests.serve

    def test_new_transport_preserves_fixed_origin_ca_and_numeric_gateway(self):
        self.serve()
        ca = self.root / "valid.pem"
        context = M.BASE.ca_context(ca, hashlib.sha256(ca.read_bytes()).hexdigest())
        with mock.patch.object(M.BASE, "PinnedConnection", fixtures.M.PinnedConnection):
            self.assertEqual(
                M.TokenAPI(TOKEN, context, "127.0.0.1", "backup").request(
                    "GET", M.BASE.LOOKUP
                ),
                fixtures.operator(),
            )

    def test_new_transport_still_enforces_total_slow_trickle_deadline(self):
        self.serve(slow=True)
        ca = self.root / "valid.pem"
        context = M.BASE.ca_context(ca, hashlib.sha256(ca.read_bytes()).hexdigest())
        started = time.monotonic()
        with mock.patch.object(M.BASE, "PinnedConnection", fixtures.M.PinnedConnection):
            with (
                mock.patch.object(M.BASE, "REQUEST_SECONDS", 0.3),
                self.assertRaises(M.Indeterminate),
            ):
                M.TokenAPI(TOKEN, context, "127.0.0.1", "backup").request(
                    "GET", M.BASE.LOOKUP
                )
        self.assertLess(time.monotonic() - started, 1.0)

    def test_new_transport_wrong_ca_cannot_authenticate_denial_or_readback(self):
        self.serve()
        ca = self.root / "wrong.pem"
        context = M.BASE.ca_context(ca, hashlib.sha256(ca.read_bytes()).hexdigest())
        with mock.patch.object(M.BASE, "PinnedConnection", fixtures.M.PinnedConnection):
            with self.assertRaises(M.Indeterminate):
                M.TokenAPI(TOKEN, context, "127.0.0.1", "backup").request(
                    "GET", M.DENY_SECRET, deny=True
                )


if __name__ == "__main__":
    unittest.main()
