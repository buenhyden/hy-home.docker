# infra_net Implementation Guide

## Overview (KR)

이 문서는 모든 인프라 서비스에 `infra_net` 공통 네트워크와 고정 IP를 할당하는 가이드다. 프로젝트의 일관성을 유지하기 위해 표준 딕셔너리 기반의 네트워크 정의 방식을 따른다.

## Guide Type

`how-to | system-guide`

## Target Audience

- Developer
- Operator
- Agent-tuner

## Purpose

이 가이드는 시스템 관리자나 개발자가 신규 서비스 또는 기존 서비스를 `hy-home.docker`의 표준 네트워크 구조인 `infra_net`에 올바르게 통합하는 것을 돕는다.

## Prerequisites

- `hy-home.docker` 프로젝트 루트 디렉터리에 대한 쓰기 권한.
- Docker Compose v2.0 이상.
- `docs/05.plans/2026-04-01-standardize-infra-net.md`의 IP 할당 현황.

## Step-by-step Instructions

1. **IP 대역 확인**:
   - `docs/05.plans/2026-04-01-standardize-infra-net.md`의 **IP Mapping Strategy** 섹션에서 서비스 그룹에 맞는 IP 가용 범위를 확인한다.
2. **Compose 파일 수정**:
   - `services:` 하위의 대상 서비스에서 `networks:` 섹션을 다음과 같이 딕셔너리 형태로 수정한다.

   ```yaml
   networks:
     infra_net:
       ipv4_address: 172.19.0.XXX
   ```

   - (선택 사항) 만약 K3s 연동을 위해 `k3d-hyhome` 네트워크가 필요한 경우 명시적으로 추가한다.
3. **루트 Docker Compose 수정**:
   - 프로젝트 루트의 `docker-compose.yml` 내 `include:` 섹션에서 해당 파일이 주석 처리되어 있지 않은지 확인한다.
4. **구성 검증**:
   - `docker compose config`를 실행하여 YAML 구문에 오류가 없는지 최종 확인한다.

## Common Pitfalls

- **IP Conflict**: 이미 할당된 IP를 중복 부여하지 않도록 `grep` 등으로 전체 조사를 수행해야 함.
- **Indentation Error**: YAML 딕셔너리 구조에서의 들여쓰기 오류 주의.
- **Network Scope**: 지정된 주소 대역(`172.19.0.0/16`) 외부의 IP를 입력할 경우 배포 실패.

## Related Documents

- **Spec**: `[../04.specs/standardize-infra-net/spec.md]`
- **Operation**: `[../08.operations/standardize-infra-net.md]`
- **Runbook**: `[../09.runbooks/0012-standardize-infra-net.md]`
- **Plan**: `[../05.plans/2026-04-01-standardize-infra-net.md]`
