from __future__ import annotations

import json
import pathlib
import tempfile
import unittest

from scripts.validation import ci_gate_contract as contract


ROOT = pathlib.Path(__file__).resolve().parents[2]
REQUIRED_JOB_ROOTS = {
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
REQUIRED_JOB_SUITES = {
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


def registry(
    *,
    nodes: tuple[contract.GateNode, ...] | None = None,
    job_roots: tuple[contract.JobRoot, ...] | None = None,
    profile_roots: tuple[contract.ProfileRoot, ...] = (),
) -> contract.GateRegistry:
    default_nodes: list[contract.GateNode] = []
    default_roots: list[contract.JobRoot] = []
    for job_id, root_gate_id in REQUIRED_JOB_ROOTS.items():
        leaf_ids = tuple(
            f"leaf.{suite_key}" for suite_key in REQUIRED_JOB_SUITES[job_id]
        )
        default_nodes.extend(
            leaf(leaf_id, suite_key)
            for leaf_id, suite_key in zip(
                leaf_ids,
                REQUIRED_JOB_SUITES[job_id],
                strict=True,
            )
        )
        default_nodes.append(aggregate(root_gate_id, leaf_ids))
        default_roots.append(
            contract.JobRoot(
                workflow=".github/workflows/ci-quality.yml",
                job_id=job_id,
                root_gate_id=root_gate_id,
                classification="required-quality",
            )
        )
    return contract.GateRegistry(
        nodes=nodes if nodes is not None else tuple(default_nodes),
        job_roots=(
            job_roots if job_roots is not None else tuple(default_roots)
        ),
        profile_roots=profile_roots,
    )


class CiGateContractTests(unittest.TestCase):
    def assert_codes(
        self,
        findings: tuple[contract.GateFinding, ...],
        *codes: str,
    ) -> None:
        self.assertEqual(set(codes), {finding.code for finding in findings})

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

    def test_gate_kind_fields_are_exact(self) -> None:
        invalid_nodes = (
            {
                "gate_id": "aggregate.invalid",
                "kind": "aggregate",
                "children": [],
                "entrypoint": "scripts/check.py",
            },
            {
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
                "children": [],
            },
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
        )
        for invalid_node in invalid_nodes:
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
                    "ci-gate-kind-fields",
                    caught.exception.code,
                )

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
        self.assert_codes(findings, "ci-gate-suite-reachable-duplicate")

    def test_required_job_roots_are_the_exact_sixteen(self) -> None:
        candidate = registry()
        findings = contract.validate_gate_registry(ROOT, candidate)
        self.assertNotIn(
            "ci-gate-required-job-roots",
            {finding.code for finding in findings},
        )
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


if __name__ == "__main__":
    unittest.main()
