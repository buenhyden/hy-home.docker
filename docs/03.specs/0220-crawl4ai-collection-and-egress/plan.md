---
title: "Crawl4AI Collection and Egress Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-09"
layer: "specs"
artifact_id: "SPEC-0220-PLAN-0001"
parent_ids:
- "SPEC-0220"
created: "2026-10-09"
---

# Crawl4AI Collection and Egress Plan

## Overview

Record the official baseline and the rights contract first, then move egress
out of the container, then build and test the adapter's job model, then prove
the whole path against the real image in isolation and update the operations
documents. Each unit is one commit.

The three project candidates below are compared for the first consumer. None of these is connected; each needs its own workspace, registry entries
and an admission change before any collection.

| | A. Public API documentation change watch | B. Permitted notice and statute notes | C. License-checked study material |
| --- | --- | --- | --- |
| Consumer | A developer workspace that calls public APIs | A study or compliance notebook owner | A planned study app (discovery only) |
| Data source | Published API reference pages and changelogs | Notices and statutes from official sites or their APIs | Openly licensed course text and question sets |
| Complete function | Weekly fetch, diff against the last raw hash, open a review item | Fetch on request, keep the cited span, attach to a note | Fetch an approved item once, extract, review, index |
| Existing infrastructure | Crawl4AI, egress gateway, a scheduler such as n8n or Airflow | Crawl4AI, Open Notebook, Qdrant | Crawl4AI, Qdrant, Ollama |
| Needed additions | Registry entries, diff store, notification route | Registry entries, an API client where the provider offers one | Per-item license records, review queue, learning store in the app workspace |
| Failure recovery | Retry next cycle; a raw hash gap shows the miss | Re-fetch on demand; a missing span blocks the note | Re-fetch the approved item; projections rebuild from raw |
| Rights | Reading and diffing public documentation; no redistribution | Statutes are often public domain, notices vary; cite and link | Only items whose license allows processing, retention and training |
| Cost | Few pages per week, one browser page at a time | On demand, low | Batch at onboarding, then rare; the highest storage and review cost |

Candidate A has the smallest rights and resource surface and exercises the
whole path (registry, bounded job, raw hash, review), so it is the
recommended first consumer when the owner admits one. Candidate C waits for
the study app's own planning.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 4, 5 | Official baseline, admission and rights contracts, candidates | None | TSK-0001 | Task evidence |
| W2 | 1 | Egress gateway, internal networks, digest pin, unit tests | W1 | TSK-0001 | Task evidence |
| W3 | 3 | Reference adapter: source registry, bounded jobs, provenance, extraction checks | W1 | TSK-0001 | Task evidence |
| W4 | 2 | Isolated rehearsal of the real image with synthetic fixtures | W2 | TSK-0001 | Task evidence |
| W5 | 5 | Operations documents and catalog | W2, W3, W4 | TSK-0001 | Task evidence |
| W6 | 1, 2, 3 | Independent security and correctness review and its fixes | W5 | TSK-0001 | Task evidence |
| W7 | 5 | Changed gate, staged style check, candidate quality, merge | W6 | TSK-0001 | Task evidence |

## Verification Plan

Unit tests for the gateway's address, port, DNS and pinning rules; adapter
tests against a local synthetic Crawl4AI endpoint for admission, retries,
deadlines, limits, malformed output, cancel, recovery, TTL and deletion, and a
golden extraction set; Compose static checks; an isolated rehearsal of the
real image whose networks, fixtures and targets are all local; and the
changed gate.

## Risks and Rollback

- A direct path from the crawler to a consumer on `crawl4ai_net` remains at
  the network layer; the in-image broker is the only control there, and the
  admission contract makes consumers authenticate their own services.
- DNS lookups leave through the forwarder, so DNS remains a narrow exfiltration
  channel; the proxy still refuses every connection that is not allowed.
- A host whose public address loops back to the LAN through router NAT, or
  the host's own public address, passes the global-address rule, and a client
  chooses the Host header or SNI. Only registered hosts are crawled, and no
  service here trusts a source-address allowlist; adding one needs this risk
  reviewed first.
- Rollback: revert the Compose change to the earlier bridge; the adapter and
  documents have no runtime state on HOME.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-crawl4ai-collection-and-egress.md)
