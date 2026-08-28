from __future__ import annotations

import dataclasses
import errno
import json
import os
import pathlib
import subprocess
import tempfile
import unittest
from unittest import mock

from scripts.validation import ci_gate_contract as contract


ROOT = pathlib.Path(__file__).resolve().parents[2]


class PublicSuiteRegistryTests(unittest.TestCase):
    def test_gate_contract_consumes_the_immutable_public_suite_registry(self) -> None:
        registry = contract.load_public_suite_registry(ROOT / "scripts/manifest.yaml")
        self.assertEqual(
            (
                "agent-governance",
                "document-contract",
                "document-graph",
                "document-lifecycle",
                "operations",
                "repository-integrity",
            ),
            registry.public_names,
        )

    def test_public_profiles_and_changed_path_impacts_are_closed(self) -> None:
        registry = contract.load_public_suite_registry(ROOT / "scripts/manifest.yaml")
        document = contract.load_contract_document(ROOT)
        public = contract.parse_public_gate_contract(document, registry)
        self.assertEqual(("changed", "full"), public.profile_names)
        self.assertEqual(registry.public_names, public.suite_names)
        self.assertEqual(
            registry.public_names,
            contract.select_public_suites(public, "full", ()),
        )
        selected = contract.select_public_suites(
            public,
            "changed",
            ("docs/05.operations/catalog/README.md",),
        )
        self.assertIn("document-contract", selected)
        self.assertIn("document-graph", selected)
        self.assertIn("document-lifecycle", selected)
        self.assertIn("operations", selected)
        with self.assertRaises(contract.GateContractError) as raised:
            contract.select_public_suites(public, "unknown", ())
        self.assertEqual("ci-gate-profile-unknown", raised.exception.code)


