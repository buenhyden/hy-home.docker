"""Sandbox selection, isolation checks and owned cleanup without a daemon."""

from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path
from subprocess import CompletedProcess
from unittest import mock

from scripts.operations import sandbox_env as sandbox

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "sandbox" / "compose.yaml"
MEMORY = 64 * 1024 * 1024


def service(**extra):
    return {"image": "busybox", "mem_limit": MEMORY, **extra}


class SandboxTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name)
        patcher = mock.patch.object(sandbox, "state_dir", self.state)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.config = {
            "services": {
                "app": service(depends_on={"db": {}}, networks={"sbx": {}}),
                "db": service(networks={"sbx": {}}),
                "lone": service(),
            },
            "secrets": {},
        }

    def state(self) -> Path:
        path = self.base / "state"
        path.mkdir(exist_ok=True)
        return path

    def fake_compose(self, calls, fail_up=False):
        def compose(host, project, files, *arguments, timeout=600):
            override = Path(files[-1])
            networks = (
                json.loads(override.read_text()) if override.suffix == ".json" else None
            )
            calls.append((project, arguments, networks))
            code = 1 if fail_up and "up" in arguments else 0
            return CompletedProcess(arguments, code, "", "boom")

        return compose

    def test_selection_resolves_the_closure_and_refuses_everything_else(self):
        self.assertEqual(["app", "db"], sandbox.closure(self.config, ["app"]))
        for bad in ([], ["all"], ["ALL"], ["db*"], ["a?"], ["missing"]):
            with self.subTest(bad=bad), self.assertRaises(sandbox.SandboxError):
                sandbox.closure(self.config, bad)

    def test_host_reaching_services_are_named_and_blocked(self):
        run_dir = self.base / "run"
        repository_file = str(sandbox.ROOT / "README.md")
        cases = {
            "socket": service(
                volumes=[{"type": "bind", "source": "/var/run/docker.sock"}]
            ),
            "outside": service(volumes=[{"type": "bind", "source": "/etc"}]),
            "repo-rw": service(volumes=[{"type": "bind", "source": repository_file}]),
            "secret": service(secrets=[{"source": "s"}]),
            "host-net": service(network_mode="host"),
            "privileged": service(privileged=True),
            "unbounded": {"image": "busybox"},
        }
        config = {"services": cases, "secrets": {"s": {"file": "/etc/hostname"}}}
        problems = sandbox.assess(config, sorted(cases), run_dir)
        self.assertEqual(set(cases), set(problems))
        allowed = {
            "repo-ro": service(
                volumes=[{"type": "bind", "source": repository_file, "read_only": True}]
            ),
            "run-dir": service(
                volumes=[{"type": "bind", "source": str(run_dir / "d")}]
            ),
        }
        self.assertEqual(
            {}, sandbox.assess({"services": allowed}, sorted(allowed), run_dir)
        )

    def test_secret_stores_volume_drivers_and_namespaces_are_blocked(self):
        run_dir = self.base / "run"
        secret = str(sandbox.ROOT / "secrets")
        cases = {
            "repo-secrets": service(
                volumes=[{"type": "bind", "source": secret, "read_only": True}]
            ),
            "repo-env": service(
                volumes=[
                    {
                        "type": "bind",
                        "source": str(sandbox.ROOT / ".env"),
                        "read_only": True,
                    }
                ]
            ),
            "driver-bind": service(volumes=[{"type": "volume", "source": "v1"}]),
            "external-volume": service(volumes=[{"type": "volume", "source": "v2"}]),
            "repo-root": service(
                volumes=[
                    {"type": "bind", "source": str(sandbox.ROOT), "read_only": True}
                ]
            ),
            "volumes-from": service(volumes_from=["other"]),
            "external-net": service(networks={"prod": {}}),
            "container-net": service(network_mode="container:traefik"),
            "bridge": service(network_mode="bridge"),
            "ipc": service(ipc="host"),
            "devices": service(devices=["/dev/kvm"]),
            "gpu": service(deploy={"resources": {"reservations": {"devices": [{}]}}}),
            "caps": service(cap_add=["SYS_ADMIN"]),
            "unconfined": service(security_opt=["seccomp:unconfined"]),
            "config": service(configs=[{"source": "c"}]),
            "env-file": service(env_file=[{"path": "/home/user/.env"}]),
        }
        config = {
            "services": cases,
            "volumes": {
                "v1": {"driver_opts": {"type": "none", "o": "bind", "device": "/"}},
                "v2": {"external": True},
            },
            "networks": {"prod": {"external": True}},
            "configs": {"c": {"file": "/etc/passwd"}},
        }
        problems = sandbox.assess(config, sorted(cases), run_dir)
        self.assertEqual(set(cases), set(problems) - {"<selection>"})
        safe = {
            "local-volume": service(volumes=[{"type": "volume", "source": "data"}]),
            "isolated": service(network_mode="none"),
        }
        config = {"services": safe, "volumes": {"data": {}}}
        self.assertEqual({}, sandbox.assess(config, sorted(safe), run_dir))

    def test_size_and_memory_budgets_are_enforced(self):
        many = {f"s{i}": service() for i in range(sandbox.MAX_SERVICES + 1)}
        problems = sandbox.assess({"services": many}, sorted(many), self.base)
        self.assertIn("exceed", problems["<selection>"][0])
        big = {"big": service(mem_limit=sandbox.MAX_MEMORY_BYTES + 1)}
        problems = sandbox.assess({"services": big}, ["big"], self.base)
        self.assertIn("memory", problems["<selection>"][-1])

    def test_up_needs_the_rootless_daemon_and_never_the_production_socket(self):
        for path in (self.base / "absent.sock", Path(sandbox.PRODUCTION_SOCKETS[0])):
            with self.subTest(path=path):
                with mock.patch.object(sandbox, "rootless_socket", return_value=path):
                    with self.assertRaises(sandbox.SandboxError):
                        sandbox.up([FIXTURE], ["app"])

    def test_up_isolates_networks_and_down_removes_only_its_project(self):
        calls = []
        with (
            mock.patch.object(
                sandbox, "_sandbox_host", return_value="unix:///sbx.sock"
            ),
            mock.patch.object(sandbox, "render", return_value=self.config),
            mock.patch.object(
                sandbox, "_compose", side_effect=self.fake_compose(calls)
            ),
        ):
            record = sandbox.up([FIXTURE], ["app"])
            self.assertEqual(
                {"removed": record["project"]}, sandbox.down(record["run_id"])
            )
        (start, stop) = calls
        self.assertTrue(start[0].startswith(sandbox.PROJECT_PREFIX))
        self.assertEqual(("app", "db"), start[1][-2:])
        self.assertEqual({"networks": {"sbx": {"internal": True}}}, start[2])
        self.assertEqual(start[0], stop[0])
        self.assertIn("down", stop[1])
        self.assertEqual([], list(self.state().iterdir()))

    def test_a_failed_start_cleans_up_its_own_run(self):
        calls = []
        with (
            mock.patch.object(
                sandbox, "_sandbox_host", return_value="unix:///sbx.sock"
            ),
            mock.patch.object(sandbox, "render", return_value=self.config),
            mock.patch.object(
                sandbox, "_compose", side_effect=self.fake_compose(calls, fail_up=True)
            ),
        ):
            with self.assertRaises(sandbox.SandboxError):
                sandbox.up([FIXTURE], ["app"])
        self.assertEqual(["up", "down"], [c[1][2] for c in calls])
        self.assertEqual([], list(self.state().iterdir()))

    def test_down_refuses_records_it_does_not_own(self):
        for project, host in (
            ("hy-home-infra", "unix:///sbx.sock"),
            ("hyhome-sbx-x", "unix:///var/run/docker.sock"),
        ):
            with self.subTest(project=project):
                (self.state() / "x.json").write_text(
                    json.dumps({"project": project, "host": host, "files": []})
                )
                with self.assertRaises(sandbox.SandboxError):
                    sandbox.down("x")
        with self.assertRaises(sandbox.SandboxError):
            sandbox.down("never-recorded")

    @unittest.skipUnless(shutil.which("docker"), "docker CLI not installed")
    def test_the_fixture_renders_with_one_allowed_closure(self):
        config = sandbox.render([FIXTURE])
        self.assertEqual(["app", "cache"], sandbox.closure(config, ["app"]))
        self.assertEqual({}, sandbox.assess(config, ["app", "cache"], self.base))
        refused = ["host-binder", "secret-user", "socket-user"]
        self.assertEqual(set(refused), set(sandbox.assess(config, refused, self.base)))

    def test_doctor_reports_without_changing_anything(self):
        report = sandbox.doctor()
        for key in ("rootless_ready", "rootless_installable", "kvm_usable", "tools"):
            self.assertIn(key, report)


if __name__ == "__main__":
    unittest.main()
