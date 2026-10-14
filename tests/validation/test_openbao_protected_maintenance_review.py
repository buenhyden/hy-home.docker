"""Focused synthetic regressions for independent protected-client review findings."""

from __future__ import annotations

import hashlib
import io
import json
import os
import sys
import unittest
from pathlib import Path
from unittest import mock

from tests.validation import test_openbao_protected_maintenance as fixtures

M = fixtures.M
TOKEN = fixtures.TOKEN
ROOT_TOKEN = fixtures.ROOT_TOKEN
CLUSTER = fixtures.CLUSTER
FakeAPI = fixtures.FakeAPI
operator = fixtures.operator


class ReviewRegressionTests(unittest.TestCase):
    setUp = fixtures.CeremonyTests.setUp
    tearDown = fixtures.CeremonyTests.tearDown
    run_ceremony = fixtures.CeremonyTests.run_ceremony

    def test_exact_owned_version_is_supported_and_unknown_suffixes_are_denied(self):
        owned = "2.7.1+hyhome.go1.27.2.net0.60.0.r1"
        M.check_seal({**fixtures.seal(), "version": owned}, CLUSTER)
        for unknown in (
            owned + ".other",
            "2.7.1+hyhome.go1.27.2.net0.60.0.r2",
            "2.7.1+other",
        ):
            with self.subTest(unknown=unknown), self.assertRaises(M.Blocked):
                M.check_seal({**fixtures.seal(), "version": unknown}, CLUSTER)

    def test_decoded_credential_requires_root_lookup_before_delivered(self):
        self.api.root_lookup = mock.Mock(return_value=operator())
        with self.assertRaises(M.Indeterminate):
            self.run_ceremony()
        self.api.root_lookup.assert_called_once_with(ROOT_TOKEN)
        self.assertTrue((self.directory / "root.token").exists())
        valid = FakeAPI().root_response
        M.check_root(valid)
        for field, value in (
            ("policies", ["root", "default"]),
            ("type", "batch"),
            ("orphan", False),
            ("ttl", True),
            ("entity_id", "user"),
            ("renewable", True),
            ("namespace_path", "other/"),
            ("id", ""),
        ):
            with self.subTest(field=field), self.assertRaises(M.Blocked):
                M.check_root({"data": {**valid["data"], field: value}})

    def test_operator_token_cannot_be_a_share_and_no_post_is_sent(self):
        self.shares = iter([TOKEN, "b" * 64])
        self.api.token = TOKEN
        with self.assertRaises(M.Blocked):
            self.run_ceremony()
        self.assertFalse(any(call[0] == "POST" for call in self.api.calls))

    def test_json_depth_node_nonfinite_or_recursion_fails_closed(self):
        for raw in (
            b'{"a":NaN}',
            b'{"a":Infinity}',
            b'{"a":' + b"[" * 1100 + b"0" + b"]" * 1100 + b"}",
            json.dumps({"a": [0] * 5000}).encode(),
        ):
            with self.subTest(prefix=raw[:12]), self.assertRaises(M.Blocked):
                M.parse_response(raw)
        with (
            mock.patch.object(M.json, "loads", side_effect=RecursionError()),
            self.assertRaises(M.Blocked),
        ):
            M.parse_response(b"{}")
        M.parse_response(b'{"literal":"{[\\"}"}')

    def test_ca_digest_mismatch_precedes_ssl_loading(self):
        ca = Path(self.tmp.name) / "ca.pem"
        ca.write_bytes(b"synthetic certificate bytes")
        ca.chmod(0o644)
        with mock.patch.object(M.ssl, "SSLContext") as context:
            with self.assertRaises(M.Blocked):
                M.ca_context(ca, "0" * 64)
            context.assert_not_called()

    def test_close_failure_preserves_active_indeterminate(self):
        custody = M.Custody(self.directory)
        original = M.Indeterminate()
        with mock.patch.object(custody, "close", side_effect=OSError("synthetic")):
            with self.assertRaises(M.Indeterminate) as caught:
                with custody:
                    raise original
        self.assertIs(caught.exception, original)
        custody.close()

    def test_close_failure_after_delivery_never_downgrades_to_blocked(self):
        original = M.Custody.close

        def failure(custody):
            original(custody)
            raise OSError("synthetic")

        with mock.patch.object(M.Custody, "close", failure):
            with self.assertRaises(M.Indeterminate):
                self.run_ceremony()

    def test_preinit_parse_failure_and_postinit_parse_failure_keep_distinct_states(
        self,
    ):
        invalid = b'{"value":NaN}'
        for method, path, document, expected in (
            ("GET", M.LOOKUP, None, M.Blocked),
            ("POST", M.ATTEMPT, {}, M.Indeterminate),
        ):
            connection = fixtures.HTTPTests().connection(200, invalid)
            with mock.patch.object(M, "PinnedConnection", return_value=connection):
                with self.assertRaises(expected):
                    M.API(TOKEN, mock.sentinel.context, "127.0.0.1").request(
                        method, path, document
                    )

    def test_fresh_root_client_reuses_ca_gateway_and_allows_only_lookup(self):
        api = M.API(TOKEN, mock.sentinel.context, "127.0.0.1")
        with mock.patch.object(M, "API") as factory:
            api.root_lookup(ROOT_TOKEN)
        factory.assert_called_once_with(
            ROOT_TOKEN, mock.sentinel.context, "127.0.0.1", lookup_only=True
        )
        factory.return_value.request.assert_called_once_with("GET", M.LOOKUP)
        with self.assertRaises(M.Blocked):
            M.API(
                ROOT_TOKEN, mock.sentinel.context, "127.0.0.1", lookup_only=True
            ).request("POST", M.ATTEMPT, {})


