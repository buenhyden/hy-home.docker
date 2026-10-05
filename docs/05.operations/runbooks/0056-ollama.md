---
title: "Ollama Runbook"
version: "1.0.3"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "RUN-0056"
parent_ids:
- "GDE-0056"
created: "2026-05-17"
---

# Ollama Runbook

## Overview

## Trigger and Preconditions

### Overview

### Trigger and Preconditions

### Overview

이 런북은 Ollama 추론 계층 장애에 대한 즉시 실행 절차를 제공한다. GPU 미인식, VRAM OOM, API 장애를 신속히 진단·복구하고 상위 서비스(Open WebUI) 영향도를 최소화한다.

> Scope: Ollama Inference Service

---

### Purpose

- Ollama 추론 가용성을 빠르게 복구한다.
- GPU 경로 이상과 리소스 고갈 문제를 표준 절차로 처리한다.
- 복구 후 Open WebUI 연동 상태를 검증한다.

### When to Use

- Ollama API(`/api/tags`, `/api/generate`) 호출 실패.
- 컨테이너 내부 GPU 미인식 또는 CPU fallback 발생.
- 모델 로드 시 VRAM OOM으로 추론 실패.
- Open WebUI에서 모델 목록 미표시.

## Procedure

### Procedure

### Execution Boundary

저장소 root에서 아래의 정확한 service/profile과 기존 container를 선택한다. 변경 전에 승인 대상, source/image, 선행 readiness, 필요한 운영 권한과 부작용 범위를 확인한다. `up`은 dependency/provisioning job을 만들 수 있고 profile은 격리가 아니다. 진단은 기존 container의 `exec`를 사용하고 단순 조회를 위해 client/provisioner를 띄우지 않는다. 재시작은 요청 중단·memory/queue 손실·부작용 반복을 일으킬 수 있으므로 대상 drain/backup 조건을 먼저 충족한다. `restart`는 바뀐 Compose 설정이나 교체된 secret bind를 불러오지 않는다.

Log를 보존하기 전에 payload·credential·header/cookie·private path를 제거하고 명령·시각·상태·제한된 시험 증거만 남긴다. 예상 밖 출력, backup 누락, dependency 실패나 승인되지 않은 부작용이면 중단하고 @buenhyden에게 넘긴다. Config rollback은 data/schema 복구가 아니다. 전체 기동·중지는 [cold-start Runbook](0098-cold-start-and-reboot.md)의 대상 선택·의존성 확인 절차를 사용한다. 공통 절차는 [백업](0021-backup-and-restore.md), [image 변경](0086-dependency-version-management.md), [시크릿](0085-openbao.md), [계정](0014-keycloak.md), [gateway·인증서](0013-traefik.md)가 소유한다. 대상이 실제 사용하는 자격 증명·상태에만 적용하며 secret 값은 증거로 요구하지 않는다.

### Service lifecycle prerequisites

`ollama`는 모델 저장소 권한과 GPU runtime을 먼저 확인한다. `ollama-exporter`는 Ollama health 뒤 시작하며 자체 영속 상태·사용자 인증·모델 복원은 없다. Exporter 재생성 후 수집 결과를 확인하되 목록 조회를 추론 성공으로 처리하지 않는다. Ollama 중지·upgrade는 pull·추론을 완료하거나 중단 영향을 승인하고 모델 출처·checksum을 보존한 뒤 수행한다.

### Checklist

- [ ] 호스트 `nvidia-smi` 정상 여부 확인
- [ ] `ollama` 컨테이너 healthcheck 확인
- [ ] 최근 모델 변경/배포 이력 확인
- [ ] Open WebUI 영향 범위 확인

### Steps

#### 1. Initial Health & API Check

```bash
docker ps --filter name=ollama
docker logs --tail 200 ollama
curl -f http://localhost:${OLLAMA_HOST_PORT:-11434}/api/tags
```

##### 2. GPU Recognition Recovery

GPU 미인식 진단과 Docker daemon/컨테이너 재시작 절차는 [GPU Recovery runbook](0055-gpu-recovery.md)을 따른다.

### 3. VRAM OOM Mitigation

