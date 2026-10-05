---
title: "Compose Network Membership Runbook"
version: "1.1.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "RUN-0077"
parent_ids:
- "GDE-0077"
created: "2026-05-10"
---

# Compose Network Membership Runbook

## Overview

## Trigger and Preconditions

### Overview

### Trigger and Preconditions

### When to Use

신규 서비스의 peer 연결, 기존 membership·고정 주소 변경 또는 DNS/IP 충돌을
검토할 때 사용한다. 저장소 루트에서 정확한 Compose service·fragment·network·peer,
선택 profile과 변경 이유를 기록한다. 공개 source 검토와 runtime 조회·변경은
별도다. 승인된 Docker context와 기존 대상이 없으면 runtime 단계는 `NOT_RUN`이다.

## Procedure

### Procedure

### 1. Confirm declaration and target

[Guide](../guides/0077-ip-address-management.md)의 flow와
[Policy](../policies/0077-ip-address-management.md)의 static-address 제한을 대조한다.
필요한 peer가 없는 network는 추가하지 않는다. 아래 검색은 선언 위치만 보여준다.

```bash
rg -n "ipv4_address:" infra docker-compose.yml
```

동일 network 안에서만 주소 중복을 비교하고 subnet·gateway·dynamic pool과
trusted-proxy/announce 주소 소비자를 함께 확인한다. target·peer·alias가 불명확하면
수정하지 않고 @buenhyden에게 전달한다.

### 2. Change and validate the scoped source

승인된 fragment의 dictionary membership만 수정하고 root include와 profile을
확인한다. 다른 service의 주소나 외부 network를 함께 바꾸지 않는다.
[RUN-0086](0086-dependency-version-management.md#static-configuration-validation)의
public/sanitized checkout 조건과 임시 파일 부작용을 먼저 확인한다.

```bash
bash scripts/validation/validate-docker-compose.sh
HYHOME_COMPOSE_PROFILES="workflow" bash scripts/validation/validate-docker-compose.sh
python3 -m unittest tests.validation.test_compose_baseline_gates.NetworkSegmentationContractTests
```

두 번째 명령의 `workflow`는 실제 변경한 named selection으로 바꾼다. 기본 검사는
모든 선언 profile과 HOME, override는 지정한 합집합 하나를 검사한다. 성공 종료와
실제 검사 범위를 기록한다. 실패하면 적용을 중단한다. 이 결과는 static-IP 전체
충돌 검사나 live reachability가 아니며 수정만으로 기존 컨테이너 network가 바뀌지 않는다.

### 3. Observe an approved running target

현재 context가 승인된 대상인지 확인한 뒤 실제 이름으로 대체한다. 아래 placeholder는
운영자가 확인한 값이며 전체 inspect나 Config.Env를 출력하지 않는다.

```bash
docker context show
docker inspect --format '{{.Name}} {{range $name, $net := .NetworkSettings.Networks}}{{$name}}={{$net.IPAddress}} {{end}}' <container_name>
docker network inspect --format '{{.Name}} {{range .Containers}}{{.Name}}={{.IPv4Address}} {{end}}' <network>
```

기대 결과는 해당 peer의 선언된 network와 올바른 subnet 주소다. 기존 컨테이너가
없거나 DNS/주소가 다르면 원인을 기록하고 service Runbook으로 넘긴다. 이 절차는
network connect/disconnect, 전체 restart나 network/volume 삭제를 실행하지 않는다.
실제 반영은 영향받는 소비자와 중단·복구 계획을 승인받아 서비스 절차 및
[RUN-0086](0086-dependency-version-management.md#runtime-configuration-apply)에 따라
수행하며, 이후 membership과 기능을 다시 확인한다.

## Verification

### Evidence

시각·context·service/profile·source commit·변경 hunk·network별 주소 대조와 검사
종료 상태를 기록한다. runtime 미실행은 명시한다. 원문 환경, 전체 inspect, secret,
개인 path나 payload를 기록하지 않는다.

## Rollback and Escalation

### Rollback or Recovery

source 오류는 해당 Compose/network hunk만 이전 승인 상태로 복원하고 다시 검증한다.
Git rollback은 실행 중인 membership을 복원하지 않는다. runtime이 별도 승인으로
변경되었다면 그 서비스의 승인된 이전 구성 반영·검증 절차로 넘긴다. 삭제나 광범위한
network 재생성이 필요하면 incident와 별도 복구 승인을 요구한다.

### Escalation

검증 실패, 잘못된 context, 알 수 없는 peer·주소 충돌, secret 노출 위험 또는 파괴적
복구가 필요하면 멈추고 @buenhyden에게 대상·값 없는 증거·시도 단계·복구 상태를 전달한다.

### Traceability

- 상위 Guide: [GDE-0077](../guides/0077-ip-address-management.md)
- 구조: [AD-0026](../../02.architecture/descriptions/0026-standardize-infra-net.md)
- 통제: [POL-0077](../policies/0077-ip-address-management.md)

## Related Documents

- [Operations index](../README.md)
- [시스템 진단](0099-system-operations.md)
