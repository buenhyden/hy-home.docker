---
title: "JupyterLab Recovery Runbook"
version: "1.0.1"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "RUN-0089"
parent_ids:
- "GDE-0089"
created: "2026-09-21"
---

# JupyterLab Recovery Runbook

## When to Use

시작 실패, 토큰 노출, 멈춘 커널, 작업 파일 손실, 이미지 업그레이드 시
사용한다.

## Procedure

1. 저장소 루트에서 점검한다.

   ```bash
   docker compose --profile core --profile data-science config --quiet
   docker compose --profile core --profile data-science ps -a jupyterlab
   docker compose --profile core --profile data-science logs --tail=100 jupyterlab
   ```

2. `64` 종료는 토큰 시크릿이 없거나 16자 미만임을 의미한다. 바인드 오류는
   `${DEFAULT_MANAGEMENT_DIR}/jupyterlab/work`가 존재하지 않는다는 뜻이다.
   Docker가 생성하도록 두지 말고 UID 1000 소유로 직접 생성한다.
3. 토큰 노출이 의심될 경우: 서비스를 정지하고, 등록된 시크릿 워크플로로
   `secrets/tools/jupyter_token.txt`를 교체하고, 예상치 못한 파일이 있는지
   작업 디렉터리를 검토한 뒤 다시 시작한다. 재시작 이후 기존 브라우저
   쿠키는 동작하지 않는다.
4. 멈춘 커널의 경우 UI에서 커널을 재시작한다. 서버 자체가 응답하지 않을
   때만 컨테이너를 재시작한다.

### Restore and upgrade

1. 서비스를 정지하고 작업 디렉터리를 복사한다. 소스 커밋과 파일 개수를
   기록한다.
2. 실행 중인 디렉터리를 교체하기 전에 새 디렉터리로 복원하고 그에 대해
   격리된 인스턴스를 시작한다.
3. 이미지 업그레이드의 경우 승인된 환경에서 재빌드하고, 고정된 모든
   라이브러리를 import하고 MLflow 실행 한 건을 기록하는 노트북을 연다.

## Evidence

종료 코드, 이미지 태그, 소스 커밋, 파일 개수를 기록한다. 토큰이나 노트북
내용은 절대 기록하지 않는다.

## Rollback or Recovery

설정 롤백은 Git에서 Compose와 requirements를 복원한다. 이전 이미지는 다시
빌드해야 한다. 작업 디렉터리 복원은 2026-09-22에 리허설했다. 작업
디렉터리가 비어 있었으므로 셀 하나짜리 테스트 노트북을 실행하고 저장한 뒤
SHA-256 매니페스트로 아카이브하고, 격리된 경로로 복원하고(매니페스트 1/1),
동일한 이미지의 `--network none` 컨테이너에서 `nbformat`으로 검증했다(저장된
출력 그대로 유지). 이후 테스트 노트북은 제거했다. 디렉터리에 사용자
데이터가 없었으므로 실행 중인 서비스는 정지하지 않았다. 사용자 데이터가
있는 경우 1단계가 요구하는 대로 먼저 정지한다.

## Escalation

알 수 없는 코드 실행의 증거, JupyterHub 없이 다중 사용자 접근 요청, 토큰
비활성화 요청이 있으면 중단한다.

## Traceability

- [Guide](../guides/0089-jupyterlab.md) (`GDE-0089`)
- [Policy](../policies/0089-jupyterlab.md) (`POL-0089`)
- [JupyterLab Compose](../../../infra/11-laboratory/jupyterlab/docker-compose.yml)

## Related Documents

- [이미지 Dockerfile](../../../infra/11-laboratory/jupyterlab/Dockerfile)과
  [파생 버전 프로젝션](../../../infra/tech-stack.versions.json)
- [MLflow 런북](0088-mlflow.md)
