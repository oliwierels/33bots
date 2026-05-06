// ── SCROLL PROGRESS ──────────────────────────────────────────
const progressBar = document.getElementById('scrollProgress');
const updateProgress = () => {
  const scrolled = window.scrollY;
  const total = document.documentElement.scrollHeight - window.innerHeight;
  progressBar.style.width = total > 0 ? `${(scrolled / total) * 100}%` : '0%';
};
window.addEventListener('scroll', updateProgress, { passive: true });

// ── NAV SCROLL ───────────────────────────────────────────────
const nav = document.getElementById('nav');
const onScroll = () => nav.classList.toggle('scrolled', window.scrollY > 16);
window.addEventListener('scroll', onScroll, { passive: true });
onScroll();

// ── MOBILE MENU ──────────────────────────────────────────────
const hamburger = document.getElementById('hamburger');
const mobileMenu = document.getElementById('mobileMenu');
hamburger.addEventListener('click', () => mobileMenu.classList.toggle('open'));
mobileMenu.querySelectorAll('a').forEach(a =>
  a.addEventListener('click', () => mobileMenu.classList.remove('open'))
);

// ── STAT COUNTERS ─────────────────────────────────────────────
// Ease-out quad: starts fast, decelerates
const easeOutQuad = t => 1 - (1 - t) * (1 - t);

function animateCounter(el) {
  const target = parseInt(el.dataset.count, 10);
  const suffix = el.dataset.suffix ?? '';
  const duration = 900;
  const start = performance.now();

  const tick = (now) => {
    const elapsed = Math.min(now - start, duration);
    const val = Math.round(easeOutQuad(elapsed / duration) * target);
    el.textContent = val + suffix;
    if (elapsed < duration) requestAnimationFrame(tick);
    else el.textContent = target + suffix;
  };
  requestAnimationFrame(tick);
}

const counterObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (!entry.isIntersecting) return;
    animateCounter(entry.target);
    counterObserver.unobserve(entry.target);
  });
}, { threshold: 0.5 });

document.querySelectorAll('[data-count]').forEach(el => counterObserver.observe(el));

// ── FADE UP (staggered per sibling) ──────────────────────────
const io = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (!entry.isIntersecting) return;
    const siblings = [...entry.target.parentElement.children]
      .filter(el => el.classList.contains('fade-up'));
    const idx = siblings.indexOf(entry.target);
    setTimeout(() => entry.target.classList.add('in'), idx * 70);
    io.unobserve(entry.target);
  });
}, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });

document.querySelectorAll('.tile, .use-item, .process-step, .stat-item, .testimonial, .faq-item')
  .forEach(el => { el.classList.add('fade-up'); io.observe(el); });

// ── FAQ ACCORDION ─────────────────────────────────────────────
document.querySelectorAll('.faq-item').forEach(item => {
  const btn = item.querySelector('.faq-q');
  const answer = item.querySelector('.faq-a');

  // Pre-measure natural height for smooth animation
  answer.removeAttribute('hidden');
  const fullHeight = answer.scrollHeight + 'px';
  answer.style.maxHeight = '0px';

  btn.addEventListener('click', () => {
    const isOpen = item.classList.contains('open');

    // Close all others
    document.querySelectorAll('.faq-item.open').forEach(openItem => {
      if (openItem === item) return;
      openItem.classList.remove('open');
      openItem.querySelector('.faq-a').style.maxHeight = '0px';
      openItem.querySelector('.faq-q').setAttribute('aria-expanded', 'false');
    });

    // Toggle current
    if (isOpen) {
      item.classList.remove('open');
      answer.style.maxHeight = '0px';
      btn.setAttribute('aria-expanded', 'false');
    } else {
      item.classList.add('open');
      answer.style.maxHeight = fullHeight;
      btn.setAttribute('aria-expanded', 'true');
    }
  });
});

// ── ACTIVE NAV TRACKING ───────────────────────────────────────
const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('.nav__links a[href^="#"]');
const trackActive = () => {
  let current = '';
  sections.forEach(s => { if (window.scrollY >= s.offsetTop - 100) current = s.id; });
  navLinks.forEach(a => {
    a.style.color = a.getAttribute('href') === `#${current}` ? 'var(--text)' : '';
  });
};
window.addEventListener('scroll', trackActive, { passive: true });

// ── CONTACT FORM ──────────────────────────────────────────────
document.getElementById('contactForm').addEventListener('submit', (e) => {
  e.preventDefault();
  const btn = e.target.querySelector('.btn-submit');
  btn.textContent = 'Wysyłanie...';
  btn.disabled = true;
  setTimeout(() => {
    e.target.innerHTML = `<div class="form-success">
      <h3>Wiadomość wysłana</h3>
      <p>Odezwiemy się w ciągu 24 godzin roboczych.</p>
    </div>`;
  }, 900);
});
