---
title: "Application Authentication Integration Policy"
version: "1.0.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
layer: "operations"
artifact_id: "POL-0079"
parent_ids:
- "ADR-0038"
created: "2026-09-18"
next_review_at: "2027-05-13"
---

# Application Authentication Integration Policy

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

이 정책은 Keycloak을 중앙 IdP로 사용하면서 OAuth2 Proxy ForwardAuth와
application-native OIDC를 선택·운영하는 기준을 정의한다.

###### Authority
<!-- core-payload-level:4 -->

- Parent: [ADR-0038](../../../02.architecture/02.decisions/0038-selective-native-oidc-for-native-auth-apps.md)
- Architecture: [AD-0002](../../../02.architecture/01.descriptions/0002-auth-architecture.md)

##### Applies To

- Keycloak
- OAuth2 Proxy
- Traefik authentication middleware
- Kafbat UI
- Apache Airflow
- OpenBao
- 신규 OIDC-capable internal applications
- Open WebUI/Gatus native 연동과 Task 0004에서 보류한 Terrakube 후보

###### Exclusions
<!-- core-payload-level:4 -->

Keycloak과 OAuth2 Proxy 서비스 자체의 운영 통제는 [POL-0014](0014-keycloak.md)와 [POL-0015](0015-oauth2-proxy.md)가 다룬다.

#### Rules

##### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0079-R1 | 항상 | 필수: 모든 사용자 authentication identity source는 Keycloak을 기준으로 한다 | none | none |
| POL-0079-R2 | 서비스 onboarding | 필수: `Gateway ForwardAuth` 또는 `Application-native OIDC` 중 하나를 주 인증 경로로 명시한다 | none | none |
| POL-0079-R3 | Superset LAB origin의 redirect 등록 | 금지: 소유자 승인 전에 등록한다 | none | none |
| POL-0079-R4 | Airflow/Grafana/Kafbat UI/OpenBao/Gatus Traefik router | 필수: `gateway-standard-chain@file`만 사용한다 | 수동 | none |
| POL-0079-R5 | Dozzle router | 필수: `gateway-standard-chain@file`에 `dozzle-admin-ip@docker` IP allowlist를 더한다 | 수동 | none |
| POL-0079-R6 | Dozzle router | 금지: SSO chain을 쓴다 | 수동 | none |
| POL-0079-R7 | Flower 등 ForwardAuth 대상 | 필수: 승인된 `sso-errors@file,sso-auth@file` chain을 유지한다 | 수동 | none |
| POL-0079-R8 | n8n | 필수: 자체 로그인만 사용하고 `gateway-standard-chain@file`만 쓴다 | none | none |
| POL-0079-R9 | OAuth2 Proxy | 필수: `allowed_groups = ["/admins"]`로 Keycloak `/admins` 그룹만 통과시킨다 | none | none |
| POL-0079-R10 | `/admins` 그룹 확대 | 필수: owner 승인을 받는다 | 수동 | none |
| POL-0079-R11 | 모든 Traefik HTTP router | 필수: SSO chain을 쓰거나 guide의 Route Authentication Matrix에 대체 인증을 명시한다 | `RouteAuthContractTests` | none |
| POL-0079-R12 | 모든 route | 금지: 인증 없는 route와 TCP route를 둔다 | `RouteAuthContractTests` | none |
| POL-0079-R13 | Exception Conditions에 기록한 Grafana 정적 예외 | 허용: 이 예외만 위 규칙의 범위를 제한한다 | none | none |
| POL-0079-R14 | Terrakube ForwardAuth 제거 | 필수: 서비스별 acceptance evidence가 기록된 뒤에만 한다 | none | none |
| POL-0079-R15 | 이미 승인된 단계별 전환 | 허용: 같은 범위의 재승인 없이 진행한다 | none | none |
| POL-0079-R16 | Compose 기반 OIDC client secret | 필수: Docker Secret 또는 소비자 Compose가 선언한 OpenBao Agent 출력 파일(`/run/openbao/...`)로 주입한다 | 수동 | none |
| POL-0079-R17 | OpenBao native OIDC secret | 필수: 승인된 절차로 auth backend에 저장한다 | [OpenBao runbook](../../03.runbooks/04.security-and-secrets/0085-openbao.md)의 비밀값 없는 점검 절차 | none |
| POL-0079-R18 | 비밀값 | 금지: 공개 설정에 넣는다 | none | none |
| POL-0079-R19 | token/refresh token/id token 원문 | 금지: 문서/incident/PR/task evidence에 기록한다 | none | none |
| POL-0079-R20 | local mkcert CA | 필수: 기존 public CA trust를 보존한 상태로 추가한다 | none | none |
| POL-0079-R21 | Airflow provider update | 필수: Keycloak permission migration 요구사항을 확인한다 | none | none |
| POL-0079-R22 | Kafbat RBAC `clusters` | 필수: configured cluster name과 일치한다 | none | none |
| POL-0079-R23 | Open WebUI | 필수: 가입을 비활성화하고 OAuth role/group 자동 관리를 끈다 | none | none |
| POL-0079-R24 | Open WebUI 이메일 병합 | 필수: 검증된 단일 기존 관리자 연결에 한정한다 | none | none |
| POL-0079-R25 | Open WebUI 수용 검증 후 | 필수: 비활성화 상태를 유지한다 | none | none |
| POL-0079-R26 | 미기동 Terrakube | 금지: 명시적 API audience 검증과 실행 검증 전에 완료로 본다 | none | none |
| POL-0079-R27 | Native OIDC 서비스 | 금지: OAuth2 Proxy ForwardAuth를 동시에 기본 인증으로 적용한다 | none | none |
| POL-0079-R28 | 항상 | 금지: `rootCA-key.pem` 배포/공유 | none | none |
| POL-0079-R29 | 항상 | 금지: secret/token 원문 기록 | none | none |
| POL-0079-R30 | 항상 | 금지: 과거 OAuth callback URL 또는 authorization code 재사용 | none | none |
| POL-0079-R31 | Airflow | 금지: Keycloak access token을 Airflow internal JWT로 취급한다 | none | none |
| POL-0079-R32 | 공통 Secret 보존/runtime 변경 승인 | 필수: [POL-0006](../01.common/0006-infrastructure-optimization-governance.md)과 [POL-0021](../10.platform-and-backup/0021-backup-and-restore.md)을 적용한다 | none | none |

