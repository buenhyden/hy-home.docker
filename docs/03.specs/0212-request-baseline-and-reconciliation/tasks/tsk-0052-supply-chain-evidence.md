---
title: "Supply-Chain Review and Artifact Evidence Task"
version: "0.1.5"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0052"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-10"
---

# Supply-Chain Review and Artifact Evidence Task

## Scope

### Objective and Parent

#### Objective

Finish the supply-chain evidence that TSK-0047 handed off for criteria 86 and
89. Criterion 104 gives every current update-ledger entry a fresh review and a
reviewed decision, so the latest-version gate passes or each unreviewable
entry is an explicit residual. Criterion 105 binds each selected image artifact
to its own signature, provenance and SBOM evidence. At initial issuance no
check had run; current partial source observations are recorded below.

- [Spec](../spec.md)
- [Plan](../plan.md)
- [Image supply-chain Task](tsk-0047-image-supply-chain-storybook.md)

### Inputs and Authority

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

## Execution Log

### Work Performed

#### Order

1. W109: review each ledger entry against its official release and advisory
   source, record the reviewed decision, and rerun the gate.
2. W110: for each selected artifact, verify the publisher signature and
   available provenance and SBOM against its exact digest, and record what the
   publisher does not provide.

Services that HOME runs go first; the rest follow in the same Task.

#### Open owner items

The following table preserves the initial questions. The current request and
public-origin section below records the later N1/N2 resolution.

| Item | Question | Needed by |
| --- | --- | --- |
| N1 | Which hosts may lookups reach? Already approved for earlier work: `github.com`, `api.github.com`, Sigstore, `cgr.dev`, the Alpine mirrors, `proxy.golang.org` and `sum.golang.org`. Registry reads also need Docker Hub, `ghcr.io` and `quay.io` metadata endpoints. | W109, W110 |
| N2 | All 89 entries now, or the services HOME runs first and the rest later? | W109 |

#### Current request and public-origin scope 2026-11-10

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

#### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0052 | draft | ready | #current-request-and-public-origin-scope-2026-11-10 |
| SPEC-0212-TSK-0052 | ready | in-progress | #current-request-and-public-origin-scope-2026-11-10 |

#### Public source refresh result 2026-11-10

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

#### Public source refresh continuation 2026-11-11

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

#### Official-advisory applicability continuation 2026-11-11

The durable review receipt is
`release-lookups.json#/master_20261111_advisory_review`; its gate receipt is
`#/master_20261111_advisory_review/gate_revalidation`. Every one of the 89
current ledger subjects now has a `reviewed_at` value, exact declared/source
binding, an official-advisory discovery/decision record or explicit
missing-origin residual, coverage limit, security applicability, separate
source action, and a latest-version disposition. The same records cover all 58
previous latest-version residuals. No declared pin, source input, selected
artifact, signature, provenance, SBOM, scan, compatibility, recovery or
acceptance field changed.

The bounded anonymous GitHub catalogue retrieval made 59 GET requests across
54 repositories and returned 1,088 records representing 688 unique advisory
identifiers; 51 endpoints completed. It is discovery evidence rather than a
claim that an empty or incomplete listing has no vulnerability: n8n returned
the same 100 records for four requested pages, SurrealDB returned the same 100
records for two pages before a 403, and `ollama-exporter` returned 404. The two
subjects without a primary advisory-source result are `ollama-exporter` and
external `blog-ingestion`. The absence of concrete advisory references and the
catalogue limitations are retained independently, so an endpoint failure or
empty result is not treated as absence of a security issue.

The security gate exits 2 with `ledger_complete=false`. It reports 29
ledger-complete rows pending independent verification, 54 `blocked-evidence`
rows, and six `blocked-no-fix` rows (60 blocked rows in total). Of the 89
reviewed classifications, 29 are component-scoped `NOT_AFFECTED`, 18 are
`AFFECTED` (12 patch candidates still need digest, scan, compatibility,
recovery and residual approval; six have no patch), and 42 are `UNKNOWN` and
therefore deferred. The 42 typed `reviewed_decision` residuals mean an
inconclusive classification, not an unreviewed subject. A component-scoped
`NOT_AFFECTED` decision does not assert that its complete image is clean.

