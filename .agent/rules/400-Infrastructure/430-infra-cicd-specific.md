---
trigger: always_on
glob: "**/.github/workflows/*.yml"
description: "CI/CD Standards (GitHub Actions): Pipelines, Security, and Caching."
---
# CI/CD Standards (GitHub Actions)

## 1. Pipeline Structure

- **Stages**:
  1. **Lint/Check**: Formatting, Static Analysis, Type Check. (Fail Fast)
  2. **Test**: Unit tests (Parallel Matrix).
  3. **Build**: Container build / Artifact packaging.
  4. **Deploy**: Staging -> (Approval) -> Prod.
- **Concurrency**: Use `concurrency: group: ${{ github.ref }}` (cancel-in-progress) for PRs.

## 2. Security & Secrets

- **Least Privilege**: `permissions: contents: read` (default). Grant writes explicitly.
- **Secrets**: Never prompt for secrets. Use `secrets.GITHUB_TOKEN` or OIDC for cloud auth.
- **Pinning**: Pin 3rd-party actions to SHA (`uses: actions/checkout@a1b2c3d...`).

## 3. Performance

- **Caching**: Aggressively cache dependencies (`actions/setup-node` cache: npm).
- **Timeouts**: Define `timeout-minutes` for ALL jobs to prevent zombie runners.
- **Artifacts**: Upload build artifacts only if deployment is needed.

## 4. Patterns

- **Paths Filter**: Use `paths-ignore` (`docs/**`, `*.md`) to skip CI on unrelated changes.
- **Reusable Workflows**: Extract complex logic to `workflow_call`.

## 5. NestJS & React Polyrepo Deployment
- **Structure**: Separate `api` and `web` repositories. Unified at build time.
- **Orchestration**: Supabase Webhook -> Pipeline Executor -> Render.
- **Environment**: Client base URL `/`, API base URL `/api` (Proxy).

## 6. Mobile CI/CD (Flutter)
- **Artifacts**: Firebase App Distribution (Android), TestFlight (iOS).
- **Notifications**: Automated WhatsApp/Twilio messages on build completion.
- **Versioning**: Artifact tagging `client-name/version/env` in storage.

## 7. Advanced Strategies
- **Downtime**: Zero-downtime using Blue/Green deployment where possible.
- **Rollback**: Automated rollback on health check failure.
- **DNS**: Automated DNS updates via API (Cloudflare/Route53) if endpoints change.