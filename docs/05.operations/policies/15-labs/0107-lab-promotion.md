---
title: "LAB Promotion Policy"
version: "0.2.0"
type: "operation/policy"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-06"
layer: "operations"
artifact_id: "POL-0107"
parent_ids:
- "AD-0026"
created: "2026-11-05"
---

# LAB Promotion Policy

## Overview

이 정책은 `labs/` 아래 LAB을 `infra/`로 승격할 때 지켜야 하는 구조, 승격 manifest, secret,
목적지와 readiness 통제를 정한다. 계약의 정본은
[SPEC-0263](../../../03.specs/0263-lab-promotion-contract/spec.md)이고, 이 정책은 그 계약을
운영 통제로 옮긴 것이다. 실행 절차는
[RUN-0107](../../runbooks/15-labs/0107-lab-promotion.md)이 소유한다.

## Scope

현재 15개 LAB 전부와 이후 추가되는 LAB에 적용된다. 이 정책은 어떤 LAB도 승격하지 않는다.
각 승격은 이 정책을 따르는 별도 Task이며 그 Task에 owner 승인과 운영 window가 필요하다.
컨테이너 기동·정지·재생성, live data 이동과 OpenBao KV 변경은 이 정책의 승인 범위가 아니다.

## Rules

### Standard layout

- 모든 LAB은 폴더 하나 `labs/<name>/`이며 `infra/<tier>/<service>/`와 같은 모양을 갖는다.
- 폴더에는 진입점 `docker-compose.yml`, [infra 서비스 문서 기준](../../../../infra/README.md)을
  따르는 `README.md`, 승격 manifest `promotion.yaml`과 LAB이 쓰는 build source, mount 설정,
  helper, Grafana 대시보드가 함께 있다.
- `labs/` root에는 [labs/README.md](../../../../labs/README.md)와 공유 `labs/.env.example`만 둔다.
- LAB은 `hy-home-lab-`로 시작하는 자신의 Compose project(예: `hy-home-lab-kafka`,
  `hy-home-lab-opensearch`), LAB network, `LAB_*` endpoint 입력,
  `LAB_DATA_DIR` 아래 데이터와 `lab.py check`의 격리를 유지한다.

### Promotion manifest

`labs/<name>/promotion.yaml`은 LAB이 어디로, 어떻게 승격될지 선언한다.
`python3 scripts/operations/lab.py check`가 이를 검증한다.

| Field | 내용 |
| --- | --- |
| `kind` | `add`, `replace-same`, `replace-substitute`, 또는 목적지가 아직 없는 `undecided`. `undecided`는 `target`이 없고 readiness 검사가 거부한다 |
| `target` | 목적지 폴더 `infra/<tier>/<service>/`와 합류할 POL-0078 profile |
| `replaces` | 두 대체 kind에서 은퇴하는 HOME 서비스, 그 Compose 경로와 소비자 |
| `integrations` | 필요한 `infra` 연동(gateway route, OIDC client, DB role과 provisioning, observability scrape·log, OpenBao secret 전달, 공유 network)과 그 `infra` 소유자 |
| `secrets` | LAB secret 사본마다 catalog 행과 `infra` 목적지 경로 |
| `documents` | Guide와 Runbook의 현재 `15-labs` 경로와 목적지 `docs/05.operations` 역할 폴더 |
| `resources` | 서비스별 선언 CPU·memory limit(`cpus`, `memory_mib`)과 reservation(`reservations.cpus`, `reservations.memory_mib`), 데이터·image에 필요한 disk |
| `host` (선택) | Compose가 표현하지 못하는 최소 Docker·Compose 버전과 kernel 기능 |

`lab.py check`는 알 수 없는 `kind`, `infra/<tier>/` 밖의 `target`, catalog 행이 없는 secret,
렌더링된 limit 또는 reservation과 다른 `resources`를 문제로 보고한다.

### Secrets

