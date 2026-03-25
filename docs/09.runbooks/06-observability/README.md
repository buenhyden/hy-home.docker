# Observability Runbook (06-observability)

> Telemetry Infrastructure Recovery & Troubleshooting

## Overview

이 런북은 `06-observability` 계층의 장애 상황에 대한 즉각적인 대응 절차를 안내한다.

## Incident Response Procedures

### 1. Prometheus Scraping 장애

지표가 수집되지 않거나 그래프가 끊기는 경우.

1. **Alloy 상태 확인**: Alloy UI (`https://alloy.${DEFAULT_URL}`)에서 커넥터 파이프라인 점검.
2. **Prometheus Targets 확인**: `https://prometheus.${DEFAULT_URL}/targets`에서 'Down' 상태의 타겟 식별.
3. **네트워크 점검**: `infra_net` 상에서 타겟 호스트와의 통신 확인.

### 2. Loki/Tempo 저장소 오류 (S3 Connectivity)

로그나 트레이스를 읽지 못하거나 쓰기 오류가 발생하는 경우.

1. **상태 코드 확인**: `500 Internal Server Error` 또는 `MinIO Connection Timeout` 여부 확인.
2. **MinIO 상태 확인**: `04-data` 계층의 MinIO 서비스 및 버킷(`loki`, `tempo`) 존재 여부 확인.
3. **Secret 확인**: `minio_app_user_password`가 정확히 주입되었는지 확인.

### 3. Grafana SSO(Keycloak) 로그인 실패

'Unauthorized' 또는 OAuth2 관련 에러 발생 시.

1. **Keycloak 상태 확인**: `02-auth` 계층의 Keycloak 서비스가 정상인지 확인.
2. **Secret 동기화**: `oauth2_proxy_client_secret`이 Keycloak 설정과 일치하는지 재발급 및 적용 검토.
3. **시간 동기화**: 호스트 머신의 시간이 어긋나면 토큰 검증이 실패할 수 있으므로 NTP 상태 확인.

---

## Verification Steps

- [ ] `docker exec infra-alloy alloy run --test ...` 로 설정 유효성 검사.
- [ ] `promtool check rules ...` 로 알람 규칙 문법 검사.

## Related Documents

- [Operations Policy](../../docs/08.operations/06-observability/README.md)
- [LGTM Stack Guide](../../docs/07.guides/06-observability/01.lgtm-stack.md)
