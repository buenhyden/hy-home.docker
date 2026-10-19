---
title: "n8n Stable Source Preparation Task"
version: "0.1.1"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-20"
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

The initial source-only frozen binding was
`cd628778fccbd13e04e73c6bf8fbabb750bf1062177af078889939270894fbcc`
across sixteen n8n build/COPY and local unit inputs. `update-ledger.json`
owns this binding; `build-inputs.json` now records both Dockerfile variants and
package/lock/TypeScript inputs. It excludes independent P05 SQL/provisioning
acceptance, which Task0018 records. At that initial source-only check no image was pulled or built; the later
isolated receipts below supersede only that build/module-loading scope. At that
point all new custom image digests remained unknown; signature/full-image SBOM/native/HOME/migration/
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

### Coupled source commit and current base — 2026-10-16

The coordinator approved one coupled source delivery for W71 (stable n8n
artifact), W72 (DEV CONNECT admission) and W73 (notification safety), together
with their exact tests, binding metadata, Plan and both new Tasks. The stable
custom artifact includes the corrected six-field lease consumer, while its
SQL migration, notifier graph and interface tests must agree. Committing only
partial shared Plan/Task references or stale image-input bindings would create
an invalid intermediate candidate. This source unit does not combine or infer
the separate native n8n/HOME/complete-recovery acceptances.

The explicit approved staging manifest contained exactly 46 paths: 42 tracked
modifications and four new files. It excluded LAB runtime, private inputs,
node_modules and temporary fixtures. The first normal commit attempt exited 1
on four Markdown MD012 double-blank-line findings in Plan/GDE/POL/RUN0053;
JSON/YAML, Ruff, Dockerfile and secret hooks passed. Only those four blank lines
were corrected, explicitly re-staged, and the same normal commit succeeded,
exit 0, with no hook bypass: `34c0319c3e3c512e1d0de2a5a8113648c635ca5d`.

The checkout was clean. Fresh `rtk git fetch origin main` returned
`5a88c7937bf427021f2fd0441e04b1011ecd28a9`; the clean owned branch rebased
without conflict, exit 0. Its actual coupled source commit is now
`8306839bb377228f76881cadaeb1ebe0f14656b5`. W71, W72 and W73 all reference this
same actual source commit; no other worktree was reset, stashed or cleaned.
The post-rebase checkout was clean and no push, PR or merge occurred.

`shutil.which('graphify')` returned no executable, so graph refresh is SKIPPED;
no installation, forced generation or stale graph authority claim is made.
Affected final gates will run once against the final source after the separate
CI policy integration; pre-rebase tests are not relabeled as final-head or
hosted CI evidence. The separate blocked image-native/HOME/recovery lanes
remain visible.

### Exact isolated image build and native peer correction — 2026-10-16

The authorized isolated build of the committed source at
`8306839bb377228f76881cadaeb1ebe0f14656b5` produced image
`sha256:22991d699454d44ae806ea525aea22c329cf7b1432b457c8820ff22c2e8eb304`,
binding `cd628778fccbd13e04e73c6bf8fbabb750bf1062177af078889939270894fbcc`.
Build exit0/234.116s did not prove runtime loading: actual n8n
`PackageDirectoryLoader` failed with `MODULE_NOT_FOUND: n8n-workflow`, exit1.
The pruned package lives under `/opt`, outside the base framework's ordinary
module ancestry. This confirmed production failure is retained in
`verification.json#/n8n_source_preparation`; it is not an accepted image.

The minimal correction adds the fixed base framework path
`NODE_PATH=/usr/local/lib/node_modules/n8n/node_modules` in both Dockerfiles.
It installs no second framework copy and keeps development dependencies pruned.
Both builds now instantiate the actual compiled `OpsflowSmtp` class and assert
its name and `NodeConnectionTypes.Main` API after checking n8n's version.
The focused regression command was `rtk proxy python3 -m unittest
tests.validation.test_workflow_version_bundle.WorkflowVersionBundleTests.test_pruned_custom_node_uses_pinned_base_framework_and_loads_at_build -v`:
RED two Dockerfile failures exit1, then GREEN one test exit0.

