# Operations — 08 AI

> AI operations documents grouped by stable GPU recovery, Ollama, Open WebUI, hardening, and RAG subjects.

## Overview

This domain co-locates the existing AI service guides, controls, and recovery
procedures under their frozen `ops-0055` through `ops-0059` identities.

## Audience

- Operators, SREs, AI platform engineers, developers, and AI agents.

## Scope

- Existing model-serving usage, AI application controls, RAG workflow guidance,
  hardening boundaries, and recovery procedures.
- No model pull, workload restart, credential access, or new operational role.

## Structure

| Subject | Available documents |
| --- | --- |
| [GPU recovery](./ops-0055-gpu-recovery/runbook.md) | [Runbook](./ops-0055-gpu-recovery/runbook.md) |
| [Ollama](./ops-0056-ollama/guide.md) | [Guide](./ops-0056-ollama/guide.md), [Policy](./ops-0056-ollama/policy.md), [Runbook](./ops-0056-ollama/runbook.md) |
| [Open WebUI](./ops-0057-open-webui/guide.md) | [Guide](./ops-0057-open-webui/guide.md), [Policy](./ops-0057-open-webui/policy.md), [Runbook](./ops-0057-open-webui/runbook.md) |
| [Optimization hardening](./ops-0058-optimization-hardening/guide.md) | [Guide](./ops-0058-optimization-hardening/guide.md), [Policy](./ops-0058-optimization-hardening/policy.md), [Runbook](./ops-0058-optimization-hardening/runbook.md) |
| [RAG workflow](./ops-0059-rag-workflow/guide.md) | [Guide](./ops-0059-rag-workflow/guide.md) |

## How to Work in This Area

Use guides for routine context, policies for control boundaries, and runbooks
for existing executable recovery procedures. Follow each document's safety,
evidence, rollback or recovery, and escalation boundaries.

## Related Documents

- [Operations index](../README.md)
- [AI infrastructure](../../../infra/08-ai/README.md)
- [Guides index](../guides/README.md)
- [Policies index](../policies/README.md)
- [Runbooks index](../runbooks/README.md)
- [Incident records](../incidents/README.md)
