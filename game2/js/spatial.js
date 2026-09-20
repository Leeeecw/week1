// Uniform grid spatial hash for fast neighbor queries.
export class SpatialHash {
  constructor(cellSize) {
    this.cellSize = cellSize;
    this.cells = new Map();
  }
  clear() { this.cells.clear(); }
  _key(cx, cy) { return cx * 73856093 ^ cy * 19349663; }
  insert(item, x, y) {
    const cx = Math.floor(x / this.cellSize);
    const cy = Math.floor(y / this.cellSize);
    const k = this._key(cx, cy);
    let arr = this.cells.get(k);
    if (!arr) { arr = []; this.cells.set(k, arr); }
    arr.push(item);
  }
  // Calls fn(item) for every item in cells overlapping the circle (x, y, r).
  query(x, y, r, fn) {
    const minX = Math.floor((x - r) / this.cellSize);
    const maxX = Math.floor((x + r) / this.cellSize);
    const minY = Math.floor((y - r) / this.cellSize);
    const maxY = Math.floor((y + r) / this.cellSize);
    for (let cx = minX; cx <= maxX; cx++) {
      for (let cy = minY; cy <= maxY; cy++) {
        const arr = this.cells.get(this._key(cx, cy));
        if (arr) for (let i = 0; i < arr.length; i++) fn(arr[i]);
      }
    }
  }
}
