---
status: active
---
<!-- Target: docs/05.operations/guides/11-laboratory/open-notebook.md -->

# Open Notebook Usage Guide

## Usage

### Overview

이 문서는 `open-notebook` 서비스를 사용해 로컬 노트북형 지식 작업 환경에 접근하고, 연결된 SurrealDB 상태를 확인하는 방법을 설명하는 가이드다. 이 서비스는 `11-laboratory` 계층의 관리/실험 도구로 분류되며, 운영 경계와 복구 절차는 별도 operations/runbook 문서를 따른다.
>
> Open Notebook and SurrealDB usage guide for the laboratory management tier.

---

### Usage Type

`how-to | system-guide`

### Target Audience

- Operator
- Developer
- AI Agent

### Purpose

Open Notebook UI에 접속해 개인/로컬 노트북 작업을 수행하고, 서비스가 Traefik, Docker Secrets, SurrealDB 의존성을 통해 정상 동작하는지 확인한다.

### Prerequisites

- `core` 또는 `admin` 실행에 필요한 gateway/SSO 경계가 준비되어 있어야 한다.
- `open_notebook_password`, `open_notebook_encryption_key`, `surreal_db_password` Docker Secret 파일이 준비되어 있어야 한다.
- `SURREALDB_USERNAME`, `SURREALDB_NAMESPACE`, `SURREALDB_DATABASE` 값이 `.env`에 정의되어 있어야 한다.
- `DEFAULT_MANAGEMENT_DIR` 아래 `open-notebook` 및 `surrealdb` 데이터 디렉터리를 쓸 수 있어야 한다.

### Step-by-step Instructions

1. 루트 Compose 진입점에서 `admin` profile이 Open Notebook과 SurrealDB를 렌더링하는지 확인한다.

   ```bash
   HYHOME_COMPOSE_PROFILES=admin bash scripts/validation/validate-docker-compose.sh
   ```

2. 승인된 runtime 환경에서 브라우저로 `https://open-notebook.${DEFAULT_URL}`에 접속한다.
3. 승인된 운영 절차로 전달받은 사용자 credential로 UI 로그인을 확인한다. `open_notebook_password` secret 값 자체는 출력하거나 문서화하지 않는다.
4. 노트북 생성, 검색, 저장 같은 기본 작업을 수행해 `/app/data` 볼륨 쓰기가 정상인지 확인한다.
5. SurrealDB 의존성 문제가 의심되면 `surrealdb` 컨테이너 health 상태와 `SURREAL_*` 환경값을 우선 점검한다.

### Common Pitfalls

- `open_notebook_encryption_key` secret 파일이 비어 있으면 credential 저장 기능이 정상 동작하지 않을 수 있다.
- `SURREAL_URL`은 컨테이너 내부 네트워크 주소인 `ws://surrealdb:8000/rpc`를 사용해야 한다.
- `OPEN_NOTEBOOK_API_URL`은 current host-bound API port 값이고, Traefik 서비스 포트는 `OPEN_NOTEBOOK_WEB_URL` 기본값 `8502`를 사용한다.
- API/SurrealDB host-bound ports는 production-like promotion 전에 방화벽과 접근 경계 evidence를 확인한다.
- `pull_policy: always` 때문에 네트워크가 제한된 환경에서는 이미지 갱신 단계가 실패할 수 있다.

## Common Checks

- `HYHOME_COMPOSE_PROFILES=admin bash scripts/validation/validate-docker-compose.sh`
- `bash scripts/hardening/check-all-hardening.sh 11-laboratory`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../../runbooks/11-laboratory/open-notebook.md)을 따른다.

## Related Documents

- [Operations index](../../README.md)
- [Operations policy](../../policies/11-laboratory/open-notebook.md)
- [Recovery runbook](../../runbooks/11-laboratory/open-notebook.md)
