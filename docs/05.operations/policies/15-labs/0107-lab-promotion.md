---
title: "LAB Promotion Policy"
version: "0.3.0"
type: "operation/policy"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "operations"
artifact_id: "POL-0107"
parent_ids:
- "AD-0026"
created: "2026-11-05"
next_review_at: "2027-05-13"
---

# LAB Promotion Policy

## Purpose and Scope

### Objective

이 정책은 `labs/` 아래 LAB을 `infra/`로 승격할 때 지켜야 하는 구조, 승격 manifest, secret,
목적지와 readiness 통제를 정한다. 계약의 정본은
[SPEC-0263](../../../03.specs/0263-lab-promotion-contract/spec.md)이고, 이 정책은 그 계약을
운영 통제로 옮긴 것이다. 실행 절차는
[RUN-0107](../../runbooks/15-labs/0107-lab-promotion.md)이 소유한다.

#### Authority

- Contract: [SPEC-0263](../../../03.specs/0263-lab-promotion-contract/spec.md) section 1–5.
- Implementation: `scripts/operations/lab.py`의 `check`, `readiness`, `budget`,
  `PROMOTION_RESERVE`, `PROMOTION_EXTERNAL_ALLOWANCE`; `infra/common-optimizations.yml`의
  resource template.
- Artifact: `POL-0107`; parent: `AD-0026`.

### Applies To

추적된 `labs/*/promotion.yaml`이 등록하는 각 LAB에 적용한다. 이 초안은 증거를 준비할 때
참고한다. 실제 승격은 별도 Task가 소유하며 해당 대상에 대한 owner 승인과 운영 window가 필요하다.

#### Exclusions

