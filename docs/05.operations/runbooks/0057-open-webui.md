---
title: "Open WebUI Runbook"
version: "1.1.1"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "RUN-0057"
parent_ids:
- "GDE-0057"
created: "2026-05-17"
---

# Open WebUI Runbook

## Overview

이 런북은 Open WebUI 장애 및 성능 저하 상황에서 즉시 실행 가능한 복구 절차를 제공한다. SQLite 데이터 복구, RAG 인덱스 재동기화, Ollama 연결과 local Chroma 일관성 복구를 표준화한다.

> Scope: Open WebUI Service

---

### Purpose

- Open WebUI 가용성을 신속히 복구한다.
- RAG 기능(인덱싱/검색) 정상 상태를 재확인한다.
- 동일 장애 재발 시 일관된 증적을 남긴다.

## When to Use

- `https://chat.${DEFAULT_URL}` 접속 실패 또는 5xx 증가.
- 모델 목록 미표시, 채팅 응답 실패.
- 문서 업로드 후 RAG 인덱싱 실패.
- Open WebUI healthcheck 실패.

## Procedure

### Execution Boundary

저장소 root에서 아래의 정확한 service/profile과 기존 container를 선택한다. 변경 전에 승인 대상, source/image, 선행 readiness, 필요한 운영 권한과 부작용 범위를 확인한다. `up`은 dependency/provisioning job을 만들 수 있고 profile은 격리가 아니다. 진단은 기존 container의 `exec`를 사용하고 단순 조회를 위해 client/provisioner를 띄우지 않는다. 재시작은 요청 중단·memory/queue 손실·부작용 반복을 일으킬 수 있으므로 대상 drain/backup 조건을 먼저 충족한다. `restart`는 바뀐 Compose 설정이나 교체된 secret bind를 불러오지 않는다.

Log를 보존하기 전에 payload·credential·header/cookie·private path를 제거하고 명령·시각·상태·제한된 시험 증거만 남긴다. 예상 밖 출력, backup 누락, dependency 실패나 승인되지 않은 부작용이면 중단하고 @buenhyden에게 넘긴다. Config rollback은 data/schema 복구가 아니다. 전체 기동·중지는 [cold-start Runbook](0098-cold-start-and-reboot.md)의 대상 선택·의존성 확인 절차를 사용한다. 공통 절차는 [백업](0021-backup-and-restore.md), [image 변경](0086-dependency-version-management.md), [시크릿](0085-openbao.md), [계정](0014-keycloak.md), [gateway·인증서](0013-traefik.md)가 소유한다. 대상이 실제 사용하는 자격 증명·상태에만 적용하며 secret 값은 증거로 요구하지 않는다.

### Service lifecycle prerequisites

`open-webui`는 Ollama health와 auth secret·CA·local data mount가 필요하다. 기존 SQLite·Chroma·업로드를 같은 시점으로 보존하고 migration·image 변경을 승인한 뒤 기동한다. 중지 전 session·ingestion을 차단한다. CUDA tag만으로 GPU 할당을 기대하지 않는다.

### Checklist

- [ ] `open-webui` 컨테이너 상태/로그 확인
- [ ] `ollama` health와 전체 WebUI data volume의 SQLite/Chroma/uploads 상태 확인
- [ ] 인증(SSO) 경로 정상 여부 확인
- [ ] 데이터 디렉터리 백업 가능 여부 확인

### Steps

#### 1. Initial Triage

```bash
docker ps --filter name=open-webui
docker logs --tail 200 open-webui
docker compose exec open-webui curl -f http://localhost:${OLLAMA_WEBUI_PORT:-8080}/health
```

##### 2. Dependency Connectivity Check

```bash

## Open WebUI -> Ollama
docker compose exec open-webui curl -f http://ollama:${OLLAMA_PORT:-11434}/api/tags

```

로컬 Chroma는 `/app/backend/data`에 포함되며 Qdrant endpoint는 선언되지 않았다. 의존 서비스가 정상화된 뒤 UI에서 승인된 RAG 질의로 확인한다.

### Native Keycloak OIDC migration and recovery

