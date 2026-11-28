---
title: "Ollama on Server B"
version: "1.0.0"
type: "sdlc/architecture-decision"
status: "proposed"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-28"
layer: "architecture"
artifact_id: "ADR-0064"
parent_ids:
- "AD-0008"
created: "2026-11-28"
---

# ADR-0064: Ollama on Server B

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the architecture-decision payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Context

##### Problem and Drivers

HOME ran Ollama as the `ollama` container on server A, whose GPU is a GTX 1060
with 6 GB (compute 6.1). Its CUDA 12 path needs a pinned library selection and
a warm-up entrypoint, and an 8B model leaves little room. Server B
(192.168.0.22, Windows) has an RTX 4060 with 8 GB, already runs Ollama, and
hosts two of its heaviest callers, OpenClaw and blog-data, which reached
server A through a Basic-auth route and a loopback proxy. ComfyUI, the other
GPU user on server A, is no longer used.

- One GPU inference engine for the LAN, on the stronger GPU.
- Callers on server B reach Ollama without a cross-host proxy.
- HOME services keep working with an endpoint change only.
- The embeddings already stored in Qdrant stay valid.

###### Sources
<!-- core-payload-level:4 -->

- [AD-0008](../01.descriptions/0008-ai-architecture.md)
- [REQ-0009](../../01.requirements/0009-ai.md)
- SPEC-0271

##### Decision Scope

This decision covers where Ollama runs and how HOME reaches it. It retires
the HOME `ollama`, `ollama-exporter` and `comfyui` services. It does not
cover models' licences or a future second inference engine.

#### Options

##### Considered Options

- Keep Ollama on server A: rejected; the weaker GPU and the cross-host proxy
  for server B's callers stay.
- Run Ollama on server B behind a Basic-auth proxy: rejected for now; every
  HOME client would need a credential and header support, and the LAN path is
  limited by a host firewall instead.
- Run Ollama on server B, reachable on the LAN only from server A through the
  Windows firewall: selected.

##### Trade-offs

| Option | Benefit | Cost and Risk | Reason |
| --- | --- | --- | --- |
| Keep Ollama on server A | No migration. | The GTX 1060 limits models; server B's callers keep the Basic route and loopback proxy. | Rejected for those costs. |
| Server B behind a Basic-auth proxy | Authenticated LAN calls. | A credential and header support in every HOME client; a proxy to run on Windows. | Rejected for now; the firewall limit is enough on this LAN. |
| Server B, firewall-limited to server A | One engine on the stronger GPU; local calls on server B; HOME changes only an endpoint. | Ollama has no authentication, so the firewall rule is the only limit, and LAN traffic is unencrypted. | Selected. |

- Trade-off: the Windows Defender rule that allows only 192.168.0.13 and
  192.168.0.14 is the only access control.
- Trade-off: HOME no longer manages the Ollama runtime, its version or its
  model store; Stage 05 documents them.

#### Decision

##### Chosen Option

1. Ollama runs natively on server B and listens on `0.0.0.0:11434`; an
   inbound firewall rule allows only server A.
2. HOME services and host programs on server A call
   `http://192.168.0.22:11434`; programs on server B call
   `http://127.0.0.1:11434`.
3. The models are `embeddinggemma-2:740m-q8_0` (embedding),
   `gemma4:e2b` (chat) and `tev1:0.8b-q8_0` (decision). The embedding model
   has the digest HOME used, so stored vectors stay valid.
4. The HOME `ollama` and `ollama-exporter` services, their gateway routes and
   the `ollama-api` credentials are removed, and so is `comfyui`. Their
   setup is kept only as Stage 05 documents.

##### Authority and Effect

Proposed by the owner, @buenhyden, on 2026-11-28 with the SPEC-0271 plan; status
`proposed`. It takes effect when the owner accepts it together with that Spec
and Plan.

#### Consequences

##### Impacts

- Positive: server A's GPU and the Ollama container's hardening exceptions are
  no longer needed.
- Positive: OpenClaw and blog-data on server B call Ollama locally.
- Negative: an Ollama outage on server B stops every model caller in HOME;
  HOME keeps no fallback engine.

##### Follow-up

SPEC-0271 moves each consumer, removes the HOME services and records the
checks.

###### Compliance
<!-- core-payload-level:4 -->

Compose validation and the service contract tests fail if an `ollama` or
`comfyui` service or route remains, or if a HOME consumer still names
`http://ollama:11434`.

## 적용과 확인

### 적용 방법

Use the procedures or reading order stated in the role payload.

### 확인 기준

Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.

## 관계와 출처

### 관련 문서

The role payload retains the current owner and dependency references.

### 외부 근거

External basis and its limits remain those stated in the role payload; a citation grants no authority.
