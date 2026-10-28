"""SPEC-0243 window gates, scoped override and hourly logrotate contracts."""

import hashlib
import json
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
DROP_IN = ROOT / "infra/03-security/openbao/config/systemd/logrotate-hourly.conf"
# service: (overlay, base Compose file, CA mount target)
BASE = {
    "traefik": (
        "infra/01-gateway/traefik/compose.window-ca.override.yml",
        "infra/01-gateway/traefik/docker-compose.yml",
        "/openbao-ca/ca.pem",
    ),
}
# Prometheus runs the Compose pin with the CA mount since 2026-10-20; a rollback
# overlay to the older image would downgrade TSDB data written by the newer one.
PROMETHEUS_COMPOSE = "infra/06-observability/docker-compose.yml"
PROMETHEUS_OVERLAY = "infra/06-observability/compose.window-ca.override.yml"
PINNED = re.compile(r"[a-z0-9./-]+:v[0-9.]+@sha256:[a-f0-9]{64}")


class WindowOverrideTests(unittest.TestCase):
    def test_each_overlay_changes_only_its_service_image(self):
        for name, (overlay, compose, target) in BASE.items():
            with self.subTest(service=name):
                model = yaml.safe_load((ROOT / overlay).read_text())
                self.assertEqual(set(model), {"x-hyhome-overlay", "services"})
                self.assertEqual(
                    model["x-hyhome-overlay"], {"version": 1, "base": compose}
                )
                self.assertEqual(set(model["services"]), {name})
                override = model["services"][name]
                self.assertEqual(set(override), {"image"})
                self.assertRegex(override["image"], PINNED)
                base = yaml.safe_load((ROOT / compose).read_text())["services"][name]
                # The pin keeps the running image, which differs from Compose's.
                self.assertNotEqual(override["image"], base["image"])
                self.assertEqual(
                    override["image"].split(":")[0], base["image"].split(":")[0]
                )
                # Recreating deploys the CA mount the base already declares.
                self.assertIn(
                    target,
                    [v.get("target") for v in base["volumes"] if isinstance(v, dict)],
                )

    def test_prometheus_has_no_downgrade_overlay_and_declares_the_ca_mount(self):
        self.assertFalse((ROOT / PROMETHEUS_OVERLAY).exists())
        base = yaml.safe_load((ROOT / PROMETHEUS_COMPOSE).read_text())["services"][
            "prometheus"
        ]
        self.assertIn(
            "/etc/prometheus/openbao-ca.pem",
            [v.get("target") for v in base["volumes"] if isinstance(v, dict)],
        )

    def test_drop_in_only_reschedules_the_shared_logrotate_timer(self):
        lines = [
            line
            for line in DROP_IN.read_text().splitlines()
            if line and not line.startswith("#")
        ]
        self.assertEqual(
            lines, ["[Timer]", "OnCalendar=", "OnCalendar=hourly", "AccuracySec=5m"]
        )

    def test_runbook_source_manifest_pins_match_the_files(self):
        # A stale pin would stop the window at W1's sha256sum check.
        runbook = (
            ROOT
            / "docs/05.operations/runbooks/04-security-and-secrets/0105-openbao-maintenance-window.md"
        ).read_text()
        body = runbook.split("<<'P01_SOURCE_MANIFEST'\n", 1)[1].split(
            "\nP01_SOURCE_MANIFEST\n", 1
        )[0]
        pins = [line.split(" ", 1) for line in body.splitlines()]
        self.assertGreaterEqual(len(pins), 10)
        for digest, path in pins:
            with self.subTest(path=path):
                raw = (ROOT / path).read_bytes()
                self.assertEqual(hashlib.sha256(raw).hexdigest(), digest)