INTERNAL_CI_ROOTS = {
    "docs-traceability": "ci.docs-traceability",
    "docs-implementation-alignment": "ci.docs-implementation-alignment",
    "repo-contracts": "ci.repo-contracts",
    "agent-output-eval-fixture-gate": "ci.agent-output-eval-fixture-gate",
    "supply-chain-fixture-policy": "ci.supply-chain-fixture-policy",
    "dependency-vulnerability-audit": "ci.dependency-vulnerability-audit",
    "git-flow-contract": "ci.git-flow-contract",
    "compose-validation": "ci.compose-validation",
    "compose-all-profiles-validation": "ci.compose-all-profiles-validation",
    "infrastructure-hardening": "ci.infrastructure-hardening",
    "template-security-baseline": "ci.template-security-baseline",
    "quickwin-baseline": "ci.quickwin-baseline",
    "pre-commit": "ci.pre-commit",
    "frontend-quality": "ci.frontend-quality",
    "storybook-coverage": "ci.storybook-coverage",
    "zizmor": "ci.zizmor",
}
INTERNAL_ROOT_SUITES = {
    "docs-traceability": ("docs-traceability",),
    "docs-implementation-alignment": (
        "docs-implementation-alignment",
        "docs-qa-gate-recommendations",
    ),
    "repo-contracts": (
        "repo-metadata-base",
        "repo-document-metadata",
        "ci-gate-contract-regressions",
        "ci-gate-runner-regressions",
        "ci-gate-adapter-regressions",
        "workflow-contract-regressions",
        "repo-contracts-control-plane-regressions",
        "ci-precommit-regressions",
        "workflow-contract",
        "operations-catalog-manifest",
        "repo-contracts",
    ),
    "agent-output-eval-fixture-gate": (
        "agent-output-eval-fixture-regressions",
        "agent-output-eval-fixture-gate",
    ),
    "supply-chain-fixture-policy": (
        "supply-chain-fixture-policy",
        "supply-chain-deterministic-policy",
        "supply-chain-summary-freshness",
    ),
    "dependency-vulnerability-audit": ("dependency-vulnerability-audit",),
    "git-flow-contract": ("git-flow-contract",),
    "compose-validation": ("compose-validation",),
    "compose-all-profiles-validation": ("compose-all-profiles-validation",),
    "infrastructure-hardening": ("infrastructure-hardening",),
    "template-security-baseline": ("template-security-baseline",),
    "quickwin-baseline": ("quickwin-baseline",),
    "pre-commit": ("pre-commit",),
    "frontend-quality": (
        "frontend-lint",
        "frontend-typecheck",
        "frontend-build",
        "frontend-quality",
    ),
    "storybook-coverage": ("storybook-coverage",),
    "zizmor": ("zizmor",),
}
INTERNAL_ROOT_CHILDREN = {
    "ci.docs-traceability": ("leaf.docs-traceability",),
    "ci.docs-implementation-alignment": (
        "leaf.docs-implementation-alignment",
        "leaf.docs-qa-gate-recommendations",
    ),
    "ci.repo-contracts": (
        "leaf.repo-metadata-base",
        "setup.repo-python-dependencies",
        "leaf.repo-document-metadata",
        "leaf.ci-gate-contract-regressions",
        "leaf.ci-gate-runner-regressions",
        "leaf.ci-gate-adapter-regressions",
        "leaf.workflow-contract-regressions",
        "leaf.repo-contracts-control-plane-regressions",
        "leaf.ci-precommit-regressions",
        "leaf.workflow-contract",
        "leaf.operations-catalog-manifest",
        "leaf.repo-contracts",
    ),
    "ci.agent-output-eval-fixture-gate": (
        "leaf.agent-output-eval-fixture-regressions",
        "leaf.agent-output-eval-fixture-gate",
    ),
    "ci.supply-chain-fixture-policy": (
        "leaf.supply-chain-fixture-policy",
        "leaf.supply-chain-deterministic-policy",
        "leaf.supply-chain-summary-freshness",
    ),
    "ci.dependency-vulnerability-audit": (
        "leaf.dependency-vulnerability-audit",
    ),
    "ci.git-flow-contract": ("leaf.git-flow-contract",),
    "ci.compose-validation": (
        "setup.compose-env",
        "leaf.compose-validation",
    ),
    "ci.compose-all-profiles-validation": (
        "setup.compose-env",
        "leaf.compose-all-profiles-validation",
    ),
    "ci.infrastructure-hardening": (
        "setup.compose-env",
        "leaf.infrastructure-hardening",
    ),
    "ci.template-security-baseline": (
        "setup.compose-env",
        "leaf.template-security-baseline",
    ),
    "ci.quickwin-baseline": (
        "setup.compose-env",
        "leaf.quickwin-baseline",
    ),
    "ci.pre-commit": (
        "setup.precommit-python-dependencies",
        "leaf.pre-commit",
    ),
    "ci.frontend-quality": (
        "setup.frontend-node-dependencies",
        "leaf.frontend-lint",
        "leaf.frontend-typecheck",
        "leaf.frontend-build",
        "leaf.frontend-quality",
    ),
    "ci.storybook-coverage": (
        "setup.storybook-node-dependencies",
        "setup.storybook-playwright",
        "leaf.storybook-coverage",
    ),
    "ci.zizmor": ("leaf.zizmor",),
}
REQUIRED_JOB_ROOTS = {
    "validation-changed": "ci.validation-changed",
    "validation-full": "ci.validation-full",
}
REQUIRED_ROOT_CHILDREN = {
    root_gate_id: tuple(INTERNAL_CI_ROOTS.values())
    for root_gate_id in REQUIRED_JOB_ROOTS.values()
}
ALL_CI_SUITES = tuple(
    suite
    for internal_job in INTERNAL_CI_ROOTS
    for suite in INTERNAL_ROOT_SUITES[internal_job]
)
REQUIRED_JOB_SUITES = {
    job_id: ALL_CI_SUITES for job_id in REQUIRED_JOB_ROOTS
}
LOCAL_AGGREGATE_CHILDREN = {
    "local.document-corpus-lifecycle": (
        "leaf.local-document-corpus-lifecycle-tests",
        "leaf.local-document-corpus-contract",
        "leaf.local-document-corpus-promoted",
    ),
    "local.target-surface": (
        "leaf.local-target-surface-regressions",
        "leaf.local-target-surface-contract",
        "leaf.local-target-delta-regressions",
        "leaf.local-target-delta-contract",
    ),
    "local.workflow-harness": (
        "leaf.ci-gate-contract-regressions",
        "leaf.ci-gate-runner-regressions",
        "leaf.ci-gate-adapter-regressions",
        "leaf.workflow-contract-regressions",
        "leaf.repo-contracts-control-plane-regressions",
        "leaf.ci-precommit-regressions",
        "leaf.workflow-contract",
    ),
    "local.supply-chain": (
        "leaf.supply-chain-deterministic-policy",
        "leaf.supply-chain-summary-freshness",
    ),
    "local.generated-freshness": (
        "leaf.local-security-readiness-freshness",
        "leaf.local-audit-matrix-freshness",
        "leaf.local-llm-wiki-freshness",
        "leaf.local-script-manifest",
        "leaf.operations-catalog-manifest",
    ),
    "local.compose-validation": ("leaf.compose-validation",),
    "local.compose-all-profiles-validation": (
        "leaf.compose-all-profiles-validation",
    ),
    "local.infrastructure-hardening": ("leaf.infrastructure-hardening",),
    "local.template-security-baseline": (
        "leaf.template-security-baseline",
    ),
    "local.quickwin-baseline": ("leaf.quickwin-baseline",),
}
LOCAL_SCRIPT_ROOTS = (
    "leaf.local-diff-hygiene",
    "leaf.local-shell-syntax",
    "leaf.local-provider-surface-drift",
    "ci.agent-output-eval-fixture-gate",
    "leaf.local-agent-governance-contract",
    "leaf.local-tech-stack-version-drift",
    "ci.docs-traceability",
    "leaf.docs-implementation-alignment",
    "local.document-corpus-lifecycle",
    "local.target-surface",
    "local.workflow-harness",
    "local.supply-chain",
    "local.compose-validation",
    "local.infrastructure-hardening",
    "local.template-security-baseline",
    "local.quickwin-baseline",
    "local.generated-freshness",
    "leaf.repo-contracts",
)
LOCAL_HARNESS_ROOTS = tuple(
    gate_id
    for gate_id in LOCAL_SCRIPT_ROOTS
    if gate_id
    not in {
        "leaf.local-tech-stack-version-drift",
        "local.quickwin-baseline",
    }
)
PROFILE_ROOTS = (
    contract.ProfileRoot("local-script-backed", LOCAL_SCRIPT_ROOTS, "local"),
    contract.ProfileRoot("local-harness", LOCAL_HARNESS_ROOTS, "local"),
    contract.ProfileRoot(
        "local-all-profiles",
        (*LOCAL_SCRIPT_ROOTS, "local.compose-all-profiles-validation"),
        "local",
    ),
)
PROFILE_ORDER = (
    "ci",
    "local-script-backed",
    "local-harness",
    "local-all-profiles",
)


