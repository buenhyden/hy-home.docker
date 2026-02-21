---
description: Protect APIs with rate limits
---

1. **Install Upstash**:
   // turbo
   - Run `npm install @upstash/ratelimit @upstash/redis`

2. **Setup**:

   ```ts
   import { Ratelimit } from '@upstash/ratelimit';

   const ratelimit = new Ratelimit({
     redis,
     limiter: Ratelimit.slidingWindow(10, '10 s')
   });
   ```

3. **Apply to Routes**:

   ```ts
   const { success } = await ratelimit.limit(ip);
   if (!success) return Response.json({ error: 'Too many requests' }, { status: 429 });
   ```

4. **Pro Tips**:
   - Different limits per endpoint.
   - Log violations.
