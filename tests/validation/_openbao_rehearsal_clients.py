"""Native selected-client and TLS scenarios for the opt-in P01 fixture."""

import http.client
import json
import os
import re
import secrets
import shutil
import time

import yaml

if __package__:
    from ._openbao_rehearsal_fixture import (
        PORT,
        ROOT,
        SOURCE,
        RehearsalFailure,
        captured,
    )
else:
    from _openbao_rehearsal_fixture import (
        PORT,
        ROOT,
        SOURCE,
        RehearsalFailure,
        captured,
    )


class OpenBaoClientCases:
    def temporal_alerts(self, fixture):
        image = (
            "sha256:5ce7540c3c00ef4ab0c9d2c995c6a5b9c421f44b4a115d97a2c7af3b1c21cbb0"
        )
        self.must(
            fixture.docker("image", "inspect", image, "--format", "{{.Id}}")
            .stdout.strip()
            .decode()
            == image,
            "cached promtool image differs",
        )
        rules = (
            ROOT
            / "infra/06-observability/prometheus/config/alert_rules/alert_rules.openbao.yml"
        )
        cases = ROOT / "tests/validation/fixtures/openbao-audit-alerts.test.yml"
        name = fixture.container(
            "promtool",
            [
                "--read-only",
                "--entrypoint",
                "/bin/promtool",
                "--tmpfs",
                "/tmp:size=32m",
                "--mount",
                f"type=bind,src={rules},dst=/rules/alert_rules.openbao.yml,readonly",
                "--mount",
                f"type=bind,src={cases},dst=/p01/openbao-audit-alerts.test.yml,readonly",
                "--workdir",
                "/p01",
            ],
            ["test", "rules", "/p01/openbao-audit-alerts.test.yml"],
            image=image,
            network="none",
        )
        self.must(
            fixture.docker("wait", name).stdout.strip() == b"0",
            "native temporal audit-alert fixture failed",
        )
        print("observed native temporal audit-alert cases: PASS", flush=True)

    def fixture_http(self, fixture, name, port, path):
        target = (
            fixture.docker(
                "inspect",
                "--format",
                '{{(index .NetworkSettings.Networks "'
                + fixture.network
                + '").IPAddress}}',
                name,
            )
            .stdout.decode()
            .strip()
        )
        if not target:
            return 0, b""
        connection = http.client.HTTPConnection(target, port, timeout=3)
        try:
            connection.request("GET", path)
            response = connection.getresponse()
            return response.status, response.read()
        except (OSError, http.client.HTTPException):
            return 0, b""
        finally:
            connection.close()

    def clients(self, fixture):
        images = {
            "prom": "sha256:5ce7540c3c00ef4ab0c9d2c995c6a5b9c421f44b4a115d97a2c7af3b1c21cbb0",
            "traefik": "sha256:f86a2cab1b5c649070c49f883c743dd32d8485a56e3368c5f93b9e91f1e91259",
            "gatus": "sha256:c52ad9511a84a5738eda73155807acd5a2fe3842bd6a33f223fc570d308bba91",
        }
        obs = ROOT / "infra/06-observability"
        uid = str(os.getuid())
        for kind, image in images.items():
            self.must(
                fixture.docker("image", "inspect", image, "--format", "{{.Id}}")
                .stdout.strip()
                .decode()
                == image,
                "selected client cached image differs",
            )
            for trusted in (True, False):
                tag = kind + ("-trusted" if trusted else "-wrong-ca")
                ca = fixture.tls / "ca.pem" if trusted else fixture.wrong_ca
                config = fixture.directory / (tag + ".yaml")
                token_file = fixture.directory / (tag + ".token")
                token_file.write_text(
                    self.metrics_token if kind == "prom" else secrets.token_urlsafe(24)
                )
                token_file.chmod(0o600)
                args = ["--user", uid + ":1000"]
                if kind == "prom":
                    original = yaml.safe_load(
                        (obs / "prometheus/config/prometheus.yml").read_text()
                    )
                    job = next(
                        item
                        for item in original["scrape_configs"]
                        if item["job_name"] == "openbao"
                    )
                    config.write_text(
                        yaml.safe_dump(
                            {
                                "global": {"scrape_interval": "1s"},
                                "scrape_configs": [job],
                            }
                        )
                    )
                    mounts = [
                        (config, "/etc/prometheus/prometheus.yml"),
                        (ca, "/etc/prometheus/openbao-ca.pem"),
                        (token_file, "/run/secrets/openbao_token"),
                        (obs / "prometheus/scripts", "/p01-scripts"),
                    ]
                    args += [
                        "--entrypoint",
                        "/bin/sh",
                        "--env",
                        f"OPENBAO_PORT={PORT}",
                        "--env",
                        "PROMETHEUS_DEV_DATA_EXPECTED=off",
                        "--tmpfs",
                        f"/etc/prometheus/targets:uid={uid},gid=1000,mode=0770",
                        "--tmpfs",
                        f"/prometheus:uid={uid},gid=1000,mode=0770",
                    ]
                    command = [
                        "/p01-scripts/start.sh",
                        "--config.file=/etc/prometheus/prometheus.yml",
                        "--storage.tsdb.path=/prometheus",
                    ]
                    port, endpoint = 9090, "/api/v1/targets"
                elif kind == "traefik":
                    transport = yaml.safe_load(
                        (ROOT / "infra/01-gateway/traefik/dynamic/tls.yaml").read_text()
                    )["http"]["serversTransports"]["openbao-tls"]
                    config.write_text(
                        yaml.safe_dump(
                            {
                                "http": {
                                    "serversTransports": {"openbao-tls": transport},
                                    "routers": {
                                        "fixture": {
                                            "rule": "PathPrefix(`/`)",
                                            "service": "bao",
                                        }
                                    },
                                    "services": {
                                        "bao": {
                                            "loadBalancer": {
                                                "serversTransport": "openbao-tls",
                                                "servers": [
                                                    {"url": f"https://openbao:{PORT}"}
                                                ],
                                            }
                                        }
                                    },
                                }
                            }
                        )
                    )
                    mounts = [(config, "/p01.yaml"), (ca, "/openbao-ca/ca.pem")]
                    command = [
                        "--entryPoints.fixture.address=:8080",
                        "--providers.file.filename=/p01.yaml",
                        "--log.level=ERROR",
                    ]
                    port, endpoint = 8080, "/v1/sys/health"
                else:
                    original = yaml.safe_load(
                        (obs / "gatus/config/config.yaml").read_text()
                    )
                    selected = next(
                        item
                        for item in original["endpoints"]
                        if item["name"] == "OpenBao"
                    )
                    selected = {**selected, "interval": "1s"}
                    config.write_text(
                        yaml.safe_dump({"metrics": True, "endpoints": [selected]})
                    )
                    mounts = [
                        (config, "/p01.yaml"),
                        (ca, "/p01-openbao-ca.pem"),
                        (fixture.wrong_ca, "/p01-root-ca.pem"),
                        (token_file, "/p01-oidc.token"),
                        (obs / "gatus/docker-entrypoint.sh", "/p01-entrypoint.sh"),
                    ]
                    args += [
                        "--entrypoint",
                        "/bin/sh",
                        "--env",
                        "GATUS_CONFIG_PATH=/p01.yaml",
                        "--env",
                        f"OPENBAO_PORT={PORT}",
                        "--env",
                        "GATUS_OPENBAO_CA_PATH=/p01-openbao-ca.pem",
                        "--env",
                        "GATUS_ROOT_CA_FILE=/p01-root-ca.pem",
                        "--env",
                        "DEFAULT_URL=p01.invalid",
                        "--env",
                        "GATUS_OIDC_ALLOWED_SUBJECT=p01-synthetic",
                        "--env",
                        "GATUS_OIDC_CLIENT_SECRET_FILE=/p01-oidc.token",
                        "--env",
                        "PORT=8080",
                    ]
                    command = ["/p01-entrypoint.sh", "/usr/local/bin/gatus"]
                    port, endpoint = 8080, "/metrics"
                config.chmod(0o644)
                for source, destination in mounts:
                    args += [
                        "--mount",
                        f"type=bind,src={source},dst={destination},readonly",
                    ]
                name = fixture.container(tag, args, command, image=image)
                deadline, observed = time.monotonic() + 25, False
                while time.monotonic() < deadline:
                    status, body = self.fixture_http(fixture, name, port, endpoint)
                    if kind == "prom" and status == 200:
                        targets = (
                            json.loads(body).get("data", {}).get("activeTargets", [])
                        )
                        observed = bool(targets) and targets[0].get("health") == (
                            "up" if trusted else "down"
                        )
                        if not trusted and targets:
                            observed &= (
                                "certificate" in targets[0].get("lastError", "").lower()
                            )
                    elif kind == "traefik":
                        observed = status == (200 if trusted else 500)
                    elif kind == "gatus" and status == 200:
                        pattern = (
                            r'gatus_results_total\{[^}]*success="'
                            + str(trusted).lower()
                            + r'"[^}]*\} ([1-9][0-9]*(?:\.[0-9]+)?)'
                        )
                        observed = re.search(pattern, body.decode()) is not None
                    if observed:
                        break
                    time.sleep(0.25)
                fixture.stop(name)
                self.must(
                    observed,
                    "selected " + kind + " client CA acceptance/rejection unobserved",
                )
                print("observed native " + tag + ": PASS", flush=True)

    def expired_certificate(self, fixture):
        directory = fixture.directory / "expired-tls"
        directory.mkdir(mode=0o750)
        for name in ("ca.pem", "server-key.pem"):
            shutil.copy2(fixture.tls / name, directory / name)
        captured(
            [
                "openssl",
                "x509",
                "-req",
                "-in",
                str(fixture.directory / "issuer/server.csr"),
                "-CA",
                str(fixture.tls / "ca.pem"),
                "-CAkey",
                str(fixture.directory / "issuer/ca-key.pem"),
                "-CAcreateserial",
                "-out",
                str(directory / "server.pem"),
                "-days",
                "-1",
                "-extfile",
                str(fixture.directory / "issuer/server.ext"),
            ]
        )
        name, expired = fixture.server("expired", tls=directory, ready=False)
        with self.assertRaisesRegex(RehearsalFailure, "SSLCertVerificationError"):
            expired.api("GET", "sys/health")
        fixture.stop(name)
        preflight = ["sh", str(SOURCE / "scripts/check-tls-material.sh")]
        self.must(
            captured(
                [
                    *preflight,
                    str(fixture.tls),
                    "openbao/openbao:2.7.1@sha256:6d2b93856e3fcf7b18ad855a0b51eaba474dc8b79cf554379ea32034797d2acf",
                ],
                allow_failure=True,
            ).returncode
            == 0,
            "native TLS material preflight rejected valid fixture",
        )
        invalid_dirs = [directory]
        for kind in ("wrong-ca", "wrong-san", "missing-loopback-san", "wrong-key"):
            invalid = fixture.directory / (kind + "-tls")
            shutil.copytree(fixture.tls, invalid)
            if kind == "wrong-ca":
                shutil.copy2(fixture.wrong_ca, invalid / "ca.pem")
            elif kind == "wrong-key":
                shutil.copy2(
                    fixture.directory / "issuer/wrong-key.pem",
                    invalid / "server-key.pem",
                )
            else:
                extension = fixture.directory / ("issuer/" + kind + ".ext")
                dns_name = (
                    "openbao" if kind == "missing-loopback-san" else "wrong.invalid"
                )
                extension.write_text(
                    "subjectAltName=DNS:" + dns_name + "\nextendedKeyUsage=serverAuth\n"
                )
                captured(
                    [
                        "openssl",
                        "x509",
                        "-req",
                        "-in",
                        str(fixture.directory / "issuer/server.csr"),
                        "-CA",
                        str(fixture.tls / "ca.pem"),
                        "-CAkey",
                        str(fixture.directory / "issuer/ca-key.pem"),
                        "-CAcreateserial",
                        "-out",
                        str(invalid / "server.pem"),
                        "-days",
                        "1",
                        "-extfile",
                        str(extension),
                    ]
                )
            invalid_dirs.append(invalid)
        for invalid in invalid_dirs:
            self.must(
                captured(
                    [
                        *preflight,
                        str(invalid),
                        "openbao/openbao:2.7.1@sha256:6d2b93856e3fcf7b18ad855a0b51eaba474dc8b79cf554379ea32034797d2acf",
                    ],
                    allow_failure=True,
                ).returncode
                != 0,
                "TLS material preflight accepted expired/CA/SAN/key mismatch",
            )
        print(
            "observed expired server certificate and material preflight rejection: PASS",
            flush=True,
        )
