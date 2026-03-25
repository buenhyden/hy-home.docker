<!-- [ID:docs:09:communication:root] -->
# 🆘 Communication Recovery Runbook

메일 서비스 장애 시 대응 절차를 안내합니다.

## 1. 메일 발송/수신 실패
- **증상**: 앱에서 메일 발송 시 에러 발생 또는 수신 지연.
- **조치**:
  1. `docker logs stalwart` 명령으로 SMTP 로그 확인.
  2. 스팸 필터 레이팅에 의한 차단 여부 검토.
  3. 포트 25가 ISP 등에 의해 차단되었는지 확인 (`telnet` 등 이용).

## 2. Stalwart 서비스 불능
- **증상**: UI 접속 불가 및 모든 메일 프로토콜 응답 없음.
- **조치**:
  1. 컨테이너 상태 확인: `docker ps | grep stalwart`
  2. 재시작 시도: `docker-compose restart stalwart`
  3. 데이터 볼륨 권한 이슈 확인.

## 3. MailHog 큐 포화
- **증상**: MailHog UI가 매우 느리거나 메일 캡처가 누락됨.
- **조치**:
  - MailHog는 인메모리 저장소를 사용하므로 컨테이너를 재시작하여 메모리를 비웁니다.
