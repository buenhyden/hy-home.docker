---
title: "ComfyUI Policy"
version: "0.2.1"
type: "operation/policy"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "POL-0081"
parent_ids:
- "AD-0008"
created: "2026-09-19"
---

# ComfyUI Policy

## Overview

ComfyUI는 항상 켜져 있는 HOME 이미지 워크플로 인터페이스다.

## Policy Scope

`comfyui`를 `ai`와 `ai-image` 하의 항상 켜져 있는 HOME 기능으로 유지한다.
Compose가 서비스 선택, gateway 레이블, GPU 요청, 리소스, 마운트를 소유한다.

## Controls

- gateway 인증과 loopback 전용 직접 게시를 유지한다. 노출이나 gateway 변경은
  범위, 만료, 롤백이 포함된 승인된 예외가 필요하다.
- 커스텀 노드를 서드파티 실행 코드로 취급한다. 설치나 업데이트 전에 출처,
  리비전, 의존성, 라이선스를 검토한다. 알려진 정상 노드 집합을 재현하기에
  충분한 인벤토리를 유지한다.
- `user`, `input`, `output`을 사용자 데이터로 보존한다. 모델 소스/체크섬과
  커스텀 노드 리비전 인벤토리를 보존한다. Hugging Face와 Torch 캐시는 재구축
  가능하지만, 승인된 복구 계획 없이 진단 중에는 삭제하지 않는다.
- 마이그레이션 전에 영속 사용자 데이터를 백업하고 먼저 격리된 저장소로만
  복구한다. 정적 Compose 점검은 백업, GPU 용량, 재시작 복구, 또는 복구를
  성립시키지 않는다.
- 업그레이드 전에 upstream 릴리스 노트와 이미지 호환성을 검토한다. 헬스와
  승인된 대표 워크플로가 성공할 때까지 이전 이미지와 데이터 인벤토리를
  보유한다. 현재 이미지 태그는 소스 선언이지, 테스트된 업그레이드 주장이
  아니다.

### Lifecycle and data controls

- ComfyUI는 소유자가 확인한 `HOME`으로 남는다. 라우팅 인증, loopback 바인딩,
  GPU 접근, 소스 리소스 제한은 명시적으로 남아야 한다. 제한은 측정된
  여유분이 아니다.
- 워크플로/사용자 설정, 복구에 필요한 입력/출력, 커스텀 노드 리비전
  인벤토리, 정확한 모델 출처를 하나의 릴리스 세트로 백업한다. 모든 아티팩트가
  재현 가능한 경우에만 캐시를 폐기 가능으로 취급한다.
- 백업, 복구, 이미지 업그레이드, 커스텀 노드 변경, 또는 모델 마이그레이션
  전에 queue 유입을 일시 중지하고 활성 job을 기다리거나 취소한다. 실행
  가능한 노드를 라이브 복구 세트에 직접 설치하지 않는다.
- 공개 경로가 없는 격리된 마운트/프로젝트에서 복구/리허설하고, 교체 전에
  헬스, GPU, 필요한 노드, 모델 체크섬/라이선스, 대표 워크플로를 검증한다.
- 제거는 마운트를 삭제하기 전에 사용자 데이터 처리, 아티팩트 출처 내보내기,
  경로 종료, 자격 증명 폐기, 명시적 승인을 필요로 한다.

## Exceptions

예외는 소유자, 범위, 위험, 만료, 복구 조건을 필요로 한다.

## Verification

배포 전에 소스와 메타데이터 점검을 사용한다. 런타임 시작, 모델 다운로드,
워크플로 실행, GPU 활용, 복구는 별도로 승인된 대상과 마스킹된 증거가
필요하다. 누락된 백업/출처, 예상치 못한 포트 노출, 또는 검토되지 않은
커스텀 노드는 에스컬레이션한다.

## Review Cadence

매월, 그리고 이미지, 커스텀 노드, 영속 데이터, 노출, 또는 GPU 정책 변경 전에
검토한다.

## Traceability

- 상위 아키텍처: [AD-0008](../../02.architecture/descriptions/0008-ai-architecture.md)
- 대상 동위 문서: [가이드](../guides/0081-comfyui.md), [런북](../runbooks/0081-comfyui.md)

## Related Documents

- [가이드](../guides/0081-comfyui.md), [런북](../runbooks/0081-comfyui.md)
- 런타임 고정 버전은 [ComfyUI Compose](../../../infra/08-ai/comfyui/docker-compose.yml)가 소유한다. 로컬 Dockerfile 대신 선언된 이미지가 선택되며, [파생 Compose 이미지 projection](../../../infra/tech-stack.versions.json)이 drift를 검증한다.
- [중앙 백업 정책](0021-backup-and-restore.md)
