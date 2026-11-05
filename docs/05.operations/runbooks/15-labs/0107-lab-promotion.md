---
title: "LAB Promotion Runbook"
version: "0.1.0"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-05"
layer: "operations"
artifact_id: "RUN-0107"
parent_ids:
- "POL-0107"
created: "2026-11-05"
---

# LAB Promotion Runbook

## Overview

LAB을 `infra/`로 승격하는 readiness 검사 실행과 세 승격 절차 `add`, `replace-same`,
`replace-substitute`를 다룬다. 통제 기준은 [POL-0107](../../policies/15-labs/0107-lab-promotion.md),
계약은 [SPEC-0263](../../../03.specs/0263-lab-promotion-contract/spec.md) section 5–6이다.

SPEC-0263은 아무 LAB도 승격하지 않는다. 이 런북은 이후 승격 Task가 따를 절차이며, 문서화는
어떤 실행 승인도 주지 않는다.

## Trigger

LAB의 `promotion.yaml`이 `undecided`가 아닌 kind를 선언하고 owner가 그 LAB의 승격 Task를 연 때
사용한다. readiness 검사 자체는 HOME 상태를 읽기만 하므로 승격 여부를 판단하려 할 때 언제든 쓴다.

## Prerequisites

- 승격 Task가 있고, 그 Task가 대상 LAB, kind, 목적지와 운영 window를 기록한다.
- **HOME runtime을 건드리는 모든 단계(기동, 정지, 재생성, 데이터 export·import, 소비자 전환,
  은퇴)는 owner가 승인한 운영 window 안에서만 실행한다.** 이 런북의 명령 목록은 승인이 아니다.
- `labs/.env`에 대상 LAB의 필수 입력(`LAB_DATA_DIR`과 LAB별 입력)이 있다. agent는 이 파일과
  `secrets/`를 읽지 않는다.
- 대체 승격이면 은퇴할 서비스의 최신 backup과 격리 복원 증거가 있다.

## Procedure

### Readiness run

repository root에서 실행한다. 이 명령은 LAB과 root render, `docker info`, `docker inspect`, disk
사용량만 읽고 아무것도 시작하지 않는다.

```bash
python3 scripts/operations/lab.py --env-file labs/.env readiness <name> --report <path>
```

보고서는 JSON이며 `lab`, `kind`, `result`, `criteria`를 갖는다. `criteria`의 다섯 기준은
`tier`, `composition`, `linux`, `docker`, `resources`이고 각각 `result`, `values`, `problems`를
갖는다. `values`의 값마다 측정값 `value`와 출처 `source`가 붙는다.

| 종료 코드 | 의미 |
| --- | --- |
| 0 | 다섯 기준이 모두 `PASS` |
| 1 | Docker 또는 Compose 실패(render 거부 포함); 보고서를 쓰지 않는다 |
| 2 | 잘못된 입력(알 수 없는 LAB, manifest 없음, 읽을 수 없는 catalog 등); 보고서를 쓰지 않는다 |
| 3 | 하나 이상의 기준이 `FAIL` 또는 `NOT_RUN` |

종료 코드가 0이 아니면 승격을 멈추고 보고서와 종료 코드를 승격 Task에 기록한다. `NOT_RUN`은
측정하지 못한 값이며 통과가 아니다.

### add

1. 목적지 규칙에 따라 Compose, README, 자산, Guide·Runbook을 옮긴다. 문서는 artifact 식별자와
   생성일을 유지하고 `git mv`로 옮긴다. 상대 경로는 새 폴더 기준으로 다시 맞춘다.
2. manifest의 `integrations`를 연결한다(gateway route, OIDC client, DB role, observability,
   OpenBao 전달, 공유 network).
