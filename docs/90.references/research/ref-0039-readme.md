---
status: active
artifact_id: ref-0039
artifact_type: reference
parent_ids: []
observed_at: '2026-07-05'
---

# Reference: Agentic Engineering Research Pack

> `hy-home.docker`의 하네스 엔지니어링, 루프 엔지니어링, provider adapter, SDLC, QA/CI 기준을 정리한 source-backed reference pack

## Overview

`docs/90.references/research/2026-07-05-agentic-research-pack-refresh`는 `hy-home.docker`의 agent-first engineering 체계를 외부 자료와 비교해 읽기 위한 research pack입니다. 이 pack은 현재 저장소의 목적, 역할, CI/CD, QA, Automation, Formatting, 운영 계약, 템플릿, 스크립트, 통합 가이드, SDLC, 거버넌스, 체계, 규칙을 repo-local evidence로 정리하고, 하네스/루프/스펙 주도 개발/품질 게이트/provider 구현 현황을 외부 source와 연결합니다.

이 pack은 active policy가 아닙니다. 발견된 개선점은 `Potential Follow-up / Gap`으로 남기며, 실제 정책이나 실행 계획 변경은 별도 승인된 canonical stage 문서에서 다룹니다.

## Purpose

`docs/90.references/research/2026-07-05-agentic-research-pack-refresh`는 하네스 엔지니어링과 루프 엔지니어링을 중심으로 한 agent-first workspace research pack입니다. 이 category는 현재 provider/runtime/governance 상태를 설명하는 보조 reference이며, Stage 00 policy, Stage 04 execution evidence, Stage 05 operations procedure를 대체하지 않습니다.

## Repository Role

This stable leaf is the canonical navigation and evidence boundary for the
agentic engineering research pack; it does not own policy or execution state.

### Consolidation and Lifecycle Boundary

- 이 2026-07-05 pack은 현재 agentic engineering research의 **유일한 active canonical pack**입니다.
- 검증된 2026-07-07 자료는 책임이 분명한 이 pack의 canonical 문서에 한 번만 반영했습니다. 2026-07-07 duplicate pack은 redirect stub만 남은 상태로 제거되었고, 경로 mapping은 [research references](README.md)의 Superseded Paths 표가 대신합니다.
- 이전에 완료된 Stage 03 research refresh spec, Stage 04 plan, Stage 04 task evidence, [2026-07-05 implementation audit](../audits/ref-0019-readme.md), [2026-07-07 audit update](../audits/ref-0033-readme.md)는 삭제하거나 본문을 복제하지 않고 historical evidence로 유지합니다.
- Stage 90은 source-backed comparison과 routing을 제공할 뿐입니다. 현재 policy는 Stage 00/05 policy 문서, execution evidence는 Stage 04, runtime truth는 tracked provider/Compose/script/config surface가 계속 담당합니다.
- 2026-07-13 document-contract 연구는 이 canonical pack의 관련 leaf만 in-place로 재검증했습니다. 별도 날짜 pack이나 dated audit snapshot을 만들거나 다시 쓰지 않았습니다.

### Current Implementation Reconciliation

2026-07-27 canonical reconciliation 결과를 이 pack의 구현 비교에 반영했습니다.
Stage 00은 14개 role, 24개 function, 3개 provider와 4개 role projection surface를
typed contract로 소유합니다. 생성기는 Claude, Codex, Gemini native adapter와
공유 `.agents` compatibility adapter를 분리하며, provider sync는 3개
provider에서 drift 0을 보고합니다. 7개 semantic hook event, 8개 harness layer,
8개 ordered workflow state, 4개 typed loop, 11개 fixture와 16개 synthetic
regression도 tracked validation owner에 연결되어 있습니다. 외부 capability
intake는 source date가 2026-07-26인 9개 merge/defer 결정으로 고정됩니다.

QA/CI tracked source는 7개 workflow와 23개 job, `ci-quality.yml`의 16개 quality
job, 24개 pre-commit hook, 그리고 typed gate registry가 소유하는 3개 local
profile의 script-backed QA step입니다. profile별 step 수는 기본
(`local-script-backed`) 34개, `local-all-profiles` 35개, `local-harness` 32개이며
`python3 scripts/validation/run-ci-gate.py --profile <p> --list`로 재현합니다.
Controlled all-files wrapper는
별도 승인된 최종 evidence gate이므로 이 step 수에 포함하지 않습니다. 이
구현 정합화에 따라 canonical audit 분포는 161개 criterion 중 Implemented 77,
Partial 60, Missing 13, Not Applicable 2, Needs Revalidation 9입니다.

