# Workflow & Orchestration Guides

> 데이터 파이프라인 및 자동화 워크플로 관리 가이드 모음.

## Overview

이 디렉터리는 `hy-home.docker` 플랫폼에서 사용하는 워크플로 엔진(Airflow, n8n 등)의 사용법과 개발 가이드를 포함합니다. 파이프라인 설계, 노드 활용, 그리고 플랫폼 특정 도구와의 연동 방법을 설명합니다.

## Audience

이 README의 주요 독자:

- **Developers**: 자동화 시나리오 및 DAG 개발자
- **Data Engineers**: 데이터 수집 및 처리 프로세스 설계자
- **AI Agents**: 워크플로 분석 및 최적화 에이전트

## Scope

### In Scope

- **Apache Airflow**: Python 기반의 복잡한 데이터 파이프라인 개발 가이드
- **n8n**: 노드 기반의 로우코드 자동화 워크플로 활용법
- 시스템 아키텍처 이해 및 로컬 개발 환경 설정 가이드

### Out of Scope

- 운영 서버의 커스터마이징 설정 (08.operations 권한)
- 클러스터 복구 및 백업 절차 (09.runbooks 권한)

## Structure

```text
07-workflow/
├── 01.airflow-dag-dev.md  # Airflow DAG 개발 표준 및 기법
├── 02.n8n-automation.md   # n8n 노드 활용 가이드
├── airflow.md               # Airflow 시스템 가이드 (시스템 가이드)
├── n8n.md                   # n8n 시스템 가이드 (시스템 가이드)
├── 01.airflow-dag-dev.md    # Airflow DAG 개발 및 배포 절차
└── 02.n8n-automation.md     # n8n을 이용한 자동화 워크플로우 구성
```

## How to Work in This Area

1. [v2026.03 표준 템플릿](../../99.templates/guide.template.md)을 사용하여 문서를 작성합니다.
2. 각 문서 최상단에는 **Overview (KR)** 섹션을 필수로 포함합니다.
3. 관련 [운영 정책](../../08.operations/07-workflow/README.md) 및 [런북](../../09.runbooks/07-workflow/README.md)과의 링크를 유지합니다.

## Related References

- **PRD**: [07-workflow PRD](../../01.prd/README.md)
- **Spec**: [07-workflow Spec](../../04.specs/README.md)
- **Operation**: [Workflow Operations](../../08.operations/07-workflow/README.md)
