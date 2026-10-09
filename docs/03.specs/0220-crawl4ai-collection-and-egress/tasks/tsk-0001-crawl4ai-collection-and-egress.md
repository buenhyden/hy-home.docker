---
title: "Crawl4AI Collection and Egress Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-09"
layer: "specs"
artifact_id: "SPEC-0220-TSK-0001"
parent_ids:
- "SPEC-0220-PLAN-0001"
created: "2026-10-09"
---

# Crawl4AI Collection and Egress Task

## Objective

Enforce Crawl4AI egress outside its container, define the source rights
registry and consumer admission, ship a reference adapter with a bounded job
model, and prove the path with local fixtures and an isolated rehearsal of the
real image.

## Inputs and Authorization

The current user request on 2026-10-09 asks to execute prompt 07 of the
analysis pack (Crawl4AI collection, provenance, egress and reprocessing) with
per-unit commits and a per-Spec PR merge. Baseline `main` `5f4832a74`
(SPEC-0219 and its follow-up merged). SPEC-0212 routes request item 04
("Crawl4AI use") to this prompt; SPEC-0204 TSK-0001 still lists the Crawl4AI
egress-deny runtime evidence as `NOT_RUN`, which this Task supplies from an
isolated rehearsal. Starting `crawl4ai` on HOME, admitting a consumer,
collecting real data and changing host firewall rules are not part of this
request.

## Work Log

### Starting State

`infra/08-ai/crawl4ai/docker-compose.yml` pins `unclecode/crawl4ai:0.9.4` by
tag on the `crawl4ai_net` bridge, as `appuser` with a read-only root, tmpfs
state, `mem_limit` 4g, `pids_limit` 512, `shm_size` 1gb and a token read from
a secret file and checked for length. The bridge is not internal, so the
container reaches the host, the LAN and the internet directly. Open Notebook
mentions Crawl4AI only in commented settings; no consumer is connected, and no
source registry, job model or adapter exists.

### W1 Baseline and Contracts

Official facts, read on 2026-10-09 from the GitHub advisory APIs, the `v0.9.4`
tag (`133e1d92e37885dfccc03ea2e3687d06c98b7ceb`) and the registry:

- 19 repository advisories; none has an affected range that includes 0.9.4.
  GHSA-6qhc-x826-342c (CVE-2026-53755, proxy settings bypass the URL check)
  affects `<=0.8.8`, fixed in 0.8.9. GHSA-5w5p-vcv6-mm3f (untrusted config
  gate), GHSA-wh5w-hmj3-vgg7 (link preview SSRF) and GHSA-f77g-77vp-r96v
  (robots fetch SSRF) affect `<=0.9.3`, fixed in 0.9.4.
- Index `sha256:9021b3cb5c6f12570bbcd5395638495e0a06969b3148e377b953d174af2ebc9b`,
  `linux/amd64` `sha256:048848e5…`, `linux/arm64` `sha256:5370d96c…`,
  released 2026-09-23.
- In-image controls: `deploy/docker/egress_broker.py` refuses non-global
  addresses after unwrapping transition forms and pins one answer; Chromium
  goes through a local pinning proxy; untrusted bodies may not set proxies,
  `extra_args`, scripts or deep crawl strategies; webhooks re-check each
  redirect; `CRAWL4AI_UPSTREAM_PROXY` chains the pinning proxy upstream with
  `CONNECT <pinned-ip>:<port>`, so an upstream proxy sees addresses, not
  hostnames. The job API has `processing`, `completed` and `failed` states, a
  one-hour Redis TTL and no cancel endpoint.
- On this host (Docker 29.8.2) a container on an internal-only network cannot
  resolve external names; with `dns` set to a forwarder on the same internal
  network it can.

The Spec records the contracts, and the Plan compares the three project
candidates.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Baseline and contracts | 4, 5 | W1 | Advisory and tag reads; DNS probe | `5f4832a74` | PASS | W1 Baseline and Contracts | accepted |

## Review and Completion

Not complete.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
