---
title: "Open Notebook Usage Guide"
version: "1.1.7"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-11-14"
layer: "operations"
artifact_id: "GDE-0073"
parent_ids:
- "POL-0073"
implementation_services:
  infra/08-ai/open-notebook/docker-compose.yml:
  - open_notebook
created: "2026-05-10"
next_review_at: "2027-05-13"
---

# Open Notebook Usage Guide

## Purpose

### Outcome

Open Notebook은 OPTIONAL 노트북 지식 워크스페이스이다. `open_notebook` 서비스는
오직 `notebook`에만 속한다. 소유자 커밋 `d5912ab03`가 이를 포괄 `admin` selector에서
제거했으며 HOME에서도 제외된다. 이 서비스의 `surrealdb` 의존성은 같은
[Open Notebook Compose](../../../../infra/08-ai/open-notebook/docker-compose.yml)에
함께 들어 있고 같은 selector를 공유하며 영속 데이터베이스를 제공한다.

Laboratory Operator와 `@buenhyden`이 OPTIONAL 노트북 워크스페이스를 `notebook` selector로 켜고 쓰는 경우를 다룬다. 목표는 승인된 비밀번호와 허용된 모델/provider만으로 노트북을 사용하고, 데이터·키·이미지 한계를 알고 운영하는 것이다.

### Boundaries

- [Policy](../../policies/09-ai-and-search/0073-open-notebook.md) (`POL-0073`)
- [Runbook](../../runbooks/09-ai-and-search/0073-open-notebook.md) (`RUN-0073`)
- [Laboratory architecture](../../../02.architecture/descriptions/0011-laboratory-architecture.md)