이 수치는 tracked definition과 deterministic test 깊이만 설명합니다. provider
CLI의 live acceptance, 모델 entitlement/actual availability, remote required-check
enforcement, CD·deployment·rollback은 별도 관찰 또는 승인이 없으므로 계속
Partial 또는 Needs Revalidation 경계에 둡니다. 모델의 historical cutoff는
2026-07-10 10:00 KST이고 typed current registry의 retrieval boundary는
2026-07-26T20:08:18+09:00이며, 공식 외부 source 재검증은
2026-07-27T02:33:54+09:00에 별도 수행했습니다. 현재 model policy는
5개 exact work profile과 11개 model record를 가지며 active fallback graph나
implicit substitution을 허용하지 않습니다.

2026-07-19 target-surface wave의 현재 저장소 근거도 같은 경계로 반영했습니다.
root Vault/content와 Stage 98 SDLC archive는 별도 profile로 분류되고, canonical
manifest promotion 후보는 483행(삭제 3, 이관 10, 보존 470)이며 전체가 독립
검토를 거친 `pass/pass`입니다. InfluxDB 2, OpenSearch `.example`, SeaweedFS
`security.toml`의 destructive evidence는 별도 검토를 유지합니다. SeaweedFS의 유지된 `.example`은 현재 Compose에
mount되지 않으며 활성화는 별도 승인 runtime 작업입니다. 로컬 workflow
contract의 품질 job은 16개입니다. 최신 read-only remote observation은
2026-07-26T18:22:32+09:00 public metadata에서 remote default commit
`a897978f`, 실패한 run `29777690571`, 15개 observed job, root cause
`unverified`, GitHub-managed workflow 3개를 기록했습니다. authenticated
ruleset/branch-protection/environment/secret/variable readback은 없으므로 remote
control plane은 계속 `unverified`이며, 2026-07-12 classic-protection 기록을
현재 enforcement 증거로 사용하지 않습니다. 이 정합화는 service startup,
remote mutation, secret value inspection 또는 deployment 증거를 포함하지
않습니다.

2026-07-19에는 GitHub workflow syntax·secure use·deployments/environments·rulesets,
pre-commit, DORA metrics, Docker Compose include·profiles·secrets·trust model,
SLSA v1.2, NIST SP 800-61 Rev. 3의 정확한 공식 URL만 다시 열었습니다. 재개방한
범위에서 낡은 외부 주장은 확인되지 않았습니다. 그 밖의 안정적·저위험 출처는
기존 retrieval 날짜와 caveat를 유지하며, provider model cutoff도 변경하지
않습니다.

2026-07-27에는 Anthropic model/ID/effort/subagent/memory, OpenAI
model/latest-model/Codex manual, Gemini model/subagent/generation/memory/hook,
GitHub secure-use/monitoring/ruleset, zizmor v1.28.0 advisory/release, 그리고
`agency-agents` immutable pin의 README·`tools.json`·integration·MIT license를
다시 확인했습니다. 이 현재 관찰은 2026-07-26 typed contract의 timestamp를
소급 변경하거나 2026-07-10 historical model ledger를 재작성하지 않습니다.

2026-08-07에는 pack을 세 개 leaf로 확장하고 기존 15개 leaf를 저장소 사실과
외부 source 양쪽으로 재검증했습니다. 확인된 변경은 다음과 같습니다. Codex가
`SessionEnd`를 포함한 11개 hook event를 공식 문서화했으므로 tracked 6-mapping
Codex binding은 provider 한계가 아니라 repository-side gap으로 재분류했습니다.
Claude는 31개, Gemini는 `Notification`을 포함한 11개 event를 문서화합니다.
Gemini subagent 파일 schema에는 reasoning/thinking 필드가 없으므로 기존
per-agent effort 서술을 settings/API 수준으로 정정했습니다. Local QA runner의
script-backed step은 helper 두 개가 누락되어 있었고, 당시 runner source에서 다시
계산한 결과는 기본 24개와 harness 22개였습니다. 이 두 수치는 runner가 typed gate
registry로 재구성된 뒤 2026-08-10 재검증에서 34/32로 대체되었으며, 아래 2026-08-10
문단이 현재 값을 기록합니다. `actions/attest@v4` 권한 집합과
immutable release attestation을 반영했고, redirect된 provider URL 4개를
교체했습니다. ISO catalog(403), Diataxis(429), editorconfig spec(429),
OpenAI practical guide(403), pytest fixtures(429)는 이번 재검증에서 다시 열지
못했으므로 반증이 아니라 미재검증으로 표시했습니다. 이 재검증은 2026-07-10
model cutoff, 2026-07-26 typed contract timestamp, `unverified` 상태를
변경하지 않습니다.

