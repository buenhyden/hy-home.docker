<!--
  PULL REQUEST TEMPLATE
  Fill in required sections and run local validation steps before requesting review.
-->

## 변경 요약

- 무엇을 변경하거나 추가했는지 간단히 설명하세요.

## 관련 이슈

- 관련된 이슈가 있으면 번호를 기입하세요.

## 검증 체크리스트 (로컬에서 모두 수행)

- [ ] `Infra/docker-compose.yml` 구문 검사: `docker compose -f Infra/docker-compose.yml config` (성공)
- [ ] 스크립트/CI 자동검증을 통과했는지 확인 (PR 시 GitHub Actions가 실행됩니다)
- [ ] 새 서비스가 포함된 경우: `cd Infra/<service> && docker compose up -d` (단일 서비스로 실행 가능해야 함)
- [ ] 시크릿 추가가 필요한 경우: `secrets/`에 파일을 추가(로컬)하고 커밋하지 마세요
- [ ] `Infra/README.md`와 루트 `README.md`에 문서/접속 정보를 추가
- [ ] `Infra/docker-compose.yml`의 `include:`에 해당 서비스 파일 경로가 정확히 기입되어 있는지 확인
- [ ] `docker-compose`로 실제 최소한의 헬스 체크 (예: curl -k https://<service>.127.0.0.1.nip.io) 확인
- [ ] 서비스 영향 범위를 PR 본문에 명시 (예: `Infra/postgresql-cluster`, `Infra/minio`)

## 변경 영향

- 어떤 서비스/리소스에 영향을 주는지 서술하세요.

## 검토시 확인 포인트(Reviewer 가 확인할 것)

- 구성파일 추가/변경을 주석으로 명확하게 작성했는지
- 민감정보가 리포에 커밋되지 않았는지
- 문서가 충분히 업데이트 되었는지

CI 안내: PR에서 변경된 `Infra/` 서비스는 CI가 감지하여 PR에 댓글로 알립니다. PR 본문에 기재한 서비스와 CI가 감지한 서비스가 일치하는지 확인하세요.

## 배포/테스트 가이드 (선택)

- 로컬에서 빠르게 검증하는 방법을 단계별로 작성하세요.
