---
description: Comprehensive performance optimization workflow for web applications
---

1. **Establish performance baseline**

    Measure current performance metrics before optimization.

    **Run Lighthouse audit:**

    ```bash
    npx lighthouse https://localhost:3000 --view --output=html --output-path=./reports/lighthouse-before.html
    ```

    **Key metrics to record:**

    - First Contentful Paint (FCP): Target < 1.8s
    - Largest Contentful Paint (LCP): Target < 2.5s
    - Total Blocking Time (TBT): Target < 200ms
    - Cumulative Layout Shift (CLS): Target < 0.1
    - Time to Interactive (TTI): Target < 3.8s

    **For APIs:**

    ```bash
    # Install Apache Bench
    # Ubuntu: sudo apt-get install apache2-utils
    # macOS: brew install ab

    # Benchmark endpoint
    ab -n 1000 -c 10 http://localhost:3000/api/users
    ```

    Record average response time and requests/second.

2. **Analyze bundle size**

    Identify large dependencies and code.

    // turbo

    ```bash
    # Analyze React/Vite bundle
    npm run build
    npx vite-bundle-visualizer

    # Analyze Next.js bundle
    npm run build
    npx @next/bundle-analyzer
    ```

    **Look for:**

    - Packages > 100KB
    - Duplicate dependencies
    - Unused code
    - Heavy libraries (moment.js, lodash, etc.)

3. **Optimize images**

    Compress and optimize image assets.

    **Convert to modern formats:**

    ```bash
    # Install sharp for image optimization
    npm install sharp

    # Convert to WebP
    npx sharp-cli --input ./images/*.png --output ./images/optimized/ --format webp --quality 80
    ```

    **Implement responsive images:**

    ```tsx
    // Use Next.js Image component
    import Image from 'next/image';

    <Image
      src="/image.jpg"
      alt="Description"
      width={800}
      height={600}
      placeholder="blur"
      loading="lazy"
    />
    ```

    **CSS sprites for icons:**

    ```bash
    # Create sprite sheet
    npx spritesh --input icons/ --output sprite.svg
    ```

4. **Code splitting and lazy loading**

    Implement dynamic imports for code splitting.

    **React lazy loading:**

    ```tsx
    import { lazy, Suspense } from 'react';

    // Before
    import HeavyComponent from './HeavyComponent';

    // After
    const HeavyComponent = lazy(() => import('./HeavyComponent'));

    function App() {
      return (
        <Suspense fallback={<div>Loading...</div>}>
          <HeavyComponent />
        </Suspense>
      );
    }
    ```

    **Next.js dynamic imports:**

    ```tsx
    import dynamic from 'next/dynamic';

    const DynamicChart = dynamic(() => import('./Chart'), {
      loading: () => <p>Loading chart...</p>,
      ssr: false, // Disable server-side rendering if not needed
    });
    ```

    **Route-based code splitting:**

    ```tsx
    // router.tsx
    const routes = [
      {
        path: '/dashboard',
        component: lazy(() => import('./pages/Dashboard')),
      },
      {
        path: '/analytics',
        component: lazy(() => import('./pages/Analytics')),
      },
    ];
    ```

5. **Optimize dependencies**

    Replace heavy libraries with lighter alternatives.

    **Common optimizations:**

    ```bash
    # Replace moment.js (67KB) with date-fns (13KB)
    npm uninstall moment
    npm install date-fns

    # Replace lodash with lodash-es (tree-shakeable)
    npm uninstall lodash
    npm install lodash-es

    # Use specific imports
    // Before
    import _ from 'lodash';
    _.debounce(fn, 300);

    // After
    import debounce from 'lodash-es/debounce';
    debounce(fn, 300);
    ```

6. **Implement caching strategies**

    Add caching at multiple levels.

    **Browser caching (HTTP headers):**

    ```javascript
    // Next.js next.config.js
    module.exports = {
      async headers() {
        return [
          {
            source: '/images/:path*',
            headers: [
              {
                key: 'Cache-Control',
                value: 'public, max-age=31536000, immutable',
              },
            ],
          },
        ];
      },
    };
    ```

    **React Query for API caching:**

    ```tsx
    import { useQuery } from '@tanstack/react-query';

    function UserProfile({ userId }) {
      const { data } = useQuery({
        queryKey: ['user', userId],
        queryFn: () => fetchUser(userId),
        staleTime: 5 * 60 * 1000, // 5 minutes
        cacheTime: 10 * 60 * 1000, // 10 minutes
      });

      return <div>{data?.name}</div>;
    }
    ```

    **Service Worker caching:**

    ```javascript
    // sw.js
    self.addEventListener('fetch', (event) => {
      event.respondWith(
        caches.match(event.request).then((response) => {
          return response || fetch(event.request);
        })
      );
    });
    ```

