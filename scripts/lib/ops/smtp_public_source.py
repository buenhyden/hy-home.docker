"""Public SMTP source validation for root and LAB Compose receipts."""

from __future__ import annotations

import hashlib
import json
import os
import posixpath
import stat
import subprocess
from contextlib import ExitStack
from pathlib import Path

import yaml

from scripts.lib.document_governance.operations_catalog import _ComposeLoader

LAB_SUPABASE_PATH = "labs/supabase.yml"
LAB_COMMON_EXTENDS_PATH = "infra/common-optimizations.yml"
LAB_COMMON_EXTENDS = {
    "file": "../" + LAB_COMMON_EXTENDS_PATH,
    "service": "template-infra-med",
}
LAB_SMTP_TARGET = "supabase_smtp_password"
LAB_SMTP_TARGET_FILE = "/run/secrets/" + LAB_SMTP_TARGET
LAB_AUTH_IMAGE = "supabase/gotrue:v2.197.0"
LAB_AUTH_ENTRYPOINT_SHA256 = (
    "41efd59cf7ac329a6a79dca81ce1ce40295d3461dec5502549f0b750a5638380"
)
LAB_NAME = "hy-home-lab-supabase"
LAB_PROFILE = "supabase"
LAB_TIER = "lab"
MAX_PUBLIC_SOURCE_BYTES = 256 * 1024
MAX_EXTENDS_DEPTH = 16
MAX_SOURCE_NODES = 128


class _PublicComposeLoader(_ComposeLoader):
    """Compose loader with duplicate mapping keys rejected for proof inputs."""


def _construct_mapping(loader, node, deep=False):
    if not isinstance(node, yaml.MappingNode):
        raise yaml.constructor.ConstructorError(
            None, None, "expected mapping", node.start_mark
        )
    seen = set()
    for key_node, _value_node in node.value:
        if key_node.tag == "tag:yaml.org,2002:merge":
            continue
        key = loader.construct_object(key_node, deep=deep)
        if key in seen:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"found duplicate key {key!r}",
                key_node.start_mark,
            )
        seen.add(key)
    loader.flatten_mapping(node)
    return dict(loader.construct_pairs(node, deep=deep))


_PublicComposeLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping
)


def _identity(info):
    return (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def _directory(root, relative, stack, error):
    if any(part in ("", ".", "..") for part in relative.parts):
        raise error("unsafe_compose_path")
    fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
    stack.callback(os.close, fd)
    for part in relative.parts:
        current = os.open(
            part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=fd
        )
        stack.callback(os.close, current)
        fd = current
    return fd


def _git_tracked(root, relative, error):
    environment = {
        key: value for key, value in os.environ.items() if not key.startswith("GIT_")
    }
    probe = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=False,
        env=environment,
    )
    if probe.returncode != 0:
        return
    if Path(probe.stdout.strip()) != root:
        raise error("unsafe_compose_path")
    tracked = subprocess.run(
        ["git", "-C", str(root), "ls-files", "--error-unmatch", "--", relative],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
        env=environment,
    )
    if tracked.returncode != 0:
        raise error("untracked_public_source")


def read_public_yaml(root, relative, error):
    root = Path(root).absolute()
    path = root / relative
    if not path.exists():
        return None
    try:
        normalized = path.relative_to(root)
    except ValueError:
        raise error("unsafe_compose_path") from None
    if str(normalized) != relative or any(
        part in ("", ".", "..") for part in normalized.parts
    ):
        raise error("unsafe_compose_path")
    _git_tracked(root, relative, error)
    with ExitStack() as stack:
        parent = _directory(root, normalized.parent, stack, error)
        try:
            fd = os.open(
                normalized.name,
                os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC,
                dir_fd=parent,
            )
        except OSError:
            raise error("unsafe_compose_path") from None
        stack.callback(os.close, fd)
        info = os.fstat(fd)
        if (
            not stat.S_ISREG(info.st_mode)
            or info.st_nlink != 1
            or info.st_size > MAX_PUBLIC_SOURCE_BYTES
        ):
            raise error("unsafe_compose_path")
        before = _identity(info)
        with os.fdopen(os.dup(fd), "rb") as stream:
            data = stream.read()
        if _identity(os.fstat(fd)) != before:
            raise error("concurrent_file_change")
    try:
        document = yaml.load(data, Loader=_PublicComposeLoader)
    except yaml.YAMLError:
        raise error("invalid_compose_document") from None
    if not isinstance(document, dict):
        raise error("invalid_compose_document")
    return data, document


