# Shopify Maintenance Guide — ARVI "Swiss Reserve" theme (Dawn 16.0.0)

## For the ARVI team (no code)
Everything below is edited in **Online Store › Themes › Customize**.

### Homepage sections (in order)
| Section | What you can change |
|---|---|
| **ARVI · Editorial hero** | Layout (text left/right, full-bleed overlay), height, colour scheme, desktop image + separate mobile image, alt text, caption, eyebrow (used as the page H1), headline, text, two links. Set a **focal point** on images in Content › Files so crops stay on the bottle. |
| **ARVI · Collections** | Up to 7 collections. The first is the large tile. Per tile: title, kicker (e.g. "France"), featured bottle, or an editorial photo instead. The reference count can be toggled. |
| **ARVI · Featured wines** | A collection, or hand-picked wines (up to 12), with the number shown and the collection link label. |
| **ARVI · Heritage & cellar** | Image, eyebrow, heading, text, link. Up to 4 **Key figure** blocks and 1 **Quote** block. |
| **ARVI · Producers index** | Up to 12 producer collections with region labels. The bottle appears on hover (desktop). |
| **ARVI · Boutiques** | One block per shop: photo, name, address, hours, phone, email, note, directions link. Structured-data fields (street, postcode, city, hours in `Mo-Fr 08:30-12:30` format). **Turn structured data on in one place only** (it's on for the boutiques page and off on the homepage). |
| **ARVI · Why ARVI** | Up to 6 values with an icon from a curated set, title, text and optional link. |
| **ARVI · Services & stories** | Up to 4 cards (image, kicker, title, text, link). |

All sections have **colour scheme** and **vertical spacing** options and can be hidden, reordered or duplicated.

### Theme settings › ARVI
- **Display typeface:** ARVI editorial serif (Newsreader, self-hosted) or your Typography heading font.
- **Bronze accent:** decorative and text colours.
- **Price on request:** on or off, plus the enquiry email or an enquiry page. When a variant is priced CHF 0.00 the theme shows "Price on request", hides Add to cart and shows an enquiry button.
- **Show bottle format on cards** (e.g. "75 cl · 150 cl · OWC").
- **Product image note** (the illustrative-image disclaimer).
- **Logo is the homepage H1** (leave off).

### Product page (template "product")
The blocks are Dawn's, plus Custom Liquid blocks for the producer line, origin line, price on request, wine facts and the image note. The facts read the store's `arvi.*` metafields automatically. The **ARVI · Wine profile** section below adds:
- **All vintages**: automatic. It lists products from `produttore-<producer>` whose title matches once the vintage is removed.
- **Critic score** blocks: connect *Critic*, *Score* and *Review* to your product metafields with the dynamic-source button (database icon). Empty blocks are hidden.
- **Producer story**: your text, or the producer collection's description.

### Pages
- `page.faq` template: assign it to the FAQ page. Edit questions as blocks; FAQPage structured data is generated automatically.
- `page.boutiques` template: assign it to *I nostri negozi*.

### Texts in other languages
Theme strings (age gate, "Price on request", labels) are translated in `it`, `de`, `fr` and `en`. Edit them in **Themes › … › Edit default theme content**, or with Translate & Adapt for section content.

### Age confirmation
This is the "ARVI · Age confirmation" section in the footer group. Its cookie (`arvi_age_ok`) is identical to the WIP theme's, so visitors aren't asked twice.

## For developers

### Customisation map (vs upstream Dawn 16.0.0, commit `7097aaf`)
Run `git diff 7097aaf -- theme` for the exact diff.

**New files (69).** All are prefixed `arvi-`:
- sections: `arvi-hero`, `arvi-collection-tiles`, `arvi-product-showcase`, `arvi-heritage`, `arvi-producers`, `arvi-boutiques`, `arvi-values`, `arvi-services`, `arvi-faq`, `arvi-wine-profile`, `arvi-breadcrumbs`, `arvi-age-gate`
- snippets: `arvi-head`, `arvi-image`, `arvi-icon`, `arvi-section-header`, `arvi-card-meta`, `arvi-wine-facts`, `arvi-sibling-vintages`, `arvi-request-price`, `arvi-pdp-vendor`, `arvi-pdp-scripts`, `arvi-number`
- assets: `arvi-base.css`, `arvi-sections.css`, `arvi.js`, `arvi-product.js`, `arvi-age-gate.js`, `arvi-variant-formato.js` (from the WIP theme), fonts, images
- templates: `page.faq.json`, `page.boutiques.json`

**Modified Dawn files (16).** Each Liquid edit is a small hook:
| File | Change |
|---|---|
| `layout/theme.liquid` | +2 lines: `{% render 'arvi-head' %}` after `base.css` |
| `snippets/card-product.liquid` | +2 lines: `{% render 'arvi-card-meta' %}` after the vendor |
| `snippets/price.liquid` | +27 lines: zero price → "Price on request" / "From <lowest published price>" |
| `sections/header.liquid` | 4 conditions gain `and settings.arvi_logo_h1` |
| `config/settings_schema.json` | Appended "ARVI" group |
| `config/settings_data.json`, `sections/*-group.json`, `templates/*.json` | Configuration |
| `locales/{en.default,it,de,fr}.json` | Appended `arvi.*` keys |

### Upgrading Dawn
Shopify does **not** auto-update a customised theme. To move to a newer Dawn:
1. Download the new Dawn and copy every `arvi-*` file, `templates/page.faq.json` and `templates/page.boutiques.json` across.
2. Re-apply the 4 Liquid hooks above, append the ARVI settings group and the `arvi` locale keys, and keep your `settings_data.json` and templates.
3. Check that Dawn's `product-info` still exposes `addPreProcessCallback` (used by the WIP format script) and that `PUB_SUB_EVENTS.variantChange` still exists (used by `arvi-product.js` and the WIP `arvi-sconto.js`).
4. Run `shopify theme check`, preview the theme unpublished, then publish.

### Merging with the WIP theme
The WIP theme ("ARVI tema dawn") is also Dawn 16.0.0. I could not read its Liquid, so these WIP sections must be merged by someone with admin access: `arvi-vintage` (critics), `arvi-vintage-grid`, `arvi-breadcrumb`, `arvi-variant-formato` (section), `disclosures`, `arvi_age_gate`, plus `arvi-sconto.js` and `arvi-prezzo-titolo.js`. The new CSS already styles the WIP class names (`.arvi-vintage*`, `.arvi-critic*`).
**Keep only one** breadcrumb section and one age gate per template.

### Local preview harness
`node preview/server.mjs` renders this theme with the captured catalogue (see INSTALL-PREVIEW.md). It is a development aid only and is not part of the theme.
