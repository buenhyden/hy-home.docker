"""Docker-free guards for the bounded n8n native rehearsal."""

from __future__ import annotations

import json
import subprocess
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

from tests.validation import _opsflow_native_ownership as ownership
from tests.validation import test_opsflow_native_rehearsal as native_driver
from tests.validation._opsflow_native_fixture import (
    NativeFixture,
    RehearsalFailure,
)
from tests.validation._opsflow_native_inputs import (
    ALIASES,
    ATTEMPT_LABEL,
    IMAGE_IDS,
    MAILPIT_ID,
    N8N_ID,
    N8N_REF,
    OWNER,
    OWNER_LABEL,
    RESOURCE_CAPS,
    ROLE_LABEL,
    precreate_headroom_failure,
)
from tests.validation._opsflow_native_ownership import (
    Container,
    Network,
    main_readiness_failure_facts,
    network_attachment_matches,
    none_network_facts,
    ordinary_network_facts,
    security_contract_facts,
    security_contract_matches,
)


class NativeGuardTests(unittest.TestCase):
    def test_n8n_entrypoint_contract_matches_fixture_mounts_and_broker(self):
        entrypoint = Path("infra/07-workflow/n8n/docker-entrypoint.sh").read_text()
        self.assertIn("require_secret /run/secrets/n8n_db_password", entrypoint)
        self.assertIn("require_secret /run/secrets/n8n_encryption_key", entrypoint)
        self.assertIn("require_secret /run/secrets/n8n_runner_auth_token", entrypoint)
        self.assertIn("n8n-valkey:n8n_valkey_password", entrypoint)

        fixture = object.__new__(NativeFixture)
        calls = []
        fixture.create = lambda *args, **kwargs: calls.append((args, kwargs))
        fixture.start = mock.Mock()
        fixture.wait_until = mock.Mock()
        synthetic = {
            key: ("withheld", Path("/owned") / f"{key}.secret")
            for key in ("metadata_n8n", "valkey_n8n", "encryption", "runner")
        }
        fixture.start_n8n(synthetic)

        self.assertEqual([args[0] for args, _ in calls], ["main", "worker"])
        self.assertEqual(ALIASES["valkey"], "n8n-valkey")
        for _, kwargs in calls:
            env = dict(value.split("=", 1) for value in kwargs["env"])
            targets = {
                mount.split("dst=", 1)[1].split(",", 1)[0] for mount in kwargs["mounts"]
            }
            self.assertEqual(
                targets,
                {
                    "/run/secrets/n8n_db_password",
                    "/run/secrets/n8n_valkey_password",
                    "/run/secrets/n8n_encryption_key",
                    "/run/secrets/n8n_runner_auth_token",
                },
            )
            self.assertEqual(env["N8N_VALKEY_HOST"], "n8n-valkey")
            self.assertEqual(env["N8N_VALKEY_SECRET"], "n8n_valkey_password")
            self.assertEqual(env["QUEUE_BULL_REDIS_HOST"], "n8n-valkey")
            self.assertNotIn("N8N_CUSTOM_EXTENSIONS", env)
            self.assertNotIn("N8N_RUNNERS_ENABLED", env)
            self.assertEqual(env["N8N_LOG_LEVEL"], "debug")
            self.assertEqual(
                env["QUEUE_BULL_REDIS_PASSWORD_FILE"],
                "/run/secrets/n8n_valkey_password",
            )
            self.assertEqual(env["N8N_USER_FOLDER"], "/tmp")

    def test_main_readiness_failure_facts_are_closed_booleans(self):
        record = Container(
            "d" * 64,
            "owned-main",
            "main",
            1,
            N8N_ID,
            N8N_REF,
            "1000:1000",
            ("ctl",),
            (),
            (),
        )
        metadata = json.dumps(
            [
                {
                    "Id": record.cid,
                    "Name": "/" + record.name,
                    "Config": {
                        "Labels": {
                            OWNER_LABEL: OWNER,
                            ATTEMPT_LABEL: "opsflow-native-" + "b" * 24,
                            ROLE_LABEL: record.role,
                            "hyhome.opsflow.native-generation": "1",
                            "hyhome.opsflow.native-image-ref": N8N_REF,
                        }
                    },
                    "State": {
                        "Status": "exited",
                        "ExitCode": 1,
                        "OOMKilled": False,
                    },
                }
            ]
        )
        client = mock.Mock()
        client.run_result.side_effect = [
            subprocess.CompletedProcess([], 0, metadata, ""),
            subprocess.CompletedProcess(
                [],
                0,
                "Starting migration Example\nThere was an error initializing DB\n",
                "password authentication failed for user withheld\n"
                "EACCES: permission denied, read-only file system\n",
            ),
        ]
        facts = main_readiness_failure_facts(
            client, record, "opsflow-native-" + "b" * 24
        )
        self.assertEqual(
            {
                "inspect_available": True,
                "state_created": False,
                "state_running": False,
                "state_exited": True,
                "state_restarting": False,
                "exit_zero": False,
                "exit_nonzero": True,
                "oom_killed": False,
                "logs_available": True,
                "log_ready": False,
                "log_migration_started": True,
                "log_migration_finished": False,
                "log_version": False,
                "log_db_init_error": True,
                "log_db_auth_error": True,
                "log_encryption_error": False,
                "log_permission_error": True,
            },
            facts,
        )
        self.assertTrue(all(isinstance(value, bool) for value in facts.values()))

    def test_readiness_facts_read_the_whole_log_and_retain_the_tail(self):
        # The listener line comes first; a fresh database then writes hundreds
        # of migration lines, so it is absent from the last 200.
        whole = (
            "n8n ready on ::, port 5678\n"
            + "Starting migration X\nFinished migration X\n" * 150
            + "Version: 2.43.6\n"
        )
        tail = subprocess.CompletedProcess([], 0, "Finished migration X\n", "")
        client = mock.Mock()
        client.run_result.side_effect = [
            tail,
            subprocess.CompletedProcess([], 0, whole, ""),
        ]
        retained = []
        with mock.patch.object(
            ownership,
            "inspect_container_identity",
            return_value={"State": {"Status": "running"}},
        ):
            facts = ownership.main_readiness_failure_facts(
                client, mock.Mock(cid="c" * 64), "a", retained.append
            )
        self.assertEqual([tail], retained)
        self.assertEqual("--tail", client.run_result.call_args_list[0].args[1])
        self.assertNotIn("--tail", client.run_result.call_args_list[1].args)
        self.assertTrue(facts["log_ready"])
        self.assertTrue(facts["log_version"])

        # A failed whole-log read still keeps the retained tail.
        client.run_result.side_effect = [tail, TimeoutError()]
        retained.clear()
        with mock.patch.object(
            ownership,
            "inspect_container_identity",
            return_value={"State": {"Status": "running"}},
        ):
            facts = ownership.main_readiness_failure_facts(
                client, mock.Mock(cid="c" * 64), "a", retained.append
            )
        self.assertEqual([tail], retained)
        self.assertFalse(facts["logs_available"])

    def test_precreate_headroom_records_low_swap_without_using_it_as_admission(self):
        gib = 1024**3
        mib = 1024**2
        self.assertIsNone(precreate_headroom_failure(8 * mib, 0, 12 * gib, 20, 4))
        for inputs in (
            (6 * mib, 2 * mib, 12 * gib, 20, 4),
            (8 * mib, 2 * mib, 9 * gib, 20, 4),
            (8 * mib, 2 * mib, 12 * gib, 9, 4),
            (8 * mib, 2 * mib, 12 * gib, 20, 3),
        ):
            with self.subTest(inputs=inputs):
                self.assertIsNotNone(precreate_headroom_failure(*inputs))

    def test_ordinary_network_mismatch_receipt_exposes_only_shape_booleans(self):
        network = Network("4" * 64, "owned-queue")
        record = Container(
            "2" * 64,
            "owned-worker",
            "worker",
            1,
            N8N_ID,
            N8N_REF,
            "1000:1000",
            ("queue",),
            (),
            (),
        )
        item = {
            "State": {"Status": "created"},
            "NetworkSettings": {
                "Networks": {
                    network.name: {
                        "NetworkID": "",
                        "EndpointID": "",
                        "Aliases": ["n8n-worker"],
                    }
                }
            },
        }
        networks = {"queue": network}
        aliases = {"worker": "n8n-worker"}
        self.assertTrue(network_attachment_matches(item, record, networks, aliases, ""))
        facts = ordinary_network_facts(
            item,
            record,
            networks,
            aliases,
        )
        self.assertEqual(
            {
                "state_created": True,
                "state_running": False,
                "state_exited": False,
                "expected_keyset": True,
                "network_ids_empty": True,
                "network_ids_match": False,
                "endpoint_ids_empty": True,
                "endpoint_ids_valid": False,
                "required_aliases_present": True,
                "aliases_exact": True,
            },
            facts,
        )
        self.assertTrue(all(isinstance(value, bool) for value in facts.values()))
        endpoint = item["NetworkSettings"]["Networks"][network.name]
        running = {
            **item,
            "State": {"Status": "running"},
            "NetworkSettings": {
                "Networks": {
                    network.name: {
                        **endpoint,
                        "NetworkID": network.network_id,
                        "EndpointID": "5" * 64,
                    }
                }
            },
        }
        self.assertTrue(
            network_attachment_matches(running, record, networks, aliases, "")
        )
        exited = {
            **running,
            "State": {"Status": "exited"},
            "NetworkSettings": {
                "Networks": {
                    network.name: {
                        **running["NetworkSettings"]["Networks"][network.name],
                        "EndpointID": "",
                    }
                }
            },
        }
        self.assertTrue(
            network_attachment_matches(exited, record, networks, aliases, "")
        )
        for changed in (
            {**endpoint, "NetworkID": network.network_id},
            {**endpoint, "EndpointID": "5" * 64},
            {**endpoint, "Aliases": ["n8n-worker", "extra"]},
        ):
            rejected = {
                **item,
                "NetworkSettings": {"Networks": {network.name: changed}},
            }
            with self.subTest(changed=tuple(sorted(changed))):
                self.assertFalse(
                    network_attachment_matches(rejected, record, networks, aliases, "")
                )

    def test_default_is_not_run_and_partial_or_wrong_selection_fails_closed(self):
        self.assertIsNone(native_driver.native_selection({}))
        for env in (
            {native_driver.FLAG: "1"},
            {
                native_driver.FLAG: "0",
                native_driver.IMAGE_ENV: N8N_ID,
                native_driver.CONTEXT_ENV: "default",
            },
            {
                native_driver.FLAG: "1",
                native_driver.IMAGE_ENV: "sha256:" + "0" * 64,
                native_driver.CONTEXT_ENV: "default",
            },
            {
                native_driver.FLAG: "1",
                native_driver.IMAGE_ENV: N8N_ID,
                native_driver.CONTEXT_ENV: "remote",
            },
            {
                native_driver.FLAG: "1",
                native_driver.IMAGE_ENV: N8N_ID,
                native_driver.CONTEXT_ENV: "default",
                "DOCKER_HOST": "tcp://example.invalid",
            },
        ):
            with self.subTest(env=tuple(sorted(env))):
                with self.assertRaises(RehearsalFailure):
                    native_driver.native_selection(env)

    def test_reviewed_topology_stays_below_four_gib_and_two_cpus(self):
        ephemeral = {"secret-prep", "capture-probe"}
        mib = sum(
            int(memory.removesuffix("m"))
            for role, (memory, _, _) in RESOURCE_CAPS.items()
            if role not in ephemeral
        )
        cpus = sum(
            float(cpu)
            for role, (_, cpu, _) in RESOURCE_CAPS.items()
            if role not in ephemeral
        )
        self.assertEqual(3136, mib)
        self.assertLessEqual(cpus, 2.0)
        self.assertEqual(N8N_ID, IMAGE_IDS[N8N_REF])
        self.assertEqual(
            "sha256:"
            + "94f6b70c1436defae6799d9ac7ff0eeff9540465b842026d5cdb018f1c0234ea",
            MAILPIT_ID,
        )

    def test_no_network_role_requires_exact_builtin_none_attachment(self):
        none_id = "1" * 64
        record = Container(
            "2" * 64,
            "owned",
            "secret-prep",
            1,
            N8N_ID,
            N8N_REF,
            "0:0",
            (),
            (),
            ("CHOWN",),
        )
        endpoint = {
            "IPAMConfig": None,
            "Links": None,
            "Aliases": None,
            "DriverOpts": None,
            "GwPriority": 0,
            "NetworkID": none_id,
            "EndpointID": "3" * 64,
            "Gateway": "",
            "IPAddress": "",
            "MacAddress": "",
            "IPPrefixLen": 0,
            "IPv6Gateway": "",
            "GlobalIPv6Address": "",
            "GlobalIPv6PrefixLen": 0,
            "DNSNames": None,
        }
        item = {
            "HostConfig": {"NetworkMode": "none"},
            "NetworkSettings": {"Networks": {"none": endpoint}},
            "State": {"Status": "running"},
        }
        self.assertTrue(network_attachment_matches(item, record, {}, {}, none_id))
        exited = {
            **item,
            "NetworkSettings": {"Networks": {"none": {**endpoint, "EndpointID": ""}}},
            "State": {"Status": "exited"},
        }
        self.assertTrue(network_attachment_matches(exited, record, {}, {}, none_id))
        exited_facts = none_network_facts(exited, none_id)
        self.assertTrue(exited_facts["state_exited"])
        self.assertFalse(exited_facts["state_running"])
        created = {
            **item,
            "NetworkSettings": {
                "Networks": {"none": {**endpoint, "NetworkID": "", "EndpointID": ""}}
            },
            "State": {"Status": "created"},
        }
        self.assertTrue(network_attachment_matches(created, record, {}, {}, none_id))
        self.assertTrue(none_network_facts(created, none_id)["network_id_empty"])
        self.assertFalse(
            network_attachment_matches(
                {
                    **item,
                    "NetworkSettings": {
                        "Networks": {"none": {**endpoint, "EndpointID": ""}}
                    },
                },
                record,
                {},
                {},
                none_id,
            )
        )
        self.assertFalse(
            network_attachment_matches(
                {**item, "State": {"Status": "exited"}},
                record,
                {},
                {},
                none_id,
            )
        )
        for equivalent in (["CHOWN"], ["CAP_CHOWN"]):
            self.assertTrue(
                security_contract_matches(
                    {
                        "CapDrop": ["ALL"],
                        "CapAdd": equivalent,
                        "SecurityOpt": ["no-new-privileges=true"],
                    },
                    ("CHOWN",),
                )
            )
        for empty_cap_add in (None, []):
            self.assertTrue(
                security_contract_matches(
                    {
                        "CapDrop": ["ALL"],
                        "CapAdd": empty_cap_add,
                        "SecurityOpt": ["no-new-privileges=true"],
                    },
                    (),
                )
            )
        for cap_add, security_opt in (
            (["CAP_CHOWN", "CAP_FOWNER"], ["no-new-privileges=true"]),
            (["CAP_NET_ADMIN"], ["no-new-privileges=true"]),
            (["CAP_CHOWN", "CAP_CHOWN"], ["no-new-privileges=true"]),
            (["CHOWN", "CAP_CHOWN"], ["no-new-privileges=true"]),
            (["CAP_CHOWN"], ["no-new-privileges:true"]),
            (["CAP_CHOWN"], ["no-new-privileges=false"]),
            (["CAP_CHOWN"], ["no-new-privileges=true", "label=extra"]),
        ):
            with self.subTest(cap_add=cap_add, security_opt=security_opt):
                self.assertFalse(
                    security_contract_matches(
                        {
                            "CapDrop": ["ALL"],
                            "CapAdd": cap_add,
                            "SecurityOpt": security_opt,
                        },
                        ("CHOWN",),
                    )
                )
        for malformed in (
            {"CHOWN": True},
            {},
            "CHOWN",
            0,
            False,
            [1],
            [["CHOWN"]],
        ):
            with self.subTest(malformed=malformed):
                self.assertFalse(
                    security_contract_matches(
                        {
                            "CapDrop": ["ALL"],
                            "CapAdd": malformed,
                            "SecurityOpt": ["no-new-privileges=true"],
                        },
                        ("CHOWN",),
                    )
                )
                self.assertFalse(
                    security_contract_facts(
                        {
                            "CapDrop": ["ALL"],
                            "CapAdd": malformed,
                            "SecurityOpt": ["no-new-privileges=true"],
                        },
                        ("CHOWN",),
                    )["cap_add_semantic_exact"]
                )
        for field, duplicate in (
            ("CapDrop", ["ALL", "ALL"]),
            (
                "SecurityOpt",
                ["no-new-privileges=true", "no-new-privileges=true"],
            ),
        ):
            host = {
                "CapDrop": ["ALL"],
                "CapAdd": ["CAP_CHOWN"],
                "SecurityOpt": ["no-new-privileges=true"],
                field: duplicate,
            }
            self.assertFalse(security_contract_matches(host, ("CHOWN",)))
        for field in ("CapDrop", "SecurityOpt"):
            for malformed in (None, {}, "ALL", 0, False, [1], [["ALL"]]):
                with self.subTest(field=field, malformed=malformed):
                    host = {
                        "CapDrop": ["ALL"],
                        "CapAdd": ["CAP_CHOWN"],
                        "SecurityOpt": ["no-new-privileges=true"],
                        field: malformed,
                    }
                    self.assertFalse(security_contract_matches(host, ("CHOWN",)))
        facts = security_contract_facts(
            {
                "CapDrop": ["ALL"],
                "CapAdd": ["CAP_CHOWN"],
                "SecurityOpt": ["no-new-privileges=true"],
            },
            ("CHOWN",),
        )
        self.assertFalse(facts["cap_add_declared_exact"])
        self.assertTrue(facts["cap_add_prefixed_exact"])
        self.assertTrue(facts["cap_add_semantic_exact"])
        self.assertTrue(facts["security_opt_equals_exact"])
        self.assertFalse(facts["security_opt_colon_exact"])
        self.assertFalse(
            network_attachment_matches(
                {
                    **item,
                    "NetworkSettings": {
                        "Networks": {"none": {**endpoint, "IPAddress": "10.0.0.2"}}
                    },
                },
                record,
                {},
                {},
                none_id,
            )
        )
        self.assertFalse(
            network_attachment_matches(
                {**created, "State": {"Status": "paused"}},
                record,
                {},
                {},
                none_id,
            )
        )

    def test_failed_create_recovers_and_tracks_exact_owned_container(self):
        for outcome in (
            subprocess.CompletedProcess([], 1, "", "withheld"),
            TimeoutError(),
        ):
            with self.subTest(outcome=type(outcome).__name__):
                cid = "a" * 64
                fixture = object.__new__(NativeFixture)
                fixture.work_deadline = time.monotonic() + 60
                fixture.attempt = "opsflow-native-" + "b" * 24
                fixture.generation = 1
                fixture.directory = Path(tempfile.mkdtemp())
                fixture.files, fixture.containers = {}, {}
                fixture.pending_containers = {}
                fixture.networks = {"ctl": Network("c" * 64, "owned-ctl")}
                fixture.client = mock.Mock()
                fixture.client.run_result.side_effect = outcome
                fixture.client.run.return_value = cid + "\n"
                try:
                    with self.assertRaises(RehearsalFailure):
                        fixture.create("main", N8N_REF, "1000:1000", ("ctl",))
                    self.assertEqual(cid, fixture.containers["main"].cid)
                finally:
                    fixture.directory.rmdir()

    def test_raised_network_create_recovers_exact_owned_identity(self):
        fixture = object.__new__(NativeFixture)
        fixture.attempt = "opsflow-native-" + "b" * 24
        fixture.networks = {}
        fixture.pending_networks = {}
        fixture.client = mock.Mock()
        fixture.client.run_result.side_effect = TimeoutError()
        fixture.client.run.return_value = "e" * 64 + "\n"
        with self.assertRaises(RehearsalFailure):
            fixture.create_networks()
        self.assertEqual("e" * 64, fixture.networks["ctl"].network_id)

    def test_failed_remove_and_stop_do_not_release_owned_identity(self):
        fixture = object.__new__(NativeFixture)
        record = Container(
            "d" * 64,
            "owned",
            "main",
            1,
            N8N_ID,
            N8N_REF,
            "1000:1000",
            ("ctl",),
            (),
            (),
        )
        fixture.containers = {"main": record}
        fixture.pending_containers = {}
        fixture.receipt = {}
        fixture.client = mock.Mock()
        fixture.final_deadline = time.monotonic() + 5
        fixture.client.cleanup_deadline, fixture.client.deadline = (
            None,
            fixture.final_deadline,
        )
        failure = subprocess.CompletedProcess([], 1, "", "")
        fixture.client.run_result.side_effect = [
            failure,
            subprocess.CompletedProcess([], 1, "", "daemon unavailable"),
        ]
        fixture._verify_owned = mock.Mock()
        with (
            mock.patch.object(
                ownership.time,
                "monotonic",
                # The absence wait spans 15 s (wait_container_absent).
                side_effect=[0.0, 0.0, 15.0, 15.0],
            ),
            mock.patch.object(ownership.time, "sleep"),
            self.assertRaises(RehearsalFailure),
        ):
            fixture.remove("main")
        self.assertEqual(
            {"present": 0, "exact_absent": 0, "unknown": 1},
            fixture.receipt["container_removal_facts"]["main"],
        )
        fixture.client.run_result.side_effect = None
        fixture.client.run_result.return_value = failure
        fixture._verify_container = mock.Mock()
        with self.assertRaises(RehearsalFailure):
            fixture.stop("main")
        self.assertIs(record, fixture.containers["main"])

    def test_remove_does_not_swallow_cancellation(self):
        fixture = object.__new__(NativeFixture)
        record = Container(
            "d" * 64,
            "owned",
            "dev-pg",
            1,
            N8N_ID,
            N8N_REF,
            "70:70",
            ("dev",),
            (),
            (),
        )
        fixture.containers = {"dev-pg": record}
        fixture.pending_containers = {}
        fixture.receipt = {}
        fixture.client = mock.Mock()
        fixture.final_deadline = time.monotonic() + 5
        fixture.client.cleanup_deadline, fixture.client.deadline = (
            None,
            fixture.final_deadline,
        )
        fixture.client.run_result.side_effect = KeyboardInterrupt()
        fixture._verify_owned = mock.Mock()
        with self.assertRaises(KeyboardInterrupt):
            fixture.remove("dev-pg")
        self.assertIs(record, fixture.containers["dev-pg"])

    def test_cleanup_adopts_create_hidden_by_transient_query_failure(self):
        fixture = object.__new__(NativeFixture)
        fixture.work_deadline = time.monotonic() + 60
        fixture.final_deadline = time.monotonic() + 65
        fixture.attempt = "opsflow-native-" + "b" * 24
        fixture.generation = 1
        fixture.directory = Path(tempfile.mkdtemp())
        fixture.files, fixture.containers, fixture.networks = {}, {}, {}
        fixture.pending_containers, fixture.pending_networks = {}, {}
        fixture.swept_cids, fixture.swept_nids = set(), set()
        fixture.receipt = {"cleanup": "PENDING"}
        fixture.dir_identity = None
        fixture.lock_fd = -1
        fixture._cleanup_host = mock.Mock()
        fixture.runtime_headroom = mock.Mock()
        fixture.client = mock.Mock()
        fixture.client.run_result.side_effect = TimeoutError()
        fixture.client.run.side_effect = TimeoutError()
        try:
            with self.assertRaises(RehearsalFailure):
                fixture.create("secret-prep", N8N_REF, "0:0", ())
            self.assertIn("secret-prep", fixture.pending_containers)
            self.assertEqual({}, fixture.containers)

            cid = "f" * 64
            pending = fixture.pending_containers["secret-prep"]
            metadata = json.dumps(
                [
                    {
                        "Id": cid,
                        "Name": "/" + pending.name,
                        "Config": {
                            "Labels": {
                                OWNER_LABEL: OWNER,
                                ATTEMPT_LABEL: fixture.attempt,
                                ROLE_LABEL: pending.role,
                                "hyhome.opsflow.native-generation": "1",
                                "hyhome.opsflow.native-image-ref": N8N_REF,
                            }
                        },
                    }
                ]
            )
            query_count = 0
            inspect_count = 0

            def run(*args):
                nonlocal query_count
                query_count += 1
                return cid + "\n" if query_count == 1 else ""

            def run_result(*args, **_kwargs):
                nonlocal inspect_count
                if args[0] == "inspect":
                    if "--format" in args:
                        return subprocess.CompletedProcess(
                            args, 1, "", f"Error: No such object: {cid}\n"
                        )
                    inspect_count += 1
                    if inspect_count <= 2:
                        return subprocess.CompletedProcess(args, 0, metadata, "")
                    return subprocess.CompletedProcess(
                        args, 1, "", f"Error: No such object: {cid}\n"
                    )
                return subprocess.CompletedProcess(args, 0, "", "")

            fixture.client.run.side_effect = run
            fixture.client.run_result.side_effect = run_result
            fixture.client.cleanup_deadline = fixture.final_deadline
            fixture.cleanup()
            self.assertEqual("PASS", fixture.receipt["cleanup"])
            self.assertEqual({}, fixture.pending_containers)
            fixture._cleanup_host.assert_called_once_with()
        finally:
            fixture.directory.rmdir()

    def test_cleanup_denies_host_release_when_final_label_sweep_finds_residue(self):
        fixture = object.__new__(NativeFixture)
        fixture.client = mock.Mock()
        fixture.client.run.side_effect = ["a" * 64 + "\n", ""]
        fixture.containers, fixture.networks = {}, {}
        fixture.pending_containers, fixture.pending_networks = {}, {}
        fixture.swept_cids, fixture.swept_nids = set(), set()
        fixture.receipt = {"cleanup": "PENDING"}
        fixture.attempt = "opsflow-native-" + "b" * 24
        fixture.directory = Path("/tmp/owned-attempt-safe-name")
        fixture.dir_identity = (1, 2)
        fixture.lock_fd = -1
        fixture._cleanup_host = mock.Mock()
        with self.assertRaises(RehearsalFailure):
            fixture.cleanup()
        self.assertEqual("FAIL", fixture.receipt["cleanup"])
        self.assertEqual(["a" * 64], fixture.receipt["retained"]["container_ids"])
        fixture._cleanup_host.assert_not_called()

    def test_cleanup_boundary_failure_still_emits_retained_receipt(self):
        fixture = object.__new__(NativeFixture)
        fixture.client = mock.Mock()
        fixture.client.begin_cleanup.side_effect = TimeoutError()
        fixture.containers, fixture.networks = {}, {}
        fixture.pending_containers, fixture.pending_networks = {}, {}
        fixture.swept_cids, fixture.swept_nids = set(), set()
        fixture.receipt = {"cleanup": "PENDING"}
        fixture.directory = Path("/tmp/owned-attempt-safe-name")
        fixture.dir_identity = None
        fixture.lock_fd = -1
        fixture._cleanup_host = mock.Mock()
        with self.assertRaises(RehearsalFailure):
            fixture.cleanup()
        self.assertEqual("FAIL", fixture.receipt["cleanup"])
        self.assertEqual([], fixture.receipt["retained"]["container_ids"])

    def test_dev_cluster_guard_is_applied_after_each_fresh_start(self):
        case = object.__new__(native_driver.OpsflowN8nNativeRehearsal)
        case.fixture = mock.Mock()
        secret = Path("/owned/dev-pg.secret")
        case.secrets = {"dev_pg": ("withheld", secret)}
        case.start_dev_cluster()
        case.start_dev_cluster()
        self.assertEqual(2, case.fixture.start_postgres.call_count)
        self.assertEqual(2, case.fixture.psql.call_count)


if __name__ == "__main__":
    unittest.main()
