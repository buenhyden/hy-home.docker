---
title: "Shared Storybook Operations Policy"
version: "2.0.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
layer: "operations"
artifact_id: "POL-0101"
parent_ids:
- "AD-0031"
created: "2026-10-03"
next_review_at: "2027-05-13"
---

# Shared Storybook Operations Policy

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

공유 Storybook은 검토된 UI 구성요소의 정적 문서 origin이고, `storybook-mcp`는
같은 빌드의 manifest를 다른 워크스페이스의 Codex·Claude Code에 제공하는 원격 문서
MCP다. 소비자는 hy-home.docker가 아닌 다른 워크스페이스다. 코드 재사용은 별도 패키지
계약이 소유한다.

###### Authority
<!-- core-payload-level:4 -->

- Artifact: `POL-0101`. 역사적 source/static 완료 근거: `SPEC-0206`. 승인된 [AD-0031](../../../02.architecture/01.descriptions/0031-home-development-host.md)이 아키텍처를 소유하며 HOME 배포 승인과 실행 증거는 별도로 기록한다.
- Runtime declaration: [Storybook Compose](../../../../infra/13-experience/storybook/docker-compose.yml).

##### Applies To

`infra/13-experience/storybook/docker-compose.yml`의 선택형 `storybook`과
`storybook-mcp` 서비스, Traefik 경로, 정적 자산, image revision, 디자인 도구 전달과
운영 검증에 적용한다. SPEC-0206은 source/static completion의 역사적 근거이며, 운영 승인과 반복 절차는 이 Stage 05 subject가 소유한다.

###### Exclusions
<!-- core-payload-level:4 -->

프로젝트 업무 앱은 포함하지 않는다.

#### Rules

##### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0101-R1 | 서비스 후보 선택 시 | 필수: `experience` profile을 명시적으로 선택할 때만 서비스 후보가 된다 | `experience`와 HOME profile의 정적 render 비교(서비스 선택) | none |
| POL-0101-R2 | 항상 | 금지: HOME 선택에 포함 | `experience`와 HOME profile의 정적 render 비교(서비스 선택) | none |
| POL-0101-R3 | 항상 | 금지: 이 문서나 profile 선택을 기동 승인으로 해석 | none | none |
| POL-0101-R4 | 항상 | 필수: 정적 origin은 `internal: true` 전용 `experience_ingress_net`에만 연결한다 | 정적 render의 network 비교 | none |
| POL-0101-R5 | 항상 | 필수: Traefik만 `experience_ingress_net`과 기존 `edge_net`에 함께 연결하고 Storybook의 `traefik.docker.network`가 전용망을 가리키게 한다 | 정적 render의 network 비교 | none |
| POL-0101-R6 | 항상 | 금지: host port 80/443이나 별도 gateway 개방 | 정적 render의 port 비교 | none |
| POL-0101-R7 | 브라우저 경로 | 필수: `req-rate-limit@file`, `gateway-standard-chain@file`, `sso-auth@file` 순서로 적용한다 | 정적 render의 router/middleware 비교 | none |
| POL-0101-R8 | 항상 | 필수: OAuth2 Proxy의 Keycloak `/admins` 제한을 유지한다 | none | none |
| POL-0101-R9 | 항상 | 금지: `sso-errors@file` 연결 | 정적 render의 router/middleware 비교 | none |
| POL-0101-R10 | 비인증 index·iframe·asset·manifest 요청 | 필수: 브라우저에는 Keycloak 인가 URL로의 302, `Accept: application/json`에는 401을 준다 | 합성 격리 실행(비인증 asset 거절 확인) | none |
| POL-0101-R11 | 비인증 요청 | 금지: 내용이나 로그인 HTML을 200으로 응답 | 합성 격리 실행(비인증 asset 거절 확인) | none |
| POL-0101-R12 | 항상 | 필수: 응답은 `Cache-Control: no-store`와 `frame-ancestors 'self'` CSP를 갖는다 | 합성 격리 실행(cache, CSP/frame 확인) | none |
| POL-0101-R13 | 검토자 그룹 추가 시 | 필수: 별도 승인을 받는다 | 수동 | none |
| POL-0101-R14 | 정적 빌드 시 | 필수: 공개 UI 문서만 포함한다 | none | none |
| POL-0101-R15 | 항상 | 금지: 실제 `.env`·secret·운영 URL/로그·사용자 데이터·합성되지 않은 화면을 build context·image layer·manifest·browser asset에 포함 | none | none |
| POL-0101-R16 | manifest를 정적 자산으로 공개할 때 | 필수: 동일한 브라우저 접근 제어와 캐시 정책을 따른다 | none | none |
| POL-0101-R17 | 항상 | 필수: origin은 비특권 사용자·읽기 전용 root filesystem·필요한 tmpfs·최소 권한·자원 제한·healthcheck를 사용한다 | 정적 render의 health/resource/read-only 계약 비교 | none |
| POL-0101-R18 | 항상 | 금지: 정적 URL과 manifest를 컴포넌트 코드 배포 경로로 취급 | none | none |
| POL-0101-R19 | 내부 패키지 배포 시 | 필수: exports·types·CSS·peer dependency·revision·배포 권한을 별도로 검증한다 | none | none |
| POL-0101-R20 | 저장소에 배포 라이선스가 등록되기 전 | 금지: 공개 npm 배포 승인 | 수동 | none |
| POL-0101-R21 | image 빌드 시 | 필수: Storybook 소스를 마지막으로 바꾼 커밋에서 `git archive`로 내보낸 context로만 빌드한다 | none | none |
| POL-0101-R22 | image 빌드 시 | 필수: `hy-home/storybook:<commit>`과 `hy-home/storybook-mcp:<commit>`을 같은 커밋으로 고정한다 | none | none |
| POL-0101-R23 | 항상 | 필수: OCI revision label·`revision.json`·lockfile·UI 패키지·manifest hash가 그 커밋과 같다 | none | none |
| POL-0101-R24 | registry 배포 시 | 필수: 배포본은 SBOM과 provenance를 가진다 | none | none |
| POL-0101-R25 | 항상 | 금지: build argument와 산출물에 secret 포함 | none | none |
| POL-0101-R26 | 원격 문서 MCP 제공 시 | 필수: `docs-list`, `docs-show`, `docs-show-story`만 제공한다 | none | none |
| POL-0101-R27 | 원격 문서 MCP 제공 시 | 필수: Traefik이 TLS를 종료하고 `/mcp`와 보호 자원 metadata만 전달한다 | none | none |
| POL-0101-R28 | 원격 문서 MCP 요청 시 | 필수: Keycloak `hy-home.realm` issuer·자기 URL과 같은 audience·유효 기간·RS256 서명·`/admins` 그룹을 모두 확인한 bearer token만 받고 그 외에는 401 또는 403으로 거절한다 | none | none |
| POL-0101-R29 | 항상 | 금지: 브라우저 cookie 기반 ForwardAuth를 기계 인증으로 재사용 | none | none |
| POL-0101-R30 | 항상 | 금지: 비인증 공개 route | none | none |
| POL-0101-R31 | 항상 | 필수: 로컬 `mcp:docs`는 loopback 전용 개발 경로로 쓴다 | none | none |
| POL-0101-R32 | 항상 | 금지: 로컬 MCP 성공을 원격 MCP의 인증 성공으로 기록 | none | none |
| POL-0101-R33 | 디자인 도구에 전달 시 | 필수: 승인된 UI 코드·토큰·합성 화면만 제공한다 | none | none |
| POL-0101-R34 | Claude Design `/design-sync` 실행 시 | 필수: `design-export.allowlist.json`의 커밋된 파일만 담은 bundle 안에서 실행한다 | none | none |
| POL-0101-R35 | 항상 | 금지: `/design-sync`를 저장소에서 직접 실행 | none | none |
| POL-0101-R36 | 항상 | 금지: 외부 저장소 전체·내부 URL·환경 파일·cookie·사용자 데이터 전송 | none | none |

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

