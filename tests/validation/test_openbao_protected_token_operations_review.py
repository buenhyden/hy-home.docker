"""Synthetic corrections for independent review; no HOME inputs or native APIs."""

from __future__ import annotations

import io
import json
import os
import sys
import unittest
from pathlib import Path
from unittest import mock

from tests.validation import test_openbao_protected_token_operations as fixtures

M = fixtures.M


def operator(ttl=3600):
    original = fixtures.fixtures.operator()
    return {"data": {**original["data"], "type": "service", "ttl": ttl}}


class ReviewTests(unittest.TestCase):
    setUp = fixtures.IssuanceTests.setUp
    tearDown = fixtures.IssuanceTests.tearDown

    def test_get_policy204_is_not_an_absent_policy(self):
        response = mock.Mock(status=204)
        response.read.return_value = b""
        connection = mock.Mock()
        connection.getresponse.return_value = response
        with mock.patch.object(M.BASE, "PinnedConnection", return_value=connection):
            with self.assertRaises(M.Blocked):
                M.TokenAPI(
                    fixtures.TOKEN,
                    mock.sentinel.context,
                    "127.0.0.1",
                    "issue",
                    self.policy,
                ).request("GET", M.POLICY)
        response.read.assert_not_called()

    def test_old_policy_data_list_is_sanitized_before_mutation(self):
        self.api.responses[2] = {"data": []}
        with self.assertRaises(M.Blocked):
            fixtures.IssuanceTests.issue(self)
        self.assertFalse(any(call[0] == "POST" for call in self.api.calls))

    def test_root_revocation_without_operator_is_blocked_before_post(self):
        api = fixtures.FakeAPI(
            "revoke",
            [
                fixtures.fixtures.FakeAPI().root_response,
                fixtures.fixtures.seal(),
                None,
                True,
            ],
        )
        with (
            M.OperationCustody(self.directory) as custody,
            self.assertRaises(M.Blocked),
        ):
            M.revoke_root(api, custody, fixtures.CLUSTER)
        self.assertFalse(any(call[0] == "POST" for call in api.calls))

    def test_low_recovery_operator_floor_is_blocked_before_post(self):
        api = fixtures.FakeAPI(
            "revoke",
            [
                fixtures.fixtures.FakeAPI().root_response,
                fixtures.fixtures.seal(),
                None,
                True,
            ],
        )
        normal = mock.Mock(token="independent-operator")
        normal.request.return_value = operator(599)
        with (
            M.OperationCustody(self.directory) as custody,
            self.assertRaises(M.Blocked),
        ):
            M.revoke_root(api, custody, fixtures.CLUSTER, normal)
        self.assertFalse(any(call[0] == "POST" for call in api.calls))

    def test_pre_recorded_home_identity_rejects_another_tree(self):
        with self.assertRaises(M.Blocked):
            M.Destination(
                self.home, self.home.stat().st_dev, self.home.stat().st_ino + 1
            )

    def test_issuance_operator_fd_is_rejected_before_private_input(self):
        arguments = [
            "issue-snapshot-token",
            "--ca",
            "public.pem",
            "--ca-sha256",
            "0" * 64,
            "--connect-ip",
            "127.0.0.1",
            "--expected-cluster-id",
            fixtures.CLUSTER,
            "--custody-directory",
            str(self.directory),
            "--w1-custody-directory",
            str(self.directory),
            "--root-fd",
            "99",
            "--operator-fd",
            "98",
            "--home-root",
            str(self.home),
            "--policy-sha256",
            M.POLICY_SHA256,
        ]
        with mock.patch.object(
            M.BASE, "ca_context", return_value=mock.sentinel.context
        ):
            with mock.patch.object(
                M, "root_input", return_value=fixtures.fixtures.ROOT_TOKEN
            ) as private:
                with mock.patch.object(M, "TokenAPI", return_value=self.api):
                    with (
                        mock.patch.object(sys, "stdout", io.StringIO()),
                        mock.patch.object(sys, "stderr", io.StringIO()),
                    ):
                        self.assertEqual(M.main(arguments), 1)
                private.assert_not_called()

    def test_invalid_preflight_and_postmutation_data_shapes_have_distinct_outcomes(
        self,
    ):
        for malformed in ([], None, {"data": []}, {"data": {"policy": []}}):
            with self.subTest(value=malformed), self.assertRaises(M.Blocked):
                M.policy_value(malformed)
        self.api.responses[4] = {"data": []}
        with self.assertRaises(M.Indeterminate):
            fixtures.IssuanceTests.issue(self)
        self.assertFalse(any(call[1] == M.CREATE for call in self.api.calls))

    def test_canonical_home_path_rejects_other_tree_and_lexical_alias(self):
        for path in (str(self.home) + "/", str(self.home.parent)):
            with self.subTest(path=path), self.assertRaises(M.Blocked):
                M.Destination(path, *self.home_identity)

    def test_w1_operation_destination_identities_are_distinct_before_lock_creation(
        self,
    ):
        with self.assertRaises(M.Blocked):
            M.OperationCustody(self.directory, w1_directory=self.directory)
        self.assertFalse((self.directory / ".lock").exists())
        with M.Destination(self.home, *self.home_identity) as destination:
            with self.assertRaises(M.Blocked):
                M.OperationCustody(
                    self.output, w1_directory=self.directory, destination=destination
                )
        self.assertFalse((self.output / ".lock").exists())

    def test_recovery_operator_requires_service_renewable_and_exact_floor(self):
        M.recovery_operator(operator(600))
        for data in (
            {**operator()["data"], "renewable": False},
            {**operator()["data"], "type": "batch"},
            {**operator()["data"], "ttl": True},
        ):
            with self.subTest(data=data), self.assertRaises(M.Blocked):
                M.recovery_operator({"data": data})

    def test_postrevocation_operator_failure_is_indeterminate(self):
        api = fixtures.FakeAPI(
            "revoke",
            [
                fixtures.fixtures.FakeAPI().root_response,
                fixtures.fixtures.seal(),
                None,
                True,
            ],
        )
        normal = mock.Mock(token="independent-operator")
        normal.request.side_effect = [operator(), operator(599)]
        with (
            M.OperationCustody(self.directory) as custody,
            self.assertRaises(M.Indeterminate),
        ):
            M.revoke_root(api, custody, fixtures.CLUSTER, normal)
        self.assertEqual(sum(call[1] == M.REVOKE for call in api.calls), 1)


