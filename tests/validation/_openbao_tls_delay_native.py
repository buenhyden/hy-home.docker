"""Bounded real-Docker TLS probe mechanics; no Native work runs on import."""

import hashlib
import json
import os
import re
import signal
import stat
import subprocess
import sys
import threading
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "infra/03-security/openbao/scripts/check-tls-material.sh"
IMAGE = "hy-home/openbao:2.7.1-go1.27.3-net0.60.0-r1@sha256:a58fb1109971e506e9de1a360aec48ae07af7b6ccf409f8bac329e30e8fde8c8"

READ_SCRIPT = 'for f in /tls/ca.pem /tls/server.pem /tls/server-key.pem; do [ -r "$f" ] && [ -s "$f" ] || exit 1; done'
EVENT_ACTIONS = ("create", "start", "die", "destroy")
NATIVE_RESOURCES = [
    "--memory=32m",
    "--memory-swap=32m",
    "--cpus=0.25",
    "--pids-limit=16",
]


def _native_regular(path, mode, uid):
    info = path.lstat()
    if (
        not stat.S_ISREG(info.st_mode)
        or stat.S_IMODE(info.st_mode) != mode
        or info.st_uid != uid
        or path.resolve() != path
    ):
        raise ValueError("fixture or tracking file identity differs")
    return info


def _native_cid(tracking, expected=None):
    path = tracking / "cid"
    try:
        info = _native_regular(path, 0o600, os.getuid())
    except FileNotFoundError:
        return None
    with os.fdopen(os.open(path, os.O_RDONLY | os.O_NOFOLLOW), "rb") as stream:
        if os.fstat(stream.fileno()) != info:
            raise ValueError("source CID file changed during read")
        raw = stream.read(66)
    if not raw and expected is None:
        return None
    if not re.fullmatch(rb"[a-f0-9]{64}\n?", raw):
        raise ValueError("source CID is malformed")
    cid = raw.decode().rstrip("\n")
    if expected is not None and cid != expected:
        raise ValueError("source CID differs from observed container")
    return cid


def _native_run_argv(material, tracking):
    name, label = tracking.name, "hyhome.openbao.tls-probe=" + tracking.name
    identity = ["run", "--rm", "--cidfile", str(tracking / "cid")]
    ownership = ["--name", name, "--label", label]
    bounds = (
        "--pull=never --network=none --user=100:1000 --read-only "
        "--cap-drop=ALL --security-opt=no-new-privileges"
    ).split()
    mounts = [
        value
        for name in ("ca.pem", "server.pem", "server-key.pem")
        for value in (
            "--mount",
            f"type=bind,src={material / name},dst=/tls/{name},readonly",
        )
    ]
    command = ["--entrypoint", "/bin/sh", IMAGE, "-c", READ_SCRIPT]
    return identity + ownership + bounds + mounts + command


def _native_validate_run(argv, material, uid):
    if len(argv) != 25 or argv[2:3] != ["--cidfile"]:
        raise ValueError("native argument count or cidfile position differs")
    tracking = Path(argv[3]).parent
    if tracking.parent != Path("/tmp") or not re.fullmatch(
        r"openbao-tls\.[A-Za-z0-9]{10}", tracking.name
    ):
        raise ValueError("tracking directory is outside the source namespace")
    info = tracking.lstat()
    if (
        not stat.S_ISDIR(info.st_mode)
        or stat.S_IMODE(info.st_mode) != 0o700
        or info.st_uid != uid
        or tracking.resolve() != tracking
    ):
        raise ValueError("tracking directory identity differs")
    _native_regular(tracking / "identity", 0o600, uid)
    expected = f"{tracking.name}\nhyhome.openbao.tls-probe={tracking.name}\n"
    if (tracking / "identity").read_text() != expected:
        raise ValueError("tracking identity differs")
    if (tracking / "cid").exists() or (tracking / "cid").is_symlink():
        raise ValueError("cidfile already exists")
    for name in ("ca.pem", "server.pem", "server-key.pem"):
        _native_regular(
            material / name, 0o640 if name == "server-key.pem" else 0o644, uid
        )
    if argv != _native_run_argv(material, tracking):
        raise ValueError("native command differs from the complete source argv")
    return tracking


