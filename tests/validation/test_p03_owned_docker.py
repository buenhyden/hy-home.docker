"""Offline authority tests for the P03 owned Docker boundary."""

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from tests.validation._p03_owned_docker import (
    NativeFixtureError,
    OwnedDocker,
    _PerCallDockerClient,
)
from tests.validation.test_datastore_rehearsal_boundary import DockerClientBoundary


class _FakeDockerClient:
    def __init__(self, boundary):
        self.boundary = boundary
        self.resources = {kind: {} for kind in ("container", "network", "volume")}
        self.cleanup_started = False

    def begin_cleanup(self):
        self.cleanup_started = True

    def add(self, kind, name):
        identity = name if kind == "volume" else f"{kind}-id-{name}"
        self.resources[kind][name] = identity
        return identity

    def item(self, kind, identity):
        match = next(
            (
                (name, stored)
                for name, stored in self.resources[kind].items()
                if identity in {name, stored}
            ),
            None,
        )
        if match is None:
            return None
        name, stored = match
        labels = {
            self.boundary.OWNER_KEY: self.boundary.OWNER,
            self.boundary.ATTEMPT_KEY: self.boundary.prefix,
        }
        if kind == "container":
            return {"Id": stored, "Name": "/" + name, "Config": {"Labels": labels}}
        return {"Id": stored, "Name": name, "Labels": labels}

    def remove(self, kind, identity):
        for name, stored in tuple(self.resources[kind].items()):
            if identity in {name, stored}:
                self.resources[kind].pop(name)

    def run_result_with_timeout(self, _timeout, *arguments):
        output = ""
        if arguments[:2] == ("network", "create"):
            output = self.add("network", arguments[-1])
        elif arguments[:2] == ("volume", "create"):
            output = self.add("volume", arguments[-1])
        elif arguments[0] == "create":
            name = arguments[arguments.index("--name") + 1]
            output = self.add("container", name)
        elif arguments[0] == "inspect":
            output = json.dumps([self.item("container", arguments[-1])])
        elif arguments[0] in {"network", "volume"} and arguments[1] == "inspect":
            output = json.dumps([self.item(arguments[0], arguments[-1])])
        elif arguments[:3] == ("ps", "-aq", "--no-trunc"):
            output = "\n".join(self.resources["container"].values())
        elif arguments[0] in {"network", "volume"} and arguments[1:3] == (
            "ls",
            "-q",
        ):
            kind = arguments[0]
            values = (
                self.resources[kind].keys()
                if kind == "volume"
                else self.resources[kind].values()
            )
            output = "\n".join(values)
        elif arguments[0] == "rm":
            self.remove("container", arguments[-1])
        elif arguments[0] in {"network", "volume"} and arguments[1] == "rm":
            self.remove(arguments[0], arguments[-1])
        return subprocess.CompletedProcess(
            arguments, 0, output + ("\n" if output else ""), ""
        )


