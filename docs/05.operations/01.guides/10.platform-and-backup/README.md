---
title: "플랫폼과 백업 가이드"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
layer: "operations"
---

# 플랫폼과 백업 가이드

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

독자는 아래 역할 본문에서 이 문서가 제공하는 정보와 판단을 확인합니다.

### 책임과 적용 범위

적용 대상과 유지 책임은 frontmatter와 역할 본문의 범위 선언이 소유합니다.

## 내용 계약

### 입력과 전제

실제 입력과 전제는 아래 역할 본문의 해당 항목을 따릅니다.

### 본문과 규칙

#### Responsibility

##### Purpose

###### Purpose and Readers
<!-- core-payload-level:4 -->

플랫폼과 백업의 정상 구성과 사용 전제를 이해하고 필요한 통제와 실행 절차로 연결한다.

###### Inputs and Outputs
<!-- core-payload-level:4 -->

이 폴더는 아래 문서의 가이드 역할만 소유한다. 구현과 운영 결과는 각 소유 문서와 Task에서 확인한다.

##### Excluded Responsibilities

실행 권한, 비밀값 원문, 새로운 서비스와 빈 분류 문서는 포함하지 않는다.

#### Current Contents

##### Paths

| Path | Purpose |
| --- | --- |
| `0002-developer-environment.md` | 이 가이드는 로컬 개발 환경의 도구, 환경 파일, 인증서 설정과 검증 범위를 설명한다. |
| `0003-env-key-comparison.md` | 이 가이드는 공개 `.env.example`과 로컬 `.env`의 키 집합을 비교하는 기준과 방법을 설명한다. |
| `0008-new-service-onboarding.md` | 이 가이드는 새 컨테이너 서비스를 `hy-home.docker`에 추가할 때 참조한다. |
| `0021-backup-and-restore.md` | HOME의 백업은 도구마다 소유 범위가 다르다. 이 문서는 pgBackRest, Restic, R2 오프사이트 사본, SQLite export, host orchestrator가 각각 무엇을 보호하고 무엇을 보호하지 않는지 설명한다. |
| `0063-tooling-optimization-hardening.md` | 이 가이드는 `09-platform-ops`와 `11-quality`의 최적화·하드닝 변경을 재현 가능하게 적용하는 기준이다. 공개 경계 보안, 네트워크 경계 표준화, 테스트 도구 안정성 계약, 검증 절차를 다룬다. |
| `0065-registry.md` | Registry는 `infra/09-platform-ops/registry/`의 `registry` service로 운영하는 HOME OCI 이미지 저장소다. `registry` 또는 `tooling` profile에서 선택된다. |
| `0069-terrakube.md` | Terrakube는 `infra/09-platform-ops/terrakube/`의 `terrakube-api`, `terrakube-ui`, `terrakube-executor`로 구성한 온디맨드 DEV IaC 자동화·제어 플레인이다. 세 servi |
| `0074-laboratory-optimization-hardening.md` | 이 가이드는 Data·Observability·AI·Analytics tier에 흩어진 관리·실험 기능(dozzle, redisinsight, open-notebook, mlflow, jupyterlab)의 최적화·하드닝 변경을 재현 가능하게 적용하는 |
| `0082-opentofu.md` | OpenTofu는 `infra/09-platform-ops/opentofu/`의 `opentofu` service로 요청 시 실행하는 DEV IaC CLI 작업이다. `iac` profile에서만 선택된다. |
| `0083-renovate.md` | Renovate는 `infra/09-platform-ops/renovate/`의 `renovate` service로 실행하는 의존성 갱신 작업이다. `dependency-update` profile에서만 선택된다. |
| `0086-dependency-version-management.md` | 이 가이드는 Compose 이미지, Dockerfile, 파생 버전 projection의 버전 선언을 어떻게 찾고 확인하는지 설명한다. 버전 변경은 선언 소유자를 먼저 찾은 뒤에 시작한다. |
| `0096-k8s-integration.md` | hy-home.k8s 저장소는 같은 호스트에서 k3d 클러스터(`hyhome`)를 실행한다. |

###### Current Items
<!-- core-payload-level:4 -->