2026-08-10에는 leaf 두 개를 추가하고 workspace-derived 수치만 재검증했습니다.
외부 source는 2026-08-07 검증 결과를 유지하며, 새 leaf가 인용하는 자료만
2026-08-10에 새로 조회했습니다. 확인된 사실은 다음과 같습니다. 검사한 13개
수치 중 11개가 그대로 일치했고, 두 가지가 drift했습니다. Local QA runner가
typed gate registry로 재구성되면서 profile이 2개에서 3개로 늘고 step 수는
기본 34개, `local-all-profiles` 35개, `local-harness` 32개가 되었습니다.
그리고 semantic-event binding 21개 중 20개만 `configured-not-executed`이며
Codex `session-end` binding은 `unsupported`이므로, "21개 전부"라는 서술
4곳을 정정했습니다. 새 leaf 두 개는 Verification/Validation 구분과 GitHub
Actions 플랫폼 메커니즘을 다루며, 후자는 automation leaf의 tracked inventory를
복제하지 않고 미채택 capability 대조만 추가합니다. 이 확장은 2026-07-10 model
cutoff, 2026-07-26 typed contract timestamp, `unverified` 상태를 변경하지
않습니다. ISO 표준 본문은 `iso.org`가 자동 조회에 403을 반환하고 공개 표준
페이지가 유료 webstore로 이전되어 이번에도 열지 못했으므로, 해당 정의는
인용하지 않고 미재검증으로 남겼습니다.

### Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- repo-local workspace baseline 분석
- 하네스 엔지니어링 구성 요소 분석
- 루프 엔지니어링과 feedback loop 분석
- spec-driven development와 SDLC 분석
- document metadata, lifecycle, agent instruction, safe vibe-coding criteria 분석
- CI/CD, QA, formatting, quality gate 분석
- Docker Compose, infrastructure harness, security governance, automation, pipeline, workflow 분석
- Claude, Codex, Gemini provider 구현 비교
- 공통 provider-neutral 환경과 규칙을 만들기 위한 요소 정리
- 외부 AI agent catalog 패턴과 repo-local agent catalog 비교 분석
- Diataxis 기준 문서 architecture와 quadrant 커버리지 분석
- LLM-WIKI 체계, 생성 방식, freshness/safety 계약 분석
- 단기/장기/영역별 memory tier와 promotion/retention/eviction 분석
- Verification과 Validation의 표준 구분과 저장소 gate/test/승인 표면 분류
- GitHub Actions 플랫폼 메커니즘과 미채택 capability 대조

### Out of Scope

- `docs/00.agent-governance/` 정책 직접 변경
- `docs/03.specs/`, `docs/04.execution/`, `docs/05.operations/` 후속 보완
- runtime provider 설정 변경
- secret 값, credential, token, private key, shell history, raw log

## Definitions / Facts

```text
2026-07-05-agentic-research-pack-refresh/
├── README.md                            # This file
├── workspace-baseline.md                # Repo-local purpose, roles, gates, contracts
├── harness-engineering.md               # Harness components and application analysis
├── loop-engineering.md                  # Agent/eval/CI/human feedback loop analysis
├── spec-driven-sdlc.md                  # Spec-driven development and SDLC mapping
├── sdlc-document-roles.md               # Role and purpose of each SDLC/operations document type
├── document-metadata-lifecycle.md        # Typed metadata and semantic lifecycle criteria
├── agent-instructions-vibe-coding.md     # Agent instruction and safe vibe-coding criteria
├── quality-ci-formatting.md             # QA, CI/CD, formatting, secure quality gates
├── provider-implementation-comparison.md # Claude, Codex, Gemini comparison
├── provider-model-landscape.md           # Cutoff-bound official provider model catalog and lifecycle evidence
├── agent-model-selection.md              # Task-characteristic model tier and reasoning-effort selection
├── docker-compose-infrastructure.md      # Docker Compose and infrastructure harness analysis
├── security-governance.md                # Secure SDLC and security governance analysis
├── automation-pipeline-workflow.md       # Automation, pipeline, and workflow analysis
├── github-actions-platform.md            # GitHub Actions platform mechanics and unadopted capability
├── verification-validation.md            # V&V standards distinction and repository gate classification
├── ai-agent-catalogs.md                  # External agent catalog vs curated catalog analysis
├── documentation-architecture.md         # Diataxis quadrant mapping and mode-mixing findings
├── llm-wiki-system.md                    # LLM Wiki structure, generation, and enforcement
├── memory-hierarchy.md                   # Short-term, long-term, and domain memory analysis
└── scope-application-matrix.md           # Per-scope view of the pack and scope reachability
```

