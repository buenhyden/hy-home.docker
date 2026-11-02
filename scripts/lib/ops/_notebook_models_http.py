"""Bounded loopback HTTP transport for the pinned Open Notebook 1.15.0 API."""

from __future__ import annotations

import http.client
import json
import math
import threading
import time
import urllib.error
import urllib.request
from typing import Any
from urllib.parse import urlsplit

from scripts.lib.ops.notebook_models import PolicyError, strict_json_loads


class ApiError(PolicyError):
    """A value-free API transport, status, or response-shape failure."""

    def __init__(self, code: str, *, status: int | None = None) -> None:
        super().__init__(code)
        self.code = code
        self.status = status


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def validate_loopback_endpoint(endpoint: object) -> str:
    """Return one exact local endpoint without inspecting any credential."""

    if not isinstance(endpoint, str):
        raise PolicyError("api_endpoint_refused")
    parsed = urlsplit(endpoint)
    try:
        port = parsed.port
    except ValueError as error:
        raise PolicyError("api_endpoint_refused") from error
    if not (
        parsed.scheme == "http"
        and parsed.hostname == "127.0.0.1"
        and port is not None
        and 1 <= port <= 65535
        and not parsed.username
        and not parsed.password
        and parsed.path in {"", "/"}
        and not parsed.query
        and not parsed.fragment
    ):
        raise PolicyError("api_endpoint_refused")
    return endpoint.rstrip("/")


class OpenNotebookClient:
    """Sequential JSON client limited to a literal IPv4 loopback endpoint."""

    def __init__(
        self,
        endpoint: str,
        password: str,
        *,
        total_seconds: float = 300,
        clock=time.monotonic,
        opener=None,
    ) -> None:
        validated_endpoint = validate_loopback_endpoint(endpoint)
        if not (
            isinstance(password, str)
            and 1 <= len(password) <= 512
            and password.strip() == password
            and all(character not in password for character in "\r\n\x00")
        ):
            raise PolicyError("password_value_refused")
        if (
            isinstance(total_seconds, bool)
            or not isinstance(total_seconds, (int, float))
            or not math.isfinite(total_seconds)
            or not 0 < total_seconds <= 300
        ):
            raise PolicyError("api_budget_refused")
        self._endpoint = validated_endpoint
        self._password = password
        self._clock = clock
        self._deadline = clock() + float(total_seconds)
        self._opener = opener or urllib.request.build_opener(
            urllib.request.ProxyHandler({}), _NoRedirect()
        )
        self._lock = threading.Lock()

    def get(self, path: str) -> Any:
        return self._request("GET", path, None)

    def post(self, path: str, payload: Any) -> Any:
        return self._request("POST", path, payload)

    def put(self, path: str, payload: Any) -> Any:
        return self._request("PUT", path, payload)

    def _request(self, method: str, path: str, payload: Any) -> Any:
        if not isinstance(path, str):
            raise ApiError("api_request_refused")
        parsed_path = urlsplit(path)
        if not (
            method in {"GET", "POST", "PUT"}
            and len(path) <= 512
            and path.startswith("/api/")
            and all(0x21 <= ord(character) <= 0x7E for character in path)
            and parsed_path.scheme == ""
            and parsed_path.netloc == ""
            and parsed_path.fragment == ""
        ):
            raise ApiError("api_request_refused")
        remaining = self._deadline - self._clock()
        if remaining <= 0:
            raise ApiError("api_budget_exhausted")
        body = None
        if payload is not None:
            try:
                body = json.dumps(
                    payload, ensure_ascii=True, separators=(",", ":"), sort_keys=True
                ).encode("utf-8")
            except (TypeError, ValueError) as error:
                raise ApiError("api_request_invalid") from error
            if len(body) > 64 * 1024:
                raise ApiError("api_request_refused")
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self._password}",
            "User-Agent": "hy-home-p03-notebook-models/1",
        }
        if body is not None:
            headers["Content-Type"] = "application/json"
        request = urllib.request.Request(
            self._endpoint + path,
            data=body,
            headers=headers,
            method=method,
        )
        if not self._lock.acquire(blocking=False):
            raise ApiError("api_concurrency_refused")
        try:
            with self._opener.open(request, timeout=min(30.0, remaining)) as response:
                if not 200 <= response.status < 300:
                    raise ApiError("api_http_error", status=response.status)
                content_type = response.headers.get_content_type()
                if content_type != "application/json":
                    raise ApiError("api_response_invalid")
                response_body = bytearray()
                while True:
                    read_remaining = self._deadline - self._clock()
                    if read_remaining <= 0:
                        raise ApiError("api_budget_exhausted")
                    self._set_read_timeout(response, min(30.0, read_remaining))
                    chunk = response.read(
                        min(64 * 1024, 1024 * 1024 + 1 - len(response_body))
                    )
                    if not chunk:
                        break
                    response_body.extend(chunk)
                    if len(response_body) > 1024 * 1024:
                        raise ApiError("api_response_too_large")
        except ApiError:
            raise
        except urllib.error.HTTPError as error:
            status = error.code
            error.close()
            raise ApiError("api_http_error", status=status) from None
        except (
            urllib.error.URLError,
            http.client.HTTPException,
            TimeoutError,
            OSError,
        ) as error:
            raise ApiError("api_transport_error") from error
        finally:
            self._lock.release()
        try:
            return strict_json_loads(bytes(response_body).decode("utf-8"))
        except (UnicodeError, ValueError, json.JSONDecodeError) as error:
            raise ApiError("api_response_invalid") from error

    @staticmethod
    def _set_read_timeout(response: Any, timeout: float) -> None:
        """Keep every socket read inside the caller's remaining total budget."""

        candidates = (
            getattr(getattr(getattr(response, "fp", None), "raw", None), "_sock", None),
            getattr(getattr(response, "fp", None), "_sock", None),
        )
        for candidate in candidates:
            if candidate is not None and hasattr(candidate, "settimeout"):
                candidate.settimeout(timeout)
                return
