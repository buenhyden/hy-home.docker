"""Public workflow graph, SQL parameterization and generated output contracts."""

import hashlib
import importlib.util
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml

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
            "SELECT id,run_id,source,row_count,lease_token, "
            "to_char(lease_until AT TIME ZONE 'UTC', 'YYYY-MM-DD\"T\"HH24:MI:SS.MS\"Z\"') AS lease_until "
            "FROM ops_flow.claim_notification();",
            nodes["Claim"]["parameters"]["query"],
        )
        contract = json.loads((WORKLOAD / "outbox-contract.json").read_text())
        reference = contract["source_reference"]
        self.assertEqual("SOURCE_REVIEW_ONLY", reference["scope"])
        self.assertEqual("NOT_RUN", reference["native_acceptance"])
        self.assertEqual(
            contract["draft"]["claim_fields"],
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
            ("Retry Not Sent", "retry_not_sent_notification", "requeued"),
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
            "Mark Unknown",
            workflow["connections"]["Verify Retry"]["main"][1][0]["node"],
        )

    def test_ambiguous_outcomes_and_ack_loss_only_reach_quarantine(self):
        workflow = builder().build_workflow()
        connections = workflow["connections"]
        nodes = {node["name"]: node for node in workflow["nodes"]}
        for name in (
            "Capture Mail",
            "Ack",
            "Verify Ack",
            "Verify Retry",
            "Retry Not Sent",
        ):
            self.assertEqual("Mark Unknown", connections[name]["main"][1][0]["node"])
        self.assertEqual(
            "SELECT ops_flow.unknown_notification($1::bigint,$2::uuid) AS quarantined;",
            nodes["Mark Unknown"]["parameters"]["query"],
        )
        condition = nodes["Retryable Receipt"]["parameters"]["conditions"][
            "conditions"
        ][0]["leftValue"]
        self.assertIn('$json.state === "cancelled"', condition)
        self.assertNotIn('"uncertain"', condition)
        self.assertEqual(
            "Mark Unknown", connections["Retryable Receipt"]["main"][1][0]["node"]
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
        for name in ("Claim", "Ack", "Retry Not Sent", "Mark Unknown"):
            self.assertEqual("continueErrorOutput", nodes[name]["onError"])
            target = workflow["connections"][name]["main"][1][0]["node"]
            if name in ("Ack", "Retry Not Sent"):
                self.assertEqual("Mark Unknown", target)
            else:
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

    def test_tracked_interface_binds_reviewed_p04_source_without_native_authority(self):
        contract = json.loads((WORKLOAD / "outbox-contract.json").read_text())
        self.assertEqual("reviewed", contract["status"])
        self.assertEqual("NOT_RUN", contract["native_execution"])
        binding = contract["binding"]
        self.assertEqual(
            "301e55f2b7f2e67aaf4d7916f96778a880e24f90", binding["sql_commit"]
        )
        sql = ROOT / contract["canonical_sql_path"] / "001_opsflow.sql"
        self.assertEqual(
            hashlib.sha256(sql.read_bytes()).hexdigest(), binding["sql_sha256"]
        )
        self.assertEqual(1, binding["interface_version"])
        receipt_path, heading = binding["review_receipt"].split("#")
        receipt = (ROOT / receipt_path).read_text()
        self.assertEqual("restore-stable-source-handoff", heading)
        self.assertIn("#### Restore-stable source handoff", receipt)
        self.assertIn(
            "independent source/security review approved the narrow "
            "ACL-normalization correction",
            " ".join(receipt.split()),
        )
        for name, value in contract["source_reference"]["sql_sha256"].items():
            if name != "004_notification_quarantine.sql":
                self.assertIn(value, receipt)
        self.assertEqual(3, contract["source_reference"]["schema_version"])
        self.assertTrue(
            (ROOT / contract["source_reference"]["safety_review_receipt"]).is_file()
        )


class OutboxWorkerPlacementTests(unittest.TestCase):
    """Offline overlay topology; does not grant network or launch a worker."""

    def test_only_queue_worker_receives_dev_and_capture_networks(self):
        overlay = WORKLOAD / "compose.workflow.override.yml"
        self.assertTrue(overlay.is_file(), "workload overlay is missing")
        data = yaml.safe_load(overlay.read_text())
        capture_network = "opsflow_capture_net"
        self.assertEqual(
            {"version": 1, "base": "docker-compose.yml"},
            data["x-hyhome-overlay"],
        )
        self.assertEqual({"n8n-worker", "mailpit"}, set(data["services"]))
        self.assertEqual({capture_network: {"internal": True}}, data["networks"])
        worker = data["services"]["n8n-worker"]
        self.assertEqual({"dev_data_net", capture_network}, set(worker["networks"]))
        self.assertNotIn("ports", worker)
        self.assertNotIn("secrets", worker)
        self.assertEqual(
            {capture_network}, set(data["services"]["mailpit"]["networks"])
        )
        self.assertEqual(
            {"n8n-worker", "mailpit"},
            {
                name
                for name, service in data["services"].items()
                if capture_network in service["networks"]
            },
        )
        base = yaml.safe_load((WORKLOAD.parents[1] / "docker-compose.yml").read_text())
        for name in ("n8n", "n8n-worker", "n8n-task-runner", "n8n-task-runner-worker"):
            networks = set(base["services"][name]["networks"])
            self.assertFalse(
                networks & {"dev_data_net", "mail_net", capture_network}, name
            )
        self.assertNotIn("ports", base["services"]["n8n-worker"])
        mailpit = yaml.safe_load(
            (ROOT / "infra/11-quality/mailpit/docker-compose.yml").read_text()
        )["services"]["mailpit"]
        self.assertEqual({"edge_net", "mail_net"}, set(mailpit["networks"]))
        self.assertIn(
            "127.0.0.1:${MAILPIT_SMTP_HOST_PORT:-1025}:${MAILPIT_SMTP_PORT:-1025}",
            mailpit["ports"],
        )
        self.assertNotIn("stalwart", overlay.read_text().lower())


class OutboxImageBridgeTests(unittest.TestCase):
    """Execute the authored bridge against synthetic assets, never deployed data."""

    def bridge(self, name, root):
        source = (WORKLOAD.parents[1] / name).read_text()
        self.assertIn("# OPSFLOW PACKAGE BRIDGE", source)
        script = source.split("# OPSFLOW PACKAGE BRIDGE\n", 1)[1].split(
            "\n# END OPSFLOW PACKAGE BRIDGE", 1
        )[0]
        # Fixture owner and fixed image path replacement are test-only seams.
        return (
            script.replace("/opt/hyhome/n8n-custom/opsflow", str(root))
            .replace("const imageOwner = 0;", "const imageOwner = process.getuid();")
            .replace(
                "['/opt', '/opt/hyhome', '/opt/hyhome/n8n-custom']",
                json.dumps([str(root.parent)]),
            )
        )

    def test_both_builds_install_locked_unmasked_same_package(self):
        for name in ("Dockerfile", "dev.Dockerfile"):
            source = (WORKLOAD.parents[1] / name).read_text()
            self.assertIn("AS opsflow-builder", source)
            self.assertIn(
                "npm ci --ignore-scripts --no-audit --no-fund --bin-links=false", source
            )
            self.assertIn(
                "node node_modules/typescript/bin/tsc -p tsconfig.json", source
            )
            self.assertIn("npm prune --omit=dev --ignore-scripts", source)
            self.assertIn(
                "COPY --from=opsflow-builder /artifact/opsflow /opt/hyhome/n8n-custom/opsflow",
                source,
            )
            self.assertIn("SHA256SUMS", source)
        compose = yaml.safe_load(
            (WORKLOAD.parents[1] / "docker-compose.yml").read_text()
        )
        for name in ("n8n", "n8n-worker"):
            service = compose["services"][name]
            self.assertNotIn("N8N_CUSTOM_EXTENSIONS", service["environment"])
            mounts = [mount.split(":")[1] for mount in service["volumes"]]
            self.assertIn("/home/node/.n8n/custom", mounts)
            # n8n-data hides the image copy, so this bind is the only source of
            # tracked custom nodes; the container must not write code into it.
            self.assertIn("./custom:/home/node/.n8n/custom:ro", service["volumes"])
            self.assertFalse(
                any(
                    "/opt/hyhome/n8n-custom/opsflow".startswith(m + "/")
                    or m == "/opt/hyhome/n8n-custom/opsflow"
                    for m in mounts
                )
            )

    def test_bridge_is_idempotent_preserves_siblings_and_refuses_tampering(self):
        for name in ("docker-entrypoint.sh", "docker-entrypoint.dev.sh"):
            with tempfile.TemporaryDirectory() as temporary:
                base = Path(temporary)
                image = base / "image"
                image.mkdir()
                (image / "dist").mkdir()
                (image / "node_modules").mkdir()
                payloads = {
                    "package.json": '{"name":"n8n-nodes-opsflow","n8n":{"n8nNodesApiVersion":1,"nodes":["dist/OpsflowSmtp.node.js"]}}',
                    "dist/OpsflowSmtp.node.js": "synthetic source",
                    "dist/transport.js": "synthetic transport",
                    "node_modules/dependency.js": "synthetic dependency",
                }
                for path, value in payloads.items():
                    (image / path).write_text(value)
                receipt = "".join(
                    hashlib.sha256((image / p).read_bytes()).hexdigest()
                    + "  "
                    + p
                    + "\n"
                    for p in sorted(payloads)
                )
                (image / "SHA256SUMS").write_text(receipt)
                for item in (image, *image.rglob("*")):
                    item.chmod(0o755 if item.is_dir() else 0o644)
                user = base / "selected"
                sibling = user / ".n8n/nodes/node_modules/n8n-nodes-existing"
                sibling.mkdir(parents=True)
                (sibling / "preserved").write_text("keep")
                custom = user / ".n8n/custom"
                custom.mkdir()
                (custom / "existing.node.js").write_text("default keep")
                for item in (user, *user.rglob("*")):
                    if item.is_dir():
                        item.chmod(0o755)
                script = self.bridge(name, image)
                environment = {**os.environ, "N8N_USER_FOLDER": str(user)}

                def run(script=script, environment=environment):
                    return subprocess.run(
                        ["sh", "-ec", script],
                        env=environment,
                        capture_output=True,
                        text=True,
                        check=False,
                    )

                target = sibling.parent / "n8n-nodes-opsflow"
                for _ in range(2):
                    result = run()
                    self.assertEqual(0, result.returncode, result.stderr)
                    self.assertEqual(str(image), os.readlink(target))
                    self.assertEqual("keep", (sibling / "preserved").read_text())
                    self.assertEqual(
                        "default keep", (custom / "existing.node.js").read_text()
                    )
                (image / "dist/OpsflowSmtp.node.js").write_text("modified")
                result = run()
                self.assertNotEqual(0, result.returncode)
                self.assertNotIn("modified", result.stdout + result.stderr)
                (image / "dist/OpsflowSmtp.node.js").write_text(
                    payloads["dist/OpsflowSmtp.node.js"]
                )
                target.unlink()
                target.mkdir()
                (target / "unknown").write_text("keep unknown")
                self.assertNotEqual(0, run().returncode)
                self.assertEqual("keep unknown", (target / "unknown").read_text())
                (target / "unknown").unlink()
                target.rmdir()
                target.symlink_to(base / "wrong")
                self.assertNotEqual(0, run().returncode)
                self.assertEqual(str(base / "wrong"), os.readlink(target))
                target.unlink()
                dependency = image / "node_modules/dependency.js"
                dependency.unlink()
                dependency.symlink_to(base / "absent")
                self.assertNotEqual(0, run().returncode)
                dependency.unlink()
                dependency.write_text(payloads["node_modules/dependency.js"])
                dependency.chmod(0o644)
                (image / "SHA256SUMS").write_text(
                    receipt + receipt.splitlines()[0] + "\n"
                )
                self.assertNotEqual(0, run().returncode)
                (image / "SHA256SUMS").write_text(receipt)
                dependency.chmod(0o666)
                self.assertNotEqual(0, run().returncode)
                dependency.chmod(0o644)
                (image / "untracked").write_text("not in receipt")
                self.assertNotEqual(0, run().returncode)
                (image / "untracked").unlink()
                processes = [
                    subprocess.Popen(
                        ["sh", "-ec", script],
                        env=environment,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                    )
                    for _ in range(2)
                ]
                for process in processes:
                    _output, error = process.communicate(timeout=10)
                    self.assertEqual(0, process.returncode, error)
                self.assertEqual(str(image), os.readlink(target))
                environment["N8N_USER_FOLDER"] = str(user / "..")
                self.assertNotEqual(0, run().returncode)
                environment["N8N_USER_FOLDER"] = str(base / "alias")
                (base / "alias").symlink_to(user)
                self.assertNotEqual(0, run().returncode)
                del environment["N8N_USER_FOLDER"]
                fallback = script.replace("process.env.HOME", json.dumps(str(user)))
                result = subprocess.run(
                    ["sh", "-ec", fallback],
                    env=environment,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(0, result.returncode, result.stderr)
