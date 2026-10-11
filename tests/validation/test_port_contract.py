"""Schema and CLI boundaries using explicitly selected synthetic inputs."""

import contextlib
import hashlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

from jsonschema import Draft202012Validator

from scripts.lib.ops.port_inventory import PortContractError, project, render_synthetic

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "tests/fixtures/port-contract"
CLI = ROOT / "scripts/operations/port-inventory.py"
SCHEMA = ROOT / "infra/09-platform-ops/service-integration/port-contract.schema.json"


class PortSchemaTests(unittest.TestCase):
    def test_complex_endpoint_uniqueness_uses_semantic_linear_sets(self):
        from scripts.lib.ops.port_inventory import validate_contract

        schema = json.loads(SCHEMA.read_text())
        endpoints = schema["properties"]["services"]["items"]["properties"][
            "internal_dns"
        ]["properties"]["endpoints"]
        self.assertNotIn("uniqueItems", endpoints)
        doc = project({"services": {"dev": {"expose": [80]}}})
        doc["services"][0]["internal_dns"]["endpoints"].append(
            deepcopy(doc["services"][0]["internal_dns"]["endpoints"][0])
        )
        with self.assertRaises(PortContractError):
            validate_contract(doc, schema)

    def test_semantic_admission_rejects_contradictory_location_states(self):
        from scripts.lib.ops.port_inventory import validate_contract

        schema = json.loads(SCHEMA.read_text())
        for location, state in [
            ("internal_dns", "absent"),
            ("traefik_backend", "declared"),
        ]:
            bad = project({"services": {"dev": {"ports": ["9000:80"]}}})
            bad["services"][0][location]["state"] = state
            with self.assertRaises(PortContractError):
                validate_contract(bad, schema)

    def test_schema_rejects_source_path_escape(self):
        document = project({"services": {"dev": {}}})
        document["source"] = [
            {"path": "tests/../../secrets/private.env", "sha256": "a" * 64}
        ]
        self.assertTrue(
            list(
                Draft202012Validator(json.loads(SCHEMA.read_text())).iter_errors(
                    document
                )
            )
        )

    def test_semantic_admission_is_pure_and_rejects_duplicates_and_inconsistent_endpoints(
        self,
    ):
        from scripts.lib.ops.port_inventory import validate_contract

        schema = json.loads(SCHEMA.read_text())
        good = project({"services": {"dev": {"ports": ["9000:80"]}}})
        original = deepcopy(good)
        with (
            patch("builtins.open", side_effect=AssertionError),
            patch("socket.socket", side_effect=AssertionError),
        ):
            self.assertIsNone(validate_contract(good, schema))
        self.assertEqual(good, original)
        duplicate = deepcopy(good)
        duplicate["services"].append(deepcopy(duplicate["services"][0]))
        duplicate["services"][1]["host_publication"]["endpoints"][0]["published"][
            "start"
        ] = 9001
        bad_range = deepcopy(good)
        bad_range["services"][0]["host_publication"]["endpoints"][0]["target"][
            "end"
        ] = 79
        bad_ip = deepcopy(good)
        bad_ip["services"][0]["host_publication"]["endpoints"][0]["host_ip"] = (
            "999.1.2.3"
        )
        bad_allocation = deepcopy(good)
        bad_allocation["services"][0]["host_publication"]["endpoints"][0][
            "allocation"
        ] = "automatic"
        for bad in [duplicate, bad_range, bad_ip, bad_allocation]:
            with self.assertRaises(PortContractError):
                validate_contract(bad, schema)
        external = deepcopy(schema)
        external["$ref"] = "https://example.invalid/schema"
        with patch("socket.socket", side_effect=AssertionError):
            with self.assertRaises(PortContractError):
                validate_contract(good, external)

    def test_valid_fixture_and_real_projection_follow_closed_schema(self):
        schema = json.loads(SCHEMA.read_text())
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)
        self.assertEqual(
            list(
                validator.iter_errors(json.loads((FIXTURES / "valid.json").read_text()))
            ),
            [],
        )
        self.assertEqual(
            list(
                validator.iter_errors(
                    project({"services": {"dev": {"ports": ["[::1]:9000:80/udp"]}}})
                )
            ),
            [],
        )

    def test_invalid_and_sensitive_fields_are_rejected(self):
        validator = Draft202012Validator(json.loads(SCHEMA.read_text()))
        self.assertTrue(
            list(
                validator.iter_errors(
                    json.loads((FIXTURES / "invalid.json").read_text())
                )
            )
        )
        doc = project({"services": {"dev": {}}})
        doc["services"][0]["credential"] = "SYNTHETIC_LEAK_MARKER"
        self.assertTrue(list(validator.iter_errors(doc)))


