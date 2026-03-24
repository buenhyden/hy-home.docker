# 08.operations

## 목적

이 폴더는 운영 정책(Operations Policy)과 공통 기준을 저장한다. 이곳의 문서는 무엇을 허용하고 금지하는지, 어떤 기준과 통제를 지켜야 하는지를 정의한다.

## 문서 책임

- 운영 기준과 통제 정의
- 환경 및 배포 승격 조건 정의
- 보안·로그·증적·보존 기준 정의
- AI Agent 변경 통제 정의

## 포함할 내용

- 운영 정책
- SLO/SLI 기준
- 보안 기준
- 배포 승격 기준
- 로그/증적/보존 정책
- 모델/프롬프트 변경 관리 정책
- 예외 승인 절차

## 포함하지 말아야 할 내용

- 실제 명령 절차
- 장애 타임라인
- 근본 원인 분석
- 온보딩 또는 how-to 설명

위 내용은 각각 `09.runbooks/`, `10.incidents/`, `11.postmortems/`, `07.guides/`로 분리한다.

## Agent 운영 정책 예시

- Model/Prompt 변경 프로세스
- Eval·Guardrail 통과 기준
- Safety Incident 임계값
- Trace/Log 보존 기준

## 시작 템플릿

- `../99.templates/operation.template.md`
