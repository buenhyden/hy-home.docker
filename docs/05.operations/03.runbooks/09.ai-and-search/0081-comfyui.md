---
title: "ComfyUI Runbook"
version: "1.0.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
layer: "operations"
artifact_id: "RUN-0081"
parent_ids:
- "GDE-0081"
created: "2026-09-19"
next_review_at: "2027-05-13"
---

# ComfyUI Runbook

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the runbook payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Trigger and Scope

##### Trigger

이 런북은 선택형 ComfyUI(`comfyui`, profile `ai-image`)의 승인된 진단과 복구, custom-node·이미지 변경 실패 대응, 격리 복원 계획을 다룬다.

승인된 ComfyUI 배포, UI 접근 불가, healthcheck 실패, 또는 계획된 데이터/이미지/custom-node
복구에 사용한다.

##### Targets

- 관장 architecture: [AD-0008](../../../02.architecture/01.descriptions/0008-ai-architecture.md)
- 대상 peer 문서: [Guide](../../01.guides/09.ai-and-search/0081-comfyui.md), [Policy](../../02.policies/09.ai-and-search/0081-comfyui.md)

- [Guide](../../01.guides/09.ai-and-search/0081-comfyui.md), [Policy](../../02.policies/09.ai-and-search/0081-comfyui.md)
- 런타임 고정 버전은 [ComfyUI Compose](../../../../infra/08-ai/comfyui/docker-compose.yml)가 소유한다. [derived Compose image projection](../../../../infra/tech-stack.versions.json)이 drift를 검증한다.
- [중앙 backup 정책](../../02.policies/10.platform-and-backup/0021-backup-and-restore.md)
- 이 문서는 SPEC-0267 secondary-listener hardening 결과를 담고 있다. 해당 패키지는 retire되었고 본문은 version history에 있다.

#### Preflight

##### Authority

승인과 실행 경계는 아래 항목에 따른다.

###### Execution Boundary
<!-- core-payload-level:4 -->

저장소 root에서 아래의 정확한 service/profile과 기존 container를 선택한다. 변경 전에 승인 대상, source/image, 선행 readiness, 필요한 운영 권한과 부작용 범위를 확인한다. `up`은 dependency/provisioning job을 만들 수 있고 profile은 격리가 아니다. 진단은 기존 container의 `exec`를 사용하고 단순 조회를 위해 client/provisioner를 띄우지 않는다. 재시작은 요청 중단·memory/queue 손실·부작용 반복을 일으킬 수 있으므로 대상 drain/backup 조건을 먼저 충족한다. `restart`는 바뀐 Compose 설정이나 교체된 secret bind를 불러오지 않는다.

Log를 보존하기 전에 payload·credential·header/cookie·private path를 제거하고 명령·시각·상태·제한된 시험 증거만 남긴다. 예상 밖 출력, backup 누락, dependency 실패나 승인되지 않은 부작용이면 중단하고 @buenhyden에게 넘긴다. Config rollback은 data/schema 복구가 아니다. 전체 기동·중지는 [cold-start Runbook](../01.common/0098-cold-start-and-reboot.md)의 대상 선택·의존성 확인 절차를 사용한다. 공통 절차는 [백업](../10.platform-and-backup/0021-backup-and-restore.md), [image 변경](../10.platform-and-backup/0086-dependency-version-management.md), [시크릿](../04.security-and-secrets/0085-openbao.md), [계정](../03.identity-and-access/0014-keycloak.md), [gateway·인증서](../02.gateway-and-networking/0013-traefik.md)가 소유한다. 대상이 실제 사용하는 자격 증명·상태에만 적용하며 secret 값은 증거로 요구하지 않는다.

##### Environment

런타임 변경 전에 commit, 선택한 서비스, mount 위치, 이미지 식별자와 backup
증거를 기록한다.

###### Service lifecycle prerequisites
<!-- core-payload-level:4 -->

