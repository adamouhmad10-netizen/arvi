/* ARVI: keep the "Price on request" enquiry in sync with Dawn's variant changes. */
if (!customElements.get('arvi-request-price')) {
  customElements.define(
    'arvi-request-price',
    class ArviRequestPrice extends HTMLElement {
      connectedCallback() {
        this.zero = (this.dataset.zeroVariants || '').split(',').filter(Boolean);
        if (typeof subscribe !== 'function' || typeof PUB_SUB_EVENTS === 'undefined') return;
        this.unsubscribe = subscribe(PUB_SUB_EVENTS.variantChange, (event) => {
          const data = event && event.data;
          if (!data || !data.variant || data.sectionId !== this.dataset.section) return;
          this.classList.toggle('hidden', !this.zero.includes(String(data.variant.id)));
        });
      }

      disconnectedCallback() {
        if (this.unsubscribe) this.unsubscribe();
      }
    }
  );
}

/* ARVI: present raw "Formato" sizes (e.g. "75.00", "150.00") as "75 cl" in variant pickers.
   Display only: option values sent to the cart are unchanged. */
(() => {
  const SIZE = /^\s*(\d+(?:[.,]\d+)?)\s*$/;
  const label = (raw) => {
    const n = parseFloat(String(raw).replace(',', '.'));
    return `${Number.isInteger(n) ? n : n.toString()} cl`;
  };
  const relabel = (root) => {
    root.querySelectorAll('variant-selects option, [data-arvi-formato="misura"] option').forEach((option) => {
      const text = option.textContent;
      const [value, rest] = text.split(' - ');
      if (SIZE.test(value)) option.textContent = label(value) + (rest ? ` - ${rest}` : '');
    });
    root.querySelectorAll('variant-selects input[type="radio"] + label').forEach((el) => {
      const node = [...el.childNodes].find((n) => n.nodeType === 3 && SIZE.test(n.textContent));
      if (node) node.textContent = label(node.textContent);
    });
  };
  const start = () => {
    document.querySelectorAll('product-info').forEach((info) => {
      relabel(info);
      new MutationObserver(() => relabel(info)).observe(info, { childList: true, subtree: true });
    });
  };
  document.readyState === 'loading' ? document.addEventListener('DOMContentLoaded', start) : start();
})();
