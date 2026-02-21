---
description: Fix infinite render loops
---

1. **State Update During Render**:
   - ❌ `setCount(count + 1)` in render
   - ✅ Use `useEffect`

2. **Fix Dependencies**:

   ```tsx
   const fetchData = useCallback(() => {
     return { data: 'value' };
   }, []);
   ```

3. **Fix Event Handlers**:
   - ❌ `onClick={handleClick()}`
   - ✅ `onClick={handleClick}`

4. **Pro Tips**:
   - Use React DevTools Profiler.
   - Enable Strict Mode.
