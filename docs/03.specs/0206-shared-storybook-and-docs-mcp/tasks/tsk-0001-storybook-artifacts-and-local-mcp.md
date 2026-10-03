---
title: "Storybook Artifacts and Local MCP Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
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
| Scaffold-only components -> reviewed package artifact | NEW `projects/storybook/nextjs/packages/ui/package.json`, `projects/storybook/nextjs/packages/ui/tsconfig.json`, `projects/storybook/nextjs/packages/ui/README.md`, `projects/storybook/nextjs/packages/ui/src/index.ts`, `projects/storybook/nextjs/packages/ui/src/styles.css`, `projects/storybook/nextjs/packages/ui/src/Button.tsx`; existing `projects/storybook/nextjs/package.json`, `package-lock.json`, `src/stories/Button.stories.ts` | Synthetic package `npm pack`/consumer import, types/CSS/a11y; private internal distribution only; revert only package and story import. Header/Page stay examples until independently justified. |
| No manifests/local MCP -> preview manifests and docs-only server | `projects/storybook/nextjs/.storybook/main.ts`, `projects/storybook/nextjs/package.json`, `projects/storybook/nextjs/package-lock.json`; NEW `projects/storybook/nextjs/mcp/server.ts` and focused protocol test | Build manifest revision, initialize/tools/list/docs reads and forbidden-tool rejection; revert scoped source and lock. |
| No static image -> confined build and origin | NEW `projects/storybook/nextjs/Dockerfile`, `projects/storybook/nextjs/.dockerignore`, `projects/storybook/nextjs/nginx.conf`; update `projects/storybook/nextjs/README.md`, `projects/storybook/README.md` | Docker context/build/static HTTP and browser checks after preflight; revert files, remove only owned scratch image/container. |
| Existing checker covers npm scripts only -> focused Storybook artifact contract | `scripts/validation/check-storybook-contract.sh` and focused tests only if the new invariant cannot be checked by existing gates | Checker self-test and changed-path gate; revert validator change. |

Exact package implementation file list may narrow after official API and consumer test design; broadening it needs amended Task approval. No root Compose, public env, secret, global client or `.github` writer is assigned here.

## Verification Evidence

`NOT_RUN`: approved source implementation has not yet started. The prior SPEC-0205 npm/build/browser results are prerequisite evidence, not this Task's verification. Docker preflight and official image digest remain pending.

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| 1 | W1 | NOT_RUN: verify packages, license and image facts | Package manifest, this Task |
| 2 | W2 | NOT_RUN: isolated image/browser checks | Dockerfile and Storybook README |
| 4 | W1 | NOT_RUN: synthetic package consumer | UI package README |
| 5 | W1 | NOT_RUN: manifest/local MCP protocol checks | MCP source and this Task |

## Review Evidence

Pending independent source and security review after exact diff and checks. Design draft is not source approval.

## Commit Ledger

Baseline `d2a5dfc79c33c412a6a9f06b9a8b49db9eb65bf7`; dependent branch base `fbbea9123751c13588022cdb76213fd8b5a14b6e`. No implementation commit.

## Rulings

Local MCP process only, outside root Compose; remote machine route disabled. This Task adds a nextjs npm workspace; its existing lockfile then owns the nested UI package. No unverified component is exported.

## Deferred Items

Reviewer group, remote audience/client, HOME and external design execution.
