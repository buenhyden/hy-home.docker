---
description: Systematically debug and fix 'Text content does not match server-rendered HTML' errors
---

1. **Check for Invalid HTML Nesting**:
   - The most common cause is invalid HTML, like a `<div>` inside a `<p>` tag.
   - **React 19 Update:** React 19 provides much better hydration error diffs. Check the console for the exact mismatch location.
   - **Bad:** `<p><div>Content</div></p>`
   - **Good:** `<div><div>Content</div></div>` or `<p><span>Content</span></p>`

2. **Handle Random Values (Dates, Math.random)**:
   - If you render data that changes between server and client (like `new Date()` or `Math.random()`), it will cause a mismatch.
   - **Fix:** Use a `useEffect` to set the value only on the client.

   ```tsx
   const [mounted, setMounted] = useState(false);
   useEffect(() => setMounted(true), []);
   if (!mounted) return null; // or a loading skeleton
   ```

3. **Fix Browser-Only APIs**:
   - Accessing `window` or `localStorage` during the initial render will fail on the server.
   - **Fix:** Ensure these are only accessed inside `useEffect` or event handlers.

4. **Suppress Warning (Last Resort)**:
   - If you absolutely cannot fix the mismatch (e.g., a timestamp that *must* be dynamic), you can suppress the warning on a specific element.

   ```tsx
   <div suppressHydrationWarning>
     {new Date().toLocaleTimeString()}
   </div>
   ```

5. **Pro Tips**:
   - Use the **React DevTools** Profiler to see exactly what props are changing.
   - Check your browser extensions; sometimes they inject HTML that messes with hydration (try Incognito mode).
