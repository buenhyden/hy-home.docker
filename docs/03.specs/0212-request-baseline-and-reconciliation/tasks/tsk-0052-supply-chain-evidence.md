---
title: "Supply-Chain Review and Artifact Evidence Task"
version: "0.1.2"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-11"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0052"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-10"
---

# Supply-Chain Review and Artifact Evidence Task

## Overview

### Objective

Finish the supply-chain evidence that TSK-0047 handed off for criteria 86 and
89. Criterion 104 gives every current update-ledger entry a fresh review and a
reviewed decision, so the latest-version gate passes or each unreviewable
entry is an explicit residual. Criterion 105 binds each selected image artifact
to its own signature, provenance and SBOM evidence. At initial issuance no
check had run; current partial source observations are recorded below.

## Inputs and Authorization

On 2026-11-10 the owner (@buenhyden) set TSK-0047 criteria 86 and 89 to
not-required and approved this dedicated Task for the unfinished work. That
decision opens the Task only. Every network lookup waits for the owner to
approve its host scope in N1 below, under the
[approval boundaries](../../../../.agents/governance/approval-boundaries.md).
No image pull, deployment or HOME change is part of this Task.

The starting state comes from the
[TSK-0047 supply-chain handoff](tsk-0047-image-supply-chain-storybook.md#supply-chain-handoff-2026-11-10):
on 2026-11-10 `security_update_gate` exits 2, with all 89 ledger entries
`blocked-evidence` (`fresh_review` and `reviewed_decision` missing for 89,
`primary_advisory` for 79).

## Work Log

### Order

1. W109: review each ledger entry against its official release and advisory
   source, record the reviewed decision, and rerun the gate.
2. W110: for each selected artifact, verify the publisher signature and
   available provenance and SBOM against its exact digest, and record what the
   publisher does not provide.

Services that HOME runs go first; the rest follow in the same Task.

### Open owner items

The following table preserves the initial questions. The current request and
public-origin section below records the later N1/N2 resolution.

| Item | Question | Needed by |
| --- | --- | --- |
| N1 | Which hosts may lookups reach? Already approved for earlier work: `github.com`, `api.github.com`, Sigstore, `cgr.dev`, the Alpine mirrors, `proxy.golang.org` and `sum.golang.org`. Registry reads also need Docker Hub, `ghcr.io` and `quay.io` metadata endpoints. | W109, W110 |
| N2 | All 89 entries now, or the services HOME runs first and the rest later? | W109 |

### Current request and public-origin scope 2026-11-10

The current trusted user explicitly requested implementation of the complete
master change plan on2026-11-10. That request authorizes bounded anonymous
public source research and local ledger/test changes. It resolves N1 for the
actual official origins below and N2 as all89 current entries, prioritizing
HOME services. The earlier opens/NOT_RUN statements remain historical inputs,
not a renewed blanket permission wait. No credential, image layer, image
activation, remote write, paid inference or outside workspace is included.

The actual GET scope is `api.github.com` and `github.com` release metadata for
the48 repository paths in the recorded inventory; vendor pages at
`www.python.org/downloads/`, `www.postgresql.org/support/versioning/`,
`docs.confluent.io/platform/current/release-notes/index.html`,
`neo4j.com/deployment-center/`, and
`raw.githubusercontent.com/aws/aws-cli/v2/CHANGELOG.rst`; and anonymous
`hub.docker.com/v2/repositories/` tag metadata for the named ledger images.
The recorded queries have no pagination, authentication or binary download.
The one direct Docker Hub retry used5-second connect and10-second total limits.
Actual URLs, times, query counts and limits remain in the existing
`release-lookups.json#/master_20261110_public_refresh` source owner.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0052 | draft | ready | #current-request-and-public-origin-scope-2026-11-10 |
| SPEC-0212-TSK-0052 | ready | in-progress | #current-request-and-public-origin-scope-2026-11-10 |

### Public source refresh result 2026-11-10

The source writer recorded49 GitHub GET attempts over48 repositories:
47 distinct published-final observations and one Searx latest-release404.
The Airflow request was repeated once in the grouped retrieval. Five vendor
pages were read. Five Docker Hub URL probes failed, including an initial
unmatched sandbox-name probe; the exact subsequent subjects and a direct
ollama-exporter retry remain recorded failures. A404 is not proof of absent
product tags, and GitHub non-prerelease metadata is not vendor stable-channel
proof.

All89 current ledger rows were classified:67 GitHub published-final facts,
13 direct Python/PostgreSQL stable-channel facts, four other vendor facts,
two local Storybook producer locations, two lookup failures and one excluded
external source. Only13 direct vendor-table stable fields were refreshed;
prior facts remain historical. No declared image pin changed.

The focused supply-chain regression suite passed88 tests in4.740 seconds and
the static policy check passed five contracts/13 cases. The latest-version
gate still exits2:13/89 have complete current lookup evidence;76 lack fresh
lookup,30 mismatch latest, four are unresolved, ten lack stable-channel proof
and seven lack a primary reference. These reason counts overlap. Missing or
unexpected services are0. All89 exact-subject signature/provenance/SBOM
executions remain NOT_RUN; release asset names/digests show availability only.
n8n full-image signature/scan remains TSK-0041 criterion60, while this Task
owns the other exact artifact residuals under criterion105.

### Public source refresh continuation 2026-11-11

The 76 rows that previously lacked a fresh lookup were reviewed together with
the 13 rows that already had current lookup fields. The source writer renewed
73 public rows and retained three deliberately unrenewed internal or external
rows (`storybook`, `storybook-mcp`, and `blog-ingestion`). The durable request
and field-level receipt is
`release-lookups.json#/master_20261111_public_refresh`; its gate receipt is
`#/master_20261111_public_refresh/gate_revalidation`. All declared pins,
candidate targets, source bindings, security and artifact fields, and
historical observations remain unchanged.

The source writer made 49 root GitHub requests: 48 published-release responses
and one Searx latest-release 404. Four separate research packets recorded
primary supplier documentation or official tag metadata. A GitHub final-release
response alone was not treated as a stable-channel result. Supplier-specific
normalization recorded explicit stable, GA, current-production, supported-line,
or selected-line facts only where the supplier documentation supported that
meaning. Examples include Gatus stable package 5.38.0, n8n production stable
2.47.3 (separate from beta 2.48.0), and the selected Neo4j 5.26 LTS patch
5.26.33 (separate from global 2026.10.2). Confluent's current 8.4.1 line was
kept distinct from the selected 8.3.2 line. Pact Broker was corrected to the
selected Docker stream 3.0.0 / full image
3.0.0-pactbroker2.121.2, rather than the separately versioned Ruby application
release 2.122.0. These source facts do not verify an image artifact.

The rerun `latest_version_gate` still exits 2 with `ready=false`: 31 of 89
rows are complete and 58 retain one or more residuals. Those residuals are 43
target/latest mismatches, 26 missing stable-channel proofs, four unresolved
latest values, and three each without a fresh lookup or primary release
reference. Counts overlap. The three fresh/reference residuals are the two
local Storybook producers and external `blog-ingestion`; ComfyUI's unknown
target remains one of the four unresolved values. The source closure remains
`44e286a69d910939ba36f59fd65a08a4f4ac7a1ae5dd8e9be11e29af4bfdac84`, with
no missing or unexpected service.

The same revalidation reran `security_update_gate`, which still exits 2 with
zero complete rows: all 89 lack a fresh review and reviewed decision, and 79
lack a primary advisory. Release and channel research is not a security
applicability review, so no decision was fabricated to satisfy that gate.
This continuation ran no new exact-subject signature, provenance, SBOM, scan,
compatibility, recovery, runtime, deployment, or rollback checks. Historical
receipts remain bound to their recorded subjects; criterion105 artifact
verification remains NOT_RUN.

## Evidence

The first two NOT_RUN rows preserve initial issuance. Their N1/N2 wait text
is historical; later source observations and the still-failing gate are separate
rows. Exact artifact execution has not run.

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Ledger fresh review | 104 | W109 | `security_update_gate` against the update ledger | 89 entries at the start of the Task | NOT_RUN | Waits for N1 and N2. | required | - |
| Artifact verification | 105 | W110 | Per-artifact signature, provenance and SBOM verification | Selected image digests | NOT_RUN | Waits for N1 and W109. | required | - |
| Public metadata refresh | 104 | W109 | anonymous-public-source-research | Source648a78a26, unchanged supply inputs at c463e4ae5 | PASS | Existing release-lookups/update-ledger master_20261110_public_refresh;89 rows classified, stable-channel limits preserved | optional | - |
| Focused source regression | 104 | W109 | supply-chain-regression | Refreshed local source records | PASS | Writer receipt:88 tests in4.740s; static policy five contracts/13 cases | optional | - |
| Current latest-version gate | 104 | W109 | latest-version-gate | Refreshed89-entry source ledger | FAIL | Exit2;13 complete,76 fresh missing,30 mismatch,4 unresolved,10 channel and7 reference residuals | required | - |
| Official source continuation | 104 | W109 | anonymous public release/channel research | 76 former fresh-lookup residuals plus 13 retained current rows | PASS | `release-lookups.json#/master_20261111_public_refresh`; 73 public rows renewed and three internal/external rows retained as residuals | optional | - |
| Revalidated latest-version gate | 104 | W109 | `latest_version_gate` | 89-entry ledger; source HEAD `b17895e7181431b7282f8e95bc6c5e4f44ab4517` | FAIL | Exit2;31 complete,58 residual;43 mismatch,26 channel,4 unresolved,3 fresh and3 reference; counts overlap, service coverage exact | required | - |
| Revalidated security-update gate | 104 | W109 | `security_update_gate` | Same 89-entry ledger | FAIL | Exit2;0 complete;89 fresh-review,89 decision,79 advisory residuals; release facts do not establish security applicability | required | - |
| Revalidation regression | 104 | W109 | focused supply-chain regression | Updated ledger facts | PASS | Initial suite:94 PASS in4.781s. The first post-change run recorded three obsolete n8n-2.46.6 expectation failures in4.839s; a first corrected suite passed94 tests in7.295s. The final robustness run passed94 tests in5.411s; it requires a residual action only for a version mismatch, rather than for every other residual. Ruff, formatting and diff checks passed. Static policy remains PASS (five contracts/13 cases). | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 104 | pending | Ledger fresh review | Official source facts refreshed for the remaining lookup scope, but latest and security gates both FAIL; 58 latest residual rows and all 89 security reviews remain unresolved. | SPEC-0212 TSK-0052 |
| 105 | pending | Artifact verification | No verification has run. | SPEC-0212 TSK-0052 |

## Review and Completion

Current source research and isolated checks have run as recorded above. The
original unrun statements and the first RED regression receipt remain
historical. The corrected regression suite is green. The latest-version and
security gates still fail, and exact artifact execution remains NOT_RUN. No
criterion is accepted.

Completion needs a passing latest-version gate or each remaining entry recorded
as a residual, and a verification row for each selected artifact. A receipt
for one artifact never proves another.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [Image supply-chain Task](tsk-0047-image-supply-chain-storybook.md)
