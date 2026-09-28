---
title: "Open Notebook Usage Guide"
version: "1.1.1"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "GDE-0073"
parent_ids:
- "POL-0073"
implementation_services:
  infra/11-laboratory/open-notebook/docker-compose.yml:
  - open_notebook
created: "2026-05-10"
---

# Open Notebook Usage Guide

## Usage

### 목적과 분류

Open Notebook은 OPTIONAL 노트북 지식 워크스페이스이다. `open_notebook` 서비스는
오직 `notebook`에만 속한다. 소유자 커밋 `d5912ab03`가 이를 포괄 `admin` selector에서
제거했으며 HOME에서도 제외된다. 이 서비스의 `surrealdb` 의존성은 같은
[Open Notebook Compose](../../../infra/11-laboratory/open-notebook/docker-compose.yml)에
함께 들어 있고 같은 selector를 공유하며 영속 데이터베이스를 제공한다.

### 현재 구현과 데이터

- [Open Notebook Compose](../../../infra/11-laboratory/open-notebook/docker-compose.yml)가
  app 서비스, 라우트, app-data 볼륨, secret, healthcheck를 정의한다.
- `/app/data`는 애플리케이션 파일을 저장한다. SurrealDB `/mydata`는 노트북, 소스,
  모델/provider 설정, 암호화된 provider credential을 저장한다.
- `open_notebook` 업스트림은 SurrealDB v2를 엄격히 요구한다. SurrealDB v3는
  호환되지 않으며 지원 대상도 아니다.
- `open_notebook_password`, `open_notebook_encryption_key`, `surreal_db_password`는
  Docker secret이다. 업스트림은 암호화 키를 잃어버리거나 변경하면 이전에 암호화된
  API 키를 읽을 수 없게 된다고 명시한다. 키는 데이터베이스 백업과 분리해서
  보관한다.
- API 호스트 포트는 `127.0.0.1`에만 바인딩된다. 브라우저는 Traefik을 거쳐 웹
  포트에 도달한다. UI 라우트는 admin CIDR 허용목록과 Open Notebook 비밀번호를
  사용한다. 소유자 커밋 `b90b74837`가 공유 SSO를 제거했으므로 이 라우트에는
  게이트웨이 identity나 그룹 검사가 적용되지 않는다.
- 디렉터리 health는 마운트 가용성만 증명할 뿐 DB, provider, 모델, 노트북 기능은
  증명하지 않는다.

### 일반적인 사용, 백업, 업그레이드

`docker compose --profile notebook config --quiet`로 검증하고, 두 서비스를 모두
확인한 다음 app보다 먼저 데이터베이스를 시작한다. 애플리케이션 비밀번호와
게이트웨이 통제를 함께 사용한다. 승인된 모델/provider endpoint와 키만 구성한다.
노트북 콘텐츠, 소스 문서, embedding, provider 키는 민감 정보이다. SurrealDB는
v2로 유지하고 v3로 업그레이드하지 않는다.

백업할 때는 app write를 멈추고 `surreal export`로 구성된 SurrealDB
namespace/database를 export하고 `/app/data`를 복사하고 암호화 키와 DB
credential을 보호된 방식으로 보관한다. provider/network egress를 비활성화한
격리된 SurrealDB로 복원하고 export를 import하고 app data를 마운트하고 같은
암호화 키를 비공개로 제공한 다음, 개수와 합성 노트북 하나를 검증한다. 업그레이드
전에는 floating-tag/release 변경 사항을 검토하고 이 복원을 테스트한다. 여기서는
백업, 복원, provider 호출, 업그레이드를 실행하지 않았다.

## Common Checks

- `docker compose --profile notebook config --quiet`
- `docker compose --profile notebook config --services`
- `bash scripts/hardening/check-all-hardening.sh 11-laboratory`

## Runbook Handoff

데이터베이스/키/provider 복구와 업그레이드에는
[runbook](../runbooks/0073-open-notebook.md)을 사용한다.

## Traceability

- [Policy](../policies/0073-open-notebook.md) (`POL-0073`)
- [Runbook](../runbooks/0073-open-notebook.md) (`RUN-0073`)
- [Laboratory architecture](../../02.architecture/descriptions/0011-laboratory-architecture.md)

## Related Documents

- [Open Notebook security and encryption-key custody](https://github.com/lfnovo/open-notebook/blob/main/docs/5-CONFIGURATION/security.md)
- [Open Notebook deployment](https://github.com/lfnovo/open-notebook/blob/main/README.md)
- [SurrealDB backups and recovery](https://surrealdb.com/docs/manage/self-hosted/backups-and-recovery)
