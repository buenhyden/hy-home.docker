---
title: "Valkey 클러스터 LAB 지원"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-05"
created: "2026-10-03"
---

# Valkey 클러스터 LAB 지원

## Overview

이 디렉터리는 독립 LAB의 추적된 보조 소스(config, scripts)를 보유합니다. Compose와 실행 안내는 [LAB 문서](../../../labs/valkey-cluster.md)에 함께 있습니다.

## Audience

LAB 소스 관리자와 검토자를 대상으로 합니다.

## Scope

정상 HOME 서비스·상태와 공유하지 않는 보조 파일만 소유합니다.

## Structure

LAB Compose가 이 디렉터리의 스크립트·설정을 참조합니다. 실제 진입점은 `labs/valkey-cluster.yml`입니다.

## Tech Stack

Valkey 클러스터의 LAB 보조 소스이며 이미지 선언은 독립 [LAB Compose](../../../labs/valkey-cluster.yml)가 소유합니다.

## Configuration

이 디렉터리의 설정·스크립트는 LAB Compose에만 연결됩니다. 환경·secret·network·volume은 [LAB 문서](../../../labs/valkey-cluster.md)를 따릅니다.

## Validation

정적 렌더와 격리 실행 절차는 [LAB 문서](../../../labs/valkey-cluster.md)에 기록합니다.

## Usage

LAB의 독립 프로젝트·환경·secret·network·volume 계약과 정적 검증은 co-located LAB 문서를 따릅니다. HOME root Compose로 실행하지 않습니다.

## Related Documents

- [LAB 문서](../../../labs/valkey-cluster.md)
- [데이터 tier](../README.md)
