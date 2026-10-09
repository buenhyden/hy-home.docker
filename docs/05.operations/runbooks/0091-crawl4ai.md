---
title: "Crawl4AI Recovery Runbook"
version: "1.1.1"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "operations"
artifact_id: "RUN-0091"
parent_ids:
- "GDE-0091"
created: "2026-09-21"
---

# Crawl4AI Recovery Runbook

## Overview

이 런북은 OPTIONAL `crawl4ai`(`crawl4ai`, `crawl4ai-egress`, profile `crawl4ai`)의 시작 실패, 토큰 노출, 메모리 압박 대응과 consumer 연결·해제, 제거 절차를 다룬다.

## Trigger and Preconditions

시작 실패, 토큰 노출, 메모리 압박, 컨슈머 연결/해제 시 사용한다.

### Service lifecycle prerequisites

`crawl4ai`는 자체 profile만으로 선택하며 token 준비 실패 시 wrapper가 종료한다. 재생성하면 tmpfs cache가 사라지므로 필요한 산출물은 먼저 승인된 위치에 보존한다. 작업을 drain한 뒤 중지하며 token 파일 교체는 기존 컨테이너 restart만으로 새 bind가 반영된다고 가정하지 않는다.

## Procedure

### Execution Boundary

저장소 root에서 아래의 정확한 service/profile과 기존 container를 선택한다. 변경 전에 승인 대상, source/image, 선행 readiness, 필요한 운영 권한과 부작용 범위를 확인한다. `up`은 dependency/provisioning job을 만들 수 있고 profile은 격리가 아니다. 진단은 기존 container의 `exec`를 사용하고 단순 조회를 위해 client/provisioner를 띄우지 않는다. 재시작은 요청 중단·memory/queue 손실·부작용 반복을 일으킬 수 있으므로 대상 drain/backup 조건을 먼저 충족한다. `restart`는 바뀐 Compose 설정이나 교체된 secret bind를 불러오지 않는다.

Log를 보존하기 전에 payload·credential·header/cookie·private path를 제거하고 명령·시각·상태·제한된 시험 증거만 남긴다. 예상 밖 출력, backup 누락, dependency 실패나 승인되지 않은 부작용이면 중단하고 @buenhyden에게 넘긴다. Config rollback은 data/schema 복구가 아니다. 전체 기동·중지는 [cold-start Runbook](0098-cold-start-and-reboot.md)의 대상 선택·의존성 확인 절차를 사용한다. 공통 절차는 [백업](0021-backup-and-restore.md), [image 변경](0086-dependency-version-management.md), [시크릿](0085-openbao.md), [계정](0014-keycloak.md), [gateway·인증서](0013-traefik.md)가 소유한다. 대상이 실제 사용하는 자격 증명·상태에만 적용하며 secret 값은 증거로 요구하지 않는다.

### 진단과 복구 단계

1. 점검한다.

   ```bash
   docker compose --profile crawl4ai config --quiet
   docker compose --profile crawl4ai ps -a crawl4ai crawl4ai-egress
   docker compose --profile crawl4ai logs --tail=100 crawl4ai crawl4ai-egress
   ```

2. `64` 종료는 토큰 시크릿이 없거나 16자 미만임을 의미한다. 크롤러가 시작되지 않고 기다리면 `crawl4ai-egress`의 healthcheck를 먼저 본다. 크롤링이 모두 실패하면 gateway log의 `egress refused` 줄에서 거절 사유(port, address, resolve)를 확인하고, 거절된 목적지를 허용하려고 gateway나 internal 네트워크를 완화하지 않는다.
3. 토큰 노출 시: 서비스를 정지하고, `secrets/tools/crawl4ai/crawl4ai_api_token.txt`를
   승인된 secret 소유자 절차로 교체하고 컨슈머의 토큰을 함께 갱신한다. 단일 파일 secret inode가 바뀌면 소비자 컨테이너 재생성이 필요하다. 새 token의 허용과 기존 token의 거부를 값 비노출로 확인한다.
4. 반복적인 메모리 부족 재시작 시, `mem_limit`을 올리기 전에 호출자 측에서
   crawl 동시성을 낮춘다.
5. 이미지나 gateway를 바꾼 뒤에는 시작 전에 격리 리허설을 실행한다. 모든 네트워크가 internal이고 대상은 로컬 fixture뿐이며, 끝나면 컨테이너와 네트워크를 지운다.

   ```bash
   docker compose --profile crawl4ai pull crawl4ai
   HYHOME_CRAWL4AI_REHEARSAL=1 python3 -m unittest -v tests.validation.test_crawl4ai_egress.Crawl4AIEgressRehearsalTests
   ```

6. 제거 승인을 받으면 호출자와 작업을 중지하고 필요한 산출물을 소비자 소유자에게 넘긴다. 승인 범위에서 include/package와 secret metadata를 정리하되 private secret 폐기는 별도 disposition/revocation 결정에 따른다. Tmpfs cache/output은 재시작으로 사라지며 durable service volume은 없다.

## Verification

격리 network의 기존 승인 client에서 health와 protected API의 무자격 거부·승인 credential 성공을 구분해 확인한다. Token을 CLI 인자에 넣거나 crawl 내용을 캡처하지 않는다. UI/static 예외는 API 우회 증거가 아니다. 누락·짧은 secret으로 종료했다면 guard를 완화하지 않는다. 승인된 시작은 root Compose의 해당 service만 대상으로 하고 health·consumer 인증·허용 URL 시험 뒤 트래픽을 허용한다. 예상 밖 LAN/private 접근이나 자원 압박이면 중단한다. Tmpfs output/cache는 재시작으로 사라질 수 있으므로 미완료 요청을 consumer와 조정한다. 자체 영속 복원은 없고 provider credential은 [시크릿 소유자](0085-openbao.md)를 따른다.

종료 코드, 이미지, 소스 커밋을 기록한다. 토큰이나 크롤링된 내용은 기록하지 않는다.

## Rollback and Escalation

### Rollback or Recovery

자체 영속 서비스 데이터는 없지만 필요한 output과 미완료 요청은 소비자와 조정한다. Compose·image·secret bind를 되돌릴 때는 restart로 적용되지 않는다. 이전 승인 image와 선언을 복원하고 [RUN-0086](0086-dependency-version-management.md)·[RUN-0085](0085-openbao.md)의 대상·token·중단 영향 검토를 거친 재생성 계획으로 넘긴다. 재생성 뒤 health, protected API 인증 거부·성공, 소비자 연결을 검증하고 실패하면 트래픽을 차단한 채 에스컬레이션한다.

### Escalation

전용 `crawl4ai_net` 밖 연결, 공개 노출, 예상치 못한 protected API 인증 성공,
SSRF 의심 또는 복구 실패이면 중단하고 @buenhyden에게 정제된 증거로 넘긴다.

## Related Documents

### Traceability

- [Guide](../guides/0091-crawl4ai.md) (`GDE-0091`)
- [Policy](../policies/0091-crawl4ai.md) (`POL-0091`)
- [Crawl4AI Compose](../../../infra/08-ai/crawl4ai/docker-compose.yml)

- [Crawl4AI self-hosting](https://docs.crawl4ai.com/core/self-hosting/)