The corrected complete sixteen-file binding is
`03892eb1a9a485b454e48c8222ecebc116d67a846560bf97fb8a783e5f6d8985`.
Before the fix commit, `git write-tree` recorded immutable candidate tree
`f511528aba724372aa0ed61b7b3c2e271d2d6942`, parent
`64434387a86b4edb65d4583ee449785eb6ec1276`. The context contained only its
32 regular tracked n8n files; ignored files and symlinks were rejected.
The existing default builder received `--platform linux/amd64 --resource
memory=2g --resource cpu-period=100000 --resource cpu-quota=100000 --load`.
One build, fifteen minutes, eight GiB disk growth and six GiB host available
memory were the stop bounds. Requested stage controls were accepted, but their
actual cgroup enforcement and daemon pull overhead remain unobserved.
The cached build passed exit0/28.177s, minimum available memory11781218304bytes,
maximum observed Docker disk growth7589888bytes, no budget stop.

The unique corrected tag is `hy-home/sec01-n8n:2.43.6-opsflow-03892eb1a9a4`,
image ID `sha256:1fda18a541144ae5519ac97bcaffa4e24fad0e71d424606d230464bec8fce153`.
The actual pinned `PackageDirectoryLoader` passed exit0/4.545s under the
production image ENV: n8n2.43.6, n8n-workflow2.43.4, the same base peer,
compiled execute/Main API, immutable bridge and CJK/emoji font artifacts.
The synthetic container used `--network none --read-only --cpus 1 --memory 1g
--memory-swap 1g --pids-limit 128 --cap-drop ALL --security-opt
no-new-privileges=true`; only owned64MiB tmpfs at `/tmp` and
`/home/node/.n8n` were writable. It used no ports, host mounts or production
entrypoint. Exact container
`2bda571aa4712e1517527f26529c9a85715c6f7878d5a1423ac67f3dc2ff79ad`
was absent after automatic cleanup. A first temporary smoke-script newline
syntax error exited1/1.586s and was retained separately, then corrected without
changing the image or assertions. Source, build and native command/result
receipts are summarized durably in the existing SEC01 JSON owners.

This accepts isolated image compilation and actual package loading only.
The worker variant has the same source guard but was not separately built.
Full n8n workflow/queue/runner execution, full-image vulnerability scan,
signature/provenance verification, HOME upgrade, combined backup/restore and
runtime clock/quiescence proof remain NOT_RUN or BLOCKED in their owners.

### ROOT official release metadata continuation — 2026-10-16

The controller granted a separate writer lease limited to the existing
`release-lookups.json` and `update-ledger.json` after independent review of
proposal SHA256
`6ecff30f3bfc5a0bb5a31613c091441eee4e140e731adf69530549c5bdef2a33`.
The original 92 requests, including failed API attempts and successful official
fallbacks, remain exact historical evidence. Thirteen bounded primary followup
observations produce 105 total observations and dated assessments for all 111
current ROOT service identities. The classification is 101 stable RELEASE fact
rows, 6 component/image-mapping rows, 1 verified vendor image snapshot,1 verified
publisher alias with a source-provenance gap and 2 internal build-provenance rows.

An official correct-product repository's latest published full non-draft,
non-prerelease release establishes a stable RELEASE fact. This current narrow
interpretation supersedes the earlier generic candidate-only label for those
products. Explicit vendor channels, calendar/LTS and wrapper/component splits
remain separate. The source writer refreshed only latest_version/channel/
checked_at/release_url on 82 unambiguous rows and archived their prior four
fields under the existing root refresh owner. Actual field changes comprise 43
version values,27 channel values,28 URLs and82 timestamps. This does not choose
new target pins or reuse old image/security/native signatures for new releases.

Independent direct comparison against the protected public before snapshot
verified every source/target/digest/security/native/deployment field unchanged
across 111 rows. Only the release lookup's dated refresh / 13 observations and the
ledger's dated assessments/four release fields changed. The current n8n 16-file
image source binding remains
`03892eb1a9a485b454e48c8222ecebc116d67a846560bf97fb8a783e5f6d8985`.
The frozen metadata file SHAs are release-lookups
`1d8a6a543edc4c003d35df35090277731872d9c5a606fefb4d26959de8ff6f36`
and update-ledger
`845f23be15d78da61c659d29903782cc41058ed9e671c6224520108aad6178f2`.
No LAB, Compose, Dockerfile, package, frozen native fixture or deployment input
was changed by this metadata continuation.

