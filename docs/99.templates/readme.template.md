<!-- Target: README.md -->
<!--
# README Template — Usage Guidelines

This template is designed to be modular. It consists of a **Base Structure** (required for all READMEs) 
and a **Snippet Library** from which you should pick sections based on the folder's purpose.

## 1. Metadata Requirement

# [Project or Component Name]

## 2. Selection Guide
- Project Root (/) -> Use 'Base' + 'Root Snippet'
- App Layers (web/, server/, app/) -> Use 'Base' + 'Implementation Snippet'
- Logic/Docs (docs/, templates/, .agent/) -> Use 'Base' + 'Docs & Governance Snippet'
- Tools/Ops (scripts/, operations/, runbooks/) -> Use 'Base' + 'Ops & Utils Snippet'

## 3. How to Use
1. Copy the "BASE STRUCTURE" below.
2. Replace placeholders in curly braces `{}`.
3. Scroll down to the "SNIPPET LIBRARY" and copy relevant sections for your folder.
4. Delete these guidelines and the unused snippets after assembly.
-->

---

## Overview (KR)

[이 폴더 또는 프로젝트의 역할과 전체 시스템에 기여하는 방식에 대한 1-2문장의 한국어 요약을 작성하십시오.]

# [BASE STRUCTURE]

# {Folder/Project Name}

> {One-line description of the purpose of this folder/project.}

## Overview

{Brief paragraph explaining the responsibility of this folder and how it contributes to the overall system.}

## Structure

```text
{folder-name}/
├── {file/dir 1}    # {Purpose}
├── {file/dir 2}    # {Purpose}
└── README.md        # This file
```

---

# [SNIPPET LIBRARY - PICK AND DROP BELOW]

<!-- 
================================================================================
SNIPPET: PROJECT ROOT (Main Onboarding)
================================================================================
-->

## Optimization Note (March 2026)

> [!IMPORTANT]
> This repository utilizes a **Thin Root** architecture for AI agents, enforcing JIT context loading and late-binding metadata routing for maximum performance and token efficiency.

## Tech Stack

| Category   | Technology                        | Notes                     |
| ---------- | --------------------------------- | ------------------------- |
| Language   | {TypeScript / Python / Go / etc.} | {Version / Build Target}  |
| Framework  | {Next.js / FastAPI / etc.}        | {Primary runtime}         |
| Database   | {PostgreSQL / MongoDB / etc.}     | {Persistence layer}       |
| Deployment | {Docker / Kubernetes / etc.}      | {Standard delivery track} |

## Prerequisites

- {Tool 1} >= {Version}
- {Tool 2} >= {Version}

## Getting Started

### 1. Clone and Setup

```bash
git clone {repository-url}
cd {project-name}
{install-command}
```

### 2. Governance Review

Before contributing, review the core entry points:

1. [AGENTS.md](./AGENTS.md) - Provider-neutral routing
2. [CLAUDE.md](./CLAUDE.md) / [GEMINI.md](./GEMINI.md) - Agent-specific context
3. [ARCHITECTURE.md](./ARCHITECTURE.md) - System blueprints

<!-- 
================================================================================
SNIPPET: IMPLEMENTATION (Source Code Layer)
================================================================================
-->

## Available Scripts

| Command            | Description               |
| ------------------ | ------------------------- |
| `npm run dev`      | Start development server  |
| `npm run build`    | Build production artifacts|
| `npm run test`     | Execute test suite        |

## Configuration

### Environment Variables

| Variable       | Required | Description                |
| -------------- | -------- | -------------------------- |
| `DATABASE_URL` | Yes      | Connection string          |
| `API_KEY`      | Yes      | Internal service secret    |

## Testing

```bash
{test-command}
```

<!-- 
================================================================================
SNIPPET: DOCS & GOVERNANCE (Specifications, Rules)
================================================================================
-->

## Documentation Standards

All documents in this folder MUST:

- Use the templates in `templates/`.
- Maintain traceability back to the original `PRD` or `ADR`.
- Include `layer:` metadata for automated routing.

## SSoT References

- [Product Requirements](../prd/)
- [Architecture Decisions](../adr/)
- [Technical Specs](../specs/)

<!-- 
================================================================================
SNIPPET: OPS & UTILS (Scripts, Runbooks)
================================================================================
-->

## Usage Instructions

{Detailed steps on how to execute tools or follow procedures defined in this folder.}

```bash
# Example script execution
./scripts/{script-name}.sh --arg value
```

## Maintenance & Monitoring

- **Log location**: `{log-path}`
- **Alert rules**: Defined in `{monitoring-config}`
- **Incident response**: Refer to [Runbooks](../runbooks/)

---

## License

Copyright (c) 2026. Licensed under the MIT License.