image upgrade 전에 새 image가 `/root/ComfyUI`에서 시작하고 `models`, `custom_nodes`, `input`, `output`, `user` mount가 그 아래에 대응하는지 확인한다. 2026-11-08에 이 다섯 volume을 `/root/ComfyUI/<dir>`로 다시 mount했으므로 이전의 `/opt` 불일치는 해소되었다. 대응이 어긋나면 image 교체나 volume 정리를 중단한다.

#### Procedure

##### Steps

| Step | Action | Expected Result | On Failure |
| --- | --- | --- | --- |
| 1 | 진단과 복구 단계: 비공개 환경 값을 렌더링하지 않고 `rg`로 source boundary를 확인한다 | 문서에 기록 없음 | 중단하고 Stop Conditions에 따라 @buenhyden에게 escalation |
| 2 | 진단과 복구 단계: 승인된 실행 중 target에서 `ps comfyui`와 `/system_stats`를 확인하고 exit status를 캡처한다 | 서비스 endpoint가 응답한다. GPU 가시성과 대표 workflow는 별도로 확인한다 | 중단하고 Stop Conditions에 따라 @buenhyden에게 escalation |
| 3 | 진단과 복구 단계: 업데이트가 실패를 유발했으면 새 workflow를 중단하고 이전 image 식별자와 custom-node revision을 보존한 뒤 추적된 구성을 되돌린다 | 문서에 기록 없음 | 첫 대응으로 model 디렉터리나 캐시를 삭제하지 않고 중단하여 @buenhyden에게 escalation |
| 4 | 진단과 복구 단계: queue를 중단하고 `models`, `custom_nodes`, `user`, `input`, `output`을 일관된 집합으로 보호하여 격리 mount에서 복원 검증한다 | 예상 노드와 대표 workflow가 로드된다 | 실제 데이터 교체 전에 승인을 받고 mount 불일치면 @buenhyden 승인 아래 중단한다 |
| 5 | 유지보수용 외부 접속: @buenhyden 승인 후 egress overlay로 ComfyUI만 재생성한다 | `comfyui_egress_net`과 `127.0.0.1:8188`이 생긴다 | 중단하고 Stop Conditions에 따라 @buenhyden에게 escalation |
| 6 | 유지보수용 외부 접속: 설치를 마치고 model과 custom node의 source/revision을 기록한다 | 문서에 기록 없음 | 중단하고 Stop Conditions에 따라 @buenhyden에게 escalation |
| 7 | 유지보수용 외부 접속: overlay 없이 재생성하고 외부 접속이 막혔는지 확인한다 | network 목록이 `comfyui_ingress_net` 하나다 | 아니면 중단하고 @buenhyden에게 넘긴다 |

절차는 아래 항목에 따른다.

###### 진단과 복구 단계
<!-- core-payload-level:4 -->

1. 비공개 환경 값을 렌더링하지 않고 source boundary를 확인한다.

   ```bash
   rg -n 'profiles:|ai-image|gpus: all|COMFYUI_ARGS|comfyui-(models|custom-nodes|output|input|user)|system_stats|middlewares' infra/08-ai/comfyui/docker-compose.yml
   ```

2. 승인된 실행 중인 target에서 선택한 서비스만 확인하고 exit status를 캡처한다.

   ```bash
   docker compose --profile ai-image ps comfyui
   docker exec comfyui wget -qO /dev/null http://127.0.0.1:${COMFYUI_PORT:-8188}/system_stats
   ```

   기본 구성은 host port를 게시하지 않으므로(SPEC-0268) container 안에서 확인한다.
   응답이 오면 서비스 endpoint가 응답한 것이다. GPU 가시성과 승인된 대표 workflow는 별도로
   확인한다. 둘 다 이 문서에서 실행한 증거로 주장하지 않는다.

