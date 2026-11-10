# Supply-Chain Network Approvals

## Purpose

Hold the written operator approvals that the supply-chain scripts below require
before they perform outbound network access. This file is the approval surface
itself, not a description of one: the scripts read it directly and refuse to
run when the approval line they need is absent.

## Current State

The Grype DB seed approval is on file (owner, 2026-10-15). The OpenBao material fetch approval is on file (owner, 2026-11-10). The Scorecard approval is not, so that script still fails closed.

## Scope

| Script                                                   | Required line, exactly                         | Grants                                                                                                         |
| -------------------------------------------------------- | ---------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| `scripts/security/seed-grype-db-cache.sh`                | `Grype DB network approval: confirmed`         | one bridged-network Grype vulnerability-database update; every other step stays on `--network none`            |
| `scripts/security/verify-sample-service-supply-chain.sh` | `Scorecard network approval: confirmed`        | one OpenSSF Scorecard call                                                                                     |
| `scripts/operations/prepare-openbao-materials.py`        | `OpenBao material network approval: confirmed` | one public-material fetch of the owned OpenBao build packet, bounded in the OpenBao material fetch entry below, including the Go module hosts |

Each line must appear on a line of its own, with no leading or trailing
characters: the scripts match it with `grep -Fqx`.

## Usage

To grant an approval, add the exact line from the table above to the
**Approvals** section below, and record who approved it and when in the same
commit message. To withdraw one, delete the line.

## Approvals

<!-- Add approval lines here, one per line, exactly as written in the table. -->

Grype DB network approval: confirmed

OpenBao material network approval: confirmed

### OpenBao material fetch

- Approved by: @buenhyden (owner), 2026-11-10, one time per rebuild of the
  owned OpenBao image packet.
- Purpose: authenticate and stage the public inputs of
  `infra/03-security/openbao/build/build-inputs.json` for
  `scripts/operations/prepare-openbao-materials.py`; no HOME or service action.
- Hosts: `github.com` (OpenBao v2.7.1 release assets, plus the GitHub asset
  CDN that `github.com` redirects to), `dl-cdn.alpinelinux.org` (Alpine v3.24
  x86_64 main and community APKINDEX and APKs), `alpinelinux.org` (the pinned
  Alpine signing key), `cgr.dev` (the pinned Chainguard Go builder digest,
  reached only by cosign) and the Sigstore public-good TUF, Rekor and Fulcio
  endpoints (reached only by cosign).
- Output bound: every download lands only under a new mode-0700
  `/tmp/hyhome-p01-owned-build-<UTC timestamp>/` directory.
- Cosign runs only through the bounded contract in
  `infra/supply-chain.tool-images.json` (`bounded_contracts`).
- Added 2026-11-10 by @buenhyden (owner): `proxy.golang.org` and
  `sum.golang.org`. Purpose: OpenBao r2 Go module cache. Output bound:
  `/tmp/hyhome-p01-owned-build-<ts>/`. They are reached only by the pinned
  builder container inside the script's bounded module step, with
  `GOTOOLCHAIN=local`, `GOFLAGS=-mod=mod` and an empty `GONOSUMDB`, and only
  when `--allow-go-proxy` is passed.
- No other host is approved, including `raw.githubusercontent.com`.

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
