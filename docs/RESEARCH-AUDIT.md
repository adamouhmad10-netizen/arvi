# ARVI — Research Audit

_Researched 28 Oct 2026. I captured every page below with a rendered Playwright browser (Chromium) at 1440×900 and 390×844. Screenshots are in `research/screens/`. Raw extracted text, metadata and image inventories are in `research/raw/` (that folder is git-ignored because it holds third-party HTML)._

## 1. Sources reviewed

| Source | Access | Pages rendered |
|---|---|---|
| **A. arvi.ch** (production, nopCommerce) | Public. Age gate bypassed after reading its script (`localStorage/cookie ageVerified=true`) | Home, Shops, About, FAQ (all 16 answers), Contact, Champagne category, Iconic wines, Krug producer page, 2 product pages (Krug Grande Cuvée 173ème, Latour 1964), Wine Vault, Horeca, Events, Arvi Green, En Primeur, Accessories (partly: some pages timed out on `networkidle`, so I relied on the screenshots I got before the timeout) |
| **B. arvi.ch/en/shops** | Public | Full page with all three boutiques (text, hours, access, photography) |
| **C. myarvi.myshopify.com** (Shopify WIP) | Storefront preview password, entered through the normal `/password` form (it never appears in screenshots, logs or committed files) | Home, `/collections`, `/collections/all`, `/collections/champagne`, search, 2 product pages, contact, shops, about, wine vault, events; public JSON endpoints (`products.json`, `collections.json` × 7 pages, `.js` product), sitemap, robots |
| Shopify admin | **Not available** | I could not read the WIP theme's Liquid source, apps or metafield definitions. Everything about them below is inferred from rendered HTML and public assets. |

## 2. Brand identity (source of truth: arvi.ch)

- **Name/legal:** ARVI SA, Via Pedemonte di Sopra 1, 6818 Melano, Switzerland. Tel +41 91 649 68 88, info@arvi.ch.
- **Positioning (verbatim, About):** "With more than thirty years of experience, we are one of the main dealers of fine and rare wines in Switzerland." It holds more than 10,000 labels in its own cellars, with large formats "from the 150 cl Magnum to 27 litre formats". Its stated values are "Trust, passion, expertise, respect".
- **Chairman quote:** Paolo Cattaneo. "Everything we do, we do because we love wine…"
- **Logo:** a hand-drawn ink sketch of a figure over the Roman-capital wordmark **ARVI**. It is monochrome black, with a white version available on Shopify (`logoarvi.jpg` and `logoarvi_white.png`, 3171×3525). A traced SVG exists (`safari-pinned-tab.svg`, potrace). The logo must not be redrawn.
- **Typography (production CSS):** **Minion Pro** (serif headings: "minion", "minion bold", "minion italic") and **Helvetica Neue LT Std Light/Extended** (UI and body). Lato is loaded but barely used.
- **Colour tokens (production CSS):**
  `--main-gold-color #998a65` (bronze/olive gold, used for CTAs) · `--main-lightgold-color #ebe7dd` · `--secondary-gold-color #d6d0c1` · `--secondary-lightgold-color #f5f4f0` · `--main-gray-color #cec8b6` · `--secondary-black-color #2b2b2b` · black/white · seasonal `--main-christmas-color #8a0707`.
  This is a **warm-stone and bronze** palette, not burgundy and gold.
- **Tone of voice:** service-oriented, factual and warm ("impeccable service and passion for wine"). Superlatives are used sparingly.
- **Languages/currency:** production runs EN/IT/DE/FR, CHF, with a "Tax incl." switch. Shopify runs IT (default) plus DE, FR and EN through `hreflang` and subfolders (`/de`, `/fr`, `/en`), in CHF.

## 3. Production site findings (arvi.ch)

**Homepage order:** utility bar (Tax/CHF/EN) → logo + pill search + account/wishlist/cart → text mega-nav (WINES, EN PRIMEUR, SHOPS, OUR SERVICES, EVENTS, ABOUT, CONTACT US) → H1 "Your Premium Wine Shop in Switzerland" → seasonal hero ("Hidden Treasures of Autumn") → *Prestigious Champagne Selection* carousel → 3 producer tiles (Pontet-Canet, Chavy-Chouet, Pavie) → *Iconic Fine Wines* carousel → Wine Vault split banner → *Limited Edition Gift Selections* carousel → *Discover our shops* (3 tiles) → *Why buy from us* (4 beige cards with clip-art icons) → contact strip → black footer.