def leaf(gate_id: str, suite_key: str) -> contract.GateNode:
    return contract.GateNode(
        gate_id=gate_id,
        kind=contract.GateKind.LEAF,
        suite_key=suite_key,
        entrypoint=pathlib.PurePosixPath(
            "scripts/validation/check-target-surface-delta-contract.py"
        ),
        argv=(),
        cwd=pathlib.PurePosixPath("."),
        allowed_env_keys=(),
        timeout_minutes=10,
        profiles=("ci",),
        opaque=True,
        children=(),
    )


def aggregate(gate_id: str, children: tuple[str, ...]) -> contract.GateNode:
    return contract.GateNode(
        gate_id=gate_id,
        kind=contract.GateKind.AGGREGATE,
        suite_key=None,
        entrypoint=None,
        argv=(),
        cwd=None,
        allowed_env_keys=(),
        timeout_minutes=None,
        profiles=("ci",),
        opaque=False,
        children=children,
    )


def setup(gate_id: str) -> contract.GateNode:
    return contract.GateNode(
        gate_id=gate_id,
        kind=contract.GateKind.SETUP,
        suite_key=None,
        entrypoint=pathlib.PurePosixPath(
            "scripts/validation/check-target-surface-delta-contract.py"
        ),
        argv=(),
        cwd=pathlib.PurePosixPath("."),
        allowed_env_keys=(),
        timeout_minutes=10,
        profiles=("ci",),
        opaque=False,
        children=(),
    )


def complete_registry() -> contract.GateRegistry:
    nodes: dict[str, contract.GateNode] = {}
    job_roots: list[contract.JobRoot] = []
    for internal_job, root_gate_id in INTERNAL_CI_ROOTS.items():
        for suite_key in INTERNAL_ROOT_SUITES[internal_job]:
            gate_id = f"leaf.{suite_key}"
            nodes.setdefault(gate_id, leaf(gate_id, suite_key))
        nodes[root_gate_id] = aggregate(
            root_gate_id,
            INTERNAL_ROOT_CHILDREN[root_gate_id],
        )
    for job_id, root_gate_id in REQUIRED_JOB_ROOTS.items():
        nodes[root_gate_id] = aggregate(
            root_gate_id,
            REQUIRED_ROOT_CHILDREN[root_gate_id],
        )
        job_roots.append(
            contract.JobRoot(
                workflow=".github/workflows/ci-quality.yml",
                job_id=job_id,
                root_gate_id=root_gate_id,
                classification="required-quality",
            )
        )

    structural_children = {
        gate_id
        for children in (
            *INTERNAL_ROOT_CHILDREN.values(),
            *REQUIRED_ROOT_CHILDREN.values(),
            *LOCAL_AGGREGATE_CHILDREN.values(),
        )
        for gate_id in children
    }
    local_direct_roots = {
        gate_id
        for profile in PROFILE_ROOTS
        for gate_id in profile.root_gate_ids
        if gate_id.startswith("leaf.")
    }
    for gate_id in structural_children | local_direct_roots:
        if gate_id.startswith("setup."):
            nodes.setdefault(gate_id, setup(gate_id))
        elif gate_id.startswith("leaf."):
            suite_key = gate_id.removeprefix("leaf.")
            nodes.setdefault(gate_id, leaf(gate_id, suite_key))
    for gate_id, children in LOCAL_AGGREGATE_CHILDREN.items():
        nodes[gate_id] = aggregate(gate_id, children)

    roots_by_profile = {
        "ci": tuple(REQUIRED_JOB_ROOTS.values()),
        **{
            profile.profile: profile.root_gate_ids
            for profile in PROFILE_ROOTS
        },
    }
    reached_by_profile: dict[str, set[str]] = {
        gate_id: set() for gate_id in nodes
    }
    for profile, roots in roots_by_profile.items():
        pending = list(reversed(roots))
        seen: set[str] = set()
        while pending:
            gate_id = pending.pop()
            if gate_id in seen:
                continue
            seen.add(gate_id)
            reached_by_profile[gate_id].add(profile)
            pending.extend(reversed(nodes[gate_id].children))
    profiled_nodes = tuple(
        dataclasses.replace(
            node,
            profiles=tuple(
                profile
                for profile in PROFILE_ORDER
                if profile in reached_by_profile[node.gate_id]
            ),
        )
        for node in nodes.values()
    )
    return contract.GateRegistry(
        nodes=profiled_nodes,
        job_roots=tuple(job_roots),
        profile_roots=PROFILE_ROOTS,
    )