컨테이너 기동·정지·재생성, live data 이동과 OpenBao KV 변경은 이 정책의 승인 범위가 아니다.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0107-R1 | LAB 구성 시 | 필수: 모든 LAB은 `infra/<tier>/<service>/`와 같은 모양의 폴더 하나 `labs/<name>/`이다 | `python3 scripts/operations/lab.py check <name>` / `tests/validation/test_lab_layout.py` | none |
| POL-0107-R2 | LAB 구성 시 | 필수: 폴더에 `docker-compose.yml`, infra 서비스 문서 기준을 따르는 `README.md`, `promotion.yaml`과 LAB이 쓰는 build source/mount 설정/helper/Grafana 대시보드를 둔다 | `python3 scripts/operations/lab.py check <name>` / `tests/validation/test_lab_layout.py` | none |
| POL-0107-R3 | LAB 구성 시 | 필수: `labs/` root에는 `labs/README.md`와 공유 `labs/.env.example`만 둔다 | `python3 scripts/operations/lab.py check <name>` / `tests/validation/test_lab_layout.py` | none |
| POL-0107-R4 | LAB 구성 시 | 필수: `hy-home-lab-`로 시작하는 자신의 Compose project, LAB network, `LAB_*` endpoint 입력, `LAB_DATA_DIR` 아래 데이터와 `lab.py check`의 격리를 유지한다 | `python3 scripts/operations/lab.py check <name>` / `tests/validation/test_lab_isolation.py` | none |
| POL-0107-R5 | 승격 선언 시 | 필수: `labs/<name>/promotion.yaml`로 LAB이 어디로 어떻게 승격될지 선언한다 | `python3 scripts/operations/lab.py check <name>` | none |
| POL-0107-R6 | manifest 작성 시 | 필수: `kind`는 `add`/`replace-same`/`replace-substitute`/`undecided` 중 하나다 | `python3 scripts/operations/lab.py check <name>` | none |
| POL-0107-R7 | `kind`가 `undecided`일 때 | 필수: `target`을 두지 않는다(readiness 검사가 거부) | `python3 scripts/operations/lab.py readiness <name>` | none |
| POL-0107-R8 | manifest 작성 시 | 필수: `target`에 목적지 폴더 `infra/<tier>/<service>/`와 합류할 `POL-0078` profile을 선언한다 | `python3 scripts/operations/lab.py check <name>`(`infra/<tier>/` 밖의 `target` 보고) | none |
| POL-0107-R9 | 두 대체 kind일 때 | 필수: `replaces`에 은퇴하는 HOME 서비스, 그 Compose 경로와 소비자를 선언한다 | none | none |
| POL-0107-R10 | manifest 작성 시 | 필수: `integrations`에 필요한 infra 연동(gateway route, OIDC client, DB role과 provisioning, observability scrape/log, OpenBao secret 전달, 공유 network)과 그 infra 소유자를 선언한다 | none | none |
| POL-0107-R11 | manifest 작성 시 | 필수: `secrets`에 LAB secret 사본마다 catalog 행과 infra 목적지 경로를 선언한다 | `python3 scripts/operations/lab.py check <name>`(catalog 행이 없는 secret 보고) | none |
| POL-0107-R12 | manifest 작성 시 | 필수: `documents`에 Guide와 Runbook의 현재 `15-labs` 경로와 목적지 `docs/05.operations` 역할 폴더를 선언한다 | none | none |
| POL-0107-R13 | manifest 작성 시 | 필수: `resources`에 서비스별 선언 limit(`cpus`, `memory_mib`)과 reservation(`reservations.cpus`, `reservations.memory_mib`), 데이터/image에 필요한 disk를 선언한다 | `python3 scripts/operations/lab.py check <name>`(렌더링된 limit 또는 reservation과 다른 `resources` 보고) | none |
| POL-0107-R14 | Compose가 표현하지 못하는 요구가 있을 때 | 허용: 선택 `host`에 최소 Docker/Compose 버전과 kernel 기능을 선언 | none | none |
| POL-0107-R15 | LAB 단계 | 필수: 모든 secret 파일은 `secrets/labs/<name>/` 아래 LAB 사본이다 | `python3 scripts/operations/lab.py check <name>` | none |
| POL-0107-R16 | LAB secret 사본마다 | 필수: catalog 행(`LAB-*`, scope `lab`)과 공개 registry placeholder 행을 따로 갖는다 | `python3 scripts/operations/lab.py check <name>`(catalog 행이 없는 secret 보고) | none |
| POL-0107-R17 | 항상 | 금지: LAB의 HOME secret 경로 읽기 | none | none |
| POL-0107-R18 | HOME도 쓰는 값(예 SMTP)일 때 | 필수: HOME 값을 LAB 위치로 복사한다 | none | none |
| POL-0107-R19 | LAB만 쓰는 값일 때 | 필수: LAB 위치로 옮긴다 | none | none |
| POL-0107-R20 | secret 파일 복사/이동 시 | 필수: owner가 한다 | 수동 | none |
| POL-0107-R21 | 승격 시 | 금지: LAB secret 값 승격 | none | none |
| POL-0107-R22 | 승격 시 | 필수: 승격된 서비스는 manifest의 목적지 경로에서 infra secret을 받는다(새 값, 또는 대체 승격이면 secret 정책에 따라 rotate한 기존 HOME secret) | none | none |
| POL-0107-R23 | 승격 시 | 필수: 각 LAB 사본과 그 catalog 행을 은퇴시키고 registry도 따라간다 | none | none |
| POL-0107-R24 | 승격 시 | 필수: 목적지마다 새 `root` catalog 행을 만들거나 기존 행에 새 소비자를 더한다 | none | none |
| POL-0107-R25 | 공개 registry 편집 시 | 필수: `secrets/SENSITIVE_ENV_VARS.md.example`은 catalog와 일치하도록 owner가 손으로 편집한다(생성 파일 아님) | 수동 | none |
| POL-0107-R26 | 공개 registry 편집 시 | 필수: agent는 placeholder 편집안만 준비한다 | 수동 | none |
| POL-0107-R27 | 항상 | 금지: 어떤 LAB도 Docker socket을 bind | `python3 scripts/operations/lab.py check <name>`(`/var/run/docker.sock`과 다른 이름의 `.sock` source를 읽기 전용 여부와 무관하게 거부) | none |
| POL-0107-R28 | 승격 시 | 필수: `labs/<name>/docker-compose.yml`은 root가 include하는 `infra/<tier>/<service>/docker-compose.yml`로 가고 LAB 전용 입력은 infra 연동으로 바꾼다 | none | none |
| POL-0107-R29 | 승격 시 | 필수: `labs/<name>/README.md`는 목적지 폴더의 서비스 README로 간다 | none | none |
| POL-0107-R30 | 승격 시 | 필수: `labs/<name>/` 자산은 같은 상대 경로로 목적지 폴더에 간다 | none | none |
| POL-0107-R31 | 승격 시 | 필수: `15-labs`의 Guide와 Runbook은 목적지 역할 폴더로 가며 artifact 식별자와 생성일을 유지한다 | none | none |
| POL-0107-R32 | 승격 시 | 필수: `secrets/labs/<name>/*`는 은퇴하고 서비스는 manifest가 지정한 infra secret을 쓴다 | none | none |
| POL-0107-R33 | 승격 시 | 필수: `promotion.yaml`은 삭제하고 그 사실을 승격 Task에 기록한다 | none | 승격 Task 기록 |
| POL-0107-R34 | 목적지 tier 선택 시 | 필수: tier는 서비스 기능을 따른다 | none | none |
| POL-0107-R35 | 운영 문서 배치 시 | 허용: 운영 문서는 서비스 domain을 따르며 tier 번호와 같을 필요가 없다 | none | none |
| POL-0107-R36 | 승격 후 | 금지: 파일, 문서, secret, catalog 행의 LAB 사본 잔존 | none | none |
| POL-0107-R37 | 승격 전 | 필수: `lab.py readiness <name>`으로 fail-closed 보고서를 만들고 측정하지 못한 값은 `NOT_RUN`(통과 아님)으로 둔다 | `python3 scripts/operations/lab.py readiness <name>` | none |
| POL-0107-R38 | 승격 시 | 필수: 다섯 기준이 모두 `PASS`일 때만 승격한다 | `python3 scripts/operations/lab.py readiness <name>` | none |
| POL-0107-R39 | manifest 경로 작성 시 | 필수: `documents.*`, `integrations[].owner`, `replaces[].compose_path`, `target.folder`는 repository 안의 상대 경로다 | `python3 scripts/operations/lab.py readiness <name>` | none |
| POL-0107-R40 | manifest 경로 작성 시 | 금지: 절대 경로와 `..` 탈출 | `python3 scripts/operations/lab.py readiness <name>` | none |
| POL-0107-R41 | 서비스 은퇴 시 | 필수: `replace-same`과 `replace-substitute`만 서비스를 은퇴시킨다 | none | none |
| POL-0107-R42 | 서비스 은퇴 시 | 필수: 은퇴 서비스는 root `docker-compose.yml`이 include하는 `compose_path`에 선언되어 root render에 나타나야 하며 아니면 composition이 실패하고 아무것도 은퇴하지 않는다 | `python3 scripts/operations/lab.py readiness <name>` | none |
| POL-0107-R43 | 이미 있는 목적지 폴더일 때 | 필수: 은퇴 서비스가 독점할 때만 대체로 인정한다(은퇴 서비스가 폴더를 점유, 유지되는 서비스의 build/bind source가 폴더 안에 없음, 그 아래 `*compose*.y*ml`이 선언한 모든 서비스가 은퇴) | `python3 scripts/operations/lab.py readiness <name>` | none |
| POL-0107-R44 | 목적지 폴더 아래 Compose 파일을 읽을 수 없거나 symlink 디렉터리가 있거나 폴더가 repository 밖으로 풀릴 때 | 필수: 실패로 판정한다 | `python3 scripts/operations/lab.py readiness <name>` | none |
| POL-0107-R45 | composition 시 | 필수: port와 container 이름은 유지되는 서비스가 선언하지 않을 때만 뺀다 | `python3 scripts/operations/lab.py readiness <name>` | none |
| POL-0107-R46 | composition 시 | 금지: network와 데이터 경로 제외 | `python3 scripts/operations/lab.py readiness <name>` | none |
| POL-0107-R47 | resources 판정 시 | 필수: limit이 아니라 선언 reservation으로 판정한다 | `python3 scripts/operations/lab.py readiness <name>` | none |
| POL-0107-R48 | resources 판정 시 | 필수: 실행 중 container의 `com.docker.compose.project`/`com.docker.compose.service` label로 root 또는 실행 중 LAB render의 서비스를 찾아 reservation을 더하고, 후보 render의 reservation과 외부 workload allowance를 한 번 더하며, 실행 중인 은퇴 서비스를 뺀다 | `python3 scripts/operations/lab.py readiness <name>` | none |
| POL-0107-R49 | resources 판정 시 | 필수: 그 합이 측정된 host 용량에서 reserve를 뺀 예산 안에 있어야 한다 | `python3 scripts/operations/lab.py readiness <name>` | none |
| POL-0107-R50 | 알려진 project 밖의 container(k3d 등)일 때 | 필수: 개수와 관계없이 allowance로만 센다 | `python3 scripts/operations/lab.py readiness <name>` | none |
| POL-0107-R51 | render가 없는 실행 중 LAB project, render에 없는 서비스, reservation 또는 limit이 없는 서비스(후보 서비스 포함)일 때 | 필수: 합할 수 없어 `NOT_RUN`으로 판정한다 | `python3 scripts/operations/lab.py readiness <name>` | none |
| POL-0107-R52 | reservation이 limit보다 클 때 | 필수: `FAIL`로 판정한다 | `python3 scripts/operations/lab.py readiness <name>` | none |
| POL-0107-R53 | 알려진 합이 이미 예산을 넘을 때 | 필수: `NOT_RUN`이 있어도 `FAIL`로 판정한다 | `python3 scripts/operations/lab.py readiness <name>` | none |
| POL-0107-R54 | manifest 검증 시 | 필수: 0이거나 빠진 limit과 render와 다른 reservation을 거부한다 | `python3 scripts/operations/lab.py check <name>`(렌더링된 limit 또는 reservation과 다른 `resources` 보고) / `python3 scripts/operations/lab.py readiness <name>` | none |
| POL-0107-R55 | disk 판정 시 | 필수: 데이터 root와 Docker data root의 여유에서 전체의 reserve 비율을 뺀 값이 `disk_gib`를 덮어야 한다 | `python3 scripts/operations/lab.py readiness <name>` | none |
| POL-0107-R56 | Owner 확인 항목 보고 시 | 필수: 세 하위 검사를 `OWNER_JUDGMENT`로 보이고 `owner_checks`에 나열한다(측정값도 차단도 아님) | `python3 scripts/operations/lab.py readiness <name>` | none |
| POL-0107-R57 | 기준/전체 결과 보고 시 | 필수: 기준과 전체 결과는 `PASS`/`FAIL`/`NOT_RUN`만 갖고 측정된 기준이 모두 `PASS`여야 `PASS`다 | `python3 scripts/operations/lab.py readiness <name>` | none |
| POL-0107-R58 | 항상 | 필수: 공유 resource template과 limit을 직접 쓰는 모든 HOME/LAB 서비스는 `deploy.resources.reservations.cpus`와 `.memory`를 선언한다 | none | none |
| POL-0107-R59 | 항상 | 필수: limit은 기존 short form(`cpus`, `mem_limit`)을 유지한다 | none | none |
| POL-0107-R60 | 자체 `deploy` 블록(GPU device 등)이 있는 서비스일 때 | 필수: 기존 key를 지우지 않고 reservation을 합친다 | none | none |
| POL-0107-R61 | reservation 크기 산정 시 | 필수: 실행 중 구성원의 `docker stats --no-stream` 표본 세 개 이상에서 구성원별 최대값을 잡는다 | none | none |
| POL-0107-R62 | reservation 크기 산정 시 | 필수: anchor 안에서 가장 큰 값에 1.5를 곱해 CPU는 0.05, memory는 32 MiB 단위로 올린다 | none | none |
| POL-0107-R63 | reservation 크기 산정 시 | 필수: 결과는 limit을 넘지 않는다 | `test_shared_templates_declare_reservations`(공유 template의 reservation이 limit 이하인지 검증) | none |
| POL-0107-R64 | reservation 크기 산정 시 | 필수: 측정값의 하한은 0.05 CPU와 32 MiB다 | none | none |
| POL-0107-R65 | 측정하지 않은 reservation일 때 | 필수: limit과 같게 둔다 | none | none |
| POL-0107-R66 | 재측정 시 | 필수: reservation을 낮춘다 | none | none |
| POL-0107-R67 | LAB reservation 측정 시 | 필수: 승인된 LAB lease 실행(`lab.py run`)에서 측정할 때까지 limit과 같게 둔다 | none | none |
| POL-0107-R68 | 승격 Task 시 | 필수: 각 승격 Task가 owner의 판단(Tier/Linux/Composition)을 checklist로 기록한다 | 수동 | none |
| POL-0107-R69 | 항상 | 필수: host reserve 표(CPUs 2, Memory MiB 4096, Disk percent 10)와 `lab.py`의 `PROMOTION_RESERVE`를 같게 둔다 | `tests/validation/test_lab_controller.py`의 `test_reserve_matches_policy` | none |
| POL-0107-R70 | 항상 | 필수: external-workload allowance 표(Allowance CPUs 2, Allowance MiB 6144)와 `lab.py`의 `PROMOTION_EXTERNAL_ALLOWANCE`를 같게 둔다 | `tests/validation/test_lab_controller.py`의 `test_allowance_matches_policy` | none |

