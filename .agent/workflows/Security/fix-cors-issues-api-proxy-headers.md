---
description: Resolve Cross-Origin Resource Sharing errors in API calls
---

1. **Understand the Error**:
   - CORS errors occur when frontend (<http://localhost:3000>) calls API (<http://api.example.com>).
   - Browser blocks the request unless the API explicitly allows it.

2. **Quick Fix (Next.js API Route Proxy)**:
   - Create a proxy to bypass CORS during development.

   ```ts
   // app/api/proxy/route.ts
   export async function GET(request: Request) {
     const { searchParams } = new URL(request.url);
     const url = searchParams.get('url');

     const response = await fetch(url!, {
       headers: { 'User-Agent': 'MyApp/1.0' },
     });

     return new Response(response.body, {
       headers: {
         'Content-Type': response.headers.get('Content-Type') || 'application/json',
       },
     });
   }
   ```

   - Call it: `fetch('/api/proxy?url=' + encodeURIComponent('https://api.example.com/data'))`

3. **Production Fix (Backend)**:
   - Add CORS headers to your API.

   ```ts
   // Express.js
   app.use((req, res, next) => {
     res.header('Access-Control-Allow-Origin', 'https://yourdomain.com');
     res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
     res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization');
     if (req.method === 'OPTIONS') return res.sendStatus(200);
     next();
   });
   ```

4. **Next.js Config (Development)**:
   - Add rewrites for local development.

   ```js
   // next.config.js
   module.exports = {
     async rewrites() {
       return [
         {
           source: '/api/:path*',
           destination: 'https://api.example.com/:path*',
         },
       ];
     },
   };
   ```

5. **Pro Tips**:
   - Never use `Access-Control-Allow-Origin: *` in production.
   - For authenticated APIs, include `Access-Control-Allow-Credentials: true`.
   - Use environment variables for allowed origins.
