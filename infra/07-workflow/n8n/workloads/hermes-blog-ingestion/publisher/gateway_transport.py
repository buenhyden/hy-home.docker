"""Explicit, Outbox-bound Gateway v1 replay; never enabled automatically.

Only enable replay after independently validating the n8n relay preserves the
identical request and Gateway response semantics. The generic HTTP transport
remains unable to reconcile on its own.
"""

import hashlib
import json

from .delivery import DispatchRequest, FailureKind, TransportFailure
from .gateway_adapter import DESTINATION, REVISION


def _object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("invalid_json")
        result[key] = value
    return result


def _validate(box, request, status):
    if not isinstance(request, DispatchRequest):
        raise ValueError("invalid_request")
    if (
        not isinstance(request.key, tuple)
        or len(request.key) != 2
        or not all(isinstance(part, str) for part in request.key)
        or not isinstance(request.body, bytes)
        or request.contract_revision != REVISION
        or request.destination != DESTINATION
        or hashlib.sha256(request.body).hexdigest() != request.body_sha256
    ):
        raise ValueError("invalid_request")
    row = box.get(request.key)
    if (
        (row["job_id"], row["run_id"]) != request.key
        or row["status"] != status
        or row["source_sha256"] != request.source_sha256
        or row["body_sha256"] != request.body_sha256
        or row["request_body"] != request.body
        or row["contract_revision"] != REVISION
        or row["destination"] != DESTINATION
    ):
        raise ValueError("invalid_binding")
    payload = json.loads(request.body.decode("utf-8"), object_pairs_hook=_object)
    key = hashlib.sha256((request.key[0] + ":" + request.key[1]).encode()).hexdigest()
    if (
        payload["job_id"] != request.key[0]
        or payload["run_id"] != request.key[1]
        or payload["source_sha256"] != request.source_sha256
        or payload["idempotency_key"] != key
    ):
        raise ValueError("invalid_binding")


class GatewayReplayTransport:
    """POST an immutable Outbox binding; opt in separately to replay."""

    def __init__(self, outbox, transport, *, allow_idempotent_replay=False):
        if type(allow_idempotent_replay) is not bool:
            raise ValueError("invalid_configuration")
        self._outbox = outbox
        self._transport = transport
        self._allow_replay = allow_idempotent_replay

    def _bound(self, request, status, failure):
        try:
            _validate(self._outbox, request, status)
        except Exception:
            raise TransportFailure(failure) from None

    def send(self, request):
        self._bound(request, "sending", FailureKind.NOT_SENT)
        return self._transport.send(request)

    def reconcile(self, request):
        if not self._allow_replay:
            raise TransportFailure(FailureKind.AMBIGUOUS)
        self._bound(request, "uncertain", FailureKind.AMBIGUOUS)
        return self._transport.send(request)
