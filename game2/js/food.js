import { CONFIG } from './config.js';
import { SpatialHash } from './spatial.js';

export class FoodManager {
  constructor() {
    this.items = [];
    this.hash = new SpatialHash(CONFIG.GRID_CELL);
    for (let i = 0; i < CONFIG.FOOD_COUNT; i++) this.spawnRandom();
  }

  randomColor() {
    return CONFIG.COLORS[Math.floor(Math.random() * CONFIG.COLORS.length)];
  }

  spawnRandom() {
    const R = CONFIG.WORLD_RADIUS * 0.97;
    const ang = Math.random() * Math.PI * 2;
    const dist = Math.sqrt(Math.random()) * R;
    const r = CONFIG.FOOD_RADIUS_MIN + Math.random() * (CONFIG.FOOD_RADIUS_MAX - CONFIG.FOOD_RADIUS_MIN);
    this.items.push({
      x: Math.cos(ang) * dist, y: Math.sin(ang) * dist,
      r, value: r / 4, color: this.randomColor(), natural: true,
    });
  }

  spawnAt(x, y, r, value, color) {
    this.items.push({ x, y, r, value, color, natural: false });
  }

  rebuildHash() {
    this.hash.clear();
    for (const f of this.items) this.hash.insert(f, f.x, f.y);
  }

  // Removes eaten food near (x,y) within radius; returns total value eaten.
  eat(x, y, radius) {
    let gained = 0;
    const eaten = [];
    this.hash.query(x, y, radius + CONFIG.FOOD_RADIUS_MAX, f => {
      if (f.eaten) return;
      const d = Math.hypot(f.x - x, f.y - y);
      if (d < radius + f.r) { f.eaten = true; eaten.push(f); gained += f.value; }
    });
    if (eaten.length) {
      this.items = this.items.filter(f => !f.eaten);
      for (const f of eaten) if (f.natural) this.spawnRandom();
    }
    return gained;
  }
}
