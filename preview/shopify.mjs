// Minimal Shopify Liquid runtime for local preview of the theme (LiquidJS + Shopify tags/filters).
// It renders the real theme files; Shopify platform behaviour (checkout, cart API, apps, Search & Discovery)
// is NOT emulated beyond what is needed to draw pages.
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
const require = createRequire(path.resolve('.tooling/package.json'));
const { Liquid, Tag, Hash, Tokenizer, Drop } = require('liquidjs');

import * as data from './data.mjs';

export const THEME = path.resolve('theme');
const read = (p) => fs.readFileSync(path.join(THEME, p), 'utf8');
const readJSON = (p) => JSON.parse(read(p).replace(/^\/\*[\s\S]*?\*\/\s*/, ''));

// ----------------------------------------------------------------- locales
function loadLocale(code) {
  const file = code === 'en' ? 'locales/en.default.json' : `locales/${code}.json`;
  return readJSON(file);
}
let enLocale = loadLocale('en');
export function reloadLocales() {
  enLocale = loadLocale('en');
}
function lookup(obj, key) {
  return key.split('.').reduce((o, k) => (o == null ? undefined : o[k]), obj);
}

// ----------------------------------------------------------------- helpers
const kw = (args) => {
  const o = {};
  const pos = [];
  for (const a of args) {
    if (Array.isArray(a) && a.length === 2 && typeof a[0] === 'string') o[a[0]] = a[1];
    else pos.push(a);
  }
  return [o, pos];
};
const attr = (o) =>
  Object.entries(o)
    .filter(([k, v]) => v !== null && v !== undefined && v !== false && (v !== '' || k === 'alt'))
    .map(([k, v]) => (v === true ? k : `${k}="${String(v).replace(/"/g, '&quot;')}"`))
    .join(' ');

class Color extends Drop {
  constructor(hex) {
    super();
    hex = String(hex || '#000000').replace('#', '');
    if (hex.length === 3) hex = hex.split('').map((c) => c + c).join('');
    this.red = parseInt(hex.slice(0, 2), 16);
    this.green = parseInt(hex.slice(2, 4), 16);
    this.blue = parseInt(hex.slice(4, 6), 16);
    this.alpha = 1;
    this.rgb = `${this.red} ${this.green} ${this.blue}`;
    this.rgba = `${this.red} ${this.green} ${this.blue} / 1.0`;
    this.hex = '#' + hex.toUpperCase();
  }
  valueOf() {
    return this.hex;
  }
  toString() {
    return this.hex;
  }
}
const toColor = (c) => (c instanceof Color ? c : new Color(String(c)));
const brightness = (c) => (c.red * 299 + c.green * 587 + c.blue * 114) / 1000;
const shift = (c, pct) => {
  const f = (v) => Math.max(0, Math.min(255, Math.round(v + (pct / 100) * 255)));
  return new Color('#' + [f(c.red), f(c.green), f(c.blue)].map((v) => v.toString(16).padStart(2, '0')).join(''));
};

// Shopify fonts (only the Inter faces used by settings are resolved to real CDN files seen on the store)
const FONT_FILES = {
  inter_n4: 'inter_n4.b2a3f24c19b4de56e8871f609e73ca7f6d2e2bb9.woff2',
  inter_n7: 'inter_n7.02711e6b374660cfc7915d1afc1c204e633421e4.woff2',
  inter_i4: 'inter_i4.feae1981dda792ab80d117249d9c7e0f1017e5b3.woff2',
  inter_i7: 'inter_i7.b377bcd4cc0f160622a22d638ae7e2cd9b86ea4c.woff2',
};
function font(handle) {
  const m = String(handle).match(/^([a-z_]+)_([ni])(\d)$/);
  const fam = m ? m[1] : 'inter';
  return {
    handle,
    family: fam.charAt(0).toUpperCase() + fam.slice(1),
    fallback_families: 'sans-serif',
    style: m && m[2] === 'i' ? 'italic' : 'normal',
    weight: m ? Number(m[3]) * 100 : 400,
    'system?': false,
    toString() {
      return handle;
    },
  };
}

function imageURL(img, opts = {}) {
  if (!img) return '';
  if (typeof img === 'string') return img;
  const src = img.src || img.url || String(img);
  const q = [];
  if (opts.width) q.push(`width=${opts.width}`);
  if (opts.height) q.push(`height=${opts.height}`);
  if (opts.crop) q.push(`crop=${opts.crop}`);
  return src + (q.length ? (src.includes('?') ? '&' : '?') + q.join('&') : '');
}

