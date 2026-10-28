"""Interaction QA on the local preview (Playwright).
Cart: the preview has no cart backend, so /cart/add.js is intercepted. This verifies what the THEME sends
(endpoint, variant id, quantity) and how it handles the response; it does not test Shopify's cart or checkout.
Also checks: size/packaging labels, vintage index, recommendations dedupe, mega menu, mobile drawer."""
import asyncio, json, sys
from playwright.async_api import async_playwright
BASE = 'http://localhost:9292'
SHOTS = sys.argv[1] if len(sys.argv) > 1 else 'presentation/screens'
results = []
def check(name, ok, detail=''):
    results.append({'test': name, 'pass': bool(ok), 'detail': detail}); print(('PASS ' if ok else 'FAIL ') + name, detail)

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={'width': 1440, 'height': 900})
        await ctx.add_cookies([{'name': 'arvi_age_ok', 'value': '1', 'url': BASE}])
        pg = await ctx.new_page()
        sent = []
        sections_payload = {}
        async def cart_add(route):
            req = route.request; body = req.post_data or ''
            sent.append({'url': req.url, 'method': req.method, 'body': body, 'ctype': req.headers.get('content-type', '')})
            await route.fulfill(status=200, content_type='application/json', body=json.dumps({'id': 1, 'quantity': 1, 'sections': sections_payload}))
        await pg.route('**/cart/add*', cart_add)
        await pg.route('**/cart.js*', lambda r: r.fulfill(status=200, content_type='application/json', body=json.dumps({'item_count': 1, 'items': []})))
        await pg.goto(BASE + '/products/maison-salon-champagne-le-mesnil-1999', wait_until='networkidle')
        labels = await pg.evaluate("[...document.querySelectorAll('product-info .form__label')].map(e=>e.textContent.trim())")
        check('Option label translated (no "Formato" on EN)', 'Formato' not in ' '.join(labels) and any(l.lower().startswith('size') for l in labels), str(labels))
        vid = await pg.evaluate("document.querySelector('product-form input[name=id]').value")
        # Answer the add with section HTML built from this page, as Shopify's Section Rendering API would
        drawer_html = await pg.evaluate("document.querySelector('cart-drawer').outerHTML")
        bubble_html = await pg.evaluate("document.getElementById('cart-icon-bubble').innerHTML")
        sections_payload['cart-drawer'] = '<div class=\"shopify-section\">' + drawer_html + '</div>'
        sections_payload['cart-icon-bubble'] = '<div class=\"shopify-section\">' + bubble_html + '</div>'
        await pg.click('product-form button[type=submit]')
        await pg.wait_for_timeout(1200)
        ok = sent and sent[0]['method'] == 'POST' and vid in sent[0]['body']
        check('Add to cart POSTs /cart/add with the selected variant', ok, (sent[0]['url'] + ' variant ' + vid) if sent else 'no request')
        qty_ok = sent and ('name="quantity"' in sent[0]['body'] and '\r\n\r\n1\r\n' in sent[0]['body'] or 'quantity=1' in sent[0]['body'])
        check('Add to cart sends quantity 1', qty_ok, sent[0]['ctype'][:40] if sent else '')
        drawer = await pg.evaluate("(()=>{const d=document.querySelector('cart-drawer');return d?d.classList.contains('active'):null})()")
        check('Cart drawer opens after the (intercepted) add', drawer, 'cart-drawer.active=' + str(drawer))
        await pg.keyboard.press('Escape')
        # vintages
        v = await pg.evaluate("[...document.querySelectorAll('.arvi-vintage')].map(a=>a.className.includes('selected')?'S':a.className.includes('unavailable')?'U':'A').join('')")
        check('Vintage index renders states', 'S' in v and len(v) > 1, v)
        dashed = await pg.evaluate("[...document.querySelectorAll('.arvi-vintage')].some(a=>getComputedStyle(a).borderStyle.includes('dashed'))")
        check('No dashed "broken" vintage boxes', not dashed)
        critics = await pg.evaluate("document.querySelectorAll('.arvi-critic').length")
        check('No unbound critic data on the page', critics == 0, f'{critics} critic blocks')
        await pg.evaluate("window.scrollTo(0, document.body.scrollHeight)"); await pg.wait_for_timeout(1500)
        recs = await pg.evaluate("[...document.querySelectorAll('product-recommendations li[data-arvi-wine]')].map(l=>l.dataset.arviWine)")
        host = await pg.evaluate("document.querySelector('product-recommendations')?.dataset.arviWine")
        check('Recommendations: no repeats, no other vintage of this wine', len(recs) == len(set(recs)) and host not in recs, f'{len(recs)} cards')
        # request price variant
        await pg.goto(BASE + '/products/chateau-latour-ex-chateau-release-2023-2015?variant=59475133137244', wait_until='networkidle')
        st = await pg.evaluate("(()=>{const r=document.querySelector('arvi-request-price');const b=[...document.querySelectorAll('product-info .price .badge')].filter(e=>e.offsetParent);return [r&&!r.classList.contains('hidden'), b.length, !!document.querySelector('.product-form__buttons')&&document.querySelector('.product-form__buttons').offsetParent!==null]})()")
        check('Price on request: enquiry shown, no conflicting badge, no add-to-cart', st[0] and st[1] == 0 and not st[2], str(st))
        # card fallback
        await pg.goto(BASE + '/collections/champagne', wait_until='networkidle')
        fb = await pg.evaluate("(()=>{const f=document.querySelector('.arvi-fallback');if(!f)return null;const c=f.closest('.card');const h=c.querySelector('.card__content .card__heading');return [getComputedStyle(h).display, h.textContent.trim().slice(0,30), c.className.includes('card--media')]})()")
        check('Missing-photo card keeps its title and media layout', fb and fb[0] != 'none' and fb[1] and fb[2], str(fb))
        # mega menu
        await pg.goto(BASE + '/', wait_until='networkidle')
        await pg.click('header-menu details summary'); await pg.wait_for_timeout(500)
        opened = await pg.evaluate("!!document.querySelector('header-menu details[open]')")
        check('Mega menu opens', opened)
        await pg.screenshot(path=f'{SHOTS}/nav-mega-1440.png')
        await ctx.close()
        # mobile drawer
        m = await b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2)
        await m.add_cookies([{'name': 'arvi_age_ok', 'value': '1', 'url': BASE}])
        mp = await m.new_page(); await mp.goto(BASE + '/', wait_until='networkidle')
        await mp.click('header-drawer summary'); await mp.wait_for_timeout(600)
        dopen = await mp.evaluate("!!document.querySelector('header-drawer details[open]')")
        check('Mobile menu drawer opens', dopen)
        acc = await mp.evaluate("(()=>{const a=document.querySelector('.header__icon--account');return !!a && a.getBoundingClientRect().width>0})()")
        check('Account access visible on mobile (Dawn 16 has no drawer account link)', acc)
        await mp.screenshot(path=f'{SHOTS}/nav-drawer-390.png')
        rail = await mp.evaluate("(()=>{const g=document.querySelector('.arvi-boutiques__grid');const c=getComputedStyle(g);return [c.overflowX, g.scrollWidth>g.clientWidth]})()")
        check('Mobile boutiques rail scrolls horizontally', rail[0] == 'auto' and rail[1], str(rail))
        await b.close()
    json.dump(results, open('presentation/qa-interactions.json', 'w'), indent=1)
    print(sum(r['pass'] for r in results), '/', len(results), 'passed')
asyncio.run(main())
