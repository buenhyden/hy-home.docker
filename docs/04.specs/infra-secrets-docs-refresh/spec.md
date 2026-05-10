---
status: completed
---

# Infra / Secrets / Docs Refresh Specification

## Overview (KR)

이 문서는 `infra/`, `secrets/`, `docs/07.operations/`, `docs/07.operations/`, `docs/07.operations/`, `docs/90.references/`의 실제 파일 내용을 기준으로 운영 문서와 README를 최신화하기 위한 명세다. 목표는 Docker Compose 런타임이나 secret 값 파일을 변경하지 않고, 구현 요소와 운영 문서가 `docs/99.templates/`의 계약을 따르도록 보강하는 것이다.

현재 기준 구조 검증은 통과 상태다. `infra/`에는 47개 Compose 파일과 40개 Compose service directory가 있으며 service README 누락은 0개다. 루트 Compose 활성 include는 14개이므로 보유 Compose와 root-active Compose를 분리해 문서화한다. `secrets/`는 secret/cert 파일명 기준 76개, 루트 Compose 선언 69개, 선언된 secret 누락 0개이며 값은 열람하지 않는다.

## Strategic Boundaries & Non-goals

이 명세는 문서 구조, README 계약, stage 문서 템플릿 적합성, infra/secrets 인벤토리 분석을 소유한다. Docker Compose 서비스 동작 변경, secret 값 열람, 인증서 재생성, agent runtime catalog 변경, 배포 또는 마이그레이션 실행은 범위 밖이다.

## Related Inputs

- **PRD**: 명시적 PRD 없음. 이번 작업은 운영 문서 정합성 보강이다.
- **ARD**: 명시적 ARD 없음. 기존 계층형 `infra/` 구조와 stage docs taxonomy를 따른다.
- **Related ADRs**: 명시적 신규 ADR 없음. 런타임 구조 변경이 없으므로 결정 기록을 추가하지 않는다.

## Contracts

- **Config Contract**: `infra/**/docker-compose*.yml`, config 파일, 루트 `docker-compose.yml`은 분석 대상이며 기본적으로 수정하지 않는다.
- **Data / Interface Contract**: `secrets/**/*.txt` 값은 열람하지 않는다. 파일명, 디렉터리, README, `.example` 파일만 문서화 입력으로 사용한다.
- **Governance Contract**: 새 stage 문서는 대응 템플릿을 따른다. README는 `docs/99.templates/readme.template.md`의 base structure를 따른다.

## Current Baseline

| Area | Baseline |
| --- | --- |
| Infra inventory | 47 Compose files, 40 Compose service directories, 0 missing service README files |
| Root include state | 14 active include files; commented optional and standalone files are not treated as active runtime |
| Secret inventory | 69 root Compose declarations, 76 value/cert filenames, 0 missing declared files |
| Secret classification | `compose-declared`, `bind-mounted-cert`, `registry/local-only`, `private-registry`, `example-registry` |
| README audit | 127 README files, heading gaps 0 |
| Stage audit | 208 non-README docs under `docs/07`, `docs/08`, `docs/09`, `docs/90`, heading gaps 0 |
| Semantic QA | Duplicate legacy/template blocks, non-link references, secret-value wording, and shell-history-sensitive examples are reviewed separately from heading audit |

## Core Design

- **Component Boundary**: 문서 보강 대상은 `README.md`, `docs/04.specs`, `docs/05.plans`, `docs/06.tasks`, `docs/07.operations`, `docs/07.operations`, `docs/07.operations`, `docs/90.references`로 제한한다.
- **Key Dependencies**: `docs/99.templates/`, `docs/00.agent-governance/rules/documentation-protocol.md`, `scripts/check-repo-contracts.sh`, `scripts/check-doc-traceability.sh`, `scripts/validate-docker-compose.sh`.
- **Tech Stack**: Markdown, Docker Compose, Bash validation scripts.

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**: 별도 데이터 저장소를 만들지 않는다. 분석 결과는 이 spec, plan, task 문서와 기존 README/stage 문서에 저장한다.
- **Migration / Transition Plan**: 기존 문서 내용을 삭제하지 않고 누락된 템플릿 섹션을 보강한다. 오래된 문서는 필요한 경우 기존 본문 아래에 template alignment 섹션을 추가한다.

## Interfaces & Data Structures

### Core Interfaces

```text
README base headings:
- Overview
- Audience
- Scope
- Structure
- How to Work in This Area
- Related References or Related Documents

Stage document template families:
- docs/07.operations -> operation.template.md
- docs/07.operations -> operation.template.md
- docs/07.operations -> operation.template.md
- docs/90.references -> reference.template.md
```

## API Contract (If Applicable)

적용되지 않는다. 이번 작업은 외부 API를 제공하지 않는다.

- **API Spec**: 해당 없음
- **Policy**: API Spec을 새로 만들지 않는다.
- **Machine-readable Contract**: 해당 없음

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: Documentation Specialist with Infra/Ops analysis.
- **Inputs**: 템플릿, README, stage docs, infra compose/config 경로, secret 파일명과 example/registry 문서.
- **Outputs**: 템플릿 정합성이 보강된 문서, 분석 spec/plan/task, 검증 결과.
- **Success Definition**: repo checks와 문서 heading audit가 통과하고, secret 값 파일을 열람하지 않은 상태로 작업이 완료된다.

