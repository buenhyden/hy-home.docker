#!/usr/bin/env bash
set -u
usage() {
  printf '%s\n' "Usage: bash .agents/skills/infra-validate/scripts/static-checks.sh [--help|-h]"
}
blocked_bootstrap() {
  local failed="$1"
  printf '%s\n' "bash-runtime PASS category=available child_exit=NA"
  local check
  for check in python-runtime yaml-parser git-discovery tracked-snapshot input-graph support-tools fixture-git yaml-lint shell-lint docker-cli compose-plugin compose-config-render compose-structure; do
    if [ "$check" = "$failed" ]; then
      printf '%s\n' "$check BLOCKED category=missing-tool child_exit=127"
    elif [ "$failed" = "yaml-parser" ] && [ "$check" = "python-runtime" ]; then
      printf '%s\n' "$check PASS category=available child_exit=NA"
    else
      printf '%s\n' "$check BLOCKED category=prerequisite-blocked child_exit=NA"
    fi
  done
  printf '%s\n' "runtime-observation NOT_RUN category=needs-separate-approval child_exit=NA"
  printf '%s\n' "secret-values NOT_RUN category=out-of-scope child_exit=NA"
  printf '%s\n' "fixture-cleanup PASS category=not-created child_exit=NA"
  if [ "$failed" = "python-runtime" ]; then
    printf '%s\n' "summary PASS=2 FAIL=0 BLOCKED=13 SKIPPED=0 NOT_APPLICABLE=0 NOT_RUN=2"
  else
    printf '%s\n' "summary PASS=3 FAIL=0 BLOCKED=12 SKIPPED=0 NOT_APPLICABLE=0 NOT_RUN=2"
  fi
}
case "$#" in
0) ;;
1)
  case "$1" in
  --help|-h) usage; exit 0 ;;
  *) usage >&2; exit 2 ;;
  esac
  ;;
