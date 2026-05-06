// Nav scroll
const nav = document.getElementById('nav');
const onScroll = () => nav.classList.toggle('scrolled', window.scrollY > 16);
window.addEventListener('scroll', onScroll, { passive: true });
onScroll();

// Mobile menu
const hamburger = document.getElementById('hamburger');
const mobileMenu = document.getElementById('mobileMenu');
hamburger.addEventListener('click', () => mobileMenu.classList.toggle('open'));
mobileMenu.querySelectorAll('a').forEach(a =>
  a.addEventListener('click', () => mobileMenu.classList.remove('open'))
);

// Staggered fade-up on scroll
const io = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (!entry.isIntersecting) return;
    const siblings = [...entry.target.parentElement.children].filter(el => el.classList.contains('fade-up'));
    const idx = siblings.indexOf(entry.target);
    setTimeout(() => entry.target.classList.add('in'), idx * 70);
    io.unobserve(entry.target);
  });
}, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });

document.querySelectorAll('.tile, .use-item, .process-step, .stat-item')
  .forEach(el => { el.classList.add('fade-up'); io.observe(el); });

// Contact form
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

// Active nav link tracking
const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('.nav__links a[href^="#"]');
const trackActive = () => {
  let current = '';
  sections.forEach(s => { if (window.scrollY >= s.offsetTop - 100) current = s.id; });
  navLinks.forEach(a => {
    const active = a.getAttribute('href') === `#${current}`;
    a.style.color = active ? 'var(--text)' : '';
  });
};
window.addEventListener('scroll', trackActive, { passive: true });
