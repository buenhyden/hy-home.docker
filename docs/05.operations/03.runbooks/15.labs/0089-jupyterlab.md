---
title: "JupyterLab Recovery Runbook"
version: "2.0.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
layer: "operations"
artifact_id: "RUN-0089"
parent_ids:
- "GDE-0089"
created: "2026-09-21"
next_review_at: "2027-05-13"
---

# JupyterLab Recovery Runbook

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the runbook payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Trigger and Scope

##### Trigger

JupyterLab의 시작 실패, 토큰 노출, 커널 정지, 작업 파일 손실, 이미지 업그레이드를 다루는 복구 런북이다.

시작 실패, 토큰 노출, 멈춘 커널, 작업 파일 손실, 이미지 업그레이드 시
사용한다.

##### Targets

- [Guide](../../01.guides/15.labs/0089-jupyterlab.md) (`GDE-0089`)
- [Policy](../../02.policies/15.labs/0089-jupyterlab.md) (`POL-0089`)
- [JupyterLab Compose](../../../../labs/jupyterlab/docker-compose.yml)
- SPEC-0262 Analytics labs migration

- [이미지 Dockerfile](../../../../labs/jupyterlab/Dockerfile)과
  [파생 버전 프로젝션](../../../../infra/tech-stack.versions.json)
- [MLflow 런북](../13.analytics-and-data-quality/0088-mlflow.md)

#### Preflight

##### Authority

변경 전 정확한 서비스·데이터 경로·승인자·중단 영향을 기록한다. 토큰 교체는 등록된 시크릿 워크플로와 승인된 재생성으로 하고, 이전 notebook 재배치는 별도 승인 아래 수동으로 한다.

##### Environment

변경 전 확인할 작업 선택과 복구 전제는 다음과 같다.

###### 작업 선택과 복구 전제
<!-- core-payload-level:4 -->

변경 전에 정확한 서비스·데이터 경로·승인자·중단 영향을 기록하고 [공통 복구 전제](../10.platform-and-backup/0021-backup-and-restore.md)를
적용한다. 격리 대상, 복구본 식별자·무결성, 여유 공간, 비밀 보관, 작성자 정지와
승격 승인 중 하나라도 불명확하면 중단한다. config·secret 교체는
[공통 수명주기 정책](../../02.policies/01.common/0006-infrastructure-optimization-governance.md)의
단일 파일 bind 재생성과 비밀 비노출 확인을 따른다. 재시작은 데이터 복원이나 자격 증명
폐기 검증을 대신하지 않는다.

#### Procedure

##### Steps

| Step | Action | Expected Result | On Failure |
| --- | --- | --- | --- |
| 1 | `config --quiet`, `ps -a jupyterlab`, `logs --tail=100 jupyterlab`로 점검 (기동/재시작은 `lab.py` lease 규칙) | 문서에 기록 없음 | 중단하고 Stop Conditions에 따라 escalation |
| 2 | secret 누락/읽기 실패와 bind 오류(경로 부재/종류/권한) 구분, `${LAB_DATA_DIR}/jupyterlab/work` 승인된 경로와 소유권(UID 1000) 확인 | 문서에 기록 없음 | Docker가 임의 생성하도록 두지 않으며 이전 notebook 재배치는 별도 승인 후 수동 |
| 3 | 토큰 노출 의심 시 서비스 정지, LAB 전용 token 파일 교체, 작업 디렉터리 검토, 승인된 재생성 | 이전 token과 기존 cookie 거부를 각각 검증 | 검증 전에는 회전 완료로 판정하지 않음 |
| 4 | 멈춘 커널은 UI에서 재시작, 서버 자체가 응답하지 않을 때만 컨테이너 재시작 | 문서에 기록 없음 | 알 수 없는 코드 실행의 증거가 있으면 중단 |
| 5 | Restore and upgrade: 서비스를 정지하고 작업 디렉터리를 복사 (소스 커밋과 파일 개수 기록) | 소스 커밋과 파일 개수 기록 | 중단하고 Stop Conditions에 따라 escalation |
| 6 | Restore and upgrade: 실행 중인 디렉터리 교체 전 새 디렉터리로 복원하고 격리된 인스턴스 시작 | 문서에 기록 없음 | 중단하고 Stop Conditions에 따라 escalation |
| 7 | Restore and upgrade: 이미지 업그레이드 시 승인된 환경에서 재빌드하고 고정된 모든 라이브러리를 import하는 노트북 열기 | 노트북이 고정된 모든 라이브러리를 import함 | MLflow 기록 확인은 승인된 `LAB_JUPYTERLAB_MLFLOW_TRACKING_URI`가 있을 때만 수행 |

1. 저장소 루트에서 점검한다. JupyterLab은 독립 LAB이다(SPEC-0262). `config`는 렌더링만 하며,
   기동·재시작은 `python3 scripts/operations/lab.py check|up|down jupyterlab`의 lease 규칙을 따른다.

   - `docker compose --env-file labs/.env -f labs/jupyterlab/docker-compose.yml --profile jupyterlab config --quiet`
   - `docker compose --env-file labs/.env -f labs/jupyterlab/docker-compose.yml --profile jupyterlab ps -a jupyterlab`
   - `docker compose --env-file labs/.env -f labs/jupyterlab/docker-compose.yml --profile jupyterlab logs --tail=100 jupyterlab`

