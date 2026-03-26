# RedisInsight

> Redis visualization, analysis, and management tool.

## Overview

RedisInsight는 Redis 데이터베이스의 키-값 조회, 스트림 분석, 메모리 프로파일링을 제공하는 GUI 도구다. `admin` 프로필을 사용하여 관리 환경에서 로드된다.

## Implementation Details

| Category   | Technology   | Notes |
| ---------- | ------------ | ----- |
| Image      | redis/redisinsight:3.0.3 | |
| Profile    | admin        | |
| Storage    | ${DEFAULT_MANAGEMENT_DIR}/redisinsight | Saved connections and settings |

## Configuration

### Environment Variables

| Variable | Required | Description |
| -------- | -------- | ----------- |
| `REDIS_INSIGHT_PORT` | No | Default: 5540 |

## Related References

- **Guide**: [Redis Analysis Guide](../../../docs/07.guides/11-laboratory/README.md#using-redisinsight)
- **Tier**: [11-laboratory](../README.md)
