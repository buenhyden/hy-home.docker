---
title: "D06 v9 Ollama and Sandbox Version Recheck Task"
version: "0.1.1"
type: "sdlc/task"
status: "in-progress"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
document_lifecycle: draft
updated: "2026-11-28"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0123"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-11-27"
---

# D06 v9 Ollama and Sandbox Version Recheck Task

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the task payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Scope

##### Objective and Parent

Own criterion180/W196 in the [Spec](../spec.md) and [Plan](../plan.md). Apply
D06 of the v9 task prompts: reuse criteria 174 to 176 (TSK-0118, TSK-0119) and
recheck only what changed after them: Ollama 0.40.16 → 0.40.18 and the
Assistant sandbox 1.8.1 → 1.16.0, whose first sandbox execution SPEC-0212
TSK-0052 records as not run.

##### Inputs and Authority

On 2026-11-27 the user directly requested D06 from
`_workspace/workspace_task_prompts_20261127_progress_v9/` (prompt
`06_ai_ollama_local_cloud_sandbox.md`), limited to that prompt's scope, with
commit, push, PR and merge after checks. Work ran in the primary checkout on
branch `docs/d06-v9-sandbox` from clean `main` `87b83e9ae`; brief
`d06-v9-sandbox` revision 1 bound this Task and the Spec and Plan rows. Direct
user authorization is authority; this record is not.

#### Execution Log

##### Work Performed

###### Census

| Task | Finding | Verdict |
| --- | --- | --- |
| T01 local Ollama | `ollama/ollama:0.40.18` healthy; TSK-0052 records the GPU check (100% GPU, 25/25 layers). From `n8n-worker`, one non-streaming `/api/chat` to `lfm2.5:8b` returned 200, `done` true, with content in 27.3 s including model load | REUSE plus current-version call |
| T02 local-only boundary | `OLLAMA_NO_CLOUD=1` in the Ollama container; the Hermes `local` profile names only `http://127.0.0.1:11434/v1` and has no fallback entry; the separately approved host cloud profile is not changed | REUSE |
| T03 Code Runner | n8n and runners stay 2.46.6, so TSK-0118 E26 holds; the native runner rehearsal pin (2.43.6, E28) stays with D09 | REUSE |
| T04 Assistant sandbox | API and runner 1.16.0 healthy. The inner dockerd (vfs) holds the pinned 1.16.0 sandbox image `sha256:4b48ced7…` plus superseded 1.15.0 `sha256:d5084349…` and 1.8.1 `sha256:b397f4b5…`, 25.9 GB in the runner volume on the HDD | VERIFIED (below); old images to D11 |
| T05 Wiki | No preparation consumer adopted; contract unchanged | REUSE |
| T06 retrieval evaluation | Criterion 176 unchanged | REUSE |

###### Sandbox 1.16.0 boundary probe

One container per inner network ran the pinned 1.16.0 sandbox image by digest
as uid 1000 with `--rm`, a probe label and a 240 s bound. Targets: metadata
`169.254.169.254:80`, the host LAN `192.168.0.13:443`, the router (the host's
default gateway `192.168.0.1:80`), the internet `1.1.1.1:443`, and DNS names
`example.com`, `n8n-worker` and `mng-pg`.

| Network | Metadata | Host LAN | Router | Internet | `example.com` | `n8n-worker`, `mng-pg` | Time |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `runner-bridge` | timeout | timeout | timeout | open | resolves | do not resolve | 56 s |
| `runner-no-egress` | unreachable | unreachable | unreachable | unreachable | does not resolve | do not resolve | 58 s |

This equals TSK-0118 E10 and E15 on 1.8.1. Afterwards no probe container and
no other inner container remained, and the API, runner, Ollama and n8n-worker
were healthy.

###### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0123 | draft | ready | #inputs-and-authority |
| SPEC-0212-TSK-0123 | ready | in-progress | #work-performed |

##### Blockers and Decisions

None that need an owner choice. Removing the superseded inner sandbox images
is cleanup, handed to D11: they are re-pullable by digest, and the runner
uses only the pinned 1.16.0 image.

#### Verification Evidence

##### Results

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E01 | 180 | W196 | method=review; tool=git; command=git diff over infra/08-ai, the n8n Compose file and tech-stack.versions.json since the TSK-0118 record | `main` 87b83e9ae | PASS | Ollama 0.40.18 and sandbox 1.16.0 are the only D06 inputs that changed | required | - |
| E02 | 180 | W196 | method=automated; tool=node in n8n-worker; command=POST `http://ollama:11434/api/chat`, model lfm2.5:8b, stream false, num_predict 8 | HOME Ollama 0.40.18, 2026-11-27 | PASS | 200, done, content present, 27.3 s | required | - |
| E03 | 180 | W196 | method=observation; tool=docker, Python3.12.3; command=OLLAMA_NO_CLOUD in the container; base_url and fallback entries of the Hermes local profile, values only | HOME and server A, 2026-11-27 | PASS | `OLLAMA_NO_CLOUD=1`; loopback only; 0 fallback entries | required | - |
| E04 | 180 | W196 | method=automated; tool=docker inner container; command=python3 reachability and DNS probe on runner-bridge and runner-no-egress with the 1.16.0 sandbox image by digest | HOME runner 1.16.0, 2026-11-27 | PASS | Table above; 0 probe containers left; services healthy | required | - |
| E05 | 180 | W196 | method=observation; tool=docker inside the runner; command=docker image ls --digests; du -sh /var/lib/docker | HOME runner 1.16.0, 2026-11-27 | PASS | Pinned 1.16.0 present; 1.15.0 and 1.8.1 superseded copies; 25.9 GB | optional | - |

##### Resolution Links

None: no row resolves another.

#### Acceptance Decision

##### Criterion Decisions

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 180 | pending | E01,E02,E03,E04 | Awaiting owner acceptance | @buenhyden |

##### Remaining Conditions

- D11: remove the superseded inner sandbox images 1.15.0 and 1.8.1 by digest
  inside `n8n-sandbox-runner-1` and keep the pinned 1.16.0 image.
- D09: the native runner rehearsal pin (TSK-0118 E28) and `d06e12CodeRunner01`
  stay with their owners until the equivalent current scenario is accepted.

#### Handoff

##### Promotion Receipt

None: this Task records verification and routing only.

##### Next Owner

The owner decides criterion 180. D11 owns the inner image cleanup and D09 the
runner rehearsal pin. No other prompt is started automatically.

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
