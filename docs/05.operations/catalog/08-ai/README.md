---
title: Operations — 08 AI
type: operation/domain-readme
layer: operations
owner: "@buenhyden"
---

# Operations — 08 AI

> AI operations documents grouped by stable GPU recovery, Ollama, Open WebUI, hardening, and RAG subjects.

## Overview

This domain co-locates the existing AI service guides, controls, and recovery
procedures under their current four-digit subject directories.

## Audience

- Operators, SREs, AI platform engineers, developers, and AI agents.

## Scope

- Existing model-serving usage, AI application controls, RAG workflow guidance,
  hardening boundaries, and recovery procedures.
- No model pull, workload restart, credential access, or new operational role.

## Structure

| Subject | Available documents |
| --- | --- |
| [GPU recovery](0055-gpu-recovery/runbook.md) | [Runbook](0055-gpu-recovery/runbook.md) |
| [Ollama](0056-ollama/guide.md) | [Guide](0056-ollama/guide.md), [Policy](0056-ollama/policy.md), [Runbook](0056-ollama/runbook.md) |
| [Open WebUI](0057-open-webui/guide.md) | [Guide](0057-open-webui/guide.md), [Policy](0057-open-webui/policy.md), [Runbook](0057-open-webui/runbook.md) |
| [Optimization hardening](0058-optimization-hardening/guide.md) | [Guide](0058-optimization-hardening/guide.md), [Policy](0058-optimization-hardening/policy.md), [Runbook](0058-optimization-hardening/runbook.md) |
| [RAG workflow](0059-rag-workflow/guide.md) | [Guide](0059-rag-workflow/guide.md) |

## How to Work in This Area

Use guides for routine context, policies for control boundaries, and runbooks
for existing executable recovery procedures. Follow each document's safety,
evidence, rollback or recovery, and escalation boundaries.

## Related Documents

- [Operations index](../../README.md)
- [AI infrastructure](../../../../infra/08-ai/README.md)
- [Guides index](../../README.md)
- [Policies index](../../README.md)
- [Runbooks index](../../README.md)
- [Incident records](../../incidents/README.md)
