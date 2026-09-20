import { CONFIG } from './config.js';

// Per-snake AI personality is stored on snake.ai.
export function initAI(snake) {
  snake.ai = {
    vision: 200 + Math.random() * 200,
    aggression: Math.random(),
    wanderAngle: snake.angle,
    wanderTimer: 0,
    boostTimer: 0,
  };
}

export function steerAI(snake, world, dt) {
  const ai = snake.ai;
  const h = snake.head;
  const r = snake.radius;

  // 1. Danger avoidance: check points ahead in a fan.
  let dangerDir = 0;
  let dangerFound = false;
  const lookDist = r * 4 + snake.speed * 0.5;
  const fan = [-0.6, -0.3, 0, 0.3, 0.6];
  for (const off of fan) {
    const a = snake.angle + off;
    const px = h.x + Math.cos(a) * lookDist;
    const py = h.y + Math.sin(a) * lookDist;
    // World boundary.
    if (Math.hypot(px, py) > CONFIG.WORLD_RADIUS - r * 3) {
      dangerFound = true; dangerDir += off === 0 ? 1 : -Math.sign(off); continue;
    }
    // Other snakes' bodies.
    let hit = false;
    world.segHash.query(px, py, r * 2, s => {
      if (hit || s.snake === snake) return;
      if (Math.hypot(s.x - px, s.y - py) < r + s.snake.radius) hit = true;
    });
    if (hit) { dangerFound = true; dangerDir += off === 0 ? 1 : -Math.sign(off); }
  }
  if (dangerFound) {
    // Turn away; if center probe hit, pick side away from world center too.
    let turn = dangerDir !== 0 ? Math.sign(dangerDir) : 1;
    if (Math.hypot(h.x, h.y) > CONFIG.WORLD_RADIUS * 0.8) {
      // Steer toward center.
      snake.targetAngle = Math.atan2(-h.y, -h.x);
    } else {
      snake.targetAngle = snake.angle + turn * 1.6;
    }
    snake.boosting = false;
    return;
  }

  // 2. Food seeking.
  let best = null, bestScore = -Infinity;
  world.food.hash.query(h.x, h.y, ai.vision, f => {
    const d = Math.hypot(f.x - h.x, f.y - h.y);
    const score = f.value * 40 - d;
    if (score > bestScore) { bestScore = score; best = f; }
  });
  if (best) {
    snake.targetAngle = Math.atan2(best.y - h.y, best.x - h.x);
  } else {
    // 3. Wander.
    ai.wanderTimer -= dt;
    if (ai.wanderTimer <= 0) {
      ai.wanderTimer = 1 + Math.random() * 2;
      ai.wanderAngle = snake.angle + (Math.random() - 0.5) * 2;
    }
    snake.targetAngle = ai.wanderAngle;
    // Drift toward center when far out.
    if (Math.hypot(h.x, h.y) > CONFIG.WORLD_RADIUS * 0.7) {
      snake.targetAngle = Math.atan2(-h.y, -h.x);
    }
  }

  // Occasional boost.
  ai.boostTimer -= dt;
  if (ai.boostTimer <= 0) {
    ai.boostTimer = 2 + Math.random() * 4;
    snake.boosting = snake.canBoost() && Math.random() < ai.aggression * 0.4;
    if (snake.boosting) ai.boostTimer = 0.5 + Math.random();
  }
}
