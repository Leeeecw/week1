import { CONFIG } from './config.js';
import { World } from './world.js';
import { Renderer } from './renderer.js';
import { Camera } from './camera.js';
import { Input } from './input.js';
import { getHighScore, saveHighScore } from './storage.js';

const canvas = document.getElementById('game');
const renderer = new Renderer(canvas);
const input = new Input(canvas);
const camera = new Camera();
const world = new World();
window.__world = world; // TEMP selftest

const $ = id => document.getElementById(id);
const hud = { length: $('hud-length'), score: $('hud-score'), high: $('hud-high'), rank: $('hud-rank') };
const overlayStart = $('overlay-start'), overlayOver = $('overlay-over');

const STATE = { START: 0, PLAYING: 1, GAME_OVER: 2 };
let state = STATE.START;
let lastTime = performance.now();
let hudTimer = 0;

function showStart() {
  state = STATE.START;
  $('start-high').textContent = getHighScore();
  overlayStart.classList.remove('hidden');
  overlayOver.classList.add('hidden');
}

function startGame() {
  world.init();
  camera.x = world.player.head.x; camera.y = world.player.head.y; camera.zoom = 1;
  overlayStart.classList.add('hidden');
  overlayOver.classList.add('hidden');
  hud.high.textContent = getHighScore();
  state = STATE.PLAYING;
  lastTime = performance.now();
}

function gameOver() {
  state = STATE.GAME_OVER;
  const score = world.player.score;
  const isNew = saveHighScore(score);
  $('over-score').textContent = score;
  $('over-high').textContent = getHighScore();
  $('over-newhigh').classList.toggle('hidden', !isNew);
  overlayOver.classList.remove('hidden');
}

function updateHUD() {
  const p = world.player;
  hud.length.textContent = Math.floor(p.length);
  hud.score.textContent = p.score;
  hud.high.textContent = Math.max(getHighScore(), p.score);
  hud.rank.innerHTML = world.ranking()
    .map(s => `<li style="color:${s.isPlayer ? '#fff' : s.color}">${s.name} (${Math.floor(s.length)})</li>`)
    .join('');
}

function loop(now) {
  const dt = Math.min((now - lastTime) / 1000, CONFIG.MAX_DT);
  lastTime = now;

  if (state === STATE.PLAYING) {
    world.update(dt, input);
    camera.follow(world.player, dt);
    hudTimer += dt;
    if (hudTimer > 0.2) { hudTimer = 0; updateHUD(); }
    if (!world.player.alive) gameOver();
  } else if (state === STATE.GAME_OVER) {
    // Keep the world alive in the background for a nicer game-over screen.
    world.update(dt, { targetAngle: () => world.player.angle, boost: false });
  }
  renderer.draw(world, camera);
  requestAnimationFrame(loop);
}

$('btn-start').addEventListener('click', startGame);
$('btn-restart').addEventListener('click', startGame);

world.init();
showStart();
requestAnimationFrame(loop);
