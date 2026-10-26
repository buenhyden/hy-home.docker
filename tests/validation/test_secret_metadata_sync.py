"""Value-preserving metadata synchronization through the public shell entrypoint."""

import json
import os
import posixpath
import re
import shlex
import stat
import subprocess
import tempfile
import unittest
from collections import Counter, defaultdict
from pathlib import Path

import yaml

from scripts.lib.document_governance.operations_catalog import (
    _ComposeLoader,
    conftest_source_context,
)
from scripts.lib.ops import secret_catalog
from tests.lib.ops.test_secret_catalog import model as synthetic_catalog_model

SCRIPT = Path(__file__).resolve().parents[2] / "scripts/operations/gen-secrets.sh"
ROOT = SCRIPT.parents[2]
# DEFAULT_MOUNT_VOLUME_PATH left this set when the Restic job mounted it directly.
INDIRECT_DERIVED_INPUTS = {
    "DEFAULT_DOCKER_PROJECT_PATH",
}
HTPASSWD_ID_INPUTS = {
    "OPENSEARCH_ADMIN_USERNAME",
    "PROMETHEUS_API_USERNAME",
    "TRAEFIK_ADMIN_USERNAME",
}
REGISTRY_PATH_EXCEPTIONS = {
    "INFRA-002": "secrets/auth/traefik/traefik_admin_password.txt",
    "OBS-013": "secrets/observability/prometheus/prometheus_api_password.txt",
    "SEC-003": "secrets/security/openbao/openbao_unseal_keys.txt",
}
CUTOVER_REGISTRY_PATH_EXCEPTIONS = {
    "PG-020": "secrets/db/legacy-app/service_password.txt",
}
HOST_INTERPOLATION_KEYS = {"HOME"}
SUPABASE_CANONICAL_SECRET_PATHS = {
    "smtp_password": "secrets/communication/smtp/smtp_password.txt",
    "supabase_db_password": "secrets/db/mng-pg/supabase_password.txt",
    **{
        name: f"secrets/data/supabase/{name}.txt"
        for name in (
            "supabase_jwt_secret",
            "supabase_anon_key",
            "supabase_service_key",
            "supabase_dashboard_password",
            "supabase_secret_key_base",
            "supabase_vault_enc_key",
            "supabase_pg_meta_crypto_key",
            "supabase_openai_api_key",
            "supabase_logflare_private_token",
        )
    },
}
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
    document = yaml.load(root_text, Loader=_ComposeLoader)
    sources = {"docker-compose.yml": root_text}
    for entry in document.get("include", []):
        relative = entry if isinstance(entry, str) else entry["path"]
        sources[relative] = (root / relative).read_text()
    return sources


def lab_compose_sources(root=ROOT):
    return {
        str(path.relative_to(root)): path.read_text()
        for path in sorted((root / "labs").glob("*.yml"))
    }


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


def lab_controller_inputs():
    # scripts/operations/lab.py is the only non-Compose consumer of LAB inputs.
    source = (ROOT / "scripts/operations/lab.py").read_text(encoding="utf-8")
    return set(re.findall(r'env(?:\.get\(|\[)"(LAB_[A-Z0-9_]+)"', source))


def environment_contract(compose_texts, env_text, supplemental_ids=HTPASSWD_ID_INPUTS):
    public = set(env_assignments(env_text))
    references = defaultdict(list)
    for relative, text in compose_texts.items():
        document = yaml.load(text, Loader=_ComposeLoader)
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
    consumed = (compose_keys & public) | derived_only | supplemental_ids
    orphan = public - consumed
    required = {
        name
        for name, uses in references.items()
        if name in public and any(operator in (None, "?", ":?") for _, operator in uses)
    }
    required |= derived_only | supplemental_ids
    optional = public - required - orphan
    return {
        "public": public,
        "missing": missing,
        "derived_only": derived_only,
        "consumed": consumed,
        "orphan": orphan,
        "required": required,
        "optional": optional,
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
    from scripts.lib.ops.smtp_contract import ContractError
    from scripts.lib.ops.smtp_contract import grants as validated_grants

    normalized = []
    for grant in service.get("secrets", []) or []:
        if isinstance(grant, str):
            normalized.append(compose_default(grant))
        elif isinstance(grant, dict) and isinstance(grant.get("source"), str):
            item = dict(grant, source=compose_default(grant["source"]))
            if "target" in item and isinstance(item["target"], str):
                item["target"] = compose_default(item["target"])
            normalized.append(item)
        else:
            raise AssertionError("invalid secret grant")
    try:
        return {
            target: source
            for source, target in validated_grants({"secrets": normalized})
        }
    except ContractError:
        raise AssertionError("duplicate or invalid secret grant") from None


class SMTPSecretContractTests(unittest.TestCase):
    def test_public_smtp_has_one_value_owner_and_value_free_alias(self):
        from scripts.lib.ops.smtp_contract import metadata_retired

        public = (ROOT / "secrets/SENSITIVE_ENV_VARS.md.example").read_bytes()
        self.assertEqual(public, metadata_retired(public))
        self.assertNotIn("COMM-003", registry_rows(public.decode()))
        self.assertEqual(
            "secrets/communication/smtp/smtp_password.txt",
            registry_rows(public.decode())["COMM-002"]["path"],
        )

    def test_service_grants_rejects_collisions_and_malformed_references(self):
        for grants in (
            ["smtp_password", "smtp_password"],
            [{"source": "a", "target": "same"}, {"source": "b", "target": "same"}],
            [{"source": "a", "target": "one"}, {"source": "a", "target": "two"}],
            [{"target": "missing"}],
            [42],
            [{"source": "a", "target": 42}],
        ):
            with self.subTest(grants=grants), self.assertRaises(AssertionError):
                service_grants({"secrets": grants})


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
    return re.sub(r"\$\{[A-Za-z_][A-Za-z0-9_]*:-([^}]+)\}", r"\1", value)


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


# Services that read tracked source as data for static analysis (Conftest).
# The files they mount name secret paths that they never dereference, so those
# names are not references; test_source_analysis_services_hold_no_secrets keeps
# the exemption safe.
SOURCE_ANALYSIS_SERVICES = {"conftest"}


def activation_environment(service):
    environment = service.get("environment", {})
    if isinstance(environment, dict):
        pairs = tuple(environment.items())
    elif isinstance(environment, list):
        if any(not isinstance(value, str) or "=" not in value for value in environment):
            return None
        pairs = tuple(value.split("=", 1) for value in environment)
    else:
        return None
    if any(
        not isinstance(key, str) or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key)
        for key, _ in pairs
    ):
        return None
    if len({key for key, _ in pairs}) != len(pairs):
        return None
    return {key: compose_default(str(value)) for key, value in pairs}