- 전용 client는 `home-openwebui`이며 S256 PKCE를 쓰는 confidential authorization-code flow다. Callback은 `https://chat.${DEFAULT_URL}/oauth/oidc/callback`, discovery realm은 `hy-home.realm`이고 private-CA TLS를 검증한다.
- `secrets/auth/openwebui_oidc_client_secret.txt`는 `/run/secrets/openwebui_oidc_client_secret`에 읽기 전용 mount된다. Capability 없는 UID 0 프로세스가 읽도록 host 파일은 **root:root 0600**이어야 한다. UID 1000 소유 0600은 읽지 못한다. 회전 시 해당 파일 소유권 이전을 승인 범위에 포함하고 권한 확대나 DAC capability 추가로 우회하지 않는다. 값을 출력하거나 Compose 환경 텍스트에 넣지 않는다. Entry point가 process 내부에서만 export한다.
- `rootCA.pem`은 공개 인증서이며 private key가 아니다. UID 0이 읽을 수 있어야 하고 mode 변경 전 certificate-only 여부를 확인한다. Entry point는 공개 CA와 결합하며 TLS 검증을 끄지 않는다.

### Historical transition record

Task 0004는 완료된 native-OIDC 전환의 당시 수용 기록이며 현재 상태를 변경하는 실행 절차가 아니다. 현재 Compose는 `home-openwebui`와 표준 gateway chain을 쓰고 proxy SSO는 없다. Password/signup/email merge/OAuth role·group 관리는 비활성화 상태를 유지하며 진단을 위해 다시 켜지 않는다.

`open-webui` bind volume은 SQLite 상태를 담는다. 쓰기 중인 DB를 복사하지 않는다. [중앙 백업 정책](../policies/0021-backup-and-restore.md)에 따라 먼저 격리 복원하고 identity/chat 보존 근거를 남긴 뒤 교체를 승인한다. Config rollback만으로 DB 복원이 허가되지 않는다.

### 3. SQLite Backup and Recovery

Live directory를 복사하지 않는다. 사용자·RAG 유입을 멈추고 `open-webui`를 정지한 뒤 승인된 SQLite 일관 backup 또는 정지 filesystem snapshot을 만든다. Image digest, migration level, secret 참조, volume identity와 SQLite/upload/local Chroma의 checksum을 같은 복구 시점으로 기록한다. Backup 검사가 성공한 뒤 재시작한다.

### 4. RAG Index Re-sync

1. Open WebUI 문서 관리에서 실패한 인덱스를 식별한다.
2. 원문/권한/embedding model과 전체 데이터 backup을 먼저 확인한다. 실패 인덱스만 승인된 UI 경로로 재인덱싱한다. 삭제·재업로드는 데이터/권한 손실 영향을 승인한 경우에만 수행한다.
3. 로컬 Chroma와 upload/metadata의 일치 및 검색 권한을 확인한다. Qdrant 복구나 raw SQL/schema 조작은 이 구현의 정상 복구 경로가 아니다.

#### 5. Service Restart Path

`ollama` 재시작/복구는 [Ollama runbook](0056-ollama.md) 및 필요 시 [GPU Recovery runbook](0055-gpu-recovery.md)을 따른다. 의존 서비스 정상화가 확인된 뒤에만 아래 명령으로 Open WebUI를 마지막에 재시작한다.

```bash
docker compose restart open-webui
```

### Local data and authentication boundary

선언 릴리스는 `DATA_DIR/vector_db`의 Chroma를 기본으로 쓰며 Compose에는 외부 vector-store나 Qdrant 연결이 없다. SQLite·vector·upload·identity와 embedding-model 출처를 함께 보존한다. CUDA image 이름만으로 GPU가 할당되지는 않으며 WebUI에는 GPU 예약이 없다. 로컬 entrypoint는 한 줄 OIDC secret과 검증된 CA bundle을 읽고 인자가 없으면 upstream `bash start.sh`로 시작한다.

`ENABLE_PASSWORD_AUTH=false`는 폼 숨김과 별도로 password 인증을 막는다. `ENABLE_OAUTH_PERSISTENT_CONFIG=false`는 OAuth 설정만 관장하며 모든 저장 설정을 끄지 않는다. 선언 버전의 `key/value`별 schema에 과거 단일 `id/data` 행 SQL 복구를 적용하지 않는다. Native login, signup/password 거부와 identity 연속성은 승인된 별도 검사로 확인하며 health가 대신하지 않는다.

### Verification Steps

- [ ] `docker compose exec open-webui curl -f http://localhost:${OLLAMA_WEBUI_PORT:-8080}/health` 성공
- [ ] UI 로그인 및 모델 목록 조회 성공
- [ ] 테스트 채팅 응답 성공
- [ ] 테스트 문서 업로드 후 RAG 질의 성공

### Observability and Evidence Sources

- **Signals**:
  - Open WebUI healthcheck 실패율
  - 5xx 응답률 상승
  - 인덱싱 실패율 증가
- **Evidence to Capture**:
  - `open-webui`/`ollama` 로그의 비식별 스니펫
  - 수행 명령 및 결과
  - 복구 전후 확인 화면/지표

