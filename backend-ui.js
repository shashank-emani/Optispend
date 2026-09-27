// Progressive enhancement for the local purchase analytics API.
// The regular prototype check remains available when the API is offline.
(() => {
  const root = document.getElementById('viewRoot');
  if (!root) return;

  const money = value => new Intl.NumberFormat('en-IN', {
    style: 'currency', currency: 'INR', maximumFractionDigits: 0
  }).format(value || 0);
  const safe = value => String(value ?? '').replace(/[&<>"']/g, char => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[char]));

  async function refreshAnalytics() {
    const panel = document.getElementById('backendAnalytics');
    if (!panel) return;
    const content = panel.querySelector('[data-analytics-content]');
    try {
      const response = await fetch('/api/analytics/summary', { cache: 'no-store' });
      if (!response.ok) throw new Error('Backend unavailable');
      const data = await response.json();
      const categories = Object.entries(data.categories || {})
        .map(([label, count]) => `${safe(label)} ${count}`)
        .join(' · ') || 'No checks yet';
      content.innerHTML = `<strong>${data.checks} sample checks processed</strong><small>${categories}</small><small>Memory only · resets when the local service stops</small>`;
    } catch {
      content.innerHTML = '<strong>Local analytics service is offline</strong><small>Start OptiSpend with <code>python3 backend/server.py</code> to enable it.</small>';
    }
  }

  function addAnalyticsPanel() {
    if (!document.getElementById('purchaseName') || document.getElementById('backendAnalytics')) return;
    const grid = root.querySelector('.page-grid');
    if (!grid) return;
    const panel = document.createElement('section');
    panel.className = 'feature-panel wide';
    panel.id = 'backendAnalytics';
    panel.innerHTML = '<div class="split"><div><h3>How the local check is processed</h3><p>OptiSpend uses sample figures and keeps the final choice with you.</p></div><span class="tag">Local demo analytics</span></div><div class="backend-analytics-content" data-analytics-content><small>Checking local service…</small></div><p class="backend-privacy-note">Your item name, link, and exact amount are used only to prepare this response. The in-memory analytics counts broad category, amount band, and guidance outcome; no account data or transaction is accessed.</p>';
    grid.append(panel);
    refreshAnalytics();
  }

  document.addEventListener('click', async event => {
    const button = event.target.closest('#evaluateSpend');
    if (!button) return;
    const name = document.getElementById('purchaseName')?.value.trim() || 'This purchase';
    const amount = Number(document.getElementById('purchaseAmount')?.value);
    const category = document.getElementById('spendCategory')?.value || 'Other';
    if (!Number.isFinite(amount) || amount <= 0) return;

    const result = document.getElementById('spendResult');
    try {
      const response = await fetch('/api/purchase-check', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, amount, category })
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || 'Could not check this purchase.');

      const comfortable = data.outcome === 'within_plan';
      const type = /car|vehicle|auto/i.test(name) ? 'Car' :
        /phone|iphone|android/i.test(name) ? 'Phone' :
        /laptop|computer|tablet|gadget|watch/i.test(name) ? 'Gadget' : '';
      const rate = type === 'Car' ? 12 : type === 'Phone' ? 25 : type === 'Gadget' ? 20 : 0;
      const depreciation = type ? `<div class="decision depreciation-nudge"><span class="decision-mark">◒</span><div><strong>A little resale context, just in case</strong><p>A broad ${rate}% annual ${type.toLowerCase()} depreciation assumption would put a ${money(data.amount)} purchase near ${money(Math.round(data.amount * (1 - rate / 100)))} after one year. Actual resale varies by exact model, condition, and market; the value it brings you matters too.</p><button class="text-link" id="trackPurchasedItem">If you buy it, track its value&nbsp; →</button></div></div>` : '';
      const offer = data.offer || {};
      result.innerHTML = `<div class="decision ${comfortable ? '' : 'warning'}"><span class="decision-mark">${comfortable ? '✦' : '◷'}</span><div><strong>${safe(data.headline)} · ${safe(data.name)}</strong><p>${safe(data.guidance)} After this ${money(data.amount)} purchase, about ${money(data.availableAfter)} remains in the sample available balance. Your final choice is yours. Sample data only.</p></div></div><div class="decision backend-offer"><span class="decision-mark">✧</span><div><strong>${safe(offer.label || 'Sample payment context')}</strong><p>Estimated benefit: ${money(offer.estimatedCashback)}. ${safe(offer.note || '')}</p></div></div>${depreciation}<p class="backend-response-note">Processed by the local OptiSpend analytics service · No payment was made or blocked.</p>`;
      document.getElementById('trackPurchasedItem')?.addEventListener('click', () => {
        if (typeof assetForm === 'function') assetForm(false, name, amount);
      });
      refreshAnalytics();
    } catch (error) {
      const note = document.createElement('p');
      note.className = 'backend-response-note';
      note.textContent = `Local backend unavailable; showing the prototype’s sample check. ${error.message}`;
      result.append(note);
    }
  });

  new MutationObserver(addAnalyticsPanel).observe(root, { childList: true, subtree: true });
  addAnalyticsPanel();
})();
