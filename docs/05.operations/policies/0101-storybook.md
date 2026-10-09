---
title: "Shared Storybook Operations Policy"
version: "1.1.1"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "operations"
artifact_id: "POL-0101"
parent_ids:
- "AD-0031"
created: "2026-10-03"
---

# Shared Storybook Operations Policy

## Overview

공유 Storybook은 검토된 UI 구성요소의 정적 문서 origin이고, `storybook-mcp`는
같은 빌드의 manifest를 다른 워크스페이스의 Codex·Claude Code에 제공하는 원격 문서
MCP다. 소비자는 hy-home.docker가 아닌 다른 워크스페이스다. 코드 재사용은 별도 패키지
계약이 소유한다.

## Scope

`infra/13-experience/storybook/docker-compose.yml`의 선택형 `storybook`과
`storybook-mcp` 서비스, Traefik 경로, 정적 자산, image revision, 디자인 도구 전달과
운영 검증에 적용한다. 프로젝트 업무 앱은 포함하지 않는다. SPEC-0206은 source/static completion의 역사적 근거이며, 운영 승인과 반복 절차는 이 Stage 05 subject가 소유한다.

## Rules

- `experience` profile을 명시적으로 선택할 때만 서비스 후보가 된다. HOME 선택에는
  포함하지 않으며, 이 문서와 profile 선택은 기동 승인이 아니다.
- 정적 origin은 `internal: true` 전용 `experience_ingress_net`에만 연결한다.
  Traefik만 이 망과 기존 `edge_net`에 함께 연결한다. Storybook의
  `traefik.docker.network`가 전용망을 가리키고 host port 80/443이나 별도 gateway를
  열지 않는다. 브라우저 경로에는 `req-rate-limit@file`,
  `gateway-standard-chain@file`, `sso-auth@file` 순서로 요청 제한·기본 게이트웨이
  보호·ForwardAuth를 적용하고 OAuth2 Proxy의 Keycloak `/admins` 제한을 유지한다.
  `sso-errors@file`은 연결하지 않는다. 비인증 index·iframe·asset·manifest는
  브라우저에 Keycloak 인가 URL로의 302, `Accept: application/json`에 401을 주며
  내용이나 로그인 HTML을 200으로 주지 않는다. 응답은 `Cache-Control: no-store`와
  `frame-ancestors 'self'` CSP를 갖는다. 검토자 그룹 추가는 별도 승인이다.
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
- image는 Storybook 소스를 마지막으로 바꾼 커밋에서 `git archive`로 내보낸
  context로만 빌드하고 `hy-home/storybook:<commit>`과 `hy-home/storybook-mcp:<commit>`을
  같은 커밋으로 고정한다. OCI revision label, `revision.json`, lockfile·UI 패키지·
  manifest hash가 그 커밋과 같아야 하며 registry 배포본은 SBOM과 provenance를 가진다.
  build argument와 산출물에 secret을 넣지 않는다.
- 원격 문서 MCP는 `docs-list`, `docs-show`, `docs-show-story`만 제공한다. Traefik이
  TLS를 종료하고 `/mcp`와 보호 자원 metadata만 전달한다. 서버는 Keycloak
  `hy-home.realm` issuer, 자기 URL과 같은 audience, 유효 기간, RS256 서명과 `/admins`
  그룹을 모두 확인한 bearer token만 받고 그 외에는 401 또는 403으로 거절한다.
  Keycloak client는 PKCE를 쓰는 public client `storybook-mcp-client`와 optional
  scope `storybook-mcp`이며 정의는 GDE-0101이 소유한다. 브라우저 cookie 기반
  ForwardAuth를 기계 인증으로 재사용하지 않고 비인증 공개 route를 두지 않는다.
  로컬 `mcp:docs`는 loopback 전용 개발 경로다.
- 디자인 도구에는 승인된 UI 코드·토큰·합성 화면만 제공한다. Claude Design
  `/design-sync`는 `design-export.allowlist.json`의 커밋된 파일만 담은 bundle 안에서
  실행하고 저장소에서 직접 실행하지 않는다. 외부 저장소 전체, 내부 URL, 환경 파일,
  cookie, 사용자 데이터는 전송 대상이 아니다.

## Exceptions

현재 `/admins` 외 검토자 그룹은 없다. Keycloak의 `storybook-mcp-client`와
`storybook-mcp` scope 생성, HOME에서의 `experience` 기동, DNS/TLS 관찰, reviewer
group 추가와 외부 design account 사용은 담당자 @buenhyden의 별도 운영 승인 뒤에
수행하는 follow-up trigger다. 정적 origin의 관리자 제한을
완화하는 예외는 이 정책에 포함되지 않는다.

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

### Traceability

- Artifact: `POL-0101`. 역사적 source/static 완료 근거: `SPEC-0206`. 아키텍처 맥락 `AD-0031`은 draft 상태다.
- Runtime declaration: [Storybook Compose](../../../infra/13-experience/storybook/docker-compose.yml).

## Related Documents

- [Shared Storybook guide](../guides/0101-storybook.md)
- [Shared Storybook runbook](../runbooks/0101-storybook.md)
- [Compose profile vocabulary](0078-compose-profile-vocabulary.md)
- [Traefik policy](0013-traefik.md)
