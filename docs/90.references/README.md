# 90.references

> 느리게 변하는 기준 지식, 표준, 인벤토리, 학습 로드맵을 관리하는 reference stage

## Overview

`docs/90.references`는 느리게 변하는 참고 지식과 외부 기준을 관리하는 reference 위치다. 이 README는 하위 reference 문서를 찾는 진입점이며, active policy, plan, runbook을 대체하지 않는다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- 용어집, 외부 표준 요약, 시스템 인벤토리
- 아키텍처 개념 참고, 공통 FAQ, Agent 관련 개념 요약
- Docker 이미지/version drift 기준
- 학습 로드맵과 이론 참고 문서
- 느리게 변하는 기준 정보
- 관련 stage 문서 링크

### Out of Scope

- 현재 진행 중인 설계 의사결정
- 실행 계획
- 운영 절차
- 실시간 운영 절차
- incident 사실 기록
- runtime 설정 원문

## Structure

```text
docs/90.references/
├── docker/  # 하위 구성 영역
├── learning/  # 하위 구성 영역
└── README.md  # This file
```

## Current References

- [docker/README.md](./docker/README.md) - Docker 이미지 버전 drift 검증 기준
- [learning/README.md](./learning/README.md) - Docker 기반 인프라 학습 로드맵과 이론 참고

## Templates

- [../99.templates/reference.template.md](../99.templates/reference.template.md)

## How to Work in This Area

1. 참고 정보가 active policy나 runbook을 대체하지 않는지 확인한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.

## Related Documents

- [docs index](../README.md)
- [reference template](../99.templates/reference.template.md)
- [docker reference](./docker/README.md)
- [learning reference](./learning/README.md)
