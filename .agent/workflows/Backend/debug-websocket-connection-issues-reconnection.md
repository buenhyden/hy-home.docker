---
description: Fix WebSocket connections
---

1. **Setup with Reconnection**:

   ```tsx
   'use client'
   export function useWebSocket(url: string) {
     const ws = useRef<WebSocket | null>(null);

     useEffect(() => {
       ws.current = new WebSocket(url);
       ws.current.onclose = () => {
         setTimeout(() => connect(), 1000);
       };
     }, [url]);
   }
   ```

2. **Implement Heartbeat**:
   - Send ping every 30 seconds.

3. **Pro Tips**:
   - Use wss:// in production.
   - Test with `wscat`.
