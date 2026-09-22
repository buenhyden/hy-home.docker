"""Value-preserving metadata synchronization through the public shell entrypoint."""

import os
import posixpath
import re
import shlex
import subprocess
import tempfile
import unittest
from collections import Counter, defaultdict
from pathlib import Path

import yaml

SCRIPT = Path(__file__).resolve().parents[2] / "scripts/operations/gen-secrets.sh"
ROOT = SCRIPT.parents[2]
MIGRATION_COMPOSE = "infra/03-security/vault/docker-compose.yml"
INDIRECT_DERIVED_INPUTS = {
    "DEFAULT_DOCKER_PROJECT_PATH",
    "DEFAULT_MOUNT_VOLUME_PATH",
}
HTPASSWD_ID_INPUTS = {"ELASTIC_USERNAME", "TRAEFIK_ADMIN_USERNAME"}
REGISTRY_PATH_EXCEPTIONS = {
    "INFRA-002": "secrets/auth/traefik_admin_password.txt",
    "SEC-001": "secrets/security/vault_token.txt",
}
HOST_INTERPOLATION_KEYS = {"HOME"}
CONFIG_SUFFIXES = {
    "",
    ".cfg",
    ".conf",
    ".ini",
    ".json",
    ".sh",
    ".toml",
    ".yaml",
    ".yml",
}
INTERPOLATION = re.compile(
    r"(?<!\$)\$\{(?P<name>[A-Za-z_][A-Za-z0-9_]*)"
    r"(?P<operator>:-|-|:\+|\+|:\?|\?)?[^}]*\}"
)
LITERAL_SECRET = re.compile(
    r"/run/secrets/(?P<name>[A-Za-z0-9][A-Za-z0-9_.-]*)"
    r"(?![A-Za-z0-9_.-])"
)
RUNTIME_PATH = re.compile(r"(?<![A-Za-z0-9_.-])(?:/|\./|\.\./)[A-Za-z0-9_./-]+")


def walk_scalars(value):
    if isinstance(value, dict):
        for key, item in value.items():
            yield from walk_scalars(key)
            yield from walk_scalars(item)
    elif isinstance(value, list):
        for item in value:
            yield from walk_scalars(item)
    elif isinstance(value, str):
        yield value


def compose_sources(root=ROOT):
    root_text = (root / "docker-compose.yml").read_text()
    document = yaml.safe_load(root_text)
    sources = {"docker-compose.yml": root_text}
    for entry in document.get("include", []):
        relative = entry if isinstance(entry, str) else entry["path"]
        sources[relative] = (root / relative).read_text()
    return sources


def env_assignments(text):
    result = {}
    for line in text.splitlines():
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)=(.*)$", line)
        if match:
            result[match[1]] = match[2]
    return result


def interpolation_references(text):
    return [
        (match["name"], match["operator"]) for match in INTERPOLATION.finditer(text)
    ]


def environment_contract(compose_texts, env_text):
    public = set(env_assignments(env_text))
    references = defaultdict(list)
    for relative, text in compose_texts.items():
        document = yaml.safe_load(text)
        for scalar in walk_scalars(document):
            for name, operator in interpolation_references(scalar):
                references[name].append((relative, operator))

    compose_keys = set(references)
    missing = compose_keys - public - HOST_INTERPOLATION_KEYS
    env_derived = {
        name
        for value in env_assignments(env_text).values()
        for name, _ in interpolation_references(value)
    }
    derived_only = env_derived - compose_keys
    consumed = (compose_keys & public) | derived_only | HTPASSWD_ID_INPUTS
    orphan = public - consumed
    migration_only = {
        name
        for name, uses in references.items()
        if name in public and {relative for relative, _ in uses} == {MIGRATION_COMPOSE}
    }
    required = {
        name
        for name, uses in references.items()
        if name in public and any(operator in (None, "?", ":?") for _, operator in uses)
    }
    required |= derived_only | HTPASSWD_ID_INPUTS
    required -= migration_only
    optional = public - required - migration_only - orphan
    return {
        "public": public,
        "missing": missing,
        "derived_only": derived_only,
        "consumed": consumed,
        "orphan": orphan,
        "required": required,
        "optional": optional,
        "migration_only": migration_only,
    }


def registry_rows(text):
    result = {}
    for line in text.splitlines():
        cells = [cell.strip().strip("*" + chr(96)).strip() for cell in line.split("|")]
        if len(cells) == 10 and re.fullmatch(r"[A-Z][A-Z0-9_-]*-[0-9]+", cells[1]):
            result[cells[1]] = {"env": cells[5], "path": cells[6]}
    return result


def literal_secret_names(text):
    return {match["name"] for match in LITERAL_SECRET.finditer(text)}


def service_grants(service):
    grants = {}
    for grant in service.get("secrets", []) or []:
        if isinstance(grant, str):
            grants[grant] = grant
        else:
            source = grant["source"]
            grants[grant.get("target", source)] = source
    return grants


