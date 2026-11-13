---
title: "Application Authentication Integration Policy"
version: "0.9.3"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "operations"
artifact_id: "POL-0079"
parent_ids:
- "ADR-0038"
created: "2026-09-18"
---

# Application Authentication Integration Policy

## Purpose

### Objective

이 정책은 Keycloak을 중앙 IdP로 사용하면서 OAuth2 Proxy ForwardAuth와
application-native OIDC를 선택·운영하는 기준을 정의한다.

### Authority

- Parent: [ADR-0038](../../../02.architecture/decisions/0038-selective-native-oidc-for-native-auth-apps.md)
- Architecture: [AD-0002](../../../02.architecture/descriptions/0002-auth-architecture.md)

## Scope

### Applies To

- Keycloak
- OAuth2 Proxy
- Traefik authentication middleware
- Kafbat UI
- Apache Airflow
- OpenBao
- 신규 OIDC-capable internal applications
- Open WebUI/Gatus native 연동과 Task 0004에서 보류한 Terrakube 후보

### Exclusions

Keycloak과 OAuth2 Proxy 서비스 자체의 운영 통제는 [POL-0014](0014-keycloak.md)와 [POL-0015](0015-oauth2-proxy.md)가 다룬다.

## Rules

### Requirements

#### Required

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

#### Disallowed

- Native OIDC 서비스에 OAuth2 Proxy ForwardAuth를 동시에 기본 인증으로 적용
- `rootCA-key.pem` 배포/공유
- secret/token 원문 기록
- 과거 OAuth callback URL 또는 authorization code 재사용
- Keycloak access token을 Airflow internal JWT로 취급

#### Source nonconformance and ownership

공통 Secret 보존·runtime 변경 승인은 [POL-0006](../01-common/0006-infrastructure-optimization-governance.md)과
[POL-0021](../10-platform-and-backup/0021-backup-and-restore.md)을 적용한다.

### Enforcement

정적 검증: [GDE-0079](../../guides/03-identity-and-access/0079-application-auth-integration.md#서비스별-정적-검증)의
profile별 Compose 검증과 tier hardening 명령이 모두 통과한다.

추가 검증:

- Airflow/Grafana/Kafbat/OpenBao/Gatus router = gateway-only, Dozzle = gateway + IP allowlist; Gatus는 외부 metrics 제외
- ForwardAuth 대상 서비스 = SSO chain 유지
- Keycloak client redirect URI/public URL 정합
- Compose client secret의 Docker Secret 또는 OpenBao Agent 출력 mapping
- OpenBao auth-backend OIDC client/role/policy 설정은 [OpenBao runbook](../../runbooks/04-security-and-secrets/0085-openbao.md)의 비밀값 없는 점검 절차로 확인
- Airflow provider/Authorization Services bootstrap 상태

## Exceptions

### Exception Conditions

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
[Guide의 source 한계](../../guides/03-identity-and-access/0079-application-auth-integration.md)에
기록한다.

### Approval and Review

- Keycloak update
- OAuth2 Proxy update
- Airflow Keycloak provider 업데이트
- Kafbat UI 업데이트
- 신규 Native OIDC 서비스 승인
- 분기별 인증 연동 검토

## Ownership

### Responsibilities

운영 책임자는 @buenhyden이다.

### Change and Adoption

- Child: [GDE-0079](../../guides/03-identity-and-access/0079-application-auth-integration.md)

- 런타임 버전은 Compose/Dockerfile 선언이 소유하며, [파생 Compose 이미지 목록](../../../../infra/tech-stack.versions.json)은 drift 검증에 사용한다.

- [Keycloak Guide](../../guides/03-identity-and-access/0014-keycloak.md)
- [OAuth2 Proxy Guide](../../guides/03-identity-and-access/0015-oauth2-proxy.md)
- [Kafka/Kafbat Guide](../../guides/06-messaging-and-cdc/0036-kafka.md)
- [Airflow Guide](../../guides/08-workflows-and-automation/0050-airflow.md)
