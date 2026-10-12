"""LAB lease controller contracts (SPEC-0215)."""

from __future__ import annotations

import datetime as dt
import importlib.util
import json
import pathlib
import subprocess
import tempfile
import unittest
from unittest import mock

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "lab_controller", ROOT / "scripts/operations/lab.py"
)
lab = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(lab)


def model(project, services, volumes=None, networks=None, data_root=None):
    rendered = {
        "name": project,
        "services": services,
        "volumes": volumes or {},
        "networks": networks or {},
    }
    if data_root is not None:
        rendered["x-hyhome-data-root"] = data_root
    return rendered


def service(container=None, ports=(), binds=(), cpus=1, memory=2**30, replicas=None):
    spec = {
        "cpus": cpus,
        "mem_limit": str(memory),
        "ports": [{"host_ip": h, "published": p} for h, p in ports],
        "volumes": [{"type": "bind", "source": b} for b in binds],
    }
    if container:
        spec["container_name"] = container
    if replicas:
        spec["deploy"] = {"replicas": replicas}
    return spec


def read_only_service(container, source, target="/etc/example/config.yml"):
    spec = service(container)
    spec["volumes"] = [
        {"type": "bind", "source": source, "target": target, "read_only": True}
    ]
    return spec


def container_record(project, *, name="", ports=(), cpus=0.0, memory=0, running=True):
    return {
        "name": name,
        "project": project,
        "ports": set(ports),
        "cpus": cpus,
        "memory": memory,
        "running": running,
    }


class LabSourceContainmentTests(unittest.TestCase):
    """Permanent path contracts; no secret file, runtime or data access."""

    def test_lab_only_build_and_bind_assets_are_inside_root_labs(self) -> None:
        family = ROOT / "labs"
        for name in ("postgresql-ha", "valkey-cluster", "locust"):
            with self.subTest(lab=name):
                self.assertEqual(f"labs/{name}.yml", lab.lab_file(name))
                source = family / f"{name}.yml"
                document = yaml.safe_load(source.read_text())
                self.assertTrue(document["services"])
                for service in document["services"].values():
                    if "build" in service:
                        context = (family / service["build"]["context"]).resolve()
                        self.assertTrue(context.is_relative_to(family))
                        self.assertTrue((context / "Dockerfile").is_file())
                    for mount in service.get("volumes", []):
                        if not isinstance(mount, str):
                            continue
                        asset = mount.split(":", 1)[0]
                        if not asset.startswith("."):
                            continue  # Named state volumes are not source artifacts.
                        path = (family / asset).resolve()
                        self.assertTrue(path.is_relative_to(family), path)
                        self.assertTrue(path.is_file(), path)
                        self.assertTrue(mount.endswith(":ro"), mount)
                    if "extends" in service:
                        shared = (family / service["extends"]["file"]).resolve()
                        self.assertEqual(
                            ROOT / "infra/common-optimizations.yml", shared
                        )

    def test_each_moved_family_has_one_source_home_and_populated_readmes(self) -> None:
        for old, name in (
            ("infra/04-data/postgresql-cluster", "postgresql-ha"),
            ("infra/04-data/valkey-cluster", "valkey-cluster"),
            ("infra/11-quality/locust", "locust"),
        ):
            with self.subTest(lab=name):
                self.assertFalse((ROOT / old).exists(), old)
                family = ROOT / "labs" / name
                self.assertTrue(family.is_dir(), family)
                directories = [family, *(p for p in family.rglob("*") if p.is_dir())]
                for directory in directories:
                    readme = directory / "README.md"
                    self.assertTrue(readme.is_file(), directory)
                    self.assertIn("## Overview", readme.read_text())
                    self.assertIn("## Scope", readme.read_text())


