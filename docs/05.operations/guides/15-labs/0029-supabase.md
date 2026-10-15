---
title: "Supabase Usage Guide"
version: "1.0.8"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-15"
layer: "operations"
artifact_id: "GDE-0029"
parent_ids:
- "POL-0029"
implementation_services:
  labs/supabase.yml:
  - 'analytics'
  - 'auth'
  - 'db'
  - 'functions'
  - 'imgproxy'
  - 'kong'
  - 'meta'
  - 'realtime'
  - 'rest'
  - 'storage'
  - 'studio'
  - 'supavisor'
  - 'vector'
created: "2026-05-10"
---

# Supabase Usage Guide

## Overview

`supabase`는 정상 root에서 분리된 [LAB Compose](../../../../labs/supabase.yml)의
exact `supabase` profile 기반 통합 백엔드 실험 환경이다. 13개 서비스가 PostgreSQL,
Kong, Auth, REST, Realtime, Storage, Studio, Functions, analytics/logging과 pooler를
전용 `hy-home-lab-supabase-core` network에서 구성한다. 이 서비스들은 하나의 recovery
unit이다. database dump만으로는 Storage objects, mounted functions/config,
JWT/provider settings를 복구할 수 없다.

## Scope

### Audience and Goal

Supabase stack을 운영하거나 사용하는 운영자, 개발자, SRE, AI 에이전트를 위한 문서다. 목표는 현재 서비스 구성, 접근 경로, secret 경계, 일반 확인 방법을 이해하는 것이다. Studio에 직접 host port가 있다고 가정하지 않고, compose가 선언한 Kong/API 경로와 운영 runbook을 기준으로 상태를 확인한다.

### SMTP 원본과 소비 경로

공용 SMTP password 원본은 COMM-002 하나입니다. Auth는 공용 `smtp_password`
source를 `/run/secrets/supabase_smtp_password`로 마운트합니다. COMM-003은 값 없는
퇴역 ID이며 별도 파일이나 OpenBao KV 값을 생성하지 않습니다. 향후 OpenBao 전환도
canonical entry 하나와 서비스별 필요한 render를 사용합니다.

GoTrue SMTP `_FILE`은 source wrapper가 처리하고 원래 user·명령·argv를 보존합니다.
값은 실행 프로세스 환경에만 전달되므로 Docker/호스트 관리자와 환경 접근 위험을
관리해야 합니다. SMTP의 격리 capture·인증 결과와 DB/JWT/전체 platform readiness는
다른 증거입니다. LAB source 이동은 11개 secret 파일을 읽거나 이동·복제·삭제하지
않았고 현재 Supabase 비선택 상태를 바꾸어 전체 stack을 가동하지 않았습니다.

## Concepts

### Current implementation

| 항목 | 이 저장소의 구현 결정 |
| --- | --- |
| Project | `hy-home-lab-supabase` |
| Services | `analytics`, `auth`, `db`, `functions`, `imgproxy`, `kong`, `meta`, `realtime`, `rest`, `storage`, `studio`, `supavisor`, `vector` |
| Consumer and data rationale | PostgreSQL, Auth, API, Realtime, object, function, pooling을 격리 검증하는 독립 LAB. 현재 이름 있는 production consumer는 없다. |
| Source / updater | [Compose](../../../../labs/supabase.yml)가 13개 이미지 선언을 소유하며, 조율된 upstream 호환성 검토가 필요하다. |
| Services / profile | frontmatter에 매핑된 13개 서비스; exact `supabase`. |
| Flow / dependency | Kong이 API 경로 앞단에 있고, PostgreSQL이 메타데이터/데이터 코어이며, Storage가 메타데이터를 object 파일과 결합하고, Supavisor가 데이터베이스 트래픽을 pooling한다. |
| Exposure / persistence | Kong/analytics/Supavisor host port는 `LAB_SUPABASE_*` 변수로 loopback에 게시되며, Studio는 직접 포트가 없고, `${LAB_DATA_DIR}/supabase`가 data/config를 소유한다. |
| Environment / secrets | 공개 입력은 `labs/.env`의 `LAB_*` 계약을 사용한다. 11개 secret declaration은 기존 canonical root 파일을 참조하며 값을 LAB로 복사하지 않는다. SMTP는 COMM-002 한 원본이다. |
| Health / resources | 서비스별 healthcheck와 의존성 그래프; 각 서비스는 Compose에 선언된 공유 템플릿을 사용하므로 총 용량을 검토해야 한다. |
| Security | Kong 경계, secret mount, JWT/provider 일관성, 생성된 증거에 credential 자료가 없어야 함. |
| Backup / upgrade | PostgreSQL + Storage + config/functions + Auth/secret reference가 하나의 recovery set을 이루며, upstream update config backup만으로는 부족하다. |
| License / edition | self-hosted stack은 저장소에 문서화된 라이선스를 가진 구성 요소를 결합하므로, 재배포나 managed-service 사용 전에 정확한 구성 요소/이미지 집합을 검토해야 한다. |

