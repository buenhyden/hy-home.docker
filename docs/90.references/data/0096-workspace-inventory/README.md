---
title: "Workspace Inventory"
version: "0.2.0"
type: "reference/data-pack"
status: "draft"
owner: "@buenhyden"
updated: "2026-11-01"
layer: "references"
artifact_id: "DATA-0096"
parent_ids:
- "SPEC-0212"
- "SPEC-0212-TSK-0040"
created: "2026-11-01"
observed_at: "2026-11-01"
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

이번 후속 검사는 이전 성공 182건의 원래 실행 시각과 결과를 보존하고, 영향받은
21건만 다시 실행해 20건 성공·1건 실패를 기록했다. 같은 69개 구성 소스 지문과
정규화한 호출·준비 입력의 동등성 확인은 이전 결과 재사용의 근거이며 새 구성
실행 성공이 아니다. 합계는 203건 중 202건 성공이고, 남은 준비 상태 예제의
망 정의 결함은 정확한 소스·작성권·재개 조건과 함께 별도 인계한다.

선택된 로컬 검사 여섯 묶음과 수정 후 일곱 번째 무결성 검사 720건은 각각
실제 통과했으며, 마지막 검사에서 P01 48건도 모두 통과했다. 이전 환경별 실패는
이력으로 보존한다. 별도 실행한 이 결과를 전체 14개 검사 일괄 통과·원격 CI·
실제 호스트 신뢰·서비스 운영 인수로 확대하지 않는다.

### Consumers

[현재 작업](../../../03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0040-workspace-inventory.md)은
시작·종료 비교와 인수 근거로 읽는다. P02–P12의 후속 담당은 서비스별 소스 지문·
소비자·증거 수준·단일 작성자와 재개 조건을 인계받는다. 이 연결은 운영 권한을
부여하거나 후속 업무의 완료를 선행 조건으로 만들지 않는다.

## Related Documents

- [범주 색인](../README.md)
- [현재 사양](../../../03.specs/0212-request-baseline-and-reconciliation/spec.md)
- [현재 계획](../../../03.specs/0212-request-baseline-and-reconciliation/plan.md)

## Sources

실제 소스 선언, 기존 수용 기록, 공식 자료와 직접 확인한 시각을 공개 자료의
해당 행에 연결한다. 제공된 역사 조사와 이번 직접 조회를 구분하고 접근 실패와
게시 연도 미확인을 보존한다. 새 버전의 존재는 설치·이미지·운영 검증과 다르다.
