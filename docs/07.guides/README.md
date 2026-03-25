# 07.guides

## 목적

이 폴더는 how-to, 온보딩, 사용 가이드, 스타일 가이드를 저장한다. Guide는 이해와 사용을 돕는 문서이지, 운영 정책이나 장애 대응 절차를 담는 문서가 아니다.

## 문서 책임

- 독자가 반복 가능한 방법으로 작업을 수행하도록 돕는다.
- 시스템, 기능, 도구 사용법을 설명한다.
- 흔한 실수와 준비 조건을 정리한다.

## Guide 타입

- onboarding
- how-to
- style-guide
- troubleshooting-guide
- system-guide

## 포함할 내용

- 대상 독자
- 선행 조건
- 단계별 절차
- 흔한 실수
- 관련 Spec/Operation/Runbook 링크

## 포함하지 말아야 할 내용

- 조직 공통 정책
- 운영 통제 기준
- 실시간 사고 대응 절차
- 사고 사후 원인 분석

위 내용은 각각 `08.operations/`, `09.runbooks/`, `11.postmortems/`로 분리한다.

## 배치 규칙

- 일반 가이드는 `07.guides/####-<topic>.md`
- 장기 유지 가이드는 날짜 없이 주제명 기반 파일명을 사용할 수 있다.

## Templates

- [04-data](./04-data/README.md)
- [05-messaging](./05-messaging/README.md)
- [06-observability](./06-observability/README.md)
- [07-workflow](./07-workflow/README.md)
- [08-ai](./08-ai/README.md)
- [09-tooling](./09-tooling/README.md)
- [99.templates](../99.templates/guide.template.md)
