---
title: "서비스 연결 포트 계약"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-11"
created: "2026-10-11"
---

# 서비스 연결·포트 계약

## Overview

포트 선언을 listener, 내부 DNS, 호스트 publication, Traefik backend로 나눠
검토하는 비밀값 없는 출력 계약입니다. 서비스 등록표는 기존
`current-service-inventory`와 그 생성기가 계속 소유합니다.

## Audience

서비스 소비자, ingress와 네트워크 연결을 검토하는 담당자입니다.

## Scope

공개 root include closure 및 명시적으로 선택한 합성 root+override만 다룹니다.
선언됨·실행 중·정상·실사용·복구됨은 별개입니다. `ports`·`expose`를 실제
listener나 인증·회복 증거로 바꾸지 않습니다. 실제 listener 관측은 이 초기
schema에서 모두 unknown이며, 차후 정확한 대상과 별도 관측 계약이 필요합니다.

## Structure

- [port-contract.schema.json](port-contract.schema.json): 알 수 없는 필드를 거부하는 1.0.0 출력 형식.
- [port_inventory.py](../../../scripts/lib/ops/port_inventory.py): 순수 선언 projector와 bounded 공개 source 및 합성 렌더 경계.
- [port-inventory.py](../../../scripts/operations/port-inventory.py): 값이 제거된 JSON만 출력하는 CLI.
- [합성 fixture](../../../tests/fixtures/port-contract/README.md): handwritten 허용/거부 예와 DEV/MNG 입력.

## Tech Stack

기존 Python·PyYAML·jsonschema와 Docker Compose `config`를 재사용합니다.
이미지 pull, 서비스 기동, secret 발급 또는 저장소 이동을 수행하지 않습니다.

## Configuration

listener는 관측이 없으므로 unknown입니다. 내부 DNS는 network의 논리 key와
실제 선언 이름을 분리하고 서비스 이름·alias 위치·포트/프로토콜을 보존합니다.
프로젝트 접두사가 필요한 실제 network 이름과 미해결 표현식은 null/unknown으로
표시합니다. alias 표현식 원문 대신 `alias_index`를 보존합니다.

호스트 publication은 IP, target/published 범위, TCP/UDP, mode를 분리합니다.
단축형의 동등 길이 범위는 paired-range, 장형의 가용 published 범위는 pool이며
자동 호스트 포트는 automatic입니다. publication이 없는 경우는 unpublished입니다.
`host_ip_state`는 IP 선언 누락(absent), 변수 미해결(unknown), 선언된 IP(declared)를
구분합니다. 장형 `name`·`app_protocol`은 주소 계약 밖의 추가 설명이므로 출력하지
않습니다. 연결 감사에서 이 설명을 소비하면 별도 소유 계약으로 다룹니다.
Traefik의 HTTP/TCP/UDP backend 선언은 각 이름·network·port·scheme을 보존하고,
`network_state`로 선택 network 누락·미해결·선언을 구분합니다. `h2c`도 선언으로
허용하며 network 미연결과 disabled를 구분합니다. 외부 File-provider endpoint와
암시적 포트 탐지는 이 Docker-label 초기 slice의 수용 범위 밖입니다.

출력에 environment 값, command, 임의 label, secret payload, route rule,
raw Compose render와 stderr를 포함하지 않습니다. 허용된 포트 metadata에도
개인 식별자가 들어갈 수 있으므로 검토한 공개 입력만 사용합니다.

## Validation

```sh
python3 -m unittest tests.lib.ops.test_port_inventory tests.validation.test_port_contract
```

스키마 통과는 endpoint 도달·listener·TLS·OIDC·machine auth·ACL·HOME·복구의
성공을 증명하지 않습니다. 실제 시험 결과와 SHA는 owning Task가 소유합니다.
입력 수용은 순수 `validate_contract(document, schema)`로 JSON Schema 구조 검사와
서비스·증거 경로 중복, 범위 순서, IP·상태·할당 정합을 함께 검사합니다. 구조 검사만으로
서비스 이름 유일성을 증명하지 않습니다. schema 참조는 문서 내부만 허용하며 외부
조회는 수행하지 않습니다. DNS 조합은 생성 전에 4,096개로 제한하며 config stdout와
stderr는 수집 중 각각 1 MiB로 제한하고 stderr는 폐기합니다. 문서 전체의 DNS·host·backend
endpoint 합도 생성 전에 16,384개로 제한합니다. 이 한도는 서비스 수 상수가 아닙니다.

## Usage

```sh
python3 scripts/operations/port-inventory.py
python3 scripts/operations/port-inventory.py \
  --synthetic-root tests/fixtures/port-contract/root.yml \
  --override tests/fixtures/port-contract/dev-override.yml \
  --synthetic-env tests/fixtures/port-contract/env.json
```

기본 source mode는 기존 `expected_from_root` closure와 bounded no-follow reader를
사용하며 dotenv·환경 치환·Docker를 실행하지 않습니다. 합성 mode는 fixture
폴더의 명명된 입력만 허용합니다. 파일의 SHA를 기록하고 private 임시 디렉터리의
명시적 public env만 사용합니다. ambient HOME/COMPOSE/DOCKER 환경, include,
mount, env_file, build, 외부 network를 거부하며 config 실행 시간을 제한합니다.
raw 렌더는 반환하거나 저장하지 않습니다. override의 실제 Compose merge 의미를
보존하며, 예제는 DEV publication 추가입니다. 실제 호스트 포트 변경 절차는 아닙니다.

공통 manifest·workflow 등록, 상위 README 탐색과 운영 문서 정합은 총괄의
단일 통합 대상으로 남습니다. P01/P02의 최종 secret/ACL/reload, SEC01의 이미지
보안 수용, P04/P05의 실제 worker, CLN01의 폐기 판단을 대신하지 않습니다.

## Related Documents

- [문서 진입점](../../../docs/README.md): owning Task `SPEC-0204-TSK-0011`과
  기존 m0021 `current-service-inventory`의 문서 소유 경계를 참조합니다.
- [Docker 포트 선언](https://docs.docker.com/reference/compose-file/services/#ports)
- [Traefik Docker backend](https://doc.traefik.io/traefik/reference/dynamic-configuration/docker/)