class DeliveryOutputTests(unittest.TestCase):
    setUp = fixtures.CLITests.setUp
    tearDown = fixtures.CLITests.tearDown

    def test_stdout_failure_after_durable_delivery_is_indeterminate(self):
        output = io.StringIO()
        with mock.patch.object(output, "write", side_effect=OSError("synthetic")):
            with (
                mock.patch.object(sys, "stdout", output),
                mock.patch.object(sys, "stderr", io.StringIO()),
            ):
                with mock.patch.object(
                    M, "ca_context", return_value=mock.sentinel.context
                ):
                    with mock.patch.object(M, "API", return_value=FakeAPI()):
                        with mock.patch.object(
                            M, "hidden_input", side_effect=[TOKEN, "a" * 64, "b" * 64]
                        ):
                            self.assertEqual(M.main(self.arguments), 2)
        self.assertEqual((self.custody / "root.token").read_text(), ROOT_TOKEN)
        self.assertEqual(
            json.loads((self.custody / "state.json").read_text())["state"], "DELIVERED"
        )

    def test_hidden_tty_operator_equal_to_share_blocks_before_post(self):
        api = FakeAPI()
        with mock.patch.object(M, "ca_context", return_value=mock.sentinel.context):
            with (
                mock.patch.object(M, "API", return_value=api),
                mock.patch.object(sys, "stderr", io.StringIO()),
            ):
                with mock.patch.object(
                    M, "hidden_input", side_effect=[TOKEN, TOKEN, "b" * 64]
                ):
                    self.assertEqual(M.main(self.arguments), 1)
        self.assertFalse(any(call[0] == "POST" for call in api.calls))

    def test_distinct_fd_files_with_equal_secret_contents_block_before_post(self):
        descriptors = []
        api = FakeAPI()
        try:
            for name, value in (("operator", TOKEN), ("one", TOKEN), ("two", "b" * 64)):
                path = self.root / name
                path.write_text(value)
                path.chmod(0o600)
                descriptors.append(os.open(path, os.O_RDONLY))
            arguments = [
                *self.arguments,
                "--operator-fd",
                str(descriptors[0]),
                "--share-one-fd",
                str(descriptors[1]),
                "--share-two-fd",
                str(descriptors[2]),
            ]
            with mock.patch.object(M, "ca_context", return_value=mock.sentinel.context):
                with (
                    mock.patch.object(M, "API", return_value=api),
                    mock.patch.object(sys, "stderr", io.StringIO()),
                ):
                    self.assertEqual(M.main(arguments), 1)
            self.assertFalse(any(call[0] == "POST" for call in api.calls))
        finally:
            for descriptor in descriptors:
                os.close(descriptor)


class MatchingSANDigestTests(unittest.TestCase):
    setUpClass = classmethod(fixtures.TLSFixtureTests.setUpClass.__func__)
    tearDownClass = classmethod(fixtures.TLSFixtureTests.tearDownClass.__func__)

    def test_another_valid_ca_with_matching_san_is_rejected_before_credentials(self):
        # The valid cert's hostname matches; the approved bytes/hash do not.
        supplied = self.root / "valid.pem"
        approved = self.root / "wrong.pem"
        arguments = [
            "--ca",
            str(supplied),
            "--ca-sha256",
            hashlib.sha256(approved.read_bytes()).hexdigest(),
            "--expected-cluster-id",
            CLUSTER,
            "--connect-ip",
            "127.0.0.1",
            "--custody-directory",
            str(self.root),
        ]
        with (
            mock.patch.object(M, "hidden_input") as prompt,
            mock.patch.object(M, "API") as api,
        ):
            with mock.patch.object(sys, "stderr", io.StringIO()):
                self.assertEqual(M.main(arguments), 1)
            prompt.assert_not_called()
            api.assert_not_called()


if __name__ == "__main__":
    unittest.main()