###### Required
<!-- core-payload-level:4 -->

- 모든 사용자 authentication identity source는 Keycloak을 기준으로 한다.
- 서비스 onboarding 시 `Gateway ForwardAuth` 또는 `Application-native OIDC` 중
  하나를 주 인증 경로로 명시한다.
- 현재 HOME Native OIDC 서비스는 Airflow, Dozzle, Grafana, Kafbat UI, OpenBao, Gatus다. Superset과 Open WebUI는 gateway route 없는 독립 LAB이다.
  Superset은 SPEC-0262 이후 gateway router가 없는 독립 LAB의 native OIDC 앱이며, LAB origin의 redirect
  등록은 소유자 승인 전까지 미결정이다. JupyterLab·SonarQube·Stalwart LAB에는 ForwardAuth가 적용되지 않는다.
- Airflow/Grafana/Kafbat/OpenBao/Gatus Traefik router는 `gateway-standard-chain@file`만 사용한다.
  Dozzle router는 여기에 `dozzle-admin-ip@docker` IP allowlist를 더하며 SSO chain은 쓰지 않는다.
- Flower 등 ForwardAuth 대상은 승인된 `sso-errors@file,sso-auth@file`
  chain을 유지한다. n8n은 자체 로그인만 사용하며 `gateway-standard-chain@file`만
  쓴다(owner 결정 2026-11-09, 이중 로그인 불가).
