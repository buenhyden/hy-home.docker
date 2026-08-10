---
status: active
artifact_id: reference:agentic-research:scope-application-matrix
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-07
---

# Reference: Scope Application Matrix

## Overview

The eighteen sibling leaves in this research pack are organized by topic:
harness, loop, security, CI, memory, metadata, Compose, provider comparison,
and so on. That axis answers "what does the research say about subject X".
It does not answer the question an executing agent actually asks, which is
"I have loaded one scope; what in this pack applies to me".

This leaf adds the second axis. It is keyed by the fourteen scope files in
`docs/00.agent-governance/scopes/`, and for each scope it records the declared
purpose, the applicable research leaves, the repository surfaces the scope
actually governs here, whether the scope is reachable from the typed agent
catalog, and what must be settled before that scope's research findings can be
applied.

This reference describes the tracked workspace at commit
`82fc20dafc86b80393352ce53c86efb29748722a`. It is advisory: Stage 00 rules,
scopes, contracts, Compose, and scripts remain authoritative.

## Purpose

Give an agent that has resolved one layer a single place to see the pack's
relevant content, the surfaces that layer owns, and the honest reachability
state of that layer, without re-reading eighteen topic leaves.

## Repository Role

This reference supports `rules/bootstrap.md` step 5, `rules/persona.md`, and
`contracts/agent-catalog.yaml`. It defines no new control, adds no scope,
removes no scope, and grants no ownership.

## Scope

### In Scope

- Declared purpose of each of the fourteen scope files, with `file:line`
- Applicable research leaves per scope, separated into citation-backed and
  subject-matter mappings
- Repository surfaces each scope governs, derived from tracked files
- Reachability verdicts against the typed agent catalog and its validator
- Per-scope adoption boundary

### Out of Scope

- Adding, retiring, merging, or renaming any scope
- Changing `contracts/agent-catalog.yaml`, `rules/persona.md`, or any scope file
- Asserting that a scope's mandated stack should be adopted or removed
- Treating an unreachable scope as dead policy; it remains loadable prose

## Definitions / Facts

- A **scope** is a layer-keyed policy file under
  `docs/00.agent-governance/scopes/`. `rules/bootstrap.md:40` requires an agent
  to "Resolve task layer and load one primary scope from `scopes/<layer>.md`".
  There are fourteen such files.
- A **persona route** is a row in the mapping table at
  `rules/persona.md:23-38`. All fourteen scopes have a persona row, so all
  fourteen are reachable by prose routing.
- A **catalog scope** is a value in the `scopes:` enum at
  `contracts/agent-catalog.yaml:8-16`. That enum lists eight values:
  `agentic`, `architecture`, `common`, `docs`, `infra`, `ops`, `qa`,
  `security`.
- The enum is **validator-enforced**, not decorative.
  `scripts/validation/agent_governance_contract.py:2667-2668` rejects any
  `agents[].scope` outside the enum, and `:2784-2785` applies the same rule to
  `functions[].scope`. A catalog entry naming `mobile` or `backend` would fail
  the contract check.
- The catalog declares 14 agents (`agent-catalog.yaml:52`) and 24 functions
  (`:273`), for 38 `scope:` declarations distributed as agentic 8, infra 7,
  qa 6, ops 6, security 3, docs 3, common 3, architecture 2.
- **Live** here means the scope has a catalog entry, a generated provider
  adapter that links it, and tracked workspace surfaces it governs.
  **Vestigial** means the scope has persona routing and prose but no catalog
  entry, no adapter reference, and no or near-no workspace surface matching its
  mandated stack. **Absorbed** is the middle case: the subject matter is live
  in this repository, but a different scope owns it in the File Ownership SSOT.
- Zero generated provider adapters reference the six non-catalog scopes. Across
  `.claude/`, `.codex/`, `.gemini/`, and `.agents/`, scope-file links resolve as
  agentic 18, infra 16, ops 12, qa 12, docs 8, security 8, common 6,
  architecture 2, and backend/entry/frontend/meta/mobile/product 0.
