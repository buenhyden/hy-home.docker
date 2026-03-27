# Dozzle Guide

> Real-time log viewer for Docker containers.

---

## Overview (KR)

이 문서는 Dozzle을 사용하여 Docker 컨테이너의 로그를 실시간으로 모니터링하고 검색하는 방법을 설명하는 가이드다. 별도의 복잡한 설정 없이 웹 UI를 통해 모든 컨테이너의 로그 스트림에 접근할 수 있다.

## Guide Type

`how-to | system-guide`

## Target Audience

- Developer (Service debugging and log analysis)
- Operator (Health monitoring)

## Purpose

Dozzle을 통해 인프라 내 컨테이너 로그를 효율적으로 확인하고 문제 발생 시 빠르게 원인을 파악한다.

## Prerequisites

- [Traefik](../../01-gateway/README.md) 활성화 및 로컬 도메인 설정.
- [SSO Auth](../../02-auth/README.md)를 통한 인증 및 인가 완료.

## Step-by-step Instructions

1. **Access Dozzle**: 브라우저에서 `https://dozzle.${DEFAULT_URL}`에 접속한다.
2. **Select Container**: 왼쪽 사이드바에서 로그를 확인하고 싶은 컨테이너를 선택한다.
3. **Real-time Monitoring**: 자동 스크롤(Auto-scroll) 기능을 활성화하여 실시간으로 유입되는 로그를 모니터링한다.
4. **Search and Filter**: 상단 검색창을 사용하여 특정 키워드(예: `ERROR`, `Exception`, `GET /api/v1`)가 포함된 로그를 필터링한다.
5. **Clear Logs**: UI 상의 'Clear' 버튼을 눌러 현재 화면의 로그를 비운다 (실제 로그 파일은 삭제되지 않음).

## Common Pitfalls

- **Stale Connection**: 장시간 브라우저를 켜둘 경우 로그 스트림 연결이 끊어질 수 있다. 이 경우 페이지를 새로고침한다.
- **Large Log Volume**: 로그 유입량이 매우 많을 경우 브라우저 성능에 영향을 줄 수 있다. 필요한 경우 검색 필터를 적극 활용하라.

## Related Documents

- **Implementation**: `[../../../infra/11-laboratory/dozzle/README.md]`
- **Operation**: `[../../08.operations/11-laboratory/dozzle.md]`
- **Runbook**: `[../../09.runbooks/11-laboratory/dozzle.md]`
