// ── SCROLL PROGRESS ──────────────────────────────────────────
const progressBar = document.getElementById('scrollProgress');
const updateProgress = () => {
  const total = document.documentElement.scrollHeight - window.innerHeight;
  progressBar.style.width = total > 0 ? `${(window.scrollY / total) * 100}%` : '0%';
};
window.addEventListener('scroll', updateProgress, { passive: true });

// ── NAV SCROLL ───────────────────────────────────────────────
const nav = document.getElementById('nav');
const onScroll = () => nav.classList.toggle('scrolled', window.scrollY > 16);
window.addEventListener('scroll', onScroll, { passive: true });
onScroll();

// ── MOBILE MENU + HAMBURGER X ────────────────────────────────
const hamburger = document.getElementById('hamburger');
const mobileMenu = document.getElementById('mobileMenu');

hamburger.addEventListener('click', () => {
  const isOpen = mobileMenu.classList.toggle('open');
  hamburger.classList.toggle('open', isOpen);
  hamburger.setAttribute('aria-label', isOpen ? 'Zamknij menu' : 'Menu');
});
mobileMenu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
  mobileMenu.classList.remove('open');
  hamburger.classList.remove('open');
}));

// ── STAT COUNTERS ─────────────────────────────────────────────
const easeOutQuad = t => 1 - (1 - t) * (1 - t);

function animateCounter(el) {
  const target = parseInt(el.dataset.count, 10);
  const suffix = el.dataset.suffix ?? '';
  const duration = 900;
  const start = performance.now();
  const tick = (now) => {
    const t = Math.min((now - start) / duration, 1);
    el.textContent = Math.round(easeOutQuad(t) * target) + suffix;
    if (t < 1) requestAnimationFrame(tick);
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

document.querySelectorAll(
  '.tile, .use-item, .process-step, .stat-item, .testimonial, .faq-item'
).forEach(el => { el.classList.add('fade-up'); io.observe(el); });

// ── FAQ ACCORDION ─────────────────────────────────────────────
document.querySelectorAll('.faq-item').forEach(item => {
  const btn   = item.querySelector('.faq-q');
  const panel = item.querySelector('.faq-a');

  panel.removeAttribute('hidden');
  const naturalHeight = panel.scrollHeight + 'px';
  panel.style.maxHeight = '0px';

  btn.addEventListener('click', () => {
    const opening = !item.classList.contains('open');

    // Collapse all siblings first
    document.querySelectorAll('.faq-item.open').forEach(other => {
      other.classList.remove('open');
      other.querySelector('.faq-a').style.maxHeight = '0px';
      other.querySelector('.faq-q').setAttribute('aria-expanded', 'false');
    });

    if (opening) {
      item.classList.add('open');
      panel.style.maxHeight = naturalHeight;
      btn.setAttribute('aria-expanded', 'true');
    }
  });
});

// ── FORM VALIDATION ──────────────────────────────────────────
const errorMessages = {
  valueMissing:  'To pole jest wymagane',
  typeMismatch:  'Nieprawidłowy format',
};

function validateField(field) {
  const wrapper = field.closest('.form-field');
  if (!wrapper) return true;
  const errEl = wrapper.querySelector('.form-field__err');

  if (!field.validity.valid) {
    const msg = field.validity.valueMissing   ? errorMessages.valueMissing
              : field.validity.typeMismatch   ? errorMessages.typeMismatch
              : 'Sprawdź to pole';
    if (errEl) errEl.textContent = msg;
    wrapper.classList.add('has-error');
    return false;
  }

  wrapper.classList.remove('has-error');
  if (errEl) errEl.textContent = '';
  return true;
}

document.querySelectorAll('.form input[required], .form textarea[required]')
  .forEach(field => {
    field.addEventListener('blur', () => validateField(field));
    field.addEventListener('input', () => {
      if (field.closest('.form-field')?.classList.contains('has-error')) {
        validateField(field);
      }
    });
  });

// ── CONTACT FORM SUBMIT ───────────────────────────────────────
document.getElementById('contactForm').addEventListener('submit', (e) => {
  e.preventDefault();
  const fields = [...e.target.querySelectorAll('input[required], textarea[required]')];
  const allValid = fields.map(validateField).every(Boolean);
  if (!allValid) return;

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

// ── ACTIVE NAV TRACKING ───────────────────────────────────────
const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('.nav__links a[href^="#"]');
window.addEventListener('scroll', () => {
  let current = '';
  sections.forEach(s => { if (window.scrollY >= s.offsetTop - 100) current = s.id; });
  navLinks.forEach(a => {
    a.style.color = a.getAttribute('href') === `#${current}` ? 'var(--text)' : '';
  });
}, { passive: true });

// ── COOKIE BANNER ─────────────────────────────────────────────
const cookieBanner = document.getElementById('cookieBanner');
if (!localStorage.getItem('33bots-cookies')) {
  // Small delay so the slide-up feels intentional, not a flash
  setTimeout(() => cookieBanner.classList.add('visible'), 1200);
}
document.getElementById('cookieAccept').addEventListener('click', () => {
  localStorage.setItem('33bots-cookies', '1');
  cookieBanner.classList.remove('visible');
});
