"""Four-location declaration boundaries; all inputs are synthetic."""

import json
import unittest
from copy import deepcopy
from unittest.mock import patch

from scripts.lib.ops.port_inventory import PortContractError, parse_port, project


def service(**changes):
    return {
        "services": {
            "dev-db": {"networks": {"dev": {"aliases": ["db.internal"]}}, **changes}
        },
        "networks": {"dev": {"name": "dev"}},
    }


class PortSyntaxTests(unittest.TestCase):
    def test_optional_port_descriptions_are_bounded_strings(self):
        for value in [
            {"target": 80, "name": {}},
            {"target": 80, "app_protocol": []},
            {"target": 80, "name": "x" * 4097},
        ]:
            with self.assertRaises(PortContractError):
                parse_port(value)

    def test_concatenated_interpolation_is_unknown_and_bind_state_is_distinct(self):
        row = parse_port("${PFX}9000:80")
        self.assertEqual(row["published"], {"state": "unknown"})
        self.assertNotIn("PFX", json.dumps(row))
        states = [
            parse_port(p)["host_ip_state"]
            for p in ["9000:80", "${BIND}:9000:80", "127.0.0.1:9000:80"]
        ]
        self.assertEqual(states, ["absent", "unknown", "declared"])

    def test_ipv6_udp_range_is_lossless(self):
        row = parse_port("[::1]:16000-16002:6000-6002/udp")
        self.assertEqual(row["host_ip"], "::1")
        self.assertEqual(
            row["published"], {"state": "declared", "start": 16000, "end": 16002}
        )
        self.assertEqual(
            row["target"], {"state": "declared", "start": 6000, "end": 6002}
        )
        self.assertEqual(row["protocol"], "udp")
        self.assertEqual(row["allocation"], "paired-range")

    def test_long_published_pool_is_not_a_short_paired_range(self):
        row = parse_port(
            {
                "target": 80,
                "published": "9000-9010",
                "host_ip": "127.0.0.1",
                "protocol": "tcp",
                "mode": "host",
            }
        )
        self.assertEqual(row["allocation"], "pool")
        self.assertEqual(row["mode"], "host")

    def test_automatic_publication_is_not_unpublished(self):
        for value in [80, "80", "0:80", "127.0.0.1::80", {"target": 80}]:
            with self.subTest(value=value):
                self.assertEqual(parse_port(value)["published"], {"state": "automatic"})

    def test_unknown_source_expression_never_copies_value(self):
        row = parse_port(
            "${PUBLIC_IP:-127.0.0.1}:${PUBLIC_PORT:-9000}:${INTERNAL_PORT:-80}/udp"
        )
        self.assertEqual(row["target"], {"state": "unknown"})
        self.assertEqual(row["published"], {"state": "unknown"})
        self.assertNotIn("PUBLIC_IP", json.dumps(row))
        self.assertNotIn("127.0.0.1", json.dumps(row))

    def test_bad_ports_fail_with_fixed_errors(self):
        for value in [
            True,
            None,
            "",
            "0",
            "65536",
            "81-80",
            "9000-9001:80",
            "::1:9000:80",
            "9000:80/sctp",
            "secret@host:80",
            "80/password",
            {"target": 80, "credential": "LEAK_MARKER"},
            {"target": False},
            "${BROKEN",
        ]:
            with self.subTest(value=value):
                with self.assertRaises(PortContractError) as caught:
                    parse_port(value)
                self.assertNotIn("LEAK_MARKER", str(caught.exception))


