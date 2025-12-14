### hy-home.docker — Copilot / AI 에이전트 지침

이 문서는 hy-home.docker 저장소에서 AI 에이전트가 빠르게 작업을 시작할 수 있도록 핵심 정보와 실무 사례를 요약합니다.

1. 핵심 아키텍처 요약

- `Infra/`: 모듈형 Docker Compose 서비스(리버스 프록시, 인증, DB, 메시징, 관측성, AI 등).
- `Projects/`: Django, FastAPI, NestJS, NextJS, ReactJS, Express, Maven/Gradle 템플릿.
- `Infra/docker-compose.yml`은 `include:`로 서비스별 `Infra/<service>/docker-compose.yml`들을 조립합니다.

2. 인프라 서비스 추가 체크리스트 (요약)

- 1. 새 폴더 생성: `Infra/<service>/` 및 `Infra/<service>/docker-compose.yml` 작성.
- 2. 네트워크/볼륨/시크릿 구성: `infra_net` 네트워크 사용, 필요한 `volumes:`와 `secrets:` 선언.
- 3. `Infra/docker-compose.yml`의 `include:`에 항목 추가:

```yaml
include:
  - kafka/docker-compose.yml
  - <service>/docker-compose.yml
```

- 4. 루트 `secrets/`에 시크릿 파일 추가(로컬만 사용):

```powershell
echo "your_password" > secrets/myservice_password.txt
```

- 5. `Infra/docker-compose.yml` 최상단 `secrets:`에 등록(파일 참조).
- 6. `Infra/docker-compose.yml` `volumes:`에 볼륨 추가(필요시).
- 7. `Infra/README.md`와 루트 `README.md`에 서비스 설명을 추가.
- 8. 로컬로 검증: `cd Infra/<service> && docker-compose up -d` 및 `docker-compose logs -f <service>`.

3. 빠른 예시: Compose 템플릿

```yaml
# Infra/myservice/docker-compose.yml
services:
  mysvc:
    image: myorg/mysvc:latest
    networks:
      - infra_net
    secrets:
      - mysvc_password
secrets:
  mysvc_password:
    file: ../../secrets/mysvc_password.txt
```

4. PR 작성 및 검증 체크리스트

- 변경 요약: PR 본문에 변경 내용(서비스 추가/변경), 로컬 테스트 방법, 영향 범위를 명시합니다.
- 민감 정보: `secrets/`는 로컬 전용, 절대 커밋 금지. 변경이 필요한 시크릿은 문서로 안내.
- 문서 업데이트: `Infra/README.md`와 루트 `README.md`에 서비스 설명 추가.
- 로컬 검증 명령 예시:

```powershell
# 전체 스택(주의: 리소스 많이 사용)
cd Infra
docker-compose up -d
# 단일 서비스
cd Infra/<service>
docker-compose up -d
docker-compose logs -f <service>
```

- 연결/헬스 체크 예시: `curl -k https://<service>.127.0.0.1.nip.io` 또는 컨테이너 내부에서 `psql`/`redis-cli` 접속 테스트.

5. 자주 사용하는 명령 모음

- 전체 로그: `docker-compose logs -f` (Infra 루트)
- 컨테이너 셸 진입: `docker exec -it <container> sh` 또는 `bash`
- 포트 충돌 확인(Windows): `netstat -an | findstr "5432"`
- 볼륨/컨테이너 정리: `docker-compose down -v` (데이터 삭제 주의)

6. 프로젝트 규약/패턴

- 서비스별 환경변수는 루트 `.env` 또는 서비스 내부 `.env.dev.example`을 사용합니다.
- `192.168`이 아닌 `127.0.0.1.nip.io` 네임 패턴 사용(테스트용). `Certs/`와 hosts 안내를 확인하세요.
- 새로운 서비스가 영향을 주는 파일: `Infra/docker-compose.yml`(include, secrets, volumes), `Infra/README.md`, `README.md`.

7. 참고 파일

- 메인 README: `README.md`
- 인프라 통합: `Infra/docker-compose.yml` 및 `Infra/README.md`
- 서비스 단위: `Infra/<service>/docker-compose.yml`
- 프로젝트 템플릿: `Projects/<Stack>/README.md`

더 확장할 항목(요청 시 추가합니다):

- PR 템플릿(검증 항목 포함), 서비스 생성 스크립트, CI 헬스 체크 예시, Kafka Connect 설정 샘플.

8. 제공된 스크립트(빠른 사용법)

- `scripts/new_infra_service.sh` / `scripts/new_infra_service.ps1`: 새 인프라 서비스 템플릿을 생성합니다.
  - 사용 예:
    - POSIX: `./scripts/new_infra_service.sh my-service`
    - PowerShell: `.\\scripts\\new_infra_service.ps1 my-service`
- `scripts/validate_compose_change.sh` / `scripts/validate_compose_change.ps1`: `Infra/docker-compose.yml` 구문 검사, 단일 서비스 smoke-test 실행용 스크립트.
  - 예: `./scripts/validate_compose_change.sh my-service --up` 또는 `.\\scripts\\validate_compose_change.ps1 -ServiceName my-service -Up`

9. CI / 검증 파이프라인

- 이 리포지토리에는 `pull_request` 이벤트에서 `Infra/`와 `scripts/` 변경을 자동으로 검증하는 GitHub Actions 워크플로가 있습니다: `.github/workflows/ci-cd.yaml`.
  - 수동 실행: GitHub UI에서 Actions -> CI/CD Pipeline -> Run workflow
- 동작: `docker compose -f Infra/docker-compose.yml config`로 형식 검증을 수행하고, POSIX/PowerShell 스크립트 테스트 및 Lint(PSScriptAnalyzer/shellcheck)를 실행합니다.
- 추가: CI는 PR에서 변경된 `Infra/<service>` 디렉터리 변경을 감지하여, 변경된 서비스만 smoke-test(`scripts/validate_compose_change.<sh|ps1>`)를 병렬로 실행합니다(최대 병렬수: 4). PR에 감지된 서비스 목록을 댓글로 게시하며, PR 본문에 명시한 `Infra/<service>`와 감지된 서비스가 일치하지 않으면 빌드를 실패시킵니다. 실패한 서비스는 로그와 함께 아티팩트로 업로드 되며, `collect-failures` 단계에서 요약 코멘트가 작성됩니다.
- 필요 시 smoke-test (`--up`)를 추가하려면 PR에 관련 옵션을 요청하세요.

---

이 파일은 저장소 문서와 동기화되도록 주기적으로 갱신하세요.

8. 제공된 스크립트(빠른 사용법)

- `scripts/new_infra_service.sh` / `scripts/new_infra_service.ps1`: 새 인프라 서비스 템플릿을 생성합니다.
  - 사용 예:
    - POSIX: `./scripts/new_infra_service.sh my-service`
    - PowerShell: `.\scripts\new_infra_service.ps1 my-service`
- `scripts/validate_compose_change.sh` / `scripts/validate_compose_change.ps1`: `Infra/docker-compose.yml` 구문 검사, 단일 서비스 smoke-test 실행용 스크립트.
  - 예: `./scripts/validate_compose_change.sh my-service --up` 또는 `.\scripts\validate_compose_change.ps1 -ServiceName my-service -Up`

---

이 파일은 저장소 문서와 동기화되도록 주기적으로 갱신하세요.
