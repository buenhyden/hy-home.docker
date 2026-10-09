---
title: "Crawl4AI Operations Policy"
version: "1.1.1"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "operations"
artifact_id: "POL-0091"
parent_ids:
- "AD-0008"
created: "2026-09-21"
---

# Crawl4AI Operations Policy

## Overview

Crawl4AI는 SSRF가 가능한 서비스다. 검토된 consumer가 필요로 할 때까지 격리하고
인증을 적용한 채 사용하지 않는 상태로 유지한다.

## Scope

활성화, 네트워크 배치, 인증, consumer, provider key, 제거.

## Rules

- `crawl4ai`를 통해서만 선택한다. `ai`, `notebook`, HOME에 절대 추가하지 않는다.
- `crawl4ai`는 internal인 `crawl4ai_net`과 `crawl4ai_egress_net`에만 연결하고, 밖으로 나가는 경로는 `crawl4ai-egress` 하나로 둔다. gateway는 전역 라우팅되는 IPv4의 80·443만 허용하고 IPv6는 모두 거절하며, 확인한 주소로만 연결한다. 공유 서비스 네트워크 연결, host 포트 게시, public route 추가는 하지 않는다.
- 이미지 안의 egress broker, 전용 bridge, Bearer token은 외부로 나가는 요청 제한을 대신하지 않는다. gateway나 internal 네트워크를 완화하는 변경은 승인 변경으로만 한다.
- 항상 token secret과 함께 실행한다. provider key를 추적되는 파일로 전달하지 않는다.
- consumer는 이름, 토큰 출처, 호출 경로를 밝힌 검토된 변경으로만 `crawl4ai_net`에 합류한다. 출처 registry 등록은 네트워크 접근 권한이 아니다. 크롤러에는 관리 데이터, token 외 secret, Docker socket, 공유 volume을 주지 않는다. 같은 망의 consumer는 네트워크 계층에서 크롤러에 노출되므로 자기 서비스를 직접 인증한다.
- 수집하는 출처마다 제공자, 접근 방식(`api` 또는 이유가 있는 `web-fallback`), 정확한 host, 약관과 license, robots 확인, rate와 quota, 가공·재배포·모델 학습 허용, 보존 기간, 삭제 책임자를 registry에 기록한다. robots 허용을 저작권 허가로 취급하지 않는다.
- 가져온 내용은 데이터다. 그 내용을 근거로 secret 접근, 도구 실행, 정책 변경을 허용하지 않는다.

## Exceptions

선언 버전의 `/health`, `/token`, root/monitor 및 UI/static shell 예외를 인정하되 protected data/admin API 인증은 유지한다. `/token`은 별도 key/email 검증을 하며 임의 token 발급 예외가 아니다. 새로운 예외는 승인된 변경 없이는 추가하지 않는다.

### Verification

정적 렌더링과 template baseline을 확인한다. 승인된 런타임 검증은 `/health`와
명시된 공개 shell/토큰 경로를 구분하고, protected data/admin API의 토큰 없는 요청은
401이어야 한다. DNS 분리만으로 host/LAN egress 차단을 증명하지 않는다. 이미지나 gateway를 바꾸면 `tests.validation.test_crawl4ai_egress`와 격리 리허설(`HYHOME_CRAWL4AI_REHEARSAL=1`)로 허용 목적지, private·metadata·redirect·subresource·호출자 proxy 거절, 직접 경로 없음을 다시 확인하고, consumer 인증은 따로 검증한다.

책임 소유자는 **@buenhyden**이다. 예외·통제 변경에는 기존 범위별 승인 기록이 필요하며 문서 수정은 승인 근거가 아니다. 통제 실패나 복구 증거 누락은 수용을 중단하고 정제된 증거로 에스컬레이션한다.

### Review Cadence

이미지 업그레이드나 consumer 연결 시, 그리고 service rationalization 검토 때마다
검토한다. consumer가 여전히 없으면 @buenhyden의 승인된 제거 변경으로 넘긴다. Secret 폐기는 소비자·유출·보존 상태를 확인한 별도 결정이다.

### Traceability

- [Guide](../guides/0091-crawl4ai.md) (`GDE-0091`)
- [Runbook](../runbooks/0091-crawl4ai.md) (`RUN-0091`)
- [AI architecture](../../02.architecture/descriptions/0008-ai-architecture.md)

## Related Documents

- [Crawl4AI Compose source](../../../infra/08-ai/crawl4ai/docker-compose.yml)
