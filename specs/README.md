# Technical Specifications Hub (`specs/`)

This directory is the absolute **Source of Truth** for the During-Development phase. It exists explicitly and exclusively for **Spec-Driven Development**.

## 1. Directory Structure

Specifications are organized by domain to ensure clarity and ease of navigation.

### 🔐 Auth & Integration

- [auth-integration/](file:///home/hy/projects/hy-home.docker/specs/auth-integration/): Keycloak, OAuth2-Proxy, and SSO integration specs.

### 🏗️ Infrastructure (`specs/infra/`)

Core infrastructure specifications and planning.

- [compose-readiness/](file:///home/hy/projects/hy-home.docker/specs/infra/compose-readiness/): "Core stack boot-ready" prerequisites and verification.
- [resource-budgets/](file:///home/hy/projects/hy-home.docker/specs/infra/resource-budgets/): Standardized CPU/Memory limits for core services.
- [security-consistency/](file:///home/hy/projects/hy-home.docker/specs/infra/security-consistency/): Rootless, `cap_drop`, and `no-new-privileges` standardization.
- [startup-automation/](file:///home/hy/projects/hy-home.docker/specs/infra/startup-automation/): Resource optimization for Supabase and Makefile-based startup automation.
- [alloy-telemetry/](file:///home/hy/projects/hy-home.docker/specs/infra/alloy-telemetry/): Alloy-based monitoring and telemetry collection.
- [gateway-routing/](file:///home/hy/projects/hy-home.docker/specs/infra/gateway-routing/): Traefik routing and dynamic configuration.
- [rag-stack/](file:///home/hy/projects/hy-home.docker/specs/infra/rag-stack/): Vector database (Qdrant) and AI-related infra components.

## 2. Path to Implementation

1. **Draft**: Planner Agent creates `spec.md` and `plan.md`.
2. **Approve**: Human Developer reviews and approves the spec.
3. **Execute**: Coder Agent implements changes following the `plan.md`.
4. **Verify**: Automated scripts and manual checks confirm success.

## 3. Golden Rules for AI Agents

**NO SPEC, NO CODE.**
Coder Agents MUST NOT write code without an approved specification in this folder.

- **Traceability**: Every coding change MUST map back to a requirement (e.g., `REQ-OPT-001`) in a `spec.md`.
- **Drift Prevention**: If technical debt or limitations force a plan change, the `spec.md` MUST be updated first.

---
> [!TIP]
> Use `scripts/validate-docker-compose.sh` to ensure your specification changes maintain syntax integrity across the entire stack.
