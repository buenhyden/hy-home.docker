---
title: "플랫폼과 백업 런북"
version: "0.1.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-29"
layer: "operations"
---

# 플랫폼과 백업 런북

## Overview

플랫폼과 백업의 상황별 전제, 명령, 기대 결과, 중단 조건, 검증과 복구를 확인한다.

## Scope

이 폴더는 아래 문서의 런북 역할만 소유한다. 구현과 운영 결과는 각 소유 문서와 Task에서 확인한다.

실행 권한, 비밀값 원문, 새로운 서비스와 빈 분류 문서는 포함하지 않는다.

## Structure

| 문서 | 식별자 | 한 줄 역할 |
| --- | --- | --- |
| [Release Management Runbook](0009-release-management.md) | `RUN-0009` | main 대상 릴리스 준비 PR과 승인된 SemVer 게시 절차를 소유한다. 일반 후보 QA는 PR의 changed-profile 한 번으로 검증하며 릴리스에서 다시 전체 QA를 실행하지 않는다. 배포·secret·HOME 복구 수용은 해당 운영 Ta |
| [Backup and Restore Runbook](0021-backup-and-restore.md) | `RUN-0021` | pgBackRest, Restic, SQLite export, R2 오프사이트 사본의 설정·실행·검증·복구 절차를 다룬다. 정책은 POL-0021, 설명은 GDE-0021이 소유한다. |
| [Platform Operations and Quality Optimization Hardening Runbook](0063-tooling-optimization-hardening.md) | `RUN-0063` | `09-platform-ops`와 `11-quality` 하드닝 회귀가 의심될 때 문서화된 기준을 복구하는 절차다. 공개 경계 SSO 체인, root가 소유한 network 경계, 독립 Locust LAB worker healthcheck, k6 vo |
| [Docker Registry Runbook](0065-registry.md) | `RUN-0065` | Registry(`registry` service)의 장애 진단, 일관된 백업·복원, 업그레이드, 별도로 승인된 garbage collection 절차다. |
| [Terrakube Recovery Runbook](0069-terrakube.md) | `RUN-0069` | Terrakube(`terrakube-api`, `terrakube-ui`, `terrakube-executor`)의 장애 진단, 조정된 백업·격리 복원, 업그레이드 절차다. |
| [Admin and Experiment Tools Hardening Runbook](0074-laboratory-optimization-hardening.md) | `RUN-0074` | 관리·실험 기능 하드닝 항목의 회귀를 복구하는 절차다. direct 노출 복원, allowlist/SSO/gateway 체인 누락, 네트워크 경계 드리프트, CI 게이트 실패를 점검하고 복구한다. 관리 UI 보안 경계와 운영 안정성 기준을 빠르게 되돌 |
| [OpenTofu Runbook](0082-opentofu.md) | `RUN-0082` | OpenTofu(`opentofu` job)의 plan 검토, lock 실패, state 백업·복구, 업그레이드 절차다. |
| [Renovate Runbook](0083-renovate.md) | `RUN-0083` | Renovate job의 정적 점검, 승인된 live run, 잘못된 변경의 복구, systemd timer 운영 절차다. |
| [Dependency Version Management Runbook](0086-dependency-version-management.md) | `RUN-0086` | 이 런북은 소스 이미지, 빌드 의존성, updater 정책, 파생 버전 projection을 바꿀 때 따르는 검증과 적용 절차를 안내한다. |
| [hy-home.k8s Integration Runbook](0096-k8s-integration.md) | `RUN-0096` | hy-home.k8s 클러스터와 이 스택을 연결하는 전체 절차와 자격 증명 회전, 문제 해결을 다루는 런북이다. 계약은 가이드가 설명한다. |

## Usage

1. 식별자와 문서 제목으로 대상을 고른다.
2. 상황별 전제, 명령, 기대 결과, 중단 조건, 검증과 복구를 확인한다.
3. 변경 시 원래 식별자와 생성일을 보존하고 이 목록과 현재 링크를 함께 갱신한다.
4. 문서 경로·메타데이터·링크·운영 카탈로그 검사와 소유 Task의 실제 검증 결과를 확인한다.

작성·검토 책임은 `@buenhyden`에게 있다. 같은 통제나 절차의 정본을 복제하지 않는다.

## Related Documents

- [상위 런북 분류](../README.md)
- [운영 문서](../../README.md)
- [문서 작성 계약](../../../../.agents/governance/documentation-protocol.md)
