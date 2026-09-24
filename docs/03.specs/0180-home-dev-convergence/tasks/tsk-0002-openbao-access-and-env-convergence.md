---
title: "OpenBao Access and Private Schema Convergence"
version: "0.1.2"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-09-24"
layer: "specs"
artifact_id: "SPEC-0180-TSK-0002"
parent_ids:
- "SPEC-0180"
- "SPEC-0180-PLAN-0001"
created: "2026-09-19"
---

# OpenBao Access and Private Schema Convergence

## Objective

Complete the owner-approved OpenBao bootstrap and native Keycloak OIDC operator
access, document official research and credential/recovery requirements, then
align private/public environment and secret-metadata key sets to actual consumers.
This follows [Task 0001](tsk-0001-home-dev-convergence.md) under the existing
[Spec](../spec.md) and [Plan](../plan.md).

## Inputs

The owner approved bootstrap, temporary protected recovery custody, unchanged
import of the two existing Docker Secrets, and Keycloak OIDC administration.
The owner separately approved the exact loopback-only legacy recovery/recreation
and the exact limited operator policy. The owner confirmed a successful human
OIDC login. Later instructions require pruning unused keys from both private and
public schema pairs after OpenBao completion; earlier unknown-row preservation
is superseded only for that scoped reconciliation. Private values remain private.

## Work Log

- Prior PR #167 was merged externally at `43e547e95`; this agent did not merge it.
  Continue on `codex/openbao-bootstrap-access` from that repaired baseline.
- Initial server was uninitialized/sealed; Agent RoleID, SecretID and outputs
  were absent. Initialized with three Shamir shares, threshold two; custody
  directory 0700 and files 0600. Existing Vault migration data was ruled out by
  the owner. Imported the two existing Docker Secret values without modification.
- Renderer uses exact two-path read policy, one-use ten-minute SecretID and a
  24-hour periodic renewable token. Agent-only stop/start delivered credentials;
  values rendered byte-identically with 0600 permissions.
- Initial root was revoked before a human administrative identity existed. This
  was a sequencing error: current generate-root APIs require authentication.
  Official research identified the deprecated listener-gated recovery alternative.
- Automatic approval review rejected the first recovery recreation as lacking
  exact approval. The owner then explicitly approved loopback-only recovery and
  same-image/same-volume recreation, unseal and removal of the temporary listener.
- Temporary 127.0.0.1:18200 listener enabled the legacy API only inside the
  container; main listener explicitly kept the legacy endpoint disabled. Quorum
  recovery preserved the same cluster and volumes. One response-decoding failure
  required another recovery attempt; the exact superseded root was identified by
  its sole accessor record and matching attempt timestamp, then revoked. A broad
  cleanup was first rejected; the narrowed, independently identified single-token
  cleanup passed automatic approval review.
- Removed the auxiliary listener immediately after root recovery, recreated only
  OpenBao and unsealed the same cluster. Ordinary legacy endpoint returned 405;
  the auxiliary port no longer accepted connections. No restore or deletion ran.
- Automatic approval review rejected broad operator rights. Owner explicitly
  approved two-secret read/update, renderer SecretID issuance, Raft snapshot read
  and authenticated quorum root recovery. No secret deletion, wildcard secret
  access, policy editing or auth-method editing was granted.
- Created confidential Keycloak client `home-openbao` in `hy-home.realm`, exact
  UI/CLI callbacks, S256 PKCE, groups claim, and `/openbao-admins` membership for
  existing user `hyunyoun`. Native OpenBao role `home-admin` binds that exact group
  to `hy-home-operator`; token TTL 1 hour, max TTL 4 hours. Issuer CA is verified;
  client secret was transmitted internally without terminal output or staging.
- Owner confirmed OIDC login. Token metadata confirmed identity binding and only
  `default` plus `hy-home-operator`. Ten-path allow/deny matrix, non-root snapshot
  reading and authenticated quorum attempt start/cancel passed. Test tokens were
  revoked. A fresh snapshot was saved; rescue root revoke was confirmed by 403.
  Agent renewal and rendering still passed afterward.

