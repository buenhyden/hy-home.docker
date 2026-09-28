---
title: "ComfyUI Runbook"
version: "0.2.1"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "RUN-0081"
parent_ids:
- "GDE-0081"
created: "2026-09-19"
---

# ComfyUI Runbook

## When to Use

승인된 ComfyUI 배포, UI 접근 불가, healthcheck 실패, 또는 계획된 데이터/이미지/custom-node
복구에 사용한다. 런타임 변경 전에 commit, 선택한 서비스, mount 위치, 이미지 식별자와 backup
증거를 기록한다.

## Procedure

1. 비공개 환경 값을 렌더링하지 않고 source boundary를 확인한다.

   ```bash
   rg -n 'profiles:|ai-image|gpus: all|COMFYUI_ARGS|comfyui-(models|custom-nodes|output|input|user)|system_stats|middlewares' infra/08-ai/comfyui/docker-compose.yml
   ```

2. 승인된 실행 중인 target에서 선택한 서비스만 확인하고 exit status를 캡처한다.

   ```bash
   docker compose --profile ai --profile ai-image ps comfyui
   curl --fail --silent --output /dev/null http://127.0.0.1:${COMFYUI_HOST_PORT:-8188}/system_stats
   ```

   응답이 오면 서비스 endpoint가 응답한 것이다. GPU 가시성과 승인된 대표 workflow는 별도로
   확인한다. 둘 다 이 문서에서 실행된 증거로 주장하지 않는다.

3. 이미지나 custom-node 업데이트가 실패를 유발했다면 새 workflow 작업을 중단하고, 이전 이미지
   식별자와 custom-node revision 인벤토리를 보존한 뒤, 추적된 구성을 검토된 버전으로 되돌린다.
   첫 대응으로 model 디렉터리나 캐시를 삭제하지 않는다.

4. 복구를 위해 queue 유입과 실행 중인 작업을 중단한 뒤 `models`, `custom_nodes`, `user`,
   `input`, `output`을 하나의 일관된 집합으로 보호한다. 먼저 격리된 mount로 복원하여 예상
   노드와 대표 workflow가 로드되는지 검증한 다음, 실제 데이터를 교체하기 전에 승인을 받는다.
   model과 캐시 다운로드는 source, digest, license, 호환성이 기록된 경우에만 재구축 가능하다.

### Planned isolated restore rehearsal

상태: **계획됨, 미실행**. 여기서는 ComfyUI restore 성공 증거를 주장하지 않는다.

1. 이미지 digest, CUDA/driver 버전, profile, mount 식별자, workflow 의존성 인벤토리, custom-node revision, model/input checksum/license를 기록한다. queue 유입을 일시 중지하고 실행 중인 작업을 완료하거나 취소한 뒤 ComfyUI를 중단하고, 승인된 일관 스냅샷을 생성한다.
2. 공개 route가 없는 별도 Compose project/network의 새 경로로 전체 집합을 복원한다. source 스냅샷은 불변 상태로 유지한다.
3. 고정된 이미지를 시작하고, `/system_stats`, GPU 가시성, model checksum, 예상 custom node, workflow 로드, 그리고 입력과 출력 invariant가 안전하게 기록 가능한 대표 생성 1건을 검증한다.
4. 불일치가 있으면 격리된 서비스를 중단하고 로그/checksum을 보존한다. 손대지 않은 source 아티팩트로 돌아간다. 프로덕션 mount나 route 교체에는 별도 승인된 변경이 필요하다.

## Evidence

정제된 명령 출력, 시각, commit, 선택한 profile, 이미지 식별자, mount 이름과 결과 상태를
현재 Task에 기록한다. 사용자 자산, workflow 콘텐츠, 비공개 환경, 토큰, 원격 다운로드
credential은 기록하지 않는다.

## Rollback or Recovery

추적된 구성만 검토된 버전으로 되돌린다. 영속 mount는 보존한다. 승인된 교체 전에 격리된
스토리지로 복원한다.

## Escalation

backup 부재, custom-node provenance 공백, 예상치 못한 노출, GPU 실패, 또는 파괴적 작업은
@buenhyden에게 에스컬레이션한다.

## Traceability

- 관장 architecture: [AD-0008](../../02.architecture/descriptions/0008-ai-architecture.md)
- 대상 peer 문서: [Guide](../guides/0081-comfyui.md), [Policy](../policies/0081-comfyui.md)

## Related Documents

- [Guide](../guides/0081-comfyui.md), [Policy](../policies/0081-comfyui.md)
- 런타임 고정 버전은 [ComfyUI Compose](../../../infra/08-ai/comfyui/docker-compose.yml)가 소유한다. [derived Compose image projection](../../../infra/tech-stack.versions.json)이 drift를 검증한다.
- [중앙 backup 정책](../policies/0021-backup-and-restore.md)