- [Open Notebook security and encryption-key custody](https://github.com/lfnovo/open-notebook/blob/main/docs/5-CONFIGURATION/security.md)
- [Open Notebook deployment](https://github.com/lfnovo/open-notebook/blob/main/README.md)
- [SurrealDB backups and recovery](https://surrealdb.com/docs/manage/self-hosted/backups-and-recovery)

## Prerequisites

### Environment

#### 현재 구현과 데이터

- [Open Notebook Compose](../../../../infra/08-ai/open-notebook/docker-compose.yml)가
  app 서비스, 라우트, app-data 볼륨, secret, healthcheck를 정의한다.
- `/app/data`는 애플리케이션 파일을 저장한다. SurrealDB `/mydata`는 노트북, 소스,
  모델/provider 설정, 암호화된 provider credential을 저장한다.
- 현재 운영 계약은 SurrealDB v2로 제한한다. 선택한 Open Notebook 이미지와의
  v3 호환성은 검증되지 않았으므로 v3 전환을 지원한다고 추정하지 않는다.
- `open_notebook_password`, `open_notebook_encryption_key`, `surreal_db_password`는
  Docker secret이다. 업스트림은 암호화 키를 잃어버리거나 변경하면 이전에 암호화된
  API 키를 읽을 수 없게 된다고 명시한다. 키는 데이터베이스 백업과 분리해서
  보관한다.
- API 호스트 포트는 `127.0.0.1`에만 바인딩된다. 브라우저는 Traefik을 거쳐 웹
  포트에 도달한다. UI 라우트는 admin CIDR 허용목록과 Open Notebook 비밀번호를
  사용한다. 소유자 커밋 `b90b74837`가 공유 SSO를 제거했으므로 이 라우트에는
  게이트웨이 identity나 그룹 검사가 적용되지 않는다.
- API `5055`의 `/health`는 제한된 앱 API 생존·기동 상태만 확인한다. DB 마이그레이션,
  provider·모델 준비, 저장된 모델 등록과 노트북 기능은 별도 증거가 필요하다. 디렉터리
  health 역시 마운트 가용성만 증명한다.

### Permissions

필요한 Docker secret은 `open_notebook_password`, `open_notebook_encryption_key`, `surreal_db_password`이며 값은 기록하지 않는다. UI 라우트는 admin CIDR 허용목록과 Open Notebook 앱 비밀번호를 사용한다. 자세한 내용은 Environment의 현재 구현과 데이터에 있다.

## Procedure

### Actions

#### 일반적인 사용, 백업, 업그레이드

실행 순서와 실패·복구 판단은 [런북](../../runbooks/09-ai-and-search/0073-open-notebook.md)의 `승인된 사용과 일관된 복구 세트` 절차를 따른다. 데이터와 권한 경계는 해당 정책을 유지한다.

### Exceptions

#### 정상 사용과 이미지 한계

승인된 비밀번호로 노트북·소스를 선택하고 허용된 모델/provider만 사용한다.
`open_notebook`은 SurrealDB health를 기다리지만 선택적 Ollama URL에 readiness
의존성은 없다. 앱은 `edge_net`·`ai_net`, DB는 `ai_net`에 연결된다. source의
secret 파일 선언과 shell의 환경변수 전달은 실제 이미지의 모든 FILE 옵션 지원·암호화
동작을 증명하지 않는다. 앱 이미지는 Compose에서 tag와 digest로 고정하지만 `pull_policy: always`를 쓴다. DB는 고정된
SurrealDB v2 binary를 [로컬 Dockerfile](../../../../infra/08-ai/open-notebook/surrealdb/Dockerfile)이 digest 없는 `debian:bookworm-slim` 위에 복사해 빌드한다.
선택한 이미지 식별자·호환성·자격 증명 복호화 결과를 별도 승인된 검증으로 확인한다.
자원·마운트 설정은 Compose가 소유하며 프로필 분리가 물리적 격리를 뜻하지 않는다.

#### P03 모델 등록 경계

P03의 현재 로컬 source 계약은 `gemma4:e2b` chat과
`embeddinggemma-2:740m` 768차원 embedding 후보를 지정한다. 이는 모델 다운로드,
Ollama 추론, provider credential, Notebook 저장 등록 또는 사용자 기능 수용 결과가
아니다. `OLLAMA_API_BASE` 같은 환경 fallback은 저장된 Provider/Credential/Model
등록 증거로 쓰지 않는다.

지원되는 UI/API로 등록할 때에는 기존 provider, credential과 동일한 모델 연결만
반복 실행할 수 있다. 다른 credential에 연결된 동명 모델, 중복 레코드 또는 변경된
사전 상태는 거부하고 전체 provider 동기화나 기존 등록 삭제 후 재생성을 하지 않는다.
embedding 작업은 terminal job 상태와 저장된 model association을 별도로 확인해야 하며,
취소 응답·`/health`·SurrealDB health는 그 증거가 아니다.

## Verification

### Expected Result

- `docker compose --profile notebook config --quiet`
- `docker compose --profile notebook config --services`
- `bash scripts/hardening/check-all-hardening.sh 08-ai`

### Troubleshooting

- `open_notebook`이 기동하지 않으면 `surrealdb` health를 먼저 확인한다. 앱은 DB가 healthy가 된 뒤에만 시작한다.
- 저장된 provider key를 읽을 수 없으면 쓰기를 멈추고 [runbook](../../runbooks/09-ai-and-search/0073-open-notebook.md)의 진단 절차를 따른다. 암호화 키를 새 값으로 덮어쓰지 않는다.

#### Runbook Handoff

데이터베이스/키/provider 복구와 업그레이드에는
[runbook](../../runbooks/09-ai-and-search/0073-open-notebook.md)을 사용한다.

복구 수용에는 동일한 SurrealDB 데이터, 앱 SQLite 상태와 대응하는
`open_notebook_encryption_key`가 함께 필요하다. API가 null 기본값 복원을 지원한다고
가정하지 않으며, 실제 복구는 별도 승인된 격리 절차의 증거가 있을 때만 기록한다.
