"""Exact-path Traefik contract for a synthetic, two-network quality fixture."""

from __future__ import annotations

import pathlib
import re
import stat
from collections.abc import Callable
from typing import Any

COMMAND = [
    "--entrypoints.quality.address=:8080",
    "--providers.file.filename=/guard/routes.yml",
    "--providers.file.watch=false",
    "--api=false",
    "--ping=false",
    "--log.level=ERROR",
]
IMAGE = re.compile(r"(?:docker.io/library/)?traefik@sha256:[0-9a-f]{64}")


def configuration(manifest: dict[str, Any]) -> dict[str, Any]:
    from quality_run import validate_manifest

    validate_manifest(manifest)
    paths = manifest["target"]["paths"]
    if any("`" in path for path in paths):
        raise ValueError("guard path contains a rule delimiter")
    return {
        "http": {
            "routers": {
                "approved": {
                    "entryPoints": ["quality"],
                    "rule": "Host(`wiremock`) && ("
                    + " || ".join(f"Path(`{path}`)" for path in paths)
                    + ")",
                    "service": "backend",
                }
            },
            "services": {
                "backend": {
                    "loadBalancer": {
                        "servers": [{"url": "http://quality-backend:8080"}],
                    }
                }
            },
        }
    }


def validate(
    manifest: dict[str, Any],
    gateway: dict[str, Any],
    runner_network: str,
    backend_network: str,
    backend_name: str,
    config_path: pathlib.Path,
    inspect: Callable[[str, str], dict[str, Any]],
    canonical: Callable[[object], bytes],
) -> None:
    """Reject every non-fixture peer/provider/network/mount before k6 starts."""
    from container_executor import ExecutorError, _peer_contract

    def reject() -> None:
        raise ExecutorError("HTTP guard isolation contract is invalid")

    path = config_path.absolute()
    try:
        if (
            path.is_symlink()
            or not stat.S_ISREG(path.lstat().st_mode)
            or path.read_bytes() != canonical(configuration(manifest))
        ):
            reject()
    except (OSError, ValueError) as exc:
        raise ExecutorError("HTTP guard configuration differs from manifest") from exc
    config = gateway.get("Config", {})
    host = gateway.get("HostConfig", {})
    settings = gateway.get("NetworkSettings", {})
    if not all(isinstance(item, dict) for item in (config, host, settings)):
        reject()
    labels = config.get("Labels", {})
    networks = settings.get("Networks", {})
    mounts = gateway.get("Mounts")
    image = config.get("Image")
    if (
        not isinstance(labels, dict)
        or labels.get("hyhome.quality.run_id") != manifest["run_id"]
        or labels.get("hyhome.quality.role") != "http-guard"
        or not isinstance(image, str)
        or not IMAGE.fullmatch(image)
        or config.get("Cmd") != COMMAND
        or not isinstance(config.get("Env"), list)
        or any(
            not isinstance(item, str) or item.startswith("TRAEFIK_")
            for item in config["Env"]
        )
        or host.get("ReadonlyRootfs") is not True
        or host.get("PortBindings") not in (None, {})
        or host.get("ExtraHosts") not in (None, [])
        or host.get("Privileged") is not False
        or host.get("CapDrop") != ["ALL"]
        or host.get("CapAdd") not in (None, [])
        or not isinstance(networks, dict)
        or set(networks) != {runner_network, backend_network}
        or not isinstance(networks[runner_network], dict)
        or "wiremock" not in (networks[runner_network].get("Aliases") or [])
        or not isinstance(mounts, list)
        or len(mounts) != 1
    ):
        reject()
    mount = mounts[0]
    if (
        not isinstance(mount, dict)
        or mount.get("Type") != "bind"
        or mount.get("Source") != str(path)
        or mount.get("Destination") != "/guard/routes.yml"
        or mount.get("RW") is not False
    ):
        reject()
    backend = inspect("network", backend_network)
    peers = backend.get("Containers")
    backend_labels = backend.get("Labels")
    if (
        backend.get("Name") != backend_network
        or backend.get("Driver") != "bridge"
        or backend.get("Scope") != "local"
        or backend.get("Internal") is not True
        or backend.get("Attachable") is not False
        or not isinstance(backend_labels, dict)
        or backend_labels.get("hyhome.quality.run_id") != manifest["run_id"]
        or not isinstance(peers, dict)
        or len(peers) != 2
        or gateway.get("Id") not in peers
    ):
        reject()
    backend_peer = inspect("container", backend_name)
    if backend_peer.get("Id") not in peers:
        reject()
    _peer_contract(
        manifest, backend_peer, backend_network, backend_name, backend_peer["Id"]
    )
    alias = backend_peer["NetworkSettings"]["Networks"][backend_network].get(
        "Aliases", []
    )
    if "quality-backend" not in alias:
        reject()
