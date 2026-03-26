<!-- Target: docs/09.runbooks/09-tooling-maintenance.md -->

# Tooling Tier Maintenance Runbook

## Overview (KR)

이 런북은 `09-tooling` 계층 서비스의 유지보수 및 긴급 복구 절차를 기술한다.

## RB-09-01: Terrakube Database Recovery

- **Symptom**: Terrakube API가 실행되지 않으며 'Database connection failed' 오류 발생.
- **Action**:
  1. `04-data` PostgreSQL 컨테이너 상태 확인.
  2. `terrakube` 데이터베이스 전용 사용자 권한 및 DB 생존 여부 확인.
  3. 필요 시 최근 백업본을 통해 스키마 복구 수행.

## RB-09-02: SonarQube ElasticSearch Index Rebuild

- **Symptom**: 분석 결과가 UI에 보이지 않거나 검색 기능 오작동.
- **Action**:
  1. SonarQube 서버 중지.
  2. `data/es8` 디렉토리 내의 인덱스 파일 삭제.
  3. 서버 재시작 (서버가 자동으로 인덱스를 재구성함).

## RB-09-03: Private Registry Storage Full

- **Symptom**: 이미지 푸시 시 'No space left on device' 오류 발생.
- **Action**:
  1. MinIO 버킷 사용량 확인.
  2. Registry 가비지 컬렉션(GC) 실행:
     ```bash
     docker exec -it registry bin/registry garbage-collect /etc/docker/registry/config.yml
     ```
  3. 불필요한 태그/레포지토리 삭제.

## RB-09-04: Syncthing Conflict Resolution

- **Symptom**: 파일 저장 시 'Conflict' 접미사가 붙은 파일 생성.
- **Action**:
  1. 충돌이 발생한 두 장치의 파일 변경 시점 확인.
  2. 수동 병합 수행 후 `.sync-conflict-...` 파일 삭제.

## Related Documents

- **Spec**: [09-tooling/spec.md](../04.specs/09-tooling/spec.md)
- **Policy**: [09-tooling-operational-policy.md](../08.operations/09-tooling-operational-policy.md)
