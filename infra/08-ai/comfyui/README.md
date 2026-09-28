---
title: "ComfyUI Implementation"
version: "0.2.0"
type: "common/package-readme"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-27"
---

# ComfyUI

## Overview

이미지 워크플로우 서비스로 상시 실행이 요구됩니다. Ollama와 공유하는 GPU 워크로드의 동시성은 함께 측정해야 하며 런타임 이미지 예외는 별도 소유자가 관리합니다.

Lifecycle: **HOME**. 루트 Compose가 이 정의를 include하며, 명시적 프로필이 활성화를 제어합니다.

## Audience

구현, 설정, 검증을 검토하는 운영자와 개발자.

## Scope

로컬 서비스 정의와 구현 탐색. 운영 통제와 복구는 [documentation index](../../../docs/README.md)를 거쳐 `docs/05.operations/guides/0081-comfyui.md`, `docs/05.operations/policies/0081-comfyui.md`, `docs/05.operations/runbooks/0081-comfyui.md`(ID: `GDE-0081`, `POL-0081`, `RUN-0081`)가 담당합니다.

## Structure

- [Dockerfile](Dockerfile)
- [docker-compose.yml](docker-compose.yml)

## Tech Stack

런타임 고정 값은 [Compose](docker-compose.yml)와 그 참조 빌드 소스에 속합니다. [버전 레지스트리](../../../infra/tech-stack.versions.json)는 정제된 프로젝션이며 배포 매니페스트가 아닙니다.

## Configuration

| Service | Profiles | Networks | `edge_net` | Secret references |
| --- | --- | --- | --- | --- |
| `comfyui` | `ai, ai-image` | `ai_net` | `127.0.0.1:${COMFYUI_HOST_PORT:-8188}:${COMFYUI_PORT:-8188}` | Compose Secret 부여 없음; 설정된 부트스트랩 파일 메타데이터를 확인합니다 |

Persistence:

- `comfyui-models`: `${DEFAULT_AI_MODEL_DIR}/comfyui/models`
- `comfyui-custom-nodes`: `${DEFAULT_AI_MODEL_DIR}/comfyui/custom_nodes`
- `comfyui-output`: `${DEFAULT_AI_MODEL_DIR}/comfyui/output`
- `comfyui-input`: `${DEFAULT_AI_MODEL_DIR}/comfyui/input`
- `comfyui-user`: `${DEFAULT_AI_MODEL_DIR}/comfyui/user`
- `comfyui-hf-cache`: `${DEFAULT_AI_MODEL_DIR}/comfyui/cache/huggingface`
- `comfyui-torch-cache`: `${DEFAULT_AI_MODEL_DIR}/comfyui/cache/torch`

환경 변수 키 이름과 기본값은 Compose와 [공개 환경 변수 예시](../../../.env.example)에 선언되어 있습니다. Compose의 마운트 권한과 헬스체크 명령은 구현을 설명할 뿐이며 설정 검사를 통과해도 런타임 준비 상태는 증명되지 않습니다. 비공개 환경 변수 값, 자격 증명 파일, 원본 렌더링된 설정은 출력하지 않습니다.

## Validation

저장소 루트에서 문서화된 프로필을 선택하고 `scripts/validation/validate-docker-compose.sh`를 사용합니다. 대상별 런타임 확인과 승인 후 복구는 소유 운영 Runbook을 사용합니다. 마운트 누락, 예상치 못한 노출, 초기화 실패 시에는 중지합니다.

## How to Work in This Area

Compose, 빌드 소스, 공개 환경 변수 키, 시크릿 참조를 일관되게 유지합니다. 게이트웨이 인증, 영속화, 리소스 예산, 버전 예외를 변경하기 전에 검토합니다. 여기에 명령을 중복 기록하지 말고 기존 운영 주제(operations subject)를 업데이트합니다.

### Convergence contract

- Classification: **HOME**. Exact profiles: `ai`, `ai-image`.
- Source authority: 이 패키지의 Compose와 선택된 이미지/빌드 입력. `infra/tech-stack.versions.json`은 파생 프로젝션입니다.
- Root preflight: `docker compose --profile ai config --quiet`. Root targeted start: `docker compose --profile ai up -d comfyui`.
- Stable entry point: [docs/README.md](../../../docs/README.md). Exact Stage 05 path `docs/05.operations/guides/0081-comfyui.md`; ID: `GDE-0081`, `POL-0081`, `RUN-0081`.
- 해당 런북의 격리 복구는 계획되어 있으나 아직 실행되지 않았습니다. 모델/콘텐츠 출처를 보존하고, 실행 중인 파일시스템 복사본을 복구 근거로 사용하지 않습니다.

## Related Documents

- [Infrastructure index](../../../infra/README.md)
- [Documentation index](../../../docs/README.md)
- [Public secret contract](../../../secrets/README.md)