#### Standard layout

- 모든 LAB은 폴더 하나 `labs/<name>/`이며 `infra/<tier>/<service>/`와 같은 모양을 갖는다.
- 폴더에는 진입점 `docker-compose.yml`, [infra 서비스 문서 기준](../../../../infra/README.md)을
  따르는 `README.md`, 승격 manifest `promotion.yaml`과 LAB이 쓰는 build source, mount 설정,
  helper, Grafana 대시보드가 함께 있다.
- `labs/` root에는 [labs/README.md](../../../../labs/README.md)와 공유 `labs/.env.example`만 둔다.
- LAB은 `hy-home-lab-`로 시작하는 자신의 Compose project(예: `hy-home-lab-kafka`,
  `hy-home-lab-opensearch`), LAB network, `LAB_*` endpoint 입력,
  `LAB_DATA_DIR` 아래 데이터와 `lab.py check`의 격리를 유지한다.

#### Promotion manifest

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

#### Secrets

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

#### Docker socket

어떤 LAB도 Docker socket을 bind하지 않는다. `lab.py check`는 `/var/run/docker.sock`과 다른 이름의
`.sock` source를 읽기 전용 여부와 무관하게 모두 거부한다. 유일한 예외였던 supabase `vector`는
2026-11-06 owner 결정으로 supabase LAB과 함께 제거되었다.

