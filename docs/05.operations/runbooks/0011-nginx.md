---
title: "01-Gateway Nginx Runbook"
version: "1.1.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "RUN-0011"
parent_ids:
- "GDE-0011"
created: "2026-05-17"
---

# 01-Gateway Nginx Runbook

## Overview

## Trigger and Preconditions

### Overview

### Trigger and Preconditions

### Overview

이 런북은 Nginx readonly/tmpfs 전환 이후 발생 가능한 장애, `nginx -t` 실패, `/ping` 헬스체크 실패 상황의 복구 절차를 정의한다.

> Scope: Nginx Special-path Proxy Recovery

### Purpose

- readonly/tmpfs 운영 안정성 확보
- config lint 실패 시 안전 롤백
- 특수 경로 프록시(`/oauth2/`, `/keycloak/`, `/cdn/`) 정상성 회복

### When to Use

- `nginx -t` 실패
- `/ping` healthcheck 반복 실패
- readonly 전환 후 캐시/로그/PID 쓰기 오류
- 백엔드 장애 전환(failover) 동작 이상

## Procedure

### Procedure

### Target and prerequisites

저장소 루트와 승인된 Docker context에서 `nginx`만 대상으로 한다. root network,
`seaweedfs-s3`, `oauth2-proxy`, `keycloak`의 주소·준비 상태와 80/443 비점유를
확인한다. `nginx` profile은 인증 의존성을 자동 선택하지 않는다. 인증서 세트와
실제 배포 이미지 identity를 owner가 확인하기 전에는 기동하지 않는다. 현재 mutable
image와 HTTP health redirect 때문에 isolated runtime 수용 검증은 미완료다.
전체 `core`/`dev`/`local` 선택으로 의존성을 해결하면 Traefik과 충돌하므로 금지한다.

### Static checks and diagnosis

```bash
HYHOME_COMPOSE_PROFILES=nginx bash scripts/validation/validate-docker-compose.sh
bash scripts/hardening/check-all-hardening.sh 01-gateway
```

성공은 구성 계약 확인뿐이다. 누락된 dependency/profile이 나오면 올바른 root
선택을 owner와 확정하고 멈춘다. 실패를 피하려고 service-local 렌더링으로 바꾸지 않는다.
승인된 Nginx가 이미 실행 중이면 다음 lint를 수행한다.

```bash
docker compose exec -T nginx nginx -t
```

exit 0이 필요하다. DNS 오류는 세 upstream의 준비, 쓰기 오류는
`/var/cache/nginx`, `/var/log/nginx`, `/var/run` tmpfs, TLS 오류는 인증서 파일명과
CA/hostname을 확인한다. 오류 위치만 정제해 남기며 private key·원문 요청 로그는
첨부하지 않는다. Compose나 설정 수정은 별도 승인 범위에서 수행한다.

### Startup, shutdown and configuration change

기존 image, root network와 모든 의존성이 준비되고 서비스 중단·재생성이 승인된
경우에만 다음 대상 명령을 사용한다. `--no-deps`는 dependency를 준비하지 않는다.
Nginx 시작은 80/443을 점유하고 stop은 해당 진입 트래픽을 중단한다.

```bash
docker compose --profile nginx up -d --no-deps --no-build --pull never nginx
# 승인된 중지에만 실행한다.
docker compose stop nginx
```

단일 파일 mount 설정을 변경했다면 `restart`나 `nginx -s reload`만으로는 바뀐
inode를 읽는다고 보장할 수 없다. [POL-0006](../policies/0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary)에
따라 해당 서비스만 `up -d --no-deps --no-build --pull never --force-recreate nginx`로
재생성하고 그 문서의 post-apply hash 검사를 수행한다. 동일 mount의 내용만 검증된
reload는 `nginx -t` 성공 뒤 승인된 `docker compose exec nginx nginx -s reload`로
수행한다. lint 실패 상태에서는 reload하지 않는다.

### Acceptance and stop conditions

