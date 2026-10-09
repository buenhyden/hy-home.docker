---
title: "Stage 05 Format Refresh Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "specs"
artifact_id: "SPEC-0227-TSK-0001"
parent_ids:
- "SPEC-0227-PLAN-0001"
created: "2026-10-10"
---

# Stage 05 Format Refresh Task

## Objective

Bring every tracked Stage 05 guide, policy and runbook to its current
template, Korean prose and current operating facts, and keep it there.

## Inputs and Authorization

The owner's prompt 16 asks for every tracked Stage 05 guide, policy and
runbook in its type's current form and language, the Guide/Policy/Runbook
ownership split, `implementation_services` checked against Compose, the
listed priority subjects first, commits in the order contract and validator,
documents, links, final verification, and a report of any file not processed;
completed historical Tasks are not changed. Base `1f552ac78`.

## Work Log

### W1 Validator

`ordered_sections` and `nonempty_sections` were added to the profile schema
and to the guide, policy and runbook profiles. `_registered_section_findings`
reports `body-heading-order`, `body-section-empty` (HTML comments are not
content; fenced blocks are) and `body-heading-repeated`. Seven unit tests
cover the order, the repeated child, comments, fenced headings, profiles
without the flags and the registry wiring; the full
`tests/lib/document_governance` suite (775 tests) passed on that commit in a
clean checkout. Run directly on `origin/main`,
the rule failed all 230 files: 476 empty sections, 464 self-repeating
headings, 4 missing required headings.

### W2 Batches

Nine documentation agents each owned whole subjects (a subject's guide,
policy and runbook together), worked from one written conversion guide, ran
no Git command and edited only their files. Each batch was checked again
(section rule, markdownlint, content-loss comparison) before its own commit.
One agent reported four of its files as absent; they existed and were
returned and converted. Two agents added a second Guide binding for a
service (`surrealdb`, `seaweedfs-table-bucket`); both were removed so each
service keeps one Guide.

Facts corrected while restructuring, against current Compose and configs:

| Subject | Correction |
| --- | --- |
| 0013 Traefik runbook | `sso-errors` handles only 403 (middleware `status: ["403"]`), as the guide already said |
| 0019 OpenSearch | Exporter-plugin mismatch claim replaced: the Dockerfile builds the plugin at the base release; compatibility marked 미검증 |
| 0024 SeaweedFS | `seaweedfs-table-bucket` described with its owner GDE-0094; version literals removed |
| 0028 management database | Six services, including `mng-pg-monitor-provision`, and the MNG monitor accounts |
| 0029 Supabase | Kong, analytics and Supavisor host ports bind to `127.0.0.1` |
| 0030 data hardening runbook | Removed profile `valkey-cluster` replaced by `dev-data` |
| 0040 Alloy | The two configs were described as identical; `config.home.alloy` adds the authenticated quality-metric receiver and remote write |
| 0041 Grafana, 0048 retention | LAB dashboards live in `labs/dashboards/` and are not provisioned |
| 0045 Prometheus | DEV/MNG labels, rendered DEV targets, `PROMETHEUS_DEV_DATA_EXPECTED`, full `/etc/prometheus` tmpfs options, node-exporter listener and `extra_hosts` |
| 0048 retention policy | A verification `rg` that never matched replaced by a retention-key check |
| 0056, 0057 runbooks | An unclosed code fence that swallowed sections repaired |
| 0096 k8s integration | LAB-only PostgreSQL HA ports removed from the HOME contract |
| 0100 DEV database | DEV exporters, the `dev_pg_monitor` and `devmonitor` accounts and their secrets |
| Several | Runtime patch versions in prose replaced by Compose links |

### W3 Links and Bindings

The full link check found two links to renamed anchors (GDE-0079 to
RUN-0050 `#steps`, POL-0049 to POL-0096 `#controls`); both were repointed.
One completed SPEC-0198 Task in the archive still links to `#controls`; as a
historical record it was left unchanged.

### W4 Full List

All 230 tracked files are processed; no file is left out:

