---
title: "01-Gateway Nginx Operations Policy"
version: "1.2.1"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "operations"
artifact_id: "POL-0011"
parent_ids:
- "AD-0001"
created: "2026-05-17"
---

# 01-Gateway Nginx Operations Policy

## Overview

이 문서는 `01-gateway`의 Nginx 운영 정책을 정의한다. Nginx는 특수 경로(`/oauth2/`, `/keycloak/`, `/cdn/`) 프록시 역할을 수행하며, `Balanced` 하드닝 기준을 준수한다.

## Scope

- `infra/01-gateway/nginx/docker-compose.yml`
- `infra/01-gateway/nginx/config/nginx.conf`
- Nginx healthcheck/readonly/tmpfs 운영 표준 and the `nginx` profile runtime boundary
- **Systems**: Nginx gateway proxy
- **Environments**: Local, Dev, Stage, Production-like

## Rules

- **필수**:
  - `check-all-hardening.sh 01-gateway` 실패 0건을 유지해야 한다.
  - `/ping` 실패, 반복 5xx 증가, 인증 루프 발생 시 즉시 런북 절차를 수행해야 한다.
  - Nginx 서비스는 `template-infra-readonly-low`를 사용해야 한다.
  - 필수 `tmpfs`: `/var/cache/nginx`, `/var/log/nginx`, `/var/run`
  - healthcheck는 `/ping` 경로를 사용해야 한다.
  - `server_tokens off;`를 유지해야 한다.
  - `proxy_connect_timeout`, `proxy_send_timeout`, `proxy_read_timeout`을 명시해야 한다.
  - 업스트림 서버는 `max_fails`, `fail_timeout` 정책을 명시해야 한다.
  - `proxy_next_upstream` 정책을 명시해야 한다.
  - 정적 자산 확장자 기반 캐시 정책(`expires`, `Cache-Control`)을 유지해야 한다.
  - `nginx`를 `${HOST_LAN_BIND_IP:-192.168.0.13}`의 host ports 80/443을
    점유하는 Traefik profile과 함께 선택하지 않는다.
  - Git config와 private certificate backup authority를 구분한다. tmpfs는 복구
    대상이 아니며 private key를 repository/evidence에 복사하지 않는다.
- **허용**:
  - 서비스 특성(대용량 업로드/다운로드)에 따른 location 단위 timeout override
- **금지**:
  - `/ping`, `/oauth2/`, `/keycloak/`, `/cdn/` 기본 흐름 훼손
  - readonly 환경에서 영구 쓰기 경로 의존 설정

### Known implementation limitations

`/ping` health 요구는 유지한다. 현재 HTTP probe는 HTTPS redirect와 인증서 검증을
거치므로 직접 200 검사로 설명할 수 없다. `/app/`의 placeholder 200은 인증과
rate limit 통과 증거가 아니며 backend proxy는 비활성이다. 이 경로를 실제 보호 앱에
재사용하기 전 별도 구현 수정과 인증·거부 검증이 필요하다. 변경 가능한 Nginx tag와
단일 upstream은 version 고정이나 failover 보장을 제공하지 않는다.

### Shared controls and accountability

운영 책임자는 @buenhyden이다. 변경·재시작·credential 작업의 대상과 영향, 승인,
종료 조건을 기록하며 예외는 위험·만료·원복 책임까지 명시한다. 공통 자원 상한과
mount 적용은 [POL-0006](0006-infrastructure-optimization-governance.md), profile·
상호 배제는 [POL-0078](0078-compose-profile-vocabulary.md), image 변경과 검토는
[POL-0086](0086-dependency-version-management.md)을 적용한다. OOM·반복 재시작·
인증 실패 증가 또는 이미지·노출·mount 변경 시 정기 주기를 기다리지 않고 검토한다.
보존할 상태와 private credential은 [POL-0021](0021-backup-and-restore.md)의
접근·암호화·retention을 적용한다. 제거 전에 소비자와 복구 입력을 확인하고,
volume·인증서·secret 삭제는 서비스 중지와 분리된 승인 대상으로 한다.

## Exceptions

- 장애 대응 중 임시 timeout 완화 가능. 단, 원복 계획과 변경 로그를 남겨야 한다.

### Verification

- `bash scripts/hardening/check-all-hardening.sh 01-gateway`
- `docker compose exec nginx nginx -t`와 같은 Nginx runtime lint는 root network와 backend 의존성을 갖춘 승인된 Nginx context가 실행 중일 때만 유효하다.
- `infra/01-gateway/nginx/docker-compose.yml`만 독립적으로 compose rendering한 결과는 readiness 증거가 아니다.

### Recovery and Upgrade Controls

Rollback은 검토된 config commit과 이에 맞는 private certificate 세트를 복구한 뒤,
실제 SeaweedFS/auth 의존성을 사용하여 모든 특수 경로를 검증한다.
image upgrade에는 `nginx -t`, 대표 route의 수용 검증, 같은 config로 복구할 수 있는
이전 image 선언이 필요하다.

### Review Cadence

- 월 1회 정기 점검
- nginx.conf 변경 시 수시 점검

### Traceability

- Declared parent: [Gateway Tier Architecture Description](../../02.architecture/descriptions/0001-gateway-architecture.md) (`AD-0001`)
- Subject peers: [Guide](../guides/0011-nginx.md) (`GDE-0011`), [Runbook](../runbooks/0011-nginx.md) (`RUN-0011`)

## Related Documents

- [Official upstream operational documentation](https://nginx.org/en/docs/beginners_guide.html)

- 런타임 버전은 Compose/Dockerfile 선언이 소유하며, [파생 Compose 이미지 목록](../../../infra/tech-stack.versions.json)은 drift 검증에 사용한다.

- [Operations index](../README.md)
- [Usage guide](../guides/0011-nginx.md)
- [Recovery runbook](../runbooks/0011-nginx.md)