7. **Optimize rendering performance**

    Reduce unnecessary re-renders.

    **Use React.memo:**

    ```tsx
    import { memo } from 'react';

    const ExpensiveComponent = memo(function ExpensiveComponent({ data }) {
      // Only re-renders when data changes
      return <div>{/* Complex render logic */}</div>;
    });
    ```

    **Use useMemo and useCallback:**

    ```tsx
    import { useMemo, useCallback } from 'react';

    function Component({ items }) {
      // Memoize expensive calculations
      const sortedItems = useMemo(() => {
        return items.sort((a, b) => a.price - b.price);
      }, [items]);

      // Memoize callbacks
      const handleClick = useCallback(() => {
        console.log('Clicked');
      }, []);

      return <List items={sortedItems} onClick={handleClick} />;
    }
    ```

    **Virtualize long lists:**

    ```bash
    npm install react-window
    ```

    ```tsx
    import { FixedSizeList } from 'react-window';

    function VirtualList({ items }) {
      return (
        <FixedSizeList
          height={600}
          width="100%"
          itemCount={items.length}
          itemSize={50}
        >
          {({ index, style }) => (
            <div style={style}>{items[index].name}</div>
          )}
        </FixedSizeList>
      );
    }
    ```

8. **Optimize database queries**

    Improve backend performance.

    **Add database indexes:**

    ```sql
    -- Create index on frequently queried column
    CREATE INDEX idx_users_email ON users(email);

    -- Composite index
    CREATE INDEX idx_orders_user_date ON orders(user_id, created_at DESC);
    ```

    **Optimize N+1 queries:**

    ```python
    # Before (N+1 problem)
    users = User.query.all()
    for user in users:
        print(user.posts)  # Triggers separate query for each user

    # After (use eager loading)
    from sqlalchemy.orm import joinedload

    users = User.query.options(joinedload(User.posts)).all()
    for user in users:
        print(user.posts)  # No additional queries
    ```

    **Add query result caching:**

    ```python
    from flask_caching import Cache

    cache = Cache(config={'CACHE_TYPE': 'redis'})

    @cache.memoize(timeout=300)
    def get_user_data(user_id):
        return User.query.get(user_id)
    ```

9. **Enable compression**

    Compress responses to reduce transfer size.

    **Enable gzip/brotli:**

    ```javascript
    // Express.js
    const compression = require('compression');
    app.use(compression());

    // Next.js (automatic in production)
    // Vercel enables brotli by default
    ```

    **Check compression:**

    ```bash
    curl -H "Accept-Encoding: gzip" -I https://yoursite.com
    ```

10. **Optimize fonts**

    Load fonts efficiently.

    **Use font-display:**

    ```css
    @font-face {
      font-family: 'CustomFont';
      src: url('/fonts/custom.woff2') format('woff2');
      font-display: swap; /* Show fallback font immediately */
    }
    ```

    **Preload critical fonts:**

    ```html
    <link
      rel="preload"
      href="/fonts/custom.woff2"
      as="font"
      type="font/woff2"
      crossorigin
    />
    ```

    **Use system fonts when possible:**

    ```css
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    ```

11. **Implement CDN**

    Use Content Delivery Network for static assets.

    **Popular CDN options:**

    - Cloudflare
    - AWS CloudFront
    - Vercel CDN (automatic with Vercel deployment)
    - Netlify CDN

    **Configure CDN:**

    ```javascript
    // Next.js with CDN
    module.exports = {
      assetPrefix: process.env.NODE_ENV === 'production'
        ? 'https://cdn.example.com'
        : '',
    };
    ```

12. **Measure improvements**

    Run performance audit again and compare.

    // turbo

    ```bash
    npx lighthouse https://localhost:3000 --view --output=html --output-path=./reports/lighthouse-after.html
    ```

    **Create comparison report:**

    ```bash
    # Compare before/after
    echo "Performance Improvements:" > performance-report.md
    echo "FCP: [Before]s → [After]s" >> performance-report.md
    echo "LCP: [Before]s → [After]s" >> performance-report.md
    echo "Bundle Size: [Before]KB → [After]KB" >> performance-report.md
    ```

    **Target improvements:**

    - Core Web Vitals: All green
    - Lighthouse score: > 90
    - Bundle size: Reduced by 30%+
    - Load time: Reduced by 40%+

    **Next Steps:**

    - Setup continuous performance monitoring (Lighthouse CI)
    - Review `agent/rules/091-core-optimization-general.md` for more patterns
    - Consider implementing Progressive Web App (PWA)
    - Setup performance budgets in CI/CD
    - Monitor real user metrics (RUM) with tools like Web Vitals
