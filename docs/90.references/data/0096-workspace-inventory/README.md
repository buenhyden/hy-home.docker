---
title: "Workspace Inventory"
version: "0.8.1"
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
- "SPEC-0212-TSK-0048"
- "SPEC-0212-TSK-0049"
- "SPEC-0212-TSK-0050"
created: "2026-11-01"
observed_at: "2026-11-03"
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
전이하지 않는다. Storybook 10.6.3 clean-lock 결과는 별도 Task에 기록하며 실제 <!-- runtime-version-exception: history — dated clean-lock observation; the Task is the evidence authority, not a runtime selection. -->
runtime·원격 인증·외부 audit은 이 패키지의 목록으로 승격하지 않는다.

P08 원장은 2026-11-02T22:15:52Z부터 22:16:20Z까지 61개 공개 릴리스 URL을
관측해 60개 응답과 1개 접근 실패를 기록했다. 기존 source owner/release URL은
112개 root 서비스 중 99개에 연결되고 13개는 미연결이며, Valkey/n8n 9개 서비스는
별도 후보 기록으로 대조한다. 원시 영수증은 보관하지 않으며 각 행은
`PUBLIC_SOURCE_OBSERVATION_ONLY`다. 공개 페이지·tag는 24시간 최신성, OCI
artifact, 안정 채널, 보안 적용성, 호환·라이선스, 실행·배포 수용의 증거가 아니다.
각 행의 `freshness_verified`, `stable_channel_verified`,
`oci_availability_verified`는 모두 `false`다.

별도 upstream 관측은 정확한 GHCR index digest에서만 n8n image signature+SLSA,
runners CycloneDX+OpenVEX의 보고된 성공을 남긴다. runners image signature/SLSA와
n8n CycloneDX의 부재·오류는 따로 남으며, Valkey signing identity/issuer는
`NOT_ASSESSABLE`이다. 명령 transcript·원시 영수증·UTC 창은 보관하지 않았고,
builder/parameters 및 SBOM/VEX 의미는 검토하지 않았다. 따라서 이 기록은 custom
image, native 기능, 호환·복원·배포 또는 운영 수용으로 전이되지 않는다.

이후 정확한 OIDC issuer와 certificate identity로 n8n/runners 네 index 관측을
재검증했다. 여기의 Cosign 3.1.3과 Syft 1.54.1은 해당 로컬 관측 실행의 도구 버전이며
서비스 런타임 pin이나 이미지 선택 근거가 아니다. 고정 Cosign 3.1.3에서 n8n signature/SLSA와 runners CycloneDX/OpenVEX은
각각 exit 0이었지만, payload는 `/dev/null`로 처리하고 원시 영수증은 보관하지 않았다.
정확한 시간·digest·identity는 P08 Task와 원장에 결속한다. Valkey amd64는 고정 Syft
1.54.1로 로컬 CycloneDX 1.7 SBOM(Alpine 3.24.3, 716 components)을 생성했을 뿐 <!-- runtime-version-exception: history — dated local SBOM-tool observation; it is not a runtime pin or publisher attestation. -->
publisher attestation이 아니다. 현재 runtime source는 [기술 버전 정본](../../../../infra/tech-stack.versions.json)에 남는다. Grype offline DB 부재(exit 1)로 취약점 scan은
`BLOCKED`/`NOT_RUN`이며, 네트워크 DB 다운로드는 하지 않았다.

[P09 역할·자원·퇴역 Task](../../../03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0048-role-resource-retirement.md)는
이 자료의 공개 service·consumer·profile 선언만으로 15개 역할 비교를 수행한다.
선언은 현재 실행·사용량·데이터 소유자·복구 완료의 증거가 아니며, 알 수 없는 행은
`UNKNOWN`으로 남긴다. SPEC-0246 C1–C6의 저장소 배치는 기존 수용 범위에서 재사용한다.
새 저장소 이동·리밋 변경·서비스 통합·실제 삭제는 별도의 대상·권한·복구 조건이
확인될 때만 재개한다.

