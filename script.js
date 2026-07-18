const navToggle = document.querySelector('.nav-toggle');
const mainNav = document.querySelector('#main-nav');

if (navToggle && mainNav) {
  navToggle.addEventListener('click', () => {
    const open = navToggle.getAttribute('aria-expanded') === 'true';
    navToggle.setAttribute('aria-expanded', String(!open));
    mainNav.classList.toggle('open', !open);
  });
  mainNav.querySelectorAll('a').forEach((link) => link.addEventListener('click', () => {
    navToggle.setAttribute('aria-expanded', 'false');
    mainNav.classList.remove('open');
  }));
}

const resumeLanguageButtons = document.querySelectorAll('[data-resume-language]');
const resumePanels = document.querySelectorAll('[data-resume-panel]');

if (resumeLanguageButtons.length && resumePanels.length) {
  resumeLanguageButtons.forEach((button) => button.addEventListener('click', () => {
    const language = button.dataset.resumeLanguage;
    resumeLanguageButtons.forEach((item) => {
      item.setAttribute('aria-pressed', String(item.dataset.resumeLanguage === language));
    });
    resumePanels.forEach((panel) => {
      panel.hidden = panel.dataset.resumePanel !== language;
    });
    document.documentElement.lang = language;
  }));
}

const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if (!reducedMotion && 'IntersectionObserver' in window) {
  document.documentElement.classList.add('js');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08 });
  document.querySelectorAll('.reveal').forEach((node) => observer.observe(node));
}
