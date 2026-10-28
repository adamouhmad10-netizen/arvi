# Refinement pass (v2) — implemented changes, tests, limitations

Date: 28 Oct 2026. Base: Dawn 16.0.0 (`7097aaf`). Nothing was uploaded to Shopify; the live theme was not touched.
Screenshots: `presentation/screens/before/` (audit state) and `presentation/screens/after/` (this pass), full page, 1440 and 390 px.

## Changes

| # | Area | Change | Files |
|---|---|---|---|
| 1 | Product cards | Wines without a photo get a designed stand-in (Champagne or still-wine bottle silhouette, "Photograph to follow") on the same stone ground, in the same 4:5 frame; the title stays below the image like every other card. Toggle: Theme settings › ARVI › *Designed placeholder*. | `snippets/arvi-card-fallback.liquid` (new), `snippets/card-product.liquid` (guarded `arvi_fallback` branch), `config/settings_schema.json` |
| 2 | Product cards | Titles reserve two lines so format and price rows align (never truncated); price 15 px / 500; sold-out label is a quiet tag instead of a boxed sticker; no stacked quick-add buttons on touch screens. | `assets/arvi-base.css` |
| 3 | Images | Bottles were clipped on mobile product pages: the padded image used Dawn's `content-box` and overflowed its frame. Now `border-box` for product and card images; larger desktop/mobile bottle. | `assets/arvi-base.css` |
| 4 | Vintages | Dashed boxes replaced by an editorial year index: serif year, status line (Available · Sold out · Viewing), bronze rule on the current year, hairline draw on hover. Full-width layout when there is no critic/producer text. | `snippets/arvi-sibling-vintages.liquid`, `sections/arvi-wine-profile.liquid`, CSS |
| 5 | Recommendations | One card per wine (deduped in Liquid by producer + title without vintage); other vintages of the viewed wine removed client-side (they are already in the vintage index); section hides if nothing distinct remains. | `snippets/arvi-wine-key.liquid` (new), `sections/related-products.liquid`, `assets/arvi-product.js` |
| 6 | Labels | Option name "Formato" shown in the visitor's language (Size · Formato · Grösse · Format); option values sent to the cart are unchanged. | `snippets/arvi-option-label.liquid` (new), `snippets/product-variant-picker.liquid`, locales |
| 7 | Critic data | The preview no longer injects critic scores (they were scraped from the WIP storefront and bound by simulation, not by the theme). Critic blocks render only when connected to real metafields. Presentation copy and screenshots updated. | `preview/server.mjs` (`PREVIEW_SIMULATE_CRITICS=1` to re-enable for layout checks), `presentation/site/` |
| 8 | Price on request | The extra "Sold out" badge beside "Price on request" is hidden (one message, one action). | CSS |
| 9 | Payments | Footer row uses Shopify's own payment SVGs via `shop.enabled_payment_types` (unchanged Dawn logic), sized 42×27 at native 38:24, never recoloured. Preview list limited to methods verified in ARVI's FAQ (Visa, Mastercard). | `assets/arvi-base.css`, `preview/payment-icons/` (MIT, Shopify Inc.) |
| 10 | Header | Announcement on one line (desktop) and balanced over two lines (mobile). Empty-cart "0" bubble was a preview bug (fixed in the harness; Dawn already hides it). | CSS, `preview/data.mjs` |
| 11 | Hero | Text centred in its panel; mobile crop is a theme-editor setting (*Mobile crop: horizontal focus*), set so the bottle stays in frame; square mobile image. | `sections/arvi-hero.liquid`, CSS, `templates/index.json` |
| 12 | Regions | Tuscany tile (31 references, looked like an error) replaced by Italy (7,042); Burgundy bottle with a baked-in line replaced by a clean Remoissenet packshot. | `templates/index.json` |
| 13 | Cellar story | Industrial warehouse photo replaced by ARVI's own laid-down bottles photo (`AS_01.png`), shown portrait at native resolution; unverifiable "Melano" caption removed. Chairman's quote centred with attribution beneath. | `templates/index.json`, CSS |
| 14 | Boutiques | Offset middle column removed; card links aligned at the foot; repeated values block disabled on the boutiques page (re-enable in the editor). | CSS, `templates/page.boutiques.json` |
| 15 | Mobile | Section padding tightened; boutiques, services and the featured selection become scroll-snap rails with a peek of the next card; values become a 2×2 grid; footer menus side by side, left-aligned bottom bar. Homepage 13,133 → 9,661 px (−26%); boutiques page 6,339 → 2,872 px. | CSS |
| 16 | Collections & search | Collection title left-aligned on mobile with an inset hairline; product counts formatted (1,742); search title in the display serif; hidden H2 restores the heading outline; 44 px sort control. | CSS, `assets/arvi.js`, `sections/main-search.liquid` |
| 17 | Details | Body copy 82% ink (was 75%); button press feedback and focus rings (reduced-motion aware); "Powered by Shopify" behind a setting (off). | CSS, `sections/footer.liquid`, settings |

## Tests (executed on the local preview, 28 Oct 2026)

| Test | Result |
|---|---|
| Shopify Theme Check (`shopify theme check`) | 0 errors, 14 warnings (unchanged: upstream Dawn + 3 ARVI snippets rendered from Custom Liquid blocks) |
| axe-core, 7 pages × 1440/390 | 0 violations in 14/14 |
| Responsive, 7 pages × 375/390/768/1024/1440/1920 | 0 px horizontal overflow, one H1, no missing alt, no heading skips in 42/42 |
| Interactions (`scripts/qa_interactions.py`) | 14/14 pass: Size label, add-to-cart request (variant + quantity), cart drawer opens, vintage states, no critic data, deduped recommendations, price-on-request state, fallback card, mega menu, mobile drawer, mobile account access, mobile rail |
| Visual review | Every page inspected at 1440 and 390 after each change; defects found and fixed in-loop (fallback centring, collection alignment, footer grid specificity, mobile account icon) |

## What was not tested, and why
- **Cart and checkout on Shopify.** No store access. The cart test intercepts `/cart/add` in the browser: it proves the theme posts the right variant and quantity and opens the drawer, not that Shopify's cart, checkout or payments work.
- **Filtering, sorting, predictive search** need Shopify's backend.
- **Real recommendations.** Shopify's algorithm runs server-side; the preview approximates it. The dedupe logic is theme-side and will apply to whatever Shopify returns.
- **Lighthouse** was not re-run in this pass (no new scripts or images above the fold; one extra small script block on the product page).

## Remaining limitations
- Payment logos show what Shopify reports as enabled. American Express, TWINT and Apple Pay are **not** verified for ARVI; they appear automatically only if enabled in Shopify Payments.
- Search shows sold-out wines first: set *Search & Discovery › Sold-out products: show last* in the admin (not a theme setting).
- Size filter order (4 cl, 7 cl first) comes from the store's filter configuration.
- Boutique photos remain 660 px originals; new photography is still recommended.
- `emilkowalski/skills` and `Leonxlnx/taste-skill` are not installed in this environment and were not applied.