| 문서 | 식별자 | 한 줄 역할 |
| --- | --- | --- |
| [Developer Environment Operations](0002-developer-environment.md) | `GDE-0002` | 이 가이드는 로컬 개발 환경의 도구, 환경 파일, 인증서 설정과 검증 범위를 설명한다. |
| [`.env.example` vs `.env` Key Comparison](0003-env-key-comparison.md) | `GDE-0003` | 이 가이드는 공개 `.env.example`과 로컬 `.env`의 키 집합을 비교하는 기준과 방법을 설명한다. |
| [New Service Onboarding Guide](0008-new-service-onboarding.md) | `GDE-0008` | 이 가이드는 새 컨테이너 서비스를 `hy-home.docker`에 추가할 때 참조한다. |
| [Backup and Restore Guide](0021-backup-and-restore.md) | `GDE-0021` | HOME의 백업은 도구마다 소유 범위가 다르다. 이 문서는 pgBackRest, Restic, R2 오프사이트 사본, SQLite export, host orchestrator가 각각 무엇을 보호하고 무엇을 보호하지 않는지 설명한다. |
| [Platform Operations and Quality Optimization Hardening Usage Guide](0063-tooling-optimization-hardening.md) | `GDE-0063` | 이 가이드는 `09-platform-ops`와 `11-quality`의 최적화·하드닝 변경을 재현 가능하게 적용하는 기준이다. 공개 경계 보안, 네트워크 경계 표준화, 테스트 도구 안정성 계약, 검증 절차를 다룬다. `system-guide \| ho |
| [Docker Registry Usage Guide](0065-registry.md) | `GDE-0065` | Registry는 `infra/09-platform-ops/registry/`의 `registry` service로 운영하는 HOME OCI 이미지 저장소다. `registry` 또는 `tooling` profile에서 선택된다. |
| [Terrakube Usage Guide](0069-terrakube.md) | `GDE-0069` | Terrakube는 `infra/09-platform-ops/terrakube/`의 `terrakube-api`, `terrakube-ui`, `terrakube-executor`로 구성한 온디맨드 DEV IaC 자동화·제어 플레인이다. 세 servi |
| [Admin and Experiment Tools Hardening Usage Guide](0074-laboratory-optimization-hardening.md) | `GDE-0074` | 이 가이드는 Data·Observability·AI·Analytics tier에 흩어진 관리·실험 기능(dozzle, redisinsight, open-notebook, mlflow, jupyterlab)의 최적화·하드닝 변경을 재현 가능하게 적용하는 |
| [OpenTofu Guide](0082-opentofu.md) | `GDE-0082` | OpenTofu는 `infra/09-platform-ops/opentofu/`의 `opentofu` service로 요청 시 실행하는 DEV IaC CLI 작업이다. `iac` profile에서만 선택된다. |
| [Renovate Guide](0083-renovate.md) | `GDE-0083` | Renovate는 `infra/09-platform-ops/renovate/`의 `renovate` service로 실행하는 의존성 갱신 작업이다. `dependency-update` profile에서만 선택된다. |
| [Dependency Version Management Guide](0086-dependency-version-management.md) | `GDE-0086` | 이 가이드는 Compose 이미지, Dockerfile, 파생 버전 projection의 버전 선언을 어떻게 찾고 확인하는지 설명한다. 버전 변경은 선언 소유자를 먼저 찾은 뒤에 시작한다. |
| [hy-home.k8s Integration Usage Guide](0096-k8s-integration.md) | `GDE-0096` | hy-home.k8s 저장소는 같은 호스트에서 k3d 클러스터(`hyhome`)를 실행한다. |

###### Classification
<!-- core-payload-level:4 -->

이 폴더의 문서는 모두 가이드 역할이며 `GDE-NNNN` 식별자를 쓴다. 같은 subject의 다른 역할 문서는 있는 경우 같은 번호와 slug로 다른 역할 폴더에 있다.

##### Owners

작성·검토 책임은 `@buenhyden`에게 있다. 같은 통제나 절차의 정본을 복제하지 않는다.

#### Usage

##### Entry Points

###### Upstream and Downstream
<!-- core-payload-level:4 -->

- [상위 가이드 분류](../README.md)
- [운영 문서](../../README.md)

###### Policy and Templates
<!-- core-payload-level:4 -->

- [문서 작성 계약](../../../00.workspace/03.process/documentation-protocol.md)
- [README 템플릿](../../../99.templates/02.templates/93.common/readme-stage.template.md): 이 README의 양식 원본이며 형식은 Stage 99 Registry의 profile이 소유합니다

##### Checks

###### Create and Review
<!-- core-payload-level:4 -->

1. 식별자와 문서 제목으로 대상을 고른다.
2. 정상 구성과 사용 전제를 이해하고 필요한 통제와 실행 절차로 연결한다.
3. 변경 시 원래 식별자와 생성일을 보존하고 이 목록과 현재 링크를 함께 갱신한다.
4. 문서 경로·메타데이터·링크·운영 카탈로그 검사와 소유 Task의 실제 검증 결과를 확인한다.

###### Transition and Exit
<!-- core-payload-level:4 -->

문서는 `operational-policy` 수명주기(draft, in-review, active, deprecated, superseded, retired)를 따른다. superseded 또는 retired에 이른 문서는 [은퇴 전제 조건](../../../00.workspace/03.process/documentation-protocol.md#retirement-preconditions)을 모두 충족할 때에만 남아야 할 내용을 소유 문서에 요약한 뒤 삭제하고, 번호를 Registry `reserved_history`에 추가하며, 이 목록의 행과 링크를 같은 변경에서 제거한다.

## 적용과 확인

### 적용 방법

아래 역할 본문의 절차나 탐색 순서에 따라 사용합니다.

### 확인 기준

해당 문서에 선언된 확인 기준과 한계만 적용하며 실행·검증·인수를 구분합니다.

## 관계와 출처

### 관련 문서

현재 소유자와 의존 문서의 연결은 아래 역할 본문의 링크가 소유합니다.

### 외부 근거

외부 출처와 적용 한계는 아래 역할 본문에 선언된 범위이며 권한을 부여하지 않습니다.
