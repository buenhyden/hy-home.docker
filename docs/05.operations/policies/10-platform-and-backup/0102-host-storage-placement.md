---
title: "Host Storage Placement Policy"
version: "0.3.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "operations"
artifact_id: "POL-0102"
created: "2026-10-27"
next_review_at: "2027-05-13"
---

# Host Storage Placement Policy

## Purpose and Scope

### Objective

이 정책은 개인 PC 호스트에서 Docker·containerd 저장소와 서비스 데이터를 SSD와 HDD 중 어디에 둘지, 그리고 저장소를 SSD로 옮기는 조건을 정한다. SPEC-0246에서 측정·이전·수용한 배치를 현재 운영 기준으로 정한 문서다.

#### Authority

- 근거와 수용 기록: SPEC-0246(삭제됨, 번호는 Registry `reserved_history`, 본문은 Git history)의
  C1–C6은 모두 소유자가 수용했다.
  - C1(2026-10-19): containerd 이전 뒤 이미지 목록, health, k3d node가 이전 전 snapshot과 같았다.
  - C2: Ollama가 SSD 경로에서 같은 model 목록을 제공하고, 첫 load가 318.4초에서 55.9초로 줄었다.
  - C3: build-cache 하한을 정하고, 보관한 이미지는 digest로 검증했으며, inventory상 소유자 없는 volume·container만 지웠다.
  - C4: 실행 중인 registry image digest가 Compose pin과 같았다.
  - C5(2026-10-27): 소유자가 수용했고, 독립 rules review 뒤 이 정책이 active가 되었다. SMART 기반 이전 조건이 Spec의 측정되지 않은 정격 수명 문구를 대신한다.
  - C6(2026-10-27): 읽기 전용 확인 뒤 소유자가 수용했다. Prometheus·Tempo volume은 SSD `fast-volumes/obs/*`에 bind되고 둘 다 healthy이며 이전 HDD 사본은 없다. Loki·Alloy·Pyroscope는 HDD에 남는다.

### Applies To

- 호스트의 containerd `root`, Docker `data-root`, BuildKit build cache, 서비스 named volume과 bind 경로
- Ollama 모델 경로, 로컬 registry blob, 쓰기가 많은 관측 저장소(Prometheus, Loki, Tempo, Pyroscope, Alloy)
- 루트 파일시스템 여유 공간과 SSD 내구성 예산

#### Exclusions

- k3s·k3d와 다른 저장소의 데이터는 범위 밖이다.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0102-R1 | 항상 | 필수: 표의 계층별 배치(containerd·Docker root·named volume·Registry·Loki 등은 HDD, Ollama·Prometheus·Tempo·루트 FS는 SSD)를 유지한다 | `docker info` Root Dir/containerd `root` 확인 / `docker volume inspect` device 확인 | 확인 출력 |
| POL-0102-R2 | 서비스를 SSD로 옮길 때 | 필수: 측정된 지연 문제가 그 서비스를 지목하고 이전 후에도 SSD 여유가 기존 경보 임계값보다 클 때만 옮긴다 | `df -h /` / `HostSystemDiskLow` 경보 | Task 기록(측정값과 소유자 결정) |
| POL-0102-R3 | 쓰기가 많은 저장소 이전 | 필수: 24시간 쓰기율과 SMART 사용률로 예측한 SSD 잔여 수명이 5년 이상일 때만 옮기고 이미 SSD에 있는 저장소의 쓰기율을 더해 판단한다 | `scripts/operations/storage-write-rate.py` collect/compare | 쓰기율 측정 결과 |
| POL-0102-R4 | 데이터베이스 | 필수: 데이터베이스는 HDD에 둔다 | none | none |
| POL-0102-R5 | 저장소 이전 시 | 필수: 대상 저장소를 멈춘 뒤 복사·권한·mount·health·데이터 조회를 확인하고 검증된 복구 원본이 있을 때만 이전 위치를 지우며 삭제는 호스트 소유자가 실행한다 | 수동 | Task 기록 |
| POL-0102-R6 | `containerd`/`docker` 기동 | 필수: unit에 `RequiresMountsFor=/home/hyunyoun/storage`를 선언해 HDD 미mount 상태로 시작하지 않게 한다 | systemd unit 선언 | none |
| POL-0102-R7 | 이미지 보관 처리 | 필수: registry 저장 manifest digest가 push한 digest와 같을 때만 보관 처리한다 | none | none |
| POL-0102-R8 | 호스트 변경 | 필수: root 권한 호스트 변경은 소유자가, 소스 변경과 검증은 에이전트가 실행하고 누가 어떤 단계를 실행했는지 Task에 기록한다 | 수동 | Task 기록 |
| POL-0102-R9 | 항상 | 금지: 무차별 `docker system prune`, volume 일괄 삭제, 검증 없는 `rsync --delete`를 쓰지 않고 소유 미확인 항목은 지우지 않는다 | 수동 | none |

