// Nav scroll effect
const nav = document.getElementById('nav');
window.addEventListener('scroll', () => {
  nav.classList.toggle('scrolled', window.scrollY > 20);
});

// Mobile menu
const hamburger = document.getElementById('hamburger');
const mobileMenu = document.getElementById('mobileMenu');
hamburger.addEventListener('click', () => {
  mobileMenu.classList.toggle('open');
});
mobileMenu.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', () => mobileMenu.classList.remove('open'));
});

// Fade-in on scroll
const fadeEls = document.querySelectorAll(
  '.about-card, .offer-card, .usecase, .step, .spec-item, .specs-card'
);
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('visible');
      observer.unobserve(e.target);
    }
  });
}, { threshold: 0.12 });

fadeEls.forEach((el, i) => {
  el.classList.add('fade-in');
  el.style.transitionDelay = `${(i % 3) * 80}ms`;
  observer.observe(el);
});

// Contact form handler
const form = document.getElementById('contactForm');
form.addEventListener('submit', (e) => {
  e.preventDefault();
  const btn = form.querySelector('button[type="submit"]');
  btn.textContent = 'Wysyłanie...';
  btn.disabled = true;

  // Simulate async send — replace with real endpoint
  setTimeout(() => {
    form.innerHTML = `
      <div class="form-success">
        <h3>Wiadomość wysłana!</h3>
        <p>Dziękujemy za zapytanie. Odezwiemy się w ciągu 24 godzin roboczych.</p>
      </div>
    `;
  }, 1200);
});

// Smooth active link highlight
const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('.nav__links a[href^="#"]');
window.addEventListener('scroll', () => {
  let current = '';
  sections.forEach(s => {
    if (window.scrollY >= s.offsetTop - 120) current = s.id;
  });
  navLinks.forEach(a => {
    a.style.color = a.getAttribute('href') === `#${current}` ? 'var(--text)' : '';
  });
});