- LAB 단계의 모든 secret 파일은 `secrets/labs/<name>/` 아래 LAB 사본이다. 사본마다 catalog 행
  (`LAB-*`, scope `lab`)과 공개 registry placeholder 행을 따로 갖는다.
- LAB은 HOME secret 경로를 읽지 않는다. HOME도 쓰는 값(예: SMTP)은 HOME 값을 LAB 위치로
  복사하고, LAB만 쓰는 값은 LAB 위치로 옮긴다. 파일 복사와 이동은 owner가 한다.
- 승격 때 LAB secret 값은 승격하지 않는다. 승격된 서비스는 manifest의 목적지 경로에서 `infra`
  secret을 받는다. 새 값이거나, 대체 승격이면 secret 정책에 따라 rotate한 기존 HOME secret이다.
- 승격 때 각 LAB 사본과 그 catalog 행을 은퇴시키고 registry도 따라간다. 목적지마다 새 `root`
  catalog 행을 만들거나 기존 행에 새 소비자를 더한다.
- 공개 registry `secrets/SENSITIVE_ENV_VARS.md.example`은 생성 파일이 아니다. catalog와
  일치해야 하므로 owner가 손으로 편집한다. agent는 placeholder 편집안만 준비한다.

### Docker socket exception

허용되는 socket bind는 supabase `vector` 서비스 하나다. source와 target이 모두
`/var/run/docker.sock`이고 `read_only: true`여야 한다. `lab.py check`는 쓰기 가능한 bind, 다른
supabase 서비스의 같은 bind, 다른 이름의 `.sock` source를 모두 거부한다.

### Destination rules

| LAB source | 승격 목적지 |
| --- | --- |
| `labs/<name>/docker-compose.yml` | root가 include하는 `infra/<tier>/<service>/docker-compose.yml`; LAB 전용 입력은 `infra` 연동으로 바꾼다 |
| `labs/<name>/README.md` | 목적지 폴더의 서비스 README |
| `labs/<name>/` 자산 | 같은 상대 경로로 목적지 폴더 |
| `15-labs`의 Guide와 Runbook | 목적지 역할 폴더; artifact 식별자와 생성일을 유지한다 |
| `secrets/labs/<name>/*` | 은퇴; 서비스는 manifest가 지정한 `infra` secret을 쓴다 |
| `promotion.yaml` | 삭제; 그 사실은 승격 Task에 기록한다 |

tier는 서비스 기능을 따른다. 운영 문서는 서비스 domain을 따르며 tier 번호와 같을 필요가 없다.
파일, 문서, secret, catalog 행의 LAB 사본은 하나도 남기지 않는다.

### Readiness rules

승격 전 `lab.py readiness <name>`은 fail-closed 보고서를 만든다. 측정하지 못한 값은
`NOT_RUN`이며 통과가 아니다. 다섯 기준이 모두 `PASS`일 때만 승격할 수 있다.

- **Manifest 경로.** `documents.*`, `integrations[].owner`, `replaces[].compose_path`,
  `target.folder`는 repository 안의 상대 경로여야 한다. 절대 경로와 `..` 탈출은 거부한다.
- **은퇴 서비스.** `replace-same`과 `replace-substitute`만 서비스를 은퇴시킨다. 은퇴 서비스는
  root `docker-compose.yml`이 include하는 `compose_path`에 선언되어 있고 root render에 나타나야
  한다. 아니면 composition이 실패하고 아무것도 은퇴하지 않는다.
- **Tier.** 이미 있는 목적지 폴더는 은퇴 서비스가 독점할 때만 대체로 인정한다. 은퇴 서비스가
  그 폴더를 점유하고, 유지되는 서비스의 build·bind source가 그 안에 없으며, 그 아래
  `*compose*.y*ml` 파일이 선언한 모든 서비스가 은퇴해야 한다. 그 아래 Compose 파일을 읽을 수
  없거나, symlink 디렉터리가 있거나, 폴더가 repository 밖으로 풀리면 실패한다.
