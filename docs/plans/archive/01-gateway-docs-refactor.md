# Plan: Reorganize and Complete 01-gateway Documentation

This plan outlines the steps to reorganize, harmonize, and complete the documentation for the `01-gateway` tier, ensuring clear separation between high-level guides in `docs/` and technical details in `infra/`.

## User Review Required

> [!IMPORTANT]
> This refactor involves moving and updating documentation. No functional changes to the infrastructure or services are planned.

## Proposed Changes

### Documentation (infra/01-gateway)

#### [MODIFY] [README.md](file:///home/hy/projects/hy-home.docker/infra/01-gateway/README.md)
Update with:
- Unified architecture view.
- Comprehensive port mapping (traefik, nginx).
- Explicit mapping of configuration files to their roles.
- Links to relevant high-level guides.

#### [MODIFY] [README.md](file:///home/hy/projects/hy-home.docker/infra/01-gateway/traefik/README.md)
Update with:
- Detailed breakdown of static (`traefik.yml`) vs dynamic (`dynamic/`) configuration.
- Detailed routing labeled explanation.
- SSO Middleware details.
- Health check and metrics verification steps.

#### [MODIFY] [README.md](file:///home/hy/projects/hy-home.docker/infra/01-gateway/nginx/README.md)
Update with:
- Specialized proxy roles (path-based routing).
- SSO integration details via `auth_request`.
- Configuration validation and reload commands.

### Documentation (docs/guides/01-gateway)

#### [MODIFY] [CONTEXT.md](file:///home/hy/projects/hy-home.docker/docs/guides/01-gateway/CONTEXT.md)
Enrich with:
- Deeper architectural details discovered from `infra/` analysis.
- Traffic lifecycle visualization (Traefik as primary, Nginx as secondary).
- Explicit dependency mapping.

#### [MODIFY] [PROCEDURAL.md](file:///home/hy/projects/hy-home.docker/docs/guides/01-gateway/PROCEDURAL.md)
Enrich with:
- Detailed lifecycle commands (start, restart, reload).
- Step-by-step certificate management (mkcert integration).
- Verification procedures (health checks, metrics).

## Verification Plan

### Automated Tests
- Run `bash scripts/validate-docker-compose.sh` to ensure no syntax errors were introduced in YAML files (though we aren't planning to change them, it's good practice).

### Manual Verification
- Verify all links in the updated READMEs.
- Check Markdown rendering for all updated files.
