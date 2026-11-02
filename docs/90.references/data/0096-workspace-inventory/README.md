---
title: "Workspace Inventory"
version: "0.7.0"
type: "reference/data-pack"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-03"
layer: "references"
artifact_id: "DATA-0096"
parent_ids:
- "SPEC-0212"
- "SPEC-0212-TSK-0040"
- "SPEC-0212-TSK-0041"
- "SPEC-0212-TSK-0042"
- "SPEC-0212-TSK-0043"
- "SPEC-0212-TSK-0044"
- "SPEC-0212-TSK-0045"
- "SPEC-0212-TSK-0046"
- "SPEC-0212-TSK-0047"
created: "2026-11-01"
observed_at: "2026-11-02"
---

# Workspace Inventory

## Overview

현재 입력 워크스페이스의 공개 파일·서비스 목록, 조사 상태, 작성권, 공식 근거와
미완료 인계 정보를 보관하는 비규범 참고 자료다. 생성 전에 현재 소비자를
SPEC-0212 TSK-0040과 후속 P02–P12 인계로 확정했다. 서비스 구현과 운영 인수의
정본은 각 기존 사양과 작업 기록에 남는다.

## Scope

### Schema

`data.yaml`은 공개 목록과 제외 집계만 담는다. 파일 목록·본문 검토·구성 렌더·
현재 실행·복원은 각각 분모와 분자를 갖는다. 별도 검토 기록은 검토자·시각·
파일 지문·검토 범위에 결속하며, 해시 계산만으로 본문 검토를 완료하지 않는다.
검토 기록의 `complete`는 기본값이 `false`인 선택 불리언이다. 해당 파일 전체를
검토한 명시적 `complete: true`만 `REVIEWED`와 전체 본문 검토 분자에 포함한다.
구간 검토와 생략값은 `PARTIAL`로 따로 집계하고, 파일 지문이 바뀌면 검토를
`STALE`로 바꿔 관련 범위만 다시 확인한다.

포트 메타데이터의 공개 네트워크 참조 필드는 `network_reference`다. 기존 포트
파서가 사용하는 `network_key`를 원본에서 바꾸지 않고, 이 공개 원장에 투영할 때만
필드 이름을 변환한다. 실제 공개 네트워크 이름과 연결 의미는 보존한다.

### Limitations

사설 경로별 메타데이터와 정제된 명령 기록은 로컬 분석 영역에 둔다. 비밀값·
인증 파일 본문·값 해시·원시 운영 로그는 수집하지 않는다. 전체 목록 확보는
모든 본문·프로필 조합·실운영·독립 복원의 검증을 뜻하지 않는다. 미열람과
미실행은 해당 필드에 남으며, 과거 수용을 현재 직접 운영 성공으로 옮기지 않는다.

## Structure

공개 단일 자료 파일 `data.yaml`은 워크스페이스와 루트, 파일·서비스·연결,
조사 분모, 요구 판정, 완료 재사용, 단일 작성권, 공식 조사, 계층·학습별 적용성과
미완료 인계를 담는다. 이 패키지에 별도 조사 본문이나 원시 로그를 추가하지 않는다.

## Usage

### Refresh

`scripts/operations/workspace-inventory.py`의 `scan`, `compare`, `validate`를
사용한다. 구현은 `scripts/lib/ops/workspace_inventory.py`와
`scripts/lib/ops/_workspace_services.py`, 격리 렌더 구현은
`scripts/lib/ops/_workspace_render.py`이며 기존 포트 원장 해석을 재사용한다.

실제 경계와 현재 지문을 다시 확인한 뒤 목록을 수집한다. 검증한 공개 자료를
원자적으로 교체하고 이전 관측과 비교하여 영향받은 행만 재조사한다. 생성된
자료 자신의 해시는 순환 계산에서 제외하고 이유를 기록한다. 사용자 변경은
보존하며 경계 밖 심볼릭 링크와 외부 체크아웃을 수정하지 않는다.

