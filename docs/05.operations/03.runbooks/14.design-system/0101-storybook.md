---
title: "Shared Storybook Source Preflight Runbook"
version: "1.2.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "operations"
artifact_id: "RUN-0101"
parent_ids:
- "GDE-0101"
created: "2026-10-03"
next_review_at: "2027-05-13"
---

# Shared Storybook Source Preflight Runbook

## Trigger and Scope

### Trigger

공유 Storybook 정적 origin과 문서 MCP의 빌드, 기동, 검증, 복구를 다루는 런북이다.

`storybook` 정적 origin의 소스, route 또는 image 변경을 검토할 때 사용한다.

### Targets

- Artifact: `RUN-0101`; parent guide: `GDE-0101`.
- 역사적 source/static 완료 근거: `SPEC-0206`. 런타임 선언:
  [Storybook Compose](../../../../infra/13-experience/storybook/docker-compose.yml).
- [Shared Storybook guide](../../01.guides/14.design-system/0101-storybook.md)
- [Shared Storybook policy](../../02.policies/14.design-system/0101-storybook.md)
- [Traefik runbook](../02.gateway-and-networking/0013-traefik.md)

## Preflight

### Authority

HOME 배포·정지·재시작, DNS/TLS 수정, 검토자 권한 변경과 원격 MCP 공개는 별도
구체적 승인이 필요하다. SPEC-0206은 source/static completion의 역사적 근거이며,
이 runbook은 이후 운영 trigger와 evidence handoff를 소유한다.

### Environment

정적 origin은 업무 데이터를 소유하지 않으므로 backup은 요구하지 않고, 읽기 전용 사전 점검은 Steps의 1~2단계(작업 revision 일치 확인과 정적 Compose 검증)에서 수행한다.

## Procedure

### Steps

| Step | Action | Expected Result | On Failure |
| --- | --- | --- | --- |
| 1 | 현재 Git SHA와 승인된 Storybook package/lock, Dockerfile, Compose, profile, 운영 문서가 같은 작업 revision에 속하는지 확인한다 (실제 `.env`/secret 값은 출력하지 않음) | 문서에 기록 없음 | 배포를 중단하고 @buenhyden에게 SHA와 대상/증거/복구 경계를 전달 |
| 2 | 공개 예제 환경으로 `docker compose --env-file .env.example --profile experience config --quiet`, `validate-docker-compose.sh`, `check-operations-catalog.py`를 실행한다 | 정적 구성 검증 명령 세 개가 성공한다 | 배포를 중단하고 @buenhyden에게 SHA와 대상/증거/복구 경계를 전달 |
| 3 | Compose가 `!override`를 해석하는지 확인하고 render 결과에서 `storybook`만 새 서비스, 전용망 `internal: true`, router의 TLS/middleware 순서, host port 없음을 확인한다 | render 결과가 기술된 구성과 일치한다(정적 검사 성공만으로 인증/TLS/브라우저 동작을 주장하지 않음) | 배포를 중단하고 @buenhyden에게 SHA와 대상/증거/복구 경계를 전달 |
| 4 | `storybook_image.py build`(필요 시 `--push`)로 Storybook 소스를 마지막으로 바꾼 커밋의 image를 만들고 `verify --registry`로 검증한다 | `storybook_image.py verify`가 통과한다 | Dockerfile은 40자리 커밋 SHA가 없으면 빌드를 거부하고 image가 없으면 기동이 실패하며 secret은 build argument로 전달하지 않음 |
| 5 | `HYHOME_STORYBOOK_REHEARSAL=1` unittest로 임시 내부망에서 Traefik/OAuth2 Proxy/Keycloak rehearsal을 실행한다 | 비인증 요청은 200을 받지 않고 관리자만 각 경로를 `no-store`와 `frame-ancestors 'self'`로 받으며 MCP는 401/403/200과 404를 확인한다 | image가 없으면 rehearsal이 빌드 명령을 알려 주며 실패하고 `down -v`나 volume prune은 쓰지 않음 |
| 6 | HOME 활성화 승인이 별도로 주어지면 Keycloak client/scope 생성 후 `experience` 기동, DNS, TLS, 관리자 로그인, 비인증 거절, MCP 로그인/tool 호출, 이전 image rollback을 시험한다 | 문서에 기록 없음 | 승인 범위 밖에서는 수행하지 않으며 문제 시 승인된 운영 Task가 이전 image와 route를 복원 |
| 7 | 검토/병합된 커밋에서 `storybook_design_export.py <빈 디렉터리>`로 bundle을 만들고 그 안에서만 `/design-sync`를 실행한다 | bundle은 allowlist 파일과 `export-manifest.json`만 담는다 | 문서에 기록 없음 |

