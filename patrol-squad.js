/* Self-Control Patrol — Patrol Squad mascot system.
 * One shared engine for all six characters:
 *   - background squad staged on clear board areas (inside the board layer, so it pans/zooms with the board)
 *   - one animated close-up stage (the game's existing #patrolCharacter reaction element)
 *   - data-driven states, priorities, pose cross-fades, talking/blinking head layer and prop layer
 * The engine never changes game state; game.js reports events and the engine only presents them.
 */
(function () {
  'use strict';
  const M = window.PATROL_SQUAD;
  const noop = () => {};
  if (!M) { window.PatrolSquad = { init: noop, react: noop, reset: noop, clear: noop, sync: noop, celebrate: noop, art: () => '', ready: false }; return; }

  const KEYS = ['coach', 'calm', 'pause', 'think', 'flex', 'focus'];
  const C = M.characters, BW = M.board.width, BH = M.board.height;
  const STAND = 1.12;               // board actor box = unit * STAND (headroom for raised arms)
  const pct = (v, total) => `${(v / total * 100).toFixed(3)}%`;

  let o = { reduced: () => false, paused: () => false, boardOn: () => true, closeupsOn: () => true, voiceOn: () => false, say: noop };
  let stage = null, layer = null, host = null, refs = {};
  const actors = {};
  let mode = 'idle';                // 'idle' | 'finished'
  let current = null, pending = null, lastEvent = { key: '', at: 0 }, lastLine = {};
  let closeTimers = [], idleTimer = null, calmTimer = null, rr = 0, hiddenTab = false, offscreen = false;

  /* ---------- helpers ---------- */
  const art = (k, group, name) => C[k]?.[group]?.[name]?.display || '';
  const poseDef = (k, name) => C[k].poses[name] || C[k].poses[C[k].defaultIdlePose];
  const reduced = () => { try { return !!o.reduced(); } catch { return false; } };
  const quiet = () => hiddenTab || offscreen || (() => { try { return !!o.paused(); } catch { return false; } })();
  function later(list, fn, ms) { const t = setTimeout(() => { const i = list.indexOf(t); if (i >= 0) list.splice(i, 1); fn(); }, ms); list.push(t); return t; }
  function clearList(list) { while (list.length) clearTimeout(list.pop()); }
  const cache = new Map();
  function preload(src) { if (!src || cache.has(src)) return; const im = new Image(); im.decoding = 'async'; im.src = src; cache.set(src, im); }

  /* ---------- figure: two stacked pose images for cross-fades ---------- */
  function makeFigure(extra) {
    const fig = document.createElement('div');
    fig.className = `ps-figure ${extra || ''}`;
    fig.innerHTML = '<div class="ps-body"><img class="ps-pose" alt="" draggable="false"><img class="ps-pose" alt="" draggable="false"></div>';
    return fig;
  }
  function setPose(fig, k, name, { instant = false, scale = 1, slow = false } = {}) {
    const p = poseDef(k, name);
    if (fig.dataset.pose === name && fig.dataset.k === k && fig.dataset.scale === String(scale)) return;
    fig.dataset.pose = name; fig.dataset.k = k; fig.dataset.scale = String(scale);
    const [a, b] = fig.querySelectorAll('.ps-pose');
    const front = a.classList.contains('on') ? a : b.classList.contains('on') ? b : null;
    const back = front === a ? b : a;
    back.style.setProperty('--hf', (p.heightFactor * scale).toFixed(4));
    const swap = () => {
      if (fig.dataset.pose !== name) return;           // a newer pose was requested meanwhile
      back.classList.toggle('slow', slow);
      back.classList.toggle('instant', instant || reduced());
      if (front) { front.classList.toggle('instant', instant || reduced()); front.classList.toggle('slow', slow); front.classList.remove('on'); }
      back.classList.add('on');
    };
    if (back.getAttribute('src') === p.display && back.complete) { swap(); return; }
    back.onload = swap; back.onerror = swap;
    back.src = p.display;
    if (back.complete) swap();
  }
  function setMotion(fig, motion, oneShot) {
    const body = fig.querySelector('.ps-body');
    body.dataset.motion = motion || '';
    body.classList.remove('ps-oneshot'); void body.offsetWidth;
    if (oneShot) body.classList.add('ps-oneshot');
  }

  /* ---------- background squad ---------- */
  function buildBoard() {
    if (!layer) return;
    layer.innerHTML = '';
    for (const k of KEYS) {
      const c = C[k], b = c.board, boxH = b.unit * STAND;
      const el = document.createElement('div');
      el.className = 'ps-actor';
      el.dataset.character = k;
      el.style.left = pct(b.x, BW);
      el.style.top = pct(b.baseline - boxH, BH);
      el.style.height = pct(boxH, BH);
      el.style.setProperty('--ps-accent', c.accent);
      const fig = makeFigure('ps-board-figure');
      el.appendChild(fig);
      layer.appendChild(el);
      // a post the close-up card sits on top of: that mascot steps aside while a close-up shows
      const cu = M.closeup.card || M.closeup, half = b.height * 0.45;
      const under = b.x + half > cu.x && b.x - half < cu.x + cu.w && b.baseline > cu.y && b.baseline - b.height < cu.y + cu.h;
      actors[k] = { el, fig, timer: [], under };
      setPose(fig, k, b.idle[0], { instant: true, scale: 1 / STAND });
      setMotion(fig, c.states.idle.motion, false);
    }
  }
  function boardIdle(k, instant) {
    const a = actors[k]; if (!a) return;
    const c = C[k];
    clearList(a.timer);
    a.el.classList.remove('ps-react', 'ps-away');
    if (mode === 'finished') {
      setPose(a.fig, k, c.board.statePose.missionComplete, { instant, scale: 1 / STAND });
      setMotion(a.fig, reduced() ? '' : 'celebrate-idle', false);
      return;
    }
    setPose(a.fig, k, c.board.idle[0], { instant, scale: 1 / STAND });
    setMotion(a.fig, c.states.idle.motion, false);
  }
  function boardReact(k, stateName, hold = 1900) {
    const a = actors[k]; if (!a) return;
    const c = C[k], st = c.states[stateName] || c.states.idle;
    clearList(a.timer);
    a.el.classList.remove('ps-away');
    a.el.classList.remove('ps-react'); void a.el.offsetWidth; a.el.classList.add('ps-react');
    setPose(a.fig, k, c.board.statePose[stateName] || c.board.idle[0], { scale: 1 / STAND });
    setMotion(a.fig, reduced() ? '' : st.motion, true);
    later(a.timer, () => boardIdle(k), reduced() ? Math.min(hold, 1400) : hold);
  }
  function idleTick() {
    if (quiet() || reduced() || mode !== 'idle') return;
    // one character at a time does a brief posture shift (no constant activity)
    for (let n = 0; n < KEYS.length; n++) {
      const k = KEYS[rr++ % KEYS.length], a = actors[k], c = C[k];
      if (!a || a.el.classList.contains('ps-react') || a.el.classList.contains('ps-away') || k === 'calm') continue;
      if (c.board.alternates.length) {
        const alt = c.board.alternates[Math.floor(Math.random() * c.board.alternates.length)];
        setPose(a.fig, k, alt, { scale: 1 / STAND });
        later(a.timer, () => { if (!a.el.classList.contains('ps-react')) setPose(a.fig, k, c.board.idle[0], { scale: 1 / STAND }); }, 1700);
      } else {
        setMotion(a.fig, 'look', true);
        later(a.timer, () => { if (!a.el.classList.contains('ps-react')) setMotion(a.fig, c.states.idle.motion, false); }, 1700);
      }
      break;
    }
  }
  function calmTick() {
    // Captain Calm's slow breathing cycle: eyes-open meditation <-> eyes-closed heart-hands breathing
    if (quiet() || reduced() || mode !== 'idle') return;
    const a = actors.calm; if (!a || a.el.classList.contains('ps-react') || a.el.classList.contains('ps-away')) return;
    const [open, closed] = C.calm.board.idle;
    setPose(a.fig, 'calm', a.fig.dataset.pose === open ? closed : open, { scale: 1 / STAND, slow: true });
  }

  /* ---------- close-up stage ---------- */
  function buildCloseup() {
    if (!host) return;
    const cu = M.closeup;
    host.style.left = pct(cu.x, BW); host.style.top = pct(cu.y, BH);
    host.style.width = pct(cu.w, BW); host.style.height = pct(cu.h, BH);
    // pieces are placed relative to the host box (board pixels -> %), so they scale with the board
    const box = r => r ? `left:${pct(r.x - cu.x, cu.w)};top:${pct(r.y - cu.y, cu.h)};width:${pct(r.w, cu.w)};height:${pct(r.h, cu.h)}` : '';
    const card = cu.card || { x: cu.x, y: cu.y, w: cu.w, h: cu.h }, bub = cu.bubble;
    const tail = bub ? pct(card.x + card.w / 2 - bub.x, bub.w) : '50%';
    host.innerHTML = `<div class="ps-panel" style="${box(card)}">
        <div class="character-art ps-stage" aria-hidden="true"><div class="ps-pad"></div></div>
      </div>
      <div class="character-bubble ps-bubble${bub ? ' ps-bubble-band' : ''}" style="${box(bub)};--ps-tail:${tail}"><span class="ps-badge-wrap"><span class="ps-badge"><img class="ps-badge-img" alt="" draggable="false"></span><span class="ps-prop-wrap"><img class="ps-prop" alt="" draggable="false"></span></span>
          <span class="ps-text"><strong id="characterName"></strong><span id="characterLine"></span></span></div>`;
    const fig = makeFigure('ps-closeup-figure');
    host.querySelector('.ps-stage').appendChild(fig);
    refs = { fig, badge: host.querySelector('.ps-badge-img'), name: host.querySelector('#characterName'), line: host.querySelector('#characterLine'),
      prop: host.querySelector('.ps-prop'), propWrap: host.querySelector('.ps-prop-wrap') };
    host.setAttribute('aria-hidden', 'true');
  }
  function pickLine(k, key, data) {
    const c = C[k], pool = c.lines[key] || c.lines.idle || [''];
    let i = Math.floor(Math.random() * pool.length);
    if (pool.length > 1 && lastLine[`${k}:${key}`] === i) i = (i + 1) % pool.length;
    lastLine[`${k}:${key}`] = i;
    return pool[i].replace(/\{name\}/g, String(data?.name || 'Patrol Squad').slice(0, 40));
  }
  function setBadge(k, exprName) { const src = art(k, 'expressions', exprName); if (src && refs.badge.getAttribute('src') !== src) refs.badge.src = src; }
  function hideCloseup(immediate) {
    clearList(closeTimers);
    if (!host) return;
    host.classList.remove('ps-show');
    KEYS.forEach(j => actors[j]?.el.classList.remove('ps-under'));
    host.classList.toggle('ps-instant', !!immediate || reduced());
    host.setAttribute('aria-hidden', 'true');
    const k = current?.k;
    current = null;
    if (k && actors[k]) boardIdle(k);
    if (!immediate && pending && Date.now() - pending.at < 2600) { const p = pending; pending = null; later(closeTimers, () => play(p.key, p.ev, p.data, true), 260); }
    else pending = null;
  }
  function showCloseup(k, stateName, line, priority) {
    const c = C[k], st = c.states[stateName] || c.states.idle, red = reduced();
    clearList(closeTimers);
    if (current && current.k !== k && actors[current.k]) boardIdle(current.k);
    host.dataset.character = k; host.dataset.mood = stateName; host.dataset.profile = c.motionProfile;
    host.style.setProperty('--ps-accent', c.accent); host.style.setProperty('--ps-accent2', c.accent2);
    refs.name.textContent = c.name; refs.line.textContent = line;
    host.setAttribute('aria-label', `${c.name}: ${line}`);
    // full-body pose sequence (pose swapping)
    const frames = st.poses;
    const scale = Math.min(1.3, 1 / Math.max(...frames.map(([n]) => poseDef(k, n).heightFactor)));
    setPose(refs.fig, k, frames[0][0], { instant: !host.classList.contains('ps-show'), scale });
    for (const [name, t] of frames.slice(1)) later(closeTimers, () => setPose(refs.fig, k, name, { scale }), red ? Math.round(t * .8) : t);
    host.classList.toggle('ps-long', line.length > 40);
    setMotion(refs.fig, red ? '' : st.motion, true);
    // independent head layer: talk cycle / blink, then settle
    const speakMs = Math.max(1100, Math.min(2600, line.length * 48));
    const [e0, e1] = [st.badge[0], st.badge[1] || st.badge[0]];
    setBadge(k, e0);
    if (!red && e1 !== e0) {
      const step = c.motionProfile === 'smooth' ? 560 : c.motionProfile === 'crisp' ? 230 : 170;
      let flip = false;
      for (let t = step; t < speakMs; t += step) later(closeTimers, () => { flip = !flip; setBadge(k, flip ? e1 : e0); }, t);
    }
    later(closeTimers, () => setBadge(k, e1), red ? 900 : speakMs);
    // independent prop layer
    if (st.prop) {
      refs.prop.src = art(k, 'accessories', st.prop[0]);
      refs.propWrap.dataset.anim = red ? 'static' : st.prop[1];
      refs.propWrap.classList.remove('ps-prop-on'); void refs.propWrap.offsetWidth; refs.propWrap.classList.add('ps-prop-on');
    } else { refs.propWrap.classList.remove('ps-prop-on'); refs.propWrap.dataset.anim = ''; }
    // step forward: the background twin leaves its post while the close-up plays
    if (actors[k]) { clearList(actors[k].timer); actors[k].el.classList.add('ps-away'); }
    KEYS.forEach(j => actors[j]?.under && actors[j].el.classList.add('ps-under'));
    host.classList.toggle('ps-instant', red);
    host.classList.remove('ps-enter'); void host.offsetWidth;
    host.classList.add('ps-show', 'ps-enter');
    host.setAttribute('aria-hidden', 'false');
    const lastFrame = frames.length > 1 ? frames[frames.length - 1][1] : 0;
    const duration = Math.max(2700, speakMs + 1100, lastFrame + 1400);
    // a lower-priority reaction may take over once this character has finished speaking
    current = { k, stateName, priority, minUntil: Date.now() + speakMs + 400, until: Date.now() + duration };
    later(closeTimers, () => hideCloseup(false), duration);
  }
  function speakLine(k, line) {
    try { if (o.voiceOn()) o.say(line, C[k].voice || {}); } catch { /* voice is optional */ }
  }

  /* ---------- event entry point ---------- */
  function play(key, ev, data, fromQueue) {
    const k = ev.char;
    const line = pickLine(k, ev.line, data);
    const compact = stage.getBoundingClientRect().width < 620;   // too small for a legible close-up: react on the board instead
    const wantCloseup = ev.closeup !== false && host && !compact && (() => { try { return o.closeupsOn(); } catch { return true; } })();
    if (wantCloseup) {
      if (current && !fromQueue && ev.priority < current.priority && Date.now() < current.minUntil) {
        pending = { key, ev, data, at: Date.now() };     // lower priority waits until the current line is delivered
        return;
      }
      showCloseup(k, ev.state, line, ev.priority);
    } else {
      boardReact(k, ev.state);
    }
    speakLine(k, line);
  }
  function react(key, data = {}) {
    const ev = M.events[key];
    if (!ev || !stage) return;
    const now = Date.now();
    if (lastEvent.key === key && now - lastEvent.at < 900) return;   // duplicate trigger guard
    lastEvent = { key, at: now };
    if (key === 'finale') { celebrate(); return; }
    play(key, ev, data, false);
  }
  function celebrate() {
    mode = 'finished';
    hideCloseup(true);
    KEYS.forEach((k, i) => {
      const a = actors[k]; if (!a) return;
      clearList(a.timer);
      if (reduced()) { boardIdle(k, true); return; }
      later(a.timer, () => { boardReact(k, 'missionComplete', 2600); }, i * 140);
    });
  }
  function clear() { pending = null; hideCloseup(true); }
  function reset() { mode = 'idle'; clear(); KEYS.forEach(k => boardIdle(k, true)); }
  function sync() {
    if (!stage) return;
    let on = true; try { on = !!o.boardOn(); } catch { /* default on */ }
    layer?.classList.toggle('ps-off', !on);
    if (host) { let cu = true; try { cu = !!o.closeupsOn(); } catch { /* default on */ } if (!cu && current) hideCloseup(true); }
  }
  function updateScale() { if (!stage) return; const w = stage.getBoundingClientRect().width || 1000; stage.style.setProperty('--ps-bw', `${w}px`); host?.classList.toggle('ps-small', w < 1000); }

  function init(options) {
    o = { ...o, ...options };
    stage = options.stage; layer = options.layer; host = options.closeup;
    if (!stage || !layer) return;
    buildBoard();
    buildCloseup();
    updateScale();
    if ('ResizeObserver' in window) new ResizeObserver(updateScale).observe(stage); else window.addEventListener('resize', updateScale);
    if ('IntersectionObserver' in window) new IntersectionObserver(entries => { offscreen = !entries[0].isIntersecting; document.documentElement.classList.toggle('ps-offscreen', offscreen); }).observe(stage);
    document.addEventListener('visibilitychange', () => {
      hiddenTab = document.hidden;
      document.documentElement.classList.toggle('ps-tab-hidden', hiddenTab);
      if (hiddenTab) clear();
    });
    idleTimer = setInterval(idleTick, 4600);
    calmTimer = setInterval(calmTick, 5200);
    // lazy-load the remaining runtime art after first paint
    const rest = () => M.runtimeFiles.forEach(preload);
    if ('requestIdleCallback' in window) requestIdleCallback(rest, { timeout: 4000 }); else setTimeout(rest, 1500);
    sync();
    window.PatrolSquad.ready = true;
  }

  window.PatrolSquad = {
    init, react, reset, clear, sync, celebrate, art, ready: false,
    characters: KEYS.map(k => ({ key: k, name: C[k].name })),
    debug: () => ({ mode, current: current && { ...current }, pending: pending && pending.key,
      actors: Object.fromEntries(KEYS.map(k => [k, { pose: actors[k]?.fig.dataset.pose, away: actors[k]?.el.classList.contains('ps-away'), react: actors[k]?.el.classList.contains('ps-react'), under: actors[k]?.el.classList.contains('ps-under') }])),
      closeupVisible: !!host?.classList.contains('ps-show'), closeupCharacter: host?.dataset.character, closeupPose: refs.fig?.dataset.pose,
      line: refs.line?.textContent, badge: refs.badge?.getAttribute('src'), prop: refs.propWrap?.classList.contains('ps-prop-on') ? refs.prop.getAttribute('src') : null })
  };
})();
