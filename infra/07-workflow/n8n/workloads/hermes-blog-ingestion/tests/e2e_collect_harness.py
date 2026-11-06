"""Drive the collector and direct plugin against an owned synthetic ingress.

The transport adapter here intentionally disables TLS verification for the
disposable Traefik certificate. It never tests the production TLS transport.
The fetched article, credentials and Gateway state are synthetic.
"""

from __future__ import annotations

import hashlib
import http.client
import ipaddress
import json
import shutil
import ssl
import sys
from contextlib import ExitStack
from datetime import UTC, datetime, timedelta
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

WORKLOAD = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKLOAD))
sys.path.insert(0, str(WORKLOAD / "hermes-plugin"))

import tools  # noqa: E402
from publisher import source_collection, source_fetch  # noqa: E402

QUOTES = {
    "a": "The synthetic deployment completed without any incident today.",
    "b": "Release notes confirm the synthetic rollout shipped everywhere.",
}
ITEMS = [
    {
        "item_id": f"devops-{key}",
        "kind": "devops",
        "title": f"Synthetic item {key}",
        "body": f"Synthetic body of item {key} for the Resource Export E2E.",
        "source_url": f"https://example.org/{key}",
        "source_quotes": [QUOTES[key]],
    }
    for key in "ab"
]
ARTICLES = {
    item["source_url"]: (
        item["title"] + "\n" + item["body"] + "\n" + item["source_quotes"][0]
    ).encode("utf-8")
    for item in ITEMS
}


REPORT = (
    "# Synthetic DevOps report\n\n"
    + "\n".join(f"- {item['title']}: {item['body']}" for item in ITEMS)
    + "\n"
)


def main(config_file: str) -> int:
    config = json.loads(Path(config_file).read_text(encoding="utf-8"))
    address = ipaddress.ip_address(config["address"])
    subnet = ipaddress.ip_network(config["subnet"], strict=True)
    if not address.is_private or address not in subnet or config["port"] != 443:
        raise ValueError("invalid isolated endpoint")
    work = Path(config["work"])
    token = config["token"]
    scheduled = datetime.now(UTC) - timedelta(seconds=30)
    run = SimpleNamespace(
        job_id="25674fbc0bf3",
        execution_id="p11-synthetic-collection",
        scheduled_instant=scheduled.isoformat(timespec="milliseconds"),
    )
    ctx = SimpleNamespace(current_cron_execution=lambda: run)
    calls = []

    def fetch(url):
        if url not in ARTICLES:
            raise ValueError("unexpected source")
        article = ARTICLES[url]
        return source_fetch.FetchResult(
            final_url=url,
            status=200,
            sha256=hashlib.sha256(article).hexdigest(),
            fetched_at=datetime.now(UTC).isoformat(timespec="milliseconds"),
            content_type="text/plain; charset=utf-8",
            body=article,
        )

    def post(url, payload, credential, policy, *, timeout):
        if url != tools.webhook_transport.APPROVED_WEBHOOK_URL or credential != token:
            raise ValueError("unexpected synthetic transport")
        calls.append(True)
        connection = http.client.HTTPSConnection(
            str(address),
            config["port"],
            timeout=timeout,
            context=ssl._create_unverified_context(),  # synthetic certificate only
        )
        try:
            connection.request(
                "POST",
                "/webhook/hermes-blog-ingestion",
                body=payload,
                headers={
                    "Host": "n8n.hy.home.arpa",
                    "X-Hermes-Ingest-Token": token,
                    "Content-Type": "application/json",
                },
            )
            response = connection.getresponse()
            body = response.read(tools.webhook_transport.MAX_RESPONSE_BYTES + 1)
            if len(body) > tools.webhook_transport.MAX_RESPONSE_BYTES:
                raise ValueError("response too large")
            return tools.webhook_transport.Response(
                response.status, body, response.getheader("Content-Type", "")
            )
        finally:
            connection.close()

    with ExitStack() as stack:
        stack.enter_context(patch.object(tools, "_CTX", ctx))
        stack.enter_context(patch.object(tools, "SOURCE_DIR", work / "plugin-sources"))
        stack.enter_context(patch.object(tools, "OUTBOX_DIR", work / "plugin-outbox"))
        stack.enter_context(patch.object(tools, "REPORT_DIR", work / "plugin-reports"))
        stack.enter_context(
            patch.object(source_collection.source_fetch, "fetch", fetch)
        )
        stack.enter_context(
            patch.object(tools, "_load_url", return_value=tools.APPROVED_WEBHOOK_URL)
        )
        stack.enter_context(
            patch.object(tools, "_load_address_policy", return_value=str(subnet))
        )
        stack.enter_context(patch.object(tools, "_load_secret", return_value=token))
        stack.enter_context(patch.object(tools.webhook_transport, "post", post))
        receipts = []
        for item in ITEMS:
            args = {"item_id": item["item_id"], "source_url": item["source_url"]}
            collected = json.loads(tools.handle_collect_source(args))
            if not collected.get("ok"):
                raise ValueError("synthetic collection rejected")
            repeated = json.loads(tools.handle_collect_source(args))
            if repeated.get("receipt_id") != collected["receipt_id"]:
                raise ValueError("collection receipt changed on replay")
            receipts.append(collected["receipt_id"])
        submission = {
            "payload": {"schema_version": "1.0", "items": ITEMS},
            "source_receipts": receipts,
            "report_markdown": REPORT,
        }
        result = json.loads(tools.handle_submit_report(submission))
        if not result.get("ok") or result.get("status") != "persisted":
            raise ValueError(
                "synthetic submission rejected: " + str(result.get("error"))
            )
        duplicate = json.loads(tools.handle_submit_report(submission))
        if (
            not duplicate.get("ok")
            or duplicate.get("status") != "already_persisted"
            or len(calls) != 1
        ):
            raise ValueError("direct submission was sent more than once")
        report_id = result["response"]["id"]
        shutil.copytree(work / "plugin-sources", work / "restored-plugin-sources")
        shutil.copytree(work / "plugin-outbox", work / "restored-plugin-outbox")
        with (
            patch.object(tools, "SOURCE_DIR", work / "restored-plugin-sources"),
            patch.object(tools, "OUTBOX_DIR", work / "restored-plugin-outbox"),
        ):
            restored = json.loads(tools.handle_submit_report(submission))
        if (
            not restored.get("ok")
            or restored.get("status") != "already_persisted"
            or restored.get("receipt", {}).get("id") != report_id
            or len(calls) != 1
        ):
            raise ValueError(
                "restored source and outbox changed the persisted identity"
            )
        output = {
            "report_id": report_id,
            "item_ids": [item["item_id"] for item in ITEMS],
            "http_posts": len(calls),
            "source_outbox_restored": True,
        }
        (work / "plugin-result.json").write_text(json.dumps(output), encoding="utf-8")
        print(json.dumps(output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1]))