| Subject | Guide | Policy | Runbook | Commit |
| --- | --- | --- | --- | --- |
| 0001 common-optimizations-template-exceptions | — | yes | — | `511c454e7` |
| 0002 developer-environment | yes | — | — | `511c454e7` |
| 0003 env-key-comparison | yes | — | — | `511c454e7` |
| 0004 harness-agent-first-engineering | yes | yes | yes | `511c454e7` |
| 0006 infrastructure-optimization-governance | — | yes | — | `511c454e7` |
| 0008 new-service-onboarding | yes | — | — | `511c454e7` |
| 0009 release-management | — | — | yes | `511c454e7` |
| 0010 sensitive-env-vars-comparison | yes | — | — | `511c454e7` |
| 0011 nginx | yes | yes | yes | `475d60ea7` |
| 0012 edge-routing-stack | yes | — | — | `475d60ea7` |
| 0013 traefik | yes | yes | yes | `475d60ea7` |
| 0014 keycloak | yes | yes | yes | `475d60ea7` |
| 0015 oauth2-proxy | yes | yes | yes | `475d60ea7` |
| 0019 opensearch | yes | yes | yes | `09b8d0b90` |
| 0021 backup-and-restore | yes | yes | yes | `09b8d0b90` |
| 0022 valkey-cluster | yes | yes | yes | `703a2f394` |
| 0024 seaweedfs | yes | yes | yes | `09b8d0b90` |
| 0025 cassandra | yes | yes | yes | `703a2f394` |
| 0026 couchdb | yes | yes | yes | `703a2f394` |
| 0027 mongodb | yes | yes | yes | `703a2f394` |
| 0028 management-database | yes | yes | yes | `09b8d0b90` |
| 0029 supabase | yes | yes | yes | `09b8d0b90` |
| 0030 data-optimization-hardening | yes | yes | yes | `703a2f394` |
| 0031 postgresql-cluster | yes | yes | yes | `703a2f394` |
| 0032 postgresql-logical-upgrade-restore-rehearsal | — | — | yes | `703a2f394` |
| 0033 neo4j | yes | yes | yes | `703a2f394` |
| 0034 qdrant | yes | yes | yes | `703a2f394` |
| 0035 storage-exhaustion | — | — | yes | `703a2f394` |
| 0036 kafka | yes | yes | yes | `d8920a7fa` |
| 0037 messaging-optimization-hardening | yes | yes | yes | `d8920a7fa` |
| 0039 alertmanager | yes | yes | yes | `f786ae6b7` |
| 0040 alloy | yes | yes | yes | `f786ae6b7` |
| 0041 grafana | yes | yes | yes | `f786ae6b7` |
| 0042 lgtm-stack | yes | — | — | `f786ae6b7` |
| 0043 loki | yes | yes | yes | `f786ae6b7` |
| 0044 observability-optimization-hardening | yes | yes | yes | `f786ae6b7` |
| 0045 prometheus | yes | yes | yes | `d8920a7fa` |
| 0046 pushgateway | yes | yes | yes | `d8920a7fa` |
| 0047 pyroscope | yes | yes | yes | `f786ae6b7` |
| 0048 telemetry-retention | — | yes | — | `f786ae6b7` |
| 0049 tempo | yes | yes | yes | `d8920a7fa` |
| 0050 airflow | yes | yes | yes | `974d5c518` |
| 0051 airflow-dag-lifecycle | yes | — | — | `768916819` |
| 0052 airflow-dag-lifecycle | — | yes | — | `768916819` |
| 0053 n8n | yes | yes | yes | `974d5c518` |
| 0054 workflow-optimization-hardening | yes | yes | yes | `974d5c518` |
| 0055 gpu-recovery | — | — | yes | `768916819` |
| 0056 ollama | yes | yes | yes | `974d5c518` |
| 0057 open-webui | yes | yes | yes | `974d5c518` |
| 0058 ai-optimization-hardening | yes | yes | yes | `974d5c518` |
| 0059 rag-workflow | yes | — | — | `768916819` |
| 0060 iac-deployment | — | yes | — | `511c454e7` |
| 0061 k6 | yes | yes | yes | `a772eb92c` |
| 0062 locust | yes | yes | yes | `a772eb92c` |
| 0063 tooling-optimization-hardening | yes | yes | yes | `a772eb92c` |
| 0064 performance-testing | yes | yes | yes | `a772eb92c` |
| 0065 registry | yes | yes | yes | `a772eb92c` |
| 0066 sonarqube | yes | yes | yes | `a772eb92c` |
| 0068 terraform | yes | yes | yes | `a772eb92c` |
| 0069 terrakube | yes | yes | yes | `a772eb92c` |
| 0070 mail | yes | yes | yes | `d8920a7fa` |
| 0072 dozzle | yes | yes | yes | `d8920a7fa` |
| 0073 open-notebook | yes | yes | yes | `974d5c518` |
| 0074 laboratory-optimization-hardening | yes | yes | yes | `a772eb92c` |
| 0076 redisinsight | yes | yes | yes | `09b8d0b90` |
| 0077 ip-address-management | yes | yes | yes | `a772eb92c` |
| 0078 compose-profile-vocabulary | — | yes | — | `511c454e7` |
| 0079 application-auth-integration | yes | yes | — | `511c454e7` |
| 0080 surrealdb | yes | yes | yes | `703a2f394` |
| 0081 comfyui | yes | yes | yes | `974d5c518` |
| 0082 opentofu | yes | yes | yes | `a772eb92c` |
| 0083 renovate | yes | yes | yes | `a772eb92c` |
| 0084 mailpit | yes | yes | yes | `d8920a7fa` |
| 0085 openbao | yes | yes | yes | `475d60ea7` |
| 0086 dependency-version-management | yes | yes | yes | `511c454e7` |
| 0087 gatus | yes | yes | yes | `475d60ea7` |
| 0088 mlflow | yes | yes | yes | `707a0bb45` |
| 0089 jupyterlab | yes | yes | yes | `707a0bb45` |
| 0090 dbt | yes | yes | yes | `707a0bb45` |
| 0091 crawl4ai | yes | yes | yes | `974d5c518` |
| 0092 wiremock | yes | yes | yes | `707a0bb45` |
| 0093 pact-broker | yes | yes | yes | `707a0bb45` |
| 0094 lakehouse | yes | yes | yes | `707a0bb45` |
| 0095 conftest | yes | yes | yes | `707a0bb45` |
| 0096 k8s-integration | yes | yes | yes | `707a0bb45` |
| 0097 superset | yes | yes | yes | `707a0bb45` |
| 0098 cold-start-and-reboot | — | — | yes | `511c454e7` |
| 0099 system-operations | yes | — | yes | `511c454e7` |
| 0100 development-database | yes | yes | yes | `09b8d0b90` |
| 0101 storybook | yes | yes | yes | `707a0bb45` |

