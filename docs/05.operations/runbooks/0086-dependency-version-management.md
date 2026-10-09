---
title: "Dependency Version Management Runbook"
version: "0.2.1"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "operations"
artifact_id: "RUN-0086"
parent_ids:
- "POL-0086"
created: "2026-09-19"
---

# Dependency Version Management Runbook

## Overview

이 런북은 소스 이미지, 빌드 의존성, updater 정책, 파생 버전 projection을 바꿀 때 따르는 검증과 적용 절차를 안내한다.

## Trigger and Preconditions

소스 이미지·빌드 의존성·updater 정책·파생 버전 projection 또는 단일 파일 config를
변경할 때 사용한다. 저장소 루트의 정확한 diff와 소유 service·profile을 기록한다.
공개 source 검증은 runtime 적용이나 Renovate 작업 실행 승인이 아니다. private
입력·Docker 작업이 필요한 단계는 대상 checkout/context와 별도 승인을 확인한다.

## Procedure

### Source and updater changes

1. Compose image와 선택된 build context/Dockerfile/args/target, 설치 package,
   복사된 requirements·설정, entrypoint/command를 확인한다. image label만으로
   실제 빌드 버전을 추정하지 않는다. [Policy](../policies/0086-dependency-version-management.md)의
   update owner를 확인하고 공식 문서·migration·호환성 근거를 선택한 버전에 맞춘다.
2. 공개 source만 읽는 projection 검사를 수행한다.

   ```bash
   bash scripts/operations/sync-tech-stack-versions.sh --dry-run
   bash scripts/operations/sync-tech-stack-versions.sh --check
   ```

   `--check`의 drift는 의도한 source 변경과 비교한다. parser/미분류 source 오류는
   중단 사유다. 옵션 없는 실행도 check이며 쓰지 않는다. 승인된 source 변경의
   projection을 갱신할 때만 다음을 실행하고 diff를 검토한다.

   ```bash
   bash scripts/operations/sync-tech-stack-versions.sh --write
   git diff -- infra/tech-stack.versions.json
   bash scripts/operations/sync-tech-stack-versions.sh --check
   ```

   기대 결과는 의도한 항목만 추가·변경·삭제되고 check가 성공하는 것이다.
3. 지원되는 Node 또는 승인된 도구 container에서 공식 strict validator를 실행한다.
   도구를 실행하려고 임의로 설치하거나 네트워크 updater를 시작하지 않는다.

   ```bash
   renovate-config-validator --strict --no-global renovate.json5
   renovate-config-validator --strict infra/09-platform-ops/renovate/config/config.js
   ```

   repository/global 모드를 구분한다. 의존성·런타임이 없으면 `BLOCKED`로 기록한다.
4. 관련 build source와 문서 계약, 기존 동기화 테스트의 누락·중복·제거·digest·
   local/custom·서로 다른 source version 사례를 검증한다. 현재 gate가 요구하는
   범위만 실행하며 Compose image projection PASS로 build pin을 대체하지 않는다.

### Static configuration validation

이 절은 network·profile·하네스 점검에도 적용된다. 실제 private `.env`와 secret을
읽지 않는 승인된 public/sanitized checkout에서 도구·선택 범위를 먼저 확인한다.
일반 validator는 `.env`가 없으면 공개 예제로 만들고, 누락된 secret 경로에 dummy
파일을 만든다. 종료 시 자신이 만든 파일을 지우지만 생성한 directory는 남을 수
있다. 기존 `.env`가 있으면 Compose가 이를 읽는다. 원문 private 모델을 출력하지
않으며 dummy 파일을 실제 서비스 입력으로 사용하지 않는다.

```bash
bash scripts/validation/validate-docker-compose.sh
```

기본 모드는 모든 선언 profile과 POL-0078의 HOME을 각각 검사한다.
`HYHOME_COMPOSE_PROFILES`를 지정하면 해당 합집합 하나만 검사한다. 기대 결과는
선택별 성공과 host-port 충돌 없음이다. 합산 서비스 수는 unique census가 아니다.
두 baseline script는 별도로 `core`가 기본이므로 각 결과의 선택 범위를 기록한다.
구문·선택 성공은 실제 credential·network 도달성·health·복구 증거가 아니다.

`--preflight`는 dummy 파일을 만들지 않지만 실제 `.env`를 source하고 로컬 파일·
mount와 network를 조회한다. 문서 전용 검증으로 실행하지 않는다. 입력이나 도구
승인이 부족하면 `NOT_RUN`/`BLOCKED`로 남기고 가능한 공개 source 검사를 계속한다.

