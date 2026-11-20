---
title: "Security Tier (03-security)"
version: "2.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
created: "2025-11-12"
---

# Security Tier (03-security)

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

독자는 아래 역할 본문에서 이 문서가 제공하는 정보와 판단을 확인합니다.

### 책임과 적용 범위

적용 대상과 유지 책임은 frontmatter와 역할 본문의 범위 선언이 소유합니다.

## 내용 계약

### 입력과 전제

실제 입력과 전제는 아래 역할 본문의 해당 항목을 따릅니다.

### 본문과 규칙

#### Service

##### Purpose

###### Overview
<!-- core-payload-level:4 -->

HOME의 canonical 비밀 관리 서비스는 OpenBao와 `openbao-agent`다. Vault와 `vault-agent`는 SPEC-0180 S08에서 제거했고 보존된 데이터 경로만 비가동 상태로 남는다. 이 구성은 기존 비밀 데이터의 이전 또는 실제 unseal 완료를 주장하지 않는다.

###### Audience
<!-- core-payload-level:4 -->

Security owner, 인프라 운영자, 서비스 개발자와 자동화 담당자.

###### Scope
<!-- core-payload-level:4 -->

OpenBao 상시 서비스의 선언, Agent 출력 계약과 운영 문서 연결을 소유한다. 비밀 원문·키 관리 자료와 자동 자격 증명 회전은 포함하지 않는다.

###### Structure
<!-- core-payload-level:4 -->

| 경로 | 책임 |
| --- | --- |
| [openbao/](openbao/README.md) | HOME canonical 서버와 Agent |

##### Interfaces

| Interface | Producer | Consumer | Contract | Failure |
| --- | --- | --- | --- | --- |
| 외부 UI `openbao.${DEFAULT_URL}` | OpenBao | 이 README는 소비자를 기록하지 않는다. | 이 README는 계약을 따로 기록하지 않는다. | 이 README는 실패 처리를 기록하지 않는다. |

###### Configuration
<!-- core-payload-level:4 -->

OpenBao는 `core`, `local`, `dev`, `security`, `secrets`에서 선택된다. `${DEFAULT_SECURITY_DIR}/openbao`와 보존된 `${DEFAULT_SECURITY_DIR}/vault` 경로를 공유하지 않는다. 외부 UI는 `openbao.${DEFAULT_URL}`이다.

###### Security Boundary
<!-- core-payload-level:4 -->

없음: 이 디렉터리는 Compose 서비스나 secret 참조를 직접 선언하지 않으며, 하위 `openbao/`가 각자 선언한다.

#### Usage

##### Prerequisites

###### Tech Stack
<!-- core-payload-level:4 -->

실행 이미지·profile·마운트의 원본은 [openbao/](openbao/)의 compose 선언이다. [Derived Compose image projection](../tech-stack.versions.json)은 선언 drift 검증을 제공한다.

##### Selected Start

###### Usage
<!-- core-payload-level:4 -->

1. 새 소비자는 [OpenBao 가이드 — 문서 인덱스](../../docs/README.md) (`GDE-0085`)를 따른다.
2. 보존된 Vault 데이터 경로와 OpenBao 데이터 경로를 분리해 둔다. 백업·복원 및 현재 데이터 상태는 별도 검증 전까지 미확인으로 기록한다.
3. seal 상태, Agent 인증 및 소비자 연결을 각각 확인한다. healthcheck 성공만으로 전체 준비 완료를 판단하지 않는다.

###### Change Impact
<!-- core-payload-level:4 -->

인증·템플릿·endpoint 변경은 소비자의 비밀 공급에 영향을 준다. 원본 데이터 삭제, 저장소 공유, 재초기화 또는 키 회전을 구성 정리와 함께 수행하지 않는다.

#### Checks

##### Readiness

###### Testing
<!-- core-payload-level:4 -->

저장소 루트에서 공개 예시 환경만 사용해 정적 구성과 하드닝을 검사한다.

```bash
docker compose --env-file .env.example --profile core config --services
bash scripts/hardening/check-all-hardening.sh 03-security
```

##### Failure Handling

###### Related Documents
<!-- core-payload-level:4 -->

- [OpenBao 정책 — 문서 인덱스](../../docs/README.md) (`POL-0085`), [OpenBao 런북 — 문서 인덱스](../../docs/README.md) (`RUN-0085`).
- [OpenBao migration 제약](https://openbao.org/docs/next/guides/migration/).
- [인프라 인덱스](../README.md).

###### Observability and Recovery
<!-- core-payload-level:4 -->

없음: 이 디렉터리는 자체 헬스체크나 관측 대상을 선언하지 않으며, 하위 `openbao/`가 각자 선언한다.

## 적용과 확인

### 적용 방법

아래 역할 본문의 절차나 탐색 순서에 따라 사용합니다.

### 확인 기준

해당 문서에 선언된 확인 기준과 한계만 적용하며 실행·검증·인수를 구분합니다.

## 관계와 출처

### 관련 문서

현재 소유자와 의존 문서의 연결은 아래 역할 본문의 링크가 소유합니다.

### 외부 근거

외부 출처와 적용 한계는 아래 역할 본문에 선언된 범위이며 권한을 부여하지 않습니다.
