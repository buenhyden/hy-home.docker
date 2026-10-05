---
title: "JupyterLab Recovery Runbook"
version: "1.0.2"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-03"
layer: "operations"
artifact_id: "RUN-0089"
parent_ids:
- "GDE-0089"
created: "2026-09-21"
---

# JupyterLab Recovery Runbook

## Overview

## Trigger and Preconditions

### Overview

### Trigger and Preconditions

### When to Use

시작 실패, 토큰 노출, 멈춘 커널, 작업 파일 손실, 이미지 업그레이드 시
사용한다.

### 작업 선택과 복구 전제

변경 전에 정확한 서비스·데이터 경로·승인자·중단 영향을 기록하고 [공통 복구 전제](0021-backup-and-restore.md)를
적용한다. 격리 대상, 복구본 식별자·무결성, 여유 공간, 비밀 보관, 작성자 정지와
승격 승인 중 하나라도 불명확하면 중단한다. config·secret 교체는
[공통 수명주기 정책](../policies/0006-infrastructure-optimization-governance.md)의
단일 파일 bind 재생성과 비밀 비노출 확인을 따른다. 재시작은 데이터 복원이나 자격 증명
폐기 검증을 대신하지 않는다.

## Procedure

### Procedure

1. 저장소 루트에서 점검한다.

   ```bash
   docker compose --profile core --profile data-science config --quiet
   docker compose --profile core --profile data-science ps -a jupyterlab
   docker compose --profile core --profile data-science logs --tail=100 jupyterlab
   ```

2. 명시적 길이 검사는 `64`로 종료하지만 secret 누락·읽기 실패는 앞선 shell 단계에서
   다른 코드로 실패할 수 있다. bind 오류는 경로 부재·종류·권한을 구분한다.
   `${DEFAULT_MANAGEMENT_DIR}/jupyterlab/work`를 Docker가 임의 생성하도록 바꾸지
   말고 승인된 경로와 소유권을 확인한 뒤 필요한 생성·수정을 수행한다.
3. 토큰 노출이 의심될 경우: 서비스를 정지하고, 등록된 시크릿 워크플로로
   `secrets/tools/jupyterlab/jupyter_token.txt`를 교체하고, 예상치 못한 파일이 있는지
   작업 디렉터리를 검토한다. 단일 파일 bind 교체를 반영하도록 공통 정책에 따라
   승인된 재생성을 수행한다. 재시작·재생성만으로 기존 cookie 폐기를 보장하지 않는다.
   선택한 base의 cookie-secret 동작을 확인하고 이전 token과 기존 cookie 거부를 각각
   검증하기 전에는 회전 완료로 판정하지 않는다.
4. 멈춘 커널의 경우 UI에서 커널을 재시작한다. 서버 자체가 응답하지 않을
   때만 컨테이너를 재시작한다.

### Restore and upgrade

1. 서비스를 정지하고 작업 디렉터리를 복사한다. 소스 커밋과 파일 개수를
   기록한다.
2. 실행 중인 디렉터리를 교체하기 전에 새 디렉터리로 복원하고 그에 대해
   격리된 인스턴스를 시작한다.
3. 이미지 업그레이드의 경우 승인된 환경에서 재빌드하고, 고정된 모든
   라이브러리를 import하고 MLflow 실행 한 건을 기록하는 노트북을 연다.

### 작업 디렉터리와 라이브러리 보존

work 디렉터리를 복사하기 전에 server를 멈춘다. notebook과 output은 민감할
수 있는 data로 취급한다. library를 바꾸려면 image를 재빌드하고, MLflow
client version을 server와 맞춘다.

## Verification

### Evidence

종료 코드, 이미지 태그, 소스 커밋, 파일 개수를 기록한다. 토큰이나 노트북
내용은 절대 기록하지 않는다.

## Rollback and Escalation

### Rollback or Recovery

설정은 검토된 Compose와 requirements로 복원하고, 보존된 이전 이미지 식별자를
우선 확인한다. 재빌드가 원래 이미지와 같다는 보장은 없다. 사용자 데이터는 먼저
서버를 정지한 뒤 격리 복원·해시 검증을 수행한다. 아래는 빈 작업 디렉터리의 과거
리허설이며 현재 사용자 데이터·kernel·의존성 복구를 증명하지 않는다.

원본: `docs/05.operations/runbooks/0089-jupyterlab.md`, SPEC-0198 이전 Git 기록.

> Historical evidence (not current authority; source: Git history):
>
> 설정 롤백은 Git에서 Compose와 requirements를 복원한다. 이전 이미지는 다시
> 빌드해야 한다. 작업 디렉터리 복원은 2026-09-22에 리허설했다. 작업
> 디렉터리가 비어 있었으므로 셀 하나짜리 테스트 노트북을 실행하고 저장한 뒤
> SHA-256 매니페스트로 아카이브하고, 격리된 경로로 복원하고(매니페스트 1/1),
> 동일한 이미지의 `--network none` 컨테이너에서 `nbformat`으로 검증했다(저장된
> 출력 그대로 유지). 이후 테스트 노트북은 제거했다. 디렉터리에 사용자
> 데이터가 없었으므로 실행 중인 서비스는 정지하지 않았다. 사용자 데이터가
> 있는 경우 1단계가 요구하는 대로 먼저 정지한다.

### Escalation

책임자는 `@buenhyden`이다. 아래 중단 조건과 영향받은 서비스·대상 소유자를 함께 기록하고, 추가 변경 없이 보고한다.

알 수 없는 코드 실행의 증거, JupyterHub 없이 다중 사용자 접근 요청, 토큰
비활성화 요청이 있으면 중단한다.

### Traceability

- [Guide](../guides/0089-jupyterlab.md) (`GDE-0089`)
- [Policy](../policies/0089-jupyterlab.md) (`POL-0089`)
- [JupyterLab Compose](../../../infra/12-analytics/jupyterlab/docker-compose.yml)

## Related Documents

- [이미지 Dockerfile](../../../infra/12-analytics/jupyterlab/Dockerfile)과
  [파생 버전 프로젝션](../../../infra/tech-stack.versions.json)
- [MLflow 런북](0088-mlflow.md)
