<!-- Target: docs/07.guides/11-laboratory-user-guide.md -->

# User Guide - 11-laboratory

## Overview (KR)
이 문서는 `11-laboratory` 계층에서 제공하는 관리 도구들을 사용하는 사용자를 위한 가이드이다. 통합 대시보드(Homer), 컨테이너 관리(Portainer), 데이터베이스 시각화(RedisInsight) 도구의 접속 및 기본 사용법을 설명한다.

## Services Access

### 1. 통합 인프라 대시보드 (Homer)
모든 인프라 서비스의 진입점이다.
- **URL**: `https://homer.${DEFAULT_URL}`
- **기능**: 등록된 모든 서비스의 상태 확인 및 원클릭 바로가기 제공.

### 2. 컨테이너 관리 센터 (Portainer)
Docker 컨테이너 환경을 시각적으로 관리한다.
- **URL**: `https://portainer.${DEFAULT_URL}`
- **사용법**: 
    - **Stacks/Containers**: 실행 중인 서비스 목록 확인 및 로그 실시간 모니터링.
    - **Images**: 미사용 이미지 정리 및 신규 이미지 풀링.
    - **Console**: 브라우저에서 즉시 컨테이너 내부 쉘 접근.

### 3. 데이터 시각화 도구 (RedisInsight)
Redis/Valkey 데이터 저장소를 분석한다.
- **URL**: `https://redisinsight.${DEFAULT_URL}`
- **사용법**: 
    - `04-data` 티어의 `redis` 연결 정보를 입력하여 접속.
    - 키 분포 분석 및 CLI 명령 실행.

## Security Notice
- 모든 도구는 Keycloak SSO 로그인이 필요하다.
- 공용 PC 사용 시 사용 후 반드시 브라우저를 종료하거나 로그아웃한다.
