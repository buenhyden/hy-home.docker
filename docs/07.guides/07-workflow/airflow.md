# Airflow System Guide

> Apache Airflow 워크플로 엔진 시스템 환경 및 운영 전반에 대한 종합 안내서.

---

## Overview (KR)

이 문서는 `hy-home.docker` 플랫폼의 Apache Airflow 시스템에 대한 가이드다. 개발자와 운영자가 시스템 아키텍처를 이해하고, 서비스 상태를 확인하며, 기본적인 파이프라인 운영을 수행할 수 있도록 돕는다.

## Guide Type

`system-guide`

## Target Audience

- **Developers**: DAG 개발 및 시스템 통합
- **Operators**: 서버 상태 모니터링 및 리소스 관리
- **AI Agents**: 자동화된 스케줄링 환경 분석

## Purpose

- Airflow 분산 아키텍처 (CeleryExecutor) 이해
- 웹 UI 및 모니터링 도구 접근 방법 확인
- 기본 개발 환경 설정 및 검증 절차 습득

## Prerequisites

- **Docker/Compose**: 로컬 실행 환경
- **Secrets**: `airflow_www_password` 등 서비스 접근 권한
- **Network**: `infra_net` 외부 통신 가능 상태

## Step-by-step Instructions

### 1. 시스템 아키텍처 이해

Airflow는 다음과 같은 분산 컴포넌트로 구성됩니다:

- **Scheduler & DAG Processor**: 작업 예약 및 DAG 파일 해석 (독립 실행으로 안정성 확보)
- **Celery Workers**: 실제 태스크가 실행되는 동적 확장 노드
- **Valkey Broker**: 스케줄러와 워커 간의 메시지 교환 (Redis 호환)
- **API Server**: UI 및 외부 통합을 위한 통합 엔드포인트

### 2. UI 접근 및 모니터링

- **Main UI**: `https://airflow.${DEFAULT_URL}` (작업 모니터링, 로그 확인)
- **Flower Dashboard**: `https://flower.${DEFAULT_URL}` (Celery 워커 부하 상태 확인)
- **Metrics**: Prometheus/Grafana를 통해 StatsD 지표 확인 가능

### 3. 개발 환경 검증

새로운 DAG를 추가하기 전에 다음 명령으로 시스템 상태를 확인합니다:

```bash
# 컨테이너 상태 확인
docker compose ps workflow

# DAG 목록 로드 확인
docker compose exec airflow-webserver airflow dags list
```

## Common Pitfalls

- **Scheduler Heavy Load**: DAG 파일 내에서 DB 쿼리나 파일 시스템 접근을 직접 수행하면 스케줄러 성능이 저하됩니다.
- **Worker Timeout**: 리소스 부족으로 워커가 종료되면 태스크가 `Queued` 상태로 멈출 수 있습니다.
- **XCom Abuse**: XCom은 작은 데이터 교환용입니다. 대용량 데이터는 S3/MinIO 등 외부 저장소를 사용하십시오.

## Related Documents

- **Spec**: [07-workflow Spec](../../04.specs/07-workflow/spec.md)
- **Operation**: [Airflow Operations Policy](../../08.operations/07-workflow/airflow.md)
- **Runbook**: [Airflow Recovery Runbook](../../09.runbooks/07-workflow/airflow.md)
