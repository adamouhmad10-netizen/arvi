"""axe-core WCAG 2.0/2.1/2.2 A+AA audit of preview pages (desktop + mobile)."""
import asyncio,json
from playwright.async_api import async_playwright
B='http://localhost:9292'
PAGES=['/','/collections/champagne','/products/maison-salon-champagne-le-mesnil-1999','/products/chateau-latour-ex-chateau-release-2023-2015?variant=59475133137244','/search?q=krug','/pages/faq','/pages/i-nostri-negozi']
AXE=open('.tooling/node_modules/axe-core/axe.min.js').read()
async def m():
  res={}
  async with async_playwright() as p:
    b=await p.chromium.launch()
    for w in [1440,390]:
      ctx=await b.new_context(viewport={'width':w,'height':900}); await ctx.add_cookies([{'name':'arvi_age_ok','value':'1','url':B}])
      pg=await ctx.new_page()
      for path in PAGES:
        await pg.goto(B+path,wait_until='networkidle')
        await pg.evaluate("async()=>{for(let y=0;y<document.body.scrollHeight;y+=400){scrollTo(0,y);await new Promise(r=>setTimeout(r,120));}scrollTo(0,0);await new Promise(r=>setTimeout(r,900));}")
        await pg.add_script_tag(content=AXE)
        r=await pg.evaluate("""async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa']}});return r.violations.map(v=>({id:v.id,impact:v.impact,n:v.nodes.length,help:v.help,nodes:v.nodes.slice(0,4).map(n=>n.target.join(' ')+' :: '+(n.failureSummary||'').split('\\n').slice(1,2).join(''))}))}""")
        res[f'{w} {path}']=r
        print(w,path[:60],'violations:',[(v['id'],v['impact'],v['n']) for v in r])
      await ctx.close()
    await b.close()
  json.dump(res,open('presentation/qa-axe.json','w'),indent=1)
asyncio.run(m())
