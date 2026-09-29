// Connect the Spend Gatekeeper to the local application API when available.
// The existing sample check remains usable if the API is offline.
(() => {
  const safe = value => String(value ?? '').replace(/[&<>"']/g, char => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[char]));
  const money = value => new Intl.NumberFormat('en-IN', {
    style: 'currency', currency: 'INR', maximumFractionDigits: 0
  }).format(value || 0);

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
      result.innerHTML = `<div class="decision ${comfortable ? '' : 'warning'}"><span class="decision-mark">${comfortable ? '✦' : '◷'}</span><div><strong>${safe(data.headline)} · ${safe(data.name)}</strong><p>${safe(data.guidance)} After this ${money(data.amount)} purchase, about ${money(data.availableAfter)} remains in the sample available balance. Your final choice is yours. Sample data only.</p></div></div><div class="decision backend-offer"><span class="decision-mark">✧</span><div><strong>${safe(offer.label || 'Sample payment context')}</strong><p>Estimated benefit: ${money(offer.estimatedCashback)}. ${safe(offer.note || '')}</p></div></div>${depreciation}<p class="backend-response-note">Processed by the local OptiSpend application service · No payment was made or blocked.</p>`;
      document.getElementById('trackPurchasedItem')?.addEventListener('click', () => {
        if (typeof assetForm === 'function') assetForm(false, name, amount);
      });
    } catch (error) {
      const note = document.createElement('p');
      note.className = 'backend-response-note';
      note.textContent = `Local backend unavailable; showing the prototype’s sample check. ${error.message}`;
      result.append(note);
    }
  });
})();