- The topic leaves in this pack explicitly cite only four scope files:
  `qa` (in 5 leaves), `security` (5), `common` (2), and `docs` (1). Ten of the
  fourteen scopes, including `infra` and `agentic`, are never linked by name
  from a sibling leaf. That coverage gap is the direct motivation for this
  scope-keyed view.

## Derivation Commands

Every count above and below is reproducible from a clean checkout at the stated
commit. Run from the repository root.

```bash
# Scope inventory (14)
ls -1 docs/00.agent-governance/scopes/*.md | wc -l

# Catalog scope enum, agent count, function count
sed -n '8,16p' docs/00.agent-governance/contracts/agent-catalog.yaml
grep -c 'agent_id:'    docs/00.agent-governance/contracts/agent-catalog.yaml   # 14
grep -c 'function_id:' docs/00.agent-governance/contracts/agent-catalog.yaml   # 24

# Scope distribution across the 38 catalog declarations
grep 'scope:' docs/00.agent-governance/contracts/agent-catalog.yaml \
  | sed 's/.*scope: //' | sort | uniq -c | sort -rn

# Generated-adapter reach per scope
for s in agentic architecture backend common docs entry frontend \
         infra meta mobile ops product qa security; do
  printf '%s %s\n' "$s" \
    "$(git grep -o "scopes/$s.md" -- .claude .codex .gemini .agents | wc -l)"
done

# Sibling-leaf citation reach per scope
cd docs/90.references/research/2026-07-05-agentic-research-pack-refresh
for s in common docs qa security; do
  printf '%s %s\n' "$s" "$(grep -l "scopes/$s.md" *.md | wc -l)"
done

# Workspace surface counts
ls -1d infra/*/ | wc -l                                  # 12 (11 domains + secrets/)
git ls-files scripts/validation | wc -l                  # 41
git ls-files docs/01.requirements | wc -l                # 26
git ls-files docs/02.architecture | wc -l                # 53
git ls-files docs/03.specs | wc -l                       # 100
git ls-files docs/04.execution | wc -l                   # 234
git ls-files docs/05.operations | wc -l                  # 263
git ls-files docs/99.templates | wc -l                   # 48
git ls-files .github/workflows | wc -l                   # 7

# Mobile and frontend reality checks
git ls-files '*.tsx' '*.jsx' | wc -l                     # 6, all under projects/storybook/nextjs
git ls-files '*.swift' '*.kt' '*.dart' 'android/*' 'ios/*' | wc -l   # 0
git ls-files 'app.json' 'eas.json' 'metro.config*' | wc -l           # 0
git grep -l -i -E 'react-native|\bexpo\b|tamagui' \
  -- ':!docs/' ':!graphify-out/' ':!.claude' ':!.agents' ':!.codex' ':!.gemini'  # no output
```

## Scope Application Matrix

Leaves are split into two columns on purpose. **Cites** means the leaf links the
scope file by path and is verifiable with `grep`. **Applies** is a subject-matter
mapping made by this leaf; it is editorial, not a tracked relationship.

