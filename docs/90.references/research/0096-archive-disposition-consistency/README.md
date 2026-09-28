---
title: "Archive Disposition Consistency Assessment"
version: "0.2.1"
type: "reference/research-pack"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-27"
layer: "references"
artifact_id: "RES-0096"
parent_ids: []
created: "2026-09-15"
observed_at: "2026-09-15"
---

# Archive Disposition Consistency Assessment

## Question

Stage 98 archive 정책, Registry, 등록된 check, 그리고 이를 설명하는 활성
문서가 `main@e233d2a19a3a266e3535184a95c55222f9793c8e`에서 서로 일치하는
지점과 갈라지는 지점은 어디인가? 갈라지는 지점마다, 어떤 현재 owner가
그것을 해소하며, 그 해소는 의미를 바꾸는가 아니면 현재 상태를 더
정확하게 설명할 뿐인가?

이 package는 [RES-0002](../0002-agentic-engineering-research-pack/README.md)에서
별도의 archive-domain 증거 owner로 링크됩니다. 이 question, 날짜가 있는
finding, SPEC-0177/SPEC-0178 route는 주제 연구나 infrastructure 연구에
병합되지 않습니다. 현재 cross-package routing만 통합됩니다.

## Scope

- 범위 안: `.agents/governance/documentation-protocol.md`(문서 보존 및
  은퇴), `docs/98.archive/README.md`, `docs/99.templates/registry.json`와
  그 schema, `REQ-0026`, `AD-0030`, `ADR-0033`, `ADR-0035`, SPEC-0177
  package, 이를 강제하는 `scripts/lib/document_governance/`와
  `tests/lib/document_governance/` 아래의 모듈과 test.
- 범위 밖: runtime service, Compose, hosted CI run, 그리고 운영자가
  비교한 다른 저장소의 archive 모델. 그 설명은 비교 입력으로만
  썼으며 거기서 나온 어떤 개수, test 총합, identifier도 이
  저장소의 사실로 이곳에 옮기지 않았습니다.

## Method

모든 claim은 확인 가능한 문장 하나로 쪼개어, 일관성과 그 문장이 어떻게
검증되었는지라는 서로 독립된 두 축으로 기록됩니다. 검증 수준은 `source
read`(관장하는 텍스트를 읽음), `static code`(강제하는 코드를 읽음),
`reproduced`(이번 관찰에서 명령이나 probe를 실행함), `unverified`
입니다. `source read`나 `static code` 행은 실행 증거가 아닙니다.

관찰된 commit의 clean tree에서 2026-09-15에 실행한 명령:

| Command | Result |
| --- | --- |
| `python3 -m unittest tests.lib.document_governance.test_archive tests.lib.document_governance.test_links tests.lib.document_governance.test_registry tests.lib.document_governance.metadata.test_reference tests.validation.lifecycle.test_equivalence` | exit 0, test 216개 |
| `python3 scripts/validation/check-document-corpus-lifecycle.py` | exit 0, `migrations=3 tombstones=140 preserved=200 decisions=286 recovery_rows=374 violations=0` |
| `python3 scripts/validation/check-document-links.py --mode all` | exit 0, `documents=885 links=6662 archive_direct_links_total=61 failures=0` |
| `archive._CATALOG_PACKAGE`, `archive.retention_unit`, `archive._ARTIFACT_IDENTIFIER`의 정규식 probe | Incident bundle 디렉터리 하나가 unit pattern과 일치하지 않고, `inc-2026-0001`도 `.agents/` 경로도 identifier pattern과 일치하지 않음 |
| 각 SPEC-0176 구성원을 `d174fc50b^` 시점과 `HEAD`의 보존 사본 사이에서 `git diff --no-index` | 모든 구성원이 `version`과 `status`에서 다르고, Task는 문단 하나와 표 행 두 개를 추가로 얻었으며, 모든 mode는 `100644` |

위 개수는 그 commit의 관찰값입니다. 이는 threshold가 아니며, link 총합은
SPEC-0177 Task가 같은 날 W3에 기록한 `links=6655`와 이미 다릅니다.

## Findings

### Consistency by review item

항목 번호 A01부터 A25까지는 이 평가의 검토 체크리스트이며 Registry
identifier가 아닙니다.

