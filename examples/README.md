# Example Implementations (`examples/`)

This directory holds sample codes, mock configurations, and proof-of-concept setups demonstrating how to use the templates defined in `/templates/`.

## 1. Necessity and Purpose

This directory is necessary to provide safe, isolated reference implementations without polluting production code or formal specifications.

- Provide humans and AI models with tangible references for how specific components or integrations are expected to work in this architecture.
- Isolate experimental code from the primary `/src` and specification paths.

## 2. Required Content

Examples must be completely self-contained and should not import live production databases or configurations.

| Example File           | Template Used         | Purpose                                                  |
| ---------------------- | --------------------- | -------------------------------------------------------- |
| `example-adr.md`       | `adr-template.md`     | Architecture Decision Record for database selection      |
| `example-prd.md`       | `prd-template.md`     | Product Requirements Document for authentication feature |
| `example-runbook.md`   | `runbook-template.md` | Deployment runbook with rollback procedures              |

*(Also see `specs/example-spec.md` for a complete feature specification example)*

## 3. General Guidelines

- All examples MUST include brief inline comments explaining their intended context.
- Assume nothing in this folder will be deployed to production.
- Examples MUST follow the exact structure defined in their corresponding templates.

## 4. AI Agent Guidelines & Anti-Patterns

While these serve as "examples" to guide format and structure, any AI agent deriving actual project templates or creating new documents from these MUST ensure full compliance with the latest `.agent/rules/`.

- **Anti-Pattern**: Using outdated example configurations to override a strict security or operational rule defined in the `.agent/rules/`. Examples do *not* supersede official standards unless explicitly permitted by `docs/guides/`.
