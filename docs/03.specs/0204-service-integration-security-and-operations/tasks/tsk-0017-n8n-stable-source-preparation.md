---
title: "n8n Stable Source Preparation Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-16"
layer: "specs"
artifact_id: "SPEC-0204-TSK-0017"
parent_ids:
- "SPEC-0204-PLAN-0001"
created: "2026-10-16"
---

# n8n Stable Source Preparation Task

## Overview

### Objective

Prepare the confirmed n8n stable source candidate under INFRA-P2, preserving
historical SEC01 evidence and the separate P05 safety writer. Source preparation
and current public metadata do not accept the entire image audit, a native
workflow, a HOME deployment, migration or recovery.

## Inputs and Authorization

The direct 2026-10-16 infrastructure request authorizes ROOT stable-version
source changes, tests, documentation and matching current evidence. The
coordinator accepted the independent prechange review before this work unit.
The source checkout is `/tmp/hyhome-infra-spec0204` on
`feature/spec-0204-workflow-safety`; the controller records its actual base HEAD.
The implementer owns n8n Compose, both Dockerfiles, OpsflowSmtp package/lock,
workflow version regressions, generated version projection, SEC01 metadata,
n8n version documentation and this Task. The P05 writer separately owns
transport/tests, workflow generation, SQL safety, Task0018 and the Plan.
No completed Task, LAB source, live secret, runtime deployment, migration or
production data is changed. Source rollback is an owning logical revert;
image rollback cannot undo a database migration.

## Work Log

### W71 stable source preparation

Official GitHub latest and npm latest return n8n 2.43.6, published
2026-10-15T07:26:03Z, and the Docker Hub stable/latest tags match its exact
n8n and runner indexes. The historical requested 2.43.5 exists but is no longer
latest. n8n 2.43.6 uses n8n-workflow 2.43.4; the custom node peer/dev lock must
match that API before compiling. Preserve unsigned metadata as unsigned.

The initial RED command was `rtk env PYTHONPATH=/tmp/hyhome-infra-audit-python
python3 -m unittest tests.validation.test_workflow_version_bundle.WorkflowVersionBundleTests.test_n8n_main_worker_runners_and_both_builds_align
tests.validation.test_workflow_version_bundle.WorkflowVersionBundleTests.test_opsflow_package_matches_upstream_workflow_api`.
It exited 1 with two expected version mismatches (2.42.7 and 2.42.3).

The frozen source binding is
`cd628778fccbd13e04e73c6bf8fbabb750bf1062177af078889939270894fbcc`
across sixteen n8n build/COPY and local unit inputs. `update-ledger.json`
owns this binding; `build-inputs.json` now records both Dockerfile variants and
package/lock/TypeScript inputs. It excludes independent P05 SQL/provisioning
acceptance, which Task0018 records. No image was pulled or built. All new custom
image digests remain unknown; signature/full-image SBOM/native/HOME/migration/
backup/restore remain NOT_RUN. Four n8n service rows carry fresh independent
stable/digest facts; other rows have no new target or security acceptance.

The official npm lock refresh removed thirty obsolete transitive entries
(185 to 155 locked packages). A no-script, no-bin-links local `npm ci` installed
136 platform-applicable packages. The existing `npm run test:coverage` initially
failed with exit 127 because that install deliberately creates no `tsc` shim.
Its build script now calls the compiler via Node, matching the Docker recipe.
Rerun passed 27 tests: lines97.38%, branches95.12%, functions88.24%. This uses
host Node 26.10.0 and in-memory SMTP doubles, not the new n8n image. Official npm
audit for the full and production-only lock each exited 0 with zero advisories;
this is not a scan of upstream n8n or the complete custom image.

The ROOT supplier continuation reuses the existing release authority: 92 bounded
metadata-only requests, thirteen vendor-channel interpretations and 111 existing
service-to-supplier references. Initial 403/404 results and successful fallbacks
remain recorded. GitHub latest non-prerelease is only a candidate unless the
vendor stable channel is separately proved. The current ledger's old runtime,
support, signature, scan and migration fields retain their separate scope.

The final focused source/evidence suite ran 36 tests: 34 passed and two native
tests were skipped, exit 0. The earlier 92-test run had five source/ledger mismatch failures while
metadata had not yet been refreshed; the fresh 36-test suite includes and passes
all those affected assertions. Public-example Compose quiet render and service
selection passed, selecting exactly the four n8n roles. Projection check passed
(91 repositories), and the generated diff changes only the ROOT n8n source.

