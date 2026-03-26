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

- Portainer를 통한 컨테이너 리소스 관리 최적화.
- RedisInsight를 활용한 데이터 분석 및 스트림 모니터링 활성화.
- Homer 대시보드를 통한 직관적인 서비스 네비게이션 구축.

## Prerequisites

- [Traefik](../01-gateway/README.md) 활성화 및 로컬 도메인 설정.
- [SSO Auth](../02-auth/README.md) 미들웨어 구성 완료.

## Step-by-step Instructions

### 1. Adding New Services to Homer
1. `infra/11-laboratory/dashboard/config/config.yml` 파일을 연다.
2. `services` 섹션에 새로운 그룹 또는 아이템을 추가한다:
   ```yaml
   - name: "My New Service"
     icon: "fas fa-server"
     url: "https://newservice.home.local"
   ```
3. 변경 사항을 저장하면 Homer 컨테이너가 볼륨 바인딩을 통해 자동으로 반영한다.

### 2. Monitoring Redis with RedisInsight
1. 브라우저에서 `redisinsight.${DEFAULT_URL}`에 접속한다.
2. 'Add Redis Database'를 클릭한다.
3. 호스트명(예: `redis` 또는 IP), 포트(6379)를 입력하고 연결을 저장한다.
4. 'Key Analyzer'를 실행하여 메모리 사용량을 분석한다.

## Common Pitfalls

- **Homer Config Syntax**: YAML 문법이 틀릴 경우 대시보드가 로드되지 않는다. 정적 분석기로 유효성을 먼저 검증하라.
- **Portainer Sock Permission**: `/var/run/docker.sock` 접근 권한 속성 문제로 컨테이너가 시작되지 않을 수 있다.

## Related Documents

- **Implementation**: `[../../../infra/11-laboratory/README.md]`
- **Operation**: `[../../08.operations/11-laboratory/README.md]`
- **Runbook**: `[../../09.runbooks/11-laboratory/README.md]`
