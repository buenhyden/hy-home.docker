"""Generate public, selection-bound Prometheus observation inputs.

The source configuration is read without interpolation or private input.  The
runtime plan is separately validated by compose_start before rendering.
"""

from __future__ import annotations

import re
from pathlib import Path, PurePosixPath

import yaml

from scripts.lib.document_governance.operations_catalog import read_bounded_regular
from scripts.lib.supply_chain.latest_version_gate import expected_from_root

CONFIG = PurePosixPath("infra/06-observability/prometheus/config/prometheus.yml")
DEV_CONFIG = PurePosixPath(
    "infra/06-observability/prometheus/config/prometheus.dev.yml"
)
START = PurePosixPath("infra/06-observability/prometheus/scripts/start.sh")
EXPECTED_GLOB = "/etc/prometheus/expected/*.yml"
_JOB = re.compile(r"[A-Za-z0-9_:.-]+\Z")
_DURATION = re.compile(r"([0-9]+)(ms|s|m|h)\Z")


class ObservationError(ValueError):
    """Fixed, non-sensitive observation contract failure."""


class _UniqueLoader(yaml.SafeLoader):
    pass


def _mapping(loader, node, deep=False):
    result = {}
    for key, value in node.value:
        key = loader.construct_object(key, deep=deep)
        if not isinstance(key, str) or key in result:
            raise ObservationError("duplicate_or_invalid_key")
        result[key] = loader.construct_object(value, deep=deep)
    return result


_UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _mapping)


def _public(root, relative):
    return read_bounded_regular(Path(root), relative)


def _configuration(root):
    try:
        primary = yaml.load(_public(root, CONFIG), Loader=_UniqueLoader)
        alternate = yaml.load(_public(root, DEV_CONFIG), Loader=_UniqueLoader)
    except (yaml.YAMLError, UnicodeError) as error:
        raise ObservationError("invalid_prometheus_config") from error
    if not isinstance(primary, dict) or primary != alternate:
        raise ObservationError("incompatible_prometheus_configs")
    return primary


def _seconds(value):
    if not isinstance(value, str) or (match := _DURATION.fullmatch(value)) is None:
        raise ObservationError("unsupported_scrape_interval")
    number = int(match.group(1))
    multiplier = {"ms": 0.001, "s": 1, "m": 60, "h": 3600}[match.group(2)]
    seconds = number * multiplier
    if not 1 <= seconds <= 86400:
        raise ObservationError("unsupported_scrape_interval")
    return int(seconds) if float(seconds).is_integer() else seconds


def _target_service(target, job, service_names):
    if not isinstance(target, str) or target.count(":") != 1:
        raise ObservationError("unsupported_scrape_target")
    hostname, port = target.rsplit(":", 1)
    if not hostname or not port.isdecimal() or not 1 <= int(port) <= 65535:
        raise ObservationError("unsupported_scrape_target")
    service = (
        "prometheus" if hostname == "localhost" and job == "prometheus" else hostname
    )
    if service not in service_names:
        raise ObservationError("unresolved_scrape_service")
    return service


def _file_sd_services(job, definitions, start, service_names):
    if not isinstance(definitions, list) or len(definitions) != 1:
        raise ObservationError("unsupported_file_discovery")
    files = definitions[0].get("files") if isinstance(definitions[0], dict) else None
    if files != [f"/etc/prometheus/targets/{job}.yml"] or job not in service_names:
        raise ObservationError("unsupported_file_discovery")
    render_marker = f"render {job} {job}:"
    destination_marker = f'"$dir/{job}.yml"'
    if render_marker not in start and destination_marker not in start:
        raise ObservationError("unresolved_file_discovery")
    return [job]