P09는 보존된 98개 검토 receipt를 입력으로 공개 `scan` 뒤 `validate`를 실행했다.
그 controls source freeze 후 최종 로컬 결과는 파일 42,018/42,018, 전체 본문 6/2,322, 부분 본문 78/2,322,
렌더 0/17, 실행 0/112, 복원 0/112이다. 이 새 목록/메타데이터 관측은 본문·구성·운영·복원
수용이 아니며, 공개 정본 `data.yaml` 교체는 최종 source 동결 뒤 별도 비교에서만 한다.

P10의 후속 공개 `scan --connections`은 처음에는 기존 검토 receipt를 보존하지 않아
거부됐다. 이후 기존 98개 공개 review metadata와 이 자료의 7개 curated 섹션을 입력으로
다시 생성해 receipt와 변경 입력 무효화를 보존했다. 최종 `validate`는 metadata
consistency만 PASS했으며, 이 갱신은 본문·구성·운영·복원 수용이 아니다.

P11 final-source refresh도 98개 공개 review metadata와 7개 curated 섹션을 보존한
`scan --connections`으로 생성했고 `validate`를 실행했다. 이전 42,102/42,102와
42,091/42,091은 각 시점 관측으로 보존하며, 현재 재수집 관측은 파일
42,094/42,094, 전체 본문 6/2,337, 부분 본문 77/2,337, 렌더 0/17, 실행 0/112,
복원 0/112이다. 42,102→42,091의 11개 차이는 `excluded.generated`
38,748→38,737뿐이었다. 42,091→42,094의 공개 파일 목록 경로는 같고, 제외 집계는
generated 38,737→38,741 및 private 241→240으로만 달라졌으며 binary/code/config/
document는 35/132/482/120으로 유지됐다. 이 공개 원장은 정확한 생성물·사설 경로
또는 어느 변화의 원인을 확인하지 않았다. 이는 Hermes cache-only isolated E2E,
운영·Windows ACK·remote CI 수용을 대체하지 않는 metadata observation이다.

**S01–S11 현재 이행 요약 — 범위와 읽는 방법.**

사용자 요청의 S01–S11은 이 저장소에 별도 정본 식별자로 존재하지 않는다. 이 표는 요청 순서대로 현재 `SPEC-0212`의 P01–P11 및 `TSK-0040`–`TSK-0050`에 대응시킨 **2026-11-03 상태 요약**이다. 기준 소스는 로컬 커밋 `4b1cd14cce32548139dbca0be017e2d373ad3e1d`이며, 각 행의 상세 Criterion, 입력 지문, 실행 시각, 작성권과 원시 증거는 링크한 Task가 유일한 정본이다. 역사 `SPEC-0204`의 같은 P 번호는 별도 업무이므로 이 표의 P 번호와 혼동하지 않는다.

`PASS`는 행에 적은 로컬 소스·정적·합성 또는 격리 검사의 결과만 뜻한다. `NOT_RUN`, `ERROR`, `FAIL`, `TEST_RESIDUAL`, `BLOCKED`는 다른 PASS로 닫히지 않는다. 사설 값·토큰·자격 본문·원시 운영 로그는 이 요약에 포함하지 않으며, 운영 서비스, 실제 자격 회전, 외부 송신, 원격 CI와 최종 운영 인수는 각 Task가 직접 기록하지 않은 한 미실행이다.