| Scope          | Declared purpose (`file:line`)                                                                                               | Leaves that cite the scope                                                                                                                        | Leaves that apply by subject                                                                                                                                                                                                                    | Repository surfaces governed                                                                                                                                                                                                                                                                                                 |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `agentic`      | "standardize planning, execution, and communication" — `scopes/agentic.md:11`                                                | none                                                                                                                                              | `harness-engineering`, `loop-engineering`, `ai-agent-catalogs`, `agent-instructions-vibe-coding`, `agent-model-selection`, `provider-model-landscape`, `provider-implementation-comparison`, `memory-hierarchy`, `automation-pipeline-workflow`, `verification-validation` | `docs/00.agent-governance/` (109 files), `.claude/` (48), `.agents/` (41), `.gemini/` (17), `.codex/` (16), `scripts/hooks/` (3), `scripts/operations/provider_surface_renderer.py`, root `AGENTS.md`/`CLAUDE.md`/`GEMINI.md`                                                                                                |
| `architecture` | "Maintain architectural integrity, scalability, and loose coupling in a distributed ecosystem" — `scopes/architecture.md:11` | none                                                                                                                                              | `spec-driven-sdlc`, `sdlc-document-roles`, `docker-compose-infrastructure`, `workspace-baseline`                                                                                                                                                | `docs/02.architecture/decisions/`, `docs/02.architecture/requirements/` (53 files combined), `docs/03.specs/` (100)                                                                                                                                                                                                          |
| `backend`      | "Delivery of performant, secure, and highly observable backend APIs" — `scopes/backend.md:11`                                | none                                                                                                                                              | `spec-driven-sdlc`, `quality-ci-formatting` (generic only)                                                                                                                                                                                      | none matching the mandated stack; see Reachability Assessment                                                                                                                                                                                                                                                                |
| `common`       | "Ensure consistency, maintainability, and readability across the entire `hy-home.docker` codebase" — `scopes/common.md:11`   | `quality-ci-formatting`, `workspace-baseline`                                                                                                     | `agent-instructions-vibe-coding`, `document-metadata-lifecycle`, `verification-validation` | `.pre-commit-config.yaml` (10 hook repos), `docs/03.specs/` (read), shared `scripts/lib/`                                                                                                                                                                                                                                    |
| `docs`         | "Boundaries and permissions for agents interacting with repository documentation" — `scopes/docs.md:7`                       | `llm-wiki-system`                                                                                                                                 | `documentation-architecture`, `document-metadata-lifecycle`, `sdlc-document-roles`, `memory-hierarchy`, `spec-driven-sdlc`                                                                                                                      | `docs/00.agent-governance/`, `docs/05.operations/` (263), `docs/98.archive/` (21), `docs/99.templates/` (48), `docs/90.references/llm-wiki/`, root instruction shims — ownership table `scopes/docs.md:59-65`                                                                                                                |
| `entry`        | "Secure, performant, and reliable routing of external traffic into the internal network" — `scopes/entry.md:11`              | none                                                                                                                                              | `docker-compose-infrastructure`, `security-governance`                                                                                                                                                                                          | `infra/01-gateway/` (17 files: `traefik/`, `nginx/`, 7 dynamic route/TLS files) — but owned by `infra-implementer` per `scopes/infra.md:74-75`                                                                                                                                                                               |
| `frontend`     | "Delivery of premium, 'WOW' factor user experiences" — `scopes/frontend.md:11`                                               | none                                                                                                                                              | `quality-ci-formatting` (Storybook/Vitest gate only)                                                                                                                                                                                            | `projects/storybook/nextjs/` (52 tracked files under `projects/`, 6 `.tsx`) — owned by `code-reviewer` per `scopes/qa.md:136`                                                                                                                                                                                                |
| `infra`        | "Maintain a highly available, performant, and secure containerized infrastructure" — `scopes/infra.md:11`                    | none                                                                                                                                              | `docker-compose-infrastructure`, `security-governance`, `workspace-baseline`, `quality-ci-formatting`, `automation-pipeline-workflow`, `github-actions-platform` | 11 `infra/` service domains (`01-gateway` … `11-laboratory`), `infra/secrets/`, `infra/tech-stack.versions.json`, root and tiered `docker-compose*.yml`, `scripts/validation/validate-docker-compose.sh` — ownership table `scopes/infra.md:74-78`                                                                           |
| `meta`         | "Maintain a highly organized, searchable, and AI-optimized documentation ecosystem" — `scopes/meta.md:11`                    | none                                                                                                                                              | `document-metadata-lifecycle`, `documentation-architecture`, `llm-wiki-system`, `sdlc-document-roles`                                                                                                                                           | `docs/99.templates/templates/` (6 families), `scripts/validation/check-document-metadata.py`, `check-document-corpus-lifecycle.py`, `scripts/knowledge/generate-llm-wiki-index.sh` — all owned by `doc-writer` per `scopes/docs.md:59-65`                                                                                    |
| `mobile`       | "Delivery of performant, accessible, and high-quality mobile experiences using React Native/Expo" — `scopes/mobile.md:11`    | none                                                                                                                                              | none                                                                                                                                                                                                                                            | none                                                                                                                                                                                                                                                                                                                         |
| `ops`          | "Minimize MTTR … and maximize system availability" — `scopes/ops.md:11`                                                      | none                                                                                                                                              | `docker-compose-infrastructure`, `automation-pipeline-workflow`, `security-governance`, `workspace-baseline`, `github-actions-platform` | `infra/06-observability/` (alertmanager, alloy, grafana, loki, prometheus, pushgateway, pyroscope, tempo), `docs/05.operations/{guides,incidents,policies,releases,runbooks}/` — ownership table `scopes/ops.md:42-45`                                                                                                       |
| `product`      | "Ensure every technical initiative corresponds to a validated product need" — `scopes/product.md:11`                         | none                                                                                                                                              | `spec-driven-sdlc`, `sdlc-document-roles`                                                                                                                                                                                                       | `docs/01.requirements/` (26 files, `001-gateway.md` onward), `docs/99.templates/.../prd.template.md` — no owner row anywhere                                                                                                                                                                                                 |
| `qa`           | "Maintain zero-defect production state and verify all technical specs" — `scopes/qa.md:11`                                   | `quality-ci-formatting`, `harness-engineering`, `loop-engineering`, `security-governance`, `workspace-baseline`, `ai-agent-catalogs`              | `agent-model-selection`, `automation-pipeline-workflow`, `verification-validation`, `github-actions-platform` | `scripts/validation/` (41 files), `.pre-commit-config.yaml`, `.github/workflows/` (7), `projects/storybook/`, `scripts/validation/check-storybook-contract.sh` — ownership table `scopes/qa.md:135-138`                                                                                                                      |
| `security`     | "zero-trust implementation and continuous security posture management" — `scopes/security.md:11`                             | `security-governance`, `quality-ci-formatting`, `harness-engineering`, `docker-compose-infrastructure`, `workspace-baseline`, `ai-agent-catalogs` | `automation-pipeline-workflow`, `github-actions-platform` | `scripts/security/` (3), `scripts/hardening/check-all-hardening.sh`, `scripts/validation/check-template-security-baseline.sh`, `check-quickwin-baseline.sh`, `check-supply-chain-policy.py`, `infra/supply-chain.*.json` (5), `infra/secrets/`, `docs/05.operations/incidents/` — ownership table `scopes/security.md:66-70` |

