"""SPEC-0263 standard LAB layout against the real LABs (W2)."""

from __future__ import annotations

import functools
import importlib.util
import os
import pathlib
import shutil
import subprocess
import tempfile
import unittest
from unittest import mock

ROOT = pathlib.Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "lab_controller_layout", ROOT / "scripts/operations/lab.py"
)
lab = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(lab)

LABS = (
    "cassandra",
    "couchdb",
    "dbt",
    "jupyterlab",
    "kafka-cluster",
    "lakehouse",
    "locust",
    "mongodb",
    "opensearch-cluster",
    "postgresql-ha",
    "sonarqube",
    "stalwart",
    "supabase",
    "superset",
    "valkey-cluster",
)
ENV_FILE = ROOT / "labs/.env.example"
# Synthetic operator inputs: only enough to render each LAB. LAB_DATA_DIR is a
# temporary absolute path; LAB_SECRET_DIR keeps its .env.example value.
OPERATOR_INPUTS = {
    "LAB_KAFKA_CLUSTER_ID": "synthetic-lab-cluster",
    "LAB_LOCUST_SCENARIO_DIR": "/nonexistent/locust-scenario",
    "LAB_LOCUST_RESULT_DIR": "/nonexistent/locust-results",
    "LAB_OPENSEARCH_CERT_DIR": "/nonexistent/opensearch-certs",
    "LAB_LAKEHOUSE_S3_ENDPOINT": "http://lab-endpoint.invalid:8333",
    "LAB_LAKEHOUSE_CATALOG_URI": "http://lab-endpoint.invalid:8181",
    "LAB_DBT_DB_HOST": "lab-endpoint.invalid",
    "LAB_SUPERSET_DB_HOST": "lab-endpoint.invalid",
    "LAB_SUPERSET_DEFAULT_URL": "lab.invalid",
    "LAB_SUPERSET_CA_FILE": "/nonexistent/lab-ca/rootCA.pem",
    "LAB_SONARQUBE_DB_HOST": "lab-endpoint.invalid",
    "LAB_STALWART_DEFAULT_URL": "lab.invalid",
}
DATA_DIR = tempfile.mkdtemp(prefix="lab-layout-data-")


def tearDownModule() -> None:
    shutil.rmtree(DATA_DIR, ignore_errors=True)


def env() -> dict[str, str]:
    return {**OPERATOR_INPUTS, "LAB_DATA_DIR": DATA_DIR}


@functools.cache
def rendered(name: str) -> dict:
    with mock.patch.dict(os.environ, env()):
        return lab.render("docker", ENV_FILE, f"labs/{name}/docker-compose.yml")


@functools.cache
def tracked() -> frozenset[str]:
    listed = subprocess.run(
        ["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True
    ).stdout.decode()
    return frozenset(str(ROOT / item) for item in listed.split("\0") if item)


def is_tracked(path: str) -> bool:
    """A tracked file, or a folder holding tracked files."""
    return path in tracked() or any(
        item.startswith(path + os.sep) for item in tracked()
    )


def needs_docker(test):
    return unittest.skipUnless(shutil.which("docker"), "docker is not installed")(test)


class LabLayoutTests(unittest.TestCase):
    def test_labs_root_holds_only_readme_and_env_example(self) -> None:
        for entry in sorted((ROOT / "labs").iterdir()):
            if entry.name == ".env":  # the ignored operator copy
                continue
            with self.subTest(entry=entry.name):
                if entry.name in {"README.md", ".env.example"}:
                    self.assertTrue(entry.is_file())
                else:
                    self.assertTrue(entry.is_dir(), entry)

    def test_every_lab_has_entrypoint_readme_manifest(self) -> None:
        folders = {p.name for p in (ROOT / "labs").iterdir() if p.is_dir()}
        self.assertEqual(set(LABS), folders)
        for name in LABS:
            for item in ("docker-compose.yml", "README.md", "promotion.yaml"):
                with self.subTest(lab=name, item=item):
                    self.assertTrue((ROOT / "labs" / name / item).is_file())


@needs_docker
class LabRenderTests(unittest.TestCase):
    def test_every_manifest_is_valid(self) -> None:
        ids = lab.catalog_ids()
        for name in LABS:
            with self.subTest(lab=name):
                found = lab.footprint(rendered(name))
                self.assertEqual(
                    [], lab.manifest_problems(name, lab.load_manifest(name), found, ids)
                )

    def test_lab_bind_sources_resolve(self) -> None:
        # Review Focus 1: a missed relative path renders to a missing file.
        operator = [
            os.path.realpath(value)
            for key, value in {**lab.read_env(ENV_FILE), **env()}.items()
            if key.startswith("LAB_")
            and key not in {"LAB_DATA_DIR", "LAB_SECRET_DIR"}
            and os.path.isabs(value)
        ]
        data = os.path.realpath(DATA_DIR)
        for name in LABS:
            secrets = os.path.realpath(ROOT / "secrets/labs" / name)
            found = lab.footprint(rendered(name))
            # Secret files are held by test_lab_secret_paths_use_lab_root.
            secret_files = {
                os.path.realpath(item["file"])
                for item in (rendered(name).get("secrets") or {}).values()
            }
            sources = [
                s["real"] for s in found["sources"] if s["real"] not in secret_files
            ]
            for source in [*sources, *found["build_inputs"]]:
                with self.subTest(lab=name, source=source):
                    self.assertTrue(
                        lab._within(source, data)
                        or lab._within(source, secrets)
                        or any(lab._within(source, item) for item in operator)
                        or is_tracked(source),
                        source,
                    )

    def assert_secret_paths(self, names) -> None:
        # Review Focus 2: Compose resolves LAB_SECRET_DIR against labs/<name>/.
        for name in names:
            prefix = str(ROOT / "secrets/labs" / name) + os.sep
            for key, secret in (rendered(name).get("secrets") or {}).items():
                with self.subTest(lab=name, secret=key):
                    self.assertTrue(secret["file"].startswith(prefix), secret["file"])

    def test_lab_secret_paths_use_lab_root(self) -> None:
        self.assert_secret_paths(name for name in LABS if name != "supabase")

    @unittest.expectedFailure  # W3 moves supabase onto secrets/labs/supabase/.
    def test_lab_secret_paths_use_lab_root_supabase(self) -> None:
        self.assert_secret_paths(["supabase"])


if __name__ == "__main__":
    unittest.main()