관측 파일을 다시 수집하는 다음 명령은 실제 존재하는 이 실행의 로컬 검토
기록을 사용한다. 다른 실행에서는 자신의 실제 검토 기록 경로를 먼저 확인한다.
결과는 로컬 비교용이며, 렌더를 요청하지 않으므로 구성·서비스를 실행하지 않는다.

```bash
rtk python3 scripts/operations/workspace-inventory.py scan --root . --output _workspace/repo-support/analysis/p01/reviewed-public.yaml --reviews _workspace/repo-support/analysis/p01/doc-reviews.yaml
```

검토 기록의 필수 필드는 `path`, `reviewer`, `observed_at`, `sha256`, `scope`다.
현재 편집한 구간만 읽은 기록을 `complete: true`로 바꾸지 않는다. 공개 사본과
이전 관측 비교 및 원장 검증은 각각 `compare`와 `validate`를 사용한다.

`--render`는 공개 소스 복제본과 합성 입력만으로 제한된 구성 검사를 수행한다.
사설 입력은 합성 파일로 대체하고 경계 밖 포함·상속 경로는 거부한다. 각 사례의
성공·실패·오류·시간 예산으로 인한 미실행을 따로 남긴다. 수집이나 메타데이터
검증 명령의 성공을 모든 구성 사례 또는 실제 서비스 실행의 성공으로 읽지 않는다.

`--render-inputs`는 `--render`와 함께 사용하는 명시적 합성 입력 계약 파일이다.
파일 전체는 사례 목록이어야 한다. 각 사례는 `source`, `selection`으로 식별하며,
선택 항목 `files`에는 base를 먼저, 선택한 overlay를 마지막에 둔다. `variables`는
변수 이름을 `directory`, `file`, `image`, `integer`, `port`, `subnet`, `text` 중
하나에 연결한다. 실제 값은 임시 복제본에서만 생성한다. 선언되지 않은 변수,
실행 환경을 제어하는 변수 이름, 알 수 없는 자료형과 경계 밖 경로는 거부한다.

다음은 현재 선언된 예제의 합성 입력 메타데이터다. 자격 값이 아닌 자료형만
기록한다. 전체 원장을 입력 파일로 전달하지 않는다.

```yaml
- source: examples/operations/postgres-logical-upgrade/docker-compose.yml
  selection: all-profiles
  variables:
    IOR_POSTGRES_PASSWORD: text
```

공개 계약의 정본 목록은 `data.yaml`의 `compose.synthetic_interpolation_inputs`다.
이 목록만 실제 존재하는 로컬 메타데이터 파일로 추출한 뒤 `--render-inputs`에
전달한다. 실제 `.env`나 운영 자격을 입력으로 사용하지 않는다. 공개된 기록은
변수 이름·자료형·결과만 포함하며 생성한 합성 값도 보관하지 않는다.

루트에 포함되는 leaf와 overlay의 검사는 공통 망 정의를 포함하는 루트 문맥을
사용한다. 별도 예제는 문서에 지정된 base 조합과 그 조합의 필수 입력을 명시한다.
누락 입력을 임의의 운영 값으로 채우거나, 실제 예제의 결함을 검사기 성공으로
바꾸지 않는다. 사례의 안전한 오류 코드와 후속 작성자·재개 조건을 따로 남긴다.

P01의 역사 후속 검사는 이전 성공 182건의 원래 실행 시각과 결과를 보존하고, 영향받은
21건만 다시 실행해 20건 성공·1건 실패를 기록했다. 같은 69개 구성 소스 지문과
정규화한 호출·준비 입력의 동등성 확인은 이전 결과 재사용의 근거이며 새 구성
실행 성공이 아니다. 합계는 203건 중 202건 성공이고, 남은 준비 상태 예제의
망 정의 결함은 정확한 소스·작성권·재개 조건과 함께 별도 인계한다.

