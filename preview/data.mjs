// Store model for the local preview harness.
// Built ONLY from data captured from the ARVI Shopify preview (research/raw/shop/*): real products, prices,
// images, collections and the facts the WIP theme renders from `arvi.*` metafields.
// Nothing here is shipped with the theme.
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
const { Drop } = createRequire(path.resolve('.tooling/package.json'))('liquidjs');

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const RAW = path.join(ROOT, 'research/raw/shop');
const readJSON = (p) => JSON.parse(fs.readFileSync(p, 'utf8'));

const cents = (s) => Math.round(parseFloat(s) * 100);
const handleize = (s) =>
  String(s ?? '')
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .toLowerCase()
    .replace(/['’]/g, '-')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
export { handleize };

// ---------------------------------------------------------------- raw products
const productsRaw = new Map();
const collectionMembers = new Map(); // handle -> [product handles]

function addProducts(list, colHandle) {
  for (const p of list) {
    if (!productsRaw.has(p.handle)) productsRaw.set(p.handle, p);
    if (colHandle) {
      if (!collectionMembers.has(colHandle)) collectionMembers.set(colHandle, []);
      collectionMembers.get(colHandle).push(p.handle);
    }
  }
}
addProducts(readJSON(path.join(RAW, 'products.json_limit=250')).products, null);
for (const f of fs.readdirSync(path.join(RAW, 'col'))) {
  const m = f.match(/^collections_(.+)_products\.json/);
  if (m) addProducts(readJSON(path.join(RAW, 'col', f)).products, m[1]);
}

const collectionsIndex = readJSON(path.join(RAW, 'collections-index.json'));
const wipMeta = fs.existsSync(path.join(RAW, 'wip-meta.json')) ? readJSON(path.join(RAW, 'wip-meta.json')) : {};

// Region membership -> arvi.regione (the store filters on this metafield; value = region name)
const REGION_COLLECTIONS = { champagne: 'Champagne', bordeaux: 'Bordeaux', burgundy: 'Burgundy', toscana: 'Toscana', piemonte: 'Piemonte' };
const COUNTRY = { Champagne: 'France', Bordeaux: 'France', Burgundy: 'France', Toscana: 'Italy', Piemonte: 'Italy' };

// ---------------------------------------------------------------- object builders
let idSeq = 1;
function imageObj(img, alt) {
  if (!img) return null;
  const src = img.src.startsWith('//') ? 'https:' + img.src : img.src;
  const o = {
    id: img.id || idSeq++,
    src,
    url: src,
    width: img.width,
    height: img.height,
    alt: alt || img.alt || '',
    aspect_ratio: img.width / img.height,
    media_type: 'image',
    position: img.position || 1,
    presentation: { focal_point: '50% 50%' },
    __image: true,
  };
  Object.defineProperty(o, 'preview_image', { value: o, enumerable: false });
  Object.defineProperty(o, 'toString', { value: () => src, enumerable: false });
  return o;
}

export function shopImage(filename, width, height, alt = '') {
  return imageObj({ src: `https://cdn.shopify.com/s/files/1/0949/2725/7948/files/${filename}`, width, height }, alt);
}

const productCache = new Map();
export function getProduct(handle) {
  if (!handle) return null;
  if (productCache.has(handle)) return productCache.get(handle);
  const raw = productsRaw.get(handle);
  if (!raw) return null;
  const images = (raw.images || []).map((i) => imageObj(i, raw.title));
  const words = raw.title.split(' ');
  const vintage = words[words.length - 1];

  const variants = raw.variants.map((v) => {
    const fm = images[0] || null;
    return {
      id: v.id,
      title: v.title,
      name: `${raw.title} - ${v.title}`,
      option1: v.option1,
      option2: null,
      option3: null,
      options: [v.option1],
      price: cents(v.price),
      compare_at_price: v.compare_at_price ? cents(v.compare_at_price) : null,
      available: !!v.available,
      sku: v.sku,
      barcode: null,
      featured_media: fm,
      featured_image: fm,
      image: fm,
      requires_shipping: true,
      requires_selling_plan: false,
      selling_plan_allocations: [],
      inventory_management: 'shopify',
      inventory_policy: 'deny',
      inventory_quantity: v.available ? 6 : 0,
      quantity_rule: { min: 1, max: null, increment: 1 },
      quantity_price_breaks: [],
      unit_price_measurement: null,
      store_availabilities: [],
      matched: true,
      url: `/products/${raw.handle}?variant=${v.id}`,
      weight: 1500,
    };
  });
  const prices = variants.map((v) => v.price);
  const firstAvail = variants.find((v) => v.available) || null;
  const selected = firstAvail || variants[0];

  const optionName = (raw.options && raw.options[0] && raw.options[0].name) || 'Formato';
  const optionValues = (raw.options && raw.options[0] && raw.options[0].values) || variants.map((v) => v.option1);

  const p = {
    id: raw.id,
    title: raw.title,
    object_type: 'product',
    handle: raw.handle,
    url: `/products/${raw.handle}`,
    vendor: raw.vendor,
    type: raw.product_type || '',
    tags: raw.tags || [],
    description: raw.body_html || '',
    content: raw.body_html || '',
    published_at: raw.published_at,
    created_at: raw.created_at,
    available: variants.some((v) => v.available),
    price: Math.min(...prices),
    price_min: Math.min(...prices),
    price_max: Math.max(...prices),
    price_varies: new Set(prices).size > 1,
    compare_at_price: null,
    compare_at_price_min: 0,
    compare_at_price_max: 0,
    compare_at_price_varies: false,
    images,
    media: images,
    featured_media: images[0] || null,
    featured_image: images[0] || null,
    variants,
    first_available_variant: firstAvail,
    selected_variant: null,
    selected_or_first_available_variant: selected,
    has_only_default_variant: false,
    requires_selling_plan: false,
    selling_plan_groups: [],
    'quantity_price_breaks_configured?': false,
    'gift_card?': false,
    template_suffix: null,
    options: [optionName],
    metafields: { arvi: {}, reviews: {}, descriptors: {} },
    collections: [],
  };

  p.options_with_values = [
    {
      name: optionName,
      position: 1,
      selected_value: selected ? selected.option1 : null,
      values: optionValues.map((val) => {
        const variant = variants.find((v) => v.option1 === val) || null;
        return {
          id: `${raw.id}-${handleize(val)}`,
          name: val,
          value: val,
          available: !!(variant && variant.available),
          selected: !!(selected && selected.option1 === val),
          variant,
          product_url: null,
          swatch: null,
          toString() {
            return val;
          },
        };
      }),
    },
  ];
  p.options_by_name = { [optionName.toLowerCase()]: p.options_with_values[0] };

  // Facts rendered by the WIP theme from arvi.* metafields (captured from the live preview, EN locale).
  const meta = wipMeta[raw.handle] && wipMeta[raw.handle].en;
  const arvi = p.metafields.arvi;
  if (/^(\d{4}|NV)$/.test(vintage)) arvi.annata = mf(vintage);
  const region = [...collectionMembers.entries()].find(([h, list]) => REGION_COLLECTIONS[h] && list.includes(raw.handle));
  if (region) {
    arvi.regione = mf(REGION_COLLECTIONS[region[0]]);
    arvi.nazione = mf(COUNTRY[REGION_COLLECTIONS[region[0]]]);
  }
  if (meta) {
    for (const [k, v] of meta.specs) {
      if (/colou?r/i.test(k)) arvi.colore = mf(v);
      if (/alcohol/i.test(k)) arvi.alcol = mf(v);
    }
    p.__critics = meta.critics || [];
  } else {
    p.__critics = [];
  }
  productCache.set(handle, p);
  return p;
}

function mf(value) {
  return { value, type: 'single_line_text_field', toString: () => String(value) };
}

export function productHandles() {
  return [...productsRaw.keys()];
}

// ---------------------------------------------------------------- collections
// Counts read from the WIP collection pages for collections missing from collections.json
const KNOWN_COUNTS = { toscana: 31 };
const colCache = new Map();
export function getCollection(handle) {
  if (!handle) return null;
  if (colCache.has(handle)) return colCache.get(handle);
  const meta = collectionsIndex.find((c) => c.handle === handle);
  const members = collectionMembers.get(handle);
  if (!meta && !members) return null;
  const all = (members || []).map(getProduct).filter(Boolean);
  const c = {
    id: idSeq++,
    handle,
    title: meta ? meta.title : handle,
    url: `/collections/${handle}`,
    description: '',
    products_count: meta ? meta.products_count : KNOWN_COUNTS[handle] || all.length,
    all_products_count: meta ? meta.products_count : all.length,
    featured_image: null,
    image: null,
    template_suffix: null,
    sort_by: '',
    default_sort_by: 'manual',
    sort_options: [
      { value: 'manual', name: 'Featured' },
      { value: 'best-selling', name: 'Best selling' },
      { value: 'title-ascending', name: 'Alphabetically, A-Z' },
      { value: 'price-ascending', name: 'Price, low to high' },
      { value: 'price-descending', name: 'Price, high to low' },
      { value: 'created-descending', name: 'Date, new to old' },
    ],
    __all: all,
    __page: null,
    get products() {
      return this.__page || this.__all;
    },
    filters: [],
  };
  c.filters = buildFilters(c);
  colCache.set(handle, c);
  return c;
}

// Mirrors the store's real Search & Discovery filters (names/params observed on the WIP collection pages).
function buildFilters(c) {
  const count = (fn) => {
    const m = new Map();
    for (const p of c.__all) for (const v of [].concat(fn(p)).filter(Boolean)) m.set(v, (m.get(v) || 0) + 1);
    return [...m.entries()];
  };
  const list = (label, param, entries, sort) => {
    const values = entries
      .sort(sort || ((a, b) => b[1] - a[1]))
      .slice(0, 12)
      .map(([v, n]) => ({
        label: v,
        value: v,
        count: n,
        active: false,
        param_name: param,
        url_to_add: `${c.url}?${param}=${encodeURIComponent(v)}`,
        url_to_remove: c.url,
        swatch: null,
        image: null,
      }));
    return { label, param_name: param, type: 'list', presentation: 'text', values, active_values: [], inactive_values: values, url_to_remove: c.url, operator: 'OR' };
  };
  const sizeLabel = (o) => (/^OWC/.test(o) ? null : o);
  const prices = c.__all.map((p) => p.price_max);
  return [
    list('Content (cl)', 'filter.v.option.formato', count((p) => [...new Set(p.variants.map((v) => sizeLabel(v.option1)))]), (a, b) => parseFloat(a[0]) - parseFloat(b[0])),
    list('Vintage', 'filter.p.m.arvi.annata', count((p) => p.metafields.arvi.annata && p.metafields.arvi.annata.value), (a, b) => String(b[0]).localeCompare(String(a[0]))),
    list('Region', 'filter.p.m.arvi.regione', count((p) => p.metafields.arvi.regione && p.metafields.arvi.regione.value)),
    list('Colour', 'filter.p.m.arvi.colore', count((p) => p.metafields.arvi.colore && p.metafields.arvi.colore.value)),
    list('Producer', 'filter.p.m.arvi.produttore', count((p) => p.vendor)),
    {
      label: 'Price',
      param_name: 'filter.v.price',
      type: 'price_range',
      min_value: { value: null, param_name: 'filter.v.price.gte' },
      max_value: { value: null, param_name: 'filter.v.price.lte' },
      range_max: Math.max(0, ...prices),
      active_values: [],
      url_to_remove: c.url,
    },
  ].filter((f) => f.type !== 'list' || f.values.length > 0);
}

// Drops so Liquid can do collections['handle'], collections.all and all_products['handle']
class CollectionsDrop extends Drop {
  liquidMethodMissing(key) {
    if (key === 'all') return getCollection('all') || allCollection();
    return getCollection(String(key)) || undefined;
  }
}
export const collectionsProxy = new CollectionsDrop();

function allCollection() {
  const all = [...productsRaw.keys()].map(getProduct).filter(Boolean);
  const c = getCollection('champagne');
  return Object.assign(Object.create(Object.getPrototypeOf(c)), c, { handle: 'all', title: 'Products', url: '/collections/all', __all: all, products_count: 19023 });
}

class ProductsDrop extends Drop {
  liquidMethodMissing(key) {
    return getProduct(String(key)) || undefined;
  }
}
export const allProductsProxy = new ProductsDrop();

export function search(q) {
  const terms = String(q || '').toLowerCase().split(/\s+/).filter(Boolean);
  const results = [...productsRaw.keys()]
    .map(getProduct)
    .filter((p) => terms.every((t) => (p.title + ' ' + p.vendor).toLowerCase().includes(t)));
  return results;
}

// Navigation mock mirroring the WIP main menu structure (real collection & page handles).
export function linklists() {
  const L = (title, url, links = []) => ({ title, url, links, levels: links.length ? 1 : 0, active: false, child_active: false, current: false, handle: handleize(title), type: 'http_link' });
  const main = {
    handle: 'main-menu',
    title: 'Main menu',
    links: [
      L('Wines', '/collections/wines', [
        L('By type', '/collections/wines', [L('Red wines', '/collections/red-wines'), L('White wines', '/collections/white-wines'), L('Rosé wines', '/collections/rose-wines'), L('Sparkling wines', '/collections/sparkling-wines'), L('Sweet wines', '/collections/sweet-wines'), L('Spirits', '/collections/spirits')]),
        L('France', '/collections/france', [L('Bordeaux', '/collections/bordeaux'), L('Burgundy', '/collections/burgundy'), L('Champagne', '/collections/champagne'), L('Rhône', '/collections/rhone'), L('Other regions', '/collections/other-regions')]),
        L('Italy', '/collections/italy', [L('Piedmont', '/collections/piemonte'), L('Tuscany', '/collections/toscana'), L('Sicily', '/collections/sicilia'), L('Veneto', '/collections/veneto'), L('Trentino-Alto Adige', '/collections/trentino-alto-adige')]),
        L('Europe & New World', '/collections/new-world', [L('Switzerland', '/collections/switzerland'), L('Spain', '/collections/spain'), L('Germany', '/collections/germany'), L('United States', '/collections/united-states'), L('Australia', '/collections/australia')]),
        L('Selections', '/collections/best-sellers', [L('Best sellers', '/collections/best-sellers'), L('Gift ideas', '/collections/gift-ideas'), L('Accessories', '/collections/accessories')]),
      ]),
      L('En Primeur', '/collections/en-primeur'),
      L('Our shops', '/pages/i-nostri-negozi'),
      L('Services', '/pages/la-wine-vault', [L('Wine Vault', '/pages/la-wine-vault'), L('Horeca', '/pages/horeca'), L('What is En Primeur', '/pages/che-cose-en-primeur')]),
      L('Events', '/pages/eventi'),
      L('About', '/pages/chi-siamo'),
      L('Contact', '/pages/contattaci'),
    ],
  };
  for (const l of main.links) l.levels = l.links.length ? (l.links.some((c) => c.links.length) ? 2 : 1) : 0;
  return {
    'main-menu': main,
    footer: { handle: 'footer', title: 'Footer', links: [L('About ARVI', '/pages/chi-siamo'), L('Wine Vault', '/pages/la-wine-vault'), L('Horeca', '/pages/horeca'), L('Events', '/pages/eventi'), L('FAQ', '/pages/faq'), L('Contact', '/pages/contattaci')] },
    'footer-wines': { handle: 'footer-wines', title: 'Wines', links: [L('Bordeaux', '/collections/bordeaux'), L('Burgundy', '/collections/burgundy'), L('Champagne', '/collections/champagne'), L('Italy', '/collections/italy'), L('En Primeur', '/collections/en-primeur'), L('Gift ideas', '/collections/gift-ideas')] },
    'customer-account-main-menu': { handle: 'customer-account-main-menu', links: [] },
  };
}