def inspect_targets(root, selected_services):
    """Return selected/unselected targets from source, never observed up series."""
    if not isinstance(selected_services, (set, frozenset, list, tuple)) or any(
        not isinstance(name, str) for name in selected_services
    ):
        raise ObservationError("invalid_service_selection")
    selected = frozenset(selected_services)
    service_names, _ = expected_from_root(root)
    service_names = frozenset(service_names)
    if not selected <= service_names:
        raise ObservationError("unknown_selected_service")
    config = _configuration(root)
    global_config = config.get("global", {})
    if not isinstance(global_config, dict):
        raise ObservationError("invalid_prometheus_config")
    default_interval = _seconds(global_config.get("scrape_interval", "1m"))
    jobs = config.get("scrape_configs")
    if not isinstance(jobs, list) or not jobs:
        raise ObservationError("invalid_scrape_jobs")
    start = _public(root, START).decode("utf-8")
    rows, seen = [], set()
    for job in jobs:
        if not isinstance(job, dict):
            raise ObservationError("invalid_scrape_job")
        name = job.get("job_name")
        if not isinstance(name, str) or not _JOB.fullmatch(name) or name in seen:
            raise ObservationError("invalid_or_duplicate_job")
        seen.add(name)
        interval = (
            _seconds(job["scrape_interval"])
            if "scrape_interval" in job
            else default_interval
        )
        services = []
        endpoints = set()
        for group in job.get("static_configs", []):
            if not isinstance(group, dict) or not isinstance(
                group.get("targets"), list
            ):
                raise ObservationError("invalid_static_targets")
            for item in group["targets"]:
                if item in endpoints:
                    raise ObservationError("duplicate_scrape_target")
                endpoints.add(item)
                services.append(_target_service(item, name, service_names))
        if "file_sd_configs" in job:
            discovered = _file_sd_services(
                name, job["file_sd_configs"], start, service_names
            )
            # Generated file discovery and a static target for the same service
            # cannot be safely counted without resolving the runtime port.
            if set(discovered) & set(services):
                raise ObservationError("ambiguous_scrape_target")
            services.extend(discovered)
        if not services or any(
            key.endswith("_sd_configs") and key != "file_sd_configs" for key in job
        ):
            raise ObservationError("unsupported_scrape_discovery")
        selected_count = sum(item in selected for item in services)
        rows.append(
            {
                "job": name,
                "services": sorted(set(services)),
                "target_count": len(services),
                "selected_count": selected_count,
                "scrape_interval_seconds": interval,
                "selected": selected_count > 0,
            }
        )
    return rows


def render(root, plan):
    """Render source-bound configuration and independent expected-count rules."""
    from scripts.lib.ops.compose_start import validate_plan

    plan = validate_plan(root, plan)
    if plan["mode"] not in ("home", "profile"):
        raise ObservationError("partial_selection")
    config = _configuration(root)
    rules = []
    rows = plan["observations"]
    for job, row in zip(config["scrape_configs"], rows, strict=True):
        # Current jobs all have one target. Refuse a mixed job until its targets
        # can be mapped individually rather than misclassifying an endpoint.
        if 0 < row["selected_count"] < row["target_count"]:
            raise ObservationError("mixed_selection_job")
        relabel = job.setdefault("relabel_configs", [])
        if not isinstance(relabel, list):
            raise ObservationError("invalid_relabel_configs")
        relabel.append(
            {
                "target_label": "expected_state",
                "replacement": "on" if row["selected"] else "off",
            }
        )
        labels = {"job": row["job"]}
        rules.extend(
            [
                {
                    "record": "hyhome_expected_job_info",
                    "expr": "vector(1)",
                    "labels": labels,
                },
                {
                    "record": "hyhome_expected_scrape_targets",
                    "expr": f"vector({row['selected_count']})",
                    "labels": labels,
                },
                {
                    "record": "hyhome_expected_scrape_interval_seconds",
                    "expr": f"vector({row['scrape_interval_seconds']})",
                    "labels": labels,
                },
            ]
        )
    config.setdefault("rule_files", []).append(EXPECTED_GLOB)
    rules.insert(0, {"record": "hyhome_expected_selection_info", "expr": "vector(1)"})
    rules.insert(
        1, {"record": "hyhome_expected_jobs_total", "expr": f"vector({len(rows)})"}
    )

    def dump(obj):
        return yaml.safe_dump(obj, sort_keys=False, allow_unicode=True).encode()

    return (
        dump(config),
        dump({"groups": [{"name": "selection.expected", "rules": rules}]}),
        {
            "fingerprint": plan["fingerprint"],
            "dev_data_expected": plan["dev_data_expected"],
        },
    )


