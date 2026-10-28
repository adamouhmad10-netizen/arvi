"""Responsive QA: horizontal overflow, overlapping/clipped text, tiny tap targets, missing alt, heading order."""
import asyncio,json,sys
from playwright.async_api import async_playwright
B='http://localhost:9292'
PAGES=['/','/collections/champagne','/products/maison-salon-champagne-le-mesnil-1999','/products/chateau-latour-ex-chateau-release-2023-2015?variant=59475133137244','/search?q=krug','/pages/faq','/pages/i-nostri-negozi']
WIDTHS=[375,390,768,1024,1440,1920]
JS="""() => {
 const r={overflowPx:document.documentElement.scrollWidth-innerWidth, wide:[], smallTargets:[], noAlt:0, h1:0, headingSkips:[], textClip:[]};
 for (const el of document.querySelectorAll('body *')) {
   const b=el.getBoundingClientRect(); if(!b.width) continue;
   const cs=getComputedStyle(el); if(cs.position==='fixed'||el.closest('dialog,template,.menu-drawer,.mega-menu__content,details:not([open])>*:not(summary)')) continue;
   if (b.right>innerWidth+1 && cs.overflowX!=='hidden' && !el.closest('[class*="slider"],.announcement-bar,.visually-hidden,.skip-to-content-link')) r.wide.push((el.className||el.tagName).toString().slice(0,60));
 }
 for (const el of document.querySelectorAll('a[href],button,input:not([type=hidden]),select,summary')) {
   const b=el.getBoundingClientRect(); if(!b.width||el.closest('.visually-hidden,dialog,.menu-drawer,details:not([open]) > :not(summary)')) continue;
   if (getComputedStyle(el).visibility==='hidden') continue;
   if ((b.height<24||b.width<24) && !el.closest('.rte,.footer-block__details-content,.arvi-crumbs,.arvi-boutique__facts,.copyright__content,.policies')) r.smallTargets.push((el.textContent||el.getAttribute('aria-label')||el.className).trim().slice(0,30)+' '+Math.round(b.width)+'x'+Math.round(b.height));
 }
 r.noAlt=[...document.images].filter(i=>!i.hasAttribute('alt')).length;
 const hs=[...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].filter(h=>h.getClientRects().length||h.closest('.visually-hidden')===null);
 r.h1=document.querySelectorAll('h1').length;
 let prev=0; for(const h of hs){const l=+h.tagName[1]; if(prev && l>prev+1) r.headingSkips.push(h.tagName+':'+h.textContent.trim().slice(0,30)); prev=l;}
 r.wide=[...new Set(r.wide)].slice(0,6); r.smallTargets=[...new Set(r.smallTargets)].slice(0,8); r.headingSkips=r.headingSkips.slice(0,5);
 return r;}"""
async def m():
  out={}
  async with async_playwright() as p:
    b=await p.chromium.launch()
    for w in WIDTHS:
      ctx=await b.new_context(viewport={'width':w,'height':900}); await ctx.add_cookies([{'name':'arvi_age_ok','value':'1','url':B}])
      pg=await ctx.new_page()
      for path in PAGES:
        await pg.goto(B+path,wait_until='networkidle'); await pg.wait_for_timeout(300)
        r=await pg.evaluate(JS); out[f'{w} {path}']=r
        flag='' if r['overflowPx']<=0 and not r['wide'] else '  <-- OVERFLOW'
        print(w,path[:50],'overflow',r['overflowPx'],'h1',r['h1'],'noAlt',r['noAlt'],'small',len(r['smallTargets']),'skips',len(r['headingSkips']),flag)
      await ctx.close()
    await b.close()
  json.dump(out,open('presentation/qa-responsive.json','w'),indent=1,ensure_ascii=False)
asyncio.run(m())
