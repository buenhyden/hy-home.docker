---
title: "n8n 워크플로 자동화"
version: "1.2.6"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
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
├── docker-entrypoint*.sh
├── custom/
└── README.md           # This file
```

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | n8n Low-code Automation 서비스 leaf. [root docker-compose.yml](../../../docker-compose.yml) -> `infra/07-workflow/n8n/docker-compose.yml` 경로로 루트 include가 활성화됨. 이 파일 하나가 이 디렉터리의 유일한 Compose 파일임 |
| Config files | `docker-compose.yml` |
| Config values | env 키: `GENERIC_TIMEZONE`, `TZ`, `DB_TYPE`, `DB_POSTGRESDB_HOST`, `DB_POSTGRESDB_PORT`, `DB_POSTGRESDB_DATABASE`, `DB_POSTGRESDB_USER`, `DB_POSTGRESDB_PASSWORD_FILE` 외 다수; 프로필: `workflow`, `workflow-n8n` |
| Compose linkage | [root docker-compose.yml](../../../docker-compose.yml) -> `infra/07-workflow/n8n/docker-compose.yml` 경로로 무조건 루트 include되며 프로필(`workflow`, `workflow-n8n`)로 선택됨 |
| Networks | `edge_net`, `mng_data_net`, `n8n_net`, `obs_net` |
| Volumes | `n8n-data:/home/node/.n8n:rw`, `./custom:/home/node/.n8n/custom:rw`, `n8n-task-runner-worker-data:/home/node/.n8n:rw`, `n8n-data`, `n8n-task-runner-data`, `n8n-task-runner-worker-data`, `n8n-valkey-data:/data:rw`, `n8n-valkey-data` |
| Ports | `${N8N_PORT:-5678}`, `${N8N_BROKER_PORT:-5679}`, `${N8N_TASK_RUNNER_PORT:-5680}`, `${VALKEY_PORT:-6379}`, `${VALKEY_BUS_PORT:-16379}`, `${VALKEY_EXPORTER_PORT:-9121}` |
| Labels | `hy-home.tier`, `traefik.enable`, `traefik.http.routers.n8n.rule`, `traefik.http.routers.n8n.entrypoints`, `traefik.http.routers.n8n.middlewares`, `traefik.http.routers.n8n.tls`, `traefik.http.routers.n8n.service`, `traefik.http.services.n8n.loadbalancer.server.port` |
| Secret refs | main/worker는 선택된 `mng_valkey_password` 또는 `n8n_valkey_password` 하나와 `n8n_db_password`, `n8n_encryption_key`, `n8n_runner_auth_token`을 마운트함. runner 둘은 `n8n_runner_auth_token`만 마운트함 |
| Healthcheck | `n8n`, `n8n-worker`, `n8n-task-runner`, `n8n-task-runner-worker`, `dedicated-valkey` 프로필의 `n8n-valkey`에 Compose 헬스체크가 선언되어 있음. exporter는 의존성 기반으로 게이트됨. main은 `/healthz/readiness`, worker·runner는 각 선언된 `/healthz`를 사용하며 같은 신호가 아님; probe 통과가 작업 실행 성공이나 runner 호환성을 입증하지 않음 |
| Operations | Guide (`docs/05.operations/guides/0053-n8n.md`), Policy (`docs/05.operations/policies/0053-n8n.md`), Runbook (`docs/05.operations/runbooks/0053-n8n.md`) |
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

## Traceability (Golden 5)

- **PRD**: 07-workflow PRD (`docs/01.requirements/0008-workflow.md`)
- **ARD**: 07-workflow Architecture Description (`docs/02.architecture/descriptions/0007-workflow-architecture.md`)
- **ADR**: N8N Integration ADR (`docs/02.architecture/decisions/0007-airflow-n8n-hybrid-workflow.md`)
- **Plan**: 활성 Spec 패키지 없음. 이전 SPEC-0008은 폐기되었습니다 (`docs/98.archive/tombstones/03.specs/0008-workflow.md`).

## Validation

- README나 n8n에 영향을 주는 Compose 참조 변경 후에는 `HYHOME_COMPOSE_PROFILES='workflow-n8n' bash scripts/validation/validate-docker-compose.sh`를 실행합니다.
- n8n 문서를 준비 완료로 표시하기 전에 `bash scripts/hardening/check-all-hardening.sh`를 실행합니다.

### SEC01 안정판 묶음

2026-10-10 [공식 Docker 설치 문서](https://docs.n8n.io/hosting/installation/docker/)의 stable channel과
[release API](https://github.com/n8n-io/n8n/releases/tag/n8n%402.42.6)를 대조했습니다. <!-- runtime-version-exception: compatibility — immutable source evidence reference; Compose/Dockerfile owns the deployment pin -->
main·worker와 두 task runner를 같은 vendor stable로 맞추고 두 custom Dockerfile의 base·font builder
OCI index digest를 고정합니다. platform manifest·custom build image ID·실제 running digest는 별도 증거입니다.
fontconfig·Noto·DejaVu·Liberation·emoji 패키지는 조회한 Alpine 안정 채널의 명시 버전으로 설치합니다.
폐기된 `ttf` alias 대신 유지되는 font package를 사용하고, 최종 이미지의
`/usr/share/hy-home-font-builder-packages.txt`에 실제 설치 목록을 보존합니다.

UNIT의 네 role 정합 검사는 native workflow import·실행이나 HOME 배포를 입증하지 않습니다.
deprecated node import 거부·JSON typeVersion·webhook·Code runner·queue·PostgreSQL·SMTP·실패 경로는 NOT_RUN입니다.
SEC01 담당자는 2026-10-17까지 독립 매니페스트 배치로 다음 검증을 수행해야 합니다.
Wiki 예약이나 실제 Wiki 소비자는 이 업데이트에 추가하지 않습니다.

HOME 전환 전 MNG DB와 n8n data, 동일 encryption key의 독립 보관, queue/진행 중 실행의
중단·재개 경계를 확인합니다. 새 schema migration 후 rollback은 사전 DB·data 백업을
빈 이전 이미지 환경에 복원해야 하며 이미지 태그 변경만으로 DB 복구를 주장하지 않습니다.
실제 backup·15분 중단 한도·복원·HOME 전환은 NOT_RUN이며 총괄 통합 순서를 따릅니다.

이번 후보는 공개 allowlist build context에서 두 Dockerfile을 각각 빌드했습니다.
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

## Troubleshooting

- 이 leaf는 루트 네트워크, Docker Secrets, 루트 include 컨텍스트에 의존하므로 루트 workflow 검증 명령으로 시작합니다.
- queue나 자격 증명 설정을 변경하기 전에 n8n 서비스 로그와 연결된 런북을 확인합니다.

### Convergence contract

- n8n core/worker/task runner는 `workflow`/`workflow-n8n`에서 **HOME**이며, n8n Valkey와 exporter는 `dedicated-valkey`에서 **OPTIONAL**입니다.
- Root preflight: `docker compose --profile workflow config --quiet`. Root start: `docker compose --profile workflow up -d n8n n8n-worker n8n-task-runner n8n-task-runner-worker`.
- `dedicated-valkey`는 해당 쌍만 시작합니다. 실제 선택은 `N8N_VALKEY_HOST`와 `N8N_VALKEY_SECRET`을 함께 일치시켜야 합니다. 두 entrypoint는 선택된 파일의 존재를 확인하고, 두 runner는 마운트된 `n8n_runner_auth_token`을 launcher에 전달합니다. 선언 버전은 모두 일치하지만 Code 노드와 DB upgrade의 격리 실행은 별도로 검증해야 합니다.
- 안정적인 진입점: [docs/README.md](../../../docs/README.md). 정확한 Stage 05 경로: `docs/05.operations/guides/0053-n8n.md`; ID: `GDE-0053`, `POL-0053`, `RUN-0053`. 격리 복구는 계획되어 있으나 아직 실행되지 않았습니다.

## Related Documents

- **Guide**: n8n usage guide (`docs/05.operations/guides/0053-n8n.md`)
- **Policy**: n8n operations policy (`docs/05.operations/policies/0053-n8n.md`)
- **Runbook**: n8n recovery runbook (`docs/05.operations/runbooks/0053-n8n.md`)
- [Documentation index](../../../docs/README.md)

런타임 고정 값은 Compose/Dockerfile 선언이 소유하고 [파생된 Compose 이미지 프로젝션](../../tech-stack.versions.json)으로 드리프트를 검증합니다.

Build source authority: [Dockerfile](Dockerfile), [dev.Dockerfile](dev.Dockerfile).