## Usage

### Identity-specific behavior

13 개 image tag 는 독립 선택이며 upstream-tested bundle 로 확인되지 않았다. db 의 pg_isready 외 process `kill -0 1` health 는 API/auth/migration 성공을 뜻하지 않는다. Compose `_FILE` 선언은 image 가 이를 처리한다는 증거가 아니다. auth/rest/realtime/storage/meta/analytics/supavisor 의 DB/JWT/config wiring, Kong temp.yml 의 실제 loader, edge-runtime function serve command, pooler.exs 적용은 source 만으로 완결되지 않는다. private host files 는 미열람이며 secret-safe adapter/config 검증 전 operational acceptance 는 중단한다. host5432/6543 은 supavisor 이고 db 직접 게시가 아니다. storage files 와 DB metadata 는 같은 recovery point 로 보존한다. vector 의 ro Docker socket 도 Docker API 접근 권한이므로 read-only 파일 표기만으로 무해하지 않다.

| 정확한 식별자 | 목적·상태·기동 차이 | 준비 상태 판단의 한계 | 구현 소유자 |
| --- | --- | --- | --- |
| `analytics` | Logflare; mounted config/DB 입력 수용 미검증 | process 생존만; API/auth/DB readiness 미증명 | [선택·의존·접속·입력·mount](../../../../labs/supabase.yml) |
| `auth` | Auth/JWT; DB/secret 입력 수용 미검증 | process 생존만; API/auth/DB readiness 미증명 | [선택·의존·접속·입력·mount](../../../../labs/supabase.yml) |
| `db` | Supabase PG; 자체 database data/init/config | PG 연결 수락; SQL 권한/업무 정합성 별도 | [선택·의존·접속·입력·mount](../../../../labs/supabase.yml) |
| `functions` | edge runtime; mounted functions serve command 미완결 | process 생존만; API/auth/DB readiness 미증명 | [선택·의존·접속·입력·mount](../../../../labs/supabase.yml) |
| `imgproxy` | 이미지 변환; local source backend 설정 미검증 | process 생존만; API/auth/DB readiness 미증명 | [선택·의존·접속·입력·mount](../../../../labs/supabase.yml) |
| `kong` | API gateway; mounted temp config의 loader 미검증 | process 생존만; API/auth/DB readiness 미증명 | [선택·의존·접속·입력·mount](../../../../labs/supabase.yml) |
| `meta` | PG metadata API; DB/secret 입력 수용 미검증 | process 생존만; API/auth/DB readiness 미증명 | [선택·의존·접속·입력·mount](../../../../labs/supabase.yml) |
| `realtime` | Realtime; DB/migration/secret 입력 수용 미검증 | process 생존만; API/auth/DB readiness 미증명 | [선택·의존·접속·입력·mount](../../../../labs/supabase.yml) |
| `rest` | PostgREST API; DB/secret 입력 수용 미검증 | process 생존만; API/auth/DB readiness 미증명 | [선택·의존·접속·입력·mount](../../../../labs/supabase.yml) |
| `storage` | Storage API; object files와 DB metadata 동시 보존 | process 생존만; API/auth/DB readiness 미증명 | [선택·의존·접속·입력·mount](../../../../labs/supabase.yml) |
| `studio` | 관리 UI; 직접 host publication 없음 | process 생존만; API/auth/DB readiness 미증명 | [선택·의존·접속·입력·mount](../../../../labs/supabase.yml) |
| `supavisor` | session/transaction pooler; host SQL publication 소유 | process 생존만; API/auth/DB readiness 미증명 | [선택·의존·접속·입력·mount](../../../../labs/supabase.yml) |
| `vector` | log collector; Docker socket API 권한과 private config | process 생존만; API/auth/DB readiness 미증명 | [선택·의존·접속·입력·mount](../../../../labs/supabase.yml) |

