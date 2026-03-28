# 01-Gateway Guides

> `01-gateway`(Traefik/Nginx) 설정/운영 이해를 위한 가이드 인덱스.

## Overview (KR)

이 디렉터리는 게이트웨이 구성 이해와 변경 작업 방법을 설명한다. 정책은 `08.operations`, 즉시 복구 절차는 `09.runbooks`를 참조한다.

## Structure

```text
01-gateway/
├── 01.setup.md   # 초기 구성 및 실행 절차
├── traefik.md    # Traefik primary gateway guide
├── nginx.md      # Nginx special-path proxy guide
└── README.md
```

## Related Documents

- [Spec](../../04.specs/01-gateway/spec.md)
- [Operations](../../08.operations/01-gateway/README.md)
- [Runbooks](../../09.runbooks/01-gateway/README.md)
- [Plan](../../05.plans/2026-03-28-01-gateway-optimization-hardening-plan.md)