### Runtime configuration apply

이 단계는 정확한 기존 service·Docker context·운영 checkout·변경 영향·백업과
rollback이 승인된 경우에만 수행한다. 새 service의 기동, image pull/build, 초기화
job 재실행은 별도 효과다. 해당 서비스 Runbook에서 종속성·중단·migration 조건을
먼저 확인하며, generic full-stack `up`/restart를 사용하지 않는다.

단일 파일 bind mount가 새 inode로 교체되면 `restart`만으로 반영되지 않는다.
승인된 service를 재생성하고 바로 hash를 확인한다. 다음 placeholder는 확인한
service/checkout으로 대체하며, 사전 확보한 image로 config만 반영하는 예다.

```bash
docker compose up -d --no-deps --no-build --pull never --force-recreate <service>
python3 scripts/operations/check-config-mount-hashes.py --root <checkout>
```

`--no-deps`는 종속성이 이미 준비된 대상에만 사용한다. mount를 directory로
바꾸거나 `docker cp`로 점검을 대체하지 않는다. script는 실행 중인 project
container에서 해당 checkout 아래 regular-file bind를 비교하고 `secrets/`는
제외한다. 출력은 경로와 상태이며 파일 내용은 출력하지 않는다.

| 관찰 | 판단과 다음 단계 |
| --- | --- |
| 기대한 config mount 전부 `MATCH` | byte 반영 증거다. 별도로 서비스 health·인증된 기능을 확인한다. |
| `DIFF`, exit1 | byte 불일치다. checkout·source·대상을 먼저 대조하고 승인된 재생성 후 다시 확인한다. 원인을 무조건 recreate 누락으로 단정하지 않는다. |
| `UNREADABLE` | host/container 읽기 실패다. `cat` 부재도 가능하다. coverage 미완료로 중단한다. |
| 행0 또는 기대 mount 누락 | 잘못된 checkout·멈춘 container·검사 대상 밖 mount 여부를 확인한다. 성공 증거가 아니다. |
| query 오류, exit2 | Docker context·권한·응답을 확인하고 추가 적용을 중단한다. |

script는 `DIFF`가 없으면 `UNREADABLE`이나 행0에도 exit0을 반환한다. 따라서
exit0만으로 완료하지 않으며 기대 coverage와 unreadable0/diff0을 모두 확인한다.
`--helper-image <local image with cat>`은 `--network none`, 대상 PID namespace와
`SYS_PTRACE`를 쓰는 일시적 `--rm` container를 실행한다. 별도 승인된 apply 범위에
있을 때만 사용하며 read-only 조회로 분류하지 않는다. helper 승인이나 읽기 경로가
없으면 검증 미완료를 보존한다. 이는 script 수정이나 runtime 검증 성공 선언이 아니다.

## Verification

명령·종료 코드·source commit·updater/validator 버전·선택과 coverage, 예상 결과와
실패/중단을 현재 Task에 기록한다. private 값·원문 환경·raw log를 남기지 않는다.
local 검사와 remote bot/hosted 실행, 실제 적용·복구를 구분하고 미실행은 명시한다.

## Rollback and Escalation

### Rollback or Recovery

source와 derived registry를 함께 이전 승인 상태로 되돌리고 검사한다. runtime
config rollback은 기존 승인된 구성의 재반영·hash·기능 확인까지 필요하다.
Git rollback은 database 파일이나 migration을 downgrade하지 않는다. 마지막
호환 image와 보호된 backup을 유지하며 data restore는 서비스 소유의 격리된
복구 절차와 별도 승인으로만 수행한다.

### Escalation

소유권 중복, 미분류 source/manager, registry만의 pin 변경, credential 오류,
지원되지 않는 migration, backup/coverage 부재 또는 예상 밖 결과는 중단하고
@buenhyden에게 전달한다. gate를 우회하거나 force push하지 않는다.

## Related Documents

- [운영 인덱스](../README.md)
- [파생 이미지 projection](../../../infra/tech-stack.versions.json)
- [Renovate 정책](../../../renovate.json5), [Dependabot 범위](../../../.github/dependabot.yml)

### Traceability

- [AD-0031](../../02.architecture/descriptions/0031-home-development-host.md)
- [Guide](../guides/0086-dependency-version-management.md), [Policy](../policies/0086-dependency-version-management.md)
- 적용 통제: [POL-0006](../policies/0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary)
