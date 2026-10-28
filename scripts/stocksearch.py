"""Discover free-license (Unsplash License) photos via rendered search pages. Prints photo page URLs + alt."""
import asyncio,sys,json
from playwright.async_api import async_playwright
async def m(qs):
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1400,'height':1000})
    out={}
    for q in qs:
      await pg.goto(f'https://unsplash.com/s/photos/{q}?license=free',wait_until='domcontentloaded'); await pg.wait_for_timeout(4000)
      items=await pg.evaluate("""()=>[...document.querySelectorAll('figure a[href*="/photos/"]')].map(a=>{const i=a.querySelector('img');return {href:a.href,alt:i?i.alt:'',src:i?(i.currentSrc||i.src):''}}).filter(x=>x.src)""")
      out[q]=items[:24]; print('==',q,len(items))
      for it in items[:24]: print(it['href'],'|',it['alt'][:80])
    json.dump(out,open(sys.argv[1],'w'),indent=1)
    await b.close()
asyncio.run(m(sys.argv[2:]))