def _native_write(path, value):
    pending = path.with_suffix(".pending")
    pending.write_text(json.dumps(value, sort_keys=True) + "\n")
    pending.chmod(0o600)
    pending.replace(path)


def _native_read(path):
    _native_regular(path, 0o600, os.getuid())
    return json.loads(path.read_text())


def _native_environment(directory):
    info = directory.lstat()
    if (
        directory.resolve() != directory
        or not stat.S_ISDIR(info.st_mode)
        or stat.S_IMODE(info.st_mode) != 0o700
        or info.st_uid != os.getuid()
        or any(directory.iterdir())
    ):
        raise ValueError("Docker config must be an owned empty private directory")
    return {
        **{
            key: value
            for key, value in os.environ.items()
            if not key.startswith("DOCKER_")
        },
        "DOCKER_CONFIG": str(directory),
    }


def _native_call(docker, argv, deadline=None, config_dir=None):
    if docker != "/usr/bin/docker" or Path(docker).resolve() != Path(docker):
        raise ValueError("only the verified /usr/bin/docker executable is admitted")
    remaining = 8 if deadline is None else min(8, deadline - time.monotonic())
    if remaining <= 0:
        raise TimeoutError("Native case deadline exhausted")
    return subprocess.run(
        [docker, "--context", "default", *argv],
        capture_output=True,
        env=_native_environment(Path(config_dir)),
        timeout=remaining,
        check=False,
    )


def _native_listing(name):
    return [
        *"container ls --all --quiet --no-trunc".split(),
        "--filter",
        "name=^/" + name + "$",
        "--filter",
        "label=hyhome.openbao.tls-probe=" + name,
    ]


def _native_container_identity(container, config, intent):
    host = container["HostConfig"]
    actual = container["Config"]
    expected_mounts = sorted(
        (str(Path(config["material"]) / name), "/tls/" + name, False, "bind")
        for name in ("ca.pem", "server.pem", "server-key.pem")
    )
    mounts = sorted(
        (item["Source"], item["Destination"], item["RW"], item["Type"])
        for item in container["Mounts"]
    )
    if (
        container["Name"] != "/" + intent["name"]
        or container["Image"] != config["image_id"]
        or actual["Image"] != IMAGE
        or actual["Labels"].get("hyhome.openbao.tls-probe") != intent["name"]
        or actual["User"] != "100:1000"
        or actual["Entrypoint"] != ["/bin/sh"]
        or actual["Cmd"] != ["-c", _native_payload(config["delay"])]
        or mounts != expected_mounts
        or actual.get("Volumes")
        or not host["ReadonlyRootfs"]
        or host["Privileged"]
        or host.get("CapAdd")
        or host["CapDrop"] != ["ALL"]
        or host["SecurityOpt"] != ["no-new-privileges"]
        or host["NetworkMode"] != "none"
        or host.get("PortBindings")
        or host.get("ExtraHosts")
        or host["Memory"] != 33554432
        or host["MemorySwap"] != 33554432
        or host["NanoCpus"] != 250000000
        or host["PidsLimit"] != 16
        or host["RestartPolicy"]["Name"] != "no"
        or not host["AutoRemove"]
        or host.get("PidMode")
        or host.get("Tmpfs")
    ):
        raise ValueError("observed native container identity or limits differ")
    if not re.fullmatch(r"[a-f0-9]{64}", container["Id"]):
        raise ValueError("observed container ID is invalid")