def overlay_activation(base_path, name, service, base_grants, model):
    if model.get("x-hyhome-overlay", {}).get("base") != base_path:
        return None
    delta = model.get("services", {}).get(name)
    if not isinstance(delta, dict) or set(delta) - {"profiles"} != {
        "environment",
        "secrets",
    }:
        return None
    grants = service_grants(delta)
    if any(
        target in base_grants and base_grants[target] != source
        for target, source in grants.items()
    ):
        raise AssertionError("conflicting conditional overlay grant")
    selectors = activation_environment(delta)
    base_environment = activation_environment(service)
    if not selectors or base_environment is None:
        return None
    if any(
        value != "1" or base_environment.get(key, "0") != "0"
        for key, value in selectors.items()
    ):
        return None
    return tuple(sorted(selectors)), grants


def conditional_source_coverage(base_path, name, service, grants, sources, context):
    # Closed activation provenance; this does not prove arbitrary shell branches.
    provenance, conditional = (), {}
    for overlay_path, model in (context or {}).get("overlay_inputs", {}).items():
        activation = overlay_activation(base_path, name, service, grants, model)
        if activation is None:
            continue
        selectors, added = activation
        for reference in sorted(
            set().union(*(source["references"] for source in sources)) - set(grants)
        ):
            paths = tuple(
                sorted(
                    source["path"]
                    for source in sources
                    if reference in source["references"]
                    and all(
                        re.search(
                            r"\$\{" + re.escape(selector) + r":?-0\}", source["text"]
                        )
                        for selector in selectors
                    )
                )
            )
            if not paths or reference not in added:
                continue
            if reference in conditional and conditional[reference] != added[reference]:
                raise AssertionError("conflicting conditional overlay grant")
            conditional = conditional | {reference: added[reference]}
            provenance = (
                *provenance,
                (base_path, name, reference, str(overlay_path), selectors, paths),
            )
    return conditional, tuple(sorted(provenance))


def service_secret_contract(root, compose_texts, source_context=None):
    services = {}
    tracked = tracked_files(root)
    for relative, text in compose_texts.items():
        if relative == "docker-compose.yml":
            continue
        document = yaml.load(text, Loader=_ComposeLoader) or {}
        for name, service in (document.get("services") or {}).items():
            grants = service_grants(service)
            direct = set().union(
                *(
                    literal_secret_names(compose_default(value))
                    for value in walk_scalars(service)
                )
            )
            source_files = (
                set()
                if name in SOURCE_ANALYSIS_SERVICES
                else set(mounted_config_files(root, relative, service, tracked))
                | set(dockerfile_input_files(root, relative, service, tracked))
            )
            sources = tuple(
                {
                    "path": str(path.relative_to(root)),
                    "text": path.read_bytes().decode("utf-8", errors="ignore"),
                }
                for path in sorted(source_files)
            )
            sources = tuple(
                source
                | {"references": literal_secret_names(compose_default(source["text"]))}
                for source in sources
            )
            mounted = set().union(*(source["references"] for source in sources))
            conditional, provenance = conditional_source_coverage(
                relative, name, service, grants, sources, source_context
            )
            services[name] = {
                "base_path": relative,
                "base_grants": grants,
                "conditional_sources": conditional,
                "conditional_overlay_grants": provenance,
                "references": direct | mounted,
                "unresolved_refs": (direct - set(grants))
                | (mounted - set(grants) - set(conditional)),
            }
    return services


def secret_contract(
    root, compose_texts, registry_text, consumed_env, source_context=None
):
    declarations = {}
    declaration_paths = {}
    lab_secret_dir = env_assignments((root / "labs/.env.example").read_text())[
        "LAB_SECRET_DIR"
    ].strip('"')
    dangling = set()
    missing_grants = set()
    granted_sources = set()
    base_grants, conditional_overlay_grants = {}, ()
    root_domain = {
        name: text
        for name, text in compose_texts.items()
        if not name.startswith("labs/")
    }
    lab_domains = [
        {name: text} for name, text in compose_texts.items() if name.startswith("labs/")
    ]
    for domain in (root_domain, *lab_domains):
        domain_declarations = {}
        for relative, text in domain.items():
            document = yaml.load(text, Loader=_ComposeLoader) or {}
            for name, value in (document.get("secrets") or {}).items():
                if name in domain_declarations:
                    raise AssertionError(f"duplicate secret declaration: {name}")
                domain_declarations[name] = value
                if "file" not in value:
                    if name in declarations:
                        raise AssertionError(f"duplicate secret declaration: {name}")
                    declarations[name] = value
                    continue
                source = value["file"]
                if relative.startswith("labs/"):
                    source = re.sub(
                        r"^\$\{LAB_SECRET_DIR(?::[-?][^}]*)?\}",
                        lab_secret_dir,
                        source,
                    )
                if "${" in source or posixpath.isabs(source):
                    raise AssertionError(f"unresolved or absolute secret path: {name}")
                path = posixpath.normpath(
                    posixpath.join(posixpath.dirname(relative), source)
                )
                if path.startswith("../") or path == "..":
                    raise AssertionError(f"secret escaped repository: {name}")
                shared_supabase = relative == "labs/supabase.yml"
                if (
                    shared_supabase
                    and SUPABASE_CANONICAL_SECRET_PATHS.get(name) != path
                ):
                    raise AssertionError(
                        f"Supabase LAB secret is not canonical: {name}"
                    )
                if (
                    relative.startswith("labs/")
                    and not shared_supabase
                    and not path.startswith("secrets/labs/")
                ):
                    raise AssertionError(f"LAB secret escaped isolated path: {name}")
                if not relative.startswith("labs/") and path.startswith(
                    "secrets/labs/"
                ):
                    raise AssertionError(f"root secret entered LAB path: {name}")
                if name in declarations:
                    if not (
                        shared_supabase
                        and name == "smtp_password"
                        and declaration_paths.get(name) == path
                    ):
                        raise AssertionError(f"duplicate secret declaration: {name}")
                else:
                    declarations[name] = value
                    declaration_paths[name] = path
        for service_name, contract in service_secret_contract(
            root, domain, source_context
        ).items():
            grants = contract["base_grants"]
            base_grants = base_grants | {(contract["base_path"], service_name): grants}
            conditional = contract["conditional_sources"]
            conditional_overlay_grants = (
                conditional_overlay_grants + contract["conditional_overlay_grants"]
            )
            granted_sources.update(grants.values())
            granted_sources.update(conditional.values())
            for reference in contract["references"]:
                source = grants.get(reference, conditional.get(reference))
                if reference in contract["unresolved_refs"]:
                    missing_grants.add((service_name, reference))
                    if reference not in domain_declarations:
                        dangling.add((service_name, reference))
                elif source not in domain_declarations:
                    dangling.add((service_name, reference))

    # A validated POL-0078 overlay may grant a root declaration to an existing
    # base service; base grants stay unchanged and the overlay stays opt-in.
    overlay_grants = set()
    for overlay_path, model in (source_context or {}).get("overlay_inputs", {}).items():
        base = model["x-hyhome-overlay"]["base"]
        for name, delta in model["services"].items():
            if (base, name) not in base_grants:
                continue
            for source in service_grants(delta).values():
                overlay_grants.add((str(overlay_path), name, source))
                if source not in declarations:
                    dangling.add((name, source))
    granted_sources.update(source for *_, source in overlay_grants)

    rows = registry_rows(registry_text)
    registered_paths = {
        row["path"] for row in rows.values() if row["path"] not in ("", "-")
    }
    expected_exceptions = set(
        (REGISTRY_PATH_EXCEPTIONS | CUTOVER_REGISTRY_PATH_EXCEPTIONS).items()
    )
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
        "unresolved_refs": missing_grants,
        "overlay_grants": overlay_grants,
        "base_grants": base_grants,
        "conditional_overlay_grants": tuple(sorted(conditional_overlay_grants)),
        "rows": rows,
        "registered_paths": registered_paths,
        "registry_orphans": registry_orphans,
    }


