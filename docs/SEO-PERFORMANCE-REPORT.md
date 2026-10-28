# SEO, AEO and Performance Report

## Implemented
**Semantics**
- One descriptive H1 per page. The homepage H1 is "Your Premium Wine Shop in Switzerland", the visible hero eyebrow (ARVI's existing H1 copy), while the campaign headline is an H2. Dawn's logo H1 is now an opt-in setting (`Theme settings › ARVI › Logo is the homepage H1`).
- Logical heading order in all ARVI sections. Product cards are H3 under section H2s, fixing arvi.ch's 50+ H2s.
- Breadcrumb navigation (`<nav aria-label>` + `<ol>`) on product, collection and page templates.
- Every image has alt text; decorative bottle tiles use `alt=""`. Boutique and service alt texts describe the real scenes.

**Structured data (all based on visible, verified content)**
| Type | Where | Source |
|---|---|---|
| Product + Offer (per variant, CHF, availability) | Product pages | Dawn's native `product \| structured_data` |
| Organization + WebSite/SearchAction | Header (homepage) | Dawn native |
| BreadcrumbList | Product, collection, page | `sections/arvi-breadcrumbs.liquid` |
| FAQPage (16 Q&As) | FAQ page only | `sections/arvi-faq.liquid`; answers are ARVI's own FAQ text |
| LiquorStore × 3 (address, phone, email, opening hours, CHF) | Boutiques page only (disabled on the homepage to avoid duplicates) | `sections/arvi-boutiques.liquid` |

No reviews, ratings or invented FAQ schema were added.

**AEO**
The facts that answer engines quote are presented as structured, visible text: vintage, producer, origin, colour, alcohol, formats and critic scores (with source) on each product. Store addresses and hours are in definition lists. The FAQ is real Q&A content, and the cellar, provenance and storage claims use ARVI's own wording.

**Technical**
Dawn's canonical, hreflang (provided by Shopify for it/de/fr/en), robots and sitemap handling are unchanged. Crawlers bypass the age gate through a user-agent allow-list, and its content is `data-nosnippet`.

## Required at launch (not done: needs store access or a merchant decision)
1. **301 redirects.** arvi.ch URLs (`/en/{producer}/{wine}/{vintage}/{size}`, `/en/wines/france/bordeaux`, `/en/shops`, …) must map to Shopify (`/products/{handle}`, `/collections/bordeaux`, `/pages/i-nostri-negozi`). Export the arvi.ch sitemap (`/sitemap.xml`) and bulk-import redirects in Shopify (Online Store › Navigation › URL redirects). The SKU in the old URL and the Shopify `sku` field allow an automated product mapping.
2. **Meta descriptions** for collections and pages in Shopify's SEO fields. The current arvi.ch description claims "over 5,000" wines while the About page says 10,000+ labels; ARVI must confirm the figure.
3. **Collection descriptions** (region and producer intros) improve both SEO and the editorial headers. Most WIP collections are currently empty.
4. Confirm the market and language URL structure (it at `/`, `/de`, `/fr`, `/en`) and the primary domain `arvi.ch`.

## Performance
**Approach:** Dawn's HTML-first architecture is kept and no framework was added. ARVI JavaScript totals about 7 KB across 3 small deferred files, plus the WIP's unchanged 7 KB format script on product pages. CSS is 2 files (≈28 KB + 20 KB uncompressed). The editorial serif is self-hosted (one 129 KB latin file preloaded; the italic loads only where used). The hero uses `fetchpriority=high` with eager loading; everything else is lazy and uses responsive `srcset`. Every image has explicit dimensions, and there is no autoplay video, parallax or carousel library.

**Fixes made from measurement:** the age-gate logo had no height, which caused CLS 0.089 on every page (now 0.000). The age-gate backdrop blur cost heavy main-thread time on throttled mobile (removed). Card format labels are computed in Liquid rather than JS.

**Lighthouse 12.2.1 on the local preview harness** (`presentation/lighthouse/`, first visit with the age gate showing):
| Page | Desktop perf / A11y / BP / SEO | Desktop LCP · CLS · TBT | Mobile perf (3 runs) | Mobile median LCP · CLS · TBT |
|---|---|---|---|---|
| Home | 98 / 100 / 96 / 100 | 1.0 s · 0.006 · 0 ms | 71, 74, 79 | 3.7 s · 0.000 · 580 ms |
| Product (Salon 1999) | 97 / 100 / 96 / 100 | 1.2 s · 0.025 · 20 ms | 73, 77, 80 | 4.4 s · 0.000 · 309 ms |
| Collection (Champagne) | 97 / 100 / 96 / 100 | 1.1 s · 0.005 · 40 ms | 61, 64, 64 | 4.4 s · 0.000 · 855 ms |

Best Practices is 96 because Lighthouse flags the HTTP (non-HTTPS) localhost origin.

**Interpretation:**
- The harness is slower than Shopify. Its server response time is 300–750 ms (LiquidJS rendering on a 2019 Intel Mac, no edge cache), there is no HTTP/2, and images come from a cold CDN. Lighthouse also ran on the same machine as the render server.
- Even so, these are lab numbers. **I make no claim that the CWV targets are met.** Mobile LCP (≤ 2.5 s) is not demonstrated here. Re-run Lighthouse and PageSpeed Insights on the unpublished Shopify theme, then watch field data (CrUX / Shopify Web Performance dashboard) after launch.
- Likely next steps if mobile LCP stays above 2.5 s on Shopify: serve a dedicated 4:5 mobile hero (the `image_mobile` setting exists), drop the hero's 1.6 s settle animation, reduce collection page size from 24 to 16, and audit app scripts, which typically dominate TBT on live stores.
