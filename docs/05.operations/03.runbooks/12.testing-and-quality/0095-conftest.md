---
title: "Conftest Recovery Runbook"
version: "2.0.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
layer: "operations"
artifact_id: "RUN-0095"
parent_ids:
- "GDE-0095"
created: "2026-09-23"
next_review_at: "2027-05-13"
---

# Conftest Recovery Runbook

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

`conftest` 정책 검사 작업이 실패했을 때 원인을 찾고 수정하는 런북이다.

`conftest` 작업이 0이 아닌 상태로 종료될 때 사용한다.

##### Targets

- [Guide](../../01.guides/12.testing-and-quality/0095-conftest.md) (`GDE-0095`)
- [Policy](../../02.policies/12.testing-and-quality/0095-conftest.md) (`POL-0095`)
- [Conftest Compose](../../../../infra/11-quality/conftest/docker-compose.yml)

- [Conftest 패키지 README](../../../../infra/11-quality/conftest/README.md)

#### Preflight

##### Authority

저장소 루트의 승인된 로컬 컨테이너 작업만 대상으로 한다. 원본이 읽기 전용이어도 컨테이너 생성은 정적 문서 검사와 구분한다.

##### Environment

이 런북은 별도 백업이나 읽기 전용 사전 점검을 요구하지 않고, 저장소 루트에서 승인된 로컬 컨테이너 작업을 실행해 첫 실패 단계를 읽는 것으로 시작한다.

#### Procedure

##### Steps

| Step | Action | Expected Result | On Failure |
| --- | --- | --- | --- |
| 1 | 저장소 루트에서 `bash scripts/validation/check-conftest-policy.sh`를 승인된 로컬 컨테이너 작업으로 실행하고 첫 실패 단계/줄을 읽는다 | wrapper가 0으로 종료하면 통과한다 | `secrets/`/`.env`/Docker 소켓 마운트 요청이나 `deny`를 `warn`으로 바꾸는 요청은 중단 |
| 2 | Docker 호출 전 준비 실패는 추적 여부, canonical overlay/base/profile 관계, 입력 경로/한계를 확인하고 `--mode verify`/`--mode corpus`로 실패 lane을 분리한다 | 문서에 기록 없음 | raw fallback이나 무시 목록으로 통과시키지 않음 |
| 3 | `FAIL - <file> - compose/dockerfile - ...`는 선언과 규칙을 명시하며 이미지 고정, Docker secret 이전, `--checksum` 추가 등 해당 선언 위반을 원본에서 수정한다 | 문서에 기록 없음 | 검증된 부분 overlay의 profile을 중복/재정의하지 않음 |
| 4 | 선언이 의도한 것이면 정책 파일의 allowlist를 사유와 함께 검토받은 변경으로 바꾼다 | 문서에 기록 없음 | 실패를 숨기기 위한 deny 완화는 하지 않음 |
| 5 | 종료 코드만으로 파싱 실패를 단정하지 않고 verify/Compose/Dockerfile 중 실행된 단계와 오류로 파싱/규칙/실행 환경 문제를 구분한다 | 실제로 실행된 단계의 요약/exit만 기록하고 실행되지 않은 단계는 미실행으로 남긴다 | 문서에 기록 없음 |
| 6 | 수정/업그레이드/복구: 실패 입력과 기존 통제의 소유자를 확인하고 source 위반은 선언을 수정하며 규칙 결함은 정책 테스트와 근거를 보존해 검토받는다 | 문서에 기록 없음 | 이미지/Rego 변경이 문제면 검토한 이전 소스로 rollback |

1. 저장소 루트에서 승인된 로컬 컨테이너 작업을 실행하고 첫 실패 단계·줄을 읽는다.

   ```bash
   bash scripts/validation/check-conftest-policy.sh
   ```

2. Docker 호출 전 준비 실패는 추적 여부·canonical overlay/base/profile 관계와
   입력 경로·한계를 확인한다. 무시된 설치 산출물은 읽지 않는다. `corpus`·기본
   실행을 직접 job으로 호출해 준비 입력이 없다면 위 wrapper를 사용한다.
   raw fallback이나 무시 목록으로 통과시키지 않는다. `--mode verify`와
   `--mode corpus`로 실패 lane을 분리할 수 있다. `verify` 요약의 실패는 `infra/11-quality/conftest/policy/`의 깨진 규칙이나
   테스트다. 무엇보다 Rego부터 수정한다.
