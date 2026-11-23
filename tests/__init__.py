"""Repository test package.

Every test process, and each hook or reconcile it starts, writes capture
records to a private temporary directory unless a test names its own, so no
test reaches the operating `.workspace-capture/` store.
"""

import atexit
import os
import shutil
import tempfile

if not os.environ.get("HY_HOME_CAPTURE_DIR"):
    _capture = tempfile.mkdtemp(prefix="hy-home-test-capture-")
    os.environ["HY_HOME_CAPTURE_DIR"] = _capture
    atexit.register(shutil.rmtree, _capture, True)
