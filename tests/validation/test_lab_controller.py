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
            volumes={"v": {"driver_opts": {"device": "/lab/x/v"}}},
            networks={"n": {"name": "hy-home-lab-x-core"}},
        )
        rendered["services"]["a"]["volumes"].append(
            {"type": "bind", "source": "/repo/config", "read_only": True}
        )
        found = lab.footprint(rendered)
        self.assertEqual({"lab-a", "hy-home-lab-x-b-1"}, found["containers"])
        self.assertEqual({"127.0.0.1:35000"}, found["ports"])
        self.assertEqual({"/lab/x/a", "/lab/x/v"}, found["paths"])
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
        self.rendered = model(
            "hy-home-lab-cassandra",
            {"c": service("lab-cassandra-c", [("127.0.0.1", "39042")])},
            volumes={"v": {"driver_opts": {"device": str(self.data / "cassandra")}}},
        )
        self.compose_rc = 0

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def fake_run(self, command, **kwargs):
        self.calls.append(command)
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
        self.assertEqual([str(self.data / "cassandra")], entry["cleanup"]["paths"])
        self.assertTrue((self.data / "cassandra").is_dir())
        up = self.calls[-1]
        self.assertEqual(["-p", "hy-home-lab-cassandra"], up[2:4])
        self.assertEqual(["up", "-d", "--wait"], up[-3:])

        self.assertEqual(0, self.main("down", "cassandra"))
        down = self.calls[-1]
        self.assertEqual(["-p", "hy-home-lab-cassandra"], down[2:4])
        self.assertEqual(["down", "--timeout", "30"], down[-3:])
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