class LocationTests(unittest.TestCase):
    def test_null_alias_and_falsy_nonmapping_definition_are_rejected(self):
        for doc in [
            {"services": {"dev": {"networks": {"dev": {"aliases": [None]}}}}},
            {"services": {"dev": {"networks": ["dev"]}}, "networks": {"dev": []}},
        ]:
            with self.assertRaises(PortContractError):
                project(doc)

    def test_document_endpoint_budget_applies_across_shared_service_inputs(self):
        shared = {
            "networks": {
                f"n{i}": {"aliases": [f"a{j}" for j in range(16)]} for i in range(16)
            },
            "expose": list(range(1, 16)),
        }
        with self.assertRaises(PortContractError):
            project({"services": {f"dev{i}": shared for i in range(6)}})

    def test_projection_caps_endpoint_product_before_materializing(self):
        doc = {
            "services": {
                "dev": {
                    "networks": {
                        f"n{i}": {"aliases": [f"a{j}" for j in range(16)]}
                        for i in range(17)
                    },
                    "expose": list(range(1, 17)),
                }
            }
        }
        with self.assertRaises(PortContractError):
            project(doc)

    def test_h2c_backend_is_a_declaration_without_runtime_proof(self):
        row = project(
            service(
                labels={
                    "traefik.http.services.dev.loadbalancer.server.port": "80",
                    "traefik.http.services.dev.loadbalancer.server.scheme": "h2c",
                }
            )
        )["services"][0]
        self.assertEqual(row["traefik_backend"]["endpoints"][0]["scheme"], "h2c")

    def test_source_evidence_scope_and_occurrence_are_strict(self):
        for paths in [
            ["docker-compose.yml/private"],
            ["infra/../private.env"],
            ["infra/a.yml", "infra/a.yml"],
        ]:
            with self.assertRaises(PortContractError):
                project(
                    {"services": {}},
                    source=[{"path": p, "sha256": "a" * 64} for p in paths],
                )

    def test_gateway_network_absent_and_unresolved_are_distinct(self):
        key = "traefik.http.services.dev.loadbalancer.server.port"
        first = project(service(labels={key: "80"}))["services"][0]
        second = project(
            service(labels={key: "80", "traefik.docker.network": "${NET}"})
        )["services"][0]
        self.assertEqual(
            first["traefik_backend"]["endpoints"][0]["network_state"], "absent"
        )
        self.assertEqual(
            second["traefik_backend"]["endpoints"][0]["network_state"], "unknown"
        )

    def test_unresolved_aliases_keep_distinct_positions_without_raw_expressions(self):
        doc = service(
            networks={"dev": {"aliases": ["keycloak.${DOMAIN}", "auth.${DOMAIN}"]}}
        )
        row = project(doc)["services"][0]
        self.assertEqual(row["internal_dns"]["state"], "unknown")
        aliases = [e for e in row["internal_dns"]["endpoints"] if e["name"] is None]
        self.assertEqual({e["alias_index"] for e in aliases}, {0, 1})
        self.assertNotIn("DOMAIN", json.dumps(row))

    def test_project_prefixed_network_name_is_unknown_without_explicit_name(self):
        row = project(
            {
                "services": {"dev": {"networks": ["isolated"]}},
                "networks": {"isolated": {}},
            }
        )["services"][0]
        endpoint = row["internal_dns"]["endpoints"][0]
        self.assertEqual(endpoint["network_key"], "isolated")
        self.assertIsNone(endpoint["network"])

    def test_declaration_does_not_invent_listener_or_runtime_acceptance(self):
        row = project(service(ports=["127.0.0.1:9000:80"], expose=["81/udp"]))[
            "services"
        ][0]
        self.assertEqual(row["listener"], {"state": "unknown", "endpoints": []})
        self.assertEqual(
            row["runtime"],
            {
                "running": "unknown",
                "healthy": "unknown",
                "used": "unknown",
                "recovered": "unknown",
            },
        )
        dns = row["internal_dns"]["endpoints"]
        self.assertEqual({x["name"] for x in dns}, {"dev-db", "db.internal"})
        self.assertEqual(
            {(x["port"]["start"], x["protocol"]) for x in dns},
            {(80, "tcp"), (81, "udp")},
        )
        self.assertEqual(row["host_publication"]["state"], "declared")

    def test_host_only_mutation_preserves_internal_and_gateway_contract(self):
        before = service(
            ports=["127.0.0.1:9000:80"],
            labels={
                "traefik.enable": "true",
                "traefik.docker.network": "dev",
                "traefik.http.services.dev.loadbalancer.server.port": "80",
            },
        )
        after = deepcopy(before)
        after["services"]["dev-db"]["ports"] = ["[::1]:19000:80"]
        first, second = [project(d)["services"][0] for d in (before, after)]
        self.assertEqual(first["internal_dns"], second["internal_dns"])
        self.assertEqual(first["traefik_backend"], second["traefik_backend"])
        self.assertNotEqual(first["host_publication"], second["host_publication"])

    def test_multiple_backends_network_identity_and_aliases(self):
        labels = {
            "traefik.enable": "true",
            "traefik.docker.network": "dev-public",
            "traefik.http.services.front.loadbalancer.server.port": "80",
            "traefik.http.services.front.loadbalancer.server.scheme": "https",
            "traefik.tcp.services.stream.loadbalancer.server.port": "9000",
            "traefik.udp.services.dns.loadbalancer.server.port": "53",
        }
        document = service(labels=[f"{k}={v}" for k, v in labels.items()], expose=[80])
        document["networks"] = {"dev": {"name": "dev-public"}}
        row = project(document)["services"][0]
        self.assertEqual(
            {
                (x["kind"], x["name"], x["port"]["start"])
                for x in row["traefik_backend"]["endpoints"]
            },
            {("http", "front", 80), ("tcp", "stream", 9000), ("udp", "dns", 53)},
        )
        self.assertTrue(
            all(
                x["network"] == "dev-public"
                for x in row["traefik_backend"]["endpoints"]
            )
        )
        self.assertEqual(row["traefik_backend"]["state"], "declared")

    def test_host_none_and_container_network_modes_do_not_invent_dns(self):
        for mode, expected in [
            ("host", "absent"),
            ("none", "absent"),
            ("service:peer", "unknown"),
        ]:
            row = project({"services": {"dev": {"network_mode": mode}}})["services"][0]
            self.assertEqual(row["internal_dns"]["state"], expected)
        with self.assertRaises(PortContractError):
            project({"services": {"dev": {"network_mode": "host", "ports": [80]}}})

    def test_absent_expose_is_unknown_port_unpublished_is_explicit(self):
        row = project({"services": {"dev": {}}})["services"][0]
        self.assertEqual(
            row["host_publication"], {"state": "unpublished", "endpoints": []}
        )
        self.assertEqual(
            row["internal_dns"]["endpoints"][0]["port"], {"state": "unknown"}
        )
        self.assertEqual(row["traefik_backend"], {"state": "unknown", "endpoints": []})

    def test_disabled_traefik_retains_declarations_without_activation(self):
        row = project(
            service(
                labels={
                    "traefik.enable": "false",
                    "traefik.http.services.dev.loadbalancer.server.port": "80",
                }
            )
        )["services"][0]
        self.assertEqual(row["traefik_backend"]["state"], "disabled")
        self.assertEqual(row["traefik_backend"]["endpoints"][0]["port"]["start"], 80)

    def test_environment_labels_commands_and_secret_payloads_are_not_projected(self):
        document = service(
            environment={"PASSWORD": "LEAK_MARKER"},
            command="LEAK_MARKER",
            secrets=["LEAK_MARKER"],
            labels={
                "private": "LEAK_MARKER",
                "traefik.http.routers.dev.rule": "LEAK_MARKER",
            },
        )
        self.assertNotIn("LEAK_MARKER", json.dumps(project(document)))
        self.assertNotIn("PASSWORD", json.dumps(project(document)))

    def test_projection_is_pure_and_does_not_mutate_input(self):
        doc = service(expose=[80])
        original = deepcopy(doc)
        with (
            patch("builtins.open", side_effect=AssertionError),
            patch("os.getenv", side_effect=AssertionError),
            patch("subprocess.run", side_effect=AssertionError),
        ):
            project(doc)
        self.assertEqual(doc, original)

    def test_backend_on_unattached_network_is_a_gap(self):
        labels = {
            "traefik.enable": "true",
            "traefik.docker.network": "mng",
            "traefik.http.services.dev.loadbalancer.server.port": "80",
        }
        row = project(service(labels=labels))["services"][0]
        self.assertEqual(row["traefik_backend"]["state"], "unknown")
        self.assertEqual(row["gaps"], ["backend-network-unattached"])

    def test_malformed_projection_never_echoes_inputs(self):
        for doc in [
            None,
            {"services": []},
            {"services": {"secret@LEAK_MARKER": {}}},
            service(expose=[False]),
            service(labels=["traefik.enable=true", "traefik.enable=false"]),
            service(networks={"dev": {"aliases": ["a@LEAK_MARKER"]}}),
        ]:
            with self.assertRaises(PortContractError) as caught:
                project(doc)
            self.assertNotIn("LEAK_MARKER", str(caught.exception))

    def test_dns_and_endpoint_dedup_is_deterministic_without_losing_protocol(self):
        doc = service(ports=["9000:80", "9000:80"], expose=[80, "80/udp"])
        self.assertEqual(project(doc), project(deepcopy(doc)))
        self.assertEqual(
            len(project(doc)["services"][0]["host_publication"]["endpoints"]), 1
        )


if __name__ == "__main__":
    unittest.main()
