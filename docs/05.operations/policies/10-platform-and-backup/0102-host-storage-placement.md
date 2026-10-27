---
title: "Host Storage Placement Policy"
version: "0.1.0"
type: "operation/policy"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-27"
layer: "operations"
artifact_id: "POL-0102"
created: "2026-10-27"
---

# Host Storage Placement Policy

## Overview

이 정책은 개인 PC 호스트에서 Docker·containerd 저장소와 서비스 데이터를 SSD와 HDD 중 어디에 둘지, 그리고 저장소를 SSD로 옮기는 조건을 정한다. [SPEC-0246](../../../03.specs/0246-host-storage-tiering/spec.md)에서 측정·이전·수용한 배치를 운영 기준으로 정리한 초안이며, 활성화 전까지는 현재 기준이 아니다.

## Scope

- 호스트의 containerd `root`, Docker `data-root`, BuildKit build cache, 서비스 named volume과 bind 경로
- Ollama 모델 경로, 로컬 registry blob, 쓰기가 많은 관측 저장소(Prometheus, Loki, Tempo, Pyroscope, Alloy)
- 루트 파일시스템 여유 공간과 SSD 내구성 예산
- k3s·k3d와 다른 저장소의 데이터는 범위 밖이다.

## Rules

### 배치

| 저장소 | 계층 | 위치 | 증가 통제 |
| --- | --- | --- | --- |
| 이미지 layer와 snapshot | HDD | containerd `root` = `/home/hyunyoun/storage/containerd` | 쓰지 않는 이미지는 registry에 보관한 뒤 로컬에서 지운다 |
| Build cache | HDD(containerd root 안) | BuildKit | `builder.gc`의 `defaultKeepStorage` 10 GB는 상한이 아니라 10 GiB 예약 하한으로 동작한다 |
| 컨테이너 metadata와 json-file 로그 | HDD | Docker `data-root` = `/home/hyunyoun/storage/docker-root/docker` | 공통 logging 기본값 `max-size` 10m × `max-file` 3 |
| 서비스 named volume | HDD | `${DEFAULT_MOUNT_VOLUME_PATH}` 하위 경로 | 각 서비스 소유 |
| Ollama 모델 | SSD | `${OLLAMA_MODEL_DIR}`(로컬 `.env`) | AI 계층이 모델 집합을 소유 |
| Registry blob | HDD | `${DEFAULT_REGISTRY_DIR}` | push한 이미지마다 보관 ledger 행 |
| Prometheus, Tempo | SSD | `${PROMETHEUS_DATA_DIR}`, `${TEMPO_DATA_DIR}`(로컬 `.env`) | 각 저장소 보존 설정 |
| Loki, Pyroscope, Alloy | HDD | `${DEFAULT_OBSERVABILITY_DIR}` 하위 경로 | 각 저장소 보존 설정 |
| 루트 파일시스템 여유 공간 | SSD | `/` | 기존 `HostSystemDiskLow` 경보(여유 25 GiB) |

변수가 비어 있으면 Compose fallback이 HDD 경로를 쓴다. 따라서 SSD 배치는 로컬 `.env`의 저장소별 변수로만 켜지며, 공개 기본값은 바뀌지 않는다.

### SSD로 옮기는 조건

- 서비스는 측정된 지연 문제가 그 서비스를 지목하고, 옮긴 뒤에도 SSD 여유 공간이 기존 경보 임계값보다 클 때만 SSD로 옮긴다.
- 쓰기가 많은 저장소는 24시간 쓰기율과 SMART 사용률(percent used) 추이로 예측한 SSD 잔여 수명이 5년 이상일 때만 옮긴다. 이 예측은 제조사 정격 TBW와 다른 값이다. 저장소별 적격성을 단순히 합산해 모두 옮기지 않고, 이미 SSD에 있는 저장소의 쓰기율을 더해 판단한다.
- 데이터베이스는 HDD에 둔다. 현재 데이터 크기가 작다.
- 이전은 대상 저장소를 멈춘 뒤 복사·권한·mount·health·데이터 조회를 확인하고, 검증된 복구 원본을 남긴 상태에서만 이전 위치를 지운다. 이전 위치 삭제는 호스트 소유자가 실행한다.

### 실행 경계

- `containerd`와 `docker` unit은 `RequiresMountsFor=/home/hyunyoun/storage`를 선언해 HDD 경로가 mount되지 않은 상태로 시작하지 않는다.
- 이미지는 registry에 저장된 manifest digest가 push한 digest와 같을 때만 보관 처리한다.
- root 권한이 필요한 호스트 변경은 소유자가 실행하고, 소스 변경과 검증은 에이전트가 실행한다. 누가 어떤 단계를 실행했는지 Task에 기록한다.
- 무차별 `docker system prune`, volume 일괄 삭제, 검증 없는 `rsync --delete`는 쓰지 않는다. 소유가 확인되지 않은 항목은 지우지 않는다.

## Exceptions

없음. 새 저장소를 SSD로 옮기려면 위 조건의 측정값과 소유자 결정을 해당 Task에 기록한다.

### Review Cadence

- SSD 쓰기율이나 SMART 마모가 바뀌었다고 판단될 때, 또는 새 쓰기 집중 저장소가 추가될 때 다시 측정한다.
- 저장소 이전, 디스크 교체, Docker·containerd root 변경 때 검토한다.

### Traceability

- 같은 번호 `0102`의 Guide/Runbook은 없다.
- 근거와 수용 기록: [SPEC-0246 Task](../../../03.specs/0246-host-storage-tiering/tasks/tsk-0001-host-storage-tiering.md)

## Verification

- `docker info`의 Docker Root Dir와 containerd 설정의 `root`가 위 경로와 같은지 확인한다.
- `docker volume inspect hy-home-infra_prometheus-data hy-home-infra_tempo-data`의 device가 SSD 경로인지 확인한다.
- `df -h /`와 `HostSystemDiskLow` 경보 상태로 루트 여유 공간을 확인한다.
- 쓰기율 측정은 `scripts/operations/storage-write-rate.py`의 collect/compare를 쓴다.

## Related Documents

- [SPEC-0246 Host Storage Tiering](../../../03.specs/0246-host-storage-tiering/spec.md)
- [Prometheus Guide](../../guides/07-observability/0045-prometheus.md)
- [Backup and Restore Policy](0021-backup-and-restore.md)