##### Exceptions

###### Exception Conditions
<!-- core-payload-level:4 -->

현재 `/admins` 외 검토자 그룹은 없다. Keycloak의 `storybook-mcp-client`와
`storybook-mcp` scope 생성, HOME에서의 `experience` 기동, DNS/TLS 관찰, reviewer
group 추가와 외부 design account 사용은 담당자 @buenhyden의 별도 운영 승인 뒤에
수행하는 follow-up trigger다. 정적 origin의 관리자 제한을
완화하는 예외는 이 정책에 포함되지 않는다.

###### Approval and Review
<!-- core-payload-level:4 -->

Storybook image, Compose route/profile, OAuth2 Proxy 허용 그룹, manifest, package export,
MCP 도구 또는 디자인 공유 범위를 변경할 때 검토한다.

#### Enforcement

##### Mechanisms

`experience`와 HOME profile을 각각 정적 render하여 서비스 선택, router,
middleware, network, port, health, resource와 read-only 계약을 비교한다. 합성
격리 실행에서는 index, iframe, JS/CSS, deep link, 404, cache, CSP/frame,
로그인 만료와 비인증 asset 거절을 확인한다. 실제 HOME DNS/TLS/OIDC와
관리자 세션은 운영 실행 승인 후에만 관찰한다. 로컬 MCP 성공을 원격 MCP의
인증 성공으로 기록하지 않는다.

##### Limits

다음 규칙은 정책이 이름 있는 자동 검사를 연결하지 않았다.

- 이름 있는 검사 없음(선택): `POL-0101-R3`
- 이름 있는 검사 없음(origin 접근): `POL-0101-R8`
- 이름 있는 검사 없음(정적 빌드): `POL-0101-R14`, `POL-0101-R15`, `POL-0101-R16`
- 이름 있는 검사 없음(배포): `POL-0101-R18`, `POL-0101-R19`
- 이름 있는 검사 없음(image): `POL-0101-R21`, `POL-0101-R22`, `POL-0101-R23`, `POL-0101-R24`, `POL-0101-R25`
- 이름 있는 검사 없음(MCP): `POL-0101-R26`, `POL-0101-R27`, `POL-0101-R28`, `POL-0101-R29`, `POL-0101-R30`, `POL-0101-R31`, `POL-0101-R32`
- 이름 있는 검사 없음(디자인 도구): `POL-0101-R33`, `POL-0101-R34`, `POL-0101-R35`, `POL-0101-R36`
- 수동 검토·승인에 의존(origin 접근): `POL-0101-R13`
- 수동 검토·승인에 의존(배포): `POL-0101-R20`
- 정책이 스스로 밝힌 한계: origin에는 peer 인증이 없어 Docker daemon 권한을 가진 운영자가 전용망에 다른 container를 붙일 수 있는 신뢰 경계가 남는다.
- 실제 HOME DNS/TLS/OIDC와 관리자 세션은 운영 실행 승인 후에만 관찰하며, 로컬 MCP 성공은 원격 MCP의 인증 성공으로 기록하지 않는다.

#### Ownership

##### Owner

이 정책의 소유자는 frontmatter의 `owner`인 `@buenhyden`이다.

##### Review Triggers

- [Shared Storybook guide](../../01.guides/14.design-system/0101-storybook.md)
- [Shared Storybook runbook](../../03.runbooks/14.design-system/0101-storybook.md)
- [Compose profile vocabulary](../01.common/0078-compose-profile-vocabulary.md)
- [Traefik policy](../02.gateway-and-networking/0013-traefik.md)

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
