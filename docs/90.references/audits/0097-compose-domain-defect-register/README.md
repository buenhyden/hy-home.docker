---
title: "Reference: Compose Domain Defect Register"
version: 1.0.0
type: reference/audit-pack
layer: references
status: active
owner: "@buenhyden"
artifact_id: AUD-0097
parent_ids: []
created: 2026-09-04
updated: 2026-09-04
observed_at: 2026-09-04
---

# Reference: Compose Domain Defect Register

## Objective

Give four defects a current owner-facing route. Each was found while executing
SPEC-0156 and SPEC-0171, and each belongs to a service domain rather than to
either Spec's scope. Both Tasks are completed and preserved under
`docs/98.archive/completed/`, where they are frozen records; a finding that
lives only there reaches nobody.

Every finding below was re-measured against `main` at commit `612bb29b` on
2026-09-04, not carried forward on the strength of the earlier reading.

## Scope

- 포함: `infra/` 하위 Compose 선언과 이를 검사하는 `scripts/hardening/`에서
  발견된, 서비스 도메인 소유자가 판단해야 하는 결함.
- 제외: 수정 자체. 이 문서는 증거와 소유자를 기록하며, 어떤 파일도 바꾸지
  않는다. 이미 해소된 결함(k6와 locust의 host port 18089 중복,
  `depends_on`이 profile 경계를 넘던 7건)은 SPEC-0156과 SPEC-0171이 닫았으므로
  여기에 없다.

## Criteria

| ID | Criterion |
| :--- | :--- |
| CDR-01 | A hardening assertion names a value that exists in the file it checks. |
| CDR-02 | A service address names a service some Compose file declares. |
| CDR-03 | Two services selected by one plausible profile combination do not publish the same host port. |
| CDR-04 | A service that declares `build:` has a build context that can produce an image, and runs the program its directory names. |

## Evidence

각 항목은 `main` `612bb29b`에서 재현한 명령과 출력이다.

### CDR-01

```bash
grep -n 'valkey/valkey:' infra/02-auth/oauth2-proxy/docker-compose.yml
#   76:    image: valkey/valkey:9.1.1-alpine
grep -n 'valkey/valkey:9.1.0-alpine' scripts/hardening/check-all-hardening.sh
#  339:  check_contains "$oauth_full_compose" "image: valkey/valkey:9.1.0-alpine" ...
```

### CDR-02

```bash
grep -n 'redis.addr' infra/07-workflow/n8n/docker-compose.yml
#  307:          -redis.addr=redis://mng-n8n-valkey:${VALKEY_PORT} \
```

렌더링된 union 모델에서 `mng-n8n-valkey`라는 서비스는 존재하지 않으며,
선언된 이름은 `n8n-valkey`다.

### CDR-03

```bash
COMPOSE_PROFILES="$(docker compose config --profiles | tr '\n' ,)" \
  docker compose config --format json
```

union 138개 서비스에서 host port가 겹치는 조합은 3건이고, 그중 2건은
`nginx` ↔ `traefik`의 80·443으로 POL-0078이 상호 배타 쌍으로 등록한 의도된
구성이다. 나머지 1건이 결함이다.

| Host port | Services | Profiles |
| :--- | :--- | :--- |
| 8000 | `kong` (supabase) | `data` |
| 8000 | `surrealdb` (open-notebook) | `admin`, `dev` |

`data`와 `dev`는 함께 고를 수 있는 조합이므로 도달 가능한 충돌이다.

### CDR-04

```bash
ls infra/09-tooling/k6/
#  README.md  docker-compose.yml
grep -n 'build:\|command:' infra/09-tooling/k6/docker-compose.yml
#   21:    build: .
#   31:    command: locust -f /mnt/locust/locustfile.py --master
```

`build: .`이 가리키는 디렉터리에 Dockerfile이 없고, 서비스 이름은 `k6-master`인데
실행하는 프로그램은 locust다. `infra/09-tooling/locust/`에는 Dockerfile이 있다.

## Findings

