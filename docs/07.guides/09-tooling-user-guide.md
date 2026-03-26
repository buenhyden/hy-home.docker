<!-- Target: docs/07.guides/09-tooling-user-guide.md -->

# Tooling Ecosystem User Guide

## Overview (KR)

이 가이드는 `09-tooling` 계층에서 제공하는 도구들(Terrakube, SonarQube, Locust 등)의 기본적인 사용 방법을 설명한다.

## Terrakube: IaC Management

Terrakube는 Terraform 상태를 관리하고 워크플로우를 자동화한다.

1.  **Organization & Workspace**: 프로젝트 단위로 Organization을 생성하고, 인프라 환경(Dev/Prod)별로 Workspace를 분리한다.
2.  **VCS 연동**: Git 저장소를 연결하여 소스 코드 변경 시 자동으로 Plan이 실행되도록 설정한다.
3.  **Variables**: 인프라 프로비저닝에 필요한 변수 및 시크릿(클라우드 자격 증명 등)을 Workspace 설정에서 관리한다.

## SonarQube: Code Quality

SonarQube를 통해 지속적으로 코드 품질을 검사한다.

1.  **Project Creation**: 분석 대상 프로젝트를 생성한다.
2.  **Analysis Run**: CI 파이프라인(GitHub Actions/Airflow)에서 `sonar-scanner`를 호출하여 분석을 수행한다.
3.  **Quality Gate**: 'New Code'에 대한 중복률, 보안 취약점, 커버리지 기준을 충족해야 배포가 가능하도록 설정한다.

## Locust: Performance Testing

대규모 부하 테스트를 수행한다.

1.  **Locustfile 작성**: Python으로 테스트 시나리오를 작성한다.
2.  **Master UI 접속**: `http://<server-ip>:18089`로 접속하여 동시 접속자 수(Spawn rate)와 목표 사용자 수를 입력한다.
3.  **Result Analysis**: 응답 시간(Latency), 실패율(Failures)을 실시간으로 확인하고 보고서를 다운로드한다.

## Syncthing: File Synchronization

노드 간 실시간 파일 동기화를 수행한다.

1.  **Device ID 공유**: 동기화할 장치 간에 Device ID를 교환한다.
2.  **Folder Share**: 동기화할 폴더를 지정하고 공유 대상 장치를 선택한다.

## Related Documents

- **PRD**: [2026-03-26-09-tooling.md](../01.prd/2026-03-26-09-tooling.md)
- **Spec**: [09-tooling/spec.md](../04.specs/09-tooling/spec.md)
