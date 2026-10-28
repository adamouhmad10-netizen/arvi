# ARVI — Content Inventory

This is verified content harvested from arvi.ch (EN) and the Shopify preview. The copy used in the theme comes **only** from this list. Where theme defaults are in English, the merchant should localise them to IT/DE/FR in the theme editor (translatable `t:` strings are already translated by Dawn's locale files).

## Brand statements (arvi.ch/en/about-us)
- "With more than thirty years of experience, we are one of the main dealers of fine and rare wines in Switzerland."
- "Our wine portfolio has become a reference point for vintage wines from all over the world and we offer customized services for private customers, wine lovers and collectors, as well as for the HORECA sector."
- "Trust, passion, expertise, respect: it is in these values that our uniqueness lies."
- "We hold in our cellars over 10 thousand labels ready for delivery … an impressive collection of large formats, from the 150 cl Magnum to 27 litre formats."
- **Our cellar:** "All wines we offer are owned by our company and stored in our wine cellars … temperature and humidity control … fully insured. Every single case is checked upon receipt and evaluated by a professional staff, photographed and registered in the Warehouse Management System, which guarantees full traceability."
- **Quote:** "Everything we do, we do because we love wine…" – Paolo Cattaneo, Arvi Chairman
- **Home H1:** "Your Premium Wine Shop in Switzerland". **Meta description:** "Buy over 5,000 fine and rare wines from Bordeaux, Burgundy, and Tuscany online. Secure shipping and 24h delivery throughout Switzerland." ⚠ The "5,000" here conflicts with About's "10 thousand labels", and the FAQ says shipping costs are separate. The merchant must confirm which figure is correct.

## Why buy from us (home, verbatim headings)
1. **Outstanding wine selection.** "We offer a selection of the finest wines from all over the world."
2. **Accurate delivery.** "We provide precise and timely delivery."
3. **Professional advice.** "Benefit from the expert guidance of our consultants to choose the perfect wine."
4. **Quality and Authenticity.** "We ensure every bottle you buy is authentic and of the highest quality."

## Boutiques
See RESEARCH-AUDIT §4 for addresses, hours and phone numbers, all verbatim from arvi.ch/en/shops. Intro: "Discover the world of fine wines in our Arvino Luxury Wine Shops. Strategically located in Melano (within our headquarters), Lugano and Zurich…"

## Services
- **Wine Vault:** "We have created the ideal storage facility to hold your fine wines … secured safe … ideal maturation, temperature and humidity conditions." Features: wine insurance, delivery, case or pallet storage, and six-monthly or annual payment.
- **Horeca:** "Tailored services for the HORECA sector … a free consultancy service to create and manage your wine list". Free for customers with ≥50% of labels supplied by Arvi.
- **Events:** tastings, blind tastings, dinners, and private/corporate events at Melano and the boutiques (Zurich: 40 standing / 18 seated).
- **En Primeur:** explainer page, 2025 Bordeaux vintage report, EP collection (Shopify handle `en-primeur`, 369 products).
- **Arvi Bio-Green:** sustainability page (bio-inspecta certificate image).

## FAQ (16 Q&As, verbatim answers captured in `research/raw/faq.html`)
These include how wines are stored, sourcing ("About 95% of ARVI's stock comes from producers, négociants and/or important traders based in Europe"), availability, payment (bank transfer, Visa/MasterCard), terms, discounts, shipping costs, pick-up at Melano, international shipping, validity of prices, 60-day free storage, Wine Vault, defective bottles (Swiss wine-trade association rules), **VAT 8.1%**, older bottles (photos on request) and En Primeur. These are real Q&As, so they are eligible for `FAQPage` structured data on the FAQ page **only**.

## Catalogue taxonomy (arvi.ch nav ↔ Shopify handles)
| Navigation | Shopify handle |
|---|---|
| Red / White / Rosé / Sparkling / Sweet | `red-wines`, `white-wines`, `rose-wines`, `sparkling-wines`, `sweet-wines` |
| France: Bordeaux, Champagne, Burgundy, Rhône, Other | `bordeaux`, `champagne`, `burgundy`, `rhone`, `other-regions` |
| Italy: Piedmont, Sicily, Tuscany, Trentino-South Tyrol, Veneto | `piemonte`, `sicilia`, `toscana`, `trentino-alto-adige`, `veneto` |
| Europe: Spain, Hungary, Austria, Portugal, Germany, Switzerland | `spain`, `hungary`, `austria`, `portugal`, `germany`, `switzerland` |
| New World | `australia`, `argentina`, `chile`, `south-africa`, `new-zealand`, `lebanon`, `united-states`, `china`, `georgia` |
| Icons | `produttore-chateau-petrus`, `-ausone`, `-lafite-rothschild`, `-mouton-rothschild`, `-latour` |
| Best sellers / Gift ideas / En Primeur / Spirits / Water | `best-sellers`, `gift-ideas`, `en-primeur`, `spirits`, `water-st-geron` |
| Accessories | `accessories`, `glasses`, `corkscrews`, `coolers`, `wine-cases`, `coravin`, `carafes`, `decanter`, `decanting-cardles` (sic) |
| Pages | `chi-siamo`, `i-nostri-negozi`, `la-wine-vault`, `horeca`, `eventi`, `faq`, `contattaci`, `che-cose-en-primeur`, `arvi-green`, `dicono-di-noi`, `carriera`, `privacy-policy`, `termini-e-condizioni` |

## Product data fields (observed)
Title (wine + vintage), vendor (producer), "Formato" option (size cl, OWC n × size), price CHF incl. VAT, availability, and metafields `arvi.annata`, `arvi.colore`, `arvi.regione`, `arvi.produttore`. Also shown (keys not visible): sub-region line ("Côte des Blancs | Champagne | Francia"), alcohol ("12.0% vol"), critic scores with source, score and review text, and a sibling-vintage list. The legal note "The product image is for illustrative purposes only and may not exactly reflect the actual characteristics of the wine." appears on both sites and is preserved.

## Legal/compliance copy
- Age gate: "As we are selling fine wines and spirits, you must be of legal drinking age in your country to visit our website." (arvi.ch). On Shopify: "Hai almeno 18 anni?"
- Shopify footer: "La vendita di bevande alcoliche ai minori di 18 anni è vietata." (sale of alcohol to minors under 18 is prohibited). This is kept in the new footer.
- arvi.ch links to Privacy Policy, Event Terms and Conditions (PDF), Cookie preferences and Sitemap.