| ID | Severity | Finding | Owner |
| :--- | :--- | :--- | :--- |
| CDR-04 | high | `infra/09-tooling/k6/`는 locust 파일의 복사본이다. Dockerfile 없이 `build: .`을 선언하므로 `tooling` 또는 `testing` profile로 기동하면 빌드가 실패한다. | `09-tooling` |
| CDR-03 | high | `kong`과 `surrealdb`가 host 8000을 함께 공개한다. `data dev` 조합을 고르면 둘 중 하나가 뜨지 못한다. | `04-data`, `11-laboratory` |
| CDR-02 | medium | `n8n-valkey-exporter`가 존재하지 않는 호스트 `mng-n8n-valkey`를 스크레이프한다. exporter는 기동하지만 메트릭을 얻지 못한다. | `07-workflow` |
| CDR-01 | medium | hardening 검사가 valkey 9.1.0을 기대하지만 파일은 9.1.1이다. `check-all-hardening.sh`는 `set -euo pipefail`과 `fail()`의 `exit 1` 때문에 **첫 실패에서 멈추므로**, 이 항목 뒤의 모든 검사가 실행되지 않는다. | `02-auth` |

CDR-01의 실질 영향은 태그 하나의 불일치보다 크다. 스위트가 중단되면서 그 뒤
tier의 검사가 전혀 돌지 않으며, 이 상태는 이 문서를 쓰는 시점 이전부터
`main`에서 재현된다.

## Conformance

| Criterion | Verdict |
| :--- | :--- |
| CDR-01 | fail |
| CDR-02 | fail |
| CDR-03 | fail |
| CDR-04 | fail |

네 항목 모두 불합격이며, 어느 것도 CI gate를 붉게 만들지 않는다.
`run-ci-gate.py --profile full`은 `612bb29b`에서 exit 0이고,
`validate-docker-compose.sh`는 28개 profile을 모두 렌더링한다. 이들 결함은
정적 렌더링이 아니라 `up` 시점 또는 hardening 스위트에서만 드러난다.

## Actions

각 항목은 소유 도메인의 판단이 필요하며, 이 문서는 그 판단을 대신하지 않는다.

| ID | Action | 판단이 필요한 이유 |
| :--- | :--- | :--- |
| CDR-01 | 검사의 기대값을 9.1.1로 올리거나 이미지를 9.1.0으로 되돌린다. | 어느 쪽이 의도였는지는 이미지 버전 결정이며, 검사를 파일에 맞추면 의도한 고정을 지울 수 있다. |
| CDR-02 | `-redis.addr`을 `n8n-valkey`로 고친다. | 단순 오타로 보이지만 `dedicated-valkey` profile을 쓰지 않을 때의 올바른 대상이 무엇인지는 도메인 결정이다. |
| CDR-03 | 한쪽의 host port를 재배정하거나 두 profile을 배타로 선언한다. | 이미 가동 중일 수 있는 스택의 공개 포트를 바꾸는 일이라 외부에 영향이 간다. |
| CDR-04 | k6를 실제로 k6로 만들거나, 디렉터리를 제거하고 locust만 남긴다. | 두 부하 시험 도구를 모두 유지할 의도였는지가 선행 질문이다. |

## Traceability

| Reference | Relation |
| :--- | :--- |
| [SPEC-0156](../../../98.archive/completed/03.specs/0156-compose-enablement-model-convergence/spec.md) | CDR-03, CDR-04를 발견한 변경 |
| [SPEC-0171](../../../98.archive/completed/03.specs/0171-compose-sibling-pair-resolution/spec.md) | CDR-01, CDR-02를 발견한 변경 |
| [POL-0078](../../../05.operations/catalog/00-workspace/0078-compose-profile-vocabulary/policy.md) | profile 어휘와 상호 배타 쌍의 현행 권위 |
| [Compose profile service coverage](../../data/0059-compose-profile-service-coverage/README.md) | 서비스와 profile의 생성된 스냅샷 |

## Related Documents

- [Audits index](../README.md)
- [Compose, Infrastructure, and Operations Readiness](../0022-compose-infrastructure-operations-readiness/README.md)
- [Operations catalog](../../../05.operations/catalog/README.md)
