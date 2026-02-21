---
description: Implement Redis caching (Upstash or self-hosted)
---

1. **Option A: Upstash Redis (Serverless Recommended)**:
   - Best for Vercel/Edge environments.
   // turbo
   - Run `npm install @upstash/redis`

   ```ts
   import { Redis } from '@upstash/redis';

   const redis = new Redis({
     url: process.env.UPSTASH_REDIS_REST_URL!,
     token: process.env.UPSTASH_REDIS_REST_TOKEN!,
   });

   // Usage
   await redis.set('key', 'value', { ex: 300 });
   const value = await redis.get('key');
   ```

2. **Option B: Self-Hosted (ioredis)**:
   - Best for long-running servers (VPS/Docker).
   // turbo
   - Run `npm install ioredis`

   ```ts
   import Redis from 'ioredis';
   const redis = new Redis(process.env.REDIS_URL);
   ```

3. **Cache Pattern**:

   ```ts
   export async function getCachedUser(id: string) {
     const cacheKey = `user:${id}`;
     const cached = await redis.get(cacheKey);
     if (cached) return cached;

     const user = await db.user.findUnique({ where: { id } });
     await redis.set(cacheKey, JSON.stringify(user), { ex: 600 }); // 10 mins
     return user;
   }
   ```

4. **Pro Tips**:
   - Use `@upstash/redis` for Edge Middleware compatibility.
   - Always set a TTL (Time To Live) to prevent stale data.
   - Use `hset`/`hgetall` for storing objects efficiently.
