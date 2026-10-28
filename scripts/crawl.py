"""Research crawler: renders pages with Playwright, saves screenshots + extracted text/images.
Usage: python3 scripts/crawl.py <label> <url> [<label> <url> ...]
Env: SHOP_PW (storefront preview password, never logged)."""
import sys, json, os, re, asyncio
from playwright.async_api import async_playwright
OUT='research'
VIEWS={'desktop':{'width':1440,'height':900},'mobile':{'width':390,'height':844}}

async def dismiss(page):
    for sel in ['text=/legal drinking age/i','text=/^(Yes|Ja|Sì|Oui|I am over|I am 18|Enter|Accept|Accept all|Akzeptieren|OK|Agree)/i',
                '#agecheck button','.agecheck button','button:has-text("18")','#cookie-accept','.cookie-bar button']:
        try:
            el=page.locator(sel).first
            if await el.is_visible(timeout=400): await el.click(timeout=1000); await page.wait_for_timeout(400)
        except Exception: pass

async def unlock(page):
    if '/password' in page.url and os.environ.get('SHOP_PW'):
        async with page.expect_navigation():
            await page.evaluate("pw=>{const i=document.querySelector('input[type=password]');i.value=pw;i.form.requestSubmit()}", os.environ['SHOP_PW'])
        await page.wait_for_load_state('networkidle')

async def run(pairs):
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for vname,vp in VIEWS.items():
            ctx=await b.new_context(viewport=vp, device_scale_factor=1, locale='en-US',
                user_agent=None if vname=='desktop' else 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1')
            await ctx.add_init_script("try{localStorage.setItem('ageVerified','true')}catch(e){};document.cookie='ageVerified=true;path=/'")
            page=await ctx.new_page()
            for label,url in pairs:
                try:
                    await page.goto(url, wait_until='networkidle', timeout=60000)
                except Exception as e:
                    print('WARN',label,e.__class__.__name__)
                if '/password' in page.url:
                    await unlock(page)
                    if '/password' not in page.url and page.url.rstrip('/')!=url.rstrip('/'): await page.goto(url, wait_until='networkidle')
                await dismiss(page)
                await page.evaluate("""async()=>{for(let y=0;y<document.body.scrollHeight;y+=600){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,120));}window.scrollTo(0,0);}""")
                await page.wait_for_timeout(800); await dismiss(page)
                await page.screenshot(path=f'{OUT}/screens/{label}-{vname}.png', full_page=True)
                await page.screenshot(path=f'{OUT}/screens/{label}-{vname}-fold.png')
                if vname=='desktop':
                    data=await page.evaluate("""()=>({url:location.href,title:document.title,
                      meta:[...document.querySelectorAll('meta[name],meta[property]')].map(m=>[m.name||m.getAttribute('property'),m.content]),
                      lang:document.documentElement.lang,
                      canonical:(document.querySelector('link[rel=canonical]')||{}).href,
                      hreflang:[...document.querySelectorAll('link[hreflang]')].map(l=>[l.hreflang,l.href]),
                      headings:[...document.querySelectorAll('h1,h2,h3,h4')].map(h=>h.tagName+' '+h.innerText.trim().replace(/\\s+/g,' ')).slice(0,200),
                      jsonld:[...document.querySelectorAll('script[type="application/ld+json"]')].map(s=>s.textContent.slice(0,3000)),
                      text:document.body.innerText.slice(0,40000),
                      images:[...document.querySelectorAll('img')].map(i=>({src:i.currentSrc||i.src,alt:i.alt,w:i.naturalWidth,h:i.naturalHeight})).filter(i=>i.src),
                      bgs:[...document.querySelectorAll('*')].map(e=>getComputedStyle(e).backgroundImage).filter(b=>b&&b!=='none'&&b.includes('url')).slice(0,50),
                      fonts:[...new Set([...document.querySelectorAll('body,h1,h2,h3,a,p,button')].map(e=>getComputedStyle(e).fontFamily))],
                      colors:[...new Set([...document.querySelectorAll('body,header,footer,h1,h2,a,button,nav')].map(e=>{const s=getComputedStyle(e);return s.color+'|'+s.backgroundColor}))].slice(0,40)
                    })""")
                    json.dump(data,open(f'{OUT}/raw/{label}.json','w'),ensure_ascii=False,indent=1)
                print('ok',vname,label,page.url[:90])
            await ctx.close()
        await b.close()

a=sys.argv[1:]; asyncio.run(run(list(zip(a[::2],a[1::2]))))