- **Composition.** port와 container 이름은 유지되는 서비스가 선언하지 않을 때만 뺀다. network와
  데이터 경로는 빼지 않는다.
- **Resources.** 판정 대상은 limit이 아니라 선언 reservation이다. 실행 중 container마다
  `com.docker.compose.project`와 `com.docker.compose.service` label로 root 또는 실행 중 LAB
  render의 서비스를 찾아 그 reservation을 더한다. 여기에 후보 render의 reservation과 아래
  외부 workload allowance를 한 번 더하고, 실행 중인 은퇴 서비스를 뺀다. 그 합이 측정된 host
  용량에서 아래 reserve를 뺀 예산 안에 있어야 한다. 알려진 project 밖의 container(k3d 등)는
  개수와 관계없이 allowance로만 센다. render가 없는 실행 중 LAB project, render에 없는 서비스,
  reservation이 없는 서비스, limit이 없는 서비스는 합할 수 없어 `NOT_RUN`이다. 후보 서비스도
  같다. reservation이 limit보다 크면 `FAIL`이고, 알려진 합이 이미 예산을 넘으면 `NOT_RUN`이
  있어도 `FAIL`이다. manifest는 0이거나 빠진 limit과 render와 다른 reservation을 거부한다.
  disk는 데이터 root와 Docker data root의 여유에서 전체의 reserve 비율을 뺀 값이
  `disk_gib`를 덮어야 한다.
- **Owner 확인 항목.** 아래 Owner check items의 세 하위 검사는 측정값도 차단도 아니다.
  보고서는 이를 `OWNER_JUDGMENT`로 보이고 `owner_checks`에 나열한다. 기준과 전체 결과는
  `PASS`, `FAIL`, `NOT_RUN`만 갖고, 측정된 기준이 모두 `PASS`여야 `PASS`다.

### Reservation rule

- 공유 resource template(`infra/common-optimizations.yml`의 `x-resource-*` anchor와 limit을
  직접 쓰는 template)과, limit을 직접 쓰는 모든 HOME·LAB 서비스는
  `deploy.resources.reservations.cpus`와 `.memory`를 선언한다. limit은 기존 short form
  (`cpus`, `mem_limit`)을 유지한다. 자체 `deploy` 블록(GPU device 등)이 있는 서비스는 기존
  key를 지우지 않고 reservation을 합친다.
- 크기는 실행 중 구성원의 `docker stats --no-stream` 표본 세 개 이상에서 구성원별 최대값을
  잡고, anchor 안에서 가장 큰 값에 1.5를 곱해 CPU는 0.05, memory는 32 MiB 단위로 올린다.
  결과는 limit을 넘지 않고, 측정값의 하한은 0.05 CPU와 32 MiB다.
- 측정하지 않은 reservation은 limit과 같다. 재측정하면 낮아진다. LAB은 상시 실행하지
  않으므로 승인된 LAB lease 실행(`lab.py run`)에서 측정할 때까지 limit과 같다.
- Docker는 CPU reservation을 강제하지 않는다. 선언된 예산일 뿐이다. memory reservation은 soft
  limit이다. HOME 서비스는 owner window에서 재생성될 때 새 reservation을 받는다.
- 표본과 결과는 [SPEC-0263-TSK-0002](../../../03.specs/0263-lab-promotion-contract/tasks/tsk-0002-lab-promotion-reservations.md)의
  Measurements에 있다.

### Owner check items

`lab.py readiness`가 측정하지 않는 SPEC-0263 5절 하위 검사다. 보고서 값은 `OWNER_JUDGMENT`이고
기준 결과를 바꾸지 않는다. 각 승격 Task가 owner의 판단을 checklist로 기록한다.

