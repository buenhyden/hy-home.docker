"""P03 external n8n runner isolation and launcher-policy contracts."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
import uuid
from pathlib import Path

import yaml

from tests.validation._opsflow_native_fixture import NativeFixture, RehearsalFailure
from tests.validation._opsflow_native_inputs import (
    N8N_REF,
    RUNNER_REF,
    bind_mount,
)
from tests.validation._opsflow_native_ownership import (
    n8n_health_probe,
    node_status_probe,
)
from tests.validation._p03_runner_native_fixture import (
    CANCEL_JS,
    FULL_REQUEST_TIMEOUT,
    FULL_TASK_TIMEOUT,
    NATIVE_EXPLICIT,
    native_selection,
    p03_api_script,
    run_full_rehearsal,
    runner_timing_environment,
    safe_execution_id,
)
from tests.validation.test_opsflow_native_rehearsal import API_JS as OPSFLOW_API_JS

ROOT = Path(__file__).resolve().parents[2]
N8N = ROOT / "infra/07-workflow/n8n"
COMPOSE = N8N / "docker-compose.yml"
ROOT_COMPOSE = ROOT / "docker-compose.yml"
RUNNER_CONFIG = N8N / "n8n-task-runners.json"
COMMON = ROOT / "infra/common-optimizations.yml"

# Main runs queue mode with manual executions offloaded, so n8n 2.46.6 never
# starts a task runner there (commands/start.js); only the worker has one
# (SPEC-0269).
RUNNER_PAIRS = {
    "n8n-task-runner-worker": ("n8n-worker", "n8n_worker_runner_net"),
}
NETWORKS = {
    "n8n_worker_runner_net": "10.250.23.0/24",
}
RUNNER_IMAGE = (
    "n8nio/runners:2.46.6@"
    "sha256:b1fe87a59b712a03e5a4fbb46a18ea5ca9487add602f8749941a69f4ab322612"
)
TMPFS = "/tmp:rw,noexec,nosuid,nodev,size=64m,mode=1777,uid=1000,gid=1000"
P03_API_JS = p03_api_script(OPSFLOW_API_JS)


def load_yaml(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected mapping in {path}")
    return value


def load_runner_config() -> dict:
    value = json.loads(RUNNER_CONFIG.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("runner config must be an object")
    return value


def runner_by_type() -> dict[str, dict]:
    rows = load_runner_config().get("task-runners")
    if not isinstance(rows, list):
        raise ValueError("task-runners must be an array")
    typed = {
        row.get("runner-type"): row
        for row in rows
        if isinstance(row, dict) and isinstance(row.get("runner-type"), str)
    }
    if len(typed) != len(rows):
        raise ValueError("runner types must be unique strings")
    return typed


class RunnerComposeContractTests(unittest.TestCase):
    def setUp(self):
        self.source = COMPOSE.read_text(encoding="utf-8")
        self.compose = load_yaml(COMPOSE)
        self.services = self.compose["services"]

    def test_runner_pairs_use_two_exact_internal_broker_networks(self):
        root_networks = load_yaml(ROOT_COMPOSE)["networks"]
        for network, subnet in NETWORKS.items():
            with self.subTest(network=network):
                definition = root_networks[network]
                self.assertIs(definition["internal"], True)
                self.assertEqual(
                    "isolated",
                    definition["driver_opts"][
                        "com.docker.network.bridge.gateway_mode_ipv4"
                    ],
                )
                # The broker binds below the dynamic range (SPEC-0267).
                self.assertEqual(
                    [
                        {
                            "subnet": subnet,
                            "ip_range": subnet.replace(".0/24", ".128/25"),
                        }
                    ],
                    definition["ipam"]["config"],
                )

        all_subnets = [
            item["subnet"]
            for definition in root_networks.values()
            for item in definition.get("ipam", {}).get("config", [])
        ]
        self.assertEqual(len(all_subnets), len(set(all_subnets)))

        for runner, (broker, network) in RUNNER_PAIRS.items():
            with self.subTest(runner=runner):
                self.assertEqual({network}, set(self.services[runner]["networks"]))
                self.assertIn(network, self.services[broker]["networks"])
                self.assertNotIn("n8n_net", self.services[runner]["networks"])

        self.assertNotIn("n8n_worker_runner_net", self.services["n8n"]["networks"])
        for peer in ("valkey-exporter", "blog-ingestion-gateway"):
            if peer in self.services:
                self.assertTrue(
                    NETWORKS.keys().isdisjoint(self.services[peer].get("networks", {})),
                    peer,
                )

    def test_runner_root_storage_and_resources_are_bounded(self):
        common = load_yaml(COMMON)["services"]["template-stateful-low"]
        self.assertEqual("0.50", common["cpus"])
        self.assertEqual("256m", common["mem_limit"])
        self.assertEqual(256, common["pids_limit"])
        self.assertEqual(["ALL"], common["cap_drop"])
        self.assertIn("no-new-privileges:true", common["security_opt"])

        for name in RUNNER_PAIRS:
            with self.subTest(runner=name):
                runner = self.services[name]
                self.assertEqual("1000:1000", runner["user"])
                self.assertIs(runner["read_only"], True)
                self.assertEqual([TMPFS], runner["tmpfs"])
                self.assertEqual(
                    1, runner["environment"]["N8N_RUNNERS_MAX_CONCURRENCY"]
                )
                self.assertEqual(300, runner["environment"]["N8N_RUNNERS_TASK_TIMEOUT"])
                self.assertEqual(RUNNER_IMAGE, runner["image"])
                self.assertEqual(
                    ["./n8n-task-runners.json:/etc/n8n-task-runners.json:ro"],
                    runner.get("volumes"),
                )
                self.assertTrue(
                    all(
                        not str(mount).startswith(
                            ("n8n-task-runner-data:", "n8n-task-runner-worker-data:")
                        )
                        for mount in runner.get("volumes", [])
                    )
                )
                self.assertNotIn("privileged", runner)
                self.assertNotIn("cap_add", runner)
                self.assertNotIn("devices", runner)
        # The declarations and their existing data are retained for rollback;
        # no service may mount either volume in the hardened candidate.
        self.assertIn("n8n-task-runner-data", self.compose.get("volumes", {}))
        self.assertIn("n8n-task-runner-worker-data", self.compose.get("volumes", {}))

    def test_main_and_worker_keep_external_mode_and_block_code_environment(self):
        for name in ("n8n", "n8n-worker"):
            with self.subTest(service=name):
                environment = self.services[name]["environment"]
                self.assertEqual("external", environment["N8N_RUNNERS_MODE"])
                self.assertIs(environment["N8N_BLOCK_ENV_ACCESS_IN_NODE"], True)
                self.assertIs(environment["OFFLOAD_MANUAL_EXECUTIONS_TO_WORKERS"], True)
                self.assertEqual(300, environment["N8N_RUNNERS_TASK_TIMEOUT"])
                self.assertNotIn("N8N_RUNNERS_INSECURE_MODE", environment)

        self.assertEqual("worker", self.services["n8n-worker"]["command"])
        for runner, (broker, _) in RUNNER_PAIRS.items():
            uri = self.services[runner]["environment"]["N8N_RUNNERS_TASK_BROKER_URI"]
            self.assertEqual(f"http://{broker}:${{N8N_BROKER_PORT:-5679}}", uri)

    def test_main_has_no_runner_while_manual_executions_are_offloaded(self):
        root = load_yaml(ROOT_COMPOSE)
        self.assertNotIn("n8n-task-runner", self.services)
        self.assertNotIn("n8n_main_runner_net", root["networks"])
        main = self.services["n8n"]
        self.assertNotIn("n8n_main_runner_net", main["networks"])
        self.assertNotIn("N8N_RUNNERS_BROKER_LISTEN_ADDRESS", main["environment"])
        # Without offload, main would need a runner of its own again.
        self.assertIs(main["environment"]["OFFLOAD_MANUAL_EXECUTIONS_TO_WORKERS"], True)
        self.assertEqual("queue", main["environment"]["EXECUTIONS_MODE"])

    def test_token_wrapper_stays_value_free_and_fails_closed(self):
        for name in RUNNER_PAIRS:
            command = self.services[name]["command"]
            wrapper = command if isinstance(command, str) else "\n".join(command)
            self.assertIn("/run/secrets/n8n_runner_auth_token", wrapper)
            self.assertIn("exec /usr/local/bin/task-runner-launcher", wrapper)
            self.assertNotIn("set -x", wrapper)
            self.assertNotRegex(wrapper, r"(?:echo|printf).*N8N_RUNNERS_AUTH_TOKEN")
            with tempfile.TemporaryDirectory() as directory:
                secret = Path(directory) / "token"
                launcher = Path(directory) / "launcher"
                launcher.write_text(
                    "#!/bin/sh\n"
                    'test "$N8N_RUNNERS_AUTH_TOKEN" = synthetic-runner-token\n',
                    encoding="utf-8",
                )
                launcher.chmod(0o700)
                simulated = (
                    wrapper.replace("$$", "$")
                    .replace("/run/secrets/n8n_runner_auth_token", str(secret))
                    .replace("/usr/local/bin/task-runner-launcher", str(launcher))
                )
                for value, expected in (
                    (None, False),
                    ("", False),
                    ("synthetic-runner-token", True),
                ):
                    if value is None:
                        secret.unlink(missing_ok=True)
                    else:
                        secret.write_text(value, encoding="utf-8")
                    result = subprocess.run(
                        ["sh", "-ec", simulated],
                        capture_output=True,
                        text=True,
                        check=False,
                        timeout=5,
                    )
                    self.assertEqual(expected, result.returncode == 0)
                    self.assertNotIn(
                        "synthetic-runner-token", result.stdout + result.stderr
                    )

    def test_rendered_runner_contract_preserves_pair_isolation(self):
        result = subprocess.run(
            [
                "docker",
                "compose",
                "--env-file",
                "/dev/null",
                "-f",
                str(COMPOSE),
                "--profile",
                "workflow-n8n",
                "config",
                "--no-interpolate",
                "--format",
                "json",
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=30,
        )
        self.assertEqual(0, result.returncode, result.stderr[-1000:])
        rendered = json.loads(result.stdout)["services"]
        for runner_name, (broker, network) in RUNNER_PAIRS.items():
            with self.subTest(runner=runner_name):
                runner = rendered[runner_name]
                self.assertEqual({network}, set(runner["networks"]))
                self.assertEqual(
                    f"http://{broker}:${{N8N_BROKER_PORT:-5679}}",
                    runner["environment"]["N8N_RUNNERS_TASK_BROKER_URI"],
                )
                self.assertEqual("1000:1000", runner["user"])
                self.assertIs(runner["read_only"], True)
                self.assertEqual([TMPFS], runner["tmpfs"])
                self.assertEqual(
                    [
                        {
                            "bind": {"create_host_path": True},
                            "read_only": True,
                            "source": str(RUNNER_CONFIG),
                            "target": "/etc/n8n-task-runners.json",
                            "type": "bind",
                        }
                    ],
                    runner["volumes"],
                )


class RunnerLauncherPolicyTests(unittest.TestCase):
    def test_launcher_keeps_exact_language_processes_and_health_ports(self):
        rows = runner_by_type()
        self.assertEqual({"javascript", "python"}, set(rows))
        javascript = rows["javascript"]
        python = rows["python"]
        self.assertEqual("/home/runner", javascript["workdir"])
        self.assertEqual("/usr/local/bin/node", javascript["command"])
        self.assertEqual(
            [
                "--disallow-code-generation-from-strings",
                "--disable-proto=delete",
                "/opt/runners/task-runner-javascript/dist/start.js",
            ],
            javascript["args"],
        )
        self.assertEqual("5681", javascript["health-check-server-port"])
        self.assertEqual("/home/runner", python["workdir"])
        self.assertEqual(
            "/opt/runners/task-runner-python/.venv/bin/python", python["command"]
        )
        self.assertEqual(
            ["-I", "-B", "-X", "disable_remote_debug", "-m", "src.main"],
            python["args"],
        )
        self.assertEqual("5682", python["health-check-server-port"])

    def test_launcher_denies_modules_transitive_imports_and_environment(self):
        rows = runner_by_type()
        javascript = rows["javascript"]["env-overrides"]
        python = rows["python"]["env-overrides"]
        self.assertEqual(
            [
                "PATH",
                "GENERIC_TIMEZONE",
                "NODE_OPTIONS",
                "NODE_PATH",
                "N8N_RUNNERS_AUTO_SHUTDOWN_TIMEOUT",
                "N8N_RUNNERS_GRACEFUL_SHUTDOWN_TIMEOUT",
                "N8N_RUNNERS_SHUTDOWN_FORCE_KILL_MARGIN",
                "N8N_RUNNERS_TASK_TIMEOUT",
                "N8N_RUNNERS_MAX_CONCURRENCY",
                "N8N_SENTRY_DSN",
                "N8N_VERSION",
                "ENVIRONMENT",
                "DEPLOYMENT_NAME",
                "HOME",
            ],
            rows["javascript"]["allowed-env"],
        )
        self.assertEqual(
            [
                "PATH",
                "N8N_RUNNERS_LAUNCHER_LOG_LEVEL",
                "N8N_RUNNERS_AUTO_SHUTDOWN_TIMEOUT",
                "N8N_RUNNERS_GRACEFUL_SHUTDOWN_TIMEOUT",
                "N8N_RUNNERS_TASK_TIMEOUT",
                "N8N_RUNNERS_MAX_CONCURRENCY",
                "N8N_SENTRY_DSN",
                "N8N_VERSION",
                "ENVIRONMENT",
                "DEPLOYMENT_NAME",
            ],
            rows["python"]["allowed-env"],
        )
        self.assertEqual("", javascript["NODE_FUNCTION_ALLOW_BUILTIN"])
        self.assertEqual("", javascript["NODE_FUNCTION_ALLOW_EXTERNAL"])
        self.assertEqual("0.0.0.0", javascript["N8N_RUNNERS_HEALTH_CHECK_SERVER_HOST"])
        self.assertEqual("", python["N8N_RUNNERS_STDLIB_ALLOW"])
        self.assertEqual("", python["N8N_RUNNERS_EXTERNAL_ALLOW"])
        self.assertEqual("false", python["N8N_RUNNERS_ALLOW_TRANSITIVE_IMPORTS"])
        self.assertEqual("true", python["N8N_BLOCK_RUNNER_ENV_ACCESS"])
        self.assertNotIn("N8N_RUNNERS_BUILTINS_DENY", python)

        forbidden = {
            "N8N_RUNNERS_AUTH_TOKEN",
            "N8N_RUNNERS_GRANT_TOKEN",
            "N8N_ENCRYPTION_KEY",
            "N8N_ENCRYPTION_KEY_FILE",
            "NODE_FUNCTION_ALLOW_BUILTIN",
            "NODE_FUNCTION_ALLOW_EXTERNAL",
            "N8N_RUNNERS_STDLIB_ALLOW",
            "N8N_RUNNERS_EXTERNAL_ALLOW",
        }
        for name, row in rows.items():
            with self.subTest(runner=name):
                allowed = row["allowed-env"]
                self.assertEqual(len(allowed), len(set(allowed)))
                self.assertTrue(forbidden.isdisjoint(allowed))
                self.assertNotIn("*", allowed)

    def test_config_has_no_secret_value_or_unbounded_allowlist(self):
        source = RUNNER_CONFIG.read_text(encoding="utf-8")
        self.assertNotRegex(source, r"(?i)(password|secret|token)\s*[:=]\s*['\"]\S+")
        self.assertNotRegex(
            source,
            r'"(?:NODE_FUNCTION|N8N_RUNNERS_(?:STDLIB|EXTERNAL)_ALLOW)"\s*:\s*"\*"',
        )
        self.assertNotIn("/var/run/docker.sock", source)
        self.assertNotIn("/run/secrets", source)


@unittest.skipUnless(NATIVE_EXPLICIT, "exact isolated P03 runner opt-in required")
class P03RunnerNativeRehearsal(unittest.TestCase):
    """A broker-focused synthetic Code run; it is not manual-worker acceptance."""

    @classmethod
    def setUpClass(cls):
        native_selection()

    def setUp(self):
        self.fixture = NativeFixture()
        self.secrets: dict[str, tuple[str, Path]] = {}
        self.email = f"owner-{self.fixture.attempt}@p03.invalid"
        self.session: str | None = None
        self.finished = False

    def tearDown(self):
        self.finish()

    def finish(self):
        if self.finished:
            return
        self.finished = True
        if self.fixture.receipt.get("native") not in {"PASS", "PARTIAL"}:
            self.fixture.receipt["native"] = "ERROR"
        try:
            self.fixture.cleanup()
        finally:
            print("P03_RUNNER_NATIVE_RECEIPT " + self.fixture.receipt_json())

    def api(self, action: str, **payload) -> dict:
        body = {
            "action": action,
            "email": self.email,
            "password": self.secrets["owner"][0],
            **({"cookie": self.session} if self.session else {}),
            **payload,
        }
        result = self.fixture.exec_result(
            "main",
            "node",
            "-e",
            P03_API_JS,
            input_=json.dumps(body, separators=(",", ":")),
        )
        if result.returncode:
            try:
                failure = json.loads(result.stdout).get("failure", {})
            except (AttributeError, TypeError, ValueError):
                failure = {}
            kind = failure.get("kind")
            error = failure.get("error", {})
            if kind in {
                "http_status",
                "fetch_unavailable",
                "response_invalid",
                "transport",
                "unknown",
            } and isinstance(error, dict):
                self.fixture.receipt["api_failure_facts"] = {
                    "kind": kind,
                    "status": failure.get("status")
                    if isinstance(failure.get("status"), int)
                    else None,
                    "code": error.get("code")
                    if error.get("code")
                    in {
                        "none",
                        "connection_refused",
                        "connection_reset",
                        "timeout",
                        "dns",
                        "other",
                    }
                    else "other",
                }
            raise RehearsalFailure("n8n REST operation failed (payload withheld)")
        try:
            value = json.loads(result.stdout)
        except (TypeError, ValueError):
            raise RehearsalFailure("n8n REST safe summary rejected") from None
        if not isinstance(value, dict):
            raise RehearsalFailure("n8n REST safe summary shape rejected")
        if "_session" in value:
            self.session = value.pop("_session")
        return value

    def n8n_mounts(self) -> tuple[str, ...]:
        return tuple(
            bind_mount(self.secrets[key][1], target)
            for key, target in (
                ("metadata_n8n", "/run/secrets/n8n_db_password"),
                ("valkey_n8n", "/run/secrets/mng_valkey_password"),
                ("encryption", "/run/secrets/n8n_encryption_key"),
                ("runner", "/run/secrets/n8n_runner_auth_token"),
            )
        )

    @staticmethod
    def n8n_environment(task_timeout: int, request_timeout: int) -> tuple[str, ...]:
        # HOME (SPEC-0269): queue mode with manual executions offloaded, so
        # main starts no broker and the worker's broker serves the runner.
        return (
            "DB_TYPE=postgresdb",
            "DB_POSTGRESDB_HOST=metadata-pg",
            "DB_POSTGRESDB_PORT=5432",
            "DB_POSTGRESDB_DATABASE=n8n",
            "DB_POSTGRESDB_USER=n8n",
            "DB_POSTGRESDB_PASSWORD_FILE=/run/secrets/n8n_db_password",
            "EXECUTIONS_MODE=queue",
            "OFFLOAD_MANUAL_EXECUTIONS_TO_WORKERS=true",
            "N8N_VALKEY_HOST=mng-valkey",
            "N8N_VALKEY_SECRET=mng_valkey_password",
            "QUEUE_BULL_REDIS_HOST=mng-valkey",
            "QUEUE_BULL_REDIS_PORT=6379",
            "QUEUE_BULL_PREFIX=n8n",
            "QUEUE_BULL_REDIS_PASSWORD_FILE=/run/secrets/mng_valkey_password",
            "N8N_RUNNERS_MODE=external",
            "N8N_RUNNERS_AUTH_TOKEN_FILE=/run/secrets/n8n_runner_auth_token",
            *runner_timing_environment(task_timeout, request_timeout),
            "N8N_ENCRYPTION_KEY_FILE=/run/secrets/n8n_encryption_key",
            "N8N_USER_FOLDER=/tmp",
            "N8N_PROTOCOL=http",
            "N8N_HOST=n8n",
            "N8N_PORT=5678",
            "N8N_LOG_LEVEL=info",
            "N8N_SECURE_COOKIE=false",
            "N8N_DIAGNOSTICS_ENABLED=false",
            "N8N_VERSION_NOTIFICATIONS_ENABLED=false",
            "N8N_TEMPLATES_ENABLED=false",
            "N8N_PERSONALIZATION_ENABLED=false",
            "N8N_BLOCK_ENV_ACCESS_IN_NODE=true",
            "GENERIC_TIMEZONE=Asia/Seoul",
            "TZ=Asia/Seoul",
        )

    def start_main(
        self,
        task_timeout: int = FULL_TASK_TIMEOUT,
        request_timeout: int = FULL_REQUEST_TIMEOUT,
    ) -> None:
        self.fixture.create(
            "main",
            N8N_REF,
            "1000:1000",
            ("ctl",),
            env=self.n8n_environment(task_timeout, request_timeout),
            mounts=self.n8n_mounts(),
        )
        self.fixture.start("main")

        def ready() -> bool:
            healthy, facts = n8n_health_probe(
                lambda *args: self.fixture.exec_result("main", *args)
            )
            self.fixture.receipt["main_health_probe"] = facts
            return healthy

        self.fixture.wait_until(ready, "n8n main readiness expired", 300)

    def start_worker(
        self,
        task_timeout: int = FULL_TASK_TIMEOUT,
        request_timeout: int = FULL_REQUEST_TIMEOUT,
    ) -> None:
        environment = (
            *self.n8n_environment(task_timeout, request_timeout),
            # Like HOME, the broker binds only the worker's runner-network address.
            f"N8N_RUNNERS_BROKER_LISTEN_ADDRESS={self.broker_ip}",
        )
        self.fixture.create(
            "worker",
            N8N_REF,
            "1000:1000",
            ("ctl", "runner"),
            env=environment,
            mounts=self.n8n_mounts(),
            command=("worker",),
            ips={"runner": self.broker_ip},
        )
        self.fixture.start("worker")

        def broker_ready() -> bool:
            ready, facts = node_status_probe(
                lambda *args: self.fixture.exec_result("worker", *args),
                f"http://{self.broker_ip}:5679/healthz",
            )
            self.fixture.receipt["worker_broker_health_probe"] = facts
            return ready

        self.fixture.wait_until(
            broker_ready, "n8n worker broker readiness expired", 300
        )

    def start_runner(self, token: Path, task_timeout: int = FULL_TASK_TIMEOUT) -> None:
        script = (
            "set -eu; "
            "N8N_RUNNERS_AUTH_TOKEN=$(cat /run/secrets/n8n-runner-token); "
            "export N8N_RUNNERS_AUTH_TOKEN; "
            "exec /usr/local/bin/task-runner-launcher javascript python"
        )
        self.fixture.create(
            "runner",
            RUNNER_REF,
            "1000:1000",
            ("runner",),
            env=(
                "N8N_RUNNERS_TASK_BROKER_URI=http://n8n-worker:5679",
                f"N8N_RUNNERS_TASK_TIMEOUT={task_timeout}",
                "N8N_RUNNERS_MAX_CONCURRENCY=1",
                "N8N_RUNNERS_AUTO_SHUTDOWN_TIMEOUT=0",
            ),
            mounts=(
                bind_mount(token, "/run/secrets/n8n-runner-token"),
                bind_mount(token, "/run/secrets/n8n_runner_auth_token"),
                bind_mount(RUNNER_CONFIG, "/etc/n8n-task-runners.json"),
            ),
            entrypoint="/bin/sh",
            command=("-ec", script),
        )
        self.fixture.start("runner")

    def import_workflow(self, workflow: dict) -> str:
        content = json.dumps(workflow, separators=(",", ":")) + "\n"
        filename = "workflow-" + uuid.uuid4().hex + ".json"
        private = self.fixture.private(filename, content)
        target = "/tmp/" + filename
        transferred = self.fixture.exec_result(
            "main",
            "/bin/sh",
            "-ec",
            f"umask 077; cat >{target}",
            input_=private.read_text(),
        )
        if transferred.returncode:
            raise RehearsalFailure("private workflow transfer failed")
        owner_id = getattr(self, "owner_id", "")
        imported = self.fixture.exec_result(
            "main",
            "n8n",
            "import:workflow",
            f"--input={target}",
            f"--userId={owner_id}",
            "--activeState=false",
        )
        if imported.returncode:
            raise RehearsalFailure("inactive workflow import failed")
        rows = self.api("workflows").get("rows")
        matches = [row for row in rows or [] if row.get("name") == workflow["name"]]
        if len(matches) != 1 or not isinstance(matches[0].get("id"), str):
            raise RehearsalFailure("imported workflow lookup failed")
        return matches[0]["id"]

    def run_workflow(
        self,
        workflow_id: str,
        expected: str | frozenset[str],
        wait_seconds: int = 30,
    ) -> tuple[str, dict]:
        execution = self.start_workflow(workflow_id)
        terminal = self.await_execution(execution, expected, wait_seconds)
        return execution, terminal

    def start_workflow(self, workflow_id: str) -> str:
        return safe_execution_id(
            self.api("run", workflowId=workflow_id).get("executionId")
        )

    def await_execution(
        self,
        execution: str,
        expected: str | frozenset[str],
        wait_seconds: int = 30,
    ) -> dict:
        terminal: dict = {}

        def finished() -> bool:
            summary = self.api("execution", executionId=execution)
            if "execution_response_facts" not in self.fixture.receipt:
                self.fixture.receipt["execution_response_facts"] = {
                    "requested_id": execution,
                    "returned_id": summary.get("id"),
                    "response_shape": summary.get("responseShape"),
                    "data_type": summary.get("dataType"),
                    "terminal_status": summary.get("status"),
                    "error_class": summary.get("errorClass"),
                    "error_category": summary.get("errorCategory"),
                }
            if summary.get("id") != execution:
                returned = summary.get("id")
                self.fixture.receipt["execution_identity_facts"] = {
                    "requested": execution,
                    "returned": returned
                    if isinstance(returned, str) and len(returned) <= 128
                    else "REJECTED",
                }
                raise RehearsalFailure("execution identity changed")
            self.fixture.receipt["execution_response_facts"]["terminal_status"] = (
                summary.get("status")
            )
            self.fixture.receipt["execution_response_facts"]["error_class"] = (
                summary.get("errorClass")
            )
            self.fixture.receipt["execution_response_facts"]["error_category"] = (
                summary.get("errorCategory")
            )
            if summary.get("status") in {"success", "error", "canceled", "crashed"}:
                terminal.update(summary)
                return True
            return False

        self.fixture.wait_until(
            finished, "Code execution did not become terminal", wait_seconds
        )
        accepted = {expected} if isinstance(expected, str) else set(expected)
        if (
            terminal.get("status") not in accepted
            or terminal.get("terminal") is not True
        ):
            raise RehearsalFailure("Code execution terminal status rejected")
        return terminal

    def cancel_execution(self, execution: str) -> None:
        if not self.session:
            raise RehearsalFailure("authenticated session required for cancellation")
        result = self.fixture.exec_result(
            "main",
            "node",
            "-e",
            CANCEL_JS,
            input_=json.dumps(
                {"executionId": execution, "cookie": self.session},
                separators=(",", ":"),
            ),
        )
        if result.returncode:
            raise RehearsalFailure("execution cancellation failed (output withheld)")
        try:
            summary = json.loads(result.stdout)
        except (TypeError, ValueError):
            raise RehearsalFailure("cancellation safe summary rejected") from None
        if summary not in (
            {"status": 200, "accepted": True},
            {"status": 204, "accepted": True},
        ):
            raise RehearsalFailure("execution cancellation was not accepted")

    def test_broker_focused_javascript_python_denials_timeout_and_recovery(self):
        run_full_rehearsal(self)


if __name__ == "__main__":
    unittest.main()
