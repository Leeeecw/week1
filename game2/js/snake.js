import { CONFIG } from './config.js';

let nextId = 1;

export class Snake {
  constructor({ x, y, angle, color, isPlayer = false, name = '' }) {
    this.id = nextId++;
    this.name = name;
    this.isPlayer = isPlayer;
    this.color = color;
    this.reset(x, y, angle);
  }

  reset(x, y, angle) {
    this.head = { x, y };
    this.angle = angle;
    this.targetAngle = angle;
    this.length = CONFIG.INITIAL_LENGTH;
    this.alive = true;
    this.boosting = false;
    this.boostTimer = 0;
    this.score = 0;
    this.deadTime = 0;
    // path: array of points the head has traveled, newest first.
    this.path = [];
    this.segments = [];
    const dx = -Math.cos(angle), dy = -Math.sin(angle);
    const total = this.length * CONFIG.SEGMENT_SPACING;
    for (let d = 0; d <= total; d += 2) {
      this.path.push({ x: x + dx * d, y: y + dy * d });
    }
    this.rebuildSegments();
  }

  get radius() {
    return CONFIG.BASE_RADIUS + Math.sqrt(this.length) * CONFIG.RADIUS_GROWTH;
  }

  get speed() {
    return CONFIG.BASE_SPEED * (this.boosting ? CONFIG.BOOST_MULT : 1);
  }

  canBoost() { return this.length > CONFIG.MIN_BOOST_LENGTH; }

  grow(amount) {
    this.length += amount;
    this.score += Math.round(amount * 10);
  }

  // Returns dropped food positions (from boost drain) this frame.
  update(dt) {
    const dropped = [];
    if (!this.alive) return dropped;

    if (this.boosting && !this.canBoost()) this.boosting = false;

    // Smooth turn toward targetAngle.
    let diff = this.targetAngle - this.angle;
    diff = Math.atan2(Math.sin(diff), Math.cos(diff));
    const maxTurn = CONFIG.TURN_SPEED * dt;
    if (Math.abs(diff) <= maxTurn) this.angle = this.targetAngle;
    else this.angle += Math.sign(diff) * maxTurn;

    // Move head.
    const step = this.speed * dt;
    this.head.x += Math.cos(this.angle) * step;
    this.head.y += Math.sin(this.angle) * step;
    this.path.unshift({ x: this.head.x, y: this.head.y });

    // Boost drain.
    if (this.boosting) {
      this.boostTimer += dt;
      if (this.boostTimer >= CONFIG.BOOST_DRAIN_INTERVAL) {
        this.boostTimer = 0;
        this.length -= 1;
        const tail = this.segments[this.segments.length - 1];
        if (tail) dropped.push({ x: tail.x, y: tail.y });
      }
    } else {
      this.boostTimer = 0;
    }

    this.rebuildSegments();
    return dropped;
  }

  // Place segments along the path at fixed spacing, then trim unused path.
  rebuildSegments() {
    const spacing = CONFIG.SEGMENT_SPACING;
    const wanted = Math.max(2, Math.floor(this.length));
    const segs = [];
    segs.push({ x: this.path[0].x, y: this.path[0].y });
    let accum = 0;
    let i = 1;
    while (segs.length < wanted && i < this.path.length) {
      const a = this.path[i - 1], b = this.path[i];
      const d = Math.hypot(b.x - a.x, b.y - a.y);
      if (accum + d >= spacing) {
        const t = (spacing - accum) / d;
        const p = { x: a.x + (b.x - a.x) * t, y: a.y + (b.y - a.y) * t };
        segs.push(p);
        // Insert p into path so we can continue from it.
        this.path.splice(i, 0, p);
        accum = 0;
        i++;
      } else {
        accum += d;
        i++;
      }
    }
    // Trim path beyond last segment (keep a little slack).
    if (i + 4 < this.path.length) this.path.length = i + 4;
    this.segments = segs;
  }
}
