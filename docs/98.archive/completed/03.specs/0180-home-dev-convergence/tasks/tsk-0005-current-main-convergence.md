---
title: "Current Main Home and Development Convergence"
version: "1.0.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-09-24"
layer: "specs"
artifact_id: "SPEC-0180-TSK-0005"
parent_ids:
- "SPEC-0180"
- "SPEC-0180-PLAN-0001"
created: "2026-09-20"
---

# Current Main Home and Development Convergence

## Objective

Close remaining [SPEC-0180](../spec.md) gaps against current main using the
refreshed [Plan](../plan.md). This Task is the canonical execution ledger for
the follow-up. Preserve earlier completion evidence and report current findings,
implementation, independent reviews and actual validation without claiming
unapproved runtime acceptance.

## Inputs

- Owner's 73-section Home + Development Server convergence implementation
  request, including critical existing-plan review and subagent-driven execution.
- Main baseline `dffc2ed8bc3bf4b2538b03884ad7ab5d7587375b`; isolated branch
  `codex/home-dev-convergence-followup`.
- [REQ-0027](../../../01.requirements/0027-home-development-host.md),
  [AD-0031](../../../02.architecture/descriptions/0031-home-development-host.md),
  current tracked implementation, public schemas, canonical profile/version
  owners, Stage 99 contracts and registered checks.
- [Task 0001](tsk-0001-home-dev-convergence.md) initial implementation;
  [Task 0002](tsk-0002-openbao-access-and-env-convergence.md) OpenBao and metadata;
  [Task 0003](tsk-0003-keycloak-oidc-operations-research.md) auth research;
  [Task 0004](tsk-0004-native-oidc-service-migration.md) completed native OIDC.

## Work Log

### Baseline and authority

- 2026-09-20: Entered the isolated follow-up worktree at the baseline above;
  loaded bootstrap/provider, documentation role, governing source and historical
  Tasks. The old Plan's 2026-09-19 baseline and linear execution sequence required
  refresh before new implementation.
- Refreshed Spec and Plan in place. The Spec retains nine acceptance criteria;
  the Plan retains correspondence to W1–W9 and defines current A–G/R dependencies,
  ownership interfaces, preflight and review checkpoints.
- Used the documentation writer's `knowledge-map-agent` procedure for canonical
  navigation. No advisory graph output is used as proof and no new Spec,
  progress ledger or duplicate policy is introduced.
- Sandbox startup reported `bwrap: loopback: Failed RTM_NEWADDR`; required reads
  and authorized worktree edits use reviewed escalated execution. This does not
  broaden repository or runtime scope.

### Acceptance assessment at current-main entry

Statuses describe demonstrated scope: **completed** means evidence covers the
named item; **partially completed** means delivered work has a remaining gap;
**stale** means evidence or assumptions need current-baseline refresh;
**not implemented** identifies an explicitly absent deliverable;
**superseded** identifies a prior instruction replaced by a current owner or
execution; **new gap** is newly identified drift. A static PASS proves only the
checked invariant. Pending audits do not become invented findings.

| Criterion | Entry classification | Evidence and remaining obligation | Current unit |
| --- | --- | --- | --- |
| 1 — measured inventory and justified disposition | partially completed; inventory cells stale | Current audit measures 42 fragments, 140 services and 64 profiles; four inventory rows are stale and five required fields plus actual-consumer evidence are missing | A |
| 2 — official architecture/dependency evidence | partially completed | Task 0001 records primary sources; current architecture references have been fetched, but retained-component deployment/security/backup/migration/lifecycle/license coverage still needs the current audit | A, C, E |
| 3 — include/profile/closure/port agreement and maintenance isolation | partially completed | All 64 profile renders pass, but broad tooling activates load/IaC, named membership is unchecked and default gates omit HOME union safety | B, G |
| 4 — Stage 99, README and Stage 05 responsibilities and literal policy | partially completed | Prior contract/navigation implementation exists and current catalog passes; Open WebUI policy still requires `sso-auth@file` despite completed native OIDC; Gatus gateway-auth wording needs correction, alongside the documentation audit | D, E |
| 5 — version projection, fail-closed sources and unique updater | partially completed | Current version projection check passes; source completeness and custom-manager duplicate extraction require separate evidence; current official repository/global strict validation passes | C |
| 6 — public/private environment and secret metadata closure | partially completed | Current safe audit confirms 247 public/private keys and 93 IDs at mode0600; missing OpenBao metrics secret, legacy Vault root-token grant, mode guardrail and consumer checks remain | F |
| 7 — focused regressions and applicable gates | stale | Prior Tasks contain passing suites for their revisions; current operations/version checks and secret dry-run are observed, full/changed/review are pending and secret readiness check is blocked by missing htpasswd | G |
| 8 — runtime, persistence, resources and restore evidence distinguished | partially completed | OpenBao, Open WebUI and Gatus acceptance is completed within Tasks 0002/0004; broad HOME cold start, reboot, peak/growth and isolated restore acceptance is not established | A, F, G |
| 9 — reviewed logical commits and PR report | superseded for prior delivery; not implemented for this follow-up | Task 0001 PR #167 and Tasks 0002/0004 branch/PR #168 are historical delivery; this branch needs its own final review, logical commit and report evidence | G |

### Original W1–W9 assessment

| Original work unit | Classification | Source-based disposition | Current owner |
| --- | --- | --- | --- |
| W1 inventory and references | partially completed; inventory cells stale | Current static counts refreshed at 42/140/64; four service rows and missing fields/consumer evidence remain | A, R |
| W2 disposition, architecture and profiles | partially completed | REQ-0027/AD-0031 and POL-0078 exist; retain always-on AI/workflow requirement and test current selection/consumer closure | B, R |
| W3 Stage 99 and regressions | completed for historical implementation; current adequacy under review | Task 0001 records implemented contracts and focused tests; no evidence yet justifies replaying or broadening them | D |
| W4 profiles, navigation and Stage 05 | partially completed | Existing catalog passes, but presence/link validity alone does not establish substantive operating/recovery guidance | B, E |
| W5 version and update ownership | partially completed | Current registry check passes; complete extraction and owner coverage require the version audit and official checks | C |
| W6 environment/secret contracts | partially completed | Tasks 0002/0004 completed prior safe synchronization; current consumer/schema closure is being compared without reading private values | F |
| W7 gates and independent review | stale | Historical final checks apply to earlier revisions; run the current changed/full and selected checks after implementation | G |
| W8 private metadata and runtime verification | partially completed; original rollout instruction superseded | Later Tasks own exact approved OpenBao/OIDC actions; their authorization does not approve a fresh blanket rollout. Broad resource/reboot/restore proof remains unimplemented | F, G |
| W9 commits and PR evidence | superseded for original branch; not implemented for current delivery | Earlier delivery remains in its Task/Git history; this follow-up needs a new reviewed delivery record | G |

The **new gap** established before implementation is that the active Plan had no
current-main comparison, bounded file ownership or dependency/review interfaces
for the requested follow-up. The refreshed Plan closes that planning gap. A further **new gap** is confirmed authentication-policy drift: the current
[Open WebUI policy](../../../05.operations/catalog/08-ai/0057-open-webui/policy.md)
requires `sso-auth@file`, while Task 0004 and its current Compose router use native
OIDC and the standard gateway chain. The
[Gatus policy](../../../05.operations/catalog/06-observability/0087-gatus/policy.md)
also needs unambiguous native-versus-gateway authentication wording. Structural
catalog success does not prove semantic policy correctness. E owns this repair;
further implementation gaps require source-backed audit evidence.

