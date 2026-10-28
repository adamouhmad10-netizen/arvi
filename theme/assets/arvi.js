/* ARVI global enhancements (progressive; the page works without them). */
(() => {
  /* Bottle formats are stored as centilitres ("75.00", "OWC 6 × 75.00"). Show them as "75 cl" in
     filter labels and active-filter chips. Display only: filter parameters are unchanged. */
  const SIZE = /^(\s*)(\d+(?:[.,]\d+)?)(\s*(?:\(\d+\))?\s*)$/;
  const OWC = /^(\s*OWC\s+\d+\s+×\s+)(\d+(?:[.,]\d+)?)(.*)$/;
  const cl = (n) => {
    const v = parseFloat(String(n).replace(',', '.'));
    return `${Number.isInteger(v) ? v : v.toString()} cl`;
  };
  const fix = (node) => {
    const t = node.textContent;
    let m = t.match(SIZE);
    if (m) return (node.textContent = m[1] + cl(m[2]) + m[3]);
    m = t.match(OWC);
    if (m) node.textContent = m[1] + cl(m[2]) + m[3];
  };
  const run = (root = document) => {
    root
      .querySelectorAll(
        'label[for^="Filter-filter.v.option.formato"] .facet-checkbox__text-label, .active-facets a[href*="option.formato"] .active-facets__button-inner'
      )
      .forEach((el) => {
        const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
        let n;
        while ((n = walker.nextNode())) if (/\d/.test(n.textContent)) fix(n);
      });
  };
  const start = () => {
    run();
    const facets = document.getElementById('ProductGridContainer') || document.querySelector('.facets-container');
    const target = document.querySelector('[id^="FacetFiltersForm"], .facets-wrapper, #main-collection-filters') || facets;
    if (target) new MutationObserver(() => run()).observe(target.parentElement || target, { childList: true, subtree: true });
  };
  document.readyState === 'loading' ? document.addEventListener('DOMContentLoaded', start) : start();
})();

/* Product counts ("1742 products") use the same thousands separator as the rest of the site ("1,742").
   Display only; re-applied when filters re-render the count. */
(() => {
  const SEL = '#ProductCount, #ProductCountDesktop, .product-count__text, .mobile-facets__count';
  const group = (root = document) =>
    root.querySelectorAll(SEL).forEach((el) => {
      const t = el.textContent;
      const f = t.replace(/\b\d{4,}\b/g, (d) => d.replace(/\B(?=(\d{3})+(?!\d))/g, ','));
      if (f !== t) el.textContent = f;
    });
  const start = () => {
    group();
    const host = document.querySelector('.facets-container, #main-collection-filters, .template-search');
    if (host) new MutationObserver(() => group()).observe(host, { childList: true, subtree: true, characterData: true });
  };
  document.readyState === 'loading' ? document.addEventListener('DOMContentLoaded', start) : start();
})();