3. 이미지나 custom-node 업데이트가 실패를 유발했다면 새 workflow 작업을 중단하고, 이전 이미지
   식별자와 custom-node revision 인벤토리를 보존한 뒤, 추적된 구성을 검토된 버전으로 되돌린다.
   첫 대응으로 model 디렉터리나 캐시를 삭제하지 않는다.

4. 복구를 위해 queue 유입과 실행 중인 작업을 중단한 뒤 `models`, `custom_nodes`, `user`,
   `input`, `output`을 하나의 일관된 집합으로 보호한다. 먼저 격리된 mount로 복원해 예상
   노드와 대표 workflow가 로드되는지 검증한 다음, 실제 데이터를 교체하기 전에 승인을 받는다.
   model과 캐시 다운로드는 source, digest, license, 호환성이 기록된 경우에만 다시 구축할 수 있다.

###### 유지보수용 외부 접속
<!-- core-payload-level:4 -->

기본 구성의 ComfyUI는 외부로 나가지 못하고 host port도 없다(SPEC-0268). 모델이나
custom node를 설치할 때만 @buenhyden의 승인을 받아 overlay를 붙이고, 작업이 끝나면
바로 떼어낸다.

1. 붙이기: overlay를 더해 ComfyUI만 재생성한다. `comfyui_egress_net`과
   `127.0.0.1:8188`이 생긴다.

   ```bash
   docker compose -p hy-home-infra -f docker-compose.yml -f infra/08-ai/comfyui/docker-compose.egress.yml --profile ai-image up -d --no-deps --force-recreate comfyui
   ```

2. 설치를 마치고 설치한 model과 custom node의 source·revision을 기록한다.
3. 떼어내기: overlay 없이 다시 재생성하고 외부 접속이 막혔는지 확인한다.

   ```bash
   docker compose -p hy-home-infra -f docker-compose.yml --profile ai-image up -d --no-deps --force-recreate comfyui
   docker inspect comfyui --format '{{range $k, $v := .NetworkSettings.Networks}}{{$k}} {{end}}'
   ```

   network 목록이 `comfyui_ingress_net` 하나여야 한다. 아니면 중단하고 @buenhyden에게 넘긴다.

###### ComfyUI-Manager 보안 수준
<!-- core-payload-level:4 -->

`comfyui-user` volume의 `__manager/config.ini`는 `security_level = normal`을 유지한다.
image bundle은 첫 실행 때 `weak`로 이 파일을 만들지만, ComfyUI-Manager의 기본값은
`normal`이다. `weak`는 ComfyUI가 `--listen 0.0.0.0`으로 떠 있는 동안 high 위험 기능
(`.safetensors`가 아닌 model 내려받기 등)까지 허용한다. `normal`은 high 위험 기능을 막고,
기본 channel에서 node를 설치·갱신·삭제하는 middle 위험 기능은 그대로 둔다. Git URL과
pip 설치는 수준과 상관없이 별도 flag와 loopback `--listen`이 있어야 하므로 계속 막힌다.

bundle 복사는 `--no-clobber`라서 기존 파일을 덮어쓰지 않는다. volume을 새로 만들었거나
값이 `weak`로 돌아갔으면 @buenhyden의 승인을 받아 아래처럼 고친다. Manager는 이 값을
시작할 때 한 번만 읽으므로 고친 뒤 재시작한다.

```bash
docker exec comfyui sed -i 's/^security_level = .*/security_level = normal/' /root/ComfyUI/user/__manager/config.ini
docker restart comfyui
docker exec comfyui grep '^security_level' /root/ComfyUI/user/__manager/config.ini
```

마지막 줄이 `security_level = normal`이고 container가 healthy로 돌아와야 한다.

##### Stop Conditions

중단 조건은 아래 항목에 기록한다.

###### Active-image persistence stop condition
<!-- core-payload-level:4 -->

