---
title: "Open WebUI Operations Policy"
version: "2.0.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
layer: "operations"
artifact_id: "POL-0057"
parent_ids:
- "AD-0008"
created: "2026-05-17"
next_review_at: "2027-05-13"
---

# Open WebUI Operations Policy

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the policy payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Purpose and Scope

##### Objective

이 문서는 독립 LAB `labs/open-webui/docker-compose.yml`로 옮긴 Open WebUI의 운영 정책을 정의한다
(ADR-0062, 2026-11-10 owner 개정). 인증, LAB 경계, data와 secret 취급, 구성 변경 승인을 통제한다.

###### Authority
<!-- core-payload-level:4 -->

- Declared parent: [AI Infrastructure Architecture Description](../../../02.architecture/01.descriptions/0008-ai-architecture.md) (`AD-0008`)
- Governing decision: [ADR-0062](../../../02.architecture/02.decisions/0062-home-lab-membership.md)
- 런타임 고정값은 Compose/Dockerfile 선언이 소유하며 [파생 이미지 목록](../../../../infra/tech-stack.versions.json)은 드리프트 검증에 사용한다.

##### Applies To

- **Systems**: LAB `open-webui`(profile `lab-open-webui`), 그 LAB data root(SQLite·로컬 vector store·upload·session key),
  LAB 전용 OIDC client secret, 승인된 Ollama endpoint와 Keycloak client `home-openwebui`. HOME에 남은
  컨테이너 `open-webui`와 volume `hy-home-infra_open-webui`는 퇴역 승인 전까지 이 정책의 data 보존 규칙을 따른다.
- **Environments**: LAB 실험. HOME 사용은 [POL-0107](0107-lab-promotion.md) 승격으로만 돌아온다.

###### Exclusions
<!-- core-payload-level:4 -->

없음: 이 정책 본문에는 명시된 제외 대상이 없다.

#### Rules

##### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0057-R1 | 항상 | 금지: LAB의 root include, HOME network 합류, gateway route 설치 | none | none |
| POL-0057-R2 | 항상 | 필수: UI는 `LAB_HOST_BIND_IP`에만 게시한다 | none | none |
| POL-0057-R3 | 기동/종료 시 | 필수: `python3 scripts/operations/lab.py`의 lease 안에서만 기동/종료한다 | none | none |
| POL-0057-R4 | 항상 | 필수: native Keycloak OIDC(`home-openwebui`, PKCE S256)만 쓴다 | none | none |
| POL-0057-R5 | 항상 | 필수: password login, signup, email merge, OAuth role/group 관리, trusted-header 인증을 끈다 | none | none |
| POL-0057-R6 | 항상 | 필수: OIDC client secret은 `LAB_SECRET_DIR` 아래 LAB 전용 파일(`LAB-037`)로만 받는다 | none | none |
| POL-0057-R7 | 항상 | 금지: HOME secret 파일이나 OpenBao Agent 출력을 LAB에 bind | none | none |
| POL-0057-R8 | 항상 | 필수: `ENABLE_OPENAI_API=false`를 유지한다 | none | none |
| POL-0057-R9 | cloud 경로를 열 때 | 필수: 키/예산/데이터 계약 승인 후에만 연다 | 수동 | none |
| POL-0057-R10 | `LAB_OPEN_WEBUI_OLLAMA_BASE_URL`/`RAG_EMBEDDING_MODEL` 변경 또는 `VECTOR_DB` 도입 시 | 필수: 사전 영향 검토와 재색인 계획을 갖춘다 | 수동 | none |
| POL-0057-R11 | lease 안 작업 시 | 허용: 문서 업로드/재인덱싱/삭제와 승인된 범위의 모델 파라미터 조정 | none | none |
| POL-0057-R12 | 항상 | 금지: LAB을 root include하거나 HOME profile로 선택 | none | none |
| POL-0057-R13 | 승인이 없을 때 | 금지: SSO 우회, password/signup 경로 활성화 | 수동 | none |
| POL-0057-R14 | 항상 | 금지: HOME volume을 LAB data root로 지정 | none | none |
| POL-0057-R15 | 승인이 없을 때 | 금지: HOME data 복사/삭제 | 수동 | none |
| POL-0057-R16 | 항상 | 필수: SQLite/upload/로컬 vector/session key와 맞는 OIDC secret을 한 복구 경계로 취급한다 | none | none |
| POL-0057-R17 | 보존이 필요한 실험 data가 있을 때 | 필수: lease 종료 전에 별도 승인으로 백업한다 | 수동 | none |
| POL-0057-R18 | HOME 퇴역 시 | 필수: 컨테이너 정지/제거, volume 이전/삭제, Keycloak client/redirect, DNS 정리를 각각 별도 승인 단계로 진행한다 | 수동 | none |
| POL-0057-R19 | HOME 퇴역 시 | 필수: 쓰기를 멈춘 일관 backup을 선행한다 | 수동 | none |
| POL-0057-R20 | upgrade 시 | 필수: 복구 가능한 copy, migration 검토, image identity, rollback 근거를 갖춘다 | 수동 | none |

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

