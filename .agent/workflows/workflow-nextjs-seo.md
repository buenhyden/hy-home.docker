---
description: Optimize Next.js application for search engines with comprehensive SEO
---

1. **Configure Next.js metadata**

    Setup app-wide metadata in root layout (App Router).

    Create/update `app/layout.tsx`:

    ```typescript
    import type { Metadata } from 'next';

    export const metadata: Metadata = {
      metadataBase: new URL('https://example.com'),
      title: {
        template: '%s | My App',
        default: 'My App - Best Service',
      },
      description: 'Comprehensive description of your app (150-160 characters)',
      keywords: ['next.js', 'react', 'seo', 'web development'],
      authors: [{ name: 'Your Name', url: 'https://example.com' }],
      creator: 'Your Company',
      publisher: 'Your Company',
      robots: {
        index: true,
        follow: true,
        googleBot: {
          index: true,
          follow: true,
          'max-video-preview': -1,
          'max-image-preview': 'large',
          'max-snippet': -1,
        },
      },
      openGraph: {
        type: 'website',
        locale: 'en_US',
        url: 'https://example.com',
        siteName: 'My App',
        title: 'My App - Best Service',
        description: 'Comprehensive description',
        images: [
          {
            url: 'https://example.com/og-image.jpg',
            width: 1200,
            height: 630,
            alt: 'My App Preview',
          },
        ],
      },
      twitter: {
        card: 'summary_large_image',
        site: '@yourusername',
        creator: '@yourusername',
        title: 'My App - Best Service',
        description: 'Comprehensive description',
        images: ['https://example.com/twitter-image.jpg'],
      },
      verification: {
        google: 'your-google-verification-code',
        yandex: 'your-yandex-verification-code',
      },
    };
    ```

2. **Add page-specific metadata**

    Customize metadata for individual pages.

    Create `app/about/page.tsx`:

    ```typescript
    import type { Metadata } from 'next';

    export const metadata: Metadata = {
      title: 'About Us',
      description: 'Learn more about our company and mission',
      openGraph: {
        title: 'About Us | My App',
        description: 'Learn more about our company',
        url: 'https://example.com/about',
        images: [
          {
            url: 'https://example.com/about-og.jpg',
            width: 1200,
            height: 630,
          },
        ],
      },
    };

    export default function AboutPage() {
      return <div>About content</div>;
    }
    ```

3. **Generate dynamic metadata**

    Create metadata from dynamic data (e.g., blog posts, products).

    ```typescript
    import { notFound } from 'next/navigation';

    interface Props {
      params: { id: string };
    }

    export async function generateMetadata({ params }: Props): Promise<Metadata> {
      const product = await fetchProduct(params.id);
      
      if (!product) {
        return {};
      }

      return {
        title: product.name,
        description: product.description,
        openGraph: {
          title: product.name,
          description: product.description,
          images: [{ url: product.image }],
          type: 'website',
        },
      };
    }

    export default async function ProductPage({ params }: Props) {
      const product = await fetchProduct(params.id);
      
      if (!product) {
        notFound();
      }

      return <div>{product.name}</div>;
    }
    ```