Comparing every file with `origin/main` found 201 removed fenced blocks,
links or inline tokens. 175 are still present in another document of the same
subject (moved to their owner and linked). The other 26 were checked one by
one: reformatted blocks whose commands remain (inline in Common Checks or
in the runbook), the removed Usage Type values, headings referred to by their
old names, the LAB-only PostgreSQL ports, the never-matching `rg`, and the
duplicate text the unclosed fence had swallowed.

### Review

An independent review found no critical or important issue and nineteen
minor ones; every fact correction it checked against `infra/` and `labs/`
held. Resolved in `b91bcd7f7` (validator) and the following documentation
commit: the empty-section scan now follows the same CommonMark fence rules
as heading extraction, keeps text after a closing comment and skips the
order check for sealed shapes, with five more tests (twelve in all); four
runbooks pointed "위 격리…" at a plan that is now below; five filler lead-in
sentences were removed; six runbooks had Traceability under Rollback and
Escalation; eight kept an old Evidence heading (renamed `증거 기록`, or dropped
where it was the only one); a dropped evidence bullet was restored in
RUN-0056 and RUN-0057; English prose in POL-0029 and RUN-0056/0057 was
translated; and POL-0045 now links the retention default instead of
repeating it. Left as they are, with reasons: the runbook profile's
optional old-template H2s are unused but still referenced by the
operations catalog code, so removing them is a separate change; spacing
and mixed endings in RUN-0021 and RUN-0053, and the command-less Common
Checks in GDE-0028, predate this change; the English history blockquote in
GDE-0040 is quoted evidence. The batch count is ten commits, not nine: the
four returned files have their own commit.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Validator | 1 | W1 | Seven unit tests; governance suite (775); rule over `origin/main` | `c012032e9` | PASS | W1 Validator | accepted |
| Batches | 2, 3 | W2 | Section rule, markdownlint, loss comparison per batch | `c012032e9..d8920a7fa` (ten batch commits and `c87867aec`) | PASS | W2 Batches | accepted |
| Links and bindings | 4 | W3 | `check-document-links.py --mode all`; `check-operations-catalog.py` | `567eafecc` | PASS | W3 Links and Bindings | accepted |
| Full list | 2, 3 | W4 | Rule over 230 files; metadata `check-changed` (230 selected, 0 violations); loss audit | `567eafecc` | PASS | W4 Full List | accepted |
| Review | 5 | W5 | Independent review; fixes | `deaf151f3` | PASS | Review | accepted |
| Changed gate | 5 | W5 | `run-ci-gate.py --profile changed --local-only`, base `1f552ac78`; hardening; operations catalog | `deaf151f3` | PASS | Review and Completion | accepted |
| Staged style check | 5 | W5 | `run-ci-precommit.sh --mode local-staged` over `1f552ac78..HEAD` | `deaf151f3` | PASS | Review and Completion | accepted |
| Remote candidate | 5 | W5 | `candidate-quality` run 37976670835, base `1f552ac78` | `af5cea75f` | PASS | Review and Completion | accepted |

## Review and Completion

The changed gate, the hardening baseline, the operations catalog and the
staged style check passed on `deaf151f3`. Run 37976670835 passed on head
`af5cea75f` and PR #403 merged as `39126d5bf` (recorded with SPEC-0228).
Complete.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
