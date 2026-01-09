---
trigger: always_on
glob: "**/*.{tsx,jsx,vue,html}"
description: "SEO: Metadata, Open Graph, and Structured Data."
---
# SEO Standards

## 1. Metadata

- **Titles**: Unique `title` for every page. Pattern: `Page Name | Brand`.
- **Description**: 150-160 chars. Action-oriented.
- **Open Graph**: Always includes `og:image`, `og:title`, `og:description` for social sharing.

### Example: Next.js Metadata

**Good**

```typescript
export const metadata = {
  title: 'Pricing | MyApp',
  description: 'Simple pricing for teams.',
  openGraph: { images: ['/og-pricing.png'] }
}
```

**Bad**

```typescript
// Missing critical tags
export const metadata = { title: 'Pricing' }
```

## 2. Content Structure

- **H1**: EXACTLY ONE `<h1>` per page.
- **Links**: Use `<a>` tags with `href` for internal navigation (allows crawling). Buttons are for actions, Links are for destinations.

### Example: Links

**Good**

```jsx
<Link href="/about">About Us</Link>
```

**Bad**

```jsx
<button onClick={() => router.push('/about')}>About Us</button>
```

## 3. Performance Core Web Vitals

- **Images**: Use explicit `width`/`height` to prevent Layout Shift (CLS).
- **LCP**: Prioritize loading of the main hero image (e.g., `priority` prop in Next.js).

### Example: Images

**Good**

```jsx
<Image src="/hero.jpg" width={800} height={400} alt="Hero" priority />
```

**Bad**

```jsx
<img src="/hero.jpg" /> // Slow LCP, High CLS
```
