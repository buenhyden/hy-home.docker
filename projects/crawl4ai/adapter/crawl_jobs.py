"""Reference Crawl4AI collection adapter for external workspaces (SPEC-0220).

A consuming workspace pins this file. It admits a URL only through the
workspace's source registry, runs each crawl as a bounded job in SQLite, keeps
provenance for raw results and deletes derived results with their raw record.
Fetched content is data: nothing here interprets it as an instruction.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from urllib.parse import urlsplit

STATES = ("queued", "running", "succeeded", "failed", "cancelled", "blocked")
RIGHTS = ("may_process", "may_redistribute", "may_train")
REQUIRED = ("id", "provider", "access", "hosts", "terms_url", "license", "robots",
            "rate_per_minute", "daily_quota", *RIGHTS, "retention_days",
            "deletion_owner", "consumer")  # fmt: skip
MAX_BYTES = 5 * 1024 * 1024
REQUEST_CAP_SECONDS = 60
LEASE_SECONDS = 300
BACKOFF_SECONDS = 30
BACKOFF_CAP_SECONDS = 900


class Blocked(Exception):
    """The registry does not allow this URL; the job is recorded as blocked."""


class Retryable(Exception):
    """A transient failure: timeout, 429 or 5xx."""


class Malformed(Exception):
    """The crawler answered with something this adapter cannot trust."""


def validate_registry(data: dict) -> list[str]:
    """Problems that make a registry unusable; empty means valid."""
    problems = []
    if not isinstance(data.get("revision"), str) or not data["revision"]:
        problems.append("registry: revision is required")
    seen = set()
    for entry in data.get("sources", []):
        name = entry.get("id", "?")
        problems += [
            f"{name}: {key} is required" for key in REQUIRED if key not in entry
        ]
        if name in seen:
            problems.append(f"{name}: duplicate id")
        seen.add(name)
        if entry.get("access") not in ("api", "web-fallback"):
            problems.append(f"{name}: access must be api or web-fallback")
        if entry.get("access") == "web-fallback" and not entry.get("fallback_reason"):
            problems.append(f"{name}: web-fallback needs fallback_reason")
        if any(not isinstance(entry.get(key), bool) for key in RIGHTS if key in entry):
            problems.append(f"{name}: rights must be true or false")
        robots = entry.get("robots", {})
        if not isinstance(robots, dict) or not {"url", "checked_at", "allows"} <= set(
            robots
        ):
            problems.append(f"{name}: robots needs url, checked_at and allows")
        hosts = entry.get("hosts", [])
        if not hosts or any("*" in host or "/" in host for host in hosts):
            problems.append(f"{name}: hosts must be exact host names")
    return problems


class Registry:
    def __init__(self, data: dict):
        problems = validate_registry(data)
        if problems:
            raise ValueError("; ".join(problems))
        self.revision = data["revision"]
        self.sources = {entry["id"]: entry for entry in data["sources"]}

    def admit(self, url: str, source_id: str) -> dict:
        """The registry entry that allows this URL, or Blocked."""
        entry = self.sources.get(source_id)
        parts = urlsplit(url)
        if entry is None:
            raise Blocked("unknown source")
        if (
            parts.scheme not in ("http", "https")
            or parts.hostname not in entry["hosts"]
        ):
            raise Blocked("host not registered for the source")
        if parts.port not in (None, 80, 443):
            raise Blocked("port not allowed")
        if not entry["may_process"]:
            raise Blocked("source does not allow processing")
        # A robots allowance is a crawl courtesy, never a license.
        if not entry["robots"]["allows"]:
            raise Blocked("robots disallows")
        return entry


@dataclass
class Fetched:
    final_url: str
    content: str


class Crawl4AI:
    """POST /crawl with a bearer token; bounded in time and bytes."""

    def __init__(self, base_url: str, token: str, max_bytes: int = MAX_BYTES):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.max_bytes = max_bytes

    def fetch(self, url: str, timeout: float) -> Fetched:
        body = json.dumps({
            "urls": [url],
            "crawler_config": {"type": "CrawlerRunConfig",
                               "params": {"cache_mode": "bypass",
                                          "page_timeout": int(timeout * 1000)}},
        }).encode()  # fmt: skip
        request = urllib.request.Request(
            f"{self.base_url}/crawl", data=body, method="POST",
            headers={"Authorization": f"Bearer {self.token}",
                     "Content-Type": "application/json"},
        )  # fmt: skip
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                payload = response.read(self.max_bytes + 1)
        except urllib.error.HTTPError as exc:
            if exc.code == 429 or exc.code >= 500:
                raise Retryable(f"http {exc.code}") from exc
            raise Malformed(f"http {exc.code}") from exc
        except (TimeoutError, urllib.error.URLError, ConnectionError) as exc:
            raise Retryable("unreachable or timed out") from exc
        if len(payload) > self.max_bytes:
            raise Malformed("response over the byte limit")
        return parse_result(payload, url)


def parse_result(payload: bytes, url: str) -> Fetched:
    try:
        document = json.loads(payload)
        result = document["results"][0]
    except (ValueError, KeyError, IndexError, TypeError) as exc:
        raise Malformed("not a Crawl4AI result") from exc
    if not isinstance(result, dict) or result.get("url") != url:
        raise Malformed("result does not match the request")
    if not result.get("success"):
        raise Retryable("crawl failed")
    markdown = result.get("markdown")
    if isinstance(markdown, dict):
        markdown = markdown.get("raw_markdown")
    content = markdown if isinstance(markdown, str) else result.get("cleaned_html")
    final = result.get("redirected_url") or url
    if not isinstance(content, str) or not isinstance(final, str):
        raise Malformed("result has no text")
    return Fetched(final, content)


SCHEMA = """
CREATE TABLE IF NOT EXISTS jobs (
  id INTEGER PRIMARY KEY, idempotency_key TEXT UNIQUE NOT NULL,
  source_id TEXT NOT NULL, url TEXT NOT NULL, state TEXT NOT NULL,
  attempts INTEGER NOT NULL DEFAULT 0, max_attempts INTEGER NOT NULL,
  next_attempt_at REAL NOT NULL, deadline_at REAL NOT NULL,
  lease_until REAL, reason TEXT, raw_sha256 TEXT, updated_at REAL NOT NULL);
