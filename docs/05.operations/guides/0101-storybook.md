---
title: "Shared Storybook Usage Guide"
version: "0.1.0"
type: "operation/guide"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-03"
layer: "operations"
artifact_id: "GDE-0101"
parent_ids:
- "POL-0101"
implementation_services:
  infra/13-experience/storybook/docker-compose.yml:
  - "storybook"
created: "2026-10-03"
---

# Shared Storybook Usage Guide

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
현재 route의 브라우저 검토자는 관리자뿐이다. 비인증 index·asset 요청은
로그인 HTML redirect 대신 401/403을 받도록 `sso-errors@file`은 연결하지 않는다.
브라우저에서는 먼저 `https://auth.${DEFAULT_URL}/oauth2/start?rd=<URL-encoded https://storybook.${DEFAULT_URL}/>`
경로로 수동 로그인한 뒤 Storybook으로 이동한다. [OAuth2 Proxy의 start endpoint](https://oauth2-proxy.github.io/oauth2-proxy/features/endpoints/)와
추적된 auth router가 이 경로를 지원하지만 HOME 브라우저 UX는 아직 시험하지 않았다.
검토자 그룹, DNS/TLS 실연결, 운영 기동은 각각 별도 승인과 관찰이 필요하다.

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
별도 `@storybook/mcp` 서버를 구분한다. 현재 저장소의 MCP는 로컬
`mcp:docs` 프로세스가 문서 읽기 도구만 제공한다. root Compose에는 MCP service,
port, router가 없고 원격 OIDC audience/client도 없다. 비인증 원격 공유나
브라우저 ForwardAuth cookie 재사용은 지원 계약이 아니다.

### Codex와 Claude Design

Codex에서 로컬 MCP를 사용하려면 Storybook 빌드와 로컬 MCP 프로세스가 같은
호스트에서 실행되는지 확인한 뒤, 사용자가 해당 Codex client의 MCP 설정에
loopback endpoint를 직접 등록한다. [Codex MCP 공식 문서](https://developers.openai.com/codex/mcp)는
CLI와 client 설정의 STDIO·Streamable HTTP 경로를 설명한다. 원격 Codex의
`localhost`는 이 서버의 host가 아니므로 원격 endpoint로 간주하지 않는다.
정확한 endpoint와 확인 명령은 구현 소유
[Storybook README](../../../projects/storybook/nextjs/README.md)를 따른다.
프로젝트 템플릿이나 사용자 전역 설정에는 MCP를 자동 추가하지 않는다.
같은 host에서 사용자가 직접 등록할 때의 Codex 설정 예시는 다음과 같다.
이 예시는 설정을 수정하지 않으며, 연결 성공도 증명하지 않는다.

```toml
[mcp_servers.hyhomeStorybookDocs]
url = "http://127.0.0.1:7613/mcp"
enabled_tools = ["docs-list", "docs-show", "docs-show-story"]
```

Claude Code도 [공식 MCP 설정 문서](https://code.claude.com/docs/en/mcp)에 따라
사용자가 같은 host의 HTTP endpoint를 로컬 scope로 등록할 수 있다.
`claude mcp add --transport http hyhome-storybook-docs --scope local http://127.0.0.1:7613/mcp`
는 `~/.claude.json`을 바꾸므로 여기서는 실행하지 않는다. 실제 클라이언트 연결은
각 사용자의 설치 버전과 권한에서 확인해야 한다.

[Claude Design 공식 안내](https://support.claude.com/en/articles/14604416-get-started-with-claude-design)는
codebase/design system import, Claude Code의 `/design-sync`와 `/design` 경로를
설명한다. 현재 설치된 계정·client의 명령 지원과 권한은 별도로 확인해야 한다.
Storybook과 Claude Design 간 전용 양방향 MCP 동기화는 이 구현의 검증 결과가
아니다. 승인된 UI 코드·토큰·합성 화면만 전달하고 내부 URL·환경 파일·
실사용자 데이터는 외부 디자인 도구로 보내지 않는다.

공통 흐름은 문서·상태 확인, 디자인 검토, 승인된 코드 구현, 상태별 story,
접근성·상호작용·회귀 검사 순서다. 공무원 학습·언어 앱의 미승인 기획을
이 Storybook의 업무 화면이나 음성 원본으로 추가하지 않는다.

## Common Checks

저장소 root에서 공개 예제 환경으로 선택형 서비스 선언만 정적 확인한다.

```bash
docker compose --env-file .env.example --profile experience config --quiet
python3 scripts/validation/check-operations-catalog.py
```

이 검사는 브라우저 TLS/SSO, 실제 이미지 health, package 소비, MCP protocol,
Claude Design 계정 연동을 증명하지 않는다. 해당 증거와 승인 경계는
[RUN-0101](../runbooks/0101-storybook.md)과 SPEC-0206의 Task에서 구분한다.

## Runbook Handoff

이미지 빌드·격리 HTTP 검사·HOME 실행 사전 점검과 rollback 순서는
[RUN-0101](../runbooks/0101-storybook.md)을 따른다.

## Traceability

- Artifact: `GDE-0101`; governing policy: `POL-0101`.
- Source contract: `SPEC-0206`; architecture context: `AD-0031`.
- Runtime declaration: `infra/13-experience/storybook/docker-compose.yml`.

## Related Documents

- [Shared Storybook policy](../policies/0101-storybook.md)
- [Shared Storybook runbook](../runbooks/0101-storybook.md)
- [Storybook source package](../../../projects/storybook/nextjs/README.md)
- [Traefik guide](0013-traefik.md)
