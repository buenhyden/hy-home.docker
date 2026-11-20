---
title: "RedisInsight Operations Policy"
version: "2.0.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
layer: "operations"
artifact_id: "POL-0076"
parent_ids:
- "AD-0011"
created: "2026-05-17"
next_review_at: "2027-05-13"
---

# RedisInsight Operations Policy

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

RedisInsight는 OPTIONAL 자격 증명 보유 관리자 클라이언트다. Gateway 접근은 각
대상 데이터베이스에 대한 최소 권한 부여를 대체하지 않는다.

###### Authority
<!-- core-payload-level:4 -->

- [Laboratory 아키텍처](../../../02.architecture/01.descriptions/0011-laboratory-architecture.md)

- [RedisInsight Compose 소스](../../../../infra/04-data/redisinsight/docker-compose.yml)

##### Applies To

활성화, gateway/CIDR, 저장된 대상 자격 증명/이력, 대상 작업, 텔레메트리/라이선스,
설정 백업/복구, 업그레이드, 제거.

###### Exclusions
<!-- core-payload-level:4 -->

대상 Redis/Valkey 데이터의 백업은 이 정책의 범위가 아니며 각 엔진 소유자를 따른다.

#### Rules

##### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0076-R1 | 항상 | 필수: `admin`/`admin-data` profile만 사용한다 | none | none |
| POL-0076-R2 | 항상 | 금지: 상시 기본 profile에 포함 | none | none |
| POL-0076-R3 | 항상 | 필수: ForwardAuth와 관리자 CIDR을 보존한다 | 수동 | none |
| POL-0076-R4 | listener | 필수: Traefik만 함께 붙는 `redisinsight_ingress_net` 고정 주소에만 연다 | none | none |
| POL-0076-R5 | 항상 | 금지: `edge_net`/데이터 망/호스트에서 UI로 가는 직접 경로 | 수동 | none |
| POL-0076-R6 | `redisinsight_ingress_net` | 필수: isolated gateway 모드를 유지한다 | none | none |
| POL-0076-R7 | 대상 연결 | 필수: 사전 등록된 읽기 전용 inspector(`devinspector`/`mnginspector`)만 쓴다 | 수동 | none |
| POL-0076-R8 | 항상 | 금지: 관리자/지표 수집/앱 계정과 그 비밀을 RedisInsight에 입력 | none | none |
| POL-0076-R9 | 쓰기가 필요할 때 | 필수: 별도 역할과 시험 prefix를 대상 소유자와 정한다 | none | none |
| POL-0076-R10 | 항상 | 금지: `MATCH`나 prefix로 프로젝트 격리 주장 | none | none |
| POL-0076-R11 | RedisInsight 접근 | 필수: 관리자 신뢰 경계로 취급한다 | none | none |
| POL-0076-R12 | 항상 | 필수: `/data`와 백업을 민감 정보로 취급한다 | none | none |
| POL-0076-R13 | 저장된 연결 비밀번호 | 필수: `RI_ENCRYPTION_KEY`로 암호화하며 키와 `encryption` 동의가 함께 있어야 한다 | 수동 | none |
| POL-0076-R14 | `/data` | 필수: 소유자만 읽는다(디렉터리 `700`/DB 파일 `600`) | none | none |
| POL-0076-R15 | 대상 Redis/Valkey 백업 | 필수: 각 엔진 소유자를 따른다 | none | none |
| POL-0076-R16 | 항상 | 금지: `/data`로 대상 Redis/Valkey 백업 대체 | none | none |
| POL-0076-R17 | 설정 사본 | 필수: 일관된 사본을 위해 서비스를 중지한다 | none | none |
| POL-0076-R18 | 복구 | 필수: 프로덕션 대상 네트워크를 비활성화한다 | 수동 | none |
| POL-0076-R19 | 암호화 키가 구성된 경우 | 필수: 일치하는 암호화 키로 복구한다 | none | none |
| POL-0076-R20 | 검증 | 필수: UI health와 별개로 DB 접속과 설정 지속성을 검증한다 | 수동 | none |
| POL-0076-R21 | 새 망 연결 | 필수: listener가 여전히 `redisinsight_ingress_net` 주소에만 열려 있는지 확인한다 | none | none |
| POL-0076-R22 | 항상 | 금지: CIDR·SSO 성공만으로 안전한 배포나 복구 완료 선언 | none | none |
| POL-0076-R23 | 항상 | 금지: 노출 확대 | none | none |
| POL-0076-R24 | 항상 | 금지: 저장된 credential을 진단 출력으로 사용 | none | none |
| POL-0076-R25 | 업그레이드 전 | 필수: 릴리스 노트/텔레메트리 설정/적용 가능한 SSPL·라이선스 조건을 검토한다 | 수동 | none |
| POL-0076-R26 | 제거 전 | 필수: 저장된 대상 자격 증명을 폐기한다 | none | none |

- `admin`/`admin-data`만 사용하며 상시 기본 profile에 넣지 않는다.
- ForwardAuth와 관리자 CIDR을 보존한다. listener는 Traefik만 함께 붙는
  `redisinsight_ingress_net` 고정 주소에만 열고, `edge_net`·데이터 망·호스트에서
  UI로 가는 직접 경로를 두지 않는다. 이 망은 isolated gateway 모드를 유지한다.
