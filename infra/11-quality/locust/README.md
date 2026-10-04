---
title: "Locust LAB 실행 이미지"
version: "1.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-05"
created: "2025-11-24"
---

<!-- [ID:11-quality:locust] -->
# Locust LAB 실행 이미지

## Overview

이 패키지는 독립 Locust LAB가 빌드하는 고정 실행 이미지만 소유한다. master,
worker, scenario, result, network 계약은 root에 포함되지 않는
[LAB Compose](../../../labs/locust.yml)가 소유한다.

## Audience

- Locust 이미지 pin을 관리하는 인프라 담당자
- 독립 LAB 진입점을 검토하는 품질 담당자
- root와 LAB 경계를 확인하는 운영자

## Scope

### In Scope

- 고정 Locust 기반 이미지
- 독립 LAB Compose가 사용하는 build context

### Out of Scope

- root **testing** profile과 HOME network·volume
- 외부 프로젝트의 업무 scenario
- 실제 target 승인, 부하 실행, 장기 결과 보존

## Structure

~~~text
locust/
├── Dockerfile # LAB 실행 이미지
└── README.md
~~~

## Tech Stack

| Category | Source | Boundary |
| --- | --- | --- |
| Runtime | [Dockerfile](Dockerfile) | 기반 이미지 tag의 권위 |
| Orchestration | [labs/locust.yml](../../../labs/locust.yml) | master/worker 전체 closure |
| Inputs | 승인된 scenario directory | 읽기 전용 mount |
| Outputs | 실행별 fresh result directory | master만 쓰기 가능 |

## Configuration

이 디렉터리는 Compose entrypoint를 갖지 않는다. 정상 root의 모든 profile과
**--profile '*'**는 Locust를 선택할 수 없다. 독립 LAB의 환경 변수, network,
volume, headless 제한은 [LAB README](../../../labs/locust.md)를 따른다.

## Validation

~~~bash
python3 -m unittest tests.validation.test_quality_mock_lab -v
~~~

이미지 build와 Locust 실행은 이번 source-only 검증에 포함되지 않는다.

## Usage

1. 이미지 tag 변경 전에 공식 release와 Python 호환성을 확인한다.
2. master/worker 옵션은 **labs/locust.yml**에서 함께 변경한다.
3. root include나 정상 HOME profile에 Locust를 다시 추가하지 않는다.
4. 변경 후 focused 테스트와 독립 LAB 정적 render를 실행한다.

## Related Documents

- [Locust LAB](../../../labs/locust.md)
- [문서 진입점](../../../docs/README.md) (`GDE-0062`, `POL-0062`, `RUN-0062`)
