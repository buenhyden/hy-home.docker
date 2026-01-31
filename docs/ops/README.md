# Operations Guide

운영 관점에서 필요한 관찰 지점과 기본 원칙을 정리합니다.

## 관측성

- 모니터링 스택: `infra/06-observability/README.md`
- 인증/접근 제어: `infra/02-auth/keycloak/README.md`, `infra/02-auth/oauth2-proxy/README.md`
 - 인프라 분류/프로파일: `infra/README.md`

## 데이터/시크릿

- 기본 시크릿은 `secrets/`에 저장합니다.
- 고급 시크릿 관리는 `infra/03-security/vault/README.md`를 참고합니다.

## 문제 대응

- 서비스별 장애/로그 확인 방법은 각 `infra/<번호-카테고리>/<서비스명>/README.md`에 정리합니다.