def volume_source(volume):
    if isinstance(volume, dict):
        if volume.get("type") != "bind":
            return None
        return volume.get("source")
    match = re.match(r"^(?P<source>.+?):/[^:]+(?::[^:]+)?$", volume)
    return match["source"] if match else None


def tracked_files(root):
    root = Path(os.path.abspath(root))
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=root,
        check=True,
        capture_output=True,
    )
    return {
        root / os.fsdecode(relative)
        for relative in result.stdout.split(b"\0")
        if relative
    }


def has_symlink_component(root, path):
    root = Path(os.path.abspath(root))
    path = Path(os.path.abspath(path))
    if not path.is_relative_to(root):
        return True
    current = root
    if current.is_symlink():
        return True
    for part in path.relative_to(root).parts:
        current /= part
        if current.is_symlink():
            return True
    return False


def mounted_config_files(root, compose_path, service, tracked):
    root = Path(os.path.abspath(root))
    base = (root / compose_path).parent
    seen = set()
    for volume in service.get("volumes", []) or []:
        source = volume_source(volume)
        if not source or not source.startswith("."):
            continue
        prefix = source.split("${", 1)[0]
        if not prefix:
            continue
        candidate = Path(os.path.abspath(base / prefix))
        if "${" in source and not prefix.endswith("/"):
            candidate = candidate.parent
        if (
            not candidate.is_relative_to(root)
            or candidate.is_relative_to(root / "secrets")
            or has_symlink_component(root, candidate)
        ):
            continue
        files = [candidate] if candidate.is_file() else sorted(candidate.rglob("*"))
        for path in files:
            path = Path(os.path.abspath(path))
            if (
                path in seen
                or has_symlink_component(root, path)
                or path not in tracked
                or not path.is_file()
                or path.suffix not in CONFIG_SUFFIXES
            ):
                continue
            seen.add(path)
            yield path


def compose_default(value):
    match = re.fullmatch(r"\$\{[A-Za-z_][A-Za-z0-9_]*:-([^}]+)\}", value)
    return match[1] if match else value


def final_stage_instructions(logical_lines):
    instructions = []
    for line in logical_lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        instruction, _, arguments = stripped.partition(" ")
        upper = instruction.upper()
        if upper == "FROM":
            instructions = []
        instructions.append((upper, arguments))
    return instructions


def docker_runtime(instructions, service):
    workdir = None
    defaults = {"CMD": None, "ENTRYPOINT": None}
    for instruction, arguments in instructions:
        if instruction == "WORKDIR":
            if "$" in arguments:
                workdir = None
            elif posixpath.isabs(arguments):
                workdir = posixpath.normpath(arguments)
            elif workdir is not None:
                workdir = posixpath.normpath(posixpath.join(workdir, arguments))
        elif instruction in defaults:
            defaults[instruction] = arguments

    runtime_parts = []
    if "entrypoint" in service:
        runtime_parts.extend(walk_scalars(service["entrypoint"]))
    elif defaults["ENTRYPOINT"] is not None:
        runtime_parts.append(defaults["ENTRYPOINT"])
    if "command" in service:
        runtime_parts.extend(walk_scalars(service["command"]))
    elif defaults["CMD"] is not None:
        runtime_parts.append(defaults["CMD"])
    runtime_paths = {
        match.group(0)
        for part in runtime_parts
        for match in RUNTIME_PATH.finditer(part)
    }
    return workdir, runtime_paths


def installed_copy_references(destination, source, workdir):
    installed = destination
    if destination.endswith("/"):
        installed += posixpath.basename(source.rstrip("/"))
    if not posixpath.isabs(installed):
        if workdir is None:
            return {installed}
        installed = posixpath.join(workdir, installed)
    installed = posixpath.normpath(installed)
    references = {installed}
    if workdir is not None:
        relative = posixpath.relpath(installed, workdir)
        if relative != "." and relative != ".." and not relative.startswith("../"):
            references |= {relative, f"./{relative}"}
    return references