## Reachability Assessment

The audit claim under review was that six of fourteen scopes sit outside the
agent catalog while `rules/persona.md:23-38` routes personas into them anyway,
that `scopes/mobile.md` mandates a React Native stack in a repository with zero
mobile files, and that `scopes/frontend.md` mandates a product stack whose only
trace is one Storybook sandbox. Each part was re-derived independently.

**Confirmed, with one refinement.** The six-scope gap is real and is stronger
than "outside the catalog": it is validator-enforced. The mobile claim is
confirmed exactly. The frontend claim is confirmed with a correction, since two
of the mandated stack elements do exist in the sandbox. Two of the six
scopes — `entry` and `meta` — are better described as absorbed than vestigial,
because their subject matter is live and owned by a different scope.

| Scope          | Verdict                                | Evidence                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| -------------- | -------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `agentic`      | Live                                   | 8 catalog declarations; 18 adapter links; owns `docs/00.agent-governance/` (109 files) and four provider surfaces                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `architecture` | Live                                   | 2 catalog declarations (`requirements-to-design-agent`, one review function); 2 adapter links; owns `docs/02.architecture/` (53 files)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `common`       | Live                                   | 3 catalog declarations; 6 adapter links; `code-reviewer` owns `.pre-commit-config.yaml` per `scopes/common.md:55`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `docs`         | Live                                   | 3 catalog declarations; 8 adapter links; `doc-writer` owns six path families per `scopes/docs.md:59-65`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `infra`        | Live                                   | 7 catalog declarations; 16 adapter links; owns 11 `infra/` domains and all `docker-compose*.yml`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `ops`          | Live                                   | 6 catalog declarations; 12 adapter links; `incident-responder` owns `docs/05.operations/` and `infra/06-observability/`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `qa`           | Live                                   | 6 catalog declarations; 12 adapter links; owns 41 validation scripts and the Storybook contract                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `security`     | Live                                   | 3 catalog declarations; 8 adapter links; `security-auditor` owns the hardening and baseline scripts                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `entry`        | Absorbed                               | Not in the enum at `agent-catalog.yaml:8-16`; 0 adapter links; but `infra/01-gateway/` holds 17 tracked files including `traefik/config/traefik.yml` and 7 dynamic route/TLS definitions, and `infra/tech-stack.versions.json:12` pins `traefik:v3.7.8`, which satisfies the `scopes/entry.md:16` Traefik v3 + Nginx mandate. Ownership sits with `infra-implementer` via `scopes/infra.md:75`. Cloudflare, the third stack element at `entry.md:16`, has no tracked trace.                                                                                                                                                                                                             |
| `meta`         | Absorbed                               | Not in the enum; 0 adapter links; but the subject matter is fully live — `scripts/validation/check-document-metadata.py` and `check-document-corpus-lifecycle.py` enforce the frontmatter contract at `meta.md:16-20`, and `docs/99.templates/templates/` holds six template families. Ownership sits with `doc-writer` via `scopes/docs.md:63`.                                                                                                                                                                                                                                                                                                                                        |
| `product`      | Vestigial as a route, live as a corpus | Not in the enum; 0 adapter links; no ownership row in any scope's File Ownership SSOT. `docs/01.requirements/` nonetheless holds 26 tracked requirement documents. No agent is assigned to author or review them under this scope.                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `frontend`     | Near-vestigial                         | Not in the enum; 0 adapter links. `git ls-files '*.tsx' '*.jsx'` returns 6 files, all under `projects/storybook/nextjs/`. Refinement to the audit claim: the sandbox does satisfy part of the `frontend.md:17-20` mandate — `next 16.2.10`, `react 19.2.7`, and `tailwindcss ^4.3.2` clear the stated Next.js 15+/React 19+/Tailwind v4 floors. Framer Motion, TanStack Query, and Zustand appear nowhere in `projects/storybook/nextjs/package.json`. The WCAG 2.2 AA mandate at `frontend.md:21` has a partial mechanism via `@storybook/addon-a11y`, but no tracked conformance evidence. The sandbox is owned by `code-reviewer` under `scopes/qa.md:136`, not by a frontend agent. |
| `backend`      | Vestigial                              | Not in the enum; 0 adapter links. `scopes/backend.md:16-18` mandates Node.js 22+ with Prisma/Zod, or Python 3.12+ with SQLAlchemy/Pydantic/FastAPI. No tracked service implements either. The single service example, `examples/sample-web-service/` (9 files), is a static site: an Alpine build stage copying `site/` into an unprivileged nginx runtime, with `nginx.conf` and `site/index.html` and no application code. The OWASP ASVS L2 requirement at `backend.md:19` and the ≥90% domain coverage requirement at `backend.md:37` have no code to bind to.                                                                                                                      |
| `mobile`       | Vestigial                              | Not in the enum; 0 adapter links. Confirmed exactly as claimed: `git ls-files '*.swift' '*.kt' '*.dart' 'android/*' 'ios/*'` returns 0; `app.json`, `eas.json`, and `metro.config*` return 0; a case-insensitive grep for `react-native`, `expo`, or `tamagui` across tracked files excluding `docs/`, `graphify-out/`, and the four provider surfaces returns no match. The only repository-wide references to `scopes/mobile.md` are `rules/persona.md`, one Stage 03 spec, one Stage 04 plan, the generated LLM Wiki index, one Stage 90 audit inventory, and nine dated `graphify-out/` snapshots.                                                                                  |

