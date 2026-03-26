# Laboratory Dashboard (Homer)

> A static service dashboard for easy navigation across infrastructure tools.

## Overview

Homer는 하이홈 인프라의 다양한 서비스 링크를 한곳에 모아 보여주는 정적 웹 대시보드다. 사용자가 환경 내 도구들에 빠르게 접근할 수 있도록 돕는다.

## Structure

```text
dashboard/
├── config/
│   └── config.yml    # Main configuration for links and groups
└── docker-compose.yml
```

## How to Work in This Area

1. **링크 추가**: `config/config.yml`의 `services` 섹션 아래에 새로운 그룹이나 아이템을 추가한다.
2. **아이콘 설정**: FontAwesome 아이콘을 사용하여 가시성을 높인다.
3. **볼륨 바인딩**: 로컬 `config` 폴더를 컨테이너의 `/www/assets` 경로에 마운트하여 실시간 반영한다.

## Related References

- **Guide**: [Adding Services to Dashboard](../../../docs/07.guides/11-laboratory/README.md#adding-new-services-to-homer)
- **Official**: [Homer Documentation](https://github.com/bastienwirtz/homer)
