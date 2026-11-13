---
title: "ComfyUI Policy"
version: "0.4.2"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "operations"
artifact_id: "POL-0081"
parent_ids:
- "AD-0008"
created: "2026-09-19"
---

# ComfyUI Policy

## Purpose

### Objective

ComfyUI는 항상 켜져 있는 HOME 이미지 워크플로 인터페이스다.

### Authority

- 상위 아키텍처: [AD-0008](../../../02.architecture/descriptions/0008-ai-architecture.md)

- 런타임 고정 버전은 [ComfyUI Compose](../../../../infra/08-ai/comfyui/docker-compose.yml)가 소유한다. 로컬 Dockerfile 대신 선언된 이미지가 선택되며, [파생 Compose 이미지 projection](../../../../infra/tech-stack.versions.json)이 drift를 검증한다.

## Scope

### Applies To

`comfyui`를 `ai`와 `ai-image` 아래에서 항상 켜져 있는 HOME 기능으로 유지한다.
Compose가 서비스 선택, gateway 레이블, GPU 요청, 리소스, 마운트를 소유한다.

### Exclusions

없음: 이 정책 본문에는 명시된 제외 대상이 없다.

## Rules

### Requirements

- gateway 인증을 유지한다. 기본 Compose는 host port를 게시하지 않으며,
  loopback 게시는 승인된 유지보수 overlay(`docker-compose.egress.yml`)로만
  붙인다. 노출이나 gateway를
  바꾸려면 범위, 만료, 롤백을 담은 승인된 예외가 있어야 한다.
- 커스텀 노드를 서드파티 실행 코드로 취급한다. 설치나 업데이트 전에 출처,
  리비전, 의존성, 라이선스를 검토한다. 알려진 정상 노드 집합을 재현할 수
  있을 만큼 인벤토리를 유지한다.
- `user`, `input`, `output`을 사용자 데이터로 보존한다. 모델 소스/체크섬과
  커스텀 노드 리비전 인벤토리를 보존한다. Hugging Face와 Torch 캐시는 재구축할
  수 있지만 승인된 복구 계획 없이 진단 중에 삭제하지 않는다.
- 마이그레이션 전에 영속 사용자 데이터를 백업하고 먼저 격리된 저장소로만
  복구한다. 정적 Compose 점검만으로 백업, GPU 용량, 재시작 복구, 또는 복구가
  성립하지는 않는다.
- 업그레이드 전에 upstream 릴리스 노트와 이미지 호환성을 검토한다. 헬스와
  승인된 대표 워크플로가 성공할 때까지 이전 이미지와 데이터 인벤토리를
  보유한다. 현재 이미지 태그는 소스 선언일 뿐, 테스트를 거친 업그레이드
  주장이 아니다.

#### Lifecycle and data controls

- ComfyUI는 소유자가 확인한 `HOME`으로 남는다. 라우팅 인증, 기본 Compose의 host port 미게시,
  GPU 접근, 소스 리소스 제한은 명시적으로 남아야 한다. 제한은 측정된
  여유분이 아니다.
- 워크플로/사용자 설정, 복구에 필요한 입력/출력, 커스텀 노드 리비전
  인벤토리, 정확한 모델 출처를 하나의 릴리스 세트로 백업한다. 모든 아티팩트를
  재현할 수 있을 때만 캐시를 폐기해도 되는 것으로 취급한다.
- 백업, 복구, 이미지 업그레이드, 커스텀 노드 변경, 또는 모델 마이그레이션
  전에 queue 유입을 일시 중지하고 활성 job을 기다리거나 취소한다. 실행
  가능한 노드를 라이브 복구 세트에 직접 설치하지 않는다.
- 공개 경로가 없는 격리된 마운트/프로젝트에서 복구/리허설하고, 교체 전에
  헬스, GPU, 필요한 노드, 모델 체크섬/라이선스, 대표 워크플로를 검증한다.
- 제거하려면 마운트를 삭제하기 전에 사용자 데이터 처리, 아티팩트 출처 내보내기,
  경로 종료, 자격 증명 폐기, 명시적 승인이 있어야 한다.

#### Active-image persistence stop condition

Compose는 mutable `yanwk/comfyui-boot:cu126-slim`을 선택하며 로컬 build는 주석 처리되어 있다. 이 image는 `/root/ComfyUI`에서 실행되며, 2026-11-08에 `models`, `custom_nodes`, `input`, `output`, `user` 다섯 volume을 `/root/ComfyUI/<dir>`로 다시 mount하고 데이터를 옮겼다(디렉터리별 파일 수 일치). 이전의 `/opt/comfyui` 불일치는 해소되었다.

Image tag가 mutable이므로 image upgrade 전에는 새 image가 여전히 `/root/ComfyUI`에서 시작하고 다섯 mount가 그 아래에 대응하는지 확인한 뒤 진행한다. 대응이 어긋나면 @buenhyden의 승인 아래 중단하고 전체 상태를 보존한다. image의 익명 `/root` volume에는 ComfyUI 코드, `/root/.cache`, 이동 전 데이터 사본이 남아 있고 이 사본이 rollback 원본이므로, @buenhyden의 승인 없이 이 volume을 recreate·prune하거나 cache와 함께 정리하지 않는다. 비활성 Dockerfile의 CUDA/Python/Torch/ComfyUI pin, non-root 사용자와 `/opt` 구조는 활성 image 증거가 아니다. 복구 계획은 격리 rehearsal 전까지 미실행 상태다.

### Enforcement

배포 전에 소스와 메타데이터 점검을 사용한다. 런타임 시작, 모델 다운로드,
워크플로 실행, GPU 활용, 복구에는 별도로 승인된 대상과 마스킹된 증거가
필요하다. 누락된 백업/출처, 예상치 못한 포트 노출, 또는 검토되지 않은
커스텀 노드는 에스컬레이션한다.

통제 실패나 복구 증거 누락은 수용을 중단하고 정제된 증거로 에스컬레이션한다.

## Exceptions

### Exception Conditions

예외에는 소유자, 범위, 위험, 만료, 복구 조건이 있어야 한다.

### Approval and Review

매월, 그리고 이미지, 커스텀 노드, 영속 데이터, 노출, 또는 GPU 정책 변경 전에
검토한다.

예외·통제 변경에는 기존 범위별 승인 기록이 필요하며 문서 수정은 승인 근거가 아니다.

## Ownership

### Responsibilities

책임 소유자는 **@buenhyden**이다.

### Change and Adoption

- 대상 동위 문서: [가이드](../../guides/09-ai-and-search/0081-comfyui.md), [런북](../../runbooks/09-ai-and-search/0081-comfyui.md)

- [가이드](../../guides/09-ai-and-search/0081-comfyui.md), [런북](../../runbooks/09-ai-and-search/0081-comfyui.md)
- [중앙 백업 정책](../10-platform-and-backup/0021-backup-and-restore.md)
- 이 문서는 SPEC-0267 secondary-listener hardening 결과를 담고 있다. 해당 패키지는 retire되었고 본문은 version history에 있다.