P01에서 선택된 로컬 검사 여섯 묶음과 수정 후 일곱 번째 무결성 검사 720건은 각각
실제 통과했으며, 마지막 검사에서 P01 48건도 모두 통과했다. 이전 환경별 실패는
이력으로 보존한다. 별도 실행한 이 결과를 전체 14개 검사 일괄 통과·원격 CI·
실제 호스트 신뢰·서비스 운영 인수로 확대하지 않는다.

### Consumers

[현재 작업](../../../03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0040-workspace-inventory.md)은
시작·종료 비교와 인수 근거로 읽는다. P02–P12의 후속 담당은 서비스별 소스 지문·
소비자·증거 수준·단일 작성자와 재개 조건을 인계받는다. 이 연결은 운영 권한을
부여하거나 후속 업무의 완료를 선행 조건으로 만들지 않는다.

P02는 같은 공개 자료를 연결 근거로 읽되, `scan --connections`의 새 공개 추출
결과가 검증·생성되기 전에는 기존 서비스 행을 제품 내부 등록이나 운영 연결의
증거로 승격하지 않는다. P02의 결과는 호출 주체, provider, 네 종류의 포트,
인증 방식, 설정 지문, 채택 판단과 제품 등록 증거 수준을 값 없이 기록한다.
비밀 URL·토큰·인증 본문·원시 설정 출력은 이 패키지와 로컬 curation 기록 모두에
넣지 않는다. P03, P04/P05, P06, P07, P08은 각자의 정본과 인수 범위를 유지한다.

[P03 모델·Runner·Wiki 준비 Task](../../../03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0042-models-runners-wiki.md)는
공개 소스 지문과 연결 근거를 소스·격리 증거로만 소비한다. 제어된 Worker native
경로 1건의 PASS는 제품 등록이나 실제 모델 추론을 뜻하지 않으며, 정확한
SurrealDB 이미지 부재에 따른 Notebook native와 보정 뒤 Runner native는 `NOT_RUN`으로
남는다. 운영·복원·원격 CI·최종 인수는 이 자료나 P03의 로컬 증거로 승격되지 않는다.

P02가 선택한 기본 토폴로지는 공유 MNG Valkey다. 이름별 n8n ACL과 전용 broker
선택 구성은 재사용 대상이며, 자격 발급·회전·운영 queue drain·독립 복원은 P06과
실제 데이터 소유자에게 남는다. Grafana의 공개 정적 예외는 정확한 두 경로의
GET/HEAD만을 대상으로 하며, 그 밖의 메서드와 모든 다른 경로는 인증/라우팅
계약에 따라 처리한다. 이 예외는 2026-12-02에 또는 범위 확대·인증 변경·관련
보안 권고가 발생하면 다시 검토한다.

[P06 Secret 구조·OpenBao Task](../../../03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0045-secret-structure-openbao.md)는
공개 Secret catalog를 정본으로 재사용하고, 값 제외 구조 검사·SMTP 읽기 경계·
과거 소비자 수용과 잔여 인계를 기록한다. 실제 `.env`와 로컬 registry는 사용자가
승인한 읽기 전용 비교 대상이며 값·값 해시·길이·원문은 이 원장에 넣지 않는다.
합성 누출 시험과 독립 보안 검토 뒤의 실제 비교에서 env와 registry는 각각
`DRIFT`, 역사 SMTP 사본은 `OLD_ABSENT`/미비교로 관찰됐다. 이후 승인된 무값
진단의 첫 공개 기준 위치는 env 52행 `PUBLIC_ASSIGNMENT`, registry 18행
`PUBLIC_TEXT`다. SMTP 부재는 진단 추가 전 보안 승인 소스에서 관측했으며 진단
추가 후 SMTP 경로를 재실행한 결과는 아니다. 공개 기준 위치는 사설 파일의 행 번호나
차이 원인을 뜻하지 않는다. 사설 수정을 허용한
것은 아니며 값 일치·소비 전환·삭제 수용을 뜻하지 않는다. 실제 운영·회전·
독립 복원·원격 CI·최종 인수는 각각의 별도 기록에 따른다.