선택 profile, version, port, 환경 입력, secret identifier와 mount의 정확한 값은 각 행의 구현이 소유한다. [공통 template](../../../../infra/common-optimizations.yml)의 resource·security 상속과 서비스 override를 함께 읽는다. 값의2026-10-01 source snapshot과 official version/build 검토는 [W4 Task](../../../98.archive/completed/03.specs/0198-operations-documentation-system/tasks/tsk-0004-data-messaging-analytics.md)에 보존했다. 반복OOM, disk/WAL/checkpoint 증가와 metrics 누락은 capacity 검토 trigger이며 health는 사용자 기능이나 복원을 증명하지 않는다.

### 사전 조건과 사용

현재 source의 `_FILE`/DB URL/config loader/start command 수용은 image별로 미완결·미검증이다. named secret 파일이 있다는 이유만으로 정상 구성이라 판단하지 않는다. 별도 source 수정과13개 기능 경로의 격리 검증 전 운영 활성화/복구 승격은 중단한다.

- 프로젝트 루트에 저장소가 checkout되어 있어야 한다.
- 로컬 또는 승인된 인프라 host에서 Docker Compose에 접근할 수 있어야 한다.
- `LAB_DATA_DIR`가 HOME data root와 겹치지 않는 격리 경로를 가리키고, 필요한
  Supabase config, storage, function, log, database 입력이 준비되어 있어야 한다.
- `LAB_SECRETS_GID`와 `LAB_SUPABASE_*` 공개 입력은 비공개 `labs/.env`에 두며,
  [공개 예시](../../../../labs/supabase/.env.example)에 secret 값을 추가하지 않는다.
- stack이 참조하는 Docker Secret 파일이 준비되어 있어야 하며, secret 값을 문서, 로그, 커밋에 복사해서는 안 된다.

1. controller의 정적 preflight로 현재 LAB surface를 확인한다. 이 명령은 service를
   시작하지 않는다.

   ```bash
   python3 scripts/operations/lab.py check supabase
   ```

   기대 서비스: `studio`, `kong`, `auth`, `rest`, `realtime`, `storage`, `imgproxy`, `meta`, `functions`, `analytics`, `db`, `vector`, `supavisor`.

2. 공개 접근 경로를 확인한다.

   - 아래 host port는 모두 `127.0.0.1`에만 게시된다.
   - Kong HTTP: `${LAB_SUPABASE_KONG_HTTP_HOST_PORT:-8000}:8000/tcp`
   - Kong HTTPS: `${LAB_SUPABASE_KONG_HTTPS_HOST_PORT:-8443}:8443/tcp`
   - Analytics: `${LAB_SUPABASE_ANALYTICS_HOST_PORT:-4000}:4000`
   - Supavisor session/transaction pooler: `${LAB_SUPABASE_POSTGRES_HOST_PORT:-5432}:5432`, `${LAB_SUPABASE_POOLER_PROXY_PORT_TRANSACTION_HOST_PORT:-6543}:6543`
   - Studio는 현재 compose 파일에 직접 host port가 없으므로, Kong과 stack 구성이 노출하는 승인된 경로를 사용한다.