def _native_private_config(path, config):
    root = path.parent
    info = root.lstat()
    if (
        root.parent != Path("/tmp")
        or not root.name.startswith("hyhome-b3-native-")
        or root.resolve() != root
        or not stat.S_ISDIR(info.st_mode)
        or stat.S_IMODE(info.st_mode) != 0o700
        or info.st_uid != os.getuid()
    ):
        raise ValueError("Native fixture root identity differs")
    material = root / "tls"
    info = material.lstat()
    if (
        config["material"] != str(material)
        or material.resolve() != material
        or not stat.S_ISDIR(info.st_mode)
        or stat.S_IMODE(info.st_mode) != 0o750
        or info.st_uid != os.getuid()
        or info.st_gid != 1000
    ):
        raise ValueError("Native material directory identity differs")
    for key, name in (
        ("intent", "intent.json"),
        ("cleanup_log", "cleanup.jsonl"),
        ("registration", "registration.json"),
        ("dispatch_result", "dispatch-result.json"),
        ("docker_config", "docker-config"),
    ):
        if config[key] != str(root / name):
            raise ValueError("Native control path differs")
    if config["docker"] != "/usr/bin/docker" or Path(
        config["docker"]
    ).resolve() != Path("/usr/bin/docker"):
        raise ValueError("only the verified /usr/bin/docker executable is admitted")


def _native_payload(scenario):
    payloads = {
        25: f"sleep 25; {READ_SCRIPT}",
        61: f"sleep 61; {READ_SCRIPT}",
        "error": "sleep 2; exit 17",
        "kill": f"sleep 120; {READ_SCRIPT}",
        "late": f"sleep 30; {READ_SCRIPT}",
    }
    if scenario not in payloads:
        raise ValueError("Native scenario is not admitted")
    return payloads[scenario]


def _native_release_allowed(code, stdout, tracking, list_code, listed):
    if (
        code == 0
        or b"cleanup=pending-reconciliation" not in stdout
        or not tracking
        or list_code != 0
        or listed.strip()
    ):
        raise ValueError("late dispatch release lacks every required witness")


def _native_control(fd):
    try:
        info = os.fstat(fd)
        if fd < 3 or not stat.S_ISFIFO(info.st_mode) or info.st_uid != os.getuid():
            raise ValueError("dispatch control is not an owned inherited pipe")
        if os.read(fd, 17) != b"release\n" or os.read(fd, 1):
            raise ValueError("dispatch requires one exact release followed by EOF")
    finally:
        os.close(fd)


def _native_delayed(argv, scenario, detached=False):
    position = argv.index(IMAGE)
    return [
        *argv[:position],
        *NATIVE_RESOURCES,
        *(["--detach"] if detached else []),
        *argv[position:-1],
        _native_payload(scenario),
    ]


