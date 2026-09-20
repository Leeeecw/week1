export class Input {
  constructor(canvas) {
    this.canvas = canvas;
    this.mouse = { x: canvas.width / 2, y: canvas.height / 2 };
    this.boost = false;
    this.mouseDown = false;
    this.spaceDown = false;

    canvas.addEventListener('mousemove', e => {
      this.mouse.x = e.clientX; this.mouse.y = e.clientY;
    });
    canvas.addEventListener('mousedown', () => { this.mouseDown = true; this._sync(); });
    window.addEventListener('mouseup', () => { this.mouseDown = false; this._sync(); });
    window.addEventListener('keydown', e => {
      if (e.code === 'Space') { e.preventDefault(); this.spaceDown = true; this._sync(); }
    });
    window.addEventListener('keyup', e => {
      if (e.code === 'Space') { this.spaceDown = false; this._sync(); }
    });
  }
  _sync() { this.boost = this.mouseDown || this.spaceDown; }

  // Angle from screen center to mouse.
  targetAngle() {
    const cx = window.innerWidth / 2, cy = window.innerHeight / 2;
    return Math.atan2(this.mouse.y - cy, this.mouse.x - cx);
  }
}
