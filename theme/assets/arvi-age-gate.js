/* ARVI age confirmation. Cookie contract identical to the WIP theme (arvi_age_ok=1, 90 days). */
(() => {
  const NAME = 'arvi_age_ok';
  const BOTS =
    /googlebot|google-inspectiontool|storebot-google|adsbot-google|mediapartners-google|bingbot|duckduckbot|applebot|yandex|gptbot|chatgpt-user|oai-searchbot|claudebot|claude-user|claude-searchbot|anthropic-ai|perplexitybot|perplexity-user|chrome-lighthouse/i;

  const hasCookie = () => new RegExp('(^|;\\s*)' + NAME + '=1(;|$)').test(document.cookie);
  const inSession = (write) => {
    try {
      if (write) sessionStorage.setItem(NAME, '1');
      return sessionStorage.getItem(NAME) === '1';
    } catch (e) {
      return false;
    }
  };

  const remember = () => {
    const host = location.hostname;
    let cookie = `${NAME}=1; Max-Age=${90 * 24 * 60 * 60}; Path=/; SameSite=Lax`;
    if (location.protocol === 'https:') cookie += '; Secure';
    if (host === 'arvi.ch' || host.endsWith('.arvi.ch')) cookie += '; Domain=arvi.ch';
    document.cookie = cookie;
    if (!hasCookie()) inSession(true);
  };

  const open = (force) => {
    const tpl = document.getElementById('ArviAgeGateTemplate');
    if (!tpl || document.querySelector('body > dialog.arvi-age')) return;
    if (!force && (BOTS.test(navigator.userAgent) || hasCookie() || inSession(false))) return;
    if (window.Shopify && window.Shopify.designMode && !force) return;

    const dialog = tpl.content.querySelector('dialog').cloneNode(true);
    if (typeof dialog.showModal !== 'function') return;
    const step = (name) => dialog.querySelector(`[data-arvi-age-step="${name}"]`);
    let answered = false;

    dialog.addEventListener('cancel', (event) => event.preventDefault());
    dialog.addEventListener('click', (event) => {
      const action = event.target.closest('[data-arvi-age]');
      if (!action) return;
      const value = action.getAttribute('data-arvi-age');
      if (value === 'yes') {
        answered = true;
        remember();
        dialog.close();
        dialog.remove();
        document.documentElement.classList.remove('arvi-age-open');
        document.dispatchEvent(new CustomEvent('arvi:age-confirmed'));
      } else if (value === 'no') {
        step('ask').hidden = true;
        step('denied').hidden = false;
        dialog.querySelector('[data-arvi-age="back"]').focus();
      } else if (value === 'back') {
        step('denied').hidden = true;
        step('ask').hidden = false;
        dialog.querySelector('[data-arvi-age="yes"]').focus();
      }
    });
    dialog.addEventListener('close', () => {
      if (!answered && dialog.isConnected) dialog.showModal();
    });

    document.body.appendChild(dialog);
    document.documentElement.classList.add('arvi-age-open');
    dialog.showModal();
  };

  window.arviAgeGate = { open: () => open(true) };
  open(false);
})();
