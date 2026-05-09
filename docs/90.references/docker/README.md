# Docker Tech Stack References

## 목적

이 폴더는 Docker 런타임 이미지와 버전 검증에 필요한 기준 정보를 저장한다.

## 포함할 내용

- 중요한 Docker 이미지 버전 레지스트리 설명
- 버전 drift 검증 절차
- floating tag 예외 정책 링크
- Compose image 선언과 문서 버전의 비교 기준

## 포함하지 말아야 할 내용

- 배포 절차
- 서비스별 운영 runbook
- 새 이미지 업그레이드 실행 계획

## 권장 하위 구조

- 현재는 README만 유지한다.
- 상세 버전 레지스트리는 `infra/tech-stack.versions.json`에 둔다.

## 운영 규칙

1. Compose 파일이 Docker 런타임의 source of truth다.
2. `infra/tech-stack.versions.json`은 주요 이미지가 Compose에 실제로 선언되어 있는지 확인하는 drift gate다.
3. 새 주요 운영 이미지가 추가되면 registry에 component, tier, image, compose file을 추가한다.
4. floating tag는 `infra/image-tag-policy.exceptions.json`에 승인 예외가 있을 때만 허용한다.

## 예시

- Airflow 기본 이미지는 Compose의 `${AIRFLOW_IMAGE_NAME:-apache/airflow:3.1.8}` 기본값으로 검증한다.
- n8n은 custom runtime image와 external runner image를 함께 registry에 둔다.

## Related Documents

- [references index](../README.md)
- [image tag exceptions](../../../infra/image-tag-policy.exceptions.json)
- [tech stack versions](../../../infra/tech-stack.versions.json)
- [repo contract checker](../../../scripts/check-repo-contracts.sh)

---

## Overview

`docs/90.references/docker`는 느리게 변하는 참고 지식과 외부 기준을 관리하는 reference 위치다. 이 README는 하위 파일을 찾는 진입점이며, 기존 본문과 실제 디렉터리 구조를 함께 기준으로 사용한다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- reference facts, glossary, roadmap
- 느리게 변하는 기준 정보
- 관련 stage 문서 링크

### Out of Scope

- 실시간 운영 절차
- incident 사실 기록
- runtime 설정 원문

## Structure

```text
docs/90.references/docker/
└── README.md  # This file
```

## How to Work in This Area

1. 참고 정보가 active policy나 runbook을 대체하지 않는지 확인한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.
