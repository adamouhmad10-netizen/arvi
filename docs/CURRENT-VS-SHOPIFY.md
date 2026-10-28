# arvi.ch (production) vs myarvi.myshopify.com (WIP)

| Area | arvi.ch | Shopify WIP | Assessment / action in new theme |
|---|---|---|---|
| Platform | nopCommerce, custom plugins | Dawn 16.0.0 ("ARVI tema dawn") | ✅ The correct foundation. The new theme is built on the **same Dawn version**, so WIP custom files can be merged 1:1 |
| Languages | EN/IT/DE/FR | IT default + DE/FR/EN | ✅ Keep. All new strings live in locale files or editable settings |
| Age gate | jQuery modal, localStorage | `<dialog>`, cookie `arvi_age_ok`, crawler bypass | ✅ Reimplemented as `arvi-age-gate` section using the **same cookie name**, so verified visitors are not re-asked after the switch |
| Header | Logo + pill search + 7 caps links | Dawn inline menu + dropdowns, IT labels | ⚠ Generic. → New two-tier header: centred logo, editorial mega menu with an image card, refined drawer on mobile |
| Hero | Seasonal campaign ("Hidden Treasures of Autumn") | Same image, Dawn banner, "Shop all" | ⚠ Keep the campaign but art-direct it as an editorial split hero with separate desktop and mobile images |
| Product cards | Grey box, score badge, wishlist, cart icon | Pinkish grey, red serif title, **stray "75.00"** | ❌ Bug. → New card: producer → wine → vintage/format line, CHF price, sold-out state, no raw option values |
| Critic scores | On card & PDP | PDP only (`arvi-vintage`) | ✅ Kept on the PDP (block reads a metafield via dynamic source) |
| Vintages | "All vintages" chips | `arvi-vintage-grid` | ✅ Merge the WIP section as is (Liquid not available to me) and restyle via `.arvi-vintage*` classes in the new CSS |
| Format/packaging | Two selects (size, format) | `arvi-variant-formato.js` splits Formato | ✅ Kept: asset reused unchanged (client-owned), styled by the new theme |
| Request price | – | **Missing**. Many variants are €0 / unavailable | ➕ New: when price = 0 or the product is tagged `request-price`, the price is replaced by "Price on request" and an enquiry button (mailto/contact form with the product prefilled) |
| Homepage narrative | 4 carousels, clip-art icons | Default Dawn order, **placeholder "Colonna" copy live** | ❌ → New 10-section editorial narrative |
| Boutiques | Rich page, small photos | Page exists (`i-nostri-negozi`) | ➕ New `arvi-boutiques` section with real addresses/hours as editable blocks, plus LocalBusiness/WineStore schema (opt-in per block) |
| Services | Vault, Horeca, Events, EP | Pages exist | ➕ Featured in the homepage "Services" editorial |
| Filters | Category tree | Native: cl, vintage, region, colour, producer | ✅ Keep native filters. Restyled as a calm left rail (desktop) and drawer (mobile) |
| Footer | Rich, 6 columns | 2 menus, "Powered by Shopify" | ⚠ → New footer: newsletter, 4 menus, boutiques, legal line, 18+ notice, payment icons |
| SEO | Single H1, many H2 on cards, keyword stuffing | Dawn defaults + breadcrumb JSON-LD | ➕ Card titles demoted to H3. Product JSON-LD extended (brand, sku, offers per variant). WineStore/Organization data. FAQPage only on the FAQ template |
| URL structure | `/en/{producer}/{wine}/{vintage}/{size}` | Shopify `/products/{handle}` | ⚠ **301 redirect map required** at launch (see SEO report) |

## What already works in the WIP
Real catalogue import (19k products) with consistent handles. `arvi.*` metafields with native filters. Translated menus. Breadcrumb section and schema. Age gate. Format/packaging split. Vintage grid. Discount display.

## What keeps it from feeling premium
1. Untouched Dawn spacing, type scale and section order.
2. Placeholder copy in production sections.
3. A pinkish product background that fights the grey PNG backgrounds of the bottle photos.
4. Burgundy (`#6b1a1d`) used on every title, which ARVI's own palette doesn't do; theirs is warm stone and bronze.
5. A raw "75.00" option value leaking into cards.
6. Minimal footer and "Powered by Shopify".
7. No boutique, service or heritage storytelling.

## Must be preserved for compatibility
Dawn 16 `product-info` custom element contract (used by `arvi-variant-formato.js`), `variant-selects` markup, `PUB_SUB_EVENTS.variantChange` (used by `arvi-sconto.js`), the `arvi_age_ok` cookie, the `arvi.*` metafield namespace, existing collection/page handles, locale coverage (it/de/fr/en), and Search & Discovery filters.
