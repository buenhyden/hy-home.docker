"""Synthetic W1c renderer role apply; never use HOME credentials or endpoints."""

from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tests.validation import test_openbao_protected_maintenance as fixtures

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "infra/03-security/openbao/scripts/protected-renderer-roles.py"
SPEC = importlib.util.spec_from_file_location("protected_renderer_roles", SOURCE)
M = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = M
SPEC.loader.exec_module(M)

CLUSTER = fixtures.CLUSTER
APPROLE = "auth/approle/role/hy-home-renderer"
OLD_IMAGE = "sha256:11fd73a2102cda9c55d5d881a8c3210303146a7ec1e8ac76f526e175c6d24641"


def plan():
    return M.targets(ROOT)


class FakeAPI:
    """Root and seal, one prior read per target, then one POST and one read each."""

    def __init__(self, prior=None, after=None):
        self.calls = []
        self.plan = plan()
        prior = prior or {}
        after = after or {}
        self.responses = [fixtures.FakeAPI().root_response, fixtures.seal()]
        for path, _document, _readback in self.plan:
            self.responses.append(prior.get(path, self.stored(path, None)))
        for path, document, readback in self.plan:
            self.responses.append(None)
            self.responses.append(
                after.get(path, self.stored(path, M.wanted(document, readback)))
            )

    @staticmethod
    def stored(path, value):
        if path == APPROLE and value is None:
            value = {"bind_secret_id": True, "token_policies": ["renderer"]}
        if value is None:
            return None
        if isinstance(value, str):
            return {"data": {"policy": value}}
        return {"data": {**value, "unrelated": "kept by server"}}

    def request(self, method, path, document=None):
        self.calls.append((method, path, document))
        value = self.responses.pop(0)
        if isinstance(value, BaseException):
            raise value
        return value


class SourceTests(unittest.TestCase):
    def test_targets_are_the_tracked_reviewed_files_in_write_order(self):
        paths = [path for path, _document, _readback in plan()]
        self.assertEqual(
            paths,
            [
                "sys/policies/acl/renderer",
                "sys/policies/acl/renderer-issuer",
                "sys/policies/acl/renderer-cleanup",
                "sys/policies/acl/hy-home-operator",
                "auth/token/roles/renderer-issuer",
                "auth/token/roles/renderer-cleanup",
                APPROLE,
            ],
        )
        config = ROOT / M.CONFIG
        for _name, source, digest in (*M.POLICIES, *M.TOKEN_ROLES, M.APPROLE):
            self.assertEqual(
                hashlib.sha256((config / source).read_bytes()).hexdigest(), digest
            )

    def test_role_readback_converts_durations_and_keeps_exact_policies(self):
        targets = {path: readback for path, _document, readback in plan()}
        issuer = targets["auth/token/roles/renderer-issuer"]
        self.assertEqual(issuer["token_explicit_max_ttl"], 300)
        self.assertEqual(issuer["allowed_policies"], ["renderer-issuer"])
        self.assertIs(issuer["renewable"], False)
        self.assertEqual(targets[APPROLE]["secret_id_ttl"], 600)
        self.assertEqual(targets[APPROLE]["token_max_ttl"], 0)
        # A periodic token renews without re-login; the SecretID is single use.
        self.assertEqual(targets[APPROLE]["token_period"], 86400)
        self.assertEqual(targets[APPROLE]["token_policies"], ["renderer"])

    def test_changed_source_bytes_block(self):
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / M.CONFIG
            for _name, source, _digest in (*M.POLICIES, *M.TOKEN_ROLES, M.APPROLE):
                target = config / source
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes((ROOT / M.CONFIG / source).read_bytes())
            (config / "policies/renderer-issuer.hcl").write_text('path "*" {}\n')
            with self.assertRaises(M.OPS.BindingBlocked):
                M.targets(directory)

    def test_unreviewed_role_fields_are_written_at_their_defaults(self):
        targets = {path: document for path, document, _readback in plan()}
        issuer = targets["auth/token/roles/renderer-issuer"]
        self.assertEqual(issuer["token_period"], 0)
        self.assertEqual(issuer["token_bound_cidrs"], [])
        self.assertEqual(issuer["disallowed_policies"], [])
        self.assertEqual(targets[APPROLE]["token_period"], "24h")
        self.assertEqual(targets[APPROLE]["secret_id_bound_cidrs"], [])
        self.assertEqual(targets[APPROLE]["token_policies"], ["renderer"])

    def test_token_operations_binding_is_hash_pinned(self):
        with mock.patch.object(M, "TOKEN_OPERATIONS_SHA256", "0" * 64):
            with self.assertRaises(ValueError):
                M.load_token_operations()


class ApplyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.directory = Path(self.tmp.name) / "operation"
        self.directory.mkdir(mode=0o700)

    def tearDown(self):
        self.tmp.cleanup()

    def apply(self, api, directory=None):
        with M.RoleCustody(directory or self.directory) as custody:
            return M.apply_roles(api, custody, CLUSTER, api.plan)

    def files(self):
        return sorted(path.name for path in self.directory.iterdir())

    def test_success_writes_each_target_once_and_a_value_free_receipt(self):
        api = FakeAPI(prior={"sys/policies/acl/renderer": {"data": {"policy": "old"}}})
        self.assertEqual(self.apply(api), "RENDERER_ROLES_APPLIED")
        posts = [call for call in api.calls if call[0] == "POST"]
        self.assertEqual([call[1] for call in posts], [path for path, *_ in api.plan])
        self.assertEqual(
            [call[2] for call in posts], [doc for _path, doc, _rb in api.plan]
        )
        state = json.loads((self.directory / "state.json").read_text())
        self.assertEqual(state["state"], "RENDERER_ROLES_APPLIED")
        changed = {item["path"]: item["changed"] for item in state["targets"]}
        self.assertTrue(changed["sys/policies/acl/renderer"])
        self.assertTrue(changed["auth/token/roles/renderer-issuer"])
        prior = json.loads((self.directory / "prior-state.json").read_text())
        self.assertEqual(prior["sys/policies/acl/renderer"], "old")
        self.assertIsNone(prior["auth/token/roles/renderer-issuer"])
        for name in self.files():
            self.assertNotIn(fixtures.ROOT_TOKEN, (self.directory / name).read_text())

    def test_missing_approle_blocks_before_any_write(self):
        api = FakeAPI()
        api.responses[2 + [path for path, *_ in api.plan].index(APPROLE)] = None
        with self.assertRaises(M.Blocked):
            self.apply(api)
        self.assertFalse(any(call[0] == "POST" for call in api.calls))
        self.assertEqual(self.files(), [".lock"])

    def test_non_root_or_wrong_cluster_blocks_before_target_reads(self):
        for position, value in (
            (0, {"data": {"policies": ["default"]}}),
            (1, {**fixtures.seal(), "cluster_id": "x"}),
        ):
            with self.subTest(position=position):
                api = FakeAPI()
                api.responses[position] = value
                directory = Path(self.tmp.name) / str(position)
                directory.mkdir(mode=0o700)
                with self.assertRaises(M.Blocked):
                    self.apply(api, directory)
                self.assertEqual(len(api.calls), position + 1)

    def test_readback_difference_stops_and_keeps_prior_state(self):
        path = "sys/policies/acl/renderer-issuer"
        api = FakeAPI(after={path: {"data": {"policy": "changed"}}})
        with self.assertRaises(M.Indeterminate):
            self.apply(api)
        posts = [call[1] for call in api.calls if call[0] == "POST"]
        self.assertEqual(posts[-1], path)
        self.assertNotIn("sys/policies/acl/renderer-cleanup", posts)
        self.assertIn("prior-state.json", self.files())
        self.assertNotIn("state.json", self.files())

    def test_plan_reads_every_target_and_writes_nothing(self):
        api = FakeAPI(prior={"sys/policies/acl/renderer": {"data": {"policy": "old"}}})
        with M.RoleCustody(self.directory) as custody:
            result = M.apply_roles(api, custody, CLUSTER, api.plan, write=False)
        self.assertEqual(result, "RENDERER_ROLES_PLANNED")
        self.assertFalse(any(call[0] == "POST" for call in api.calls))
        self.assertEqual(len(api.calls), 2 + len(api.plan))
        state = json.loads((self.directory / "state.json").read_text())
        changed = {item["path"]: item["changed"] for item in state["targets"]}
        self.assertTrue(changed["sys/policies/acl/renderer"])
        self.assertEqual(self.files(), [".lock", "prior-state.json", "state.json"])

    def test_write_failure_is_indeterminate_and_never_retried(self):
        api = FakeAPI()
        api.responses[2 + len(api.plan)] = M.Indeterminate()
        with self.assertRaises(M.Indeterminate):
            self.apply(api)
        self.assertEqual(sum(call[0] == "POST" for call in api.calls), 1)


