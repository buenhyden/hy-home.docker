---
title: "Port contract synthetic fixtures"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-11"
created: "2026-10-11"
---

# 포트 계약 합성 입력

## Overview

운영 값 없이 포트 선언·출력 schema와 DEV/MNG 독립성을 검증하는 합성 자산입니다.

## Audience

P03 source 계약의 구현·검토 담당자입니다.

## Scope

실제 앱·DB·listener·credential·network를 생성하지 않습니다.
`example.invalid` image는 config 검증용이며 pull하거나 실행하지 않습니다.

## Structure

- `valid.json`, `invalid.json`: projector에서 복사하지 않은 schema 허용/거부 예.
- `root.yml`: 분리된 DEV/MNG 네트워크와 공개 publication 선언.
- `dev-override.yml`: DEV publication만 추가하는 Compose merge 입력.
- `env.json`: 명시적 합성 public 환경. NOISE marker는 출력 누출 거부 시험용입니다.

## Tech Stack

기존 Python unittest·jsonschema와 daemonless Docker Compose config를 사용합니다.

## Configuration

alias·host-only 변경, IPv6·UDP·범위·다중 backend 경계는 unit builder가 소유합니다.
운영 데이터, 비밀번호·인증서와 real dotenv는 이 폴더에 넣지 않습니다.

## Validation

```sh
python3 -m unittest tests.lib.ops.test_port_inventory tests.validation.test_port_contract
```

## Usage

명명된 root·override·env를 [전용 CLI](../../../scripts/operations/port-inventory.py)에
선택합니다. raw stdout/stderr와 private 값은 보고하지 않습니다.

## Related Documents

- [포트 계약](../../../infra/09-platform-ops/service-integration/README.md)
- [문서 진입점](../../../docs/README.md): owning Task는 `SPEC-0204-TSK-0011`입니다.
