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

from scripts.lib.gate import ci_gate_contract as contract


ROOT = pathlib.Path(__file__).resolve().parents[3]


class PublicSuiteRegistryTests(unittest.TestCase):
    def test_retired_job_roots_are_rejected_by_the_strict_contract(self) -> None:
        document = contract.load_contract_document(ROOT)
        document["job_roots"] = []
        with self.assertRaises(contract.GateContractError) as caught:
            contract.parse_gate_registry(document, ".github/workflow-contract.yml")
        self.assertEqual("ci-gate-document-fields", caught.exception.code)

    def test_workflow_contract_owns_the_immutable_public_suite_registry(self) -> None:
        public = contract.parse_public_gate_contract(
            contract.load_contract_document(ROOT)
        )
        self.assertEqual(
            (
                "agent-governance",
                "document-contract",
                "document-graph",
                "document-lifecycle",
                "operations",
                "repository-integrity",
            ),
            public.suite_names,
        )

    def test_public_profiles_and_changed_path_impacts_are_closed(self) -> None:
        document = contract.load_contract_document(ROOT)
        public = contract.parse_public_gate_contract(document)
        self.assertEqual(("changed", "full"), public.profile_names)
        self.assertEqual(contract.PUBLIC_SUITE_NAMES, public.suite_names)
        self.assertEqual(
            contract.PUBLIC_SUITE_NAMES,
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

    def test_changed_root_rules_are_typed_and_only_prune_optional_roots(self) -> None:
        public = contract.parse_public_gate_contract(
            contract.load_contract_document(ROOT)
        )
        optional = {"ci.frontend-quality", "ci.storybook-coverage"}
        self.assertEqual(
            optional,
            {
                gate_id
                for rule in public.changed_root_rules
                for gate_id in rule.root_gate_ids
            },
        )
        all_roots = set(contract.public_root_gate_ids(public, public.suite_names))
        self.assertLessEqual(optional, all_roots)

        known_paths = (
            "docs/03.specs/0173-governance-qa-surface-convergence/plan.md",
            ".agents/governance/sdlc.md",
            "infra/monitoring/config.yml",
        )
        for path in known_paths:
            with self.subTest(path=path):
                selected = contract.select_public_suites(public, "changed", (path,))
                roots = set(
                    contract.public_root_gate_ids(
                        public, selected, changed_paths=(path,)
                    )
                )
                self.assertFalse(optional & roots)
                repository = next(
                    route
                    for route in public.suites
                    if route.name == "repository-integrity"
                )
                self.assertLessEqual(set(repository.root_gate_ids) - optional, roots)

        relevant_paths = (
            "projects/storybook/nextjs/package-lock.json",
            "projects/storybook/nextjs/src/app/page.tsx",
            "scripts/validation/ci_gate_runner.py",
            "tests/validation/test_ci_gate_plan.py",
            ".github/workflow-contract.yml",
            ".pre-commit-config.yaml",
        )
        for path in relevant_paths:
            with self.subTest(path=path):
                selected = contract.select_public_suites(public, "changed", (path,))
                roots = set(
                    contract.public_root_gate_ids(
                        public, selected, changed_paths=(path,)
                    )
                )
                self.assertLessEqual(optional, roots)

        selected = contract.select_public_suites(
            public, "changed", ("docs/03.specs/example.md", "unknown-root.txt")
        )
        self.assertLessEqual(
            optional,
            set(
                contract.public_root_gate_ids(
                    public,
                    selected,
                    changed_paths=("docs/03.specs/example.md", "unknown-root.txt"),
                )
            ),
        )

    def test_changed_root_rules_reject_mandatory_or_unknown_roots(self) -> None:
        baseline = contract.load_contract_document(ROOT)
        for label, gate_id in (
            ("mandatory", "ci.dependency-vulnerability-audit"),
            ("unknown", "ci.unknown"),
        ):
            with self.subTest(label=label):
                candidate = json.loads(json.dumps(baseline))
                candidate["public_gate"]["changed_root_rules"][0]["root_gate_ids"] = [
                    gate_id
                ]
                with self.assertRaises(contract.GateContractError) as raised:
                    contract.parse_public_gate_contract(candidate)
                self.assertEqual("ci-gate-changed-root-rules", raised.exception.code)

    def test_public_validator_records_fail_closed_on_ownership_and_argv_drift(
        self,
    ) -> None:
        baseline = contract.load_contract_document(ROOT)
        cases: list[tuple[str, dict[str, object], str]] = []

        missing = json.loads(json.dumps(baseline))
        del missing["public_gate"]["validators"]
        cases.append(("missing-validators", missing, "ci-gate-public-contract"))

        duplicate = json.loads(json.dumps(baseline))
        duplicate["public_gate"]["validators"][1]["entrypoint"] = duplicate[
            "public_gate"
        ]["validators"][0]["entrypoint"]
        cases.append(("duplicate-entrypoint", duplicate, "ci-gate-public-validators"))

        contexts = json.loads(json.dumps(baseline))
        contexts["public_gate"]["validators"][0]["contexts"].reverse()
        cases.append(("context-order", contexts, "ci-gate-public-validators"))

        weakened = json.loads(json.dumps(baseline))
        links = next(
            row
            for row in weakened["public_gate"]["validators"]
            if row["entrypoint"] == "scripts/validation/check-document-links.py"
        )
        links["argv"] = ["--mode", "traceability"]
        cases.append(("weakened-capability", weakened, "ci-gate-validator-arguments"))

        for label, document, expected_code in cases:
            with self.subTest(label=label):
                with self.assertRaises(contract.GateContractError) as caught:
                    contract.parse_public_gate_contract(document)
                self.assertEqual(expected_code, caught.exception.code)

    def test_manifest_reader_rejects_ambiguous_unbounded_and_nonregular_inputs(
        self,
    ) -> None:
        valid = b"schema_version: 1\nfiles: []\n"
        cases = (
            b"schema_version: 0\n" + valid,
            b"files: [{path: one, path: two}]\n",
            b"files: &a []\nother: *a\n",
            b"files: []\nother: " + b"[" * 65 + b"]" * 65,
            valid + b"#" * contract.MAX_MANIFEST_BYTES,
            valid + b"\xff",
        )
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            path = root / "manifest.yaml"
            for raw in cases:
                with self.subTest(raw=raw[:40]):
                    path.write_bytes(raw)
                    with self.assertRaises(contract.ManifestContractError):
                        contract.load_manifest_document(path)

            path.unlink()
            target = root / "source.yaml"
            target.write_bytes(valid)
            path.symlink_to(target)
            with self.subTest(boundary="file-symlink"):
                with self.assertRaises(contract.ManifestContractError):
                    contract.load_manifest_document(path)
            path.unlink()
            path.mkdir()
            with self.subTest(boundary="directory"):
                with self.assertRaises(contract.ManifestContractError):
                    contract.load_manifest_document(path)

    def test_manifest_reader_rejects_ancestor_symlink_and_fifo_swap(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            source = root / "source"
            source.mkdir()
            path = source / "manifest.yaml"
            path.write_text("files: []\n", encoding="utf-8")
            alias = root / "alias"
            alias.symlink_to(source, target_is_directory=True)
            with self.subTest(boundary="ancestor-symlink"):
                with self.assertRaises(contract.ManifestContractError):
                    contract.load_manifest_document(alias / "manifest.yaml")

            real_open = os.open
            swapped = False

            def swap_before_open(name, flags, *args, **kwargs):
                nonlocal swapped
                if str(name) == path.name and not swapped:
                    swapped = True
                    path.unlink()
                    os.mkfifo(path)
                    self.assertTrue(flags & os.O_NONBLOCK)
                return real_open(name, flags, *args, **kwargs)

            with mock.patch.object(contract.os, "open", side_effect=swap_before_open):
                with self.assertRaises(contract.ManifestContractError):
                    contract.load_manifest_document(path)


LOCAL_AGGREGATE_CHILDREN = contract._LOCAL_AGGREGATE_CHILDREN


def leaf(gate_id: str, suite_key: str) -> contract.GateNode:
    return contract.GateNode(
        gate_id=gate_id,
        kind=contract.GateKind.LEAF,
        suite_key=suite_key,
        entrypoint=pathlib.PurePosixPath("scripts/validation/check-document-links.py"),
        argv=(),
        cwd=pathlib.PurePosixPath("."),
        allowed_env_keys=(),
        timeout_minutes=10,
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
        opaque=False,
        children=children,
    )


def complete_registry() -> contract.GateRegistry:
    return contract.parse_gate_registry(
        contract.load_contract_document(ROOT),
        ".github/workflow-contract.yml",
    )


def registry(
    *,
    nodes: tuple[contract.GateNode, ...] | None = None,
    public_roots: tuple[str, ...] | None = None,
) -> contract.GateRegistry:
    default = complete_registry()
    return contract.GateRegistry(
        nodes=nodes if nodes is not None else default.nodes,
        public_roots=(
            public_roots if public_roots is not None else default.public_roots
        ),
    )


class CiGateContractTests(unittest.TestCase):
    def assert_codes(
        self,
        findings: tuple[contract.GateFinding, ...],
        *codes: str,
    ) -> None:
        self.assertEqual(set(codes), {finding.code for finding in findings})

    def test_operations_catalog_current_authority_is_an_exact_required_ci_leaf(
        self,
    ) -> None:
        registry = contract.parse_gate_registry(
            contract.load_contract_document(ROOT),
            ".github/workflow-contract.yml",
        )
        nodes = {node.gate_id: node for node in registry.nodes}
        leaf = nodes["leaf.operations-catalog"]
        self.assertEqual(
            pathlib.PurePosixPath("scripts/validation/check-operations-catalog.py"),
            leaf.entrypoint,
        )
        self.assertEqual((), leaf.argv)
        public = contract.parse_public_gate_contract(
            contract.load_contract_document(ROOT)
        )
        operations_roots = next(
            route.root_gate_ids for route in public.suites if route.name == "operations"
        )
        self.assertIn(leaf.gate_id, operations_roots)

    def test_schema_v2_contract_is_strict_json_and_duplicate_safe(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            contract_path = root / ".github/workflow-contract.yml"
            contract_path.parent.mkdir()
            cases = (
                (
                    '{"schema_version":2,"schema_version":2,"gate_nodes":[]}',
                    "ci-gate-json-duplicate-key",
                ),
                (
                    "schema_version: 2\ngate_nodes: []\n",
                    "ci-gate-json-invalid",
                ),
                (
                    '{"schema_version":1,"gate_nodes":[]}',
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
                + "}",
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
                        "opaque": True,
                    }
                    for index in range(2049)
                ],
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
                    "profiles": ["ci"],
                },
                "ci-gate-kind-fields",
            ),
            ({**valid_leaf, "opaque": False}, "ci-gate-kind-fields"),
        )
        for invalid_node, expected_code in invalid_nodes:
            with self.subTest(kind=invalid_node["kind"]):
                document: dict[str, object] = {
                    "schema_version": 2,
                    "gate_nodes": [invalid_node],
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
                        aggregate(
                            node.gate_id,
                            (*node.children, "local.workflow-harness"),
                        )
                        if node.gate_id == "local.workflow-harness"
                        else node
                        for node in candidate.nodes
                    )
                elif mutation == "missing-child":
                    candidate = registry()
                    nodes = tuple(
                        aggregate(node.gate_id, ("leaf.missing",))
                        if node.gate_id == "local.workflow-harness"
                        else node
                        for node in candidate.nodes
                    )
                else:
                    candidate = registry()
                    nodes = (*candidate.nodes, leaf("leaf.orphan", "orphan"))
                findings = contract.validate_gate_registry(
                    ROOT,
                    registry(nodes=nodes),
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
            ("aggregate.deep-0",),
        )
        with self.subTest(boundary="deep-iterative-expansion"):
            self.assertEqual(
                ("leaf.deep",),
                contract.expand_public_gate_ids(
                    deep_registry,
                    ("aggregate.deep-0",),
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
            if node.gate_id == "leaf.operations-catalog"
            else node
            for node in candidate.nodes
        )
        findings = contract.validate_gate_registry(
            ROOT,
            registry(nodes=duplicate_suite_nodes),
        )
        self.assert_codes(findings, "ci-gate-suite-duplicate")

    def test_public_routes_require_setup_before_frontend_consumers(self) -> None:
        candidate = complete_registry()
        cases = (
            (
                "frontend-reversed",
                "ci.frontend-quality",
                lambda children: tuple(reversed(children)),
                "ci-gate-setup-prerequisite",
            ),
            (
                "frontend-missing",
                "ci.frontend-quality",
                lambda children: tuple(
                    child
                    for child in children
                    if child != "setup.frontend-node-dependencies"
                ),
                "ci-gate-active-aggregate-child",
            ),
            (
                "storybook-playwright-before-npm-ci",
                "ci.storybook-coverage",
                lambda children: (
                    "setup.storybook-playwright",
                    "setup.frontend-node-dependencies",
                    "leaf.storybook-coverage",
                ),
                "ci-gate-setup-prerequisite",
            ),
            (
                "storybook-late-playwright",
                "ci.storybook-coverage",
                lambda children: (
                    "setup.frontend-node-dependencies",
                    "leaf.storybook-coverage",
                    "setup.storybook-playwright",
                ),
                "ci-gate-setup-prerequisite",
            ),
        )
        for label, root_gate_id, mutate, expected_code in cases:
            with self.subTest(case=label):
                nodes = tuple(
                    dataclasses.replace(node, children=mutate(node.children))
                    if node.gate_id == root_gate_id
                    else node
                    for node in candidate.nodes
                )
                mutated = dataclasses.replace(candidate, nodes=nodes)
                self.assert_codes(
                    contract.validate_gate_registry(ROOT, mutated),
                    expected_code,
                )
                with self.assertRaises(contract.GateContractError) as caught:
                    contract.expand_public_gate_ids(mutated, (root_gate_id,))
                self.assertEqual(
                    expected_code,
                    caught.exception.code,
                )

    def test_active_aggregates_retain_every_mandatory_child(self) -> None:
        candidate = complete_registry()
        for (
            aggregate,
            required_children,
        ) in contract._REQUIRED_ACTIVE_AGGREGATE_CHILDREN.items():
            for missing_child in required_children:
                with self.subTest(
                    aggregate=aggregate,
                    missing_child=missing_child,
                ):
                    nodes = tuple(
                        dataclasses.replace(
                            node,
                            children=tuple(
                                child
                                for child in node.children
                                if child != missing_child
                            ),
                        )
                        if node.gate_id == aggregate
                        else node
                        for node in candidate.nodes
                    )
                    mutated = dataclasses.replace(candidate, nodes=nodes)
                    self.assert_codes(
                        contract.validate_gate_registry(ROOT, mutated),
                        "ci-gate-active-aggregate-child",
                    )
                    with self.assertRaises(contract.GateContractError) as caught:
                        contract.expand_public_gate_ids(mutated, (aggregate,))
                    self.assertEqual(
                        "ci-gate-active-aggregate-child",
                        caught.exception.code,
                    )
        for missing_root in contract._REQUIRED_ACTIVE_AGGREGATE_CHILDREN:
            with self.subTest(missing_root=missing_root):
                mutated = dataclasses.replace(
                    candidate,
                    nodes=tuple(
                        node for node in candidate.nodes if node.gate_id != missing_root
                    ),
                    public_roots=tuple(
                        root for root in candidate.public_roots if root != missing_root
                    ),
                )
                self.assert_codes(
                    contract.validate_gate_registry(ROOT, mutated),
                    "ci-gate-active-aggregate-root",
                )

    def test_public_roots_are_the_only_graph_reachability_authority(self) -> None:
        candidate = complete_registry()
        reachable = contract._expanded_all_ids(
            {node.gate_id: node for node in candidate.nodes},
            candidate.public_roots,
        )
        self.assertEqual(
            {node.gate_id for node in candidate.nodes},
            set(reachable),
        )
        self.assertEqual((), contract.validate_gate_registry(ROOT, candidate))
        for roots in (
            (),
            (candidate.public_roots[0], candidate.public_roots[0]),
            ("leaf.docs-traceability",),
        ):
            with self.subTest(boundary="public-root-admission", roots=roots):
                with self.assertRaises(contract.GateContractError) as caught:
                    contract.expand_public_gate_ids(candidate, roots)
                self.assertEqual("ci-gate-public-roots", caught.exception.code)

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
            self.assertTrue(observed)
            for arguments, kwargs in observed:
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
                    {"GIT_DIR", "GIT_INDEX_FILE"} & set(environment),
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

    def test_retired_profile_grammar_is_rejected_and_local_children_are_exact(
        self,
    ) -> None:
        live = contract.load_contract_document(ROOT)
        self.assertNotIn("profile_roots", live)
        self.assertTrue(all("profiles" not in node for node in live["gate_nodes"]))
        retired_root = json.loads(json.dumps(live))
        retired_root["profile_roots"] = []
        with self.subTest(boundary="retired-profile-roots"):
            with self.assertRaises(contract.GateContractError) as caught:
                contract.parse_gate_registry(
                    retired_root,
                    ".github/workflow-contract.yml",
                )
            self.assertEqual("ci-gate-document-fields", caught.exception.code)

        retired_node = json.loads(json.dumps(live))
        retired_node["gate_nodes"][0]["profiles"] = ["ci"]
        with self.subTest(boundary="retired-node-profiles"):
            with self.assertRaises(contract.GateContractError) as caught:
                contract.parse_gate_registry(
                    retired_node,
                    ".github/workflow-contract.yml",
                )
            self.assertEqual("ci-gate-kind-fields", caught.exception.code)

        candidate = complete_registry()
        wrong_local_children = tuple(
            dataclasses.replace(
                node,
                children=tuple(reversed(node.children)),
            )
            if node.gate_id == "local.workflow-harness"
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
                        with self.assertRaises(contract.GateContractError) as caught:
                            contract.load_contract_document(real_root)
                    self.assertEqual(expected_code, caught.exception.code)
                    self.assertNotIn("sensitive", str(caught.exception))

            with self.subTest(boundary="read-error"):
                with mock.patch.object(
                    contract.os,
                    "read",
                    side_effect=OSError(errno.EIO, "sensitive"),
                ):
                    with self.assertRaises(contract.GateContractError) as caught:
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
                "GITHUB_ACTIONS",
                "HEAD_REF",
                "PR_TITLE",
                "TEMPLATE_GATE_BASE",
            },
            {key for node in registry.nodes for key in node.allowed_env_keys},
        )
        # The allowlist admits no key that no node declares.
        self.assertEqual(
            contract._ADMITTED_ENV_KEYS,
            frozenset(key for node in registry.nodes for key in node.allowed_env_keys),
        )


if __name__ == "__main__":
    unittest.main()
