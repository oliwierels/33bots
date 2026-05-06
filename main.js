// Nav scroll
const nav = document.getElementById('nav');
window.addEventListener('scroll', () => {
  nav.classList.toggle('scrolled', window.scrollY > 10);
}, { passive: true });

// Mobile menu
const hamburger = document.getElementById('hamburger');
const mobileMenu = document.getElementById('mobileMenu');
hamburger.addEventListener('click', () => mobileMenu.classList.toggle('open'));
mobileMenu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => mobileMenu.classList.remove('open')));

// Fade-up on scroll
const fadeEls = document.querySelectorAll('.tile, .use-item, .process-step, .stat-item');
const io = new IntersectionObserver((entries) => {
  entries.forEach((e, i) => {
    if (e.isIntersecting) {
      setTimeout(() => e.target.classList.add('in'), i * 60);
      io.unobserve(e.target);
    }
  });
}, { threshold: 0.1 });
fadeEls.forEach(el => { el.classList.add('fade-up'); io.observe(el); });

// Contact form
document.getElementById('contactForm').addEventListener('submit', (e) => {
  e.preventDefault();
  const btn = e.target.querySelector('.btn-submit');
  btn.textContent = 'Wysyłanie...';
  btn.disabled = true;
  setTimeout(() => {
    e.target.innerHTML = `
      <div class="form-success">
        <h3>Wiadomość wysłana</h3>
        <p>Odezwiemy się w ciągu 24 godzin roboczych.</p>
      </div>`;
  }, 1000);
});
