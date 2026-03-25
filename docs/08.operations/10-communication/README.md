<!-- [ID:docs:08:communication:root] -->
# 🔐 Communication Operations Policy

메일 인프라의 안정성과 보안을 유지하기 위한 운영 정책입니다.

## 1. 보안 정책
- **SPF/DKIM/DMARC**: 모든 발신 도메인은 필수적으로 해당 레코드를 DNS에 유지해야 합니다.
- **TLS 강제**: SMTP Submission(587) 및 IMAPS(993)는 반드시 암호화된 연결을 사용해야 합니다.

## 2. 계정 및 패스워드 관리
- 관리자 계정 패스워드는 Docker Secrets를 통해 주기적으로 갱신합니다.
- 불필요한 메일박스 생성을 제한하고 정기적으로 휴면 계정을 정리합니다.

## 3. 백업 및 모니터링
- `/opt/stalwart` 가 탑재된 볼륨 데이터는 일 단위로 백업해야 합니다.
- SMTP 큐의 적체 상태를 모니터링하여 평소보다 높은 발송 지연 발생 시 원인을 파악합니다.