3. 서비스 상태와 lease는 [RUN-0029 절차](../../runbooks/15-labs/0029-supabase.md#procedure)의
   `lab.py status` 확인을 따른다. 실제 기동은 승인된 목적과 제한된 lease가 있을 때만
   controller를 사용한다.

4. 데이터와 config 경계를 확인한다.

   Supabase runtime 파일은 `${LAB_DATA_DIR}/supabase/...`에서 마운트되며,
   Kong config, storage, functions, database init SQL, logs, pooler config를
   포함한다. 이 mount가 바뀌면 구현 문서와 운영 문서를 함께 갱신한다.

5. recovery inventory는 PostgreSQL roles/schema/data, Storage metadata와 object files, mounted Kong/functions/pooler configuration, Auth/JWT/SMTP/provider settings를 별도 protected artifacts로 기록한다. 빈 격리 stack에서 이들을 coherent set으로 복원한 뒤에만 recoverable로 판정한다.

### 주의점

- Studio가 직접 local host port로 접근 가능하다고 가정하는 것 — 현재 compose 파일은 그런 포트를 게시하지 않는다.
- 승인된 구현 변경 없이 공개 API 접근에서 Kong을 우회하는 것.
- `supabase_anon_key`, `supabase_service_key`, JWT secret, dashboard credential, SMTP 비밀번호, 데이터베이스 비밀번호를 문서나 증거에 기록하는 것.
- 생성된 Kong 또는 데이터베이스 config를 문서 전용 상태로 취급하는 것 — 이 config는 `${LAB_DATA_DIR}`에서 마운트되는 runtime 구성이다.
- 정상 root의 `docker compose --profile supabase`로 이 LAB를 선택할 수 있다고
  가정하거나 controller를 우회해 기동하는 것.
- self-hosted update config backup을 데이터베이스나 Storage backup으로 사용하는 것 — upstream 문서는 update backup을 구성 전용으로만 설명한다.

### Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은
[recovery runbook](../../runbooks/15-labs/0029-supabase.md)을 따른다.

### Traceability

- Declared parent: [Supabase Operations Policy](../../policies/15-labs/0029-supabase.md) (`POL-0029`)
- Governing authority: [Data Tier (04-data) Architecture Description](../../../02.architecture/descriptions/0004-data-architecture.md) (`AD-0004`)
- Subject peers: [Policy](../../policies/15-labs/0029-supabase.md) (`POL-0029`), [Runbook](../../runbooks/15-labs/0029-supabase.md) (`RUN-0029`)

## Troubleshooting

### Common Checks

- `python3 scripts/operations/lab.py check supabase`
- `python3 scripts/operations/lab.py status`
- 커밋 전에 짝을 이루는 guide/policy/runbook에서 직접 Studio host-port 가정, 오래된 Compose CLI 표기, template copyright 잔재를 검색한다.
- 기대 결과: compose가 렌더링되고, 서비스가 compose 파일과 일치하며, 오래된 Studio/직접 포트 또는 template 잔재가 없다.

## Related Documents

- [Supabase self-hosted restore guidance](https://supabase.com/docs/guides/self-hosting/restore-from-platform)
- [Supabase self-hosted update guidance](https://supabase.com/docs/guides/self-hosting/updating)
- [Supabase source and licenses](https://github.com/supabase/supabase)

- [Operations index](../../README.md)
- [Operations policy](../../policies/15-labs/0029-supabase.md)
- [Recovery runbook](../../runbooks/15-labs/0029-supabase.md)
- [Supabase LAB source README](../../../../labs/supabase/README.md)
- [Compose implementation: labs/supabase.yml](../../../../labs/supabase.yml)
