---
title: "OpenBao Policy"
version: "0.8.5"
type: "operation/policy"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-27"
layer: "operations"
artifact_id: "POL-0085"
parent_ids:
- "AD-0003"
created: "2026-09-19"
---

# OpenBao Policy

## Overview

HOME secret control plane이다. 레거시 Vault는 2026-09-25 폐기되었으므로 현재 마이그레이션·복구 소스로 취급하지 않는다.

## Scope

`infra/03-security/openbao`와 `core / dev / local / security / secrets` 프로필 아래의 서비스
`openbao openbao-agent`.

## Rules

unseal/recovery 자료는 오프라인으로 유지한다. token, role_id, secret_id 또는 렌더링된
파일을 절대 로깅하지 않는다. 현재 서버 health는 unsealed 상태만 허용한다. Agent
health만으로는 새 인증·출력 갱신과 secret 전달을 증명할 수 없다. 기존 애플리케이션 Docker Secret은 Agent
출력으로 자동 대체되지 않는다.

사람이 하는 일반 관리 작업은 Keycloak을 backend로 하는 OpenBao native OIDC를 통해
발급된 non-root OpenBao 토큰을 사용해야 한다. 승인된 HOME 바인딩은 Keycloak 그룹
`/openbao-admins`, role `home-admin`, OpenBao OIDC client `home-openbao`, OpenBao
operator policy `hy-home-operator`다. 사람 토큰의 policy TTL은 유한해야 한다. OpenBao
UI 앞의 Gateway SSO는 HTTP 접근 제어일 뿐이며 OpenBao native OIDC 인가를 대체하지
않는다.

### Prometheus Metrics Credential

Prometheus는 전용 service token으로 `sys/metrics`에 인증해야 하며, 그 유일한 service
policy는 추적되는 `infra/03-security/openbao/config/policies/prometheus.hcl`이다. 이
policy는 `sys/metrics`에 대한 `read`만 부여한다. 토큰은 수동으로 발급해
`secrets/security/openbao/openbao_token.txt`에 저장하고 Prometheus만 마운트하며 유한한 만료
전에 회전한다. 인증 없는 metrics를 활성화하거나 root, human operator, renderer AppRole,
renderer sink 토큰을 재사용하지 않는다.

policy 적용, 토큰 발급/폐기, 파일 작성, Prometheus 재생성은 별도로 승인된 유지보수
기록이 필요한 실제 credential/runtime 변경이다. 추적되는 policy, Compose, scrape 설정은
소스 계약만 증명한다.

### hy-home.k8s Kubernetes Auth

hy-home.k8s 클러스터는 `kubernetes` auth method로 인증한다. External Secrets service
account (`external-secrets`, namespace `external-secrets`, audience `vault`)만 role
`eso-read-platform`을 통해 로그인할 수 있으며, 그 policy는 `secret/platform/{argocd,postgres-app,notifications,prometheus-api,grafana-api}`의
정확한 KV v2 data/metadata 경로만 읽는다. wildcard, list, create/update/delete/sudo를
부여하지 않는다. 클러스터 부트스트랩 토큰은 오직
`k8s-bootstrap` 토큰 role에서 나온다: orphan, 2시간 TTL, policy `k8s-bootstrap`
(`platform/argocd` 읽기). OIDC operator는 클러스터 재구축마다 `auth/kubernetes/config`를
갱신하고 이 토큰을 발급할 수 있다. method 활성화, policy/role 작성, KV 항목 작성에는
승인된 root 세션이 필요하다. 클러스터가 도달할 수 있도록 OpenBao Traefik route는 SSO나
IP allowlist 없이 유지한다.