1. 현재 Git SHA와 승인된 Storybook package/lock, Dockerfile, Compose, profile,
   운영 문서가 같은 작업 revision에 속하는지 확인한다. 실제 `.env`나 secret의 값을
   출력하지 않는다.
2. 저장소 root에서 공개 예제 환경으로 정적 구성을 검증한다.

   ```bash
   docker compose --env-file .env.example --profile experience config --quiet
   HYHOME_COMPOSE_PROFILES='core experience' bash scripts/validation/validate-docker-compose.sh
   python3 scripts/validation/check-operations-catalog.py
   ```

3. [Compose merge 문서](https://docs.docker.com/reference/compose-file/merge/)에 따라
   사용 중인 Compose가 `!override`를 해석하는지 확인한다. render 결과에서
   `storybook`만 새 선택 서비스이고, `experience`가 HOME에 없으며,
   Storybook은 `experience_ingress_net`만, Traefik은 그 망과 `edge_net`을
   사용하며 전용망이 `internal: true`인지 확인한다. router가 `websecure`
   TLS와 `req-rate-limit@file,gateway-standard-chain@file,sso-auth@file` 순서의
   middleware를 사용하고 `sso-errors@file`과 host port가 없는지도 확인한다.
   수동 로그인 진입점은 기존
   `auth.${DEFAULT_URL}/oauth2/start` router이며 `rd`에 Storybook URL을 인코딩해
   전달한다. 정적 검사 성공만으로 실제 인증·TLS·브라우저 동작을 주장하지 않는다.
4. image는 Storybook 소스를 마지막으로 바꾼 커밋으로만 빌드한다. 무관한 문서
   커밋에 맞춰 재태깅하지 않는다.

   ```bash
   python3 scripts/operations/storybook_image.py build          # 로컬 preload
   python3 scripts/operations/storybook_image.py build --push   # 로컬 registry 배포
   python3 scripts/operations/storybook_image.py verify --registry
   ```

   `build`는 `git archive`로 커밋된 `projects/storybook/nextjs`만 context로
   내보내고, lockfile 기준 `npm ci`로 `hy-home/storybook:<commit>`을 SBOM·max
   provenance attestation과 함께 만든다. `--push`는 같은 image를
   `127.0.0.1:${REGISTRY_PORT}/hy-home/storybook:<commit>`에도 올린다.
   `verify`는 OCI revision label, 정적 `revision.json`의 `sourceRevision`,
   lockfile SHA-256, UI 패키지 이름·버전, 두 manifest SHA-256이 그 커밋과
   같은지, 정적 출력에 `.env`·key·source map·`node_modules`가 없는지 확인한다.
   `--registry`는 registry index digest가 로컬 image와 같고 SBOM과 소스
   revision을 기록한 provenance가 있는지도 확인한다. Dockerfile은 40자리
   커밋 SHA가 없으면 빌드를 거부한다. Compose는 `hy-home/storybook:<commit>`을
   `pull_policy: never`로 고정하므로 image가 없으면 기동이 실패한다.
   provenance `mode=max`는 build argument를 기록하므로 secret은 build
   argument로 전달하지 않는다. 이 빌드에는 secret 입력이 없다.
5. 격리 검사는 고정된 두 image로 실제 Traefik·OAuth2 Proxy·Keycloak을 임시 내부망에
   올리는 rehearsal로 수행한다. 모든 container, network, 임시 CA와 realm은 합성이며
   시험이 끝나면 그 이름으로만 정리한다. `down -v`나 volume prune은 쓰지 않는다.

   ```bash
   HYHOME_STORYBOOK_REHEARSAL=1 python3 -m unittest \
     tests.validation.test_compose_baseline_gates.StorybookIngressRehearsalTests -v
   ```

   Compose label로 만든 router에서 비인증·비관리자 요청이 index, iframe, asset,
   manifest의 내용이나 로그인 HTML을 200으로 받지 않는지, 관리자는 각 경로를
   `no-store`와 `frame-ancestors 'self'`로 받는지, 404와 `revision.json`의 커밋을
   확인한다. 원격 MCP는 HTTPS issuer와 `storybook-mcp` scope의 Audience mapper로
   발급한 token으로 401(token 없음, audience 없음), 403(`/admins` 아님), 200(문서
   tool 세 개), 보호 자원 metadata와 route 밖 경로 404를 확인한다. image가 없으면
   rehearsal은 빌드 명령을 알려 주며 실패한다.
6. HOME 활성화 승인이 별도로 주어지면 GDE-0101의 Keycloak client와 scope를 만든 뒤
   해당 승인 범위에서만 `experience` 기동, DNS, TLS, 관리자 로그인, 비인증 거절,
   다른 워크스페이스의 Codex·Claude Code 로그인과 문서 tool 호출, 이전 image로의
   rollback을 시험한다.
7. Claude Design 전달은 검토·병합된 커밋에서 bundle을 만든 뒤 그 안에서만
   `/design-sync`를 실행한다.

   ```bash
   python3 scripts/operations/storybook_design_export.py <빈 디렉터리>
   ```

   bundle은 `projects/storybook/nextjs/design-export.allowlist.json`의 파일과
   `export-manifest.json`만 담는다. 계정 로그인과 업로드는 담당자가 수행한다.

### Stop Conditions

다음이 확인되면 배포를 중단한다: 잘못된 관리자 허용 범위, 비인증 asset 노출, 로그인 HTML의 asset/MCP 응답 혼입, image/context에 비밀값 유입, port 충돌, read-only runtime 실패, manifest revision 불일치.

## Verification

### Expected Results

#### Service Checks

정적 구성 검증 명령 세 개가 성공하고 `storybook_image.py verify`가 통과해야 하며, 격리 rehearsal에서 비인증 요청이 200을 받지 않고 관리자만 각 경로를 받아야 한다.

#### Evidence

운영 Task에 기준/작업 SHA, 변경 파일, 명령·exit code, 정적·격리·HOME 결과를 구분해
기록한다. Trigger는 HOME route 활성화, `/admins` 이외 reviewer 승인, remote MCP
issuer/audience/client 승인, DNS/TLS 관찰 요청 또는 external design account 승인이다. host secret, 세션 cookie, 인증 HTML 원문, private Compose 전체 출력,
실사용자 데이터와 원시 로그는 기록하지 않는다.

### Unverified Conditions

이 runbook이 아직 관찰된 적 없는 항목은 다음과 같다.

- HOME 활성화(`experience` 기동, DNS, TLS, 관리자 로그인, 비인증 거절, MCP 로그인과 tool 호출, 이전 image rollback): 별도 승인이 필요하며 이 문서에는 실행 결과가 기록되어 있지 않다. 승인된 운영 Task의 HOME 결과 기록이 검증 근거가 된다.
- 실제 인증/TLS/브라우저 동작: 문서는 정적 검사 성공만으로 주장하지 않는다고 밝힌다. 격리 rehearsal 결과와 HOME 관찰이 검증 근거가 된다.
- 격리 rehearsal(`StorybookIngressRehearsalTests`)과 image `verify`: 이 문서에는 실행 결과가 기록되어 있지 않다. 명령 종료 코드와 비인증 200 부재, 관리자 응답 확인이 검증 근거가 된다.
- Claude Design 전달: 계정 로그인과 업로드는 담당자가 수행하며 이 문서에는 기록이 없다. bundle과 `export-manifest.json` 확인이 검증 근거가 된다.

## Escalation

### Next Owner

잘못된 관리자 허용 범위, 비인증 asset 노출, 로그인 HTML의 asset/MCP 응답 혼입,
image/context에 비밀값 유입, port 충돌, read-only runtime 실패 또는 manifest
revision 불일치가 확인되면 배포를 중단하고 @buenhyden에게 SHA와 대상·증거·복구
경계를 전달한다.

### Recovery or Forward Repair

정적 구성 오류는 Storybook leaf Compose와 root include/profile 문서 변경만 되돌린 뒤
같은 검사를 재실행한다. HOME 실행 이후에는 승인된 운영 Task가 이전 image와
route를 복원하고 브라우저 경로를 다시 검사한다. 정적 origin은 업무 데이터를
소유하지 않으므로 DB·volume 삭제나 migration은 복구 절차가 아니다.
