# [Feature Name] Specification

> Use this template for `docs/specs/YYYY-MM-DD-<feature-name>.md`.
>
> Repository-derived contract:
>
> - Use exactly one meaningful H1.
> - Use relative links only.
> - Remove every placeholder before saving.
> - Allowed spec status values: `Canonical | Implementation | Validated | Superseded | Deprecated`.
> - Allowed scope values where your doc set uses them: `master | domain | historical`.
> - Allowed scope values layer values: `common | architecture | backend | frontend | infra | mobile | product | qa | security`
> - Every active spec must declare PRD and ARD references or make the absence explicit.
> - Verification is mandatory even for documentation-only tracks.
> - Keep all structural and narrative content in English.
> - Add exactly one `Overview (KR)` summary near the top. That overview summary alone should be written in Korean.

## Optional Frontmatter

```yaml
---
title: '[Feature Name] Specification'
status: 'Canonical'
version: '1.0'
owner: 'buenhyden'
scope: 'master'
prd_reference: '../prd/<feature-or-system>-prd.md'
arch_reference: '../ard/<system-or-domain>-ard.md'
decision_reference: '../adr/NNNN-decision.md'
tags: ['spec','implementation']
layer: '<layer>'
---
```

## H1 and Metadata

# [Feature Name] Specification

> **Status**: [Canonical | Implementation | Validated | Superseded | Deprecated]
> **Scope**: [master | domain | historical]
> **layer:** [common | architecture | backend | frontend | infra | mobile | product | qa | security]
> **Parent Master Spec**: `[./YYYY-MM-DD-system-master-spec.md]` (Optional for `domain`)
> **Related PRD**: `[../prd/feature-or-system-prd.md]`
> **Related Architecture**: `[../ard/system-or-domain-ard.md]`
> **Decision Record**: `[../adr/NNNN-decision.md]` (Optional)

**Overview (KR):** [Write a 1-2 sentence Korean summary of the technical baseline, the implementation boundary, and the main risk or contract this spec addresses.]

## Required Core Sections

These sections are the minimum contract even for compact active-chain specs.

## Technical or Platform Baseline

[Explain the baseline system, platform, or implementation boundary this spec owns.]

## Contracts

Use the headings that best fit the domain, but make the contract explicit.

- **Config Contract**: [If applicable]
- **Data or Interface Contract**: [If applicable]
- **Asset / Routing / Rendering Contract**: [If applicable]
- **Archive / Governance Contract**: [If applicable]

## Verification

List the required commands, manual checks, or evidence capture steps.

```bash
[command 1]
[command 2]
```

## Optional Extended Sections

Use these sections when the spec needs full implementation detail and traceability.

## 1. Technical Overview & Architecture Style

[Explain the technical baseline, what this spec owns, and how it fits into the wider system.]

- **Component Boundary**: [What this spec owns]
- **Key Dependencies**: [Libraries, generated artifacts, configs, or upstream docs]
- **Tech Stack**: [Runtime, build, and verification stack]

## 2. Coded Requirements (Traceability)

| ID                | Requirement Description | Priority | Parent PRD REQ |
| ----------------- | ----------------------- | -------- | -------------- |
| **[REQ-SPC-001]** | [Technical requirement] | High     | REQ-PRD-FUN-01 |
| **[REQ-SPC-002]** | [Technical requirement] | Critical | REQ-PRD-FUN-02 |

## 3. Data Modeling & Storage Strategy

- **Database Engine**: [PostgreSQL | None | File-based | N/A]
- **Schema Strategy**: [How data, config, or generated artifacts are structured]
- **Migration Plan**: [How existing data or docs transition, or N/A]

## 4. Interfaces & Data Structures

### 4.1 Core Interfaces

```typescript
interface ExampleContract {
  id: string;
  name: string;
}
```

### 4.2 Authority or Integration Model (Optional)

```typescript
type DocumentationScope = 'master' | 'domain' | 'historical';
```

## 5. Component Breakdown

- **`path/to/file-or-doc`**: [Responsibility or planned change]
- **`path/to/another-file`**: [Responsibility or planned change]

## 6. Domain-Specific Contract Sections

Add only the sections that the domain truly needs. Examples from the current repository:

- **Routing Rules**
- **Markdown and Resource Processing**
- **Multilingual and Taxonomy Contracts**
- **Common Field Contract**
- **Enum Registry**
- **Type-Specific Requirements**
- **Family Shells**
- **Asset Presentation Rule**
- **Anti-Patterns**

## 7. Edge Cases & Error Handling

- **Error 1**: [Describe the concrete condition and expected behavior]
- **Error 2**: [Describe the concrete condition and expected behavior]

## 8. Verification Plan (Testing & QA)

- **[VAL-SPC-001] Structural review**: [Heading, title, document-shape, or ownership checks]
- **[VAL-SPC-002] Link review**: [Relative-link and reference checks]
- **[VAL-SPC-003] Build / test / runtime review**: [Commands or manual validation]
- **[VAL-SPC-004] Evidence capture**: [How the work is proven complete]

## 9. Non-Functional Requirements (NFR) & Scalability

- **Performance / Latency**: [Target or "no runtime change"]
- **Throughput**: [Target or N/A]
- **Scalability Strategy**: [How this area scales]

## 10. Operations & Observability

- **Deployment Strategy**: [How changes reach production or "documentation-only"]
- **Monitoring & Alerts**: [Signals, dashboards, or N/A]
- **Logging**: [Describe the evidence source, signal, or logging rule]
- **Sensitive Data Handling**: [Describe handling rules or state that they are not applicable]