class OperatorFDTests(unittest.TestCase):
    setUp = fixtures.CLITests.setUp
    tearDown = fixtures.CLITests.tearDown
    prepare_w1 = fixtures.CLITests.prepare_w1
    arguments = fixtures.CLITests.arguments
    run_main = fixtures.CLITests.run_main

    def prepare_operator(self, token="independent-operator"):
        path = Path(self.tmp.name) / "operator"
        path.write_text(token)
        path.chmod(0o600)
        return path

    def test_revoke_requires_independent_operator_before_and_after(self):
        w1, root = self.prepare_w1()
        path = self.prepare_operator()
        api = fixtures.FakeAPI(
            "revoke",
            [
                fixtures.fixtures.FakeAPI().root_response,
                fixtures.fixtures.seal(),
                None,
                True,
            ],
        )
        normal = mock.Mock(token="independent-operator")
        normal.request.return_value = operator()
        with root.open("rb") as root_stream, path.open("rb") as operator_stream:
            arguments = [
                *self.arguments("revoke-root", w1, root_stream.fileno()),
                "--operator-fd",
                str(operator_stream.fileno()),
            ]
            self.assertEqual(self.run_main(arguments, api, operator=normal), 0)
        self.assertEqual(normal.request.call_count, 2)
        self.assertEqual(
            json.loads((self.directory / "state.json").read_text())["state"],
            "ROOT_REVOKED_OPERATOR_HEALTHY",
        )

    def test_duplicate_fd_inode_blocks_before_any_private_input(self):
        w1, root = self.prepare_w1()
        with root.open("rb") as stream:
            duplicate = os.dup(stream.fileno())
            try:
                arguments = [
                    *self.arguments("revoke-root", w1, stream.fileno()),
                    "--operator-fd",
                    str(duplicate),
                ]
                with mock.patch.object(M, "root_input") as private:
                    self.assertEqual(self.run_main(arguments, self.api), 1)
                private.assert_not_called()
            finally:
                os.close(duplicate)
        self.assertEqual(self.api.calls, [])

    def test_different_fd_inode_with_same_root_contents_cannot_revoke(self):
        w1, root = self.prepare_w1()
        path = self.prepare_operator(fixtures.fixtures.ROOT_TOKEN)
        with root.open("rb") as root_stream, path.open("rb") as operator_stream:
            arguments = [
                *self.arguments("revoke-root", w1, root_stream.fileno()),
                "--operator-fd",
                str(operator_stream.fileno()),
            ]
            self.assertEqual(self.run_main(arguments, self.api), 1)
        self.assertEqual(self.api.calls, [])


if __name__ == "__main__":
    unittest.main()