### Entry A–G/R task ledger (superseded)

This table records the entry plan before implementation. Its pending labels are
historical and are superseded by the dated current implementation ledger below.

| Unit | State | Evidence/output | Next checkpoint |
| --- | --- | --- | --- |
| A inventory | audit completed; integration pending | 42 includes, 140 services, 64 profiles; 140 classification rows with four stale entries | Populate all twenty mission fields and actual-consumer evidence without claiming runtime proof |
| B profiles | implementation pending | Confirmed tooling load/IaC bypass and missing membership/HOME safety enforcement | Repair canonical profiles/gates with negative tests and independent review |
| C versions | in progress | Current tech-stack check passes; source audit pending | Complete ownership/source/extraction matrix and focused review |
| D templates/contracts | pending audit | Existing contract implementation retained | Prove a gap before changes, then focused contract review |
| E docs/README | in progress | Current source coverage audit pending | Substantive retained-service closure and reviewed documentation |
| F env/secrets | audit completed; implementation pending | Current schema equality/modes safe; credential closure and mode/consumer guardrails fail | Correct scoped public contracts and synthetic preservation/security regressions |
| R rationalization | pending evidence review | Existing dispositions: HOME37 DEV8 OPTIONAL48 LAB45 MIGRATE2 REMOVE0 | Distinct implementer verifies actual consumers and owns justified lifecycle decisions/path handoffs; no removal assumed |
| G validation/review | pending integration | Baseline checks below; full profile explain passes | Unit spec/quality reviews, corrections, full/changed gates, whole-branch review |

Implementers own disjoint assigned files. Shared validator edits require an
explicit handoff; scratch SDD coordination may mirror this ledger but cannot
replace it. No unit is complete merely because its implementation was written.

### Current audit findings

The read-only inventory, profile and environment audits at baseline
`dffc2ed8bc3bf4b2538b03884ad7ab5d7587375b` establish:

- **Inventory:** 42 tracked Compose fragments equal 42 root includes; no
  missing/unreachable include, duplicate service or unprofiled service. There
  are 140 unique services, 64 policy/Compose profiles and 261 profile-service
  declarations. Current policy service lists match exactly but are not enforced.
  All 140 services have dated classifications: HOME 37, DEV 8, OPTIONAL 48,
  LAB 45, MIGRATE 2, REMOVE 0. The historical Task 0001 coverage matrix has
  420 resolving links (132 active and eight draft triplets), not a current
  production validator contract.
- **Stale inventory:** m0021 Gatus/Open WebUI rows predate native OIDC secrets,
  environment and mounts; Mailpit row omits loopback/listeners/health; SurrealDB
  row incorrectly describes all-interface publication. Required Security,
  Backup, Operations docs, Runtime version authority and Update owner fields
  are absent. Domain/component are only derivable, disposition is conflated
  with classification, and declared reverse dependencies do not prove actual
  consumers. A/E refresh derived coverage; R owns disposition decisions.
- **Profile gap:** `tooling` selects Locust and OpenTofu/Terrakube as well as
  their explicit automation purposes. Locust worker lacks `testing`. A synthetic
  wrong `Selected services` row is accepted by the current validator; same-count
  swaps, malformed/duplicate members and missing lists need negative tests.
  Default Compose validation checks individual profiles, not the HOME union.
  Current HOME selects exactly its 37 dispositions with no required dependency
  escape or unsafe selector, but CI must enforce that fact and union port safety.
- **Public/private metadata:** deterministic value-free inspection found 247
  exact public/private keys and 93 exact public/private IDs; private targets are
  ignored and mode `0600`. There are 23 registry env mappings, 70 registered
  secret-file paths, and 69 root declarations/granted identities with exact
  equality. Public keys classify as `ACTIVE_REQUIRED` 59, `ACTIVE_OPTIONAL`
  186, `MIGRATION_ONLY` 2 (`VAULT_PORT`, `VAULT_CLUSTER_PORT`), `DEPRECATED` 0,
  `ORPHAN` 0. All 93 public values are placeholders. This current safe instance
  does not prove the synchronization guardrails are sufficient.
- **Secret/config gap:** both Prometheus configs read
  `/run/secrets/openbao_token` without its declaration/grant/registry contract.
  Active Prometheus grants `vault_token`, whose public metadata identifies a
  legacy Vault root token, and retains the legacy scrape job. F must resolve
  least-privilege public configuration within scope; issuing or rotating a
  credential and restarting services remain separately authorized runtime work.
- **Sync/check gap:** synthetic mode `0644` targets pass metadata check unchanged;
  current tests only prove mode `0600` for a newly created registry. Require
  existing-target mode checks/atomic correction and symlink/non-regular rejection
  for both files. Current CI validates schema shape but omits full consumer,
  migration-only, registry-consumer and service-owned literal secret closure.
  Preserve ID-based values and unknown/removed entries by default; only an exact
  explicit pruning exception may remove metadata, never secret files.
- **CI coverage:** the inventory audit finds five of the thirteen requested drift
  classes covered, two partial (profile membership and env orphans), and six
  missing (new/removed service operations ownership, missing Guide infra path,
  updater overlap, duplicate custom extraction and stale Dependabot directory).
  Extend canonical checks rather than adding parallel validators. The version
  audit subsequently confirms missing enforcement for updater ownership and
  extraction coverage; current strict-validator/projection PASS does not prove
  completeness. Its authored-source audit finds 31 registry components/34 image
  entries against 81 distinct active Compose repositories, with 46 external
  repositories unregistered. A new unregistered source and missing top-level
  `source_of_truth` each pass synthetic checks incorrectly. Active README/ADR
  literal coverage is incomplete; 0083 duplicates policy owned by 0086.
  Renovate unknown-timestamp release-age handling needs an explicit decision;
  infrastructure updater overlap is not currently observed.