def _safe_public_compose_path(relative, error):
    if not isinstance(relative, str) or not relative:
        raise error("unsafe_compose_path")
    path = Path(relative)
    if path.is_absolute():
        raise error("unsafe_compose_path")
    normalized = posixpath.normpath(relative.replace(os.sep, "/"))
    if normalized in ("", ".") or normalized.startswith("../") or normalized == "..":
        raise error("unsafe_compose_path")
    parts = tuple(Path(normalized).parts)
    if any(part in ("", ".", "..") for part in parts):
        raise error("unsafe_compose_path")
    if parts[0] in {"secrets", ".git"} or any(part.startswith(".") for part in parts):
        raise error("unsafe_compose_path")
    if Path(normalized).suffix not in {".yml", ".yaml"}:
        raise error("unsafe_compose_path")
    return normalized


def _include_path(current, include, error):
    item = (
        include
        if isinstance(include, str)
        else include.get("path")
        if isinstance(include, dict)
        else None
    )
    if not isinstance(item, str):
        raise error("unsafe_compose_path")
    if Path(item).is_absolute():
        raise error("unsafe_compose_path")
    return _safe_public_compose_path(str(Path(current).parent / item), error)


def _service_map(document, error):
    services = document.get("services", {})
    if not isinstance(services, dict):
        raise error("invalid_services")
    return services


def _extends_reference(current, service, error):
    spec = service.get("extends")
    if spec is None:
        return None
    if not isinstance(spec, dict):
        raise error("unsafe_compose_path")
    target = spec.get("service")
    if not isinstance(target, str) or not target:
        raise error("unsafe_compose_path")
    file_name = spec.get("file")
    if file_name is None:
        return current, target
    if not isinstance(file_name, str) or not file_name:
        raise error("unsafe_compose_path")
    return _include_path(current, file_name, error), target


def _load_source(root, relative, hashes, documents_by_path, ordered_documents, error):
    relative = _safe_public_compose_path(relative, error)
    if relative in documents_by_path:
        return documents_by_path[relative]
    if len(documents_by_path) >= MAX_SOURCE_NODES:
        raise error("unsafe_compose_path")
    loaded = read_public_yaml(root, relative, error)
    if loaded is None:
        raise error("unsafe_compose_path")
    data, document = loaded
    hashes[relative] = hashlib.sha256(data).hexdigest()
    documents_by_path[relative] = document
    ordered_documents.append(document)
    return document


def _service_auth_alias(service, *, canonical, old, grants, error):
    try:
        return (canonical, old) in grants(service)
    except Exception as exc:
        if isinstance(exc, error):
            raise
        raise


def _resolve_service_contract(
    root,
    relative,
    name,
    hashes,
    documents_by_path,
    ordered_documents,
    error,
    stack,
    *,
    canonical,
    old,
    grants,
):
    if len(stack) >= MAX_EXTENDS_DEPTH:
        raise error("unsafe_compose_path")
    key = (relative, name)
    if key in stack:
        raise error("unsafe_compose_path")
    document = _load_source(
        root, relative, hashes, documents_by_path, ordered_documents, error
    )
    service = _service_map(document, error).get(name)
    if not isinstance(service, dict):
        raise error("invalid_service")
    parent = _extends_reference(relative, service, error)
    inherited_image, inherited_auth = None, False
    if parent is not None:
        inherited_image, inherited_auth = _resolve_service_contract(
            root,
            *parent,
            hashes,
            documents_by_path,
            ordered_documents,
            error,
            (*stack, key),
            canonical=canonical,
            old=old,
            grants=grants,
        )
    image = service.get("image")
    if image is not None and not isinstance(image, str):
        raise error("invalid_service")
    if isinstance(image, str) and "$" in image:
        raise error("unresolved_root_image")
    auth_alias = inherited_auth
    if "secrets" in service:
        auth_alias = _service_auth_alias(
            service, canonical=canonical, old=old, grants=grants, error=error
        )
    return image or inherited_image, auth_alias


