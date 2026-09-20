import { CONFIG } from './config.js';
import { Snake } from './snake.js';
import { FoodManager } from './food.js';
import { SpatialHash } from './spatial.js';
import { initAI, steerAI } from './ai.js';

const AI_NAMES = ['Viper', 'Cobra', 'Mamba', 'Python', 'Adder', 'Boa', 'Krait', 'Asp',
  'Taipan', 'Racer', 'Coral', 'Garter', 'Anaconda', 'Sidewinder', 'Rattler', 'Copperhead'];

export class World {
  constructor() {
    this.food = new FoodManager();
    this.segHash = new SpatialHash(CONFIG.GRID_CELL);
    this.snakes = [];
    this.player = null;
  }

  randomSpawn() {
    const R = CONFIG.WORLD_RADIUS * 0.7;
    const ang = Math.random() * Math.PI * 2;
    const dist = Math.sqrt(Math.random()) * R;
    return { x: Math.cos(ang) * dist, y: Math.sin(ang) * dist, angle: Math.random() * Math.PI * 2 };
  }

  init() {
    this.snakes = [];
    const ps = this.randomSpawn();
    this.player = new Snake({ ...ps, color: CONFIG.PLAYER_COLOR, isPlayer: true, name: 'You' });
    this.snakes.push(this.player);
    for (let i = 0; i < CONFIG.AI_COUNT; i++) {
      const s = new Snake({
        ...this.randomSpawn(),
        color: CONFIG.COLORS[i % CONFIG.COLORS.length],
        name: AI_NAMES[i % AI_NAMES.length],
      });
      initAI(s);
      this.snakes.push(s);
    }
    this.food.rebuildHash();
    this.rebuildSegHash();
  }

  rebuildSegHash() {
    this.segHash.clear();
    for (const s of this.snakes) {
      if (!s.alive) continue;
      // Skip the first few segments near the head so heads don't self-trigger; other snakes still check all.
      for (let i = 0; i < s.segments.length; i++) {
        const p = s.segments[i];
        this.segHash.insert({ x: p.x, y: p.y, snake: s, index: i }, p.x, p.y);
      }
    }
  }

  kill(snake) {
    snake.alive = false;
    snake.boosting = false;
    snake.deadTime = 0;
    // Drop food along body.
    for (let i = 0; i < snake.segments.length; i += 2) {
      const p = snake.segments[i];
      const jx = (Math.random() - 0.5) * 8, jy = (Math.random() - 0.5) * 8;
      this.food.spawnAt(p.x + jx, p.y + jy, 7, 2.5, snake.color);
    }
  }

  update(dt, input) {
    // Steering.
    const p = this.player;
    if (p.alive) {
      p.targetAngle = input.targetAngle();
      p.boosting = input.boost && p.canBoost();
    }
    for (const s of this.snakes) if (!s.isPlayer && s.alive) steerAI(s, this, dt);

    // Movement + boost drops.
    for (const s of this.snakes) {
      const drops = s.update(dt);
      for (const d of drops) this.food.spawnAt(d.x, d.y, 4, 0.8, s.color);
    }

    this.food.rebuildHash();
    this.rebuildSegHash();

    // Eating.
    for (const s of this.snakes) {
      if (!s.alive) continue;
      const gained = this.food.eat(s.head.x, s.head.y, s.radius * 1.3);
      if (gained > 0) s.grow(gained);
    }

    // Collisions.
    const dead = [];
    for (const s of this.snakes) {
      if (!s.alive) continue;
      const h = s.head, r = s.radius;
      if (Math.hypot(h.x, h.y) + r > CONFIG.WORLD_RADIUS) { dead.push(s); continue; }
      let hit = false;
      this.segHash.query(h.x, h.y, r * 3, seg => {
        if (hit || seg.snake === s || !seg.snake.alive) return;
        if (Math.hypot(seg.x - h.x, seg.y - h.y) < r + seg.snake.radius) hit = true;
      });
      if (hit) dead.push(s);
    }
    for (const s of dead) this.kill(s);

    // Respawn AI.
    for (const s of this.snakes) {
      if (s.alive || s.isPlayer) continue;
      s.deadTime += dt;
      if (s.deadTime >= CONFIG.AI_RESPAWN_DELAY) {
        const sp = this.randomSpawn();
        s.reset(sp.x, sp.y, sp.angle);
        initAI(s);
      }
    }
  }

  ranking() {
    return this.snakes.filter(s => s.alive).sort((a, b) => b.length - a.length).slice(0, 5);
  }
}
