# Tooling Runbook (09-tooling)

> Toolchain Failure Recovery & Performance Troubleshooting

## Overview

이 런북은 `09-tooling` 계층에서 발생할 수 있는 주요 도구(SonarQube, Terrakube, Locust)의 장애 상황에 대한 조치 방법을 설명한다.

- [01. IaC Automation Guide](../../07.guides/09-tooling/01.iac-automation.md) - Managed Terraform workflows with Terrakube.
- [02. Performance Testing Guide](./performance-testing.md) - Context-level load testing (Locust).
- [03. Locust Guide](./locust.md) - Dedicated Locust service guide.
- [04. k6 Guide](./k6.md) - Dedicated k6 (Performance Testing unit) service guide.
- [05. Registry Runbook](./registry.md) - Service maintenance and recovery procedure.
- [06. SonarQube Runbook](./sonarqube.md) - Diagnostic and recovery steps for code quality scanning.
- [07. Syncthing Runbook](./syncthing.md) - Diagnostic and recovery steps for P2P file synchronization.
- [08. Terraform Runbook](./terraform.md) - State lock recovery and IaC troubleshooting.
- [09. Terrakube Runbook](./terrakube.md) - Platform recovery and hung executor cleanup.

## Emergency Procedures

### 1. 성능 및 리소스 관리

- [Performance Testing Operations Policy](./performance-testing.md) - General benchmarking and scaling policies.
- [Locust Operations Policy](./locust.md) - Specific governance for Locust service units.
- [k6 Operations Policy](./k6.md) - Specific governance for k6 infrastructure units.
- **Memory Limits**: SonarQube는 높은 메모리 할당을 요구하므로, `common-optimizations.yml`의 `high` 최적화 템플릿을 준수한다.

### 2. SonarQube DB 연결 장애

SonarQube가 시작되지 않거나 'DB Connection Failure'가 로그에 나타날 때.

1. **스키마 확인**: PostgreSQL(`mng-db`)에 `sonarqube` 스키마가 존재하는지 확인.
2. **비밀번호 검증**: `docker secret inspect sonarqube_db_password`로 마운트된 비밀번호가 DB 계정과 일치하는지 확인.
3. **Elasticsearch 인덱스 손상**: 컨테이너 데이터 폴더 내의 `es8` 디렉터리를 삭제하고 재시작하여 인덱스를 다시 구축한다.

### 3. Terrakube 실행기(Executor) 중단

Terraform 작업이 'Pending' 상태에서 진행되지 않을 때.

1. **Docker 소켓 점검**: `terrakube-executor` 컨테이너가 호스트의 `/var/run/docker.sock`을 정상적으로 마운트했는지 확인.
2. **MinIO 연결성**: 실행기가 원격 상태를 저장하는 MinIO 버킷에 접근 가능한지 로그를 통해 확인.
3. **Valkey 잠금 해제**: 비정상 종료로 인해 잔류한 Terraform 락이 있다면 DB 또는 Valkey에서 수동으로 제거한다.

### 4. private Registry 푸시 실패 (Forbidden)

이미지 업로드 중 권한 에러가 발생하는 경우.

1. **Auth 확인**: `docker login registry.${DEFAULT_URL}`을 통해 인증 정보 유효성 점검.
2. **가비지 컬렉션**: [Registry Runbook](./registry.md)을 참조하여 GC를 수행하고 용량을 확보한다.
3. **디스크 용량**: 도구 계층의 영구 저장소(`${DEFAULT_TOOLING_DIR}`)가 가득 찼는지 확인.

---

## Verification Steps

- [ ] `sonarqube` UI 접속 및 관리 대시보드 상태 확인.
- [ ] Terrakube API `/actuator/health` 응답 확인.

## Related Operational Documents

- [Operations Policy](../../08.operations/09-tooling/README.md)
- [IaC Automation Guide](../../07.guides/09-tooling/01.iac-automation.md)