Jupyter's dated/source-SHA/latest aliases now resolve to the same observed
manifest; the remaining platform/config/signature/custom-build gates are stated
explicitly. PostgreSQL 18 support end 2030-11-14 and security references are
component facts and do not claim the complete custom Timescale image lifecycle
or a clean installed-image vulnerability scan. Internal Storybook images still
need owner build provenance. The legacy historical 92-map count remains preserved;
the nested dated refresh explicitly records the current 105 total.

The source writer executed
`rtk proxy python3 -m unittest tests.lib.supply_chain.test_update_gates tests.validation.test_workflow_version_bundle.WorkflowVersionBundleTests -v`:
35 PASS, exit 0, 5.693 seconds. The supply-chain policy check passed 5 external
contracts / 13 cases; the two-file diff check passed. The protected invariance
receipt is `/tmp/hyhome-root-release-join-invariance-20261016.json`, SHA256
`9a593591cb6447292ad99bb1375daef3e4f6a4898e7a1cd9608a8c4157040f74`;
independent field comparison reproduced its preservation result.

The actual latest-version gate remains not ready, exit 2. Its 111 rows report
39 latest-unresolved,16 latest-mismatch,29 fresh-lookup,12 stable-channel and11
primary-reference diagnostics; these sets may overlap. The dated component
assessments must be read alongside the gate's legacy top-level release fields.
There are no missing or unexpected service identities, no deployed promotion
and no external acceptance claim. Exact report
`/tmp/hyhome-root-release-join-latest-gate-20261016.json`, SHA256
`0ea128ba26aee7abf1fdb15eef46f394e7f6822d8d1d9299412336e9c87798d3`.
The gate was not weakened or made green by assigning untested targets. Remaining
artifact selection, OCI/platform, applicability/support, signatures, SBOM,
compatibility, native/HOME and recovery decisions need their own evidence.

### Runner port aliases and deprecated runner switch — 2026-10-20

The v22 execution prompt §8.3 asks whether the `N8N_BROKER_PORT` and
`N8N_TASK_RUNNER_PORT` aliases move the real listeners. They did not. The
aliases set the runner `N8N_RUNNERS_TASK_BROKER_URI`, both `expose` lists and
the worker and runner healthchecks, but nothing set the listener variables, so
any non-default value would have pointed the runners and healthchecks at a
port nobody listened on.