- 대상 연결은 사전 등록된 읽기 전용 inspector(`devinspector`, `mnginspector`)만
  쓴다. 관리자·지표 수집·앱 계정과 그 비밀은 RedisInsight에 넣지 않는다. 쓰기가
  필요하면 별도 역할과 시험 prefix를 대상 소유자와 정한다.
- 키 브라우저의 `SCAN`은 DB 전체 키 이름을 보여 주므로 RedisInsight 접근은
  관리자 신뢰 경계다. `MATCH`나 prefix로 프로젝트 격리를 주장하지 않는다.
- `/data`와 백업을 민감 정보로 취급한다. 저장된 연결 비밀번호는
  `RI_ENCRYPTION_KEY`로 암호화하며, 키와 `encryption` 동의가 함께 있어야 한다.
  `/data`는 소유자만 읽는다(디렉터리 `700`, DB 파일 `600`).
- RedisInsight 백업은 클라이언트 설정만 다룬다. 대상 Redis/Valkey 백업은 각
  엔진 소유자를 따르며 `/data`로 대체할 수 없다.
- 일관된 설정 사본을 위해 서비스를 중지한다. 프로덕션 대상 네트워크를
  비활성화하고, 구성된 경우 일치하는 암호화 키로 복구한다.
- 새 망을 붙일 때는 listener가 여전히 `redisinsight_ingress_net` 주소에만 열려
  있는지 확인한다. CIDR·SSO 성공만으로 안전한 배포나 복구 완료를 선언하지 않으며,
  노출을 확대하거나 저장된 credential을 진단 출력으로 쓰지 않는다.
- 업그레이드 전에 릴리스 노트, 텔레메트리 설정, 적용 가능한 SSPL/라이선스
  조건을 검토한다. 제거 전에 저장된 대상 자격 증명을 폐기한다.

##### Exceptions

###### Exception Conditions
<!-- core-payload-level:4 -->

대상 권한 부여를 우회하거나 gateway 로그인을 데이터베이스 권한으로 취급하는
예외는 없다. `encryption` 동의가 꺼진 저장소는 안전하다고 할 수 없다.

###### Approval and Review
<!-- core-payload-level:4 -->

이미지/라이선스, 인증/CIDR, 암호화 키, 대상, 저장소 변경 시 검토한다.

#### Enforcement

##### Mechanisms

gateway/CIDR 허용/거부, 데이터 망에서의 직접 접속 거부, inspector의 읽기
허용과 쓰기·금지 명령 거부, UI health와 별개인 DB 접속, 저장 비밀번호의 평문
부재, 설정 지속성을 검증하고, 복구 테스트가 프로덕션 대상에 도달할 수 없음을
검증한다.

##### Limits

이 정책은 검증 항목만 나열하고 실행 검사의 이름을 지정하지 않으며, 아래 규칙은 자동 검사 없이 검토·승인에 의존합니다.

- profile/노출: 자동 검사 없음(none) `POL-0076-R1`, `POL-0076-R2`, `POL-0076-R4`, `POL-0076-R6`
- 대상 연결: 자동 검사 없음(none) `POL-0076-R8`, `POL-0076-R9`, `POL-0076-R10`, `POL-0076-R11`
- `/data`/백업: 자동 검사 없음(none) `POL-0076-R12`, `POL-0076-R14`, `POL-0076-R15`, `POL-0076-R16`, `POL-0076-R17`, `POL-0076-R19`
- 변경: 자동 검사 없음(none) `POL-0076-R21`, `POL-0076-R22`, `POL-0076-R23`, `POL-0076-R24`, `POL-0076-R26`; 수동 검토/승인 `POL-0076-R25`
- 정책이 밝힌 공백: Mechanisms는 검증 대상 항목(CIDR 허용/거부, 직접 접속 거부, inspector 권한, 평문 부재, 설정 지속성, 복구 격리)만 나열하며 이를 실행하는 명령/script/검사 이름은 지정하지 않는다. 표에서 Enforcement에 적힌 항목은 이 검증 항목이다.
- 정책이 밝힌 공백: `encryption` 동의가 꺼진 저장소는 안전하다고 할 수 없으나 이를 자동으로 확인하는 검사는 정의되지 않았다.
- POL-0076-R3, POL-0076-R5, POL-0076-R7, POL-0076-R13, POL-0076-R18, POL-0076-R20: 수동 검증에 맡겨진다.

#### Ownership

##### Owner

정책 소유자는 @buenhyden이다.

##### Review Triggers

- [가이드](../../01.guides/05.databases-and-storage/0076-redisinsight.md) (`GDE-0076`)
- [런북](../../03.runbooks/05.databases-and-storage/0076-redisinsight.md) (`RUN-0076`)

- [RedisInsight 설정](https://redis.io/docs/latest/operate/redisinsight/configuration/)
- [RedisInsight 문서](https://redis.io/docs/latest/develop/tools/insight/)

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
