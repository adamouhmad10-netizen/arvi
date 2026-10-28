"""Extract product facts that the WIP theme renders from arvi.* metafields (region line, spec rows, critic scores, sibling vintages).
Used only to give the local preview harness truthful data. Usage: SHOP_PW=... scrape_wip_meta.py out.json handle..."""
import asyncio,os,sys,json,re,html
from playwright.async_api import async_playwright
def txt(s): return html.unescape(re.sub(r'<[^>]+>','',s)).strip()
async def m(out,handles):
  async with async_playwright() as p:
    b=await p.chromium.launch(); ctx=await b.new_context(); pg=await ctx.new_page()
    await pg.goto('https://myarvi.myshopify.com/password',wait_until='networkidle')
    async with pg.expect_navigation():
        await pg.evaluate("pw=>{const i=document.querySelector('input[type=password]');i.value=pw;i.form.requestSubmit()}", os.environ['SHOP_PW'])
    res={}
    for h in handles:
      for loc in ['', '/en']:
        r=await ctx.request.get(f'https://myarvi.myshopify.com{loc}/products/{h}'); s=(await r.text())
        d=res.setdefault(h,{})
        key='en' if loc else 'it'
        specs=[(txt(a),txt(b)) for a,b in re.findall(r'<div class="arvi-specs__row"><dt>(.*?)</dt><dd>(.*?)</dd>',s,re.S)]
        critics=[{'name':txt(a),'score':txt(b),'review':txt(c)} for a,b,c in re.findall(r'arvi-critic__name">(.*?)</span>\s*<span class="arvi-critic__score">(.*?)</span>(?:<p class="arvi-critic__review">(.*?)</p>)?',s,re.S)]
        vint=[{'label':txt(t),'href':(re.search(r'href="([^"]+)"',a) or [None,None])[1],'state':'selected' if 'selected' in a else ('unavailable' if 'unavailable' in a else '')} for a,t in re.findall(r'<(?:a|span) (class="arvi-vintage[^>]*)>(.*?)</(?:a|span)>',s)]
        # region line: text block under title in WIP main product
        m2=re.search(r'class="product__text inline-richtext[^"]*"[^>]*>(.*?)</p>',s,re.S)
        reg=[txt(x) for x in re.findall(r'class="product__text[^"]*"[^>]*>(.*?)</p>',s,re.S)]
        d[key]={'specs':specs,'critics':critics,'vintages':vint,'text_blocks':reg}
      print(h, len(d['en']['specs']), len(d['en']['critics']), len(d['en']['vintages']))
    json.dump(res,open(out,'w'),ensure_ascii=False,indent=1)
    await b.close()
asyncio.run(m(sys.argv[1],sys.argv[2:]))
