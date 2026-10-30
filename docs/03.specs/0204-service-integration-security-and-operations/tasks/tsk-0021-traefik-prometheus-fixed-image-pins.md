---
title: "Traefik and Prometheus Fixed Image Pins Task"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-10-30"
layer: "specs"
artifact_id: "SPEC-0204-TSK-0021"
parent_ids:
- "SPEC-0204-PLAN-0001"
created: "2026-10-30"
---

# Traefik and Prometheus Fixed Image Pins Task

## Overview

### Objective

Adopt the fixed upstream Traefik v3.7.16 and Prometheus v3.15.1 images in the
Compose pins and supersede the two lapsed SEC01 risk acceptances recorded in
POL-0013 and POL-0045. Criterion 15 keeps its acceptance record in the
completed, frozen SPEC-0204-TSK-0009; this Task continues the SEC01 image
version work as a new unit, as TSK-0017 did for n8n, and rewrites no earlier
Task body.

## Inputs and Authorization

On 2026-10-30 the owner decided to adopt the fixed upstream images in place of
the two acceptances in TSK-0009 ("Traefik and Prometheus upstream candidates",
2026-10-15). Those acceptances ran until the first upstream release built with
a fixed Go and `golang.org/x/net` 0.60.0 plus 7 days, and lapsed on 2026-10-22
(Traefik) and 2026-10-28 (Prometheus). This decision authorizes the tracked
source change, ledger refresh and documentation below. It does not authorize
an image pull, a scan, a container recreation or any other runtime action.

| Service | Previous pin | Adopted pin | Release |
| --- | --- | --- | --- |
| Traefik | `traefik:v3.7.14@sha256:575fa15b…` | `traefik:v3.7.16@sha256:1336e85aaed293bd63d005086e0dd013b04078b26aaeb1c18b26a2f928af7e65` | 2026-10-20T15:19:30Z, go1.26.10, x/net v0.60.0 |
| Prometheus | `prom/prometheus:v3.15.0@sha256:efd719c9…` | `prom/prometheus:v3.15.1@sha256:fa3302279710be2f21a8301ec17a8b4f2301fd829bd113839b3b6b02b6f191a2` | 2026-10-21T16:15:57Z, go1.27.3, x/net v0.60.0 |

The Go and x/net versions are the owner's release facts and the upstream
release notes; the images were not pulled or inspected here.

## Work Log

### Source pins — 2026-10-30

The anonymous Docker Hub registry API returned the index digests above. Each
raw index body hashes to the `Docker-Content-Digest` header, and the
linux/amd64 manifests (Traefik `abb2b9c1…`, Prometheus `d445d180…`) match their
headers too; config digests `3733df53…` and `876ae6bc…` are descriptors only.
The anonymous GitHub API reports both tags as the latest non-draft,
non-prerelease release, so no newer stable exists.

Changed pins: `infra/01-gateway/traefik/docker-compose.yml`,
`infra/06-observability/docker-compose.yml`, and through
`sync-tech-stack-versions.sh --write` both entries in
`infra/tech-stack.versions.json`. Prometheus copies that mean the current pin
now follow it: `scripts/operations/prometheus-isolated-restore.py`,
`examples/operations/quality-metrics/acceptance.py` and
`tests/validation/test_datastore_observation_rehearsal.py`. The tag sample in
`ImageTagPolicyTests` (`tests/validation/test_compose_baseline_gates.py`) is a
version-shape example and moves to `v3.15.1` with them.

Left unchanged on purpose: `infra/01-gateway/traefik/compose.window-ca.override.yml`
(v3.7.13) is the SPEC-0243 rollback overlay for the image Traefik ran on
2026-10-14. Its header says it is used only as a second `-f` to roll back, so
it records a historical image and does not track the main pin. The
`traefik:v3.7.13` stage guard in `examples/operations/quality-metrics/acceptance.py`
is a quality-metrics fixture and also keeps its tag.

Because the restore script and rehearsal test now name v3.15.1, those
rehearsals need the new image cached; the owner pull below provides it.
SPEC-0245 (in progress) preserves Prometheus on v3.15.0 and excludes a version
change, so the owner should order its recreate and the one below explicitly.

### Ledger and policy

