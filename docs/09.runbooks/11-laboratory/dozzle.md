# Dozzle Runbook

: Dozzle (Real-time Log Viewer)

---

## Overview (KR)

이 런북은 Dozzle 서비스의 장애 대응 및 유지보수 절차를 정의한다. 로그 스트림 끊김, UI 응답 없음 등 발생 가능한 일반적인 문제에 대한 해결 단계를 제공한다.

## Purpose

Dozzle 서비스의 가용성을 유지하고 로그 기반의 트러블슈팅 역량을 보존한다.

## Canonical References

- `[../../../infra/11-laboratory/dozzle/README.md]`
- `[../../08.operations/11-laboratory/dozzle.md]`
- `[../../07.guides/11-laboratory/dozzle.md]`

## When to Use

- Dozzle UI에 접속이 불가능한 경우.
- 특정 컨테이너의 로그가 Dozzle에서 보이지 않거나 업데이트되지 않는 경우.
- `/var/run/docker.sock` 관련 권한 오류가 발생하는 경우.

## Procedure or Checklist

### Checklist

- [ ] Dozzle 컨테이너가 `Up` 상태인가?
- [ ] `/var/run/docker.sock` 볼륨 마운트가 정상인가?
- [ ] Traefik 라우팅 및 SSO 인증이 정상인가?

### Procedure

#### Case 1: 로그 스트림 업데이트 중단

1. 브라우저 페이지를 새로고침한다.
2. 해결되지 않을 경우 도커 컴포즈 명령으로 서비스를 재시작한다.

   ```bash
   cd infra/11-laboratory/dozzle
   docker compose restart dozzle
   ```

#### Case 2: 특정 컨테이너 로그 미노출

1. 해당 컨테이너가 실행 중인지 확인한다 (`docker ps`).
2. Dozzle 컨테이너의 로그를 확인하여 접근 거부(Permission Denied) 오류가 있는지 검사한다.

   ```bash
   docker logs dozzle
   ```

## Verification Steps

- [ ] `https://dozzle.${DEFAULT_URL}` 접속 후 실시간 로그가 흐르는지 확인.
- [ ] 사이드바에서 여러 컨테이너를 전환하며 정상 응답 여부 확인.

## Safe Rollback or Recovery Procedure

- 이미지 업데이트 후 장애 발생 시, 이전 태그(`v10.2.0`)로 명시적으로 롤백한 후 재배포한다.
- 설정 파일 오류 시 백업본(`.bak` 등)에서 복원한다.

## Related Operational Documents

- **Incident Record**: `[../../10.incidents/README.md]`
- **Postmortem**: `[../../11.postmortems/README.md]`
