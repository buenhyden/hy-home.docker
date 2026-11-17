---
title: "Open WebUI Operations Policy"
version: "1.2.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "operations"
artifact_id: "POL-0057"
parent_ids:
- "AD-0008"
created: "2026-05-17"
next_review_at: "2027-05-13"
---

# Open WebUI Operations Policy

## Purpose and Scope

### Objective

이 문서는 독립 LAB `labs/open-webui/docker-compose.yml`로 옮긴 Open WebUI의 운영 정책을 정의한다
(ADR-0062, 2026-11-10 owner 개정). 인증, LAB 경계, data와 secret 취급, 구성 변경 승인을 통제한다.

#### Authority

- Declared parent: [AI Infrastructure Architecture Description](../../../02.architecture/descriptions/0008-ai-architecture.md) (`AD-0008`)
- Governing decision: [ADR-0062](../../../02.architecture/decisions/0062-home-lab-membership.md)
- 런타임 고정값은 Compose/Dockerfile 선언이 소유하며 [파생 이미지 목록](../../../../infra/tech-stack.versions.json)은 드리프트 검증에 사용한다.

### Applies To

- **Systems**: LAB `open-webui`(profile `lab-open-webui`), 그 LAB data root(SQLite·로컬 vector store·upload·session key),
  LAB 전용 OIDC client secret, 승인된 Ollama endpoint와 Keycloak client `home-openwebui`. HOME에 남은
  컨테이너 `open-webui`와 volume `hy-home-infra_open-webui`는 퇴역 승인 전까지 이 정책의 data 보존 규칙을 따른다.
- **Environments**: LAB 실험. HOME 사용은 [POL-0107](0107-lab-promotion.md) 승격으로만 돌아온다.

#### Exclusions

없음: 이 정책 본문에는 명시된 제외 대상이 없다.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0057-R1 | 항상 | 필수: LAB은 root에 include하지 않고 HOME network에 합류하지 않으며 gateway route를 두지 않고 UI는 `LAB_HOST_BIND_IP`에만 게시하며 기동/종료는 `python3 scripts/operations/lab.py` lease 안에서만 한다 | `bash scripts/hardening/check-all-hardening.sh 08-ai` / `python3 scripts/operations/lab.py check open-webui` / lease 안 health 확인 | 변경 티켓(PR)/검증 로그/롤백 결과 |
| POL-0057-R2 | 항상 | 필수: native Keycloak OIDC(`home-openwebui`, PKCE S256)만 쓰고 password login/signup/email merge/OAuth role-group 관리/trusted-header 인증은 끈다 | `bash scripts/hardening/check-all-hardening.sh 08-ai` / `python3 scripts/operations/lab.py check open-webui` / lease 안 health 확인 | 변경 티켓(PR)/검증 로그/롤백 결과 |
| POL-0057-R3 | 항상 | 필수: OIDC client secret은 `LAB_SECRET_DIR` 아래 LAB 전용 파일(`LAB-037`)로만 받고 HOME secret 파일/OpenBao Agent 출력을 LAB에 bind하지 않는다 | `bash scripts/hardening/check-all-hardening.sh 08-ai` / `python3 scripts/operations/lab.py check open-webui` / lease 안 health 확인 | 변경 티켓(PR)/검증 로그/롤백 결과 |
| POL-0057-R4 | 항상 | 필수: `ENABLE_OPENAI_API=false`를 유지하고 cloud 경로는 키/예산/데이터 계약 승인 후에만 연다 | `bash scripts/hardening/check-all-hardening.sh 08-ai` / `python3 scripts/operations/lab.py check open-webui` / lease 안 health 확인 | 변경 티켓(PR)/검증 로그/롤백 결과 |
| POL-0057-R5 | 변경 시 | 필수: `LAB_OPEN_WEBUI_OLLAMA_BASE_URL`/`RAG_EMBEDDING_MODEL` 변경과 `VECTOR_DB` 도입은 사전 영향 검토와 재색인 계획이 필요하다 | 수동 | 변경 티켓(PR) |
| POL-0057-R6 | lease 안 작업 시 | 허용: lease 안의 문서 업로드/재인덱싱/삭제와 승인된 범위의 모델 파라미터 조정 | 수동 | none |
| POL-0057-R7 | 항상 | 금지: LAB을 root include/HOME profile로 선택, 승인 없는 SSO 우회/password-signup 활성화, HOME volume을 LAB data root로 지정하거나 승인 없이 HOME data 복사/삭제 | `bash scripts/hardening/check-all-hardening.sh 08-ai` / `python3 scripts/operations/lab.py check open-webui` / lease 안 health 확인 | 검증 로그 |
| POL-0057-R8 | lifecycle 단계 | 필수: SQLite/upload/vector/session key와 OIDC secret을 한 복구 경계로 취급하고 보존이 필요한 data는 lease 종료 전 별도 승인으로 백업하며 HOME 퇴역은 단계별 별도 승인과 일관 backup이 선행하고 upgrade에는 복구 copy/migration 검토/rollback 근거가 필요하다 | 수동 | 변경 티켓(PR)/롤백 결과 |

