(() => {
  const menuButton = document.querySelector('.menu-toggle');
  const navigation = document.querySelector('.nav-links');
  if (menuButton && navigation) {
    const closeMenu = () => { navigation.classList.remove('is-open'); menuButton.setAttribute('aria-expanded', 'false'); document.body.classList.remove('menu-open'); };
    menuButton.addEventListener('click', () => { const open = menuButton.getAttribute('aria-expanded') !== 'true'; menuButton.setAttribute('aria-expanded', String(open)); navigation.classList.toggle('is-open', open); document.body.classList.toggle('menu-open', open); });
    navigation.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
    document.addEventListener('keydown', event => { if (event.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') { closeMenu(); menuButton.focus(); } });
    window.matchMedia('(min-width: 601px)').addEventListener('change', event => { if (event.matches) closeMenu(); });
  }
  const states = {
    observe: ['Observe the application', 'Service traffic and infrastructure telemetry describe a changing environment.'],
    decide: ['Choose a placement', 'A scheduling policy uses workload, network, and resource information to place services.'],
    evaluate: ['Measure and repeat', 'Controlled scenarios make policy behavior easier to compare and reproduce.']
  };
  document.querySelectorAll('[data-diagram-mode]').forEach(button => button.addEventListener('click', () => {
    const mode = button.dataset.diagramMode;
    document.querySelectorAll('[data-diagram-mode]').forEach(tab => tab.setAttribute('aria-pressed', String(tab === button)));
    const diagram = document.querySelector('.system-svg');
    const caption = document.querySelector('.diagram-caption');
    if (diagram) diagram.dataset.mode = mode;
    if (caption) { caption.querySelector('strong').textContent = states[mode][0]; caption.querySelector('span').textContent = states[mode][1]; }
  }));
  document.querySelectorAll('[data-filter]').forEach(button => button.addEventListener('click', () => {
    const filter = button.dataset.filter;
    const grid = document.querySelector('.project-grid');
    if (grid) grid.classList.toggle('is-filtered', filter !== 'all');
    let count = 0;
    document.querySelectorAll('[data-project-area]').forEach(card => { card.hidden = filter !== 'all' && card.dataset.projectArea !== filter; if (!card.hidden) count++; });
    document.querySelectorAll('[data-filter]').forEach(tab => tab.setAttribute('aria-pressed', String(tab === button)));
    const status = document.querySelector('#filter-status');
    if (status) status.textContent = `${count} projects shown`;
  }));
  let toastTimer;
  function announce(message) {
    let toast = document.querySelector('.toast');
    if (!toast) { toast = document.createElement('div'); toast.className = 'toast'; toast.setAttribute('role', 'status'); document.body.append(toast); }
    clearTimeout(toastTimer); toast.textContent = message; toast.hidden = false; toastTimer = setTimeout(() => { toast.hidden = true; }, 3500);
  }
  document.querySelectorAll('[data-copy-citation]').forEach(button => button.addEventListener('click', async () => {
    const citation = document.getElementById(button.dataset.copyCitation);
    if (!citation) return;
    try { await navigator.clipboard.writeText(citation.textContent.trim()); announce('Citation copied.'); }
    catch { const selection = window.getSelection(); const range = document.createRange(); range.selectNodeContents(citation); selection.removeAllRanges(); selection.addRange(range); announce('Citation selected. Use your browser’s Copy command.'); }
  }));
  document.querySelectorAll('[data-print]').forEach(button => button.addEventListener('click', () => window.print()));
})();