| 요청 / 현재 Task | 이번에 구현·재사용한 범위 | 확인된 로컬 증거 | 미완료·보류·실패 | 재개 조건과 정본 |
| --- | --- | --- | --- | --- |
| S01 / P01 — [TSK-0040](../../../03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0040-workspace-inventory.md) | 공개 `scan`/`compare`/`validate`, 파일·서비스·작성권·13계층/8학습축 원장과 DATA-0096을 구현했다. | 21개 잔여 렌더 재시험 중 20개 `PASS`; 나머지 182개는 같은 입력 지문의 과거 성공 결과를 **재실행 없이 재사용**했다. | `compose-core-readiness` override의 `!override`가 `edge_net`을 정의하지 않아 1개 `FAIL`; 전체 본문 검토·실운영·회전·독립 복원·원격 CI·최종 인수는 미실행이다. | 해당 fixture 작성자와 문서화된 base/overlay 조합을 확정·수정하고 그 조합과 영향 회귀를 다시 렌더한다. 상세 Evidence/Handoff는 TSK-0040이다. |
| S02 / P02 — [TSK-0041](../../../03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0041-service-connection-contracts.md) | listener/네 포트 계약, DEV/MNG 분리, Valkey ACL wrapper, Grafana의 정확한 두 정적 경로 GET/HEAD 예외와 연결 원장을 보완했다. | 격리 전체 SSO 3/3과 중단 정리 1/1이 `PASS`다. | 광범위 1,330건은 1,234 `PASS`, 95 `SKIP`, 오래된 n8n source receipt 1 `FAIL`이다. P05/P08 지문 정정은 그 전체 집합의 재통과 증거가 아니다. 제품 저장 설정·실자격·서비스 적용·회전·복원·원격 CI는 `NOT_RUN`이다. | 최신 P05/P08 source binding으로 관련 광범위 검사를 재실행하고, 제품 소유자·운영 창·복구 조건을 확보한다. |
| S03 / P03 — [TSK-0042](../../../03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0042-models-runners-wiki.md) | local-only/명시 모델 경로, Notebook 등록 소스, Runner 보호와 도구 목적지 정책을 구현했고 Wiki 오프라인 준비 수용을 재사용했다. | 합성 등록·소스 검증과 캐시 fixture의 Main→Valkey→Worker→합성 Ollama 1건은 `PASS`다. 이는 실제 모델 추론이 아니다. | 정확한 SurrealDB 이미지가 없어 Notebook native는 `NOT_RUN`; Runner 전체 native는 예상 모듈 거부를 분류하지 못해 `ERROR`였고, 후속 영수증 보존 수정은 정적 `PASS`일 뿐 현 소스 native 재실행·거부/peer/취소/복구·실제 egress는 미검증이다. Wiki 제품 런타임은 범위 밖이다. | 정확한 캐시 fixture와 안전 예산으로 현 소스 native를 재실행하고, Notebook 의존 이미지를 확보해 실제 등록·호출을 검증한다. 데이터·운영 소유자도 확인한다. |
| S04 / P04 — [TSK-0043](../../../03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0043-opsflow-data-path.md) | Airflow URI 단일 인코딩, **검증 실패 입력 격리**, `data_version`/읽기 view를 추가하고 DEV/MNG·outbox 계약을 보존했다. | 로컬 합성 QA 129건이 `PASS`다. | 격리 Worker 전체 리허설은 S3 principal 불일치로 게시 전에 `FAIL`(약 583초), 수정 뒤 좁은 retry는 관리자 canary에서 `ERROR`(약 190초)였다. Worker 게시·격리·독립 복원은 `NOT_RUN`이다. CDC는 실제 Opsflow 소비자/offset/복구까지 보류했고, 데이터 과학은 실제 입력이 없으며 Iceberg는 기존 선택 수용만 재사용한다. | 단계별 시간 진단 뒤 같은 안전·자원 경계에서 정정된 S3 권한 매트릭스, Worker 게시/격리와 별도 복원을 실행한다. 실제 데이터 버전·시간 필드·목표·baseline·소유자가 새 실험의 선행조건이다. |
| S05 / P05 — [TSK-0044](../../../03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0044-opsflow-notifier-recovery.md) | 승인당 추가 전송 1회, 누적 시도/감사, `unknown` 불확실성의 자동 재전송 금지, SMTP 차단·작업 확인 복원 장벽과 선택형 STARTTLS Mailpit을 구현했다. | 격리 native Worker 6회, 같은 Credential ID 갱신 뒤 새 실행, 정지 상태 복원과 캡처는 합성 입력으로 `PASS`다. | 진행 중 전송 중단, 같은 입력 replay와 기존 `unknown`/`accepted`·audit/attempt 동등성, 잔존 Queue 작업 차단 뒤 재개는 `TEST_RESIDUAL`이다. 실제 자격 회전·운영 메일·최종 전달·원격 CI는 `NOT_RUN`; SMTP 수락은 최종 전달 증거가 아니다. | 소유한 합성 fixture에서 잔여 복원 시나리오를 실행·결속한다. 실제 전환은 P06 정본·발급/회전 계약과 운영 승인·복구 경계가 필요하다. |
| S06 / P06 — [TSK-0045](../../../03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0045-secret-structure-openbao.md) | 값 제외 구조 검사, SMTP 제한 읽기, 합성 누출 회귀와 n8n 인계 계약을 구현했다. | 공개 catalog/구조와 합성 보안 회귀는 별도 로컬 증거로 보존했다. | 읽기 전용 실제 env/registry 구조 비교는 `DRIFT`/`FAIL`; SMTP 정본은 존재하나 역사 사본이 없어 값 비교는 `NOT_RUN`이다. 사설 정정·실제 소비/회전·독립 복원·퇴역은 `NOT_RUN` 또는 `BLOCKED`다. | 소유자와 승인된 사설 읽기 범위, 유효 자격 및 롤백 근거를 확보한 뒤 값 없는 구조 차이부터 해소한다. 사설 값을 출력·복제하거나 임의 전환하지 않는다. |
| S07 / P07 — [TSK-0046](../../../03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0046-exporter-observability.md) | 동반 기동 계획, 선택 대상/경보, 합성 Prometheus·Alloy와 패널 검사를 구현했다. | 격리 지표·패널·규칙 검증은 `PASS`다. | 실제 작업공간 계획 생성은 group-writable 출력 경로의 안전 검사에서 거부됐다. 실제 지표·알림·재적재·복원·원격 CI는 `NOT_RUN`이다. | 소유자가 관리하는 안전한 출력 경로·권한을 확보하고 계획을 재생성·검증한다. 운영 관측·알림 전달은 별도 환경/권한으로 실행한다. |
| S08 / P08 — [TSK-0047](../../../03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0047-image-supply-chain-storybook.md) | 이미지 원장 누락/지문을 정정했고 현재 pin의 Storybook 격리 build·브라우저 검사와 후보 Valkey의 합성 ACL/복원을 검증했다. | 위 Storybook 및 Valkey 격리 범위는 `PASS`다. | 후보 n8n artifact 확보가 중단돼 활성 전환은 보류됐다. Valkey 운영 전환은 `NOT_RUN`; 13개 서비스 매핑과 서명·provenance·SBOM·취약성 판정은 미완성이며 `npm audit`은 DNS 실패 `ERROR`다. | 정확한 artifact/digest·발행자, 전체 호환·독립 복원 근거와 필요한 취약점 DB/네트워크 권한을 확보한 뒤 후보별로 재개한다. |
| S09 / P09 — [TSK-0048](../../../03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0048-role-resource-retirement.md) | 15 역할 비교, overlay 제어·평가 근거 결속과 퇴역 manifest 입력 보호를 구현·시험했다. | 해당 정적/합성 시험은 `PASS`다. | 실제 리밋 변경·서비스 통합·스토리지 이전·삭제는 수행하지 않았고 `NOT_RUN`이다. | 대표 부하, 소유자·RPO/RTO, writer 중지, 백업·복원 근거를 확보한 정확한 대상만 별도 승인으로 다룬다. P03 parity와 P04/P05 selector의 과거 CI 실패는 P10에서 정정한 역사 기록이다. |
| S10 / P10 — [TSK-0049](../../../03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0049-document-governance-qa-ci.md) | Task 근거 형식, P03 공개 validator, P04/P05 필수 selector, hook 소유권/조건과 결과 수명주기를 정정했다. | TSK-0049의 당시 link-alignment는 exit 0과 역사 경고 1로 기록됐고, 이전 metadata/corpus `FAIL`은 P11 후속 metadata/corpus `PASS`와 날짜별로 구분된다. | 이 당시 Task 범위의 기록은 이후 전체 alignment 경고 232건의 해소를 뜻하지 않는다. 원격 CI와 실제 provider hook 전달/수용도 `NOT_RUN`이다. | 현재 변경 집합으로 hosted CI를 실행하고, 전체 alignment의 현재 경고를 해당 소유자별로 분류한다. 신뢰된 provider 환경에서 hook delivery를 관측하며, 계획 생성이나 로컬 selector `PASS`로 대체하지 않는다. |
| S11 / P11 — [TSK-0050](../../../03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0050-hermes-provenance-trust-export.md) | 수집 영수증, 불변 제출, 엄격한 Gateway 영수증, 대기함/Attester 재전송 검증과 합성 복원을 구현했다. | 최종 오프라인 gate 415건은 `PASS`다. 별도 격리 E2E 55건은 마지막 형식 변경 전 결과이며, 이후 AST 동등성과 최종 gate로 그 차이를 별도 확인했다. | 실제 Windows Export 2.0 ACK·예약·운영 독립 복원·원격 CI는 `NOT_RUN`이다. `getaddrinfo`의 hard deadline 부재와 Attester의 run당 10-page 안정 cursor 부재는 DNS 지연/over-window starvation 위험으로 남는다. 과거 Export 1.0 실제 ACK 2건은 그 버전·시점 범위에서만 재사용한다. | provider 측 job/run/hash 결속, SDK Call-ID, 실제 데이터 소유자와 Windows 인수자를 확보해 새로운 항목의 실제 수신·ACK·복원을 검증한다. Publisher 서명과 독립 Attester 증거는 계속 분리한다. DNS는 bounded 관측으로, 대기열은 versioned cursor·terminal ACK/compaction 및 over-window fairness 시험으로 각각 재개한다. |