### Safe Rollback or Recovery Procedure

- [ ] Open WebUI 변경 직후 이상 발생 시 이전 설정으로 되돌린다.
- [ ] 데이터 손상 시 검증된 image/schema/secret 일치 backup으로 전체 data set을 먼저 격리 복원한다. 가장 최신이라는 이유만으로 live DB를 덮어쓰지 않는다.
- [ ] 재기동 후 최소 기능(로그인/채팅/인덱싱) 확인까지 완료한다.

### Agent Operations (If Applicable)

- **Prompt Rollback**: 최근 프롬프트/설정 변경을 직전 안정 버전으로 복원
- **Model Fallback**: operator approval을 받은 뒤에만 고부하 모델에서 안정 모델로 전환
- **Tool Disable / Revoke**: 문서 업로드/자동 인덱싱 기능 임시 비활성
- **Eval Re-run**: 기본 채팅 + RAG smoke test 재실행
- **Trace Capture**: 장애 시간대 로그/지표를 증적으로 보존

### Planned isolated restore rehearsal

**Project 이름만 바꿔서는 실행할 수 없다.** Rehearsal 전에 고정 container name, host port, bind path, external network와 route 충돌을 제거하고 production 통지·workflow egress를 차단한 별도 Compose/storage 정의를 승인한다. 격리와 대상 backup 계약을 검토하기 전에는 NOT_RUN으로 유지한다. 임의 project에 production volume이나 credential을 연결하지 않는다.

상태: **계획됨·미실행**. Open WebUI 복원 성공을 주장하지 않는다.

1. 새 세션과 입력을 차단하고 이미지·DB 버전 및 사용자·대화·업로드 건수를 기록한다. Open WebUI를 중지한 뒤 전체 `/app/backend/data` volume과 일치하는 auth·OIDC secret 참조를 일관되게 백업한다. SQLite, 로컬 Chroma, 업로드를 같은 복구 시점에 포함한다.
2. 운영 경로가 없는 별도 Compose 프로젝트·네트워크에 WebUI 백업과 승인된 secret을 복원한다. RAG 검증 전에 로컬 Chroma index·업로드와 WebUI 메타데이터의 일관성을 유지한다.
3. 격리된 Ollama와 복원한 로컬 데이터에 연결해 Open WebUI를 기동한다. 스키마 시작, 사용자·대화 건수, 업로드, `home-openwebui`의 Keycloak 네이티브 로그인, 비활성화된 비밀번호·가입 경로, 모델 목록, 통제된 RAG 질의 한 건을 확인한다.
4. 불일치하면 격리 프로젝트를 중지하고 로그·checksum을 보존한다. 변경하지 않은 원본 백업으로 돌아가며 운영 volume·로컬 index·OIDC client·경로 교체에는 별도 승인이 필요하다.

## Evidence

- 실행 명령·결과·시각과 운영자 또는 agent 조치를 기록한다.
- 실패 검사, 관찰 증상과 최종 복구·에스컬레이션 상태를 관련 Task/Incident에 남긴다.

## Rollback or Recovery

- 이 Runbook에 기록된 복구·rollback 절차와 위의 `Safe Rollback or Recovery Procedure` 하위 절차만 사용한다.
- 위 격리 복원 계획은 미실행 상태다. rehearsal 완료로 표시하기 전에 날짜가 있는 WebUI·로컬 index 증거를 첨부한다.
- 관찰한 장애가 문서화된 절차와 다르면 변경을 중지하고 증거를 보존한 뒤 `## Escalation`에 따라 보고한다.

## Escalation

검증 실패, secret 노출 위험, 파괴적 변경 필요 또는 예상 절차와 다른 상태이면 중단하고 @buenhyden에게 넘긴다. 정제된 증거, 시도한 단계와 현재 rollback/recovery 상태를 함께 전달한다.

## Traceability

- Declared parent: [Open WebUI Usage Guide](../guides/0057-open-webui.md) (`GDE-0057`)
- Governing authority: [AI Infrastructure Architecture Description](../../02.architecture/descriptions/0008-ai-architecture.md) (`AD-0008`)
- Subject peers: [Guide](../guides/0057-open-webui.md) (`GDE-0057`), [Policy](../policies/0057-open-webui.md) (`POL-0057`)

## Related Documents

- 런타임 고정값은 Compose/Dockerfile 선언이 소유하며 [파생 이미지 목록](../../../infra/tech-stack.versions.json)은 드리프트 검증에 사용한다.

- [Operations index](../README.md)
- [Usage guide](../guides/0057-open-webui.md)
- [Operations policy](../policies/0057-open-webui.md)