3. secret을 옮기지 않고 은퇴시킨다. 아래 [Secret retirement](#secret-retirement)를 따른다.
4. readiness 검사를 실행한다. 0이 아니면 멈춘다.
5. root render와 관련 test를 실행한다.
6. 승인된 운영 window에서 서비스를 시작하고 health와 사용자 기능을 확인한다.
7. `promotion.yaml`을 삭제하고 그 사실을 승격 Task에 기록한다.

### replace-same

`add`의 모든 단계에 다음을 더한다. 6단계(기동)는 아래 순서 안에서 실행한다.

#### Consumer inventory

1. manifest `replaces[].consumers`를 시작점으로 `git grep`으로 은퇴 서비스의 이름, host, port,
   secret, network를 참조하는 모든 파일을 찾는다.
2. 소비자마다 연결 방식, 전환 순서, 중단 허용 여부를 승격 Task에 표로 기록한다.

#### Data migration

1. **Export.** 승인된 window에서 writer를 멈추거나 합의한 일관성 지점을 정한다. 엔진 공식
   방식으로 export하고 파일, 크기, checksum manifest를 남긴다.
2. **Import.** 새 서비스에 import한다. 이전 서비스의 identity 파일(cluster ID, node ID 등)은
   재사용하지 않는다.
3. **Verify.** 객체 수, key·topic·index 목록, 표본 값과 애플리케이션 read를 export manifest와
   비교한다. 불일치가 있으면 cutover하지 않는다.

#### Cutover

1. inventory 순서대로 소비자 하나씩 새 서비스로 전환하고 각 전환 뒤 기능을 확인한다.
2. 전환하는 동안 이전 서비스와 데이터는 정지만 하고 삭제하지 않는다.

#### Rollback

1. 소비자를 이전 서비스로 되돌리고 이전 서비스를 보존한 데이터로 다시 시작한다.
2. cutover 이후 새 서비스에만 쓰인 데이터가 있으면 그 범위를 Task에 기록하고 owner가 처리를
   결정한다. 실패한 새 서비스의 데이터는 보존한다.

#### Retirement

새 서비스가 검증되고 rollback window가 끝난 뒤에만 은퇴 서비스를 Compose에서 제거한다. 그
데이터는 [POL-0021](../../policies/10-platform-and-backup/0021-backup-and-restore.md)의 보존
기간을 따르며, 삭제는 별도 승인이다. 은퇴 서비스의 secret도 아래 절차로 정리한다.

### replace-substitute

`replace-same`의 모든 단계에 다음을 더한다. 제품이 다르므로 export와 import 사이에 변환이 있다.

#### Configuration and data format mapping

1. 이전 제품의 설정 키마다 새 제품의 대응 키, 기본값 차이, 대응이 없는 키를 표로 만든다.
2. 데이터 형식(schema, type, encoding, index·topic 구조)의 대응과 변환 도구를 정한다. 손실되는
   속성은 명시하고 owner가 승인한다.
3. 소비자 측 protocol·client 차이와 필요한 코드·설정 변경을 inventory에 더한다.
4. Data migration의 Verify는 변환 뒤 값으로 비교한다.

### Secret retirement

LAB secret 값은 승격하지 않는다. 승격된 서비스는 manifest `secrets[].destination`의 `infra`
secret을 쓴다.

1. agent가 `infra/03-security/openbao/secret-catalog.json`에서 LAB 행을 은퇴시키고 목적지 `root`
   행을 만들거나 기존 행에 소비자를 더한다.
2. `secrets/SENSITIVE_ENV_VARS.md.example`은 생성되지 않는다. `load_catalog`가 catalog와의 일치를
   요구하므로 owner가 agent가 준비한 행을 손으로 편집한다.
3. owner가 controller venv를 `PATH` 맨 앞에 두고 확인 후 동기화한다.

   ```bash
   PATH="$HOME/.local/share/hy-home/controller-venv-py312/bin:$PATH" bash scripts/operations/gen-secrets.sh --sync-metadata-check
   PATH="$HOME/.local/share/hy-home/controller-venv-py312/bin:$PATH" bash scripts/operations/gen-secrets.sh --sync-metadata
   ```

4. `--sync-metadata-prune`은 private registry가 COMM-003을 갖고 있는 동안 막힌다. COMM-003은
   SMTP01 은퇴(`--retire-supabase-smtp`, [RUN-0029](0029-supabase.md))만 제거한다.
5. catalog를 검사한다. root는 절대 경로여야 하므로 `.`이 아니라 `--root "$PWD"`를 쓴다.

   ```bash
   python3 scripts/operations/secret-catalog.py check --root "$PWD"
   ```

6. owner가 LAB 사본 파일을 제거한다.

## Verification

승격 Task에 readiness 보고서, 종료 코드, source revision, export manifest 요약, verify 결과,
소비자별 전환 결과, rollback window와 은퇴 시점을 기록한다. secret 값, raw payload와 rendered
private 설정은 기록하지 않는다.

## Failure and Recovery

### Rollback or Recovery

각 대체 절차의 Rollback을 따른다. 이전 서비스와 데이터는 Retirement 전까지 삭제하지 않으므로
언제든 되돌릴 수 있어야 한다. `add`는 새 서비스를 정지하고 root include를 되돌린다.

### Escalation

readiness가 0이 아니거나, verify가 불일치하거나, 소비자 전환이 실패하거나, 데이터·secret 소유가
불명확하면 멈추고 @buenhyden에게 보고서와 실패 신호를 전달한다.

## Related Documents

### Traceability

- Contract: [SPEC-0263](../../../03.specs/0263-lab-promotion-contract/spec.md) section 5–6.
- Implementation: `scripts/operations/lab.py` `readiness`.
- Artifact: `RUN-0107`; parent: `POL-0107`.

- [LAB promotion policy](../../policies/15-labs/0107-lab-promotion.md)
- [LAB README](../../../../labs/README.md)
- [Domain catalog](../../README.md)
