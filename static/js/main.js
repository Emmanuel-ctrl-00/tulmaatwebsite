// Off-canvas nav toggle — shared across all pages
document.addEventListener('DOMContentLoaded', function () {
  var topbar = document.querySelector('[data-topbar]');
  var toggle = document.querySelector('[data-menu-toggle]');
  var panel = document.querySelector('[data-nav-panel]');
  var scrim = panel ? panel.querySelector('.nav-panel__scrim') : null;

  if (!toggle || !panel) return;

  function openNav() {
    panel.classList.add('open');
    topbar.classList.add('nav-open');
    toggle.setAttribute('aria-expanded', 'true');
    document.body.style.overflow = 'hidden';
  }

  function closeNav() {
    panel.classList.remove('open');
    topbar.classList.remove('nav-open');
    toggle.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
  }

  toggle.addEventListener('click', function () {
    var isOpen = panel.classList.contains('open');
    isOpen ? closeNav() : openNav();
  });

  if (scrim) scrim.addEventListener('click', closeNav);

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeNav();
  });

  // Close the panel after tapping a link (useful once it navigates/scrolls)
  panel.querySelectorAll('.nav-links a').forEach(function (link) {
    link.addEventListener('click', closeNav);
  });
});
