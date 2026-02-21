---
description: Prevent white screens of death with a fallback UI
---

1. **Create Component**:
   - Create `src/components/ErrorBoundary.tsx`.

   ```tsx
   'use client';
   import React, { Component, ReactNode } from 'react';

   interface Props {
     children: ReactNode;
     fallback?: ReactNode;
   }

   interface State {
     hasError: boolean;
   }

   class ErrorBoundary extends Component<Props, State> {
     constructor(props: Props) {
       super(props);
       this.state = { hasError: false };
     }

     static getDerivedStateFromError(_: Error): State {
       return { hasError: true };
     }

     componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
       console.error('ErrorBoundary caught:', error, errorInfo);
     }

     render() {
       if (this.state.hasError) {
         return this.props.fallback || (
           <div className="p-8 text-center">
             <h1 className="text-2xl font-bold">Something went wrong</h1>
             <button onClick={() => this.setState({ hasError: false })}>
               Try again
             </button>
           </div>
         );
       }
       return this.props.children;
     }
   }

   export default ErrorBoundary;
   ```

2. **Wrap App**:
   - Use it in `layout.tsx` or specific page components.

   ```tsx
   <ErrorBoundary>
     {children}
   </ErrorBoundary>
   ```

3. **Pro Tips**:
   - In Next.js App Router, use the `error.tsx` file convention for route-level error handling.
   - Error boundaries only catch errors in child components, not in event handlers or async code.