[정책의 조건](../../02.policies/09.ai-and-search/0081-comfyui.md#active-image-persistence-stop-condition)을 따른다. image upgrade 전에 `/root/ComfyUI` 아래 mount 대응을 확인하고, 어긋나면 @buenhyden의 승인 아래 중단한다.

#### Verification

##### Expected Results

###### Service Checks
<!-- core-payload-level:4 -->

`docker compose --profile ai-image ps comfyui`와 `/system_stats` 응답 상태를 확인한다. GPU 가시성과 승인된 대표 workflow는 별도로 확인한다.

###### Evidence
<!-- core-payload-level:4 -->

정제된 명령 출력, 시각, commit, 선택한 profile, 이미지 식별자, mount 이름과 결과 상태를
현재 Task에 기록한다. 사용자 자산, workflow 콘텐츠, 비공개 환경, 토큰, 원격 다운로드
credential은 기록하지 않는다.

##### Unverified Conditions

이 런북이 아직 관찰하지 못한 항목은 다음과 같다. 문서는 GPU 가시성과 승인된 대표 workflow를 이 문서에서 실행한 증거로 주장하지 않는다고 밝힌다.

- `/system_stats` 응답과 GPU 가시성, 대표 workflow 실행: 승인된 실행 target에서의 exit status와 결과가 필요하다.
- 일관된 집합 보호와 격리 mount 복원(승인 필요): 예상 노드와 대표 workflow가 로드되는 관찰이 필요하다.
- 유지보수용 외부 접속 overlay 부착과 분리(@buenhyden 승인 필요): 분리 뒤 network 목록이 `comfyui_ingress_net` 하나인 출력이 필요하다.
- ComfyUI-Manager `security_level = normal` 보정과 재시작(승인 필요): 보정 뒤 `grep` 출력과 healthy 복귀가 필요하다.

#### Escalation

##### Next Owner

backup 부재, custom-node provenance 공백, 예상치 못한 노출, GPU 실패, 또는 파괴적 작업은
@buenhyden에게 에스컬레이션한다.

##### Recovery or Forward Repair

추적된 구성만 검토된 버전으로 되돌린다. 영속 mount는 보존한다. 승인된 교체 전에 격리된
스토리지로 복원한다.

###### Planned isolated restore rehearsal
<!-- core-payload-level:4 -->

**Project 이름만 바꿔서는 실행할 수 없다.** Rehearsal 전에 고정 container name, host port, bind path, external network와 route 충돌을 제거하고 production 통지·workflow egress를 차단한 별도 Compose/storage 정의를 승인한다. 격리와 대상 backup 계약을 검토하기 전에는 NOT_RUN으로 유지한다. 임의 project에 production volume이나 credential을 연결하지 않는다.

상태: **계획됨, 미실행**. 여기서는 ComfyUI restore 성공 증거를 주장하지 않는다.

1. 이미지 digest, CUDA/driver 버전, profile, mount 식별자, workflow 의존성 인벤토리, custom-node revision, model/input checksum/license를 기록한다. queue 유입을 일시 중지하고 실행 중인 작업을 완료하거나 취소한 뒤 ComfyUI를 중단하고, 승인된 일관 스냅샷을 생성한다.
2. 공개 route가 없는 별도 Compose project/network의 새 경로로 전체 집합을 복원한다. source 스냅샷은 불변 상태로 유지한다.
3. 고정된 이미지를 시작하고, `/system_stats`, GPU 가시성, model checksum, 예상 custom node, workflow 로드, 그리고 입력과 출력 invariant가 안전하게 기록 가능한 대표 생성 1건을 검증한다.
4. 불일치가 있으면 격리된 서비스를 중단하고 로그/checksum을 보존한다. 손대지 않은 source 아티팩트로 돌아간다. 프로덕션 mount나 route 교체에는 별도 승인된 변경이 필요하다.

## 적용과 확인

### 적용 방법

Use the procedures or reading order stated in the role payload.

### 확인 기준

Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.

## 관계와 출처

### 관련 문서

The role payload retains the current owner and dependency references.

### 외부 근거

External basis and its limits remain those stated in the role payload; a citation grants no authority.