## Sources

- [workspace-baseline.md](ref-0058-workspace-baseline.md) - workspace 목적, 역할, CI/CD, QA, Automation, 운영 계약, 템플릿, 스크립트, SDLC, 거버넌스 baseline
- [harness-engineering.md](ref-0047-harness-engineering.md) - test/eval/runtime harness와 저장소 적용 요소 분석
- [loop-engineering.md](ref-0049-loop-engineering.md) - agent loop, eval loop, CI loop, human approval loop 분석
- [spec-driven-sdlc.md](ref-0057-spec-driven-sdlc.md) - spec-driven development, SDLC, traceability 분석
- [sdlc-document-roles.md](ref-0055-sdlc-document-roles.md) - PRD, ARD, ADR, spec/children, plan, task, guide, policy, runbook, incident, postmortem, Release의 분리된 역할과 Release/deployment evidence 경계 분석
- [document-metadata-lifecycle.md](ref-0045-document-metadata-lifecycle.md) - consumer-specific typed metadata, deterministic serialization, artifact identity, parent/supersession, freshness, lifecycle, README/generated-document, staged enforcement 기준
- [agent-instructions-vibe-coding.md](ref-0040-agent-instructions-vibe-coding.md) - instruction authority/context/tools/permissions, generated-code ownership/review, debt/escalation, safe vibe-coding 경계
- [quality-ci-formatting.md](ref-0053-quality-ci-formatting.md) - CI/CD, QA, formatting, secure quality gate, tracked check와 remote required-check/ruleset 경계 분석
- [provider-implementation-comparison.md](ref-0051-provider-implementation-comparison.md) - Claude, Codex, Gemini provider 현황과 공통 체계 분석
- [provider-model-landscape.md](ref-0052-provider-model-landscape.md) - 2026-07-10 10:00 KST cutoff 기준 Claude, OpenAI/Codex, Gemini 공식 model catalog, lifecycle, ID, source caveat 분석
- [agent-model-selection.md](ref-0041-agent-model-selection.md) - 작업 특성에 맞는 모델 tier와 reasoning-effort 선택, per-provider 메커니즘, 변경 프로토콜 분석
- [docker-compose-infrastructure.md](ref-0044-docker-compose-infrastructure.md) - Docker Compose, infrastructure harness, profiles, networks, secrets, validation, hardening 분석
- [security-governance.md](ref-0056-security-governance.md) - secure SDLC reference frameworks, workflow security, secret boundaries, approval evidence 분석
- [automation-pipeline-workflow.md](ref-0043-automation-pipeline-workflow.md) - automation, pipeline, workflow loop, provider hook, Release/deployment, local/CI/remote enforcement boundary 분석
- [github-actions-platform.md](ref-0084-github-actions-platform.md) - GITHUB_TOKEN scope 모델, OIDC claim/subject, reusable workflow와 composite action, script injection과 privileged trigger, SHA pinning/attestation/immutable release, concurrency·matrix·cache, ruleset read-back 경계, runner 모델, 그리고 저장소가 채택하지 않은 capability 대조
- [verification-validation.md](ref-0085-verification-validation.md) - IEEE 1012 기준 Verification/Validation 구분, 기법으로서의 testing 위치, 비결정성 아래의 V&V, 16개 job root와 24개 test와 승인 게이트의 분류, tracked label의 용어 표류
- [ai-agent-catalogs.md](ref-0042-ai-agent-catalogs.md) - agency-agents 같은 외부 agent catalog 패턴과 repo-local curated catalog, import 경계 분석
- [documentation-architecture.md](ref-0046-documentation-architecture.md) - Diataxis 4분면과 저장소 문서 타입 매핑, 미충족 quadrant, template mode-mixing 분석
- [llm-wiki-system.md](ref-0048-llm-wiki-system.md) - LLM Wiki artifact 구조, 생성/freshness/safety 계약, 외부 convention 비교
- [memory-hierarchy.md](ref-0050-memory-hierarchy.md) - 단기/장기/영역별 memory tier, provider memory 메커니즘, promotion/retention/eviction 분석
- [scope-application-matrix.md](ref-0054-scope-application-matrix.md) - 14개 scope별 적용 범위, live/흡수/vestigial 판정, scope-to-workspace 소유 매핑, scope별 adoption boundary

