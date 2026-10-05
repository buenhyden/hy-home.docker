---
title: "Gatus Implementation"
version: "0.3.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-05"
---

# Gatus

## Overview

설정된 엔드포인트 가용성을 모니터링하고 SQLite 이력을 `gatus-data`의
`/data/gatus.db`에 저장합니다. Compose는 호스트에 직접 게시하지 않고 네이티브
Keycloak OIDC 설정을 선택합니다. 네이티브 로그인 승인이 기록된 이후, 라우터는
표준 게이트웨이 체인만 유지하며 OAuth2 Proxy ForwardAuth는 제거되었습니다.
모니터가 정상이라고 해서 모니터링 대상 애플리케이션이 모두 정상 동작함을
증명하지는 않습니다.

## Audience

서비스 설정을 검토하는 운영자와 개발자.

## Scope

Lifecycle: **HOME**. 운영 통제와 복구는 [documentation index](../../../docs/README.md)를 거쳐 `docs/05.operations/guides/0087-gatus.md`, `docs/05.operations/policies/0087-gatus.md`, `docs/05.operations/runbooks/0087-gatus.md`(ID: `GDE-0087`, `POL-0087`, `RUN-0087`)가 담당합니다.

## Structure

[Compose](../docker-compose.yml)가 서비스, 마운트, 네트워크 권한, 엔트리포인트를 소유합니다.

## Tech Stack

업스트림 빌드 고정 값은 [Dockerfile](Dockerfile)에, 런타임 설정은 [Compose](../docker-compose.yml)에 속합니다. [버전 레지스트리](../../../infra/tech-stack.versions.json)는 정제된 프로젝션이며 배포 매니페스트가 아닙니다.

## Configuration

프로필: `availability / obs / dev`. 루트 Compose가 이 정의를 include하지만 include 자체만으로는 서비스가 시작되지 않습니다. 네트워크는 `edge_net`과 `obs_net`입니다. 비공개 값을 출력하지 않고 [공개 환경 변수 키](../../../.env.example)와 [시크릿 참조](../../../secrets/README.md)를 검토합니다.

기밀 클라이언트 ID는 `home-gatus`이며 정확한 콜백은
`https://status.<domain>/authorization-code/callback`입니다. 클라이언트
시크릿은 엔트리포인트가 Docker Secret에서 읽습니다. Gatus는
`allowed-subjects`를 ID 토큰의 불변 `sub` 클레임과 비교하므로,
`GATUS_OIDC_ALLOWED_SUBJECT`에는 정확한 Keycloak subject 값이 들어 있어야
합니다. 시크릿, subject, 도메인, CA 입력값이 없으면 엔트리포인트는 fail-closed
방식으로 동작합니다.

이미지는 [Dockerfile](Dockerfile)에서 선택한 불변 업스트림 소스를 빌드하고,
아카이브 체크섬을 검증한 뒤 [로컬 OIDC 하드닝 패치](patches/oidc-hardening.patch)를
퍼지(fuzz) 없이 적용합니다. 이 패치는 S256 PKCE, secure 및 HTTP-only 쿠키,
1회용 state/nonce/PKCE 쿠키 정리, 인증된 상태 데이터 라우트, 소스 수준
회귀 테스트를 추가합니다. 이 로컬 패치는 고정된 업스트림 구현이 해당
통제를 갖추지 않았기 때문에 필요하며 업스트림 소스를 변경할 때는
다시 검토해야 합니다.

외부 라우트 경계는 다음과 같습니다.

| Route | Boundary | Reason |
| --- | --- | --- |
| `/`, `/endpoints/*`, `/suites/*`, 정적 자산 | Public bootstrap | 네이티브 세션이 존재하기 전에 SPA와 로그인 화면이 먼저 로드되어야 합니다. |
| `/oidc/login`, `/authorization-code/callback` | OIDC protocol | authorization-code 플로우를 시작하고 완료합니다. |
| `/api/v1/config` | Public minimal bootstrap | `oidc`와 `authenticated` 플래그, UI 공지를 반환합니다. 공지는 OIDC 인증에 성공하기 전까지는 비어 있습니다. |
| `/health` | Public minimal probe | 컨테이너 헬스체크에 필요하며 응답에는 헬스 상태만 포함됩니다. |
| `/metrics` | Internal network only | Prometheus가 컨테이너를 직접 스크레이프합니다. Traefik 라우터는 이 경로를 제외하므로 공개 호스트명으로는 일치하는 Gatus 라우트가 없습니다. |
| 엔드포인트/suite 상태, 헬스 배지, 가동 시간, 응답 시간 배지/차트/이력 | Native OIDC session | 이 모니터링 데이터 라우트들은 동일한 세션 미들웨어를 사용합니다. |
| `POST /api/v1/endpoints/:key/external` | Per-endpoint bearer token | 머신 수집은 독립된 토큰 경계를 유지합니다. |

## Validation

저장소 루트에서 문서화된 프로필을 선택하고
`scripts/validation/validate-docker-compose.sh`를 실행합니다. 이미지 빌드는
패치된 업스트림 보안 테스트를 실행합니다. 런타임 확인은 소유 Runbook을
사용합니다. 설정 검증만으로는 네이티브 로그인, 로그아웃, 거부, 세션 만료,
모니터링 이력 복구를 증명하지 못합니다.

## Usage

변경 작업 중에는 데이터와 자격 증명을 보존합니다. 배포 전에 정확한 런타임
대상을 검토합니다. 운영 절차는 기존 운영 주제(operations subject) 안에
유지합니다.

### Convergence contract

- Classification: **HOME**. Exact profiles: `obs`, `availability`, `dev`.
- Source authority: `infra/06-observability/docker-compose.yml`과 이 패키지의 추적 설정/빌드 입력. 이미지 선언이 권위이며 `infra/tech-stack.versions.json`은 파생 값입니다.
- Root preflight: `docker compose --profile obs config --quiet`. Root targeted start: `docker compose --profile obs up -d gatus`.
- 안정적인 진입점은 [docs/README.md](../../../docs/README.md)입니다. 정확한 Stage 05 경로: `docs/05.operations/guides/0087-gatus.md`; ID: `GDE-0087`, `POL-0087`, `RUN-0087`.
- 해당 런북의 계획된 격리 복구 절차를 따릅니다. 날짜가 명시된 근거가 없는 한 아직 실행되지 않은 것으로 간주하며 이 README에서 운영 중인 상태를 변경하지 않습니다.

## Related Documents

- [Infrastructure index](../../../infra/README.md)
- [Documentation index](../../../docs/README.md)