// ----------------------------------------------------------------- engine
export function createEngine(ctxGlobals) {
  const engine = new Liquid({
    root: [path.join(THEME, 'sections'), path.join(THEME, 'snippets'), path.join(THEME, 'layout')],
    partials: [path.join(THEME, 'snippets')],
    extname: '.liquid',
    dynamicPartials: true,
    strictFilters: false,
    strictVariables: false,
    lenientIf: true,
    jsTruthy: false,
    cache: false,
    outputEscape: undefined,
    globals: ctxGlobals,
  });

  const locale = () => ctxGlobals.__locale || enLocale;

  // ----- translation
  engine.registerFilter('t', function (key, ...args) {
    const [o] = kw(args);
    let v = lookup(locale(), key);
    if (v === undefined) v = lookup(enLocale, key);
    if (v === undefined) return key;
    if (typeof v === 'object') v = o.count === 1 ? v.one ?? v.other : v.other ?? v.one;
    return String(v).replace(/\{\{\s*(\w+)\s*\}\}/g, (_, k) => (o[k] !== undefined ? o[k] : ''));
  });

  // ----- urls & assets
  engine.registerFilter('asset_url', (f) => `/assets/${f}`);
  engine.registerFilter('file_url', (f) => `https://cdn.shopify.com/s/files/1/0949/2725/7948/files/${f}`);
  engine.registerFilter('shopify_asset_url', (f) => `https://cdn.shopify.com/shopifycloud/${f}`);
  engine.registerFilter('global_asset_url', (f) => `https://cdn.shopify.com/s/global/${f}`);
  engine.registerFilter('stylesheet_tag', (u, ...args) => {
    const [o] = kw(args);
    return `<link href="${u}" rel="stylesheet" type="text/css" media="${o.media || 'all'}" />`;
  });
  engine.registerFilter('script_tag', (u) => `<script src="${u}" type="text/javascript"></script>`);
  engine.registerFilter('preload_tag', (u, ...args) => {
    const [o] = kw(args);
    return `<link href="${u}" rel="preload" ${attr(o)}>`;
  });
  engine.registerFilter('inline_asset_content', (f) => {
    try {
      return read('assets/' + f);
    } catch {
      return '';
    }
  });
  engine.registerFilter('link_to', (text, url) => `<a href="${url}">${text}</a>`);
  engine.registerFilter('within', (url) => url);
  engine.registerFilter('url_for_type', (t) => `/collections/types?q=${encodeURIComponent(t)}`);
  engine.registerFilter('url_for_vendor', (t) => `/collections/vendors?q=${encodeURIComponent(t)}`);
  engine.registerFilter('handleize', (s) => data.handleize(s));
  engine.registerFilter('handle', (s) => data.handleize(s));
  engine.registerFilter('camelize', (s) => String(s).replace(/[-_\s]+(.)?/g, (_, c) => (c ? c.toUpperCase() : '')));
  engine.registerFilter('pluralize', (n, a, b) => (n === 1 ? a : b));
  engine.registerFilter('md5', (s) => String(s).length.toString(16));
  engine.registerFilter('default_errors', () => '');
  engine.registerFilter('highlight', (s) => s);
  engine.registerFilter('structured_data', (obj) => {
    if (!obj || !obj.variants) return '{}';
    return JSON.stringify({
      '@context': 'http://schema.org/',
      '@type': 'Product',
      name: obj.title,
      url: obj.url,
      brand: { '@type': 'Brand', name: obj.vendor },
      image: obj.featured_media ? [imageURL(obj.featured_media, { width: 1920 })] : [],
      offers: obj.variants.map((v) => ({
        '@type': 'Offer',
        sku: v.sku,
        price: (v.price / 100).toFixed(2),
        priceCurrency: 'CHF',
        availability: v.available ? 'http://schema.org/InStock' : 'http://schema.org/OutOfStock',
        url: v.url,
      })),
    });
  });
  engine.registerFilter('standard_event_data', () => '{}');

  // ----- money
  const fmt = (c) => {
    const n = (Number(c) || 0) / 100;
    return n.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  };
  engine.registerFilter('money', (c) => `CHF ${fmt(c)}`);
  engine.registerFilter('money_with_currency', (c) => `CHF ${fmt(c)}`);
  engine.registerFilter('money_without_currency', (c) => fmt(c));
  engine.registerFilter('money_without_trailing_zeros', (c) => `CHF ${fmt(c).replace(/\.00$/, '')}`);
  engine.registerFilter('money_amount', (c) => fmt(c));

  // ----- images
  engine.registerFilter('image_url', (img, ...args) => {
    const [o] = kw(args);
    const url = imageURL(img, o);
    const s = new String(url);
    s.__img = img;
    return s;
  });
  engine.registerFilter('img_url', (img, size) => {
    const w = String(size || '').match(/^(\d+)x/);
    return imageURL(img, w ? { width: w[1] } : {});
  });
  engine.registerFilter('image_tag', (urlObj, ...args) => {
    const [o] = kw(args);
    const img = (urlObj && urlObj.__img) || null;
    const base = String(urlObj).replace(/([?&])width=\d+&?/, '$1').replace(/[?&]$/, '');
    const maxW = img && img.width ? img.width : 2000;
    const widths = String(o.widths || '352, 832, 1200, 1920')
      .split(',')
      .map((w) => parseInt(w))
      .filter((w) => w && w <= maxW);
    const join = base.includes('?') ? '&' : '?';
    const srcset = widths.map((w) => `${base}${join}width=${w} ${w}w`).join(', ');
    let width = o.width !== undefined ? o.width : img ? img.width : undefined;
    let height = o.height;
    if (height === undefined && img && img.width) height = width ? Math.round((width / img.width) * img.height) : img.height;
    if (o.height === null) height = undefined;
    const a = {
      src: String(urlObj),
      alt: o.alt !== undefined ? o.alt : img ? img.alt : '',
      srcset: o.srcset === null ? null : srcset,
      width,
      height,
      loading: o.loading,
      sizes: o.sizes,
      class: o.class,
      style: o.style,
      fetchpriority: o.fetchpriority,
      id: o.id,
    };
    if (o.preload) a.fetchpriority = 'high';
    return `<img ${attr(a)}>`;
  });
  engine.registerFilter('placeholder_svg_tag', (name, cls) => {
    const svg = (() => {
      try {
        return read(`assets/${name}.svg`);
      } catch {
        return '';
      }
    })();
    return svg
      ? svg.replace('<svg', `<svg class="${cls || 'placeholder-svg'}"`)
      : `<svg class="${cls || 'placeholder-svg'}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 525 525"><rect width="525" height="525" fill="#E8E3D8"/></svg>`;
  });
  engine.registerFilter('media_tag', (m) => (m ? `<img src="${imageURL(m, { width: 1200 })}" alt="${m.alt || ''}">` : ''));
  engine.registerFilter('video_tag', () => '');
  engine.registerFilter('external_video_tag', () => '');
  engine.registerFilter('external_video_url', () => '');
  engine.registerFilter('model_viewer_tag', () => '');
  engine.registerFilter('metafield_tag', (m) => (m ? String(m.value ?? m) : ''));
  engine.registerFilter('metafield_text', (m) => (m ? String(m.value ?? m) : ''));
  engine.registerFilter('payment_type_svg_tag', (t) => `<svg class="icon icon--full-color" viewBox="0 0 38 24" width="38" height="24" role="img" aria-label="${t}"><rect width="38" height="24" rx="3" fill="#F2EEE6"/><text x="19" y="15" font-size="7" text-anchor="middle" fill="#1C1A17" font-family="Arial">${String(t).slice(0, 6).toUpperCase()}</text></svg>`);
  engine.registerFilter('payment_button', () => '');
  engine.registerFilter('payment_terms', () => '');
  engine.registerFilter('login_button', () => '');
  engine.registerFilter('item_count_for_variant', () => 0);
  engine.registerFilter('line_items_for', () => []);
  engine.registerFilter('unit_price_with_measurement', () => '');
  engine.registerFilter('format_address', (a) => (a ? Object.values(a).join('<br>') : ''));
  engine.registerFilter('time_tag', (d) => `<time>${d}</time>`);
  engine.registerFilter('default_pagination', (p) => (p && p.parts ? p.parts.map((x) => (x.is_link ? `<a href="${x.url}">${x.title}</a>` : `<span>${x.title}</span>`)).join(' ') : ''));

  // ----- fonts
  engine.registerFilter('font_face', (f) => {
    if (!f || !f.handle) return '';
    const file = FONT_FILES[f.handle] || FONT_FILES.inter_n4;
    return `@font-face { font-family: ${f.family}; font-weight: ${f.weight}; font-style: ${f.style}; font-display: swap; src: url("https://myarvi.myshopify.com/cdn/fonts/inter/${file}") format("woff2"); }`;
  });
  engine.registerFilter('font_modify', (f, prop, val) => {
    if (!f || !f.handle) return f;
    let h = f.handle;
    if (prop === 'weight') h = h.replace(/\d$/, val === 'bold' ? '7' : String(val).replace(/00$/, '') || '4');
    if (prop === 'style') h = h.replace(/_[ni]/, val === 'italic' ? '_i' : '_n');
    return font(h);
  });
  engine.registerFilter('font_url', (f) => `https://myarvi.myshopify.com/cdn/fonts/inter/${FONT_FILES[f && f.handle] || FONT_FILES.inter_n4}`);

  // ----- colors
  engine.registerFilter('color_brightness', (c) => brightness(toColor(c)));
  engine.registerFilter('color_lighten', (c, p) => shift(toColor(c), +p));
  engine.registerFilter('color_darken', (c, p) => shift(toColor(c), -p));
  engine.registerFilter('color_to_rgb', (c) => {
    const x = toColor(c);
    return `rgb(${x.red}, ${x.green}, ${x.blue})`;
  });
  engine.registerFilter('color_modify', (c, prop, v) => {
    const x = toColor(c);
    return prop === 'alpha' ? `rgba(${x.red}, ${x.green}, ${x.blue}, ${v})` : x;
  });
  engine.registerFilter('color_extract', (c, k) => toColor(c)[k]);
  engine.registerFilter('color_mix', (a) => a);
  engine.registerFilter('color_contrast', () => 7);

  // ----- tags
  const blockTag = (name, render) => {
    engine.registerTag(
      name,
      class extends Tag {
        constructor(token, remain, liquid, parser) {
          super(token, remain, liquid);
          this.args = token.args;
          this.tpls = [];
          const stream = parser
            .parseStream(remain)
            .on('tag:end' + name, () => stream.stop())
            .on('template', (t) => this.tpls.push(t))
            .on('end', () => {
              throw new Error(`tag ${name} not closed`);
            });
          stream.start();
        }
        *render(ctx, emitter) {
          const inner = yield this.liquid.renderer.renderTemplates(this.tpls, ctx);
          const out = yield* render.call(this, ctx, inner);
          emitter.write(out);
        }
      }
    );
  };
  const rawTag = (name, wrap) => {
    engine.registerTag(
      name,
      class extends Tag {
        constructor(token, remain, liquid) {
          super(token, remain, liquid);
          this.raw = '';
          while (remain.length) {
            const t = remain.shift();
            if (t.name === 'end' + name) return;
            this.raw += t.getText ? t.getText() : t.input.slice(t.begin, t.end);
          }
        }
        render(ctx, emitter) {
          emitter.write(wrap(this.raw));
        }
      }
    );
  };
  rawTag('schema', () => '');
  rawTag('doc', () => '');
  rawTag('javascript', (s) => `<script>${s}</script>`);
  blockTag('style', function* (ctx, inner) {
    return `<style data-shopify>${inner}</style>`;
  });
  blockTag('stylesheet', function* (ctx, inner) {
    return `<style>${inner}</style>`;
  });
  blockTag('form', function* (ctx, inner) {
    const m = this.args.match(/^\s*['"]([^'"]+)['"]\s*(?:,\s*([\s\S]*))?$/);
    const type = m ? m[1] : '';
    const parts = m && m[2] ? m[2].split(',') : [];
    if (parts.length && !parts[0].includes(':')) parts.shift();
    const h = yield new Hash(parts.join(',')).render(ctx);
    const actions = { product: '/cart/add', localization: '/localization', contact: '/contact#contact_form', customer: '/contact#newsletter', cart: '/cart', 'storefront_password': '/password' };
    const a = { method: 'post', action: actions[type] || '/', id: h.id, class: h.class, 'accept-charset': 'UTF-8', 'data-type': h['data-type'], novalidate: h.novalidate ? 'novalidate' : null, enctype: type === 'product' ? 'multipart/form-data' : null };
    return `<form ${attr(a)}><input type="hidden" name="form_type" value="${type}"><input type="hidden" name="utf8" value="✓">${inner}</form>`;
  });
  engine.registerTag(
    'paginate',
    class extends Tag {
      constructor(token, remain, liquid, parser) {
        super(token, remain, liquid);
        const m = token.args.match(/^\s*([\w.\[\]'"]+)\s+by\s+([\w.\[\]'"]+)/);
        this.expr = m[1];
        this.by = m[2];
        this.tpls = [];
        const stream = parser
          .parseStream(remain)
          .on('tag:endpaginate', () => stream.stop())
          .on('template', (t) => this.tpls.push(t));
        stream.start();
      }
      *render(ctx, emitter) {
        const coll = yield engine.evalValue(this.expr.replace(/\.(products|results|articles)$/, ''), ctx);
        const by = Number(yield engine.evalValue(this.by, ctx)) || 24;
        const page = Number(ctxGlobals.__query.page || 1);
        const listKey = /\.results$/.test(this.expr) ? 'results' : 'products';
        const all = coll ? (listKey === 'results' ? coll.__results || [] : coll.__all || []) : [];
        const pages = Math.max(1, Math.ceil(all.length / by));
        if (coll) {
          if (listKey === 'products') coll.__page = all.slice((page - 1) * by, page * by);
          else coll.results = all.slice((page - 1) * by, page * by);
        }
        const base = ctxGlobals.request.path;
        const parts = [];
        for (let i = 1; i <= Math.min(pages, 5); i++) parts.push({ title: i, url: `${base}?page=${i}`, is_link: i !== page });
        const total = coll && coll.products_count ? Math.max(all.length, 0) : all.length;
        ctx.push({
          paginate: {
            current_page: page,
            current_offset: (page - 1) * by,
            items: total,
            page_size: by,
            pages,
            parts,
            previous: page > 1 ? { url: `${base}?page=${page - 1}`, title: 'Previous' } : null,
            next: page < pages ? { url: `${base}?page=${page + 1}`, title: 'Next' } : null,
            page_param: 'page',
          },
        });
        const out = yield this.liquid.renderer.renderTemplates(this.tpls, ctx);
        ctx.pop();
        emitter.write(out);
      }
    }
  );

  return engine;
}

// ----------------------------------------------------------------- settings resolution
export function resolveURL(u) {
  if (!u || typeof u !== 'string') return u;
  return u
    .replace(/^shopify:\/\/collections\/(.+)$/, '/collections/$1')
    .replace(/^shopify:\/\/products\/(.+)$/, '/products/$1')
    .replace(/^shopify:\/\/pages\/(.+)$/, '/pages/$1')
    .replace(/^shopify:\/\/blogs\/(.+)$/, '/blogs/$1');
}

const SHOP_IMAGES = {
  'logoarvi.jpg': [3171, 3525, 'ARVI'],
  'logoarvi_white.png': [3171, 3525, 'ARVI'],
};

export function resolveSetting(type, value, linklists) {
  if (value === undefined || value === null) return value;
  switch (type) {
    case 'collection':
      return data.getCollection(value) || null;
    case 'product':
      return data.getProduct(value) || null;
    case 'product_list':
      return (value || []).map(data.getProduct).filter(Boolean);
    case 'collection_list':
      return (value || []).map(data.getCollection).filter(Boolean);
    case 'image_picker': {
      const m = String(value).match(/^shopify:\/\/shop_images\/(.+)$/);
      if (!m) return null;
      const [w, h, alt] = SHOP_IMAGES[m[1]] || [2000, 2000, ''];
      return data.shopImage(m[1], w, h, alt);
    }
    case 'url':
      return resolveURL(value);
    case 'link_list':
      return linklists[value] || null;
    case 'color':
      return new Color(value);
    case 'font_picker':
      return font(value);
    default:
      return value;
  }
}

export function defaultsFrom(schemaSettings = []) {
  const o = {};
  for (const s of schemaSettings) if (s.id) o[s.id] = s.default;
  return o;
}

export function schemaOf(sectionType) {
  const src = read(`sections/${sectionType}.liquid`);
  const m = src.match(/\{%-?\s*schema\s*-?%\}([\s\S]*?)\{%-?\s*endschema\s*-?%\}/);
  return m ? JSON.parse(m[1]) : {};
}

export function globalSettings(linklists) {
  const schema = readJSON('config/settings_schema.json');
  const dataJ = readJSON('config/settings_data.json');
  const cur = typeof dataJ.current === 'string' ? dataJ.presets[dataJ.current] : dataJ.current;
  const types = {};
  const out = {};
  for (const group of schema) for (const s of group.settings || []) if (s.id) {
    types[s.id] = s.type;
    out[s.id] = s.default;
  }
  Object.assign(out, cur);
  for (const [k, v] of Object.entries(out)) {
    if (k === 'color_schemes') continue;
    out[k] = resolveSetting(types[k], v, linklists);
  }
  out.color_schemes = Object.entries(cur.color_schemes).map(([id, s]) => {
    const settings = {};
    for (const [k, v] of Object.entries(s.settings)) settings[k] = k === 'background_gradient' ? v : new Color(v);
    return { id, settings, toString: () => id };
  });
  return out;
}