def registry(
    *,
    nodes: tuple[contract.GateNode, ...] | None = None,
    job_roots: tuple[contract.JobRoot, ...] | None = None,
    profile_roots: tuple[contract.ProfileRoot, ...] | None = None,
) -> contract.GateRegistry:
    default = complete_registry()
    return contract.GateRegistry(
        nodes=nodes if nodes is not None else default.nodes,
        job_roots=(
            job_roots if job_roots is not None else default.job_roots
        ),
        profile_roots=(
            profile_roots
            if profile_roots is not None
            else default.profile_roots
        ),
    )


class CiGateContractTests(unittest.TestCase):
    def assert_codes(
        self,
        findings: tuple[contract.GateFinding, ...],
        *codes: str,
    ) -> None:
        self.assertEqual(set(codes), {finding.code for finding in findings})

    def test_operations_catalog_current_authority_is_an_exact_required_ci_leaf(self) -> None:
        registry = contract.parse_gate_registry(
            contract.load_contract_document(ROOT),
            ".github/workflow-contract.yml",
        )
        nodes = {node.gate_id: node for node in registry.nodes}
        leaf = nodes["leaf.operations-catalog-manifest"]
        self.assertEqual(
            pathlib.PurePosixPath("scripts/validation/check-operations-catalog.py"),
            leaf.entrypoint,
        )
        self.assertEqual(("--mode", "complete"), leaf.argv)
        self.assertIn("ci", leaf.profiles)
        self.assertIn(
            leaf.gate_id,
            nodes["ci.repo-contracts"].children,
        )

    def test_schema_v2_contract_is_strict_json_and_duplicate_safe(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            contract_path = root / ".github/workflow-contract.yml"
            contract_path.parent.mkdir()
            cases = (
                (
                    '{"schema_version":2,"schema_version":2,'
                    '"gate_nodes":[],"job_roots":[],"profile_roots":[]}',
                    "ci-gate-json-duplicate-key",
                ),
                (
                    "schema_version: 2\ngate_nodes: []\n"
                    "job_roots: []\nprofile_roots: []\n",
                    "ci-gate-json-invalid",
                ),
                (
                    '{"schema_version":1,"gate_nodes":[],'
                    '"job_roots":[],"profile_roots":[]}',
                    "ci-gate-schema-version",
                ),
            )
            for source, expected_code in cases:
                with self.subTest(expected_code=expected_code):
                    contract_path.write_text(source, encoding="utf-8")
                    with self.assertRaises(contract.GateContractError) as caught:
                        contract.load_contract_document(root)
                    self.assertEqual(expected_code, caught.exception.code)

            unknown = {
                "schema_version": 2,
                "gate_nodes": [],
                "job_roots": [],
                "profile_roots": [],
                "unknown": [],
            }
            with self.assertRaises(contract.GateContractError) as caught:
                contract.parse_gate_registry(
                    unknown,
                    ".github/workflow-contract.yml",
                )
            self.assertEqual("ci-gate-document-fields", caught.exception.code)

            float_schema = {
                "schema_version": 2.0,
                "gate_nodes": [],
                "job_roots": [],
                "profile_roots": [],
            }
            with self.subTest(boundary="float-schema"):
                with self.assertRaises(contract.GateContractError) as caught:
                    contract.parse_gate_registry(
                        float_schema,
                        ".github/workflow-contract.yml",
                    )
                self.assertEqual(
                    "ci-gate-schema-version",
                    caught.exception.code,
                )

            contract_path.write_text(
                '{"schema_version":2,"gate_nodes":'
                + "[" * 1500
                + "0"
                + "]" * 1500
                + ',"job_roots":[],"profile_roots":[]}',
                encoding="utf-8",
            )
            with self.subTest(boundary="deep-json"):
                with self.assertRaises(contract.GateContractError) as caught:
                    contract.load_contract_document(root)
                self.assertEqual(
                    "ci-gate-json-invalid",
                    caught.exception.code,
                )

            over_limit = {
                "schema_version": 2,
                "gate_nodes": [
                    {
                        "gate_id": f"leaf.over-{index}",
                        "kind": "leaf",
                        "suite_key": f"over-{index}",
                        "entrypoint": "scripts/check.py",
                        "argv": [],
                        "cwd": ".",
                        "allowed_env_keys": [],
                        "timeout_minutes": 10,
                        "profiles": ["ci"],
                        "opaque": True,
                    }
                    for index in range(2049)
                ],
                "job_roots": [],
                "profile_roots": [],
            }
            with self.subTest(boundary="node-limit"):
                with self.assertRaises(contract.GateContractError) as caught:
                    contract.parse_gate_registry(
                        over_limit,
                        ".github/workflow-contract.yml",
                    )
                self.assertEqual(
                    "ci-gate-node-limit",
                    caught.exception.code,
                )

    def test_gate_kind_fields_are_exact(self) -> None:
        valid_leaf = {
            "gate_id": "leaf.invalid",
            "kind": "leaf",
            "suite_key": "invalid",
            "entrypoint": "scripts/check.py",
            "argv": [],
            "cwd": ".",
            "allowed_env_keys": [],
            "timeout_minutes": 10,
            "profiles": ["ci"],
            "opaque": True,
        }
        invalid_nodes = (
            (
                {
                "gate_id": "aggregate.invalid",
                "kind": "aggregate",
                "children": [],
                "entrypoint": "scripts/check.py",
                },
                "ci-gate-kind-fields",
            ),
            (
                {**valid_leaf, "children": []},
                "ci-gate-kind-fields",
            ),
            (
                {
                "gate_id": "setup.invalid",
                "kind": "setup",
                "suite_key": "invalid",
                "entrypoint": "scripts/check.py",
                "argv": [],
                "cwd": ".",
                "allowed_env_keys": [],
                "timeout_minutes": 10,
                "profiles": ["ci"],
                "opaque": False,
                },
                "ci-gate-kind-fields",
            ),
            ({**valid_leaf, "argv": "not-an-array"}, "ci-gate-argv"),
            ({**valid_leaf, "cwd": "../outside"}, "ci-gate-cwd"),
            (
                {**valid_leaf, "allowed_env_keys": ["API_TOKEN"]},
                "ci-gate-env",
            ),
            ({**valid_leaf, "timeout_minutes": 1.5}, "ci-gate-timeout"),
            (
                {
                    **valid_leaf,
                    "profiles": ["local-script-backed", "ci"],
                },
                "ci-gate-profiles",
            ),
            ({**valid_leaf, "opaque": False}, "ci-gate-kind-fields"),
        )
        for invalid_node, expected_code in invalid_nodes:
            with self.subTest(kind=invalid_node["kind"]):
                document: dict[str, object] = {
                    "schema_version": 2,
                    "gate_nodes": [invalid_node],
                    "job_roots": [],
                    "profile_roots": [],
                }
                with self.assertRaises(contract.GateContractError) as caught:
                    contract.parse_gate_registry(
                        document,
                        ".github/workflow-contract.yml",
                    )
                self.assertEqual(
                    expected_code,
                    caught.exception.code,
                )
        self._assert_rejects_immutable_or_dangerous_execution_environment_keys()
        self._assert_canonical_registry_uses_exact_safe_environment_key_catalog()

    def test_gate_graph_rejects_cycles_missing_children_and_orphans(self) -> None:
        for mutation, expected_code in (
            ("cycle", "ci-gate-cycle"),
            ("missing-child", "ci-gate-child-missing"),
            ("orphan", "ci-gate-orphan"),
        ):
            with self.subTest(mutation=mutation):
                if mutation == "cycle":
                    candidate = registry()
                    nodes = tuple(
                        aggregate(node.gate_id, ("ci.repo-contracts",))
                        if node.gate_id == "ci.docs-traceability"
                        else aggregate(
                            node.gate_id,
                            (*node.children, "ci.docs-traceability"),
                        )
                        if node.gate_id == "ci.repo-contracts"
                        else node
                        for node in candidate.nodes
                    )
                    roots = candidate.job_roots
                elif mutation == "missing-child":
                    candidate = registry()
                    nodes = tuple(
                        aggregate(node.gate_id, ("leaf.missing",))
                        if node.gate_id == "ci.docs-traceability"
                        else node
                        for node in candidate.nodes
                    )
                    roots = candidate.job_roots
                else:
                    candidate = registry()
                    nodes = (*candidate.nodes, leaf("leaf.orphan", "orphan"))
                    roots = candidate.job_roots
                findings = contract.validate_gate_registry(
                    ROOT,
                    registry(nodes=nodes, job_roots=roots),
                )
                self.assertEqual(
                    {finding.code for finding in findings},
                    {expected_code},
                )

        depth = 1500
        deep_nodes = tuple(
            aggregate(
                f"aggregate.deep-{index}",
                (
                    (
                        f"aggregate.deep-{index + 1}"
                        if index + 1 < depth
                        else "leaf.deep"
                    ),
                ),
            )
            for index in range(depth)
        ) + (leaf("leaf.deep", "deep"),)
        deep_registry = contract.GateRegistry(
            deep_nodes,
            (),
            (
                contract.ProfileRoot(
                    "local-script-backed",
                    ("aggregate.deep-0",),
                    "local",
                ),
            ),
        )
        with self.subTest(boundary="deep-iterative-expansion"):
            self.assertEqual(
                ("leaf.deep",),
                contract.expand_gate_ids(
                    deep_registry,
                    "local-script-backed",
                    None,
                    True,
                ),
            )

        candidate = complete_registry()
        over_limit_nodes = tuple(
            dataclasses.replace(
                node,
                children=("leaf.docs-traceability",) * 8193,
            )
            if node.gate_id == "ci.docs-traceability"
            else node
            for node in candidate.nodes
        )
        with self.subTest(boundary="edge-limit"):
            self.assert_codes(
                contract.validate_gate_registry(
                    ROOT,
                    dataclasses.replace(candidate, nodes=over_limit_nodes),
                ),
                "ci-gate-edge-limit",
            )

    def test_suite_keys_and_required_owners_are_unique(self) -> None:
        candidate = registry()
        duplicate_suite_nodes = tuple(
            leaf(node.gate_id, "docs-traceability")
            if node.gate_id == "leaf.docs-implementation-alignment"
            else node
            for node in candidate.nodes
        )
        findings = contract.validate_gate_registry(
            ROOT,
            registry(
                nodes=duplicate_suite_nodes,
                job_roots=candidate.job_roots,
            ),
        )
        self.assert_codes(
            findings,
            "ci-gate-suite-duplicate",
            "ci-gate-suite-owner-duplicate",
        )

        candidate = registry()
        duplicate_path_nodes = tuple(
            aggregate(
                node.gate_id,
                (*node.children, "aggregate.duplicate-path"),
            )
            if node.gate_id == "ci.docs-traceability"
            else node
            for node in candidate.nodes
        ) + (
            aggregate(
                "aggregate.duplicate-path",
                ("leaf.docs-traceability",),
            ),
        )
        findings = contract.validate_gate_registry(
            ROOT,
            registry(
                nodes=duplicate_path_nodes,
                job_roots=candidate.job_roots,
            ),
        )
        self.assert_codes(findings, "ci-gate-internal-root-children")

    def test_required_job_roots_are_the_exact_two_workflow_jobs(self) -> None:
        candidate = complete_registry()
        findings = contract.validate_gate_registry(ROOT, candidate)
        self.assertEqual((), findings)
        findings = contract.validate_gate_registry(
            ROOT,
            contract.GateRegistry(
                candidate.nodes,
                candidate.job_roots[:-1],
                candidate.profile_roots,
            ),
        )
        self.assert_codes(findings, "ci-gate-required-job-roots")

        duplicate = contract.GateRegistry(
            candidate.nodes,
            (*candidate.job_roots, candidate.job_roots[0]),
            candidate.profile_roots,
        )
        self.assert_codes(
            contract.validate_gate_registry(ROOT, duplicate),
            "ci-gate-required-job-roots",
        )
        for label, extra in (
            (
                "third-required-job",
                contract.JobRoot(
                    ".github/workflows/ci-quality.yml",
                    "validation-third",
                    "ci.validation-full",
                    "required-quality",
                ),
            ),
            (
                "missing-workflow-job-id",
                dataclasses.replace(
                    candidate.job_roots[0], job_id="not-in-workflow"
                ),
            ),
        ):
            with self.subTest(label=label):
                mutated_jobs = (
                    (*candidate.job_roots, extra)
                    if label == "third-required-job"
                    else (extra, candidate.job_roots[1])
                )
                self.assert_codes(
                    contract.validate_gate_registry(
                        ROOT,
                        dataclasses.replace(
                            candidate, job_roots=mutated_jobs
                        ),
                    ),
                    "ci-gate-required-job-roots",
                )

        wrong_children = tuple(
            dataclasses.replace(
                node,
                children=tuple(reversed(node.children)),
            )
            if node.gate_id == "ci.repo-contracts"
            else node
            for node in candidate.nodes
        )
        with self.subTest(boundary="required-root-children"):
            self.assert_codes(
                contract.validate_gate_registry(
                    ROOT,
                    dataclasses.replace(candidate, nodes=wrong_children),
                ),
                "ci-gate-internal-root-children",
            )

        with self.subTest(boundary="hostile-git-environment"):
            with mock.patch.dict(
                os.environ,
                {
                    "GIT_DIR": "/hostile/repository",
                    "GIT_INDEX_FILE": "/hostile/index",
                    "GIT_CONFIG_GLOBAL": "/hostile/config",
                },
            ):
                self.assertEqual(
                    (),
                    contract.validate_gate_registry(ROOT, candidate),
                )

        observed: list[tuple[list[str], dict[str, object]]] = []

        def fake_git(
            arguments: list[str],
            **kwargs: object,
        ) -> subprocess.CompletedProcess[bytes]:
            observed.append((arguments, kwargs))
            return subprocess.CompletedProcess(arguments, 0)

        with self.subTest(boundary="git-command-contract"):
            with mock.patch.object(
                contract.subprocess,
                "run",
                side_effect=fake_git,
            ):
                self.assertEqual(
                    (),
                    contract.validate_gate_registry(ROOT, candidate),
                )
            self.assertEqual(1, len(observed))
            arguments, kwargs = observed[0]
            self.assertEqual(
                [
                    "git",
                    "--literal-pathspecs",
                    "ls-files",
                    "--error-unmatch",
                    "--",
                ],
                arguments[:-1],
            )
            self.assertEqual(ROOT, kwargs["cwd"])
            self.assertEqual(5, kwargs["timeout"])
            environment = kwargs["env"]
            self.assertIsInstance(environment, dict)
            self.assertFalse(
                {
                    "GIT_DIR",
                    "GIT_INDEX_FILE",
                }
                & set(environment),
            )
            self.assertEqual("/dev/null", environment["GIT_CONFIG_GLOBAL"])
            self.assertEqual("1", environment["GIT_CONFIG_NOSYSTEM"])

        with self.subTest(boundary="git-timeout"):
            with mock.patch.object(
                contract.subprocess,
                "run",
                side_effect=subprocess.TimeoutExpired(["git"], 5),
            ):
                findings = contract.validate_gate_registry(ROOT, candidate)
            self.assert_codes(findings, "ci-gate-entrypoint-invalid")

    def test_profile_roots_are_ordered_and_cannot_override_nodes(self) -> None:
        leaf_fields = {
            "kind": "leaf",
            "suite_key": "first",
            "entrypoint": (
                "scripts/validation/check-target-surface-delta-contract.py"
            ),
            "argv": [],
            "cwd": ".",
            "allowed_env_keys": [],
            "timeout_minutes": 10,
            "profiles": ["local-script-backed"],
            "opaque": True,
        }
        ordered_document: dict[str, object] = {
            "schema_version": 2,
            "gate_nodes": [
                {"gate_id": "leaf.first", **leaf_fields},
                {
                    "gate_id": "leaf.second",
                    **{**leaf_fields, "suite_key": "second"},
                },
            ],
            "job_roots": [],
            "profile_roots": [
                {
                    "profile": "local-script-backed",
                    "root_gate_ids": ["leaf.first", "leaf.second"],
                    "classification": "local",
                }
            ],
        }
        parsed = contract.parse_gate_registry(
            ordered_document,
            ".github/workflow-contract.yml",
        )
        self.assertEqual(
            ("leaf.first", "leaf.second"),
            contract.expand_gate_ids(
                parsed,
                "local-script-backed",
                None,
                True,
            ),
        )
        reversed_document = json.loads(json.dumps(ordered_document))
        reversed_document["profile_roots"][0]["root_gate_ids"].reverse()
        reversed_registry = contract.parse_gate_registry(
            reversed_document,
            ".github/workflow-contract.yml",
        )
        self.assertEqual(
            ("leaf.second", "leaf.first"),
            contract.expand_gate_ids(
                reversed_registry,
                "local-script-backed",
                None,
                True,
            ),
        )

        document = json.loads(json.dumps(ordered_document))
        document["profile_roots"][0]["gate_nodes"] = []
        with self.assertRaises(contract.GateContractError) as caught:
            contract.parse_gate_registry(document, ".github/workflow-contract.yml")
        self.assertEqual("ci-gate-profile-fields", caught.exception.code)

        wrong_classification = json.loads(json.dumps(ordered_document))
        wrong_classification["profile_roots"][0]["classification"] = (
            "local-override"
        )
        with self.subTest(boundary="profile-classification"):
            with self.assertRaises(contract.GateContractError) as caught:
                contract.parse_gate_registry(
                    wrong_classification,
                    ".github/workflow-contract.yml",
                )
            self.assertEqual(
                "ci-gate-profile-classification",
                caught.exception.code,
            )

        candidate = complete_registry()
        for aggregate_id, prohibited_child in (
            ("local.compose-validation", "setup.compose-env"),
            ("local.workflow-harness", "leaf.pre-commit"),
        ):
            with self.subTest(prohibited_child=prohibited_child):
                unsafe_nodes = tuple(
                    dataclasses.replace(
                        node,
                        children=(prohibited_child, *node.children),
                    )
                    if node.gate_id == aggregate_id
                    else node
                    for node in candidate.nodes
                )
                self.assert_codes(
                    contract.validate_gate_registry(
                        ROOT,
                        dataclasses.replace(candidate, nodes=unsafe_nodes),
                    ),
                    "ci-gate-local-unsafe",
                )

        wrong_local_children = tuple(
            dataclasses.replace(
                node,
                children=tuple(reversed(node.children)),
            )
            if node.gate_id == "local.target-surface"
            else node
            for node in candidate.nodes
        )
        with self.subTest(boundary="local-aggregate-children"):
            self.assert_codes(
                contract.validate_gate_registry(
                    ROOT,
                    dataclasses.replace(
                        candidate,
                        nodes=wrong_local_children,
                    ),
                ),
                "ci-gate-local-aggregate-children",
            )

    def test_contract_reader_rejects_symlink_noncanonical_and_oversized_inputs(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = pathlib.Path(temporary)
            real_root = base / "repo"
            contract_path = real_root / ".github/workflow-contract.yml"
            contract_path.parent.mkdir(parents=True)
            valid = {
                "schema_version": 2,
                "gate_nodes": [],
                "job_roots": [],
                "profile_roots": [],
            }
            contract_path.write_text(json.dumps(valid), encoding="utf-8")
            symlink_root = base / "repo-link"
            symlink_root.symlink_to(real_root, target_is_directory=True)
            with self.assertRaises(contract.GateContractError) as caught:
                contract.load_contract_document(symlink_root)
            self.assertEqual("ci-gate-path-noncanonical", caught.exception.code)

            github_directory = real_root / ".github"
            real_github_directory = real_root / ".github-real"
            github_directory.rename(real_github_directory)
            github_directory.symlink_to(
                real_github_directory.name,
                target_is_directory=True,
            )
            with self.subTest(boundary="symlink-parent"):
                with self.assertRaises(contract.GateContractError) as caught:
                    contract.load_contract_document(real_root)
                self.assertEqual(
                    "ci-gate-parent-invalid",
                    caught.exception.code,
                )
            github_directory.unlink()
            real_github_directory.rename(github_directory)

            github_directory.rename(real_github_directory)
            github_directory.write_text("not a directory", encoding="utf-8")
            with self.subTest(boundary="nondirectory-parent"):
                with self.assertRaises(contract.GateContractError) as caught:
                    contract.load_contract_document(real_root)
                self.assertEqual(
                    "ci-gate-parent-invalid",
                    caught.exception.code,
                )
            github_directory.unlink()
            real_github_directory.rename(github_directory)

            for error_number, expected_code in (
                (errno.ELOOP, "ci-gate-input-symlink"),
                (errno.ENOTDIR, "ci-gate-parent-invalid"),
                (errno.EACCES, "ci-gate-input-unreadable"),
            ):
                with self.subTest(open_errno=error_number):
                    with mock.patch.object(
                        contract.os,
                        "open",
                        side_effect=OSError(error_number, "sensitive"),
                    ):
                        with self.assertRaises(
                            contract.GateContractError
                        ) as caught:
                            contract.load_contract_document(real_root)
                    self.assertEqual(expected_code, caught.exception.code)
                    self.assertNotIn("sensitive", str(caught.exception))

            with self.subTest(boundary="read-error"):
                with mock.patch.object(
                    contract.os,
                    "read",
                    side_effect=OSError(errno.EIO, "sensitive"),
                ):
                    with self.assertRaises(
                        contract.GateContractError
                    ) as caught:
                        contract.load_contract_document(real_root)
                self.assertEqual(
                    "ci-gate-input-unreadable",
                    caught.exception.code,
                )
                self.assertNotIn("sensitive", str(caught.exception))

            contract_path.unlink()
            target = real_root / "contract.json"
            target.write_text(json.dumps(valid), encoding="utf-8")
            contract_path.symlink_to(target)
            with self.assertRaises(contract.GateContractError) as caught:
                contract.load_contract_document(real_root)
            self.assertEqual("ci-gate-input-symlink", caught.exception.code)

            contract_path.unlink()
            contract_path.write_bytes(b" " * (1024 * 1024 + 1))
            with self.assertRaises(contract.GateContractError) as caught:
                contract.load_contract_document(real_root)
            self.assertEqual("ci-gate-input-oversized", caught.exception.code)

            contract_path.write_bytes(b"\xff")
            with self.assertRaises(contract.GateContractError) as caught:
                contract.load_contract_document(real_root)
            self.assertEqual("ci-gate-input-non-utf8", caught.exception.code)

    def _assert_rejects_immutable_or_dangerous_execution_environment_keys(
        self,
    ) -> None:
        valid_leaf = {
            "gate_id": "leaf.safe",
            "kind": "leaf",
            "suite_key": "safe",
            "entrypoint": "scripts/check.py",
            "argv": [],
            "cwd": ".",
            "allowed_env_keys": [],
            "timeout_minutes": 10,
            "profiles": ["ci"],
            "opaque": True,
        }
        dangerous = (
            "HOME",
            "PATH",
            "LANG",
            "LC_ALL",
            "TMPDIR",
            "PYTHONPATH",
            "PYTHONSTARTUP",
            "HYHOME_CI_GATE_ROOT",
            "BASH_ENV",
            "ENV",
            "NODE_OPTIONS",
            "CDPATH",
            "IFS",
            "SHELLOPTS",
            "GLOBIGNORE",
            "GIT_DIR",
            "GIT_CONFIG_COUNT",
        )
        for key in dangerous:
            with self.subTest(key=key):
                document: dict[str, object] = {
                    "schema_version": 2,
                    "gate_nodes": [
                        {
                            **valid_leaf,
                            "allowed_env_keys": [key],
                        }
                    ],
                    "job_roots": [],
                    "profile_roots": [],
                }
                with self.assertRaises(contract.GateContractError) as caught:
                    contract.parse_gate_registry(
                        document,
                        ".github/workflow-contract.yml",
                    )
                self.assertEqual("ci-gate-env", caught.exception.code)

    def _assert_canonical_registry_uses_exact_safe_environment_key_catalog(
        self,
    ) -> None:
        document = contract.load_contract_document(ROOT)
        registry = contract.parse_gate_registry(
            document,
            ".github/workflow-contract.yml",
        )
        self.assertEqual(
            {
                "CI",
                "EVENT_NAME",
                "GITHUB_ACTIONS",
                "GITHUB_STEP_SUMMARY",
                "HEAD_REF",
                "HYHOME_COMPOSE_PROFILES",
                "PR_BASE_SHA",
                "PR_TITLE",
                "PUSH_BEFORE_SHA",
                "SKIP",
                "TEMPLATE_GATE_BASE",
            },
            {
                key
                for node in registry.nodes
                for key in node.allowed_env_keys
            },
        )


if __name__ == "__main__":
    unittest.main()
