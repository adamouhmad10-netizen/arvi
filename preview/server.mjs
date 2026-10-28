// Local preview server for the ARVI Dawn theme.
// Usage (from repo root): node preview/server.mjs [port]
// Renders theme/ Liquid files with real catalogue data captured from the ARVI Shopify preview.
import http from 'node:http';
import zlib from 'node:zlib';
import fs from 'node:fs';
import path from 'node:path';
import { reloadLocales, createEngine, schemaOf, defaultsFrom, resolveSetting, globalSettings, resolveURL, THEME } from './shopify.mjs';
import * as data from './data.mjs';

const PORT = Number(process.argv[2] || 9292);
const linklists = data.linklists();
const readJSON = (p) => JSON.parse(fs.readFileSync(path.join(THEME, p), 'utf8').replace(/^\/\*[\s\S]*?\*\/\s*/, ''));
const LANGS = [
  { iso_code: 'it', endonym_name: 'Italiano', primary: true },
  { iso_code: 'de', endonym_name: 'Deutsch' },
  { iso_code: 'fr', endonym_name: 'Français' },
  { iso_code: 'en', endonym_name: 'English' },
];

const PAGES = {
  'i-nostri-negozi': { title: 'Our shops', template: 'page.boutiques' },
  faq: { title: 'FAQ', template: 'page.faq' },
};

function baseGlobals(req, url) {
  const g = {
    __query: Object.fromEntries(url.searchParams),
    settings: globalSettings(linklists),
    shop: {
      name: 'ARVI',
      url: `http://localhost:${PORT}`,
      domain: `localhost:${PORT}`,
      permanent_domain: 'myarvi.myshopify.com',
      currency: 'CHF',
      money_format: 'CHF {{amount}}',
      // Verified from ARVI's FAQ ("credit card (Visa & MasterCard)"). On Shopify this list comes from the store's payment settings.
      enabled_payment_types: (process.env.PREVIEW_PAYMENT_TYPES || 'visa,master').split(','),
      'customer_accounts_enabled?': true,
      customer_accounts_enabled: true,
      brand: { logo: null },
      policies: [{ title: 'Privacy policy', url: '/policies/privacy-policy' }, { title: 'Terms of service', url: '/policies/terms-of-service' }],
      privacy_policy: { title: 'Privacy policy', url: '/policies/privacy-policy' },
    },
    request: {
      locale: { iso_code: 'en', primary: false, root_url: '/' },
      design_mode: false,
      visual_preview_mode: false,
      path: url.pathname,
      host: `localhost:${PORT}`,
      origin: `http://localhost:${PORT}`,
      page_type: 'index',
    },
    routes: {
      root_url: '/',
      account_url: '/account',
      account_login_url: '/account/login',
      account_register_url: '/account/register',
      cart_url: '/cart',
      cart_add_url: '/cart/add',
      cart_change_url: '/cart/change',
      cart_update_url: '/cart/update',
      collections_url: '/collections',
      all_products_collection_url: '/collections/all',
      search_url: '/search',
      predictive_search_url: '/search/suggest',
      product_recommendations_url: '/recommendations/products',
    },
    localization: {
      available_languages: LANGS,
      language: LANGS[3],
      available_countries: [{ iso_code: 'CH', name: 'Switzerland', currency: { iso_code: 'CHF', symbol: 'CHF' } }],
      country: { iso_code: 'CH', name: 'Switzerland', currency: { iso_code: 'CHF', symbol: 'CHF' } },
    },
    cart: new data.CartDrop(),
    customer: null,
    linklists,
    collections: data.collectionsProxy,
    all_products: data.allProductsProxy,
    pages: {},
    blogs: {},
    // Stand-in for Shopify's content_for_header (defines window.Shopify on real stores)
    content_for_header: '<script>window.Shopify = window.Shopify || { designMode: false, routes: { root: "/" }, locale: "en", currency: { active: "CHF", rate: "1.0" } };</script>',
    powered_by_link: '<a target="_blank" rel="nofollow" href="https://www.shopify.com">Powered by Shopify</a>',
    current_page: Number(url.searchParams.get('page') || 1),
    current_tags: null,
    canonical_url: `https://www.arvi.ch${url.pathname}`,
    page_title: 'ARVI',
    page_description: '',
    template: { name: 'index', suffix: null, directory: null, toString: () => 'index' },
    scheme_classes: '',
  };
  return g;
}

