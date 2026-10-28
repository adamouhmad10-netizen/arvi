# Remaining Requirements & Decisions

## Access needed
- [ ] **Shopify staff/collaborator access** (or a Theme Access password) to upload the unpublished theme, run `shopify theme dev`, read the WIP theme's Liquid, apps and metafield definitions, and test cart, checkout and filters end-to-end.
- [ ] **Metafield definitions** for alcohol, sub-region, country, grapes and critic scores. The theme assumes `arvi.alcol`, `arvi.sottoregione`, `arvi.nazione` and `arvi.uvaggio`; `annata`, `colore`, `regione` and `produttore` are confirmed. Adjust `snippets/arvi-wine-facts.liquid` if the keys differ.

## Merchant decisions
- [ ] **Price on request policy:** should zero-priced *sold-out* wines show "Price on request" with an enquiry button (current behaviour), or simply "Sold out"? Should enquiries go by email (default info@arvi.ch) or to a contact form page?
- [ ] **Zero-priced variants must not be purchasable.** The theme hides Add to cart, but quick-add and the cart API do not check price. Make sure CHF 0.00 variants are unavailable in inventory, or set a real price.
- [ ] **Catalogue size claim:** "over 5,000" (arvi.ch meta) or "10,000+ labels" (About page). The theme uses 10,000+.
- [ ] **Hero campaign:** keep the seasonal Autumn campaign, or use a permanent brand image (needs high-resolution photography).
- [ ] Footer menus `footer-wines` / `footer`, and whether to show "Powered by Shopify" (edit in *Edit default theme content*).
- [ ] Legal review of the age-gate wording (18+), and of whether spirits require 18+ while wine and beer could be 16+ under Swiss law. The current gate uses 18+ for the whole site, matching the WIP.

## Content and assets
- [ ] **High-resolution boutique photography** (≥ 2000 px). The current originals are 660 px.
- [ ] Product photos for products without images (≈16% of the sampled catalogue), and vintage-specific labels where one photo is reused.
- [ ] Collection and producer descriptions and SEO meta descriptions.
- [ ] Translations of section content (hero, values, boutique notes, FAQ) into IT, DE and FR via Translate & Adapt. Theme strings are already translated.
- [ ] The **Tuscany** collection (`toscana`) contains only 31 products in the WIP store, while arvi.ch lists Tuscany as a main region. Check the collection conditions.
- [ ] Rights confirmation for ARVI's own photography (see ASSET-LICENSES.md).

## Integrations not validated
Cart and checkout, payment methods (TWINT etc.), customer accounts, Search & Discovery filters and predictive search, product recommendations, analytics and consent banner, the WIP discount display (`arvi-sconto.js`, Storefront API token), any installed apps, markets and currency, and language switching.

## Launch tasks
- [ ] 301 redirect map from arvi.ch URLs (SEO-PERFORMANCE-REPORT.md).
- [ ] Lighthouse/PageSpeed on the Shopify-hosted theme (confirm mobile LCP ≤ 2.5 s), then field CWV monitoring.
- [ ] A screen-reader pass (VoiceOver/NVDA) on the Shopify-hosted theme, including the cart drawer and checkout handoff.

## Not available in this environment
The skill packs named in the brief (`emilkowalski/skills`, `Leonxlnx/taste-skill`) are **not installed**, so they were not applied.
