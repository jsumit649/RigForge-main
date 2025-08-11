// Minimal progressive enhancement for component pickers on build page
// No external libraries; uses existing API endpoints defined in core/urls.py

(function () {
  // Toggle helpers for profile page
  document.addEventListener('click', (e) => {
    const toggleTarget = e.target && e.target.getAttribute('data-toggle');
    if (!toggleTarget) return;
    const el = document.getElementById(toggleTarget);
    if (!el) return;
    const isVisible = getComputedStyle(el).display !== 'none';
    el.style.display = isVisible ? 'none' : 'block';
  });

  const pickerSelector = '.component-picker';
  const listPickerSelector = '.list-picker';

  // Auto-dismiss toasts after 10 seconds (CSS handles animation too)
  function setupToasts() {
    const container = document.getElementById('toast-container');
    if (!container) return;
    const toasts = Array.from(container.querySelectorAll('.toast'));
    // Remove after 10s to avoid tabbing focus or screen-reader clutter
    toasts.forEach((t) => {
      const timer = setTimeout(() => t.remove(), 10000);
      const closeBtn = t.querySelector('.toast-close');
      if (closeBtn) {
        closeBtn.addEventListener('click', () => {
          clearTimeout(timer);
          t.remove();
        });
      }
    });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setupToasts, { once: true });
  } else { setupToasts(); }

  // Small helper to show toast programmatically
  window.showToast = function (text, tag = 'info') {
    const container = document.getElementById('toast-container');
    if (!container) return;
    const toast = document.createElement('div');
    toast.className = `toast toast-${tag}`;
    toast.innerHTML = `<span class="toast-text">${text}</span><button class="toast-close" type="button" aria-label="Close notification">&times;</button>`;
    container.appendChild(toast);
    // Trigger auto-remove and close behavior
    const timer = setTimeout(() => toast.remove(), 10000);
    toast.querySelector('.toast-close').addEventListener('click', () => { clearTimeout(timer); toast.remove(); });
    // Force reflow to ensure CSS animations apply on dynamically added toasts
    // eslint-disable-next-line no-unused-expressions
    toast.offsetHeight;
    toast.style.animation = 'toast-in 300ms ease forwards, toast-out 300ms ease 9.7s forwards';
  };

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
      <button type="button" class="card-pick btn btn-primary">Select</button>
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
      const btn = card.querySelector('.card-pick');
      btn.addEventListener('click', () => {
        const hiddenSelect = pickerEl.querySelector('.hidden-select select');
        const alreadySelected = hiddenSelect && hiddenSelect.value == item.id;
        if (alreadySelected) {
          // Deselect
          hiddenSelect.value = '';
          hiddenSelect.dispatchEvent(new Event('change', { bubbles: true }));
          const selectedEl = pickerEl.querySelector('.picker-selected');
          const priceEl = pickerEl.querySelector('.picker-price');
          if (selectedEl) selectedEl.textContent = selectedEl.getAttribute('data-placeholder') || '';
          if (priceEl) priceEl.textContent = '';
          btn.textContent = 'Select';
          btn.classList.remove('btn-danger');
          btn.classList.add('btn-primary');
          if (window.showToast) window.showToast('Component deselected', 'warning');
        } else {
          // Select
          syncHiddenSelect(pickerEl, item.id, item.name, item.price);
          btn.textContent = 'Deselect';
          btn.classList.remove('btn-primary');
          btn.classList.add('btn-danger');
          pickerEl.classList.remove('open');
          if (window.showToast) window.showToast('Component selected', 'success');
        }
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

    // Checkout-like list pickers
    document.querySelectorAll(listPickerSelector).forEach((picker) => {
      const header = picker.querySelector('.picker-header');
      const panel = picker.querySelector('.picker-panel');
      const hidden = picker.querySelector('input[type="hidden"]');
      if (header) header.addEventListener('click', () => {
        picker.classList.toggle('open');
      });
      picker.querySelectorAll('.list-pick').forEach((btn) => {
        btn.addEventListener('click', () => {
          const id = btn.getAttribute('data-id');
          const selected = picker.querySelector('.picker-selected');
          hidden.value = id;
          if (selected) selected.textContent = btn.parentElement.querySelector('.card-title, .card-desc')?.textContent?.trim() || id;
          picker.classList.remove('open');
          if (window.showToast) window.showToast('Selected', 'success');
        });
      });
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

  // Mobile navbar burger toggle
  function setupBurger() {
    const burger = document.getElementById('navbar-burger');
    const menu = document.querySelector('.navbar-menu');
    if (!burger || !menu) return;
    burger.addEventListener('click', () => {
      const isOpen = menu.classList.toggle('open');
      burger.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setupBurger, { once: true });
  } else { setupBurger(); }
})();