def _bind_service_extends(
    root,
    hashes,
    documents_by_path,
    ordered_documents,
    selected_paths,
    error,
    *,
    canonical,
    old,
    grants,
):
    resolved_images = []
    selected_auth_alias = False
    for relative in selected_paths:
        document = documents_by_path[relative]
        for name, service in _service_map(document, error).items():
            if not isinstance(service, dict):
                raise error("invalid_service")
            image, auth_alias = _resolve_service_contract(
                root,
                relative,
                name,
                hashes,
                documents_by_path,
                ordered_documents,
                error,
                (),
                canonical=canonical,
                old=old,
                grants=grants,
            )
            if image is not None:
                resolved_images.append(image)
            if name == "auth" and auth_alias:
                selected_auth_alias = True
    return {"images": tuple(resolved_images), "auth_alias": selected_auth_alias}


def source_documents(root, *, canonical, canonical_path, old, old_path, grants, error):
    root = Path(root).absolute()
    pending, hashes, documents_by_path, documents = ["docker-compose.yml"], {}, {}, []
    selected_paths = []
    while pending:
        relative = _safe_public_compose_path(pending.pop(), error)
        if relative in hashes:
            continue
        selected_paths.append(relative)
        document = _load_source(
            root, relative, hashes, documents_by_path, documents, error
        )
        if relative != "docker-compose.yml":
            definitions = document.get("secrets", {})
            if not isinstance(definitions, dict):
                raise error("invalid_secret_definition")
            for name, entry in definitions.items():
                filename = entry.get("file") if isinstance(entry, dict) else None
                normalized_file = None
                if isinstance(filename, str) and not Path(filename).is_absolute():
                    normalized_file = posixpath.normpath(
                        str(Path(relative).parent / filename).replace(os.sep, "/")
                    )
                if (
                    name == canonical
                    or filename
                    in (
                        canonical_path,
                        "./" + canonical_path,
                        old_path,
                        "./" + old_path,
                    )
                    or normalized_file in (canonical_path, old_path)
                ):
                    raise error("included_smtp_redefinition")
        includes = document.get("include", [])
        if includes is None:
            continue
        if not isinstance(includes, list):
            raise error("unsafe_compose_path")
        for include in includes:
            pending.append(_include_path(relative, include, error))
    selected = _bind_service_extends(
        root,
        hashes,
        documents_by_path,
        documents,
        tuple(selected_paths),
        error,
        canonical=canonical,
        old=old,
        grants=grants,
    )
    return hashes, documents, selected


def _is_gotrue_image(image):
    if not isinstance(image, str):
        return False
    if "$" in image:
        return True
    repository = image.split("@", 1)[0]
    last_slash = repository.rfind("/")
    colon = repository.rfind(":")
    if colon > last_slash:
        repository = repository[:colon]
    return (
        repository.endswith("/supabase/gotrue") or repository.split("/")[-1] == "gotrue"
    )


def has_root_gotrue_service(_documents, selected=None):
    images = (
        selected.get("images", ()) if isinstance(selected, dict) else selected or ()
    )
    return any(_is_gotrue_image(image) for image in images)


def _json_dump(value, error):
    try:
        return json.dumps(value)
    except (TypeError, ValueError):
        raise error("invalid_compose_document") from None


def _mapping(value, code, error):
    if not isinstance(value, dict):
        raise error(code)
    return value


