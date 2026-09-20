import { CONFIG } from './config.js';

export class Renderer {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.resize();
    window.addEventListener('resize', () => this.resize());
  }

  resize() {
    this.dpr = window.devicePixelRatio || 1;
    this.w = window.innerWidth; this.h = window.innerHeight;
    this.canvas.width = this.w * this.dpr;
    this.canvas.height = this.h * this.dpr;
  }

  draw(world, camera) {
    const ctx = this.ctx, w = this.w, h = this.h;
    ctx.setTransform(this.dpr, 0, 0, this.dpr, 0, 0);
    ctx.fillStyle = '#0d1117';
    ctx.fillRect(0, 0, w, h);

    // World transform: translate to center, scale by zoom, translate by -camera.
    ctx.save();
    ctx.translate(w / 2, h / 2);
    ctx.scale(camera.zoom, camera.zoom);
    ctx.translate(-camera.x, -camera.y);

    const b = camera.bounds(w, h, 60);
    this.drawGrid(ctx, b);
    this.drawBoundary(ctx);
    this.drawFood(ctx, world, b);
    for (const s of world.snakes) if (s.alive) this.drawSnake(ctx, s, b);
    ctx.restore();

    this.drawMinimap(ctx, world);
  }

  drawGrid(ctx, b) {
    const step = 50;
    ctx.strokeStyle = 'rgba(255,255,255,0.05)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    const x0 = Math.floor(b.minX / step) * step, x1 = b.maxX;
    const y0 = Math.floor(b.minY / step) * step, y1 = b.maxY;
    for (let x = x0; x <= x1; x += step) { ctx.moveTo(x, b.minY); ctx.lineTo(x, b.maxY); }
    for (let y = y0; y <= y1; y += step) { ctx.moveTo(b.minX, y); ctx.lineTo(b.maxX, y); }
    ctx.stroke();
  }

  drawBoundary(ctx) {
    ctx.strokeStyle = 'rgba(255,80,80,0.7)';
    ctx.lineWidth = 6;
    ctx.beginPath();
    ctx.arc(0, 0, CONFIG.WORLD_RADIUS, 0, Math.PI * 2);
    ctx.stroke();
  }

  drawFood(ctx, world, b) {
    for (const f of world.food.items) {
      if (f.x < b.minX || f.x > b.maxX || f.y < b.minY || f.y > b.maxY) continue;
      ctx.fillStyle = f.color;
      ctx.globalAlpha = 0.9;
      ctx.beginPath();
      ctx.arc(f.x, f.y, f.r, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.globalAlpha = 1;
  }

  drawSnake(ctx, s, b) {
    const r = s.radius;
    const segs = s.segments;
    ctx.fillStyle = s.color;
    // Draw tail to head so head is on top.
    for (let i = segs.length - 1; i >= 0; i--) {
      const p = segs[i];
      if (p.x < b.minX || p.x > b.maxX || p.y < b.minY || p.y > b.maxY) continue;
      ctx.beginPath();
      ctx.arc(p.x, p.y, r, 0, Math.PI * 2);
      ctx.fill();
    }
    // Outline the head slightly.
    const head = segs[0];
    if (head.x >= b.minX && head.x <= b.maxX && head.y >= b.minY && head.y <= b.maxY) {
      if (s.boosting) {
        ctx.strokeStyle = 'rgba(255,255,255,0.8)';
        ctx.lineWidth = 2;
        ctx.beginPath(); ctx.arc(head.x, head.y, r + 2, 0, Math.PI * 2); ctx.stroke();
      }
      // Eyes.
      const ex = Math.cos(s.angle), ey = Math.sin(s.angle);
      const px = -ey, py = ex;
      const eyeR = Math.max(2, r * 0.35);
      for (const side of [-1, 1]) {
        const cx = head.x + ex * r * 0.4 + px * side * r * 0.5;
        const cy = head.y + ey * r * 0.4 + py * side * r * 0.5;
        ctx.fillStyle = '#fff';
        ctx.beginPath(); ctx.arc(cx, cy, eyeR, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = '#000';
        ctx.beginPath(); ctx.arc(cx + ex * eyeR * 0.4, cy + ey * eyeR * 0.4, eyeR * 0.5, 0, Math.PI * 2); ctx.fill();
      }
      // Name label.
      if (!s.isPlayer) {
        ctx.fillStyle = 'rgba(255,255,255,0.7)';
        ctx.font = `${Math.max(10, r * 1.2)}px system-ui`;
        ctx.textAlign = 'center';
        ctx.fillText(s.name, head.x, head.y - r - 6);
      }
    }
  }

  drawMinimap(ctx, world) {
    const size = 140, pad = 14;
    const cx = this.w - pad - size / 2, cy = this.h - pad - size / 2;
    const scale = (size / 2) / CONFIG.WORLD_RADIUS;
    ctx.fillStyle = 'rgba(0,0,0,0.5)';
    ctx.beginPath(); ctx.arc(cx, cy, size / 2, 0, Math.PI * 2); ctx.fill();
    ctx.strokeStyle = 'rgba(255,80,80,0.6)'; ctx.lineWidth = 1.5; ctx.stroke();
    for (const s of world.snakes) {
      if (!s.alive) continue;
      ctx.fillStyle = s.isPlayer ? '#fff' : s.color;
      ctx.beginPath();
      ctx.arc(cx + s.head.x * scale, cy + s.head.y * scale, s.isPlayer ? 4 : 2.5, 0, Math.PI * 2);
      ctx.fill();
    }
  }
}
