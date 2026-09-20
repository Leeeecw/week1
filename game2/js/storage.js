const KEY = 'slither_highscore';

export function getHighScore() {
  try {
    const v = parseInt(localStorage.getItem(KEY), 10);
    return Number.isFinite(v) ? v : 0;
  } catch { return 0; }
}

// Returns true if a new high score was saved.
export function saveHighScore(score) {
  try {
    if (score > getHighScore()) { localStorage.setItem(KEY, String(score)); return true; }
  } catch { /* ignore */ }
  return false;
}