class SyntheticRenderTests(unittest.TestCase):
    def test_config_process_caps_both_pipes_during_collection(self):
        from scripts.lib.ops.port_inventory import _run_config

        for descriptor in (1, 2):
            with self.assertRaises(PortContractError):
                _run_config(
                    [
                        sys.executable,
                        "-c",
                        f"import os; os.write({descriptor}, b'x' * 2097152)",
                    ],
                    env={"PATH": "/usr/bin:/bin"},
                    cwd=ROOT,
                )

    def test_environment_is_closed_and_raw_stdout_stderr_never_escapes(self):
        payload = {
            "services": {
                "dev": {
                    "environment": {"PASSWORD": "SYNTHETIC_LEAK_MARKER"},
                    "labels": {"private": "SYNTHETIC_LEAK_MARKER"},
                    "ports": [{"target": 80, "published": "9000"}],
                }
            }
        }
        observed = []

        def fake_run(argv, **kwargs):
            observed.append((argv, kwargs))
            return subprocess.CompletedProcess(
                argv, 0, json.dumps(payload).encode(), b"SYNTHETIC_LEAK_MARKER"
            )

        with (
            patch.dict(
                os.environ,
                {
                    "COMPOSE_FILE": "/private/.env",
                    "HOME": "/private",
                    "PUBLIC_PORT": "19000",
                    "DOCKER_CONTEXT": "production",
                },
            ),
            patch("scripts.lib.ops.port_inventory._run_config", side_effect=fake_run),
        ):
            output = render_synthetic(
                [
                    b'services:\n  dev:\n    image: example.invalid/synthetic:1\n    ports: ["${PUBLIC_PORT}:80"]\n'
                ],
                {"PUBLIC_PORT": "9000"},
            )
        self.assertNotIn("SYNTHETIC_LEAK_MARKER", json.dumps(output))
        env = observed[0][1]["env"]
        self.assertNotIn("COMPOSE_FILE", env)
        self.assertNotIn("DOCKER_CONTEXT", env)
        self.assertNotIn("PUBLIC_PORT", env)
        self.assertEqual(env["COMPOSE_DISABLE_ENV_FILE"], "1")
        self.assertNotIn("/private", env["HOME"])
        self.assertIn("--env-file", observed[0][0])
        self.assertIn("config", observed[0][0])

    def test_reject_file_inputs_and_ambient_or_external_edges_before_docker(self):
        for body in [
            b"include: [../../.env]\n",
            b"services:\n  dev:\n    env_file: .env\n",
            b"services:\n  dev:\n    volumes: [secret:/data]\n",
            b"services:\n  dev:\n    build: /private\n",
            b"services:\n  dev: {}\n  dev: {}\n",
            b"services:\n  dev:\n    extends: other.yml\n",
        ]:
            with patch(
                "scripts.lib.ops.port_inventory._run_config",
                side_effect=AssertionError("must not run"),
            ):
                with self.assertRaises(PortContractError):
                    render_synthetic([body], {})

    def test_failure_timeout_and_oversize_are_fixed_errors(self):
        body = b"services:\n  dev: {}\n"
        for failure in [
            subprocess.CompletedProcess(
                [], 1, b"SYNTHETIC_LEAK_MARKER", b"SYNTHETIC_LEAK_MARKER"
            ),
            subprocess.TimeoutExpired([], 30, output=b"SYNTHETIC_LEAK_MARKER"),
            subprocess.CompletedProcess([], 0, b"x" * (1024 * 1024 + 1), b""),
        ]:
            with patch(
                "scripts.lib.ops.port_inventory._run_config",
                side_effect=failure if isinstance(failure, Exception) else None,
                return_value=failure,
            ):
                with self.assertRaises(PortContractError) as caught:
                    render_synthetic([body], {})
                self.assertNotIn("SYNTHETIC_LEAK_MARKER", str(caught.exception))

    def test_native_compose_config_dev_change_does_not_mutate_mng(self):
        # Compose config only: no container, daemon mutation, image pull or private file.
        base = (FIXTURES / "root.yml").read_bytes()
        first = render_synthetic([base], {"DEV_PORT": "15432", "MNG_PORT": "25432"})
        second = render_synthetic(
            [base, (FIXTURES / "dev-override.yml").read_bytes()],
            {"DEV_PORT": "15432", "MNG_PORT": "25432"},
        )
        first, second = [
            {r["service"]: r for r in doc["services"]} for doc in (first, second)
        ]
        self.assertEqual(first["mng-db"], second["mng-db"])
        self.assertNotEqual(
            first["dev-db"]["host_publication"], second["dev-db"]["host_publication"]
        )
        self.assertEqual(
            first["dev-db"]["internal_dns"], second["dev-db"]["internal_dns"]
        )
        self.assertEqual(
            first["dev-db"]["traefik_backend"], second["dev-db"]["traefik_backend"]
        )