- **Required**:
  - LAB은 root에 include하지 않고 HOME network에 합류하지 않으며 gateway route를 두지 않는다. UI는
    `LAB_HOST_BIND_IP`에만 게시한다. 기동·종료는 `python3 scripts/operations/lab.py`의 lease 안에서만 한다.
  - native Keycloak OIDC(`home-openwebui`, PKCE S256)만 쓴다. password login, signup, email merge,
    OAuth role/group 관리와 trusted-header 인증은 꺼 둔다.
  - OIDC client secret은 `LAB_SECRET_DIR` 아래 LAB 전용 파일(`LAB-037`)로만 받는다. HOME secret 파일이나
    OpenBao Agent 출력을 LAB에 bind하지 않는다.
  - `ENABLE_OPENAI_API=false`를 유지한다. Cloud 경로는 키·예산·데이터 계약 승인 후에만 연다.
  - `LAB_OPEN_WEBUI_OLLAMA_BASE_URL`, `RAG_EMBEDDING_MODEL` 변경과 `VECTOR_DB` 도입은 사전 영향 검토와
    재색인 계획이 필요하다.
- **Allowed**:
  - lease 안의 문서 업로드·재인덱싱·삭제와 승인된 범위의 모델 파라미터 조정.
- **Disallowed**:
  - LAB을 root include하거나 HOME profile로 선택하는 것.
  - 승인 없는 SSO 우회, password/signup 경로 활성화.
  - HOME volume을 LAB data root로 지정하거나 승인 없이 HOME data를 복사·삭제하는 것.

#### Lifecycle and data controls

- SQLite·upload·로컬 vector·session key와 맞는 OIDC secret을 한 복구 경계로 취급한다. HOME Restic은 LAB
  data를 백업하지 않으므로 보존이 필요한 실험 data는 lease 종료 전에 별도 승인으로 백업한다.
- HOME 퇴역(컨테이너 정지·제거, volume 이전 또는 삭제, Keycloak client·redirect, DNS 정리)은 각각 별도
  승인 단계이며 쓰기를 멈춘 일관 backup이 선행한다.
- Upgrade에는 복구 가능한 copy, migration 검토, image identity와 rollback 근거가 필요하다.

### Exceptions

#### Exception Conditions

- LAB lease 안에서 SSO 우회를 검토해야 하면 loopback 게시, 명시 승인, lease 종료 즉시 복구가 필수다.

#### Approval and Review

- **Quarterly**: 정책/권한/데이터 취급 기준 검토
- **Per Release**: 모델/임베딩/연동 구성 변경 시 사전 검토

## Enforcement

### Mechanisms

- 배포 전 체크:
  - `bash scripts/hardening/check-all-hardening.sh 08-ai`
  - `python3 scripts/operations/lab.py check open-webui`
  - lease 안에서 `open-webui` container-internal health와 승인된 Ollama endpoint 연결성 확인
- 운영 중 체크:
  - 인증 실패율, 5xx 비율, 인덱싱 실패율 모니터링
- 증적:
  - 변경 티켓(또는 PR), 검증 로그, 롤백 결과

### Limits

배포 전 체크 세 가지가 이름 붙은 검사이며, 아래 항목은 기계적으로 강제되지 않는다.

- 운영 중 체크(인증 실패율, 5xx 비율, 인덱싱 실패율)는 모니터링 항목이며 이름 붙은 게이트나 임계값이 없다.
- HOME 퇴역, upgrade 복구 copy, lease 종료 전 백업은 별도 승인 단계의 수동 검토에 의존한다.
- cloud 경로 개방과 모델/임베딩 변경의 사전 영향 검토는 수동이다.
- 분기별 정책 검토와 릴리스별 사전 검토도 수동이다.

## Ownership

### Owner

책임 소유자는 **@buenhyden**이다. 예외·통제 변경에는 기존 범위별 승인 기록이 필요하며 문서 수정은 승인 근거가 아니다. 통제 실패나 복구 증거 누락은 수용을 중단하고 정제된 증거로 에스컬레이션한다.

### Review Triggers

- Subject peers: [Guide](../../guides/15-labs/0057-open-webui.md) (`GDE-0057`), [Runbook](../../runbooks/15-labs/0057-open-webui.md) (`RUN-0057`)
- [Operations index](../../README.md)
- [Usage guide](../../guides/15-labs/0057-open-webui.md)
- [Recovery runbook](../../runbooks/15-labs/0057-open-webui.md)