| Item | Statement checked | Observed fact | Consistency | Level | Disposition |
| --- | --- | --- | --- | --- | --- |
| A01 Authority | index가 navigation을, 정책이 의미를, Registry가 machine 값을 소유 | index는 그렇게 말하고 정책에 위임하지만, 정책의 두 처분 표를 한국어로 다시 적음 | 중복, owner는 정책으로 명명됨 | source read | 유지; SPEC-0177 W7이 그 전환과 함께 index를 다시 씀 |
| A02 Six dispositions | retention class 넷과 route disposition 둘 | 정책, `REQ-0026-FR-0013`, `ADR-0035`가 일치; `PRESERVED_DISPOSITIONS`가 네 class를 명명 | 일관됨 | static code | 유지 |
| A03 Retention modes | frozen 본문, 봉인된 기록, 제자리 보존, Git history only | Registry에 mode 어휘가 없음; `sealed-record`는 lifecycle임; 어떤 profile도 Git-history-only가 아님(정책 Transition 항목 6) | 지역적 차이 | source read | 유지; 결함 아님 |
| A04 Stage boundary | 현재 통제 문서는 남고, 개별 형태는 profile별로 이동 | `ACTIVE_STAGE_PREFIXES`가 Stage 01, 02, 03, 05, 90을 포괄; Stage 99 문서가 terminal 상태에 도달할 수 있는지는 확인하지 않음 | Stage 99에 대해 unverified | static code | 기록 |
| A05 First-use paths | 처음 사용될 때만 disposition 디렉터리가 존재 | `resolved/`는 없음; `load_archive`는 `adopted`에서만 이를 인정; index와 정책 Transition 항목 2는 여전히 Registry와 loader가 이를 모른다고 말함 | 구현되었지만 비활성인 코드를 오래된 것으로 설명 | reproduced | 이 평가를 기록하는 변경에서 수정됨 |
| A06 Units and members | unit은 전체 Spec package, 전체 Incident bundle, 또는 독립 문서 | catalog unit pattern은 Stage 03 package만 일치; coverage scan은 `*.md`만 다루는 반면 `retired/90.references/data/`는 `data.yaml` 구성원을 가짐 | 정책-구현 gap | reproduced | SPEC-0177 W4b |
| A07 Status and disposition | unit의 의미가 그 disposition을 결정 | `validate_active_stage_occupancy`가 각 문서를 판정; `TERMINAL_DOCUMENT_STATUSES`는 `resolved`와 `published`를 제외하며, SPEC-0177은 이를 범위 밖으로 기록 | 정책에 문서화된 제약 | static code | occupancy는 SPEC-0178; terminal-status gap은 계속 기록됨 |
| A08 Completion and disposition approval | 완료된 Task는 package가 처분되기 전에 그렇다고 말할 수 있음 | 정책은 미완료 package의 완료된 Task를 `in-progress`로 유지하라고 지시; `_validate_execution_states`는 `in-progress`와 `blocked` Task만 제약 | status 필드가 규칙상 기록된 사실과 모순 | static code | SPEC-0178(완료된 Task만) |
| A09 Promotion receipt | receipt owner 하나 | SPEC-0176의 Task가 receipt 행을 가짐; 갈라진 handoff는 `branch_integration_receipts`를 사용 | 일관됨 | source read | 유지 |
| A10 Atomicity | 상태 변경과 이동이 하나의 결과 tree에 착지 | `REQ-0026-FR-0009`와 `ADR-0033` Decision 3가 이를 요구; SPEC-0173과 SPEC-0176을 완료하는 commit이 이동 안에서 상태를 편집; pre-commit이 commit마다 `run-ci-gate.py --profile changed`를 실행 | 일관됨 | reproduced | 유지 |
| A11 Closure evidence | 해결된 Incident는 종료 날짜를 가짐 | `incident` profile은 `resolved_at`을 optional로 나열하며 status 조건부 요구를 선언하지 않는 반면, `postmortem`은 `published`에서 `reviewed_at`을 요구 | Gap | static code | SPEC-0178 Behavior Contract 10, 2026-09-16에 운영자가 배정 |
| A12 Catalog | unit 하나당 자기 class가 이름 가져야 하는 것을 명명하는 행 하나 | W4가 header, 행, class, `Source`를 확인; index는 아직 catalog section이 없으며 이는 `transition`에서 비활성; `Names`는 `retired` 밖에서 대문자 identifier를 요구 | `Names`에 대한 정책-구현 gap | reproduced | SPEC-0177 W4b |
| A13 Git provenance | `Source`가 원본 object를 증명 | check는 경로, 계보, object type을 다루지만 byte, mode, 구성원은 다루지 않음; `ci-quality.yml`은 `fetch-depth: 0`으로 checkout | 설계상 부분적(SPEC-0177 Behavior Contract 7) | static code | SPEC-0178 |
| A14 Freeze and allowed transforms | 보존된 본문은 이동 시점 본문과 byte 단위로 동일 | 완료 commit이 같은 commit 안에서 `version`, `status`, Task 증거를 바꾸므로 이동 전 byte를 담은 Git object가 없음; 상대 링크는 다시 계산되지 않음 | 요구사항-실무 불일치(`REQ-0026-FR-0012`) | reproduced | SPEC-0178 |
| A15 Legacy generations | 봉인된 형태는 base에 존재하던 기록에만 허용 | SPEC-0177 W5로 설계됨; `sealed_section_shapes`는 tree 어디에도 나타나지 않음; Tombstone parser는 여전히 봉인된 heading을 요구 | 승인됨, 미구현 | static code | SPEC-0177 W5 |
| A16 Citation by target | 활성 문서는 index와 `completed/`를 인용하고, 채택 후 `resolved/`도 인용 | `links.py`가 일치하며, 채택 목록은 switch 뒤에 있음 | 일관됨 | reproduced | 유지 |
| A17 Source and exception order | incident 예외는 보존된 본문을 위해 존재 | 그 예외는 route 기록을 포함한 모든 archive 경로를 인정; test는 `retired/`만 다룸; runbook은 이를 상속하지 않음; `docs/` 밖 문서는 `docs/README.md`(`entrypoint` mode)를 통해서만 Stage 98에 닿음 | 명시된 이유보다 넓은 예외 | static code | SPEC-0178 |
| A18 Reference syntax | 코드 예시는 링크가 아님 | `_unfenced_lines`가 fence와 빈 줄을 건너뜀; reference, wiki, HTML 링크 지원은 확인하지 않음 | 부분적으로 검증됨 | static code | 기록 |
| A19 Link integrity | 역사적 링크는 그 자체 맥락에서 판정 | 보존된 본문의 outbound 링크는 건너뛰며 원본 snapshot과 비교하지 않음; inbound 링크는 확인됨; `architecture.py`는 dangling, cross-type, 비유효 supersession을 거부 | 지역적 선택 | static code | 기록 |
| A20 Templates and identity | identity 하나당 machine contract 하나 | Tombstone은 `tomb-<은퇴한 identity>`를 쓰는 반면 그 파일명은 별도 `tombstone` 발급을 사용(정책 Authoring Rule 8); 그 발급의 high water(234)는 추적된 Tombstone 140개와 조정되지 않음 | 규칙은 일관됨; 개수는 미검증 | source read | 기록 |
| A21 Gates | switch로 gate된 규칙이 비활성임을 증명 | W3, W4, W6의 test가 `transition`에서 비활성임을 단정; 위 corpus check는 위반을 보고하지 않음 | 일관됨 | reproduced | 유지 |
| A22 Publishing and context | archive 본문은 현재로 재게시되지 않음 | 추적되는 문서 site 설정이 없음; `llms.txt`는 어떤 archive 경로도 명명하지 않음 | 해당 없음 | reproduced | 유지 |
| A23 Security and public routes | archive route 기록은 HTTP routing이 아님 | 추적되는 public site나 redirect 설정이 없음; secret 처리는 `.agents/governance/approval-boundaries.md`를 따름 | 해당 없음 | source read | 유지 |
| A24 Stale facts and counts | 현재 텍스트가 현재 tree와 일치 | SPEC-0177 Task의 날짜가 있는 개수는 날짜가 있는 관찰임; index와 정책의 transition 표는 구현된 코드를 없는 것으로 설명(A05, A12); Task의 Commit Ledger는 W2 승인 이전에서 끝남 | 오래된 현재 설명 | reproduced | 이 평가를 기록하는 변경에서 수정됨 |
| A25 Integration | 기존 작업을 재사용하지 중복하지 않음 | SPEC-0177 W5, W7, W8은 남아 있음; `ADR-0035`는 `proposed`; 이 평가가 드러낸 정책 변경은 SPEC-0177을 넓히는 대신 별도 draft package로 제안됨 | 일관됨 | source read | SPEC-0177은 W4b로 수정됨; SPEC-0178 작성됨 |

