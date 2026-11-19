---
title: "Traefik and Prometheus Fixed Image Pins Task"
version: "0.3.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-11-19"
layer: "specs"
artifact_id: "SPEC-0204-TSK-0021"
parent_ids:
- "SPEC-0204-PLAN-0001"
created: "2026-10-30"
---

# Traefik and Prometheus Fixed Image Pins Task

## Scope

### Objective and Parent

#### Objective

Adopt the fixed upstream Traefik v3.7.16 and Prometheus v3.15.1 images in the
Compose pins and supersede the two lapsed SEC01 risk acceptances recorded in
POL-0013 and POL-0045. Criterion 15 keeps its acceptance record in the
completed, frozen SPEC-0204-TSK-0009; this Task continues the SEC01 image
version work as a new unit, as TSK-0017 did for n8n, and rewrites no earlier
Task body.

- [Plan](../plan.md)
- [SEC01 Task (completed)](tsk-0009-sec01-stable-security-integration.md)
- [POL-0013 Traefik policy](../../../05.operations/policies/02-gateway-and-networking/0013-traefik.md)
- [POL-0045 Prometheus policy](../../../05.operations/policies/07-observability/0045-prometheus.md)
- [RUN-0013 Traefik runbook](../../../05.operations/runbooks/02-gateway-and-networking/0013-traefik.md)
- [RUN-0045 Prometheus runbook](../../../05.operations/runbooks/07-observability/0045-prometheus.md)

### Inputs and Authority

#### Inputs and Authorization

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

## Execution Log

### Work Performed

#### Source pins — 2026-10-30

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

#### Ledger and policy

The four ledger files in `infra/09-platform-ops/security-updates/` carry the
new pins, digests, GitHub and registry lookups, new input SHA-256 values and a
`source_refreshes` entry. The two rows keep the old receipts under
`previous_adopted_pin_assessment`; `sbom_scan`, `applicability` and
`compatibility` for the adopted pins read `NOT_RUN`. The restic Compose hash
was stale from an earlier non-image edit and is re-bound in the same refresh.
POL-0013 and POL-0045 keep their 2026-10-15 acceptance paragraphs and add a
dated "Superseded" paragraph. TSK-0009 is untouched.

#### Owner steps — NOT_RUN

The owner pull, scan, config-boot and recreation steps for `traefik:v3.7.16`
and `prom/prometheus:v3.15.1` never ran here. The Traefik pin was superseded by
v3.7.17 (see the supersession note), so its steps no longer apply. On
2026-11-19 HOME runs `prom/prometheus:v3.15.1` and `traefik:v3.7.17`, both
healthy (HOME running images row); that observation is not a scan,
applicability review or rollback result.

#### Owner decisions 2026-11-19

In this chat the owner deferred the image pull and offline scan, the
config boot and promtool checks, and the recreation and rollback steps,
because HOME already runs `prom/prometheus:v3.15.1` and Traefik's later
`v3.7.17` healthy (HOME running images). Those three optional rows stay
`NOT_RUN`; the deferral is not a scan or applicability result. The required
source rows pass, so this Task closes.

#### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0204-TSK-0021 | draft | ready | #inputs-and-authorization |
| SPEC-0204-TSK-0021 | ready | in-progress | #source-pins-2026-10-30 |
| SPEC-0204-TSK-0021 | in-progress | completed | #owner-decisions-2026-11-19 |

#### Supersession note 2026-11-10

On 2026-11-10 the Traefik v3.7.16 pin is superseded by v3.7.17 (PR #881,
merge `125a884d1`; `infra/01-gateway/traefik/docker-compose.yml:13`). The
Prometheus pin is unchanged. Earlier entries are unchanged.

### Blockers and Decisions

- On 2026-11-15 the owner directed that content conflicting with the v14.7 W00 to W05 requirements be discarded; removed from spec.md and plan.md: retired-package owners, archive preservation, restated Task results, acceptance and status, local-main delivery and non-Registry results (`BLOCKED`, `DEFER`).
- On 2026-11-19 the owner directed that Stage 03 passages conflicting with the current implementation be deleted. The owner-step commands that pull `traefik:v3.7.16` were removed, because v3.7.17 superseded that pin and HOME runs it.

## Verification Evidence

### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Registry index and platform digests | 15 | W76 | Anonymous registry API digest equality | Traefik v3.7.16 and Prometheus v3.15.1; raw body SHA-256 equals Docker-Content-Digest | PASS | Work Log | required | - |
| Latest stable release | 15 | W76 | GitHub latest-release API for both repositories | Non-draft, non-prerelease v3.7.16 and v3.15.1 | PASS | Work Log | required | - |
| Image pull and offline scan | 15 | W76 | Syft and Grype on `--network none`, independent applicability review | Adopted digests; owner approval absent | NOT_RUN | Owner steps | optional | - |
| Config boot and promtool checks | 15 | W76 | Traefik config boot, `check config`, `check rules` | Adopted images; no pull | NOT_RUN | Owner steps | optional | - |
| HOME recreation and rollback | 15 | W76 | Recreate, health, route and scrape checks, rollback | Named HOME target and backup absent | NOT_RUN | Owner steps | optional | - |
| HOME running images | 15 | W76 | `docker ps` image and health for `prometheus` and `traefik` | HOME on 2026-11-19, `main` at `f4dc70905` | PASS | Owner steps | optional | - |

### Resolution Links

None: nothing was recorded here before this Task moved to the common form.

## Acceptance Decision

### Criterion Decisions

Criterion 15 keeps its durable decision in the completed TSK-0009. This Task
creates no duplicate decision. A pinned source is not a deployed update, and
the latest and security gates still exit 2 for other open evidence.

### Remaining Conditions

None for this Task. The deferred scan, applicability review and config
checks stay `NOT_RUN`; criterion 15 keeps its decision in TSK-0009.

## Handoff

### Promotion Receipt

None: nothing was recorded here before this Task moved to the common form.

### Next Owner

None: nothing was recorded here before this Task moved to the common form.