The [task runner variables](https://docs.n8n.io/hosting/configuration/environment-variables/task-runners/)
name the listeners `N8N_RUNNERS_BROKER_PORT` (n8n, default 5679) and
`N8N_RUNNERS_LAUNCHER_HEALTH_CHECK_PORT` (launcher, default 5680), and mark
`N8N_RUNNERS_ENABLED` deprecated from 2.0. The running HOME `n8n` and
`n8n-worker` (2.41.6) both log `N8N_RUNNERS_ENABLED -> Remove this
environment variable; it is no longer needed.`

The change sets `N8N_RUNNERS_BROKER_PORT: ${N8N_BROKER_PORT:-5679}` in the
shared n8n environment, sets
`N8N_RUNNERS_LAUNCHER_HEALTH_CHECK_PORT: ${N8N_TASK_RUNNER_PORT:-5680}` on both
runners and removes `N8N_RUNNERS_ENABLED`. `N8N_RUNNERS_TASK_TIMEOUT: 300`
stays explicit; 2.41.6 warns that its default will drop to 60, and no
`N8N_RUNNER_TASK_TIMEOUT` remains. Default values render unchanged.

- RED: the new `test_n8n_port_aliases_move_the_listeners_they_advertise`
  renders the four combinations of 5679/15679 and 5680/15680 and failed all
  four with `KeyError: 'N8N_RUNNERS_BROKER_PORT'`; the existing timeout test
  failed on `N8N_RUNNERS_ENABLED`. GREEN after the change.
- `docker compose --env-file .env.example --profile workflow-n8n config` with
  15679/15680 renders both listener variables and the matching URIs.
- Affected suites: 157 OK, 30 opt-in skipped.
- Isolated runtime, 2026-10-20, internal network, synthetic token, tmpfs data,
  cached `hyhome/n8n:2.41.6-local` and `n8nio/runners:2.41.6`: with
  `N8N_RUNNERS_BROKER_PORT=15679` the broker answered `/healthz` on 15679 and
  refused 5679; with `N8N_RUNNERS_LAUNCHER_HEALTH_CHECK_PORT=15680` the
  launcher logged its health server on 15680, answered there and refused
  5680. No `N8N_RUNNERS_ENABLED` warning without the variable. Cleanup left 0
  containers and 0 networks. The first main attempt used the project
  entrypoint, which stops without the HOME secrets; the rerun started
  `n8n start` directly. The declared 2.43.6 images were not cached and were
  not used.

On the owner's 2026-10-20 instruction the W74 fixture
`tests/validation/_opsflow_native_fixture.py` also stops passing
`N8N_RUNNERS_ENABLED=true`; TSK-0019 records the consequence for its frozen
source review.

The custom-node bind was reviewed the same day. `n8n-data` is mounted at
`/home/node/.n8n`, so the `COPY ./custom` in both Dockerfiles is hidden at run
time and the bind is the only way tracked `custom/` reaches n8n. HOME main and
worker had it read-write, and the folder holds only `.gitkeep`;
`N8N_CUSTOM_EXTENSIONS` is unset, so n8n loads `~/.n8n/custom`. A read-write
bind let the container write code into the tracked folder that n8n would load
on the next start. Both binds are now `:ro`. The Opsflow package is not
affected: it lives at `/opt/hyhome/n8n-custom/opsflow` and the entrypoint links
it under `~/.n8n/nodes/node_modules`. `test_n8n_outbox_contract` and
`test_opsflow_native_boundaries` failed on the old source (RED) and pass now;
the n8n, Opsflow native, runtime, Compose and workflow-contract suites give
245 OK, 31 opt-in skipped. The Dockerfile `COPY ./custom` stays because the
image build ledger records it; it is dead at run time.

HOME still runs 2.41.6 against the declared 2.43.6, and its image has no
Opsflow bridge (`/opt/hyhome/n8n-custom` is absent). RUN-0053 stops HOME
application until an isolated Code-node and DB-upgrade check and an
independent backup with the same encryption key exist.

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
| Native peer loading RED | 2 | W71 | Actual pinned PackageDirectoryLoader | Original cd628 image; missing framework peer; exit1 and cleanupPASS | FAIL | Exact isolated image build and native peer correction — 2026-10-16 | required | - |
| Native peer loading GREEN | 2 | W71 | Actual pinned PackageDirectoryLoader | Corrected03892 image; core2.43.6/framework2.43.4; exit0/4.545s and cleanupPASS | PASS | Exact isolated image build and native peer correction — 2026-10-16 | required | Native peer loading RED |
| Isolated corrected build | 2 | W71 | Exact Git candidate image build | Treef511528; image1fda18; exit0/28.177s; budgets respected | PASS | Exact isolated image build and native peer correction — 2026-10-16 | required | - |
| ROOT release metadata join | 2 | W71 | Fresh official product release facts and exact service join |105 observations;111 assessments;82 release-only updates;35 source tests PASS | PASS | ROOT official release metadata continuation — 2026-10-16 | required | - |
| ROOT metadata preservation | 2 | W71 | Source target and security evidence remain scoped | Independent 111-row comparison; original 92 observations and n8n 03892 binding preserved | PASS | ROOT official release metadata continuation — 2026-10-16 | required | - |
| Current latest artifact target gate | 2 | W71 | Latest target and release readiness | Actual gate exit 2 ready false; unresolved/mismatch/applicability decisions remain | FAIL | ROOT official release metadata continuation — 2026-10-16 | required | - |
| Native and recovery | 2 | W71 | Complete workflow and HOME recovery acceptance | Isolated module smoke does not prove workflow/queue/runner/HOME/restore | NOT_RUN | Exact isolated image build and native peer correction — 2026-10-16 | optional | - |

## Criterion Acceptance

Criterion 2 retains its existing durable acceptance owner in Task0001. W71
provides supporting source evidence and does not create a duplicate acceptance row.

## Review and Completion

The current Plan owns criterion routing. This continuation does not rewrite
prior Task acceptance. Independent final source/security review and exact-head
gates remain pending. Current ROOT release research is joined above. Exact image/advisory/support,
signature, SBOM, compatibility and recovery coverage remains incomplete; neither
release metadata nor the earlier four-service version preparation accepts it.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [SEC01 prior Task](tsk-0009-sec01-stable-security-integration.md)
- [P05 prior Task](tsk-0013-p05-n8n-outbox-notifier.md)
