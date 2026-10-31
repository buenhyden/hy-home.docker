"""Contract relay safeguards, tested without importing a live workflow."""

import json
import subprocess
import unittest
import uuid
from pathlib import Path

WORKFLOW = Path(__file__).resolve().parents[1] / "workflow.json"


class WorkflowSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workflow = json.loads(WORKFLOW.read_text(encoding="utf-8"))
        cls.nodes = {node["name"]: node for node in cls.workflow["nodes"]}

    def get_node(self, name):
        self.assertIn(name, self.nodes)
        return self.nodes[name]

    def run_code(self, name, item):
        script = self.get_node(name)["parameters"]["jsCode"]
        program = (
            "const item = JSON.parse(process.argv[1]);\n"
            "const $input = {first: () => ({json: item})};\n"
            "const $ = () => ({first: () => ({json: {body: {items: [{}, {}]}}})});\n"
            "try { const fn = new Function('$input', '$', process.argv[2]); "
            "process.stdout.write(JSON.stringify(fn($input, $))); } "
            "catch (e) { process.stderr.write(e.message); process.exit(1); }"
        )
        return subprocess.run(
            ["node", "-e", program, json.dumps(item), script],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_workflow_is_inactive_authenticated_and_has_no_credentials(self):
        self.assertFalse(self.workflow["active"])
        webhook = self.get_node("Authenticated Ingress")["parameters"]
        self.assertEqual(webhook["authentication"], "headerAuth")
        self.assertEqual(webhook["responseMode"], "responseNode")
        self.assertNotIn("credentials", json.dumps(self.workflow))
        settings = self.workflow["settings"]
        self.assertEqual(settings["saveDataErrorExecution"], "none")
        self.assertEqual(settings["saveDataSuccessExecution"], "none")

    def test_ingress_has_stable_webhook_id_for_the_configured_path(self):
        # n8n prefixes webhook paths with workflow/node IDs if webhookId is absent.
        ingress = self.get_node("Authenticated Ingress")
        self.assertEqual(ingress["webhookId"], "e0e44720-8ff3-4c52-a052-6cd0472582c3")
        self.assertEqual(str(uuid.UUID(ingress["webhookId"])), ingress["webhookId"])
        # The exact path the Traefik router admits without SSO; nothing else is.
        self.assertEqual(ingress["parameters"]["path"], "hermes-blog-ingestion")
        self.assertEqual(ingress["parameters"]["httpMethod"], "POST")

    def test_relay_configuration_is_fixed_and_preserves_http_status(self):
        request = self.get_node("Send to Gateway")["parameters"]
        # Fixed internal Gateway on the isolated overlay network; never input-derived.
        self.assertEqual(request["url"], "http://blog-ingestion:8787/v1/ingestions")
        self.assertEqual(request["authentication"], "genericCredentialType")
        self.assertEqual(request["genericAuthType"], "httpHeaderAuth")
        self.assertEqual(
            request["options"]["redirect"]["redirect"]["followRedirects"], False
        )
        self.assertEqual(
            request["options"]["response"]["response"]["fullResponse"], True
        )
        self.assertEqual(request["options"]["response"]["response"]["neverError"], True)
        self.assertGreater(request["options"]["timeout"], 0)
        self.assertEqual(
            self.get_node("Return Gateway Response")["type"],
            "n8n-nodes-base.respondToWebhook",
        )

    def test_invalid_ingress_has_dedicated_fixed_400_response(self):
        decision = self.get_node("Input Accepted")
        self.assertEqual(decision["type"], "n8n-nodes-base.if")
        conditions = decision["parameters"]["conditions"]
        self.assertEqual(conditions["combinator"], "and")
        self.assertEqual(len(conditions["conditions"]), 1)
        condition = conditions["conditions"][0]
        self.assertEqual(condition["leftValue"], "={{ $json.valid === true }}")
        self.assertEqual(
            condition["operator"],
            {"operation": "true", "singleValue": True, "type": "boolean"},
        )
        self.assertEqual(conditions["options"]["typeValidation"], "strict")
        edges = self.workflow["connections"]["Input Accepted"]["main"]
        self.assertEqual(edges[0][0]["node"], "Send to Gateway")
        self.assertEqual(edges[1][0]["node"], "Return Invalid Input")
        response = self.get_node("Return Invalid Input")["parameters"]
        self.assertEqual(response["options"]["responseCode"], 400)
        self.assertEqual(
            json.loads(response["responseBody"]), {"error": "INVALID_REQUEST"}
        )

    def test_valid_receipt_relay_and_status_identity(self):
        receipt = {
            "id": "12345678-1234-1234-1234-123456789abc",
            "persisted": True,
            "duplicate": False,
            "status": "received",
            "candidate_count": 2,
            "status_url": "/v1/ingestions/12345678-1234-1234-1234-123456789abc",
        }
        result = self.run_code(
            "Validate Gateway Response",
            {
                "statusCode": 201,
                "body": receipt,
                "headers": {"content-type": "application/json; charset=utf-8"},
            },
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            json.loads(result.stdout)[0]["json"],
            {"statusCode": 201, "body": receipt},
        )
        receipt["duplicate"] = True
        self.assertEqual(
            self.run_code(
                "Validate Gateway Response",
                {
                    "statusCode": 200,
                    "body": receipt,
                    "headers": {"content-type": "application/json; charset=utf-8"},
                },
            ).returncode,
            0,
        )
        self.assertNotEqual(
            self.run_code(
                "Validate Gateway Response",
                {
                    "statusCode": 201,
                    "body": receipt,
                    "headers": {"content-type": "application/json; charset=utf-8"},
                },
            ).returncode,
            0,
        )
        receipt["persisted"] = False
        self.assertNotEqual(
            self.run_code(
                "Validate Gateway Response",
                {
                    "statusCode": 200,
                    "body": receipt,
                    "headers": {"content-type": "application/json; charset=utf-8"},
                },
            ).returncode,
            0,
        )

    def test_error_response_is_preserved_but_never_echoes_arbitrary_content(self):
        good = {"statusCode": 409, "body": {"error": "IDEMPOTENCY_CONFLICT"}}
        result = self.run_code("Validate Gateway Response", good)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)[0]["json"], good)
        bad = {"statusCode": 409, "body": {"error": "bad", "source_text": "secret"}}
        result = self.run_code("Validate Gateway Response", bad)
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("secret", result.stderr)

    def test_fixture_passes_screen_without_content_transformation(self):
        fixture = json.loads(
            (WORKFLOW.parent / "tests/fixtures/synthetic-report.json").read_text()
        )
        result = self.run_code("Screen Ingestion", {"body": fixture})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            json.loads(result.stdout)[0]["json"], {"valid": True, "body": fixture}
        )
        fixture["unexpected"] = "sensitive"
        result = self.run_code("Screen Ingestion", {"body": fixture})
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout), [{"json": {"valid": False}}])
        self.assertNotIn("sensitive", result.stdout)

    def test_screen_runs_in_empty_node_vm_without_url_global(self):
        fixture = json.loads(
            (WORKFLOW.parent / "tests/fixtures/synthetic-report.json").read_text()
        )
        code = self.get_node("Screen Ingestion")["parameters"]["jsCode"]
        program = (
            "const vm = require('node:vm'); "
            "const item = JSON.parse(process.argv[1]); "
            "const ctx = {$input: {first: () => ({json: {body: item}})}}; "
            "const result = vm.runInNewContext('(function(){' + process.argv[2] + '})()', ctx); "
            "process.stdout.write(JSON.stringify(result));"
        )
        result = subprocess.run(
            ["node", "-e", program, json.dumps(fixture), code],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            json.loads(result.stdout), [{"json": {"valid": True, "body": fixture}}]
        )

    def test_screen_counts_non_bmp_characters_as_code_points(self):
        fixture = json.loads(
            (WORKFLOW.parent / "tests/fixtures/synthetic-report.json").read_text()
        )
        fixture["items"][0]["title"] = "😀" * 300
        result = self.run_code("Screen Ingestion", {"body": fixture})
        self.assertEqual(result.returncode, 0, result.stderr)
        fixture["items"][0]["title"] += "😀"
        result = self.run_code("Screen Ingestion", {"body": fixture})
        self.assertEqual(json.loads(result.stdout), [{"json": {"valid": False}}])

    def test_kst_offset_on_previous_utc_day_passes_unchanged(self):
        fixture = json.loads(
            (WORKFLOW.parent / "tests/fixtures/synthetic-report.json").read_text()
        )
        mutated = dict(fixture, scheduled_at="2026-10-31T08:00:00+09:00")
        result = self.run_code("Screen Ingestion", {"body": mutated})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            json.loads(result.stdout), [{"json": {"valid": True, "body": mutated}}]
        )

    def test_invalid_times_and_source_urls_are_screened(self):
        fixture = json.loads(
            (WORKFLOW.parent / "tests/fixtures/synthetic-report.json").read_text()
        )
        for invalid in (
            "2026-10-30T00:00:00",
            "2026-02-30T00:00:00Z",
            "2026-10-30T24:00:00Z",
        ):
            mutated = dict(fixture, scheduled_at=invalid)
            result = self.run_code("Screen Ingestion", {"body": mutated})
            self.assertEqual(result.returncode, 0)
            self.assertEqual(json.loads(result.stdout), [{"json": {"valid": False}}])
        for invalid in ("https://example.org/a b", "https://example.org/\nprivate"):
            item = dict(fixture["items"][0], source_url=invalid)
            mutated = dict(fixture, items=[item])
            result = self.run_code("Screen Ingestion", {"body": mutated})
            self.assertEqual(result.returncode, 0)
            self.assertEqual(json.loads(result.stdout), [{"json": {"valid": False}}])

    def test_gateway_owns_url_parsing_and_screen_preserves_valid_forms(self):
        fixture = json.loads(
            (WORKFLOW.parent / "tests/fixtures/synthetic-report.json").read_text()
        )
        for source_url in (
            "HTTPS://example.org/a",
            "https://[::1]/",
            "https://한글.example/",
        ):
            item = dict(fixture["items"][0], source_url=source_url)
            request = dict(fixture, items=[item])
            result = self.run_code("Screen Ingestion", {"body": request})
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(
                json.loads(result.stdout), [{"json": {"valid": True, "body": request}}]
            )

    def test_success_requires_json_content_type(self):
        receipt = {
            "id": "12345678-1234-1234-1234-123456789abc",
            "persisted": True,
            "duplicate": False,
            "status": "received",
            "candidate_count": 2,
            "status_url": "/v1/ingestions/12345678-1234-1234-1234-123456789abc",
        }
        for header in (None, "text/plain"):
            result = self.run_code(
                "Validate Gateway Response",
                {
                    "statusCode": 201,
                    "body": receipt,
                    "headers": {"content-type": header},
                },
            )
            self.assertNotEqual(result.returncode, 0)

    def test_mismatched_candidate_count_fails_closed(self):
        receipt = {
            "id": "12345678-1234-1234-1234-123456789abc",
            "persisted": True,
            "duplicate": False,
            "status": "received",
            "candidate_count": 1,
            "status_url": "/v1/ingestions/12345678-1234-1234-1234-123456789abc",
        }
        result = self.run_code(
            "Validate Gateway Response",
            {
                "statusCode": 201,
                "body": receipt,
                "headers": {"content-type": "application/json; charset=utf-8"},
            },
        )
        self.assertNotEqual(result.returncode, 0)

    def test_invalid_ingress_fails_without_echoing_input(self):
        result = self.run_code(
            "Screen Ingestion", {"body": {"source_text": "sensitive"}}
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout), [{"json": {"valid": False}}])
        self.assertNotIn("sensitive", result.stdout)


if __name__ == "__main__":
    unittest.main()