class ComposeSchemaTagTests(unittest.TestCase):
    def test_supabase_lab_shares_only_the_exact_canonical_smtp_source(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            (root / "labs").mkdir()
            (root / "labs/.env.example").write_text(
                'LAB_SECRET_DIR="../secrets/labs"\n'
            )
            home = "secrets:\n  smtp_password:\n    file: ./secrets/communication/smtp/smtp_password.txt\n"
            lab = "secrets:\n  smtp_password:\n    file: ../secrets/communication/smtp/smtp_password.txt\n"
            found = secret_contract(
                root, {"docker-compose.yml": home, "labs/supabase.yml": lab}, "", set()
            )
            self.assertEqual({"smtp_password"}, found["declarations"])
            self.assertEqual(
                {"secrets/communication/smtp/smtp_password.txt"},
                found["declaration_paths"],
            )
            for route, text in (
                ("labs/other.yml", lab),
                (
                    "labs/supabase.yml",
                    lab.replace("communication/smtp", "security/openbao"),
                ),
                ("labs/supabase.yml", lab.replace("smtp_password:", "openbao_token:")),
                ("labs/supabase.yml", lab.replace("../secrets/", "../../secrets/")),
            ):
                with self.subTest(route=route, text=text):
                    with self.assertRaises(AssertionError):
                        secret_contract(
                            root, {"docker-compose.yml": home, route: text}, "", set()
                        )

    def test_compose_tags_preserve_values_and_references_without_unsafe_loading(self):
        text = (
            "services:\n"
            "  probe:\n"
            "    group_add: !override ['${TAGGED_GROUP}']\n"
            "    environment: !override {REQUIRED: '${TAGGED_ENV}'}\n"
            "    volumes: !reset []\n"
            "    command: !override synthetic-command\n"
        )
        contract = environment_contract(
            {"synthetic.yml": text}, "", supplemental_ids=set()
        )
        self.assertEqual({"TAGGED_GROUP", "TAGGED_ENV"}, contract["missing"])
        service = yaml.load(text, Loader=_ComposeLoader)["services"]["probe"]
        self.assertEqual(["${TAGGED_GROUP}"], service["group_add"])
        self.assertEqual({"REQUIRED": "${TAGGED_ENV}"}, service["environment"])
        self.assertEqual([], service["volumes"])
        self.assertEqual("synthetic-command", service["command"])
        with self.assertRaises(yaml.constructor.ConstructorError):
            yaml.safe_load(text)
        with self.assertRaises(yaml.constructor.ConstructorError):
            environment_contract(
                {"synthetic.yml": "services: !!python/object/apply:builtins.list []\n"},
                "",
                supplemental_ids=set(),
            )


class SecretMetadataSyncTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        # The FD-bound generator executes the public implementation owned by
        # this synthetic root, rather than reopening the external source root.
        for relative in (
            "scripts/operations/gen-secrets.sh",
            "scripts/lib/ops/smtp_contract.py",
            "scripts/lib/ops/retire_materials.py",
            "scripts/lib/ops/secret_catalog.py",
            "scripts/lib/ops/_secret_catalog_io.py",
        ):
            destination = self.root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes((ROOT / relative).read_bytes())
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
        self.prepare_catalog()

    def prepare_catalog(self, public_root=None):
        """Only temp synthetic roots; reuse the public parser and declared fixtures."""
        public_root = public_root or self.root
        self.assertTrue(public_root.is_relative_to(self.root))
        source = public_root / secret_catalog.METADATA_PATH
        if source.is_symlink():
            return  # The real entrypoint must reject this negative fixture.
        text = source.read_text().replace("(empty)", "(비어있음)")
        document = synthetic_catalog_model()
        canonical = document["entries"][0]
        canonical["automation"] = "X"
        canonical["classification"] = "bootstrap_external"
        canonical["destination_plan"]["kv_path"] = None
        baseline = secret_catalog.render_views(document)[
            secret_catalog.VIEW_NAMES[0]
        ].decode()
        # Fixture rows already use issued synthetic IDs. Keep the production
        # table/alias shapes without inventing another metadata authority.
        if not any(line.startswith("| COMM-002 |") for line in text.splitlines()):
            text += ("" if not text or text.endswith("\n") else "\n") + baseline
        source.write_text(text)
        try:
            metadata = secret_catalog.parse_public_table(text.encode())
        except ValueError:
            return  # Keep the malformed source, never repair a negative input.
        declarations = {
            "COMM-002": ("root", "bootstrap_external", "ACTIVE_KEEP", "consumer_owned"),
            "TEST-001": ("root", "kv_static", "ACTIVE_KEEP", "consumer_owned"),
            "TEST-002": ("root", "kv_static", "ACTIVE_KEEP", "consumer_owned"),
            "INFRA-001": (
                "root",
                "public_configuration",
                "ACTIVE_KEEP",
                "not_applicable",
            ),
            "INFRA-002": ("root", "kv_static", "ACTIVE_KEEP", "consumer_owned"),
            "INFRA-003": ("root", "derived_runtime", "ACTIVE_KEEP", "consumer_owned"),
            "LAB-999": ("lab", "lab_excluded", "LAB_EXCLUDED", "consumer_owned"),
        }
        if getattr(self, "recovery_fixture", False):
            declarations["TEST-001"] = (
                "root",
                "stable_crypto",
                "RETAINED_FOR_RECOVERY",
                "independent_required",
            )
        entries = []
        for public_entry in metadata["entries"]:
            scope, classification, disposition, custody = declarations[
                public_entry["id"]
            ]
            entry = {
                **canonical,
                **public_entry,
                "scope": scope,
                "classification": classification,
                "disposition": disposition,
                "recovery": {**canonical["recovery"], "custody": custody},
            }
            # Only these explicitly selected synthetic positive generation cases
            # request IMPLEMENT. Other fixture actions preserve NO_CHANGE.
            if (
                disposition == "ACTIVE_KEEP"
                and classification == "kv_static"
                and public_entry["id"] in {"TEST-001", "TEST-002", "INFRA-002"}
            ):
                entry["action"] = "IMPLEMENT"
            elif disposition == "LAB_EXCLUDED":
                entry["action"] = "OUT_OF_SCOPE"
            entry["destination_plan"] = {
                **canonical["destination_plan"],
                "kv_path": "secret/root/fixture/" + entry["id"].lower()
                if classification == "kv_static"
                and disposition != "RETAINED_FOR_RECOVERY"
                else None,
            }
            entries.append(entry)
        document = {**document, "entries": entries, "aliases": metadata["aliases"]}
        secret_catalog.validate_catalog(document)
        for relative, raw in (
            (secret_catalog.CATALOG_PATH, (json.dumps(document) + "\n").encode()),
            (
                secret_catalog.SCHEMA_PATH,
                (ROOT / secret_catalog.SCHEMA_PATH).read_bytes(),
            ),
            (secret_catalog.SUPPORT_PATH, b"{}\n"),
        ):
            target = public_root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw)
        if public_root != self.root:
            subprocess.run(["git", "init", "-q", str(public_root)], check=True)
        subprocess.run(
            [
                "git",
                "add",
                "--",
                secret_catalog.CATALOG_PATH,
                secret_catalog.SCHEMA_PATH,
                secret_catalog.METADATA_PATH,
                secret_catalog.SUPPORT_PATH,
            ],
            cwd=public_root,
            check=True,
        )

    def run_mode(self, mode="--sync-metadata"):
        self.prepare_catalog()
        result = subprocess.run(
            [
                "bash",
                str(self.root / "scripts/operations/gen-secrets.sh"),
                *([mode] if mode else []),
            ],
            cwd=self.root,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotIn("synthetic-private", result.stdout + result.stderr)
        return result

    def test_alternate_public_root_updates_owner_metadata_without_copying_private_files(
        self,
    ):
        source = self.root / "public-input"
        (source / "secrets").mkdir(parents=True)
        (source / "labs").mkdir()
        (source / "secrets/SENSITIVE_ENV_VARS.md.example").write_text(
            self.example.read_text()
        )
        (source / ".env.example").write_text("EXISTING=example\nADDED=example\n")
        (source / "labs/.env.example").write_text("LAB_KEEP=example\n")
        (self.root / "labs").mkdir()
        (self.root / "labs/.env").write_text("LAB_KEEP=synthetic-private-lab\n")
        self.prepare_catalog(source)
        before_source = {
            path: path.read_bytes() for path in source.rglob("*") if path.is_file()
        }
        args = [
            "bash",
            str(self.root / "scripts/operations/gen-secrets.sh"),
            "--sync-metadata-prune",
            "--metadata-source-root",
            str(source),
        ]
        result = subprocess.run(
            args, cwd=self.root, capture_output=True, text=True, check=False
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertNotIn("synthetic-private", result.stdout + result.stderr)
        self.assertIn("synthetic-private-value", self.target.read_text())
        self.assertIn(
            "EXISTING=synthetic-private-env", (self.root / ".env").read_text()
        )
        self.assertEqual(
            "LAB_KEEP=synthetic-private-lab\n", (self.root / "labs/.env").read_text()
        )
        self.assertEqual(
            before_source,
            {path: path.read_bytes() for path in source.rglob("*") if path.is_file()},
        )
        self.assertEqual(
            0,
            subprocess.run(
                [*args[:2], "--sync-metadata-prune-check", *args[3:]],
                cwd=self.root,
                capture_output=True,
                check=False,
            ).returncode,
        )

    def test_alternate_public_root_is_rejected_outside_metadata_modes(self):
        before = self.target.read_bytes(), (self.root / ".env").read_bytes()
        for mode in (None, "--dry-run", "--check", "--help"):
            result = subprocess.run(
                [
                    "bash",
                    str(self.root / "scripts/operations/gen-secrets.sh"),
                    *([mode] if mode else []),
                    "--metadata-source-root",
                    str(self.root),
                ],
                cwd=self.root,
                capture_output=True,
                check=False,
            )
            self.assertEqual(2, result.returncode, mode)
            self.assertEqual(
                before, (self.target.read_bytes(), (self.root / ".env").read_bytes())
            )

    def test_mirrors_public_layout_keeps_values_unknown_rows_and_env_bytes(self):
        self.example.write_text(
            "# Registry\n\n"
            "| **TEST-002** | `O` | `PW` | `(empty)` | `-` | `secrets/two.txt` | 2026-02-02 | Second |\n"
            + self.example.read_text()
            + "*last updated: 2026-01-01*\n"
        )
        unknown = "| **LOCAL-001** | `X` | `PW` | `synthetic-private-local` | `-` | | 2025-01-01 | Local |\n"
        self.target.write_text("operator note\n" + self.private + unknown)
        result = self.run_mode()
        self.assertEqual(0, result.returncode, result.stderr)
        text = self.target.read_text()
        # Everything but the value cell comes from the public registry, in its
        # order, including the date and the free text around the table.
        mirrored = self.example.read_text().replace(
            "`(비어있음)` | `NEW_KEY`", "`synthetic-private-value` | `NEW_KEY`"
        )
        self.assertTrue(text.startswith(mirrored), text)
        self.assertNotIn("2025-01-01 | Old purpose", text)
        self.assertNotIn("operator note", text)
        self.assertIn(unknown, text)
        self.assertEqual(
            "# operator comment\nEXISTING=synthetic-private-env\nUNKNOWN=keep\nADDED=default\n",
            (self.root / ".env").read_text(),
        )
        self.assertFalse((self.root / "secrets/test.txt").exists())
        self.assertEqual(0, self.run_mode().returncode)

    def test_generation_preserves_existing_derived_htpasswd_custody(self):
        rows = (
            "| **INFRA-001** | `X` | `ID` | `(empty)` | `TRAEFIK_ADMIN_USERNAME` | | 2026-01-01 | Admin name |\n"
            "| **INFRA-002** | `O` | `PW` | `(empty)` | `-` | `secrets/auth/admin.txt` | 2026-01-01 | Admin password |\n"
            "| **INFRA-003** | `O` | `Secret` | `(empty)` | `-` | `secrets/auth/traefik/traefik_basicauth_password.txt` | 2026-01-01 | Admin hash |\n"
        )
        self.example.write_text(rows)
        self.target.write_text(rows)
        self.target.chmod(0o600)
        (self.root / ".env").write_text("TRAEFIK_ADMIN_USERNAME=synthetic-user\n")
        (self.root / "secrets/auth").mkdir()
        (self.root / "secrets/auth/admin.txt").write_text("synthetic-password\n")
        htpasswd = self.root / "secrets/auth/traefik/traefik_basicauth_password.txt"
        htpasswd.parent.mkdir()
        htpasswd.write_bytes(b"synthetic-user:synthetic-existing-hash\n")
        before = htpasswd.read_bytes()
        expected_registry = rows.replace(
            "`(empty)` | `-` | `secrets/auth/admin.txt`",
            "`synthetic-password` | `-` | `secrets/auth/admin.txt`",
        ).encode()
        for _ in range(2):
            result = self.run_mode("")
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertNotIn("Updating htpasswd hash", result.stdout + result.stderr)
            self.assertEqual(before, htpasswd.read_bytes())
            self.assertEqual(expected_registry, self.target.read_bytes())
        htpasswd.unlink()
        self.assertEqual(0, self.run_mode("").returncode)
        self.assertFalse(htpasswd.exists())

    def test_generation_preserves_lab_identity_and_ignores_lab_dotenv(self):
        lab = self.root / "labs"
        lab.mkdir()
        (lab / ".env").write_text("LAB_ID=synthetic-lab-id\n")
        row = "| **LAB-999** | `X` | `ID` | `(empty)` | `LAB_ID` |  | 2026-01-01 | LAB identity |\n"
        self.example.write_text(row)
        self.target.write_text(row)
        self.target.chmod(0o600)
        self.assertEqual(0, self.run_mode("").returncode)
        self.assertEqual(row, self.target.read_text())

        before = self.target.read_bytes()
        (lab / ".env").write_text("EXISTING=collision\nLAB_ID=synthetic-lab-id\n")
        self.assertEqual(0, self.run_mode("").returncode)
        self.assertEqual(before, self.target.read_bytes())
        self.assertEqual(
            "EXISTING=collision\nLAB_ID=synthetic-lab-id\n", (lab / ".env").read_text()
        )

    def test_generation_writes_only_the_value_cell(self):
        text = (
            "# Registry\n\n"
            "| **TEST-001** | `O` | `PW` | `(empty)` | `-` | `secrets/gen.txt` | 2026-01-01 | Generated |\n"
            "*last updated: 2026-01-01*\n"
        )
        self.example.write_text(text)
        self.target.write_text(text)
        self.target.chmod(0o600)
        result = self.run_mode("")
        self.assertEqual(0, result.returncode, result.stderr)
        after = self.target.read_text()
        value = (self.root / "secrets/gen.txt").read_text()
        self.assertEqual(16, len(value))
        self.assertEqual(text.replace("`(empty)`", f"`{value}`"), after)

    def test_generation_keeps_a_multiline_file_out_of_the_registry(self):
        text = "| **TEST-001** | `X` | `Recovery` | `(empty)` | `-` | `secrets/shares.txt` | 2026-01-01 | Shares |\n"
        self.example.write_text(text)
        self.target.write_text(text)
        self.target.chmod(0o600)
        self.recovery_fixture = True
        shares = self.root / "secrets/shares.txt"
        shares.write_text("synthetic-share-1\nsynthetic-share-2\n")
        result = self.run_mode("")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(text, self.target.read_text())
        self.assertEqual("synthetic-share-1\nsynthetic-share-2\n", shares.read_text())

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
        self.assertNotIn("# registry comment", registry)  # public layout only
        self.assertNotIn("LOCAL-001", registry)
        rows = [
            line.split("|") for line in registry.splitlines() if line.startswith("| **")
        ]
        self.assertEqual({"TEST-001", "TEST-002"}, {row[1].strip("* ") for row in rows})
        retained = next(row for row in rows if "TEST-001" in row[1])
        self.assertEqual(before_retained[4], retained[4])
        self.assertEqual(" 2026-01-01 ", retained[7])  # the public date
        self.assertEqual("NEW_KEY", retained[5].strip(" `"))
        self.assertTrue(secret_file.is_file())
        self.assertEqual("synthetic-secret-file", secret_file.read_text())

        env_before = (self.root / ".env").read_bytes()
        registry_before = self.target.read_bytes()
        self.assertEqual(0, self.run_mode("--sync-metadata-prune-check").returncode)
        self.assertEqual(0, self.run_mode("--sync-metadata-prune").returncode)
        self.assertEqual(env_before, (self.root / ".env").read_bytes())
        self.assertEqual(registry_before, self.target.read_bytes())

    def test_lab_environment_sync_preserves_values_and_prunes_stale_keys(self):
        lab = self.root / "labs"
        lab.mkdir()
        (lab / ".env.example").write_text("LAB_KEEP=public\nLAB_NEW=default\n")
        private = lab / ".env"
        private.write_text("LAB_KEEP=synthetic-private-lab\nLAB_STALE=remove\n")
        private.chmod(0o644)
        registry_before = self.target.read_bytes()

        self.assertEqual(1, self.run_mode("--sync-metadata-prune-check").returncode)
        self.assertEqual(registry_before, self.target.read_bytes())
        self.assertEqual(0, self.run_mode("--sync-metadata-prune").returncode)
        self.assertEqual(
            "LAB_KEEP=synthetic-private-lab\nLAB_NEW=default\n",
            private.read_text(),
        )
        self.assertEqual(0o600, private.stat().st_mode & 0o777)
        self.assertEqual(0, self.run_mode("--sync-metadata-prune-check").returncode)

    def test_bad_lab_environment_rejects_all_metadata_writes(self):
        lab = self.root / "labs"
        lab.mkdir()
        (lab / ".env.example").write_text("LAB_KEY=public\n")
        private = lab / ".env"
        private.write_text("LAB_KEY=one\nLAB_KEY=two\n")
        before = self.target.read_bytes()
        root_before = (self.root / ".env").read_bytes()
        self.assertEqual(2, self.run_mode("--sync-metadata-prune").returncode)
        self.assertEqual(before, self.target.read_bytes())
        self.assertEqual(root_before, (self.root / ".env").read_bytes())
        self.assertEqual("LAB_KEY=one\nLAB_KEY=two\n", private.read_text())

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
        cls.source_context = conftest_source_context(ROOT)
        cls.compose_texts = compose_sources()
        cls.lab_compose_texts = lab_compose_sources()
        cls.env_text = (ROOT / ".env.example").read_text()
        cls.environment = environment_contract(cls.compose_texts, cls.env_text)
        cls.lab_environment = environment_contract(
            cls.lab_compose_texts,
            (ROOT / "labs/.env.example").read_text(),
            supplemental_ids=lab_controller_inputs(),
        )
        cls.registry_text = (ROOT / "secrets/SENSITIVE_ENV_VARS.md.example").read_text()

    def scoped_secret_contract(self, compose_texts, registry_text):
        return secret_contract(
            ROOT,
            compose_texts | self.lab_compose_texts,
            registry_text,
            self.environment["consumed"] | self.lab_environment["consumed"],
            source_context=self.source_context,
        )

    def test_optional_activation_keeps_base_grants_and_records_closed_provenance(self):
        contract = self.scoped_secret_contract(self.compose_texts, self.registry_text)
        self.assertEqual(set(), contract["missing_grants"])
        base = "infra/04-data/mng-db/docker-compose.yml"
        self.assertNotIn(
            "mng_valkey_n8n_password", contract["base_grants"][(base, "mng-valkey")]
        )
        self.assertIn(
            (
                base,
                "mng-valkey",
                "mng_valkey_n8n_password",
                "infra/04-data/mng-db/docker-compose.n8n-acl.yml",
                ("MNG_VALKEY_N8N_ENABLED",),
                ("infra/04-data/mng-db/valkey/scripts/render-acl.sh",),
            ),
            contract["conditional_overlay_grants"],
        )

    def _activation_contract(self, overlays, environment=None):
        base = "infra/04-data/mng-db/docker-compose.yml"
        compose_texts = self.compose_texts
        if environment is not None:
            document = yaml.load(compose_texts[base], Loader=_ComposeLoader)
            service = document["services"]["mng-valkey"]
            service = service | {"environment": service["environment"] | environment}
            document = document | {
                "services": document["services"] | {"mng-valkey": service}
            }
            compose_texts = compose_texts | {base: yaml.safe_dump(document)}
        return secret_contract(
            ROOT,
            compose_texts | self.lab_compose_texts,
            self.registry_text,
            self.environment["consumed"] | self.lab_environment["consumed"],
            source_context=self.source_context | {"overlay_inputs": overlays},
        )

    def test_conditional_coverage_rejects_wrong_activation_or_overlay_delta(self):
        path = Path("infra/04-data/mng-db/docker-compose.n8n-acl.yml")
        model = self.source_context["overlay_inputs"][path]
        service = model["services"]["mng-valkey"]
        variants = [
            ("absent", {}),
            (
                "missing grant",
                {path: model | {"services": {"mng-valkey": service | {"secrets": []}}}},
            ),
            (
                "wrong base",
                {
                    path: model
                    | {
                        "x-hyhome-overlay": {
                            "version": 1,
                            "base": "infra/other/docker-compose.yml",
                        }
                    }
                },
            ),
            (
                "wrong service",
                {path: model | {"services": {"different-service": service}}},
            ),
            (
                "unrelated selector",
                {
                    path: model
                    | {
                        "services": {
                            "mng-valkey": service
                            | {"environment": {"UNRELATED_ENABLED": "1"}}
                        }
                    }
                },
            ),
            (
                "other delta",
                {
                    path: model
                    | {
                        "services": {
                            "mng-valkey": service | {"command": ["unexpected"]}
                        }
                    }
                },
            ),
            (
                "duplicate selector",
                {
                    path: model
                    | {
                        "services": {
                            "mng-valkey": service
                            | {
                                "environment": [
                                    "MNG_VALKEY_N8N_ENABLED=1",
                                    "MNG_VALKEY_N8N_ENABLED=1",
                                ]
                            }
                        }
                    }
                },
            ),
        ]
        for label, overlays in variants:
            with self.subTest(case=label):
                contract = self._activation_contract(overlays)
                self.assertIn(
                    ("mng-valkey", "mng_valkey_n8n_password"),
                    contract["unresolved_refs"],
                )

    def test_conditional_coverage_never_replaces_base_or_direct_grants(self):
        path = Path("infra/04-data/mng-db/docker-compose.n8n-acl.yml")
        overlays = {path: self.source_context["overlay_inputs"][path]}
        for environment in (
            {"MNG_VALKEY_N8N_ENABLED": "1"},
            {"DIRECT_REFERENCE": "/run/secrets/mng_valkey_n8n_password"},
        ):
            with self.subTest(environment_names=tuple(environment)):
                contract = self._activation_contract(overlays, environment)
                self.assertIn(
                    ("mng-valkey", "mng_valkey_n8n_password"),
                    contract["missing_grants"],
                )
        disabled = self._activation_contract(overlays, {"MNG_VALKEY_N8N_ENABLED": "0"})
        self.assertEqual(set(), disabled["missing_grants"])

    def test_overlay_grants_cover_only_declared_sources_of_base_services(self):
        contract = self.scoped_secret_contract(self.compose_texts, self.registry_text)
        self.assertIn(
            (
                "infra/07-workflow/n8n/docker-compose.monitor-acl.yml",
                "n8n-valkey-exporter",
                "n8n_valkey_monitor_password",
            ),
            contract["overlay_grants"],
        )
        path = Path("infra/07-workflow/n8n/docker-compose.monitor-acl.yml")
        model = self.source_context["overlay_inputs"][path]
        service = model["services"]["n8n-valkey-exporter"]
        undeclared = model | {
            "services": {"n8n-valkey-exporter": service | {"secrets": ["undeclared"]}}
        }
        contract = self._activation_contract({path: undeclared})
        self.assertIn(("n8n-valkey-exporter", "undeclared"), contract["dangling"])
        foreign = model | {"services": {"not-in-base": service}}
        contract = self._activation_contract({path: foreign})
        self.assertFalse(
            any(row[1] == "not-in-base" for row in contract["overlay_grants"])
        )

    def test_conditional_coverage_rejects_conflicting_target_sources(self):
        path = Path("infra/04-data/mng-db/docker-compose.n8n-acl.yml")
        model = self.source_context["overlay_inputs"][path]
        service = model["services"]["mng-valkey"]
        grants = service["secrets"] + [
            {"source": "grafana_admin_password", "target": "mng_valkey_password"}
        ]
        changed = model | {"services": {"mng-valkey": service | {"secrets": grants}}}
        with self.assertRaisesRegex(
            AssertionError, "conflicting conditional overlay grant"
        ):
            self._activation_contract({path: changed})

    def test_public_environment_has_current_consumers_and_four_way_classification(self):
        contract = self.environment
        self.assertTrue(contract["public"])
        self.assertEqual(set(), contract["missing"])
        self.assertEqual(set(), contract["orphan"])
        self.assertEqual(INDIRECT_DERIVED_INPUTS, contract["derived_only"])
        self.assertTrue(contract["required"])
        self.assertTrue(contract["optional"])
        self.assertEqual(
            contract["public"],
            contract["required"] | contract["optional"] | contract["orphan"],
        )
        lab = self.lab_environment
        self.assertTrue(lab["required"])
        self.assertTrue(lab["optional"])
        self.assertIn("LAB_SUPABASE_DASHBOARD_USERNAME", lab["public"])
        self.assertFalse(
            any(name.startswith("SUPABASE_") for name in contract["public"])
        )
        self.assertEqual(set(), lab["missing"] | lab["orphan"])
        self.assertEqual(set(), contract["public"] & lab["public"])
        self.assertFalse(any(name.startswith("LAB_") for name in contract["public"]))
        self.assertTrue(all(name.startswith("LAB_") for name in lab["public"]))
        self.assertIn("ADMIN_UI_ALLOWED_CIDRS", contract["public"])
        self.assertEqual(lab["public"], lab["required"] | lab["optional"])

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

    def test_source_analysis_services_hold_no_secrets(self):
        found = set()
        for text in self.compose_texts.values():
            document = yaml.load(text, Loader=_ComposeLoader) or {}
            for name, service in (document.get("services") or {}).items():
                if name not in SOURCE_ANALYSIS_SERVICES:
                    continue
                found.add(name)
                self.assertEqual({}, service_grants(service), name)
                self.assertEqual("none", service.get("network_mode"), name)
                for volume in service.get("volumes", []):
                    self.assertTrue(str(volume).endswith(":ro"), (name, volume))
                    self.assertNotIn("secrets", str(volume), (name, volume))
        self.assertEqual(SOURCE_ANALYSIS_SERVICES, found)

    def test_secret_directory_markers_are_empty_regular_files(self):
        markers = list((ROOT / "secrets").rglob(".gitkeep"))
        for relative in (
            "communication/smtp/.gitkeep",
            "db/surrealdb/.gitkeep",
            "security/openbao/.gitkeep",
            "backup/openbao/.gitkeep",
        ):
            self.assertIn(ROOT / "secrets" / relative, markers)
        for path in markers:
            info = path.lstat()
            self.assertTrue(stat.S_ISREG(info.st_mode), path)
            self.assertEqual(0, info.st_size, path)

    def test_literal_secret_references_are_declared_granted_and_registered(self):
        contract = self.scoped_secret_contract(self.compose_texts, self.registry_text)
        self.assertIn("smtp_password", contract["declarations"])
        self.assertNotIn("supabase_smtp_password", contract["declarations"])
        self.assertNotIn("COMM-003", contract["rows"])
        self.assertEqual(
            "secrets/db/surrealdb/surreal_db_password.txt",
            contract["rows"]["AI-003"]["path"],
        )
        self.assertEqual(
            "secrets/communication/smtp/smtp_password.txt",
            contract["rows"]["COMM-002"]["path"],
        )
        self.assertEqual(set(), contract["dangling"])
        self.assertEqual(set(), contract["missing_grants"])
        self.assertEqual(contract["declarations"], contract["granted_sources"])
        self.assertEqual(
            set(), contract["declaration_paths"] - contract["registered_paths"]
        )
        self.assertEqual(
            set((REGISTRY_PATH_EXCEPTIONS | CUTOVER_REGISTRY_PATH_EXCEPTIONS).values()),
            contract["registered_paths"] - contract["declaration_paths"],
        )
        self.assertEqual(set(), contract["registry_orphans"])
        self.assertEqual(
            set((REGISTRY_PATH_EXCEPTIONS | CUTOVER_REGISTRY_PATH_EXCEPTIONS).items()),
            {
                (identity, contract["rows"][identity]["path"])
                for identity in REGISTRY_PATH_EXCEPTIONS
                | CUTOVER_REGISTRY_PATH_EXCEPTIONS
            },
        )

    def test_registry_paths_use_service_directories_and_preserve_instance_ownership(
        self,
    ):
        rows = registry_rows(self.registry_text)
        for identity, row in rows.items():
            if row["path"].startswith("secrets/"):
                self.assertGreaterEqual(len(Path(row["path"]).parts), 4, identity)
                self.assertNotIn("common", Path(row["path"]).parts)
                self.assertNotIn("surreal_db", Path(row["path"]).parts)
        self.assertEqual("secrets/db/dev-pg/dbt_password.txt", rows["PG-023"]["path"])
        self.assertEqual(
            "secrets/db/dev-pg/debezium_password.txt", rows["PG-025"]["path"]
        )
        self.assertEqual(
            "secrets/db/mng-pg/grafana_reader_password.txt", rows["PG-030"]["path"]
        )
        self.assertEqual(
            "secrets/db/legacy-app/service_password.txt", rows["PG-020"]["path"]
        )

    def test_secret_scanner_mutations_detect_dangling_grant_and_registry_drift(self):
        observability_path = "infra/06-observability/docker-compose.yml"
        observability = yaml.load(
            self.compose_texts[observability_path], Loader=_ComposeLoader
        )
        observability["services"]["prometheus"].setdefault("environment", {})[
            "DANGLING_FILE"
        ] = "/run/secrets/missing_literal"
        mutated = dict(self.compose_texts)
        mutated[observability_path] = yaml.safe_dump(observability)
        contract = self.scoped_secret_contract(mutated, self.registry_text)
        self.assertIn(("prometheus", "missing_literal"), contract["dangling"])

        observability = yaml.load(
            self.compose_texts[observability_path], Loader=_ComposeLoader
        )
        observability["services"]["prometheus"]["secrets"].remove("openbao_token")
        mutated[observability_path] = yaml.safe_dump(observability)
        contract = self.scoped_secret_contract(mutated, self.registry_text)
        self.assertIn(("prometheus", "openbao_token"), contract["missing_grants"])

        observability = yaml.load(
            self.compose_texts[observability_path], Loader=_ComposeLoader
        )
        observability["services"]["loki"]["secrets"] = ["grafana_admin_password"]
        mutated[observability_path] = yaml.safe_dump(observability)
        contract = self.scoped_secret_contract(mutated, self.registry_text)
        self.assertIn(
            ("loki", "seaweedfs_s3_loki_secret_key"), contract["missing_grants"]
        )

        registry = (
            self.registry_text + "\n| **TEST-999** | X | Token | (empty) | - | "
            "secrets/security/unmapped.txt | 2026-09-20 | Mutation probe |\n"
        )
        contract = self.scoped_secret_contract(self.compose_texts, registry)
        self.assertIn(
            ("TEST-999", "secrets/security/unmapped.txt"),
            contract["registry_orphans"],
        )

    def test_lab_secret_must_be_declared_in_its_own_entrypoint(self):
        path = "labs/couchdb.yml"
        couchdb = yaml.load(self.lab_compose_texts[path], Loader=_ComposeLoader)
        name = next(iter(couchdb["secrets"]))
        couchdb["secrets"].pop(name)
        lab = dict(self.lab_compose_texts)
        lab[path] = yaml.safe_dump(couchdb)
        contract = secret_contract(
            ROOT,
            self.compose_texts | lab,
            self.registry_text,
            self.environment["consumed"] | self.lab_environment["consumed"],
        )
        self.assertIn(name, contract["granted_sources"])
        self.assertTrue(any(reference == name for _, reference in contract["dangling"]))

        couchdb = yaml.load(self.lab_compose_texts[path], Loader=_ComposeLoader)
        couchdb["secrets"][name]["file"] = "${LAB_SECRET_DIR}/../../escape"
        lab[path] = yaml.safe_dump(couchdb)
        with self.assertRaisesRegex(AssertionError, "escaped isolated path"):
            secret_contract(
                ROOT,
                self.compose_texts | lab,
                self.registry_text,
                self.environment["consumed"] | self.lab_environment["consumed"],
            )

    def test_root_secret_cannot_use_lab_credential_tree(self):
        root = yaml.load(
            self.compose_texts["docker-compose.yml"], Loader=_ComposeLoader
        )
        root["secrets"]["mng_postgres_password"]["file"] = "./secrets/labs/wrong.txt"
        changed = dict(self.compose_texts)
        changed["docker-compose.yml"] = yaml.safe_dump(root)
        with self.assertRaisesRegex(AssertionError, "root secret entered LAB path"):
            self.scoped_secret_contract(changed, self.registry_text)

    def test_secret_scanner_detects_n8n_workdir_entrypoint_grant_swap(self):
        n8n_path = "infra/07-workflow/n8n/docker-compose.yml"
        n8n = yaml.load(self.compose_texts[n8n_path], Loader=_ComposeLoader)
        n8n["services"]["n8n"]["secrets"] = [
            "grafana_admin_password"
            if compose_default(grant) == "mng_valkey_password"
            else grant
            for grant in n8n["services"]["n8n"]["secrets"]
        ]
        mutated = dict(self.compose_texts)
        mutated[n8n_path] = yaml.safe_dump(n8n)

        contract = self.scoped_secret_contract(mutated, self.registry_text)

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
        declarations = yaml.load(
            (root / "docker-compose.yml").read_text(), Loader=_ComposeLoader
        )["secrets"]
        self.assertEqual(
            {"file": "./secrets/security/openbao/openbao_token.txt"},
            declarations.get("openbao_token"),
        )
        self.assertNotIn("vault_token", declarations)

        observability = yaml.load(
            (root / "infra/06-observability/docker-compose.yml").read_text(),
            Loader=_ComposeLoader,
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
        self.assertNotIn("**SEC-001**", registry)  # legacy Vault token, removed in S08
        self.assertIn("**SEC-002**", registry)
        self.assertIn("secrets/security/openbao/openbao_token.txt", registry)

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
        declarations = yaml.load(
            (root / "docker-compose.yml").read_text(), Loader=_ComposeLoader
        )["secrets"]
        expected = {
            value["file"].removeprefix("./")
            for value in declarations.values()
            if "file" in value
        }
        self.assertFalse(expected - {row[6] for row in rows})
        keys = re.findall(
            r"^([A-Za-z_][A-Za-z0-9_]*)=", (root / ".env.example").read_text(), re.M
        )
        keys += re.findall(
            r"^([A-Za-z_][A-Za-z0-9_]*)=",
            (root / "labs/.env.example").read_text(),
            re.M,
        )
        self.assertEqual(len(keys), len(set(keys)))
        self.assertFalse(
            {row[5] for row in rows if row[5] not in ("", "-")} - set(keys)
        )
