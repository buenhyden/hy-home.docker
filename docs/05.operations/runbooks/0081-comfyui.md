---
title: "ComfyUI Runbook"
version: "0.2.2"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "operations"
artifact_id: "RUN-0081"
parent_ids:
- "GDE-0081"
created: "2026-09-19"
---

# ComfyUI Runbook

## Overview

이 런북은 ComfyUI(`comfyui`, profile `ai`/`ai-image`)의 승인 게이트된 진단과 복구, custom-node·이미지 변경 실패 대응, 격리 복원 계획을 다룬다.

## Trigger and Preconditions

승인된 ComfyUI 배포, UI 접근 불가, healthcheck 실패, 또는 계획된 데이터/이미지/custom-node
복구에 사용한다. 런타임 변경 전에 commit, 선택한 서비스, mount 위치, 이미지 식별자와 backup
증거를 기록한다.

### Service lifecycle prerequisites

최초 기동·재생성·upgrade·삭제 전 활성 image 경로와 실제 데이터 mount 대응을 별도로 입증해야 한다. 현재 `/opt`와 upstream `/root` 불일치가 해결되지 않아 완전한 백업·복구를 인증할 수 없다. 이 조건이 충족되기 전에는 image 교체나 volume 정리를 중단한다.

## Procedure

### Execution Boundary

저장소 root에서 아래의 정확한 service/profile과 기존 container를 선택한다. 변경 전에 승인 대상, source/image, 선행 readiness, 필요한 운영 권한과 부작용 범위를 확인한다. `up`은 dependency/provisioning job을 만들 수 있고 profile은 격리가 아니다. 진단은 기존 container의 `exec`를 사용하고 단순 조회를 위해 client/provisioner를 띄우지 않는다. 재시작은 요청 중단·memory/queue 손실·부작용 반복을 일으킬 수 있으므로 대상 drain/backup 조건을 먼저 충족한다. `restart`는 바뀐 Compose 설정이나 교체된 secret bind를 불러오지 않는다.

Log를 보존하기 전에 payload·credential·header/cookie·private path를 제거하고 명령·시각·상태·제한된 시험 증거만 남긴다. 예상 밖 출력, backup 누락, dependency 실패나 승인되지 않은 부작용이면 중단하고 @buenhyden에게 넘긴다. Config rollback은 data/schema 복구가 아니다. 전체 기동·중지는 [cold-start Runbook](0098-cold-start-and-reboot.md)의 대상 선택·의존성 확인 절차를 사용한다. 공통 절차는 [백업](0021-backup-and-restore.md), [image 변경](0086-dependency-version-management.md), [시크릿](0085-openbao.md), [계정](0014-keycloak.md), [gateway·인증서](0013-traefik.md)가 소유한다. 대상이 실제 사용하는 자격 증명·상태에만 적용하며 secret 값은 증거로 요구하지 않는다.

### 진단과 복구 단계

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
   확인한다. 둘 다 이 문서에서 실행한 증거로 주장하지 않는다.

3. 이미지나 custom-node 업데이트가 실패를 유발했다면 새 workflow 작업을 중단하고, 이전 이미지
   식별자와 custom-node revision 인벤토리를 보존한 뒤, 추적된 구성을 검토된 버전으로 되돌린다.
   첫 대응으로 model 디렉터리나 캐시를 삭제하지 않는다.

4. 복구를 위해 queue 유입과 실행 중인 작업을 중단한 뒤 `models`, `custom_nodes`, `user`,
   `input`, `output`을 하나의 일관된 집합으로 보호한다. 먼저 격리된 mount로 복원해 예상
   노드와 대표 workflow가 로드되는지 검증한 다음, 실제 데이터를 교체하기 전에 승인을 받는다.
   model과 캐시 다운로드는 source, digest, license, 호환성이 기록된 경우에만 다시 구축할 수 있다.

### Active-image persistence stop condition

[정책의 중단 조건](../policies/0081-comfyui.md#active-image-persistence-stop-condition)을 따른다. 재생성·image upgrade·cache/volume 정리·완전한 backup 판정 전에 활성 image 경로와 mount 대응을 확인하고 @buenhyden의 승인을 받는다.

## Verification

`docker compose --profile ai --profile ai-image ps comfyui`와 `/system_stats` 응답 상태를 확인한다. GPU 가시성과 승인된 대표 workflow는 별도로 확인한다.

정제된 명령 출력, 시각, commit, 선택한 profile, 이미지 식별자, mount 이름과 결과 상태를
현재 Task에 기록한다. 사용자 자산, workflow 콘텐츠, 비공개 환경, 토큰, 원격 다운로드
credential은 기록하지 않는다.

## Rollback and Escalation

### Rollback or Recovery

추적된 구성만 검토된 버전으로 되돌린다. 영속 mount는 보존한다. 승인된 교체 전에 격리된
스토리지로 복원한다.

#### Planned isolated restore rehearsal

**Project 이름만 바꿔서는 실행할 수 없다.** Rehearsal 전에 고정 container name, host port, bind path, external network와 route 충돌을 제거하고 production 통지·workflow egress를 차단한 별도 Compose/storage 정의를 승인한다. 격리와 대상 backup 계약을 검토하기 전에는 NOT_RUN으로 유지한다. 임의 project에 production volume이나 credential을 연결하지 않는다.

상태: **계획됨, 미실행**. 여기서는 ComfyUI restore 성공 증거를 주장하지 않는다.

1. 이미지 digest, CUDA/driver 버전, profile, mount 식별자, workflow 의존성 인벤토리, custom-node revision, model/input checksum/license를 기록한다. queue 유입을 일시 중지하고 실행 중인 작업을 완료하거나 취소한 뒤 ComfyUI를 중단하고, 승인된 일관 스냅샷을 생성한다.
2. 공개 route가 없는 별도 Compose project/network의 새 경로로 전체 집합을 복원한다. source 스냅샷은 불변 상태로 유지한다.
3. 고정된 이미지를 시작하고, `/system_stats`, GPU 가시성, model checksum, 예상 custom node, workflow 로드, 그리고 입력과 출력 invariant가 안전하게 기록 가능한 대표 생성 1건을 검증한다.
4. 불일치가 있으면 격리된 서비스를 중단하고 로그/checksum을 보존한다. 손대지 않은 source 아티팩트로 돌아간다. 프로덕션 mount나 route 교체에는 별도 승인된 변경이 필요하다.

### Escalation

backup 부재, custom-node provenance 공백, 예상치 못한 노출, GPU 실패, 또는 파괴적 작업은
@buenhyden에게 에스컬레이션한다.

## Related Documents

### Traceability

- 관장 architecture: [AD-0008](../../02.architecture/descriptions/0008-ai-architecture.md)
- 대상 peer 문서: [Guide](../guides/0081-comfyui.md), [Policy](../policies/0081-comfyui.md)

- [Guide](../guides/0081-comfyui.md), [Policy](../policies/0081-comfyui.md)
- 런타임 고정 버전은 [ComfyUI Compose](../../../infra/08-ai/comfyui/docker-compose.yml)가 소유한다. [derived Compose image projection](../../../infra/tech-stack.versions.json)이 drift를 검증한다.
- [중앙 backup 정책](../policies/0021-backup-and-restore.md)
