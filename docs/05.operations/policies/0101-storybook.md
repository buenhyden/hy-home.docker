---
title: "Shared Storybook Operations Policy"
version: "1.0.1"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-03"
layer: "operations"
artifact_id: "POL-0101"
parent_ids:
- "AD-0031"
created: "2026-10-03"
---

# Shared Storybook Operations Policy

## Overview

### Overview

공유 Storybook은 검토된 UI 구성요소의 정적 문서 origin이다. 코드 재사용은 별도
패키지 계약이 소유하고, 로컬 문서 MCP는 root Compose의 서비스가 아니다.

## Scope

### Policy Scope

`infra/13-experience/storybook/docker-compose.yml`의 선택형 `storybook` 서비스,
Traefik 브라우저 경로, 공개 정적 자산, 코드 revision 및 운영 검증에 적용한다.
프로젝트 업무 앱과 원격 MCP 배포는 포함하지 않는다. SPEC-0206은 source/static completion의 역사적 근거이며, 운영 승인과 반복 절차는 이 Stage 05 subject가 소유한다.

### Traceability

- Artifact: `POL-0101`; historical source/static completion: `SPEC-0206`; architecture context `AD-0031` remains draft.
- Runtime declaration: [Storybook Compose](../../../infra/13-experience/storybook/docker-compose.yml).

## Rules

### Controls

- `experience` profile을 명시적으로 선택할 때만 서비스 후보가 된다. HOME 선택에는
  포함하지 않으며, 이 문서와 profile 선택은 기동 승인이 아니다.
- 정적 origin은 `internal: true` 전용 `experience_ingress_net`에만 연결한다.
  Traefik만 이 망과 기존 `edge_net`에 함께 연결한다. Storybook의
  `traefik.docker.network`가 전용망을 가리키고 host port 80/443이나 별도 gateway를
  열지 않는다. 브라우저 경로에는 `req-rate-limit@file`,
  `gateway-standard-chain@file`, `sso-auth@file` 순서로 요청 제한·기본 게이트웨이
  보호·ForwardAuth를 적용하고 OAuth2 Proxy의 Keycloak `/admins` 제한을 유지한다.
  `sso-errors@file`은 연결하지 않는다. 비인증 index·asset은
  401/403으로 거절하고 로그인 HTML로 rewrite하지 않는다. 검토자 그룹 추가는 별도 승인이다.
  origin에는 peer 인증이 없으므로 Docker daemon 권한을 가진 운영자가 전용망에
  다른 container를 붙일 수 있다는 신뢰 경계는 남는다.
- 정적 빌드에는 공개 UI 문서만 포함한다. 실제 `.env`, secret, 운영 URL/로그,
  사용자 데이터와 합성되지 않은 화면은 build context, image layer, manifest,
  browser asset에 넣지 않는다. manifest가 정적 자산으로 공개되면 동일한 브라우저
  접근 제어와 캐시 정책을 따른다.
- origin은 비특권 사용자, 읽기 전용 root filesystem, 필요한 tmpfs, 최소 권한,
  자원 제한과 healthcheck를 사용한다. 실제 값은 Compose와 Dockerfile이 소유한다.
- 정적 URL과 manifest는 컴포넌트 코드 배포 경로가 아니다. 내부 패키지의 exports,
  types, CSS, peer dependency, revision과 배포 권한을 별도로 검증한다. 저장소에
  배포 라이선스가 등록되기 전 공개 npm 배포를 승인하지 않는다.
- 문서 MCP는 로컬 프로세스에서 문서 읽기 도구만 제공한다. 원격 MCP용 issuer,
  audience, client, reader 권한이 승인·검증되기 전에는 원격 route와 token 소비를
  추가하지 않는다. 브라우저 cookie 기반 ForwardAuth를 기계 인증으로 재사용하지 않는다.
- 디자인 도구에는 승인된 UI 코드·토큰·합성 화면만 제공한다. 외부 저장소 전체,
  내부 URL, 환경 파일, 사용자 데이터는 전송 대상이 아니다.

### Verification

`experience`와 HOME profile을 각각 정적 render하여 서비스 선택, router,
middleware, network, port, health, resource와 read-only 계약을 비교한다. 합성
격리 실행에서는 index, iframe, JS/CSS, deep link, 404, cache, CSP/frame,
로그인 만료와 비인증 asset 거절을 확인한다. 실제 HOME DNS/TLS/OIDC와
관리자 세션은 운영 실행 승인 후에만 관찰한다. 로컬 MCP 성공을 원격 MCP의
인증 성공으로 기록하지 않는다.

### Review Cadence

Storybook image, Compose route/profile, OAuth2 Proxy 허용 그룹, manifest, package export,
MCP 도구 또는 디자인 공유 범위를 변경할 때 검토한다.

## Exceptions

### Exceptions

현재 검토자 그룹과 원격 MCP 클라이언트가 없다. 담당자 @buenhyden이 접근 대상,
OIDC issuer/audience/client, 권한, 만료·철회 및 검증 결과를 승인할 때 별도 운영 Task에서
해제한다. HOME route 활성화, DNS/TLS 관찰, reviewer group 추가, remote MCP 공개,
외부 design account 사용은 이 정책의 follow-up trigger다. 정적 origin의 관리자 제한을
완화하는 예외는 이 정책에 포함되지 않는다.

## Related Documents

- [Shared Storybook guide](../guides/0101-storybook.md)
- [Shared Storybook runbook](../runbooks/0101-storybook.md)
- [Compose profile vocabulary](0078-compose-profile-vocabulary.md)
- [Traefik policy](0013-traefik.md)
