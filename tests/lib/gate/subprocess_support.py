"""Test subprocess support for the CI Gate's held repository root."""

from __future__ import annotations

import os
import pathlib
import re
import stat


_PROC_FD_ROOT = re.compile(r"/proc/self/fd/(0|[1-9][0-9]*)")


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
