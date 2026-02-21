---
description: Identify and fix memory leaks causing app slowdowns and crashes
---

1. **Take Heap Snapshots**:
   - Open Chrome DevTools → Memory tab.
   - Take a snapshot, interact with your app, take another snapshot.
   - Click "Comparison" to see what objects are being retained.

2. **Common Culprits**:
   - **Event Listeners**: Not removed in cleanup.

   ```tsx
   useEffect(() => {
     const handler = () => console.log("resize");
     window.addEventListener("resize", handler);
     return () => window.removeEventListener("resize", handler); // ✅ Cleanup
   }, []);
   ```

   - **Timers**: `setInterval` not cleared.

   ```tsx
   useEffect(() => {
     const id = setInterval(() => {}, 1000);
     return () => clearInterval(id); // ✅ Cleanup
   }, []);
   ```

   - **Subscriptions**: WebSocket/Observable not closed.

3. **Use React DevTools Profiler**:
   - Enable "Record why each component rendered".
   - Look for components that never unmount or re-render excessively.

4. **Check for Detached DOM**:
   - In Memory tab, filter by "Detached".
   - These are DOM nodes removed from the page but still in memory.

5. **Pro Tips**:
   - Use `useEffect` cleanup functions religiously.
   - Avoid storing large objects in state unnecessarily.
   - Use React's built-in `AbortController` for fetch cleanup.
   - Test with React Strict Mode enabled (mounts/unmounts twice).