**Strengths to keep:** a deep, real catalogue (rare vintages back to 1959, large formats, OWC cases). Critic scores sit on cards (RP, WS, VI…). Long producer and critic texts sit on product pages. The three boutiques are real and distinctive. The FAQ is substantive and genuinely useful for AEO. The physical services (Wine Vault, Horeca, Events, En Primeur) set ARVI apart.

**What makes it feel "basic":**
1. The visual language is template-like: four carousels in a row on one homepage, with equal-weight sections and no narrative.
2. The icons are cartoon clip-art (truck, waiter, rosette), which clashes with the ink-sketch logo.
3. Product tiles sit on grey boxes with tiny type, and the price is not related to the vintage or format hierarchy.
4. The boutique photography is excellent but shown as small 660px squares.
5. Brand typography (Minion) only appears in headings. The UI is mixed Helvetica/Lato in caps.
6. The PDP has a large empty right column, long critic notes in 11px serif, and an illustrative-image disclaimer under the gallery.
7. The meta keywords tag is stuffed. The SEO description claims "over 5,000" wines, while About says "over 10 thousand labels". **This needs merchant confirmation.**

**SEO structure:** a single H1 on the homepage. Each product card uses an H2, giving 50+ H2s. URLs follow `/en/{producer}/{wine}/{vintage}/{size}` and use accented characters. `nopCommerce` is the generator. I found no Product JSON-LD in the rendered home or category pages.

## 4. Physical boutiques (arvi.ch/shops)

| | Melano (HQ) | Lugano | Zurich |
|---|---|---|---|
| Address | Via Pedemonte di Sopra 1, 6818 Melano | Via Emilio Bossi 1, 6900 Lugano | Sankt Annagasse 9, 8001 Zurich |
| Phone / email | +41 91 649 68 88 · arvino.melano@arvi.ch | +41 91 924 94 88 · arvino.lugano@arvi.ch | +41 43 810 08 88 · arvino.zurich@arvi.ch |
| Hours | Mon–Fri 8.30–12.30 / 13.00–18.00 | Tue–Sat 10.00–19.00 | Mon–Sat 10.00–18.00 |
| Character | Cellar in the same building, 10,000+ labels | Sommeliers, open tastings | Events for up to 40 standing / 18 seated |

**Visual language of the stores** (from `Melano.png`, `Lugano.png`, `Zurigo.png`, `Events_*.png` and `Shops_01.png`):
- **Materials:** pale natural oak floors and long tables, slatted oak wall cladding, white-oak cubby walls for bottles, black lacquer and black leather (Le Corbusier-style club chairs in Lugano), and oak barrels used as display tables.
- **Light:** warm 2700K downlights. Each niche is backlit, so every bottle reads as an object. Zurich has **brass/gold dome pendants**, its one metallic accent. Ceilings are a dark warm grey.
- **Merchandising:** dense yet ordered grids, with one hero bottle per lit niche. Cases sit in lower drawers.
- **Atmosphere:** a calm, architectural, warm-neutral setting where precision meets craft. **It is not dark, moody or baroque.** It is a light-oak gallery with black and brass punctuation.

This is the strongest design input. The digital store should feel like walking along that oak wall: generous light surfaces, precise grid, objects lit individually, black for authority, and bronze used sparingly.

## 5. Shopify WIP (myarvi.myshopify.com)