```bash

## Verification

### Evidence

- 실행 명령·결과·시각과 운영자 또는 agent 조치를 기록한다.
- 실패 검사, 관찰 증상과 최종 복구·에스컬레이션 상태를 관련 Task/Incident에 남긴다.

## Rollback and Escalation

### keep_alive=0으로 상주 모델 언로드(예시)
curl -X POST http://localhost:${OLLAMA_HOST_PORT:-11434}/api/generate -d '{
  "model": "llama3",
  "prompt": "",
  "keep_alive": 0
}'
```

- 고부하 모델 사용 중이면 operator approval을 받은 뒤에만 경량 모델로 전환한다.

### 4. Model Integrity Check

```bash
docker compose exec ollama ollama list
```

- 운영 기준 모델 태그가 존재하는지 확인한다.

#### 5. Open WebUI Dependency Recheck

```bash

### Open WebUI 컨테이너에서 Ollama 접근 확인
docker compose exec open-webui curl -f http://ollama:${OLLAMA_PORT:-11434}/api/tags
```

### 6. Scoped Upgrade Check and Rollback

이미지 버전의 단일 기준은 `infra/08-ai/ollama/docker-compose.yml`의 `ollama` image pin이다. 저장소 root에서 변경 전 `hy-home-infra_ollama-data` 볼륨과 기존 모델 목록·digest를 기록하고, 승인된 변경에서만 `ollama` 하나를 재생성한다.

```bash
docker compose --project-name hy-home-infra --profile ollama config --quiet
docker compose --project-name hy-home-infra --profile ollama pull ollama
docker compose --project-name hy-home-infra --profile ollama up -d --no-deps --force-recreate ollama
docker compose --project-name hy-home-infra --profile ollama ps ollama
curl -f http://127.0.0.1:${OLLAMA_HOST_PORT:-11434}/api/tags
```

재생성 뒤 version, health, 기존 digest, loopback 포트, GPU 요청, `ai_net`/`edge_net`, exporter와 Open WebUI backend `/api/tags`를 확인한다. decision 확인은 Guide의 synthetic `tev1:0.8b` 요청과 `keep_alive: 0`을 사용한다.

실패 시 승인된 rollback 계획에 따라 Compose pin을 변경 전에 기록한 image tag/digest로 복원하고 derived version projection을 재생성한 뒤 같은 단일-service 명령을 실행한다. `hy-home-infra_ollama-data`와 기존 모델은 삭제·교체하지 않는다. rollback rehearsal과 인증된 브라우저 UI 검증은 아직 실행되지 않았다.

위 unload 요청은 빈 prompt와 `keep_alive: 0`을 사용한다. 메모리가 부족할 때 새 모델을 불러오지 말고 이미 load된 승인 모델을 선택한다. 빈 문자열이 아닌 일반 prompt는 추론을 시작하므로 unload 검사가 아니다. `ollama list`/`api/tags`는 목록을, `nvidia-smi`는 장치 가시성을 보여준다. 복구 판정 전 제한된 승인 추론과 GPU 사용을 따로 확인하고 OOM 반복·예상 밖 download이면 중단한다.

### Model and exporter capacity boundary

`ollama`/`ollama-exporter`는 `ai`/`ai-llm`/`ollama`가 선택하는 HOME이다. 모델·추론은 Ollama가 소유하고 병렬·loaded-model·queue 설정은 context 크기와 공유 GPU 메모리와 함께 평가한다. 한도는 실측 여유가 아니며 과부하 요청은 실패할 수 있다. Exporter는 Ollama health 뒤 내부 model 목록·실행 모델·VRAM metric을 제공한다. Model volume, Docker Secret, 사용자 route나 독립 복구 상태는 없고 추론 proxy 또는 token throughput 증거도 아니다. Maintainer tag는 확인했으나 버전 일치 소스는 확보하지 못했으므로 Compose·maintainer 설명을 넘는 동작을 단정하지 않는다. Upgrade에는 metric 호환성과 제한된 추론 검증이 필요하다. 모델 삭제·download·driver 변경은 기존 승인·출처 및 [GPU 복구](../runbooks/0055-gpu-recovery.md) 경계를 따른다.

### Verification Steps

- [ ] `curl -f http://localhost:${OLLAMA_HOST_PORT:-11434}/api/tags` 성공
- [ ] `docker compose exec ollama nvidia-smi` 성공
- [ ] 기본 추론 요청(`/api/generate`) 성공
- [ ] Open WebUI에서 모델 조회/채팅 성공

### Observability and Evidence Sources