The four ledger files in `infra/09-platform-ops/security-updates/` carry the
new pins, digests, GitHub and registry lookups, new input SHA-256 values and a
`source_refreshes` entry. The two rows keep the old receipts under
`previous_adopted_pin_assessment`; `sbom_scan`, `applicability` and
`compatibility` for the adopted pins read `NOT_RUN`. The restic Compose hash
was stale from an earlier non-image edit and is re-bound in the same refresh.
POL-0013 and POL-0045 keep their 2026-10-15 acceptance paragraphs and add a
dated "Superseded" paragraph. TSK-0009 is untouched.

### Owner steps — NOT_RUN

Every step below needs a separate owner approval for its named target. None
ran here, so no scan, applicability, boot, recreation or rollback result exists
for the adopted images.

1. Pull and offline scan, with an independent applicability review. The
   approval line for one Grype DB update is on file in
   `infra/supply-chain.network-approvals.md` for 2026-10-15; this pull and any
   new DB seed need a fresh approval.

   ```bash
   docker pull traefik:v3.7.16@sha256:1336e85aaed293bd63d005086e0dd013b04078b26aaeb1c18b26a2f928af7e65
   docker pull prom/prometheus:v3.15.1@sha256:fa3302279710be2f21a8301ec17a8b4f2301fd829bd113839b3b6b02b6f191a2
   # In a new mode-0700 directory $SCAN: save each archive, then run both tools offline.
   docker save traefik:v3.7.16@sha256:1336e85aaed293bd63d005086e0dd013b04078b26aaeb1c18b26a2f928af7e65 -o "$SCAN/traefik.tar"
   docker save prom/prometheus:v3.15.1@sha256:fa3302279710be2f21a8301ec17a8b4f2301fd829bd113839b3b6b02b6f191a2 -o "$SCAN/prometheus.tar"
   docker run --pull=never --rm --network none -v "$SCAN:/scan" \
     anchore/syft@sha256:3eb5379ba7b409c3f4069b686110527af0c47df993fa5c10d13e7cf34f49b1aa \
     docker-archive:/scan/traefik.tar -o syft-json=/scan/traefik.sbom.json
   docker run --pull=never --rm --network none -v "$SCAN:/scan" -v "$GRYPE_DB:/db:ro" \
     -e GRYPE_DB_CACHE_DIR=/db -e GRYPE_DB_AUTO_UPDATE=false \
     anchore/grype@sha256:e4a44ef45d285b829ce6efe2642980329661bd2d18eab5fc539138d4adaebbbe \
     sbom:/scan/traefik.sbom.json -o json > "$SCAN/traefik.grype.json"
   ```

   Repeat the Syft and Grype runs for `prometheus.tar`. `$GRYPE_DB` is the
   path printed by `python3 scripts/lib/supply_chain/grype_db_seed.py --resolve-current . _workspace/repo-support/task-2026-07-23-security-supply-chain-runtime-closure/grype-db-seed`
   (reseed first with `bash scripts/security/seed-grype-db-cache.sh --seed`
   only under the fresh approval). A `security-auditor` then reviews each match
   against the primary sources, as the 2026-10-15 review did. Record archive,
   SBOM and Grype SHA-256 values, counts and the reviewed applicability here.

2. Config checks on the pulled images, `--network none`, nothing mounted
   except read-only repository config. Traefik static and dynamic config must
   boot with the same expected errors as v3.7.14 (no Docker socket, no
   certificate mount); Prometheus runs both checks on both config files and
   the 13 rule files:

   ```bash
   docker run --pull=never --rm --network none -v "$PWD/infra/01-gateway/traefik/config:/etc/traefik:ro" \
     traefik:v3.7.16@sha256:1336e85aaed293bd63d005086e0dd013b04078b26aaeb1c18b26a2f928af7e65 --configFile=/etc/traefik/traefik.yml
   docker run --pull=never --rm --network none --entrypoint promtool -v "$PWD/infra/06-observability/prometheus:/etc/prometheus:ro" \
     prom/prometheus:v3.15.1@sha256:fa3302279710be2f21a8301ec17a8b4f2301fd829bd113839b3b6b02b6f191a2 \
     check config --syntax-only /etc/prometheus/prometheus.yml
   docker run --pull=never --rm --network none --entrypoint /bin/sh -v "$PWD/infra/06-observability/prometheus:/etc/prometheus:ro" \
     prom/prometheus:v3.15.1@sha256:fa3302279710be2f21a8301ec17a8b4f2301fd829bd113839b3b6b02b6f191a2 \
     -c 'promtool check rules /etc/prometheus/alert_rules/*.yml'
   ```

   Repeat `check config --syntax-only` for `prometheus.dev.yml`. Adjust the
   mount sources to the actual config paths first; a path error is a failure
   of the check, not a pass.