CREATE TABLE IF NOT EXISTS raws (
  sha256 TEXT PRIMARY KEY, source_id TEXT NOT NULL, url TEXT NOT NULL,
  final_url TEXT NOT NULL, retrieved_at REAL NOT NULL,
  registry_revision TEXT NOT NULL, license TEXT NOT NULL,
  content TEXT NOT NULL, expires_at REAL NOT NULL);
CREATE TABLE IF NOT EXISTS derived (
  id INTEGER PRIMARY KEY,
  raw_sha256 TEXT NOT NULL REFERENCES raws(sha256) ON DELETE CASCADE,
  kind TEXT NOT NULL, data TEXT NOT NULL, expires_at REAL NOT NULL);
"""


class Jobs:
    def __init__(self, path: str, registry: Registry, clock=time.time):
        self.db = sqlite3.connect(path, isolation_level=None)
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA foreign_keys = ON")
        self.db.executescript(SCHEMA)
        self.registry = registry
        self.clock = clock

    def job(self, job_id: int) -> sqlite3.Row:
        return self.db.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()

    def enqueue(self, url: str, source_id: str, key: str,
                deadline_seconds: float = 3600, max_attempts: int = 3) -> int:  # fmt: skip
        """One job per idempotency key; a blocked URL is recorded, not run."""
        existing = self.db.execute(
            "SELECT id, url, source_id FROM jobs WHERE idempotency_key = ?", (key,)
        ).fetchone()
        if existing:
            if (existing["url"], existing["source_id"]) != (url, source_id):
                raise ValueError("idempotency key reused for a different request")
            return existing["id"]
        now = self.clock()
        state, reason = "queued", None
        try:
            self.registry.admit(url, source_id)
        except Blocked as exc:
            state, reason = "blocked", str(exc)
        return self.db.execute(
            "INSERT INTO jobs (idempotency_key, source_id, url, state, max_attempts,"
            " next_attempt_at, deadline_at, reason, updated_at) VALUES (?,?,?,?,?,?,?,?,?)",
            (key, source_id, url, state, max_attempts, now, now + deadline_seconds,
             reason, now),
        ).lastrowid  # fmt: skip

    def cancel(self, job_id: int) -> None:
        self._set(
            job_id, "cancelled", "cancelled by caller", only=("queued", "running")
        )

    def recover(self) -> int:
        """Return jobs whose worker died to the queue; the attempt stays counted."""
        now = self.clock()
        return self.db.execute(
            "UPDATE jobs SET state='queued', lease_until=NULL, updated_at=? "
            "WHERE state='running' AND lease_until < ?", (now, now),
        ).rowcount  # fmt: skip

    def purge(self) -> None:
        """Expire raw records (derived ones go with them) and derived ones."""
        now = self.clock()
        self.db.execute("DELETE FROM derived WHERE expires_at <= ?", (now,))
        self.db.execute("DELETE FROM raws WHERE expires_at <= ?", (now,))

    def delete_source(self, source_id: str) -> None:
        self.db.execute("DELETE FROM raws WHERE source_id = ?", (source_id,))

    def add_derived(
        self, raw_sha256: str, kind: str, data: dict, ttl_seconds: float
    ) -> None:
        self.db.execute(
            "INSERT INTO derived (raw_sha256, kind, data, expires_at) VALUES (?,?,?,?)",
            (raw_sha256, kind, json.dumps(data), self.clock() + ttl_seconds),
        )

    def run_once(self, client: Crawl4AI) -> int | None:
        """Claim and run one due job; the id, or None when nothing is due."""
        now = self.clock()
        row = self.db.execute(
            "SELECT * FROM jobs WHERE state='queued' AND next_attempt_at <= ? "
            "ORDER BY next_attempt_at, id LIMIT 1", (now,),
        ).fetchone()  # fmt: skip
        if row is None:
            return None
        if now >= row["deadline_at"]:
            self._set(row["id"], "failed", "deadline passed")
            return row["id"]
        entry = self.registry.sources[row["source_id"]]
        if self._over_budget(entry, now):
            self.db.execute("UPDATE jobs SET next_attempt_at=? WHERE id=?",
                            (now + 60, row["id"]))  # fmt: skip
            return row["id"]
        self.db.execute(
            "UPDATE jobs SET state='running', attempts=attempts+1, lease_until=?,"
            " updated_at=? WHERE id=? AND state='queued'",
            (now + LEASE_SECONDS, now, row["id"]),
        )
        timeout = min(REQUEST_CAP_SECONDS, row["deadline_at"] - now)
        try:
            fetched = client.fetch(row["url"], timeout)
            self.registry.admit(fetched.final_url, row["source_id"])
        except Blocked as exc:
            self._set(row["id"], "blocked", f"redirect: {exc}", only=("running",))
        except Retryable as exc:
            self._retry(row["id"], str(exc))
        except Malformed as exc:
            self._set(row["id"], "failed", str(exc), only=("running",))
        else:
            # A job cancelled while it ran keeps nothing.
            if self.job(row["id"])["state"] == "running":
                self._store(row, entry, fetched)
        return row["id"]

    def _over_budget(self, entry: dict, now: float) -> bool:
        def count(window: float) -> int:
            return self.db.execute(
                "SELECT COUNT(*) FROM jobs WHERE source_id=? AND attempts>0 AND updated_at>?",
                (entry["id"], now - window),
            ).fetchone()[0]  # fmt: skip

        return (
            count(60) >= entry["rate_per_minute"]
            or count(86400) >= entry["daily_quota"]
        )

    def _retry(self, job_id: int, reason: str) -> None:
        row = self.job(job_id)
        now = self.clock()
        delay = min(BACKOFF_CAP_SECONDS, BACKOFF_SECONDS * 2 ** (row["attempts"] - 1))
        if row["attempts"] >= row["max_attempts"] or now + delay >= row["deadline_at"]:
            self._set(
                job_id, "failed", f"{reason}; retries exhausted", only=("running",)
            )
            return
        self.db.execute(
            "UPDATE jobs SET state='queued', lease_until=NULL, next_attempt_at=?,"
            " reason=?, updated_at=? WHERE id=? AND state='running'",
            (now + delay, reason, now, job_id),
        )

    def _store(self, row: sqlite3.Row, entry: dict, fetched: Fetched) -> None:
        now = self.clock()
        digest = hashlib.sha256(fetched.content.encode()).hexdigest()
        self.db.execute(
            "INSERT OR IGNORE INTO raws (sha256, source_id, url, final_url, retrieved_at,"
            " registry_revision, license, content, expires_at) VALUES (?,?,?,?,?,?,?,?,?)",
            (digest, row["source_id"], row["url"], fetched.final_url, now,
             self.registry.revision, entry["license"], fetched.content,
             now + entry["retention_days"] * 86400),
        )  # fmt: skip
        self.db.execute("UPDATE jobs SET raw_sha256=? WHERE id=?", (digest, row["id"]))
        self._set(row["id"], "succeeded", None, only=("running",))

    def _set(self, job_id, state, reason, only=None) -> None:
        guard = f" AND state IN ({','.join('?' * len(only))})" if only else ""
        self.db.execute(
            f"UPDATE jobs SET state=?, reason=?, lease_until=NULL, updated_at=? WHERE id=?{guard}",
            (state, reason, self.clock(), job_id, *(only or ())),
        )


def check_extraction(raw: str, extraction: dict, fields: dict[str, type]) -> list[str]:
    """Schema and citation problems; every field must quote the raw text."""
    problems = [f"unexpected field {name}" for name in extraction if name not in fields]
    for name, kind in fields.items():
        item = extraction.get(name)
        if not isinstance(item, dict) or set(item) != {"value", "quote"}:
            problems.append(f"{name}: needs value and quote")
            continue
        if not isinstance(item["value"], kind):
            problems.append(f"{name}: value is not {kind.__name__}")
        if (
            not isinstance(item["quote"], str)
            or not item["quote"]
            or item["quote"] not in raw
        ):
            problems.append(f"{name}: quote is not in the raw text")
    return problems


def evaluate(golden: list[dict], extract, fields: dict[str, type]) -> float:
    """Share of golden cases whose extraction is valid and equals the expected values."""
    passed = 0
    for case in golden:
        result = extract(case["raw"])
        values = {
            name: item.get("value")
            for name, item in result.items()
            if isinstance(item, dict)
        }
        if (
            not check_extraction(case["raw"], result, fields)
            and values == case["expected"]
        ):
            passed += 1
    return passed / len(golden) if golden else 0.0
