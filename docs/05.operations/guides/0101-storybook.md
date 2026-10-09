---
title: "Shared Storybook Usage Guide"
version: "1.2.1"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "operations"
artifact_id: "GDE-0101"
parent_ids:
- "POL-0101"
implementation_services:
  infra/13-experience/storybook/docker-compose.yml:
  - "storybook"
  - "storybook-mcp"
created: "2026-10-03"
---

# Shared Storybook Usage Guide

## Overview

공유 Storybook은 `projects/storybook/nextjs`의 UI story와 문서를 읽기 전용 정적 origin(`storybook`)과 문서 MCP(`storybook-mcp`)로 제공하는 선택형 `experience` 서비스다. HOME 기본 선택에는 포함되지 않는다.

## Audience and Goal

공유 Storybook과 문서 MCP를 운영하거나 다른 워크스페이스에서 소비하는 운영자와 개발자를 위한 문서다. 빌드, 접근 경로, 소비 워크스페이스 설정과 점검 방법을 이해하는 것이 목표다.

## Usage

`projects/storybook/nextjs`는 공유 UI 구성요소의 story와 문서를 소유한다.
`storybook`은 그 빌드 결과를 읽기 전용으로 제공하는 선택형 정적 origin이다.
Traefik이 HTTPS를 종료하고 `req-rate-limit@file`,
`gateway-standard-chain@file`, `sso-auth@file` 순서로 요청 제한·기본 게이트웨이
보호·ForwardAuth를 적용한다. OAuth2 Proxy의 Keycloak `/admins` 접근 제한은
그대로 유지한다. `experience` profile은 HOME 기본 선택에 포함되지 않는다.

정적 origin은 `internal: true`인 `experience_ingress_net`에만 연결되고
host port를 열지 않는다. Traefik은 그 망과 기존 `edge_net`에 함께 연결하고
`traefik.docker.network`로 Storybook backend 망을 지정한다. 공유 `edge_net`의
다른 container는 정적 origin에 직접 닿지 않는다. Docker daemon 권한으로 전용망에
container를 연결할 수 있는 운영자는 별도 신뢰 경계이며, origin 자체에는 peer
인증이 없다. 비특권 내부 HTTP 서버는 정적 파일만 제공하고 업무 API, 사용자 데이터, 영속
volume과 secret을 소비하지 않는다. 실제 build context, image, 내부 port,
healthcheck, resource 및 security 선언은
[Compose](../../../infra/13-experience/storybook/docker-compose.yml)와
[Dockerfile](../../../projects/storybook/nextjs/Dockerfile)이 소유한다.
현재 route의 브라우저 검토자는 관리자뿐이다. `sso-errors@file`은 연결하지 않는다.
비인증 브라우저 요청(`Accept: text/html` 또는 `*/*`)은 index·iframe·asset·manifest
모두 OAuth2 Proxy가 정한 Keycloak 인가 URL로 302를 받고, `Accept:
application/json` 요청은 401을 받는다. 어느 경우에도 Storybook 내용이나 로그인
HTML이 200으로 오지 않는다. 브라우저 탐색은 302를 따라 Keycloak 로그인으로
진입하며, 수동 진입점은 `https://auth.${DEFAULT_URL}/oauth2/start?rd=<URL-encoded https://storybook.${DEFAULT_URL}/>`이다.
로그인 후 `.${DEFAULT_URL}` 범위의 `__Secure-sso-cookie`(Secure, HttpOnly)가
세션을 전달한다. `/admins`가 아닌 사용자는 callback에서 403을 받아 cookie가
만들어지지 않는다. 정적 origin은 모든 응답에 `Cache-Control: no-store`와
`Content-Security-Policy: frame-ancestors 'self'; object-src 'none'; base-uri 'self'`를
붙여 인증된 내용이 공유 cache에 남지 않고 다른 origin에 frame으로 들어가지
않게 한다. 이 결과는 Compose label에서 만든 router와 실제 Traefik·OAuth2 Proxy·
Keycloak을 쓰는 격리 rehearsal(`HYHOME_STORYBOOK_REHEARSAL=1`)이 검사한다.
HOME DNS/TLS와 실제 관리자 세션은 별도 관찰 대상이다.

### 코드 재사용과 문서