def _lab_auth_service(
    document, *, canonical, canonical_path, old, old_path, grants, error
):
    if document.get("name") != LAB_NAME:
        raise error("invalid_lab_source")
    secrets = _mapping(document.get("secrets"), "invalid_lab_source", error)
    services = _mapping(document.get("services"), "invalid_lab_source", error)
    smtp = secrets.get(canonical)
    if not isinstance(smtp, dict) or smtp.get("file") != "../" + canonical_path:
        raise error("invalid_lab_source")
    serialized = _json_dump(document, error)
    if old in secrets or old_path in serialized:
        raise error("source_cutover_pending")
    auth = _mapping(services.get("auth"), "invalid_lab_source", error)
    if auth.get("extends") != LAB_COMMON_EXTENDS:
        raise error("invalid_lab_source")
    profiles = auth.get("profiles")
    if not isinstance(profiles, list) or not profiles or LAB_PROFILE not in profiles:
        raise error("invalid_lab_source")
    image = auth.get("image")
    if image != LAB_AUTH_IMAGE:
        raise error("invalid_lab_source")
    labels = auth.get("labels")
    if not isinstance(labels, dict) or labels.get("hy-home.tier") != LAB_TIER:
        raise error("invalid_lab_source")
    environment = auth.get("environment")
    if not isinstance(environment, dict):
        raise error("invalid_lab_source")
    if "GOTRUE_SMTP_PASS" in environment:
        raise error("invalid_lab_source")
    if environment.get("GOTRUE_SMTP_PASS_FILE") != LAB_SMTP_TARGET_FILE:
        raise error("invalid_lab_source")
    entrypoint = auth.get("entrypoint")
    if (
        not isinstance(entrypoint, list)
        or len(entrypoint) != 4
        or entrypoint[:2] != ["/bin/sh", "-ec"]
        or not isinstance(entrypoint[2], str)
        or not entrypoint[2].strip()
        or not isinstance(entrypoint[3], str)
        or not entrypoint[3].strip()
    ):
        raise error("invalid_lab_source")
    entrypoint_digest = hashlib.sha256(
        json.dumps(entrypoint, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    if entrypoint_digest != LAB_AUTH_ENTRYPOINT_SHA256:
        raise error("invalid_lab_source")
    if auth.get("command") != ["auth"]:
        raise error("invalid_lab_source")
    if (canonical, LAB_SMTP_TARGET) not in grants(auth):
        raise error("auth_alias_missing")
    return auth


def validate_root_documents(
    documents,
    *,
    require_auth,
    canonical,
    canonical_path,
    old,
    old_path,
    grants,
    unify,
    error,
    selected_auth_alias=None,
):
    root_document = documents[0]
    unified = unify(root_document)
    if unified != root_document:
        raise error("source_cutover_pending")
    auth_seen = bool(selected_auth_alias) if selected_auth_alias is not None else False
    for document in documents:
        if old_path in _json_dump(document, error):
            raise error("source_cutover_pending")
        if old in document.get("secrets", {}):
            raise error("source_cutover_pending")
        definitions = document.get("secrets", {})
        if not isinstance(definitions, dict):
            raise error("invalid_secret_definition")
        if document is not root_document:
            for name, entry in definitions.items():
                filename = entry.get("file") if isinstance(entry, dict) else None
                normalized_file = None
                if isinstance(filename, str) and not Path(filename).is_absolute():
                    normalized_file = posixpath.normpath(filename.replace(os.sep, "/"))
                if (
                    name == canonical
                    or filename
                    in (
                        canonical_path,
                        "./" + canonical_path,
                        old_path,
                        "./" + old_path,
                    )
                    or normalized_file in (canonical_path, old_path)
                ):
                    raise error("included_smtp_redefinition")
        services = document.get("services", {})
        if not isinstance(services, dict):
            raise error("invalid_services")
        for name, service in services.items():
            if not isinstance(service, dict):
                raise error("invalid_service")
            for source, target in grants(service):
                if source == old:
                    raise error("source_cutover_pending")
                if (
                    selected_auth_alias is None
                    and name == "auth"
                    and source == canonical
                    and target == old
                ):
                    auth_seen = True
    if require_auth and not auth_seen:
        raise error("auth_alias_missing")


def validate_lab_sources(
    root, *, canonical, canonical_path, old, old_path, grants, error
):
    lab = read_public_yaml(root, LAB_SUPABASE_PATH, error)
    if lab is None:
        return {}, False
    lab_data, lab_document = lab
    _lab_auth_service(
        lab_document,
        canonical=canonical,
        canonical_path=canonical_path,
        old=old,
        old_path=old_path,
        grants=grants,
        error=error,
    )
    common = read_public_yaml(root, LAB_COMMON_EXTENDS_PATH, error)
    if common is None:
        raise error("invalid_lab_source")
    common_data, common_document = common
    services = _mapping(common_document.get("services"), "invalid_lab_source", error)
    template = services.get(LAB_COMMON_EXTENDS["service"])
    if not isinstance(template, dict):
        raise error("invalid_lab_source")
    template_payload = _json_dump(template, error)
    if (
        old_path in template_payload
        or old in template_payload
        or "SMTP" in template_payload.upper()
    ):
        raise error("invalid_lab_source")
    return {
        LAB_SUPABASE_PATH: hashlib.sha256(lab_data).hexdigest(),
        LAB_COMMON_EXTENDS_PATH: hashlib.sha256(common_data).hexdigest(),
    }, True
