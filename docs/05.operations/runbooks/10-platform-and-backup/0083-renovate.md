---
title: "Renovate Runbook"
version: "0.5.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "operations"
artifact_id: "RUN-0083"
parent_ids:
- "POL-0083"
created: "2026-09-19"
next_review_at: "2027-05-13"
---

# Renovate Runbook

## Trigger and Scope

### Trigger

Renovate job의 정적 점검, 승인된 live run, 잘못된 변경의 복구, systemd timer 운영 절차다.

정적 readiness 점검, 구체적으로 승인된 live job, 또는 잘못된 Renovate 변경의 복구에
사용한다.

### Targets

- 관장 architecture: [AD-0009](../../../02.architecture/descriptions/0009-tooling-architecture.md)
- 대상 peer 문서: [Guide](../../guides/10-platform-and-backup/0083-renovate.md), [Policy](../../policies/10-platform-and-backup/0083-renovate.md)

- [Renovate Compose source](../../../../infra/09-platform-ops/renovate/docker-compose.yml)
- [Derived Compose image projection](../../../../infra/tech-stack.versions.json)
- [Renovate self-hosted configuration](https://docs.renovatebot.com/self-hosted-configuration/)
- [운영 인덱스](../../README.md)

## Preflight

### Authority

저장소 루트에서 작업한다.

### Environment

remote 저장소에 접근하지 않고 `renovate-config-validator`와 `sync-tech-stack-versions.sh --check`로 먼저 검증한다.

시작 상태 확인은 Steps의 1단계에 있다. remote 저장소에 접근하지 않고 `renovate-config-validator`와 `sync-tech-stack-versions.sh --check`로 검증한다.

## Procedure

### Steps

| Step | Action | Expected Result | On Failure |
| --- | --- | --- | --- |
| 1 | remote 접근 없이 `renovate-config-validator --strict`(두 설정)와 `sync-tech-stack-versions.sh --check`로 검증한다 | 문서에 기록 없음 | 문서에 기록 없음; 예상 밖 결과는 Stop Conditions에 따라 중단 |
| 2 | dry-run/discovery 출력, 저장소 scope, token owner, branch protection, 승인 여부를 검토한다 | 1단계 결과만으로 remote readiness를 추론하지 않는다 | 인식되지 않는 허용 명령 또는 과도한 token 권한이면 @buenhyden에게 escalation |
| 3 | remote write가 승인된 경우에만 `docker compose -p hy-home-infra --profile dependency-update run --rm --no-deps renovate`를 실행한다 | Renovate 자체의 run 종료 코드와 로그로 성공 여부를 판단한다 | 사전 secret 확인 또는 이미지 pull 실패 시 실행을 중단하고 원인을 확인 |
| 4 | 정제된 exit status를 기록하고 생성된 remote 변경 사항을 열거하며 각 branch/PR를 검토한다 (merge/close 금지) | 생성된 모든 branch/PR이 기록된다 | 알 수 없는 remote write면 @buenhyden에게 escalation |
| 5 | 캐시·원격 변경 복구와 업그레이드: live job 미사용 확인 후 cache를 삭제/재생성하고 upgrade 전 release note를 검토하며 dry-run 후 단일 canary repository를 실행한다 | 문서에 기록 없음 | 노출 의심 시 secret owner를 통해 token을 회전하고 @buenhyden에게 escalation |
| 6 | 승인된 systemd 설치: 설치본과 추적 파일을 `diff`로 비교한 뒤 검토된 unit 파일을 `/etc/systemd/system/`에 복사한다 | 문서에 기록 없음 | 별도 승인이 없으면 수행하지 않음 |
| 7 | 승인된 systemd 설치: `daemon-reload` 후 `hyhome-renovate.timer`만 enable/start 한다 | 문서에 기록 없음 | 원격 쓰기가 승인되지 않았다면 timer를 활성화하지 않음 |
| 8 | Timer 점검: `systemctl status`/`list-timers`로 상태와 다음 실행 시각을 보고 `journalctl`로 최근 로그만 제한적으로 확인한다 | timer 상태와 다음 trigger 시각을 확인한다 | 문서에 기록 없음 |
| 9 | Timer 수동 실행: 승인된 실행에 한해 `sudo systemctl start hyhome-renovate.service`를 실행한다 | 문서에 기록 없음 | 승인 규칙은 timer 실행과 동일하게 적용되며 미승인이면 실행하지 않음 |
| 10 | Timer 중지: `systemctl disable --now hyhome-renovate.timer`와 service 중지 후 one-off 컨테이너 종료를 별도로 확인한다 | Compose project/service 및 one-off label로 컨테이너 종료를 확인한다 | 남은 작업은 정확한 컨테이너에 한해 승인된 중지 절차로 종료(호스트 전역 prune 금지) |
| 11 | 예약 실행 변경의 예상 효과: 승인 범위(대상 저장소 / token 권한 / 실행 시간)와 service 작업 디렉터리 / 실행 사용자 / Docker 접근을 설치본과 대조한다 | 문서에 기록 없음 | 사전 secret 확인 또는 이미지 pull이 실패하면 실행을 중단하고 원인을 확인 |

1. remote 저장소에 접근하지 않고 검증한다.

   ```bash
   renovate-config-validator --strict --no-global renovate.json5
   renovate-config-validator --strict infra/09-platform-ops/renovate/config/config.js
   bash scripts/operations/sync-tech-stack-versions.sh --check
   ```

2. dry-run/discovery 출력, 저장소 scope, token owner, branch protection, 승인 여부를
   검토한다. 1단계 결과만으로 remote readiness를 추론하지 않는다.
3. remote write가 승인된 경우에만 job을 실행한다.

   ```bash
   docker compose -p hy-home-infra --profile dependency-update run --rm --no-deps renovate
   ```

   실행의 성공 여부는 wrapper 종료 코드가 아니라 Renovate 자체의 run 종료 코드와 로그로 판단한다.
   Renovate PR을 갱신(rebase)하려면 `rebase` label을 붙이거나 job을 다시 실행한다. GitHub
   update-branch는 쓰지 않는다(merge commit이 commitizen 검사를 깨뜨림, #893).
   PR 처리 규칙은 [POL-0086](../../policies/10-platform-and-backup/0086-dependency-version-management.md#renovate-운영-규칙)이 소유한다.

4. 정제된 exit status를 기록하고 생성된 remote 변경 사항을 열거한다. 각 branch/PR를 검토한다.
   이 실행 승인 범위에서는 merge나 close를 하지 않는다.

#### 캐시·원격 변경 복구와 업그레이드

live job이 사용하지 않는지 확인한 후에만 cache를 삭제/재생성한다. policy를
Git에서 복원하고, 잘못된 원격 branch/PR을 개별적으로 검토하거나 닫으며,
노출이 의심될 때만 secret owner를 통해 token을 회전한다. 이미지 upgrade
전에는 Renovate release note와 migration을 검토하고 두 설정 모두를
validation한 뒤, 제한된 repository 집합에 대해 dry-run/discovery를 실행하고
단일 승인된 canary repository를 실행한다.

#### 승인된 systemd 설치

주간 timer(`hyhome-renovate.timer`)는 HOME 호스트에 설치된 기본 실행이다. 위 Compose 명령은 머지 사이의 rebase·재시도용 온디맨드 실행이다.
host unit을 설치하거나 교체하는 것은 별도 승인이 필요한 host 변경이다.
symlink 대신 검토된 파일을 복사해 checkout이나 branch 전환, pull이 systemd가
실행하는 내용을 조용히 바꾸지 못하게 한다. 설치본과 현재 추적 파일을 별도로 비교한다.

```bash
# 1. Compare, then copy the reviewed revision (approved host change only)
diff /etc/systemd/system/hyhome-renovate.service infra/09-platform-ops/renovate/systemd/hyhome-renovate.service
diff /etc/systemd/system/hyhome-renovate.timer infra/09-platform-ops/renovate/systemd/hyhome-renovate.timer
sudo install -m 0644 infra/09-platform-ops/renovate/systemd/hyhome-renovate.service /etc/systemd/system/
sudo install -m 0644 infra/09-platform-ops/renovate/systemd/hyhome-renovate.timer /etc/systemd/system/

# 2. Reload and enable only the timer
sudo systemctl daemon-reload
sudo systemctl enable hyhome-renovate.timer
sudo systemctl start hyhome-renovate.timer
```

#### Timer 점검·수동 실행·중지

```bash
# Timer status and next trigger time
systemctl status hyhome-renovate.timer
systemctl list-timers hyhome-renovate.timer

# 최근 로그만 제한적으로 확인하고 비밀·개인정보를 제거한다
journalctl -u hyhome-renovate.service -n 200 --no-pager

# Trigger manually (bypass timer, authorized runs only)
sudo systemctl start hyhome-renovate.service

# Stop and disable scheduled runs without removing the unit
sudo systemctl disable --now hyhome-renovate.timer
# service 중지 뒤 정확한 one-off 컨테이너 종료 여부를 별도로 확인한다
sudo systemctl stop hyhome-renovate.service
```

> policy와 runbook의 모든 live-run 승인과 evidence 규칙은 timer가 트리거한
> run과 수동으로 트리거한 run에 똑같이 적용된다.

#### 예약 실행 변경의 예상 효과

timer 시작·재활성화는 놓친 일정의 catch-up 작업을 유발할 수 있다. 승인 범위에
대상 저장소·token 권한·실행 시간을 포함하고 원격 쓰기가 승인되지 않았다면 timer를
활성화하지 않는다. service의 작업 디렉터리·실행 사용자·Docker 접근을 설치본과
대조한다. 사전 secret 확인 또는 이미지 pull이 실패하면 실행을 중단하고 원인을 확인한다.

`systemctl stop` 성공만으로 Docker daemon의 작업 컨테이너 종료를 단정하지 않는다.
Compose project/service 및 one-off label로 해당 실행을 식별하고
`docker compose --profile dependency-update ps --all renovate`와 필요한 제한된
상태 조회로 확인한다. 남은 작업은 정확한 컨테이너에 한해 승인된 중지 절차로 종료한다.
`--rm`은 컨테이너 종료 후 제거 설정이며 호스트 전역 prune은 금지한다.

### Stop Conditions

사전 secret 확인 또는 이미지 pull이 실패하면 실행을 중단하고 원인을 확인한다. 알 수 없는 remote write, 과도한 token 권한, token 노출 의심, 인식되지 않는 허용 명령, 안전하게 조정할 수 없는 remote 상태는 에스컬레이션 사유다.

사전 secret 확인 또는 이미지 pull이 실패하면 Steps에서 실행을 중단하고 원인을 확인한다. 알 수 없는 remote write, 과도한 token 권한, token 노출 의심 등은 Escalation에 있다.

## Verification

### Expected Results

#### Service Checks

서비스 점검은 아래 항목에 따른다.

#### 복구 완료 기준

Renovate job이 실행 중이지 않고, config가 검증되고, remote 변경 사항이 파악되고, token
처리 상태가 확인되면 복구가 완료된 것이다. 이 복구 단계는 아직 실행되지 않았으므로
remote 저장소 변경이나 token validation은 주장하지 않는다.

#### Evidence

승인 여부, config commit, 이미지 선언, 대상 저장소, exit status, 정제된 job 요약, 생성된
모든 branch/PR을 기록한다. token, 원본 환경 값, 저장소 credential은 기록하지 않는다.

### Unverified Conditions

이 runbook이 아직 관찰된 적 없는 항목은 다음과 같다.

- 복구 절차 전체: 문서가 이 복구 단계는 아직 실행되지 않았다고 명시하며 remote 저장소 변경이나 token validation은 주장하지 않는다. job 미실행, config 검증, remote 변경 파악, token 처리 상태가 확인된 기록이 검증 근거가 된다.
- remote write가 승인된 Renovate job 실행: 이 문서에는 실행 결과가 기록되어 있지 않다. Renovate 자체 종료 코드, 정제된 로그, 생성된 branch/PR 목록이 검증 근거가 된다.
- 승인된 host systemd unit 설치, timer 활성화, 수동 service 실행: 별도 승인이 필요한 host 변경이며 이 문서에는 실행 결과가 기록되어 있지 않다. 설치본과 추적 파일의 `diff`, `systemctl list-timers` 출력이 검증 근거가 된다.
- service 중지 후 작업 컨테이너 종료: 문서는 `systemctl stop` 성공만으로 단정하지 않는다고 밝힌다. `docker compose --profile dependency-update ps --all renovate` 결과가 검증 근거가 된다.
- Dependabot 보안 업데이트 중단: owner의 별도 승인이 필요한 원격 설정이며 이 문서는 변경하지 않는다.

## Escalation

### Next Owner

책임자는 `@buenhyden`이다. 아래 중단 조건과 영향받은 서비스·대상 소유자를 함께 기록하고, 추가 변경 없이 보고한다.

알 수 없는 remote write, 과도한 token 권한, token 노출 의심, 인식되지 않는 허용 명령, 또는
한 번에 하나씩 안전하게 조정할 수 없는 remote 상태는 에스컬레이션한다.

### Recovery or Forward Repair

1. 활성 실행이 원치 않는 변경을 만들고 있다면 해당 컨테이너를 중단한다.
2. 잘못된 local policy를 Git에서 복원하고 strict validation을 다시 실행한다.
3. remote branch/PR을 개별적으로 검토한다. 명시적 승인이 있을 때만 close 또는 revert하고
   audit trail을 보존한다.
4. token이 노출됐을 가능성이 있으면 job을 비활성화하고 secret owner에게 rotate/revoke를
   요청한다. 현재 token을 복사하거나 표시하지 않는다.
5. 캐시 손상은 job이 실행 중이지 않을 때 폐기 가능한 캐시를 재생성하여 복구한다. remote
   저장소 상태는 절대 그 캐시에서 복원하지 않는다.