공유 구성요소는 [UI package](../../../projects/storybook/nextjs/packages/ui/package.json)의
exports·TypeScript 타입·CSS·React peer와 version을 확인해 내부 프로젝트에서
소비한다. Storybook URL과 `components.json`/`docs.json` manifest는 코드 패키지
배포가 아니다. 새 외부 프로젝트는 승인된 패키지 계약을 소비하며 원본 파일을
무관리 복사하지 않는다. 저장소 배포 라이선스가 정해지기 전 공개 npm 게시를
가정하지 않는다.

[Storybook manifest 안내](https://storybook.js.org/docs/ai/manifests)는 manifest를
story와 문서에서 생성하는 preview 기능으로 설명한다.
[자가 호스팅 MCP 안내](https://storybook.js.org/docs/ai/mcp/sharing)는 정적 사이트와
별도 `@storybook/mcp` 서버를 구분한다. 정적 site 자체는 MCP가 아니다. 원격 문서
MCP는 별도 `storybook-mcp` 서비스이며 아래 절의 Keycloak bearer token으로만
접근한다. 비인증 원격 공유나 브라우저 ForwardAuth cookie 재사용은 지원 계약이
아니다.

UI 패키지의 소비 절차와 호환되지 않는 변경은
[UI 패키지 README](../../../projects/storybook/nextjs/packages/ui/README.md)가 소유한다.

### 다른 워크스페이스에서 쓰는 Storybook과 문서 MCP

Storybook과 문서 MCP의 소비자는 hy-home.docker가 아니라 다른 워크스페이스다.
같은 HOME 호스트의 프로젝트와 다른 기기의 Codex·Claude Code가 같은 경로를 쓴다.

| 대상 | 주소 | 인증 |
| --- | --- | --- |
| Storybook 문서 | `https://storybook.hy.home.arpa/` | 브라우저 SSO, `/admins` |
| 문서 MCP | `https://storybook-mcp.hy.home.arpa/mcp` | Keycloak bearer token, audience는 이 URL, `/admins` 그룹 |
| UI 코드 | `@hy-home/storybook-ui` tarball | 소비 프로젝트 lockfile의 integrity |

`storybook-mcp`는 같은 커밋의 manifest를 읽는 `@storybook/mcp` 서버이며
`docs-list`, `docs-show`, `docs-show-story`만 제공한다. Traefik이 TLS를 종료하고
`/mcp`와 `/.well-known/oauth-protected-resource`만 전달한다. 서버는 token의
서명(Keycloak JWKS, RS256), issuer `https://keycloak.hy.home.arpa/realms/hy-home.realm`,
audience `https://storybook-mcp.hy.home.arpa/mcp`, 만료와 `groups`의 `/admins`를
검사한다. token이 없거나 맞지 않으면 401과 `WWW-Authenticate: Bearer scope="storybook-mcp",
resource_metadata=".../.well-known/oauth-protected-resource/mcp"`, 그룹이 없으면
403 `insufficient_scope`다. 브라우저 SSO cookie는 이 경로를 인증하지 않는다.
이 동작은 [MCP 인가 사양](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization)의
보호 자원 metadata(RFC 9728)와 audience 검증을 따른다.

#### Keycloak 준비(운영자)

`hy-home.realm`에 다음을 만든다. 생성과 변경은 RUN-0014 절차와 별도 승인을 따른다.

1. Client scope `storybook-mcp`(Optional, token scope에 포함): Audience mapper의
   Included Custom Audience를 `https://storybook-mcp.hy.home.arpa/mcp`로, Group
   Membership mapper를 claim `groups`, full path, access token 포함으로 둔다.
2. Client `storybook-mcp-client`: public client, Standard flow만 사용, Direct access
   grants 끔, PKCE `S256`, Valid redirect URI는 `http://localhost:33418/callback`
   (Claude Code)과 `http://127.0.0.1:33419/callback/*`(Codex), optional client scope
   `storybook-mcp`. client secret과 Dynamic Client Registration은 쓰지 않는다.
3. 읽기 권한은 `/admins` 그룹이다. 다른 검토자 그룹은 POL-0101 예외 절차를 따른다.

Keycloak 26은 RFC 8707 `resource` 매개변수를 실험 기능으로만 지원하므로 audience는
위 client scope의 Audience mapper가 넣는다.

#### 소비 워크스페이스 설정

소비 워크스페이스의 project 설정에 둔다. hy-home.docker와 사용자 전역 설정은
바꾸지 않는다. Claude Code `.mcp.json`:

```json
{
  "mcpServers": {
    "hyhome-storybook": {
      "type": "http",
      "url": "https://storybook-mcp.hy.home.arpa/mcp",
      "oauth": {
        "clientId": "storybook-mcp-client",
        "callbackPort": 33418,
        "scopes": "openid storybook-mcp",
        "authServerMetadataUrl": "https://keycloak.hy.home.arpa/realms/hy-home.realm/.well-known/openid-configuration"
      }
    }
  }
}
```

Claude Code는 처음 사용할 때 project 서버 승인을 묻고 `/mcp`에서 브라우저 로그인을
시작한다. Codex `.codex/config.toml`(신뢰된 project에서만 읽음):

```toml
[mcp_servers.hyhome_storybook]
url = "https://storybook-mcp.hy.home.arpa/mcp"
scopes = ["openid", "storybook-mcp"]
enabled_tools = ["docs-list", "docs-show", "docs-show-story"]

[mcp_servers.hyhome_storybook.oauth]
client_id = "storybook-mcp-client"
callback_port = 33419
```

그 뒤 `codex mcp login hyhome_storybook`으로 로그인한다. 두 예시는
[Claude Code MCP](https://code.claude.com/docs/en/mcp)와
[Codex MCP](https://learn.chatgpt.com/docs/extend/mcp) 문서의 키를 따른 것이며,
HOME에는 Keycloak client와 scope가 만들어져 있고 `experience`가 기동돼 있다.
관리자 브라우저 로그인은 확인했지만, 다른 워크스페이스의 실제 로그인과 tool
호출은 아직 확인하지 않았다.

#### 소비 워크스페이스 연결 확인

소비 워크스페이스에서 처음 연결할 때 다음 순서로 확인한다. token과 authorization
code는 출력하거나 기록하지 않는다.

1. 클라이언트 기기에서 `https://storybook-mcp.hy.home.arpa/.well-known/oauth-protected-resource/mcp`가
   200과 `"resource": "https://storybook-mcp.hy.home.arpa/mcp"`를 돌려주는지 본다.
   이름 해석이나 인증서 오류가 나면 아래 클라이언트 기기 조건부터 맞춘다.
2. 위 예시대로 project 설정을 넣는다. Claude Code는 `/mcp`에서
   `hyhome-storybook`을 골라 로그인하고, Codex는 `codex mcp login hyhome_storybook`을
   실행한다. 브라우저에서 `/admins` 그룹 계정으로 로그인한다.
3. 연결 뒤 `docs-list`를 한 번 호출해 문서 목록이 오는지 본다. 이어서
   `docs-show`로 문서 하나를 연다.
4. 결과를 이렇게 읽는다.
   - 401: token이 없거나 audience가 맞지 않는다. `storybook-mcp` scope를 요청했는지
     확인한다.
   - 403 `insufficient_scope`: 계정이 `/admins` 그룹에 속하지 않는다.
   - 로그인 창의 redirect URI 오류: callback 포트가 33418(Claude Code)이나
     33419(Codex)와 다르거나, Codex redirect URI가 `/callback/*`로 등록되지 않았다.
   - `OAuth metadata discovery failed ... error sending request`: 요청이 서버에
     닿지 않았다. 그 기기에서 이름 해석, root CA 신뢰, proxy 환경 변수를 확인한다.
   - 로그인 뒤 브라우저에 "사이트를 연결할 수 없음": 브라우저와 Codex가 다른 기기에
     있다. callback은 브라우저 기기의 `127.0.0.1`로 가기 때문이다. 로그인 명령이
     기다리는 동안 그 주소창의 URL 전체를 Codex 기기에서 `curl '<URL>'`로 보내거나,
     브라우저 기기에서 `ssh -L 33419:127.0.0.1:33419 <Codex 기기>`를 연 뒤 다시
     로그인한다. Claude Code는 33418을 같은 방법으로 쓴다.
5. 확인한 날짜, 워크스페이스, 클라이언트 종류와 결과(성공, 401, 403)만 해당 Spec
   Task에 남긴다.

#### 클라이언트 기기 조건

- `*.hy.home.arpa`가 HOME 주소(LAN)로 해석되어야 한다. HOME 밖의 클라우드 실행기나
  원격 세션은 이 이름과 주소에 닿지 않는다.
- HOME 인증서는 mkcert CA가 발급하므로 클라이언트 기기가 그 root CA를 신뢰해야
  한다. Node 기반 Claude Code는 `NODE_EXTRA_CA_CERTS`, Codex는
  `CODEX_CA_CERTIFICATE`로 root CA 파일을 지정할 수도 있다. 설정 방법은 아래
  [root CA와 환경 변수 설정](#root-ca와-환경-변수-설정)에 있다.
- Codex는 callback 경로 뒤에 매번 다른 경로 조각을 붙인다
  (`/callback/<임의 값>`). 그래서 Codex redirect URI는 `/callback/*`로 등록한다.
  정확히 `/callback`만 등록하면 Keycloak이 `Invalid parameter: redirect_uri`로
  거부한다.
- token 수명은 Keycloak realm 설정을 따르며 client가 refresh로 갱신한다. 폐기는
  RUN-0014의 session·token 절차를 따른다.

#### root CA와 환경 변수 설정

HOME에서 `mkcert -CAROOT`가 가리키는 디렉터리의 `rootCA.pem`만 클라이언트 기기로
복사한다. 같은 디렉터리의 `rootCA-key.pem`은 CA 개인 키이므로 어떤 기기로도
복사하지 않는다. 두 환경 변수는 프로그램이 시작될 때 한 번 읽히므로, 설정한 뒤
새 터미널을 열거나 다시 로그인해야 적용된다.

Ubuntu(Linux):

```bash
mkdir -p ~/.local/share/hy-home
cp rootCA.pem ~/.local/share/hy-home/rootCA.pem   # HOME에서 복사해 온 파일

# 시스템 전체 신뢰(curl, 브라우저 일부). 확장자는 .crt여야 한다.
sudo cp ~/.local/share/hy-home/rootCA.pem /usr/local/share/ca-certificates/hy-home-mkcert.crt
sudo update-ca-certificates

# 셸 시작 파일(~/.profile, zsh면 ~/.zshrc)에 추가
export NODE_EXTRA_CA_CERTS="$HOME/.local/share/hy-home/rootCA.pem"
export CODEX_CA_CERTIFICATE="$HOME/.local/share/hy-home/rootCA.pem"
```

새 셸에서 `printenv NODE_EXTRA_CA_CERTS CODEX_CA_CERTIFICATE`로 경로가 나오는지
확인한다.

Windows(PowerShell, 관리자 권한 불필요):

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.hy-home" | Out-Null
Copy-Item .\rootCA.pem "$env:USERPROFILE\.hy-home\rootCA.pem"   # HOME에서 복사해 온 파일

# 현재 사용자 신뢰 저장소에 추가(브라우저, Windows 앱)
Import-Certificate -FilePath "$env:USERPROFILE\.hy-home\rootCA.pem" -CertStoreLocation Cert:\CurrentUser\Root

# 사용자 환경 변수로 영구 설정
[Environment]::SetEnvironmentVariable("NODE_EXTRA_CA_CERTS", "$env:USERPROFILE\.hy-home\rootCA.pem", "User")
[Environment]::SetEnvironmentVariable("CODEX_CA_CERTIFICATE", "$env:USERPROFILE\.hy-home\rootCA.pem", "User")
```

새 PowerShell 창에서 `$env:NODE_EXTRA_CA_CERTS`와 `$env:CODEX_CA_CERTIFICATE`로
경로를 확인한다. `Import-Certificate`를 실행하면 신뢰 확인 창이 뜨므로 지문을
확인한 뒤 수락한다. WSL 안에서 실행하는 Claude Code·Codex는 Windows가 아니라
Ubuntu 절차를 따른다.

이름 해석은 기기의 DNS를 HOME의 dnsmasq로 지정하는 방법이 가장 단순하다. 그렇게
할 수 없으면 hosts 파일에 `192.168.0.13 storybook-mcp.hy.home.arpa keycloak.hy.home.arpa`를
추가한다. Ubuntu는 `/etc/hosts`, Windows는
`C:\Windows\System32\drivers\etc\hosts`이며 둘 다 관리자 권한이 필요하다.

로컬 개발용 `npm run mcp:docs`(`127.0.0.1:7613`, 인증 없음, loopback 전용)는 그대로
남는다. Storybook의 AI·manifest 기능은 [preview](https://storybook.js.org/docs/ai/manifests)이고
schema가 안정 API가 아니므로, 고정된 `@storybook/mcp` 버전의 tool 목록과 manifest
내용을 시험으로 고정해 변경을 감지한다.

### Claude Design 전달

Claude Design은 Claude Code와 별개 제품이다. Claude Code의 `/design-sync`가 현재
저장소의 React 디자인 시스템을 Claude Design에 올리고, `/design`과 Claude
Design의 "Hand off to Claude Code"가 반대 방향을 맡는다. `/design-sync`가 올리는
파일 범위를 제한하는 공식 옵션은 확인되지 않았으므로 저장소에서 직접 실행하지
않는다. 대신 검토된 파일만 담은 bundle을 만들어 그 안에서 실행한다.

```bash
python3 scripts/operations/storybook_design_export.py <빈 디렉터리>
cd <빈 디렉터리> && claude   # /design-login 후 /design-sync "hy-home shared UI"
```

bundle은 `projects/storybook/nextjs/design-export.allowlist.json`이 이름 붙인
커밋된 파일(UI 패키지 소스·CSS 토큰, 상태별 story, 소개 문서)과
그 SHA-256 `export-manifest.json`만 담는다. glob, 상위 경로, `.env`·secret·key
파일, secret 형태의 내용이 있으면 내보내지 않는다. 내부 URL, cookie, 사용자
자료, 저장소 전체는 대상이 아니다.

작업 순서는 다음과 같다.

1. Claude Design에서 동기화된 토큰과 컴포넌트로 화면을 설계한다.
2. 결과를 Claude Code로 hand off하고 `packages/ui`를 바꾼다.
3. 상태별 story와 play 함수로 동작을 고정하고 `npm run coverage`로 상호작용·
   a11y 시험을 통과시킨다.
4. PR 검토와 병합 후 image를 그 커밋으로 다시 빌드하고 bundle을 다시 내보낸다.

`/design-sync`는 코드·토큰 전달 경로이며 localhost MCP 도달성이나 Claude Design
계정 권한의 증거가 아니다. 공무원 학습·언어 앱의 미승인 기획을 이 Storybook의
업무 화면이나 음성 원본으로 추가하지 않는다.

### Common Checks

저장소 root에서 공개 예제 환경으로 선택형 서비스 선언만 정적 확인한다.

```bash
docker compose --env-file .env.example --profile experience config --quiet
python3 scripts/validation/check-operations-catalog.py
```

이 검사는 브라우저 TLS/SSO, 실제 이미지 health, package 소비, MCP protocol,
Claude Design 계정 연동을 증명하지 않는다. image와 격리 인증 검사는
[RUN-0101](../runbooks/0101-storybook.md)의 `storybook_image.py`와 rehearsal이 맡는다. 해당 증거와 승인 경계는
[RUN-0101](../runbooks/0101-storybook.md)과 승인된 운영 Task에서 구분한다.

### Runbook Handoff

이미지 빌드·격리 HTTP 검사·HOME 실행 사전 점검과 rollback 순서는
[RUN-0101](../runbooks/0101-storybook.md)을 따른다. 운영 follow-up 소유자는
GDE/POL/RUN-0101이며 trigger는 HOME route 활성화, 검토자 그룹 승인, 원격 MCP
OIDC 승인, 외부 디자인 계정 사용 승인 또는 DNS/TLS 관찰 요청이다.

### Traceability

- Artifact: `GDE-0101`; governing policy: `POL-0101`.
- 역사적 source/static 완료 근거: `SPEC-0206`. 아키텍처 맥락 `AD-0031`은 draft 상태이며 이 가이드가 승격하지 않는다.
- Runtime declaration: `infra/13-experience/storybook/docker-compose.yml`.

## Related Documents

- [Shared Storybook policy](../policies/0101-storybook.md)
- [Shared Storybook runbook](../runbooks/0101-storybook.md)
- [Storybook source package](../../../projects/storybook/nextjs/README.md)
- [Traefik guide](0013-traefik.md)