### External sources

각 행은 그 source가 뒷받침하는 것과 뒷받침하지 않는 것을 명시합니다.
2026-09-15에 읽기 전용으로 수집했습니다.

| Source | Supports | Does not establish |
| --- | --- | --- |
| Git `gitrevisions` | `<rev>:<path>`는 그 commit의 해당 경로에 있는 blob이나 tree를 명명 | object가 얼마나 오래 남아 있는지 |
| Git `git-cat-file` | `-e`와 `-t`는 object가 로컬에 존재하는지와 그 type을 확인 | 없는 object가 upstream에도 없는지, 아니면 shallow/partial clone 밖에 있는지 |
| Git `git-gc` | reflog가 붙잡지 않는 도달 불가 object는 prune grace period(기본 2주) 후 정리됨 | Hosting 측 보존 |
| Git `git-clone` | `--depth`는 history를 자르고 `--filter=blob:none`은 필요할 때까지 blob을 생략 | check가 생략된 object를 필요로 할 때의 실패 방식 |
| Nygard, *Documenting Architecture Decisions* | 번복된 decision은 남아서 대체물을 가리키며 superseded로 표시됨 | superseded 기록이 어디 사는지, 또는 역사로 링크하는 것에 대한 어떤 금지 |
| Google SRE Book, *Postmortem Culture* | Postmortem은 검토되어 공유 저장소에 남고 나중에 읽힘 | action item의 owner가 누구인지 |
| Google SRE Workbook, *Postmortem Culture* | action item은 owner와 추적 번호가 필요 | postmortem 종료의 공식 정의 |
| PREMIS ontology | 조회되지 않음: HTTP 403 | fixity나 transformation event에 대한 어떤 claim도 없음; 여기서도 하지 않음 |
| RFC 9110 §15.4.2, §15.4.9, §15.5.11 | 301과 308은 새 영구 URI를 부여; 410은 의도된 영구 제거를 표시하며 유지될 필요 없음 | 저장소 내부 상대 링크에 대한 어떤 것도 |
| GitHub, *Removing sensitive data from a repository* | secret을 먼저 회전시킴; rewrite는 이후 모든 commit identity를 바꿈; clone, fork, 캐시된 view는 데이터를 유지할 수 있음 | Squash나 reflog 동작 |
| JSON Schema, *Conditionals*, *Annotations*, *Type* | `if`/`then`은 필드를 조건부로 필수화; `default`와 `deprecated`는 검증하지 않음; `format`은 validator가 단정하지 않는 한 annotation | 특정 validator의 동작 |
| Diátaxis | reference와 explanation은 서로 다른 독자 필요를 다루며 섞이면 품질이 떨어짐 | archive나 supersession |
| Write the Docs, *Docs as Code* | 문서화는 version control, 검토, 자동화된 test를 사용함 | 어떤 check를 실행할지 |
| CommonMark 0.31.2 §4.4, §4.5, §4.7, §6.1, §6.3 | code block과 fence는 literal text임; code span은 link bracket보다 강하게 결합됨; reference definition은 reference link를 해석함 | GitHub Flavored Markdown 확장 |