[P04 Opsflow Task](../../../03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0043-opsflow-data-path.md)는
기존 Airflow DAG·adapter·DEV 소유권을 재사용하고 연결 인코딩·불량 입력 격리·
data_version·객체 메타데이터 복원의 차분을 소비한다. 기존 CDC의 `platform_dev`와
Opsflow의 `opsflow_dev`는 다른 소유권 계약이며 임의로 연결하지 않는다. dbt/GX와
선택형 분석 엔진의 연결 시험은 업무 게시 완료가 아니다. Iceberg 플랫폼의 과거
수용은 보존하고 이번 workload 채택은 보류한다. 새 실험은 실제 데이터·시간 필드·
목표·기준선·소유자 입력까지 보류하며 사설 notebook의 존재나 내용을 추정하지 않는다.

P04 시작 시점의 실제 HEAD는 `6853286dbd73851a6419f7fb5457c53720ba6d98`이고
작업트리는 깨끗했다. 이 값과 이전 P03의 pre-commit 관측을 구분한다. 최종 목록은
소스 동결 뒤 다시 수집하며, 해시 계산을 본문 검토나 제품 기능 인수로 집계하지 않는다.
격리 대상 복원과 실제 HOME 복원, 운영·회전·원격 CI·최종 인수는 독립 결과다.
공개 `coverage.runtime`과 `coverage.restore`는 원장에 선언된 실제 서비스의 이번
운영·복원 관측 분모다. 합성 fixture의 별도 컨테이너 실행·복원 결과는 해당 Task의
격리 증거로 기록하며 이 분자에 더하지 않는다. `--render` 없는 목록 갱신은 이전
구성 실행 결과를 새 실행으로 재사용하지 않으며 과거 결과와 선택형 렌더 증거는
각 Task에 보존한다.

[P05 notifier Task](../../../03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0044-opsflow-notifier-recovery.md)은
기존 C19/C22의 version·이미지·환경·Criterion별 수용을 재사용하고 현재 재처리·복원
장벽·STARTTLS·credential 조회의 차분을 소비한다. clean 시작 HEAD는
`e14ebe0fd5e562f8c7557bd9408a1985d9971c5c`로 관측했으며 당시 branch는
`codex/p05-n8n-outbox-recovery`였다. 과거 수용, 공개 source binding과 실제
private workflow·설치 이미지·운영 자격은 별도 축이다.

SQL007/008은 개별 승인에 한 번의 no-send 추가 claim과 복원 sending의 unknown
격리를 제공한다. 관리 함수의 증거 지문은 외부 실행 장벽 attestation이며 SMTP
fencing이나 capture 부재의 no-send 판정을 대신하지 않는다. 기본 plain capture와
선택형 인증 STARTTLS 모두 격리된 고정 Mailpit 대상만 허용한다. Node package의
owned loopback 검사는 실제 n8n Worker/Mailpit·DB native 수용과 구분한다.
같은 native credential ID의 다음 실행 조회는 P06의 실제 발급·정본·회전과 다르다.

선택 notifier는 binary를 소비하지 않고 신규 저장소를 만들지 않는다. 고정 release
source의 queue 기본값과 최신 generic 문서의 기본값을 구분하며 실제 override를
읽었다고 주장하지 않는다. P08의17-input SOURCE_REVIEW_ONLY binding 갱신은
이전 이력을 보존한 공개 소스 지문 보정이다. 서명·새 이미지 build·HOME 적용·복원
성공으로 승격하지 않는다. P12 offline quarantine seam 보정도 실제 Airflow→n8n
종단 수용이나 P04 Worker/복원 잔여를 닫지 않는다.