### What the gap does and does not mean

- It is **not** a broken link. All fourteen scope files exist and load. An agent
  following `rules/bootstrap.md:40` can read any of them.
- It **is** a delegation gap. No typed agent or function can declare one of the
  six scopes without failing
  `scripts/validation/agent_governance_contract.py:2667`. Work in those layers
  either routes through a persona with no matching agent, or is absorbed by an
  adjacent scope that does have one.
- It is also a **research coverage gap in this pack**. Because the topic leaves
  cite only `qa`, `security`, `common`, and `docs`, a reader working in `entry`,
  `meta`, or `product` gets no signposting at all from the existing index. This
  leaf is the compensating index, not a fix for the underlying gap.

## Scope-to-Workspace Mapping

Derived surfaces, keyed by scope. Counts are `git ls-files` counts at the stated
commit and include README files.

- **`agentic`** — `docs/00.agent-governance/` (109). Provider surfaces
  `.claude/` (48), `.agents/` (41), `.gemini/` (17), `.codex/` (16). Hook
  dispatch `scripts/hooks/agent-event-hook.sh`, `post-tool-validate.sh`,
  `patch-graphify-post-commit.sh`. Renderer
  `scripts/operations/provider_surface_renderer.py` and
  `sync-provider-surfaces.sh`. Root shims `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`.