## Sources

- <https://git-scm.com/docs/gitrevisions>
- <https://git-scm.com/docs/git-cat-file>
- <https://git-scm.com/docs/git-gc>
- <https://git-scm.com/docs/git-clone>
- <https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions>
- <https://sre.google/sre-book/postmortem-culture/>
- <https://sre.google/workbook/postmortem-culture/>
- <https://www.loc.gov/standards/premis/ontology/index.html> (not retrieved)
- <https://www.rfc-editor.org/rfc/rfc9110.html>
- <https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository>
- <https://json-schema.org/understanding-json-schema/reference/conditionals>
- <https://json-schema.org/understanding-json-schema/reference/annotations>
- <https://json-schema.org/understanding-json-schema/reference/type>
- <https://diataxis.fr/>
- <https://www.writethedocs.org/guide/docs-as-code/>
- <https://spec.commonmark.org/>

### 2026-09-28 외부 근거 재확인

Archive 표준안 3.0.0 대조를 위해 다음 공식 설명을 다시 조회했습니다. 기존
2026-09-15 관찰은 당시의 증거로 유지합니다. 이번 구현·검증 결과는 현재
SPEC-0179 Task가 소유하며 완료된 SPEC-0185를 다시 열지 않습니다.

| 출처 | 확인한 범위 | 이 저장소에 대한 한계 |
| --- | --- | --- |
| [Git ls-tree](https://git-scm.com/docs/git-ls-tree) | tree 항목의 mode, object type, object name, path를 조회하며 `-z`로 경로 경계를 보존 | 객체 조회가 승인이나 보존 ref 유지를 증명하지 않음 |
| [Git attributes](https://git-scm.com/docs/gitattributes) | text/EOL, encoding, filter가 index와 checkout 표현에 관여 | 현재 작업 트리 바이트 비교만으로 Git 정본·index 동일성을 주장하지 않음; 동결 자료에 renormalize를 수행하지 않음 |
| [JSON Schema 조건부 검증](https://json-schema.org/understanding-json-schema/reference/conditionals) | `if`/`then`/`else`와 조건 선택자의 존재 여부를 명시적으로 설계 | schema에 승인자 문자열이 있다는 사실은 실제 승인 권한·단위·시점의 증거가 아님 |

위 자료는 여섯 처분 디렉터리, 다섯 현재 평가값, history-only 제거 권한을
정하지 않습니다. 이들은 별도 채택이 필요한 저장소 설계입니다. 재검토 조건은
새 보존 세대, 평가 schema, index/checkout 비교 또는 승인 검증 계약이 도입될
때입니다. 다른 R01–R28 자료의 이번 재조회는 수행하지 않았습니다.

## Implications

- 여섯 개 disposition, retention class 이름, 두 번째 복구 원장 금지는
  지역적 설계 선택입니다. 어떤 조회된 source도 이를 요구하지 않으며,
  superseded decision을 역사로 인용하는 것을 금지하지도 않습니다. 이
  저장소의 인용 제한은 대체된 규칙이 인용을 통해 되살아나는 것을
  막는 자체 규칙입니다.
- 항목 A06과 A12는 이미 Incident bundle과 교정 작업 owner를 명명하는
  `ADR-0035`와, 둘 중 어느 것도 기록할 수 없는 catalog check 사이의
  gap입니다. 의미를 바꾸지 않으므로 SPEC-0177이 W4b로 처리합니다.
- 항목 A08, A14, A17은 의미를 바꿉니다: 어떤 status가 활성 package에
  남을 수 있는지, "byte-identical"이 무엇을 보장하는지, 어떤 archive
  경로를 incident가 인용할 수 있는지입니다. 이들은 `ADR-0036`과
  SPEC-0178에서 제안되며, SPEC-0177 완료에 의존합니다.
- 항목 A05와 A24는 구현되었지만 비활성인 코드를 없는 것으로 설명합니다.
  그 표현을 고쳐도 어떤 규칙도 바뀌지 않습니다.
- 항목 A11은 이 평가를 작성할 당시 어느 package에도 owner가 없었습니다.
  운영자가 2026-09-16에 SPEC-0178에 배정했습니다.

## Traceability

- [문서 보존 정책](../../../../.agents/governance/documentation-protocol.md#document-retention-and-retirement)
- [REQ-0026 문서 보존 및 은퇴](../../../01.requirements/0026-document-retention-and-retirement.md)
- ADR-0035 Stage 98 Retention Classes and Route Dispositions (superseded)
- [ADR-0036 보존 기록 탐색](../../../98.archive/README.md)
- [ADR-0037 Package Waiting, Cancellation and Archive Reassessment](../../../02.architecture/decisions/0037-package-disposition-wait-and-task-cancellation.md)
- [SPEC-0177 Archive Disposition Enforcement](../../../98.archive/completed/03.specs/0177-archive-disposition-enforcement/spec.md)
- [SPEC-0178 Archive Occupancy, Route Citation, and Frozen Identity](../../../98.archive/completed/03.specs/0178-archive-occupancy-citation-and-frozen-identity/spec.md)

## Limitations

- 이는 commit 한 개에 대한 날짜가 있는 관찰입니다. hosted CI run,
  all-files나 full-profile 실행, 어떤 runtime 상태도 기록하지 않습니다.
- Retention Catalog보다 먼저 존재한 보존된 본문은 기록된 source가 없어,
  원본 object와의 동일성을 평가하지 않습니다.
- PREMIS는 조회하지 않았으므로 어떤 preservation-standard conformance도
  주장하거나 암시하지 않습니다.
