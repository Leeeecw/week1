import { CONFIG } from './config.js';

export class Camera {
  constructor() {
    this.x = 0; this.y = 0; this.zoom = 1;
  }
  follow(snake, dt) {
    const k = 1 - Math.exp(-10 * dt);
    this.x += (snake.head.x - this.x) * k;
    this.y += (snake.head.y - this.y) * k;
    const target = Math.max(CONFIG.ZOOM_MIN, Math.min(CONFIG.ZOOM_MAX, 1 / (1 + snake.length * CONFIG.ZOOM_FACTOR)));
    this.zoom += (target - this.zoom) * (1 - Math.exp(-3 * dt));
  }
  toScreen(wx, wy, w, h) {
    return { x: (wx - this.x) * this.zoom + w / 2, y: (wy - this.y) * this.zoom + h / 2 };
  }
  // Visible world bounds with margin.
  bounds(w, h, margin = 50) {
    const hw = w / 2 / this.zoom + margin, hh = h / 2 / this.zoom + margin;
    return { minX: this.x - hw, maxX: this.x + hw, minY: this.y - hh, maxY: this.y + hh };
  }
}
