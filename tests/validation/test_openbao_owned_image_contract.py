"""Synthetic trust, ownership, resource and reproducibility guards; no HOME."""

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tarfile
import tempfile
import unittest
from io import BytesIO
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "infra/03-security/openbao/scripts/build-owned-image.py"
spec = importlib.util.spec_from_file_location("owned_openbao_build", SOURCE)
builder = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = builder
spec.loader.exec_module(builder)


class MaterialGuards(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_symlink_never_becomes_a_public_input(self):
        (self.root / "target").write_bytes(b"synthetic")
        (self.root / "link").symlink_to("target")
        with self.assertRaises(builder.Blocked):
            builder.read_regular(self.root / "link", 64)

    def test_multiple_links_refuse_input_role_aliases(self):
        (self.root / "target").write_bytes(b"synthetic")
        os.link(self.root / "target", self.root / "other")
        with self.assertRaises(builder.Blocked):
            builder.read_regular(self.root / "target", 64)

    def test_over_bound_payload_is_not_hashed_or_accepted(self):
        (self.root / "large").write_bytes(b"x" * 65)
        with self.assertRaises(builder.Blocked):
            builder.read_regular(self.root / "large", 64)

    def test_mismatching_material_stops_before_execution(self):
        with self.assertRaises(builder.Blocked):
            builder.require_hash(b"changed", hashlib.sha256(b"expected").hexdigest())

    def test_stable_regular_input_survives_its_own_access_time_update(self):
        path = self.root / "input"
        path.write_bytes(b"public fixture")
        path.chmod(0o600)
        os.utime(path, (1, 1))
        self.assertEqual(b"public fixture", builder.read_regular(path, 64))

    def test_symlink_directory_never_grants_input_access(self):
        (self.root / "real").mkdir()
        (self.root / "real/input").write_bytes(b"public fixture")
        (self.root / "alias").symlink_to("real", target_is_directory=True)
        with self.assertRaises(builder.Blocked):
            builder.read_regular(self.root / "alias/input", 64)

    def test_archive_escape_is_rejected_before_extraction(self):
        archive = self.root / "source.tar"
        with tarfile.open(archive, "w") as out:
            member = tarfile.TarInfo("openbao-dist-v2.7.1/../../outside")
            member.size = 1
            out.addfile(member, BytesIO(b"x"))
        with self.assertRaises(builder.Blocked):
            builder.archive_members(archive, "openbao-dist-v2.7.1", 64)


class ExecutionGuards(unittest.TestCase):
    def test_compile_caps_are_real_and_swap_total_equals_memory(self):
        args = builder.container_limits("compile")
        for flag, value in (
            ("--memory", "4g"),
            ("--memory-swap", "4g"),
            ("--cpus", "2"),
            ("--pids-limit", "128"),
            ("--user", "1000:1000"),
        ):
            self.assertEqual(value, args[args.index(flag) + 1])
        self.assertIn("--read-only", args)
        self.assertEqual("ALL", args[args.index("--cap-drop") + 1])

    def test_ambient_go_configuration_is_explicitly_disabled(self):
        env = builder.go_environment(offline=True)
        self.assertEqual("off", env["GOENV"])
        self.assertEqual("off", env["GOWORK"])
        self.assertEqual("local", env["GOTOOLCHAIN"])
        self.assertEqual("off", env["GOPROXY"])
        self.assertEqual("sum.golang.org", env["GOSUMDB"])
        for key in ("GOPRIVATE", "GONOSUMDB", "GONOPROXY", "GOINSECURE"):
            self.assertEqual("", env[key])

    def test_low_memory_or_disk_never_admits_compile(self):
        for memory, disk in (
            (11 * 1024**3, 40 * 1024**3),
            (14 * 1024**3, 31 * 1024**3),
        ):
            with self.assertRaises(builder.Blocked):
                builder.admit_resources(memory, disk)

    def test_every_oci_identity_must_match_for_reproducibility(self):
        good = {"binary": "a", "config": "b", "layers": ["c"], "manifest": "d"}
        for key in good:
            changed = {**good, key: "different"}
            with self.assertRaises(builder.Blocked):
                builder.require_reproducible(good, changed)

    def test_scratch_creation_does_not_follow_a_symlink_parent(self):
        with tempfile.TemporaryDirectory(prefix="hyhome-p01-owned-build-") as root:
            path = Path(root)
            (path / "alias").symlink_to("/tmp", target_is_directory=True)
            target = path / "alias/new-directory-that-must-not-exist"
            with self.assertRaises(builder.Blocked):
                builder.private_directory(target, create=True)
            self.assertFalse(Path("/tmp/new-directory-that-must-not-exist").exists())

    def test_scratch_dotdot_is_rejected_before_creation(self):
        target = Path("/tmp/hyhome-p01-owned-build-invalid/../outside-owned-attempt")
        with self.assertRaises(builder.Blocked):
            builder.private_directory(target, create=True)
        self.assertFalse(Path("/tmp/outside-owned-attempt").exists())


class ModuleSelectionGuards(unittest.TestCase):
    def test_only_the_authenticated_minimal_selection_may_change(self):
        before = {"Require": [{"Path": "example.org/other", "Version": "v1.0.0"}]}
        after = {"Require": [{"Path": "example.org/other", "Version": "v2.0.0"}]}
        with self.assertRaises(builder.Blocked):
            builder.module_delta(before, after)

    def test_go_directives_and_replace_edges_cannot_change(self):
        for key in ("Go", "Replace", "Exclude"):
            before = {key: "original", "Require": []}
            after = {key: "changed", "Require": []}
            with self.assertRaises(builder.Blocked):
                builder.module_delta(before, after)

    def test_duplicate_module_rows_are_not_silently_collapsed(self):
        rows = [{"Path": "golang.org/x/net", "Version": "v0.60.0"}] * 2
        with self.assertRaises(builder.Blocked):
            builder.module_delta({"Require": []}, {"Require": rows})


class DockerBoundaryGuards(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="hyhome-p01-owned-build-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.docker = builder.LocalDocker(self.root)

    def valid_inspection(self):
        return {
            "HostConfig": {
                "Memory": 4 * 1024**3,
                "MemorySwap": 4 * 1024**3,
                "NanoCpus": 2000000000,
                "PidsLimit": 128,
                "NetworkMode": "none",
                "ReadonlyRootfs": True,
                "Privileged": False,
                "CapDrop": ["ALL"],
                "CapAdd": None,
                "SecurityOpt": ["no-new-privileges"],
                "Tmpfs": {"/tmp": "rw,nosuid,nodev,noexec,size=128m,mode=1777"},
            },
            "Config": {"User": "1000:1000"},
            "Mounts": [],
        }

    def test_real_created_caps_must_match_before_start(self):
        for key, value in (
            ("Memory", 0),
            ("MemorySwap", -1),
            ("NanoCpus", 0),
            ("Privileged", True),
            ("NetworkMode", "bridge"),
            ("CapAdd", ["SYS_ADMIN"]),
        ):
            row = self.valid_inspection()
            row["HostConfig"][key] = value
            with mock.patch.object(
                self.docker, "captured", return_value=json.dumps([row]).encode()
            ):
                with self.assertRaises(builder.Blocked):
                    self.docker.created_boundary("a" * 64, "compile", [])

    def test_undeclared_host_socket_mount_is_refused(self):
        row = self.valid_inspection()
        row["Mounts"] = [
            {
                "Source": "/var/run/docker.sock",
                "Destination": "/socket",
                "RW": True,
                "Type": "bind",
            }
        ]
        with mock.patch.object(
            self.docker, "captured", return_value=json.dumps([row]).encode()
        ):
            with self.assertRaises(builder.Blocked):
                self.docker.created_boundary("a" * 64, "compile", [])

    def test_expected_prestart_tmpfs_and_only_optional_tmp_mount_are_accepted(self):
        for extra in (
            [],
            [
                {
                    "Type": "tmpfs",
                    "Source": "",
                    "Destination": "/tmp",
                    "Mode": "",
                    "RW": True,
                    "Propagation": "",
                }
            ],
        ):
            row = self.valid_inspection()
            row["Mounts"] = extra
            with mock.patch.object(
                self.docker, "captured", return_value=json.dumps([row]).encode()
            ):
                self.docker.created_boundary("a" * 64, "compile", [])

    def test_missing_extra_or_weakened_tmpfs_is_refused(self):
        for tmpfs in (
            None,
            {},
            {"/tmp": "rw,nosuid,nodev,exec,size=128m,mode=1777"},
            {"/tmp": "rw,nosuid,nodev,noexec,size=1g,mode=1777"},
            {"/tmp": "rw,nosuid,nodev,noexec,size=128m,mode=1777", "/extra": "rw"},
        ):
            row = self.valid_inspection()
            row["HostConfig"]["Tmpfs"] = tmpfs
            with mock.patch.object(
                self.docker, "captured", return_value=json.dumps([row]).encode()
            ):
                with self.assertRaises(builder.Blocked):
                    self.docker.created_boundary("a" * 64, "compile", [])

    def test_tmpfs_view_cannot_hide_extra_mounts_or_flags(self):
        for extra in (
            [{"Type": "tmpfs", "Destination": "/private", "RW": True}],
            [{"Type": "tmpfs", "Destination": "/tmp", "RW": True, "Mode": "exec"}],
            [{"Type": "tmpfs", "Destination": "/tmp", "RW": False}],
            [{"Type": "volume", "Destination": "/tmp", "RW": True}],
        ):
            row = self.valid_inspection()
            row["Mounts"] = extra
            with mock.patch.object(
                self.docker, "captured", return_value=json.dumps([row]).encode()
            ):
                with self.assertRaises(builder.Blocked):
                    self.docker.created_boundary("a" * 64, "compile", [])

    def test_invalid_mount_never_reaches_docker_create(self):
        newline = self.root / "public\ninjected"
        newline.mkdir()
        for number, source in enumerate((Path("/var/run/docker.sock"), newline)):
            with (
                mock.patch.object(
                    self.docker, "captured", return_value=b"a" * 64
                ) as capture,
                mock.patch.object(
                    self.docker,
                    "created_boundary",
                    side_effect=AssertionError("unsafe create"),
                ),
            ):
                with self.assertRaises(builder.Blocked):
                    self.docker.container(
                        f"invalid-{number}",
                        "compile",
                        "synthetic",
                        "true",
                        [(source, "/out", True)],
                        {},
                    )
                capture.assert_not_called()


class SelectedOciGuards(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = ROOT / "infra/03-security/openbao/build/owned_image_oci.py"
        spec = importlib.util.spec_from_file_location("selected_openbao_oci", path)
        cls.oci = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.oci)

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def export(self, name, rows):
        target = self.root / name
        with tarfile.open(target, "w") as out:
            for path, payload, stamp in rows:
                item = tarfile.TarInfo(path)
                item.size, item.mtime, item.mode = len(payload), stamp, 0o555
                item.uid, item.gid = 100, 1000
                out.addfile(item, BytesIO(payload))
        target.chmod(0o600)
        return target

    def test_order_and_transient_times_do_not_change_layer_identity(self):
        first = self.export(
            "first.tar",
            [("usr/bin/bao", b"public", 1), ("licenses/mozilla.txt", b"license", 2)],
        )
        second = self.export(
            "second.tar",
            [("licenses/mozilla.txt", b"license", 80), ("usr/bin/bao", b"public", 90)],
        )
        a = self.oci.canonical_layer(first, self.root / "a.tar", 123, 1024**2)
        b = self.oci.canonical_layer(second, self.root / "b.tar", 123, 1024**2)
        self.assertEqual(a, b)
        self.assertEqual(
            (self.root / "a.tar").read_bytes(), (self.root / "b.tar").read_bytes()
        )

    def test_export_traversal_never_enters_an_image(self):
        source = self.export("bad.tar", [("../private", b"x", 1)])
        with self.assertRaises(self.oci.InvalidImage):
            self.oci.canonical_layer(source, self.root / "out.tar", 123, 1024**2)

    def test_export_duplicates_are_refused(self):
        source = self.export("bad.tar", [("usr/bin/bao", b"x", 1)] * 2)
        with self.assertRaises(self.oci.InvalidImage):
            self.oci.canonical_layer(source, self.root / "out.tar", 123, 1024**2)

    def test_destination_is_exclusive_and_preserves_prior_receipts(self):
        source = self.export("input.tar", [("usr/bin/bao", b"x", 1)])
        dest = self.root / "prior.tar"
        dest.write_bytes(b"prior receipt")
        with self.assertRaises(self.oci.InvalidImage):
            self.oci.canonical_layer(source, dest, 123, 1024**2)
        self.assertEqual(b"prior receipt", dest.read_bytes())

    def test_recipe_cannot_add_unreviewed_downloads_or_private_context(self):
        for instruction in (
            "ADD https://example.invalid/code /bin/code",
            "COPY ../../../.ssh/id_ed25519 /root/key",
            "ENV BAO_TOKEN=synthetic-value",
        ):
            with self.assertRaises(self.oci.InvalidImage):
                self.oci.runtime_recipe(instruction, "synthetic")

    def test_links_preserve_internal_alpine_paths_and_reject_root_escape(self):
        for link, accepted in (
            ("../../lib/libc.so", True),
            ("/lib/libc.so", True),
            ("/../../private", False),
            ("../../../private", False),
        ):
            target = self.root / (
                "link-" + str(accepted) + "-" + str(len(link)) + ".tar"
            )
            with tarfile.open(target, "w") as archive:
                item = tarfile.TarInfo("usr/lib/alias")
                item.type, item.linkname = tarfile.SYMTYPE, link
                archive.addfile(item)
            target.chmod(0o600)
            with tarfile.open(target) as archive:
                if accepted:
                    self.assertEqual(1, len(self.oci.export_rows(archive, 1024)))
                else:
                    with self.assertRaises(self.oci.InvalidImage):
                        self.oci.export_rows(archive, 1024)

    def test_oci_graph_bytes_are_complete_and_stable(self):
        layer = self.export("layer.tar", [("usr/bin/bao", b"public", 1)])
        config = {"architecture": "amd64", "os": "linux", "config": {"User": "openbao"}}
        first = self.oci.image_archive(
            layer, self.root / "first", config, "hy-home/openbao:synthetic", 123
        )
        second = self.oci.image_archive(
            layer, self.root / "second", config, "hy-home/openbao:synthetic", 123
        )
        self.assertEqual(
            {k: first[k] for k in ("config", "layers", "manifest")},
            {k: second[k] for k in ("config", "layers", "manifest")},
        )
        with tarfile.open(first["archive"]) as archive:
            names = archive.getnames()
            self.assertIn("oci-layout", names)
            self.assertIn("index.json", names)
            self.assertEqual(5, len(names))


class PipelineProof(unittest.TestCase):
    """Exercise the selected pipeline without Docker or compilation."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="hyhome-p01-owned-build-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.build = ROOT / "infra/03-security/openbao/build"
        self.inputs = builder.build_inputs(self.build)

    def binary(self, output):
        raw = bytearray(64)
        raw[:6] = b"\x7fELF\x02\x01"
        raw[18:20] = (62).to_bytes(2, "little")
        raw[54:56] = (56).to_bytes(2, "little")
        (output / "bao").write_bytes(raw)
        (output / "build-info.txt").write_text(
            "/out/bao: go1.27.2\n\tdep\tgolang.org/x/net\tv0.60.0\n"
        )
        return hashlib.sha256(raw).hexdigest()

    def test_compile_uses_empty_cache_and_readonly_materials(self):
        docker = mock.Mock()
        docker.container.side_effect = lambda *a, **kw: self.binary(self.root / "pass")
        identity = builder.compile_pass(
            docker, self.root, self.root / "pass", self.inputs, 1
        )
        self.assertEqual(64, len(identity["binary"]))
        self.assertEqual(
            [],
            [
                path
                for path in (self.root / "pass/cache").iterdir()
                if path.name != "tmp"
            ],
        )
        args = docker.container.call_args.args
        self.assertTrue(all(row[2] for row in args[4][:2]))
        self.assertEqual("off", args[5]["GOPROXY"])
        (self.root / "pass/build-info.txt").write_text("/out/bao: go1.27.1\n")
        with self.assertRaises(builder.Blocked):
            builder.verify_binary(
                self.root / "pass/bao", self.root / "pass/build-info.txt", self.inputs
            )

    def test_go_workspace_uses_fresh_directory_on_existing_writable_cache_mount(self):
        docker = mock.Mock()
        workspaces = []

        def compile_with_workspace(label, phase, image, command, mounts, environment):
            cache_mount = next(row for row in mounts if row[1] == "/cache")
            self.assertFalse(cache_mount[2])
            self.assertEqual("/cache/tmp", environment.get("GOTMPDIR"))
            workspace = cache_mount[0] / environment["GOTMPDIR"].removeprefix("/cache/")
            self.assertTrue(workspace.is_dir())
            self.assertEqual(0o700, workspace.stat().st_mode & 0o777)
            self.assertEqual([], list(workspace.iterdir()))
            (workspace / "synthetic-go-work").write_bytes(b"temporary build data")
            workspaces.append(workspace)
            self.binary(next(row[0] for row in mounts if row[1] == "/out"))

        docker.container.side_effect = compile_with_workspace
        for number in (1, 2):
            builder.compile_pass(
                docker, self.root, self.root / f"pass-{number}", self.inputs, number
            )
        self.assertNotEqual(workspaces[0], workspaces[1])

    def test_runtime_recipe_prevents_actual_apk_wallclock_repro_regression(self):
        # Reduced suffixes from the two failed R4 exported var/log/apk.log files.
        clocks = iter(("2026-10-14 02:27:16", "2026-10-14 02:36:35"))

        def synthetic_export(*args, export, **kwargs):
            clock = next(clocks)
            rows = [("usr/bin/bao", b"bao")]
            if "apk --no-logfile" not in args[3]:
                rows.append(
                    ("var/log/apk.log", f"Running apk add at {clock}\\n".encode())
                )
            with tarfile.open(export, "w") as archive:
                for name, data in rows:
                    item = tarfile.TarInfo(name)
                    item.mode, item.size = 0o555, len(data)
                    archive.addfile(item, BytesIO(data))

        docker = mock.Mock()
        docker.container.side_effect = synthetic_export
        identities = []
        for number in (1, 2):
            output = self.root / f"runtime-{number}"
            output.mkdir()
            self.binary(output)
            identities.append(
                builder.runtime_pass(
                    docker,
                    self.root,
                    output,
                    self.inputs,
                    (self.build / "Dockerfile").read_text(),
                    builder.load_oci(self.build),
                    number,
                    {},
                )
            )
        for key in ("config", "layers", "manifest"):
            self.assertEqual(identities[0][key], identities[1][key])
        args = docker.container.call_args.args
        self.assertIn("--keys-dir /public/keys verify", args[3])
        self.assertTrue(all(row[2] for row in args[4]))
        self.assertEqual(
            str(self.inputs["source_date_epoch"]), args[5]["SOURCE_DATE_EPOCH"]
        )

    def test_recipe_shadow_epoch_changes_only_locked_new_account_day(self):
        recipe = (self.build / "Dockerfile").read_text()
        self.assertIn(" && awk -F:", recipe)
        clause = "awk -F:" + recipe.split(" && awk -F:", 1)[1].split(" && ln -s", 1)[0]
        shadow = self.root / "shadow"
        clause = clause.replace("/etc/shadow", str(shadow))
        original = "root:!:20000:0:99999:7:::\nopenbao:!:20999:0:99999:7:::\nother:*:111:2:30:3:4:5:6\n"
        for epoch in (
            self.inputs["source_date_epoch"],
            self.inputs["source_date_epoch"] + 3 * 86400,
        ):
            shadow.write_text(original)
            shadow.chmod(0o600)
            result = subprocess.run(
                ["/bin/sh", "-ec", clause],
                check=False,
                capture_output=True,
                env={"PATH": "/usr/bin:/bin", "SOURCE_DATE_EPOCH": str(epoch)},
            )
            self.assertEqual(0, result.returncode)
            expected = original.replace(
                "openbao:!:20999:", f"openbao:!:{epoch // 86400}:"
            )
            self.assertEqual(expected, shadow.read_text())
            self.assertEqual(0o600, shadow.stat().st_mode & 0o777)
        for bad in (
            original.replace("openbao:!:", "openbao:unlocked:"),
            original.replace("openbao", "different"),
            original + "openbao:*:1:2:3:4:5:6:7\n",
        ):
            shadow.write_text(bad)
            result = subprocess.run(
                ["/bin/sh", "-ec", clause],
                check=False,
                capture_output=True,
                env={"PATH": "/usr/bin:/bin", "SOURCE_DATE_EPOCH": "1790861574"},
            )
            self.assertNotEqual(0, result.returncode)
            self.assertEqual(bad, shadow.read_text())

    def test_two_independent_passes_and_changed_material_stop(self):
        image = {"config": "c", "layers": ["l"], "manifest": "m"}
        with (
            mock.patch.object(builder, "materials", return_value={}),
            mock.patch.object(builder, "LocalDocker"),
            mock.patch.object(builder, "host_headroom"),
            mock.patch.object(
                builder, "compile_pass", return_value={"binary": "b"}
            ) as compile_phase,
            mock.patch.object(
                builder, "runtime_pass", return_value=image
            ) as runtime_phase,
        ):
            result = builder.run_build(
                self.root,
                "synthetic",
                self.root / "result",
                self.build,
                self.inputs,
                builder.current_packet(ROOT),
            )
            self.assertEqual("PASS", result["status"])
            self.assertEqual(2, compile_phase.call_count)
            self.assertEqual(2, runtime_phase.call_count)
        with (
            mock.patch.object(
                builder, "materials", side_effect=[{}, {"changed": True}]
            ),
            mock.patch.object(builder, "LocalDocker"),
            mock.patch.object(builder, "host_headroom"),
            mock.patch.object(builder, "compile_pass", return_value={"binary": "b"}),
            mock.patch.object(builder, "runtime_pass") as runtime_phase,
        ):
            with self.assertRaises(builder.Blocked):
                builder.run_build(
                    self.root,
                    "synthetic",
                    self.root / "refused",
                    self.build,
                    self.inputs,
                    builder.current_packet(ROOT),
                )
            runtime_phase.assert_not_called()

    def test_failed_inspection_removes_only_created_container_before_start(self):
        docker = builder.LocalDocker(self.root)
        cid = "a" * 64
        with (
            mock.patch.object(
                docker, "captured", side_effect=[cid.encode(), b""]
            ) as capture,
            mock.patch.object(
                docker, "created_boundary", side_effect=builder.Blocked("refused")
            ),
            mock.patch.object(builder.subprocess, "run") as launch,
        ):
            with self.assertRaises(builder.Blocked):
                docker.container(
                    "refused", "compile", self.inputs["builder"], "synthetic", [], {}
                )
            launch.assert_not_called()
            self.assertEqual(["rm", "--force", cid], capture.call_args.args[0])
        self.assertEqual(
            "FAIL",
            json.loads((self.root / "refused-receipt.json").read_text())["status"],
        )

    def test_actual_exit_and_image_identity_are_recorded(self):
        docker = builder.LocalDocker(self.root)
        row = {
            "Id": self.inputs["builder"].split("@")[1],
            "Os": "linux",
            "Architecture": "amd64",
            "Config": {},
        }
        with mock.patch.object(
            docker, "captured", return_value=json.dumps([row]).encode()
        ):
            self.assertEqual(row, docker.image(self.inputs["builder"]))
        state = {"ExitCode": 0, "OOMKilled": False}
        with (
            mock.patch.object(
                docker,
                "captured",
                side_effect=[b"b" * 64, json.dumps(state).encode(), b""],
            ),
            mock.patch.object(docker, "created_boundary"),
            mock.patch.object(
                docker, "attached", return_value=SimpleNamespace(returncode=0)
            ),
        ):
            docker.container(
                "success",
                "compile",
                self.inputs["builder"],
                "synthetic",
                [(self.root, "/out", False)],
                {"GOENV": "off"},
            )
        self.assertEqual(
            "PASS",
            json.loads((self.root / "success-receipt.json").read_text())["status"],
        )
        with mock.patch.object(
            builder.subprocess,
            "run",
            return_value=SimpleNamespace(returncode=1, stdout=b"", stderr=b""),
        ):
            with self.assertRaises(builder.Blocked):
                docker.captured(["synthetic"])
            with self.assertRaises(builder.Blocked):
                docker.streamed(["synthetic"], self.root / "stream", 64, 1)

    def test_plan_is_readonly_and_changed_packet_prevents_launch(self):
        argv = [
            "--materials-directory",
            str(self.root),
            "--materials-sha256",
            "synthetic",
            "--output-directory",
            str(self.root / "unused"),
            "--packet-sha256",
            builder.current_packet(ROOT),
        ]
        with (
            mock.patch.object(builder, "materials", return_value={}),
            mock.patch("builtins.print"),
        ):
            self.assertEqual(0, builder.main(argv))
            self.assertFalse((self.root / "unused").exists())
            self.assertEqual(1, builder.main([*argv[:-1], "changed"]))

    def test_every_frozen_material_digest_is_checked(self):
        for name in ("source", "modules", "apks", "keys", "proof"):
            (self.root / name).mkdir()
        (self.root / "source/go.mod").write_bytes(b"module")
        (self.root / "source/go.sum").write_bytes(b"sums")
        (self.root / "keys/key.pub").write_bytes(b"public key")
        proof = self.root / "proof"
        (proof / "source.tar.xz").write_bytes(b"archive")
        receipt = b'{"status":"PASS","exit":0}'
        for name in ("builder", "source_checksums"):
            (proof / (name + "-receipt.json")).write_bytes(receipt)
        for name in ("main", "community"):
            (proof / (name + "-APKINDEX.tar.gz")).write_bytes(b"signed index")
        for path in self.root.rglob("*"):
            if path.is_file():
                path.chmod(0o600)
        inputs = {
            **self.inputs,
            "apk_closure": [],
            "alpine_key_sha256": hashlib.sha256(b"public key").hexdigest(),
            "source_archive_sha256": hashlib.sha256(b"archive").hexdigest(),
            "publisher_receipts": {
                name: hashlib.sha256(receipt).hexdigest()
                for name in ("builder", "source_checksums")
            },
            "apk_indexes": {
                name: hashlib.sha256(b"signed index").hexdigest()
                for name in ("main", "community")
            },
        }
        document = {
            name + "_files": builder.file_manifest(self.root / name)
            for name in ("source", "modules", "apks", "keys", "proof")
        }
        document.update(
            source_archive_sha256=inputs["source_archive_sha256"],
            go_patch_sha256=inputs["go_patch_sha256"],
            offline_module_verification="PASS",
            signed_apk_verification="PASS",
            go_mod_sha256=hashlib.sha256(b"module").hexdigest(),
            go_sum_sha256=hashlib.sha256(b"sums").hexdigest(),
        )
        builder.exclusive_json(self.root / "materials.json", document)
        digest = hashlib.sha256((self.root / "materials.json").read_bytes()).hexdigest()
        self.assertEqual(document, builder.materials(self.root, digest, inputs))
        (self.root / "source/go.sum").write_bytes(b"changed")
        with self.assertRaises(builder.Blocked):
            builder.materials(self.root, digest, inputs)

    def test_mount_parser_rejects_socket_and_mount_option_injection_before_create(self):
        docker = builder.LocalDocker(self.root)
        for source, target in (
            (Path("/var/run/docker.sock"), "/out"),
            (self.root / "file,readonly=false", "/out"),
            (self.root, "/private"),
        ):
            with self.assertRaises(builder.Blocked):
                docker.admitted_mounts("compile", [(source, target, True)])

    def test_attached_process_stops_at_scratch_budget_and_preserves_failure(self):
        docker = builder.LocalDocker(self.root)
        process = mock.Mock()
        process.poll.side_effect = [None, None]
        process.wait.return_value = 0
        with (
            mock.patch.object(builder.subprocess, "Popen", return_value=process),
            mock.patch.object(
                builder.shutil, "disk_usage", return_value=SimpleNamespace(free=0)
            ),
        ):
            with self.assertRaises(builder.Blocked):
                docker.attached("synthetic", mock.Mock(), mock.Mock(), 1)
        process.terminate.assert_called_once()

    def test_attached_success_observes_real_process_exit(self):
        docker = builder.LocalDocker(self.root)
        process = mock.Mock()
        process.poll.side_effect = [None, 0, 0]
        process.wait.return_value = 0
        with (
            mock.patch.object(builder.subprocess, "Popen", return_value=process),
            mock.patch.object(
                builder.shutil,
                "disk_usage",
                return_value=SimpleNamespace(free=32 * 1024**3),
            ),
        ):
            self.assertIs(
                process, docker.attached("synthetic", mock.Mock(), mock.Mock(), 1)
            )
        process.terminate.assert_not_called()

    def test_json_and_module_metadata_guards(self):
        for payload in (b'{"a":1,"a":2}', b'{"a":NaN}', b"broken"):
            with self.assertRaises(builder.Blocked):
                builder.decode_json(payload)
        with self.assertRaises(builder.Blocked):
            builder.container_limits("unknown")
        builder.container_limits("prefetch")
        builder.admit_resources(12 * 1024**3, 32 * 1024**3)
        with mock.patch.object(builder, "admit_resources") as guard:
            builder.host_headroom(self.root)
            guard.assert_called_once()
        before = {
            "Require": [
                {"Path": name, "Version": v[0]} for name, v in builder.SELECTION.items()
            ]
        }
        after = {
            "Require": [
                {"Path": name, "Version": v[1]} for name, v in builder.SELECTION.items()
            ]
        }
        self.assertEqual(self.inputs["modules"], builder.module_delta(before, after))


if __name__ == "__main__":
    unittest.main()