class PortCliTests(unittest.TestCase):
    def test_duplicate_and_excess_inputs_fail_before_any_read_or_render(self):
        spec = importlib.util.spec_from_file_location("port_cli", CLI)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        root = "tests/fixtures/port-contract/root.yml"
        for overrides in [
            [root],
            ["tests//fixtures/port-contract/root.yml"],
            [f"tests/fixtures/port-contract/input{i}.yml" for i in range(8)],
        ]:
            args = [
                "--synthetic-root",
                root,
                "--synthetic-env",
                "tests/fixtures/port-contract/env.json",
            ]
            for override in overrides:
                args.extend(["--override", override])
            with (
                patch.object(
                    module, "_read", side_effect=AssertionError("must not read")
                ),
                contextlib.redirect_stderr(io.StringIO()),
            ):
                self.assertEqual(module.main(args), 2)

    def test_bounded_reader_rejects_symlink_and_oversize_without_target_output(self):
        spec = importlib.util.spec_from_file_location("port_cli", CLI)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            fixture = root / "tests/fixtures/port-contract"
            fixture.mkdir(parents=True)
            target = root / "synthetic-private.txt"
            target.write_text("SYNTHETIC_LEAK_MARKER")
            (fixture / "link.yml").symlink_to(target)
            (fixture / "oversize.yml").write_bytes(b"x" * 65537)
            with patch.object(module, "ROOT", root):
                for name in ["link.yml", "oversize.yml"]:
                    with self.assertRaises(ValueError) as caught:
                        module._read("tests/fixtures/port-contract/" + name)
                    self.assertNotIn("SYNTHETIC_LEAK_MARKER", str(caught.exception))

    def test_source_root_matches_existing_closure_without_rendering(self):
        from scripts.lib.ops.port_inventory import project_root
        from scripts.lib.supply_chain.latest_version_gate import expected_from_root

        names, evidence = expected_from_root(ROOT)
        with patch("subprocess.run", side_effect=AssertionError("no render")):
            result = project_root(ROOT)
        self.assertEqual(sorted(r["service"] for r in result["services"]), names)
        self.assertEqual(
            result["source"],
            sorted(
                evidence["input_files"], key=lambda r: json.dumps(r, sort_keys=True)
            ),
        )

    def test_cli_synthetic_is_filtered_and_input_hash_bound(self):
        result = subprocess.run(
            [
                sys.executable,
                str(CLI),
                "--synthetic-root",
                "tests/fixtures/port-contract/root.yml",
                "--synthetic-env",
                "tests/fixtures/port-contract/env.json",
            ],
            cwd=ROOT,
            capture_output=True,
            check=False,
            timeout=40,
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        self.assertNotIn(b"SYNTHETIC_LEAK_MARKER", result.stdout + result.stderr)
        document = json.loads(result.stdout)
        self.assertEqual(document["mode"], "synthetic-render")
        self.assertIn(
            {
                "path": "tests/fixtures/port-contract/env.json",
                "sha256": hashlib.sha256(
                    (FIXTURES / "env.json").read_bytes()
                ).hexdigest(),
            },
            document["source"],
        )

    def test_cli_cannot_select_private_env_or_symlink_or_nonfixture(self):
        for args in [
            ["--synthetic-root", ".env", "--synthetic-env", ".env"],
            ["--override", "../../.env"],
            [
                "--synthetic-root",
                "infra/a.yml",
                "--synthetic-env",
                "tests/fixtures/port-contract/env.json",
            ],
        ]:
            result = subprocess.run(
                [sys.executable, str(CLI), *args],
                cwd=ROOT,
                capture_output=True,
                check=False,
                timeout=10,
            )
            self.assertEqual(result.returncode, 2)
            self.assertNotIn(b"Traceback", result.stderr)
            self.assertNotIn(b"SYNTHETIC_LEAK_MARKER", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
