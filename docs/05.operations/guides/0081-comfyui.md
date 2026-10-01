---
title: "ComfyUI Guide"
version: "0.2.2"
type: "operation/guide"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "GDE-0081"
parent_ids:
- "POL-0081"
implementation_services:
  infra/08-ai/comfyui/docker-compose.yml:
  - comfyui
created: "2026-09-19"
---

# ComfyUI Guide

## Usage

ComfyUI는 `ai`와 `ai-image`가 선택하는 상시 실행 HOME 이미지 워크플로 UI이다.
root Compose가 [해당 구현](../../../infra/08-ai/comfyui/docker-compose.yml)을
포함하며 이 서비스는 Traefik을 거쳐 도달하고 선언된 loopback 호스트 포트도
바인딩한다. `gateway-standard-chain@file,sso-errors@file,sso-auth@file`이 공개
라우트를 보호한다.

이 서비스는 Compose에 선언된 현재 업스트림 이미지를 사용한다. mutable tag의 실제 digest/source는 배포 전 확인해야 하며,
라이선스, 라이프사이클, 업그레이드 노트는 업스트림 이미지와
[ComfyUI 저장소](https://github.com/Comfy-Org/ComfyUI)가 소유한다. 로컬
[Dockerfile](../../../infra/08-ai/comfyui/Dockerfile)은 현재 선택되지 않은 별도의
빌드 권한이다. [파생된 Compose 이미지 프로젝션](../../../infra/tech-stack.versions.json)은
drift 확인용 뷰일 뿐이다.

### 데이터와 설정 경계

아래는 Compose가 `/opt/comfyui` 아래에 의도한 mount 역할이며, 활성 이미지가 실제 사용하는 경로임을 증명하지 않는다.

| Mount | 의도한 내용 | 복구 취급 |
| --- | --- | --- |
| `models` | 다운로드된 모델 가중치 | 출처와 checksum/라이선스 증거를 기록한 후에만 교체 가능 |
| `custom_nodes` | 서드파티 실행 가능 노드 코드 | 리비전 인벤토리를 보존한다; 설치나 업데이트 전에 검토한다 |
| `user`, `input`, `output` | 워크플로, 사용자 설정, 제공 및 생성된 자산 | 파괴적 작업 전에 사용자 데이터로 백업한다 |
| Hugging Face와 Torch 캐시 | 다운로드된 아티팩트 | 재빌드 가능한 캐시, 모델 출처의 대체물이 아님 |

`COMFYUI_ARGS`는 healthcheck와 Traefik 백엔드가 일치시키는 listener와 포트를
유지해야 한다. `HF_HOME`, `TORCH_HOME`, NVIDIA compute/utility capability,
`gpus: all`과 linked Compose의 CPU/memory 설정은 선언된 소스 한도일 뿐 측정된 여유 자원이
아니다. Ollama와의 공유 GPU 피크 동시성은 검증되지 않았다.

### 일반적인 운영

승인된 워크플로를 사용하고 필요한 모델과 custom-node 리비전을 기록한 다음
UI에서 큐에 등록한다. `/system_stats` 응답이 성공해도 endpoint가 응답한다는
사실만 보여줄 뿐, 모델을 로드할 수 있는지나 워크플로가 안전한지는 증명하지
않는다. 승인 게이트된 런타임 점검과 복구에는
[runbook](../runbooks/0081-comfyui.md)을 사용한다.

### 소스 기반 라이프사이클 계약

- 선택된 `yanwk/comfyui-boot:cu126-slim` 이미지가 권위를 갖는다. 로컬
  Dockerfile은 현재 선택되지 않았다. 업그레이드 전에 이미지 digest,
  CUDA/드라이버 호환성, 모델 digest/라이선스, 워크플로 의존성, custom-node
  리비전을 기록한다.
- `models`, `custom_nodes`, `user`, `input`, `output`은 보존 요구 대상이다. 현재 bind 목록만으로 이 전체 집합이 실제 보존됨을 주장하지 않는다.
  캐시는 기록된 소스로부터만 재빌드 가능하다. 환경 값에는 listener/포트와 캐시
  경로가 포함된다. registry/다운로드 토큰이 도입되면 여전히 secret 소유자
  입력이다.
- Traefik의 standard/error/SSO 체인이 라우트를 보호한다. loopback 포트는 로컬
  운영용이다. 의존성은 NVIDIA 런타임/드라이버, 모델 스토리지, 게이트웨이/인증,
  root CA, `edge_net`이다.
- root에서 `docker compose --profile ai --profile ai-image config --quiet`를
  사용한다. 업그레이드 전에는 큐 유입과 활성 작업을 중지하고, 일관된 정지
  스냅샷을 만들고, 격리된 마운트에서 새 이미지/노드/모델을 테스트하고,
  `/system_stats`, GPU 가시성, 예상 노드, 대표 워크플로를 검증한다.
- ComfyUI는 GPL-3.0 라이선스이다. custom node와 모델은 별도의 라이선스를 갖는다.
  [공식 저장소](https://github.com/Comfy-Org/ComfyUI)와
  [Manager 가이드](https://docs.comfy.org/manager/overview)를 사용한다.

### Active-image persistence stop condition

Compose는 mutable `yanwk/comfyui-boot:cu126-slim`을 선택하며 로컬 build는 주석 처리되어 있다. Image 소유자의 현재 소스는 `/root/ComfyUI`에서 시작하고 `/root` volume을 선언하지만 Compose는 `/opt/comfyui`에 상태를 bind한다. 두 경로를 연결하는 command override는 없다. 실제 image bytes와 실행 경로·mount를 관찰하지 않았으므로 영속성 위험을 기록하되 데이터 유실이나 안전을 단정하지 않는다.

재생성·image upgrade·cache/volume 정리·완전한 backup 판정 전에 중단한다. @buenhyden의 승인 아래 실제 image와 모든 사용 경로(익명 `/root` volume 포함)를 확인하고 전체 상태를 보존한 뒤 별도 구현을 조정한다. Workflow/model/node/input/output/user 정책을 유지한다. 비활성 Dockerfile의 CUDA/Python/Torch/ComfyUI pin, non-root 사용자와 `/opt` 구조는 활성 image 증거가 아니다. 기존 복구 계획은 전제 충족 전까지 미실행 상태다.

## Common Checks

- [Compose 소스](../../../infra/08-ai/comfyui/docker-compose.yml)에서 profile,
  라우트, 마운트, 리소스, healthcheck를 점검한다.
- 업그레이드 전에 실제 custom-node와 모델 출처를 점검한다; 캐시 디렉터리를
  출처로 신뢰하지 않는다.
- 영속 콘텐츠를 변경하기 전에 중앙 [백업 정책](../policies/0021-backup-and-restore.md)을
  사용한다.

## Runbook Handoff

승인 게이트된 진단과 복구에는 [ComfyUI Runbook](../runbooks/0081-comfyui.md)을
사용한다.

## Traceability

- Governing architecture: [AD-0008](../../02.architecture/descriptions/0008-ai-architecture.md)
- [Policy](../policies/0081-comfyui.md) and [Runbook](../runbooks/0081-comfyui.md)
- [Official custom-node management guidance](https://docs.comfy.org/manager/overview)

## Related Documents

- [ComfyUI Compose](../../../infra/08-ai/comfyui/docker-compose.yml)
- [Policy](../policies/0081-comfyui.md), [Runbook](../runbooks/0081-comfyui.md)
