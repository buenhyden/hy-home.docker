"""P08 update surfaces must select their deterministic local acceptance gates."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.lib.gate.ci_gate_contract import (
    load_contract_document,
    parse_public_gate_contract,
    public_root_gate_ids,
    select_public_suites,
)

ROOT = Path(__file__).resolve().parents[2]
P08_ROUTING_MODULE = "tests.validation.test_p08_ci_routing"
INFRA_SURFACES = (
    "infra/09-platform-ops/security-updates/update-ledger.json",
    "infra/tech-stack.versions.json",
    "infra/04-data/mng-db/docker-compose.yml",
    "infra/07-workflow/n8n/docker-compose.yml",
    "infra/07-workflow/n8n/workloads/manifest-outbox-notifier/package-lock.json",
)
COMPOSE_REGRESSIONS = (
    "tests.validation.test_dev_valkey_acl",
    "tests.validation.test_mng_valkey_acl",
    "tests.validation.test_storybook_image",
    "tests.validation.test_workflow_version_bundle",
)


class P08RoutingTests(unittest.TestCase):
    def setUp(self):
        self.document = json.loads(
            (ROOT / ".github/workflow-contract.yml").read_text(encoding="utf-8")
        )
        self.nodes = {node["gate_id"]: node for node in self.document["gate_nodes"]}
        self.public = parse_public_gate_contract(load_contract_document(ROOT))

    def test_update_and_runtime_surfaces_select_local_supply_chain_and_regressions(
        self,
    ):
        for path in INFRA_SURFACES:
            with self.subTest(path=path):
                changed = (path,)
                suites = select_public_suites(self.public, "changed", changed)
                roots = public_root_gate_ids(self.public, suites, changed_paths=changed)
                self.assertIn("operations", suites)
                self.assertIn("repository-integrity", suites)
                self.assertIn("local.supply-chain", roots)
                self.assertIn("local.compose-validation", roots)
                self.assertIn("leaf.local-tech-stack-version-drift", roots)
                self.assertIn("leaf.repository-integrity-regressions", roots)

    def test_storybook_lock_selects_clean_install_and_frontend_contracts(self):
        changed = ("projects/storybook/nextjs/package-lock.json",)
        suites = select_public_suites(self.public, "changed", changed)
        roots = public_root_gate_ids(self.public, suites, changed_paths=changed)
        self.assertEqual(("repository-integrity",), suites)
        for gate_id in (
            "ci.dependency-vulnerability-audit",
            "ci.frontend-quality",
            "leaf.storybook-contract",
            "ci.storybook-coverage",
        ):
            with self.subTest(gate_id=gate_id):
                self.assertIn(gate_id, roots)

    def test_supply_chain_aggregate_keeps_both_verification_layers(self):
        self.assertEqual(
            {
                "leaf.supply-chain-fixture-policy",
                "leaf.supply-chain-deterministic-policy",
            },
            set(self.nodes["local.supply-chain"]["children"]),
        )
        fixture_argv = self.nodes["leaf.supply-chain-fixture-policy"]["argv"]
        self.assertEqual(
            1, fixture_argv.count("tests.lib.supply_chain.test_update_gates")
        )

    def test_compatibility_regressions_remain_required(self):
        argv = self.nodes["leaf.compose-baseline-regressions"]["argv"]
        required = argv[: argv.index("--optional-runtime-skips")]
        for module in COMPOSE_REGRESSIONS:
            with self.subTest(module=module):
                self.assertEqual(1, argv.count(module))
                self.assertIn(module, required)

    def test_routing_regression_is_itself_required(self):
        argv = self.nodes["leaf.repository-integrity-regressions"]["argv"]
        self.assertEqual(1, argv.count(P08_ROUTING_MODULE))

    def test_routing_regression_has_bounded_public_owners(self):
        changed = ("tests/validation/test_p08_ci_routing.py",)
        suites = select_public_suites(self.public, "changed", changed)
        self.assertEqual(("operations", "repository-integrity"), suites)


if __name__ == "__main__":
    unittest.main()