###### Lifecycle and data controls
<!-- core-payload-level:4 -->

- SQLite·upload·로컬 vector·session key와 맞는 OIDC secret을 한 복구 경계로 취급한다. HOME Restic은 LAB
  data를 백업하지 않으므로 보존이 필요한 실험 data는 lease 종료 전에 별도 승인으로 백업한다.
- HOME 퇴역(컨테이너 정지·제거, volume 이전 또는 삭제, Keycloak client·redirect, DNS 정리)은 각각 별도
  승인 단계이며 쓰기를 멈춘 일관 backup이 선행한다.
- Upgrade에는 복구 가능한 copy, migration 검토, image identity와 rollback 근거가 필요하다.

##### Exceptions

###### Exception Conditions
<!-- core-payload-level:4 -->

- LAB lease 안에서 SSO 우회를 검토해야 하면 loopback 게시, 명시 승인, lease 종료 즉시 복구가 필수다.

###### Approval and Review
<!-- core-payload-level:4 -->

- **Quarterly**: 정책/권한/데이터 취급 기준 검토
- **Per Release**: 모델/임베딩/연동 구성 변경 시 사전 검토

#### Enforcement

##### Mechanisms

- 배포 전 체크:
  - `bash scripts/hardening/check-all-hardening.sh 08-ai`
  - `python3 scripts/operations/lab.py check open-webui`
  - lease 안에서 `open-webui` container-internal health와 승인된 Ollama endpoint 연결성 확인
- 운영 중 체크:
  - 인증 실패율, 5xx 비율, 인덱싱 실패율 모니터링
- 증적:
  - 변경 티켓(또는 PR), 검증 로그, 롤백 결과

##### Limits

정책은 배포 전 체크와 운영 중 체크를 개별 규칙과 연결하지 않으므로 아래 규칙은 이름 붙은 검사로 강제되지 않으며, 일부는 승인/검토에 의존한다.

- 격리/노출: 강제 수단 없음 `POL-0057-R1`~`R3`
- 인증/secret: 강제 수단 없음 `POL-0057-R4`~`R7`
- cloud/모델 구성: 수동 검토 `POL-0057-R9`~`R10`; 강제 수단 없음 `POL-0057-R8`
- 허용/금지 작업: 수동 검토 `POL-0057-R13`, `POL-0057-R15`; 강제 수단 없음 `POL-0057-R11`~`R12`, `POL-0057-R14`
- lifecycle/data: 수동 검토 `POL-0057-R17`~`R20`; 강제 수단 없음 `POL-0057-R16`
- 운영 중 체크(인증 실패율, 5xx 비율, 인덱싱 실패율)는 모니터링 항목이며 이름 붙은 게이트나 임계값이 없다.
- 분기별 정책 검토와 릴리스별 사전 검토는 수동이다.

#### Ownership

##### Owner

책임 소유자는 **@buenhyden**이다. 예외·통제 변경에는 기존 범위별 승인 기록이 필요하며 문서 수정은 승인 근거가 아니다. 통제 실패나 복구 증거 누락은 수용을 중단하고 정제된 증거로 에스컬레이션한다.

##### Review Triggers

- Subject peers: [Guide](../../01.guides/15.labs/0057-open-webui.md) (`GDE-0057`), [Runbook](../../03.runbooks/15.labs/0057-open-webui.md) (`RUN-0057`)
- [Operations index](../../README.md)
- [Usage guide](../../01.guides/15.labs/0057-open-webui.md)
- [Recovery runbook](../../03.runbooks/15.labs/0057-open-webui.md)

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