The controller also refreshed the official [MinIO community repository](https://github.com/minio/minio)
on 2026-09-20: GitHub reports it archived/read-only on 2026-04-25 and the README
states it is no longer maintained, with source-only distributions. Current AIStor
documentation is not equivalent evidence for the community implementation. R must
preserve the existing HOME S3 capability, actual consumers and data while recording
migration evaluation as a separate disposition/reason; no automatic replacement
or data migration is authorized. The m0021 and MinIO operator-document updates
follow the reviewed inventory/contracts handoff.

### Scoped planning-review correction

The planning reviewer found that read-only inventory and lifecycle implementation
were conflated, F's acceptance omitted required classifications and file-safety
details, and the inventory checkpoint did not enumerate the complete field set. The Plan now assigns Task 8/R as a distinct rationalization
implementer with exact lifecycle path handoffs, evidence-backed decisions and no
assumed removal. F now names all five key classes, mode `0600` check/write,
symlink/non-regular rejection, ID-based preservation, explicit prune exceptions
and no secret-file deletion. A's checkpoint now explicitly requires every row
to include Domain, Component, Compose path, Service, Profiles, Runtime
classification, Consumer, Dependencies, Network, Ports, Persistence, Env, Secret
metadata, Resources, Security, Backup for stateful services, Operations docs,
Runtime version authority, Update owner and Disposition. Independent scoped
re-review confirmed those three corrections. A subsequent medium finding
identified missing R↔G shared-file handoff wording. The Plan now explicitly
routes R's lifecycle validators, shared tests and examples to G and requires G
to accept the exact-path handoff before edits/integration. That focused
correction awaits scoped re-review.

### Current implementation update (2026-09-20)

This section supersedes the entry-state labels and interim status statements above.
The entry tables remain historical evidence of what the follow-up found; they are
not the current implementation verdict. All implementation units now have
independent specification and quality approval within their reviewed scopes.
All four later whole-branch findings were corrected and independently approved.
Final whole-branch review is SPEC APPROVED, QUALITY APPROVED and SECURITY
APPROVED with no Critical, Important or Minor findings in that reviewed snapshot.
The local changed runner used its no-PR-base `check-active` substitution
(selected 449, violations 0), while the local full gate used
`check-contracts`; neither exercised the PR-range changed-body heading ratchet.
The first required hosted `validation-changed` check failed on committed metadata
coverage. That 24-document heading-only correction is independently reviewed,
green, committed and pushed. Draft PR 169 now has three commits at
`0eaa445a7a9820a8dd6289adacd7b900543443b0`. Its next hosted run passed metadata
and lifecycle, then failed the later all-files pre-commit leaf when 35 unique formatting targets were found: 11 EOF targets plus 6 trailing-
whitespace targets with one overlap (16 unique), and 19 additional Markdownlint
targets, and the Gatus Dockerfile triggered DL4006.
Those exact local corrections are frozen, green and independently approved but
are not yet committed or pushed; no merge or runtime action occurred.

The canonical current inventory is the
[140-service, 20-field matrix](../../../90.references/research/0002-agentic-engineering-research-pack/m0021-local-docker-service-consolidation.md).
Profile vocabulary and HOME activation are owned by
[POL-0078](../../../05.operations/catalog/00-workspace/0078-compose-profile-vocabulary/policy.md).
Version and updater ownership are owned by
[POL-0086](../../../05.operations/catalog/00-workspace/0086-dependency-version-management/policy.md).
This Task records execution evidence and does not duplicate those policy surfaces.

| Unit | Current result | Independent review and remaining boundary |
| --- | --- | --- |
| A — inventory | The canonical renderer and catalog join cover 140 current services, all twenty required fields, exact source identities, consumer/backup/disposition evidence and typed Guide ownership. | **APPROVED**. Twelve direct inventory tests pass after the direct-entrypoint minor was corrected. Static source closure is not runtime proof. |
| B — profiles | Current checks enforce required HOME selectors, case-insensitive reserved HOME handling, tooling and lifecycle isolation, and conservative ksql automation treatment. | **APPROVED**. Reviewer reran 29 focused tests; the implementation also recorded 77 whole-module tests. |
| C — versions | The derived projection contains 81 repositories: 75 external and six local/custom. Source discovery, updater ownership, strict configuration and non-writing preview behavior are covered. | **APPROVED**. Reviewer ran 30 focused and 49 full tests and both official strict Renovate validators. |
| D — contracts | Root Compose variants, inline Dockerfile authority and real CommonMark authority links fail closed after the three reproduced bypasses were corrected. | **APPROVED**. Same reviewer observed the three exact witnesses, 28 runtime tests, 63 heading tests and the 12 direct A tests. |
| E — documentation | Storage, databases/messaging, applications, platform and root/architecture correction packets are frozen. Exact current README, Guide/Policy/Runbook, source-authority, lifecycle, auth, recovery and onboarding statements replaced the initial shallow pass. | **APPROVED** in every E subdomain: storage plus README integration, databases, applications, platform and root. Earlier correction-required and pending labels are superseded by their final reviews. |
| F — environment/secrets | Public schema remains 247 keys and now contains 94 IDs; SEC-002 is a staged manual OpenBao metrics contract. The scanner covers copied build inputs, lexical tracked symlinks and normalized runtime paths. | **APPROVED**. Reviewer reran 30 focused tests. Deployed main private metadata remains 93 IDs; no credential was issued or synchronized. |
| R — lifecycle | Final counts are HOME 37, DEV 9, OPTIONAL 47, LAB 45, MIGRATE 2 and REMOVE 0. The only classification change from the provisional set is locust-worker from OPTIONAL to DEV. | **APPROVED**. All 140 judgments and ten overlap decisions were source checked. Four currently running non-HOME containers remain a transition gap. |
| G — integration/delivery | All four earlier whole-branch findings are corrected and independently approved. The first hosted run exposed 25 metadata rows across 24 files; the pushed heading correction resolved them. Run 35476114948 / job 105985535619 then passed hosted metadata 282/0 and lifecycle before all-files pre-commit found 35 unique formatting targets: 11 EOF targets plus 6 trailing-whitespace targets with one overlap (16 unique), and 19 additional Markdownlint targets, and found Gatus DL4006. The exact 36-path local packet is green: formatting is semantic-whitespace-only and idempotent, Gatus hadolint is GREEN, 12 Gatus tests pass, explicit-base metadata is 285/0 and links are 920/8,950/0. | **DRAFT PR 169 — CURRENT LOCAL CORRECTION SPEC/QUALITY/SECURITY APPROVED**. PR head `0eaa445a7a9820a8dd6289adacd7b900543443b0` has three commits. The PR-head hosted result is failed. The new 36-path correction and this Task delta are not committed or pushed; a hosted rerun containing them remains pending. |

### Actual baseline and current source matrix

| Surface | Actual evidence | Interpretation |
| --- | --- | --- |
| Git baseline | Baseline `dffc2ed8bc3bf4b2538b03884ad7ab5d7587375b`; branch `codex/home-dev-convergence-followup`; three pushed commits through `0eaa445a7a9820a8dd6289adacd7b900543443b0` | Draft PR 169 head is `0eaa445a7a9820a8dd6289adacd7b900543443b0`; not merged |
| Compose inventory at entry | 42 tracked root-included Compose sources, 140 unique services, 64 declared profiles and 261 profile-service memberships | Historical entry measurement, preserved for comparison |
| Current static Compose validation | Entry run: 65 registered selection cases, 293 aggregate selected-service checks and HOME 37; exit 0; later focused port corrections passed seven tests | The entry result retains its historical scope; current omitted-host dual-stack and IPv4-mapped IPv6 overlap semantics are established by the later correction/review |
| Current lifecycle | HOME 37, DEV 9, OPTIONAL 47, LAB 45, MIGRATE 2, REMOVE 0 | Canonical current judgment in m0021; no automatic activation or deletion |
| Current operations ownership | 50 typed service Guides own all 140 exact services across all 42 Compose sources; 50 complete Guide/Policy/Runbook triplets and 41 existing source-parent READMEs | Current public typed binding result; supersedes the historical 132-active/eight-draft narrative |
| Current version projection | 81 Compose repositories: 75 external and six local/custom | Derived Compose image projection, not all ecosystem dependencies |
| Current public metadata | 247 public environment keys; 94 public secret IDs; 69 root secret declarations and 70 distinct registered secret-file paths | Public schema only; values were not inspected or copied |
| Deployed private metadata boundary | Main deployed checkout remains at 93 IDs and is not read into this evidence packet | Post-merge same-root synchronization/provisioning remains pending |
| Read-only host snapshot | 12 logical CPUs, 31 GiB RAM, GTX 1060 6144 MiB; 38 running containers plus three completed init containers at observation | Point-in-time observation, not peak, growth, reboot or recovery proof |
| Runtime/source delta | `infra-pyroscope`, `infra-tempo`, `pushgateway` and `mailpit` were running outside the HOME 37 source selection | Pending transition assessment; no stop/restart or lifecycle reclassification |

### Fourteen-category drift matrix

| Category | Current disposition and evidence | Remaining uncertainty or boundary |
| --- | --- | --- |
| INFRA | A/R approve the exact 42-source, 140-service, 20-field inventory and current lifecycle ledger. | Optional/LAB traffic and data are not established by source declarations. |
| PROFILE | B approves exact vocabulary, membership, required HOME closure, reserved selectors and automation/lifecycle isolation. The later port-overlap blind spot is corrected and independently approved. | Profile selection is not access control or runtime health proof. |
| OPERATIONS | E approves current service purpose, commands, security, backup/restore, upgrade and recovery routing; the operations catalog passes in unit evidence. | Procedures marked planned were not executed. |
| TEMPLATES | D approves Stage 99 optional typed Guide binding and runtime-authority/link controls after three bypass corrections. | A schema PASS cannot prove service-specific prose accuracy without E review, which was performed separately. |
| README | E restored ten omitted storage README frontmatters/headings and corrected domain, component and root navigation/content. | Current coverage derives from typed bindings and existing paths, not prose row counts. |
| VERSION | C approves complete tracked Compose repository projection and fail-closed source discovery; 81/75/6 is byte stable. | Offline manager extraction does not cover every ecosystem dependency. |
| RENOVATE | C validates repository and global configs strictly; isolated mutation tests enforce ownership and a deterministic non-writing pin preview. | No networked Renovate update, PR or runtime pin change occurred. |
| DEPENDABOT | POL-0086 limits Dependabot to Storybook npm and tests reject stale directory/lock paths or Renovate overlap. | Other dependency families remain maintainer- or operator-reviewed as POL-0086 states. |
| ENV | F preserves exact 247-key public schema equality, classification, tracked-source consumption and file-safety rules. | Private values were neither read nor synchronized in this branch. |
| SECRETS | F stages 94 public IDs, replaces the stale Prometheus Vault grant with a manual least-privilege OpenBao contract and validates consumers/build inputs. | SEC-002 is unissued; synthetic fixture equality is not a usable credential or live acceptance. |
| SECURITY | Current docs and source distinguish OpenBao HOME from Vault MIGRATE custody and native OIDC from proxy-only services; hardening/static checks passed in their recorded scope. | Live authorization, target health, credential issuance and current enforcement remain unverified. |
| NETWORK | Source joins cover declared networks, ports and the corrected static-address map. HOME port checks now cover omitted-host dual-stack and IPv4-mapped IPv6 overlap semantics; seven focused tests pass. | Static port closure does not prove complete live isolation or future rootless compatibility. |
| DATA | E records per-state-owner backup/recovery boundaries, including Grafana's source-derived default SQLite state and storage engine procedures. | No new backup consistency, isolated restore, cold start or reboot rehearsal was executed. |
| CI | Earlier four-finding corrections remain approved. The pushed structure-only repair resolved the 25/24 metadata failure; the next hosted run passed metadata 282/0 and lifecycle before all-files pre-commit found the formatter/Gatus issues. The exact follow-up is locally green and independently SPEC/QUALITY/SECURITY APPROVED. | The PR-head hosted result is failed; the 36-path follow-up is not committed or pushed, so its hosted rerun remains pending. No validator relaxation was used. |

### Current documentation coverage

Coverage is derived from public `implementation_services` frontmatter in current
service Guides. Each binding maps an existing repository-relative Compose path to
nonempty exact service identities. All 140 identities are unique across 50 service
Guides and 42 Compose sources. Every mapped subject has current
`guide.md`, `policy.md` and `runbook.md`; every source parent has a README.
MinIO's standard and cluster Compose files intentionally share one package README,
so 42 source paths resolve to 41 unique parent README paths.

| Catalog group | Typed Guide artifacts | Services | Compose sources / parent READMEs | Current triplets |
| --- | --- | ---: | ---: | ---: |
| [Gateway](../../../05.operations/catalog/01-gateway/README.md) | GDE-0011, GDE-0013 | 2 | 2 / 2 | 2 / 2 |
| [Authentication](../../../05.operations/catalog/02-auth/README.md) | GDE-0014, GDE-0015 | 4 | 2 / 2 | 2 / 2 |
| [Security](../../../05.operations/catalog/03-security/README.md) | GDE-0016, GDE-0085 | 4 | 2 / 2 | 2 / 2 |
| [Data](../../../05.operations/catalog/04-data/README.md) | GDE-0017, 0018, 0019, 0020, 0022–0029, 0031, 0033, 0034, 0080 | 75 | 17 / 16 | 16 / 16 |
| [Messaging](../../../05.operations/catalog/05-messaging/README.md) | GDE-0036 | 9 | 1 / 1 | 1 / 1 |
| [Observability](../../../05.operations/catalog/06-observability/README.md) | GDE-0039–0041, 0043–0047, 0049, 0087 | 11 | 1 / 1 | 10 / 10 |
| [Workflow](../../../05.operations/catalog/07-workflow/README.md) | GDE-0050, GDE-0053 | 16 | 2 / 2 | 2 / 2 |
| [AI](../../../05.operations/catalog/08-ai/README.md) | GDE-0056, GDE-0057, GDE-0081 | 4 | 3 / 3 | 3 / 3 |
| [Tooling](../../../05.operations/catalog/09-tooling/README.md) | GDE-0061, 0062, 0065, 0066, 0069, 0082, 0083 | 10 | 7 / 7 | 7 / 7 |
| [Communication](../../../05.operations/catalog/10-communication/README.md) | GDE-0070, GDE-0084 | 2 | 2 / 2 | 2 / 2 |
| [Laboratory](../../../05.operations/catalog/11-laboratory/README.md) | GDE-0072, GDE-0073, GDE-0076 | 3 | 3 / 3 | 3 / 3 |
| **Total** | **50 typed Guides** | **140** | **42 / 41** | **50 / 50** |

### Version and dependency compliance

| Check | Actual result | Scope |
| --- | --- | --- |
| Derived projection check | exit 0; 81 repositories, 75 external, six local/custom | All tracked infrastructure Compose image repositories exactly once |
| C final tests | reviewer: 30 focused and 49 full PASS | Source discovery, ownership, updater mutation isolation and preview behavior |
| Official Renovate validation | repository strict exit 0; global strict exit 0 | Syntax and migration warnings; no update lookup or PR |
| Offline manager extraction | 117 Compose dependencies, 63 Dockerfile dependencies, two narrow custom dependencies; custom/Compose overlap empty | Retained because manager inputs did not change after extraction |
| Storybook npm audit | exit 0; zero known vulnerabilities | Lockfile-only audit, no dependency update |
| Installed Python environment audit | exit 0; 63 packages, zero known vulnerabilities; all five declared requirements satisfied | Actual temporary validation environment only |
| Fresh Python resolver audit | stopped before resolution because host `ensurepip` is unavailable | Prerequisite failure, not a vulnerability finding or fresh-resolution PASS |

### External evidence matrix

The detailed dated source assessment remains in
[m0021](../../../90.references/research/0002-agentic-engineering-research-pack/m0021-local-docker-service-consolidation.md)
and each component's linked Guide/Policy/Runbook. This matrix routes evidence;
it does not restate product facts or turn a source visit into runtime proof.

| Evidence family | Canonical repository route | Used for | Limit |
| --- | --- | --- | --- |
| Compose include, profiles, networking, interpolation, secrets; Engine security/rootless; NIST container guidance | m0021 framework sources and [POL-0078](../../../05.operations/catalog/00-workspace/0078-compose-profile-vocabulary/policy.md) | Profile union, dependency, path, network and security interpretation | Guidance does not authorize host migration or runtime mutation |
| Component deployment, security, persistence, backup, upgrade and license sources | m0021 retained-family tables and the 50 typed service Guide groups above | E service-specific procedures and R lifecycle decisions | Official availability is not tested restore or compatibility evidence |
| MinIO community maintenance state and storage alternatives | m0021 MinIO decision plus MinIO operations `GDE-0023` (superseded by GDE-0024) | Preserve HOME S3 while requiring a separately designed migration evaluation | No replacement, object migration or credential change is approved |
| Version managers and updater configuration | [POL-0086](../../../05.operations/catalog/00-workspace/0086-dependency-version-management/policy.md), [GDE-0086](../../../05.operations/catalog/00-workspace/0086-dependency-version-management/guide.md) and [Renovate Guide](../../../05.operations/catalog/09-tooling/0083-renovate/guide.md) | Compose/Dockerfile/custom-manager ownership and update review | No networked update or automatic deployment proof |
| Recovery and operating procedures | Per-component Guide/Policy/Runbook triplets in the coverage table | Planned, source-specific backup, restore, health and rollback boundaries | No procedure is recorded as executed unless separately dated evidence says so |

## Verification Evidence

### Read-only runtime and host evidence

The point-in-time host snapshot above observed 38 running containers and three
successful init containers. Four exact non-HOME instances were running:
`infra-pyroscope`, `infra-tempo`, `pushgateway` and `mailpit`. They are
pending transition assessment, not dormant. Selecting HOME does not stop them,
and no stop, restart, restore, deployment or other runtime mutation occurred.
There is no new live, reboot, cold-start, restore, sustained-load, peak-resource
or growth acceptance.

### Current source/static checks

| Check | Actual result | Boundary |
| --- | --- | --- |
| Entry serialized Compose validation | exit 0; 65 selections, aggregate 293, HOME 37 | Historical scope; later port regressions and final gates supersede its overlap coverage |
| Final secret prerequisite check | exit 0 | Public prerequisites only; private registry absent |
| Final secret dry run | exit 0; 94 rows | No generation, synchronization or secret mutation |
| Final version projection check | exit 0 | Derived Compose sources only |
| B final review | 29 focused PASS; prior 77 whole-module PASS retained | No runtime activation |
| C final review | 30 focused and 49 full PASS; two strict validators exit 0 | Offline extraction not rerun because inputs were unchanged |
| D final review | three exact witnesses, 28 runtime, 63 heading and 12 direct A PASS | Document/source contracts only |
| F final review | 30 focused PASS | No private value or credential action |
| R final review | 140 rows/unique services and ten comparisons approved | Source judgments, not traffic or recovery proof |
| E final reviews | storage, storage README integration, databases, applications, platform and root all approved | Scoped document evidence, no runtime acceptance |
| Compose discovery / replica Resources corrections | independently approved; operations 84, versions 50, baseline 31 and zero-depth discovery 3 tests PASS; catalog and 81-repository synchronization PASS | Covers both filename families including `infra/compose.yaml`; explicit replicas remain separate from per-container limits |
| Prometheus command correction | independently approved; corrected rule command passed all 12 mounted YAML files and reported 110 rules; exact three-document metadata 3/0, links, catalog and diff PASS | Separate config check stopped on absent staged `/run/secrets/openbao_token`; no reload, loaded-rule or target-UP proof |
| Published-port overlap correction | independently approved; seven focused tests PASS | Covers omitted-host dual-stack and IPv4-mapped IPv6 overlap semantics; static evidence only |
| Entrypoint mode correction | exact isolated-worktree `chmod g-w` changed Open WebUI/Gatus entrypoints from 0775 to 0755; focused 2/2 and integrated 50/50 PASS | Git index stayed 100755, original files stayed 0755/0555, and no source/index bytes changed |
| Local pre-PR changed check | exit 0; `/tmp/convergence-final-changed-gate-modefixed.log`; metadata `check-active` selected 449, violations 0 | No PR-base context caused the deliberate active-corpus substitution; changed-body heading ratchet was not exercised |
| Local pre-PR full check | exit 0; `/tmp/convergence-final-full-gate.log`; `check-contracts` passed | Contract validation does not apply the PR-range changed-body heading ratchet; no runtime deployment acceptance |
| First hosted required `validation-changed` | run 35474733788 / job 105981909050: **FAIL**; 25 findings in 24 files | Historical pushed-head failure; superseded by the pushed heading correction |
| Host committed-range reproduction | exit 1; selected 282, violations 25, legacy 0, overrides 0; `/tmp/convergence-hosted-metadata-repro.log` | Explicit baseline confirms repository defect, not runner failure |
| Corrected-head hosted run | run 35476114948 / job 105985535619: metadata selected 282/0 and lifecycle PASS; overall **FAIL** after 21m38s at all-files pre-commit | 35 unique formatting targets: 11 EOF targets plus 6 trailing-whitespace targets with one overlap (16 unique), and 19 additional Markdownlint targets, plus Gatus Dockerfile DL4006; `/tmp/convergence-hosted-corrected-head-failure.log` |
| All-files inspection and Markdown correction | 35 unique formatting targets: 11 EOF targets plus 6 trailing-whitespace targets with one overlap (16 unique), and 19 additional Markdownlint targets; pinned markdownlint-cli2 0.22.1 plus cached checks are idempotent on the second pass; whitespace-insensitive diff exit 0 | 17 prior-PR paths and 18 baseline-unchanged paths; semantic content preserved; `/tmp/convergence-hosted-lint-inspection.txt` |
| Gatus Dockerfile correction | official hadolint 2.14.0 checksum verified; DL4006 RED exit 1 to GREEN exit 0; 12 Gatus tests PASS | Builder change is limited to the `ash -eo pipefail` shell correction and two lines; no runtime action |
| Current explicit-base metadata | exit 0; selected 285, violations 0, legacy 0, overrides 0 | Includes the frozen local correction packet; not yet pushed |
| Storage heading correction | explicit-base selected 17, violations 0 | Heading-only; non-heading bytes preserved |
| Messaging/AD heading correction | explicit-base selected 7, violations 0 | Heading-only; non-heading bytes preserved |
| Combined corrected PR range | exit 0; selected 282, violations 0, legacy 0, overrides 0; `/tmp/convergence-pr-range-metadata-after-heading-fix.log` | Historical heading packet; subsequently pushed at `0eaa445a7a9820a8dd6289adacd7b900543443b0` |
| Corrected integration checks | operations catalog PASS; all-links 920 documents / 8,950 links / 0 failures | Catalog log: `/tmp/convergence-operations-catalog-after-heading-fix.log` |
| Task-only metadata/link/diff checks | metadata selected 1, violations 0; all-links 920 documents / 8,950 links / 0 failures; exact diff check PASS | Task consolidation only; registered gate results are recorded in separate rows |

The earlier combined 261-test run exited 1 because ten storage READMEs had lost
their complete frontmatter. The active metadata selector reported 444/0 because
untyped READMEs were outside its selection. The bounded repair restored baseline
frontmatter and required headings; the integration reviewer then passed exact
11-document metadata, contract, registry and diff checks. This corrects the
specific omission but does not turn the earlier failed whole run into a global
PASS. Those scoped repair checks do not replace the current hosted committed-range
metadata result.

Whole-branch review found four cross-surface issues and independently approved
all corrections. Discovery now covers Git-tracked
`infra/**/{compose,docker-compose}*.{yml,yaml}`, including zero-depth
`infra/compose.yaml`; operations 84, versions 50, baseline 31 and zero-depth
discovery three tests pass. The six source-family documents are corrected and
approved. Derived Resources now record Locust worker `deploy.replicas: 2`
beside per-container limits while preserving R-authored judgment cells. No
multiplied capacity or runtime claim is made.

The Prometheus correction runs rule globbing inside the container and passed 12
mounted YAML files / 110 rules. Its separate config check remains blocked by the
unprovisioned SEC-002 token; there was no reload or target-UP proof. Published-port
validation now covers omitted-host dual-stack and IPv4-mapped IPv6 overlap
semantics; seven focused tests pass. These are static/read-only results.

The final changed gate passed after three earlier non-PASS attempts retained for
traceability: initial index identity failure; a later exit-130 interruption; and
`/tmp/convergence-final-changed-gate-final.log` exit 1 because the isolated
checkout's Open WebUI/Gatus entrypoints were mode 0775. The Git index remained
100755 and originals remained 0755/0555. Authorized isolated-only
`chmod g-w` produced 0755 without changing source/index bytes; focused 2/2 and
integrated 50/50 checks passed. The final changed gate then exited 0, and the
registered full gate exited 0.

These two later local exits are limited evidence. Without PR-base context, the
changed runner deliberately substituted metadata `check-active`
(`ci_gate_runner.py` lines 451–459; log line 470 selected 449, violations 0).
The full gate's `check-contracts` route also does not apply the PR-range
changed-body heading ratchet. Required hosted
`validation-changed` run 35474733788 / job 105981909050 failed with 25
metadata findings across 24 files. The exact host reproduction was:

`TEMPLATE_GATE_BASE=dffc2ed8bc3bf4b2538b03884ad7ab5d7587375b /tmp/hy-home-validation-tools/bin/python3 scripts/validation/check-document-metadata.py --mode check-changed`

It exited 1 with selected 282, violations 25, legacy exceptions 0 and overrides
0; log: `/tmp/convergence-hosted-metadata-repro.log`. The affected set is 24 documents spanning AD-0005, storage and messaging.
This was a real document-structure defect, not a runner issue or validator false
positive. The correction changes heading structure only, preserves non-heading
bytes and does not change config or relax the validator. Storage explicit-base
metadata passes 17/0; messaging/AD passes 7/0; the combined PR range passes
282/0 with zero legacy exceptions and overrides. Operations catalog and all
links pass. Independent correction review is SPEC/QUALITY APPROVED with no
findings. That repair was committed and pushed as the third PR commit. Hosted run
35476114948 / job 105985535619 then passed metadata 282/0 and lifecycle before
its all-files pre-commit leaf failed: the formatter set contained 35 unique targets: 11 EOF targets plus 6 trailing-
whitespace targets with one overlap (16 unique), and 19 additional Markdownlint
targets, and the Gatus Dockerfile
triggered DL4006. This later result does not
invalidate the narrower local changed/full checks; it establishes that they did
not execute the required all-files leaf.

The exact follow-up contains those 35 formatting-hook outputs plus the Gatus
Dockerfile correction. Pinned markdownlint-cli2 0.22.1 and cached EOF/trailing-
whitespace checks are clean and idempotent on a second pass; whitespace-
insensitive diff exits 0, raw diff check exits 0, links pass 920/8,950/0 and
explicit-base metadata passes 285/0 with zero legacy exceptions/overrides.
MIG-0004 is the current sealed archive artifact and retains its required single
LF; frozen MIG-0001 through MIG-0003 were not changed. GDE-0086's fenced block
is indented under step 2 so its rendered list remains steps 1–6. Official
hadolint 2.14.0 was checksum verified and changed Gatus DL4006 from RED exit 1
to GREEN exit 0; 12 Gatus tests pass. Independent review approves the 35-file
formatter packet for SPEC/QUALITY/SECURITY and the Gatus correction for
QUALITY/SECURITY, with no findings. This Task delta, the new local correction commit, a separately approved push
and a hosted rerun containing that correction remain pending; the current PR-head
hosted result is failed.

## Review Evidence

The planning packet is approved. Independent final reviews approve A, B, C, D,
F and R. Independent E reviews approve storage, storage README integration,
databases, applications, platform and root. Earlier findings and interim states
remain useful correction history and are superseded as current status by these
same-scope final reviews.

The review loop exposed and corrected several evidence failures:

- Directory-valued metadata arguments selected four entries rather than the 81
  actual application files. The correction enumerated all 81 exact files and
  passed 81/0. Directory arguments are not recursive coverage evidence.
- Active metadata reported 444/0 while ten untyped storage READMEs were omitted.
  Registry common-six tests exposed the omission; exact baseline frontmatter and
  headings were restored, with no validator weakening.
- SEC-002 file equality involved the validator-known synthetic dummy fixture.
  It proves deterministic preservation only and is not a live or usable token.
- Source authority overrode prose assumptions: Grafana has no external database
  setting and therefore uses its current default SQLite state in `grafana-data`;
  Renovate remains DEV maintenance in the frozen ledger.
- Scoped reviews corrected stale Prometheus Vault guidance, native-OIDC versus
  proxy-auth statements, root onboarding, Kafka-only messaging, exact IP
  ownership, Registry exposure and storage recovery authority links. Later
  whole-branch review also found the three-document Prometheus wildcard command.
  Its correction passed 12 YAML files / 110 rules and is independently approved;
  the separate config check remains blocked by unprovisioned SEC-002.
- Public 94-ID staging remains separate from deployed main private 93-ID
  metadata. Same-root synchronization and credential provisioning wait until
  merge/main and their own authorization.

The pre-PR reviewed snapshot was SPEC/QUALITY/SECURITY APPROVED with no
findings. The 24-document metadata correction is independently SPEC/QUALITY
APPROVED and pushed. Its hosted rerun passed metadata and lifecycle, then exposed
the later all-files pre-commit findings. The exact 35-file formatting-hook packet is
independently SPEC/QUALITY/SECURITY APPROVED, including its whitespace-only diff,
GDE-0086 rendering and MIG-0004 line ending. The Gatus correction is independently
QUALITY/SECURITY APPROVED. The local correction remains uncommitted and unpushed. The current PR-head
hosted result is failed, and a rerun containing the correction has not occurred.

Repository quality standards make the 90% domain-code coverage target N/A for
this documentation, policy, infrastructure configuration and validation-script
change set because no application-domain code signal changed. The evidence is the
actual focused, negative and mutation test results recorded above; no unmeasured
80% or 90% percentage is claimed. The final PR report must preserve this N/A
rationale and the concrete test counts.

### Delivery status

| Delivery field | Current value | Evidence boundary |
| --- | --- | --- |
| Local pre-PR changed/full checks | **PASS WITH LIMITED SCOPE** | Changed used `check-active` (449/0) without PR-base context; full used `check-contracts`; neither exercised the PR-range changed-body heading ratchet |
| Hosted required `validation-changed` | **FAIL — LATER ALL-FILES CORRECTION PREPARED** | First failure was fixed and pushed. Run 35476114948 / job 105985535619 passed metadata 282/0 and lifecycle, then failed all-files pre-commit with 35 unique formatting targets: 11 EOF targets plus 6 trailing-whitespace targets with one overlap (16 unique), and 19 additional Markdownlint targets, plus Gatus DL4006 |
| Independent review | **PRE-PR, METADATA, FORMATTER AND GATUS PACKETS APPROVED** | Formatter: SPEC/QUALITY/SECURITY; Gatus: QUALITY/SECURITY; no findings. This Task factual delta and a hosted run containing the local packet remain pending |
| Logical commit(s) | **THREE COMMITS PUSHED; NEW CORRECTION PACKET UNCOMMITTED** | Implementation `8919696e8a65f47ccd830e577d80c781b810cbd3`; evidence `4ed7724ce83605fe5d8d1e553a52f367f45757cc`; current pushed head `0eaa445a7a9820a8dd6289adacd7b900543443b0`; the 36-path local packet has no commit identity yet |
| Push / PR | **DRAFT PR 169 OPEN; NEW LOCAL PACKET NOT PUSHED** | [PR 169](https://github.com/buenhyden/hy-home.docker/pull/169), three-commit head `0eaa445a7a9820a8dd6289adacd7b900543443b0`; no merge. Prior approval covered that push, not the new 36-path payload |
| Remote governance readback | **READ-ONLY COMPLETE** | `validation-changed` required from app 15368 with strict=true; approvals 0, code-owner reviews false, enforce-admins false; effective `/rules/branches/main` empty; CODEOWNERS routes to `@buenhyden` only |
| Hook/message preflight | **PASS** | Normal pre-commit hook passed for the implementation commit; explicit Commitizen validation passed; global ECC `core.hooksPath` has no commit-msg hook and no setting changed |
| Merge / deployment | **PENDING and unauthorized here** | No merge, private synchronization or runtime rollout |

## Commit Ledger

This Task begins from `dffc2ed8bc3bf4b2538b03884ad7ab5d7587375b` on
`codex/home-dev-convergence-followup`. Implementation commit
`8919696e8a65f47ccd830e577d80c781b810cbd3`
(`feat(operations): Converge HOME service governance`) contains 306 files and
309 changed pathnames because renames contribute multiple pathnames. Its normal
pre-commit hook and explicit Commitizen validation passed. Evidence commit
`4ed7724ce83605fe5d8d1e553a52f367f45757cc` records the three
Spec/Plan/Task paths. The reviewed 24-document metadata correction was committed
and pushed as the third commit; current PR head is
`0eaa445a7a9820a8dd6289adacd7b900543443b0`.

The first push request was rejected because the 306-file tracked payload targeted
the unverified `https://github.com/buenhyden/hy-home.docker.git` without
explicit trusted-user egress approval. The user then explicitly approved that
same target and branch, so the push proceeded and
[PR 169](https://github.com/buenhyden/hy-home.docker/pull/169) was created at
head `4ed7724ce83605fe5d8d1e553a52f367f45757cc`. Required CI failed as
recorded above. The 24-document heading-only correction was independently
SPEC/QUALITY APPROVED, committed and pushed at current head
`0eaa445a7a9820a8dd6289adacd7b900543443b0`. Its hosted run passed metadata and
lifecycle before the later all-files pre-commit failure. The exact 35-file
formatting plus Gatus correction is locally green and independently approved but
has no commit or push yet. The PR remains draft. No merge, repository-setting
change or runtime action occurred.
Historical PR evidence in Tasks 0001–0004 retains only its dated scope.

## Rulings

| Decision | Evidence | What could be wrong | Cost if wrong |
| --- | --- | --- | --- |
| Refresh SPEC-0180 in place and retain prior Tasks | Owner requires comparison with the existing package; the old Plan baseline differed from current main | Historical work may have regressed | Current audits/gates must rediscover drift; old PASS cannot stand in for current proof |
| Use SDD review/tracking with bounded parallel units | Owner requested the workflow and disjoint ownership | Hidden integration coupling may remain | Scoped rework in the isolated worktree; serialize shared owners and final gates |
| Keep routine repository changes inside the approved mission | Repository implementation is approved; runtime/protected state is not | A source change could cross a live boundary | Stop at runtime, secret value, data, remote and merge boundaries |
| Extend canonical owners and checks only for demonstrated gaps | Existing catalog, policy and version owners already exist | A passing owner can still have coverage blind spots | Add focused mutations to the current owner; avoid a competing registry or policy |
| Treat typed Guide bindings as navigation, not another registry | D's optional `implementation_services` field and A's global join cover 140 services | Bindings can drift after refactors | Existing catalog fails until sources and bindings agree |
| Keep core distinct from HOME | HOME is the named union of required profiles for 37 services | Required dependencies may change later | Revise Spec, POL-0078 and tests together |
| Use timestamp-optional Renovate fallback with manual review | Missing release timestamps otherwise block proposals indefinitely | An unknown-age release may be younger than seven days | Manual maturity review remains mandatory; no infrastructure automerge or deployment |
| Preserve dependency-audit distinctions | npm and installed Python audits are clean; fresh resolver lacked `ensurepip` | Installed packages may differ from a clean future resolution | Record the prerequisite failure, rerun when available and do not call it a PASS |
| Report domain coverage as N/A with actual tests | Quality standards permit N/A for docs/policy/infra configuration/validation-script changes with no domain-code signal; this branch has concrete negative/mutation/unit results | An unmeasured percentage could be mistaken for coverage evidence | Preserve N/A rationale and exact test counts in the final PR; do not invent an 80% or 90% result |
| Preserve current HOME S3 and evaluate MinIO migration separately | Current consumers/data remain; official community repository is archived/unmaintained | Continued use carries maintenance risk; alternatives may differ | Require compatibility, backup/restore, cutover and rollback evidence before any replacement |
| Preserve OpenBao HOME and Vault/Vault Agent MIGRATE custody | Current authority and legacy recovery material differ | Legacy templates/tokens/data may still be needed | Do not delete custody material or create duplicate active authority |
| Keep private values outside evidence | Confidentiality and value-preservation contract | A tool could interpolate or print protected values | Use public/value-free checks and record prerequisite blocks |
| Stage SEC-002 without live provisioning | Public contract exists; no issued token or loaded target is proven | Token, policy or scrape behavior may fail | Separate approval, provisioning, restart and measured UP evidence are required |
| Keep public 94-ID work separate from private 93-ID main state | Branch adds one manual contract; deployed main retains its prior registry | Premature rollout would lack the credential | After merge, use the canonical same-root sync/check flow; never copy values across roots |
| Treat synthetic SEC-002 as fixture evidence only | Equality check matched a known dummy fixture | It could be mistaken for a valid credential | Never claim issuance, usability or target recovery from the fixture |
| Treat directory metadata selection as nonrecursive | Application correction proved directory arguments selected four, while exact enumeration selected 81 | Future reports may again overstate selection | Enumerate actual files or use a validated recursive mode; report selected count |
| Treat untyped README omission as a coverage defect | 444/0 excluded ten READMEs with no frontmatter; common-six tests caught them | Active-only checks can hide removed metadata | Restore exact baseline metadata/headings and retain registry coverage checks |
| Let source/inventory win over prose | Compose shows Grafana default SQLite; frozen m0021 classifies Renovate DEV | A prose hint can misclassify state/lifecycle | Correct prose and keep source-backed lifecycle; do not mutate source to match a hint |
| Route root docs through the stable documentation index | Outside-docs direct numbered-stage links violate lifecycle routing | Readers take one extra hop | Link `docs/README.md` and name exact Stage 05 path/artifact ID in plain text |
| Treat host numbers as a snapshot | Single read-only observation | Idle use can understate peak demand or recovery cost | Keep peak/growth/reboot/restore acceptance open |
| Treat four non-HOME running containers as transition work | Exact names observed outside HOME 37 | Consumers or restart state may require them | Assess data and consumers before any authorized stop; no automatic cleanup |
| Preserve no-removal lifecycle result | All 140 judgments lack sufficient deletion evidence | Unknown optional/LAB data or consumers may exist | Preserve data/config until explicit evidence supports retirement |
| Keep profile selection distinct from access control | Official Compose semantics and current policy | A union may expose an unintended service | Enforce membership/ports and review security separately |
| Keep E corrections bounded and independently reviewed | Initial broad pass missed semantic and coverage defects | Cross-domain fixes can create new contradictions | Freeze exact scopes, perform same-scope rereview, then integrate |
| Treat snapshot approval, local correction and pushed-head CI separately | Pre-PR review approved its snapshot; the pushed metadata correction cleared hosted metadata/lifecycle; the later all-files packet is approved/green but unpushed | Local evidence does not change the pushed PR status | Commit and obtain separate push approval for the new payload, then require current-head hosted CI before merge consideration |
| Require explicit-base changed-body metadata evidence | Local changed substituted `check-active` (449/0) and local full used `check-contracts`; hosted/reproduced PR range found 25 rows in 24 documents; corrected explicit-base range passes 282/0 | Omitting the base can produce a valid but narrower PASS | Preserve the explicit baseline in correction evidence and do not relax heading contracts |
| Align standard Compose filename discovery across canonical owners | Corrected descriptor covers Git-tracked `infra/**/{compose,docker-compose}*.{yml,yaml}`, including `infra/compose.yaml`; six prose contracts align | A future source family could diverge across owners | Keep shared discovery and zero-depth regressions; update code and authority docs together |
| Record declared replicas beside per-container Resources | Approved derived cell records Locust worker replicas 2 beside per-container limits and preserves R-authored cells | Readers could still multiply or reinterpret limits as measured use | Keep explicit replicas separate from per-container limits and make no calculated capacity/runtime claim |
| Verify container-side Prometheus rule globbing | Approved `/bin/sh -c` command checked 12 YAML files / 110 rules | The config check remains blocked by absent staged SEC-002, and rule parsing does not prove loaded state or targets | Keep credential provisioning, reload and target-UP evidence separate; no runtime mutation is authorized |
| Treat omitted-host, dual-stack and mapped addresses as overlapping where they bind the same port | Approved correction covers wildcard/loopback, omitted-host dual-stack and IPv4-mapped IPv6 semantics; seven tests pass | Kernel/platform bind behavior can evolve | Preserve focused regressions and rerun Compose/baseline gates with network changes |
| Correct isolated entrypoint modes without source/index mutation | Final changed gate exposed 0775 modes only in the isolated checkout; index stayed 100755 and originals 0755/0555 | Treating the worktree mode as source drift could cause an unnecessary content/index change | Apply exact isolated-only `chmod g-w`, verify 2/2 focused and 50/50 integrated checks, and record no source/index byte change |
| Require explicit approval before remote tracked-payload transmission | Automatic review first rejected the 306-file push; the user then explicitly approved the disclosed origin/branch and PR 169 was created | Push approval does not approve merge, settings, runtime or a failing CI state | Preserve the approval scope, keep PR draft during corrections and require passing current-head CI before merge consideration |
| Traefik / Nginx | Traefik HOME; Nginx OPTIONAL alternative | A future cutover may need Nginx | Never co-select conflicting route/port authority; require cutover evidence |
| mng-db / Supabase / PostgreSQL HA | HOME management DB, OPTIONAL Supabase and LAB PostgreSQL HA serve different contracts | Data/identity/HA assumptions may be conflated | No consolidation without consumer, data and recovery proof |
| MinIO / SeaweedFS | MinIO HOME; SeaweedFS OPTIONAL; distributed MinIO LAB | S3/data compatibility is not automatic | Preserve objects/credentials and test migration separately |
| Prometheus / InfluxDB | Prometheus HOME; InfluxDB OPTIONAL | InfluxDB consumer/data evidence is incomplete | Preserve data; do not promote or remove from snapshot absence |
| Cassandra / CouchDB / MongoDB | All LAB, with no substitution or host-HA claim | Unknown data/client use may exist | Removal can lose data; promotion consumes unproven resources |
| Airflow / n8n | Both HOME for distinct automation contracts | Consolidation may lose schedules, credentials or retries | Retain both until workload and recovery evidence supports change |
| k6 / Locust | Both DEV-only explicit load generators | Target authorization and scripts are unverified | Do not broad-start; preserve test assets |
| OpenTofu / Terrakube | Both DEV and on demand | State/history and Docker-socket exposure differ | No HOME promotion or removal without exact evidence |
| Mailpit / Stalwart | Mailpit DEV capture; Stalwart OPTIONAL mail server | Test mail and real mailbox state differ | Avoid exposure or mailbox loss |

## Deferred Items

Closure (2026-09-24): PR #169 merged on 2026-09-20 with its last hosted `validation-changed` run failing; later main runs pass (for example #250). The draft and unpushed states above are historical. Private registry synchronization closed in Task 0008 (#243). Cold start, reboot, sustained and peak resource measurement, isolated restore rehearsals, OpenBao recovery custody, SEC-002 provisioning and runtime acceptance, and the non-HOME running-container assessment move to [SPEC-0181](../../0181-home-residual-operations/spec.md).

- PR 169 is draft at `0eaa445a7a9820a8dd6289adacd7b900543443b0`.
  The exact 35-file formatting-hook plus Gatus Dockerfile packet is locally green and
  independently approved but uncommitted/unpushed. Its commit identity, separate
  push approval and a hosted rerun containing the correction remain required before any merge
  consideration.
- Broad HOME cold start, reboot recovery, sustained/peak CPU/RAM/GPU, growth and
  isolated stateful restore rehearsals remain unverified.
- OpenBao recovery custody and SEC-002 provisioning/runtime acceptance require
  separate protected actions and evidence.
- The four exact non-HOME running containers require an approved transition
  assessment before any stop or source-to-runtime convergence action.
- Private 94-ID synchronization is deferred until merge/main and an authorized
  same-root operation. No private value is part of this Task.
