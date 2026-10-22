---
title: "Root resource optimization preparation"
version: "1.1.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-22"
created: "2026-10-11"
---

# Root resource optimization preparation

## Overview

P07 W10의 공개 측정 계약과 bounded 평가 자료입니다. 진행·검증 증거는
현재 Task `SPEC-0218-TSK-0002`에 기록합니다.
서비스 목록과 소비자 판단은 기존 inventory를 재사용하며 여기서 별도 목록을 만들지 않습니다.

## Scope

### Audience

서비스 소유자, 총괄 통합자와 코드·보안 검토자가 준비 자료를 사용합니다.

[measurement.schema.json](measurement.schema.json)은 source·배포 식별자, 관측 시간·주기,
대표 업무 부하, 20개 측정값과 11개 예산, 기존 controls v2의 선택된 root projection을
받습니다. provenance는 수집자 식별자·읽기 전용 수집 방법·공개 receipt SHA256·집계 방식을
명시합니다. 이는 제출자의 선언이며 receipt를 읽거나 진위를 인증하지 않습니다.
미상 provenance와 합성 수집 방법은 차단합니다.
값은 `known`, `unknown`, `not_applicable`을 명시하고 측정 단위를 고정합니다.
메모리·CPU·PID의 필수 사실은 `not_applicable`로 생략할 수 없습니다.
source·배포 SHA와 digest의 일치 여부는 입력끼리 비교하며 실제 배포를 확인하지 않습니다.

[평가기](../../../scripts/lib/ops/root_resource_assessment.py)는 기존 Compose controls의
순수 평가 API를 호출합니다. Docker·네트워크·실제 환경 파일·로그·secret을 읽거나
자원·권한을 변경하지 않습니다. registry projection은 평가 입력이며 canonical 예외의
추가·승인·폐기를 대신하지 않습니다.

`security_opt` projection은 정확한 `no-new-privileges:true` 또는
`no-new-privileges:false` 토큰 하나만 지원합니다. 임의·상충 토큰은 입력 거부입니다.

입력은 명시적으로 지정한 공개 JSON 한 파일입니다. 최대 256 KiB, 깊이 32,
노드 8192, 숫자 절댓값 10^15의 경계를 적용합니다. 중복 key, 비유한 숫자,
외부 schema reference, symlink·hardlink·비정규 파일, private 이름·디렉터리,
읽는 중 교체·변경된 파일은 고정 오류 코드로 거부합니다. 경로나 입력값을 오류에 출력하지 않습니다.

## Structure

### Tech Stack

Python 평가기와 JSON Schema Draft 2020-12를 사용합니다. 기존 controls v2가 정책 소유자입니다.

### Documents

| Path | Purpose |
| --- | --- |
| [measurement.schema.json](measurement.schema.json) | 공개 측정 입력 계약 |
| [fixtures/README.md](fixtures/README.md) | 합성 입력과 예상 거부 결과 |

## Usage

저장소 루트에서 [CLI](../../../scripts/operations/root-resource-assessment.py)를 실행합니다.

```bash
python scripts/operations/root-resource-assessment.py infra/09-platform-ops/resource-optimization/fixtures/idle-unknown.synthetic.json
```

종료 코드 `0`은 입력이 `REVIEWABLE`, `1`은 `BLOCKED`, `2`는 입력 거부입니다.
합성 fixture는 항상 `BLOCKED`이며 위 예시의 종료 코드 `1`은 예상 결과입니다.
`REVIEWABLE`도 운영 승인이나 실제 사용·부하·복구 수용을 뜻하지 않습니다.
모든 결과는 `SOURCE/UNIT/STATIC`, `runtime_acceptance=false`,
`mutation_authorized=false`를 유지합니다.

### SSD 쓰기율 측정

`SPEC-0246-TSK-0001` W7은 [쓰기율 CLI](../../../scripts/operations/storage-write-rate.py)로
관측 저장소(Prometheus·Loki·Tempo·Pyroscope·Alloy)의 24시간 쓰기량을 비교합니다.
`collect`는 Docker 메타데이터·`/proc/diskstats`·cgroup `io.stat`만 읽고 기존 snapshot을
덮어쓰지 않습니다. `compare`는 owner가 읽은 SMART 사용률과 누적 host 쓰기 바이트
(`Total_LBAs_Written` × 512)로 SSD 수명을 추정합니다.

```bash
python scripts/operations/storage-write-rate.py collect /home/hyunyoun/storage/ops-snapshots/w7-write-rate-20261019 t1
python scripts/operations/storage-write-rate.py compare /home/hyunyoun/storage/ops-snapshots/w7-write-rate-20261019 \
  --smart-used-percent 24 --smart-host-bytes 41863677045248
```

24시간 미만 창, 컨테이너 재시작, 카운터 감소, 같은 장치명의 major:minor 변경,
snapshot 누락, SMART 미입력이나 사용률 0은
`DEFER`입니다. cgroup 쓰기량은 t0와 같이 모든 `io.stat` 줄의 합이며 dm-0이 SSD 줄을
반복하므로 상한값입니다. `ELIGIBLE`은 5년 내구성 예산만 통과했다는 뜻이며, 이동에는
측정된 지연 문제와 owner 결정이 따로 필요합니다. 종료 코드 `0`은 모든 저장소 표본이
유효, `1`은 하나 이상 무효, `2`는 입력 오류입니다.

SMART 사용률은 유한한 0–100 숫자이고 누적 host 쓰기는 양의 정수여야 합니다.
Boolean, 비유한 값, 음수·중복 장치·잘못된 카운터와 유한 범위를 벗어난 계산은
입력 오류로 거부하며 결과 JSON에는 `NaN`이나 무한대를 기록하지 않습니다.
기존 세 파일 형식과 과거 표본은 유지합니다. 이 형식에는 boot ID, mount·파일시스템
결속, 수집기·입력 해시가 없으므로 major:minor와 StartedAt 일치만으로 재부팅이나
동일 장치 번호의 재할당, 현재 배치·출처를 완전히 입증하지 않습니다. 해당 정보는
미검증으로 남기며 새 현장 표본이나 담당자 인수를 이 소스 검사로 대신하지 않습니다.

### Configuration

CLI는 지정한 JSON 외에 이 디렉터리의 schema를 읽습니다. 실행 환경·Compose·secret 설정을 변경하지 않습니다.

### Validation

[합성 fixture](fixtures/README.md)는 unknown·idle 축소·식별 불일치·예산 모순의
거부 동작을 검증합니다. 실제 관측은 대상 서비스·정확한 배포 이미지·플랫폼,
읽기 전용 권한·시간 배정·출력 정제를 먼저 기록해야 합니다.
부하·limit·UID/capability/rootfs/secret 권한 변경과 재기동은 서비스별 이미지·기능·접속,
대표 업무 부하·백업/복구 계약 및 운영 시간 배정 이후 별도로 진행합니다.
Wiki·학습 앱·LAB runtime은 이 준비 자료의 범위 밖입니다.

## Related Documents

- [상위 platform operations](../README.md)
- [controls v2 예외 registry](../../common-optimizations.exceptions.json)
- [프로젝트 문서 진입점](../../../docs/README.md)에서 현재 Task와 기존 서비스 inventory의 소유 문서를 찾습니다.
