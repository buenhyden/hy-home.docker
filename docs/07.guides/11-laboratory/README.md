# Laboratory (11-laboratory) Guide

> 실험 및 관리용 서비스 그룹인 Laboratory 티어의 효율적인 활용 및 구성 가이드.

---

## Overview (KR)

이 문서는 `11-laboratory` 티어에 포함된 관리 도구(Portainer, RedisInsight)와 서비스 대시보드(Homer)의 설정 및 활용 방법을 설명한다. 운영 환경 내 도구 접근성을 높이고 데이터를 시각화하는 절차를 제공한다.

## Guide Type

`system-guide | how-to`

## Target Audience

- Operator (인프라 관리)
- Developer (데이터 조회 및 컨테이너 분석)
- AI Agent (인프라 매핑 및 자동화)

## Purpose

- [Portainer Guide](./portainer.md): Docker environment and container management.
- [RedisInsight Guide](./redisinsight.md): Redis visualization and analysis.
- [Dozzle Guide](./dozzle.md): Real-time log viewer for Docker containers.
- [Homer Dashboard](./dashboard.md)를 통한 직관적인 서비스 네비게이션 구축.

## Prerequisites

- [Traefik](../01-gateway/README.md) 활성화 및 로컬 도메인 설정.
- [SSO Auth](../02-auth/README.md) 미들웨어 구성 완료.

## Step-by-step Instructions

1. [Portainer Guide](./portainer.md)를 참고하여 컨테이너 환경을 연결한다.
2. [Dashboard Guide](./dashboard.md)를 참고하여 `config.yml` 파일을 수정한다.
3. [Dozzle Guide](./dozzle.md)를 참고하여 실시간 로그를 모니터링한다.

### 2. Monitoring Redis with RedisInsight

1. [RedisInsight Guide](./redisinsight.md)를 참고하여 데이터베이스를 연결하고 분석한다.

## Common Pitfalls

- **Homer Config Syntax**: YAML 문법이 틀릴 경우 대시보드가 로드되지 않는다. 정적 분석기로 유효성을 먼저 검증하라.
- **Portainer Sock Permission**: `/var/run/docker.sock` 접근 권한 속성 문제로 컨테이너가 시작되지 않을 수 있다.

## Related Documents

- **Implementation**: `[../../../infra/11-laboratory/README.md]`
- **Portainer Guide**: `[./portainer.md]`
- **RedisInsight Guide**: `[./redisinsight.md]`
- **Dozzle Guide**: `[./dozzle.md]`
- **Dashboard Guide**: `[./dashboard.md]`
- **Operation**: `[../../08.operations/11-laboratory/README.md]`
- **Runbook**: `[../../09.runbooks/11-laboratory/README.md]`
