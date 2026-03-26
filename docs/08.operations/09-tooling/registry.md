<!-- Target: docs/08.operations/09-tooling/registry.md -->

# Docker Registry Operations Policy

> Private OCI-compliant image distribution service governance.

---

## Overview (KR)

이 문서는 `hy-home.docker` 도커 레지스트리 운영 정책을 정의한다. 이미지의 생명주기 관리, 보안 통제 기준, 그리고 저장 용량 최적화 방법을 규정한다.

## Policy Scope

- `infra/09-tooling/registry` 내에서 구동되는 서비스.
- 저장소 내 모든 컨테이너 이미지 및 OCI 아티팩트.

## Applies To

- **Systems**: Internal Docker Registry v2.
- **Agents**: CI/CD Pipelines, Internal Developers.
- **Environments**: Production (On-premise).

## Controls

- **Required**:
  - `REGISTRY_STORAGE_DELETE_ENABLED: "true"` 설정 유지 (GC를 위해 필수).
  - 이미지 푸시 전 태그 컨벤션 준수 (`registry:<port>/<project>/<image>:<tag>`).
- **Allowed**:
  - `insecure-registries`를 통한 내부 망 접근.
- **Disallowed**:
  - 외부 공인 IP를 통한 레지스트리 직접 노출 금지.

## Exceptions

- 대용량 데이터셋(이미지 외) 저장은 MinIO를 우선 활용하며, 레지스트리 저장 허용 시 별도 승인 필요.

## Verification

- `docker-compose.yml` 환경 변수 설정값 정기 점검.
- `${DEFAULT_REGISTRY_DIR}` 디스크 사용량 임계치(90%) 알림 모니터링.

## Review Cadence

- Quarterly

## AI Agent Policy Section (If Applicable)

- **Registry Access**: 에이전트는 프라이빗 레지스트리의 이미지를 풀(Pull)할 수 있으나, 프로덕션 태그(`v*`)에 대한 푸시는 휴먼 게이트 승인이 필요함.

## Related Documents

- **ARD**: [infra/09-tooling/registry/README.md](../../../infra/09-tooling/registry/README.md)
- **Runbook**: [../09.runbooks/09-tooling/registry.md](../../09.runbooks/09-tooling/registry.md)