def _outputs(root, plan, directory):
    config, rules, _ = render(root, plan)
    overlay = {
        "services": {
            "prometheus": {
                "environment": {"P07_DECLARED_DEV_EXPECTED": plan["dev_data_expected"]},
                "volumes": [
                    {
                        "type": "bind",
                        "source": str(directory / "prometheus.yml"),
                        "target": "/etc/prometheus/prometheus.yml",
                        "read_only": True,
                    },
                    {
                        "type": "bind",
                        "source": str(directory / "selection.yml"),
                        "target": "/etc/prometheus/expected/selection.yml",
                        "read_only": True,
                    },
                ],
            }
        }
    }
    return {
        "prometheus.yml": config,
        "selection.yml": rules,
        "overlay.yml": yaml.safe_dump(overlay, sort_keys=False).encode(),
    }


def _selection_path(root, plan, output_dir):
    root = Path(root)
    if not root.is_absolute() or root.resolve(strict=True) != root:
        raise ObservationError("unsafe_root")
    fingerprint = plan.get("fingerprint")
    if not isinstance(fingerprint, str) or not re.fullmatch(
        r"[a-f0-9]{64}", fingerprint
    ):
        raise ObservationError("invalid_fingerprint")
    expected = root / "_workspace/repo-support/analysis/p07/selections" / fingerprint
    import os

    temporary = Path("/tmp") / f"hyhome-p07-{os.geteuid()}" / fingerprint
    if Path(output_dir) not in (expected, temporary):
        raise ObservationError("unsafe_output_path")
    return Path(output_dir)


