# Asset Licenses

| Asset | Source | License / right to use | Attribution | Use | Optimization |
|---|---|---|---|---|---|
| ARVI photographs (boutiques, cellar, services, campaign) | arvi.ch and ARVI's own Shopify Files | **Client-owned** (ARVI's own published brand assets). ⚠ ARVI should confirm it holds the photographers' rights for web use, which is standard for commissioned work | None | Hero, heritage, boutiques, services | WebP q78, 2–4 responsive widths, `srcset` and `sizes`, lazy below the fold, `fetchpriority=high` on the hero |
| ARVI logo | ARVI Shopify Files | Client-owned trademark | — | Header, age gate | Shopify CDN `image_url` |
| Product bottle photos | ARVI Shopify catalogue | Client-owned or supplier-provided (as already used on arvi.ch) | — | Cards, product page | Shopify CDN responsive images |
| Newsreader typeface | github.com/productiontype/Newsreader via Google Fonts | SIL Open Font License 1.1 (commercial use, embedding and self-hosting allowed) | Not required; the licence text travels with redistributed font files | Display type | woff2, unicode-range subsets, `font-display: swap`, latin roman preloaded |
| Inter typeface | Shopify font library | Licensed by Shopify for themes | — | UI and body | Shopify font CDN |
| Lucide icons | lucide-static 0.460.0 (unpkg) | ISC License (commercial use allowed); portions MIT (Feather) | Keep the copyright notice with redistributed source (`assets-library/icons/LICENSE-lucide.txt`) | Boutique facts, values, PDP accordions | Inline SVG, 1.25 stroke |
| `arvi-variant-formato.js` | ARVI WIP theme (myarvi.myshopify.com) | Client-owned code (commissioned for ARVI) | — | Size/packaging selectors | Unchanged; source-map comment removed |

## External stock imagery
**None used.** Automated access to Unsplash returned HTTP 403, and Google Images results are not licensed for reuse, so no third-party photograph appears in the theme or presentation. If ARVI wants additional editorial imagery, commission original photography of the boutiques and cellar (recommended) or license it through an account the client controls. Then record each item in this table.

No watermarked, AI-generated or fictitious product imagery is used anywhere.