| 하위 검사 | 보고서 값 |
| --- | --- |
| Tier: 목적지 tier가 서비스 기능에 맞는가 | `tier.values.function_fit` |
| Linux: 서비스에 필요한 group과 file mode | `linux.values.groups_and_file_modes` |
| Composition: profile과 consumer 충돌 | `composition.values.profile_and_consumer_clashes` |

### Host reserve

OS와 Docker를 위해 남기는 reserve다. 2026-11-05 owner가 승인했고 `lab.py`의
`PROMOTION_RESERVE`가 이 표와 같아야 한다.

| Resource | Reserve |
| --- | --- |
| CPUs | 2 |
| Memory MiB | 4096 |
| Disk percent | 10 |

### External-workload allowance

HOME과 LAB Compose project 밖의 workload(k3d 등)를 위한 고정 allowance다. 실행 중인 외부
container 수와 관계없이 resource 합에 한 번 더한다. 2026-11-06 k3d container 다섯 개가 약
1.0 CPU와 4.1 GiB를 썼다. `lab.py`의 `PROMOTION_EXTERNAL_ALLOWANCE`가 이 표와 같아야 한다.

| Resource | Allowance |
| --- | --- |
| Allowance CPUs | 2 |
| Allowance MiB | 6144 |

## Exceptions

### Current HOME resource state

2026-11-06 owner가 limit 대신 reservation으로 판정하기로 결정했다(SPEC-0263 0.3.0). 같은 날
read-only HOME readiness에서 `valkey-cluster`와 `postgresql-ha`는 tier, composition, linux,
docker가 `PASS`이고 resources가 `FAIL`이었다. 12 CPU host의 예산은 10 CPU와 27924 MiB다.
실행 중 HOME container의 reservation 합은 27.75 CPU와 22080 MiB이며, 그중 `x-resource-db`
구성원 10개가 20 CPU다. 이 anchor의 표본에서 `airflow-dag-processor`가 1.65 CPU까지 올라가
reservation이 limit인 2.00 CPU가 되었다. 후보는 측정 전이라 reservation이 limit과 같다
(`valkey-cluster` 7.0 CPU, `postgresql-ha` 10.5 CPU). 이 값은 render에서 오므로 HOME
container를 재생성하지 않아도 같다. resource `FAIL`은 승격 거부다. 예외 owner는 @buenhyden이다.

### Review Cadence

reserve, allowance, reservation 값, host 사양, readiness 규칙 또는 LAB 목록이 바뀔 때와 승격
Task를 열기 전마다 검토한다.

### Traceability

- Contract: [SPEC-0263](../../../03.specs/0263-lab-promotion-contract/spec.md) section 1–5.
- Implementation: `scripts/operations/lab.py`의 `check`, `readiness`, `budget`,
  `PROMOTION_RESERVE`, `PROMOTION_EXTERNAL_ALLOWANCE`; `infra/common-optimizations.yml`의
  resource template.
- Artifact: `POL-0107`; parent: `AD-0026`.

## Verification

- `python3 scripts/operations/lab.py check <name>`가 layout, manifest, secret 경로를 검증한다.
- `tests/validation/test_lab_controller.py`의 `test_reserve_matches_policy`와
  `test_allowance_matches_policy`가 위 reserve·allowance 표와 `PROMOTION_RESERVE`,
  `PROMOTION_EXTERNAL_ALLOWANCE`의 일치를 검증한다. `test_shared_templates_declare_reservations`가
  모든 공유 template의 reservation이 limit 이하인지 검증한다.
- `tests/validation/test_lab_isolation.py`와 `tests/validation/test_lab_layout.py`가 격리와
  layout을 검증한다.

## Related Documents

- [LAB promotion runbook](../../runbooks/15-labs/0107-lab-promotion.md)
- [LAB README](../../../../labs/README.md)
- [Spec](../../../03.specs/0263-lab-promotion-contract/spec.md)
- [Domain catalog](../../README.md)
