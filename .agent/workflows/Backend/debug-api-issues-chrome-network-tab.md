---
description: Master Chrome DevTools Network tab for API debugging
---

1. **Open Network Tab**:
   - Press F12 → Network tab.
   - Reload the page to capture all requests.

2. **Filter Requests**:
   - Click "Fetch/XHR" to see only API calls.
   - Use the search box to find specific endpoints.

3. **Analyze Failed Requests**:
   - Red requests = failed. Click to see details:
     - **Status**: 400 (bad request), 401 (unauthorized), 404 (not found), 500 (server error)
     - **Headers**: Check `Authorization`, `Content-Type`
     - **Payload**: See what data was sent
     - **Response**: See the error message

4. **Copy as cURL**:
   - Right-click request → Copy → Copy as cURL.
   - Test in terminal to isolate frontend vs backend issues.

5. **Throttle Network**:
   - Select "Slow 3G" to test loading states.
   - Check if your app shows proper loading indicators.

6. **Check Timing**:
   - Click "Timing" tab in request details.
   - Look for slow DNS lookup, initial connection, or waiting time.

7. **Common Fixes**:
   - **CORS Error**: See "Fix CORS Issues" workflow.
   - **401 Unauthorized**: Check if auth token is being sent.

   ```tsx
   fetch("/api/data", {
     headers: { Authorization: `Bearer ${token}` },
   });
   ```

   - **500 Error**: Check server logs, often a backend bug.

8. **Pro Tips**:
   - Enable "Preserve log" to keep requests across page reloads.
   - Use "Disable cache" during development to avoid stale data.
   - Right-click request → "Replay XHR" to re-test without page reload.