class RequestTests(unittest.TestCase):
    def api(self):
        documents = ((path, document) for path, document, _readback in plan())
        return M.RoleAPI(
            fixtures.ROOT_TOKEN, mock.sentinel.context, "127.0.0.1", documents
        )

    def test_only_fixed_paths_and_reviewed_bodies_are_allowed(self):
        api = self.api()
        policy = plan()[1][0]
        with mock.patch.object(M.BASE, "PinnedConnection") as connection:
            for method, path, document in (
                ("POST", "sys/policies/acl/root", {"policy": "x"}),
                ("POST", policy, {"policy": 'path "*" { capabilities = ["sudo"] }'}),
                ("GET", "secret/data/hy-home/02-auth/keycloak", None),
                ("DELETE", policy, None),
                ("GET", policy, {}),
            ):
                with self.subTest(method=method, path=path):
                    with self.assertRaises(M.Blocked):
                        api.request(method, path, document)
            connection.assert_not_called()

    def test_plan_identity_refuses_every_write(self):
        documents = [(path, document) for path, document, _readback in plan()]
        api = M.RoleAPI(
            fixtures.ROOT_TOKEN,
            mock.sentinel.context,
            "127.0.0.1",
            documents,
            write=False,
        )
        with mock.patch.object(M.BASE, "PinnedConnection") as connection:
            with self.assertRaises(M.Blocked):
                api.request("POST", documents[0][0], documents[0][1])
            connection.assert_not_called()

    def test_changed_config_reports_blocked_not_a_traceback(self):
        arguments = [
            "apply",
            "--ca",
            "x",
            "--ca-sha256",
            "0" * 64,
            "--connect-ip",
            "127.0.0.1",
            "--expected-cluster-id",
            CLUSTER,
            "--custody-directory",
            "a",
            "--w1-custody-directory",
            "b",
            "--root-fd",
            "5",
        ]
        with (
            mock.patch.object(M.BASE, "ca_context"),
            mock.patch.object(M, "targets", side_effect=M.OPS.BindingBlocked()),
            mock.patch("sys.stderr"),
        ):
            self.assertEqual(M.main(arguments), 1)

    def test_main_blocks_bad_inputs_without_network(self):
        common = ["--ca", "x", "--ca-sha256", "0", "--connect-ip", "127.0.0.1"]
        rest = ["--custody-directory", "a", "--w1-custody-directory", "b"]
        with mock.patch.object(M.BASE, "PinnedConnection") as connection:
            for cluster, descriptor in (("bad", "5"), (CLUSTER, "1")):
                arguments = [
                    "apply",
                    *common,
                    "--expected-cluster-id",
                    cluster,
                    *rest,
                    "--root-fd",
                    descriptor,
                ]
                with self.subTest(cluster=cluster), mock.patch("sys.stderr"):
                    self.assertEqual(M.main(arguments), 1)
            connection.assert_not_called()


