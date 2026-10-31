"""The proposed Traefik route admits exactly one host-local webhook POST."""

import json
import unittest
from pathlib import Path

import yaml

WORKLOAD = Path(__file__).resolve().parents[1]
ROUTE = WORKLOAD / "traefik/hermes-webhook.yml"


class IngressRouteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = ROUTE.read_text(encoding="utf-8")
        cls.http = yaml.safe_load(cls.text)["http"]
        workflow = json.loads((WORKLOAD / "workflow.json").read_text())
        ingress = next(
            n for n in workflow["nodes"] if n["name"] == "Authenticated Ingress"
        )
        cls.path = "/webhook/" + ingress["parameters"]["path"]

    def test_file_is_a_proposal_outside_the_live_dynamic_directory(self):
        self.assertTrue(self.text.startswith("# PROPOSAL"))
        self.assertNotIn("dynamic", ROUTE.parent.name)

    def test_router_matches_only_the_workflow_path_by_post(self):
        (name,) = self.http["routers"]
        router = self.http["routers"][name]
        self.assertEqual(
            "Host(`n8n.hy.home.arpa`) && Path(`" + self.path + "`) && Method(`POST`)",
            router["rule"],
        )
        self.assertEqual(["websecure"], router["entryPoints"])
        self.assertEqual({}, router["tls"])
        self.assertEqual("n8n@docker", router["service"])
        # Higher than the Host-only SSO router, so only this exact request skips SSO.
        self.assertGreater(router["priority"], 100)

    def test_middlewares_bound_source_size_and_rate(self):
        (router,) = self.http["routers"].values()
        middlewares = self.http["middlewares"]
        self.assertEqual(set(router["middlewares"]), set(middlewares))
        kinds = {next(iter(m)): m[next(iter(m))] for m in middlewares.values()}
        self.assertEqual({"ipAllowList", "buffering", "rateLimit"}, set(kinds))
        # Host processes reach the published port through the edge_net gateway.
        self.assertEqual(["10.250.1.128/32"], kinds["ipAllowList"]["sourceRange"])
        self.assertEqual(0, kinds["ipAllowList"]["ipStrategy"]["depth"])
        # The Gateway rejects bodies above 1 MiB; stop them at the edge.
        self.assertEqual(1048576, kinds["buffering"]["maxRequestBodyBytes"])
        self.assertLessEqual(kinds["rateLimit"]["average"], 10)
        self.assertNotIn("sso", json.dumps(router))


if __name__ == "__main__":
    unittest.main()
