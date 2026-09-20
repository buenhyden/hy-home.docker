---
title: "Open WebUI Runbook"
version: "1.1.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "RUN-0057"
parent_ids:
- "GDE-0057"
created: "2026-05-17"
---

# Open WebUI Runbook

## Overview

이 런북은 Open WebUI 장애 및 성능 저하 상황에서 즉시 실행 가능한 복구 절차를 제공한다. SQLite 데이터 복구, RAG 인덱스 재동기화, Ollama/Qdrant 연결 복구를 표준화한다.

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

### Checklist

- [ ] `open-webui` 컨테이너 상태/로그 확인
- [ ] `ollama`, `qdrant` 상태 및 health 확인
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

## Open WebUI -> Qdrant
docker compose exec open-webui curl -f http://qdrant:${QDRANT_PORT:-6333}/collections
```

### Native Keycloak OIDC migration and recovery

- Dedicated client: `home-openwebui`; confidential authorization-code flow with
  S256 PKCE. Callback: `https://chat.${DEFAULT_URL}/oauth/oidc/callback`.
  Discovery uses the `hy-home.realm` realm and verified private-CA TLS.
- Client secret: `secrets/auth/openwebui_oidc_client_secret.txt`, mounted read-only
  at `/run/secrets/openwebui_oidc_client_secret`. Open WebUI runs as UID 0 with
  all capabilities dropped: the host file must be **root:root 0600**. A UID 1000
  mode-0600 file is unreadable to this process. Rotation must include a privileged
  ownership transfer of this exact file; do not broaden permissions or add DAC
  capabilities to the application. Never print the file or put its value in
  Compose environment text. The entrypoint exports it only inside the process.
- The mounted `rootCA.pem` is a public certificate, not a private key. It must be
  readable by UID 0 (0644); verify certificate-only content before changing mode.
  The entrypoint combines it with public CA roots without disabling TLS checks.

### Historical transition record

Task 0004 records the completed native-OIDC migration and acceptance evidence;
it is not an executable current-state procedure. Current Compose uses the
`home-openwebui` client and `gateway-standard-chain@file`, without `sso-auth@file`.
Password login, signup, email account merge, and OAuth role/group management
remain disabled. Do not re-enable them to diagnose an incident.

The named `open-webui` bind volume holds the SQLite state. Do not copy its live
database while the service may write. Follow the central [backup policy](../../04-data/0021-backup-and-restore/policy.md), restore first to isolated storage, and record identity/chat preservation evidence before any replacement. A configuration rollback does not justify a database restore.

### 3. SQLite Backup and Recovery

Do not copy the live directory. Quiesce users and RAG ingestion, stop
`open-webui`, then use an approved SQLite-consistent backup or stopped
filesystem snapshot. Record the image digest, database migration level, secret
references, volume identity, file checksums, and the separately owned Qdrant
snapshot reference. Restart only after the backup check succeeds.

### 4. RAG Index Re-sync

1. Open WebUI 문서 관리에서 실패한 인덱스를 식별한다.
2. 문제 문서를 삭제 후 재업로드하여 재인덱싱한다.
3. 필요 시 Qdrant 해당 컬렉션 상태를 점검하고 재동기화한다.

#### 5. Service Restart Path

```bash
docker compose restart ollama
docker compose restart open-webui
```

- 의존 서비스 정상화 후 Open WebUI를 마지막에 재시작한다.

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
  - `open-webui`/`ollama`/`qdrant` 로그 스니펫
  - 수행 명령 및 결과
  - 복구 전후 확인 화면/지표

### Safe Rollback or Recovery Procedure

- [ ] Open WebUI 변경 직후 이상 발생 시 이전 설정으로 되돌린다.
- [ ] 데이터 손상 시 최신 백업 디렉터리에서 DB 복구한다.
- [ ] 재기동 후 최소 기능(로그인/채팅/인덱싱) 확인까지 완료한다.

### Agent Operations (If Applicable)

- **Prompt Rollback**: 최근 프롬프트/설정 변경을 직전 안정 버전으로 복원
- **Model Fallback**: 고부하 모델에서 안정 모델로 임시 전환
- **Tool Disable / Revoke**: 문서 업로드/자동 인덱싱 기능 임시 비활성
- **Eval Re-run**: 기본 채팅 + RAG smoke test 재실행
- **Trace Capture**: 장애 시간대 로그/지표를 증적으로 보존

### Planned isolated restore rehearsal

Status: **planned and not executed**. No successful Open WebUI restore is claimed here.

1. Disable new sessions and ingestion, record image/database versions and identity/chat/upload counts, stop Open WebUI, and create a consistent backup of the whole `/app/backend/data` volume plus the matching auth/OIDC secret references. Obtain the Qdrant snapshot reference from [RUN-0034](../../04-data/0034-qdrant/runbook.md); do not operate on its storage here.
2. Restore the WebUI backup and approved secrets into a separate Compose project/network with no production route. Restore or attach the separately rehearsed Qdrant copy under its owner before RAG verification.
3. Start Open WebUI against isolated Ollama/Qdrant dependencies. Verify schema startup, user and chat counts, uploads, native Keycloak login with `home-openwebui`, disabled password/signup paths, model listing, and one controlled RAG query.
4. On mismatch, stop the isolated project and retain logs/checksums. Return to untouched source backups; production volume, Qdrant, OIDC-client, or route replacement is a separate approved action.

## Evidence

- Capture command output, timestamps, and operator or agent actions for any execution of this runbook.
- Record failed checks, observed symptoms, and the final recovery or escalation state in the related task or incident evidence.

## Rollback or Recovery

- Use only recovery or rollback steps already documented in this runbook, including any `Safe Rollback or Recovery Procedure` subsection above.
- The isolated restore plan above remains unexecuted; attach dated WebUI and Qdrant-owner evidence before marking it rehearsed.
- If the observed failure does not match the documented steps, stop changes, preserve evidence, and escalate under `## Escalation`.

## Escalation

Stop and escalate to the owning operator when verification fails, secret exposure risk appears, destructive data changes are required, or observed state diverges from expected procedure results. Include captured evidence, attempted steps, and current rollback/recovery state.

## Traceability

- Declared parent: [Open WebUI Usage Guide](guide.md) (`GDE-0057`)
- Governing authority: [AI Infrastructure Architecture Description](../../../../02.architecture/descriptions/0008-ai-architecture.md) (`AD-0008`)
- Subject peers: [Guide](guide.md) (`GDE-0057`), [Policy](policy.md) (`POL-0057`)

## Related Documents

- Runtime pins: Compose/Dockerfile declarations are authoritative; the [derived Compose image projection](../../../../../infra/tech-stack.versions.json) provides drift verification.

- [Operations index](../../../README.md)
- [Usage guide](guide.md)
- [Operations policy](policy.md)
