---
title: "n8n 워크플로 자동화"
version: "1.2.15"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-26"
created: "2025-11-12"
---

# n8n 워크플로 자동화

## Overview

n8n은 시각적 인터페이스로 워크플로우 자동화를 구현하는 로우코드 도구이다. 복잡한 Airflow DAG와 달리 직관적인 노드 연결로 API 통합, 웹후크 처리, 이벤트 기반 자동화를 빠르게 배포할 수 있다.

2026-10-04 확인한 [선정 버전의 공식 LICENSE](https://github.com/n8n-io/n8n/blob/f5da43d99f6599a24574206f922625dcabfd4de0/LICENSE.md)는
일반 소스에 Sustainable Use License, Enterprise 부분에 별도 조건을 적용합니다.
무료 내부 자체 호스팅과 무제한 오픈소스·외부 제공 권한을 동일하게 취급하지 않습니다.

## Audience

이 README의 주요 독자:

- Workflow Operators
- Integration Developers
- AI Agents

## Scope

### In Scope

- n8n 메인 서비스, worker, task runner, 메타데이터 DB, queue 모드 compose 연결
- 비밀이 아닌 환경 변수와 런타임 토폴로지 노트
- 정식 가이드, 정책, 런북, 워크플로우 스펙으로의 연결

### Out of Scope

- Airflow DAG 작성 및 스케줄러 운영
- n8n 자격 증명 값, 워크플로우 시크릿, 내보낸 비공개 워크플로우 데이터
- 서드파티 SaaS 계정 설정

## Structure

```text
n8n/
├── Dockerfile
├── dev.Dockerfile
├── docker-compose.yml  # n8n, worker, task runner, and queue wiring
├── docker-compose.ollama-local.yml # 선택형 Worker/Ollama internal 망
├── docker-entrypoint*.sh
├── custom/
└── README.md           # This file
```

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | n8n Low-code Automation 서비스 leaf. [root docker-compose.yml](../../../docker-compose.yml) -> `infra/07-workflow/n8n/docker-compose.yml` 경로로 루트 include가 활성화됨. 선택형 Ollama overlay는 root include 밖에서 명시적으로 결합함 |
| Config files | `docker-compose.yml`, `docker-compose.ollama-local.yml` |
| Config values | env 키: `GENERIC_TIMEZONE`, `TZ`, `DB_TYPE`, `DB_POSTGRESDB_HOST`, `DB_POSTGRESDB_PORT`, `DB_POSTGRESDB_DATABASE`, `DB_POSTGRESDB_USER`, `DB_POSTGRESDB_PASSWORD_FILE` 외 다수; 프로필: `workflow`, `workflow-n8n` |
| Compose linkage | [root docker-compose.yml](../../../docker-compose.yml) -> `infra/07-workflow/n8n/docker-compose.yml` 경로로 무조건 루트 include되며 프로필(`workflow`, `workflow-n8n`)로 선택됨 |
| Networks | `edge_net`, `mng_data_net`, `n8n_net`, `obs_net` |
| Volumes | `n8n-data:/home/node/.n8n:rw`, `./custom:/home/node/.n8n/custom:ro`, `n8n-task-runner-worker-data:/home/node/.n8n:rw`, `n8n-data`, `n8n-task-runner-data`, `n8n-task-runner-worker-data`, `n8n-valkey-data:/data:rw`, `n8n-valkey-data` |
| Ports | `${N8N_PORT:-5678}`, `${N8N_BROKER_PORT:-5679}`, `${N8N_TASK_RUNNER_PORT:-5680}`, `${VALKEY_PORT:-6379}`, `${VALKEY_BUS_PORT:-16379}`, `${VALKEY_EXPORTER_PORT:-9121}`. `N8N_BROKER_PORT`는 main·worker의 `N8N_RUNNERS_BROKER_PORT`로, `N8N_TASK_RUNNER_PORT`는 두 runner의 `N8N_RUNNERS_LAUNCHER_HEALTH_CHECK_PORT`로 전달되어 URI·expose·healthcheck와 실제 listener가 같은 값을 씁니다 |
| Labels | `hy-home.tier`, `traefik.enable`, `traefik.http.routers.n8n.rule`, `traefik.http.routers.n8n.entrypoints`, `traefik.http.routers.n8n.middlewares`, `traefik.http.routers.n8n.tls`, `traefik.http.routers.n8n.service`, `traefik.http.services.n8n.loadbalancer.server.port` |
| Secret refs | main/worker는 선택된 `mng_valkey_password`, `mng_valkey_n8n_password` 또는 `n8n_valkey_password` 하나와 `n8n_db_password`, `n8n_encryption_key`, `n8n_runner_auth_token`을 마운트함. runner 둘은 `n8n_runner_auth_token`만 마운트함 |
| Healthcheck | `n8n`, `n8n-worker`, `n8n-task-runner`, `n8n-task-runner-worker`, `dedicated-valkey` 프로필의 `n8n-valkey`에 Compose 헬스체크가 선언되어 있음. exporter는 의존성 기반으로 게이트됨. main은 `/healthz/readiness`, worker·runner는 각 선언된 `/healthz`를 사용하며 같은 신호가 아님; probe 통과가 작업 실행 성공이나 runner 호환성을 입증하지 않음 |
| Operations | 아래 Related Documents의 Guide·Policy·Runbook 탐색점에서 `GDE-0053`·`POL-0053`·`RUN-0053`을 선택합니다. |
| Validation | [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh); [run-ci-gate.py](../../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | `HYHOME_COMPOSE_PROFILES='workflow-n8n' bash scripts/validation/validate-docker-compose.sh`로 시작한 뒤 서비스 로그와 연결된 런북 근거를 확인합니다. |

## Usage

공통 실행 및 문서 규칙은 [공통 Agent 거버넌스 agentic governance](../../../.agents/governance/agentic.md)와 [documentation protocol](../../../.agents/governance/documentation-protocol.md)을 따른다.

1. n8n 설정을 변경하기 전에 연결된 운영 가이드, 정책, 런북을 검토합니다.
2. 외부 자격 증명은 n8n의 암호화된 Credentials 시스템이나 Docker Secrets에 보관합니다.
3. 통합을 추가하기 전에 간단한 로우코드 자동화와 Airflow가 소유하는 DAG 워크플로우를 구분합니다.
4. compose나 queue 모드를 변경한 뒤에는 아래 검증 명령을 실행합니다.
5. 병렬 워크로드를 변경할 때는 `EXECUTIONS_MODE: queue` 동작을 염두에 둡니다.

6. **Modularization**: 복잡한 로직은 `Sub-workflows`로 분리해 재사용성을 확보하십시오.
7. **Credential Safety**: 모든 외부 인증 정보는 n8n 내부의 `Credentials` 시스템에 암호화되어 저장되어야 하며 `docker-compose.yml`의 시크릿(`secrets`)으로 안전하게 공급됩니다.

## Tech Stack

| Component | Technology | Version | Note |
| :--- | :--- | :--- | :--- |
| Core Service | n8n | declared version | Node.js 기반 |
| Metadata DB | PostgreSQL | Management PostgreSQL | `infra/04-data/mng-db`를 통해 관리됨 |
| Queue Broker | Valkey (Redis 호환) | 선택은 `${N8N_VALKEY_HOST:-mng-valkey}`와 `${N8N_VALKEY_SECRET:-mng_valkey_password}`가 소유함; `dedicated-valkey`는 전용 broker를 활성화할 뿐 main/worker의 host·secret을 바꾸지 않음 | Queue 오케스트레이션 |
| Task Runner | n8nio/runners | declared version | 격리된 실행 환경 |

## Architecture

n8n 환경은 고성능과 확장성을 위해 분산 모드로 구성된다:

- **Main Service**: UI 제공 및 워크플로우 관리.
- **Worker**: 실제 태스크 실행 담당 (Valkey 큐 기반).
- **Task Runner**: 특정 복잡한 태스크를 격리된 환경에서 안전하게 처리.
- **Valkey**: 워커 간 작업 분배를 위한 메시지 브로커.

### 선택형 공유 계정과 Ollama 실행 경로

기본 broker는 기존 default 계정·DB0이며 신규 비밀 파일을 요구하지 않습니다.
`SHARE_NAMED_USER`는 MNG의 typed ACL overlay와 `N8N_VALKEY_USERNAME=n8n`,
`N8N_VALKEY_SECRET=mng_valkey_n8n_password`, 기존 host·DB0를 함께 선택합니다.
두 entrypoint는 Host/User/Secret/DB와 실제 Queue 변수가 같은지 검사하고 혼합 입력을
거부합니다. 전용 Valkey의 username 없는 기존 pair도 유지합니다. 설정이 준비됐다는
사실은 실제 Bull queue의 인증·Retry·복원 인수가 아닙니다.

[`docker-compose.ollama-local.yml`](docker-compose.ollama-local.yml)은 실제 실행자인
`n8n-worker`와 `ollama`만 새 `internal:true` 망에 추가합니다. Main/Code Runner에는
추가 망을 주지 않습니다. 기존 Ollama `edge_net`/`ai_net` peer 접근은 유지되므로
이 overlay를 전체 API 격리라고 표현하지 않습니다. 저장된 Ollama Credential·Node
실행과 거부·복구는 별도이며 Cloud 호출·fallback은 추가하지 않습니다.
정확한 선택과 인수 절차는
[워크플로와 자동화 런북 목록](../../../docs/05.operations/runbooks/08-workflows-and-automation/README.md)의
n8n Runbook 「선택형 공유 Valkey 계정과 Local Ollama」 절이 소유합니다.

## Traceability (Golden 5)

- **PRD**: 07-workflow PRD (`docs/01.requirements/0008-workflow.md`)
- **ARD**: 07-workflow Architecture Description (`docs/02.architecture/descriptions/0007-workflow-architecture.md`)
- **ADR**: N8N Integration ADR (`docs/02.architecture/decisions/0007-airflow-n8n-hybrid-workflow.md`)
- **Plan**: [Spec Package 탐색](../../../docs/03.specs/README.md)의 SPEC-0204 Task0017이 이번 버전 소스 준비를 담당합니다.

## Validation

- README나 n8n에 영향을 주는 Compose 참조 변경 후에는 `HYHOME_COMPOSE_PROFILES='workflow-n8n' bash scripts/validation/validate-docker-compose.sh`를 실행합니다.
- n8n 문서를 준비 완료로 표시하기 전에 `bash scripts/hardening/check-all-hardening.sh`를 실행합니다.

### SEC01 안정판 묶음

2026-10-16 KST [공식 릴리스](https://github.com/n8n-io/n8n/releases/tag/n8n%402.43.6), <!-- runtime-version-exception: compatibility — immutable source evidence reference; Compose/Dockerfile owns the deployment pin -->
[npm stable 배포](https://registry.npmjs.org/n8n/latest)와 Docker stable/latest channel의 OCI index를 대조했습니다.
요청에 인용된 이전 안정판 다음으로 발표된 패치는 webhook 요청마다 XML parser를 생성하도록 수정합니다.
공식 index·amd64 manifest·config descriptor의 digest를 각각 구분해 장부에 기록했습니다.
main·worker와 두 task runner를 같은 vendor stable로 맞추고 두 custom Dockerfile의 base·font builder
OCI index digest를 고정합니다. platform manifest·custom build image ID·실제 running digest는 별도 증거입니다.
fontconfig·Noto·DejaVu·Liberation·emoji 패키지는 조회한 Alpine 안정 채널의 명시 버전으로 설치합니다.
폐기된 `ttf` alias 대신 유지되는 font package를 사용하고, 최종 이미지의
`/usr/share/hy-home-font-builder-packages.txt`에 실제 설치 목록을 보존합니다.

UNIT의 네 role 정합 검사는 native workflow import·실행이나 HOME 배포를 입증하지 않습니다.
deprecated node import 거부·JSON typeVersion·webhook·Code runner·queue·PostgreSQL·SMTP·실패 경로는 NOT_RUN입니다.
Opsflow custom node의 peer/dev API와 lock도 upstream 본체가 사용하는 버전에 정렬했습니다.
Task0017의 고정 입력으로 빌드한 production 이미지와 실제 PackageDirectoryLoader의 custom node
등록·동일 base peer 해석·font 검사는 ISOLATED PASS입니다. dev recipe는 별도로 빌드하지
않았습니다. 후속 전체 시험도 main readiness에서 ERROR였고 migration 완료와 cleanup
PASS까지만 확인했습니다. fixture의 mount·alias·user-folder를 맞췄으며 production
entrypoint·이미지는 바꾸지 않았습니다. SMTP·runner 업무는 미검증이고 서명·SBOM·
full-image scan·HOME 수용은 NOT_RUN입니다.
Wiki 예약이나 실제 Wiki 소비자는 이 업데이트에 추가하지 않습니다.

HOME 전환 전 MNG DB와 n8n data, 동일 encryption key의 독립 보관, queue/진행 중 실행의
중단·재개 경계를 확인합니다. 새 schema migration 후 rollback은 사전 DB·data 백업을
빈 이전 이미지 환경에 복원해야 하며 이미지 태그 변경만으로 DB 복구를 주장하지 않습니다.
실제 backup·15분 중단 한도·복원·HOME 전환은 NOT_RUN이며 총괄 통합 순서를 따릅니다.

2026-10-10 당시 후보는 공개 allowlist build context에서 두 Dockerfile을 각각 빌드했습니다.
`HYHOME_WORKFLOW_REHEARSAL=1 python3 -m unittest tests.validation.test_workflow_version_bundle`는
2026-10-10 UNIT 5건과 ISOLATED 3건 PASS(EXIT 0)였습니다. 두 variant의 실제 UID·n8n
버전·font package inventory를 network none/read-only 임시 container에서 확인했습니다.
정확한 시험 입력 SHA는 [Airflow 후보 검증 기록](../airflow/README.md#sec01-업데이트-검증-경계)에 연결합니다.
linux/amd64 custom manifest는 production
`sha256:4298977846ed580208c670a87b125ab86873958bc25057a6e9aca1fa8a5f329b`,
dev `sha256:c32096b2ded1c1c9d6a00c39f32eb3e9ecf3a82a3282910d5d77a9cef8b1c710`입니다.
이 결과는 production main/worker·runner 실행이 아니며 서명·SBOM·scan·HOME·DB 복원은 NOT_RUN입니다.

독립 검토 보완 후 native 시험은 두 후보의 immutable OCI index가 선택하는 정확한
linux/amd64 manifest를 대조한 뒤 같은 index로 실행합니다. digest/architecture/OS가 다르면
실행 전에 실패하며 mutable tag를 실제 실행 대상으로 사용하지 않습니다. 보완한 opt-in
명령은 8건 PASS(EXIT 0)였고 현재 입력 SHA는 연결된 Airflow 검증 기록이 소유합니다.

Airflow의 명시 shell lint 보완으로 해당 후보만 다시 빌드한 후, n8n 두 variant를 포함한
전체 immutable-candidate 시험 8건을 새로 수행해 PASS(EXIT 0)였습니다. n8n 이미지 내용은
그 보완에서 변경하지 않았으며, 최신 시험 입력과 새 Airflow artifact는 연결된 검증 기록에 있습니다.

위 후보 build·native 결과는 과거 고정 입력의 기록입니다. Task0017 고정 입력의 production build·
module loading 결과는 위 안정판 묶음에서 구분합니다. 위 후보 시험은 현재
bundle 버전과 맞지 않아 저장소 시험에서 제외했습니다. 현재 bundle 회귀는
`WorkflowVersionBundleTests`가 계속 검사합니다.

### 독립 DEV 통지 워크로드

[매니페스트 outbox 통지](workloads/manifest-outbox-notifier/README.md)는
P04 SQL을 소비하는 비활성 workflow·제한된 SMTP node·합성 시험입니다.
실제 import·예약·credential·복구는 P05 Task 선행 계약 이후 검증합니다.
전체 native 시험의 자동 cleanup FAIL과 후속 정확한 소유 대상 reconciliation PASS는
별도 결과입니다. 기본 시험은 native 실행을 skip하며 명시 선택자와 고정 캐시 이미지가
필요합니다. 실행·중단·정리 절차는 아래 Runbook 탐색점의 RUN-0053이 소유합니다.
Airflow 게시 데이터의 실제 n8n 인계·combined E2E·HOME 복구는 미검증입니다.

## Troubleshooting

- 이 leaf는 루트 네트워크, Docker Secrets, 루트 include 컨텍스트에 의존하므로 루트 workflow 검증 명령으로 시작합니다.
- queue나 자격 증명 설정을 변경하기 전에 n8n 서비스 로그와 연결된 런북을 확인합니다.

### Convergence contract

- n8n core/worker/task runner는 `workflow`/`workflow-n8n`에서 **HOME**이며, n8n Valkey와 exporter는 `dedicated-valkey`에서 **OPTIONAL**입니다.
- Root preflight: `docker compose --profile workflow config --quiet`. Root start: `docker compose --profile workflow up -d n8n n8n-worker n8n-task-runner n8n-task-runner-worker`.
- `dedicated-valkey`는 해당 쌍만 시작합니다. 실제 선택은 `N8N_VALKEY_HOST`와 `N8N_VALKEY_SECRET`을 함께 일치시켜야 합니다. 두 entrypoint는 선택된 파일의 존재를 확인하고, 두 runner는 마운트된 `n8n_runner_auth_token`을 launcher에 전달합니다. 선언 버전은 모두 일치하지만 Code 노드와 DB upgrade의 격리 실행은 별도로 검증해야 합니다.
- 운영 문서는 아래 탐색점의 `GDE-0053`, `POL-0053`, `RUN-0053`을 사용합니다. HOME 격리 복구는 미실행입니다.

### 선택형 전용 Valkey 관측 계정

기본 `dedicated-valkey` 설정의 exporter는 여전히 기본 애플리케이션 비밀번호와
관리 권한을 공유합니다. 별도 계정을 준비한 뒤 루트에서
루트 파일 뒤에 Airflow, n8n, OAuth2 Proxy의 `docker-compose.monitor-acl.yml`을
각각 `-f`로 명시하면 세 전용 broker/exporter 쌍에만 최소 관측 ACL을 적용합니다.
서비스별 `monitor_password.txt` 파일 경로는 루트 Secret 선언과 공개 카탈로그가
소유합니다. 기존 기본 계정·앱 비밀번호·네트워크·AOF는 유지하며, 선택형 경로에서는
exporter가 자기 관측 파일만 마운트하고 비밀번호를 명령 인자로 넘기지 않습니다.
이 overlay 조합만으로 앱의 shared/dedicated endpoint 선택이 바뀌지는 않습니다.

관측 계정은 PING, INFO, COMMAND INFO, SLOWLOG LEN, COMMANDLOG LEN만 허용합니다.
키·채널·Lua·관리 명령은 허용하지 않으며 INFO의 전체 DB 집계 노출은 남습니다.
exporter의 선택적 SLOWLOG GET 거부는 상세 지표 부재로 기록하고 권한을 넓혀
없애지 않습니다. `/scrape`는 비활성화하고 기존 Prometheus `/metrics`를 유지합니다.
관측 파일은 의도한 UID/보조 GID가 읽을 수 있는 안전한 단일 파일이어야 하고,
broker는 자신의 기본/관측 비밀번호가 같은 경우 시작을 거부합니다. 서로 다른
서비스 간 비밀번호 분리·회전은 별도 운영 인수입니다.

공개 합성 렌더링과 ACL 파일 검사는 실제 채택·수집·앱 queue/session·AOF·회전·복구를
대신하지 않습니다. 실제 실행은 고정 이미지·정확한 대상·정리/복구 경계 검토 후
분리 검증합니다. 직접 대상과 companion 선택은 POL-0078이 소유합니다.

## Related Documents

- [Guide 탐색](../../../docs/05.operations/guides/08-workflows-and-automation/README.md)
- [Policy 탐색](../../../docs/05.operations/policies/08-workflows-and-automation/README.md)
- [Runbook 탐색](../../../docs/05.operations/runbooks/08-workflows-and-automation/README.md)
- [Documentation index](../../../docs/README.md)

런타임 고정 값은 Compose/Dockerfile 선언이 소유하고 [파생된 Compose 이미지 프로젝션](../../tech-stack.versions.json)으로 드리프트를 검증합니다.

Build source authority: [Dockerfile](Dockerfile), [dev.Dockerfile](dev.Dockerfile).