3. `FAIL - <file> - compose - service <name>: …` 또는 `… - dockerfile - …`는
   선언과 규칙을 명시한다. 일반 서비스의 누락 profile은 원본에서 수정한다.
   검증된 부분 overlay는 base profile을 상속하므로 profile을 중복·재정의하지
   않는다. 이미지를 고정하거나 리터럴을 Docker secret으로 옮기거나
   `--checksum`을 추가하는 등 해당 선언 위반을 수정한다.
4. 선언이 의도한 것이면(예: 새 권한 필요), 정책 파일의 allowlist를
   사유와 함께 검토받은 변경으로 바꾼다.
5. 종료 코드만으로 파싱 실패를 단정하지 않는다. wrapper의 `2`는 사용법 오류,
   입력 준비 실패, Docker 불가용, 준비 manifest 누락·digest 불일치일 수 있고
   job 안의 xargs·shell 상태가 전달될 수도 있다. verify/Compose/Dockerfile
   중 실행된 단계와 오류를 확인하고 파싱·규칙·실행 환경 문제를 구분한다.

###### 수정·업그레이드·복구
<!-- core-payload-level:4 -->

규칙과 파일 수정 전 실패 입력·기존 통제의 소유자를 확인한다. source 위반은 선언을
수정하고, 규칙 결함이면 해당 정책 테스트와 근거를 보존해 검토받는다. 실패를 숨기기
위한 deny 완화는 하지 않는다. 이미지·Rego 변경은 버전에 맞는 release/API와 정책
테스트를 확인하고 검토한 이전 소스로 rollback한다. 작업 자체 데이터·credential·TLS
복원은 적용되지 않으며 Git의 정책 원본과 정제된 검사 근거만 보존한다.

##### Stop Conditions

`secrets/`, `.env` 또는 Docker 소켓을 작업에 마운트하라는 요청, 또는 실패하는
변경을 통과시키기 위해 `deny`를 `warn`으로 바꾸라는 요청이 있으면 중단한다.

#### Verification

##### Expected Results

###### Service Checks
<!-- core-payload-level:4 -->

`scripts/validation/check-conftest-policy.sh`가 0으로 종료하면 통과이고, 0이 아니면 첫 실패 단계·줄을 읽어 원인을 분리한다.

###### Evidence
<!-- core-payload-level:4 -->

실제로 실행된 단계의 요약·exit와 소스 커밋을 기록한다. 첫 실패 뒤 실행되지 않은
단계는 미실행으로 남기며 세 요약을 만들거나 전체 PASS로 해석하지 않는다.

##### Unverified Conditions

이 runbook이 아직 관찰된 적 없는 항목은 다음과 같다.

- `check-conftest-policy.sh` 실행: 이 문서에는 실행 결과가 기록되어 있지 않다. wrapper 종료 코드 0과 실행된 단계의 요약이 검증 근거가 된다.
- 첫 실패 뒤 실행되지 않은 단계: 문서는 미실행으로 남기고 전체 PASS로 해석하지 않는다고 밝힌다. 각 단계(verify, Compose, Dockerfile)의 개별 요약이 검증 근거가 된다.
- 정책 allowlist 변경, 이미지/Rego 변경과 rollback: 검토가 필요하며 이 문서에는 실행 결과가 기록되어 있지 않다. 정책 테스트 통과가 검증 근거가 된다.

#### Escalation

##### Next Owner

책임자는 `@buenhyden`이다. 위 중단 조건과 영향받은 서비스·대상 소유자를 함께 기록하고, 추가 변경 없이 보고한다.

##### Recovery or Forward Repair

검사 원본과 운영 데이터는 변경하지 않는다. wrapper가 만든 임시 공개 입력과 일회성 job은 종료 시 정리하며 작업 데이터 복원은 적용되지 않는다.

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
