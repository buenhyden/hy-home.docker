---
title: "플랫폼과 백업 가이드"
version: "0.1.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-14"
layer: "operations"
---

# 플랫폼과 백업 가이드

## Overview

플랫폼과 백업의 정상 구성과 사용 전제를 이해하고 필요한 통제와 실행 절차로 연결한다.

## Scope

이 폴더는 아래 문서의 가이드 역할만 소유한다. 구현과 운영 결과는 각 소유 문서와 Task에서 확인한다.

실행 권한, 비밀값 원문, 새로운 서비스와 빈 분류 문서는 포함하지 않는다.

## Structure

| 문서 | 식별자 | 한 줄 역할 |
| --- | --- | --- |
| [Developer Environment Operations](0002-developer-environment.md) | `GDE-0002` | 이 가이드는 로컬 개발 환경의 도구, 환경 파일, 인증서 설정과 검증 범위를 설명한다. |
| [`.env.example` vs `.env` Key Comparison](0003-env-key-comparison.md) | `GDE-0003` | 이 가이드는 공개 `.env.example`과 로컬 `.env`의 키 집합을 비교하는 기준과 방법을 설명한다. |
| [New Service Onboarding Guide](0008-new-service-onboarding.md) | `GDE-0008` | 이 가이드는 새 컨테이너 서비스를 `hy-home.docker`에 추가할 때 참조한다. |
| [Backup and Restore Guide](0021-backup-and-restore.md) | `GDE-0021` | HOME의 백업은 도구마다 소유 범위가 다르다. 이 문서는 pgBackRest, Restic, R2 오프사이트 사본, SQLite export, host orchestrator가 각각 무엇을 보호하고 무엇을 보호하지 않는지 설명한다. |
| [Platform Operations and Quality Optimization Hardening Usage Guide](0063-tooling-optimization-hardening.md) | `GDE-0063` | 이 가이드는 `09-platform-ops`와 `11-quality`의 최적화·하드닝 변경을 재현 가능하게 적용하는 기준이다. 공개 경계 보안, 네트워크 경계 표준화, 테스트 도구 안정성 계약, 검증 절차를 다룬다. `system-guide \| ho |
| [Docker Registry Usage Guide](0065-registry.md) | `GDE-0065` | Registry는 `infra/09-platform-ops/registry/`의 `registry` service로 운영하는 HOME OCI 이미지 저장소다. `registry` 또는 `tooling` profile에서 선택된다. |
| [Operations: Terraform Policy Usage Guide](0068-terraform.md) | `GDE-0068` | 이 가이드는 기존 Terraform 사용자의 OpenTofu 이관 맥락을 보존한다. 현재 저장소의 실행 도구는 OpenTofu이며 Terraform Compose 서비스는 없다. |
| [Terrakube Usage Guide](0069-terrakube.md) | `GDE-0069` | Terrakube는 `infra/09-platform-ops/terrakube/`의 `terrakube-api`, `terrakube-ui`, `terrakube-executor`로 구성한 온디맨드 DEV IaC 자동화·제어 플레인이다. 세 servi |
| [Administration and Experimentation Hardening Usage Guide](0074-laboratory-optimization-hardening.md) | `GDE-0074` | 이 가이드는 Data·Observability·AI·Analytics tier에 흩어진 관리·실험 기능(dozzle, redisinsight, open-notebook, mlflow, jupyterlab)의 최적화·하드닝 변경을 재현 가능하게 적용하는 |
| [OpenTofu Guide](0082-opentofu.md) | `GDE-0082` | OpenTofu는 `infra/09-platform-ops/opentofu/`의 `opentofu` service로 요청 시 실행하는 DEV IaC CLI 작업이다. `iac` profile에서만 선택된다. |
| [Renovate Guide](0083-renovate.md) | `GDE-0083` | Renovate는 `infra/09-platform-ops/renovate/`의 `renovate` service로 실행하는 의존성 갱신 작업이다. `dependency-update` profile에서만 선택된다. |
| [Dependency Version Management Guide](0086-dependency-version-management.md) | `GDE-0086` | 이 가이드는 Compose 이미지, Dockerfile, 파생 버전 projection의 버전 선언을 어떻게 찾고 확인하는지 설명한다. 버전 변경은 선언 소유자를 먼저 찾은 뒤에 시작한다. |
| [hy-home.k8s Integration Usage Guide](0096-k8s-integration.md) | `GDE-0096` | hy-home.k8s 저장소는 같은 호스트에서 k3d 클러스터(`hyhome`)를 실행한다. |

## Usage

1. 식별자와 문서 제목으로 대상을 고른다.
2. 정상 구성과 사용 전제를 이해하고 필요한 통제와 실행 절차로 연결한다.
3. 변경 시 원래 식별자와 생성일을 보존하고 이 목록과 현재 링크를 함께 갱신한다.
4. 문서 경로·메타데이터·링크·운영 카탈로그 검사와 소유 Task의 실제 검증 결과를 확인한다.

작성·검토 책임은 `@buenhyden`에게 있다. 같은 통제나 절차의 정본을 복제하지 않는다.

## Related Documents

- [상위 가이드 분류](../README.md)
- [운영 문서](../../README.md)
- [문서 작성 계약](../../../../.agents/governance/documentation-protocol.md)
