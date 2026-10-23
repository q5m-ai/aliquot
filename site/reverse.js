'use strict';
const $ = id => document.getElementById(id), canvas = $('graph'), ctx = canvas.getContext('2d');
const BLUE = '#285cff', AMBER = '#bd7410', PATH_WINDOW = 180;
const fmt = n => n.toLocaleString('en-CA');
const signed = n => `${n > 0n ? '+' : ''}${fmt(n)}`;
let path = [], table = null, result = null, candidates = [], extras = [];
let searchJob = null, verifyJob = null, inspectionJob = null, inspectionIssue = '';
let pathPoints = [], candidatePoints = [], plotPoints = [], screenPoints = [];
let hoveredPoint = null, pinnedPoint = null, suppressedPoint = null;
let width = 0, height = 0, framePending = false, layoutDirty = true, drawnCandidateCount = 0;
let view = {xlo: -1.2, xhi: .2, lo: 0, hi: 2, exponent: 0, mode: 'linear'};
const records = new Map();

function requestDraw() {
  if (framePending) return;
  framePending = true;
  requestAnimationFrame(() => { framePending = false; draw(); });
}
function integer(raw, positive = false) {
  raw = raw.trim();
  if (!/^\d+$/.test(raw)) throw new Error(`Enter a ${positive ? 'positive' : 'non-negative'} decimal integer.`);
  if (raw.length > AliquotMath.MAX_DIGITS) throw new Error('Input exceeds the 1,000-digit browser resource budget.');
  const n = BigInt(raw);
  if (positive && n === 0n) throw new Error('A predecessor must be positive: s(0) is undefined.');
  return n;
}
function readBound() {
  const raw = $('source-bound').value.trim();
  if (!/^\d{1,7}$/.test(raw) || Number(raw) < 1 || Number(raw) > AliquotReverse.MAX_BOUND) {
    throw new Error('Source bound must be an integer from 1 to 1,000,000.');
  }
  return Number(raw);
}
function seedButtons() {
  let n;
  try { n = integer($('root-input').value); } catch { /* Disabled until input is valid. */ }
  $('root-decrement').disabled = n === undefined || n === 0n;
  $('root-increment').disabled = n === undefined || (n + 1n).toString().length > AliquotMath.MAX_DIGITS;
}
function changeSeed(delta) {
  let n;
  try { n = integer($('root-input').value) + delta; }
  catch (error) { $('input-status').textContent = error.message; return; }
  if (n < 0n || n.toString().length > AliquotMath.MAX_DIGITS) return;
  $('root-input').value = n.toString();
  return start();
}
function remember(n, info) {
  const key = n.toString();
  records.set(key, {...records.get(key), ...info});
  if (records.size > 1000) records.delete(records.keys().next().value);
}
function knownNext(n) {
  if (n === 0n) return undefined;
  if (n === 1n) return 0n;
  const saved = records.get(n.toString());
  if (saved) return saved.next;
  if (table && n <= BigInt(table.bound)) return BigInt(table.sums[Number(n)]);
  return undefined;
}
function rebuildPlot() {
  const previous = new Map(plotPoints.map(p => [p.key, p]));
  const firstSeen = new Map();
  path.forEach((n, i) => { if (!firstSeen.has(n)) firstSeen.set(n, i); });
  const first = Math.max(0, path.length - PATH_WINDOW);
  function point(kind, n, index) {
    const key = kind === 'path' ? `path-${index}` : `candidate-${n}`;
    const p = previous.get(key) || {};
    const earlier = firstSeen.get(n);
    Object.assign(p, {key, kind, n, index, k: -index, target: path.at(-1),
      firstSeen: earlier !== undefined && (kind === 'candidate' || earlier < index) ? earlier : null});
    return p;
  }
  pathPoints = path.slice(first).map((n, i) => point('path', n, first + i));
  candidatePoints = candidates.map(n => point('candidate', n, path.length));
  // Left-to-right keyboard order; candidates within their column are value-sorted.
  plotPoints = [...candidatePoints, ...pathPoints.slice().reverse()];
  if (pinnedPoint && !plotPoints.includes(pinnedPoint)) clearDetails(false);
  if (hoveredPoint && !plotPoints.includes(hoveredPoint)) hoveredPoint = null;
  screenPoints = []; // Old hit targets must never survive a rescale or a new frontier.
  layoutDirty = true;
  $('path-window').textContent = first > 0 ? `Latest ${PATH_WINDOW} chosen points shown; the full chain is retained.` : '';
  canvas.setAttribute('aria-label', `Reverse aliquot graph: ${fmt(candidates.length)} found predecessors. Arrow keys inspect; Enter selects; Space pins details.`);
  showDetails();
  requestDraw();
}
function fitGraph() {
  const mode = $('scale').value;
  let largest = 0n;
  for (const p of plotPoints) if (p.n > largest) largest = p.n;
  const exponent = mode === 'linear' ? Math.max(0, largest.toString().length - 6) : 0;
  let low = Infinity, high = -Infinity;
  for (const p of plotPoints) {
    p.coordinate = AliquotMath.coordinate(p.n, mode, exponent);
    low = Math.min(low, p.coordinate);
    high = Math.max(high, p.coordinate);
  }
  if (!plotPoints.length) { low = 0; high = 1; }
  const span = Math.max(mode === 'log' ? .5 : 1, high - low);
  const first = Math.max(0, path.length - PATH_WINDOW);
  view = {xlo: -Math.max(1, path.length) - .18, xhi: -first + .18,
    lo: Math.max(0, low - span * .22), hi: high + span * .32, exponent, mode};
  const W = Math.max(1, width - 82), H = Math.max(1, height - 76);
  screenPoints = plotPoints.map(point => ({point,
    x: 58 + (point.k - view.xlo) / (view.xhi - view.xlo) * W,
    y: 30 + H - (point.coordinate - view.lo) / (view.hi - view.lo) * H,
  }));
  layoutDirty = false;
}
function resize() {
  const box = canvas.getBoundingClientRect(), dpr = window.devicePixelRatio || 1;
  width = box.width; height = box.height;
  canvas.width = Math.round(width * dpr); canvas.height = Math.round(height * dpr);
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  screenPoints = [];
  layoutDirty = true;
  requestDraw();
}
function draw() {
  if (layoutDirty) fitGraph();
  ctx.clearRect(0, 0, width, height);
  ctx.font = '11px monospace';
  ctx.lineWidth = 1;
  for (let i = 0; i <= 4; i++) {
    const value = view.lo + (view.hi - view.lo) * i / 4;
    const y = 30 + (height - 76) * (1 - i / 4);
    ctx.strokeStyle = '#edf0f2';
    ctx.beginPath(); ctx.moveTo(58, y); ctx.lineTo(width - 24, y); ctx.stroke();
    ctx.fillStyle = '#87919a'; ctx.textAlign = 'right';
    ctx.fillText(AliquotMath.axisLabel(value, view.mode, view.exponent), 49, y + 4);
  }
  ctx.textAlign = 'center';
  const start = Math.ceil(view.xlo), end = Math.floor(view.xhi);
  const ticks = new Set([end]);
  for (let k = start; k <= end; k += Math.max(1, Math.ceil((end - start) / 6))) ticks.add(k);
  for (const k of ticks) ctx.fillText(String(k), 58 + (k - view.xlo) / (view.xhi - view.xlo) * (width - 82), height - 25);
  ctx.fillText('← backward · step k', (width + 34) / 2, height - 8);
  ctx.textAlign = 'left'; ctx.fillText('value', 8, 15);
  const frontier = screenPoints.find(t => t.point === pathPoints.at(-1));
  const selected = pinnedPoint || hoveredPoint;
  const inspected = screenPoints.find(t => t.point === selected);
  // Preview only the inspected alternative, never connect candidates to one another.
  if (inspected?.point.kind === 'candidate' && frontier) {
    ctx.strokeStyle = '#9bb2ee'; ctx.lineWidth = 1; ctx.setLineDash([4, 4]);
    ctx.beginPath(); ctx.moveTo(inspected.x, inspected.y); ctx.lineTo(frontier.x, frontier.y); ctx.stroke();
    ctx.setLineDash([]);
  }
  const chosen = screenPoints.filter(t => t.point.kind === 'path');
  ctx.strokeStyle = BLUE; ctx.lineWidth = 2; ctx.beginPath();
  chosen.forEach((t, i) => { if (i) ctx.lineTo(t.x, t.y); else ctx.moveTo(t.x, t.y); });
  ctx.stroke();
  // Every candidate retains its exact hit/keyboard target. Repeated pixels need
  // only one glyph, avoiding tens of thousands of identical draw calls for n=1.
  const pixels = new Set();
  drawnCandidateCount = 0;
  for (const t of screenPoints) {
    const p = t.point, repeat = p.firstSeen !== null;
    if (p.kind === 'candidate') {
      const pixel = `${Math.round(t.y * 2)}:${repeat}`;
      if (pixels.has(pixel)) continue;
      pixels.add(pixel); drawnCandidateCount++;
      ctx.strokeStyle = repeat ? AMBER : BLUE; ctx.lineWidth = 1.4;
      ctx.beginPath(); ctx.arc(t.x, t.y, 3.5, 0, Math.PI * 2); ctx.stroke();
    } else {
      ctx.fillStyle = repeat ? AMBER : BLUE;
      ctx.beginPath(); ctx.arc(t.x, t.y, p === pathPoints.at(-1) ? 4 : 2.5, 0, Math.PI * 2); ctx.fill();
    }
  }
  if (inspected) {
    ctx.strokeStyle = BLUE; ctx.lineWidth = 2;
    ctx.beginPath(); ctx.arc(inspected.x, inspected.y, 7, 0, Math.PI * 2); ctx.stroke();
  }
  canvas.style.cursor = hoveredPoint ? 'pointer' : 'default';
  positionDetails();
  // No idle animation loop: redraw only on data, pointer, keyboard, or size changes.
}
function positionDetails() {
  const p = pinnedPoint || hoveredPoint, card = $('point-details');
  if (!p || card.hidden) return;
  const anchor = screenPoints.find(t => t.point === p) || {x: width / 2, y: height / 2};
  const box = card.getBoundingClientRect(), inset = 8, gap = 14;
  let left = anchor.x + gap, top = anchor.y + gap;
  if (left + box.width > width - inset) left = anchor.x - box.width - gap;
  if (top + box.height > height - inset) top = anchor.y - box.height - gap;
  card.style.left = `${Math.max(inset, Math.min(left, Math.max(inset, width - box.width - inset)))}px`;
  card.style.top = `${Math.max(inset, Math.min(top, Math.max(inset, height - box.height - inset)))}px`;
}
function showDetails() {
  const p = pinnedPoint || hoveredPoint;
  $('point-details').hidden = !p;
  if (!p) return;
  $('point-details').dataset.pinned = String(!!pinnedPoint);
  const next = p.kind === 'candidate' ? p.target : p.index > 0 ? path[p.index - 1] : knownNext(p.n);
  const previous = p.kind === 'path' ? path[p.index + 1] : undefined;
  const details = {...AliquotPointInfo.basic(p.n, next, previous),
    ...AliquotPointInfo.divisors(p.n, records.get(p.n.toString())?.factors)};
  details.change = p.n === 0n || next === undefined ? '—' : signed(next - p.n);
  if (p.firstSeen !== null) details.status += ` · cycle link to step ${-p.firstSeen}`;
  $('point-title').textContent = `${p.kind === 'candidate' ? 'Predecessor' : 'Point'} · step ${p.k}`;
  for (const field of ['value', 'size', 'residue', 'previous', 'change', 'next', 'status', 'divisors', 'divisor-summary']) {
    $('point-' + field).textContent = details[field];
  }
  PageLatex.render($('point-factorization'), details.factorizationTex, {fallback: details.factorization});
  $('point-mode').textContent = pinnedPoint ? 'Pinned' : p.kind === 'candidate' ? 'Click to step back' : 'Click to pin';
  $('point-compute').hidden = !details.canCompute;
  $('point-compute').disabled = !pinnedPoint || !!inspectionJob;
  $('point-compute').textContent = inspectionJob ? 'Computing…' : 'Compute divisors';
  $('point-branch').hidden = !pinnedPoint || p.kind !== 'path' || p.index === path.length - 1;
  $('point-issue').textContent = inspectionIssue;
  positionDetails();
}
function clearDetails(suppress = true) {
  suppressedPoint = suppress ? pinnedPoint || hoveredPoint : null;
  inspectionJob = null; inspectionIssue = '';
  pinnedPoint = null; hoveredPoint = null;
  $('keyboard-status').textContent = '';
  showDetails(); requestDraw();
}
function hoverPoint(p) {
  if (p === suppressedPoint) p = null;
  else suppressedPoint = null;
  if (hoveredPoint === p) return;
  hoveredPoint = p;
  if (!pinnedPoint) inspectionIssue = '';
  showDetails(); requestDraw();
}
function pinPoint(p) {
  inspectionJob = null; inspectionIssue = '';
  pinnedPoint = p; hoveredPoint = null; suppressedPoint = null;
  showDetails(); requestDraw();
}
function hitPoint(event) {
  const box = canvas.getBoundingClientRect();
  const x = (event.clientX - box.left) * width / box.width;
  const y = (event.clientY - box.top) * height / box.height;
  const radius = event.pointerType === 'touch' ? 24 : 12;
  let closest = null, distance = radius ** 2;
  for (const t of screenPoints) {
    if (Math.abs(t.x - x) > radius) continue;
    const d = (t.x - x) ** 2 + (t.y - y) ** 2;
    if (d <= radius ** 2 && (!closest || d < distance)) { closest = t.point; distance = d; }
  }
  return closest;
}
function announcePoint(p) {
  $('keyboard-status').textContent = p ? `${p.kind === 'candidate' ? 'Predecessor' : 'Chosen point'} ${fmt(p.n)}, step ${p.k}. ${p.kind === 'candidate' ? 'Enter steps backward.' : 'Enter pins details.'}` : '';
}
function followPoint(p) {
  if (p?.kind !== 'candidate' || p.target !== path.at(-1) || !candidates.includes(p.n)) return;
  return changePath([...path, p.n]);
}
function activatePoint(p, inspectOnly = false) {
  if (!p) { clearDetails(); return; }
  if (p.kind === 'candidate' && !inspectOnly) return followPoint(p);
  if (p === pinnedPoint) clearDetails(); else pinPoint(p);
}
canvas.onpointermove = event => hoverPoint(hitPoint(event));
canvas.onpointerleave = () => { hoveredPoint = null; suppressedPoint = null; showDetails(); requestDraw(); };
canvas.onclick = event => activatePoint(hitPoint(event), !!event.shiftKey);
canvas.onkeydown = event => {
  if (event.key === 'Escape') { event.preventDefault(); clearDetails(); return; }
  if (!plotPoints.length) return;
  const current = pinnedPoint || hoveredPoint;
  if (event.key === 'Enter' || event.key === ' ') {
    event.preventDefault();
    return activatePoint(current || pathPoints.at(-1), event.key === ' ');
  }
  if (!['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', 'Home', 'End'].includes(event.key)) return;
  event.preventDefault();
  const index = plotPoints.indexOf(current), increment = ['ArrowRight', 'ArrowUp'].includes(event.key);
  const next = event.key === 'Home' ? 0 : event.key === 'End' ? plotPoints.length - 1
    : index < 0 ? increment ? 0 : plotPoints.length - 1
    : Math.max(0, Math.min(plotPoints.length - 1, index + (increment ? 1 : -1)));
  if (pinnedPoint) pinPoint(plotPoints[next]); else { suppressedPoint = null; hoverPoint(plotPoints[next]); }
  announcePoint(plotPoints[next]);
};
async function computeDetails() {
  if (!pinnedPoint || inspectionJob || pinnedPoint.n < 2n) return;
  const n = pinnedPoint.n, job = {};
  inspectionJob = job; inspectionIssue = ''; showDetails();
  const cancelled = () => inspectionJob !== job;
  try {
    let factors;
    const next = await AliquotMath.sum(n, {cancelled, onFactors: value => { factors = value; }});
    if (cancelled()) return;
    remember(n, {next, factors});
  } catch (error) {
    if (!cancelled()) inspectionIssue = `Divisor computation unresolved: ${error.message}`;
  } finally {
    if (!cancelled()) { inspectionJob = null; showDetails(); }
  }
}
function mergeCandidates() {
  candidates = [...new Set([...(result?.values || []), ...extras])].sort((a, b) => a < b ? -1 : a > b ? 1 : 0);
}
function searchMessage(text, complete = false) {
  $('search-status').textContent = text;
  $('search-status').dataset.complete = String(complete);
}
function resultMessage() {
  if (!result) return;
  const count = result.values.length, target = fmt(result.target), checked = fmt(result.checked);
  const extra = candidates.length - count;
  const message = result.complete
    ? count ? `${fmt(count)} predecessor${count === 1 ? '' : 's'} of ${target} · complete (m ≤ ${checked}).`
      : `No positive predecessors of ${target} · complete (m ≤ ${checked}).`
    : `${fmt(count)} predecessor${count === 1 ? '' : 's'} of ${target} found through m = ${checked} · partial; larger sources unsearched.`;
  searchMessage(message + (extra ? ` +${fmt(extra)} individually verified.` : ''), result.complete);
}
function stopSearch(announce = true) {
  const wasRunning = !!searchJob;
  searchJob = null;
  $('search-stop').disabled = true; $('search-progress').hidden = true;
  if (wasRunning && announce) searchMessage('Search stopped · incomplete. This does not establish that predecessors are absent.');
}
async function searchPredecessors() {
  if (!path.length) return;
  let bound;
  try { bound = readBound(); }
  catch (error) { searchMessage(error.message); return; }
  stopSearch(false); clearDetails(false);
  const target = path.at(-1), job = {};
  searchJob = job; result = null;
  mergeCandidates(); rebuildPlot();
  $('search-stop').disabled = false; $('search-progress').hidden = false; $('search-progress').value = 0;
  searchMessage(`Finding predecessors of ${fmt(target)} through m = ${fmt(bound)}…`);
  const cancelled = () => searchJob !== job;
  try {
    if (!table || table.bound < bound) {
      const completed = await AliquotReverse.sieve(bound, {cancelled, onProgress: (done, total) => {
        if (!cancelled()) $('search-progress').value = total ? done / total : 1;
      }});
      if (cancelled()) return;
      table = completed;
    }
    if (cancelled()) return;
    result = AliquotReverse.predecessors(table, target, bound);
    mergeCandidates(); resultMessage();
  } catch (error) {
    if (!cancelled()) searchMessage(`Search unresolved: ${error.message}. No conclusion about missing predecessors.`);
  } finally {
    if (!cancelled()) { stopSearch(false); rebuildPlot(); }
  }
}
function stopVerification(announce = true) {
  const wasRunning = !!verifyJob;
  verifyJob = null;
  $('verify-button').disabled = false; $('verify-stop').disabled = true;
  if (wasRunning && announce) $('verify-status').textContent = 'Verification stopped; candidate unresolved.';
}
function changePath(nextPath) {
  stopSearch(false); stopVerification(false); clearDetails(false);
  path = nextPath; extras = []; candidates = []; result = null;
  $('verify-status').textContent = ''; $('verify-input').value = '';
  $('depth-value').textContent = fmt(path.length - 1);
  $('frontier-value').textContent = fmt(path.at(-1));
  $('gain-value').textContent = signed(path[0] - path.at(-1));
  $('undo').disabled = path.length === 1;
  $('cycle-status').textContent = new Set(path).size < path.length ? 'Cycle in chosen chain.' : '';
  rebuildPlot();
  return searchPredecessors();
}
function start() {
  let n;
  seedButtons();
  try { n = integer($('root-input').value); }
  catch (error) {
    $('input-status').textContent = error.message;
    if (!path.length) {
      searchMessage('No graph started. Enter a valid target.');
      $('frontier-value').textContent = '—'; $('gain-value').textContent = '—';
    }
    return;
  }
  $('input-status').textContent = '';
  document.querySelectorAll('[data-root]').forEach(button => button.setAttribute('aria-pressed', String(BigInt(button.dataset.root) === n)));
  return changePath([n]);
}
async function verifyPredecessor() {
  if (!path.length || verifyJob) return;
  let n;
  try { n = integer($('verify-input').value, true); }
  catch (error) { $('verify-status').textContent = error.message; return; }
  const target = path.at(-1), job = {};
  verifyJob = job;
  $('verify-button').disabled = true; $('verify-stop').disabled = false;
  $('verify-status').textContent = `Checking s(${fmt(n)}) = ${fmt(target)} exactly…`;
  const cancelled = () => verifyJob !== job;
  try {
    let factors;
    const next = await AliquotMath.sum(n, {cancelled, onFactors: value => { factors = value; }});
    if (cancelled()) return;
    remember(n, {next, factors});
    if (next !== target) {
      $('verify-status').textContent = `Not a predecessor: s(${fmt(n)}) = ${fmt(next)}, not ${fmt(target)}.`;
      return;
    }
    if (!extras.includes(n)) extras.push(n);
    mergeCandidates(); rebuildPlot(); resultMessage();
    pinPoint(candidatePoints.find(p => p.n === n));
    $('verify-status').textContent = `Verified: ${fmt(n)} → ${fmt(target)}. Click its point to step backward. This check does not expand the exhaustive search range.`;
  } catch (error) {
    if (!cancelled()) $('verify-status').textContent = `Unresolved, not rejected: ${error.message}`;
  } finally {
    if (!cancelled()) stopVerification(false);
  }
}
function trace() {
  return {
    format: 'aliquot-reverse-chain-v1',
    direction: 'Target first; s(backward_path[k+1]) = backward_path[k].',
    backward_path: path.map(n => n.toString()),
    forward_gain: path.length ? (path[0] - path.at(-1)).toString() : null,
    frontier_search: result ? {
      source_bound: String(result.bound), checked_through: String(result.checked), complete: result.complete,
      sieve_predecessors: result.values.map(n => n.toString()),
    } : {status: 'not_completed'},
    manually_verified_predecessors: extras.map(n => n.toString()),
    scope: 'A finite backward chain, not evidence of an unbounded forward orbit.',
  };
}
function download() {
  const url = URL.createObjectURL(new Blob([JSON.stringify(trace(), null, 2) + '\n'], {type: 'application/json'}));
  const link = document.createElement('a');
  link.href = url; link.download = 'aliquot-reverse-chain.json';
  document.body.append(link); link.click(); link.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
$('root-form').onsubmit = event => { event.preventDefault(); return start(); };
$('root-decrement').onclick = () => changeSeed(-1n);
$('root-increment').onclick = () => changeSeed(1n);
$('root-input').oninput = seedButtons;
$('search-form').onsubmit = event => { event.preventDefault(); return searchPredecessors(); };
$('search-stop').onclick = () => stopSearch();
$('undo').onclick = () => path.length > 1 ? changePath(path.slice(0, -1)) : undefined;
$('scale').onchange = () => { hoveredPoint = null; layoutDirty = true; screenPoints = []; showDetails(); requestDraw(); };
$('download').onclick = download;
$('point-close').onclick = () => { clearDetails(); canvas.focus(); };
$('point-compute').onclick = computeDetails;
$('point-branch').onclick = () => pinnedPoint?.kind === 'path' && pinnedPoint.index < path.length - 1
  ? changePath(path.slice(0, pinnedPoint.index + 1)) : undefined;
$('verify-form').onsubmit = event => { event.preventDefault(); return verifyPredecessor(); };
$('verify-stop').onclick = () => stopVerification();
document.querySelectorAll('[data-root]').forEach(button => {
  button.onclick = () => { $('root-input').value = button.dataset.root; return start(); };
});
window.addEventListener('resize', resize);
const query = new URLSearchParams(window.location.search).get('n');
if (query !== null) $('root-input').value = query;
resize();
const ready = start();