- **Signals**:
  - GPU 사용률 급락(미인식), VRAM 과점유, API 에러율 증가
- **Evidence to Capture**:
  - `ollama`/`open-webui` 로그
  - 수행 명령과 결과
  - 복구 전후 지표 스냅샷

### Safe Rollback or Recovery Procedure

- [ ] 직전 안정 모델 세트로 복원
- [ ] 임시 변경(대형 모델 상주, 디버그 설정) 제거
- [ ] 운영 정책 기준으로 자원 제한/모델 목록 재정렬

### Agent Operations (If Applicable)

- **Prompt Rollback**: 모델별 기본 프롬프트를 직전 안정값으로 복원
- **Model Fallback**: operator approval을 받은 뒤에만 경량 모델로 전환
- **Tool Disable / Revoke**: 문제 모델 호출 경로 일시 차단
- **Eval Re-run**: 추론 smoke test + Open WebUI 연동 테스트 재실행
- **Trace Capture**: 장애 시간대 API/리소스 로그 보존

### Planned isolated restore rehearsal

**Project 이름만 바꿔서는 실행할 수 없다.** Rehearsal 전에 고정 container name, host port, bind path, external network와 route 충돌을 제거하고 production 통지·workflow egress를 차단한 별도 Compose/storage 정의를 승인한다. 격리와 대상 backup 계약을 검토하기 전에는 NOT_RUN으로 유지한다. 임의 project에 production volume이나 credential을 연결하지 않는다.

상태: **계획됨·미실행**. 이 문서에는 Ollama 모델 저장소의 복원 성공 증거가 없다.

1. 이미지 digest, 드라이버·runtime 버전, 모델 목록, manifest·blob checksum, 모델 출처·라이선스, Compose profile, 대표 추론 요청과 기대 불변 조건을 기록한다. 모델 받기와 활성 추론을 중지한 뒤 `ollama-data`의 일관된 중지 상태 복사본이나 승인된 스토리지 snapshot을 만든다.
2. 공개 경로가 없는 별도 프로젝트와 격리 모델 경로에 복원한다. 재구축을 선택하면 승인된 출처에서 기록한 digest·버전만 받고 라이선스·checksum을 확인한다.
3. 호환되는 GPU·runtime 설정으로 Ollama를 기동하고 `/api/tags`, 모델 digest, GPU 인식, 대표 추론 한 건, exporter 수집을 확인한다. Open WebUI는 격리 endpoint에 대해서만 시험한다.
4. 불일치하면 격리 서비스를 중지하고 로그·checksum을 보존한 뒤 변경하지 않은 백업·원본 manifest로 돌아간다. 운영 volume이나 경로 교체에는 별도 변경 승인이 필요하다.

### Rollback or Recovery

- 이 Runbook에 기록된 복구·rollback 절차와 위의 `Safe Rollback or Recovery Procedure` 하위 절차만 사용한다.
- 위 격리 복구 계획은 미실행 상태다. rehearsal 완료로 표시하기 전에 날짜가 있는 증거를 첨부한다.
- 관찰한 장애가 문서화된 절차와 다르면 변경을 중지하고 증거를 보존한 뒤 `## Escalation`에 따라 보고한다.

### Escalation

검증 실패, secret 노출 위험, 파괴적 변경 필요 또는 예상 절차와 다른 상태이면 중단하고 @buenhyden에게 넘긴다. 정제된 증거, 시도한 단계와 현재 rollback/recovery 상태를 함께 전달한다.

### Traceability

- Declared parent: [Ollama Usage Guide](../guides/0056-ollama.md) (`GDE-0056`)
- Governing authority: [AI Infrastructure Architecture Description](../../02.architecture/descriptions/0008-ai-architecture.md) (`AD-0008`)
- Subject peers: [Guide](../guides/0056-ollama.md) (`GDE-0056`), [Policy](../policies/0056-ollama.md) (`POL-0056`)

## Related Documents

- 런타임 고정값은 Compose/Dockerfile 선언이 소유하며 [파생 이미지 목록](../../../infra/tech-stack.versions.json)은 드리프트 검증에 사용한다.

- [Operations index](../README.md)
- [Usage guide](../guides/0056-ollama.md)
- [Operations policy](../policies/0056-ollama.md)
- [Ollama release notes](https://github.com/ollama/ollama/releases)