P05의 최종 owned editor-REST 시험은747.701초와 cleanup PASS로 끝났다. 실제
Worker/Bull/인증 STARTTLS, 잘못된 old/new 자격의 unknown 보존, 같은 ID의 다음 실행
갱신과 gen2 DB/metadata+같은 합성 encryption key를 통한 fresh 실행을 확인했다.
복원은 해당 기록된 범위로만 수용하며 같은 입력 replay·기존 unknown/accepted와
attempt/audit 동등성·live-inflight 중단은 TEST_RESIDUAL이다. 이전 세 번의 ERROR와
각 cleanup PASS는 보존한다. 격리 PASS를 실제 운영·P06 발급/회전·외부 배달·원격 CI·
P12 최종 인수로 옮기지 않는다. P03의 전역 CI admission 잔여도 별도 인계한다.

[P07 관측 Task](../../../03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0046-exporter-observability.md)는
공개 선택 계획과 기대 대상의 근거를 소비한다. SPEC-0224의 DB 관측과 SPEC-0214의
인증 OTLP에 관한 과거 수용은 해당 기록의 환경과 범위에서만 재사용한다. 이번
소스·격리 시험과 실제 서비스 기동, 운영 재적재, 실제 알림, 독립 복원 및 원격 CI는
각각 별도로 기록한다. Opsflow 업무 신선도는 데이터와 업무 소유자에게 인계한다.

[P08 이미지·공급망·Storybook Task](../../../03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0047-image-supply-chain-storybook.md)는
이 자료의 공개 image/build/lock 목록을 조사 분모와 source binding으로만 소비한다.
기존 관측의 루트 Compose 44개 입력과 112개 선언을 P08 시작 분모로 재사용하며,
소스 동결 후 새 관측으로 갱신한다. 이 목록은 전체 이미지·패키지의 공식
최신성·지원·라이선스·호환·복원·서명/provenance 조사가 완료됐다는 뜻이 아니다.
`blog-ingestion` 원장 행, 48개 변경 입력 영향 행과 기존 5개 stale 행의 이력은
보존한다. 최신성 조회가 미완료이면 해당 gate는 `exit 2`/`ledger_complete: false`로
남는다. Valkey 9.1.3과 n8n 2.45.7은 개별 source/격리/복원 증거가 필요한 후보이며,
sample/base/GHCR artifact 증거를 Docker Hub 또는 custom artifact의 공급망 PASS로
전이하지 않는다. Storybook 10.6.3 clean-lock 결과는 별도 Task에 기록하며 실제
runtime·원격 인증·외부 audit은 이 패키지의 목록으로 승격하지 않는다.

## Related Documents

- [범주 색인](../README.md)
- [현재 사양](../../../03.specs/0212-request-baseline-and-reconciliation/spec.md)
- [현재 계획](../../../03.specs/0212-request-baseline-and-reconciliation/plan.md)
- [P02 서비스 연결 Task](../../../03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0041-service-connection-contracts.md)
- [P03 모델·Runner·Wiki 준비 Task](../../../03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0042-models-runners-wiki.md)
- [P05 notifier 복구 Task](../../../03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0044-opsflow-notifier-recovery.md)
- [P07 관측 Task](../../../03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0046-exporter-observability.md)
- [P08 이미지·공급망·Storybook Task](../../../03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0047-image-supply-chain-storybook.md)
- [P04 Opsflow 데이터 경로 Task](../../../03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0043-opsflow-data-path.md)

## Sources

실제 소스 선언, 기존 수용 기록, 공식 자료와 직접 확인한 시각을 공개 자료의
해당 행에 연결한다. 제공된 역사 조사와 이번 직접 조회를 구분하고 접근 실패와
게시 연도 미확인을 보존한다. 새 버전의 존재는 설치·이미지·운영 검증과 다르다.
