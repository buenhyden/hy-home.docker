"""Synthetic requests client event contract; never records URLs or bodies."""

import importlib.util
import json
import math
import os
from pathlib import Path
from typing import ClassVar

BUCKETS = (25, 50, 100, 250, 1000)


def record_event(previous, method, group, duration_ms, exception, status):
    if method != "GET" or group not in {"health", "timeout"}:
        raise ValueError("unapproved method/group")
    if (
        isinstance(duration_ms, bool)
        or not isinstance(duration_ms, (int, float))
        or not math.isfinite(duration_ms)
        or duration_ms < 0
    ):
        raise ValueError("invalid response time")
    outcome = "timeout" if exception is not None else str(status)
    if outcome not in {"200", "timeout"}:
        raise ValueError("unexpected status")
    key = group + ":" + outcome
    result = json.loads(json.dumps(previous))
    current = result.get(
        key,
        {
            "count": 0,
            "sum_ms": 0,
            "buckets_ms": {str(b): 0 for b in BUCKETS},
            "infinity": 0,
        },
    )
    current["count"] += 1
    current["sum_ms"] += duration_ms
    current["infinity"] += 1
    for bucket in BUCKETS:
        current["buckets_ms"][str(bucket)] += duration_ms <= bucket
    result[key] = current
    return result


if importlib.util.find_spec("locust") is not None:
    from locust import HttpUser, SequentialTaskSet, between, events, task
    from locust.runners import MasterRunner
    from requests.exceptions import ReadTimeout

    observed = {}
    invalid = 0
    timeouts = 0

    @events.request.add_listener
    def capture(
        request_type, name, response_time, exception=None, response=None, **kwargs
    ):
        global observed, invalid, timeouts
        # Never consume event.url, context, headers, response body or exception text.
        if exception is not None and not isinstance(exception, ReadTimeout):
            invalid += 1
            return
        try:
            observed = record_event(
                observed,
                request_type,
                name,
                response_time,
                exception,
                response.status_code if response is not None else 0,
            )
            timeouts += exception is not None
        except ValueError:
            invalid += 1

    @events.test_stop.add_listener
    def save(environment, **kwargs):
        if isinstance(environment.runner, MasterRunner):
            return
        evidence = {
            "schema_version": "hyhome.locust-event/v1",
            "project_id": "synthetic-locust",
            "client": "HttpUser.requests",
            "counter_unit": "requests",
            "histogram_unit": "ms",
            "timeout_seconds": 0.05,
            "invalid_events": invalid,
            "read_timeouts": timeouts,
            "series": observed,
        }
        path = Path("/mnt/locust/results/events-" + str(os.getpid()) + ".json")
        with path.open("x") as stream:
            json.dump(evidence, stream, sort_keys=True)

    class SyntheticTasks(SequentialTaskSet):
        @task
        def health(self):
            self.client.get(
                "/health", name="health", timeout=(0.2, 0.2), allow_redirects=False
            )

        @task
        def timeout(self):
            self.client.get(
                "/slow", name="timeout", timeout=(0.2, 0.05), allow_redirects=False
            )

    class SyntheticUser(HttpUser):
        host = "http://mock-backend:8080"
        tasks: ClassVar[list] = [SyntheticTasks]
        wait_time = between(0.1, 0.1)
