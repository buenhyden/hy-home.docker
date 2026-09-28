---
title: "Dependency Version Management Runbook"
version: "0.1.1"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "RUN-0086"
parent_ids:
- "POL-0086"
created: "2026-09-19"
---

# Dependency Version Management Runbook

## When to Use

소스 이미지, 업데이트 정책 또는 파생 버전 프로젝션이 변경될 때 사용한다.
저장소 루트에서 작업하며, diff를 명확히 식별하고 출력에 비공개 값을 포함하지
않는다. 이 절차는 네트워크로 연결된 Renovate 업데이트 작업을 실행하지 않는다.

## Procedure

1. 변경된 Compose/Dockerfile 핀, 빌드 인자, 매니저 소유권을 식별한다.
2. 쓰기 없이 파생 프로젝션을 미리 보고 검증한다.

   ```bash
   bash scripts/operations/sync-tech-stack-versions.sh --dry-run
   bash scripts/operations/sync-tech-stack-versions.sh --check
   ```

3. 소스 변경이 의도된 것이면, 옵션 없이 동일한 스크립트를 실행해 파생 레지스트리
   항목을 원자적으로 추가/갱신/삭제한 뒤, 해당 diff를 검사하고 `--check`를
   반복한다.
4. 지원되는 Renovate Node 런타임 또는 승인된 도구 컨테이너를 사용해 공식
   `renovate-config-validator --strict --no-global renovate.json5`와
   `renovate-config-validator --strict infra/09-tooling/renovate/config/config.js`를
   실행한다.
5. 선택한 Compose 프로파일과 관련 빌드 변경을 검증한다. 누락, 중복, 제거,
   digest, local/custom, 버전이 서로 다른 소스 그룹을 기존 동기화 테스트
   스위트로 테스트한다.
6. 실제 업데이트 작업이나 배포의 경우, 해당 명명된 작업에 대한 승인을 받고
   실행 전에 마이그레이션/백업 전제 조건을 기록한다.

## Evidence

명령, 종료 상태, 소스 커밋, 파서/검증기 런타임과 한계를 기록한다. 지원되지
않는 Node나 누락된 네이티브 검증 의존성은 명시해야 한다. 로컬 문법 검사
결과만으로는 원격 봇 실행이나 복원된 애플리케이션 데이터베이스를 증명하지
못한다.

## Rollback or Recovery

소스와 레지스트리 변경을 함께 되돌린다. 설정 롤백은 기존 데이터베이스 파일을
다운그레이드하지 않는다. 마지막으로 호환되던 이미지와 보호된 백업을 유지하며,
데이터는 서비스 소유의 격리된 복구 절차로만 복원한다.

## Escalation

소유권 중복, 미분류 소스, 새로운 미상 매니저, 레지스트리 전용 핀 변경,
크리덴셜 오류, 지원되지 않는 마이그레이션 경로 또는 복구 증거 부재 시
중단한다. 정확한 결정은 @buenhyden에게 문의하며, 게이트를 우회하거나 force
push를 하지 않는다.

## Traceability

- [Home/Dev architecture](../../02.architecture/descriptions/0031-home-development-host.md) (`AD-0031`)
- [Guide](../guides/0086-dependency-version-management.md), [Policy](../policies/0086-dependency-version-management.md), [Runbook](0086-dependency-version-management.md)

## Related Documents

- [운영 인덱스](../README.md)
- [런타임 버전 프로젝션](../../../infra/tech-stack.versions.json)
- [저장소 Renovate 정책](../../../renovate.json5)
- [Dependabot 범위](../../../.github/dependabot.yml)
