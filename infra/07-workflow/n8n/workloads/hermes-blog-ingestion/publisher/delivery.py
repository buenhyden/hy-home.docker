"""Adapter-independent delivery engine. No HTTP or production Gateway contract.

Only a separately reviewed adapter may interpret authenticated Gateway evidence.
The types below are local interfaces, never a proposed Gateway wire format.
"""

import hashlib
import math
import time
from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import Enum
from types import MappingProxyType
from typing import Protocol

from . import trust
from .outbox import Outbox, OutboxError, valid_gateway_report_id

Key = tuple[str, str]


@dataclass(frozen=True)
class BoundRequest:
    contract_revision: str
    destination: str
    body: bytes = field(repr=False)


@dataclass(frozen=True)
class DispatchRequest:
    key: Key
    source_sha256: str
    body_sha256: str
    contract_revision: str
    destination: str
    body: bytes = field(repr=False)
    endpoint_sha256: str | None = None
    # SHA-256 of the producer-authenticated evidence this request was built from.
    trust: str | None = None


@dataclass(frozen=True)
class Receipt:
    key: Key
    source_sha256: str
    body_sha256: str
    persisted: bool
    gateway_report_id: str | None = None


class OutcomeKind(Enum):
    DURABLE = "durable"
    ABSENT = "absent"
    CONFLICT = "conflict"
    REJECTED = "rejected"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class Outcome:
    kind: OutcomeKind
    receipt: Receipt | None = None


class FailureKind(Enum):
    NOT_SENT = "not_sent"
    AMBIGUOUS = "ambiguous"
    AUTH = "auth"
    TLS = "tls"
    CONFLICT = "conflict"


class TransportFailure(Exception):
    """A reviewed transport must prove NOT_SENT; timeouts are AMBIGUOUS."""

    def __init__(self, kind: FailureKind):
        if not isinstance(kind, FailureKind):
            raise ValueError("invalid_failure")
        self.kind = kind
        super().__init__(kind.value)


class Adapter(Protocol):
    idempotent_writes: bool

    def prepare(self, snapshot: Mapping) -> BoundRequest: ...

    def interpret(self, response: object, request: DispatchRequest) -> Outcome: ...


class Transport(Protocol):
    def send(self, request: DispatchRequest) -> object: ...

    def reconcile(self, request: DispatchRequest) -> object: ...


def _parameters(now, max_attempts, base_delay, max_delay):
    if type(max_attempts) is not int or not 1 <= max_attempts <= 1000:
        raise ValueError("invalid_retry_budget")
    for value in (now, base_delay, max_delay):
        if type(value) not in (int, float) or not math.isfinite(value) or value < 0:
            raise ValueError("invalid_retry_clock")
    if base_delay == 0 or max_delay == 0:
        raise ValueError("invalid_retry_clock")


def _move(box, key, expected, target, **fields):
    if not box.transition(key, expected, target, **fields):
        raise OutboxError("stale_delivery")
    return target


def _prepare_failure(box, key, status, code):
    if status == "uncertain":
        # The delivery lock serializes this check and subsequent transition.
        for event in reversed(box.events(key)):
            if event["code"] not in ("request_conflict", "adapter_error"):
                break
            if event["code"] == code:
                return "uncertain"
        return _move(box, key, status, "uncertain", code=code)
    return _move(box, key, status, "failed", code=code)


def _prepare(box, key, row, adapter, transport, token):
    try:
        bound = adapter.prepare(MappingProxyType(dict(row)))
        if not isinstance(bound, BoundRequest):
            raise ValueError("invalid_request")
        endpoint_sha256 = getattr(transport, "endpoint_sha256", None)
        body = box.bind_request(
            key,
            bound.contract_revision,
            bound.body,
            destination=bound.destination,
            endpoint_sha256=endpoint_sha256,
        )
    except OutboxError as error:
        if str(error) == "evidence_unverified":
            # A trust change between gates blocks without a terminal state.
            return None, "blocked"
        return None, _prepare_failure(box, key, row["status"], "request_conflict")
    except Exception:
        return None, _prepare_failure(box, key, row["status"], "adapter_error")
    request = DispatchRequest(
        key,
        row["source_sha256"],
        hashlib.sha256(body).hexdigest(),
        bound.contract_revision,
        bound.destination,
        body,
        endpoint_sha256,
        token,
    )
    if row["status"] == "awaiting_contract":
        _move(box, key, "awaiting_contract", "pending", code="request_ready")
    return request, None


def _durable(receipt, request):
    return (
        isinstance(receipt, Receipt)
        and receipt.persisted is True
        and receipt.key == request.key
        and receipt.source_sha256 == request.source_sha256
        and receipt.body_sha256 == request.body_sha256
        and (
            receipt.gateway_report_id is None
            or valid_gateway_report_id(receipt.gateway_report_id)
        )
    )


