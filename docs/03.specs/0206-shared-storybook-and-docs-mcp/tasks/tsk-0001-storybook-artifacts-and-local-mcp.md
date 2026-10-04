---
title: "Storybook Artifacts and Local MCP Task"
version: "1.0.1"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-03"
layer: "specs"
artifact_id: "SPEC-0206-TSK-0001"
parent_ids:
- "SPEC-0206"
- "SPEC-0206-PLAN-0001"
created: "2026-10-03"
---

# Storybook Artifacts and Local MCP Task

## Objective

Produce a tested static Storybook image, reusable component artifact, revision-matched manifests and a local docs-only MCP source.

## Inputs

SPEC-0206 and Plan W1-W2; user approved the design, written SPEC and Plan/Task execution in this chat on 2026-10-03; dependency base `fbbea9123751c13588022cdb76213fd8b5a14b6e`; Storybook 10.6 official manifest/MCP APIs; existing scaffold components, lockfile and path-aware frontend gates.

## Work Log

| Current -> target | Exact writer files | Regression / rollback |
| --- | --- | --- |
| Scaffold-only components -> reviewed package artifact | NEW `projects/storybook/nextjs/packages/ui/package.json`, `projects/storybook/nextjs/packages/ui/tsconfig.json`, `projects/storybook/nextjs/packages/ui/README.md`, `projects/storybook/nextjs/packages/ui/src/index.ts`, `projects/storybook/nextjs/packages/ui/src/styles.css`, `projects/storybook/nextjs/packages/ui/src/Button.tsx`; existing `projects/storybook/nextjs/package.json`, `package-lock.json`, `src/stories/Button.stories.ts`, `src/stories/Header.tsx`, `.storybook/preview.ts` | Synthetic package `npm pack`/consumer import, types/CSS/a11y; private internal distribution only; revert only package and story import. Header/Page remain examples; Header consumes the reviewed Button. |
| No manifests/local MCP -> preview manifests and docs-only server | `projects/storybook/nextjs/.storybook/main.ts`, `projects/storybook/nextjs/package.json`, `projects/storybook/nextjs/package-lock.json`; NEW `projects/storybook/nextjs/mcp/server.ts`, `mcp/stamp.ts`, `tests/artifacts.test.mjs`, `tests/mcp.test.mjs` | Build manifest revision, initialize/tools/list/docs reads and forbidden-tool rejection; revert scoped source and lock. |
| No static image -> confined build and origin | NEW `projects/storybook/nextjs/Dockerfile`, `projects/storybook/nextjs/.dockerignore`, `projects/storybook/nextjs/nginx.conf`; update `projects/storybook/nextjs/README.md`, `projects/storybook/README.md` | Docker context/build/static HTTP and browser checks after preflight; revert files, remove only owned scratch image/container. |
| Existing checker covers npm scripts only -> focused Storybook artifact contract | `scripts/validation/check-storybook-contract.sh` and focused tests only if the new invariant cannot be checked by existing gates | Checker self-test and changed-path gate; revert validator change. |

Exact package implementation file list may narrow after official API and consumer test design; broadening it needs amended Task approval. No root Compose, public env, secret, global client or `.github` writer is assigned here.

## Verification Evidence

Source commit `e811e159afa2dc7245bb2d6b562a91cf931283fe` was reviewed and rebuilt with the same `STORYBOOK_SOURCE_REVISION`. Official Storybook 10.6 manifests/MCP preview APIs and Docker base-image digest/platform support were checked on 2026-10-03; builder `node:24.21.0-alpine3.24@sha256:ebfe2f90462722a7a4de65e91990e97fe0d401c70e0e762c5b53302f905ec1c1`, runtime `nginxinc/nginx-unprivileged:1.31.6-alpine3.24@sha256:26b0bf6fbf07297983cb341998d79c831508787de26627dd2a112321b9c3a4af` support amd64/arm64; tested host is amd64. No repository LICENSE is tracked, so `@hy-home/storybook-ui` remains private and `UNLICENSED`.

