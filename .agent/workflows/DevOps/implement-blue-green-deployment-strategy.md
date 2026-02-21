---
description: Zero-downtime deploys
---

1. **Setup Two Environments**:
   - Blue: Current (v1.0)
   - Green: New (v1.1)

2. **Route Traffic Gradually**:

   ```ts
   const rolloutPercent = await get('green_rollout') || 0;
   if (Math.random() * 100 < rolloutPercent) {
     return NextResponse.rewrite(new URL('/green', request.url));
   }
   ```

3. **Monitor Metrics**:

   ```ts
   Sentry.setTag('environment', isGreen ? 'green' : 'blue');
   ```

4. **Pro Tips**:
   - Test thoroughly before routing.
   - Keep blue for rollback.