#### Destination rules

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

#### Readiness rules

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

#### Reservation rule

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

#### Owner check items

`lab.py readiness`가 측정하지 않는 SPEC-0263 5절 하위 검사다. 보고서 값은 `OWNER_JUDGMENT`이고
기준 결과를 바꾸지 않는다. 각 승격 Task가 owner의 판단을 checklist로 기록한다.

| 하위 검사 | 보고서 값 |
| --- | --- |
| Tier: 목적지 tier가 서비스 기능에 맞는가 | `tier.values.function_fit` |
| Linux: 서비스에 필요한 group과 file mode | `linux.values.groups_and_file_modes` |
| Composition: profile과 consumer 충돌 | `composition.values.profile_and_consumer_clashes` |

#### Host reserve

OS와 Docker를 위해 남기는 reserve다. 2026-11-05 owner가 승인했고 `lab.py`의
`PROMOTION_RESERVE`가 이 표와 같아야 한다.

| Resource | Reserve |
| --- | --- |
| CPUs | 2 |
| Memory MiB | 4096 |
| Disk percent | 10 |

#### External-workload allowance

HOME과 LAB Compose project 밖의 workload(k3d 등)를 위한 고정 allowance다. 실행 중인 외부
container 수와 관계없이 resource 합에 한 번 더한다. 2026-11-06 k3d container 다섯 개가 약
1.0 CPU와 4.1 GiB를 썼다. `lab.py`의 `PROMOTION_EXTERNAL_ALLOWANCE`가 이 표와 같아야 한다.