| Check (worktree unless noted) | Exit / evidence |
| --- | --- |
| `npm ci`; `npm run lint`; `npm run typecheck`; `npm run build`; `PLAYWRIGHT_BROWSERS_PATH=/tmp/p05-playwright-browsers npm run test` in `projects/storybook/nextjs` | 0 each; Storybook browser suite 3 files / 9 tests. |
| `npm run build-storybook` | 0; builds UI package and static site, stamps SHA-256 for `components.json` and `docs.json`, then runs artifact/MCP tests 5/5. Button manifest has `reactDocgen.props.label` and no error. |
| `npm pack` plus synthetic React/TypeScript/CSS consumer; `bash scripts/validation/check-storybook-contract.sh`; `git diff --check` | 0 each; public Button import, types and explicit CSS entry work. |
| `docker build --build-arg STORYBOOK_SOURCE_REVISION=e811e159afa2dc7245bb2d6b562a91cf931283fe -t hy-home/storybook:e811e159afa2dc7245bb2d6b562a91cf931283fe -f Dockerfile .` | 0; OCI revision label and `/revision.json` equal source SHA. |
| Isolated `p05-storybook-final` on `p05-storybook-final-net`, localhost 18967, no volumes, 128 MiB, 0.5 CPU, read-only root, UID/GID 101:101 | Health `healthy`; index/iframe/manifests/revision 200; unknown path 404; manifest hashes, CSP, no-store and nosniff pass. Playwright Button/CSS/assets/404 exit 0. Exact trial container and network removed; tagged image retained for Task 2. HOME service untouched. |
| One-off Playwright + installed axe-core on Button/Header/Page iframe stories | 0 violations; Button has one `bypass` incomplete because isolated canvas lacks page heading/landmark/skip link. Browser test exit 0; full HOME auth/TLS browser flow remains Task 2/operation evidence. |
| `npm audit --json` | Historical result: exit 1 with five high reports from one existing dev-only `eslint-config-next → fast-glob → micromatch → braces@3.0.3` chain. Official GHSA readback was refreshed on 2026-10-04 with no patched release; current dependency-audit handling belongs to the canonical quality policy and gate contract. This Task changes no exception. |

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| 1 | W1 | PASS: package/license/version and image digests/platform checked; dependency-audit handling delegated to canonical quality policy | [Package manifest](../../../../projects/storybook/nextjs/package.json) |
| 2 | W2 | PASS: exact-SHA isolated image, hardening, static HTTP/browser checks | [Dockerfile](../../../../projects/storybook/nextjs/Dockerfile) |
| 4 | W1 | PASS: synthetic external package consumer | [UI package README](../../../../projects/storybook/nextjs/packages/ui/README.md) |
| 5 | W1 | PASS: revision/hashes, docs-only MCP positive/negative and transport checks | [MCP source](../../../../projects/storybook/nextjs/mcp/server.ts) |

## Review Evidence

Independent source reviewer initially found missing Button docgen definition and unbundled CSS. Both were corrected; second review approved the manifest props, emitted CSS and regression assertions. A minor README import explanation mismatch was corrected before source commit. Independent security review found no new Critical/High source issue; real loopback tests now assert forged Host 403 and oversized request 413. The shared-network Traefik bypass is assigned to Task 2's user-approved dedicated ingress topology. Dependency-audit handling is historical here and current in the canonical quality policy.

## Commit Ledger

Baseline main/origin-main `d2a5dfc79c33c412a6a9f06b9a8b49db9eb65bf7`; dependency base `fbbea9123751c13588022cdb76213fd8b5a14b6e`; source `e811e159afa2dc7245bb2d6b562a91cf931283fe`. This Task record is written after exact-SHA image evidence.

## Rulings

Local MCP process only, outside root Compose; remote machine route disabled. This Task adds a nextjs npm workspace; its existing lockfile then owns the nested UI package. No unverified component is exported.

## Deferred Items

Reviewer group, remote audience/client, HOME and external design execution are handed off to GDE/POL/RUN-0101. Triggers: approved reviewer access, approved remote MCP issuer/audience/client, approved HOME route activation, or approved external design-account use.