### 공통 후속 경계

이 표는 로컬 구현과 기록된 수용을 안내할 뿐, 다음 중 어느 것도 승인·실행·완료로 바꾸지 않는다: 운영 서비스 재생성, 호스트/스토리지 변경, 실제 Secret 발급·회전·삭제, 외부 송신, 외부 저장소 변경, 실제 Windows 수신, 원격 CI 또는 최종 운영 인수. 후속 담당자는 정확한 Task의 Criterion, 최신 입력 지문, 데이터/운영 소유자, 승인 창, 백업·복구 경계와 안전한 시험 대상이 모두 확인된 경우에만 해당 행을 재개한다.

## Related Documents

- [범주 색인](../README.md)
- [현재 사양](../../../03.specs/0212-request-baseline-and-reconciliation/spec.md)
- [현재 계획](../../../03.specs/0212-request-baseline-and-reconciliation/plan.md)
- [P02 서비스 연결 Task](../../../03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0041-service-connection-contracts.md)
- [P03 모델·Runner·Wiki 준비 Task](../../../03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0042-models-runners-wiki.md)
- [P05 notifier 복구 Task](../../../03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0044-opsflow-notifier-recovery.md)
- [P07 관측 Task](../../../03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0046-exporter-observability.md)
- [P08 이미지·공급망·Storybook Task](../../../03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0047-image-supply-chain-storybook.md)
- [P09 역할·자원·퇴역 Task](../../../03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0048-role-resource-retirement.md)
- [P04 Opsflow 데이터 경로 Task](../../../03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0043-opsflow-data-path.md)

## Sources

실제 소스 선언, 기존 수용 기록, 공식 자료와 직접 확인한 시각을 공개 자료의
해당 행에 연결한다. 제공된 역사 조사와 이번 직접 조회를 구분하고 접근 실패와
게시 연도 미확인을 보존한다. 새 버전의 존재는 설치·이미지·운영 검증과 다르다.