def _open_directory(path):
    import os
    import stat

    fd = os.open("/", os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for part in path.parts[1:]:
            next_fd = os.open(
                part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd
            )
            os.close(fd)
            fd = next_fd
        info = os.fstat(fd)
        if info.st_uid != os.geteuid() or stat.S_IMODE(info.st_mode) & 0o022:
            raise ObservationError("unsafe_output_directory")
        return fd
    except BaseException:
        os.close(fd)
        raise


def validate_materialized(root, plan, overlay_path):
    import os
    import stat

    directory = _selection_path(root, plan, Path(overlay_path).parent)
    if Path(overlay_path).name != "overlay.yml":
        raise ObservationError("invalid_overlay_path")
    expected = _outputs(root, plan, directory)
    if directory.parent.parent == Path("/tmp"):
        parent_fd = _temporary_parent(directory.parent, create=False)
        os.close(parent_fd)
    fd = _open_directory(directory)
    try:
        if (
            directory.parent.parent == Path("/tmp")
            and stat.S_IMODE(os.fstat(fd).st_mode) != 0o700
        ):
            raise ObservationError("unsafe_output_directory")
        for name, data in expected.items():
            file_fd = os.open(
                name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=fd
            )
            try:
                info = os.fstat(file_fd)
                if (
                    not stat.S_ISREG(info.st_mode)
                    or info.st_uid != os.geteuid()
                    or info.st_nlink != 1
                    or info.st_mode & 0o022
                ):
                    raise ObservationError("unsafe_output_file")
                read = b""
                while len(read) <= len(data):
                    chunk = os.read(file_fd, len(data) + 1 - len(read))
                    if not chunk:
                        break
                    read += chunk
                after = os.fstat(file_fd)

                def identity(st):
                    return (
                        st.st_dev,
                        st.st_ino,
                        st.st_mode,
                        st.st_uid,
                        st.st_nlink,
                        st.st_size,
                        st.st_mtime_ns,
                        st.st_ctime_ns,
                    )

                if read != data or identity(after) != identity(info):
                    raise ObservationError("output_mismatch")
                path_info = os.stat(name, dir_fd=fd, follow_symlinks=False)
                if (path_info.st_dev, path_info.st_ino) != (info.st_dev, info.st_ino):
                    raise ObservationError("output_rebound")
            finally:
                os.close(file_fd)
    finally:
        os.close(fd)
    return directory / "overlay.yml"


def _ensure_parent(root, parent):
    import os
    import stat

    if parent.parent == Path("/tmp"):
        fd = _temporary_parent(parent)
        return fd
    fd = _open_directory(root)
    try:
        for part in parent.relative_to(root).parts:
            try:
                os.mkdir(part, 0o755, dir_fd=fd)
            except FileExistsError:
                pass
            child = os.open(
                part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd
            )
            info = os.fstat(child)
            if info.st_uid != os.geteuid() or stat.S_IMODE(info.st_mode) & 0o022:
                os.close(child)
                raise ObservationError("unsafe_output_directory")
            os.close(fd)
            fd = child
        return fd
    except BaseException:
        os.close(fd)
        raise


def _temporary_parent(parent, *, create=True):
    import os
    import stat

    tmp_fd = os.open("/tmp", os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        info = os.fstat(tmp_fd)
        if info.st_uid != 0 or stat.S_IMODE(info.st_mode) != 0o1777:
            raise ObservationError("unsafe_temporary_root")
        if create:
            try:
                os.mkdir(parent.name, 0o700, dir_fd=tmp_fd)
            except FileExistsError:
                pass
        fd = os.open(
            parent.name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=tmp_fd
        )
        info = os.fstat(fd)
        current = os.stat(parent.name, dir_fd=tmp_fd, follow_symlinks=False)
        if (
            info.st_uid != os.geteuid()
            or stat.S_IMODE(info.st_mode) != 0o700
            or (info.st_dev, info.st_ino) != (current.st_dev, current.st_ino)
        ):
            os.close(fd)
            raise ObservationError("unsafe_temporary_directory")
        return fd
    finally:
        os.close(tmp_fd)


def materialize(root, plan, output_dir):
    """Publish new full-plan files atomically; never replace prior output."""
    import ctypes
    import errno
    import os
    import secrets

    directory = _selection_path(root, plan, output_dir)
    outputs = _outputs(root, plan, directory)
    parent_fd = _ensure_parent(Path(root), directory.parent)
    temporary = ".p07-" + secrets.token_hex(16)
    created = False
    try:
        os.mkdir(
            temporary,
            0o700 if directory.parent.parent == Path("/tmp") else 0o755,
            dir_fd=parent_fd,
        )
        created = True
        temp_fd = os.open(
            temporary, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=parent_fd
        )
        try:
            for name, data in outputs.items():
                file_fd = os.open(
                    name,
                    os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                    0o644,
                    dir_fd=temp_fd,
                )
                try:
                    with os.fdopen(file_fd, "wb") as stream:
                        stream.write(data)
                        stream.flush()
                        os.fsync(stream.fileno())
                except BaseException:
                    raise
            os.fsync(temp_fd)
        finally:
            os.close(temp_fd)
        libc = ctypes.CDLL(None, use_errno=True)
        renameat2 = libc.renameat2
        result = renameat2(
            parent_fd, temporary.encode(), parent_fd, directory.name.encode(), 1
        )
        if result:
            error = ctypes.get_errno()
            if error == errno.EEXIST:
                return validate_materialized(root, plan, directory / "overlay.yml")
            raise OSError(error, os.strerror(error))
        created = False
        os.fsync(parent_fd)
        return validate_materialized(root, plan, directory / "overlay.yml")
    finally:
        if created:
            tmp_fd = os.open(
                temporary,
                os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                dir_fd=parent_fd,
            )
            try:
                for name in outputs:
                    try:
                        os.unlink(name, dir_fd=tmp_fd)
                    except FileNotFoundError:
                        pass
            finally:
                os.close(tmp_fd)
            os.rmdir(temporary, dir_fd=parent_fd)
        os.close(parent_fd)
