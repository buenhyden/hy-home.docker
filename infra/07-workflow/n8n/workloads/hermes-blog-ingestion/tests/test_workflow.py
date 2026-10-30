"""Static security invariants for the inactive, contract-blocked n8n stub."""

import json
import unittest
from pathlib import Path

WORKFLOW = Path(__file__).resolve().parents[1] / "workflow.json"


class WorkflowSourceTests(unittest.TestCase):
    def load_workflow(self):
        self.assertTrue(WORKFLOW.is_file(), "inactive workflow source is missing")
        return json.loads(WORKFLOW.read_text(encoding="utf-8"))

    def test_source_is_explicitly_inactive_and_contract_blocked(self):
        workflow = self.load_workflow()
        self.assertIs(workflow["active"], False)
        self.assertIn("BLOCKED_GATEWAY_CONTRACT", workflow["name"])

    def test_ingress_requires_header_auth_without_an_immediate_ack(self):
        workflow = self.load_workflow()
        webhook = next(
            node
            for node in workflow["nodes"]
            if node["type"] == "n8n-nodes-base.webhook"
        )
        self.assertEqual(webhook["parameters"]["authentication"], "headerAuth")
        self.assertEqual(webhook["parameters"]["responseMode"], "responseNode")
        self.assertEqual(webhook["parameters"]["httpMethod"], "POST")

    def test_every_ingress_path_ends_with_static_contract_error(self):
        workflow = self.load_workflow()
        nodes = {node["name"]: node for node in workflow["nodes"]}
        self.assertEqual(len(nodes), 2)
        self.assertEqual(
            {node["type"] for node in nodes.values()},
            {"n8n-nodes-base.webhook", "n8n-nodes-base.stopAndError"},
        )
        webhook = next(
            node for node in nodes.values() if node["type"] == "n8n-nodes-base.webhook"
        )
        connections = workflow["connections"]
        self.assertEqual(set(connections), {webhook["name"]})
        outputs = connections[webhook["name"]]
        self.assertEqual(set(outputs), {"main"})
        self.assertEqual(len(outputs["main"]), 1)
        self.assertEqual(len(outputs["main"][0]), 1)
        edge = outputs["main"][0][0]
        self.assertEqual((edge["type"], edge["index"]), ("main", 0))
        stop = nodes[edge["node"]]
        self.assertEqual(stop["type"], "n8n-nodes-base.stopAndError")
        self.assertEqual(stop["parameters"]["errorType"], "errorMessage")
        self.assertEqual(
            stop["parameters"]["errorMessage"], "GATEWAY_CONTRACT_NOT_BOUND"
        )
        for node in nodes.values():
            self.assertFalse(node.get("disabled", False))
            self.assertFalse(node.get("continueOnFail", False))
            self.assertIn(node.get("onError", "stopWorkflow"), ("stopWorkflow",))

    def test_execution_payload_persistence_is_disabled_and_bounded(self):
        settings = self.load_workflow()["settings"]
        self.assertIs(settings["saveExecutionProgress"], False)
        self.assertIs(settings["saveManualExecutions"], False)
        self.assertEqual(settings["saveDataErrorExecution"], "none")
        self.assertEqual(settings["saveDataSuccessExecution"], "none")
        self.assertIsInstance(settings["executionTimeout"], int)
        self.assertGreater(settings["executionTimeout"], 0)
        self.assertLessEqual(settings["executionTimeout"], 30)
        self.assertNotIn("errorWorkflow", settings)

    def test_source_contains_no_credentials_payloads_or_expressions(self):
        forbidden = {"credentials", "pinData", "staticData", "credentialId", "url"}

        def inspect(value):
            if isinstance(value, dict):
                self.assertFalse(forbidden.intersection(value))
                for child in value.values():
                    inspect(child)
            elif isinstance(value, list):
                for child in value:
                    inspect(child)
            elif isinstance(value, str):
                self.assertFalse(value.startswith("="))
                self.assertNotIn("{{", value)
                self.assertNotIn("http://", value)
                self.assertNotIn("https://", value)

        inspect(self.load_workflow())


if __name__ == "__main__":
    unittest.main()
