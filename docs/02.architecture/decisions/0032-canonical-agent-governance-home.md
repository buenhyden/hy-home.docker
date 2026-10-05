---
title: "Canonical Agent Governance Home"
version: "1.0.2"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "architecture"
artifact_id: "ADR-0032"
parent_ids:
- "AD-0027"
supersedes:
- "ADR-0029"
created: "2026-09-06"
---

# ADR-0032: Canonical Agent Governance Home

## Context

ADR-0029 separated the responsibilities of common norms, document machine
contracts, executors, and native adapters. While keeping that separation, the
user explicitly requested moving the common canonical source to
repository-owned `.agents/` and removing the old governance directory. The
current non-authoritative, empty-directory contract is the target of this
change.

This document supersedes the location/loading decision based on the explicit
user relocation request and the Task's independent design review. The Task
owns the remaining items of implementation verification. Human signatures,
approval timestamps, and native execution results are not backfilled.

### Compliance

The approval basis is the explicit relocation request in the current
conversation and the actual independent review recorded in the Task. No
commit, remote, operations, secret, or global setting changes are approved.
Protected-path writes are performed only through the normal approval procedure
with a bounded target and action.

### Follow-up

Change only ADR-0029's reciprocal supersession metadata and the lawful
lifecycle metadata immediately before initial preservation. The decision body
is not modified and stays preserved in Stage 98. Already-frozen ADR-0027 and
other records are left as they are. Required static checks, protected-path
approval status, and pending native verification continue to be tracked in the
current Task.

## Decision

### Decision

### Decision Drivers

- Keep exactly one canonical source per shared meaning and changeable list.
- Align Codex's repository skill discovery with the actual owning path.
- Preserve native format and per-provider support differences, and existing
  approval/security boundaries.
- Review and dispose of the content of 77 originals while keeping the
  identifiers of 14 roles and 23 skills.
- Document validation, CI, and the wiki must not miss the hidden canonical
  source.
- Do not modify archived Tasks or already-frozen bodies for the sake of path
  cleanup.

### Decision

Adopt the following location model after an independent design review.

- `.agents/governance/` owns common policy and the normative SDLC.
- `.agents/roles/` owns the existing responsibility/input-output/permission/
  delegation contracts.
- `.agents/skills/<name>/SKILL.md` owns the actual invocable procedures.
  Existing metadata is preserved inside the standard native envelope, and both
  providers' explicit invocation controls apply.
- The governance/providers Registry owns the common provider mapping. Tool-
  specific authored descriptions use `.claude/provider.md`/`.codex/provider.md`,
  and generated READMEs and role/skill adapters use the existing native
  locations. Generated output is not an input canonical source.
- Stage 99 is the sole machine authority for document path, profile, ID,
  section, lifecycle, traceability, and template. Existing scripts own
  execution verification and conversion.
- Keep the inventory responsibility of six suites, two profiles, workflow
  execution configuration, and the script manifest. This relocation does not
  grant execution approval to access operational input.
- Detailed Requirement, Architecture, Spec/Plan/Task, and Operations documents
  stay in the existing docs. Stage 90 is non-authoritative evidence, and Stage
  98 is the preserved record per ADR-0031. Git history is the recovery/identity
  basis for preserved bodies, not a substitute for Task bodies.
- Remove the old common directory from current reading, generation, linking,
  and fallback targets. Old paths in frozen records and regression-test
  strings are classified as history/negative examples.

## Alternatives

### Alternatives

### Options Considered

| Alternative | Effect and cost | Judgment |
| --- | --- | --- |
| Move the reviewed canonical source to `.agents` | Aligns native skill discovery with ownership; requires converting all consumers | Fits the request's goal |
| Keep the canonical source at the current document Stage | Preserves existing explicit reads; misses the requested canonical location/discovery goal | Not adopted for this request |
| Full duplication or root symlink | Duplicate authority, format mixing, output/input cycle and boundary risk | Not adopted |

## Consequences

- Common skills become native discovery targets, so controls that block
  implicit execution expansion must be checked separately from actual
  discovery results. Metadata is not an approval gate.
- Canonical input is not a generation/quarantine/deletion target. Unexpected
  files are preserved and cause failure.
- Path changes also change the Registry/schema/template/validator/test and
  relative links together.
- New plugins, servers, memory, `.codex/config.toml`, or additional common
  directories are not created for formal symmetry. Model, permission, and hook
  trust are not changed.
- Local syntax/contract success, native discovery, invocation, permission
  enforcement, and actual hook receipt are separate pieces of evidence.

## Related Documents

### Traceability

- [Agent governance requirement](../../01.requirements/0024-agent-governance-standardization.md)
- [Canonical adapter architecture](../descriptions/0027-agent-governance-canonical-adapter.md)
- Predecessor authority decision
- Preserved-record decision
- [Owning specification](../../98.archive/completed/03.specs/0173-governance-qa-surface-convergence/spec.md)
- [Current plan](../../98.archive/completed/03.specs/0173-governance-qa-surface-convergence/plan.md)