The required canonical static helper exited 2: 11 PASS, 0 FAIL, 4 BLOCKED, 2 NOT_RUN.
Its external-absolute-path input graph blocked dependent Compose checks; YAML,
shell lint and owned fixture cleanup passed. The separate scoped public render
does not erase that incomplete helper. Initial six-path document metadata
exited 1 with 148 findings: new Task initial status and a duplicate Plan table
were corrected; historical archive fallback findings were included in the fresh validation.
No archive was edited. After correcting new Tasks to draft and keeping one unique
Work Unit table, the authoritative `load_spec_packages` reader passed all 36
packages, exit 0. The subsequent scoped metadata command selected all seven
changed documents including the Spec amendment and exited 0 with zero violations,
legacy exceptions or transition overrides. It covers the initial six paths and
resolves their earlier document metadata failure. Independent final review and
exact-head registered delivery gates remain separate.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Version regression RED | 2 | W71 | Atomic image and custom-node API versions | Existing 2.42.7/2.42.3 source; two expected failures; exit 1 | FAIL | W71 stable source preparation | required | - |
| Version regression GREEN | 2 | W71 | Atomic image and custom-node API versions | Current stable source; focused 36-test run includes exact bundle/API checks; exit 0 | PASS | W71 stable source preparation | required | Version regression RED |
| Source binding RED | 2 | W71 | Current source binding and historical acceptance separation | Missing source_binding; one expected KeyError; exit 1 | ERROR | W71 stable source preparation | required | - |
| Source binding GREEN | 2 | W71 | Current source binding and historical acceptance separation | Sixteen-file binding; focused 36-test run; exit 0 | PASS | W71 stable source preparation | required | Source binding RED |
| ROOT supplier map RED | 2 | W71 | Current supplier references resolve | Missing root_official_refresh; one expected KeyError; exit 1 | ERROR | W71 stable source preparation | required | - |
| ROOT supplier map GREEN | 2 | W71 | Current supplier references resolve |92 official observations and 111 mapped services; focused 36-test run; exit 0 | PASS | W71 stable source preparation | required | ROOT supplier map RED |
| Package coverage RED | 2 | W71 | Compile and 80-percent custom-node coverage | No-bin-links install; missing tsc shim; exit 127 | FAIL | W71 stable source preparation | required | - |
| Package coverage GREEN | 2 | W71 | Compile and 80-percent custom-node coverage | Explicit Node compiler;27 tests and 97.38/95.12/88.24 percent; exit 0 | PASS | W71 stable source preparation | required | Package coverage RED |
| Public Compose and projection | 2 | W71 | Static source render and image projection | Public example env; four n8n roles; projection current; exit 0 | PASS | W71 stable source preparation | required | - |
| Canonical helper | 2 | W71 | Required infrastructure static helper | External-absolute-path;11PASS/0FAIL/4BLOCKED/2NOT_RUN; exit2 | NOT_RUN | W71 stable source preparation | required | - |
| Initial document metadata | 2 | W71 | Six-path document metadata | Initial Task/Plan defects and archive fallback;148 findings; exit 1 | FAIL | W71 stable source preparation | required | - |
| Corrected document metadata | 2 | W71 | Six-path document metadata | Seven paths including the initial six; zero violations/exceptions/overrides; exit 0 | PASS | W71 stable source preparation | required | Initial document metadata |
| Native and recovery | 2 | W71 | New exact images and isolated feature/recovery acceptance | No new build/native/HOME/restore receipt | NOT_RUN | W71 stable source preparation | optional | - |

## Criterion Acceptance

Criterion 2 retains its existing durable acceptance owner in Task0001. W71
provides supporting source evidence and does not create a duplicate acceptance row.

## Review and Completion

The current Plan owns criterion routing. This continuation does not rewrite
prior Task acceptance. Independent final source/security review and exact-head
gates remain pending. Full ROOT supplier, advisory, signature, SBOM and recovery
coverage remains incomplete; a four-service version preparation is no substitute.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [SEC01 prior Task](tsk-0009-sec01-stable-security-integration.md)
- [P05 prior Task](tsk-0013-p05-n8n-outbox-notifier.md)
