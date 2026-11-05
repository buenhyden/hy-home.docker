"""LAB lease controller contracts (SPEC-0215)."""

from __future__ import annotations

import datetime as dt
import importlib.util
import io
import json
import os
import pathlib
import subprocess
import tempfile
import unittest
from unittest import mock

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "lab_controller", ROOT / "scripts/operations/lab.py"
)
lab = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(lab)


def model(project, services, volumes=None, networks=None, data_root=None):
    rendered = {
        "name": project,
        "services": services,
        "volumes": volumes or {},
        "networks": networks or {},
    }
    if data_root is not None:
        rendered["x-hyhome-data-root"] = data_root
    return rendered


def service(
    container=None, ports=(), binds=(), cpus=1, memory=2**30, replicas=None,
    reserve=True,
):  # fmt: skip
    """A rendered service; reserve True reserves its limits, a pair sets them."""
    spec = {
        "cpus": cpus,
        "mem_limit": str(memory),
        "ports": [{"host_ip": h, "published": p} for h, p in ports],
        "volumes": [{"type": "bind", "source": b} for b in binds],
    }
    if container:
        spec["container_name"] = container
    deploy = {}
    if replicas:
        deploy["replicas"] = replicas
    if reserve:
        cpu, mem = (cpus, memory) if reserve is True else reserve
        # Compose renders a reservation memory as a byte string.
        deploy["resources"] = {"reservations": {"cpus": cpu, "memory": str(int(mem))}}
    if deploy:
        spec["deploy"] = deploy
    return spec


def read_only_service(container, source, target="/etc/example/config.yml"):
    spec = service(container)
    spec["volumes"] = [
        {"type": "bind", "source": source, "target": target, "read_only": True}
    ]
    return spec


ROOTFP = {"home_data_root": "/data/home", "docker_root": "/var/lib/docker-data"}


def container_record(
    project, *, name="", ports=(), cpus=0.0, memory=0, running=True, service=""
):
    return {
        "name": name,
        "project": project,
        "service": service,
        "ports": set(ports),
        "cpus": cpus,
        "memory": memory,
        "running": running,
    }


class LabSourceContainmentTests(unittest.TestCase):
    """Permanent path contracts; no secret file, runtime or data access."""

    def test_lab_only_build_and_bind_assets_are_inside_root_labs(self) -> None:
        family = ROOT / "labs"
        for name in ("postgresql-ha", "valkey-cluster", "locust"):
            with self.subTest(lab=name):
                self.assertEqual(f"labs/{name}/docker-compose.yml", lab.lab_file(name))
                source = family / name / "docker-compose.yml"
                base = source.parent
                document = yaml.safe_load(source.read_text())
                self.assertTrue(document["services"])
                for service in document["services"].values():
                    if "build" in service:
                        context = (base / service["build"]["context"]).resolve()
                        self.assertTrue(context.is_relative_to(family))
                        self.assertTrue((context / "Dockerfile").is_file())
                    for mount in service.get("volumes", []):
                        if not isinstance(mount, str):
                            continue
                        asset = mount.split(":", 1)[0]
                        if not asset.startswith("."):
                            continue  # Named state volumes are not source artifacts.
                        path = (base / asset).resolve()
                        self.assertTrue(path.is_relative_to(family), path)
                        self.assertTrue(path.is_file(), path)
                        self.assertTrue(mount.endswith(":ro"), mount)
                    if "extends" in service:
                        shared = (base / service["extends"]["file"]).resolve()
                        self.assertEqual(
                            ROOT / "infra/common-optimizations.yml", shared
                        )

    def test_each_moved_family_has_one_source_home_and_populated_readmes(self) -> None:
        for old, name in (
            ("infra/04-data/postgresql-cluster", "postgresql-ha"),
            ("infra/04-data/valkey-cluster", "valkey-cluster"),
            ("infra/11-quality/locust", "locust"),
        ):
            with self.subTest(lab=name):
                self.assertFalse((ROOT / old).exists(), old)
                family = ROOT / "labs" / name
                self.assertTrue(family.is_dir(), family)
                directories = [family, *(p for p in family.rglob("*") if p.is_dir())]
                for directory in directories:
                    readme = directory / "README.md"
                    self.assertTrue(readme.is_file(), directory)
                    self.assertIn("## Overview", readme.read_text())
                    self.assertIn("## Scope", readme.read_text())


class FootprintTests(unittest.TestCase):
    def test_footprint_counts_replicas_writable_binds_and_devices(self) -> None:
        rendered = model(
            "hy-home-lab-x",
            {
                "a": service("lab-a", [("127.0.0.1", "35000")], ["/lab/x/a"]),
                "b": service(cpus=0.5, memory=2**20, replicas=3),
            },
            volumes={
                "v": {"driver_opts": {"device": "/lab/x/v"}},
                "s": {"driver_opts": {"device": "/lab/x/scenario"}},
            },
            networks={"n": {"name": "hy-home-lab-x-core"}},
        )
        rendered["services"]["a"]["volumes"] += [
            {"type": "bind", "source": "/repo/config", "read_only": True},
            {"type": "volume", "source": "v"},
            {"type": "volume", "source": "s", "read_only": True},
        ]
        found = lab.footprint(rendered)
        replicas = {f"hy-home-lab-x-b-{i}" for i in (1, 2, 3)}
        self.assertEqual({"lab-a"} | replicas, found["containers"])
        self.assertEqual({"127.0.0.1:35000"}, found["ports"])
        self.assertEqual(
            {"/lab/x/a", "/lab/x/v", "/lab/x/scenario", "/repo/config"},
            found["paths"],
        )
        # A read-only input collides like state but is never a cleanup target.
        self.assertEqual({"/lab/x/a", "/lab/x/v"}, found["state"])
        self.assertEqual({"/lab/x/scenario", "/repo/config"}, found["inputs"])
        self.assertEqual({"hy-home-lab-x-core"}, found["networks"])
        self.assertEqual(2.5, found["cpus"])
        self.assertEqual(2**30 + 3 * 2**20, found["memory"])
        # Reservations are multiplied by replicas like the limits.
        self.assertEqual(2.5, found["reserved_cpus"])
        self.assertEqual(2**30 + 3 * 2**20, found["reserved_memory"])

    def test_footprint_reads_limits_from_deploy_resources(self) -> None:
        spec = {
            "deploy": {
                "resources": {
                    "limits": {"cpus": "4.0", "memory": str(8 * 2**30)},
                    "reservations": {"cpus": "0.05", "memory": str(4 * 2**30)},
                }
            }
        }
        found = lab.footprint(model("hy-home-lab-x", {"o": spec}))
        self.assertEqual(
            {"cpus": 4.0, "memory": float(8 * 2**30)}, found["services"]["o"]
        )
        self.assertEqual(4.0, found["cpus"])
        self.assertEqual(0.05, found["reserved_cpus"])


class CollisionAndBudgetTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = lab.footprint(
            model(
                "hy-home-infra",
                {"pg": service("mng-pg", [("0.0.0.0", "5432")], ["/data/home/pg"])},
                networks={"n": {"name": "infra_net"}},
            )
        )
        self.lab1 = lab.footprint(
            model(
                "hy-home-lab-one",
                {"x": service("lab-one-x", [("127.0.0.1", "35001")], ["/lab/one"])},
                networks={"n": {"name": "hy-home-lab-one"}},
            )
        )

    def test_clean_selection_has_no_problem(self) -> None:
        self.assertEqual([], lab.collisions({"one": self.lab1}, self.root, []))

    def test_two_labs_with_shared_names_ports_and_paths_are_refused(self) -> None:
        lab2 = lab.footprint(
            model(
                "hy-home-lab-two",
                {
                    "x": service(
                        "lab-one-x", [("0.0.0.0", "35001")], ["/lab/one/nested"]
                    )
                },
                networks={"n": {"name": "hy-home-lab-one"}},
            )
        )
        problems = lab.collisions({"one": self.lab1, "two": lab2}, self.root, [])
        text = "\n".join(problems)
        for fragment in (
            "container lab-one-x",
            "network hy-home-lab-one",
            "host port",
            "data path",
        ):
            self.assertIn(fragment, text)

    def test_lab_inside_home_data_or_on_home_port_is_refused(self) -> None:
        bad = lab.footprint(
            model(
                "hy-home-lab-bad",
                {"x": service("lab-bad", [("127.0.0.1", "5432")], ["/data/home"])},
            )
        )
        text = "\n".join(lab.collisions({"bad": bad}, self.root, []))
        self.assertIn("host port 127.0.0.1:5432 also in root", text)
        self.assertIn("data path /data/home overlaps root", text)

    def test_lab_reusing_the_home_kafka_cluster_id_is_refused(self) -> None:
        def kafka(project, container, cluster_id):
            spec = service(container)
            spec["environment"] = {"CLUSTER_ID": cluster_id}
            return lab.footprint(model(project, {"broker": spec}))

        home = kafka("hy-home-infra", "kafka-1", "home-kraft-id")
        same = kafka("hy-home-lab-kafka", "lab-kafka-1", "home-kraft-id")
        own = kafka("hy-home-lab-kafka", "lab-kafka-1", "lab-kraft-id")
        text = "\n".join(lab.collisions({"kafka": same}, home, []))
        self.assertIn("cluster_id home-kraft-id also in root", text)
        self.assertEqual([], lab.collisions({"kafka": own}, home, []))

    def test_a_kept_volume_for_another_data_root_is_refused(self) -> None:
        rendered = model(
            "hy-home-lab-x",
            {"x": service("lab-x")},
            volumes={
                "v": {"name": "hy-home-lab-x_v", "driver_opts": {"device": "/new/v"}}
            },
        )
        selected = {"x": lab.footprint(rendered)}

        def inspect(device):
            def fake(command, **kwargs):
                self.assertEqual(subprocess.DEVNULL, kwargs.get("stdin"))
                options = json.dumps({"device": device, "o": "bind"})
                return subprocess.CompletedProcess(command, 0, options, "")

            return fake

        with mock.patch.object(lab.subprocess, "run", side_effect=inspect("/old/v")):
            text = "\n".join(lab.stale_volumes("docker", selected))
        self.assertIn("docker volume rm hy-home-lab-x_v", text)
        with mock.patch.object(lab.subprocess, "run", side_effect=inspect("/new/v")):
            self.assertEqual([], lab.stale_volumes("docker", selected))

    def test_read_only_host_root_observer_owns_no_lab_path(self) -> None:
        # cadvisor and node-exporter bind / read-only to observe the host.
        # That contains every path but owns none, so it must not refuse
        # every LAB; a LAB that itself binds / is still refused.
        rendered = model(
            "hy-home-infra",
            {"pg": service("mng-pg", binds=["/data/home/pg"])},
        )
        rendered["services"]["cadvisor"] = service("cadvisor")
        rendered["services"]["cadvisor"]["volumes"] = [
            {"type": "bind", "source": "/", "target": "/rootfs", "read_only": True}
        ]
        root = lab.footprint(rendered)
        self.assertEqual([], lab.collisions({"one": self.lab1}, root, []))
        greedy = model("hy-home-lab-g", {"x": service("lab-g")})
        greedy["services"]["x"]["volumes"] = [
            {"type": "bind", "source": "/", "target": "/host", "read_only": True}
        ]
        text = "\n".join(lab.collisions({"g": lab.footprint(greedy)}, root, []))
        self.assertIn("data path / overlaps root", text)
        writable = model("hy-home-infra", {"w": service("w", binds=["/"])})
        text = "\n".join(
            lab.collisions({"one": self.lab1}, lab.footprint(writable), [])
        )
        self.assertIn("overlaps root", text)

    def test_read_only_source_tree_tool_owns_no_lab_config(self) -> None:
        # conftest binds the infra/ and labs/ source trees read-only. A LAB's
        # own read-only config inside them is not HOME data; writable,
        # secret or whole-tree LAB binds, or a writable HOME bind, still are.
        def home(read_only=True):
            spec = service("conftest")
            spec["volumes"] = [
                {
                    "type": "bind",
                    "source": str(ROOT / "labs"),
                    "target": "/project/labs",
                    "read_only": read_only,
                }
            ]
            return lab.footprint(model("hy-home-infra", {"conftest": spec}))

        def lab_with(source, read_only=True, target="/etc/lab/config"):
            spec = service("lab-x")
            spec["volumes"] = [
                {
                    "type": "bind",
                    "source": source,
                    "target": target,
                    "read_only": read_only,
                }
            ]
            return lab.footprint(model("hy-home-lab-x", {"x": spec}))

        config = str(ROOT / "labs/dbt/profiles")
        self.assertEqual([], lab.collisions({"x": lab_with(config)}, home(), []))
        for name, selected, root in (
            ("writable LAB path", lab_with(config, read_only=False), home()),
            ("secret LAB path", lab_with(str(ROOT / "labs/x/secrets/a")), home()),
            ("whole tree", lab_with(str(ROOT / "labs")), home()),
            ("writable HOME tree", lab_with(config), home(read_only=False)),
        ):
            with self.subTest(case=name):
                self.assertTrue(lab.collisions({"x": selected}, root, []))

    def test_read_only_secrets_backup_owns_no_lab_secret_copy(self) -> None:
        # restic binds the repo's secrets/ read-only to back it up. A LAB's
        # read-only copy under secrets/labs/<name>/ is not HOME data; a
        # writable HOME bind, a HOME secret, the whole LAB secrets tree or a
        # writable LAB bind still clash.
        def home(read_only=True):
            spec = service("restic")
            spec["volumes"] = [
                {
                    "type": "bind",
                    "source": str(ROOT / "secrets"),
                    "target": "/src/host/secrets",
                    "read_only": read_only,
                }
            ]
            # root_footprint makes every HOME sensitive input HOME state.
            return lab.root_footprint(
                model("hy-home-infra", {"restic": spec}, data_root="/data/home")
            )

        def lab_secret(path):
            rendered = model("hy-home-lab-x", {"x": service("lab-x")})
            rendered["secrets"] = {"s": {"name": "s", "file": path}}
            return lab.footprint(rendered)

        def lab_bind(path):
            spec = service("lab-x")
            spec["volumes"] = [{"type": "bind", "source": path, "target": "/x"}]
            return lab.footprint(model("hy-home-lab-x", {"x": spec}))

        def writable_repo():
            spec = service("w")
            spec["volumes"] = [{"type": "bind", "source": str(ROOT), "target": "/r"}]
            return lab.root_footprint(
                model("hy-home-infra", {"w": spec}, data_root="/data/home")
            )

        copy = str(ROOT / "secrets/labs/x/password.txt")
        other = str(ROOT / "secrets/labs/y/password.txt")
        env = {"LAB_DATA_DIR": "/lab-data"}
        self.assertEqual([], lab.collisions({"x": lab_secret(copy)}, home(), []))
        self.assertEqual(
            [], lab.source_allowlist_problems({"x": lab_secret(copy)}, env, home())
        )
        with tempfile.TemporaryDirectory() as directory:
            link = os.path.join(directory, "password.txt")
            os.symlink(other, link)
            symlinked = lab_secret(link)
        escaping = lab_secret(str(ROOT / "secrets/labs/x/../y/password.txt"))
        for name, selected in (
            ("another LAB's copy", lab_secret(other)),
            ("symlink to another LAB's copy", symlinked),
            ("..-escaping copy", escaping),
        ):
            with self.subTest(case=name):
                self.assertTrue(lab.collisions({"x": selected}, home(), []))
                self.assertTrue(
                    lab.source_allowlist_problems({"x": selected}, env, home())
                )
        for name, selected, root in (
            ("writable root ancestor bind", lab_secret(copy), writable_repo()),
            ("writable HOME bind", lab_secret(copy), home(read_only=False)),
            (
                "HOME secret",
                lab_secret(str(ROOT / "secrets/auth/example_password.txt")),
                home(),
            ),
            ("whole LAB secrets tree", lab_secret(str(ROOT / "secrets/labs")), home()),
            ("writable LAB bind", lab_bind(str(ROOT / "secrets/labs/x")), home()),
        ):
            with self.subTest(case=name):
                self.assertTrue(lab.collisions({"x": selected}, root, []))

    def test_host_root_observer_exemption_keeps_home_secrets_env_and_docker(self):
        # With HOME's read-only / exempt, assets no HOME bind covers must be
        # footprinted explicitly: top-level secret files, the root env file
        # and Docker's data root (security review 2026-11-05).
        observer = service("cadvisor")
        observer["volumes"] = [
            {"type": "bind", "source": "/", "target": "/rootfs", "read_only": True}
        ]
        rendered = model(
            "hy-home-infra", {"cadvisor": observer}, data_root="/data/home"
        )
        secret = str(ROOT / "secrets/auth/example_password.txt")
        rendered["secrets"] = {"example": {"name": "example", "file": secret}}
        root = lab.root_footprint(
            rendered, env_file=ROOT / ".env", docker_root="/var/lib/docker-data"
        )
        for name, source, read_only in (
            ("HOME secret", secret, True),
            ("root env", str(ROOT / ".env"), True),
            ("docker volumes", "/var/lib/docker-data/volumes", False),
        ):
            spec = service("lab-x")
            spec["volumes"] = [
                {
                    "type": "bind",
                    "source": source,
                    "target": "/x",
                    "read_only": read_only,
                }
            ]
            selected = lab.footprint(model("hy-home-lab-x", {"x": spec}))
            with self.subTest(case=name):
                self.assertTrue(lab.collisions({"x": selected}, root, []))
        # A LAB compose secret that reuses a HOME secret file is refused too.
        reuse = model("hy-home-lab-x", {"x": service("lab-x")})
        reuse["secrets"] = {"s": {"name": "s", "file": secret}}
        self.assertTrue(lab.collisions({"x": lab.footprint(reuse)}, root, []))

    def test_source_tree_exemption_needs_a_tracked_non_env_path(self) -> None:
        tree = service("conftest")
        tree["volumes"] = [
            {
                "type": "bind",
                "source": str(ROOT / "infra"),
                "target": "/project/infra",
                "read_only": True,
            }
        ]
        root = lab.footprint(model("hy-home-infra", {"conftest": tree}))
        for source in (
            str(ROOT / "infra/05-messaging/kafka/.env"),
            str(ROOT / "infra/05-messaging/kafka/untracked-p05-review.txt"),
        ):
            spec = read_only_service("lab-x", source)
            with self.subTest(source=source):
                self.assertTrue(
                    lab.collisions(
                        {"x": lab.footprint(model("hy-home-lab-x", {"x": spec}))},
                        root,
                        [],
                    )
                )
        self.assertTrue(lab._sensitive_input(str(ROOT / "labs/.env"), None))
        self.assertFalse(lab._sensitive_input(str(ROOT / "labs/.env.example"), None))

    def test_lab_sources_must_be_on_the_allowlist(self) -> None:
        # Owner decision 2026-11-05: LAB data, read-only LAB secrets,
        # read-only operator LAB_* path inputs and read-only tracked
        # non-sensitive repo files; everything else is refused.
        env = {
            "LAB_DATA_DIR": "/lab-data",
            "LAB_SECRET_DIR": "../../secrets/labs",
            "LAB_SUPERSET_CA_FILE": "/srv/ca/rootCA.pem",
            "LAB_LOCUST_RESULT_DIR": "/srv/locust-results",
        }

        def one(source, read_only):
            spec = service("lab-x")
            spec["volumes"] = [
                {
                    "type": "bind",
                    "source": source,
                    "target": "/x",
                    "read_only": read_only,
                }
            ]
            return {"x": lab.footprint(model("hy-home-lab-x", {"x": spec}))}

        tracked = str(ROOT / "labs/dbt/profiles")
        with mock.patch.object(lab, "_tracked_only", lambda p: p == tracked):
            for source, read_only in (
                ("/lab-data/x/state", False),
                (str(ROOT / "secrets/labs/x/password.txt"), True),
                ("/srv/ca/rootCA.pem", True),
                (tracked, True),
                ("/srv/locust-results/run-1", False),
            ):
                with self.subTest(allowed=source):
                    self.assertEqual(
                        [],
                        lab.source_allowlist_problems(
                            one(source, read_only), env, ROOTFP
                        ),
                    )
            for source, read_only in (
                (str(ROOT / ".git/hooks"), False),
                (str(ROOT / "scripts"), True),
                (str(ROOT / "secrets/.retired/auth/key.txt"), True),
                (str(ROOT / ".env.oidc.tmp"), True),
                (str(pathlib.Path.home() / ".ssh"), True),
                ("/run/docker.sock", True),
                (str(ROOT / "secrets/labs/x/password.txt"), False),
                # Another LAB's copy, and the whole LAB secrets tree.
                (str(ROOT / "secrets/labs/dbt/password.txt"), True),
                (str(ROOT / "secrets/labs"), True),
                ("/srv/ca/rootCA.pem", False),
                (tracked, False),
            ):
                with self.subTest(refused=source, read_only=read_only):
                    self.assertTrue(
                        lab.source_allowlist_problems(
                            one(source, read_only), env, ROOTFP
                        )
                    )

    def test_allowlist_roots_cannot_cover_home_or_the_repo(self) -> None:
        # A LAB_* value equal to or above the repo, its secrets, HOME data,
        # Docker's root or the user home admits nothing (re-review B).
        home = str(pathlib.Path.home())
        repo = str(ROOT)
        root = {"home_data_root": "/data/home", "docker_root": "/var/lib/docker-data"}

        def bind(source, read_only):
            spec = service("lab-x")
            spec["volumes"] = [
                {
                    "type": "bind",
                    "source": source,
                    "target": "/x",
                    "read_only": read_only,
                }
            ]
            return {"x": lab.footprint(model("hy-home-lab-x", {"x": spec}))}

        base = {"LAB_DATA_DIR": "/lab-data"}
        with mock.patch.object(lab, "_tracked_only", lambda p: False):
            for env, source, read_only in (
                ({"LAB_X": "/"}, home + "/.ssh/id_ed25519", True),
                ({"LAB_X": home}, home + "/.ssh/id_ed25519", True),
                ({"LAB_X": repo}, repo + "/secrets/.retired/a.txt", True),
                ({"LAB_X_RESULT_DIR": repo}, repo + "/.git/hooks", False),
                ({"LAB_X_RESULT_DIR": home}, home + "/.ssh/authorized_keys", False),
                (
                    {"LAB_SUPABASE_DOCKER_SOCKET_LOCATION": "/var/run/docker.sock"},
                    "/var/run/docker.sock",
                    True,
                ),
                (
                    {"LAB_SECRET_DIR": "../../secrets"},
                    repo + "/secrets/.retired/a.txt",
                    True,
                ),
            ):
                with self.subTest(env=env):
                    self.assertTrue(
                        lab.source_allowlist_problems(
                            bind(source, read_only), {**base, **env}, root
                        )
                    )
            for data in (home, repo, "/"):
                with self.subTest(data=data):
                    self.assertTrue(
                        lab.source_allowlist_problems(
                            bind(data + "/x", False), {"LAB_DATA_DIR": data}, root
                        )
                    )

    def test_config_files_build_inputs_and_env_files_are_checked(self) -> None:
        root = {"home_data_root": "/data/home", "docker_root": "/var/lib/docker-data"}
        env = {"LAB_DATA_DIR": "/lab-data"}
        rendered = model("hy-home-lab-x", {"x": service("lab-x")})
        rendered["configs"] = {"k": {"file": str(ROOT / "secrets/.retired/a.txt")}}
        with mock.patch.object(lab, "_tracked_only", lambda p: False):
            self.assertTrue(
                lab.source_allowlist_problems({"x": lab.footprint(rendered)}, env, root)
            )
            for build in (
                {"context": str(ROOT)},
                {"context": str(ROOT / "labs/dbt"), "ssh": ["default"]},
                {"context": str(ROOT / "labs/dbt"), "secrets": ["s"]},
                {
                    "context": str(ROOT / "labs/dbt"),
                    "additional_contexts": {"e": str(ROOT)},
                },
            ):
                spec = service("lab-x")
                spec["build"] = build
                with self.subTest(build=sorted(build)):
                    self.assertTrue(
                        lab.source_allowlist_problems(
                            {"x": lab.footprint(model("hy-home-lab-x", {"x": spec}))},
                            env,
                            root,
                        )
                    )
        # The model is rendered with --no-env-resolution, so env_file survives
        # whatever YAML style, extends or include put it there.
        spec = service("lab-x")
        spec["env_file"] = [{"path": str(ROOT / ".env")}]
        selected = {"x": lab.footprint(model("hy-home-lab-x", {"x": spec}))}
        self.assertTrue(lab.source_allowlist_problems(selected, env, root))
        for build in (
            {"context": str(ROOT / "labs/dbt"), "cache_to": ["type=local,dest=/tmp/c"]},
            {
                "context": str(ROOT / "labs/dbt"),
                "cache_from": ["type=local,src=/tmp/c"],
            },
            {"context": str(ROOT / "labs/dbt"), "network": "host"},
            {"context": str(ROOT / "labs/dbt"), "entitlements": ["network.host"]},
            {"context": str(ROOT / "labs/dbt"), "dockerfile": "/etc/Dockerfile"},
            {"context": str(ROOT / "labs/dbt"), "dockerfile": "../../secrets/x"},
            {"context": str(ROOT / "labs/dbt"), "privileged": True},
            {"context": str(ROOT / "labs/dbt"), "dockerfile_inline": "FROM x"},
        ):
            spec = service("lab-x")
            spec["build"] = build
            with self.subTest(build=sorted(build)):
                self.assertTrue(
                    lab.footprint(model("hy-home-lab-x", {"x": spec}))[
                        "build_forbidden"
                    ]
                )

    def test_lab_include_is_refused_in_any_yaml_style(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            raw = pathlib.Path(tmp) / "x.yml"
            for text in (
                "include:\n  - path: ./inc.yml\n    env_file: ../.env\n",
                '{"include": [{path: ./inc.yml, env_file: ../.env}], services: {}}\n',
            ):
                raw.write_text(text, encoding="utf-8")
                with self.subTest(text=text[:20]):
                    self.assertTrue(lab.include_problems("x", raw))
            raw.write_text("services:\n  x:\n    image: busybox\n", encoding="utf-8")
            self.assertEqual([], lab.include_problems("x", raw))
            raw.write_text("- not a mapping\n", encoding="utf-8")
            self.assertTrue(lab.include_problems("x", raw))

    def test_plain_build_inside_its_context_is_allowed(self) -> None:
        spec = service("lab-x")
        spec["build"] = {"context": str(ROOT / "labs/dbt"), "dockerfile": "Dockerfile"}
        self.assertEqual(
            [], lab.footprint(model("hy-home-lab-x", {"x": spec}))["build_forbidden"]
        )

    def test_secret_root_in_the_repo_must_be_secrets_labs(self) -> None:
        env = {"LAB_DATA_DIR": "/lab-data"}

        def secret(source):
            rendered = model("hy-home-lab-x", {"x": service("lab-x")})
            rendered["secrets"] = {"s": {"name": "s", "file": source}}
            return {"x": lab.footprint(rendered)}

        for value, source in (
            ("../../secrets/.retired", "secrets/.retired/auth/key.txt"),
            ("../../secrets/db", "secrets/db/mng-pg/password.txt"),
            ("../../.git", ".git/config"),
        ):
            with self.subTest(value=value):
                self.assertTrue(
                    lab.source_allowlist_problems(
                        secret(str(ROOT / source)),
                        {**env, "LAB_SECRET_DIR": value},
                        ROOTFP,
                    )
                )
        self.assertEqual(
            [],
            lab.source_allowlist_problems(
                secret(str(ROOT / "secrets/labs/x/p.txt")),
                {**env, "LAB_SECRET_DIR": "../../secrets/labs"},
                ROOTFP,
            ),
        )
        # Outside the repo the per-LAB rule is <LAB_SECRET_DIR>/<name>/ too.
        outside = {**env, "LAB_SECRET_DIR": "/srv/lab-secrets"}
        self.assertEqual(
            [],
            lab.source_allowlist_problems(
                secret("/srv/lab-secrets/x/p.txt"), outside, ROOTFP
            ),
        )
        self.assertTrue(
            lab.source_allowlist_problems(
                secret("/srv/lab-secrets/y/p.txt"), outside, ROOTFP
            )
        )

    def test_symlinked_secrets_tree_keeps_the_secrets_labs_rule(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo, vault = pathlib.Path(tmp) / "repo", pathlib.Path(tmp) / "vault"
            (vault / "secrets/.retired").mkdir(parents=True)
            (vault / "secrets/labs").mkdir()
            repo.mkdir()
            (repo / "secrets").symlink_to(vault / "secrets")
            rendered = model("hy-home-lab-x", {"x": service("lab-x")})
            rendered["secrets"] = {
                "s": {"name": "s", "file": str(vault / "secrets/.retired/key.txt")}
            }
            selected = {"x": lab.footprint(rendered)}
            env = {
                "LAB_DATA_DIR": "/lab-data",
                "LAB_SECRET_DIR": str(vault / "secrets/.retired"),
            }
            with mock.patch.object(lab, "ROOT", repo):
                self.assertTrue(lab.source_allowlist_problems(selected, env, ROOTFP))

    def test_sensitive_source_needs_the_secret_root_even_under_other_roots(self):
        spec = service("lab-x")
        spec["volumes"] = [
            {
                "type": "bind",
                "source": "/run/docker.sock",
                "target": "/s",
                "read_only": True,
            }
        ]
        selected = {"x": lab.footprint(model("hy-home-lab-x", {"x": spec}))}
        for env in ({"LAB_X": "/run"}, {"LAB_DATA_DIR": "/run"}):
            with self.subTest(env=env):
                self.assertTrue(lab.source_allowlist_problems(selected, env, ROOTFP))

    def test_tracked_only_uses_literal_pathspecs_and_rejects_ignored_files(self):
        calls = []

        def fake(command, **kwargs):
            calls.append(command)
            if "diff" in command:
                return subprocess.CompletedProcess(
                    command, 1 if fake.mode == "dirty" else 0, "", ""
                )
            if "--others" in command:
                out = "labs/dbt/profiles/.user.yml\0" if "ignored" in fake.mode else ""
            else:
                out = "labs/dbt/profiles/profiles.yml\0"
            return subprocess.CompletedProcess(command, 0, out, "")

        for mode, expected in (("clean", True), ("ignored", False), ("dirty", False)):
            fake.mode = mode
            lab._tracked_only.cache_clear()
            with (
                self.subTest(mode=mode),
                mock.patch.object(lab, "run", side_effect=fake),
            ):
                self.assertIs(
                    expected, lab._tracked_only(str(ROOT / "labs/dbt/profiles"))
                )
        lab._tracked_only.cache_clear()
        self.assertTrue(all("--literal-pathspecs" in command for command in calls))

    def test_symlink_into_home_data_is_still_an_overlap(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = pathlib.Path(tmp) / "home-data"
            home.mkdir()
            alias = pathlib.Path(tmp) / "lab-data"
            alias.symlink_to(home)
            root = lab.footprint(
                model("hy-home-infra", {"pg": service("mng-pg", binds=[str(home)])})
            )
            sneaky = lab.footprint(
                model(
                    "hy-home-lab-s", {"x": service("lab-s", binds=[str(alias / "x")])}
                )
            )
            text = "\n".join(lab.collisions({"s": sneaky}, root, []))
            self.assertIn("overlaps root", text)

    def test_running_name_and_port_are_refused_but_own_project_is_not(self) -> None:
        running = [
            container_record("other", name="lab-one-x", ports=["0.0.0.0:35001"]),
            container_record("hy-home-lab-one", name="lab-one-x", running=False),
        ]
        problems = lab.collisions({"one": self.lab1}, self.root, running)
        self.assertEqual(2, len(problems))

    def test_stopped_container_name_is_reserved_but_its_port_is_not(self) -> None:
        stopped = [
            container_record(
                "other",
                name="lab-one-x",
                ports=["0.0.0.0:35001"],
                cpus=50.0,
                memory=2**40,
                running=False,
            )
        ]
        problems = lab.collisions({"one": self.lab1}, self.root, stopped)
        self.assertEqual(["one: container lab-one-x already exists"], problems)
        stopped[0]["project"] = "hy-home-lab-one"
        self.assertEqual([], lab.collisions({"one": self.lab1}, self.root, stopped))
        stopped[0]["project"] = "hy-home-lab-old"
        allowance = lab.PROMOTION_EXTERNAL_ALLOWANCE
        env = {
            "LAB_HOST_BUDGET_CPUS": str(1 + allowance["cpus"]),
            "LAB_HOST_BUDGET_MEMORY_MIB": str(1024 + allowance["memory_mib"]),
            "LAB_MAX_CONCURRENT": "1",
        }
        self.assertEqual([], lab.budget({"one": self.lab1}, stopped, env, {}))

    def test_shared_public_read_only_config_is_allowed_but_state_is_not(self) -> None:
        def readonly(project, name, source, target="/etc/example/config.yml"):
            return lab.footprint(
                model(project, {"x": read_only_service(name, source, target)})
            )

        shared = str(ROOT / "infra/common-optimizations.yml")
        one = readonly("hy-home-lab-one", "lab-one-x", shared)
        two = readonly("hy-home-lab-two", "lab-two-x", shared)
        self.assertEqual([], lab.collisions({"one": one, "two": two}, self.root, []))
        provision = str(
            ROOT / "infra/04-data/mng-db/pg/provision/run-feature-provision.sh"
        )
        home_job = readonly("hy-home-infra", "grafana-db-provision", provision)
        lab_job = readonly("hy-home-lab-dbt", "dbt-provision", provision)
        self.assertEqual([], lab.collisions({"dbt": lab_job}, home_job, []))
        # Any identical git-tracked, non-sensitive file both sides mount
        # read-only is a shared public input (HOME opensearch and the LAB
        # mount the same tracked security config).
        tracked_file = str(
            ROOT
            / "infra/04-data/opensearch/opensearch/config/opensearch-security/roles.yml"
        )
        home_reader = readonly("hy-home-infra", "opensearch", tracked_file)
        lab_reader = readonly("hy-home-lab-os", "lab-os", tracked_file)
        self.assertEqual([], lab.collisions({"os": lab_reader}, home_reader, []))

        writable = lab.footprint(
            model(
                "hy-home-lab-two",
                {"x": service("lab-two-x", binds=[str(ROOT / "infra")])},
            )
        )
        self.assertIn(
            f"one: data path {shared} overlaps lab two",
            lab.collisions({"one": one, "two": writable}, self.root, []),
        )

        external_one = readonly("hy-home-lab-one", "lab-one-x", "/external/shared.yml")
        external_two = readonly("hy-home-lab-two", "lab-two-x", "/external/shared.yml")
        self.assertTrue(
            lab.collisions({"one": external_one, "two": external_two}, self.root, [])
        )

        for unsafe in (ROOT, ROOT / ".env"):
            with self.subTest(unsafe=unsafe):
                unsafe_one = readonly("hy-home-lab-one", "lab-one-x", str(unsafe))
                unsafe_two = readonly("hy-home-lab-two", "lab-two-x", str(unsafe))
                self.assertTrue(
                    lab.collisions(
                        {"one": unsafe_one, "two": unsafe_two}, self.root, []
                    )
                )

    def test_mixed_read_write_path_cannot_use_public_share_exception(self) -> None:
        shared = str(ROOT / "infra/common-optimizations.yml")
        mixed_spec = service("lab-one-x")
        mixed_spec["volumes"] = [
            {
                "type": "bind",
                "source": shared,
                "target": "/config/read-only.yml",
                "read_only": True,
            },
            {
                "type": "bind",
                "source": shared,
                "target": "/config/writable.yml",
            },
        ]
        readonly_spec = read_only_service("lab-two-x", shared, "/config/read-only.yml")
        mixed = lab.footprint(model("hy-home-lab-one", {"x": mixed_spec}))
        readonly = lab.footprint(model("hy-home-lab-two", {"x": readonly_spec}))

        self.assertIn(shared, mixed["state"])
        self.assertTrue(
            lab.collisions({"mixed": mixed, "readonly": readonly}, self.root, [])
        )

    def test_shared_secret_or_socket_input_is_refused(self) -> None:
        def readonly(project, name, source, target):
            return lab.footprint(
                model(project, {"x": read_only_service(name, source, target)})
            )

        for source, target in (
            ("/repo/secrets/token", "/run/secrets/token"),
            ("/var/run/docker.sock", "/var/run/docker.sock"),
        ):
            with self.subTest(target=target):
                one = readonly("hy-home-lab-one", "lab-one-x", source, target)
                two = readonly("hy-home-lab-two", "lab-two-x", source, target)
                text = "\n".join(
                    lab.collisions({"one": one, "two": two}, self.root, [])
                )
                self.assertIn("sensitive read-only path", text)

    def test_check_budget_uses_reservations(self) -> None:
        # SPEC-0263 0.3.0 section 5: reservations, not limits, plus the
        # external-workload allowance once.
        allowance = lab.PROMOTION_EXTERNAL_ALLOWANCE
        root = lab.footprint(
            model(
                "hy-home-infra",
                {"pg": service("mng-pg", cpus=4, memory=8 * 2**30,
                               reserve=(0.5, 2**29))},
            )
        )  # fmt: skip
        known = {"hy-home-infra": root}
        running = [
            container_record("hy-home-infra", name="mng-pg", service="pg",
                             cpus=4.0, memory=8 * 2**30),
            container_record("", name="k3d-a", cpus=0.0),
            container_record("", name="k3d-b", cpus=0.0),
        ]  # fmt: skip
        # lab1 reserves its limits: 1 CPU, 1 GiB. Needed: 0.5 + 1 + allowance.
        cpus = 0.5 + 1 + allowance["cpus"]
        memory_mib = 512 + 1024 + allowance["memory_mib"]
        env = {
            "LAB_HOST_BUDGET_CPUS": str(cpus),
            "LAB_HOST_BUDGET_MEMORY_MIB": str(memory_mib),
            "LAB_MAX_CONCURRENT": "1",
        }
        self.assertEqual([], lab.budget({"one": self.lab1}, running, env, known))
        env["LAB_HOST_BUDGET_CPUS"] = str(cpus - 0.05)
        env["LAB_HOST_BUDGET_MEMORY_MIB"] = str(memory_mib - 1)
        problems = lab.budget({"one": self.lab1}, running, env, known)
        self.assertEqual(2, len(problems), problems)
        self.assertIn("reserved CPUs", problems[0])
        # A known service without a reservation cannot be summed.
        root["reservations"]["pg"] = {"cpus": 0.0, "memory": 0.0}
        env["LAB_HOST_BUDGET_CPUS"] = "100"
        env["LAB_HOST_BUDGET_MEMORY_MIB"] = "100000"
        problems = lab.budget({"one": self.lab1}, running, env, known)
        self.assertTrue(any("mng-pg" in p and "reservation" in p for p in problems))
        with self.assertRaises(lab.LabError):
            lab.budget({"one": self.lab1}, running, {"LAB_HOST_BUDGET_CPUS": ""}, {})
        # The concurrency limit still counts running LAB projects.
        other = lab.footprint(model("hy-home-lab-old", {"o": service("lab-old")}))
        old = [container_record("hy-home-lab-old", name="lab-old", service="o")]
        problems = lab.budget({"one": self.lab1}, old, env, {"hy-home-lab-old": other})
        self.assertEqual(["2 LABs would run; limit is 1"], problems)
        # The selected LAB's own running containers are not counted twice,
        # and a stopped container is not counted.
        env["LAB_HOST_BUDGET_CPUS"] = str(1 + allowance["cpus"])
        env["LAB_HOST_BUDGET_MEMORY_MIB"] = str(1024 + allowance["memory_mib"])
        own = [container_record("hy-home-lab-one", name="lab-one-x", service="x")]
        self.assertEqual([], lab.budget({"one": self.lab1}, own, env, {}))
        stopped = [container_record("hy-home-lab-old", running=False)]
        self.assertEqual([], lab.budget({"one": self.lab1}, stopped, env, {}))


class AdmissionGuardTests(unittest.TestCase):
    def test_root_marker_is_required_and_must_be_absolute(self) -> None:
        for marker in (None, "relative/home"):
            with self.subTest(marker=marker), self.assertRaises(lab.LabError):
                lab.root_footprint(model("hy-home-infra", {}, data_root=marker))

    def test_lab_data_root_must_not_equal_or_nest_with_home_in_either_direction(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = pathlib.Path(tmp)
            home = base / "home"
            home.mkdir()
            alias = base / "home-alias"
            alias.symlink_to(home)
            root = lab.root_footprint(model("hy-home-infra", {}, data_root=str(home)))
            for candidate in (
                home,
                home / "labs",
                base,
                alias / "labs",
                pathlib.Path("/"),
            ):
                with self.subTest(candidate=candidate):
                    problems = lab.data_root_problems(
                        {"LAB_DATA_DIR": str(candidate)}, root
                    )
                    self.assertEqual(1, len(problems))
                    self.assertIn("LAB_DATA_DIR", problems[0])

            separate = base / "separate-labs"
            self.assertEqual(
                [], lab.data_root_problems({"LAB_DATA_DIR": str(separate)}, root)
            )

    def test_read_only_sources_must_exist_without_symlink_components(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = pathlib.Path(tmp)
            real = base / "real"
            real.mkdir()
            alias = base / "alias"
            alias.symlink_to(real)

            spec = service("lab-x")
            spec["volumes"] = [
                {
                    "type": "bind",
                    "source": str(alias),
                    "target": "/config",
                    "read_only": True,
                },
                {
                    "type": "bind",
                    "source": str(base / "missing"),
                    "target": "/fixtures",
                    "read_only": True,
                },
            ]
            found = lab.footprint(model("hy-home-lab-x", {"x": spec}))
            problems = lab.path_integrity_problems({"x": found})
            self.assertTrue(any("symlink" in problem for problem in problems))
            self.assertTrue(any("does not exist" in problem for problem in problems))
            # Each problem names its source: as declared outside the repo.
            self.assertIn(
                f"x: read-only source {base / 'missing'} does not exist", problems
            )
            self.assertIn(f"x: read-only source {alias} contains a symlink", problems)
            # Repo-relative inside the repository, and a relative one as declared.
            spec["volumes"] = [
                {"type": "bind", "source": str(ROOT / "labs/no-such-input"),
                 "target": "/a", "read_only": True},
                {"type": "bind", "source": "relative/input", "target": "/b",
                 "read_only": True},
            ]  # fmt: skip
            found = lab.footprint(model("hy-home-lab-x", {"x": spec}))
            found["sources"][1]["declared"] = "relative/input"
            problems = lab.path_integrity_problems({"x": found})
            self.assertIn(
                "x: read-only source labs/no-such-input does not exist", problems
            )
            self.assertIn(
                "x: read-only source relative/input must be absolute", problems
            )
            self.assertEqual(set(), found["state"])

    def test_running_container_inventory_includes_stopped_state(self) -> None:
        listed = subprocess.CompletedProcess(
            ["docker", "ps", "--all", "--quiet"], 0, "run\nstop\n", ""
        )
        records = [
            {
                "Name": "/running",
                "Config": {
                    "Labels": {
                        "com.docker.compose.project": "other",
                        "com.docker.compose.service": "svc",
                    }
                },
                "HostConfig": {"NanoCpus": 10**9, "Memory": 2**30},
                "State": {"Running": True},
            },
            {
                "Name": "/stopped",
                "Config": {"Labels": {"com.docker.compose.project": "other"}},
                "HostConfig": {"NanoCpus": 9 * 10**9, "Memory": 9 * 2**30},
                "State": {"Running": False},
            },
        ]
        inspected = subprocess.CompletedProcess(
            ["docker", "inspect", "run", "stop"], 0, json.dumps(records), ""
        )
        with mock.patch.object(lab, "run", side_effect=[listed, inspected]) as called:
            found = lab.running_containers("docker")
        self.assertEqual(
            ["docker", "ps", "--all", "--quiet"], called.call_args_list[0].args[0]
        )
        self.assertEqual([True, False], [item["running"] for item in found])
        self.assertEqual(["svc", ""], [item["service"] for item in found])


def manifest(**changes) -> dict:
    """A valid promotion manifest for a LAB with one service `node`."""
    found = {
        "kind": "replace-same",
        "target": {"folder": "infra/04-data/mng-db/valkey/", "profile": "data"},
        "replaces": [
            {
                "service": "valkey",
                "compose_path": "infra/04-data/mng-db/valkey/docker-compose.yml",
                "consumers": ["infra/07-workflow/airflow/docker-compose.yml"],
            }
        ],
        "integrations": [
            {"kind": "gateway-route", "owner": "infra/01-gateway/traefik/"}
        ],
        "secrets": [
            {"row": "LAB-001", "destination": "secrets/data/valkey/password.txt"}
        ],
        "documents": {"guide": "docs/guide.md", "runbook": "docs/runbook.md"},
        "resources": {
            "services": {
                "node": {
                    "cpus": 0.5,
                    "memory_mib": 512,
                    "reservations": {"cpus": 0.5, "memory_mib": 512},
                }
            },
            "disk_gib": {"data": 5, "images": 1},
        },
    }
    found.update(changes)
    return found


def lab_repo(root: pathlib.Path, name: str, promotion: dict) -> pathlib.Path:
    """A repository holding one folder LAB, its manifest, documents and catalog."""
    folder = root / "labs" / name
    folder.mkdir(parents=True)
    (folder / "docker-compose.yml").write_text("services: {}\n", encoding="utf-8")
    (folder / "promotion.yaml").write_text(yaml.safe_dump(promotion), "utf-8")
    (root / "docs").mkdir()
    for document in ("guide.md", "runbook.md"):
        (root / "docs" / document).write_text("# doc\n", encoding="utf-8")
    catalog = root / "infra/03-security/openbao/secret-catalog.json"
    catalog.parent.mkdir(parents=True)
    catalog.write_text(json.dumps({"entries": [{"id": "LAB-001"}]}), "utf-8")
    return root


class LabLayoutAndManifestTests(unittest.TestCase):
    """SPEC-0263 sections 1-3: folder entrypoint, manifest, socket exception."""

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = lab_repo(pathlib.Path(self.tmp.name), "x", manifest())
        patcher = mock.patch.object(lab, "ROOT", self.repo)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.lab = lab.footprint(
            model(
                "hy-home-lab-x",
                {"node": service("lab-node", cpus=0.5, memory=512 * 2**20)},
            )
        )

    def problems(self, promotion: dict) -> list[str]:
        return lab.manifest_problems("x", promotion, self.lab, {"LAB-001"})

    def assert_problem(self, phrase: str, promotion: dict) -> None:
        found = self.problems(promotion)
        self.assertTrue(any(phrase in item for item in found), found)

    def test_lab_file_resolves_folder_entrypoint(self) -> None:
        self.assertEqual("labs/x/docker-compose.yml", lab.lab_file("x"))
        self.assertEqual("replace-same", lab.load_manifest("x")["kind"])
        for name in ("missing", "../x", "X"):
            with self.subTest(name=name), self.assertRaises(lab.LabError) as raised:
                lab.lab_file(name)
            self.assertIn("unknown LAB", str(raised.exception))
        (self.repo / "labs/x/promotion.yaml").unlink()
        with self.assertRaises(lab.LabError):
            lab.load_manifest("x")

    def test_lab_file_refuses_flat_file(self) -> None:
        (self.repo / "labs/flat.yml").write_text("services: {}\n", encoding="utf-8")
        with self.assertRaises(lab.LabError) as raised:
            lab.lab_file("flat")
        self.assertEqual(
            "flat: flat labs/flat.yml is retired; use labs/flat/docker-compose.yml",
            str(raised.exception),
        )

    def test_manifest_unknown_kind(self) -> None:
        self.assert_problem("unknown kind", manifest(kind="promote"))

    def test_manifest_undecided_with_target(self) -> None:
        self.assert_problem("target", manifest(kind="undecided", replaces=[]))
        missing = manifest(kind="add", replaces=[])
        del missing["target"]
        self.assert_problem("target", missing)

    def test_manifest_target_outside_infra(self) -> None:
        for folder in ("labs/valkey/", "infra/valkey/", "infra/04-data/../../x"):
            with self.subTest(folder=folder):
                self.assert_problem(
                    "outside infra/<tier>/",
                    manifest(target={"folder": folder, "profile": "data"}),
                )

    def test_manifest_replacement_needs_replaces(self) -> None:
        for kind in ("replace-same", "replace-substitute"):
            with self.subTest(kind=kind):
                self.assert_problem("replaces", manifest(kind=kind, replaces=[]))

    def test_manifest_unknown_integration(self) -> None:
        self.assert_problem(
            "integration",
            manifest(integrations=[{"kind": "telepathy", "owner": "infra/"}]),
        )

    def test_manifest_secret_without_catalog_row(self) -> None:
        self.assert_problem(
            "no catalog row",
            manifest(secrets=[{"row": "LAB-999", "destination": "secrets/x"}]),
        )

    def test_manifest_resources_disagree_with_render(self) -> None:
        self.lab = lab.footprint(
            model(
                "hy-home-lab-x",
                {"node": service("lab-node", cpus=1, memory=512 * 2**20)},
            )
        )
        self.assertEqual(
            {"node": {"cpus": 1.0, "memory": float(512 * 2**20)}}, self.lab["services"]
        )
        self.assert_problem("disagrees with rendered limits", manifest())
        extra = manifest()
        extra["resources"]["services"]["ghost"] = {"cpus": 1, "memory_mib": 1}
        self.assert_problem("disagrees with rendered limits", extra)
        # Reservations are carried per service and checked against the render.
        self.lab = lab.footprint(
            model("hy-home-lab-x", {"node": service("lab-node", cpus=0.5,
                  memory=512 * 2**20, reserve=(0.1, 64 * 2**20))})
        )  # fmt: skip
        self.assert_problem("disagree with rendered reservations", manifest())
        bare = manifest()
        del bare["resources"]["services"]["node"]["reservations"]
        self.assert_problem("disagree with rendered reservations", bare)
        good = manifest()
        good["resources"]["services"]["node"]["reservations"] = {
            "cpus": 0.1, "memory_mib": 64
        }  # fmt: skip
        self.assertEqual([], self.problems(good))

    def test_manifest_missing_document(self) -> None:
        self.assert_problem(
            "documents",
            manifest(documents={"guide": "docs/none.md", "runbook": "docs/runbook.md"}),
        )

    def test_manifest_valid_passes(self) -> None:
        self.assertEqual([], self.problems(manifest()))
        undecided = manifest(kind="undecided", replaces=[])
        del undecided["target"]
        self.assertEqual([], self.problems(undecided))

    def test_socket_allowed_only_for_supabase_vector_read_only(self) -> None:
        env = {"LAB_DATA_DIR": "/lab-data", "LAB_SECRET_DIR": "../../secrets/labs"}

        def bind(name, service_name, source, read_only):
            spec = service(f"lab-{service_name}")
            spec["volumes"] = [
                {
                    "type": "bind",
                    "source": source,
                    "target": "/var/run/docker.sock",
                    "read_only": read_only,
                }
            ]
            found = lab.footprint(model(f"hy-home-lab-{name}", {service_name: spec}))
            return lab.source_allowlist_problems({name: found}, env, ROOTFP)

        self.assertEqual([], bind("supabase", "vector", "/var/run/docker.sock", True))
        for case in (
            ("supabase", "vector", "/var/run/docker.sock", False),
            ("supabase", "kong", "/var/run/docker.sock", True),
            ("supabase", "vector", "/run/user/1000/docker.sock", True),
            ("other", "vector", "/var/run/docker.sock", True),
        ):
            with self.subTest(case=case):
                self.assertTrue(bind(*case))

    def test_socket_exception_holds_across_the_check_path(self) -> None:
        # The checks check() composes over sources and paths: integrity,
        # allowlist and HOME collisions. HOME binds the socket read-only too.
        env = {"LAB_DATA_DIR": "/lab-data", "LAB_SECRET_DIR": "../../secrets/labs"}
        socket = "/var/run/docker.sock"

        def mount(source, read_only):
            return {
                "type": "bind",
                "source": source,
                "target": socket,
                "read_only": read_only,
            }

        home = service("hy-alloy")
        home["volumes"] = [mount(socket, True)]
        root = lab.root_footprint(
            model("hy-home-infra", {"alloy": home}, data_root="/data/home"),
            docker_root="/var/lib/docker-data",
        )

        def problems(name, service_name, source, read_only):
            spec = service(f"lab-{service_name}")
            spec["volumes"] = [mount(source, read_only)]
            found = {
                name: lab.footprint(model(f"hy-home-lab-{name}", {service_name: spec}))
            }
            return {
                "integrity": lab.path_integrity_problems(found),
                "allowlist": lab.source_allowlist_problems(found, env, root),
                "collisions": lab.collisions(found, root, []),
            }

        # Real path facts on every host: the socket exists and /var/run is a
        # symlink to /run, as on this server.
        with (
            mock.patch.object(lab.os.path, "lexists", return_value=True),
            mock.patch.object(lab.pathlib.Path, "exists", return_value=True),
            mock.patch.object(lab, "_has_symlink_component", return_value=True),
        ):
            allowed = problems("supabase", "vector", socket, True)
            self.assertEqual(
                {"integrity": [], "allowlist": [], "collisions": []}, allowed
            )
            for case in (
                ("supabase", "vector", socket, False),
                ("supabase", "kong", socket, True),
                ("other", "vector", socket, True),
                ("supabase", "vector", "/run/user/1000/docker.sock", True),
            ):
                found = problems(*case)
                with self.subTest(case=case):
                    self.assertTrue(found["allowlist"])
                    # Integrity checks read-only sources only.
                    if case[3]:
                        self.assertTrue(found["integrity"])
                    if case[2] == socket:  # shared with HOME
                        self.assertTrue(found["collisions"])


class LifecycleTests(unittest.TestCase):
    def setUp(self) -> None:
        # Hermetic: read_env lets exported LAB_* values win over the env file.
        clean = {k: v for k, v in os.environ.items() if not k.startswith("LAB_")}
        env = mock.patch.dict(os.environ, clean, clear=True)
        env.start()
        self.addCleanup(env.stop)
        self.tmp = tempfile.TemporaryDirectory()
        self.data = pathlib.Path(self.tmp.name) / "lab-data"
        self.env_file = pathlib.Path(self.tmp.name) / "lab.env"
        self.outside = pathlib.Path(self.tmp.name) / "outside"
        # A writable operator path outside LAB_DATA_DIR, as LAB_LOCUST_RESULT_DIR
        # is; the allowlist admits only *_RESULT_DIR inputs for writes.
        self.env_file.write_text(
            f'LAB_DATA_DIR="{self.data}"\nLAB_HOST_BUDGET_CPUS="8"\n'
            'LAB_HOST_BUDGET_MEMORY_MIB="8192"\nLAB_MAX_CONCURRENT="1"\n'
            f'LAB_FIXTURE_RESULT_DIR="{self.outside}"\n',
            encoding="utf-8",
        )
        # A fixture repository: the LAB folder, its manifest and the catalog.
        cassandra = manifest(
            kind="add",
            target={"folder": "infra/04-data/nosql/cassandra/", "profile": "data"},
            replaces=[],
            resources={
                "services": {
                    "c": {
                        "cpus": 1,
                        "memory_mib": 1024,
                        "reservations": {"cpus": 1, "memory_mib": 1024},
                    }
                }
            },
        )
        repo = lab_repo(pathlib.Path(self.tmp.name) / "repo", "cassandra", cassandra)
        patcher = mock.patch.object(lab, "ROOT", repo)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.calls: list[list[str]] = []
        self.home_data = pathlib.Path(self.tmp.name) / "home-data"
        self.rendered = model(
            "hy-home-lab-cassandra",
            {"c": service("lab-cassandra-c", [("127.0.0.1", "39042")])},
            volumes={
                "v": {"driver_opts": {"device": str(self.data / "cassandra")}},
                "o": {"driver_opts": {"device": str(self.outside)}},
            },
        )
        self.rendered["services"]["c"]["volumes"] += [
            {"type": "volume", "source": "v"},
            {"type": "volume", "source": "o"},
        ]
        self.compose_rc = 0
        self.ready = [
            {"Id": "node", "Name": "/lab-node",
             "State": {"Status": "running", "Health": {"Status": "healthy"}}},
            {"Id": "init", "Name": "/lab-init", "State": {"Status": "exited", "ExitCode": 0}},
        ]  # fmt: skip

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def fake_run(self, command, **kwargs):
        self.calls.append(command)
        if command[-2:] == ["up", "-d"]:
            # The ledger must exist before anything starts.
            self.assertEqual("starting", self.ledger()["state"])
        if "config" in command:
            payload = (
                self.rendered
                if "-f" in command
                else model("hy-home-infra", {}, data_root=str(self.home_data))
            )
            return subprocess.CompletedProcess(command, 0, json.dumps(payload), "")
        if command[1] == "info":
            # Docker's data root joins the HOME footprint.
            return subprocess.CompletedProcess(command, 0, "/var/lib/docker-test\n", "")
        if command[1:] == ["ps", "--all", "--quiet"]:
            return subprocess.CompletedProcess(command, 0, "", "")
        if command[1:3] == ["ps", "--all"]:
            # Readiness poll of the started project.
            ids = "\n".join(record["Id"] for record in self.ready)
            return subprocess.CompletedProcess(command, 0, ids, "")
        if command[1] == "inspect":
            return subprocess.CompletedProcess(command, 0, json.dumps(self.ready), "")
        if command[1] == "ps":
            return subprocess.CompletedProcess(command, 0, "", "")
        return subprocess.CompletedProcess(command, self.compose_rc, "", "boom")

    def main(self, *argv: str) -> int:
        with mock.patch.object(lab, "run", side_effect=self.fake_run):
            with mock.patch("sys.stdout"), mock.patch("sys.stderr"):
                return lab.main(["--env-file", str(self.env_file), *argv])

    def up(self, lease: str = "1h", purpose: str = "drill", name: str = "cassandra"):
        return self.main("up", name, "--purpose", purpose, "--lease", lease)

    def ledger(self) -> dict:
        path = self.data / ".ledger/cassandra.json"
        return json.loads(path.read_text(encoding="utf-8"))

    def started(self) -> bool:
        return any("up" in call for call in self.calls)

    def test_up_needs_purpose_and_bounded_lease(self) -> None:
        self.assertEqual(2, self.up(lease="0h"))
        self.assertEqual(2, self.up(purpose=" "))
        self.assertEqual(2, self.up(lease="25h"))
        self.assertEqual(2, self.up(name="../etc"))
        self.assertFalse(self.started())

    def test_up_records_ledger_then_down_stops_only_its_project(self) -> None:
        self.assertEqual(0, self.up(lease="2h", purpose="failover drill"))
        entry = self.ledger()
        self.assertEqual("running", entry["state"])
        self.assertEqual("hy-home-lab-cassandra", entry["project"])
        self.assertEqual(
            sorted([str(self.data / "cassandra"), str(self.outside)]),
            entry["cleanup"]["paths"],
        )
        self.assertTrue((self.data / "cassandra").is_dir())
        # Group-writable whatever the umask, for LAB processes in that group.
        self.assertEqual(0o770, (self.data / "cassandra").stat().st_mode & 0o777)
        # Only paths under LAB_DATA_DIR are created.
        self.assertFalse(self.outside.exists())
        up = next(call for call in self.calls if call[-2:] == ["up", "-d"])
        self.assertEqual(["-p", "hy-home-lab-cassandra"], up[2:4])
        self.assertEqual(["up", "-d"], up[-2:])

        self.assertEqual(0, self.main("down", "cassandra"))
        down = self.calls[-1]
        self.assertEqual(["-p", "hy-home-lab-cassandra", "down"], down[2:5])
        self.assertEqual(["down", "--timeout", "30"], down[-3:])
        self.assertNotIn("-f", down)
        self.assertFalse({"-v", "--volumes", "--rmi"} & set(down))
        self.assertEqual("stopped", self.ledger()["state"])

    def test_existing_read_only_input_is_never_created_or_recorded_for_cleanup(
        self,
    ) -> None:
        fixture = pathlib.Path(self.tmp.name) / "fixture.json"
        fixture.write_text('{"input":true}\n', encoding="utf-8")
        # An operator read-only input, as LAB_LOCUST_SCENARIO_DIR is.
        with self.env_file.open("a", encoding="utf-8") as handle:
            handle.write(f'LAB_FIXTURE_INPUT="{fixture}"\n')
        before = (fixture.read_bytes(), fixture.stat().st_mode)
        self.rendered["services"]["c"]["volumes"].append(
            {
                "type": "bind",
                "source": str(fixture),
                "target": "/fixtures/input.json",
                "read_only": True,
            }
        )

        self.assertEqual(0, self.up())
        self.assertNotIn(str(fixture), self.ledger()["cleanup"]["paths"])
        self.assertEqual(before, (fixture.read_bytes(), fixture.stat().st_mode))

    def test_up_waits_for_health_and_accepts_a_finished_init_job(self) -> None:
        # compose `up --wait` fails when an init job exits 0; lab.py does not.
        self.assertEqual(0, self.up())
        self.assertEqual("running", self.ledger()["state"])
        # A one-shot job that is still running is not ready yet.
        self.ready = [
            {"Id": "init", "Name": "/lab-init", "State": {"Status": "running"},
             "HostConfig": {"RestartPolicy": {"Name": "no"}}},
        ]  # fmt: skip
        with (
            mock.patch.object(lab.time, "sleep"),
            mock.patch.dict(lab.os.environ, {"LAB_READY_TIMEOUT_SECONDS": "0"}),
        ):
            self.assertEqual(1, self.up())
        for bad in (
            {"Id": "init", "Name": "/lab-init", "State": {"Status": "exited", "ExitCode": 2}},
            {"Id": "node", "Name": "/lab-node",
             "State": {"Status": "running", "Health": {"Status": "unhealthy"}}},
        ):  # fmt: skip
            with self.subTest(state=bad["State"]):
                self.ready = [bad]
                self.assertEqual(1, self.up())
                self.assertEqual("failed", self.ledger()["state"])

    def test_failed_start_and_stop_exit_non_zero(self) -> None:
        self.compose_rc = 1
        self.assertEqual(1, self.up())
        self.assertEqual("failed", self.ledger()["state"])
        self.assertEqual(1, self.main("down", "cassandra"))
        self.assertEqual("stop-failed", self.ledger()["state"])
        self.assertEqual(2, self.main("down", "valkey-cluster"))

    def test_refused_check_exits_three_without_starting(self) -> None:
        self.rendered["services"]["c"]["cpus"] = 99
        self.assertEqual(3, self.up())
        self.assertFalse(self.started())
        self.assertFalse((self.data / ".ledger/cassandra.json").exists())

    def test_missing_or_symlinked_read_only_input_is_refused_before_ledger(
        self,
    ) -> None:
        real = pathlib.Path(self.tmp.name) / "fixture"
        real.write_text("public fixture", encoding="utf-8")
        alias = pathlib.Path(self.tmp.name) / "fixture-link"
        alias.symlink_to(real)
        for source in (pathlib.Path(self.tmp.name) / "missing", alias):
            with self.subTest(source=source):
                self.calls.clear()
                self.rendered["services"]["c"]["volumes"] = [
                    {
                        "type": "bind",
                        "source": str(source),
                        "target": "/fixtures/input",
                        "read_only": True,
                    }
                ]
                self.assertEqual(3, self.up())
                self.assertFalse(self.started())
                self.assertFalse((self.data / ".ledger/cassandra.json").exists())

    def test_reap_retries_a_failed_stop_and_refuses_non_lab_ledgers(self) -> None:
        self.assertEqual(0, self.up())
        self.compose_rc = 1
        self.assertEqual(1, self.main("down", "cassandra"))
        self.assertEqual("stop-failed", self.ledger()["state"])
        entry = self.ledger()
        past = dt.datetime.now(dt.UTC) - dt.timedelta(minutes=1)
        entry["expires_at"] = past.isoformat()
        path = self.data / ".ledger/cassandra.json"
        path.write_text(json.dumps(entry))
        self.compose_rc = 0
        self.assertEqual(0, self.main("reap"))
        self.assertEqual("stopped", self.ledger()["state"])
        entry["project"] = "hy-home-infra"
        path.write_text(json.dumps(entry))
        self.calls.clear()
        self.assertEqual(2, self.main("down", "cassandra"))
        self.assertFalse(any("down" in call for call in self.calls))

    def test_malformed_render_exits_two_without_a_traceback(self) -> None:
        # A rendered value of an unexpected type (deploy as a string) raised
        # AttributeError out of main as a traceback with exit 1.
        self.rendered["services"]["c"]["deploy"] = "bogus"
        for argv in (["check", "cassandra"], ["readiness", "cassandra"]):
            with self.subTest(argv=argv):
                stderr = io.StringIO()
                with (
                    mock.patch.object(lab, "run", side_effect=self.fake_run),
                    mock.patch("sys.stdout"),
                    mock.patch("sys.stderr", stderr),
                ):
                    code = lab.main(["--env-file", str(self.env_file), *argv])
                self.assertEqual(2, code)
                self.assertIn("invalid input", stderr.getvalue())
                self.assertNotIn("Traceback", stderr.getvalue())

    def test_bad_inputs_exit_two_instead_of_crashing(self) -> None:
        with self.env_file.open("a", encoding="utf-8") as handle:
            handle.write('LAB_MAX_LEASE_MINUTES="soon"\n')
        self.assertEqual(2, self.up())
        self.assertFalse(self.started())

    def run_job(self, wait_result, deadline: str = "5m", jobs: str = "job-1\n"):
        """`lab.py run` with a fake job container and a scripted `docker wait`."""
        original = self.fake_run

        def fake_run(command, **kwargs):
            if command[1:3] == ["ps", "--all"]:
                self.calls.append(command)
                return subprocess.CompletedProcess(command, 0, jobs, "")
            if command[1] == "wait":
                self.calls.append(command)
                self.assertEqual(300 if deadline == "5m" else 60, kwargs["timeout"])
                if isinstance(wait_result, BaseException):
                    raise wait_result
                return subprocess.CompletedProcess(command, 0, f"{wait_result}\n", "")
            return original(command, **kwargs)

        with mock.patch.object(lab, "run", side_effect=fake_run):
            with mock.patch("sys.stdout"), mock.patch("sys.stderr"):
                return lab.main(
                    ["--env-file", str(self.env_file), "run", "cassandra",
                     "--purpose", "drill", "--lease", "1h", "--deadline", deadline,
                     "--grace", "7"]
                )  # fmt: skip

    def test_run_propagates_the_job_exit_code_and_always_stops(self) -> None:
        self.assertEqual(3, self.run_job(3))
        self.assertTrue(any(call[-2:] == ["up", "-d"] for call in self.calls))
        self.assertFalse(any("--wait" in call for call in self.calls))
        self.assertEqual(["down", "--timeout", "30"], self.calls[-1][-3:])
        entry = self.ledger()
        self.assertEqual(
            ("failed", 3, "stopped"),
            (entry["outcome"], entry["job_exit_code"], entry["state"]),
        )
        self.assertFalse(any(call[1] == "stop" for call in self.calls))

    def test_run_stops_the_job_at_the_deadline_or_on_cancel(self) -> None:
        for raised, code, outcome in (
            (subprocess.TimeoutExpired("docker wait", 60), 124, "deadline_exceeded"),
            (KeyboardInterrupt(), 130, "cancelled"),
        ):
            with self.subTest(outcome=outcome):
                self.calls.clear()
                self.assertEqual(code, self.run_job(raised, deadline="1m"))
                stops = [call for call in self.calls if call[1] == "stop"]
                # SIGTERM with grace lets Locust flush its CSV before `down`.
                self.assertEqual([["docker", "stop", "--time", "7", "job-1"]], stops)
                self.assertLess(self.calls.index(stops[0]), len(self.calls) - 1)
                self.assertEqual(["down", "--timeout", "30"], self.calls[-1][-3:])
                self.assertEqual(outcome, self.ledger()["outcome"])

    def test_run_stops_a_project_whose_start_failed_or_was_cancelled(self) -> None:
        # `up -d` can exit non-zero after starting some services.
        self.compose_rc = 1
        self.assertEqual(1, self.run_job(0))
        self.compose_rc = 0
        self.assertEqual(["down", "--timeout", "30"], self.calls[-1][-3:])
        self.assertEqual("start_failed", self.ledger()["outcome"])
        original = self.fake_run

        def cancelled_up(command, **kwargs):
            if command[-2:] == ["up", "-d"]:
                self.calls.append(command)
                raise KeyboardInterrupt
            return original(command, **kwargs)

        self.calls.clear()
        with mock.patch.object(self, "fake_run", side_effect=cancelled_up):
            self.assertEqual(130, self.run_job(0))
        self.assertEqual(["down", "--timeout", "30"], self.calls[-1][-3:])
        self.assertEqual("cancelled", self.ledger()["outcome"])

    def test_run_refuses_a_deadline_beyond_the_lease_or_no_single_job(self) -> None:
        self.assertEqual(2, self.run_job(0, deadline="2h"))
        self.assertFalse(self.started())
        self.assertEqual(1, self.run_job(0, jobs="job-1\njob-2\n"))
        self.assertEqual(["down", "--timeout", "30"], self.calls[-1][-3:])

    def test_reap_stops_only_expired_leases(self) -> None:
        self.assertEqual(0, self.up())
        self.calls.clear()
        self.assertEqual(0, self.main("reap"))
        self.assertFalse(any("down" in call for call in self.calls))
        entry = self.ledger()
        past = dt.datetime.now(dt.UTC) - dt.timedelta(minutes=1)
        entry["expires_at"] = past.isoformat()
        (self.data / ".ledger/cassandra.json").write_text(json.dumps(entry))
        self.assertEqual(0, self.main("reap"))
        self.assertTrue(any("down" in call for call in self.calls))
        self.assertEqual("stopped", self.ledger()["state"])


GIB, MIB = 2**30, 2**20


def readiness_case(cpus=1.0, memory=GIB, **changes):
    """A promotion candidate that passes every readiness criterion."""
    candidate = service(cpus=cpus, memory=int(memory))
    candidate["user"] = "999:999"
    case = {
        "manifest": manifest(
            kind="add",
            target={"folder": "infra/04-data/promo-candidate/", "profile": "dev-data"},
            replaces=[],
            integrations=[
                {"kind": "observability", "owner": "infra/06-observability/"}
            ],
            documents={
                "guide": "docs/05.operations/guides/15-labs/0022-valkey-cluster.md",
                "runbook": "docs/05.operations/runbooks/15-labs/0022-valkey-cluster.md",
            },
            resources={
                "services": {
                    "node": {
                        "cpus": cpus,
                        "memory_mib": memory / MIB,
                        "reservations": {"cpus": cpus, "memory_mib": memory / MIB},
                    }
                },
                "disk_gib": {"data": 5, "images": 1},
            },
        ),
        "lab": lab.footprint(model("hy-home-lab-candidate", {"node": candidate})),
        "host": {
            "NCPU": {"value": 12, "source": "docker info"},
            "MemTotal": {"value": 32 * GIB, "source": "docker info"},
            "DockerRootDir": {"value": "/var/lib/docker", "source": "docker info"},
            "docker_version": {"value": "29.9.2", "source": "docker info"},
            "compose_version": {"value": "5.6.1", "source": "docker compose"},
            "cgroup_version": {"value": "2", "source": "docker info"},
            "disk_data": {
                "value": {"free": 100 * GIB, "total": 200 * GIB},
                "source": "shutil.disk_usage",
            },
            "disk_docker": {
                "value": {"free": 100 * GIB, "total": 200 * GIB},
                "source": "shutil.disk_usage",
            },
        },
        # Limits are 4 CPUs and 4 GiB; only the reservation is summed.
        "running": [
            container_record(
                "hy-home", name="home-1", service="home", cpus=4.0, memory=4 * GIB
            ),
        ],
        "root": lab.footprint(
            model(
                "hy-home",
                {
                    "home": service(
                        "home-1", cpus=4, memory=4 * GIB, reserve=(2.0, 2 * GIB)
                    )
                },
            )
        ),
    }
    case.update(changes)
    return case


def reserve(case: dict, service: str, cpus: float, memory: float | None = None):
    """Set a root service's rendered reservation."""
    found = case["root"]["reservations"][service]
    found["cpus"] = cpus
    if memory is not None:
        found["memory"] = memory


ALLOWANCE = lab.PROMOTION_EXTERNAL_ALLOWANCE


def readiness(case: dict) -> dict:
    return lab.readiness("candidate", **case)


DEV_DB = ROOT / "infra/04-data/dev-db"


def dev_db_root() -> dict:
    """A root render with dev-valkey (bind under valkey/) and dev-pg (build
    context pg/), as infra/04-data/dev-db/docker-compose.yml declares."""
    pg = service("dev-pg", ports=[("0.0.0.0", 5432)], cpus=4)
    pg["build"] = {"context": str(DEV_DB / "pg"), "dockerfile": "Dockerfile"}
    valkey = service(
        "dev-valkey", ports=[("0.0.0.0", 6379)], binds=[str(DEV_DB / "valkey/config")],
        cpus=4,
    )  # fmt: skip
    home = service("home-1", cpus=8, memory=4 * GIB, reserve=(2.0, 2 * GIB))
    return lab.footprint(
        model("hy-home", {"home": home, "dev-valkey": valkey, "dev-pg": pg})
    )


def replacement_case(folder: str, services: list[str], kind="replace-same") -> dict:
    case = readiness_case(root=dev_db_root())
    case["manifest"].update(
        kind=kind,
        target={"folder": folder, "profile": "dev-data"},
        replaces=[
            {
                "compose_path": "infra/04-data/dev-db/docker-compose.yml",
                "services": services,
                "consumers": [],
            }
        ],
    )
    return case


class ReadinessTests(unittest.TestCase):
    """SPEC-0263 section 5: the promotion readiness check fails closed."""

    def result(self, report: dict, criterion: str) -> str:
        return report["criteria"][criterion]["result"]

    def test_readiness_passes_within_budget(self) -> None:
        report = readiness(readiness_case())
        self.assertEqual("add", report["kind"])
        for criterion, found in report["criteria"].items():
            self.assertEqual("PASS", found["result"], (criterion, found))
            self.assertTrue(all("source" in v for v in found["values"].values()))
        self.assertEqual("PASS", report["result"])

    def test_owner_check_items_do_not_block_pass(self) -> None:
        report = readiness(readiness_case())
        items = {
            "tier": "function_fit",
            "composition": "profile_and_consumer_clashes",
            "linux": "groups_and_file_modes",
        }
        for criterion, item in items.items():
            found = report["criteria"][criterion]
            self.assertEqual("PASS", found["result"], (criterion, found))
            self.assertEqual("OWNER_JUDGMENT", found["values"][item]["value"])
            self.assertIn("promotion Task", found["values"][item]["source"])
        self.assertEqual(sorted(items.values()), sorted(report["owner_checks"]))
        self.assertEqual("PASS", report["result"])
        # Criteria and the overall result never take OWNER_JUDGMENT.
        results = {c["result"] for c in report["criteria"].values()}
        self.assertLessEqual(results, {"PASS", "FAIL", "NOT_RUN"})

    def test_readiness_sums_reservations_not_limits(self) -> None:
        # Running limits 4 CPUs / 4 GiB, reservation 2 / 2 GiB; the candidate
        # reserves 1 CPU and 1 GiB; the allowance adds 2 CPUs and 6 GiB.
        report = readiness(readiness_case())
        values = report["criteria"]["resources"]["values"]
        self.assertEqual(2.0, values["running_reserved_cpus"]["value"])
        self.assertEqual(1.0, values["candidate_reserved_cpus"]["value"])
        self.assertEqual(ALLOWANCE["cpus"], values["allowance_cpus"]["value"])
        self.assertEqual(2.0 + 1.0 + ALLOWANCE["cpus"], values["cpus_needed"]["value"])
        self.assertEqual(
            2048 + 1024 + ALLOWANCE["memory_mib"], values["memory_needed_mib"]["value"]
        )
        # 7 running reserved CPUs + 1 + 2 = 10 fits the 10-CPU budget even
        # though the running limit alone would be 12.
        case = readiness_case()
        reserve(case, "home", 7.0)
        case["root"]["services"]["home"]["cpus"] = 12.0
        self.assertEqual("PASS", self.result(readiness(case), "resources"))
        reserve(case, "home", 7.05)
        self.assertEqual("FAIL", self.result(readiness(case), "resources"))

    def test_readiness_external_allowance_counts_once(self) -> None:
        base = readiness(readiness_case())["criteria"]["resources"]["values"]
        for count in (1, 5):
            with self.subTest(count=count):
                case = readiness_case()
                case["running"] += [
                    container_record("", name=f"k3d-{i}", cpus=0.0)
                    for i in range(count)
                ]
                found = readiness(case)["criteria"]["resources"]
                self.assertEqual("PASS", found["result"], found)
                values = found["values"]
                self.assertEqual(count, len(values["external_containers"]["value"]))
                self.assertEqual(base["cpus_needed"], values["cpus_needed"])
                self.assertEqual(base["memory_needed_mib"], values["memory_needed_mib"])

    def test_readiness_service_without_reservation_is_not_run(self) -> None:
        case = readiness_case()
        reserve(case, "home", 0.0, 0.0)
        found = readiness(case)["criteria"]["resources"]
        self.assertEqual("NOT_RUN", found["result"], found)
        self.assertTrue(any("home-1" in p for p in found["problems"]), found)
        # A container of a known project whose service is not rendered.
        case = readiness_case()
        case["running"].append(
            container_record("hy-home", name="ghost-1", service="ghost", cpus=1.0)
        )
        found = readiness(case)["criteria"]["resources"]
        self.assertEqual("NOT_RUN", found["result"], found)
        # A running LAB project without a render is not external.
        case = readiness_case()
        case["running"].append(
            container_record("hy-home-lab-other", name="lab-o", service="o")
        )
        found = readiness(case)["criteria"]["resources"]
        self.assertEqual("NOT_RUN", found["result"], found)
        # With its render, the LAB counts by its reservation.
        other = lab.footprint(
            model("hy-home-lab-other", {"o": service("lab-o", reserve=(0.5, GIB))})
        )
        case["labs"] = {"hy-home-lab-other": other}
        found = readiness(case)["criteria"]["resources"]
        self.assertEqual("PASS", found["result"], found)
        self.assertEqual(2.5, found["values"]["running_reserved_cpus"]["value"])
        # A candidate service without a reservation.
        case = readiness_case()
        case["lab"]["reservations"]["node"] = {"cpus": 0.0, "memory": 0.0}
        found = readiness(case)["criteria"]["resources"]
        self.assertEqual("NOT_RUN", found["result"], found)
        self.assertTrue(any("candidate service node" in p for p in found["problems"]))
        # An over-budget known sum stays FAIL with an unmeasured service.
        case = readiness_case()
        reserve(case, "home", 9.5)
        case["running"].append(
            container_record("hy-home", name="ghost-1", service="ghost", cpus=1.0)
        )
        self.assertEqual("FAIL", self.result(readiness(case), "resources"))

    def test_readiness_reservation_above_limit_fails(self) -> None:
        case = readiness_case()
        reserve(case, "home", 5.0)  # limit 4
        found = readiness(case)["criteria"]["resources"]
        self.assertEqual("FAIL", found["result"], found)
        self.assertTrue(any("exceeds its limit" in p for p in found["problems"]))
        case = readiness_case()
        case["lab"]["reservations"]["node"]["memory"] = 2.0 * GIB  # limit 1 GiB
        found = readiness(case)["criteria"]["resources"]
        self.assertEqual("FAIL", found["result"], found)

    def test_readiness_fails_over_cpu_budget(self) -> None:
        # 12 CPUs minus the 2-CPU reserve leaves 10; 7.5 reserved running,
        # 1 candidate and the 2-CPU allowance is 10.5.
        case = readiness_case()
        reserve(case, "home", 7.5)
        case["root"]["services"]["home"]["cpus"] = 8.0
        report = readiness(case)
        self.assertEqual("FAIL", self.result(report, "resources"))
        self.assertEqual("FAIL", report["result"])
        values = report["criteria"]["resources"]["values"]
        self.assertEqual(10.0, values["cpu_budget"]["value"])
        self.assertEqual(12, values["NCPU"]["value"])
        self.assertEqual(10.5, values["cpus_needed"]["value"])

    def test_readiness_compares_memory_bytes_with_mib(self) -> None:
        # Budget: 4096 reserve plus the allowance plus 3072 MiB; 2 GiB is
        # reserved by the running service.
        total = (4096 + ALLOWANCE["memory_mib"] + 3072) * MIB
        case = readiness_case(memory=1024 * MIB)
        case["host"]["MemTotal"]["value"] = total
        self.assertEqual("PASS", self.result(readiness(case), "resources"))
        case = readiness_case(memory=1025 * MIB)
        case["host"]["MemTotal"]["value"] = total
        report = readiness(case)
        self.assertEqual("FAIL", self.result(report, "resources"))
        values = report["criteria"]["resources"]["values"]
        self.assertEqual(
            3072 + ALLOWANCE["memory_mib"], values["memory_budget_mib"]["value"]
        )
        self.assertEqual(
            3073 + ALLOWANCE["memory_mib"], values["memory_needed_mib"]["value"]
        )

    def test_readiness_unlimited_container_is_not_run(self) -> None:
        case = readiness_case()
        case["root"] = lab.footprint(model("hy-home", {
            "home": service("home-1", cpus=4, memory=4 * GIB, reserve=(2.0, 2 * GIB)),
            "free": service("free-1", cpus=0, reserve=(0.5, GIB)),
        }))  # fmt: skip
        case["running"].append(
            container_record("hy-home", name="free-1", service="free")
        )
        report = readiness(case)
        self.assertEqual("NOT_RUN", self.result(report, "resources"))
        self.assertEqual("NOT_RUN", report["result"])
        self.assertTrue(
            any("free-1" in p for p in report["criteria"]["resources"]["problems"])
        )

    def test_readiness_replacement_subtracts_only_running_retired(self) -> None:
        def case(retired_running: bool) -> dict:
            found = readiness_case()
            found["manifest"].update(
                kind="replace-same",
                target={
                    "folder": "infra/04-data/dev-db/valkey/",
                    "profile": "dev-data",
                },
                replaces=[
                    {
                        "compose_path": "infra/04-data/dev-db/docker-compose.yml",
                        "services": ["dev-valkey"],
                        "consumers": [],
                    }
                ],
            )
            found["lab"]["ports"] = {"127.0.0.1:6379"}
            found["root"] = dev_db_root()
            reserve(found, "home", 7.0)
            reserve(found, "dev-valkey", 3.0)
            found["running"].append(
                container_record("hy-home", name="dev-valkey", service="dev-valkey",
                                 ports={"0.0.0.0:6379"}, running=retired_running)
            )  # fmt: skip
            return found

        # Reserved: 7 + 3 retired + 1 candidate + 2 allowance, minus the 3
        # retired once.
        report = readiness(case(True))
        for criterion in ("tier", "resources"):
            self.assertEqual("PASS", self.result(report, criterion), report)
        values = report["criteria"]["resources"]["values"]
        self.assertEqual(3.0, values["retired_reserved_cpus"]["value"])
        self.assertEqual(10.0, values["cpus_needed"]["value"])
        # Stopped: never counted, so nothing is subtracted.
        report = readiness(case(False))
        for criterion in ("tier", "resources"):
            self.assertEqual("PASS", self.result(report, criterion), report)
        values = report["criteria"]["resources"]["values"]
        self.assertEqual(0.0, values["retired_reserved_cpus"]["value"])
        self.assertEqual(10.0, values["cpus_needed"]["value"])

    def test_readiness_undecided_fails_tier(self) -> None:
        case = readiness_case()
        case["manifest"]["kind"] = "undecided"
        del case["manifest"]["target"]
        report = readiness(case)
        self.assertEqual("FAIL", self.result(report, "tier"))
        self.assertEqual("FAIL", report["result"])

    def test_readiness_refuses_a_target_outside_the_tier(self) -> None:
        case = readiness_case()
        case["manifest"]["target"]["folder"] = "infra/04-data/../../etc/"
        self.assertEqual("FAIL", self.result(readiness(case), "tier"))

    def test_readiness_add_does_not_honor_replaces(self) -> None:
        # Reviewer repro: an add candidate naming a "root" service hid a real
        # port and network clash with root.
        case = readiness_case()
        case["root"]["ports"] = {"0.0.0.0:8080"}
        case["lab"]["ports"] = {"0.0.0.0:8080"}
        case["root"]["networks"] = case["root"]["networks"] | {"shared"}
        case["lab"]["networks"] = case["lab"]["networks"] | {"shared"}
        case["manifest"]["replaces"] = [
            {"compose_path": "infra/04-data/x/docker-compose.yml", "services": ["root"]}
        ]
        report = readiness(case)
        self.assertEqual("FAIL", self.result(report, "composition"))
        problems = report["criteria"]["composition"]["problems"]
        self.assertTrue(any("8080" in p for p in problems), problems)
        self.assertTrue(any("shared" in p for p in problems), problems)

    def test_readiness_retired_name_filters_no_other_clash(self) -> None:
        # Reviewer repro: retiring "held" dropped "host port ... held by other".
        for services in (["held"], ["dev-valkey"]):
            with self.subTest(services=services):
                case = replacement_case("infra/04-data/dev-db/valkey/", services)
                case["lab"]["ports"] = {"0.0.0.0:6380"}
                case["running"].append(
                    {"name": "other-svc", "project": "hy-home",
                     "ports": {"0.0.0.0:6380"}, "cpus": 1, "memory": GIB,
                     "running": True}
                )  # fmt: skip
                report = readiness(case)
                self.assertEqual("FAIL", self.result(report, "composition"))
                problems = report["criteria"]["composition"]["problems"]
                self.assertTrue(any("other-svc" in p for p in problems), problems)

    def test_readiness_retired_service_must_exist(self) -> None:
        case = replacement_case("infra/04-data/dev-db/valkey/", ["ghost"])
        report = readiness(case)
        self.assertEqual("FAIL", self.result(report, "composition"))
        problems = report["criteria"]["composition"]["problems"]
        self.assertTrue(any("ghost" in p for p in problems), problems)
        case = replacement_case("infra/04-data/dev-db/valkey/", ["dev-valkey"])
        case["manifest"]["replaces"][0]["compose_path"] = "infra/04-data/nope.yml"
        self.assertEqual("FAIL", self.result(readiness(case), "composition"))

    def test_readiness_tier_needs_the_folder_of_a_retired_service(self) -> None:
        # Reviewer repro: the valkey manifest claimed dev-db/pg/ (dev-pg stays).
        case = replacement_case("infra/04-data/dev-db/pg/", ["dev-valkey"])
        self.assertEqual("FAIL", self.result(readiness(case), "tier"))
        case = replacement_case("infra/04-data/dev-db/pg/", ["dev-pg"])
        self.assertEqual("PASS", self.result(readiness(case), "tier"))
        case = replacement_case("infra/04-data/dev-db/valkey/", ["dev-valkey"], "add")
        self.assertEqual("FAIL", self.result(readiness(case), "tier"))

    def test_readiness_tier_needs_exclusive_ownership(self) -> None:
        # Review probes A3 and A5: a retired service binding a file in a kept
        # folder, or a parent folder that still holds dev-pg.
        case = replacement_case("infra/04-data/qdrant/", ["dev-valkey"])
        case["root"] = lab.footprint(
            model(
                "hy-home",
                {
                    "dev-valkey": service(
                        "dev-valkey",
                        binds=[str(ROOT / "infra/04-data/qdrant/README.md")],
                    ),
                    "qdrant": service(
                        "qdrant", binds=[str(ROOT / "infra/04-data/qdrant/config")]
                    ),
                },
            )
        )
        self.assertEqual("FAIL", self.result(readiness(case), "tier"))
        # Probe shape: no qdrant in root; qdrant/docker-compose.yml still
        # declares the kept qdrant service.
        del case["root"]["by_service"]["qdrant"]
        self.assertEqual("FAIL", self.result(readiness(case), "tier"))
        case = replacement_case("infra/04-data/dev-db/", ["dev-valkey"])
        report = readiness(case)
        self.assertEqual("FAIL", self.result(report, "tier"))
        self.assertTrue(
            any("dev-pg" in p for p in report["criteria"]["tier"]["problems"])
        )

    def test_readiness_shared_provision_file_claims_no_folder(self) -> None:
        # kafka binds mng-pg's provisioning script; retiring kafka-1 cannot
        # claim mng-db/pg/, which mng-pg keeps.
        provision = ROOT / "infra/04-data/mng-db/pg/provision/run-feature-provision.sh"
        case = readiness_case()
        case["manifest"].update(
            kind="replace-same",
            target={"folder": "infra/04-data/mng-db/pg/", "profile": "dev-data"},
            replaces=[
                {
                    "compose_path": "infra/05-messaging/kafka/docker-compose.yml",
                    "services": ["kafka-1"],
                }
            ],
        )
        case["root"] = lab.footprint(
            model(
                "hy-home",
                {
                    "kafka-1": read_only_service("kafka-1", str(provision)),
                    "mng-pg": service(
                        "mng-pg", binds=[str(ROOT / "infra/04-data/mng-db/pg/config")]
                    ),
                },
            )
        )
        self.assertEqual("FAIL", self.result(readiness(case), "tier"))

    def test_readiness_keeps_a_port_a_kept_service_declares(self) -> None:
        # Review probe B: a stopped kept service publishes the retired port.
        case = replacement_case("infra/04-data/dev-db/valkey/", ["dev-valkey"])
        root = dev_db_root()
        extra = lab.footprint(
            model("hy-home", {"other": service("other-1", ports=[("0.0.0.0", 6379)])})
        )
        root["by_service"]["other"] = extra["by_service"]["other"]
        root["containers"] |= extra["containers"]
        case["root"] = root
        case["lab"]["ports"] = {"0.0.0.0:6379"}
        report = readiness(case)
        self.assertEqual("FAIL", self.result(report, "composition"))

    def test_readiness_add_cannot_claim_an_existing_folder(self) -> None:
        # Reviewer repro: add with a made-up compose_path claimed qdrant/.
        case = readiness_case()
        case["manifest"].update(
            target={"folder": "infra/04-data/qdrant/", "profile": "dev-data"},
            replaces=[
                {"compose_path": "infra/04-data/qdrant/nope.yml", "services": []}
            ],
        )
        self.assertEqual("FAIL", self.result(readiness(case), "tier"))

    def test_readiness_fails_tier_on_manifest_problems(self) -> None:
        case = readiness_case()
        case["manifest"]["secrets"] = [{"row": "NO-SUCH-ROW", "destination": "x"}]
        report = readiness(case)
        self.assertEqual("FAIL", self.result(report, "tier"))
        self.assertTrue(
            any("NO-SUCH-ROW" in p for p in report["criteria"]["tier"]["problems"])
        )

    def test_readiness_over_budget_with_unlimited_stays_fail(self) -> None:
        # Ruling: the known lower bound already exceeds the budget.
        case = readiness_case()
        reserve(case, "home", 9.5)
        case["root"]["services"]["home"]["cpus"] = 10.0
        case["running"].append(
            container_record("hy-home", name="free-1", service="free")
        )
        self.assertEqual("FAIL", self.result(readiness(case), "resources"))

    def test_measure_host_omits_unparsable_docker_info(self) -> None:
        answers = [
            subprocess.CompletedProcess([], 0, "not json", ""),
            subprocess.CompletedProcess([], 1, "", ""),
        ]
        with (
            mock.patch.object(lab, "run", side_effect=answers),
            mock.patch.object(lab.shutil, "disk_usage", side_effect=OSError),
        ):
            host = lab.measure_host("docker", "/data/home")
        self.assertEqual({}, host)
        self.assertEqual("NOT_RUN", readiness(readiness_case(host=host))["result"])

    def test_readiness_candidate_without_limits_is_not_run(self) -> None:
        # Review probe: a candidate with no limits summed as 0 and passed.
        report = readiness(readiness_case(cpus=0, memory=0))
        self.assertEqual("NOT_RUN", self.result(report, "resources"))
        problems = report["criteria"]["resources"]["problems"]
        self.assertTrue(any("candidate service node" in p for p in problems))
        self.assertEqual("FAIL", self.result(report, "tier"))

    def test_manifest_refuses_a_zero_or_missing_limit(self) -> None:
        rendered = {"services": {"node": {"cpus": 0.0, "memory": 0.0}}}
        for declared in ({"cpus": 0, "memory_mib": 0}, {}):
            with self.subTest(declared=declared):
                found = manifest(resources={"services": {"node": declared}})
                problems = lab.manifest_problems("x", found, rendered, {"LAB-001"})
                self.assertTrue(any("no cpus or memory" in p for p in problems))

    def test_readiness_tier_refuses_an_unreadable_or_escaping_subtree(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = pathlib.Path(tmp) / "repo"
            folder = repo / "infra/04-data/x"
            (folder / "docker-compose.yml").mkdir(parents=True)  # unreadable
            outside = pathlib.Path(tmp) / "outside"
            outside.mkdir()
            (folder / "linked").symlink_to(outside, target_is_directory=True)
            (repo / "infra/04-data/escape").symlink_to(outside)
            case = readiness_case()
            with mock.patch.object(lab, "ROOT", repo):
                case["manifest"]["target"]["folder"] = "infra/04-data/x/"
                problems = readiness(case)["criteria"]["tier"]["problems"]
                self.assertTrue(any("cannot be read" in p for p in problems), problems)
                self.assertTrue(any("symlinked directory" in p for p in problems))
                case["manifest"]["target"]["folder"] = "infra/04-data/escape/"
                problems = readiness(case)["criteria"]["tier"]["problems"]
                self.assertTrue(any("outside the repository" in p for p in problems))

    def test_manifest_paths_stay_inside_the_repository(self) -> None:
        self.assertIsNone(lab._repo_path("/etc/passwd"))
        self.assertIsNone(lab._repo_path("docs/../../etc"))
        self.assertIsNone(lab._repo_path(None))
        self.assertEqual(ROOT / "docs", lab._repo_path("docs"))
        found = manifest(documents={"guide": "/etc/hostname", "runbook": "../x"})
        problems = lab.manifest_problems(
            "x", found, {"services": {"node": {"cpus": 0.5, "memory": 512.0 * MIB}}},
            {"LAB-001"},
        )  # fmt: skip
        self.assertTrue(any("guide" in p for p in problems), problems)
        self.assertTrue(any("runbook" in p for p in problems), problems)
        case = readiness_case()
        case["manifest"]["integrations"] = [{"kind": "network", "owner": "/etc"}]
        self.assertEqual("FAIL", self.result(readiness(case), "composition"))
        case = readiness_case()
        case["manifest"]["target"]["folder"] = "infra/04-data/../../etc/"
        self.assertEqual("FAIL", self.result(readiness(case), "tier"))

    def test_readiness_compose_path_must_be_a_root_include(self) -> None:
        # labs/valkey-cluster/docker-compose.yml declares valkey-node-0, but
        # root does not include it, so it cannot retire anything.
        case = replacement_case("infra/04-data/dev-db/valkey/", ["valkey-node-0"])
        case["manifest"]["replaces"][0]["compose_path"] = (
            "labs/valkey-cluster/docker-compose.yml"
        )
        case["root"]["by_service"]["valkey-node-0"] = {
            "containers": set(), "ports": set(), "dirs": set()
        }  # fmt: skip
        report = readiness(case)
        self.assertEqual("FAIL", self.result(report, "composition"))
        problems = report["criteria"]["composition"]["problems"]
        self.assertTrue(any("not included by root" in p for p in problems), problems)

    def test_readiness_bad_input_is_a_lab_error(self) -> None:
        case = readiness_case()
        case["manifest"]["resources"]["disk_gib"]["data"] = "lots"
        with self.assertRaises(lab.LabError) as raised:
            readiness(case)
        self.assertEqual(2, raised.exception.code)
        with (
            mock.patch.object(lab, "catalog_ids", side_effect=KeyError("id")),
            self.assertRaises(lab.LabError) as raised,
        ):
            readiness(readiness_case())
        self.assertEqual(2, raised.exception.code)
        with tempfile.TemporaryDirectory() as tmp:
            catalog = pathlib.Path(tmp) / lab.SECRET_CATALOG
            catalog.parent.mkdir(parents=True)
            catalog.write_text(json.dumps({"entries": [{}]}), "utf-8")
            with (
                mock.patch.object(lab, "ROOT", pathlib.Path(tmp)),
                self.assertRaises(lab.LabError),
            ):
                lab.catalog_ids()

    def test_readiness_unknown_profile_fails_composition(self) -> None:
        case = readiness_case()
        case["manifest"]["target"]["profile"] = "no-such-profile"
        report = readiness(case)
        self.assertEqual("FAIL", self.result(report, "composition"))
        self.assertEqual("FAIL", report["result"])

    def test_readiness_old_docker_fails(self) -> None:
        case = readiness_case()
        case["manifest"]["host"] = {"docker": "30.0", "compose": "2.20"}
        report = readiness(case)
        self.assertEqual("FAIL", self.result(report, "docker"))
        self.assertTrue(
            any("30.0" in p for p in report["criteria"]["docker"]["problems"])
        )

    def test_readiness_unmeasured_value_is_not_run(self) -> None:
        case = readiness_case()
        del case["host"]["NCPU"]
        report = readiness(case)
        self.assertEqual("NOT_RUN", self.result(report, "resources"))
        self.assertEqual("NOT_RUN", report["result"])

    def test_readiness_checks_rendered_users(self) -> None:
        for user, expected in (
            # Groups and file modes are an owner check item, not a block.
            ("999:999", "PASS"), ("postgres", "PASS"), ("0", "PASS"),
            ("70000", "FAIL"), ("1000:", "FAIL"),
        ):  # fmt: skip
            with self.subTest(user=user):
                case = readiness_case()
                case["lab"]["users"]["node"] = user
                self.assertEqual(expected, self.result(readiness(case), "linux"))

    def test_measure_host_records_sources_and_omits_failures(self) -> None:
        info = {"NCPU": 12, "MemTotal": 32 * GIB, "DockerRootDir": "/var/lib/docker",
                "ServerVersion": "29.9.2", "CgroupVersion": "2"}  # fmt: skip
        answers = [
            subprocess.CompletedProcess([], 0, json.dumps(info), ""),
            subprocess.CompletedProcess([], 1, "", "no compose"),
        ]
        usage = mock.Mock(free=5 * GIB, total=10 * GIB)
        with (
            mock.patch.object(lab, "run", side_effect=answers) as called,
            mock.patch.object(lab.shutil, "disk_usage", return_value=usage),
        ):
            host = lab.measure_host("docker", "/data/home")
        self.assertEqual(
            ["docker", "info", "--format", "{{json .}}"],
            called.call_args_list[0].args[0],
        )
        self.assertEqual(12, host["NCPU"]["value"])
        self.assertIn("docker info", host["NCPU"]["source"])
        self.assertEqual("2", host["cgroup_version"]["value"])
        self.assertNotIn("compose_version", host)
        self.assertEqual(5 * GIB, host["disk_data"]["value"]["free"])
        self.assertEqual("/var/lib/docker", host["disk_docker"]["value"]["path"])

    def test_readiness_cli_writes_the_report_and_exits_on_result(self) -> None:
        for result, code in (("PASS", 0), ("NOT_RUN", 3), ("FAIL", 3)):
            with (
                self.subTest(result=result),
                tempfile.TemporaryDirectory() as tmp,
                mock.patch.object(lab, "render", return_value=model("p", {})),
                mock.patch.object(lab, "docker_root", return_value="/var/lib/docker"),
                mock.patch.object(
                    lab, "root_footprint", return_value={"home_data_root": "/d"}
                ),
                mock.patch.object(lab, "measure_host", return_value={}),
                mock.patch.object(lab, "running_containers", return_value=[]),
                mock.patch.object(lab, "load_manifest", return_value={}),
                mock.patch.object(
                    lab, "lab_file", return_value="labs/x/docker-compose.yml"
                ),
                mock.patch.object(lab, "readiness", return_value={"result": result}),
                mock.patch("sys.stdout"),
            ):
                path = pathlib.Path(tmp) / "report.json"
                self.assertEqual(
                    code, lab.main(["readiness", "x", "--report", str(path)])
                )
                self.assertEqual(result, json.loads(path.read_text())["result"])

    def test_allowance_matches_policy(self) -> None:
        policy = (
            ROOT / "docs/05.operations/policies/15-labs/0107-lab-promotion.md"
        ).read_text(encoding="utf-8")
        rows = {}
        for line in policy.splitlines():
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if len(cells) == 2 and cells[0] in {"Allowance CPUs", "Allowance MiB"}:
                rows[cells[0]] = float(cells[1])
        self.assertEqual(
            {
                "Allowance CPUs": lab.PROMOTION_EXTERNAL_ALLOWANCE["cpus"],
                "Allowance MiB": lab.PROMOTION_EXTERNAL_ALLOWANCE["memory_mib"],
            },
            rows,
        )

    def test_reserve_matches_policy(self) -> None:
        policy = (
            ROOT / "docs/05.operations/policies/15-labs/0107-lab-promotion.md"
        ).read_text(encoding="utf-8")
        rows = {}
        for line in policy.splitlines():
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if len(cells) == 2 and cells[0] in {"CPUs", "Memory MiB", "Disk percent"}:
                rows[cells[0]] = float(cells[1])
        self.assertEqual(
            {
                "CPUs": lab.PROMOTION_RESERVE["cpus"],
                "Memory MiB": lab.PROMOTION_RESERVE["memory_mib"],
                "Disk percent": lab.PROMOTION_RESERVE["disk_percent"],
            },
            rows,
        )


def _bytes(value: object) -> float:
    """A Compose size such as 256m, 2g or 32M, in bytes."""
    text = str(value).strip().lower()
    units = {"k": 2**10, "m": 2**20, "g": 2**30}
    if text[-1:] in units:
        return float(text[:-1]) * units[text[-1]]
    return float(text.rstrip("b"))


class SharedTemplateTests(unittest.TestCase):
    def test_shared_templates_declare_reservations(self) -> None:
        # SPEC-0263 AC8: every resource anchor and every template that sets
        # limits inline reserves no more than its limit.
        loaded = yaml.safe_load(
            (ROOT / "infra/common-optimizations.yml").read_text(encoding="utf-8")
        )
        blocks = {k: v for k, v in loaded.items() if k.startswith("x-resource-")}
        blocks |= {
            name: spec
            for name, spec in loaded["services"].items()
            if "cpus" in spec or "mem_limit" in spec
        }
        self.assertGreaterEqual(len(blocks), 7)
        for name, block in blocks.items():
            with self.subTest(name=name):
                reserved = block["deploy"]["resources"]["reservations"]
                self.assertGreater(float(reserved["cpus"]), 0)
                self.assertGreater(_bytes(reserved["memory"]), 0)
                self.assertLessEqual(float(reserved["cpus"]), float(block["cpus"]))
                self.assertLessEqual(
                    _bytes(reserved["memory"]), _bytes(block["mem_limit"])
                )


if __name__ == "__main__":
    unittest.main()