@unittest.skipUnless(
    os.environ.get("HYHOME_OPENBAO_REHEARSAL") == "1",
    "opt-in native rehearsal on an owned synthetic OpenBao server",
)
class NativeRehearsalTests(unittest.TestCase):
    """Real server and real tool; only the fixture name and port replace HOME's."""

    def setUp(self):
        from tests.validation import _openbao_rehearsal_fixture as native

        self.native = native
        self.work = tempfile.TemporaryDirectory()
        self.addCleanup(self.work.cleanup)

    def ok(self, client, method, path, payload=None, **kwargs):
        status, body = client.api(method, path, payload, **kwargs)
        self.assertIn(status, (200, 204), "synthetic setup request failed")
        return body

    def custody(self, client):
        work = Path(self.work.name)
        w1 = work / "w1"
        if not w1.exists():
            w1.mkdir(mode=0o700)
            for name, value in (
                ("root.token", client.token),
                (
                    "state.json",
                    json.dumps({"state": "DELIVERED", "operator_healthy": True}),
                ),
            ):
                descriptor = os.open(
                    w1 / name, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600
                )
                os.write(descriptor, value.encode())
                os.close(descriptor)
        operation = Path(tempfile.mkdtemp(dir=work))
        operation.chmod(0o700)
        return w1, operation

    def run_tool(self, client, cluster, operation_name="apply"):
        w1, operation = self.custody(client)
        ca = self.fixture.tls / "ca.pem"
        root_fd = os.open(w1 / "root.token", os.O_RDONLY)
        self.addCleanup(os.close, root_fd)
        original = M.BASE.PinnedConnection
        port = self.native.PORT

        def fixture_port(host, _port, **kwargs):
            return original(host, port, **kwargs)

        output = io.StringIO()
        with (
            mock.patch.object(M.BASE, "HOST", "openbao"),
            mock.patch.object(M.BASE, "PinnedConnection", fixture_port),
            mock.patch("sys.stdout", output),
        ):
            code = M.main(
                [
                    operation_name,
                    "--ca",
                    str(ca),
                    "--ca-sha256",
                    hashlib.sha256(ca.read_bytes()).hexdigest(),
                    "--connect-ip",
                    client.target,
                    "--expected-cluster-id",
                    cluster,
                    "--custody-directory",
                    str(operation),
                    "--w1-custody-directory",
                    str(w1),
                    "--root-fd",
                    str(root_fd),
                ]
            )
        result = "RENDERER_ROLES_" + (
            "APPLIED" if operation_name == "apply" else "PLANNED"
        )
        self.assertEqual((code, output.getvalue()), (0, result + "\n"))
        return operation

    def test_native_apply_on_the_owned_candidate_image(self):
        self.rehearse(self.native.OwnedFixture())

    def test_native_apply_on_the_running_home_image(self):
        # W1c runs before W4, so HOME's current server version receives it.
        fixture = self.native.OwnedFixture(
            image=OLD_IMAGE, version="2.6.2", image_reference="openbao/openbao:2.6.2"
        )
        self.rehearse(fixture)

    def rehearse(self, fixture):
        self.fixture = fixture
        self.addCleanup(fixture.cleanup)
        self.fixture.prepare()
        _name, client = self.fixture.server("roles")
        client.initialize()
        cluster = self.ok(client, "GET", "sys/seal-status")["cluster_id"]
        self.ok(client, "POST", "sys/auth/approle", {"type": "approle"})
        self.ok(client, "POST", "sys/policies/acl/renderer", {"policy": "# stale\n"})
        self.ok(
            client,
            "POST",
            APPROLE,
            {"token_policies": ["renderer"], "secret_id_ttl": "1h"},
        )
        role_id = self.ok(client, "GET", APPROLE + "/role-id")["data"]["role_id"]

        planned = self.run_tool(client, cluster, "plan")
        state = json.loads((planned / "state.json").read_text())
        self.assertTrue(all(item["changed"] for item in state["targets"]))
        self.assertEqual(
            self.ok(client, "GET", "sys/policies/acl/renderer")["data"]["policy"],
            "# stale\n",
        )
        status, _body = client.api("GET", "auth/token/roles/renderer-issuer")
        self.assertEqual(status, 404)

        first = self.run_tool(client, cluster)
        state = json.loads((first / "state.json").read_text())
        changed = {item["path"]: item["changed"] for item in state["targets"]}
        self.assertTrue(all(changed.values()))
        prior = json.loads((first / "prior-state.json").read_text())
        self.assertEqual(prior["sys/policies/acl/renderer"], "# stale\n")
        self.assertIsNone(prior["auth/token/roles/renderer-issuer"])
        self.assertEqual(prior[APPROLE]["secret_id_ttl"], 3600)
        self.assertEqual(
            self.ok(client, "GET", APPROLE + "/role-id")["data"]["role_id"], role_id
        )

        # An operator-policy token, not root, makes the W5 request through each role.
        operator = self.ok(
            client,
            "POST",
            "auth/token/create",
            {"policies": ["hy-home-operator"], "ttl": "10m"},
        )["auth"]["client_token"]
        for role in ("renderer-issuer", "renderer-cleanup"):
            issued = self.ok(
                client,
                "POST",
                "auth/token/create/" + role,
                token=operator,
                payload={
                    "policies": role,  # RUN-0085 W5 sends the exact string.
                    "renewable": False,
                    "no_default_policy": True,
                    "ttl": "5m",
                    "explicit_max_ttl": "5m",
                },
            )["auth"]
            self.assertEqual(issued["policies"], [role])
            self.assertIs(issued["renewable"], False)
            self.assertEqual(issued["lease_duration"], 300)
            data = self.ok(
                client, "GET", "auth/token/lookup-self", token=issued["client_token"]
            )["data"]
            self.assertEqual(data["path"], "auth/token/create/" + role)
            self.assertEqual(data["explicit_max_ttl"], 300)
            if role == "renderer-issuer":
                issuer = issued["client_token"]
        # The operator policy refuses any other parameters through the role.
        status, _body = client.api(
            "POST",
            "auth/token/create/renderer-issuer",
            {
                "policies": "renderer-issuer",
                "renewable": False,
                "no_default_policy": True,
                "ttl": "1h",
                "explicit_max_ttl": "1h",
            },
            token=operator,
        )
        self.assertNotIn(status, (200, 204))
        wrapped = self.ok(
            client,
            "POST",
            APPROLE + "/secret-id",
            {},
            token=issuer,
            headers={"X-Vault-Wrap-TTL": "60s"},
        )
        self.assertIn("token", wrapped["wrap_info"])
        status, _body = client.api("POST", APPROLE + "/secret-id", {}, token=issuer)
        self.assertNotIn(status, (200, 204))

        second = self.run_tool(client, cluster)
        state = json.loads((second / "state.json").read_text())
        self.assertFalse(any(item["changed"] for item in state["targets"]))


if __name__ == "__main__":
    unittest.main()