- **`architecture`** — `docs/02.architecture/decisions/` and
  `docs/02.architecture/requirements/` (53 combined), plus `docs/03.specs/`
  (100) as the downstream boundary artifact named at `architecture.md:17`.
- **`backend`** — none. The nearest surface, `examples/sample-web-service/`, is
  an infra reference Dockerfile, not a backend service.
- **`common`** — `.pre-commit-config.yaml` (10 hook repos), `scripts/lib/` (1),
  and cross-cutting naming/formatting rules that bind to every other surface.
  `common.md:52-55` claims `common/`, `lib/`, `shared/` path patterns; only
  `scripts/lib/` exists.
- **`docs`** — `docs/05.operations/` (263), `docs/04.execution/` (234),
  `docs/03.specs/` (100), `docs/90.references/` (96),
  `docs/02.architecture/` (53), `docs/99.templates/` (48),
  `docs/01.requirements/` (26), `docs/98.archive/` (21). Validators
  `check-doc-implementation-alignment.sh`, `check-doc-traceability.sh`,
  `check-document-metadata.py`, `check-document-corpus-lifecycle.py`.
  Generator `scripts/knowledge/generate-llm-wiki-index.sh`.
- **`entry`** — `infra/01-gateway/` (17): `traefik/config/traefik.yml`,
  `traefik/dynamic/` (7 route and TLS files including `middleware.yml`,
  `tls.yaml`, and four k3d service routes), `nginx/config/nginx.conf`, and two
  `docker-compose.yml` files.
- **`frontend`** — `projects/storybook/nextjs/` only: 6 `.tsx`, 3 `.stories.ts`,
  `.storybook/` config (3), `next.config.ts`, `eslint.config.mjs`,
  `postcss.config.mjs`, `package.json`. Contract gate
  `scripts/validation/check-storybook-contract.sh`.
- **`infra`** — the 11 numbered service domains `infra/01-gateway`,
  `02-auth`, `03-security`, `04-data`, `05-messaging`, `06-observability`,
  `07-workflow`, `08-ai`, `09-tooling`, `10-communication`, `11-laboratory`;
  plus `infra/secrets/`, `infra/tech-stack.versions.json`,
  `infra/common-optimizations.yml`, `infra/image-tag-policy.exceptions.json`,
  the five `infra/supply-chain.*.json` policy files, root
  `docker-compose.yml`, and `scripts/validation/validate-docker-compose.sh`.
- **`meta`** — `docs/99.templates/templates/` with six families (`common`,
  `governance`, `operations`, `sdlc`, `spec-contracts`, plus the index README),
  `check-document-metadata.py`, `check-document-corpus-lifecycle.py`,
  `check-target-surface-contract.py`, `check-target-surface-delta-contract.py`.
- **`mobile`** — none.
- **`ops`** — `infra/06-observability/` with eight component directories
  (`alertmanager`, `alloy`, `grafana`, `loki`, `prometheus`, `pushgateway`,
  `pyroscope`, `tempo`) plus `docker-compose.yml` and `docker-compose.dev.yml`;
  `docs/05.operations/` with five subdirectories (`guides/`, `incidents/`,
  `policies/`, `releases/`, `runbooks/`); `scripts/operations/` (8).
- **`product`** — `docs/01.requirements/` (26), numbered `001-gateway.md`
  through the current series, and the PRD template under `docs/99.templates/`.