- OAuth2 Proxy는 `allowed_groups = ["/admins"]`로 Keycloak `/admins` 그룹만
  통과시킨다. 그룹을 넓히는 것은 owner 승인이 필요한 변경이다.
- 모든 Traefik HTTP router는 SSO chain을 쓰거나, guide의 Route Authentication
  Matrix에 대체 인증을 명시한다. 인증 없는 route와 TCP route는 두지 않는다
  (`RouteAuthContractTests`). Exception Conditions에 기록한 Grafana 정적 예외만 이 규칙의 범위를
  제한한다.
- Open WebUI와 Gatus의 ForwardAuth 제거는 Task 0004 acceptance evidence 뒤에 완료됐다. Terrakube의 ForwardAuth 제거는 서비스별 acceptance evidence가 기록된 뒤에만 허용한다. 단계별 전환은 사용자가 이미 승인했으며, 같은 범위의 재승인을 요구하지 않는다.
- Compose 기반 OIDC client secret은 Docker Secret 또는 소비자 Compose가 선언한 OpenBao Agent
  출력 파일(`/run/openbao/...`)로 주입한다. OpenBao native
  OIDC secret은 승인된 절차로 auth backend에 저장한다. 비밀값은 공개 설정에 넣지 않는다.
- token/refresh token/id token 원문을 문서, incident, PR, task evidence에 기록하지 않는다.
- local mkcert CA는 기존 public CA trust를 보존한 상태로 추가한다.
- Airflow provider update 시 Keycloak permission migration 요구사항을 확인한다.
- Kafbat RBAC `clusters`는 configured cluster name과 일치해야 한다.

- Open WebUI는 가입을 비활성화하고 OAuth role/group 자동 관리를 끈다. 이메일 병합은
  검증된 단일 기존 관리자 연결에 한정했으며 수용 검증 후 비활성화 상태를 유지한다.
- 미기동 Terrakube는 명시적 API audience 검증과 실행 검증 전까지 완료로 보지 않는다.

###### Disallowed
<!-- core-payload-level:4 -->

- Native OIDC 서비스에 OAuth2 Proxy ForwardAuth를 동시에 기본 인증으로 적용
- `rootCA-key.pem` 배포/공유
- secret/token 원문 기록
- 과거 OAuth callback URL 또는 authorization code 재사용
- Keycloak access token을 Airflow internal JWT로 취급

###### Shared controls
<!-- core-payload-level:4 -->

공통 Secret 보존·runtime 변경 승인은 [POL-0006](../01.common/0006-infrastructure-optimization-governance.md)과
[POL-0021](../10.platform-and-backup/0021-backup-and-restore.md)을 적용한다.

##### Exceptions

###### Exception Conditions
<!-- core-payload-level:4 -->

긴급한 auth 우회는 적용 범위, 시작/종료 조건, rollback, evidence를 incident/task에
기록한 경우에만 허용한다. Native OIDC 앱에 임시 ForwardAuth를 적용하려면
`Authorization` header 충돌이 없음을 먼저 검증해야 한다.

2026-11-02 사용자 승인에 따라
`grafana-static`은 Grafana host의 `/favicon.ico`와 `/robots.txt` GET/HEAD만
SSO 인증 예외로 허용하며 `gateway-standard-chain@file`은 유지한다. 다른 메서드는 더 높은 우선순위의
`grafana-static-deny` router가 `noop@internal`으로 종료하여 일반
Grafana router로 우회하지 못하게 하고 `418`을 반환해야 한다. 이 예외는 Grafana
RBAC, 다른 경로, 다른 host 또는 다른 method로 넓어지지 않는다.