class WindowEsoGateTests(unittest.TestCase):
    """Execute RUN-0085's actual gate against public synthetic API replies."""

    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        script = (ROOT / "infra/03-security/openbao/scripts/k8s-writers.sh").read_text()
        self.function = (
            "p01_eso_gate() {\n"
            + script.split("p01_eso_gate() {\n", 1)[1].split("\n# end p01_eso_gate", 1)[
                0
            ]
        )
        self.expected = [
            {
                "namespace": "fixture",
                "name": f"consumer-{index}",
                "store": {"kind": "ClusterSecretStore", "name": "vault-backend"},
            }
            for index in range(6)
        ]
        self.items = [
            {
                "metadata": {"namespace": item["namespace"], "name": item["name"]},
                "spec": {"secretStoreRef": item["store"]},
                "status": {
                    "refreshTime": "2023-11-14T22:13:21Z",
                    "conditions": [
                        {"type": "Ready", "status": "True", "reason": "SecretSynced"}
                    ],
                },
            }
            for item in self.expected
        ]
        self.store = {"status": {"conditions": [{"type": "Ready", "status": "True"}]}}
        self.apps = [
            {"status": {"sync": {"status": "Synced"}, "health": {"status": "Healthy"}}}
            for _ in range(3)
        ]
        stub = self.root / "kubectl"
        stub.write_text(
            '#!/bin/bash\nprintf "%s\\n" "$*" >>"$FIXTURE/calls"\n'
            '[[ "$1 $2 $3" == "--context k3d-hyhome --request-timeout=5s" ]] || exit 97\n'
            'shift 3\ncase "$*" in\n'
            '"get clustersecretstore vault-backend -o json") part=store ;;\n'
            '"get externalsecrets -A -o json") part=actual ;;\n'
            '"-n argocd get applications root-platform platform-cluster-config platform-external-secrets-operator -o json") part=apps ;;\n'
            "*) exit 97 ;;\nesac\n"
            '[[ "$part" != "$FAIL_API" ]] || exit 42\ncat "$FIXTURE/$part.json"\n'
        )
        stub.chmod(0o700)

    def gate(self, *, items=None, store=None, apps=None, fail_api=""):
        for name, document in {
            "expected": self.expected,
            "actual": {"items": self.items if items is None else items},
            "store": self.store if store is None else store,
            "apps": {"items": self.apps if apps is None else apps},
        }.items():
            (self.root / f"{name}.json").write_text(json.dumps(document))
        calls = self.root / "calls"
        calls.unlink(missing_ok=True)
        result = subprocess.run(
            ["bash", "-c", self.function + "\np01_eso_gate"],
            env={
                "PATH": str(self.root) + ":/usr/bin:/bin",
                "FIXTURE": str(self.root),
                "FAIL_API": fail_api,
                "P01_EXPECTED_ES": str(self.root / "expected.json"),
                "P01_FINISH_EPOCH": "1700000000",
            },
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        for call in calls.read_text().splitlines():
            self.assertTrue(
                call.startswith("--context k3d-hyhome --request-timeout=5s ")
            )
        return result.returncode

    def test_exact_fresh_synced_set_accepts(self):
        self.assertEqual(self.gate(items=list(reversed(self.items))), 0)
        fractional = {
            **self.items[0],
            "status": {
                **self.items[0]["status"],
                "refreshTime": "2023-11-14T22:13:21.123Z",
            },
        }
        self.assertEqual(self.gate(items=[fractional, *self.items[1:]]), 0)

    def test_stale_wrong_missing_extra_or_unready_target_refuses(self):
        first = self.items[0]
        for bad in (
            {
                **first,
                "status": {**first["status"], "refreshTime": "2023-11-14T22:13:19Z"},
            },
            {
                **first,
                "status": {**first["status"], "refreshTime": "2023-11-14T22:13:20Z"},
            },
            {**first, "status": {**first["status"], "refreshTime": "invalid"}},
            {**first, "metadata": {**first["metadata"], "name": "wrong"}},
            {
                **first,
                "spec": {
                    "secretStoreRef": {"kind": "ClusterSecretStore", "name": "wrong"}
                },
            },
            {
                **first,
                "status": {
                    **first["status"],
                    "conditions": [{"type": "Ready", "status": "False"}],
                },
            },
        ):
            with self.subTest(bad=bad):
                self.assertEqual(self.gate(items=[bad, *self.items[1:]]), 1)
        self.assertEqual(self.gate(items=self.items[1:]), 1)
        self.assertEqual(self.gate(items=[*self.items, first]), 1)

    def test_store_or_application_failure_refuses(self):
        self.assertEqual(
            self.gate(
                store={"status": {"conditions": [{"type": "Ready", "status": "False"}]}}
            ),
            1,
        )
        for sync, health in (("OutOfSync", "Healthy"), ("Synced", "Degraded")):
            bad = {"status": {"sync": {"status": sync}, "health": {"status": health}}}
            self.assertEqual(self.gate(apps=[*self.apps[:2], bad]), 1)

    def test_api_failure_aborts_with_distinct_exit(self):
        for stage in ("store", "actual", "apps"):
            with self.subTest(stage=stage):
                self.assertEqual(self.gate(fail_api=stage), 2)


class WindowWriterRestoreTests(unittest.TestCase):
    """Only saved changed writers may be restored, in reverse stop order."""

    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        script = (ROOT / "infra/03-security/openbao/scripts/k8s-writers.sh").read_text()
        start = script.index("p01_ns=(")
        self.function = script[start : script.index("p01_writers_zero() {", start)]
        for index in range(3):
            (self.root / f"{index}.json").write_text(
                json.dumps({"uid": f"uid-{index}", "desired": index + 1})
            )
        stub = self.root / "kubectl"
        stub.write_text("""#!/usr/bin/python3
import json, os, pathlib, sys
root = pathlib.Path(os.environ["P01_K8S_STATE"])
args = sys.argv[1:]
with (root / "calls").open("a") as stream:
    stream.write(json.dumps(args) + "\\n")
if args[:3] != ["--context", "k3d-hyhome", "--request-timeout=15s"] or args[3] != "-n":
    sys.exit(97)
command = args[5:]
resource = command[2] if command[0] == "rollout" else command[1]
resources = ["statefulset/argocd-application-controller", "deployment/argocd-applicationset-controller", "deployment/external-secrets"]
index = resources.index(resource)
if args[4] != ["argocd", "argocd", "external-secrets"][index]:
    sys.exit(97)
saved = json.loads((root / f"{index}.json").read_text())
if command[0] == "get":
    if command[-1].startswith("jsonpath="):
        print("changed-uid" if os.environ.get("WRONG_UID") == str(index) else saved["uid"])
    else:
        n = saved["desired"]
        print(json.dumps({"metadata": {"uid": saved["uid"]}, "spec": {"replicas": n}, "status": {"replicas": n, "readyReplicas": n}}))
elif command[0] == "scale":
    if command[-1] != "--replicas=" + str(saved["desired"]):
        sys.exit(97)
    if os.environ.get("FAIL_SCALE") == str(index):
        sys.exit(42)
elif command != ["rollout", "status", resource, "--timeout=90s"]:
    sys.exit(97)
""")
        stub.chmod(0o700)

    def restore(self, changed, **failures):
        calls = self.root / "calls"
        calls.unlink(missing_ok=True)
        result = subprocess.run(
            [
                "bash",
                "-o",
                "pipefail",
                "-c",
                self.function + f"\np01_changed=({changed})\np01_restore_writers",
            ],
            env={
                "PATH": str(self.root) + ":/usr/bin:/bin",
                "P01_K8S_STATE": str(self.root),
                **failures,
            },
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        history = [json.loads(line) for line in calls.read_text().splitlines()]
        for call in history:
            self.assertEqual(
                call[:3], ["--context", "k3d-hyhome", "--request-timeout=15s"]
            )
        return result.returncode, [call[6] for call in history if call[5] == "scale"]

    def test_changed_writers_restore_in_reverse_order(self):
        self.assertEqual(
            self.restore("0 1 2"),
            (
                0,
                [
                    "deployment/external-secrets",
                    "deployment/argocd-applicationset-controller",
                    "statefulset/argocd-application-controller",
                ],
            ),
        )
        self.assertEqual(
            self.restore("0 1"),
            (
                0,
                [
                    "deployment/argocd-applicationset-controller",
                    "statefulset/argocd-application-controller",
                ],
            ),
        )

    def test_uid_mismatch_refuses_that_writer_and_restores_others(self):
        self.assertEqual(
            self.restore("0 1 2", WRONG_UID="2"),
            (
                1,
                [
                    "deployment/argocd-applicationset-controller",
                    "statefulset/argocd-application-controller",
                ],
            ),
        )

    def test_scale_failure_is_reported_after_restoring_others(self):
        code, scales = self.restore("0 1 2", FAIL_SCALE="2")
        self.assertEqual(code, 1)
        self.assertEqual(len(scales), 3)

    def test_original_zero_replicas_are_restored_as_zero(self):
        (self.root / "2.json").write_text(json.dumps({"uid": "uid-2", "desired": 0}))
        self.assertEqual(self.restore("2"), (0, ["deployment/external-secrets"]))


if __name__ == "__main__":
    unittest.main()
