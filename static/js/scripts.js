// Minimal progressive enhancement for component pickers on build page
// No external libraries; uses existing API endpoints defined in core/urls.py

(function () {
  const pickerSelector = '.component-picker';

  function moneyINR(value) {
    try {
      return new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(Number(value));
    } catch (_) {
      return `₹${value}`;
    }
  }

  function buildApiPath(type) {
    switch (type) {
      case 'cpu': return '/api/cpus/';
      case 'gpu': return '/api/gpus/';
      case 'motherboard': return '/api/motherboards/';
      case 'ram': return '/api/ram/';
      case 'psu': return '/api/power-supplies/';
      case 'ssdstorage': return '/api/ssdstorage/';
      case 'hddstorage': return '/api/hddstorage/';
      case 'case': return '/api/cases/';
      case 'coolers': return '/api/coolers/';
      default: return '';
    }
  }

  async function fetchComponents(type) {
    const path = buildApiPath(type);
    if (!path) return [];
    const res = await fetch(path, { headers: { 'Accept': 'application/json' } });
    if (!res.ok) return [];
    return await res.json();
  }

  function renderCard(item) {
    // Basic fields: name, description, price
    const container = document.createElement('div');
    container.className = 'component-card';
    container.innerHTML = `
      <div class="card-title">${item.name ?? ''}</div>
      <div class="card-desc">${(item.description ?? '').toString().slice(0, 120)}</div>
      <div class="card-price">${moneyINR(item.price ?? 0)}</div>
      <button type="button" class="card-pick">Select</button>
    `;
    return container;
  }

  function syncHiddenSelect(pickerEl, id, label, price) {
    // Hidden select is the Django form field; set its value then update UI text
    const hiddenSelect = pickerEl.querySelector('.hidden-select select');
    if (!hiddenSelect) return;
    hiddenSelect.value = id;
    // Ensure change event in case server-side validation depends on it
    hiddenSelect.dispatchEvent(new Event('change', { bubbles: true }));

    const selectedEl = pickerEl.querySelector('.picker-selected');
    const priceEl = pickerEl.querySelector('.picker-price');
    if (selectedEl) selectedEl.textContent = label || selectedEl.getAttribute('data-placeholder') || '';
    if (priceEl) priceEl.textContent = price != null ? moneyINR(price) : '';
  }

  async function openPicker(pickerEl) {
    const type = pickerEl.getAttribute('data-type');
    const panel = pickerEl.querySelector('.picker-panel');
    const grid = pickerEl.querySelector('.component-grid');
    if (!panel || !grid) return;

    pickerEl.classList.toggle('open');
    if (!pickerEl.classList.contains('open')) return;

    // If already populated, don't re-fetch each time
    if (grid.childElementCount > 0) return;

    panel.classList.add('loading');
    const items = await fetchComponents(type);
    panel.classList.remove('loading');

    items.forEach((item) => {
      const card = renderCard(item);
      card.querySelector('.card-pick').addEventListener('click', () => {
        syncHiddenSelect(pickerEl, item.id, item.name, item.price);
        pickerEl.classList.remove('open');
      });
      grid.appendChild(card);
    });
  }

  function attachPickers() {
    document.querySelectorAll(pickerSelector).forEach((picker) => {
      const header = picker.querySelector('.picker-header');
      if (header) header.addEventListener('click', () => openPicker(picker));

      // Hide the raw select but keep it in DOM for form submit/validation
      const hiddenSelect = picker.querySelector('.hidden-select select');
      if (hiddenSelect) {
        hiddenSelect.style.display = 'none';
        // Initialize selected text if value is pre-filled (edit mode)
        const currentOption = hiddenSelect.selectedOptions && hiddenSelect.selectedOptions[0];
        if (currentOption && currentOption.value) {
          const priceAttr = currentOption.getAttribute('data-price');
          const price = priceAttr ? Number(priceAttr) : undefined;
          syncHiddenSelect(picker, currentOption.value, currentOption.textContent, price);
        }
      }
    });
  }

  // Click outside to close any open picker
  document.addEventListener('click', (e) => {
    const open = document.querySelector(`${pickerSelector}.open`);
    if (!open) return;
    if (!open.contains(e.target)) open.classList.remove('open');
  });

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', attachPickers);
  } else {
    attachPickers();
  }
})();

