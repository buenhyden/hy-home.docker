---
title: "n8n 독립 워크로드"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-11"
---

# n8n 독립 워크로드

## Overview

기존 n8n의 독립 DEV 통지 소비자 소스와 합성 시험을 보관합니다.

## Scope

공개 소스·비활성 workflow·합성 fixture에 한정합니다. SQL과 게시 배치는
Airflow의 P04가 소유하며, 실제 import·예약·자격 증명 작업은 Task의 선행 조건을 따릅니다.

## Structure

- [매니페스트 outbox 통지](manifest-outbox-notifier/README.md): 결정적 생성기,
  제한된 SMTP node와 합성 시험입니다.
- [Hermes 수집 전송](hermes-blog-ingestion/README.md): 로컬 영속 대기함과
  계약 미확정 상태의 비활성 차단 흐름입니다.

## Usage

각 워크로드 README에서 소스 검증 명령과 운영 대기 조건을 확인합니다.
공통 이미지·Compose·네트워크·CI 등록은 총괄 통합 제안으로 전달합니다.

## Related Documents

- [기존 n8n](../README.md)
- [Spec Package 탐색](../../../../docs/03.specs/README.md): 정본 Task는 SPEC-0204-TSK-0013입니다.
