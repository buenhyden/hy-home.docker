"""Frozen image, ownership, resource, and tmpfs inputs for the native rehearsal."""

OWNER_LABEL = "hyhome.opsflow.native-owner"
ATTEMPT_LABEL = "hyhome.opsflow.native-attempt"
ROLE_LABEL = "hyhome.opsflow.native-role"
OWNER = "test_opsflow_native_rehearsal"

N8N_ID = "sha256:1fda18a541144ae5519ac97bcaffa4e24fad0e71d424606d230464bec8fce153"
N8N_REF = "hy-home/sec01-n8n:2.43.6-opsflow-03892eb1a9a4"
N8N_LABELS = {
    "hyhome.source-binding": "03892eb1a9a485b454e48c8222ecebc116d67a846560bf97fb8a783e5f6d8985",
    "hyhome.source-tree": "f511528aba724372aa0ed61b7b3c2e271d2d6942",
    "org.opencontainers.image.revision": "64434387a86b4edb65d4583ee449785eb6ec1276",
}
PG_ID = "sha256:77f585114c32fbca283dc835b0596f4e52b51b4c6662d7810b2f4084f60a1873"
PG_REF = "postgres:18.6-alpine"
VALKEY_ID = "sha256:a0dbf4c1d5708782907c10e2c72deff317518518b5288a58416981d9db95d30b"
VALKEY_REF = "valkey/valkey:9.1.2-alpine"
RUNNER_ID = "sha256:3168a82b29b3a8ec9acbe876d9e654b3333dfd630b257f6cc2bc81fc5f93b2bf"
RUNNER_REF = "n8nio/runners:2.43.6@" + RUNNER_ID
RUNNER_RUNTIME_CONFIG = (
    "sha256:28c5a510d7624e5ce079d2204e4d8421bc96ced83ebc2e1717d6ee33a0ccc1bb"
)
MAILPIT_ID = "sha256:94f6b70c1436defae6799d9ac7ff0eeff9540465b842026d5cdb018f1c0234ea"
MAILPIT_REF = "axllent/mailpit:v1.31.5@" + MAILPIT_ID
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
    "mailpit": (
        "/data:rw,nosuid,nodev,noexec,mode=0700,uid=1000,gid=1000,size=64m",
        "/tmp:rw,nosuid,nodev,noexec,mode=1777,size=16m",
    ),
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
    "valkey": "n8n-valkey",
    "main": "n8n",
    "worker": "n8n-worker",
    "runner": "runner",
    "mailpit": "mailpit",
    "capture-probe": "capture-probe",
}
