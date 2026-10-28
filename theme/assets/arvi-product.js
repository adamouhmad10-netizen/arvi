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