| Resource | Allowance |
| --- | --- |
| Allowance CPUs | 2 |
| Allowance MiB | 6144 |

### Exceptions

#### Current HOME resource state

2026-11-06 owner가 limit 대신 reservation으로 판정하기로 결정했다(SPEC-0263 0.3.0). 같은 날
read-only HOME readiness에서 `valkey-cluster`와 `postgresql-ha`는 tier, composition, linux,
docker가 `PASS`이고 resources가 `FAIL`이었다. 12 CPU host의 예산은 10 CPU와 27924 MiB다.
anchor 하나의 reservation이 가장 높은 구성원 peak를 모두에게 적용하므로, owner 결정으로 peak가
두드러진 서비스가 자체 reservation을 갖는다: `airflow-dag-processor`(2.00 CPU, 512M), `openbao`,
`blog-ingestion`, `dozzle`, `alloy`, `seaweedfs-filer`, `dev-valkey`, `mng-valkey`. anchor는 나머지
구성원의 peak로 낮췄다(`x-resource-db` 0.15 CPU, `x-resource-med` 0.05 CPU와 192M,
`x-resource-low` 0.05 CPU). 실행 중 HOME reservation 합은 6.8 CPU와 19072 MiB다.
`valkey-cluster`는 2026-11-06 lease run 측정값(1.15 CPU, 480 MiB)으로 resources `PASS`다(필요
9.8 CPU와 25536 MiB). `postgresql-ha`는 측정 전이라 reservation이 limit(10.5 CPU)이고 `FAIL`이다.
측정은 유휴 표본이므로 승격 전 부하 측정이 필요하다. 이 값은 render에서 오므로 HOME
container를 재생성하지 않아도 같다. resource `FAIL`은 승격 거부다. 예외 owner는 @buenhyden이다.

