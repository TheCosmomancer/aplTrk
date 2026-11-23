document.addEventListener('DOMContentLoaded', () => {
  const searchItems = document.querySelectorAll('.toggle-on-search');
  const searchInput = document.querySelector('#searchbar');
  const PARAM = 'q';

  function filter(rawq) {
    const q = String(rawq ?? '').trim().toLowerCase();
    searchItems.forEach((element) => {
      element.style.display = element.dataset.name.toLowerCase().includes(q) ? '' : 'none';
    });
  }

  function update(q) {
    const url = new URL(location.href);
    q = q.trim();

    if (q) url.searchParams.set(PARAM, q);
    else url.searchParams.delete(PARAM);

    if (url.href === location.href) return;

    const state = { [PARAM]: q };
    history.replaceState(state, '', url);
  }

  function urlLoad() {
    const q = new URLSearchParams(location.search).get(PARAM) ?? '';
    searchInput.value = q;
    filter(q);
  }

  urlLoad();

  let t;
    searchInput.addEventListener('input', (event) => {
    clearTimeout(t);
    t = setTimeout(() => {
        filter(event.target.value);
        update(event.target.value);
    }, 150);
    });
});