async function renderValue(engine, val, scope) {
  if (typeof val === 'string' && val.includes('{{')) return engine.parseAndRender(val, scope);
  return val;
}

async function buildSection(engine, type, id, json, scope) {
  const schema = schemaOf(type);
  const types = Object.fromEntries((schema.settings || []).filter((s) => s.id).map((s) => [s.id, s.type]));
  const settings = { ...defaultsFrom(schema.settings), ...(json.settings || {}) };
  for (const k of Object.keys(settings)) settings[k] = resolveSetting(types[k], await renderValue(engine, settings[k], scope), linklists);
  const blocks = [];
  const order = json.block_order || Object.keys(json.blocks || {});
  for (const bid of order) {
    const b = json.blocks[bid];
    if (!b || b.disabled) continue;
    const bs = (schema.blocks || []).find((x) => x.type === b.type) || { settings: [] };
    const btypes = Object.fromEntries((bs.settings || []).filter((s) => s.id).map((s) => [s.id, s.type]));
    const bset = { ...defaultsFrom(bs.settings), ...(b.settings || {}) };
    for (const k of Object.keys(bset)) bset[k] = resolveSetting(btypes[k], await renderValue(engine, bset[k], scope), linklists);
    blocks.push({ id: bid, type: b.type, settings: bset, shopify_attributes: '' });
  }
  const section = { id, settings, blocks, index: 1, location: 'template' };
  // `liquid` settings (Custom Liquid) are executed by Shopify with section/block in scope
  for (const [k, t] of Object.entries(types)) if (t === 'liquid' && settings[k]) settings[k] = await engine.parseAndRender(settings[k], { ...scope, section });
  for (const b of blocks) {
    const bs = (schema.blocks || []).find((x) => x.type === b.type) || { settings: [] };
    for (const st of bs.settings || []) {
      if (st.type === 'liquid' && b.settings[st.id]) {
        const prev = scope.section;
        scope.section = section;
        b.settings[st.id] = await engine.parseAndRender(b.settings[st.id], { ...scope, section, block: b });
        scope.section = prev;
      }
    }
  }
  return { schema, section };
}

// Simulates the merchant connecting critic blocks to product metafields (dynamic sources) in the theme editor.
// Values come from the critic data the WIP theme renders for that product.
// Off by default: customer-facing screenshots must not show critic data the theme is not actually bound to.
// Set PREVIEW_SIMULATE_CRITICS=1 only to check the critic block layout.
function simulateDynamicSources(type, json, scope) {
  if (process.env.PREVIEW_SIMULATE_CRITICS !== '1') return json;
  if (type !== 'arvi-wine-profile' || !scope.product) return json;
  const copy = JSON.parse(JSON.stringify(json));
  const critics = scope.product.__critics || [];
  let i = 0;
  for (const bid of copy.block_order || []) {
    const b = copy.blocks[bid];
    if (b.type === 'critic') {
      const c = critics[i++];
      b.settings = c ? { source: c.name, score: c.score, review: c.review ? `<p>${c.review}</p>` : '' } : {};
    }
  }
  return copy;
}

async function renderSectionHTML(engine, type, id, json, scope, groupClass = '') {
  json = simulateDynamicSources(type, json, scope);
  const { schema, section } = await buildSection(engine, type, id, json, scope);
  let html;
  const prevSection = scope.section;
  scope.section = section; // Shopify exposes `section` inside rendered snippets
  try {
    html = await engine.renderFile(type, { ...scope, section });
  } catch (e) {
    console.error(`[section ${type}]`, e.message);
    html = `<pre style="color:#b00;padding:20px">Liquid error in section ${type}: ${e.message}</pre>`;
  }
  scope.section = prevSection;
  const tag = schema.tag || 'div';
  return `<${tag} id="shopify-section-${id}" class="shopify-section${groupClass}${schema.class ? ' ' + schema.class : ''}">${html}</${tag}>`;
}

