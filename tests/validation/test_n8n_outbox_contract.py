"""Public workflow graph, SQL parameterization and generated output contracts."""

import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKLOAD = ROOT / "infra/07-workflow/n8n/workloads/manifest-outbox-notifier"


def builder():
    spec = importlib.util.spec_from_file_location(
        "p05_contract_builder", WORKLOAD / "tools/build_workflow.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class OutboxContractTests(unittest.TestCase):
    def test_claim_projects_only_consumer_fields_from_p04_source(self):
        nodes = {node["name"]: node for node in builder().build_workflow()["nodes"]}
        self.assertEqual(
            "SELECT id,run_id,source,row_count,lease_token "
            "FROM ops_flow.claim_notification();",
            nodes["Claim"]["parameters"]["query"],
        )
        contract = json.loads((WORKLOAD / "outbox-contract.json").read_text())
        reference = contract["source_reference"]
        self.assertEqual("SOURCE_REVIEW_ONLY", reference["scope"])
        self.assertEqual("NOT_RUN", reference["native_acceptance"])
        self.assertEqual(
            contract["draft"]["claim_fields"] + ["lease_until"],
            reference["claim_output_fields"],
        )
        for name, expected in reference["sql_sha256"].items():
            source = ROOT / contract["canonical_sql_path"] / name
            self.assertEqual(expected, hashlib.sha256(source.read_bytes()).hexdigest())

    def test_generated_bytes_are_current_without_import_side_effects(self):
        self.assertEqual(
            builder().render_workflow(),
            (WORKLOAD / "workflows/manifest-outbox-mailpit.json").read_text(),
        )

    def test_graph_is_closed_and_has_one_inactive_polling_trigger(self):
        workflow = builder().build_workflow()
        nodes = {node["name"]: node for node in workflow["nodes"]}
        self.assertEqual(len(nodes), len(workflow["nodes"]))
        self.assertEqual(len({node["id"] for node in nodes.values()}), len(nodes))
        for source, outputs in workflow["connections"].items():
            self.assertIn(source, nodes)
            for branch in outputs["main"]:
                for edge in branch:
                    self.assertIn(edge["node"], nodes)
                    self.assertEqual(
                        {"type": "main", "index": 0},
                        {k: edge[k] for k in ("type", "index")},
                    )
        schedule = [
            node
            for node in nodes.values()
            if node["type"] == "n8n-nodes-base.scheduleTrigger"
        ]
        self.assertEqual(1, len(schedule))
        self.assertEqual(
            [{"field": "minutes", "minutesInterval": 1}],
            schedule[0]["parameters"]["rule"]["interval"],
        )
        self.assertFalse(workflow["active"])
        self.assertFalse(nodes["Claim"]["alwaysOutputData"])
        self.assertEqual(
            "Valid Claim", workflow["connections"]["Claim"]["main"][0][0]["node"]
        )
        self.assertEqual(
            "Capture Mail", workflow["connections"]["Valid Claim"]["main"][0][0]["node"]
        )

    def test_ack_retry_use_current_claim_parameters_and_strict_booleans(self):
        workflow = builder().build_workflow()
        nodes = {node["name"]: node for node in workflow["nodes"]}
        for name, function, result in (
            ("Ack", "ack_notification", "acknowledged"),
            ("Retry Unknown", "retry_notification", "requeued"),
        ):
            parameters = nodes[name]["parameters"]
            self.assertEqual(
                f"SELECT ops_flow.{function}($1::bigint,$2::uuid) AS {result};",
                parameters["query"],
            )
            self.assertEqual(
                '={{ [$("Claim").first().json.id, $("Claim").first().json.lease_token] }}',
                parameters["options"]["queryReplacement"],
            )
            guard = nodes["Verify Ack" if name == "Ack" else "Verify Retry"]
            self.assertIn(
                f"$json.{result} === true",
                guard["parameters"]["conditions"]["conditions"][0]["leftValue"],
            )
        self.assertEqual(
            "Ack", workflow["connections"]["SMTP Accepted"]["main"][0][0]["node"]
        )
        self.assertEqual(
            "Redact Lost Lease",
            workflow["connections"]["Verify Retry"]["main"][1][0]["node"],
        )

    def test_privacy_and_error_branches_have_no_unbounded_payload_options(self):
        workflow = builder().build_workflow()
        self.assertEqual({}, workflow["pinData"])
        settings = workflow["settings"]
        self.assertEqual("none", settings["saveDataSuccessExecution"])
        self.assertEqual("none", settings["saveDataErrorExecution"])
        self.assertFalse(settings["saveManualExecutions"])
        self.assertFalse(settings["saveExecutionProgress"])
        self.assertEqual(120, settings["executionTimeout"])
        nodes = {node["name"]: node for node in workflow["nodes"]}
        self.assertEqual({"claim": "={{ $json }}"}, nodes["Capture Mail"]["parameters"])
        for name in ("Claim", "Ack", "Retry Unknown"):
            self.assertEqual("continueErrorOutput", nodes[name]["onError"])
            target = workflow["connections"][name]["main"][1][0]["node"]
            self.assertTrue(target.startswith("Redact "))
            self.assertNotIn("$input", nodes[target]["parameters"]["jsCode"])
        for node in nodes.values():
            for credential in node.get("credentials", {}).values():
                self.assertEqual("REPLACE_WITH_LOCAL_CREDENTIAL_ID", credential["id"])

    def test_explicit_cli_write_and_check_detect_drift_without_rewriting(self):
        module = builder()
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "workflow.json"
            self.assertEqual(1, module.main(["--output", str(output), "--check"]))
            self.assertEqual(0, module.main(["--output", str(output)]))
            self.assertEqual(0, module.main(["--output", str(output), "--check"]))
            output.write_text("{}\n")
            self.assertEqual(1, module.main(["--output", str(output), "--check"]))
            self.assertEqual("{}\n", output.read_text())

    def test_tracked_interface_is_provisional_without_invented_authority(self):
        contract = json.loads((WORKLOAD / "outbox-contract.json").read_text())
        self.assertEqual("provisional", contract["status"])
        self.assertEqual("NOT_RUN", contract["native_execution"])
        self.assertIsNone(contract["binding"]["sql_commit"])
        self.assertIsNone(contract["binding"]["sql_sha256"])
        self.assertIsNone(contract["binding"]["interface_version"])
