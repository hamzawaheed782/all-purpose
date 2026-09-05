const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

document.querySelectorAll('.card').forEach((card, i) => {
  const img = card.querySelector('.card-image');
  if (!img) return;
  const base = img.getAttribute('data-color') || '#ffd6e0';
  img.style.background = base;

  card.addEventListener('mousemove', (e) => {
    if (prefersReduced) return;
    const rect = card.getBoundingClientRect();
    const x = ((e.clientX - rect.left) / rect.width) * 100;
    const y = ((e.clientY - rect.top) / rect.height) * 100;
    img.style.background = `
      radial-gradient(circle at ${x}% ${y}%, ${lighten(base, 35)}, ${base})
    `;
  });

  card.addEventListener('mouseleave', () => {
    img.style.background = base;
  });
});

function lighten(hex, percent) {
  const num = parseInt(hex.replace('#', ''), 16);
  const amt = Math.round(2.55 * percent);
  const R = Math.min(255, (num >> 16) + amt);
  const G = Math.min(255, ((num >> 8) & 0x00ff) + amt);
  const B = Math.min(255, (num & 0x0000ff) + amt);
  return `rgb(${R}, ${G}, ${B})`;
}

const track = document.querySelector('.track');
if (track) {
  const items = [...track.children];
  items.forEach((el) => {
    const clone = el.cloneNode(true);
    track.appendChild(clone);
  });
}

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.style.animationPlayState = 'running';
      } else {
        entry.target.style.animationPlayState = 'paused';
      }
    });
  },
  { threshold: 0.1 }
);

document.querySelectorAll('.track').forEach((t) => observer.observe(t));