- HTTPS `/ping`은 trusted CA·일치하는 hostname으로 200/pong을 확인한다.
  HTTP `/ping`은 현재 301이 정상 source 동작이다. health probe 실패를 TLS 검사
  비활성화로 숨기지 않는다. 이 불일치는 별도 구현 수정 대상이다.
- `/oauth2/`의 실제 로그인/callback/거부와 `/keycloak/` prefix·issuer 호환성을
  따로 확인한다. 200만으로 SSO가 작동한다고 기록하지 않는다.
- `/cdn/` 루트는404, 알려진 공개 객체 GET/HEAD만 허용하고 쓰기/삭제는 거부되어야
  한다. 시험 쓰기나 삭제는 별도 승인이 없으면 수행하지 않는다.
- `/app/` placeholder 200은 `auth_request` 이전 종료이므로 보호 검증에서 제외한다.
  backend proxy는 주석이다. 실제 앱 연결 전에 구현 수정과 독립 인증 검증이 필요하다.
- timeout·`proxy_next_upstream`·`max_fails/fail_timeout`을 확인하되 단일 upstream을
  다중 노드 failover로 보고하지 않는다. 실패 시 트래픽 전환을 멈춘다.

## Verification

### Evidence

시각, source revision, 승인 대상, lint 종료 상태, HTTP/HTTPS 구분, route별
최소 상태 코드, 수행하지 않은 검증을 Task/Incident에 기록한다. 원문 access/error
로그와 인증정보는 수집하지 않고 오류 종류·빈도만 전달한다.

## Rollback and Escalation

### Rollback or Recovery

1. Traefik이 같은 listener를 점유하지 않는지 확인하고 마지막 검토된 Compose와
   `nginx.conf`를 복구한다. 인증서는 private owner의 일치하는 세트를 사용한다.
2. 위 static/lint와 승인된 대상 재생성·hash 검사를 따른다. lint 실패 또는 실제
   route 동작 불일치 시 80/443 트래픽 전환을 멈춘다.
3. upgrade는 [RUN-0086](0086-dependency-version-management.md)에 따라 실제 이미지
   identity와 이전 identity를 보존하고 OAuth2/Keycloak/read-only CDN을 canary에서
   검증한다. mutable tag 문자열만으로 이전 byte 복구를 보장하지 않는다.
4. cache/log/PID tmpfs는 복원 대상이 아니다. 중지와 인증서·설정 삭제를 혼동하지
   않으며 정리는 [Policy](../policies/0011-nginx.md)의 승인·보존 기준을 따른다.

격리 검증 환경과 현재 Nginx route 수용 결과는 제공되지 않았다. 기존 2026-09-20
교정과 이번 문서 감사 모두 복구를 실행하지 않았다.

### Escalation

반복 lint/health 실패, OOM·5xx 증가, 인증 루프, placeholder를 보호 route로
사용하려는 변경, secret 노출 징후 또는 dependency 불명은 @buenhyden에게
전달한다. 여러 앱 영향은 [RUN-0099](0099-system-operations.md)로 연결한다.
원인 후보, 정제된 결과와 미검증 항목을 남기고 임의 전체 재시작은 하지 않는다.

### Traceability

- Declared parent: [01-Gateway Nginx Usage Guide](../guides/0011-nginx.md) (`GDE-0011`)
- Governing authority: [Gateway Tier Architecture Description](../../02.architecture/descriptions/0001-gateway-architecture.md) (`AD-0001`)
- Subject peers: [Guide](../guides/0011-nginx.md) (`GDE-0011`), [Policy](../policies/0011-nginx.md) (`POL-0011`)

## Related Documents

- [Official upstream operational documentation](https://nginx.org/en/docs/beginners_guide.html)

- 런타임 버전은 Compose/Dockerfile 선언이 소유하며, [파생 Compose 이미지 목록](../../../infra/tech-stack.versions.json)은 drift 검증에 사용한다.

- [Operations index](../README.md)
- [Usage guide](../guides/0011-nginx.md)
- [Operations policy](../policies/0011-nginx.md)
