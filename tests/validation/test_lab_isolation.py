"""LAB entrypoints stay outside the normal root (SPEC-0215)."""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LABS = sorted((ROOT / "labs").glob("*.yml"))
# Synthetic, non-HOME inputs: only enough to render each LAB model.
LAB_INPUTS = {
    "LAB_DATA_DIR": "/nonexistent/lab-data",
    "LAB_SECRET_DIR": "/nonexistent/lab-secrets",
    "LAB_KAFKA_CLUSTER_ID": "synthetic-lab-cluster",
    "LAB_LOCUST_SCENARIO_DIR": "/nonexistent/locust-scenario",
    "LAB_LOCUST_RESULT_DIR": "/nonexistent/locust-results",
    "LAB_OPENSEARCH_CERT_DIR": "/nonexistent/opensearch-certs",
}


def compose(*args: str, extra_env: dict[str, str] | None = None):
    with tempfile.TemporaryDirectory() as home:
        return subprocess.run(
            ["docker", "compose", *args],
            cwd=ROOT,
            env={"PATH": os.environ["PATH"], "HOME": home, **(extra_env or {})},
            capture_output=True,
            text=True,
            check=False,
            timeout=60,
        )


def render(*args: str, extra_env: dict[str, str] | None = None) -> dict:
    result = compose(*args, "config", "--format", "json", extra_env=extra_env)
    if result.returncode != 0:
        raise AssertionError(f"render failed: {' '.join(args)}\n{result.stderr}")
    return json.loads(result.stdout)


class RootClosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = render("--env-file", ".env.example", "--profile", "*")
        cls.labs = {
            path.name: render(
                "--env-file",
                "labs/.env.example",
                "-f",
                str(path.relative_to(ROOT)),
                "--profile",
                "*",
                extra_env=LAB_INPUTS,
            )
            for path in LABS
        }

    def test_wildcard_root_render_selects_no_lab_service(self) -> None:
        self.assertEqual(8, len(self.labs))
        root_services = set(self.root["services"])
        for name, lab in self.labs.items():
            with self.subTest(lab=name):
                self.assertEqual(set(), root_services & set(lab["services"]))

    def test_root_declares_no_lab_network_variable_or_secret(self) -> None:
        root_networks = {net.get("name") for net in self.root["networks"].values()}
        self.assertNotIn("lab_net", root_networks)
        for name, lab in self.labs.items():
            with self.subTest(lab=name):
                lab_networks = {net.get("name") for net in lab["networks"].values()}
                self.assertEqual(set(), root_networks & lab_networks)
        for secret in self.root.get("secrets", {}).values():
            self.assertNotIn("/secrets/labs/", secret.get("file", ""))
        root_text = (ROOT / "docker-compose.yml").read_text(encoding="utf-8")
        self.assertNotIn("labs/", root_text)
        self.assertNotIn("${LAB_", root_text)

    def test_a_lab_service_cannot_be_targeted_through_the_root(self) -> None:
        for name, lab in self.labs.items():
            service = sorted(lab["services"])[0]
            with self.subTest(lab=name, service=service):
                result = compose(
                    "--env-file", ".env.example", "--profile", "*", "config", service
                )
                self.assertNotEqual(0, result.returncode)
                self.assertIn("no such service", result.stderr.lower())


class LabBoundaryTests(RootClosureTests):
    def test_every_lab_volume_binds_under_a_required_lab_input(self) -> None:
        roots = tuple(value + "/" for value in LAB_INPUTS.values())
        for name, lab in self.labs.items():
            for volume, spec in (lab.get("volumes") or {}).items():
                with self.subTest(lab=name, volume=volume):
                    device = (spec.get("driver_opts") or {}).get("device", "")
                    self.assertTrue((device + "/").startswith(roots), device)

    def test_labs_are_tiered_lab_and_never_routed_by_home_traefik(self) -> None:
        for name, lab in self.labs.items():
            for service, spec in lab["services"].items():
                with self.subTest(lab=name, service=service):
                    # HOME Traefik has exposedByDefault false, so an absent
                    # label is not routed; an explicit "true" would be.
                    labels = spec.get("labels") or {}
                    self.assertEqual("lab", labels.get("hy-home.tier"))
                    self.assertNotEqual("true", labels.get("traefik.enable"))
                    self.assertFalse(
                        [key for key in labels if key.startswith("traefik.http")]
                    )

    def test_kafka_lab_tolerates_one_broker_loss_and_home_does_not(self) -> None:
        brokers = {
            name: spec["environment"]
            for name, spec in self.labs["kafka-cluster.yml"]["services"].items()
            if name.startswith("lab-kafka-") and name[-1].isdigit()
        }
        self.assertEqual(3, len(brokers))
        for env in brokers.values():
            self.assertEqual("2", str(env["KAFKA_MIN_INSYNC_REPLICAS"]))
            self.assertEqual("3", str(env["KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR"]))
        home = self.root["services"]["kafka-1"]["environment"]
        self.assertEqual("1", str(home["KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR"]))

    def test_default_lab_host_ports_collide_with_nothing(self) -> None:
        def published(model: dict) -> list[str]:
            return [
                port["published"]
                for spec in model["services"].values()
                for port in spec.get("ports", []) or []
                if port.get("published")
            ]

        seen = {port: "root" for port in published(self.root)}
        for name, lab in self.labs.items():
            for port in published(lab):
                with self.subTest(lab=name, port=port):
                    self.assertNotIn(port, seen, f"also used by {seen.get(port)}")
                    seen[port] = name


