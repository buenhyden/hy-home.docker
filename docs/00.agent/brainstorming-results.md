# Brainstorming Results: Documentation & Agent Refactor (Cycle 2)

## 1. Root File Analysis Summary

| File | Status | Layer | Findings / Required Fixes |
| --- | --- | --- | --- |
| `ARCHITECTURE.md` | ✅ Partially Aligned | `core` | Mentions `docs/plans/` correctly, but needs internal link audit. |
| `CODE_OF_CONDUCT.md` | ✅ Aligned | `meta` | Content is standard; metadata in place. |
| `COLLABORATING.md` | ✅ Aligned | `meta` | Redirects to `docs/manuals/`. |
| `CONTRIBUTING.md` | ✅ Aligned | `meta` | Redirects to `docs/guides/`. |
| `OPERATIONS.md` | ⚠️ Needs Update | `ops` | Links to `docs/plans/README.md` and `docs/runbooks/README.md` are correct, but needs explicit confirmation for all incident paths. |
| `README.md` | ⚠️ Needs Update | `entry` | Directory tree and footer links need synchronization with the `docs/00.agent/gateway.md`. |

## 2. Legacy Content vs. Mandatory Requirements ("# 필수 사항")

**Goal**: Authority docs = Singular (`adr`, `ard`, `prd`). Implementation/Operations = Plural (`plans`, `specs`, `runbooks`, `operations`).

- **Plans**: `docs/05.plans/` (template: `docs/99.templates/plan.template.md`) -> **Current Status**: Partially migrated. Need to remove `docs/plan_tmp/`.
- **Specs**: `docs/04.specs/` (template: `docs/99.templates/spec.template.md`) -> **Current Status**: Verified.
- **Runbooks**: `docs/09.runbooks/` (template: `docs/99.templates/runbook.template.md`) -> **Current Status**: Verified.
- **Operations**: `docs/08.operations/` (incidents & postmortems) -> **Current Status**: Sub-folders exist; need template verification.

## 3. Agent Entrypoints Strategy (March 2026)

**Protocol**: *Discovery Gateway*

- `AGENTS.md`: Must act as the primary contract. No direct instructions.
- `CLAUDE.md` / `GEMINI.md`: Must be lightweight triggers.
- **Triggers**: `[LOAD:RULES:REFACTOR]`, `[LOAD:RULES:INFRA]`, etc.
- **Instruction Hub**: All behavioral logic moves to `docs/00.agent/instructions.md` or specialized rule files.
- **Skill Autonomy**: Explicitly state "No restricted skills" to empower agents.

## 4. Ideal Lazy-Loading Structure in `docs/agentic/`

```text
docs/00.agent/
├── gateway.md        # The Map (Triggers -> Paths)
├── instructions.md   # Behavioral Baseline (Communication, Ethics)
└── rules/            # Specialized Logic
    ├── refactor.md
    ├── infra.md
    └── ops.md
```

## 5. Metadata Enforcement

- Every `.md` file must have `layer:` frontmatter.
- Automation check: `grep -r "layer:" docs/`.