`ollama`는 측정 최대 47 MiB와 달리 model loading을 위한 4G memory reservation을 유지한다.
2026-11-06 owner가 sizing 규칙의 예외로 승인했다.

render가 없는 Compose project(따로 띄운 HOME stack, 외부 Compose stack)의 container는
allowance로 세지 않고 `NOT_RUN`이다. Compose label이 없는 container(k3d 등)만 allowance로
센다(2026-11-06 owner 결정).

#### Approval and Review

reserve, allowance, reservation 값, host 사양, readiness 규칙 또는 LAB 목록이 바뀔 때와 승격
Task를 열기 전마다 검토한다.

## Enforcement

### Mechanisms

- `python3 scripts/operations/lab.py check <name>`가 layout, manifest, secret 경로를 검증한다.
- `tests/validation/test_lab_controller.py`의 `test_reserve_matches_policy`와
  `test_allowance_matches_policy`가 위 reserve·allowance 표와 `PROMOTION_RESERVE`,
  `PROMOTION_EXTERNAL_ALLOWANCE`의 일치를 검증한다. `test_shared_templates_declare_reservations`가
  모든 공유 template의 reservation이 limit 이하인지 검증한다.
- `tests/validation/test_lab_isolation.py`와 `tests/validation/test_lab_layout.py`가 격리와
  layout을 검증한다.

### Limits

아래 규칙은 이름 붙은 검사가 규칙에 연결되어 있지 않거나 owner의 수동 작업에 의존한다.

- promotion manifest: 강제 수단 없음 `POL-0107-R9`~`R10`, `POL-0107-R12`, `POL-0107-R14`
- secret: 수동 검토 `POL-0107-R20`, `POL-0107-R25`~`R26`; 강제 수단 없음 `POL-0107-R17`~`R19`, `POL-0107-R21`~`R24`
- 승격 목적지: 강제 수단 없음 `POL-0107-R28`~`R36`
- readiness: 강제 수단 없음 `POL-0107-R41`
- reservation: 강제 수단 없음 `POL-0107-R58`~`R62`, `POL-0107-R64`~`R67`
- owner 확인 항목: 수동 검토 `POL-0107-R68`
- Owner check items(Tier/Linux/Composition)는 `OWNER_JUDGMENT`로 보고되며 측정값도 차단도 아니고 승격 Task의 owner checklist에 의존한다.
- 측정하지 못한 readiness 값은 `NOT_RUN`이며 통과가 아니다.
- `postgresql-ha`는 측정 전이라 resources `FAIL`이며 승격 전 부하 측정이 필요하다.
- Docker는 CPU reservation을 강제하지 않고 memory reservation은 soft limit이다.
- secret 파일 복사/이동과 `SENSITIVE_ENV_VARS.md.example` 편집은 owner의 수동 작업이다.

## Ownership

### Owner

이 정책의 소유자는 frontmatter의 `owner`인 `@buenhyden`이다.

### Review Triggers

- [LAB promotion runbook](../../runbooks/15-labs/0107-lab-promotion.md)
- [LAB README](../../../../labs/README.md)
- [Domain catalog](../../README.md)
