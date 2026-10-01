"""Copy live SQLite databases with the Online Backup API and verify each copy."""

import os
import pathlib
import sqlite3
import sys

SOURCES = {
    "grafana": pathlib.Path("/src/grafana/grafana.db"),
    "gatus": pathlib.Path("/src/gatus/gatus.db"),
    "open-webui": pathlib.Path("/src/open-webui/webui.db"),
}
TARGET = pathlib.Path("/exports/sqlite")


def export(name: str, source: pathlib.Path) -> None:
    if not source.is_file() or source.is_symlink():
        raise SystemExit(f"{name}: source database missing or not a regular file")
    TARGET.mkdir(mode=0o700, exist_ok=True)
    sidecars = [source.with_name(source.name + suffix) for suffix in ("-wal", "-shm")]
    existed = {path: path.exists() for path in sidecars}
    owner = source.stat()
    partial = TARGET / f"{name}.db.partial"
    final = TARGET / f"{name}.db"
    partial.unlink(missing_ok=True)
    src = sqlite3.connect(f"file:{source}?mode=ro", uri=True, timeout=60)
    dst = sqlite3.connect(partial)
    try:
        src.backup(dst)
        result = dst.execute("PRAGMA integrity_check").fetchone()[0]
    finally:
        dst.close()
        src.close()
        # Opening a stopped WAL database creates -wal/-shm as root; hand any new
        # sidecar back to the database owner so the application can open it.
        for path, was_there in existed.items():
            if not was_there and path.exists():
                os.chown(path, owner.st_uid, owner.st_gid)
    if result != "ok":
        partial.unlink(missing_ok=True)
        raise SystemExit(f"{name}: integrity_check failed")
    uid, gid = (int(part) for part in os.environ["HYHOME_EXPORT_OWNER"].split(":"))
    os.chmod(partial, 0o600)
    os.chown(partial, uid, gid)
    partial.replace(final)
    print(f"{name}: exported {final.stat().st_size} bytes, integrity ok")


def main(names: list[str]) -> int:
    for name in names or list(SOURCES):
        if name not in SOURCES:
            raise SystemExit(f"unknown database: {name}")
        export(name, SOURCES[name])
    uid, gid = (int(part) for part in os.environ["HYHOME_EXPORT_OWNER"].split(":"))
    os.chown(TARGET, uid, gid)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