def _interpret(box, key, status, response, request, adapter, attempts, max_attempts):
    try:
        outcome = adapter.interpret(response, request)
    except Exception:
        outcome = Outcome(OutcomeKind.UNKNOWN)
    if not isinstance(outcome, Outcome):
        outcome = Outcome(OutcomeKind.UNKNOWN)
    if outcome.kind is OutcomeKind.DURABLE and _durable(outcome.receipt, request):
        receipt = {
            "job_id": key[0],
            "run_id": key[1],
            "source_sha256": request.source_sha256,
            "body_sha256": request.body_sha256,
            "persisted": True,
        }
        if outcome.receipt.gateway_report_id is not None:
            receipt["gateway_report_id"] = outcome.receipt.gateway_report_id
        return _move(
            box,
            key,
            status,
            "delivered",
            receipt=receipt,
            next_attempt=0,
            code="durable_receipt",
        )
    if outcome.kind in (OutcomeKind.CONFLICT, OutcomeKind.REJECTED):
        if status == "uncertain":
            # A prior write may be durable, so stay uncertain, but a permanent
            # rejection exhausts the budget: no automatic re-POST follows.
            return _move(
                box,
                key,
                status,
                "uncertain",
                code="gateway_rejected",
                attempts=max_attempts,
            )
        return _move(box, key, status, "failed", code="gateway_rejected")
    if (
        status == "uncertain"
        and outcome.kind is OutcomeKind.ABSENT
        and getattr(adapter, "idempotent_writes", False) is True
    ):
        target = "failed" if attempts >= max_attempts else "pending"
        return _move(
            box,
            key,
            status,
            target,
            next_attempt=0,
            code="retry_exhausted" if target == "failed" else "absence_confirmed",
        )
    return _move(box, key, status, "uncertain", code="unconfirmed_response")


def _failure(box, key, status, kind, attempts, max_attempts):
    if kind in (FailureKind.AUTH, FailureKind.TLS, FailureKind.CONFLICT):
        # Reconciliation failure cannot disprove a prior durable write.
        target = "uncertain" if status == "uncertain" else "failed"
        return _move(
            box,
            key,
            status,
            target,
            code=f"{kind.value}_failed",
            attempts=max_attempts if target == "uncertain" else attempts,
        )
    if kind is FailureKind.NOT_SENT and status == "sending":
        target = "failed" if attempts >= max_attempts else "pending"
        return _move(
            box,
            key,
            status,
            target,
            code="retry_exhausted" if target == "failed" else "not_sent",
        )
    return _move(box, key, status, "uncertain", code="transport_uncertain")


def _operate(
    box, key, row, request, adapter, transport, now, max_attempts, base_delay, max_delay
):
    attempts = row["attempts"] + 1
    delay = min(max_delay, base_delay * 2 ** min(attempts - 1, 30))
    deadline = now + delay
    if not math.isfinite(deadline):
        raise ValueError("invalid_retry_clock")
    reconcile = row["status"] == "uncertain"
    status = "uncertain" if reconcile else "sending"
    _move(
        box,
        key,
        row["status"],
        status,
        attempts=attempts,
        next_attempt=deadline,
        code="reconcile_started" if reconcile else "send_started",
    )
    try:
        response = (
            transport.reconcile(request) if reconcile else transport.send(request)
        )
    except TransportFailure as error:
        return _failure(box, key, status, error.kind, attempts, max_attempts)
    except Exception:
        return _failure(box, key, status, FailureKind.AMBIGUOUS, attempts, max_attempts)
    return _interpret(
        box, key, status, response, request, adapter, attempts, max_attempts
    )


def process_one(
    outbox: Outbox,
    key: Key,
    adapter: Adapter | None = None,
    transport: Transport | None = None,
    *,
    now=None,
    max_attempts=5,
    base_delay=30,
    max_delay=3600,
) -> str:
    """Perform at most one transport operation, under the global Outbox lock.

    Missing contract/transport returns blocked without dispatch. Delayed work
    returns deferred; other results are durable Outbox states. Uncertainty always
    reconciles first. Only explicit absence plus idempotent writes permits a
    subsequent send. Exhausted uncertainty remains unresolved for operator review.
    No source bytes, transport responses or exception strings are logged.
    """
    now = time.time() if now is None else now
    _parameters(now, max_attempts, base_delay, max_delay)
    with outbox.delivery_lock():
        outbox.recover_sending()
        row = outbox.get(key)
        if row["status"] in ("delivered", "failed"):
            return row["status"]
        try:
            authorization = trust.authorize(outbox, key)
        except (trust.TrustError, OutboxError):
            return "blocked"
        token = None if authorization is None else authorization.evidence_sha256
        if adapter is None or transport is None:
            return "blocked"
        if row["attempts"] >= max_attempts:
            target = "uncertain" if row["status"] == "uncertain" else "failed"
            if (
                not outbox.events(key)
                or outbox.events(key)[-1]["code"] != "retry_exhausted"
            ):
                _move(outbox, key, row["status"], target, code="retry_exhausted")
            return target
        if row["next_attempt"] > now:
            return "deferred"
        request, error = _prepare(outbox, key, row, adapter, transport, token)
        if error:
            return error
        return _operate(
            outbox,
            key,
            outbox.get(key),
            request,
            adapter,
            transport,
            now,
            max_attempts,
            base_delay,
            max_delay,
        )