- **Theme:** "ARVI tema dawn", `schema_name: Dawn`, **`schema_version: 16.0.0`**, role `main` on the dev store. This matches the upstream Dawn I vendored (v16.0.0, released 10 Aug 2026).
- **Catalogue:** **19,023 products** and **1,750 collections**, using producer collections (`produttore-*`), region collections (`regione-*`, plus clean handles like `champagne`, `bordeaux`, `burgundy`, `piemonte`, `toscana`) and country collections (`nazione-*`, `italy`, `france`). Real handles used in menus include `best-sellers`, `gift-ideas`, `en-primeur`, `accessories`, `spirits`, `red-wines`, `white-wines`, `sparkling-wines`, `sweet-wines`, `rose-wines` and `switzerland`.
- **Product model:** `vendor` = producer. A single option **"Formato"** holds values such as `75.00`, `150.00` and `OWC 6 × 75.00` (size in cl, optionally an original wooden case). `body_html` is empty. Rich data lives in **metafields under the `arvi` namespace**, confirmed through storefront filter params: `arvi.annata` (vintage), `arvi.colore`, `arvi.regione`, `arvi.produttore`, plus the variant option filter `formato`. The PDP shows further fields (alcohol, sub-region, critic scores and reviews) whose metafield keys I could not see.
- **Price model:** unavailable variants commonly have `price 0.00`. 416 of 470 variants in the 250-product sample are unavailable. **"Request price" is not implemented** in the WIP theme.
- **Custom features already built (must be preserved):**
  - `arvi_age_gate` section with a native `<dialog>`, cookie `arvi_age_ok` (90 days, `Domain=arvi.ch`), a crawler allow-list, and IT copy "Hai almeno 18 anni?".
  - `arvi-variant-formato.js`: splits "Formato" into **Size** and **Packaging** (single bottle or OWC case) selects, hooking `product-info.addPreProcessCallback`.
  - `arvi-vintage-grid`: "Tutte le annate", links to sibling vintages with unavailable/selected states.
  - `arvi-vintage`: "Il vino" spec list and **critic scores** ("Robert Parker / Wine Advocate 95" plus the review).
  - `arvi-breadcrumb`: visible breadcrumb plus `BreadcrumbList` JSON-LD.
  - `arvi-sconto.js`: shows automatic-discount prices through the Storefront API `cartCreate`.
  - `arvi-prezzo-titolo.js`: mirrors the price next to the title.
  - `cart-disclosure-modal.js` / `-tooltip.js` and a `disclosures` section.
  - Native filters: Contenuto (cl), Annata, Regione, Colore, Produttore.
- **Design state:** Inter + Cormorant Garamond, with a burgundy accent (`#6b1a1d`-ish) on a pinkish-grey product background. The default Dawn section order remains, and placeholder copy is still live ("Colonna – Associa un testo a un'immagine…"). Cards show a stray **"75.00"** on sold-out products (raw option value). The footer is minimal (one "Vini" link), and "Powered by Shopify" is visible.

See `CURRENT-VS-SHOPIFY.md` for the gap analysis.

## 6. Benchmark research (design principles, not layouts to copy)

I reviewed the composition patterns of established fine-wine merchants and Champagne houses. I used no assets from them.
- **What reads as premium:** restraint in the number of sections, one idea per screen, a large serif set at light weight with tight leading, small tracked uppercase labels, product shots on a consistent neutral ground with generous padding, prices stated plainly, and imagery that is real (cellars, people, places) rather than staged lifestyle.
- **What reads as cliché:** gold everywhere, black-on-black "luxury" with low contrast, script fonts, autoplay video heroes, parallax, endless carousels, and rating stars.
- **Applicable to ARVI:** treat the product grid like the lit oak niches (one bottle per cell, the label always legible), state provenance and storage facts (a real differentiator), show critic scores as typographic data, and make the boutiques and services part of the commerce journey.

## 7. Skill packs requested in the brief

The brief asks me to apply `emilkowalski/skills` and `Leonxlnx/taste-skill`. **Neither is installed in this environment.** I checked `~/.claude/skills` and the plugin registry and found no matching packs, so neither was applied. I followed established practice instead: restrained motion with `prefers-reduced-motion`, ease-out curves, interactions under 300ms, and no layout shift from animation.

## 8. Limitations

- No Shopify admin, so the WIP Liquid source, installed apps, markets, metafield definitions and policies were not inspected. Checkout was not tested.
- No licensed external stock imagery could be sourced: Unsplash returned HTTP 403 to automated access, and I did not use unlicensed Google Images. See `ASSET-LICENSES.md`.
- Some arvi.ch pages timed out on network idle because of third-party scripts. The content I captured before the timeout is used.
