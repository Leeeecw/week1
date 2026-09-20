// 초기화: 렌더링 + 네비 활성화 + 섹션 reveal

function setupSectionObserver() {
  const sections = document.querySelectorAll('.section[data-section]');
  const navLinks = document.querySelectorAll('.nav__links a');

  const setActive = (id) => {
    navLinks.forEach((a) => {
      a.classList.toggle('is-active', a.getAttribute('href') === `#${id}`);
    });
  };

  // reveal: 한 번 보이면 유지
  const revealObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          revealObserver.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.1 }
  );

  // active nav: 화면 상단 영역에 걸친 섹션을 활성으로
  const activeObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) setActive(entry.target.id);
      });
    },
    { rootMargin: '-40% 0px -55% 0px', threshold: 0 }
  );

  sections.forEach((s) => {
    revealObserver.observe(s);
    activeObserver.observe(s);
  });
}

document.addEventListener('DOMContentLoaded', () => {
  renderAll(RESUME);
  setupSectionObserver();
});