class OwnedDockerSourceTests(unittest.TestCase):
    def test_engine_initialization_uses_fixed_client_and_exact_context(self):
        boundary = OwnedDocker("p03-test-engine-init")
        client = Mock()
        client.run_result_with_timeout.side_effect = (
            subprocess.CompletedProcess([], 0, "default\n", ""),
            subprocess.CompletedProcess([], 0, "engine-id|28.5.1\n", ""),
        )
        with patch(
            "tests.validation._p03_owned_docker._PerCallDockerClient",
            return_value=client,
        ) as constructor:
            boundary._initialize_client()
        kwargs = constructor.call_args.kwargs
        self.assertEqual(kwargs["binary"], Path("/usr/bin/docker"))
        self.assertEqual(kwargs["socket_path"], Path("/var/run/docker.sock"))
        self.assertEqual(kwargs["config_dir"].stat().st_mode & 0o777, 0o700)
        self.assertEqual(kwargs["deadline_seconds"], 20 * 60)
        boundary._client = None
        boundary._cleanup_config()

    def test_engine_verification_refuses_overrides_and_cleans_failed_init(self):
        boundary = OwnedDocker("p03-test-engine-refusal")
        with patch.dict(os.environ, {"DOCKER_HOST": "tcp://external"}, clear=True):
            with self.assertRaisesRegex(
                NativeFixtureError, "docker_environment_refused"
            ):
                boundary.verify_local_engine()

        boundary = OwnedDocker("p03-test-engine-failure")
        boundary._acquire_lock = Mock()
        boundary._initialize_client = Mock(
            side_effect=NativeFixtureError("docker_unavailable")
        )
        boundary._release_lock = Mock()
        with (
            patch.dict(os.environ, {}, clear=True),
            self.assertRaisesRegex(NativeFixtureError, "docker_unavailable"),
        ):
            boundary.verify_local_engine()
        boundary._release_lock.assert_called_once_with()

    def test_per_call_client_caps_parent_deadline_and_resets_state(self):
        client = object.__new__(_PerCallDockerClient)
        client._requested_timeout = 1.25
        with patch.object(DockerClientBoundary, "_remaining_timeout", return_value=50):
            self.assertEqual(client._remaining_timeout(), 1.25)
        client._requested_timeout = None
        client.run_result = Mock(
            return_value=subprocess.CompletedProcess([], 0, "ok", "")
        )
        self.assertEqual(client.run_result_with_timeout(2, "info").stdout, "ok")
        self.assertIsNone(client._requested_timeout)
        for invalid in (True, 0, float("nan"), 301):
            with (
                self.subTest(invalid=invalid),
                self.assertRaisesRegex(NativeFixtureError, "docker_timeout_invalid"),
            ):
                client.run_result_with_timeout(invalid, "info")

    def test_image_cache_distinguishes_missing_permission_and_unavailable(self):
        boundary = OwnedDocker("p03-test-image-cache")
        boundary._client = Mock()
        outcomes = (
            (subprocess.CompletedProcess([], 0, "sha256:x", ""), True),
            (subprocess.CompletedProcess([], 1, "", "No such image"), False),
        )
        for completed, expected in outcomes:
            boundary._client.run_result_with_timeout.return_value = completed
            self.assertEqual(boundary.image_cached("synthetic:image"), expected)
        for stderr, code in (
            ("permission denied", "docker_permission"),
            ("daemon unavailable", "docker_unavailable"),
        ):
            boundary._client.run_result_with_timeout.return_value = (
                subprocess.CompletedProcess([], 1, "", stderr)
            )
            with self.assertRaisesRegex(NativeFixtureError, code):
                boundary.image_cached("synthetic:image")

    def test_private_config_cleanup_and_unverified_resource_refusal(self):
        boundary = OwnedDocker("p03-test-config-cleanup")
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / "config"
            config.mkdir(mode=0o700)
            metadata = config.stat(follow_symlinks=False)
            boundary._config = config
            boundary._config_identity = (
                metadata.st_dev,
                metadata.st_ino,
                metadata.st_uid,
            )
            boundary.cleanup()
            self.assertFalse(config.exists())

        refused = OwnedDocker("p03-test-unverified")
        refused.pending["volume"].add("pending")
        with self.assertRaisesRegex(NativeFixtureError, "docker_boundary_unverified"):
            refused.cleanup()

    def test_nonzero_client_result_is_value_free_and_classified(self):
        boundary = OwnedDocker("p03-test-client-result")
        boundary._client = Mock()
        for stderr, code in (
            ("permission denied SENSITIVE", "docker_permission"),
            ("other failure SENSITIVE", "docker_failed"),
        ):
            boundary._client.run_result_with_timeout.return_value = (
                subprocess.CompletedProcess([], 1, "", stderr)
            )
            with self.assertRaises(NativeFixtureError) as raised:
                boundary.command("inspect", "SENSITIVE")
            self.assertEqual(str(raised.exception), code)
            self.assertNotIn("SENSITIVE", str(raised.exception))

    def test_create_inspect_and_cleanup_use_exact_owned_identities(self):
        boundary = OwnedDocker("p03-test-owned-lifecycle")
        client = _FakeDockerClient(boundary)
        boundary._client = client

        network_id = boundary.create_network(boundary.prefix + "-net")
        volume_id = boundary.create_volume(boundary.prefix + "-volume")
        container_id = boundary.create_container(
            boundary.prefix + "-container",
            "--pull=never",
            "synthetic:image",
        )

        self.assertEqual(
            boundary.container_id(boundary.prefix + "-container"), container_id
        )
        self.assertTrue(network_id.startswith("network-id-"))
        self.assertEqual(volume_id, boundary.prefix + "-volume")
        boundary.cleanup()
        self.assertTrue(client.cleanup_started)
        self.assertTrue(all(not values for values in client.resources.values()))
        self.assertTrue(all(not values for values in boundary.records.values()))

    def test_cleanup_adopts_late_labeled_resources_before_removal(self):
        boundary = OwnedDocker("p03-test-owned-adoption")
        client = _FakeDockerClient(boundary)
        boundary._client = client
        for kind in ("container", "network", "volume"):
            name = boundary.prefix + "-" + kind
            client.add(kind, name)
            boundary.pending[kind].add(name)

        boundary.cleanup()

        self.assertTrue(all(not values for values in client.resources.values()))
        self.assertTrue(all(not values for values in boundary.pending.values()))

    def test_metadata_label_and_missing_record_fail_closed(self):
        boundary = OwnedDocker("p03-test-owned-refusal")
        with self.assertRaisesRegex(
            NativeFixtureError, "owned_resource_labels_changed"
        ):
            boundary._validate_labels({})
        with self.assertRaisesRegex(
            NativeFixtureError, "owned_container_record_missing"
        ):
            boundary.container_id("missing")
        boundary.command = Mock(return_value="not-json")
        with self.assertRaisesRegex(
            NativeFixtureError, "owned_resource_metadata_invalid"
        ):
            boundary._inspect_json("container", "missing")

    def test_command_forwards_the_declared_per_call_timeout(self):
        boundary = OwnedDocker("p03-test-timeout")
        boundary._client = Mock()
        boundary._client.run_result_with_timeout.return_value = Mock(
            returncode=0, stdout="ok\n", stderr=""
        )

        self.assertEqual(boundary.command("inspect", "synthetic", timeout=1.25), "ok")

        boundary._client.run_result_with_timeout.assert_called_once_with(
            1.25, "inspect", "synthetic"
        )

    def test_client_timeout_is_normalized_without_command_values(self):
        boundary = OwnedDocker("p03-test-timeout-value")
        boundary._client = Mock()
        boundary._client.run_result_with_timeout.side_effect = (
            subprocess.TimeoutExpired(
                ["docker", "--password", "SENSITIVE-SENTINEL"], 0.1
            )
        )

        with self.assertRaises(NativeFixtureError) as raised:
            boundary.command("inspect", "SENSITIVE-SENTINEL", timeout=0.1)

        self.assertEqual(str(raised.exception), "docker_unavailable")
        self.assertNotIn("SENSITIVE-SENTINEL", str(raised.exception))

    def test_container_create_requires_exact_pull_never(self):
        boundary = OwnedDocker("p03-test-pull-policy")
        for arguments in (
            ("synthetic:image",),
            ("--pull=always", "synthetic:image"),
            ("--pull=never", "--pull=always", "synthetic:image"),
            ("--pull=never", "--pull", "always", "synthetic:image"),
        ):
            with (
                self.subTest(arguments=arguments),
                self.assertRaisesRegex(
                    NativeFixtureError, "container_pull_policy_refused"
                ),
            ):
                boundary.create_container("p03-test-container", *arguments)

    def test_container_create_injects_owner_security_and_resource_bounds(self):
        boundary = OwnedDocker("p03-test-create-policy")
        boundary.command = Mock(return_value="a" * 64)
        boundary._inspect_json = Mock(
            return_value={
                "Id": "a" * 64,
                "Name": "/p03-test-container",
                "Config": {
                    "Labels": {
                        boundary.OWNER_KEY: boundary.OWNER,
                        boundary.ATTEMPT_KEY: boundary.prefix,
                    }
                },
            }
        )

        boundary.create_container(
            "p03-test-container", "--pull=never", "synthetic:image"
        )

        arguments = boundary.command.call_args.args
        self.assertIn("--pull=never", arguments)
        self.assertIn("no-new-privileges=true", arguments)
        self.assertIn("--memory", arguments)
        self.assertIn("--pids-limit", arguments)