#### 배치

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

#### SSD로 옮기는 조건

- 서비스는 측정된 지연 문제가 그 서비스를 지목하고, 옮긴 뒤에도 SSD 여유 공간이 기존 경보 임계값보다 클 때만 SSD로 옮긴다.
- 쓰기가 많은 저장소는 24시간 쓰기율과 SMART 사용률(percent used) 추이로 예측한 SSD 잔여 수명이 5년 이상일 때만 옮긴다. 이 예측은 제조사 정격 TBW와 다른 값이다. 저장소별 적격성을 단순히 합산해 모두 옮기지 않고, 이미 SSD에 있는 저장소의 쓰기율을 더해 판단한다.
- 데이터베이스는 HDD에 둔다. 현재 데이터 크기가 작다.
- 이전은 대상 저장소를 멈춘 뒤 복사·권한·mount·health·데이터 조회를 확인하고, 검증된 복구 원본을 남긴 상태에서만 이전 위치를 지운다. 이전 위치 삭제는 호스트 소유자가 실행한다.

#### 실행 경계

- `containerd`와 `docker` unit은 `RequiresMountsFor=/home/hyunyoun/storage`를 선언해 HDD 경로가 mount되지 않은 상태로 시작하지 않는다.
- 이미지는 registry에 저장된 manifest digest가 push한 digest와 같을 때만 보관 처리한다.
- root 권한이 필요한 호스트 변경은 소유자가 실행하고, 소스 변경과 검증은 에이전트가 실행한다. 누가 어떤 단계를 실행했는지 Task에 기록한다.
- 무차별 `docker system prune`, volume 일괄 삭제, 검증 없는 `rsync --delete`는 쓰지 않는다. 소유가 확인되지 않은 항목은 지우지 않는다.

### Exceptions

#### Exception Conditions

없음. 새 저장소를 SSD로 옮기려면 위 조건의 측정값과 소유자 결정을 해당 Task에 기록한다.

#### Approval and Review

- SSD 쓰기율이나 SMART 마모가 바뀌었다고 판단될 때, 또는 새 쓰기 집중 저장소가 추가될 때 다시 측정한다.
- 저장소 이전, 디스크 교체, Docker·containerd root 변경 때 검토한다.

## Enforcement

### Mechanisms

- `docker info`의 Docker Root Dir와 containerd 설정의 `root`가 위 경로와 같은지 확인한다.
- `docker volume inspect hy-home-infra_prometheus-data hy-home-infra_tempo-data`의 device가 SSD 경로인지 확인한다.
- `df -h /`와 `HostSystemDiskLow` 경보 상태로 루트 여유 공간을 확인한다.
- 쓰기율 측정은 `scripts/operations/storage-write-rate.py`의 collect/compare를 쓴다.

#### Current reconciliation boundary

2026-11-03 P09는 이 정책과 위 Authority에 요약한 SPEC-0246 C1–C6 수용 기록을 읽기 전용으로 대조한다.
그 작업의 Docker root metadata와 짧은 사용량 표본은 현재 배치·실행 상태를 바꾸거나
용량, RPO/RTO, 피크 또는 에너지 예산을 수용하는 근거가 아니다. 관측 환경의 read-only
mount 표시는 호스트 mount 실패로 해석하지 않는다. Prometheus·Tempo SSD 및
Loki·Alloy·Pyroscope와 containerd/Docker/BuildKit HDD의 수용된 배치는 새로운 측정된
drift와 명시적 소유자 승인이 없는 한 유지한다.

### Limits

다음은 정책이 이름 있는 자동 검사를 보이지 않는 부분이다.

- 배치 확인(`docker info`, `docker volume inspect`, `df -h /`)과 쓰기율 측정은 사람이 실행하는 확인이며 지속 검사 게이트가 아니다.
- 데이터베이스 HDD 배치, 이미지 digest 보관 조건, 삭제 금지 규칙, 호스트 변경 분담은 이름 있는 검사 없이 소유자 검토와 Task 기록에 의존한다.
- SSD 이전 조건은 측정값과 소유자 결정을 Task에 기록해야 하며 SMART 기반 예측은 제조사 정격 TBW와 다른 값이다.
- 2026-11-03 읽기 전용 대조의 짧은 사용량 표본은 용량, RPO/RTO, 피크, 에너지 예산을 수용하는 근거가 아니다.
- 관측 환경의 read-only mount 표시는 호스트 mount 실패로 해석하지 않는다.

## Ownership

### Owner

책임 소유자는 frontmatter `owner`인 **@buenhyden**이다.

### Review Triggers

- 같은 번호 `0102`의 Guide/Runbook은 없다.
- [Prometheus Guide](../../guides/07-observability/0045-prometheus.md)
- [Backup and Restore Policy](0021-backup-and-restore.md)
