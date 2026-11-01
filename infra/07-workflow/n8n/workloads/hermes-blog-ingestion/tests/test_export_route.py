"""The live export host admits exactly four Gateway request shapes."""

import re
import unittest
from pathlib import Path

import yaml
from traefik_template import ENV, LIVE, SAMPLE, rendered

WORKLOAD = Path(__file__).resolve().parents[1]
ROUTE = LIVE / "blog-export.yml"
HOST = f"Host(`blog-export.{SAMPLE['DEFAULT_URL']}`)"
UUID = "[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}"
STANDARD = "gateway-standard-chain@file"
WINDOWS = [f"{SAMPLE['BLOG_EXPORT_RECEIVER_IP']}/32"]
HOST_A = [f"{SAMPLE['HOST_LAN_BIND_IP']}/32"]


class ExportRouteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = ROUTE.read_text(encoding="utf-8")
        cls.http = yaml.safe_load(rendered(cls.text))["http"]
        cls.routers = cls.http["routers"]
        cls.middlewares = cls.http["middlewares"]

    def kinds(self, router):
        found = {}
        for name in router["middlewares"]:
            if name == STANDARD:
                continue
            ((kind, value),) = self.middlewares[name].items()
            found[kind] = value
        return found

    def test_route_is_live_with_no_workload_copy(self):
        # Traefik loads the live directory at once; the workload keeps no copy.
        self.assertTrue(self.text.startswith("# LIVE"))
        self.assertFalse((WORKLOAD / "traefik").exists())

    def test_site_values_come_from_traefik_environment(self):
        # Hosts and source addresses differ per site; the route names them only
        # through variables that the Traefik service receives from Compose.
        names = {m[1] for f in LIVE.glob("*.yml") for m in ENV.finditer(f.read_text())}
        self.assertEqual(set(SAMPLE), names)
        compose = yaml.safe_load((LIVE.parent / "docker-compose.yml").read_text())
        environment = compose["services"]["traefik"]["environment"]
        for name in names:
            self.assertEqual(f"${{{name}", str(environment[name])[: len(name) + 2])

    def test_exactly_four_routes_to_the_gateway_over_tls(self):
        self.assertEqual(
            {
                "blog-export-read",
                "blog-export-ack",
                "blog-attestation",
                "blog-attestation-read",
            },
            set(self.routers),
        )
        self.assertEqual(
            {"blog-ingestion-export": {"loadBalancer": {"servers": [
                {"url": "http://blog-ingestion:8787"}]}}},
            self.http["services"],
        )  # fmt: skip
        for router in self.routers.values():
            self.assertTrue(router["rule"].startswith(HOST + " && "))
            self.assertEqual(["websecure"], router["entryPoints"])
            self.assertEqual({}, router["tls"])
            self.assertEqual("blog-ingestion-export", router["service"])
            self.assertNotIn("sso", " ".join(router["middlewares"]))
        self.assertEqual(
            set(self.middlewares),
            {m for r in self.routers.values() for m in r["middlewares"]} - {STANDARD},
        )

    def test_rules_admit_only_the_export_api_shapes(self):
        rules = {name: router["rule"] for name, router in self.routers.items()}
        self.assertEqual(
            HOST + " && Method(`GET`) && (Path(`/v1/exports`) || "
            f"PathRegexp(`^/v1/exports/{UUID}(/files/[0-9]{{1,3}})?$`))",
            rules["blog-export-read"],
        )
        self.assertEqual(
            HOST + f" && Method(`POST`) && PathRegexp(`^/v1/exports/{UUID}/acks$`)",
            rules["blog-export-ack"],
        )
        self.assertEqual(
            HOST
            + f" && Method(`POST`) && PathRegexp(`^/v1/ingestions/{UUID}/attestations$`)",
            rules["blog-attestation"],
        )
        self.assertEqual(
            HOST + " && Method(`GET`) && (Path(`/v1/attestation-queue`) || "
            f"PathRegexp(`^/v1/ingestions/{UUID}/request$`))",
            rules["blog-attestation-read"],
        )
        read = re.compile(f"^/v1/exports/{UUID}(/files/[0-9]{{1,3}})?$")
        export = "0f0e0d0c-0b0a-4908-8706-050403020100"
        for path in (f"/v1/exports/{export}", f"/v1/exports/{export}/files/0"):
            self.assertTrue(read.match(path), path)
        for path in (
            f"/v1/exports/{export}/acks",
            f"/v1/exports/{export}/files/0/x",
            f"/v1/exports/{export}/../../summary",
            "/v1/exports/../summary",
            f"/v1/exports/{export.upper()}",
        ):
            self.assertIsNone(read.match(path), path)

    def test_windows_and_host_sources_bodies_and_rates_are_bounded(self):
        read, ack, attest = (
            self.kinds(self.routers[name])
            for name in ("blog-export-read", "blog-export-ack", "blog-attestation")
        )
        for kinds, sources in ((read, WINDOWS), (ack, WINDOWS), (attest, HOST_A)):
            self.assertEqual(sources, kinds["ipAllowList"]["sourceRange"])
            self.assertEqual(0, kinds["ipAllowList"]["ipStrategy"]["depth"])
            self.assertLessEqual(kinds["rateLimit"]["average"], 120)
        self.assertEqual({"ipAllowList", "rateLimit"}, set(read))
        for kinds in (ack, attest):
            self.assertEqual({"ipAllowList", "buffering", "rateLimit"}, set(kinds))
        # ACKs are small; attestation/2 lists reach ~213 KB at 100 long URLs.
        self.assertEqual(16384, ack["buffering"]["maxRequestBodyBytes"])
        self.assertGreaterEqual(attest["buffering"]["maxRequestBodyBytes"], 230000)
        self.assertLessEqual(attest["buffering"]["maxRequestBodyBytes"], 262144)
        self.assertLessEqual(attest["rateLimit"]["average"], 10)
        reads = self.routers["blog-attestation-read"]
        self.assertEqual(
            ["blog-attestation-host", STANDARD, "blog-attestation-read-rate"],
            reads["middlewares"],
        )
        kinds = self.kinds(reads)
        self.assertEqual({"ipAllowList", "rateLimit"}, set(kinds))
        self.assertEqual(HOST_A, kinds["ipAllowList"]["sourceRange"])
        self.assertLessEqual(kinds["rateLimit"]["average"], 60)
        # POL-0013: the shared per-peer chain follows the source check on
        # every router. Then rate, then buffering: a limited request is never
        # buffered.
        for router in self.routers.values():
            self.assertEqual(STANDARD, router["middlewares"][1])
        for name in ("blog-export-ack", "blog-attestation"):
            chain = [
                next(iter(self.middlewares[m]))
                for m in self.routers[name]["middlewares"]
                if m != STANDARD
            ]
            self.assertEqual(["ipAllowList", "rateLimit", "buffering"], chain, name)


if __name__ == "__main__":
    unittest.main()
