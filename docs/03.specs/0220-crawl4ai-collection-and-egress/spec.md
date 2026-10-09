---
title: "Crawl4AI Collection and Egress"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-09"
layer: "specs"
artifact_id: "SPEC-0220"
parent_ids:
- "REQ-0009"
- "AD-0008"
created: "2026-10-09"
---

# Crawl4AI Collection and Egress

## Overview

`infra/08-ai/crawl4ai` runs `unclecode/crawl4ai:0.9.4` on a dedicated bridge
with a token, a read-only root and Chromium limits. No advisory published for
Crawl4AI covers 0.9.4, and the image already enforces SSRF rules in-process:
a pinning forward proxy for Chromium, a non-global address block with IPv6
transition forms unwrapped, re-checked redirects, stripped caller proxy and
browser arguments, and validated webhook, robots and URL-seeder fetches. What
the repository still lacked is an enforcement point outside the container:
the bridge reached the host, the LAN and the internet directly, so a
compromised browser could ignore the in-process rules. Nothing defined which
sources may be collected, under what rights, or how a consumer runs bounded
jobs and keeps provenance. No consumer is connected today.

This package moves egress outside the container, defines the source rights
registry and the consumer admission contract, and ships a reference adapter
with a bounded job model for external workspaces, proven with local synthetic
fixtures and an isolated rehearsal of the real image.

## Scope

In scope: the Crawl4AI Compose service and networks, an egress gateway
container (DNS forwarder and forward proxy), the source rights registry schema,
the consumer admission contract, a reference collection adapter with a bounded
job model and extraction validation under `projects/crawl4ai`, unit tests, the
isolated rehearsal, the project candidate comparison and the operations
documents. Out of scope: starting `crawl4ai` on HOME, admitting a consumer,
collecting real data, load against any external service, host firewall
changes, and any application, learning database, GPU, ASR or TTS service in
`infra/`. Application collection workflows belong to their own workspaces.

## Contracts

1. Official baseline. The pin is `unclecode/crawl4ai:0.9.4` with index digest
   `sha256:9021b3cb5c6f12570bbcd5395638495e0a06969b3148e377b953d174af2ebc9b`
   (`linux/amd64` and `linux/arm64`). GHSA-6qhc-x826-342c affects `<=0.8.8`
   and was fixed in 0.8.9; the newest advisories, GHSA-5w5p-vcv6-mm3f,
   GHSA-wh5w-hmj3-vgg7 and GHSA-f77g-77vp-r96v, affect `<=0.9.3` and were fixed
   in 0.9.4. The negative regressions of those advisories (caller proxy,
   `extra_args`, link preview, robots fetch) stay in the rehearsal.
2. Egress outside the container. `crawl4ai` joins only internal networks.
   Its only route out is `crawl4ai-egress`, which answers DNS (AAAA queries get
   an empty answer so egress stays IPv4) and proxies `CONNECT` and plain HTTP.
   The proxy resolves a hostname itself and dials the address it checked, and
   it refuses every address that is not globally routable, including IPv4
   mapped, compatible, NAT64, 6to4 and Teredo forms, and every port except 80
   and 443. The in-image broker pins and checks first and chains to this proxy
   through `CRAWL4AI_UPSTREAM_PROXY`. Redirects, subresources, link previews,
   robots and seeder fetches take the same path. A direct connection from the
   crawler to any address fails because no route exists.
3. Inbound. Consumers reach the API only on the internal `crawl4ai_net` with
   `Authorization: Bearer`; `GET /health` is the only unauthenticated path.
   No host port, Traefik route or other repository network is attached.
4. Consumer admission. A consumer joins `crawl4ai_net` only through a reviewed
   change that names the consumer, its token source and its call routes. A
   source registry entry grants no network access. The crawler gets no
   management data, secret other than its token, Docker socket or shared
   volume. A consumer on `crawl4ai_net` is reachable from the crawler at the
   network layer; only the in-image broker refuses its private address, so a
   consumer must authenticate its own services.
5. Source rights. Every collected source has a registry entry with its
   provider, access mode (`api` or `web-fallback`), allowed hosts, terms and
   license reference, robots observation, rate and quota, permission to
   process, redistribute and train models, retention and the deletion owner. A
   web fallback is allowed only when the entry says why no API serves the
   need. A robots allowance is never a copyright license.
6. Bounded jobs. The adapter runs a job through `queued`, `running`,
   `succeeded`, `failed`, `cancelled` or `blocked` with an idempotency key,
   bounded retries with backoff, a deadline, and per-job limits on pages and
   bytes. A job interrupted while running returns to `queued` with its attempt
   counted. Raw results keep the source, final URL, SHA-256, `retrieved_at`,
   registry revision and license; derived results reference their raw hash,
   expire with a TTL and are deleted with it.
7. Untrusted content. Fetched HTML, documents and search text are data. They
   never authorize secret access, tool execution or policy change. Extracted
   or generated fields pass a schema check and cite spans that exist in the
   raw text, and a golden dataset guards the extraction. A vector projection
   such as Qdrant is rebuilt from raw and derived records and is never the
   source of truth; user ACLs are enforced by the consuming API.

## Acceptance Criteria

1. Unit tests show the proxy refusing private, loopback, link-local, metadata
   and transition-form addresses, other ports and DNS answers that change
   after the check, and the DNS forwarder answering AAAA with no records.
2. The isolated rehearsal of the real image shows an allowed synthetic
   endpoint fetched through the gateway, while private and metadata targets,
   a redirect to a private host, a private subresource, caller proxy and
   browser arguments, and a direct connection from the crawler are refused.
   The token and the resource limits are checked separately.
3. Adapter tests cover admission against the registry, allowed and refused
   sources, redirects off the registry, oversize, timeout, malformed output,
   cancel, retry, interruption recovery, TTL and deletion.
4. The candidate comparison names the consumer, data source, complete
   function, existing and needed infrastructure, failure recovery, rights and
   cost for each of three projects, and states that none is connected.
5. Operations documents, the service catalog and the gate contract match, and
   the changed gate passes. HOME activation, consumer admission and host
   firewall enforcement are recorded as not run.

## Related Documents

- [Plan](plan.md)
- [Task](tasks/tsk-0001-crawl4ai-collection-and-egress.md)
- [Crawl4AI policy](../../05.operations/policies/0091-crawl4ai.md)
- [AI architecture](../../02.architecture/descriptions/0008-ai-architecture.md)
- [Request baseline](../0212-request-baseline-and-reconciliation/spec.md)
- [Service integration](../0204-service-integration-security-and-operations/spec.md)