4. **Add JSON-LD structured data**

    Implement rich snippets for better search appearance.

    Create `app/products/[id]/page.tsx`:

    ```typescript
    export default function ProductPage({ product }) {
      const jsonLd = {
        '@context': 'https://schema.org',
        '@type': 'Product',
        name: product.name,
        image: product.images,
        description: product.description,
        brand: {
          '@type': 'Brand',
          name: product.brand,
        },
        offers: {
          '@type': 'Offer',
          url: `https://example.com/products/${product.id}`,
          priceCurrency: 'USD',
          price: product.price,
          priceValidUntil: '2024-12-31',
          availability: 'https://schema.org/InStock',
        },
        aggregateRating: {
          '@type': 'AggregateRating',
          ratingValue: product.rating,
          reviewCount: product.reviewCount,
        },
      };

      return (
        <>
          <script
            type="application/ld+json"
            dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
          />
          <div>{/* Product content */}</div>
        </>
      );
    }
    ```

    **Common schema types:**

    - Article (blog posts)
    - Product (e-commerce)
    - Organization
    - LocalBusiness
    - FAQ
    - Breadcrumb

5. **Create sitemap**

    Generate XML sitemap for search engines.

    Create `app/sitemap.ts`:

    ```typescript
    import { MetadataRoute } from 'next';

    export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
      const products = await fetchAllProducts();
      const posts = await fetchAllPosts();

      const productUrls = products.map((product) => ({
        url: `https://example.com/products/${product.id}`,
        lastModified: product.updatedAt,
        changeFrequency: 'weekly' as const,
        priority: 0.8,
      }));

      const postUrls = posts.map((post) => ({
        url: `https://example.com/blog/${post.slug}`,
        lastModified: post.publishedAt,
        changeFrequency: 'monthly' as const,
        priority: 0.7,
      }));

      return [
        {
          url: 'https://example.com',
          lastModified: new Date(),
          changeFrequency: 'daily',
          priority: 1,
        },
        {
          url: 'https://example.com/about',
          lastModified: new Date(),
          changeFrequency: 'monthly',
          priority: 0.5,
        },
        ...productUrls,
        ...postUrls,
      ];
    }
    ```

    Sitemap accessible at: `/sitemap.xml`

6. **Add robots.txt**

    Configure crawler access rules.

    Create `app/robots.ts`:

    ```typescript
    import { MetadataRoute } from 'next';

    export default function robots(): MetadataRoute.Robots {
      return {
        rules: [
          {
            userAgent: '*',
            allow: '/',
            disallow: ['/admin/', '/api/', '/private/'],
          },
          {
            userAgent: 'Googlebot',
            allow: '/',
            disallow: '/admin/',
          },
        ],
        sitemap: 'https://example.com/sitemap.xml',
      };
    }
    ```

    Accessible at: `/robots.txt`

7. **Optimize images for SEO**

    Use Next.js Image component with proper attributes.

    ```tsx
    import Image from 'next/image';

    export default function ProductImage({ product }) {
      return (
        <Image
          src={product.image}
          alt={`${product.name} - High quality ${product.category}`}
          width={800}
          height={600}
          priority={false} // Only true for above-the-fold images
          placeholder="blur"
          blurDataURL={product.blurDataUrl}
          sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
        />
      );
    }
    ```

    **Image SEO checklist:**

    - [ ] Descriptive alt text
    - [ ] Optimized file size (WebP format)
    - [ ] Proper dimensions
    - [ ] Lazy loading for below-fold images
    - [ ] Use descriptive filenames

8. **Implement canonical URLs**

    Prevent duplicate content issues.

    ```typescript
    export const metadata: Metadata = {
      alternates: {
        canonical: 'https://example.com/products/best-product',
      },
    };
    ```

    **For paginated content:**

    ```typescript
    export async function generateMetadata({ searchParams }): Promise<Metadata> {
      const page = searchParams.page || 1;
      
      return {
        alternates: {
          canonical: page === 1 
            ? 'https://example.com/blog'
            : `https://example.com/blog?page=${page}`,
        },
      };
    }
    ```

9. **Add breadcrumbs**

    Improve navigation and SEO with breadcrumbs.

    ```typescript
    export default function ProductPage({ product }) {
      const breadcrumbJsonLd = {
        '@context': 'https://schema.org',
        '@type': 'BreadcrumbList',
        itemListElement: [
          {
            '@type': 'ListItem',
            position: 1,
            name: 'Home',
            item: 'https://example.com',
          },
          {
            '@type': 'ListItem',
            position: 2,
            name: product.category,
            item: `https://example.com/${product.category}`,
          },
          {
            '@type': 'ListItem',
            position: 3,
            name: product.name,
            item: `https://example.com/products/${product.id}`,
          },
        ],
      };

      return (
        <>
          <script
            type="application/ld+json"
            dangerouslySetInnerHTML={{ __html: JSON.stringify(breadcrumbJsonLd) }}
          />
          <nav aria-label="Breadcrumb">
            <ol>
              <li><a href="/">Home</a></li>
              <li><a href={`/${product.category}`}>{product.category}</a></li>
              <li aria-current="page">{product.name}</li>
            </ol>
          </nav>
        </>
      );
    }
    ```

10. **Optimize page speed**

    Improve Core Web Vitals for better rankings.

    **Measures:**

    - Use Next.js Image component
    - Implement lazy loading
    - Reduce JavaScript bundle size
    - Enable compression (automatic in Next.js)
    - Use CDN (Vercel CDN automatic)

    // turbo
    **Run Lighthouse:**

    ```bash
    npx lighthouse https://your-site.com --view
    ```

    **Targets:**

    - LCP (Largest Contentful Paint): < 2.5s
    - FID (First Input Delay): < 100ms
    - CLS (Cumulative Layout Shift): < 0.1

11. **Add internationalization (i18n)**

    Support multiple languages with proper hreflang tags.

    Configure `next.config.js`:

    ```javascript
    module.exports = {
      i18n: {
        locales: ['en', 'es', 'fr'],
        defaultLocale: 'en',
      },
    };
    ```

    Add hreflang in metadata:

    ```typescript
    export const metadata: Metadata = {
      alternates: {
        languages: {
          'en': 'https://example.com/en',
          'es': 'https://example.com/es',
          'fr': 'https://example.com/fr',
        },
      },
    };
    ```

12. **Verify and monitor SEO**

    Test and track SEO performance.

    **Verification:**

    - Google Search Console: Submit sitemap
    - Bing Webmaster Tools: Submit sitemap
    - Test rich snippets: <https://search.google.com/test/rich-results>

    **Monitoring:**

    ```bash
    # Check page indexing
    curl -I https://your-site.com

    # Check robots.txt
    curl https://your-site.com/robots.txt

    # Check sitemap
    curl https://your-site.com/sitemap.xml
    ```

    **Tools:**

    - Google Analytics 4
    - Google Search Console
    - Ahrefs / SEMrush
    - PageSpeed Insights
