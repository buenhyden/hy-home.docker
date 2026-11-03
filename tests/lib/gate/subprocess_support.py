"""Test subprocess support for the CI Gate's held repository root."""

from __future__ import annotations

import contextlib
import os
import pathlib
import re
import shutil
import stat
from collections.abc import Iterator
from unittest import mock

_PROC_FD_ROOT = re.compile(r"/proc/self/fd/(0|[1-9][0-9]*)")


@contextlib.contextmanager
def root_owned_system_git_fixture() -> Iterator[None]:
    """Model ownership only for the exact Git used by hosted-behavior fixtures."""
    system_git = pathlib.Path(shutil.which("git") or "/usr/bin/git")
    original_stat = pathlib.Path.stat

    def fixture_stat(path, *args, **kwargs):
        metadata = original_stat(path, *args, **kwargs)
        if path == system_git:
            fields = list(metadata)
            fields[stat.ST_UID] = 0
            return os.stat_result(fields)
        return metadata

    with mock.patch.object(pathlib.Path, "stat", fixture_stat):
        yield


def gate_root_pass_fds(expected_root: pathlib.Path) -> tuple[int, ...]:
    """Forward the Gate root only when it is the expected open directory."""

    match = _PROC_FD_ROOT.fullmatch(os.environ.get("HYHOME_CI_GATE_ROOT", ""))
    if match is None:
        return ()
    descriptor = int(match.group(1))
    try:
        held = os.fstat(descriptor)
        expected = expected_root.stat()
    except OSError:
        return ()
    if not stat.S_ISDIR(held.st_mode):
        return ()
    if (held.st_dev, held.st_ino) != (expected.st_dev, expected.st_ino):
        return ()
    return (descriptor,)
