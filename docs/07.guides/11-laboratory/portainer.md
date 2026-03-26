# Portainer System Guide

> Docker 환경 관리 및 컨테이너 오케스트레이션 UI 활용 가이드.

---

## Overview (KR)

이 문서는 Portainer를 사용하여 로컬 및 원격 Docker 환경을 관리하는 방법을 설명한다. 웹 인터페이스를 통한 실시간 모니터링, 로그 분석, 볼륨/네트워크 관리 절차를 포함한다.

## Guide Type

`system-guide | how-to`

## Step-by-step Instructions

### 1. Initial Admin Setup

1. `https://portainer.${DEFAULT_URL}`에 처음 접속하면 관리자 계정 생성 화면이 나타난다.
2. 강력한 비밀번호를 설정한다 (최소 12자 권장).
3. 'Get Started'를 클릭하여 로컬 환경을 자동으로 연결한다.

### 2. Managing Containers

1. 왼쪽 메뉴에서 'Containers'를 선택한다.
2. 특정 컨테이너를 클릭하여 'Logs', 'Inspect', 'Stats' 기능을 활용한다.
3. 'Add container' 기능을 사용하여 임시 어위(Ad-hoc) 컨테이너를 생성할 수 있다 (운영 시에는 주로 Docker Compose 사용 권장).

### 3. Stack Deployment

1. 'Stacks' 메뉴에서 Docker Compose 파일을 직접 업로드하거나 붙여넣어 배포할 수 있다.
2. `infra/` 폴더의 서비스 수정 시에는 터미널에서 `docker compose` 명령을 사용하는 것이 형상 관리 측면에서 권장된다.

## Best Practices

- **Resource Limits**: 컨테이너 생성 시 CPU/Memory 제한을 설정하여 시스템 전체의 안정성을 확보하라.
- **Pruning**: 정기적으로 'Images' 메뉴에서 Unused 이미지를 삭제하여 디스크 공간을 관리하라.
- **Network Isolation**: 서비스 간 통신은 가급적 전용 네트워크를 사용하고 Portainer에서 이를 시각적으로 확인하라.

## Common Pitfalls

- **Docker Socket Availability**: `/var/run/docker.sock` 볼륨 바인딩이 누락되거나 권한이 없을 경우 Portainer가 로컬 환경을 인식하지 못한다.
- **SSO Double Auth**: Traefik `sso-auth`와 Portainer 내부 인증이 중복되므로, SSO 로그인 후 Portainer 로그인도 수행해야 함을 인지하라.

## Related Documents

- **Implementation**: `[../../../infra/11-laboratory/portainer/README.md]`
- **Operation**: `[../../08.operations/11-laboratory/portainer.md]`
- **Runbook**: `[../../09.runbooks/11-laboratory/portainer.md]`