리스크는 인증 없는 응답이 두 정적 경로에 남는 것이다. 기존 초당 100회, burst
200의 서비스 rate limit은 유지하며 사용자별 제한으로 표현하지 않는다. 이 예외는
2026-12-02에 재검토하고, 경로·메서드 범위 확대, 인증 체인 변경 또는 관련 보안
권고가 있으면 즉시 종료 또는 재승인한다. source와 테스트를 이 문서 변경만으로
수정 또는 통과했다고 주장하지 않으며, 정적 계약은 Grafana 접근·로그인·권한·backend
호출의 운영 검증이 아니다. LAN/TLS 도달 경계와 제한의 구현 증거는
[Guide의 source 한계](../../01.guides/03.identity-and-access/0079-application-auth-integration.md)에
기록한다.

###### Approval and Review
<!-- core-payload-level:4 -->

- Keycloak update
- OAuth2 Proxy update
- Airflow Keycloak provider 업데이트
- Kafbat UI 업데이트
- 신규 Native OIDC 서비스 승인
- 분기별 인증 연동 검토

#### Enforcement

##### Mechanisms

정적 검증: [GDE-0079](../../01.guides/03.identity-and-access/0079-application-auth-integration.md#서비스별-정적-검증)의
profile별 Compose 검증과 tier hardening 명령이 모두 통과한다.

추가 검증:

- Airflow/Grafana/Kafbat/OpenBao/Gatus router = gateway-only, Dozzle = gateway + IP allowlist; Gatus는 외부 metrics 제외
- ForwardAuth 대상 서비스 = SSO chain 유지
- Keycloak client redirect URI/public URL 정합
- Compose client secret의 Docker Secret 또는 OpenBao Agent 출력 mapping
- OpenBao auth-backend OIDC client/role/policy 설정은 [OpenBao runbook](../../03.runbooks/04.security-and-secrets/0085-openbao.md)의 비밀값 없는 점검 절차로 확인
- Airflow provider/Authorization Services bootstrap 상태

##### Limits

이 정책은 아래 규칙에 대해 명명된 자동 검사를 연결하지 않거나 수동 검토에 맡긴다.

- 인증 경로: 명명된 검사 없음 R1~R3 (`POL-0079-` 접두)
- 라우터 체인: 명명된 검사 없음 R8, R9, R13~R15; 수동 검토 R10 (`POL-0079-` 접두)
- secret/token: 명명된 검사 없음 R18~R20 (`POL-0079-` 접두)
- 서비스별: 명명된 검사 없음 R21~R26 (`POL-0079-` 접두)
- 금지 목록: 명명된 검사 없음 R27~R31 (`POL-0079-` 접두)
- 공통 통제: 명명된 검사 없음 R32 (`POL-0079-` 접두)
- 정책이 명명한 검증은 GDE-0079의 서비스별 정적 검증(profile별 Compose 검증과 tier hardening)과 추가 검증 목록이며 `RouteAuthContractTests` 외에는 규칙별로 이름 붙은 스크립트가 없다.
- Keycloak client redirect URI/public URL 정합, Airflow provider/Authorization Services bootstrap 상태는 추가 검증 목록에 있으나 어느 규칙에 대응하는지 본문이 연결하지 않는다.
- POL-0079-R4, POL-0079-R5, POL-0079-R6, POL-0079-R7, POL-0079-R16: 수동 검증에 맡겨진다.

#### Ownership

##### Owner

운영 책임자는 @buenhyden이다.

##### Review Triggers

- Child: [GDE-0079](../../01.guides/03.identity-and-access/0079-application-auth-integration.md)

- 런타임 버전은 Compose/Dockerfile 선언이 소유하며, [파생 Compose 이미지 목록](../../../../infra/tech-stack.versions.json)은 drift 검증에 사용한다.

- [Keycloak Guide](../../01.guides/03.identity-and-access/0014-keycloak.md)
- [OAuth2 Proxy Guide](../../01.guides/03.identity-and-access/0015-oauth2-proxy.md)
- [Kafka/Kafbat Guide](../../01.guides/06.messaging-and-cdc/0036-kafka.md)
- [Airflow Guide](../../01.guides/08.workflows-and-automation/0050-airflow.md)

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
