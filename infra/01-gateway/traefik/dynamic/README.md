---
title: "Traefik Dynamic Configuration"
version: "1.0.10"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
---

# Traefik Dynamic Configuration

Traefik은 이 디렉터리의 설정을 재시작 없이 hot-reload합니다.

- **middleware.yml**: `sso-auth`(ForwardAuth), `dashboard-auth`(BasicAuth) 같은 재사용 가능한 미들웨어를 정의합니다.
- **tls.yaml**: 기본 TLS store와 인증서 위치를 정의합니다.
- **hermes.yml**: host systemd unit으로 도는 Hermes Agent dashboard를 `hermes.<DEFAULT_URL>`로
  노출합니다. container가 아니므로 Docker label 대신 edge_net gateway IP로 연결하며, dashboard가
  자체 OIDC 인증을 하므로 Traefik 인증 middleware를 겹치지 않습니다.
- **hermes-webhook.yml**: Hermes 호스트의 `POST /webhook/hermes-blog-ingestion` 하나를 별도 router로 n8n에
  보냅니다. n8n의 나머지 경로는 2026-11-09부터 SSO 없이 `gateway-standard-chain@file`과 n8n 자체 로그인을 쓰며, n8n router는 `/metrics`와 Hermes 경로 접두를 대소문자 구분 없이 제외하며(`PathRegexp` `(?i)`), 이 router는 정확한 경로만 받으므로 대소문자가 다른 Hermes 요청은 어느 router에도 맞지 않아 404입니다. 출발지 `<HOST_LAN_BIND_IP>/32`, 본문 1 MiB, 분당 6회. 인증은 n8n 헤더 인증입니다.
- **blog-export.yml**: `blog-export.<DEFAULT_URL>`에서 Windows B(`<BLOG_EXPORT_RECEIVER_IP>/32`)의 Export 조회·ACK와
  서버 A 호스트(`<HOST_LAN_BIND_IP>/32`)의 Attestation만 Blog-data Gateway로 보냅니다. 다른 경로는 404입니다.
  세 파일의 호스트와 출발지는 `{{ env "이름" }}`으로 Traefik 환경에서 읽습니다. 값은 `.env`의 `DEFAULT_URL`,
  `HOST_LAN_BIND_IP`, `BLOG_EXPORT_RECEIVER_IP`이고 Traefik Compose가 전달하므로, 값을 바꾸면 Traefik을 재생성합니다.
  변수가 비면 해당 router가 비활성화되어 요청을 받지 않습니다.
  두 파일의 출처와 승인 기록은 [수집 전송 소스](../../../07-workflow/n8n/workloads/hermes-blog-ingestion/README.md)와 RUN-0053입니다.

---

## Purpose

### Service Role

`infra/01-gateway/traefik/dynamic`는 Docker Compose 서비스, 설정, 운영 문서의 구현 위치다. 이 README는 하위 파일을 찾는 진입점이며 기존 본문과 실제 디렉터리 구조를 함께 기준으로 삼는다.

#### Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers

#### In Scope

- Compose 서비스 정의와 관련 설정 설명
- 서비스별 README와 운영 문서 연결
- 검증 시 참고해야 할 구성 파일 인벤토리

#### Out of Scope

- secret 값 원문
- 사용자 승인 없는 runtime 동작 변경
- 다른 tier의 서비스 정책 중복 정의

#### Structure

```text
infra/01-gateway/traefik/dynamic/
├── blog-export.yml  # Blog-data Export·ACK·Attestation route
├── hermes-webhook.yml  # Hermes 수집 Webhook route
├── hermes.yml  # Hermes dashboard route
├── middleware.yml  # 구성 파일
├── README.md  # 이 파일
└── tls.yaml  # 구성 파일
```

### Supported Environment

파일 공급자용 동적 설정(`blog-export.yml`, `hermes-webhook.yml`, `hermes.yml`, `middleware.yml`, `tls.yaml`)만 두며 Compose와 Dockerfile은 없다. 상위 Compose가 이 폴더를 `/dynamic`에 읽기 전용으로 마운트한다.

## Interfaces

### Inputs and Outputs

라우터 호스트는 `blog-export.`, `n8n.`, `hermes.` 하위 도메인이며, 도메인 값은 `{{ env "DEFAULT_URL" }}`로 읽는다. 별도 포트는 열지 않는다.

### Security Boundary

`tls.yaml`은 `/certs/cert.pem`과 `/certs/key.pem` 경로만 참조하며 인증서 본문은 이 폴더에 없다. 보호 대상 라우터는 `middleware.yml`의 미들웨어와 `oauth2-proxy-svc` 서비스를 거친다.

## Development

### Local Workflow

1. 상위 tier README와 해당 서비스의 `docker-compose*.yml` 또는 설정 파일을 먼저 확인한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.

### Checks

없음: 이 폴더는 자체 테스트나 검증 스크립트를 두지 않는다. Traefik 파일 공급자가 로드 오류를 로그로 남기며, 로드 결과는 `traefik` 서비스 로그로 확인한다.

## Operations

### Runbook Links

#### Related Documents

- [infra/README.md](../../../README.md)
- [Traefik 서비스 README](../README.md)
- 게이트웨이 운영 정책 (`docs/05.operations/policies/README.md`)
- [문서 인덱스](../../../../docs/README.md)

런타임 고정 값은 Compose/Dockerfile 선언이 소유하며 [curated 버전 투영](../../../tech-stack.versions.json)으로 drift를 검증합니다.

### Observability and Recovery

없음: 이 폴더는 자체 헬스체크를 선언하지 않는다. 라우터와 서비스 로드 상태는 상위 `traefik` 서비스의 헬스체크와 로그가 소유한다.