class FootprintTests(unittest.TestCase):
    def test_footprint_counts_replicas_writable_binds_and_devices(self) -> None:
        rendered = model(
            "hy-home-lab-x",
            {
                "a": service("lab-a", [("127.0.0.1", "35000")], ["/lab/x/a"]),
                "b": service(cpus=0.5, memory=2**20, replicas=3),
            },
            volumes={
                "v": {"driver_opts": {"device": "/lab/x/v"}},
                "s": {"driver_opts": {"device": "/lab/x/scenario"}},
            },
            networks={"n": {"name": "hy-home-lab-x-core"}},
        )
        rendered["services"]["a"]["volumes"] += [
            {"type": "bind", "source": "/repo/config", "read_only": True},
            {"type": "volume", "source": "v"},
            {"type": "volume", "source": "s", "read_only": True},
        ]
        found = lab.footprint(rendered)
        replicas = {f"hy-home-lab-x-b-{i}" for i in (1, 2, 3)}
        self.assertEqual({"lab-a"} | replicas, found["containers"])
        self.assertEqual({"127.0.0.1:35000"}, found["ports"])
        self.assertEqual(
            {"/lab/x/a", "/lab/x/v", "/lab/x/scenario", "/repo/config"},
            found["paths"],
        )
        # A read-only input collides like state but is never a cleanup target.
        self.assertEqual({"/lab/x/a", "/lab/x/v"}, found["state"])
        self.assertEqual({"/lab/x/scenario", "/repo/config"}, found["inputs"])
        self.assertEqual({"hy-home-lab-x-core"}, found["networks"])
        self.assertEqual(2.5, found["cpus"])
        self.assertEqual(2**30 + 3 * 2**20, found["memory"])


class CollisionAndBudgetTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = lab.footprint(
            model(
                "hy-home-infra",
                {"pg": service("mng-pg", [("0.0.0.0", "5432")], ["/data/home/pg"])},
                networks={"n": {"name": "infra_net"}},
            )
        )
        self.lab1 = lab.footprint(
            model(
                "hy-home-lab-one",
                {"x": service("lab-one-x", [("127.0.0.1", "35001")], ["/lab/one"])},
                networks={"n": {"name": "hy-home-lab-one"}},
            )
        )

    def test_clean_selection_has_no_problem(self) -> None:
        self.assertEqual([], lab.collisions({"one": self.lab1}, self.root, []))

    def test_two_labs_with_shared_names_ports_and_paths_are_refused(self) -> None:
        lab2 = lab.footprint(
            model(
                "hy-home-lab-two",
                {
                    "x": service(
                        "lab-one-x", [("0.0.0.0", "35001")], ["/lab/one/nested"]
                    )
                },
                networks={"n": {"name": "hy-home-lab-one"}},
            )
        )
        problems = lab.collisions({"one": self.lab1, "two": lab2}, self.root, [])
        text = "\n".join(problems)
        for fragment in (
            "container lab-one-x",
            "network hy-home-lab-one",
            "host port",
            "data path",
        ):
            self.assertIn(fragment, text)

    def test_lab_inside_home_data_or_on_home_port_is_refused(self) -> None:
        bad = lab.footprint(
            model(
                "hy-home-lab-bad",
                {"x": service("lab-bad", [("127.0.0.1", "5432")], ["/data/home"])},
            )
        )
        text = "\n".join(lab.collisions({"bad": bad}, self.root, []))
        self.assertIn("host port 127.0.0.1:5432 also in root", text)
        self.assertIn("data path /data/home overlaps root", text)

    def test_lab_reusing_the_home_kafka_cluster_id_is_refused(self) -> None:
        def kafka(project, container, cluster_id):
            spec = service(container)
            spec["environment"] = {"CLUSTER_ID": cluster_id}
            return lab.footprint(model(project, {"broker": spec}))

        home = kafka("hy-home-infra", "kafka-1", "home-kraft-id")
        same = kafka("hy-home-lab-kafka", "lab-kafka-1", "home-kraft-id")
        own = kafka("hy-home-lab-kafka", "lab-kafka-1", "lab-kraft-id")
        text = "\n".join(lab.collisions({"kafka": same}, home, []))
        self.assertIn("cluster_id home-kraft-id also in root", text)
        self.assertEqual([], lab.collisions({"kafka": own}, home, []))

    def test_a_kept_volume_for_another_data_root_is_refused(self) -> None:
        rendered = model(
            "hy-home-lab-x",
            {"x": service("lab-x")},
            volumes={
                "v": {"name": "hy-home-lab-x_v", "driver_opts": {"device": "/new/v"}}
            },
        )
        selected = {"x": lab.footprint(rendered)}

        def inspect(device):
            def fake(command, **kwargs):
                self.assertEqual(subprocess.DEVNULL, kwargs.get("stdin"))
                options = json.dumps({"device": device, "o": "bind"})
                return subprocess.CompletedProcess(command, 0, options, "")

            return fake

        with mock.patch.object(lab.subprocess, "run", side_effect=inspect("/old/v")):
            text = "\n".join(lab.stale_volumes("docker", selected))
        self.assertIn("docker volume rm hy-home-lab-x_v", text)
        with mock.patch.object(lab.subprocess, "run", side_effect=inspect("/new/v")):
            self.assertEqual([], lab.stale_volumes("docker", selected))

    def test_symlink_into_home_data_is_still_an_overlap(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = pathlib.Path(tmp) / "home-data"
            home.mkdir()
            alias = pathlib.Path(tmp) / "lab-data"
            alias.symlink_to(home)
            root = lab.footprint(
                model("hy-home-infra", {"pg": service("mng-pg", binds=[str(home)])})
            )
            sneaky = lab.footprint(
                model(
                    "hy-home-lab-s", {"x": service("lab-s", binds=[str(alias / "x")])}
                )
            )
            text = "\n".join(lab.collisions({"s": sneaky}, root, []))
            self.assertIn("overlaps root", text)

    def test_running_name_and_port_are_refused_but_own_project_is_not(self) -> None:
        running = [
            container_record("other", name="lab-one-x", ports=["0.0.0.0:35001"]),
            container_record("hy-home-lab-one", name="lab-one-x", running=False),
        ]
        problems = lab.collisions({"one": self.lab1}, self.root, running)
        self.assertEqual(2, len(problems))

    def test_stopped_container_name_is_reserved_but_its_port_is_not(self) -> None:
        stopped = [
            container_record(
                "other",
                name="lab-one-x",
                ports=["0.0.0.0:35001"],
                cpus=50.0,
                memory=2**40,
                running=False,
            )
        ]
        problems = lab.collisions({"one": self.lab1}, self.root, stopped)
        self.assertEqual(["one: container lab-one-x already exists"], problems)
        stopped[0]["project"] = "hy-home-lab-one"
        self.assertEqual([], lab.collisions({"one": self.lab1}, self.root, stopped))
        stopped[0]["project"] = "hy-home-lab-old"
        env = {
            "LAB_HOST_BUDGET_CPUS": "1",
            "LAB_HOST_BUDGET_MEMORY_MIB": "1024",
            "LAB_MAX_CONCURRENT": "1",
        }
        self.assertEqual([], lab.budget({"one": self.lab1}, stopped, env))

    def test_shared_public_read_only_config_is_allowed_but_state_is_not(self) -> None:
        def readonly(project, name, source, target="/etc/example/config.yml"):
            return lab.footprint(
                model(project, {"x": read_only_service(name, source, target)})
            )

        shared = str(ROOT / "infra/common-optimizations.yml")
        one = readonly("hy-home-lab-one", "lab-one-x", shared)
        two = readonly("hy-home-lab-two", "lab-two-x", shared)
        self.assertEqual([], lab.collisions({"one": one, "two": two}, self.root, []))

        writable = lab.footprint(
            model(
                "hy-home-lab-two",
                {"x": service("lab-two-x", binds=[str(ROOT / "infra")])},
            )
        )
        self.assertIn(
            f"one: data path {shared} overlaps lab two",
            lab.collisions({"one": one, "two": writable}, self.root, []),
        )

        external_one = readonly("hy-home-lab-one", "lab-one-x", "/external/shared.yml")
        external_two = readonly("hy-home-lab-two", "lab-two-x", "/external/shared.yml")
        self.assertTrue(
            lab.collisions({"one": external_one, "two": external_two}, self.root, [])
        )

        for unsafe in (ROOT, ROOT / ".env"):
            with self.subTest(unsafe=unsafe):
                unsafe_one = readonly("hy-home-lab-one", "lab-one-x", str(unsafe))
                unsafe_two = readonly("hy-home-lab-two", "lab-two-x", str(unsafe))
                self.assertTrue(
                    lab.collisions(
                        {"one": unsafe_one, "two": unsafe_two}, self.root, []
                    )
                )

    def test_mixed_read_write_path_cannot_use_public_share_exception(self) -> None:
        shared = str(ROOT / "infra/common-optimizations.yml")
        mixed_spec = service("lab-one-x")
        mixed_spec["volumes"] = [
            {
                "type": "bind",
                "source": shared,
                "target": "/config/read-only.yml",
                "read_only": True,
            },
            {
                "type": "bind",
                "source": shared,
                "target": "/config/writable.yml",
            },
        ]
        readonly_spec = read_only_service("lab-two-x", shared, "/config/read-only.yml")
        mixed = lab.footprint(model("hy-home-lab-one", {"x": mixed_spec}))
        readonly = lab.footprint(model("hy-home-lab-two", {"x": readonly_spec}))

        self.assertIn(shared, mixed["state"])
        self.assertTrue(
            lab.collisions({"mixed": mixed, "readonly": readonly}, self.root, [])
        )

    def test_shared_secret_or_socket_input_is_refused(self) -> None:
        def readonly(project, name, source, target):
            return lab.footprint(
                model(project, {"x": read_only_service(name, source, target)})
            )

        for source, target in (
            ("/repo/secrets/token", "/run/secrets/token"),
            ("/var/run/docker.sock", "/var/run/docker.sock"),
        ):
            with self.subTest(target=target):
                one = readonly("hy-home-lab-one", "lab-one-x", source, target)
                two = readonly("hy-home-lab-two", "lab-two-x", source, target)
                text = "\n".join(
                    lab.collisions({"one": one, "two": two}, self.root, [])
                )
                self.assertIn("sensitive read-only path", text)

    def test_budget_sums_running_and_selected_and_limits_concurrency(self) -> None:
        env = {
            "LAB_HOST_BUDGET_CPUS": "4",
            "LAB_HOST_BUDGET_MEMORY_MIB": "4096",
            "LAB_MAX_CONCURRENT": "1",
        }
        running = [
            container_record("hy-home-infra", cpus=2.0, memory=2 * 2**30),
            container_record("hy-home-lab-old", cpus=0.5, memory=2**29),
        ]
        problems = lab.budget({"one": self.lab1}, running, env)
        self.assertEqual(["2 LABs would run; limit is 1"], problems)
        env["LAB_HOST_BUDGET_CPUS"] = "3"
        env["LAB_HOST_BUDGET_MEMORY_MIB"] = "3000"
        env["LAB_MAX_CONCURRENT"] = "2"
        self.assertEqual(2, len(lab.budget({"one": self.lab1}, running, env)))
        with self.assertRaises(lab.LabError):
            lab.budget({"one": self.lab1}, running, {"LAB_HOST_BUDGET_CPUS": ""})
        # The selected LAB's own running containers are not counted twice.
        own = [container_record("hy-home-lab-one", cpus=50.0, memory=2**40)]
        env["LAB_HOST_BUDGET_CPUS"] = "1"
        env["LAB_HOST_BUDGET_MEMORY_MIB"] = "1024"
        self.assertEqual([], lab.budget({"one": self.lab1}, own, env))

        stopped = [
            container_record("hy-home-lab-old", cpus=50.0, memory=2**40, running=False)
        ]
        self.assertEqual([], lab.budget({"one": self.lab1}, stopped, env))


class AdmissionGuardTests(unittest.TestCase):
    def test_root_marker_is_required_and_must_be_absolute(self) -> None:
        for marker in (None, "relative/home"):
            with self.subTest(marker=marker), self.assertRaises(lab.LabError):
                lab.root_footprint(model("hy-home-infra", {}, data_root=marker))

    def test_lab_data_root_must_not_equal_or_nest_with_home_in_either_direction(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = pathlib.Path(tmp)
            home = base / "home"
            home.mkdir()
            alias = base / "home-alias"
            alias.symlink_to(home)
            root = lab.root_footprint(model("hy-home-infra", {}, data_root=str(home)))
            for candidate in (
                home,
                home / "labs",
                base,
                alias / "labs",
                pathlib.Path("/"),
            ):
                with self.subTest(candidate=candidate):
                    problems = lab.data_root_problems(
                        {"LAB_DATA_DIR": str(candidate)}, root
                    )
                    self.assertEqual(1, len(problems))
                    self.assertIn("LAB_DATA_DIR", problems[0])

            separate = base / "separate-labs"
            self.assertEqual(
                [], lab.data_root_problems({"LAB_DATA_DIR": str(separate)}, root)
            )

    def test_read_only_sources_must_exist_without_symlink_components(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = pathlib.Path(tmp)
            real = base / "real"
            real.mkdir()
            alias = base / "alias"
            alias.symlink_to(real)

            spec = service("lab-x")
            spec["volumes"] = [
                {
                    "type": "bind",
                    "source": str(alias),
                    "target": "/config",
                    "read_only": True,
                },
                {
                    "type": "bind",
                    "source": str(base / "missing"),
                    "target": "/fixtures",
                    "read_only": True,
                },
            ]
            found = lab.footprint(model("hy-home-lab-x", {"x": spec}))
            problems = lab.path_integrity_problems({"x": found})
            self.assertTrue(any("symlink" in problem for problem in problems))
            self.assertTrue(any("does not exist" in problem for problem in problems))
            self.assertEqual(set(), found["state"])

    def test_running_container_inventory_includes_stopped_state(self) -> None:
        listed = subprocess.CompletedProcess(
            ["docker", "ps", "--all", "--quiet"], 0, "run\nstop\n", ""
        )
        records = [
            {
                "Name": "/running",
                "Config": {"Labels": {"com.docker.compose.project": "other"}},
                "HostConfig": {"NanoCpus": 10**9, "Memory": 2**30},
                "State": {"Running": True},
            },
            {
                "Name": "/stopped",
                "Config": {"Labels": {"com.docker.compose.project": "other"}},
                "HostConfig": {"NanoCpus": 9 * 10**9, "Memory": 9 * 2**30},
                "State": {"Running": False},
            },
        ]
        inspected = subprocess.CompletedProcess(
            ["docker", "inspect", "run", "stop"], 0, json.dumps(records), ""
        )
        with mock.patch.object(lab, "run", side_effect=[listed, inspected]) as called:
            found = lab.running_containers("docker")
        self.assertEqual(
            ["docker", "ps", "--all", "--quiet"], called.call_args_list[0].args[0]
        )
        self.assertEqual([True, False], [item["running"] for item in found])


class LifecycleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.data = pathlib.Path(self.tmp.name) / "lab-data"
        self.env_file = pathlib.Path(self.tmp.name) / "lab.env"
        self.env_file.write_text(
            f'LAB_DATA_DIR="{self.data}"\nLAB_HOST_BUDGET_CPUS="8"\n'
            'LAB_HOST_BUDGET_MEMORY_MIB="8192"\nLAB_MAX_CONCURRENT="1"\n',
            encoding="utf-8",
        )
        self.calls: list[list[str]] = []
        self.outside = pathlib.Path(self.tmp.name) / "outside"
        self.home_data = pathlib.Path(self.tmp.name) / "home-data"
        self.rendered = model(
            "hy-home-lab-cassandra",
            {"c": service("lab-cassandra-c", [("127.0.0.1", "39042")])},
            volumes={
                "v": {"driver_opts": {"device": str(self.data / "cassandra")}},
                "o": {"driver_opts": {"device": str(self.outside)}},
            },
        )
        self.rendered["services"]["c"]["volumes"] += [
            {"type": "volume", "source": "v"},
            {"type": "volume", "source": "o"},
        ]
        self.compose_rc = 0
        self.ready = [
            {"Id": "node", "Name": "/lab-node",
             "State": {"Status": "running", "Health": {"Status": "healthy"}}},
            {"Id": "init", "Name": "/lab-init", "State": {"Status": "exited", "ExitCode": 0}},
        ]  # fmt: skip

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def fake_run(self, command, **kwargs):
        self.calls.append(command)
        if command[-2:] == ["up", "-d"]:
            # The ledger must exist before anything starts.
            self.assertEqual("starting", self.ledger()["state"])
        if "config" in command:
            payload = (
                self.rendered
                if "-f" in command
                else model("hy-home-infra", {}, data_root=str(self.home_data))
            )
            return subprocess.CompletedProcess(command, 0, json.dumps(payload), "")
        if command[1:] == ["ps", "--all", "--quiet"]:
            return subprocess.CompletedProcess(command, 0, "", "")
        if command[1:3] == ["ps", "--all"]:
            # Readiness poll of the started project.
            ids = "\n".join(record["Id"] for record in self.ready)
            return subprocess.CompletedProcess(command, 0, ids, "")
        if command[1] == "inspect":
            return subprocess.CompletedProcess(command, 0, json.dumps(self.ready), "")
        if command[1] == "ps":
            return subprocess.CompletedProcess(command, 0, "", "")
        return subprocess.CompletedProcess(command, self.compose_rc, "", "boom")

    def main(self, *argv: str) -> int:
        with mock.patch.object(lab, "run", side_effect=self.fake_run):
            with mock.patch("sys.stdout"), mock.patch("sys.stderr"):
                return lab.main(["--env-file", str(self.env_file), *argv])

    def up(self, lease: str = "1h", purpose: str = "drill", name: str = "cassandra"):
        return self.main("up", name, "--purpose", purpose, "--lease", lease)

    def ledger(self) -> dict:
        path = self.data / ".ledger/cassandra.json"
        return json.loads(path.read_text(encoding="utf-8"))

    def started(self) -> bool:
        return any("up" in call for call in self.calls)

    def test_up_needs_purpose_and_bounded_lease(self) -> None:
        self.assertEqual(2, self.up(lease="0h"))
        self.assertEqual(2, self.up(purpose=" "))
        self.assertEqual(2, self.up(lease="25h"))
        self.assertEqual(2, self.up(name="../etc"))
        self.assertFalse(self.started())

    def test_up_records_ledger_then_down_stops_only_its_project(self) -> None:
        self.assertEqual(0, self.up(lease="2h", purpose="failover drill"))
        entry = self.ledger()
        self.assertEqual("running", entry["state"])
        self.assertEqual("hy-home-lab-cassandra", entry["project"])
        self.assertEqual(
            sorted([str(self.data / "cassandra"), str(self.outside)]),
            entry["cleanup"]["paths"],
        )
        self.assertTrue((self.data / "cassandra").is_dir())
        # Group-writable whatever the umask, for LAB processes in that group.
        self.assertEqual(0o770, (self.data / "cassandra").stat().st_mode & 0o777)
        # Only paths under LAB_DATA_DIR are created.
        self.assertFalse(self.outside.exists())
        up = next(call for call in self.calls if call[-2:] == ["up", "-d"])
        self.assertEqual(["-p", "hy-home-lab-cassandra"], up[2:4])
        self.assertEqual(["up", "-d"], up[-2:])

        self.assertEqual(0, self.main("down", "cassandra"))
        down = self.calls[-1]
        self.assertEqual(["-p", "hy-home-lab-cassandra", "down"], down[2:5])
        self.assertEqual(["down", "--timeout", "30"], down[-3:])
        self.assertNotIn("-f", down)
        self.assertFalse({"-v", "--volumes", "--rmi"} & set(down))
        self.assertEqual("stopped", self.ledger()["state"])

    def test_existing_read_only_input_is_never_created_or_recorded_for_cleanup(
        self,
    ) -> None:
        fixture = pathlib.Path(self.tmp.name) / "fixture.json"
        fixture.write_text('{"input":true}\n', encoding="utf-8")
        before = (fixture.read_bytes(), fixture.stat().st_mode)
        self.rendered["services"]["c"]["volumes"].append(
            {
                "type": "bind",
                "source": str(fixture),
                "target": "/fixtures/input.json",
                "read_only": True,
            }
        )

        self.assertEqual(0, self.up())
        self.assertNotIn(str(fixture), self.ledger()["cleanup"]["paths"])
        self.assertEqual(before, (fixture.read_bytes(), fixture.stat().st_mode))

    def test_up_waits_for_health_and_accepts_a_finished_init_job(self) -> None:
        # compose `up --wait` fails when an init job exits 0; lab.py does not.
        self.assertEqual(0, self.up())
        self.assertEqual("running", self.ledger()["state"])
        # A one-shot job that is still running is not ready yet.
        self.ready = [
            {"Id": "init", "Name": "/lab-init", "State": {"Status": "running"},
             "HostConfig": {"RestartPolicy": {"Name": "no"}}},
        ]  # fmt: skip
        with (
            mock.patch.object(lab.time, "sleep"),
            mock.patch.dict(lab.os.environ, {"LAB_READY_TIMEOUT_SECONDS": "0"}),
        ):
            self.assertEqual(1, self.up())
        for bad in (
            {"Id": "init", "Name": "/lab-init", "State": {"Status": "exited", "ExitCode": 2}},
            {"Id": "node", "Name": "/lab-node",
             "State": {"Status": "running", "Health": {"Status": "unhealthy"}}},
        ):  # fmt: skip
            with self.subTest(state=bad["State"]):
                self.ready = [bad]
                self.assertEqual(1, self.up())
                self.assertEqual("failed", self.ledger()["state"])

    def test_failed_start_and_stop_exit_non_zero(self) -> None:
        self.compose_rc = 1
        self.assertEqual(1, self.up())
        self.assertEqual("failed", self.ledger()["state"])
        self.assertEqual(1, self.main("down", "cassandra"))
        self.assertEqual("stop-failed", self.ledger()["state"])
        self.assertEqual(2, self.main("down", "valkey-cluster"))

    def test_refused_check_exits_three_without_starting(self) -> None:
        self.rendered["services"]["c"]["cpus"] = 99
        self.assertEqual(3, self.up())
        self.assertFalse(self.started())
        self.assertFalse((self.data / ".ledger/cassandra.json").exists())

    def test_missing_or_symlinked_read_only_input_is_refused_before_ledger(
        self,
    ) -> None:
        real = pathlib.Path(self.tmp.name) / "fixture"
        real.write_text("public fixture", encoding="utf-8")
        alias = pathlib.Path(self.tmp.name) / "fixture-link"
        alias.symlink_to(real)
        for source in (pathlib.Path(self.tmp.name) / "missing", alias):
            with self.subTest(source=source):
                self.calls.clear()
                self.rendered["services"]["c"]["volumes"] = [
                    {
                        "type": "bind",
                        "source": str(source),
                        "target": "/fixtures/input",
                        "read_only": True,
                    }
                ]
                self.assertEqual(3, self.up())
                self.assertFalse(self.started())
                self.assertFalse((self.data / ".ledger/cassandra.json").exists())

    def test_reap_retries_a_failed_stop_and_refuses_non_lab_ledgers(self) -> None:
        self.assertEqual(0, self.up())
        self.compose_rc = 1
        self.assertEqual(1, self.main("down", "cassandra"))
        self.assertEqual("stop-failed", self.ledger()["state"])
        entry = self.ledger()
        past = dt.datetime.now(dt.UTC) - dt.timedelta(minutes=1)
        entry["expires_at"] = past.isoformat()
        path = self.data / ".ledger/cassandra.json"
        path.write_text(json.dumps(entry))
        self.compose_rc = 0
        self.assertEqual(0, self.main("reap"))
        self.assertEqual("stopped", self.ledger()["state"])
        entry["project"] = "hy-home-infra"
        path.write_text(json.dumps(entry))
        self.calls.clear()
        self.assertEqual(2, self.main("down", "cassandra"))
        self.assertFalse(any("down" in call for call in self.calls))

    def test_bad_inputs_exit_two_instead_of_crashing(self) -> None:
        with self.env_file.open("a", encoding="utf-8") as handle:
            handle.write('LAB_MAX_LEASE_MINUTES="soon"\n')
        self.assertEqual(2, self.up())
        self.assertFalse(self.started())

    def run_job(self, wait_result, deadline: str = "5m", jobs: str = "job-1\n"):
        """`lab.py run` with a fake job container and a scripted `docker wait`."""
        original = self.fake_run

        def fake_run(command, **kwargs):
            if command[1:3] == ["ps", "--all"]:
                self.calls.append(command)
                return subprocess.CompletedProcess(command, 0, jobs, "")
            if command[1] == "wait":
                self.calls.append(command)
                self.assertEqual(300 if deadline == "5m" else 60, kwargs["timeout"])
                if isinstance(wait_result, BaseException):
                    raise wait_result
                return subprocess.CompletedProcess(command, 0, f"{wait_result}\n", "")
            return original(command, **kwargs)

        with mock.patch.object(lab, "run", side_effect=fake_run):
            with mock.patch("sys.stdout"), mock.patch("sys.stderr"):
                return lab.main(
                    ["--env-file", str(self.env_file), "run", "cassandra",
                     "--purpose", "drill", "--lease", "1h", "--deadline", deadline,
                     "--grace", "7"]
                )  # fmt: skip

    def test_run_propagates_the_job_exit_code_and_always_stops(self) -> None:
        self.assertEqual(3, self.run_job(3))
        self.assertTrue(any(call[-2:] == ["up", "-d"] for call in self.calls))
        self.assertFalse(any("--wait" in call for call in self.calls))
        self.assertEqual(["down", "--timeout", "30"], self.calls[-1][-3:])
        entry = self.ledger()
        self.assertEqual(
            ("failed", 3, "stopped"),
            (entry["outcome"], entry["job_exit_code"], entry["state"]),
        )
        self.assertFalse(any(call[1] == "stop" for call in self.calls))

    def test_run_stops_the_job_at_the_deadline_or_on_cancel(self) -> None:
        for raised, code, outcome in (
            (subprocess.TimeoutExpired("docker wait", 60), 124, "deadline_exceeded"),
            (KeyboardInterrupt(), 130, "cancelled"),
        ):
            with self.subTest(outcome=outcome):
                self.calls.clear()
                self.assertEqual(code, self.run_job(raised, deadline="1m"))
                stops = [call for call in self.calls if call[1] == "stop"]
                # SIGTERM with grace lets Locust flush its CSV before `down`.
                self.assertEqual([["docker", "stop", "--time", "7", "job-1"]], stops)
                self.assertLess(self.calls.index(stops[0]), len(self.calls) - 1)
                self.assertEqual(["down", "--timeout", "30"], self.calls[-1][-3:])
                self.assertEqual(outcome, self.ledger()["outcome"])

    def test_run_stops_a_project_whose_start_failed_or_was_cancelled(self) -> None:
        # `up -d` can exit non-zero after starting some services.
        self.compose_rc = 1
        self.assertEqual(1, self.run_job(0))
        self.compose_rc = 0
        self.assertEqual(["down", "--timeout", "30"], self.calls[-1][-3:])
        self.assertEqual("start_failed", self.ledger()["outcome"])
        original = self.fake_run

        def cancelled_up(command, **kwargs):
            if command[-2:] == ["up", "-d"]:
                self.calls.append(command)
                raise KeyboardInterrupt
            return original(command, **kwargs)

        self.calls.clear()
        with mock.patch.object(self, "fake_run", side_effect=cancelled_up):
            self.assertEqual(130, self.run_job(0))
        self.assertEqual(["down", "--timeout", "30"], self.calls[-1][-3:])
        self.assertEqual("cancelled", self.ledger()["outcome"])

    def test_run_refuses_a_deadline_beyond_the_lease_or_no_single_job(self) -> None:
        self.assertEqual(2, self.run_job(0, deadline="2h"))
        self.assertFalse(self.started())
        self.assertEqual(1, self.run_job(0, jobs="job-1\njob-2\n"))
        self.assertEqual(["down", "--timeout", "30"], self.calls[-1][-3:])

    def test_reap_stops_only_expired_leases(self) -> None:
        self.assertEqual(0, self.up())
        self.calls.clear()
        self.assertEqual(0, self.main("reap"))
        self.assertFalse(any("down" in call for call in self.calls))
        entry = self.ledger()
        past = dt.datetime.now(dt.UTC) - dt.timedelta(minutes=1)
        entry["expires_at"] = past.isoformat()
        (self.data / ".ledger/cassandra.json").write_text(json.dumps(entry))
        self.assertEqual(0, self.main("reap"))
        self.assertTrue(any("down" in call for call in self.calls))
        self.assertEqual("stopped", self.ledger()["state"])


if __name__ == "__main__":
    unittest.main()
