# Supply-Chain Network Approvals

## Purpose

Hold the written operator approvals that two supply-chain scripts require
before they perform outbound network access. This file is the approval surface
itself, not a description of one: the scripts read it directly and refuse to
run when the approval line they need is absent.

## Current State

**No approval is on file.** Both scripts fail closed.

## Scope

| Script                                                   | Required line, exactly                  | Grants                                                                                              |
| -------------------------------------------------------- | --------------------------------------- | --------------------------------------------------------------------------------------------------- |
| `scripts/security/seed-grype-db-cache.sh`                | `Grype DB network approval: confirmed`  | one bridged-network Grype vulnerability-database update; every other step stays on `--network none` |
| `scripts/security/verify-sample-service-supply-chain.sh` | `Scorecard network approval: confirmed` | one OpenSSF Scorecard call                                                                          |

Each line must appear on a line of its own, with no leading or trailing
characters: the scripts match it with `grep -Fqx`.

## Usage

To grant an approval, add the exact line from the table above to the
**Approvals** section below, and record who approved it and when in the same
commit message. To withdraw one, delete the line.

## Approvals

<!-- Add approval lines here, one per line, exactly as written in the table. -->

## Why This File Exists

Both scripts previously read their approval from
`docs/04.execution/tasks/2026-07-23-security-supply-chain-runtime-closure.md`
and `docs/04.execution/tasks/2026-07-19-security-supply-chain-remediation.md`.
Commit `65e994f3` moved those documents out of Stage 04 when that stage was
removed from the taxonomy, and `9ef889b5` removed the last copy of either
approval line. Neither string survived anywhere in the tracked corpus, so both
scripts stopped at their first policy check with
`seed-contract-surface-missing` and
`policy-task-or-cosign-config-boundary-missing` — failures that named a missing
contract surface rather than a missing approval.

The approval now sits beside the policy files the same scripts already read,
under a path the current taxonomy admits, so it cannot be carried away by a
stage rename again. The scripts still fail closed; they now fail for the
accurate reason.

No approval was written as part of that move. Granting one is an operator
decision about outbound network access, and recording it is the only thing this
file is for.

## Related Documents

- [Scripts index](../scripts/README.md)
- [Script manifest](../scripts/manifest.yaml)