### Reading Order

1. [workspace-baseline.md](ref-0058-workspace-baseline.md)에서 이 저장소의 현재 체계를 먼저 확인합니다.
2. [harness-engineering.md](ref-0047-harness-engineering.md)와 [loop-engineering.md](ref-0049-loop-engineering.md)에서 개념적 구조를 확인합니다.
3. [spec-driven-sdlc.md](ref-0057-spec-driven-sdlc.md)에서 stage-gate를, [sdlc-document-roles.md](ref-0055-sdlc-document-roles.md)에서 문서 역할을, [document-metadata-lifecycle.md](ref-0045-document-metadata-lifecycle.md)에서 metadata/lifecycle 기준을 확인합니다.
4. Pack leaf metadata는 stable `artifact_id`와 direct `parent_ids`를 통해
   Spec 123에 연결하며, 이 README는 folder-index 예외로 유지합니다.
5. [agent-instructions-vibe-coding.md](ref-0040-agent-instructions-vibe-coding.md)에서 instruction/vibe 기준을 확인하고 [quality-ci-formatting.md](ref-0053-quality-ci-formatting.md)에서 실제 QA evidence surface를 확인합니다. gate 커버리지를 주장하기 전에 [verification-validation.md](ref-0085-verification-validation.md)에서 각 gate가 실제로 답하는 질문을 확인합니다.
6. [docker-compose-infrastructure.md](ref-0044-docker-compose-infrastructure.md), [security-governance.md](ref-0056-security-governance.md), [automation-pipeline-workflow.md](ref-0043-automation-pipeline-workflow.md)에서 targeted reference를 확인합니다. workflow를 변경하기 전에는 [github-actions-platform.md](ref-0084-github-actions-platform.md)에서 플랫폼 규칙을 먼저 확인합니다.
7. [provider-implementation-comparison.md](ref-0051-provider-implementation-comparison.md)에서 Claude, Codex, Gemini adapter 차이를 확인하고, [provider-model-landscape.md](ref-0052-provider-model-landscape.md)에서 cutoff-bound 공식 model/lifecycle evidence를 확인한 뒤 [agent-model-selection.md](ref-0041-agent-model-selection.md)에서 작업 특성에 맞는 model tier와 reasoning-effort 분석을 읽습니다.
8. [ai-agent-catalogs.md](ref-0042-ai-agent-catalogs.md)에서 외부 agent catalog와 repo-local catalog의 import 경계를 확인합니다.
9. [documentation-architecture.md](ref-0046-documentation-architecture.md)에서 Diataxis 기준 문서 구조를, [llm-wiki-system.md](ref-0048-llm-wiki-system.md)에서 machine-facing navigation surface를, [memory-hierarchy.md](ref-0050-memory-hierarchy.md)에서 memory tier 구조를 확인합니다.
10. 특정 layer에서 작업할 때는 [scope-application-matrix.md](ref-0054-scope-application-matrix.md)에서 해당 scope에 적용되는 leaf와 workspace 소유 범위를 먼저 확인합니다. 이 문서는 주제축이 아닌 scope축 진입점이며, 형제 leaf를 종합하되 수정하지 않습니다.

## Maintenance

1. 이 pack의 문서는 active policy가 아니라 reference라는 경계를 유지합니다.
2. 최신 provider 기능을 인용할 때는 공식 문서를 다시 확인합니다.
3. 새 non-README reference는 closed-surface contract에 맞춰 영어로 작성합니다.
4. repo-local 사실은 root README, Stage 00 governance, provider notes, scripts, CI workflow에서 확인합니다.
5. 다른 stage 수정이 필요하면 이 pack에서 직접 고치지 않고 gap으로 기록합니다.
6. 새 문서를 추가하면 이 README와 상위 [research README](README.md)를 갱신합니다.
7. 변경 후 `bash scripts/validation/check-repo-contracts.sh`를 실행합니다.
8. normative 외부 claim은 primary source의 direct URL과 access date를 남기고, mutable guidance와 fixed standard를 구분합니다.

## Related Documents

- [research references](README.md)
- [90.references](../README.md)
- [agent governance hub](../../00.agent-governance/README.md)
- [HAFE specification](../../03.specs/spec-0094-harness-agent-first-engineering/spec.md)
- [HAFE operations guide](../../05.operations/00-workspace/ops-0004-harness-agent-first-engineering/guide.md)
- [HAFE operations policy](../../05.operations/00-workspace/ops-0004-harness-agent-first-engineering/policy.md)