function registerSectionsTag(engine, scopeRef) {
  engine.registerTag('sections', {
    parse(token) {
      this.group = token.args.replace(/['"\s]/g, '');
    },
    *render(ctx, emitter) {
      const group = this.group;
      const out = yield (async () => {
        const groupJson = readJSON(`sections/${group}.json`);
        let html = '';
        for (const key of groupJson.order) {
          const sj = groupJson.sections[key];
          if (sj.disabled) continue;
          html += await renderSectionHTML(engine, sj.type, `sections--1__${key}`, sj, scopeRef.scope, ` shopify-section-group-${group}`);
        }
        return html;
      })();
      emitter.write(out);
    },
  });
}

async function renderPage(templateName, scope, engine) {
  const tpl = readJSON(`templates/${templateName}.json`);
  let content = '';
  for (const key of tpl.order) {
    const sj = tpl.sections[key];
    if (sj.disabled) continue;
    content += await renderSectionHTML(engine, sj.type, `template--1__${key}`, sj, scope);
  }
  scope.content_for_layout = content;
  return engine.renderFile('theme', scope);
}

const MIME = { '.css': 'text/css', '.js': 'application/javascript', '.svg': 'image/svg+xml', '.webp': 'image/webp', '.woff2': 'font/woff2', '.png': 'image/png', '.jpg': 'image/jpeg', '.json': 'application/json' };

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, `http://localhost:${PORT}`);
  try {
    if (url.pathname.startsWith('/assets/')) {
      const f = path.join(THEME, 'assets', path.basename(decodeURIComponent(url.pathname)));
      if (!fs.existsSync(f)) {
        res.writeHead(404);
        return res.end();
      }
      const type = MIME[path.extname(f)] || 'application/octet-stream';
      const gz = /text|javascript|json|svg/.test(type) && /gzip/.test(req.headers['accept-encoding'] || '');
      res.writeHead(200, { 'content-type': type, 'cache-control': 'max-age=3600', ...(gz ? { 'content-encoding': 'gzip' } : {}) });
      return gz ? fs.createReadStream(f).pipe(zlib.createGzip()).pipe(res) : fs.createReadStream(f).pipe(res);
    }
    reloadLocales(); // pick up locale edits without restarting
    const g = baseGlobals(req, url);
    const scopeRef = { scope: g };
    const engine = createEngine(g);
    g.__locale = undefined;
    registerSectionsTag(engine, scopeRef);

    let templateName = 'index';
    let m;
    if (url.pathname === '/' || url.pathname === '') {
      g.page_title = 'ARVI | The Premium Online Wine Shop for Fine & Rare Wines';
      g.page_description = 'Fine and rare wines from Bordeaux, Burgundy, Champagne and Italy. Arvino boutiques in Melano, Lugano and Zurich.';
    } else if ((m = url.pathname.match(/^\/products\/([^/]+)/))) {
      const p = data.getProduct(m[1]);
      if (!p) throw Object.assign(new Error('Product not found'), { status: 404 });
      const vid = url.searchParams.get('variant');
      const pick = (vid && p.variants.find((x) => String(x.id) === vid)) || p.first_available_variant || p.variants[0];
      for (const val of p.options_with_values[0].values) val.selected = val.name === pick.option1;
      p.selected_variant = null;
      p.selected_or_first_available_variant = p.first_available_variant || p.variants[0];
      if (vid) {
        const v = p.variants.find((x) => String(x.id) === vid);
        if (v) {
          p.selected_variant = v;
          p.selected_or_first_available_variant = v;
        }
      }
      g.product = p;
      g.page_title = p.title;
      g.page_description = `${p.title} by ${p.vendor}. Buy online from ARVI, Switzerland.`;
      g.request.page_type = 'product';
      templateName = 'product';
    } else if ((m = url.pathname.match(/^\/collections\/([^/]+)/))) {
      const c = data.getCollection(m[1]);
      if (!c) throw Object.assign(new Error('Collection not found'), { status: 404 });
      c.__page = null;
      g.collection = c;
      g.page_title = c.title;
      g.page_description = `${c.title}: ${c.products_count} references from ARVI's cellar. Fine and rare wines delivered in Switzerland.`;
      g.request.page_type = 'collection';
      templateName = 'collection';
    } else if (url.pathname === '/search') {
      const q = url.searchParams.get('q') || '';
      const results = data.search(q);
      g.search = { performed: !!q, terms: q, __results: results, results, results_count: results.length, filters: [], types: ['product'], sort_by: 'relevance', sort_options: [{ value: 'relevance', name: 'Relevance' }, { value: 'price-ascending', name: 'Price, low to high' }] };
      g.page_title = `Search: ${q}`;
      g.request.page_type = 'search';
      templateName = 'search';
    } else if ((m = url.pathname.match(/^\/pages\/([^/]+)/)) && PAGES[m[1]]) {
      g.page = { title: PAGES[m[1]].title, handle: m[1], url: url.pathname, content: '', template_suffix: PAGES[m[1]].template.split('.')[1] };
      g.page_title = PAGES[m[1]].title;
      g.request.page_type = 'page';
      templateName = PAGES[m[1]].template;
    } else if (url.pathname === '/recommendations/products') {
      const p = data.getProduct(url.searchParams.get('product_handle')) || null;
      const pid = url.searchParams.get('product_id');
      const prod = p || data.productHandles().map(data.getProduct).find((x) => String(x.id) === pid);
      // Approximation of Shopify's related intent (the real algorithm is server-side): the producer's other
      // wines first, then wines from the same region. The current product is always excluded, as on Shopify.
      const all = data.productHandles().map(data.getProduct).filter((x) => prod && x.id !== prod.id && x.featured_media);
      const region = (x) => (x.metafields.arvi.regione && x.metafields.arvi.regione.value) || '';
      const byVendor = prod ? all.filter((x) => x.vendor === prod.vendor) : [];
      const byRegion = prod ? all.filter((x) => x.vendor !== prod.vendor && region(x) && region(x) === region(prod)) : [];
      const same = [];
      for (let i = 0; same.length < Number(url.searchParams.get('limit') || 4) && (i < byVendor.length || i < byRegion.length); i++) {
        if (byVendor[i]) same.push(byVendor[i]);
        if (byRegion[i]) same.push(byRegion[i]);
      }
      g.recommendations = { performed: true, products: same, products_count: same.length };
      const sid = url.searchParams.get('section_id') || '';
      const key = sid.split('__')[1] || 'related-products';
      const tpl = readJSON('templates/product.json');
      const html = await renderSectionHTML(engine, 'related-products', sid, tpl.sections[key] || tpl.sections['related-products'], g);
      res.writeHead(200, { 'content-type': 'text/html; charset=utf-8' });
      return res.end(html);
    } else {
      throw Object.assign(new Error('Not found'), { status: 404 });
    }
    const [tname, suffix] = templateName.split('.');
    g.template = { name: tname, suffix: suffix || null, directory: null, toString: () => templateName };
    const html = await renderPage(templateName, g, engine);
    if (/gzip/.test(req.headers['accept-encoding'] || '')) {
      res.writeHead(200, { 'content-type': 'text/html; charset=utf-8', 'content-encoding': 'gzip' });
      return res.end(zlib.gzipSync(html));
    }
    res.writeHead(200, { 'content-type': 'text/html; charset=utf-8' });
    res.end(html);
  } catch (e) {
    console.error(req.url, e.stack || e.message);
    res.writeHead(e.status || 500, { 'content-type': 'text/plain' });
    res.end(String(e.message));
  }
});

server.listen(PORT, () => console.log(`ARVI theme preview on http://localhost:${PORT}`));
