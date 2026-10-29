---
title: "플랫폼과 백업 정책"
version: "0.1.2"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-29"
layer: "operations"
---

# 플랫폼과 백업 정책

## Overview

플랫폼과 백업의 적용 범위의 필수 통제, 승인, 예외와 검토 기준을 확인한다.

## Scope

이 폴더는 아래 문서의 정책 역할만 소유한다. 구현과 운영 결과는 각 소유 문서와 Task에서 확인한다.

실행 권한, 비밀값 원문, 새로운 서비스와 빈 분류 문서는 포함하지 않는다.

## Structure

| 문서 | 식별자 | 한 줄 역할 |
| --- | --- | --- |
| [04-Data Backup Policy](0021-backup-and-restore.md) | `POL-0021` | 이 policy는 현재 source configuration을 data protection, security, resource, lifecycle, 독립적으로 검증 가능한 operator control에 묶는다. 이 policy는 보존되는 모든 HOM |
| [IaC Deployment Policy](0060-iac-deployment.md) | `POL-0060` | 이 정책은 `09-platform-ops`의 OpenTofu CLI helper와 Terrakube API/UI/executor를 이용한 IaC 변경의 승인, state, secret, evidence 기준을 정의한다. |
| [Platform Operations and Quality Optimization Hardening Operations Policy](0063-tooling-optimization-hardening.md) | `POL-0063` | 이 문서는 `09-platform-ops`·`11-quality`의 최적화/하드닝 운영 정책을 정의한다. 관리 경로 보안, 네트워크 경계, 테스트 도구 안정성, 카탈로그 확장 승인 게이트를 통제한다. |
| [Docker Registry Operations Policy](0065-registry.md) | `POL-0065` | Registry는 `HOME` 아티팩트 저장소다. 현재 추적 중인 엔드포인트는 네이티브 TLS/인증을 갖추지 않았으므로 명시적으로 격리된 신뢰 네트워크에서만 서비스할 수 있다. |
| [Terrakube Operations Policy](0069-terrakube.md) | `POL-0069` | Terrakube는 명시적인 `iac` 컨트롤 플레인이다. Apache-2.0 프로젝트 라이선스가 이 단일 호스트 배포의 지원, SLA, 엔터프라이즈 기능, HA를 보장하지는 않는다. |
| [Admin and Experiment Tools Hardening Operations Policy](0074-laboratory-optimization-hardening.md) | `POL-0074` | 이 문서는 여러 tier의 관리·실험 기능 최적화/하드닝 운영 정책을 정의한다. 관리 UI 보안 경계, 실험성 서비스 운영 통제, 카탈로그 확장 승인 게이트를 명문화한다. |
| [OpenTofu Policy](0082-opentofu.md) | `POL-0082` | OpenTofu는 명시적인 `iac` job이다. 정적 선택과 검증은 provider 계정을 읽거나 원격 인프라를 변경할 권한을 결코 뜻하지 않는다. |
| [Renovate Policy](0083-renovate.md) | `POL-0083` | Renovate는 원격 저장소 쓰기 권한을 가지며 명시적으로 선택하는 `dependency-update` job이다. HOME이나 일반 도구 기동에는 절대 포함되지 않는다. |
| [Dependency Version Management Policy](0086-dependency-version-management.md) | `POL-0086` | 인프라 버전 변경은 하나의 HOME/DEV 호스트에서 검토 가능하고 재현 가능해야 한다. 버전 업데이트가 배포나 데이터 마이그레이션을 승인하지는 않는다. |
| [hy-home.k8s Integration Operations Policy](0096-k8s-integration.md) | `POL-0096` | hy-home.k8s 클러스터는 host 주소상의 고정된 엔드포인트 집합과 두 개의 OpenBao 인증 경로를 사용한다. 이 정책은 그 집합과 인증 방식, 두 저장소 사이를 오가는 자격 증명의 처리 방식을 고정한다. |
| [Host Storage Placement Policy](0102-host-storage-placement.md) | `POL-0102` | 이 정책은 개인 PC 호스트에서 Docker·containerd 저장소와 서비스 데이터를 SSD와 HDD 중 어디에 둘지, 그리고 저장소를 SSD로 옮기는 조건을 정한다. |

## Usage

1. 식별자와 문서 제목으로 대상을 고른다.
2. 적용 범위의 필수 통제, 승인, 예외와 검토 기준을 확인한다.
3. 변경 시 원래 식별자와 생성일을 보존하고 이 목록과 현재 링크를 함께 갱신한다.
4. 문서 경로·메타데이터·링크·운영 카탈로그 검사와 소유 Task의 실제 검증 결과를 확인한다.

작성·검토 책임은 `@buenhyden`에게 있다. 같은 통제나 절차의 정본을 복제하지 않는다.

## Related Documents

- [상위 정책 분류](../README.md)
- [운영 문서](../../README.md)
- [문서 작성 계약](../../../../.agents/governance/documentation-protocol.md)