def _native_dispatch(config_path, control_fd):
    if os.getpid() != os.getpgrp() or os.getsid(0) != os.getpid():
        raise ValueError("dispatch helper must own its new process session")
    config = _native_read(Path(config_path))
    _native_private_config(Path(config_path), config)
    if os.environ.get("DOCKER_HOST"):
        raise ValueError("dispatch Docker host override is not admitted")
    _native_control(control_fd)
    registration = _native_read(Path(config["registration"]))
    if config["delay"] != "late" or registration["config"] != str(config_path):
        raise ValueError("dispatch registration differs")
    argv = registration["argv"]
    tracking = _native_validate_run(argv, Path(config["material"]), os.getuid())
    intent = _native_read(Path(config["intent"]))
    if str(tracking) != registration["tracking"] or intent != {
        "name": tracking.name,
        "tracking": str(tracking),
    }:
        raise ValueError("dispatch registration differs from original source intent")
    attempt = Path(config["registration"]).with_suffix(".dispatched")
    fd = os.open(attempt, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    os.close(fd)
    result_path = Path(config["dispatch_result"])
    try:
        result = _native_call(
            config["docker"],
            _native_delayed(argv, "late", True),
            config["deadline"],
            config["docker_config"],
        )
        cid = result.stdout.decode().strip()
        if result.returncode or not re.fullmatch(r"[a-f0-9]{64}", cid):
            raise RuntimeError("dispatch did not return a definitive successful CID")
        _native_write(
            result_path,
            {
                "result": "DISPATCHED",
                "cid": cid,
                "exit_code": result.returncode,
                "at": time.time(),
            },
        )
    except BaseException as error:
        _native_write(result_path, {"result": "INDETERMINATE", "error": str(error)})
        raise


def _native_docker_wrapper(argv, config_path):
    config = _native_read(Path(config_path))
    if os.environ.get("DOCKER_HOST") or config["delay"] not in (
        25,
        61,
        "error",
        "kill",
        "late",
    ):
        raise ValueError("native context or delay is not admitted")
    if argv[:1] == ["run"]:
        tracking = _native_validate_run(argv, Path(config["material"]), os.getuid())
        _native_private_config(Path(config_path), config)
        _native_write(
            Path(config["intent"]), {"name": tracking.name, "tracking": str(tracking)}
        )
        if config["delay"] == "late":
            _native_write(
                Path(config["registration"]),
                {"argv": argv, "tracking": str(tracking), "config": str(config_path)},
            )
            while True:
                signal.pause()  # The real source timeout terminates this registered client.
        delayed = _native_delayed(argv, config["delay"])
        os.execve(
            config["docker"],
            [config["docker"], "--context", "default", *delayed],
            _native_environment(Path(config["docker_config"])),
        )
    _native_wrapper_cleanup(argv, config)


def _native_wrapper_cleanup(argv, config):
    intent = _native_read(Path(config["intent"]))
    if argv != _native_listing(intent["name"]):
        if (
            len(argv) != 4
            or argv[:3] != ["container", "rm", "--force"]
            or not re.fullmatch(r"[a-f0-9]{64}", argv[3])
        ):
            raise ValueError("source cleanup command is not admitted")
        inspected = _native_call(
            config["docker"],
            ["container", "inspect", argv[3]],
            config_dir=config["docker_config"],
        )
        if inspected.returncode:
            raise ValueError("source cleanup identity is unavailable")
        container = json.loads(inspected.stdout)[0]
        _native_container_identity(container, config, intent)
        if container["Id"] != argv[3]:
            raise ValueError("source cleanup ID differs")
    result = _native_call(config["docker"], argv, config_dir=config["docker_config"])
    with open(config["cleanup_log"], "a", encoding="utf-8") as output:
        output.write(
            json.dumps(
                {
                    "argv": argv,
                    "exit_code": result.returncode,
                    "observed_at": time.time(),
                }
            )
            + "\n"
        )
    sys.stdout.buffer.write(result.stdout)
    sys.stderr.buffer.write(result.stderr)
    raise SystemExit(result.returncode)


class OwnedDispatch:
    """One parent-owned session, one pipe release and one registered dispatch."""

    def __init__(self, root):
        self.write_fd = None
        read_fd, write_fd = os.pipe()
        self.write_fd = write_fd
        output_fd = os.open(
            root / "helper.log", os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600
        )
        try:
            self.process = subprocess.Popen(
                [
                    sys.executable,
                    str(Path(__file__).resolve()),
                    "--dispatch",
                    str(root / "config.json"),
                    str(read_fd),
                ],
                pass_fds=(read_fd,),
                stdout=output_fd,
                stderr=output_fd,
                start_new_session=True,
                env=_native_environment(root / "docker-config"),
            )
        except BaseException:
            os.close(write_fd)
            self.write_fd = None
            raise
        finally:
            os.close(read_fd)
            os.close(output_fd)

    def release(self):
        if self.write_fd is None or self.process.poll() is not None:
            raise ValueError("helper release is disabled")
        os.write(self.write_fd, b"release\n")
        os.close(self.write_fd)
        self.write_fd = None

    def finish(self, cancel=False):
        if self.write_fd is not None:
            os.close(self.write_fd)
            self.write_fd = None
        if cancel and self.process.poll() is None:
            if os.getpgid(self.process.pid) != self.process.pid:
                raise RuntimeError("owned helper process group differs") from None
            os.killpg(self.process.pid, signal.SIGTERM)
        try:
            code = self.process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            if os.getpgid(self.process.pid) != self.process.pid:
                raise RuntimeError("owned helper process group differs") from None
            os.killpg(self.process.pid, signal.SIGKILL)
            self.process.wait(timeout=5)
            raise
        try:
            os.killpg(self.process.pid, 0)
        except ProcessLookupError:
            return {
                "exit_code": code,
                "reaped": True,
                "group_gone": True,
                "control_closed": True,
                "future_dispatch_disabled": True,
            }
        raise RuntimeError("owned helper process group is still present")


class NativeHarness(unittest.TestCase):
    def _call(self, config, argv):
        return _native_call(
            self.docker, argv, config["deadline"], config["docker_config"]
        )

    def _observe(self, config, stop, witness):
        deadline = config["deadline"] - 20
        try:
            while not stop.is_set() and time.monotonic() < deadline:
                if Path(config["intent"]).exists():
                    intent = _native_read(Path(config["intent"]))
                    cid = _native_cid(Path(intent["tracking"]))
                    if cid is None:
                        stop.wait(0.1)
                        continue
                    result = self._call(config, ["container", "inspect", cid])
                    if not result.returncode:
                        container = json.loads(result.stdout)[0]
                        _native_container_identity(container, config, intent)
                        _native_cid(Path(intent["tracking"]), container["Id"])
                        if container["State"]["Running"]:
                            if config["delay"] != "late":
                                since, required = witness["started"], EVENT_ACTIONS[:2]
                                witness["events"] = self._events(
                                    config, intent, since, time.time(), cid, required
                                )
                            witness.update(
                                {"container": container, "observed_at": time.time()}
                            )
                            if config["delay"] == "kill":
                                killed = self._call(
                                    config,
                                    [
                                        "container",
                                        "kill",
                                        "--signal",
                                        "KILL",
                                        container["Id"],
                                    ],
                                )
                                witness["kill_exit"] = killed.returncode
                            return
                stop.wait(0.1)
        except Exception as error:
            witness["error"] = f"{type(error).__name__}: {error}"

    def _events(self, config, intent, started, ended, cid, required=EVENT_ACTIONS):
        self.assertTrue(required, "required daemon actions must not be empty")
        stamps = [f"{value:.9f}" for value in (started, ended)]
        result = self._call(
            config,
            [
                "events",
                "--since=" + stamps[0],
                "--until=" + stamps[1],
                "--filter=type=container",
                "--filter=label=hyhome.openbao.tls-probe=" + intent["name"],
                *("--filter=event=" + action for action in required),
                "--format={{json .}}",
            ],
        )
        self.assertEqual(0, result.returncode, "bounded daemon events unavailable")
        events = [json.loads(line) for line in result.stdout.splitlines()]
        self.assertLessEqual(len(events), 100)
        for event in events:
            self.assertEqual(cid, event["Actor"]["ID"])
            self.assertEqual(intent["name"], event["Actor"]["Attributes"]["name"])
            self.assertEqual(
                intent["name"], event["Actor"]["Attributes"]["hyhome.openbao.tls-probe"]
            )
        actions = {event["Action"] for event in events}
        self.assertTrue(set(required) <= actions)
        return events

    def _reconcile(self, config, intent, receipt, external=False):
        result = self._call(config, _native_listing(intent["name"]))
        if result.returncode:
            raise RuntimeError("exact source-owned container listing failed")
        ids = result.stdout.decode().split()
        if ids:
            if len(ids) != 1 or not re.fullmatch(r"[a-f0-9]{64}", ids[0]):
                raise RuntimeError("ambiguous source-owned container identity")
            inspected = self._call(config, ["container", "inspect", ids[0]])
            if inspected.returncode:
                raise RuntimeError("fallback identity is unavailable")
            container = json.loads(inspected.stdout)[0]
            _native_container_identity(container, config, intent)
            receipt["external_reconciliation" if external else "fallback_cleanup"] = {
                "cid": ids[0],
                "exit_code": self._call(
                    config, ["container", "rm", "--force", ids[0]]
                ).returncode,
            }
        remaining = self._call(config, _native_listing(intent["name"]))
        if remaining.returncode or remaining.stdout.strip():
            raise RuntimeError("source-owned container absence is unverified")
        receipt["exact_name_label_absent"] = True
        cid = receipt.get("witness", {}).get("container", {}).get("Id")
        if cid:
            query = ["container", "ls", "--all", "--quiet", "--no-trunc"]
            result = self._call(config, [*query, "--filter", "id=" + cid])
            if result.returncode or result.stdout.strip():
                raise RuntimeError("exact observed container ID absence is unverified")
            receipt["exact_cid_absent"] = True

    def _checker(self, root, config):
        process = subprocess.Popen(
            ["sh", str(SCRIPT), config["material"], IMAGE],
            env={
                **_native_environment(Path(config["docker_config"])),
                "PATH": f"{root / 'bin'}:/usr/bin:/bin",
            },
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True,
        )
        try:
            stdout, stderr = process.communicate(
                timeout=max(1, config["deadline"] - time.monotonic() - 20)
            )
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.communicate(timeout=5)
            raise
        return process.returncode, stdout, stderr

    def _late(self, config, result, helper, receipt, started):
        code, stdout, stderr = result
        checker_ended = time.time()
        intent = _native_read(Path(config["intent"]))
        listed = self._call(config, _native_listing(intent["name"]))
        _native_release_allowed(
            code,
            stdout,
            Path(intent["tracking"]).is_dir(),
            listed.returncode,
            listed.stdout,
        )
        receipt.update(
            {
                "checker_exit": code,
                "checker_ended": checker_ended,
                "stdout": stdout.decode(),
                "stderr": stderr.decode(),
                "source_cleanup": "FAIL pending-reconciliation",
                "initial_exact_query_empty": True,
            }
        )
        helper.release()
        receipt["helper"] = helper.finish()
        dispatch = _native_read(Path(config["dispatch_result"]))
        receipt["dispatch"] = dispatch
        self.assertEqual("DISPATCHED", dispatch["result"], "INDETERMINATE dispatch")
        self.assertEqual(0, receipt["helper"]["exit_code"])
        self._late_result(config, dispatch, intent, receipt, started, checker_ended)

    def _late_result(self, config, dispatch, intent, receipt, started, checker_ended):
        stop, witness = threading.Event(), {}
        self._observe(config, stop, witness)
        self.assertIn("container", witness, witness)
        self.assertEqual(dispatch["cid"], witness["container"]["Id"])
        receipt["witness"] = witness
        self._reconcile(config, intent, receipt, external=True)
        self.assertIn("external_reconciliation", receipt)
        self.assertEqual(0, receipt["external_reconciliation"]["exit_code"])
        receipt["events"] = self._events(
            config, intent, started, time.time(), dispatch["cid"]
        )
        created = [
            event["timeNano"] / 1e9
            for event in receipt["events"]
            if event["Action"] == "create"
        ]
        self.assertGreater(created[0], checker_ended)
        self.assertTrue(Path(intent["tracking"]).is_dir())
        receipt["cleanup_classification"] = "external_controlled_reconciliation"
        receipt["source_explicit_rm"] = False
        receipt["cleanup_commands"] = [
            json.loads(line)
            for line in Path(config["cleanup_log"]).read_text().splitlines()
        ]
        receipt["elapsed_seconds"] = time.time() - started
        receipt["result"] = "PASS controlled dispatch; source FAIL retained"

    def _delay_events(self, config, intent, started, ended, cid, receipt):
        receipt["events"] = receipt["witness"]["events"] + self._events(
            config, intent, started, ended, cid, ("die", "destroy")
        )
        receipt["cleanup_commands"] = [
            json.loads(line)
            for line in Path(config["cleanup_log"]).read_text().splitlines()
        ]
        receipt["source_explicit_rm"] = any(
            row["argv"] == ["container", "rm", "--force", cid] and row["exit_code"] == 0
            for row in receipt["cleanup_commands"]
        )
        receipt["cleanup_classification"] = (
            "source_explicit_rm"
            if receipt["source_explicit_rm"]
            else "automatic_destroy_without_source_rm"
        )
        times = {
            event["Action"]: event["timeNano"] / 1e9 for event in receipt["events"]
        }
        receipt["native_seconds"] = times["die"] - times["start"]

    def _check_delay(self, config, result, witness, receipt, started):
        code, stdout, stderr = result
        ended = time.time()
        receipt.update(
            {
                "checker_exit": code,
                "elapsed_seconds": ended - started,
                "stdout": stdout.decode(),
                "stderr": stderr.decode(),
            }
        )
        self.assertIn("container", witness, witness)
        intent = _native_read(Path(config["intent"]))
        cid = witness["container"]["Id"]
        receipt["witness"] = witness
        self._delay_events(config, intent, started, ended, cid, receipt)
        if config["delay"] == 25:
            self.assertEqual(0, code, stdout)
            self.assertIn(b"TLS_MATERIAL PASS", stdout)
            self.assertGreaterEqual(receipt["native_seconds"], 25)
            self.assertFalse(Path(intent["tracking"]).exists())
        else:
            self.assertNotEqual(0, code)
            self.assertIn(b"cleanup=pending-reconciliation", stdout)
            self.assertTrue(Path(intent["tracking"]).is_dir())
            if config["delay"] == 61:
                self.assertGreaterEqual(receipt["elapsed_seconds"], 60)
            else:
                expected = 17 if config["delay"] == "error" else 137
                died = [
                    event for event in receipt["events"] if event["Action"] == "die"
                ]
                self.assertEqual(
                    str(expected), died[-1]["Actor"]["Attributes"]["exitCode"]
                )
                if config["delay"] == "kill":
                    self.assertEqual(0, witness["kill_exit"])
        receipt["result"] = "PASS"

    def _receipt(self, delay):
        return {
            "requested_delay": delay,
            "source_sha256": hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),
            "helper_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "test_sha256": hashlib.sha256(self.test_source.read_bytes()).hexdigest(),
            "image": IMAGE,
            "image_id": self.image_id,
            "fallback_cleanup": None,
        }

    def _run_delay(self, delay):
        root, config = self._fixture(delay)
        receipt = self._receipt(delay)
        receipt["docker_config"] = config["docker_config"]
        receipt["client_environment"] = "all inherited DOCKER_* cleared"
        stop, witness = threading.Event(), {"started": time.time()}
        observer = threading.Thread(target=self._observe, args=(config, stop, witness))
        started = witness["started"]
        helper = OwnedDispatch(root) if delay == "late" else None
        if not helper:
            observer.start()
        try:
            result = self._checker(root, config)
            if helper:
                self._late(config, result, helper, receipt, started)
            else:
                stop.set()
                observer.join(timeout=10)
                self.assertFalse(observer.is_alive(), "observer did not finish")
                self._check_delay(config, result, witness, receipt, started)
        except BaseException as error:
            receipt["result"] = f"FAIL {type(error).__name__}: {error}"
            raise
        finally:
            stop.set()
            if observer.ident is not None:
                observer.join(timeout=10)
            try:
                if helper:
                    receipt["helper_final"] = helper.finish(cancel=True)
                if observer.is_alive():
                    raise RuntimeError("bounded observer did not finish")
                if Path(config["intent"]).exists():
                    self._reconcile(
                        config, _native_read(Path(config["intent"])), receipt
                    )
                self.assertIsNone(
                    receipt["fallback_cleanup"],
                    "fallback cleanup is not source cleanup PASS",
                )
            except BaseException as error:
                receipt["cleanup_error"] = f"{type(error).__name__}: {error}"
                if receipt.get("result", "").startswith("PASS"):
                    receipt["result"] = "FAIL cleanup"
                    raise
            finally:
                _native_write(root / "receipt.json", receipt)
                print(f"B3_NATIVE_RECEIPT {root / 'receipt.json'}")


if __name__ == "__main__":
    os.umask(0o077)
    if len(sys.argv) != 4 or sys.argv[1] != "--dispatch":
        raise SystemExit("only the owned dispatch helper entry point is admitted")
    _native_dispatch(Path(sys.argv[2]), int(sys.argv[3]))
