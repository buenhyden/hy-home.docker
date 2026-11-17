---
title: "RedisInsight Operations Policy"
version: "1.3.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "operations"
artifact_id: "POL-0076"
parent_ids:
- "AD-0011"
created: "2026-05-17"
next_review_at: "2027-05-13"
---

# RedisInsight Operations Policy

## Purpose and Scope

### Objective

RedisInsight는 OPTIONAL 자격 증명 보유 관리자 클라이언트다. Gateway 접근은 각
대상 데이터베이스에 대한 최소 권한 부여를 대체하지 않는다.

#### Authority

- [Laboratory 아키텍처](../../../02.architecture/descriptions/0011-laboratory-architecture.md)

- [RedisInsight Compose 소스](../../../../infra/04-data/redisinsight/docker-compose.yml)

### Applies To

활성화, gateway/CIDR, 저장된 대상 자격 증명/이력, 대상 작업, 텔레메트리/라이선스,
설정 백업/복구, 업그레이드, 제거.

#### Exclusions

대상 Redis/Valkey 데이터의 백업은 이 정책의 범위가 아니며 각 엔진 소유자를 따른다.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0076-R1 | 항상 | 필수: `admin`/`admin-data`에서만 사용, 상시 기본 profile 금지 | none | none |
| POL-0076-R2 | 항상 | 필수: ForwardAuth와 관리자 CIDR 보존, listener는 `redisinsight_ingress_net` 고정 주소에만 열고 직접 경로 금지, isolated gateway 모드 유지 | gateway/CIDR 허용/거부, 데이터 망 직접 접속 거부 검증 | none |
| POL-0076-R3 | 항상 | 필수: 대상 연결은 읽기 전용 inspector(`devinspector`/`mnginspector`)만, 관리자/지표/앱 계정과 비밀 투입 금지 | inspector 읽기 허용과 쓰기/금지 명령 거부 검증 | none |
| POL-0076-R4 | 항상 | 금지: `MATCH`/prefix로 프로젝트 격리 주장; RedisInsight 접근은 관리자 신뢰 경계 | none | none |
| POL-0076-R5 | 항상 | 필수: `/data`/백업을 민감 정보로 취급, 연결 비밀번호는 `RI_ENCRYPTION_KEY`로 암호화(`encryption` 동의 필요), `/data` 디렉터리 `700`/DB 파일 `600` | 저장 비밀번호의 평문 부재 검증 | none |
| POL-0076-R6 | 항상 | 필수: RedisInsight 백업은 클라이언트 설정만 다루며 대상 Redis/Valkey 백업은 각 엔진 소유자를 따름 | none | none |
| POL-0076-R7 | 복구 시 | 필수: 서비스 중지 후 일관 사본, 프로덕션 대상 네트워크 비활성화, 일치하는 암호화 키로 복구 | 복구 테스트가 프로덕션 대상에 도달할 수 없음 검증 / 설정 지속성 검증 | none |
| POL-0076-R8 | 새 망을 붙일 때 | 필수: listener가 `redisinsight_ingress_net` 주소에만 열려 있는지 확인, CIDR/SSO 성공만으로 안전/복구 완료 선언 금지, 노출 확대/저장 credential 진단 출력 금지 | UI health와 별개인 DB 접속 검증 | none |
| POL-0076-R9 | 업그레이드/제거 시 | 필수: 업그레이드 전 릴리스 노트/텔레메트리/SSPL 라이선스 검토, 제거 전 저장된 대상 자격 증명 폐기 | none | none |

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

### Exceptions

#### Exception Conditions

대상 권한 부여를 우회하거나 gateway 로그인을 데이터베이스 권한으로 취급하는
예외는 없다. `encryption` 동의가 꺼진 저장소는 안전하다고 할 수 없다.

#### Approval and Review

이미지/라이선스, 인증/CIDR, 암호화 키, 대상, 저장소 변경 시 검토한다.

## Enforcement

### Mechanisms

gateway/CIDR 허용/거부, 데이터 망에서의 직접 접속 거부, inspector의 읽기
허용과 쓰기·금지 명령 거부, UI health와 별개인 DB 접속, 저장 비밀번호의 평문
부재, 설정 지속성을 검증하고, 복구 테스트가 프로덕션 대상에 도달할 수 없음을
검증한다.

### Limits

Mechanisms는 검증 대상 항목을 나열하지만 명령, script, 검사 이름은 정책에 지정되어 있지 않다.

- 위 검증 항목(CIDR 허용/거부, 직접 접속 거부, inspector 권한, 평문 부재, 설정 지속성, 복구 격리)을 실행하는 이름 붙은 check나 script가 없다.
- `/data` 권한(`700`/`600`), profile 제한, 업그레이드 전 라이선스 검토, 제거 전 credential 폐기에는 지정된 검사가 없다.
- `encryption` 동의가 꺼진 저장소는 안전하다고 할 수 없으나 이를 자동으로 확인하는 검사는 정의되지 않았다.

## Ownership

### Owner

정책 소유자는 @buenhyden이다.

### Review Triggers

- [가이드](../../guides/05-databases-and-storage/0076-redisinsight.md) (`GDE-0076`)
- [런북](../../runbooks/05-databases-and-storage/0076-redisinsight.md) (`RUN-0076`)

- [RedisInsight 설정](https://redis.io/docs/latest/operate/redisinsight/configuration/)
- [RedisInsight 문서](https://redis.io/docs/latest/develop/tools/insight/)
