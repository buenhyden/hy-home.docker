---
title: "미래 사용자 흐름과 E2E 인수 시나리오"
version: "1.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-26"
---

# 미래 사용자 흐름과 E2E 인수 시나리오

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

독자는 아래 역할 본문에서 이 문서가 제공하는 정보와 판단을 확인합니다.

### 책임과 적용 범위

적용 대상과 유지 책임은 frontmatter와 역할 본문의 범위 선언이 소유합니다.

## 내용 계약

### 입력과 전제

실제 입력과 전제는 아래 역할 본문의 해당 항목을 따릅니다.

### 본문과 규칙

#### Service

##### Purpose

아래는 앱 구현 후의 인수 시나리오이며 실행 결과는 모두 NOT_RUN입니다.

| 흐름 | 정상 수용 | 실패·거부 수용 |
|---|---|---|
| 로그인·원천 선택 | issuer/audience와 사용자 ACL에 맞는 원천만 표시 | 로그아웃·만료·잘못된 audience·교차 프로젝트 거부 |
| 동기화·최신성 | revision/generation/지연 상태 표시 | 빈 원천·timeout·partial store를 최신 정상으로 표시하지 않음 |
| 탐색·인용 | 허용 artifact의 revision/hash/시각·근거 연결 | 삭제·철회·old generation의 query/download/citation/cache 모두 거부 |
| 후보 검토·선택 | 사람이 선택한 Literature 후보만 정확한 write set 인계 | 미선택·중복·추가 경로·stale base·hash 불일치 거부 |
| 재시도·취소 | 동일 key 재시도 중복 side effect 없음, 취소 상태 명시 | dead/timeout은 실패 원인을 값 노출 없이 표시 |
| 빈 환경 복원 | outbox·삭제 watermark·세 store 재검증 후 공개 | 이전 ACL/content resurrect 또는 미검증 generation 노출 거부 |

###### 검색 품질 기준

미래 Wiki 검색은 아래를 수용 조건으로 삼습니다. 현재 범위는 준비이므로 검색 구현과 색인은 만들지 않으며 결과는 NOT_RUN입니다.

- 기준선: SPEC-0212 TSK-0119 criterion 176의 저장소 문서 검색 평가(commit `c01fe08eb`, 591 문서, 시간순 뒤 20% 119 문서)에서
  hybrid(BM25 + dense, RRF k=10)가 recall@1 0.429, recall@5 0.866, recall@10 0.916, MRR@10 0.616이었습니다.
  BM25 단독은 MRR@10 0.472, dense 단독은 0.566입니다.
- 수용: 미래 검색은 같은 평가(`scripts/lib/ops/docs_retrieval_eval.py`, MLflow 실험 `docs-retrieval-eval`)를
  같은 corpus 정의와 시간순 분할로 다시 돌려 위 hybrid 값 이상이어야 합니다. 낮으면 원인과 owner 결정을 남깁니다.
  이 값은 제목→자기 문서라는 구조적 대리 지표이므로 실제 사용자 질의 평가를 대신하지 않습니다.
- 구성: Qdrant 한 collection에 named vector 두 개를 둡니다. `dense`는 로컬 Ollama `embeddinggemma-2:740m`(768차원,
  Cosine)이 만들고, `bm25`는 client가 token 빈도로 만든 sparse vector에 Qdrant `modifier: idf`를 적용합니다. 질의는
  Query API의 `prefetch` 두 개(dense, bm25)와 `fusion: rrf`로 Qdrant 안에서 합칩니다. 2026-11-26 Qdrant 1.19.2에서
  임시 collection으로 이 구성이 동작했고(한국어 질의의 정답 문서가 1위), collection은 지웠습니다.
- 색인 계약: collection metadata에 embedding 모델 이름·digest·차원과 tokenizer 규칙을 기록하고, 모델이나 규칙이
  바뀌면 새 collection으로 전부 다시 색인한 뒤 alias를 바꿉니다. 섞인 vector로 검색하지 않습니다.
- 자원: HOME Ollama는 `OLLAMA_MAX_LOADED_MODELS=1`이라 embedding 호출이 상주 대화 모델(lfm2.5:8b)을 내립니다.
  대량 색인은 사용이 적은 시간에 돌리거나, 공유 GPU 여유를 측정해 상주 모델 수를 늘리는 결정을 따로 받습니다.
- 권한: Qdrant 쓰기 key는 색인 작업만, 검색은 read-only key를 씁니다. key는 파일로만 읽고 출력하지 않습니다.

지연·부분 실패·취소·권한 거부·복원 중 UI는 진척과 미확인 상태를 분리해야 합니다. 미래 Wiki 앱의 owning exact Task가 이 조건을 executable E2E로 구현하고, P10은 전체 인프라 수용을 조정합니다. Storybook 앱 코드나 가짜 PASS는 작성하지 않습니다.

###### Audience
<!-- core-payload-level:4 -->

인프라 담당자, 미래 consumer 작성자와 독립 검토자입니다.

###### Scope
<!-- core-payload-level:4 -->

준비 문서·기계 schema·합성 검증에 한정합니다.

###### Structure
<!-- core-payload-level:4 -->

[readiness](../readiness/README.md)

##### Interfaces

###### Inputs and Outputs
<!-- core-payload-level:4 -->

비밀값과 실제 환경 변수는 입력하지 않습니다.

###### Security Boundary
<!-- core-payload-level:4 -->

없음: 이 디렉터리는 Markdown 문서와 합성 JSON만 두며 Compose 서비스·포트·네트워크·Docker Secret·접근 제어를 정의하지 않는다. 비밀값과 실제 환경 변수는 입력하지 않는다.

#### Usage

##### Prerequisites

기존 Python·jsonschema와 오프라인 JSON 문서를 사용합니다.

##### Selected Start

총괄의 공통 계약 통합 후 해당 증거를 Task에 연결합니다.

#### Checks

##### Readiness

저장소 루트에서 활성화한 격리 venv에 `python -m pip install -r scripts/requirements.txt`를 실행한 뒤 `python -m unittest tests.lib.ops.test_wiki_preparation tests.validation.test_wiki_preparation_contracts -v`를 실행합니다. 시스템의 오래된 jsonschema는 검증 환경이 아닙니다. 단위검사는 native 실행 증거가 아닙니다.

##### Failure Handling

###### Runbook Links
<!-- core-payload-level:4 -->

문서 체계는 저장소 docs README 진입점을 통해 확인합니다.

###### Observability and Recovery
<!-- core-payload-level:4 -->

없음: 실행되는 서비스가 아니므로 헬스체크·지표·로그가 없고, 이 패키지를 대상으로 하는 운영 런북도 `docs/05.operations/03.runbooks`에 없다. 계약 문서가 어긋나면 위 Checks의 단위 검사 실패로 드러나며, 복구는 Git 이력에서 해당 문서 변경을 되돌리는 것이다.

## 적용과 확인

### 적용 방법

아래 역할 본문의 절차나 탐색 순서에 따라 사용합니다.

### 확인 기준

해당 문서에 선언된 확인 기준과 한계만 적용하며 실행·검증·인수를 구분합니다.

## 관계와 출처

### 관련 문서

현재 소유자와 의존 문서의 연결은 아래 역할 본문의 링크가 소유합니다.

### 외부 근거

외부 출처와 적용 한계는 아래 역할 본문에 선언된 범위이며 권한을 부여하지 않습니다.
