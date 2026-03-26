<!-- Target: docs/03.adr/0009-tooling-services.md -->

# ADR-0009: 09-tooling 계층 주요 서비스 선정 및 구성

## Context

`09-tooling` 계층은 개발 및 운영 효율성을 극대화하기 위한 보조 도구들을 포함한다. 인프라 자동화(IaC), 코드 품질 분석, 성능 테스트, 데이터 동기화 등 다양한 요구사항을 충족하기 위해 검증된 오픈소스 솔루션들을 선정하고 통합해야 한다.

## Decision

다음과 같은 서비스 스택을 `09-tooling`의 표준 도구로 선정한다.

1. **IaC Automation**: **Terrakube**
    * 이유: Terraform Cloud의 오픈소스 대안으로, 팀 단위의 상태 관리 및 자동화된 실행 환경(Plan/Apply)을 제공한다.
2. **Code Quality**: **SonarQube**
    * 이유: 다중 언어 지원 및 정밀한 정적 분석 기능을 통해 프로젝트의 전반적인 코드 품질과 보안 취약점을 중앙에서 관리한다.
3. **Performance Testing**: **Locust**
    * 이유: Python 기반의 시나리오 정의가 가능하여 확장이 용이하며, 분산 아키텍처를 통해 대규모 부하를 생성할 수 있다.
4. **OCI Registry**: **Docker Registry (v2)**
    * 이유: 내부 서비스 배포를 위한 경량화된 사설 이미지 저장소를 제공한다.
5. **Data Synchronization**: **Syncthing**
    * 이유: 중앙 서버 없이 장치 간 P2P 파일 동기화를 지원하여, 분산된 개발 환경 간의 리소스 공유를 최적화한다.

## Rationale

* **통합성**: 모든 서비스는 Keycloak SSO와 연동되어 단일 계정으로 접근 가능하다.
* **지속성**: Terraform 상태 정보 및 분석 데이터는 `04-data` 계층(MinIO, PostgreSQL)에 저장되어 데이터 유실을 방지한다.
* **표준화**: 각 서비스는 Docker Compose 및 사전에 정의된 환경 변수를 통해 일관된 방식으로 배포된다.

## Consequences

* **Positive**:
  * 인프라 변경 이력이 투명하게 관리된다.
  * 코드 품질 게이트를 통해 결함 있는 코드의 배포를 사전에 차단할 수 있다.
  * 성능 병목 지점을 데이터 기반으로 파악할 수 있다.
* **Negative**:
  * 다양한 도구 운영에 따른 유지보수 리소스(메모리, CPU) 점유율이 증가한다.
  * 도구 간의 복잡한 네트워크 권한 설정이 필요하다.

## Status

Accepted (2026-03-26)
