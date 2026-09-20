const report = (path, obj) => fetch('/__' + path + '?' + encodeURIComponent(JSON.stringify(obj))).catch(() => {});
window.addEventListener('error', e => report('error', { msg: e.message, file: e.filename, line: e.lineno }));
window.addEventListener('unhandledrejection', e => report('error', { msg: String(e.reason) }));
setTimeout(() => {
  document.getElementById('btn-start').click();
  const c = document.getElementById('game');
  setInterval(() => c.dispatchEvent(new MouseEvent('mousemove', { clientX: window.innerWidth - 10, clientY: window.innerHeight / 2 })), 200);
  let frames = 0;
  const raf = () => { frames++; requestAnimationFrame(raf); };
  requestAnimationFrame(raf);
  setInterval(() => {
    const p = window.__world && window.__world.player;
    report('hb', { frames, alive: p && p.alive, x: p && Math.round(p.head.x), y: p && Math.round(p.head.y),
      overHidden: document.getElementById('overlay-over').classList.contains('hidden'),
      high: localStorage.getItem('slither_highscore'), overScore: document.getElementById('over-score').textContent });
  }, 3000);
}, 500);