def dockerfile_input_files(root, compose_path, service, tracked):
    root = Path(os.path.abspath(root))
    build = service.get("build")
    if not build:
        return
    context_value = build if isinstance(build, str) else build.get("context", ".")
    context_value = compose_default(context_value)
    if "${" in context_value or "://" in context_value:
        return
    context = Path(os.path.abspath((root / compose_path).parent / context_value))
    if (
        not context.is_relative_to(root)
        or context.is_relative_to(root / "secrets")
        or has_symlink_component(root, context)
        or not context.is_dir()
    ):
        return

    dockerfile_value = "Dockerfile"
    if isinstance(build, dict):
        dockerfile_value = compose_default(build.get("dockerfile", dockerfile_value))
    if "${" in dockerfile_value:
        return
    dockerfile = Path(os.path.abspath(context / dockerfile_value))
    if (
        dockerfile not in tracked
        or not dockerfile.is_relative_to(context)
        or has_symlink_component(root, dockerfile)
        or not dockerfile.is_file()
    ):
        return
    logical_lines = dockerfile.read_text().replace("\\\n", " ").splitlines()
    instructions = final_stage_instructions(logical_lines)
    workdir, runtime_paths = docker_runtime(instructions, service)

    for instruction, arguments in instructions:
        if instruction not in {"ADD", "COPY"}:
            continue
        tokens = shlex.split(arguments)
        flags = []
        while tokens and tokens[0].startswith("--"):
            flags.append(tokens.pop(0))
        if any(flag.startswith("--from=") for flag in flags) or len(tokens) < 2:
            continue
        destination = tokens[-1]
        for source in tokens[:-1]:
            if "${" in source or "://" in source or Path(source).is_absolute():
                continue
            if not (
                installed_copy_references(destination, source, workdir) & runtime_paths
            ):
                continue
            for candidate in context.glob(source):
                candidate = Path(os.path.abspath(candidate))
                if (
                    not candidate.is_relative_to(context)
                    or candidate.is_relative_to(root / "secrets")
                    or has_symlink_component(root, candidate)
                ):
                    continue
                candidates = (
                    [candidate] if candidate.is_file() else sorted(candidate.rglob("*"))
                )
                for path in candidates:
                    path = Path(os.path.abspath(path))
                    if (
                        not path.is_relative_to(context)
                        or path.is_relative_to(root / "secrets")
                        or has_symlink_component(root, path)
                        or path not in tracked
                        or not path.is_file()
                    ):
                        continue
                    yield path


def service_secret_contract(root, compose_texts):
    services = {}
    tracked = tracked_files(root)
    for relative, text in compose_texts.items():
        if relative == "docker-compose.yml":
            continue
        document = yaml.safe_load(text) or {}
        for name, service in (document.get("services") or {}).items():
            grants = service_grants(service)
            references = set()
            for scalar in walk_scalars(service):
                references |= literal_secret_names(scalar)
            source_files = set(
                mounted_config_files(root, relative, service, tracked)
            ) | set(dockerfile_input_files(root, relative, service, tracked))
            for path in source_files:
                references |= literal_secret_names(
                    path.read_bytes().decode("utf-8", errors="ignore")
                )
            services[name] = {"grants": grants, "references": references}
    return services


def secret_contract(root, compose_texts, registry_text, consumed_env):
    root_document = yaml.safe_load(compose_texts["docker-compose.yml"])
    declarations = root_document["secrets"]
    declaration_paths = {
        name: value["file"].removeprefix("./")
        for name, value in declarations.items()
        if "file" in value
    }
    services = service_secret_contract(root, compose_texts)
    dangling = set()
    missing_grants = set()
    granted_sources = set()
    for service_name, contract in services.items():
        grants = contract["grants"]
        granted_sources.update(grants.values())
        for reference in contract["references"]:
            source = grants.get(reference)
            if source is None:
                missing_grants.add((service_name, reference))
                if reference not in declarations:
                    dangling.add((service_name, reference))
            elif source not in declarations:
                dangling.add((service_name, reference))

    rows = registry_rows(registry_text)
    registered_paths = {
        row["path"] for row in rows.values() if row["path"] not in ("", "-")
    }
    expected_exceptions = set(REGISTRY_PATH_EXCEPTIONS.items())
    registry_orphans = {
        (identity, row["path"])
        for identity, row in rows.items()
        if row["env"] not in consumed_env
        and row["path"] not in declaration_paths.values()
        and (identity, row["path"]) not in expected_exceptions
    }
    return {
        "declarations": set(declarations),
        "declaration_paths": set(declaration_paths.values()),
        "granted_sources": granted_sources,
        "dangling": dangling,
        "missing_grants": missing_grants,
        "rows": rows,
        "registered_paths": registered_paths,
        "registry_orphans": registry_orphans,
    }


class SecretMetadataSyncTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        (self.root / "secrets").mkdir()
        self.example = self.root / "secrets/SENSITIVE_ENV_VARS.md.example"
        self.target = self.root / "secrets/SENSITIVE_ENV_VARS.md"
        self.example.write_text(
            "| **TEST-001** | `X` | `PW` | `(empty)` | `NEW_KEY` | `secrets/test.txt` | 2026-01-01 | New purpose |\n"
        )
        self.private = "| **TEST-001** | `O` | `PW` | `synthetic-private-value` | `OLD_KEY` | `secrets/old.txt` | 2025-01-01 | Old purpose |\n"
        self.target.write_text(self.private)
        (self.root / ".env.example").write_text("EXISTING=public\nADDED=default\n")
        (self.root / ".env").write_text(
            "# operator comment\nEXISTING=synthetic-private-env\nUNKNOWN=keep\n"
        )

    def run_mode(self, mode="--sync-metadata"):
        result = subprocess.run(
            ["bash", str(SCRIPT), mode],
            cwd=self.root,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotIn("synthetic-private", result.stdout + result.stderr)
        return result

    def test_preserves_values_dates_unknown_rows_and_env_bytes(self):
        unknown = "| **LOCAL-001** | `X` | `PW` | `synthetic-private-local` | `-` | | 2025-01-01 | Local |\n"
        self.target.write_text(self.private + unknown)
        result = self.run_mode()
        self.assertEqual(0, result.returncode, result.stderr)
        text = self.target.read_text()
        self.assertIn("`synthetic-private-value`", text)
        self.assertIn("2025-01-01", text)
        self.assertIn(unknown, text)
        self.assertIn("`NEW_KEY`", text)
        self.assertEqual(
            "# operator comment\nEXISTING=synthetic-private-env\nUNKNOWN=keep\nADDED=default\n",
            (self.root / ".env").read_text(),
        )
        self.assertFalse((self.root / "secrets/test.txt").exists())
        self.assertEqual(0, self.run_mode().returncode)

    def test_check_reports_drift_without_writes(self):
        before = self.target.read_bytes()
        result = self.run_mode("--sync-metadata-check")
        self.assertEqual(1, result.returncode)
        self.assertEqual(before, self.target.read_bytes())
        self.assertEqual(0, self.run_mode().returncode)
        self.assertEqual(0, self.run_mode("--sync-metadata-check").returncode)

    def test_rejects_traversal_without_any_writes(self):
        self.example.write_text(
            self.example.read_text().replace("secrets/test.txt", "secrets/../../escape")
        )
        before = self.target.read_bytes()
        self.assertEqual(2, self.run_mode().returncode)
        self.assertEqual(before, self.target.read_bytes())
        self.assertNotIn("ADDED=", (self.root / ".env").read_text())

    def test_rejects_symlink_target(self):
        outside = self.root / "outside"
        outside.write_text(self.private)
        self.target.unlink()
        self.target.symlink_to(outside)
        self.assertEqual(2, self.run_mode().returncode)
        self.assertEqual(self.private, outside.read_text())

    def test_rejects_symlink_environment_target(self):
        outside = self.root / "outside-env"
        outside.write_text("EXISTING=synthetic-private-env\n")
        environment = self.root / ".env"
        environment.unlink()
        environment.symlink_to(outside)
        registry_before = self.target.read_bytes()

        self.assertEqual(2, self.run_mode().returncode)
        self.assertEqual("EXISTING=synthetic-private-env\n", outside.read_text())
        self.assertEqual(registry_before, self.target.read_bytes())

    def test_rejects_nonregular_registry_target_before_any_write(self):
        environment = self.root / ".env"
        environment_before = environment.read_bytes()
        self.target.unlink()
        self.target.mkdir()

        self.assertEqual(2, self.run_mode().returncode)
        self.assertTrue(self.target.is_dir())
        self.assertEqual(environment_before, environment.read_bytes())

    def test_rejects_nonregular_environment_target_before_any_write(self):
        registry_before = self.target.read_bytes()
        environment = self.root / ".env"
        environment.unlink()
        environment.mkdir()

        self.assertEqual(2, self.run_mode().returncode)
        self.assertTrue(environment.is_dir())
        self.assertEqual(registry_before, self.target.read_bytes())

    def test_rejects_duplicate_public_identity(self):
        self.example.write_text(self.example.read_text() * 2)
        self.assertEqual(2, self.run_mode().returncode)
        self.assertEqual(self.private, self.target.read_text())

    def test_rejects_unparseable_value_without_exposure(self):
        body = self.private.replace(
            "synthetic-private-value", "synthetic-private|ambiguous"
        )
        self.target.write_text(body)
        self.assertEqual(2, self.run_mode().returncode)
        self.assertEqual(body, self.target.read_text())

    def test_new_registry_and_env_use_public_placeholders_only(self):
        self.target.unlink()
        (self.root / ".env").unlink()
        self.assertEqual(0, self.run_mode().returncode)
        self.assertEqual(self.example.read_bytes(), self.target.read_bytes())
        self.assertEqual(0o600, self.target.stat().st_mode & 0o777)
        self.assertEqual(0o600, (self.root / ".env").stat().st_mode & 0o777)

    def test_mode_only_drift_is_reported_and_atomically_normalized(self):
        self.assertEqual(0, self.run_mode().returncode)
        targets = (self.target, self.root / ".env")
        for target in targets:
            for unsafe_mode in (0o644, 0o660):
                with self.subTest(target=target.name, unsafe_mode=oct(unsafe_mode)):
                    for candidate in targets:
                        candidate.chmod(0o600)
                    target.chmod(unsafe_mode)
                    before = target.read_bytes()

                    self.assertEqual(
                        1, self.run_mode("--sync-metadata-check").returncode
                    )
                    self.assertEqual(before, target.read_bytes())
                    self.assertEqual(unsafe_mode, target.stat().st_mode & 0o777)

                    self.assertEqual(0, self.run_mode().returncode)
                    self.assertEqual(before, target.read_bytes())
                    self.assertEqual(0o600, target.stat().st_mode & 0o777)

    def test_second_replacement_failure_rolls_back_bytes_and_mode(self):
        self.assertEqual(0, self.run_mode().returncode)
        self.example.write_text(
            self.example.read_text()
            + "| **TEST-002** | `X` | `PW` | `(empty)` | `-` | "
            "`secrets/second.txt` | 2026-01-02 | Second purpose |\n"
        )
        (self.root / ".env.example").write_text(
            (self.root / ".env.example").read_text() + "SECOND=public\n"
        )
        self.target.chmod(0o660)
        registry_before = self.target.read_bytes()
        environment = self.root / ".env"
        environment_before = environment.read_bytes()
        original_root_mode = self.root.stat().st_mode & 0o777

        try:
            self.root.chmod(0o500)
            result = self.run_mode()
        finally:
            self.root.chmod(original_root_mode)

        self.assertEqual(2, result.returncode)
        self.assertEqual(registry_before, self.target.read_bytes())
        self.assertEqual(0o660, self.target.stat().st_mode & 0o777)
        self.assertEqual(environment_before, environment.read_bytes())
        self.assertEqual(0o600, environment.stat().st_mode & 0o777)

    def test_preserving_mode_keeps_unparsed_environment_lines(self):
        env_text = "# operator comment\nsource local-overrides.env\nEXISTING=synthetic-private-env\n"
        (self.root / ".env").write_text(env_text)

        result = self.run_mode()

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(env_text + "ADDED=default\n", (self.root / ".env").read_text())

    def test_prune_makes_public_and_private_key_sets_exact(self):
        self.example.write_text(
            self.example.read_text()
            + "| **TEST-002** | `O` | `PW` | `(empty)` | `ADDED` | `secrets/added.txt` | 2026-01-02 | Added purpose |\n"
        )
        unknown = (
            "| **LOCAL-001** | `X` | `PW` | `synthetic-private-local` | "
            "`UNKNOWN` | `secrets/local.txt` | 2025-01-03 | Local purpose |\n"
        )
        self.target.write_text("# registry comment\n" + self.private + unknown)
        secret_file = self.root / "secrets/local.txt"
        secret_file.write_text("synthetic-secret-file")
        before_retained = self.private.split("|")
        before_env_line = "EXISTING=synthetic-private-env\n"

        result = self.run_mode("--sync-metadata-prune")

        self.assertEqual(0, result.returncode, result.stderr)
        env_text = (self.root / ".env").read_text()
        self.assertEqual(
            "# operator comment\n" + before_env_line + "ADDED=default\n",
            env_text,
        )
        self.assertEqual(
            {"EXISTING", "ADDED"},
            {
                line.split("=", 1)[0]
                for line in env_text.splitlines()
                if line and not line.startswith("#")
            },
        )
        registry = self.target.read_text()
        self.assertIn("# registry comment\n", registry)
        self.assertNotIn("LOCAL-001", registry)
        rows = [
            line.split("|") for line in registry.splitlines() if line.startswith("| **")
        ]
        self.assertEqual({"TEST-001", "TEST-002"}, {row[1].strip("* ") for row in rows})
        retained = next(row for row in rows if "TEST-001" in row[1])
        self.assertEqual(before_retained[4], retained[4])
        self.assertEqual(before_retained[7], retained[7])
        self.assertEqual("NEW_KEY", retained[5].strip(" `"))
        self.assertTrue(secret_file.is_file())
        self.assertEqual("synthetic-secret-file", secret_file.read_text())

        env_before = (self.root / ".env").read_bytes()
        registry_before = self.target.read_bytes()
        self.assertEqual(0, self.run_mode("--sync-metadata-prune-check").returncode)
        self.assertEqual(0, self.run_mode("--sync-metadata-prune").returncode)
        self.assertEqual(env_before, (self.root / ".env").read_bytes())
        self.assertEqual(registry_before, self.target.read_bytes())

    def test_prune_check_reports_exact_set_drift_without_writes(self):
        registry_before = self.target.read_bytes()
        env_before = (self.root / ".env").read_bytes()

        result = self.run_mode("--sync-metadata-prune-check")

        self.assertEqual(1, result.returncode)
        self.assertEqual(registry_before, self.target.read_bytes())
        self.assertEqual(env_before, (self.root / ".env").read_bytes())
        self.assertEqual(0, self.run_mode("--sync-metadata-prune").returncode)
        self.assertEqual(0, self.run_mode("--sync-metadata-prune-check").returncode)

    def test_prune_rejects_multiline_environment_forms_before_any_write(self):
        cases = (
            'EXISTING="synthetic-private\ncontinued"\nUNKNOWN=keep\n',
            "EXISTING=synthetic-private\\\ncontinued\nUNKNOWN=keep\n",
        )
        for env_text in cases:
            with self.subTest(env_text=repr(env_text)):
                (self.root / ".env").write_text(env_text)
                registry_before = self.target.read_bytes()
                env_before = (self.root / ".env").read_bytes()

                result = self.run_mode("--sync-metadata-prune")

                self.assertEqual(2, result.returncode)
                self.assertEqual(registry_before, self.target.read_bytes())
                self.assertEqual(env_before, (self.root / ".env").read_bytes())

    def test_prune_rejects_duplicate_environment_key_before_any_write(self):
        (self.root / ".env.example").write_text(
            "EXISTING=public\nADDED=default\nEXISTING=duplicate\n"
        )
        registry_before = self.target.read_bytes()
        env_before = (self.root / ".env").read_bytes()

        result = self.run_mode("--sync-metadata-prune")

        self.assertEqual(2, result.returncode)
        self.assertEqual(registry_before, self.target.read_bytes())
        self.assertEqual(env_before, (self.root / ".env").read_bytes())

    def test_prune_rejects_malformed_registry_row_before_any_write(self):
        self.target.write_text(
            self.private
            + "| BROKEN | `X` | `PW` | `(empty)` | `-` | `-` | 2025-01-01 | Bad |\n"
        )
        registry_before = self.target.read_bytes()
        env_before = (self.root / ".env").read_bytes()

        result = self.run_mode("--sync-metadata-prune")

        self.assertEqual(2, result.returncode)
        self.assertEqual(registry_before, self.target.read_bytes())
        self.assertEqual(env_before, (self.root / ".env").read_bytes())

    def test_prune_rejects_symlink_source_before_any_write(self):
        outside = self.root / "outside-env-example"
        outside.write_text("EXISTING=public\nADDED=default\n")
        (self.root / ".env.example").unlink()
        (self.root / ".env.example").symlink_to(outside)
        registry_before = self.target.read_bytes()
        env_before = (self.root / ".env").read_bytes()

        result = self.run_mode("--sync-metadata-prune")

        self.assertEqual(2, result.returncode)
        self.assertEqual(registry_before, self.target.read_bytes())
        self.assertEqual(env_before, (self.root / ".env").read_bytes())


class PublicSecretSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.compose_texts = compose_sources()
        cls.env_text = (ROOT / ".env.example").read_text()
        cls.environment = environment_contract(cls.compose_texts, cls.env_text)
        cls.registry_text = (ROOT / "secrets/SENSITIVE_ENV_VARS.md.example").read_text()

    def test_public_environment_has_current_consumers_and_five_way_classification(self):
        contract = self.environment
        self.assertEqual(266, len(contract["public"]))
        self.assertEqual(set(), contract["missing"])
        self.assertEqual(set(), contract["orphan"])
        self.assertEqual(INDIRECT_DERIVED_INPUTS, contract["derived_only"])
        self.assertEqual(
            {"VAULT_CLUSTER_PORT", "VAULT_PORT"}, contract["migration_only"]
        )
        self.assertEqual(59, len(contract["required"]))
        self.assertEqual(205, len(contract["optional"]))
        self.assertEqual(
            contract["public"],
            contract["required"]
            | contract["optional"]
            | contract["migration_only"]
            | contract["orphan"],
        )

    def test_environment_scanner_mutations_fail_closed_without_shell_false_positives(
        self,
    ):
        mutated = dict(self.compose_texts)
        mutated["synthetic.yml"] = (
            "services:\n"
            "  scanner-probe:\n"
            "    image: example:latest\n"
            "    environment:\n"
            "      REQUIRED: '${UNDECLARED_CONTRACT_KEY}'\n"
            "      RUNTIME_ONLY: '$$RUNTIME_VALUE $${RUNTIME_TEMPLATE}'\n"
        )
        contract = environment_contract(mutated, self.env_text)
        self.assertEqual({"UNDECLARED_CONTRACT_KEY"}, contract["missing"])

        with_orphan = self.env_text + "\nUNUSED_CONTRACT_KEY=value\n"
        contract = environment_contract(self.compose_texts, with_orphan)
        self.assertIn("UNUSED_CONTRACT_KEY", contract["orphan"])

        outside_migration = dict(self.compose_texts)
        outside_migration["synthetic.yml"] = (
            "services:\n  scanner-probe:\n"
            "    image: example:latest\n"
            "    environment:\n      PORT: '${VAULT_PORT}'\n"
        )
        contract = environment_contract(outside_migration, self.env_text)
        self.assertNotIn("VAULT_PORT", contract["migration_only"])

    def test_literal_secret_references_are_declared_granted_and_registered(self):
        contract = secret_contract(
            ROOT,
            self.compose_texts,
            self.registry_text,
            self.environment["consumed"],
        )
        self.assertEqual(75, len(contract["declarations"]))
        self.assertEqual(103, len(contract["rows"]))
        self.assertEqual(set(), contract["dangling"])
        self.assertEqual(set(), contract["missing_grants"])
        self.assertEqual(contract["declarations"], contract["granted_sources"])
        self.assertEqual(
            set(), contract["declaration_paths"] - contract["registered_paths"]
        )
        self.assertEqual(
            set(REGISTRY_PATH_EXCEPTIONS.values()),
            contract["registered_paths"] - contract["declaration_paths"],
        )
        self.assertEqual(set(), contract["registry_orphans"])
        self.assertEqual(
            set(REGISTRY_PATH_EXCEPTIONS.items()),
            {
                (identity, contract["rows"][identity]["path"])
                for identity in REGISTRY_PATH_EXCEPTIONS
            },
        )

    def test_secret_scanner_mutations_detect_dangling_grant_and_registry_drift(self):
        observability_path = "infra/06-observability/docker-compose.yml"
        observability = yaml.safe_load(self.compose_texts[observability_path])
        observability["services"]["prometheus"].setdefault("environment", {})[
            "DANGLING_FILE"
        ] = "/run/secrets/missing_literal"
        mutated = dict(self.compose_texts)
        mutated[observability_path] = yaml.safe_dump(observability)
        contract = secret_contract(
            ROOT, mutated, self.registry_text, self.environment["consumed"]
        )
        self.assertIn(("prometheus", "missing_literal"), contract["dangling"])

        observability = yaml.safe_load(self.compose_texts[observability_path])
        observability["services"]["prometheus"]["secrets"].remove("openbao_token")
        mutated[observability_path] = yaml.safe_dump(observability)
        contract = secret_contract(
            ROOT, mutated, self.registry_text, self.environment["consumed"]
        )
        self.assertIn(("prometheus", "openbao_token"), contract["missing_grants"])

        observability = yaml.safe_load(self.compose_texts[observability_path])
        observability["services"]["loki"]["secrets"] = ["grafana_admin_password"]
        mutated[observability_path] = yaml.safe_dump(observability)
        contract = secret_contract(
            ROOT, mutated, self.registry_text, self.environment["consumed"]
        )
        self.assertIn(("loki", "minio_app_user_password"), contract["missing_grants"])

        registry = (
            self.registry_text + "\n| **TEST-999** | X | Token | (empty) | - | "
            "secrets/security/unmapped.txt | 2026-09-20 | Mutation probe |\n"
        )
        contract = secret_contract(
            ROOT, self.compose_texts, registry, self.environment["consumed"]
        )
        self.assertIn(
            ("TEST-999", "secrets/security/unmapped.txt"),
            contract["registry_orphans"],
        )

    def test_secret_scanner_detects_n8n_workdir_entrypoint_grant_swap(self):
        n8n_path = "infra/07-workflow/n8n/docker-compose.yml"
        n8n = yaml.safe_load(self.compose_texts[n8n_path])
        n8n["services"]["n8n"]["secrets"] = [
            "grafana_admin_password" if grant == "mng_valkey_password" else grant
            for grant in n8n["services"]["n8n"]["secrets"]
        ]
        mutated = dict(self.compose_texts)
        mutated[n8n_path] = yaml.safe_dump(n8n)

        contract = secret_contract(
            ROOT, mutated, self.registry_text, self.environment["consumed"]
        )

        self.assertIn(("n8n", "mng_valkey_password"), contract["missing_grants"])

    def test_literal_secret_scanner_ignores_templated_secret_names(self):
        self.assertEqual(
            {"fixed_name"},
            literal_secret_names(
                "/run/secrets/fixed_name /run/secrets/${SECRET_NAME} "
                "/run/secrets/${SECRET_NAME:-fallback}"
            ),
        )

    def test_build_source_scanner_stays_local_and_git_tracked(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            context = root / "stack/image"
            context.mkdir(parents=True)
            dockerfile = context / "Dockerfile"
            entrypoint = context / "docker-entrypoint.sh"
            dockerfile.write_text(
                "FROM example:latest\n"
                "COPY docker-entrypoint.sh /docker-entrypoint.sh\n"
                'ENTRYPOINT ["/docker-entrypoint.sh"]\n'
            )
            entrypoint.write_text("cat /run/secrets/private_probe\n")
            service = {"build": {"context": "./image"}}

            self.assertEqual(
                [],
                list(
                    dockerfile_input_files(
                        root, "stack/docker-compose.yml", service, {dockerfile}
                    )
                ),
            )
            self.assertEqual(
                {entrypoint},
                set(
                    dockerfile_input_files(
                        root,
                        "stack/docker-compose.yml",
                        service,
                        {dockerfile, entrypoint},
                    )
                ),
            )
            dockerfile.write_text(
                "FROM example:latest\n"
                "COPY docker-entrypoint.sh /docker-entrypoint.sh\n"
                'ENTRYPOINT ["/docker-entrypoint.sh.backup"]\n'
            )
            self.assertEqual(
                [],
                list(
                    dockerfile_input_files(
                        root,
                        "stack/docker-compose.yml",
                        service,
                        {dockerfile, entrypoint},
                    )
                ),
            )
            self.assertEqual(
                [],
                list(
                    dockerfile_input_files(
                        root,
                        "stack/docker-compose.yml",
                        {"build": "https://example.invalid/context.git"},
                        {dockerfile, entrypoint},
                    )
                ),
            )

    def test_tracked_files_preserve_lexical_git_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            stack = root / "stack"
            stack.mkdir()
            private = root / "untracked-private.yml"
            private.write_text("password_file: /run/secrets/private_probe\n")
            tracked_link = stack / "config.yml"
            tracked_link.symlink_to(private)
            subprocess.run(["git", "add", "stack/config.yml"], cwd=root, check=True)

            self.assertEqual({tracked_link}, tracked_files(root))

    def test_mounted_config_scanner_rejects_tracked_symlink_before_read(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            stack = root / "stack"
            stack.mkdir()
            private = root / "untracked-private.yml"
            private.write_text("password_file: /run/secrets/private_probe\n")
            tracked_link = stack / "config.yml"
            tracked_link.symlink_to(private)
            subprocess.run(["git", "add", "stack/config.yml"], cwd=root, check=True)
            service = {"volumes": ["./config.yml:/etc/service/config.yml:ro"]}

            self.assertEqual(
                [],
                list(
                    mounted_config_files(
                        root,
                        "stack/docker-compose.yml",
                        service,
                        tracked_files(root),
                    )
                ),
            )

    def test_prometheus_uses_a_dedicated_openbao_metrics_token(self):
        root = SCRIPT.parents[2]
        declarations = yaml.safe_load((root / "docker-compose.yml").read_text())[
            "secrets"
        ]
        self.assertEqual(
            {"file": "./secrets/security/openbao_token.txt"},
            declarations.get("openbao_token"),
        )
        self.assertNotIn("vault_token", declarations)

        observability = yaml.safe_load(
            (root / "infra/06-observability/docker-compose.yml").read_text()
        )
        grants = observability["services"]["prometheus"]["secrets"]
        self.assertIn("openbao_token", grants)
        self.assertNotIn("vault_token", grants)

        for name in ("prometheus.yml", "prometheus.dev.yml"):
            config = yaml.safe_load(
                (root / "infra/06-observability/prometheus/config" / name).read_text()
            )
            jobs = {job["job_name"]: job for job in config["scrape_configs"]}
            self.assertNotIn("vault", jobs)
            self.assertEqual(
                "/run/secrets/openbao_token",
                jobs["openbao"]["bearer_token_file"],
            )

        policy = (
            root / "infra/03-security/openbao/config/policies/prometheus.hcl"
        ).read_text()
        self.assertEqual('path "sys/metrics" {\n  capabilities = ["read"]\n}\n', policy)

        registry = (root / "secrets/SENSITIVE_ENV_VARS.md.example").read_text()
        self.assertIn("**SEC-001**", registry)
        self.assertIn("**SEC-002**", registry)
        self.assertIn("secrets/security/openbao_token.txt", registry)

    def test_public_ids_paths_and_env_keys_have_unique_owners(self):
        root = SCRIPT.parents[2]
        text = (root / "secrets/SENSITIVE_ENV_VARS.md.example").read_text()
        rows = []
        for line in text.splitlines():
            cells = [cell.strip().strip("*`").strip() for cell in line.split("|")]
            if len(cells) == 10 and re.fullmatch(r"[A-Z][A-Z0-9_-]*-[0-9]+", cells[1]):
                rows.append(cells)
        for column in (1, 5, 6):
            counts = Counter(
                row[column] for row in rows if row[column] not in ("", "-")
            )
            self.assertEqual([], [name for name, count in counts.items() if count > 1])
        declarations = yaml.safe_load((root / "docker-compose.yml").read_text())[
            "secrets"
        ]
        expected = {
            value["file"].removeprefix("./")
            for value in declarations.values()
            if "file" in value
        }
        self.assertFalse(expected - {row[6] for row in rows})
        keys = re.findall(
            r"^([A-Za-z_][A-Za-z0-9_]*)=", (root / ".env.example").read_text(), re.M
        )
        self.assertEqual(len(keys), len(set(keys)))
        self.assertFalse(
            {row[5] for row in rows if row[5] not in ("", "-")} - set(keys)
        )