- **`qa`** — `scripts/validation/` (41), spanning Compose validation, repo
  contracts, traceability, document metadata, CI gate contract and runner,
  agent-output eval fixtures and scorer, the controlled all-files wrapper, the
  CI-only pre-commit entry point, and the local QA gate runner;
  `.pre-commit-config.yaml`; `.github/workflows/` (7);
  `tests/validation/test_agent_output_eval_fixtures.py`; `projects/storybook/`.
- **`security`** — `scripts/security/` (3: supply-chain summary, grype DB seed,
  sample-service verification), `scripts/hardening/check-all-hardening.sh`,
  `scripts/validation/check-template-security-baseline.sh`,
  `check-quickwin-baseline.sh`, `check-supply-chain-policy.py`,
  `grype_db_seed.py`, the five `infra/supply-chain.*.json` policy files,
  `infra/secrets/`, `docs/05.operations/incidents/`.

## Adoption Boundary per Scope

Research in this pack is advisory everywhere. This section records the specific
precondition that must be settled before a given scope's findings can move from
reading to change.

| Scope          | What must be investigated or changed first                                                                                                                                                                                                                                                                                   |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `agentic`      | Nothing structural blocks adoption. Any new hook event, adapter field, or catalog role still needs an approved Stage 03 specification plus Stage 04 work, and `sync-provider-surfaces.sh --check` must stay green. Live provider interception remains unobserved, so adopt from the typed contract, not from provider prose. |
| `architecture` | The scope mandates gRPC internally and Kafka/RabbitMQ asynchronously (`architecture.md:20-22`). No tracked service consumes either. Adoption of any communication-protocol finding needs a real service first, or the mandate needs an ADR that narrows it to future work.                                                   |
| `backend`      | Requires a backend service to exist. Until one does, applying a backend finding means writing the mandate's stack from scratch, which is a product decision, not a research application. Decide first whether `backend.md` describes intent or aspiration.                                                                   |
| `common`       | The ownership table at `common.md:52-55` names `common/`, `lib/`, and `shared/`; only `scripts/lib/` exists. Reconcile the path pattern before treating the row as an enforceable boundary. Formatter and linter findings must route through `.pre-commit-config.yaml`, never through ad hoc commands.                       |
| `docs`         | `docs/01`–`docs/99` are read-only by default (`docs.md:21`). Any adoption needs explicit user approval, template-first compliance against `docs/99.templates/`, and regeneration of the LLM Wiki index when documents are added, removed, or renamed.                                                                        |
| `entry`        | Ownership is the blocker, not evidence. `infra/01-gateway/` is owned by `infra-implementer`. Either route gateway findings through the `infra` scope, or resolve whether `entry` should gain a catalog entry. Cloudflare edge findings have no tracked surface to land on.                                                   |
| `frontend`     | The Storybook sandbox is a QA-owned fixture, not a product frontend. Confirm whether it is meant to become one before applying Core Web Vitals, design-token, or state-management findings. Three of the six mandated stack elements are absent.                                                                             |
| `infra`        | Run `bash scripts/validation/validate-docker-compose.sh` before any change (`infra.md:36`). Live runtime mutation needs the Approved Runtime Mutation Protocol at `infra.md:44-58`, including a concrete target, pre-check, rollback, and post-check. Approval without a target authorizes planning only.                    |
| `meta`         | Frontmatter and taxonomy findings are enforceable today through the metadata validators, but the edits land in `doc-writer`-owned paths. Route through the `docs` scope. Structural folder changes additionally require a Meta ADR (`meta.md:41`).                                                                           |
| `mobile`       | Nothing is applicable. Before any mobile finding can be adopted, the repository needs a mobile surface to exist and a decision on whether `scopes/mobile.md` should be retired, archived, or retained as forward-looking policy.                                                                                             |
| `ops`          | Observability findings can be applied to `infra/06-observability/` configuration, but dashboards, alert rules, and SLO definitions bind to live services. Verify service health evidence before claiming an MTTR or availability outcome.                                                                                    |
| `product`      | No agent owns `docs/01.requirements/` in any File Ownership SSOT table. Assign ownership, or accept that requirement findings are applied by a human. PRD changes also cross the `docs/01`–`docs/99` read-only boundary.                                                                                                     |
| `qa`           | Coverage thresholds at `qa.md:18` presume a measurable suite. For docs-only, policy-only, or infrastructure-configuration changes the scope itself directs marking coverage N/A (`qa.md:37`). Direct `pre-commit run` is prohibited; the all-files wrapper is limited to an approved final QA gate.                          |
| `security`     | Local tracked files cannot prove remote branch protection, external secret hygiene, or provider global configuration. Secret work needs the Approved Secrets Work Protocol at `security.md:39-50`: metadata-only evidence, a concrete redacted target, and a recorded rollback path.                                         |

