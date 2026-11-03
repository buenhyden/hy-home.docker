"""P02 Prometheus consumer contracts for configurable provider listeners."""

from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
START = ROOT / "infra/06-observability/prometheus/scripts/start.sh"


class PrometheusKeycloakTargetContractTests(unittest.TestCase):
    def _run(
        self, target_dir: Path, port: str, path: str | None = None
    ) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        environment.update(
            {
                "KEYCLOAK_MANAGEMENT_PORT": port,
                "OPENBAO_PORT": "8200",
                "PROMETHEUS_BIN": "/bin/true",
                "PROMETHEUS_DEV_DATA_EXPECTED": "on",
                "PROMETHEUS_TARGETS_DIR": str(target_dir),
            }
        )
        if path is not None:
            environment["PATH"] = path
        return subprocess.run(
            ["sh", str(START)],
            cwd=ROOT,
            env=environment,
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )

    def test_default_and_nondefault_ports_render_exact_keycloak_target(self) -> None:
        for port in ("9000", "19000"):
            with self.subTest(port=port), tempfile.TemporaryDirectory() as directory:
                target_dir = Path(directory) / "targets"
                result = self._run(target_dir, port)
                self.assertEqual(0, result.returncode, result.stderr)
                keycloak = (target_dir / "keycloak.yml").read_text(encoding="utf-8")
                self.assertIn(f"keycloak:{port}", keycloak)

    def test_invalid_port_is_rejected_before_any_target_output(self) -> None:
        for port in ("", "0", "65536", "12x", "9000;touch /tmp/no"):
            with self.subTest(port=port), tempfile.TemporaryDirectory() as directory:
                target_dir = Path(directory) / "targets"
                result = self._run(target_dir, port)
                self.assertEqual(64, result.returncode)
                self.assertFalse(target_dir.exists())

    def test_failed_keycloak_rename_preserves_previous_target(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            target_dir = temporary / "targets"
            target_dir.mkdir(mode=0o700)
            keycloak = target_dir / "keycloak.yml"
            keycloak.write_text("previous-safe-target\n", encoding="ascii")
            tools = temporary / "bin"
            tools.mkdir(mode=0o700)
            move = tools / "mv"
            move.write_text(
                "#!/bin/sh\n"
                'case "$3" in */keycloak.yml) exit 75 ;; esac\n'
                'exec /bin/mv "$@"\n',
                encoding="ascii",
            )
            move.chmod(0o700)
            result = self._run(target_dir, "19000", f"{tools}:/usr/bin:/bin")
            self.assertNotEqual(0, result.returncode)
            self.assertEqual("previous-safe-target\n", keycloak.read_text())
            self.assertEqual([], list(target_dir.glob(".keycloak.*")))


if __name__ == "__main__":
    unittest.main()