class LabInventoryAndSelectionTests(RootClosureTests):
    def test_each_lab_guide_names_exactly_its_project_and_services(self) -> None:
        import re

        for name, lab in self.labs.items():
            guide = (
                (ROOT / "labs" / name).with_suffix(".md").read_text(encoding="utf-8")
            )
            with self.subTest(lab=name):
                project = re.search(
                    r"^\| Project \| [`*]+([^`*]+)[`*]+ \|$", guide, re.M
                )
                services = re.search(r"^\| Services \| (.+) \|$", guide, re.M)
                self.assertIsNotNone(project, "guide lacks a Project row")
                self.assertIsNotNone(services, "guide lacks a Services row")
                self.assertEqual(lab["name"], project[1])
                self.assertEqual(
                    set(lab["services"]),
                    set(re.findall(r"[`*]+([^`*,]+)[`*]+", services[1])),
                )

    def test_home_prometheus_scrapes_no_lab_container(self) -> None:
        import re

        lab_hosts = {
            host
            for lab in self.labs.values()
            for name, spec in lab["services"].items()
            for host in (name, spec.get("container_name"), spec.get("hostname"))
            if host
        }
        for config in (ROOT / "infra/06-observability/prometheus/config").glob(
            "prometheus*.yml"
        ):
            targets = re.findall(
                r"""["']([A-Za-z0-9_.-]+):\d+["']""", config.read_text(encoding="utf-8")
            )
            with self.subTest(config=config.name):
                self.assertTrue(targets)
                self.assertEqual(set(), lab_hosts & set(targets))

    def test_no_document_or_script_starts_the_root_with_every_profile(self) -> None:
        import re

        # `--profile '*'` may render (config) a model; it must never start one.
        start = re.compile(
            r"""--profile[ =]+['"]?\*['"]?(?:\s+-[-\w]+(?:\s+\S+)?)*\s+(?:up|start|run|restart)\b"""
            r"""|COMPOSE_PROFILES=['"]?\*"""
        )
        tracked = subprocess.run(
            ["git", "ls-files", "--", "*.md", "*.sh", "*.py", "*.service", "Makefile"],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout.split()  # fmt: skip
        offenders = [
            path
            for path in tracked
            if not path.startswith(("docs/98.archive/", "docs/03.specs/", "tests/"))
            and path != "scripts/operations/lab.py"
            and start.search((ROOT / path).read_text(encoding="utf-8", errors="ignore"))
        ]
        self.assertEqual([], offenders)

    def test_home_selection_starts_no_lab_or_alternate_gateway(self) -> None:
        import re

        policy = (
            ROOT / "docs/05.operations/policies/0078-compose-profile-vocabulary.md"
        ).read_text(encoding="utf-8")
        row = next(line for line in policy.splitlines() if line.startswith("| HOME |"))
        profiles = re.findall(r"`([A-Za-z0-9][A-Za-z0-9_.-]*)`", row)
        self.assertTrue(profiles)
        self.assertNotIn("nginx", profiles)
        arguments = [item for name in profiles for item in ("--profile", name)]
        home = render("--env-file", ".env.example", *arguments)
        self.assertNotIn("nginx", home["services"])
        lab_services = {s for lab in self.labs.values() for s in lab["services"]}
        self.assertEqual(set(), lab_services & set(home["services"]))


if __name__ == "__main__":
    unittest.main()
