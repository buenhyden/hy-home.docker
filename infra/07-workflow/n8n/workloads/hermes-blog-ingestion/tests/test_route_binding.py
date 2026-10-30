"""Synthetic immutable network endpoint binding tests."""

import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from publisher.candidates import Snapshot
from publisher.delivery import BoundRequest, process_one
from publisher.http_transport import HttpTransport
from publisher.outbox import Outbox

KEY = ("6eabd835f969", "a" * 32)


class Adapter:
    def prepare(self, snapshot):
        return BoundRequest("test", "local", b"payload")


def transport(endpoint):
    return HttpTransport(
        endpoint=endpoint, destination="local", auth=("X-Test", "fake")
    )


class RouteBindingTests(unittest.TestCase):
    def test_endpoint_change_after_restart_cannot_send(self):
        with tempfile.TemporaryDirectory(dir="/tmp") as tmp:
            path = Path(tmp) / "private" / "box.sqlite"
            box = Outbox(path)
            box.stage(Snapshot(*KEY, b"candidate", "source", b"report"))
            with patch(
                "publisher.http_transport.subprocess.run", side_effect=RuntimeError
            ):
                self.assertEqual(
                    process_one(
                        box, KEY, Adapter(), transport("https://first.test/in"), now=100
                    ),
                    "uncertain",
                )
            digest = box.get(KEY)["endpoint_sha256"]
            self.assertRegex(digest, r"^[0-9a-f]{64}$")
            box.close()
            box = Outbox(path)
            with patch("publisher.http_transport.subprocess.run") as send:
                self.assertEqual(
                    process_one(
                        box,
                        KEY,
                        Adapter(),
                        transport("https://second.test/in"),
                        now=200,
                    ),
                    "uncertain",
                )
                send.assert_not_called()
            self.assertEqual(box.get(KEY)["endpoint_sha256"], digest)
            box.close()

    def test_preexisting_unbound_request_cannot_acquire_endpoint(self):
        with tempfile.TemporaryDirectory(dir="/tmp") as tmp:
            box = Outbox(Path(tmp) / "private" / "box.sqlite")
            box.stage(Snapshot(*KEY, b"candidate", "source", b"report"))
            box.bind_request(KEY, "test", b"payload", destination="local")
            with patch("publisher.http_transport.subprocess.run") as send:
                self.assertEqual(
                    process_one(
                        box, KEY, Adapter(), transport("https://first.test/in"), now=100
                    ),
                    "failed",
                )
                send.assert_not_called()
            box.close()

    def test_old_database_migration_does_not_bind_legacy_request(self):
        with tempfile.TemporaryDirectory(dir="/tmp") as tmp:
            path = Path(tmp) / "private" / "box.sqlite"
            box = Outbox(path)
            box.stage(Snapshot(*KEY, b"candidate", "source", b"report"))
            box.bind_request(KEY, "test", b"payload", destination="local")
            box.close()
            with sqlite3.connect(path) as database:
                database.execute("ALTER TABLE records DROP COLUMN endpoint_sha256")
            box = Outbox(path)
            self.assertIsNone(box.get(KEY)["endpoint_sha256"])
            with patch("publisher.http_transport.subprocess.run") as send:
                self.assertEqual(
                    process_one(
                        box, KEY, Adapter(), transport("https://first.test/in"), now=100
                    ),
                    "failed",
                )
                send.assert_not_called()
            box.close()

    def test_http_refuses_unbound_or_other_target(self):
        from publisher.delivery import DispatchRequest, TransportFailure

        first = transport("https://first.test/in")
        second = transport("https://second.test/in")
        request = DispatchRequest(KEY, "a" * 64, "b" * 64, "test", "local", b"payload")
        with patch("publisher.http_transport.subprocess.run") as send:
            with self.assertRaises(TransportFailure):
                first.send(request)
            with self.assertRaises(TransportFailure):
                second.send(
                    __import__("dataclasses").replace(
                        request, endpoint_sha256=first.endpoint_sha256
                    )
                )
            send.assert_not_called()