The following decisions are source-only and separate normal version currency
from a security patch decision. Five declared image consumers carry the
affected pgBackRest component and require a candidate patch; encrypted
repositories also require a separately approved key/subkey inspection and, if
necessary, a new backup plus restore rehearsal. Qdrant's declared single-node
topology does not show the documented exploit path, but its version range is
affected. SurrealDB requires a candidate move from 2.7 to 4.0.1 with separate
migration, backup and restore planning, and Open Notebook requires the 1.15.1
fix candidate. The two OpenBao rows retain the vendor-unpatched `go-jose/v3`
line residual; existing acceptance is not renewed. SeaweedFS has publisher
no-fix evidence. Gatus lacks sufficient fixed-range evidence and remains
`UNKNOWN` even though normal version work is tracked.

Source binding discrepancies remain explicit residuals. MLflow has a 3.16.1
candidate, 3.17.2 rendered output and 3.18.0 Dockerfile input; OAuth has a
7.15.5 candidate but a 7.15.6 Dockerfile input. Pushgateway's selected 1.11.5
is newer than the reported 1.11.4 and is not downgraded. Neo4j's selected 5.26
LTS line and Confluent's supported 8.3 line are retained independently of
their newer global/current lines. n8n's direct production changelog names
2.47.3 stable and 2.48.0 beta, while the rendered GitHub UI difference remains
recorded; incomplete catalogue coverage and its separate runner product leave
the aggregate security decision `UNKNOWN`.

The revalidated `latest_version_gate` also exits 2 with `ready=false`: 33 of
89 rows are complete and 56 retain residuals. The overlapping reasons are 43
target/latest mismatches, 21 missing stable-channel proofs, four unresolved
latest values, and three each lacking fresh lookup or primary reference. Its
89-service/33-file closure remains
`44e286a69d910939ba36f59fd65a08a4f4ac7a1ae5dd8e9be11e29af4bfdac84`.
Twelve numeric current/candidate pairs are component proposals only, not
selected-image changes. No operational upgrade, image pull, build, scan,
deployment, credential use, recovery action or risk-acceptance renewal ran.

#### Exact artifact and official-source continuation (2026-11-11)

The owner's follow-up authorizes public registry reads and temporary isolated
scans for this review. The [version and artifact receipts](../../../../infra/09-platform-ops/security-updates/release-lookups.json)
record actions for the 56 previous latest-version residuals and the 60 open
security rows under `master_20261111_artifact_review`. The declaration and
target remain bound to the current source. The publisher's Renovate release
advanced to 44.227.4, and n8n's release notes identify 2.47.3 as stable.
Pushgateway has a 1.11.5 tag and matching image while the project's download
page and GitHub Latest still report 1.11.4. The 1.11.5 pin is retained pending
publisher channel confirmation.

The three public patch candidates have exact linux/amd64 manifest and matching
local Syft and Grype receipts. Qdrant's publisher signature verifies the
multi-platform index, which binds the scanned platform and its attached
SPDX and SLSA predicates. Keycloak and Open Notebook expose subject-matching
SLSA predicates. Their publisher signatures and publisher SBOMs are pending.

| Public candidate | Publisher signature | Grype Critical matches | Grype High matches |
| --- | --- | ---: | ---: |
| Keycloak 26.8.2 | Unverified | 1 | 5 |
| Open Notebook 1.15.1-single | Unverified | 48 | 512 |
| Qdrant v1.20.0-unprivileged | Verified index | 0 | 62 |

These counts describe package matches. Compatibility, recovery, and residual
adjudication remain required for all 12 patch rows. Nine rows await a final
custom artifact. SurrealDB, Tempo, OpenTofu, and the Storybook MCP Node runtime
have separately scanned upstream inputs. OpenTofu also has a verified upstream
index signature. For the five pgBackRest consumers the supplier fix floor is
2.59.3. Alpine publishes 2.60.0-r0 on edge; the two tracked build lines use
v3.23 and v3.24, which still list 2.57.0-r0 and 2.58.0-r0 respectively.

The six no-fix rows remain blocked on the applicable OpenBao go-jose v3 and
SeaweedFS advisories. For the 42 deferred rows, the receipt records observed
publisher advisories, lookup failures, and the action for each service. Exact
declared-image scans cover 20 of those services across 17 distinct images.
The Ollama exporter now has official Node.js and OpenSSL evidence for packages
found in its image. Service applicability remains pending. Blog ingestion
still needs evidence from its external producer. GitHub API pagination and
registry access failures are recorded alongside their bounded fallbacks.

### Blockers and Decisions

None: nothing was recorded here before this Task moved to the common form.

## Verification Evidence

### Results

