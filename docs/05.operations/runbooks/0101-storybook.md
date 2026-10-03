---
title: "Shared Storybook Source Preflight Runbook"
version: "1.0.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-03"
layer: "operations"
artifact_id: "RUN-0101"
parent_ids:
- "GDE-0101"
created: "2026-10-03"
---

# Shared Storybook Source Preflight Runbook

## When to Use

`storybook` 정적 origin의 소스, route 또는 image 변경을 검토할 때 사용한다.
HOME 배포·정지·재시작, DNS/TLS 수정, 검토자 권한 변경과 원격 MCP 공개는 별도
구체적 승인이 필요하다.

## Procedure

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
4. image는 TSK-0001의 커밋 SHA로 고정한 `hy-home/storybook:<source-SHA>`만
   사용하고 Compose는 `pull_policy: never`로 원격 pull을 막는다. 배포 전 image의
   `org.opencontainers.image.revision` label, 정적 `revision.json.sourceRevision`,
   승인된 TSK-0001 source SHA가 모두 같은지 확인한다. `uncommitted` 또는 누락된
   label·manifest는 배포 중단 조건이다.
5. 격리 컨테이너 검사는 Docker context, project, port, network, volume, resource,
   UID/GID와 정확한 정리 대상을 먼저 기록한 뒤 합성 자산으로 수행한다. image의
   index, iframe, JS/CSS, manifest, deep link, 404, cache, CSP/frame과 health를
   검사한다. task 소유 컨테이너만 정리하며 `down -v` 또는 volume prune은 사용하지 않는다.
6. HOME 활성화 승인이 별도로 주어지면 해당 승인 범위에서만 DNS, TLS, 관리자 로그인,
   비인증 거절, 만료 후 asset 접근과 이전 image로의 source rollback을 시험한다.
   MCP는 별도 로컬 절차이며 HOME Compose에 올리지 않는다.

## Evidence

Task에 기준/작업 SHA, 변경 파일, 명령·exit code, 정적·격리·HOME 결과를 구분해
기록한다. host secret, 세션 cookie, 인증 HTML 원문, private Compose 전체 출력,
실사용자 데이터와 원시 로그는 기록하지 않는다.

## Rollback or Recovery

정적 구성 오류는 Storybook leaf Compose와 root include/profile 문서 변경만 되돌린 뒤
같은 검사를 재실행한다. HOME 실행 이후에는 승인된 운영 Task가 이전 image와
route를 복원하고 브라우저 경로를 다시 검사한다. 정적 origin은 업무 데이터를
소유하지 않으므로 DB·volume 삭제나 migration은 복구 절차가 아니다.

## Escalation

잘못된 관리자 허용 범위, 비인증 asset 노출, 로그인 HTML의 asset/MCP 응답 혼입,
image/context에 비밀값 유입, port 충돌, read-only runtime 실패 또는 manifest
revision 불일치가 확인되면 배포를 중단하고 @buenhyden에게 SHA와 대상·증거·복구
경계를 전달한다.

## Traceability

- Artifact: `RUN-0101`; parent guide: `GDE-0101`.
- Source contract: `SPEC-0206`; runtime declaration:
  [Storybook Compose](../../../infra/13-experience/storybook/docker-compose.yml).

## Related Documents

- [Shared Storybook guide](../guides/0101-storybook.md)
- [Shared Storybook policy](../policies/0101-storybook.md)
- [Traefik runbook](0013-traefik.md)