## Corrections and Caveats

- The phrase "outside the agent catalog" understates the constraint. The six
  scopes are rejected by `agent_governance_contract.py:2667` and `:2784`, so
  they cannot be added to the catalog without either extending the
  `agent-catalog.yaml:8-16` enum or failing the contract check.
- `entry` and `meta` should not be filed alongside `mobile` and `backend`. Their
  subject matter is live and validator-backed; only their routing is absent.
- The frontend sandbox partially satisfies its scope's stack mandate. Reporting
  it as a bare "one Storybook sandbox" omits that Next 16.2.10, React 19.2.7,
  and Tailwind v4 are present and clear the stated floors.
- The leaf-to-scope "applies by subject" column is this leaf's editorial
  judgement. Only the "cites" column is greppable. Do not cite the applies
  column as a tracked relationship.
- `product` is the only scope with a substantial live corpus (26 requirement
  documents) and no ownership row anywhere in the File Ownership SSOT tables of
  `common.md`, `docs.md`, `infra.md`, `ops.md`, `qa.md`, or `security.md`.
- Counts are commit-bound. `docs/04.execution/` and `docs/05.operations/` grow
  with every task; re-run the derivation commands rather than reusing these
  figures.

## Sources

This leaf cites no external sources. It is an internal-synthesis reference: it
reorganizes the eighteen sibling leaves of this research pack along a scope axis
and grounds every repository claim in tracked files at commit
`82fc20dafc86b80393352ce53c86efb29748722a`. External provider, framework, and
vendor evidence for the underlying topics lives in the sibling leaves that own
those topics, each of which carries its own `## Sources` section with retrieval
timestamps. Nothing here supersedes or restates those citations.

The tracked evidence used is:

- `docs/00.agent-governance/scopes/` — all 14 scope files
- `docs/00.agent-governance/rules/persona.md:14`, `:23-38`
- `docs/00.agent-governance/rules/bootstrap.md:40`
- `docs/00.agent-governance/contracts/agent-catalog.yaml:8-16`, `:52`, `:273`
- `scripts/validation/agent_governance_contract.py:2601-2612`, `:2667-2668`, `:2784-2785`
- `infra/tech-stack.versions.json:12`
- `projects/storybook/nextjs/package.json`
- `examples/sample-web-service/Dockerfile`
- `git ls-files` and `git grep` output as recorded in Derivation Commands

## Maintenance

- **Owner**: Documentation maintainers
- **Review Cadence**: Quarterly, or when the scope set changes
- **Update Trigger**: A scope file added, removed, or retargeted; a change to
  the `scopes:` enum in `contracts/agent-catalog.yaml`; a change to the persona
  mapping table in `rules/persona.md`; a new agent or function in the catalog;
  a new or removed leaf in this research pack; or the appearance of a workspace
  surface for a scope currently recorded as vestigial

## Related Documents

- [research pack index](./README.md)
- [workspace baseline](./workspace-baseline.md)
- [harness engineering](./harness-engineering.md)
- [AI agent catalogs](./ai-agent-catalogs.md)
- [documentation architecture](./documentation-architecture.md)
- [quality, CI, and formatting](./quality-ci-formatting.md)
- [security governance](./security-governance.md)
- [persona protocol](../../../00.agent-governance/rules/persona.md)
- [bootstrap rule](../../../00.agent-governance/rules/bootstrap.md)
- [agent catalog contract](../../../00.agent-governance/contracts/agent-catalog.yaml)
