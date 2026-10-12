/* POLIS documentation interactions — dependency-free, accessible by keyboard. */
(() => {
  'use strict';
  const body = document.body;
  const base = body.dataset.base || '/';
  const lang = body.dataset.lang === 'en' ? 'en' : 'pt';
  const messages = {
    pt: {themeLight:'Ativar tema claro', themeDark:'Ativar tema escuro',copy:'Código copiado',done:'Copiado!',copyError:'Não foi possível copiar; selecione o código manualmente.', empty:'Pesquise comandos, conceitos ou fluxos do POLIS.', none:'Nenhum resultado encontrado. Tente termos diferentes.', searchError:'Não foi possível carregar a busca. Verifique a conexão com o site.'},
    en: {themeLight:'Use light theme', themeDark:'Use dark theme',copy:'Code copied',done:'Copied!',copyError:'Could not copy; select the code manually.', empty:'Search POLIS commands, concepts, or workflows.', none:'No results found. Try different terms.', searchError:'Could not load search. Check your connection to the website.'}
  };
  const msg = messages[lang];
  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => Array.from(root.querySelectorAll(selector));
  const showToast = (message) => {
    const toast = $('[data-toast]');
    if (!toast) return;
    toast.textContent = message;
    toast.classList.add('visible');
    window.clearTimeout(showToast.timer);
    showToast.timer = window.setTimeout(() => toast.classList.remove('visible'), 1900);
  };

  // Persist theme when storage is available; respect OS preference otherwise.
  $$('[data-theme-toggle]').forEach(button => button.addEventListener('click', () => {
    const next = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
    document.documentElement.dataset.theme = next;
    try { localStorage.setItem('polis-theme', next); } catch (_) { /* private browsing */ }
    const themeColor = $('meta[name="theme-color"]');
    if (themeColor) themeColor.content = next === 'dark' ? '#091622' : '#f5f2e9';
    button.setAttribute('aria-label', next === 'dark' ? msg.themeLight : msg.themeDark);
  }));

  async function copyText(value) {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(value);
      return;
    }
    const area = document.createElement('textarea');
    area.value = value;
    area.setAttribute('readonly', '');
    area.style.cssText = 'position:fixed;left:-9999px;top:0;';
    body.appendChild(area);
    area.select();
    try {
      if (!document.execCommand('copy')) throw Error('Cópia indisponível');
    } finally { area.remove(); }
  }
  document.addEventListener('click', async (event) => {
    const button = event.target.closest('[data-copy-code], [data-copy-target]');
    if (!button) return;
    const selector = button.dataset.copyTarget;
    const source = selector ? document.getElementById(selector) : button.closest('.code-block')?.querySelector('pre code');
    if (!source) return;
    try {
      await copyText(source.textContent.trim());
      showToast(msg.copy);
      const label = $('span', button);
      if (label) {
        const old = label.textContent;
        label.textContent = msg.done;
        window.setTimeout(() => { label.textContent = old; }, 1400);
      }
    } catch (_) { showToast(msg.copyError); }
  });

  // Mobile navigation drawer.
  const sidebar = $('#docs-sidebar');
  const navOverlay = $('[data-nav-overlay]');
  const navTrigger = $('[data-open-nav]');
  const mobileNavQuery = window.matchMedia('(max-width: 760px)');
  const isMobileNav = () => mobileNavQuery.matches;
  function closeNav(restoreFocus = false) {
    if (!sidebar) return;
    const wasOpen = body.classList.contains('nav-open');
    body.classList.remove('nav-open');
    if (navOverlay) navOverlay.hidden = true;
    navTrigger?.setAttribute('aria-expanded', 'false');
    sidebar.inert = isMobileNav();
    if (restoreFocus && wasOpen && isMobileNav()) navTrigger?.focus();
  }
  function openNav() {
    if (!sidebar || !isMobileNav()) return;
    sidebar.inert = false;
    body.classList.add('nav-open');
    if (navOverlay) navOverlay.hidden = false;
    navTrigger?.setAttribute('aria-expanded', 'true');
    $('[data-close-nav]', sidebar)?.focus();
  }
  if (sidebar) sidebar.inert = isMobileNav();
  navTrigger?.addEventListener('click', () => body.classList.contains('nav-open') ? closeNav(true) : openNav());
  $('[data-close-nav]', sidebar)?.addEventListener('click', () => closeNav(true));
  navOverlay?.addEventListener('click', () => closeNav(true));
  $$('.docs-sidebar a').forEach(link => link.addEventListener('click', () => closeNav()));
  window.addEventListener('resize', () => {
    if (!isMobileNav()) closeNav();
    else if (sidebar && !body.classList.contains('nav-open')) sidebar.inert = true;
  });

  // Search uses a lightweight generated index (built from every Markdown page).
  const overlay = $('[data-search-overlay]');
  const input = $('#site-search');
  const results = $('#search-results');
  let index = null;
  let selectedIndex = 0;
  let currentResults = [];
  let opener = null;
  const normalize = str => (str || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  function score(item, terms) {
    const title = normalize(item.title), desc = normalize(item.description), text = normalize(item.text), group = normalize(item.group);
    let total = 0;
    for (const term of terms) {
      let n = 0;
      if (title === term) n += 120;
      if (title.includes(term)) n += 55;
      if (title.split(/\s+/).some(w => w.startsWith(term))) n += 25;
      if (group.includes(term)) n += 12;
      if (desc.includes(term)) n += 14;
      if (text.includes(term)) n += 3;
      if (!n) return 0;
      total += n;
    }
    return total;
  }
  function renderResults() {
    const terms = normalize(input.value).trim().split(/\s+/).filter(Boolean);
    results.replaceChildren();
    currentResults = !terms.length || !index ? [] : index.map(item => ({ ...item, score: score(item, terms) })).filter(x => x.score > 0).sort((a,b) => b.score-a.score || a.title.localeCompare(b.title)).slice(0,9);
    selectedIndex = 0;
    input.setAttribute('aria-expanded', overlay && !overlay.hidden ? 'true' : 'false');
    input.removeAttribute('aria-activedescendant');
    if (!currentResults.length) {
      const empty = document.createElement('div');
      empty.className = 'search-empty';
      empty.textContent = !terms.length ? msg.empty : msg.none;
      results.appendChild(empty);
      return;
    }
    for (let i = 0; i < currentResults.length; i++) {
      const item = currentResults[i];
      const a = document.createElement('a');
      a.id = `search-result-${i}`;
      a.href = item.url;
      a.className = 'search-result' + (i === selectedIndex ? ' selected' : '');
      a.setAttribute('role', 'option');
      a.setAttribute('aria-selected', i === selectedIndex ? 'true' : 'false');
      const main = document.createElement('span'); main.className = 'search-result-main';
      const title = document.createElement('span'); title.className = 'search-result-title'; title.textContent = item.title;
      const desc = document.createElement('span'); desc.className = 'search-result-sub'; desc.textContent = item.description;
      const group = document.createElement('span'); group.className = 'search-result-group'; group.textContent = item.group;
      main.append(title, desc); a.append(main, group);
      a.addEventListener('mouseenter', () => selectResult(i));
      results.append(a);
    }
    input.setAttribute('aria-activedescendant', 'search-result-0');
  }
  function selectResult(next) {
    const links = $$('.search-result', results);
    if (!links.length) return;
    selectedIndex = (next + links.length) % links.length;
    links.forEach((link, i) => {
      link.classList.toggle('selected', i === selectedIndex);
      link.setAttribute('aria-selected', i === selectedIndex ? 'true' : 'false');
    });
    input.setAttribute('aria-activedescendant', links[selectedIndex].id);
    links[selectedIndex].scrollIntoView({ block: 'nearest' });
  }
  async function openSearch() {
    if (!overlay || !overlay.hidden) return;
    opener = body.classList.contains('nav-open') ? navTrigger : document.activeElement;
    if (body.classList.contains('nav-open')) closeNav();
    overlay.hidden = false;
    body.classList.add('modal-open');
    input.value = '';
    input.focus();
    renderResults();
    if (!index) {
      try {
        const response = await fetch(base + (lang === 'en' ? 'en/search.json' : 'search.json'));
        if (!response.ok) throw Error('Index unavailable');
        index = await response.json();
        renderResults();
      } catch (_) {
        const empty = document.createElement('div');
        empty.className = 'search-empty';
        empty.textContent = msg.searchError;
        results.replaceChildren(empty);
      }
    }
  }
  function closeSearch() {
    if (!overlay || overlay.hidden) return;
    overlay.hidden = true;
    body.classList.remove('modal-open');
    input.setAttribute('aria-expanded', 'false');
    input.removeAttribute('aria-activedescendant');
    if (opener instanceof HTMLElement) opener.focus();
  }
  $$('[data-open-search]').forEach(x => x.addEventListener('click', openSearch));
  $$('[data-close-search]').forEach(x => x.addEventListener('click', closeSearch));
  input?.addEventListener('input', renderResults);
  input?.addEventListener('keydown', e => {
    if (e.key === 'ArrowDown') { e.preventDefault(); selectResult(selectedIndex + 1); }
    if (e.key === 'ArrowUp') { e.preventDefault(); selectResult(selectedIndex - 1); }
    if (e.key === 'Enter' && currentResults.length) { e.preventDefault(); location.href = currentResults[selectedIndex].url; }
  });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') { if (!overlay.hidden) closeSearch(); else if (body.classList.contains('nav-open')) closeNav(true); return; }
    if ((e.key === '/' && !e.ctrlKey && !e.metaKey) || ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k')) {
      if (e.target.closest('input,textarea,[contenteditable="true"]')) return;
      e.preventDefault();
      if (overlay.hidden) openSearch(); else closeSearch();
    }
    if (e.key === 'Tab' && overlay && !overlay.hidden) {
      const focusable = $$('input,button,a[href]', overlay).filter(el => el.offsetParent !== null);
      if (!focusable.length) return;
      const first = focusable[0], last = focusable[focusable.length-1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    } else if (e.key === 'Tab' && body.classList.contains('nav-open') && sidebar) {
      const focusable = $$('button,a[href]', sidebar).filter(el => el.offsetParent !== null);
      if (!focusable.length) return;
      const first = focusable[0], last = focusable[focusable.length-1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  });

  // Keep the local table of contents in sync with visible headings.
  const tocLinks = $$('.docs-toc a[href^="#"]');
  if (tocLinks.length && 'IntersectionObserver' in window) {
    const visible = new Set();
    const headers = tocLinks.map(a => $(a.getAttribute('href'))).filter(Boolean);
    const tocObserver = new IntersectionObserver(entries => {
      entries.forEach(entry => entry.isIntersecting ? visible.add(entry.target.id) : visible.delete(entry.target.id));
      const active = headers.find(h => visible.has(h.id)) || [...headers].reverse().find(h => h.getBoundingClientRect().top < 160) || headers[0];
      tocLinks.forEach(a => a.classList.toggle('toc-current', a.getAttribute('href') === '#' + active.id));
    }, { rootMargin: '-105px 0px -65% 0px', threshold: 0 });
    headers.forEach(header => tocObserver.observe(header));
  }
})();
