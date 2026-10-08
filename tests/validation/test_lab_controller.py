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

ROOT = pathlib.Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "lab_controller", ROOT / "scripts/operations/lab.py"
)
lab = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(lab)


def model(project, services, volumes=None, networks=None):
    return {
        "name": project,
        "services": services,
        "volumes": volumes or {},
        "networks": networks or {},
    }


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
        self.assertEqual({"/lab/x/a", "/lab/x/v", "/lab/x/scenario"}, found["paths"])
        # A read-only input collides like state but is never a cleanup target.
        self.assertEqual({"/lab/x/a", "/lab/x/v"}, found["state"])
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
            {"name": "lab-one-x", "project": "other", "ports": {"0.0.0.0:35001"}},
            {"name": "lab-one-x", "project": "hy-home-lab-one", "ports": set()},
        ]
        problems = lab.collisions({"one": self.lab1}, self.root, running)
        self.assertEqual(2, len(problems))

    def test_budget_sums_running_and_selected_and_limits_concurrency(self) -> None:
        env = {
            "LAB_HOST_BUDGET_CPUS": "4",
            "LAB_HOST_BUDGET_MEMORY_MIB": "4096",
            "LAB_MAX_CONCURRENT": "1",
        }
        running = [
            {"project": "hy-home-infra", "cpus": 2.0, "memory": 2 * 2**30},
            {"project": "hy-home-lab-old", "cpus": 0.5, "memory": 2**29},
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
        own = [{"project": "hy-home-lab-one", "cpus": 50.0, "memory": 2**40}]
        env["LAB_HOST_BUDGET_CPUS"] = "1"
        env["LAB_HOST_BUDGET_MEMORY_MIB"] = "1024"
        self.assertEqual([], lab.budget({"one": self.lab1}, own, env))


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

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def fake_run(self, command, **kwargs):
        self.calls.append(command)
        if command[-3:] == ["up", "-d", "--wait"]:
            # The ledger must exist before anything starts.
            self.assertEqual("starting", self.ledger()["state"])
        if "config" in command:
            payload = self.rendered if "-f" in command else model("hy-home-infra", {})
            return subprocess.CompletedProcess(command, 0, json.dumps(payload), "")
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
        # Only paths under LAB_DATA_DIR are created.
        self.assertFalse(self.outside.exists())
        up = self.calls[-1]
        self.assertEqual(["-p", "hy-home-lab-cassandra"], up[2:4])
        self.assertEqual(["up", "-d", "--wait"], up[-3:])

        self.assertEqual(0, self.main("down", "cassandra"))
        down = self.calls[-1]
        self.assertEqual(["-p", "hy-home-lab-cassandra", "down"], down[2:5])
        self.assertEqual(["down", "--timeout", "30"], down[-3:])
        self.assertNotIn("-f", down)
        self.assertFalse({"-v", "--volumes", "--rmi"} & set(down))
        self.assertEqual("stopped", self.ledger()["state"])

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