이 다섯 경로는 [추적 ACL](../../../../infra/03-security/openbao/config/policies/eso-read-platform.hcl)의
범위이며 사람이 쓰는 operator의 create/update 권한과 구분한다. 기존 세 경로 설명
이후 owner-authored 변경 `e3d811870`과 `5fb725b2a`(2026-09-23)가 Prometheus와
Kiali Grafana 읽기를 추가했고, [완료된 Task 0008](../../../98.archive/completed/03.specs/0180-home-dev-convergence/tasks/tsk-0008-storage-security-lakehouse-convergence.md)의
해당 경로·통합/merge 기록과 [2026-09-24 owner 완료 결정](../../../98.archive/completed/03.specs/0180-home-dev-convergence/spec.md#completion-basis-owner-decision-2026-09-24)이
그 제한된 추가의 역사적 근거다. 이 교정은 임의 권한 확대를 허용하지 않는다.
ESO 주체가 침해되면 이 다섯 항목에 대한 읽기가 함께 영향을 받으므로 exact
service-account/namespace/audience 바인딩을 유지한다. 실제 설치된 정책·role과
경로 밖 거부는 별도 검증하며 source나 문자열 하드닝 통과로 증명하지 않는다.

Root 토큰은 bootstrap, break-glass, 그리고 아래 유지보수 window의 임시 root(W1c·W2·W7과 이전 root 정리) 용도로만 사용한다. 다음 사항이 모두 동일한 유지보수
기록 안에서 검증되기 전에는 마지막으로 사용 가능한 root 토큰을 폐기하지 않는다: human
OIDC 로그인이 성공한다, 결과로 나온 OpenBao 토큰이 기대한 non-root policy를 가진다,
AppRole renderer 접근이 여전히 선언된 두 KV data와 해당 metadata 경로만 읽는다, 배포된 OpenBao 버전의 root
recovery 방법이 문서화되어 있다. 그 뒤 root를 폐기하고 거부 결과를 같은 기록에 남긴다.

Traceability에 문서화된 upstream OpenBao 릴리스 라인은 `operator generate-root`에
대해 인증된 `/sys/generate-root-token` 엔드포인트를 사용한다. 권한 있는 사람이나 root
토큰이 남아 있지 않을 때, Agent read-only 토큰을 root-generation 엔드포인트 호출로
승격해서는 안 된다. deprecated된 인증 없는 `/sys/generate-root/*` 엔드포인트는 2.5.3부터
기본적으로 비활성화되어 있으며 <!-- runtime-version-exception: history — unauthenticated root generation was disabled upstream to close a recovery-path security exposure --> 임시 loopback 전용
listener에서 명시적으로 승인된 break-glass 예외로만 다시 활성화할 수 있다. 이 예외는
동일한 데이터 볼륨과 seal 설정을 유지해야 하고 기본적으로 스냅샷을 restore해서는 안
되며 native OIDC 관리가 검증되면 즉시 제거해야 하고 복구된 root 토큰의 폐기로
끝나야 한다.

[Implementation](../../../../infra/03-security/openbao/docker-compose.yml)과
[version projection](../../../../infra/tech-stack.versions.json)이 런타임 고정값을 소유한다.

### Persistence, limits and removal

두 서비스의 공통 자원 상한·변경 적용은 [POL-0006](../01-common/0006-infrastructure-optimization-governance.md),
버전 변경은 [POL-0086](../10-platform-and-backup/0086-dependency-version-management.md)을 적용한다.
Raft 상태와 Agent bootstrap/output, offline custody는 서로 다른 보호 입력이며
[POL-0021](../10-platform-and-backup/0021-backup-and-restore.md)의 OpenBao state-owner retention·암호화·복구
기준을 함께 적용한다. renderer는 선언된 두 KV data 경로만 read하며 unused template가
있다는 이유로 권한을 넓히지 않는다. Agent 재생성은 secret authority 복원이 아니다.

Raft upgrade 전 backup과 독립 stateful recovery 계약 검토가 필요하다. 승인된
격리 복원 없이 data rollback을 준비됐다고 표시하지 않는다. 마지막 관리 접근이나
unseal/custody 자료를 검증 전에 폐기하지 않는다. 서비스·Agent 제거는 소비자 이관,
credential 폐기와 보호 자료 보존을 각각 승인받아 수행하며 `down -v`로 대체하지 않는다.

### Maintenance window credential handling

HOME 유지보수 window(SPEC-0243, 절차는 RUN-0105)는 아래 규칙을 따른다.

- share·root·operator token은 숨김 입력, stdin, 보호된 FD, tmpfs의 0600 파일, 또는 명령 하나에만
  붙는 환경 변수(`BAO_TOKEN="$(cat …)"`와 이름만 넘기는 `docker compose exec -e BAO_TOKEN`)로만
  다룬다. 명령 인자, 셸 기록, 화면 출력, OpenBao CLI token helper(영구 disk)에 두지 않는다.
  container 안 process 환경의 노출은 아래 UID 100 잔여 위험이 다룬다.
- window에서 만든 임시 root는 window 끝이나 중단 때 폐기한다. server가 sealed라 폐기할 수 없으면
  그 root를 다시 만들 수 있는 custody 파일을 모두 지우고, 다음 window가 W1 직후 이전 root를 찾아
  폐기한다. 이 정리는 기록과 상관없이 매 window 실행한다.
- server가 unsealed인데 새 OIDC 로그인이 되지 않으면 root와 custody를 지우지 않고 OIDC 접근부터
  복구한다. 마지막 관리 접근을 복구 수단 없이 버리지 않는다. 이렇게 남긴 root는 OIDC를 고칠
  때까지, 최대 재부팅이나 다음 window까지만 owner가 tmpfs에 보관하며, 그동안 Linger나 로그인
  세션을 유지하고 기한 날짜를 값 없이 기록한다.
- window에서 쓴 operator token은 폐기하고, 값이나 accessor는 기록하지 않는다. 예외는 둘이다.
  server가 sealed라 폐기할 수 없는 token은 OIDC 최대 TTL(4시간) 안에 만료되며 그 사실을 기록한다.
  위 OIDC 장애로 root를 남길 때는 operator token 파일도 함께 남기고 OIDC 복구 뒤 폐기한다.

## Exceptions

owner @buenhyden은 모든 편차 전에 범위, 위험, 만료, 종료 조건을 기록해야 한다. 정적
설정은 실제 backup이나 recovery의 증거가 아니다.

임시 인증 없는 generate-root recovery로 승인되는 유일한 형태는 대체 root 토큰을
생성하고 정상적인 OIDC administrator 경로를 확립하는 데 필요한 기간 동안
`disable_unauthed_generate_root_endpoints = false`로 설정된 loopback 전용 listener다.
이 설정은 public이나 gateway listener에서는 금지되며 steady-state 설정에 남아 있을 수
없다.

### Existing custody decision and missing closure

기존 owner 결정(2026-09-22)은 share3개를 `secrets/security/openbao/openbao_unseal_keys.txt`
한 파일에 함께 보관한다. 파일은0600, Git-ignored, 컨테이너에 mount하지 않으며
private registry는 SEC-003 placeholder만 보관한다. 이 파일은 유일한 사본이 아니다.
host Restic 저장소(BKP-002로 암호화)는 `secrets/` 전체를 담고, `restic-offsite`가 그
저장소를 R2(BKP-003으로 암호화)로 복사한다. 그 사본은 owner가 `forget-prune`이나 별도
승인된 삭제로 지울 때까지 남는다(R2 bucket lock 30일).
이는 분리 custody의 기존 명시적 예외다. 파일을 읽는 한 주체, BKP-003과 R2 읽기 권한을
함께 가진 한 주체, BKP-002와 local host 저장소를 가진 한 주체가 unseal threshold를 충족할
수 있다. 2026-10-14 owner는 처음에 파일을 host 백업에서 빼고 rekey하며 share를 장소별로
나누기로 했다가(SPEC-0240), 같은 날 관리자가 1명인 운영에 맞춰 이를 거두고 host 중심
배치를 정했다(SPEC-0242). share와 CA key는 host `secrets/`와 owner의 host 보조 사본에 두고
host 백업에 포함한다. BKP-003·R2 자격 증명·BKP-002·Cloudflare 계정 접근과 secret이 아닌 R2
식별자만 owner가 관리하는 host 밖 장소(비밀번호 관리자 계정이나 별도 데스크탑)에 둔다. host를
잃어도 R2에서 모두 복구하려는 배치이지만(R2 원격 복구는 아직 미실행), 그 장소가 뚫리면 모든 secret과 share가 노출되고 off-host 사본을 지울 수도 있으며, host를 읽는 한 주체가 threshold를 넘는다. owner는 이 노출을
받아들였고 rekey는 하지 않는다(RUN-0105). 이 결정은 이 예외를 닫지 않는다. 이 문서는
결정을 기록할 뿐 그 실행이나 새 credential 처리, 이 결정을 넘는 예외 확대를 승인하지 않는다.
기존 기록에는 **만료와 종료 조건이 없다**. 위 Exceptions의 필수 항목을 충족했다고
표시하지 않으며 @buenhyden의 후속 결정이 필요하다. 파일을 읽거나 이동하거나
share를 재발급해 이 문서 불일치를 자동 해결하지 않는다.

### SEC01 image acceptance

owner는 SEC01(SPEC-0204 TSK-0009)에서 자체 빌드 OpenBao image의 잔여 위험(서명 없음,
CVE-2025-60876, GO-2026-5932 처분)을 받아들였다. 처음 수용한 manifest `46bf9b5c`(Go 1.27.2)는 <!-- runtime-version-exception: history — 교체 전 수용 image의 builder Go 버전이며 build-inputs.json이 현재 pin을 소유함 -->
2026-10-21 stable 조회에서 Go 1.27.3의 crypto/x509 수정(CVE-2026-111943)이 나와 교체됐고, owner는 같은
처분을 가진 교체 image manifest `a58fb110`(Go 1.27.3)을 같은 날 승인했다("이미지 교체 승인"). 교체 image의 재스캔(Grype DB 2026-10-20)도 CVE-2025-60876 Medium 3건과 GO-2026-5932 Unknown 1건만 보고했고, 두 항목의 처분은 바뀌지 않았다. <!-- runtime-version-exception: history — 승인 시점 교체 image의 builder Go 버전이며 build-inputs.json이 pin을 소유함 -->
만료는 SEC01 기준 15 수용이나 image 교체 중 이른 때다. 서명 없음은 기준 15 수용 뒤에도 남을 수 있으므로 그때 따로 판단한다. 이와
별도로, window 시작 7일 안의 stable 조회에서 이 image에 영향을 주는 보안 수정이 나오면 W4·W5
gate가 실패한다. 같은 window가 쓰는 Traefik·Prometheus image의 수용은 각 서비스 정책
([POL-0013](../02-gateway-and-networking/0013-traefik.md#exceptions),
[POL-0045](../07-observability/0045-prometheus.md#exceptions))이 소유한다.

### Maintenance window residuals

2026-10-15 owner는 아래 잔여 위험을 **2026-11-15까지** 받아들였다(마지막 행은 2026-10-21 추가). 2026-10-27 owner는 sealed 정리·남겨 둔 W2 custody·만료 없는 renderer token 세 행을 같은 범위·보완 통제·종료 조건으로 **2026-12-15까지** 다시 받아들였다. token·root·lock은 바꾸지 않았다. 같은 날 owner는 UID 100 공유와 암호화 안 된 swap 두 행도 같은 범위·종료 조건으로 **2026-12-15까지** 다시 받아들였다. 다섯 행 모두 그날 다시 결정한다. UID 100과
swap은 기록 전부터 있던 조건이며, window 전에 기록해 window의 편차로 다룬다.

| 잔여 위험 | 범위와 위험 | 종료 조건 |
| --- | --- | --- |
| UID 100 공유 | host `dhcpcd` 계정이 OpenBao와 같은 UID라 audit log, TLS server key, Raft data, Agent token·SecretID·`role_id`, 렌더 값, exec 중 container 안 `bao` 환경의 token을 읽을 수 있다. dhcpcd 권한 분리 process는 chroot된다 | OpenBao를 host에 없는 UID로 옮기거나 경로 권한으로 막음 |
| 암호화 안 된 swap | host `/swap.img`가 암호화되지 않아 tmpfs의 custody·token page가 disk로 나갈 수 있고 `shred`가 그 사본을 지우지 못한다 | swap 암호화, 또는 window 동안 swap 끄기 |
| sealed 정리의 관리 접근 상실 | server가 sealed인 채 window가 멈추면 OIDC 확인 없이 root custody를 지운다. 복구는 share 2개로 unseal한 뒤 OIDC operator와 W1 절차 | 정리 전에 unseal할 수 있는 검토된 절차 |
| 남겨 둔 W2 custody | W2가 INDETERMINATE로 끝나면 snapshot 전용 token(최대 720시간)이 tmpfs에 남고, 다음 window의 W2·W3는 BLOCKED다 | 검토된 W2 복구 절차 |
| 만료 없는 renderer token | SecretID가 1회용이라 renderer AppRole은 24시간 periodic token을 준다(2026-10-21 owner 수용, 지금 HOME과 같은 방식). Agent가 갱신하는 한 만료가 없어, sink token을 복사한 쪽도 계속 갱신할 수 있다. 권한은 Keycloak·Grafana KV 2개 읽기이고 sink는 0600이며, 갱신이 멈추면 24시간 안에 만료된다. W5 재발급은 이전 Agent token을 폐기하지 않는다 | W5에서 이전 Agent token을 폐기하는 검토된 절차, 또는 재인증 없이 유지되는 유한 수명 |

### P01 Native Trust and Audit Gate

정상 경로는 내부 native TLS와 검증된 CA/SAN이다. bootstrap key/CA trust는 해당
OpenBao에만 의존하지 않는다. wrapping SecretID의 creation path·짧은 TTL·1회 사용과
제한 role fetch/render version을 검증하며 sink 존재는 readiness가 아니다. Agent에
Docker socket을 주거나 무제한 restart로 인증 실패를 숨기지 않는다.

config-owned HMAC file audit를 유지하며 모든 필수 backend 실패 시 업무 요청의
실패/지연을 수용한다. health 응답은 audit 증거가 아니며 audit 비활성화로 성공시키지
않는다. 실제 filesystem 용량, rotation owner/schedule/보존, 실패 알림을 HOME에서
검증해야 한다. rotation은 host logrotate 규칙(`/etc/logrotate.d/openbao`)과 기존
`logrotate.timer`의 시간 단위 drop-in이 맡는다. 회전이 멈춰 `audit.json.1`이 계속 커지는 경우를
알리는 경보는 아직 없으며, 이 운영 공백은 owner @buenhyden이 맡고 logrotate 실패나 audit 파일
정체 경보를 더하면 닫는다. 기존 single-file custody 예외는 미해결 상태로 보존한다. P01 격리 시험은
그 예외를 종료하거나 HOME 복구 자료를 만들어내지 않는다. P06 확대는 실제 cold boot·
RUN-0105 5단계 custody 기록(SPEC-0242)·선정 snapshot 복구 수용 이후만 허용한다.

### Versioned issuance identity control

새 renderer issuance는 `schema_version: 2` journal과 `issuance_id`를 사용하며,
`issuance_id`와 legacy `nonce`는 동일해야 한다. v2 accessor metadata는
`issuance_schema: "2"`, `issuance_id`, `sec01_nonce`를 모두 포함하고 두 identity 값을
일치시켜야 한다. v1 journal과 anchor의 version 없는 역사적 정확한 형태는 호환 대상으로
보존한다.

journal과 활성 anchor의 version·identity가 정확히 같고, accessor metadata가 해당 journal
version에서 유도한 전체 metadata와 정확히 같은 경우만 정합화할 수 있다. completion witness는
중단된 정리의 복구를 허용하는 별도 기록이다. cross-version 조합, alias 불일치, 복수 accessor는
accessor 폐기 전에 차단한다. 이전 발급을 정합화한 같은 실행은 새 SecretID를 발급하지 않는다.
이 통제는 HOME의 credential, custody, snapshot 또는 recovery 수용을 증명하지 않으며 해당 실제
입력이 확정될 때까지 HOME 적용을 금지한다.

### P02 공개 catalog 통제

catalog와 schema는 공개 분류·보존 계약의 단일 원천이다. 값·값의 hash·token·실제 KV
payload를 넣거나 같은 ID를 별도 inventory로 복제하지 않는다. `source_recorded_at`은
공개 원본의 기록 날짜이며 runtime 증거 날짜로 승격하지 않는다.

현재 destination plan의 mount·field·UID/GID·mode는 null이며 ACL·delivery·reload·restart·
rotation은 `BLOCKED_P01`이다. 이를 실제 binding으로 바꾸려면 해당 소비자·신원·경로와
복구 경계를 후속 검토해야 한다. `CONFIRMED` lane의 증거 pointer는 구조적 기록일 뿐,
실제 소비·이관·rotation·복구를 별도로 확인하지 않은 수용을 허용하지 않는다.

canonical `COMM-002`와 alias `COMM-003`, crypto/bootstrap/recovery/LAB/unknown/migrated/
retired 또는 이미 observed/consumed인 항목의 재생성을 거부한다. alias는 별도 credential,
파일 생성 또는 KV 경로를 만들 수 없다. COMM-003 실제 폐기는 SMTP01만 실행하며,
PG-020의 초기화·복구 보존 판정을 변경하지 않는다. `UNUSED_DELETE`도 source, runtime,
jobs, backup/restore, external 소비자와 복구 증거를 확인하기 전에는 삭제 승인이 아니다.

CLI 입력은 네 추적 공개 파일로 한정한다. `render`는 operator-owned 경로와 regular,
single-link README 및 no-follow 조건을 충족한 `.agent-work/p02-views`의 네 공개 출력만
갱신한다. private metadata·환경·KV·HOME 또는 기존 공개 원본을 덮어쓰지 않는다.
상속 lock은 참여하는 협력 writer의 경계이므로 CLN이나 비참여 writer의 동시 쓰기 중지는
별도로 확인한다. staging 일치·비활성 profile·traffic zero·source search zero를 실제
consumer zero 또는 운영 수용 증거로 보고하지 않는다.

### Review Cadence

매월, 그리고 이미지, persistence, 인증, 노출이 변경되기 전에 검토한다.

### Traceability

- Governing architecture: [AD-0003](../../../02.architecture/descriptions/0003-security-architecture.md)
- [Guide](../../guides/04-security-and-secrets/0085-openbao.md), [Policy](0085-openbao.md), [Runbook](../../runbooks/04-security-and-secrets/0085-openbao.md)
- OpenBao 공식 TCP listener 파라미터: <https://openbao.org/docs/configuration/listener/tcp/>
- OpenBao 공식 authenticated root generation API: <https://openbao.org/docs/api/system/generate-root-token/>
- OpenBao 공식 deprecated legacy root generation API: <https://openbao.org/docs/api/system/generate-root/>
- unauthenticated generate-root를 다루는 OpenBao 공식 deprecation note: <https://openbao.org/community/deprecation/unauthed-generate-root/>
- authenticated root generation을 다루는 OpenBao 공식 release notes: <https://openbao.org/community/release-notes/2-6-0/>

## Verification

Compose/profile 검증과 [runbook](../../runbooks/04-security-and-secrets/0085-openbao.md)이 별도의 정적/런타임 증거를
제공한다. 예상치 못한 서비스, 마운트, 인증, readiness 상태가 보이면 중단한다.

## Related Documents

- [Operations index](../../README.md)
- [Upstream documentation](https://openbao.org/docs/agent-and-proxy/agent/)
- [OpenBao unauthenticated generate-root deprecation](https://openbao.org/community/deprecation/unauthed-generate-root/)

고정 runtime의 미사용 SecretID 만료 결함(GHSA-7m59-mp95-w6ph)은 TTL·wrapping·1회 사용 선언으로
해결됐다고 간주하지 않는다. 수정 버전 검증과 HOME gate 전에는 배포·P06 확대를 보류하며,
미사용 발급의 명시적 폐기와 거부를 별도로 확인한다. 상세 근거는 RUN-0085의 Known Runtime Residual을 따른다.