## Tools & Tool Contract (If Applicable)

- **Tool List**: `rg`, `find`, `python3` 기반 문서 audit, repository validation scripts.
- **Permission Boundary**: workspace 내부 문서 파일만 수정한다. secret 값 파일, Docker Compose runtime 파일, agent runtime 파일은 수정하지 않는다.
- **Failure Handling**: 검증 실패 시 실패 파일과 누락 섹션을 task evidence에 기록하고 최소 문서 보강으로 해결한다.

## Prompt / Policy Contract (If Applicable)

- **System / Instruction Contract**: 사용자 지시가 stage 문서 수정 권한을 부여했으므로 `docs/01`~`docs/10`, `docs/90`, `docs/99`의 기본 read-only 정책 예외로 처리한다.
- **Policy Constraints**: 새 active stage 문서는 허용 taxonomy 아래에만 둔다. 비밀값은 응답, 문서, 로그에 노출하지 않는다.
- **Versioning Rule**: 날짜 기반 문서는 `2026-05-09-*` 형식을 따른다.

## Memory & Context Strategy (If Applicable)

- **Short-term Context**: 이번 실행에서 조사한 파일 수, README gap, stage template gap을 task evidence에 보존한다.
- **Long-term Memory**: 별도 memory 파일을 갱신하지 않는다.
- **Retrieval Boundary**: repo-local 파일과 제공된 사용자 계획을 우선한다.

## Guardrails (If Applicable)

- **Input Guardrails**: `secrets/**/*.txt` 값을 읽지 않는다.
- **Output Guardrails**: secret 값, token, private key, 인증서 원문을 문서에 쓰지 않는다.
- **Blocked Conditions**: secret 값 확인, 외부 네트워크 조회, Docker runtime 변경이 필요하면 중단하고 별도 승인을 요청한다.
- **Escalation Rule**: 문서 수정 범위를 넘어 compose/runtime 변경이 필요해지면 plan 업데이트 후 사용자 승인으로 분리한다.

## Evaluation (If Applicable)

- **Eval Types**: structural heading audit, repository contract checks, traceability checks, compose config validation.
- **Metrics**: README missing heading count 0, stage missing heading count 0, repository checks pass, semantic QA findings resolved without runtime or secret value changes.
- **Datasets / Fixtures**: live repository files under target paths.
- **How to Run**: 아래 Verification 명령과 문서 audit를 실행한다.

## Edge Cases & Error Handling

- **README가 기존 커스텀 구조를 가진 경우**: 기존 내용을 유지하고 누락된 base heading만 추가한다.
- **문서명과 infra 디렉터리명이 다른 경우**: rename 없이 README에 alias를 기록한다. `ksql` infra와 `ksqldb` 문서는 이 규칙을 따른다.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: 템플릿 보강이 기존 문서 의미를 바꾸는 경우.
- **Fallback**: 기존 본문을 그대로 둔 채 별도 보강 섹션만 추가한다.
- **Human Escalation**: compose 파일 수정, secret 값 재생성, 문서 taxonomy 변경이 필요하면 별도 승인을 요청한다.

## Verification

```bash
bash scripts/check-repo-contracts.sh
bash scripts/check-doc-traceability.sh
bash scripts/validate-docker-compose.sh
bash scripts/check-template-security-baseline.sh
bash scripts/check-quickwin-baseline.sh
bash scripts/check-all-hardening.sh
git diff --check
```

## Success Criteria & Verification Plan

- **VAL-SPC-001**: 새 stage 문서가 대응 템플릿의 필수 섹션을 포함한다.
- **VAL-SPC-002**: 대상 README가 base heading을 포함한다.
- **VAL-SPC-003**: `docs/07`, `docs/08`, `docs/09`, `docs/90`의 non-README Markdown이 대응 템플릿 heading을 포함한다.
- **VAL-SPC-004**: secret 값 파일을 열람하거나 수정하지 않는다.
- **VAL-SPC-005**: repository validation scripts가 통과한다.
- **VAL-SPC-006**: root-active, optional, standalone, variant Compose 상태를 문서에서 혼동하지 않는다.
- **VAL-SPC-007**: secret 값 확인을 유도하거나 shell history에 민감값을 남길 수 있는 예시를 제거하거나 안전하게 재표현한다.

## Related Documents

- **Plan**: [../../05.plans/2026-05-09-infra-secrets-docs-refresh.md](../../05.plans/2026-05-09-infra-secrets-docs-refresh.md)
- **Tasks**: [../../06.tasks/2026-05-09-infra-secrets-docs-refresh.md](../../06.tasks/2026-05-09-infra-secrets-docs-refresh.md)
- **Guide**: [../../07.operations/README.md](../../07.operations/README.md)
- **Operation**: [../../07.operations/README.md](../../07.operations/README.md)
- **Runbook**: [../../07.operations/README.md](../../07.operations/README.md)
- **References**: [../../90.references/README.md](../../90.references/README.md)