- Applied explicit metadata pruning after independent review and protected backup.
  Both env schemas now contain 246 consumed keys; both registries contain 91 IDs
  (23 env inputs). Removed 99 private env assignments, 17 private registry rows
  and 16 unused public registry rows. Retained assignment bytes and private value/
  date cells match the backup; both private modes remain 0600 and Git-ignored.
  All 98 other secret files retain the same inventory, size, mode and timestamp.
  The post-apply prune check reports zero changes.

## Verification Evidence

| Check | Result |
| --- | --- |
| Protected init persistence and failure handling | Exclusive 0600 creation; overwrite/symlink rejection; no root revoke on failed verification or backup persistence |
| OpenBao identity | Same initialized cluster; unsealed after each bounded restart |
| Renderer | Exact read scope; unrelated/admin paths denied; two outputs byte-identical and 0600; SecretID consumed |
| OIDC | Trusted discovery, exact callback/client/S256 contract; real owner login succeeded; server-side policy/identity evidence |
| Operator policy | Ten-path allow/deny matrix passed; no root policy |
| Authenticated recovery | Non-root start/cancel passed, threshold two, no shares submitted in acceptance test |
| Backup | Initial, pre-OIDC and post-OIDC snapshots saved protected; archive structure checked, isolated restoration untested |
| Root lifecycle | Initial, superseded recovery and final rescue roots revoked; final lookup rejected (403) |
| Agent continuity | Actual renewal and post-root-revocation rendering passed |
| Private/public schema equality | 246 env keys and 91 registry IDs match; retained values/dates unchanged; prune check exit 0 |
| Metadata sync regression | 15 tests pass, including strict prune and legacy preserving behavior; Bash syntax and Ruff checks pass |
| Public Compose rendering | 64 selections, 261 service renderings pass in isolated public-only worktree |
| Final focused checks | Metadata selected=9, violations=0; 11 Markdown files clean; staged Gitleaks clean; diff check clean |
| Secret file preservation | 98-file inventory unchanged; private metadata modes 0600 and ignored |

An initial post-unseal request and first KV write were rejected while services
became ready; metadata checks proved no partial secret write before bounded
retry. A new authenticated API response used a data envelope; the initial
acceptance check stopped before mutation, then passed after correctly unwrapping
that envelope. Failures are retained as evidence, not counted as successful runs.

## Review Evidence

Independent security review required loopback-only exposure, preserved image and
mount identity, protected snapshots, exact ACLs, real OIDC acceptance and proof
of authenticated recovery before revoking the final root. Those runtime gates
passed. Independent final OpenBao specification and quality/security review
approved the public scope with no findings. Independent prune review approved
implementation and exact consumer inventories, with one non-blocking status-label
wording note (`values=preserved` means retained values). The isolated public-snapshot `changed` profile passed (exit 0). Final legacy-mode
compatibility and evidence-text adjustments passed focused tests (15), Ruff,
Bash syntax, metadata and Markdown checks separately; the gate snapshot preceded
those final adjustments. The final two-document review passed without findings.

## Commit Ledger

Prior convergence commits and PR #167 are already in main. Follow-up source and
operational evidence are delivered on `codex/openbao-bootstrap-access`; Git owns
commit IDs. The owner-authorized follow-up targets a Draft PR in
`buenhyden/hy-home.docker`, with branch push and PR creation only. The branch did
not exist remotely before delivery; recovery uses normal follow-up commits.
Authenticated main protection readback requires `validation-changed`, zero
approving reviews and no enforced CODEOWNERS approval. All touched ownership
routes resolve to `@buenhyden`. Hosted checks remain pending delivery.
No force push, merge, broad rollout or remote-setting change is authorized.

## Rulings

The latest explicit owner decisions authorize only the named runtime, identity
and private-schema changes. No secret value, token, key, client secret or raw
runtime log may enter committed evidence. Recovery custody location was handed
to the owner privately; offline separation and backup retention remain required.

## Deferred Items

Closure (2026-09-24): PR #168 merged on 2026-09-19 with its last hosted `validation-changed` run failing, which closes the pending hosted checks below; later main runs pass. Offline custody of the recovery shares and snapshots, isolated snapshot restore, broader HOME runtime acceptance and host reboot move to [SPEC-0181](../../0181-home-residual-operations/spec.md).

Owner must move recovery shares and snapshots to offline protected custody.
Isolated snapshot restoration, broader HOME runtime acceptance and host reboot
remain unverified. Hosted PR checks remain pending; no overall mission completion
is claimed.