*) usage >&2; exit 2 ;;
esac
SCRIPT_DIR="$(CDPATH= cd -- "${BASH_SOURCE[0]%/*}" && pwd -P)" || exit 2
REPO_ROOT="$(CDPATH= cd -- "$SCRIPT_DIR/../../../.." && pwd -P)" || exit 2
if ! command -v python3 >/dev/null 2>&1; then
  blocked_bootstrap python-runtime
  exit 2
fi
if ! python3 -I -c 'import yaml' </dev/null >/dev/null 2>&1; then
  blocked_bootstrap yaml-parser
  exit 2
fi
exec python3 -I - "$REPO_ROOT" <<'PY'
import atexit
import collections
import os
import pathlib
import re
import selectors
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
import time
import yaml
STATES = ("PASS", "FAIL", "BLOCKED", "SKIPPED", "NOT_APPLICABLE", "NOT_RUN")
CHECKS = ("bash-runtime", "python-runtime", "yaml-parser", "git-discovery", "tracked-snapshot",
          "input-graph", "support-tools", "fixture-git", "yaml-lint", "shell-lint",
          "docker-cli", "compose-plugin", "compose-config-render", "compose-structure")
MAX_CAPTURE = 16 * 1024 * 1024
MAX_SOURCE = 16 * 1024 * 1024
TIMEOUT_SECONDS = 59
KILL_GRACE_SECONDS = 1
root = pathlib.Path(sys.argv[1])
results: dict[str, tuple[str, str, int | None]] = {}
fixture: pathlib.Path | None = None
fixture_identity: tuple[int, int, int, int] | None = None
source_root_identity: tuple[int, int, int, int] | None = None
cleanup_attempted = False
def add(check: str, state: str, category: str, code: int | None = None) -> None:
    if check not in results:
        results[check] = (state, category, code)
def record_child(check: str, code: int, problem: str | None = None,
                 *, failure: str = "FAIL", success: str = "validated") -> None:
    add(check, "PASS" if code == 0 else failure,
        success if code == 0 else problem or "command-failed", code)
def block_unset(category: str = "prerequisite-blocked") -> None:
    for check in CHECKS:
        if check not in results:
            add(check, "BLOCKED", category)
def resolve_tool(name: str) -> pathlib.Path | None:
    raw = shutil.which(name)
    if raw is None:
        return None
    try:
        path = pathlib.Path(raw).resolve(strict=True)
        observed = path.stat()
    except OSError:
        return None
    if not stat.S_ISREG(observed.st_mode) or observed.st_mode & 0o111 == 0:
        return None
    return path
def child(argv: list[str], cwd: pathlib.Path, env: dict[str, str],
          *, capture: bool = False) -> tuple[int, bytes, str | None]:
    try:
        process = subprocess.Popen(argv, cwd=cwd, env=env, stdin=subprocess.DEVNULL,
                                   stdout=subprocess.PIPE if capture else subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL, start_new_session=True)
    except OSError:
        return 127, b"", "launch-error"
    def stop() -> None:
        try:
            os.killpg(process.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        try:
            process.wait(timeout=KILL_GRACE_SECONDS)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            process.wait()
    if not capture:
        try:
            process.wait(timeout=TIMEOUT_SECONDS)
        except subprocess.TimeoutExpired:
            stop()
            return 124, b"", "timeout"
        return process.returncode, b"", None
    assert process.stdout is not None
    data = bytearray()
    deadline = time.monotonic() + TIMEOUT_SECONDS
    with selectors.DefaultSelector() as selector:
        selector.register(process.stdout, selectors.EVENT_READ)
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                stop()
                return 124, b"", "timeout"
            events = selector.select(min(remaining, 0.1))
            if events:
                chunk = os.read(process.stdout.fileno(), min(65536, MAX_CAPTURE + 1 - len(data)))
                if not chunk:
                    break
                data.extend(chunk)
                if len(data) > MAX_CAPTURE:
                    stop()
                    return 125, b"", "output-limit"
            elif process.poll() is not None:
                break
    try:
        process.wait(timeout=max(0.0, deadline - time.monotonic()))
    except subprocess.TimeoutExpired:
        stop()
        return 124, b"", "timeout"
    return process.returncode, bytes(data), None
def identity(observed: os.stat_result) -> tuple[int, ...]:
    return (observed.st_dev, observed.st_ino, observed.st_mode, observed.st_uid,
            observed.st_gid, observed.st_size, observed.st_mtime_ns, observed.st_ctime_ns)
def safe_read(relative: str) -> tuple[bytes, tuple[int, ...]]:
    parts = pathlib.PurePosixPath(relative).parts
    if not parts or any(part in ("", ".", "..") for part in parts):
        raise ValueError("unsafe-tracked-file")
    root_before = os.lstat(root)
    root_fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        root_after = os.fstat(root_fd)
        if (not stat.S_ISDIR(root_before.st_mode)
                or (root_before.st_dev, root_before.st_ino) != (root_after.st_dev, root_after.st_ino)):
            raise ValueError("unsafe-tracked-file")
        directory_fd = root_fd
        owned_fd = False
        try:
            for part in parts[:-1]:
                before = os.stat(part, dir_fd=directory_fd, follow_symlinks=False)
                next_fd = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                                  dir_fd=directory_fd)
                after = os.fstat(next_fd)
                if (not stat.S_ISDIR(before.st_mode)
                        or (before.st_dev, before.st_ino, before.st_mode)
                        != (after.st_dev, after.st_ino, after.st_mode)):
                    os.close(next_fd)
                    raise ValueError("unsafe-tracked-file")
                if owned_fd:
                    os.close(directory_fd)
                directory_fd = next_fd
                owned_fd = True
            before = os.stat(parts[-1], dir_fd=directory_fd, follow_symlinks=False)
            file_fd = os.open(parts[-1], os.O_RDONLY | os.O_NONBLOCK | os.O_NOFOLLOW,
                              dir_fd=directory_fd)
            try:
                opened = os.fstat(file_fd)
                if not stat.S_ISREG(opened.st_mode) or identity(before) != identity(opened):
                    raise ValueError("unsafe-tracked-file")
                chunks: list[bytes] = []
                total = 0
                while True:
                    chunk = os.read(file_fd, min(1024 * 1024, MAX_SOURCE + 1 - total))
                    if not chunk:
                        break
                    total += len(chunk)
                    if total > MAX_SOURCE:
                        raise ValueError("unsafe-tracked-file")
                    chunks.append(chunk)
                after = os.fstat(file_fd)
                if identity(opened) != identity(after):
                    raise ValueError("unsafe-tracked-file")
                return b"".join(chunks), identity(after)
            finally:
                os.close(file_fd)
        finally:
            if owned_fd:
                os.close(directory_fd)
    finally:
        os.close(root_fd)
def safe_write(relative: str, data: bytes, *, executable: bool = False) -> pathlib.Path:
    if fixture is None:
        raise ValueError("unsafe-fixture")
    parts = pathlib.PurePosixPath(relative).parts
    if not parts or any(part in ("", ".", "..") for part in parts):
        raise ValueError("unsafe-fixture")
    parent = fixture
    for part in parts[:-1]:
        parent = parent / part
        try:
            parent.mkdir(mode=0o700)
        except FileExistsError:
            observed = parent.lstat()
            if not stat.S_ISDIR(observed.st_mode) or stat.S_ISLNK(observed.st_mode):
                raise ValueError("unsafe-fixture")
    destination = parent / parts[-1]
    fd = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                 0o755 if executable else 0o644)
    try:
        view = memoryview(data)
        while view:
            written = os.write(fd, view)
            if written <= 0:
                raise OSError("short write")
            view = view[written:]
        os.fsync(fd)
    finally:
        os.close(fd)
    return destination
def sensitive_source(relative: str) -> bool:
    parts = pathlib.PurePosixPath(relative).parts
    lowered = tuple(part.lower() for part in parts)
    name = lowered[-1] if lowered else ""
    if relative == ".env.example":
        return False
    if any(part == "secrets" for part in lowered):
        return True
    if name.startswith(".env"):
        return True
    if any(token in name for token in ("credential", "password", "token")):
        return not name.endswith((".sh", ".py", ".md", ".example", ".template"))
    return False
def cleanup() -> bool:
    global cleanup_attempted, fixture
    cleanup_attempted = True
    if fixture is None or fixture_identity is None:
        return True
    if not getattr(shutil.rmtree, "avoids_symlink_attacks", False):
        return False
    try:
        observed = fixture.lstat()
        parent = fixture.parent.lstat()
        if (fixture.parent != root or not fixture.name.startswith(".infra-static-")
                or stat.S_IMODE(observed.st_mode) != 0o700
                or not stat.S_ISDIR(observed.st_mode) or stat.S_ISLNK(observed.st_mode)
                or (observed.st_uid, observed.st_dev, observed.st_ino, observed.st_mode)
                != fixture_identity or source_root_identity is None
                or (parent.st_uid, parent.st_dev, parent.st_ino, parent.st_mode)
                != source_root_identity):
            return False
        shutil.rmtree(fixture)
        fixture = None
        return True
    except OSError:
        return False
def emergency_cleanup() -> None:
    if not cleanup_attempted:
        cleanup()
atexit.register(emergency_cleanup)
class UniqueLoader(yaml.SafeLoader):
    pass
def unique_mapping(loader: UniqueLoader, node: yaml.Node, deep: bool = False) -> dict:
    mapping: dict = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str) or key in mapping:
            raise ValueError("unsupported-input-graph")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping
UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)
def main() -> None:
    global fixture, fixture_identity, source_root_identity
    add("bash-runtime", "PASS", "available")
    add("python-runtime", "PASS", "available")
    add("yaml-parser", "PASS", "available")
    tool_names = ("git", "bash", "cp", "dirname", "mkdir", "python3", "rm", "sed",
                  "sort", "tr", "wc", "docker", "yamllint", "shellcheck")
    tools = {name: resolve_tool(name) for name in tool_names}
    required_support = ("bash", "cp", "dirname", "git", "mkdir", "python3",
                        "rm", "sed", "sort", "tr", "wc")
    missing_support = [name for name in required_support if tools[name] is None]
    add("support-tools", "BLOCKED" if missing_support else "PASS",
        "missing-tool" if missing_support else "available",
        127 if missing_support else None)
    add("docker-cli", "BLOCKED" if tools["docker"] is None else "PASS",
        "missing-tool" if tools["docker"] is None else "available",
        127 if tools["docker"] is None else None)
    if tools["git"] is None:
        add("git-discovery", "BLOCKED", "missing-tool", 127)
        block_unset()
        return
    base_env = {
        "PATH": str(tools["git"].parent),
        "LC_ALL": "C",
        "LANG": "C",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": "/dev/null",
        "GIT_OPTIONAL_LOCKS": "0",
    }
    code, top, problem = child([str(tools["git"]), "rev-parse", "--show-toplevel"],
                               root, base_env, capture=True)
    if code or problem or len(top) > 4096:
        add("git-discovery", "BLOCKED", problem or "command-failed", code)
        block_unset()
        return
    try:
        discovered = pathlib.Path(top.decode("utf-8").strip())
    except UnicodeError:
        add("git-discovery", "BLOCKED", "invalid-output", code)
        block_unset()
        return
    if discovered != root:
        add("git-discovery", "BLOCKED", "wrong-root", code)
        block_unset()
        return
    code, listing, problem = child([str(tools["git"]), "ls-files", "-z"],
                                   root, base_env, capture=True)
    if code or problem:
        add("git-discovery", "BLOCKED", problem or "command-failed", code)
        block_unset()
        return
    try:
        decoded = listing.decode("utf-8")
        tracked = [item for item in decoded.split("\0") if item]
    except UnicodeError:
        add("git-discovery", "BLOCKED", "invalid-output", code)
        block_unset()
        return
    if any(pathlib.PurePosixPath(item).is_absolute()
           or any(part in ("", ".", "..") for part in pathlib.PurePosixPath(item).parts)
           for item in tracked):
        add("git-discovery", "BLOCKED", "invalid-output", code)
        block_unset()
        return
    add("git-discovery", "PASS", "tracked-index", 0)
    tracked_set = set(tracked)
    root_stat = root.lstat()
    source_root_identity = (root_stat.st_uid, root_stat.st_dev,
                            root_stat.st_ino, root_stat.st_mode)
    fixture = pathlib.Path(tempfile.mkdtemp(prefix=".infra-static-", dir=root))
    fixture.chmod(0o700)
    fixture_stat = fixture.lstat()
    fixture_identity = (fixture_stat.st_uid, fixture_stat.st_dev,
                        fixture_stat.st_ino, fixture_stat.st_mode)
    copied: set[str] = set()
    generated: set[str] = set()
    identities: dict[str, tuple[int, ...]] = {}
    def copy_one(relative: str, *, content: bytes | None = None) -> None:
        if relative in copied:
            return
        if relative not in tracked_set or sensitive_source(relative):
            raise ValueError("unsafe-tracked-file")
        source, observed = safe_read(relative)
        payload = source if content is None else content
        source_mode = observed[2]
        safe_write(relative, payload, executable=bool(source_mode & 0o111))
        copied.add(relative)
        identities[relative] = observed
    required_inputs = (
        ".yamllint",
        ".shellcheckrc",
        ".env.example",
        "docker-compose.yml",
        "scripts/validation/validate-docker-compose.sh",
        "docs/05.operations/policies/0078-compose-profile-vocabulary.md",
    )
    if any(relative not in tracked_set for relative in required_inputs):
        add("tracked-snapshot", "BLOCKED", "missing-graph-input")
        block_unset()
        return
    env_source, env_identity = safe_read(".env.example")
    try:
        env_lines = env_source.decode("utf-8").splitlines()
    except UnicodeError as error:
        raise ValueError("unsafe-tracked-file") from error
    keys: dict[str, str] = {}
    for index, line in enumerate(env_lines):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        match = re.match(r"^(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)=", line)
        if not match or match.group(1) in keys:
            raise ValueError("unsafe-tracked-file")
        key = match.group(1)
        if "PORT" in key:
            value = str(20000 + index)
        elif key.endswith(("_UID", "_GID")):
            value = "1000"
        elif any(token in key for token in ("PATH", "DIR", "HOME", "ROOT", "REPO")):
            value = f"./.synthetic/{key.lower()}"
        elif key.endswith("DOCKERFILE"):
            value = "Dockerfile"
        elif key.endswith(("ENABLED", "DEBUG")):
            value = "false"
        else:
            value = "fixture"
        keys[key] = value
    synthetic_env = "".join(f"{key}={value}\n" for key, value in keys.items()).encode()
    safe_write(".env.example", synthetic_env)
    copied.add(".env.example")
    identities[".env.example"] = env_identity
    safe_write(".env", synthetic_env)
    generated.add(".env")
    (fixture / ".synthetic").mkdir(mode=0o700)
    generated.add(".synthetic")
    for relative in required_inputs:
        if relative != ".env.example":
            copy_one(relative)
    lint_candidates = [
        item
        for item in tracked
        if item.startswith("infra/") and item.endswith((".sh", ".yaml", ".yml"))
    ]
    for relative in lint_candidates:
        copy_one(relative)
    add("tracked-snapshot", "PASS", "verified")
    def materialize(relative: str) -> bool:
        if sensitive_source(relative):
            raise ValueError("unsafe-input-graph")
        candidates = (
            [relative]
            if relative in tracked_set
            else [item for item in tracked if item.startswith(relative.rstrip("/") + "/")]
        )
        if not candidates:
            return False
        for item in candidates:
            copy_one(item)
        return True
    variable = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)(?:(:-|-)([^}]*))?\}")
    def interpolate(raw: str) -> str:
        if not isinstance(raw, str):
            raise ValueError("unsupported-input-graph")
        def replace(match: re.Match[str]) -> str:
            key = match.group(1)
            if key not in keys:
                raise ValueError("unresolved-path-interpolation")
            return keys[key]
        value = variable.sub(replace, raw)
        if "${" in value or "$" in value or "://" in value or value.startswith("~"):
            raise ValueError("unresolved-path-interpolation")
        return value
    def accepted(relative: str, target: pathlib.Path) -> bool:
        if relative in copied or relative in generated:
            return True
        prefix = relative.rstrip("/") + "/"
        if target.is_dir() and any(item.startswith(prefix) for item in copied | generated):
            return True
        return False
    def local(
        raw: str,
        base: pathlib.Path,
        *,
        generate: bool = False,
    ) -> pathlib.Path:
        value = interpolate(raw)
        candidate = pathlib.PurePosixPath(value)
        if candidate.is_absolute():
            raise ValueError("external-absolute-path")
        target = (base / candidate).resolve()
        fixture_root = fixture.resolve()
        if target != fixture_root and fixture_root not in target.parents:
            raise ValueError("external-absolute-path")
        relative = target.relative_to(fixture).as_posix()
        if generate:
            if target.exists() or relative in copied or relative in generated:
                raise ValueError("unsafe-input-graph")
            safe_write(relative, b"fixture\n")
            generated.add(relative)
        elif not accepted(relative, target):
            if not materialize(relative) or not accepted(relative, target):
                raise ValueError("missing-graph-input")
        observed = target.lstat()
        if stat.S_ISLNK(observed.st_mode):
            raise ValueError("unsafe-input-graph")
        return target
    def graph_paths(document: object, compose: pathlib.Path) -> list[pathlib.Path]:
        if not isinstance(document, dict):
            raise ValueError("unsupported-input-graph")
        top_keys = {"name", "version", "services", "configs", "secrets", "include"}
        if any(key not in top_keys and not key.startswith("x-") for key in document):
            raise ValueError("unsupported-input-graph")
        dependencies: list[pathlib.Path] = []
        includes = document.get("include", [])
        if isinstance(includes, str):
            includes = [includes]
        if not isinstance(includes, list) or not all(isinstance(item, str) for item in includes):
            raise ValueError("unsupported-input-graph")
        dependencies.extend(local(path, compose.parent) for path in includes)
        services = document.get("services") or {}
        if not isinstance(services, dict):
            raise ValueError("unsupported-input-graph")
        for name, service in services.items():
            if not isinstance(name, str) or not isinstance(service, dict):
                raise ValueError("unsupported-input-graph")
            service_keys = {"image", "profiles", "environment", "ports", "networks",
                            "depends_on", "command", "entrypoint", "healthcheck", "restart",
                            "deploy", "logging", "read_only", "user", "working_dir",
                            "hostname", "container_name", "cap_add", "cap_drop", "security_opt",
                            "sysctls", "tmpfs", "stop_grace_period", "stop_signal", "expose",
                            "extra_hosts", "init", "ipc", "pid", "platform", "privileged",
                            "pull_policy", "stdin_open", "tty", "ulimits", "userns_mode",
                            "network_mode", "configs", "secrets", "env_file", "build", "volumes"}
            if any(key not in service_keys and not key.startswith("x-") for key in service):
                raise ValueError("unsupported-input-graph")
            env_files = service.get("env_file", [])
            if isinstance(env_files, (str, dict)):
                env_files = [env_files]
            if not isinstance(env_files, list):
                raise ValueError("unsupported-input-graph")
            for item in env_files:
                if isinstance(item, str):
                    raw = item
                elif isinstance(item, dict) and set(item) <= {"path", "required"}:
                    raw = item.get("path")
                    if "required" in item and not isinstance(item["required"], bool):
                        raise ValueError("unsupported-input-graph")
                else:
                    raise ValueError("unsupported-input-graph")
                local(raw, compose.parent)
            build = service.get("build")
            if isinstance(build, str):
                local(build, compose.parent)
            elif build is not None:
                if not isinstance(build, dict):
                    raise ValueError("unsupported-input-graph")
                safe_build = {"context", "dockerfile", "additional_contexts", "args", "target",
                              "network", "no_cache", "pull", "shm_size", "labels", "tags",
                              "platforms", "provenance", "sbom", "ulimits", "extra_hosts",
                              "isolation", "privileged"}
                if set(build) - safe_build:
                    raise ValueError("unsupported-input-graph")
                context_raw = build.get("context", ".")
                dockerfile_raw = build.get("dockerfile", "Dockerfile")
                if not isinstance(context_raw, str) or not isinstance(dockerfile_raw, str):
                    raise ValueError("unsupported-input-graph")
                context = local(context_raw, compose.parent)
                local(dockerfile_raw, context)
                extra = build.get("additional_contexts", {})
                if isinstance(extra, dict):
                    if not all(isinstance(key, str) and isinstance(value, str) for key, value in extra.items()):
                        raise ValueError("unsupported-input-graph")
                    extra_values = list(extra.values())
                elif isinstance(extra, list) and all(isinstance(value, str) and "=" in value for value in extra):
                    extra_values = [value.split("=", 1)[1] for value in extra]
                else:
                    raise ValueError("unsupported-input-graph")
                for value in extra_values:
                    local(value, compose.parent)
            volumes = service.get("volumes", [])
            if not isinstance(volumes, list):
                raise ValueError("unsupported-input-graph")
            for volume in volumes:
                if isinstance(volume, str):
                    if ":" not in volume:
                        continue
                    source = volume.split(":", 1)[0]
                    if (
                        source.startswith((".", "/", "~", "$"))
                        or "/" in source
                    ):
                        local(source, compose.parent)
                elif isinstance(volume, dict):
                    if volume.get("type") == "bind":
                        source = volume.get("source", volume.get("src"))
                        if not isinstance(source, str):
                            raise ValueError("unsupported-input-graph")
                        local(source, compose.parent)
                    elif volume.get("type") not in {"volume", "tmpfs", "image"}:
                        raise ValueError("unsupported-input-graph")
                else:
                    raise ValueError("unsupported-input-graph")
        for group in ("configs", "secrets"):
            definitions = document.get(group) or {}
            if not isinstance(definitions, dict):
                raise ValueError("unsupported-input-graph")
            for name, definition in definitions.items():
                if not isinstance(name, str) or not isinstance(definition, dict):
                    raise ValueError("unsupported-input-graph")
                allowed = {"file", "environment", "external", "name"}
                if group == "configs":
                    allowed.add("content")
                if set(definition) - allowed:
                    raise ValueError("unsupported-input-graph")
                if "file" in definition:
                    if not isinstance(definition["file"], str):
                        raise ValueError("unsupported-input-graph")
                    local(
                        definition["file"],
                        compose.parent,
                        generate=group == "secrets",
                    )
        return dependencies
    def validate_graph() -> None:
        pending = [fixture / "docker-compose.yml"]
        edges: dict[pathlib.Path, list[pathlib.Path]] = {}
        while pending:
            compose = pending.pop()
            if compose in edges:
                continue
            if len(edges) >= 256:
                raise ValueError("unsupported-input-graph")
            with compose.open("r", encoding="utf-8") as stream:
                document = yaml.load(stream, Loader=UniqueLoader)
            edges[compose] = graph_paths(document, compose)
            pending.extend(edges[compose])
        visiting: set[pathlib.Path] = set()
        visited: set[pathlib.Path] = set()
        def visit(node: pathlib.Path) -> None:
            if node in visiting:
                raise ValueError("unsupported-input-graph")
            if node in visited:
                return
            visiting.add(node)
            for dependency in edges.get(node, []):
                visit(dependency)
            visiting.remove(node)
            visited.add(node)
        visit(fixture / "docker-compose.yml")
        code, final_listing, problem = child(
            [str(tools["git"]), "ls-files", "-z"], root, base_env, capture=True)
        if code or problem or final_listing != listing:
            raise ValueError("unsafe-input-graph")
        for relative, expected in identities.items():
            _, observed = safe_read(relative)
            if observed != expected:
                raise ValueError("unsafe-input-graph")
    try:
        validate_graph()
        add("input-graph", "PASS", "verified")
    except (OSError, UnicodeError, ValueError, TypeError, yaml.YAMLError) as error:
        category = str(error)
        safe_categories = {"external-absolute-path", "missing-graph-input",
                           "unresolved-path-interpolation", "unsupported-input-graph",
                           "unsafe-input-graph", "unsafe-tracked-file"}
        if category not in safe_categories:
            category = "unsafe-input-graph"
        add("input-graph", "BLOCKED", category)
    bin_dir = fixture / ".bin"
    bin_dir.mkdir(mode=0o700)
    for name, target in tools.items():
        if target is not None:
            os.symlink(target, bin_dir / name)
    for directory in (".home", ".xdg", ".docker", ".tmp"):
        (fixture / directory).mkdir(mode=0o700)
        generated.add(directory)
    child_env = {
        "PATH": str(bin_dir),
        "LC_ALL": "C",
        "LANG": "C",
        "HOME": str(fixture / ".home"),
        "XDG_CONFIG_HOME": str(fixture / ".xdg"),
        "DOCKER_CONFIG": str(fixture / ".docker"),
        "TMPDIR": str(fixture / ".tmp"),
        "DOCKER_HOST": "unix://" + str(fixture / ".no-docker.sock"),
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": "/dev/null",
        "GIT_OPTIONAL_LOCKS": "0",
    }
    if tools["git"] is None or missing_support:
        add("fixture-git", "BLOCKED", "prerequisite-blocked")
    else:
        code, _, problem = child([str(tools["git"]), "init", "-q"], fixture, child_env)
        record_child("fixture-git", code, problem, failure="BLOCKED", success="initialized")
    yaml_inputs = [item for item in lint_candidates if item.endswith((".yaml", ".yml"))]
    if tools["yamllint"] is None:
        add("yaml-lint", "BLOCKED", "missing-tool", 127)
    elif not yaml_inputs:
        add("yaml-lint", "NOT_APPLICABLE", "no-eligible-input")
    else:
        code, _, problem = child(
            [str(tools["yamllint"]), "-c", ".yamllint", "-s", *yaml_inputs],
            fixture, child_env)
        record_child("yaml-lint", code, problem)
    shell_inputs = [item for item in lint_candidates if item.endswith(".sh")]
    if not shell_inputs:
        add("shell-lint", "NOT_APPLICABLE", "no-eligible-input")
    elif tools["shellcheck"] is None:
        add("shell-lint", "BLOCKED", "missing-tool", 127)
    else:
        code, _, problem = child(
            [str(tools["shellcheck"]), "--rcfile=.shellcheckrc",
             "--severity=warning", *shell_inputs], fixture, child_env)
        record_child("shell-lint", code, problem)
    prerequisites = (
        results.get("input-graph", ("BLOCKED", "", None))[0] == "PASS"
        and results.get("support-tools", ("BLOCKED", "", None))[0] == "PASS"
        and results.get("fixture-git", ("BLOCKED", "", None))[0] == "PASS"
    )
    if not prerequisites or tools["docker"] is None:
        add("compose-plugin", "BLOCKED", "prerequisite-blocked")
        add("compose-config-render", "BLOCKED", "prerequisite-blocked")
        add("compose-structure", "BLOCKED", "prerequisite-blocked")
        return
    code, _, problem = child(
        [str(tools["docker"]), "compose", "version"],
        fixture,
        child_env,
    )
    if code:
        add(
            "compose-plugin",
            "FAIL" if code == 124 else "BLOCKED",
            problem or ("timeout" if code == 124 else "plugin-unavailable"),
            code,
        )
        add("compose-config-render", "BLOCKED", "prerequisite-blocked")
        add("compose-structure", "BLOCKED", "prerequisite-blocked")
        return
    add("compose-plugin", "PASS", "available", 0)
    code, _, problem = child(
        [str(tools["docker"]), "compose", "config", "--quiet"],
        fixture,
        child_env,
    )
    record_child("compose-config-render", code, problem)
    if code:
        add("compose-structure", "BLOCKED", "prerequisite-blocked")
        return
    validator = fixture / "scripts/validation/validate-docker-compose.sh"
    code, _, problem = child(
        [str(tools["bash"]), str(validator)],
        fixture,
        child_env,
    )
    record_child("compose-structure", code, problem)
try:
    main()
except (OSError, UnicodeError, ValueError, TypeError, yaml.YAMLError) as error:
    safe_category = str(error)
    if safe_category not in {
        "external-absolute-path",
        "missing-graph-input",
        "unresolved-path-interpolation",
        "unsupported-input-graph",
        "unsafe-input-graph",
        "unsafe-tracked-file",
    }:
        safe_category = "unsafe-input-graph"
    if "input-graph" not in results and "tracked-snapshot" in results:
        add("input-graph", "BLOCKED", safe_category)
    elif "tracked-snapshot" not in results:
        add("tracked-snapshot", "BLOCKED", safe_category)
    else:
        add("controller", "BLOCKED", safe_category)
    block_unset()
except Exception:
    add("controller", "BLOCKED", "internal-error")
    block_unset()
finally:
    add("runtime-observation", "NOT_RUN", "needs-separate-approval")
    add("secret-values", "NOT_RUN", "out-of-scope")
    cleanup_ok = cleanup()
    add(
        "fixture-cleanup",
        "PASS" if cleanup_ok else "BLOCKED",
        "verified" if cleanup_ok else "cleanup-refused",
    )
counts = collections.Counter(state for state, _, _ in results.values())
for check, (state, category, code) in results.items():
    child_exit = str(code) if code is not None else "NA"
    print(f"{check} {state} category={category} child_exit={child_exit}"[:4096])
print("summary " + " ".join(f"{state}={counts[state]}" for state in STATES))
raise SystemExit(1 if counts["FAIL"] else 2 if counts["BLOCKED"] else 0)
PY
