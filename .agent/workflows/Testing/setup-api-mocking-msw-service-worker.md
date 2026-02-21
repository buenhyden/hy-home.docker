---
description: Mock API requests for testing and development
---

1. **Install MSW**:
   - Mock Service Worker for API mocking.
   // turbo
   - Run `npm install --save-dev msw@latest`

2. **Initialize MSW**:
   - Generate service worker file.
   // turbo
   - Run `npx msw init public/ --save`

3. **Create Handlers**:
   - Define mock API responses.

   ```ts
   // mocks/handlers.ts
   import { http, HttpResponse } from 'msw';

   export const handlers = [
     http.get('/api/user', () => {
       return HttpResponse.json({
         id: '1',
         name: 'John Doe',
         email: 'john@example.com',
       });
     }),

     http.post('/api/login', async ({ request }) => {
       const { email } = await request.json() as { email: string };

       if (email === 'test@example.com') {
         return HttpResponse.json({ token: 'fake-jwt-token' });
       }

       return new HttpResponse(null, { status: 401 });
     }),
   ];
   ```

4. **Setup Browser Worker**:
   - Enable mocking in browser.

   ```ts
   // mocks/browser.ts
   import { setupWorker } from 'msw/browser';
   import { handlers } from './handlers';

   export const worker = setupWorker(...handlers);
   ```

5. **Start MSW in Development**:
   - Create a provider to conditionally start MSW.

   ```tsx
   // app/msw-provider.tsx
   'use client'
   import { useEffect, useState } from 'react';

   export function MSWProvider({ children }: { children: React.ReactNode }) {
     const [mswReady, setMswReady] = useState(false);

     useEffect(() => {
       async function init() {
         if (process.env.NODE_ENV === 'development') {
           const { worker } = await import('../mocks/browser');
           await worker.start({
             onUnhandledRequest: 'bypass',
           });
           setMswReady(true);
         } else {
           setMswReady(true);
         }
       }

       init();
     }, []);

     if (!mswReady) return null;
     return <>{children}</>;
   }
   ```

   - Add to layout:

   ```tsx
   // app/layout.tsx
   import { MSWProvider } from './msw-provider';

   export default function RootLayout({ children }) {
     return (
       <html>
         <body>
           <MSWProvider>{children}</MSWProvider>
         </body>
       </html>
     );
   }
   ```

6. **Use in Tests**:
   - Setup for Vitest/Jest.

   ```ts
   // vitest.setup.ts
   import { afterAll, afterEach, beforeAll } from 'vitest';
   import { setupServer } from 'msw/node';
   import { handlers } from './mocks/handlers';

   const server = setupServer(...handlers);

   beforeAll(() => server.listen({ onUnhandledRequest: 'error' }));
   afterEach(() => server.resetHandlers());
   afterAll(() => server.close());
   ```

7. **Pro Tips**:
   - Use MSW to develop frontend before backend is ready.
   - Override handlers per test for different scenarios.
   - MSW works with fetch, axios, and any HTTP client.
   - The browser worker only runs in development mode.