The first two NOT_RUN rows preserve initial issuance. Their N1/N2 wait text
is historical. Later rows record the source observations, partial exact
artifact verification and the current gate results.

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
| Official-advisory continuation | 104 | W109 | anonymous official advisory applicability review | All 89 current ledger subjects and all 58 preceding latest residuals; source base `305d93a8dbb16b71f7c34a55a7b20370f78d6f6f` | PASS | `release-lookups.json#/master_20261111_advisory_review`; 59 GitHub GETs/54 repositories, 1,088 returned records/688 unique identifiers, with incomplete n8n and SurrealDB pagination and `ollama-exporter` 404 retained as limits | required | - |
| Revalidated latest-version gate (advisory continuation) | 104 | W109 | `latest_version_gate` | 89-entry ledger and 33-file source closure | FAIL | Exit2; 33 complete and 56 residual;43 mismatch,21 channel,4 unresolved,3 fresh and3 reference residuals (overlap); exact service coverage and closure hash retained | required | - |
| Revalidated security-update gate (advisory continuation) | 104 | W109 | `security_update_gate` | Same 89-entry ledger | FAIL | Exit2; all89 fresh reviews recorded;29 ledger-complete pending independent verification,54 blocked-evidence and6 blocked-no-fix. No artifact-level security proof or operational acceptance is inferred. | required | - |
| Advisory gate policy check | 104 | W109 | static supply-chain policy | Updated review contract | PASS | Five contracts/13 cases; policy/static result only, not a live artifact or recovery observation | required | - |
| Advisory review regression | 104 | W109 | focused supply-chain gate tests | Frozen `master_20261111_advisory_review` records | PASS | TDD RED: one expected missing-key failure; integration then exposed and corrected three empty-reason failures. Initial GREEN:96 tests in4.970s, including two new tests in0.104s; Ruff, formatting and lint passed. No production gate code changed. | required | - |
| Exact artifact investigation | 105 | W110 | Registry and isolated Cosign, Syft and Grype | 12 patch rows | FAIL | Three exact final scans; one verified final index signature and matched published SBOM. Nine final custom images pending. Scans, publisher evidence and remaining actions are bound to the named subject. | required | - |
| Official evidence and follow-up | 104 | W109 | Public release, security and package sources | 56 latest residuals and 60 security residuals | FAIL | 56 latest actions, six no-fix reviews, 42 deferred decisions, and 20 deferred services with exact scans. One primary advisory reference still missing. | required | - |
| Latest-version gate (artifact continuation) | 104 | W109 | `latest_version_gate` | 89 ledger rows and 33 Compose source files | FAIL | Exit2; 33 complete and 56 residual. Both gates independently match the same 89 services and source closure. | required | - |
| Security-update gate (artifact continuation) | 104 | W109 | `security_update_gate` | Same 89 rows and source closure | FAIL | Exit2; 29 pending independent verification, 54 blocked-evidence, six blocked-no-fix. Exact candidate and scan gaps fell from 12 to nine; the primary advisory gap fell from two to one. | required | - |
| Artifact gate regression | 104 | W109 | Focused supply-chain and CI routing tests | Ledger and lookup references | PASS | RED reproduced the absent artifact evidence. The final focused run passed 97 tests; static policy passed five contracts and 13 cases. | required | - |
| Controller dependency audit | 104 | W109 | `pip-audit` and `npm audit` | Controller lock and Storybook production lock | FAIL | Python audit reported 25 findings across 36 checked requirements. Storybook npm audit reported zero. Both locks match the source baseline; controller findings need separate dependency triage. | optional | - |

### Resolution Links

None: nothing was recorded here before this Task moved to the common form.

## Acceptance Decision

### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 104 | pending | Ledger fresh review | All89 entries now have an official-advisory applicability classification and reviewed decision, but both gates FAIL:56 latest residuals remain and security rows still require independent artifact/compatibility/recovery evidence or retain an explicit block/defer. | SPEC-0212 TSK-0052 |
| 105 | pending | Artifact verification | Three public final candidates scanned. Qdrant index signature verified; other publisher proofs, final custom artifacts and residual decisions remain pending. | SPEC-0212 TSK-0052 |

### Remaining Conditions

Current source research and isolated artifact checks have run as recorded
above. Both ledger gates still fail. Criteria 104 and 105 remain pending.
Compatibility, recovery and operational execution remain separate and are
recorded as NOT_RUN.

Completion needs a passing latest-version gate or each remaining entry recorded
as a residual, independently verified security dispositions for affected or
blocked components, and a verification row for each selected artifact. A
receipt for one component or artifact never proves another.

## Handoff

### Promotion Receipt

None: nothing was recorded here before this Task moved to the common form.

### Next Owner

None: nothing was recorded here before this Task moved to the common form.