3. HOME recreation with rollback, run by the owner from the HOME checkout
   after the scan and checks pass. Record the running image identity first
   (`docker inspect --format '{{.Image}} {{.Config.Image}}' traefik prometheus`);
   the expected rollback targets are the previous pins above. Follow RUN-0013
   (Startup, shutdown and apply) and RUN-0045.

   ```bash
   # Traefik: back up nothing stateful (no ACME storage). Apply, then verify.
   docker compose --profile core up -d --no-deps --no-build --pull never --force-recreate traefik
   docker compose ps traefik
   docker compose exec -T traefik traefik healthcheck --ping
   # Prometheus: first a consistent TSDB backup and isolated restore (SPEC-0245
   # procedure). Then apply and verify.
   docker compose --profile obs up -d --no-deps --no-build --pull never --force-recreate prometheus
   docker exec prometheus wget -qO- http://localhost:9090/-/healthy
   docker exec prometheus promtool check config /etc/prometheus/prometheus.yml
   docker exec prometheus /bin/sh -c 'promtool check rules /etc/prometheus/alert_rules/*.yml'
   ```

   Verify Traefik by healthy state, dashboard BasicAuth success and denial,
   one ForwardAuth and one native-OIDC route, and internal metrics scrape;
   verify Prometheus by `up` for every job, rule loading and a TSDB head
   time that did not move backwards. Rollback restores the previous image
   with the Compose edit reverted in a scratch copy or with
   `docker compose ... up -d --no-deps --no-build --pull never --force-recreate`
   against the previous digest (Traefik may use the SPEC-0243
   `compose.window-ca.override.yml` overlay only for the older v3.7.13). A
   tag change does not reverse a TSDB or schema change, so a failed Prometheus
   start after a data-affecting step goes to the SPEC-0245 restore.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0204-TSK-0021 | draft | ready | #inputs-and-authorization |
| SPEC-0204-TSK-0021 | ready | in-progress | #source-pins-2026-10-30 |

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Registry index and platform digests | 15 | W76 | Anonymous registry API digest equality | Traefik v3.7.16 and Prometheus v3.15.1; raw body SHA-256 equals Docker-Content-Digest | PASS | Work Log | required | - |
| Latest stable release | 15 | W76 | GitHub latest-release API for both repositories | Non-draft, non-prerelease v3.7.16 and v3.15.1 | PASS | Work Log | required | - |
| Image pull and offline scan | 15 | W76 | Syft and Grype on `--network none`, independent applicability review | Adopted digests; owner approval absent | NOT_RUN | Owner steps | optional | - |
| Config boot and promtool checks | 15 | W76 | Traefik config boot, `check config`, `check rules` | Adopted images; no pull | NOT_RUN | Owner steps | optional | - |
| HOME recreation and rollback | 15 | W76 | Recreate, health, route and scrape checks, rollback | Named HOME target and backup absent | NOT_RUN | Owner steps | optional | - |

## Criterion Acceptance

Criterion 15 keeps its durable decision in the completed TSK-0009. This Task
creates no duplicate decision. A pinned source is not a deployed update, and
the latest and security gates still exit 2 for other open evidence.

## Review and Completion

In progress. Source pins, ledger and policy text are done; the owner steps
above remain `NOT_RUN`. Close this Task only after the scan, applicability
review, config checks and HOME recreation (or an owner decision to defer them)
are recorded. Source rollback is a logical revert of this unit; it does not
revert a recreated container or its data.

## Related Documents

- [Plan](../plan.md)
- [SEC01 Task (completed)](tsk-0009-sec01-stable-security-integration.md)
- [POL-0013 Traefik policy](../../../05.operations/policies/02-gateway-and-networking/0013-traefik.md)
- [POL-0045 Prometheus policy](../../../05.operations/policies/07-observability/0045-prometheus.md)
- [RUN-0013 Traefik runbook](../../../05.operations/runbooks/02-gateway-and-networking/0013-traefik.md)
- [RUN-0045 Prometheus runbook](../../../05.operations/runbooks/07-observability/0045-prometheus.md)
