<!-- Target: docs/08.operations/09-tooling-operational-policy.md -->

# Tooling Tier Operational Policy

## Overview (KR)

이 문서는 `09-tooling` 계층에 포함된 도구들의 운영 기준 및 거버넌스 정책을 정의한다.

## IaC Automation Policy (Terrakube)

1.  **State Protection**: 모든 Terraform State는 MinIO의 버전 관리 버킷에 저장되어야 한다.
2.  **Approval Workflow**: Production 환경에 대한 `apply` 작업은 최소 1명 이상의 권한 있는 운영자 승인이 필요하다.
3.  **Drift Detection**: 정기적으로(매주 1회) Drift Detection을 수행하여 실제 인프라와 코드 간의 불일치를 해소한다.

## Code Quality Policy (SonarQube)

1.  **Standard Quality Gate**: 모든 신규 코드는 `Sonar way` 이상의 엄격한 품질 게이트를 통과해야 한다.
2.  **Security Scan**: Critical/Blocker 등급의 보안 취약점이 발견된 경우 배포 파이프라인을 즉시 중단한다.
3.  **Retention**: 분석 이력은 최근 6개월간 보관하며, 이전 데이터는 아카이빙한다.

## Performance Testing Policy (Locust)

1.  **Pre-test Notification**: 대규모 부하 테스트(1,000 TPS 이상) 수행 전에는 인프라 팀에 사전 통보해야 한다.
2.  **Environment Isolation**: 부하 테스트는 반드시 전용 성능 테스트 환경 또는 스테이징 환경에서 수행한다.

## Registry & Storage Policy

1.  **Image Tagging**: `latest` 태그 사용을 지양하며, 의미 있는 버전 정보 또는 Git Commit Hash를 사용한다.
2.  **Purge Policy**: 90일 이상 사용되지 않은 임시/테스트 이미지는 정기적으로 삭제한다.

## Related Documents

- **ARD**: [0009-tooling-architecture.md](../02.ard/0009-tooling-architecture.md)
- **Spec**: [09-tooling/spec.md](../04.specs/09-tooling/spec.md)
