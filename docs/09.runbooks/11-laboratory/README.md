# Laboratory (11-laboratory) Runbook

> 관리 도구 및 대시보드 장애 복구 및 일상 운영 절차.

---

## Overview (KR)

이 런북은 `11-laboratory` 티어의 서비스 유지보수 및 긴급 복구 절차를 정의한다. 관리 데이터의 초기화나 설정 오류 발생 시 즉시 적용 가능한 지침을 제공한다.

## Purpose

관리 UIs의 가용성을 유지하고 설정 오류로 인한 접근 차단 상황을 해결한다.

## Canonical References

- `[../../../infra/11-laboratory/README.md]`
- `[../../08.operations/11-laboratory/README.md]`

## When to Use

- Portainer 관리자 비밀번호 망실 시.
- Homer 대시보드 설정 파일(YAML) 오류로 페이지가 깨진 경우.
- RedisInsight 연결 설정 초기화가 필요한 경우.

## Procedure or Checklist

### Portainer Admin Reset
1. Portainer 컨테이너를 중단한다: `docker compose down`
2. `portainer-password-reset` 도구 또는 `helper` 이미지를 사용하여 볼륨 내 데이터베이스를 수정한다.
3. 컨테이너를 다시 시작한다.

### Homer Configuration Recovery
1. 이전에 백업된 `config.yml.bak`이 있는지 확인한다.
2. 구문 오류 발생 시 `ymllint`를 사용하여 오류 위치를 찾는다.
3. 기본 템플릿으로 복원 후 설정을 하나씩 재적용한다.

## Verification Steps

- [ ] `curl -I https://portainer.${DEFAULT_URL}` 호출 시 200 또는 302(Redirect to SSO) 확인.
- [ ] Homer 대시보드에서 각 아이콘이 정상적으로 렌더링되는지 확인.

## Safe Rollback Procedure

- 설정 변경 전 반드시 `cp config.yml config.yml.$(date +%F)` 명령으로 원본을 보관한다.
- 장애 발생 시 백업본을 원문으로 복사한 뒤 컨테이너를 재시작한다.

---

## Related Operational Documents

- **Postmortem**: `[../../11.postmortems/2026/03-26-homer-config-corruption.md]` (가상 예시)
