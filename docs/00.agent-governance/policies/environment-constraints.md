---
title: Environment Constraints
type: governance/policy
layer: agentic
owner: "@buenhyden"
---

# Environment Constraints

Detailed execution boundaries, verification rules, and Graphify behaviors for the `hy-home.docker` workspace.

## 1. Hard Constraints

- `docs/01` to `docs/99` are read-only by default; modify only with explicit user instruction.
- Active stage artifacts belong only under `docs/01.requirements`, `docs/02.architecture`, `docs/03.specs`, `docs/05.operations`, `docs/90.references`, and `docs/99.templates`.
- `_workspace` is an ignored repo-support staging surface, not an active stage.
  Only `_workspace/README.md` and `_workspace/repo-support/README.md` are
  approved tracked contract files. Runtime artifacts must stay under
  `_workspace/repo-support/` and must not contain diagnostics dumps, local logs,
  raw logs, auth files, tokens, credentials, private keys, shell history, or
  secret values.
- Run checks listed by the active rules and primary scope before declaring completion.
- Most-specific in-scope instruction file wins when multiple repository instructions apply.
- System, developer, and direct user instructions always override repository instruction files.
- Use in-place refactors only; do not create parallel replacement files for canonical docs.
- Never write plaintext secrets; use Docker Secrets or `secrets/` mounts.
- Session bootstrap is repository-context inspection only. It must not run
  `docker ps`, probe live services, or imply runtime readiness.
- Agent-output evaluation is deterministic and model-free. Use only synthetic
  fixture content; never load diagnostics dumps, local logs, auth files,
  credentials, tokens, secret values, or shell history as evaluation input.

## 2. Infrastructure Constraints

- **Networking**: all inter-service traffic MUST use `infra_net`. Direct
  external exposure is PROHIBITED except via authorized gateways.
- **Storage**: use named volumes following the `[Service]-[Data]-[Volume]`
  convention.
- **Security**: `no-new-privileges: true` is mandatory for all containers. Use
  Docker Secrets for production credentials.
- **Container build review**: for Dockerfile or image-build changes, review
  multi-stage builds, pinned base image tags or digests, `.dockerignore`
  hygiene, non-root users, health checks, layer ordering, and secret-free image
  layers. These are manual review expectations unless a repository validator
  already enforces the specific rule.
- **Compose review**: for Compose changes, review profile behavior, service
  health checks, restart policy, named volumes, resource limits where supported,
  network segmentation, and localhost-only port binding where external exposure
  is not intended.
- **Pruning**: `docker system prune` requires explicit user consent. Never run
  it without one.

### 2.1 Approved Runtime Mutation Protocol

When the user approves live runtime or Docker mutation, the agent still needs a
concrete target before changing service state. The co-located Task evidence must
record:

- target service or Compose file,
- intended runtime action and approval source,
- pre-check command and result,
- rollback or recovery command,
- post-check command and result,
- reason any live mutation was skipped.

Approval without a concrete runtime target authorizes planning and validation
only; it does not require starting, stopping, rebuilding, or recreating services.

### 2.2 Approved Secrets Work Protocol

When the user approves secrets work, agents may inspect repository-local secret
metadata needed for the task, but secret values remain non-output data.
Permitted evidence includes counts, IDs, file paths, key names, registry
metadata, rotation status, and command success/failure. Prohibited evidence
includes plaintext values, private keys, token-bearing logs, shell history, and
full secret file bodies.

Secret value reads, writes, or rotations require a concrete target and task
evidence that records the redaction boundary, validation command, and rollback
or recovery path. Do not commit, print, summarize, or quote secret values.

## 3. Verification

- For infra changes, run `bash scripts/validation/validate-docker-compose.sh`.
- For governance/root changes, run `python3 scripts/validation/check-document-links.py --mode traceability` and link/stale-reference checks for edited files.
- Direct `pre-commit run` execution by agents is prohibited. At an approved
  final QA gate, use only
  `scripts/validation/run-agent-precommit-all-files.sh` from an initially clean
  linked worktree with a tracked co-located Task and reviewed allowed prefixes.
  Record its concise result and review hook-managed edits; never auto-reset,
  checkout, clean, or write task evidence from the wrapper.
- Wrapper evidence covers only Git-visible, non-ignored repository paths.
  Ignored or outside-repository writes are not observed, and the wrapper is not
  a process or filesystem sandbox.
- Run the completion checklist in `docs/00.agent-governance/policies/task-checklists.md` before declaring done.
- Provider surface `--write` is allowed once only after an approved canonical
  Stage 00 or Provider Registry change. Ordinary postflight and CI use
  `scripts/operations/sync-provider-surfaces.sh --check`; hooks and validation
  commands must not regenerate provider surfaces implicitly. A reported
  quarantine is a nonzero cleanup handoff, not successful regeneration; follow
  the exact-path procedure in `docs/00.agent-governance/providers/README.md`
  before rerunning write and check.
- Repository script-reference validation is bounded to 4,096 scanned surfaces,
  8,192 discovery entries, 16 MiB per regular file, and 64 MiB in aggregate.
  These validator-owned ceilings are immutable contract safety limits; a limit
  failure is value-free and requires an explicit validator review rather than
  a caller override.

## 4. Graphify

This project has a graphify knowledge graph at `graphify-out/`.

- Before architecture or codebase answers, read `graphify-out/GRAPH_REPORT.md`.
- If `graphify-out/wiki/index.md` exists, prefer it over raw-file browsing.
- Use Graphify as a navigation aid only when corpus health is clean.
- If Graphify output includes `volumes/`, gitlink/submodule content, minified/generated artifacts, meaningless god nodes, or unrelated cross-root inferred edges, treat it as advisory only.
- Corroborate architecture and codebase conclusions against tracked source files, `docs/00.agent-governance/`, and active stage docs.
- After modifying code files, run `graphify update .` when the CLI is available; if `graphify` is unavailable, report that graph refresh was skipped.

## Related Documents

- `../README.md`
- `agentic.md`
- `github-governance.md`
- `quality-standards.md`
