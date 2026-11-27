"""Frozen image, ownership, resource, and tmpfs inputs for the native rehearsal."""

OWNER_LABEL = "hyhome.opsflow.native-owner"
ATTEMPT_LABEL = "hyhome.opsflow.native-attempt"
ROLE_LABEL = "hyhome.opsflow.native-role"
OWNER = "test_opsflow_native_rehearsal"

N8N_ID = "sha256:e4cbed5083c5f857ea778d243964e8e2dfe439428bef845e2ad50ee3b5a44b84"
N8N_REF = "hy-home/sec01-n8n:2.49.7-opsflow-099418ca2fb4"
N8N_LABELS = {
    "hyhome.source-binding": "099418ca2fb4e57e420b4edb3d2f661b279e3a2b78f9aed9a965a8f0e6417337",
    "hyhome.source-tree": "6a9867a31be1343f4eedbf289f19598ff105a0be",
    "org.opencontainers.image.revision": "4a5c7fe8680e55d81cf8d2b26341bc10001efdef",
}
PG_ID = "sha256:0115267ab5a509022df9319c77be365cef335adb71556c75f60f5360ee247e71"
PG_REF = "postgres:18.7-alpine"
VALKEY_ID = "sha256:56729e68bdda139cbd3f6a2538683dc3523325fc5711ea1a379938f1b37893f0"
VALKEY_REF = "valkey/valkey:9.1.4-alpine"
RUNNER_ID = "sha256:be8031ab2badedb7af0ceb68ea46ac5317bb941c06f97b3f0e9bc3bc2b67050e"
RUNNER_REF = "n8nio/runners:2.49.7@" + RUNNER_ID
RUNNER_RUNTIME_CONFIG = (
    "sha256:9aea154e132841c7c3b46efa0a285f8cdc1ac16932017f5a131d31ddb8754a21"
)
# A container's Image is the config digest with the classic image store and
# the pinned index digest with the containerd store (HOME since 2026-10-16,
# SPEC-0246). Both name the same pinned runner.
RUNNER_RUNTIME_IDS = frozenset({RUNNER_RUNTIME_CONFIG, RUNNER_ID})
MAILPIT_ID = "sha256:23a2ef85bc50853ab3093645d1d64679afd8887e89da5e48a88940c172591a4e"
MAILPIT_REF = "axllent/mailpit:v1.34.0@" + MAILPIT_ID
IMAGE_IDS = {
    N8N_REF: N8N_ID,
    PG_REF: PG_ID,
    VALKEY_REF: VALKEY_ID,
    RUNNER_REF: RUNNER_ID,
    MAILPIT_REF: MAILPIT_ID,
}

RESOURCE_CAPS = {
    "metadata-pg": ("384m", "0.20", 128),
    "dev-pg": ("512m", "0.25", 128),
    "valkey": ("128m", "0.10", 64),
    "main": ("768m", "0.35", 256),
    "worker": ("768m", "0.35", 256),
    "runner": ("384m", "0.25", 128),
    "mailpit": ("192m", "0.10", 128),
    "secret-prep": ("32m", "0.05", 16),
    "capture-probe": ("128m", "0.10", 64),
}
TMPFS = {
    "metadata-pg": (
        "/var/lib/postgresql:rw,nosuid,nodev,noexec,mode=0700,uid=70,gid=70,size=256m",
        "/var/run/postgresql:rw,nosuid,nodev,noexec,mode=0770,uid=70,gid=70,size=16m",
        "/tmp:rw,nosuid,nodev,noexec,mode=1777,size=16m",
    ),
    "dev-pg": (
        "/var/lib/postgresql:rw,nosuid,nodev,noexec,mode=0700,uid=70,gid=70,size=384m",
        "/var/run/postgresql:rw,nosuid,nodev,noexec,mode=0770,uid=70,gid=70,size=16m",
        "/tmp:rw,nosuid,nodev,noexec,mode=1777,size=16m",
    ),
    "valkey": (
        "/data:rw,nosuid,nodev,noexec,mode=0700,uid=999,gid=999,size=64m",
        "/run/valkey:rw,nosuid,nodev,noexec,mode=0700,uid=999,gid=999,size=8m",
        "/tmp:rw,nosuid,nodev,noexec,mode=1777,size=8m",
    ),
    "main": ("/tmp:rw,nosuid,nodev,noexec,mode=0700,uid=1000,gid=1000,size=192m",),
    "worker": ("/tmp:rw,nosuid,nodev,noexec,mode=0700,uid=1000,gid=1000,size=192m",),
    "runner": (
        "/tmp:rw,nosuid,nodev,noexec,mode=0700,uid=1000,gid=1000,size=128m",
        "/home/runner/.cache:rw,nosuid,nodev,noexec,mode=0700,uid=1000,gid=1000,size=64m",
    ),
    # Mailpit's /data is an owned bind so its store survives stop/start.
    "mailpit": ("/tmp:rw,nosuid,nodev,noexec,mode=1777,size=16m",),
    "capture-probe": (
        "/tmp:rw,nosuid,nodev,noexec,mode=0700,uid=1000,gid=1000,size=32m",
    ),
}


def memory_bytes(value: str) -> int:
    return int(value.removesuffix("m")) * 1024 * 1024


def bind_mount(path, target: str, *, readonly: bool = True) -> str:
    suffix = ",readonly" if readonly else ""
    return f"type=bind,src={path},dst={target}{suffix}"


def precreate_headroom_failure(
    available: int, _swap_free: int, disk_free: int, inode_percent: int, cpus: int
) -> str | None:
    if available < 7 * 1024**2:
        return "native rehearsal memory headroom is insufficient"
    if disk_free < 10 * 1024**3 or inode_percent < 10:
        return "native rehearsal disk/inode headroom is insufficient"
    if cpus < 4:
        return "native rehearsal CPU headroom is insufficient"
    return None


ALIASES = {
    "metadata-pg": "metadata-pg",
    "dev-pg": "dev-pg",
    "valkey": "mng-valkey",
    "main": "n8n",
    "worker": "n8n-worker",
    "runner": "runner",
    "mailpit": "mailpit",
    "capture-probe": "capture-probe",
}
