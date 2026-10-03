"""WireMock mode and standalone Locust LAB contracts."""

import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


class QualityMockLabContractTest(unittest.TestCase):
    def test_wiremock_modes_have_distinct_journal_and_exposure_contracts(self):
        compose = yaml.safe_load(
            (ROOT / "infra/11-quality/wiremock/docker-compose.yml").read_text()
        )
        function = compose["services"]["wiremock"]
        load_path = ROOT / "infra/11-quality/wiremock/wiremock.load.yml"
        self.assertFalse(
            (ROOT / "infra/11-quality/wiremock/docker-compose.load.yml").exists()
        )
        self.assertTrue(load_path.is_file())
        load = load_path.read_text()

        self.assertEqual(function["profiles"], ["api-mock"])
        self.assertIn("--max-request-journal-entries", function["command"])
        self.assertNotIn("--no-request-journal", function["command"])
        self.assertEqual(set(compose["services"]), {"wiremock"})
        self.assertEqual(
            function["ports"],
            ["127.0.0.1:${WIREMOCK_HOST_PORT:-18088}:8080"],
        )
        self.assertIn("./mappings:/home/wiremock/mappings:ro", function["volumes"])
        self.assertIn("./__files:/home/wiremock/__files:ro", function["volumes"])
        self.assertEqual(function["labels"]["traefik.enable"], "false")
        self.assertNotIn("profiles:", load)
        self.assertIn("ports: !reset []", load)
        self.assertIn("--no-request-journal", load)
        self.assertIn("--admin-api-require-https", load)
        self.assertIn("http://localhost:8080/hyhome/ping", load)
        self.assertNotIn("wiremock-load:", load)
        readme = (ROOT / "infra/11-quality/wiremock/README.md").read_text()
        self.assertIn("GET /__admin/requests", readme)
        self.assertIn("HTTP 500", readme)
        self.assertIn("빈 요청 저널", readme)

    def test_locust_is_a_complete_standalone_lab(self):
        root = yaml.safe_load((ROOT / "docker-compose.yml").read_text())
        includes = root["include"]
        self.assertNotIn("infra/11-quality/locust/docker-compose.yml", includes)
        self.assertFalse((ROOT / "infra/11-quality/locust/docker-compose.yml").exists())

        lab = yaml.safe_load((ROOT / "labs/locust.yml").read_text())
        self.assertEqual(lab["name"], "hy-home-lab-locust")
        self.assertEqual(
            set(lab["services"]), {"lab-locust-master", "lab-locust-worker"}
        )
        self.assertEqual(set(lab["networks"]), {"lab_locust_net"})
        self.assertEqual(
            set(lab["volumes"]),
            {"lab-locust-scenario", "lab-locust-results"},
        )

        master = lab["services"]["lab-locust-master"]
        worker = lab["services"]["lab-locust-worker"]
        self.assertEqual(master["profiles"], ["lab-locust"])
        self.assertEqual(worker["profiles"], ["lab-locust"])
        self.assertNotIn("ports", master)
        self.assertNotIn("extra_hosts", master)
        self.assertNotIn("extra_hosts", worker)
        self.assertIn("--headless", master["command"])
        self.assertIn("--expect-workers", master["command"])
        self.assertIn("--csv-full-history", master["command"])
        self.assertIn("--exit-code-on-error", master["command"])
        self.assertIn("--worker", worker["command"])
        self.assertEqual(
            master["volumes"],
            [
                "lab-locust-scenario:/mnt/locust/scenario:ro",
                "lab-locust-results:/mnt/locust/results:rw",
            ],
        )
        self.assertEqual(
            worker["volumes"],
            ["lab-locust-scenario:/mnt/locust/scenario:ro"],
        )
        self.assertIn(
            "${LAB_LOCUST_SCENARIO_DIR:?set an approved Locust scenario directory}",
            lab["volumes"]["lab-locust-scenario"]["driver_opts"]["device"],
        )
        self.assertIn(
            "${LAB_LOCUST_RESULT_DIR:?set a fresh Locust result directory}",
            lab["volumes"]["lab-locust-results"]["driver_opts"]["device"],
        )


if __name__ == "__main__":
    unittest.main()