2. 명시적 길이 검사는 `64`로 종료하지만 secret 누락·읽기 실패는 앞선 shell 단계에서
   다른 코드로 실패할 수 있다. bind 오류는 경로 부재·종류·권한을 구분한다.
   `${LAB_DATA_DIR}/jupyterlab/work`를 Docker가 임의 생성하도록 바꾸지
   말고 승인된 경로와 소유권(UID 1000)을 확인한 뒤 필요한 생성·수정을 수행한다. 이전
   `${DEFAULT_MANAGEMENT_DIR}/jupyterlab/work`의 notebook은 자동으로 옮겨지지 않았으며 재배치는
   별도 승인 아래 수동으로 한다.
3. 토큰 노출이 의심될 경우: 서비스를 정지하고, 등록된 시크릿 워크플로로
   LAB 전용 token 파일(`${LAB_SECRET_DIR:-../../secrets/labs}/jupyterlab/` 아래, 정확한 파일명은 `labs/jupyterlab/docker-compose.yml`의 `secrets:`가 소유)을 교체하고, 예상치 못한 파일이 있는지
   작업 디렉터리를 검토한다. 단일 파일 bind 교체를 반영하도록 공통 정책에 따라
   승인된 재생성을 수행한다. 재시작·재생성만으로 기존 cookie 폐기를 보장하지 않는다.
   선택한 base의 cookie-secret 동작을 확인하고 이전 token과 기존 cookie 거부를 각각
   검증하기 전에는 회전 완료로 판정하지 않는다.
4. 멈춘 커널의 경우 UI에서 커널을 재시작한다. 서버 자체가 응답하지 않을
   때만 컨테이너를 재시작한다.

###### Restore and upgrade
<!-- core-payload-level:4 -->

1. 서비스를 정지하고 작업 디렉터리를 복사한다. 소스 커밋과 파일 개수를
   기록한다.
2. 실행 중인 디렉터리를 교체하기 전에 새 디렉터리로 복원하고 그에 대해
   격리된 인스턴스를 시작한다.
3. 이미지 업그레이드의 경우 승인된 환경에서 재빌드하고, 고정된 모든
   라이브러리를 import하는 노트북을 연다. MLflow 기록 확인은 승인된
   `LAB_JUPYTERLAB_MLFLOW_TRACKING_URI`가 있을 때만 한다(SPEC-0262 미결정 항목).

###### 작업 디렉터리와 라이브러리 보존
<!-- core-payload-level:4 -->

work 디렉터리를 복사하기 전에 server를 멈춘다. notebook과 output은 민감할
수 있는 data로 취급한다. library를 바꾸려면 image를 재빌드하고, MLflow
client version을 server와 맞춘다.

##### Stop Conditions

알 수 없는 코드 실행의 증거, JupyterHub 없이 다중 사용자 접근 요청, 토큰
비활성화 요청이 있으면 중단한다.

#### Verification

##### Expected Results

###### Service Checks
<!-- core-payload-level:4 -->

토큰 교체 뒤에는 이전 token과 기존 cookie 거부를 각각 검증해야 회전 완료로 판정하며, 이미지 업그레이드는 고정된 모든 라이브러리를 import하는 노트북을 열어 확인한다.

###### Evidence
<!-- core-payload-level:4 -->

종료 코드, 이미지 태그, 소스 커밋, 파일 개수를 기록한다. 토큰이나 노트북
내용은 절대 기록하지 않는다.

##### Unverified Conditions

이 runbook이 아직 관찰하지 못한 항목은 다음과 같다.

- 점검 명령(`config`, `ps`, `logs`): 이 문서에는 실행 결과가 기록되어 있지 않다. 종료 코드와 이미지 태그, 소스 커밋이 관찰되면 검증된다.
- 토큰 회전: 이전 token과 기존 cookie 거부를 각각 확인하기 전에는 회전 완료로 볼 수 없으며 실행 기록이 없다. 선택한 base의 cookie-secret 동작도 확인되지 않았다.
- 작업 디렉터리 복원과 이미지 업그레이드: 실행 결과가 기록되어 있지 않다. 격리 인스턴스에서 노트북의 라이브러리 import가 관찰되면 검증된다.
- MLflow 기록 확인: 승인된 `LAB_JUPYTERLAB_MLFLOW_TRACKING_URI`가 없으면 수행하지 않으며 SPEC-0262 미결정 항목이다.

#### Escalation

##### Next Owner

책임자는 `@buenhyden`이다. 위 중단 조건과 영향받은 서비스·대상 소유자를 함께 기록하고, 추가 변경 없이 보고한다.

##### Recovery or Forward Repair

설정은 검토된 Compose와 requirements로 복원하고, 보존된 이전 이미지 식별자를
우선 확인한다. 재빌드가 원래 이미지와 같다는 보장은 없다. 사용자 데이터는 먼저
서버를 정지한 뒤 격리 복원·해시 검증을 수행한다. 아래는 빈 작업 디렉터리의 과거
리허설이며 현재 사용자 데이터·kernel·의존성 복구를 증명하지 않는다.

원본: `docs/05.operations/03.runbooks/13.analytics-and-data-quality/0089-jupyterlab.md`, SPEC-0198 이전 Git 기록.

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

## 적용과 확인

### 적용 방법

Use the procedures or reading order stated in the role payload.

### 확인 기준

Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.

## 관계와 출처

### 관련 문서

The role payload retains the current owner and dependency references.

### 외부 근거

External basis and its limits remain those stated in the role payload; a citation grants no authority.
