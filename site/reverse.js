'use strict';
const $ = id => document.getElementById(id);
const fmt = n => n.toLocaleString('en-CA');
const signed = n => `${n > 0n ? '+' : ''}${fmt(n)}`;
const short = n => { const s = n.toString(); return s.length > 15 ? `${s.slice(0, 7)}…${s.slice(-5)}` : fmt(n); };
const PAGE_SIZE = 8, PATH_WINDOW = 5;
let path = [], table = null, result = null, candidates = [], extras = [], page = 0;
let selection = null, searchJob = null, verifyJob = null, inspectionJob = null, inspectionIssue = '';
const records = new Map();
let nodeButtons = [];

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
function selectionKey(s) { return s ? s.kind === 'path' ? `path-${s.index}` : `candidate-${s.n}` : ''; }
function markSelection() {
  for (const button of nodeButtons) button.setAttribute('aria-pressed', String(button.dataset.key === selectionKey(selection)));
}
function mobileScroll(element) {
  if (window.matchMedia('(max-width: 800px)').matches) element.scrollIntoView({block: 'nearest'});
}
function selectNode(s, scroll = true) {
  inspectionJob = null;
  inspectionIssue = '';
  selection = s;
  markSelection();
  showDetails();
  if (scroll) mobileScroll($('point-details'));
}
function closeDetails() {
  const button = nodeButtons.find(b => b.dataset.key === selectionKey(selection));
  selectNode(null, false);
  (button || $('reverse-scroll')).focus();
}
function showDetails() {
  $('point-details').hidden = !selection;
  $('inspect-help').hidden = !!selection;
  if (!selection) return;
  const {n, kind, index} = selection;
  const next = kind === 'candidate' ? path.at(-1) : index > 0 ? path[index - 1] : knownNext(n);
  const previous = kind === 'path' ? path[index + 1] : undefined;
  const details = {...AliquotPointInfo.basic(n, next, previous),
    ...AliquotPointInfo.divisors(n, records.get(n.toString())?.factors)};
  // Unlike the home page's arrival change, this is the selected node's outgoing gain.
  details.change = n === 0n || next === undefined ? '—' : signed(next - n);
  $('point-title').textContent = kind === 'candidate' ? 'Possible predecessor' : index === 0 ? 'Original target' : `Chosen · depth ${fmt(index)}`;
  for (const field of ['value', 'size', 'residue', 'previous', 'change', 'next', 'status', 'divisors', 'divisor-summary']) {
    $('point-' + field).textContent = details[field];
  }
  PageLatex.render($('point-factorization'), details.factorizationTex, {fallback: details.factorization});
  const repeated = kind === 'candidate' ? path.indexOf(n) : path.slice(0, index).indexOf(n);
  $('point-role').textContent = (kind === 'candidate'
    ? `Verified edge: ${fmt(n)} → ${fmt(next)}.`
    : index === path.length - 1 ? 'Current backward frontier.' : 'Part of your chosen chain.')
    + (repeated >= 0 ? ` ↺ Same value as depth ${fmt(repeated)}; this closes a cycle, not unbounded growth.` : '');
  $('point-compute').hidden = !details.canCompute;
  $('point-compute').disabled = !!inspectionJob;
  $('point-compute').textContent = inspectionJob ? 'Computing…' : 'Compute divisors';
  $('point-issue').textContent = inspectionIssue;
  $('point-follow').disabled = kind === 'path' && index === path.length - 1;
  $('point-follow').textContent = kind === 'candidate' ? '← Follow predecessor'
    : index === path.length - 1 ? 'Current backward frontier' : 'Branch backward from here';
}
async function computeDetails() {
  if (!selection || inspectionJob || selection.n < 2n) return;
  const n = selection.n, job = {};
  inspectionJob = job;
  inspectionIssue = '';
  showDetails();
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
function element(tag, text, className) {
  const node = document.createElement(tag);
  if (text !== undefined) node.textContent = text;
  if (className) node.className = className;
  return node;
}
function svgElement(tag, attributes) {
  const node = document.createElementNS('http://www.w3.org/2000/svg', tag);
  for (const [key, value] of Object.entries(attributes)) node.setAttribute(key, value);
  return node;
}
function renderGrid() {
  const nodes = $('reverse-nodes'), lines = $('reverse-lines');
  nodes.replaceChildren();
  lines.replaceChildren();
  nodeButtons = [];
  if (!path.length) return;
  const visible = candidates.slice(page * PAGE_SIZE, (page + 1) * PAGE_SIZE);
  const first = Math.max(0, path.length - PATH_WINDOW);
  const width = 180 * (path.length - first + 1);
  const height = Math.max(350, 125 + visible.length * 58);
  const middle = height / 2;
  $('reverse-surface').style.width = `${width}px`;
  $('reverse-surface').style.height = `${height}px`;
  $('reverse-edges').setAttribute('viewBox', `0 0 ${width} ${height}`);
  function caption(text, x) {
    const label = element('div', text, 'grid-caption');
    label.style.left = `${x}px`;
    nodes.append(label);
  }
  function node(s, x, y, captionText, repeat) {
    const button = element('button', undefined, `orbit-node${s.kind === 'path' ? ' chosen' : ''}${repeat ? ' repeat' : ''}`);
    button.type = 'button';
    button.dataset.key = selectionKey(s);
    button.setAttribute('aria-label', `${fmt(s.n)} · ${captionText}${repeat ? ' · repeated value on chosen chain' : ''}`);
    button.title = fmt(s.n);
    button.style.left = `${x}px`;
    button.style.top = `${y}px`;
    button.append(element('span', short(s.n), 'node-value'), element('span', `${repeat ? '↺ ' : ''}${captionText}`, 'node-caption'));
    button.onclick = () => selectNode(s);
    nodes.append(button);
    nodeButtons.push(button);
  }
  function edge(x1, y1, x2, y2, className) {
    const mid = (x1 + x2) / 2;
    lines.append(svgElement('path', {d: `M ${x1} ${y1} C ${mid} ${y1}, ${mid} ${y2}, ${x2} ${y2}`, class: `reverse-edge ${className}`}));
  }
  caption('Possible predecessors', 90);
  if (!visible.length) {
    const empty = element('p', searchJob ? 'Searching…' : result
      ? result.complete ? 'No positive predecessors exist.' : 'None found in this range. Try a larger bound or test a source below.'
      : 'No completed search. Set a bound and Search.', 'grid-empty');
    nodes.append(empty);
  }
  visible.forEach((n, i) => {
    const y = 88 + i * 58, repeat = path.includes(n);
    node({kind: 'candidate', n}, 90, y, repeat ? 'cycle link' : 'inspect / choose', repeat);
    edge(160, y, 198, middle, repeat ? 'repeat' : '');
  });
  for (let index = path.length - 1; index >= first; index--) {
    const x = 270 + (path.length - 1 - index) * 180;
    const repeat = path.slice(0, index).includes(path[index]);
    caption(index === path.length - 1 ? 'Current frontier' : index === 0 ? 'Original target' : 'Chosen chain', x);
    node({kind: 'path', n: path[index], index}, x, middle, index === 0 ? 'target · depth 0' : `depth ${fmt(index)}`, repeat);
    if (index > first) edge(x + 70, middle, x + 108, middle, 'chosen');
  }
  markSelection();
  $('page-previous').disabled = page === 0;
  $('page-next').disabled = (page + 1) * PAGE_SIZE >= candidates.length;
  $('page-info').textContent = candidates.length
    ? `${fmt(page * PAGE_SIZE + 1)}–${fmt(Math.min((page + 1) * PAGE_SIZE, candidates.length))} of ${fmt(candidates.length)}` : '0 candidates';
  $('path-window').textContent = first > 0
    ? `Showing latest ${PATH_WINDOW} of ${fmt(path.length)} chosen nodes. The full chain is retained; Undo revisits it and Download saves it.`
    : 'Inspect first, then Follow predecessor. Nothing advances automatically.';
}
function mergeCandidates() {
  candidates = [...new Set([...(result?.values || []), ...extras])].sort((a, b) => a < b ? -1 : a > b ? 1 : 0);
  page = Math.min(page, Math.max(0, Math.ceil(candidates.length / PAGE_SIZE) - 1));
}
function searchMessage(text, complete = false) {
  $('search-status').textContent = text;
  $('search-status').dataset.complete = String(complete);
}
function stopSearch(announce = true) {
  const wasRunning = !!searchJob;
  searchJob = null;
  $('search-stop').disabled = true;
  $('search-progress').hidden = true;
  if (wasRunning && announce) {
    searchMessage('Search stopped. No completed search result; this does not establish that predecessors are absent.');
    renderGrid();
  }
}
async function searchPredecessors() {
  if (!path.length) return;
  let bound;
  try { bound = readBound(); }
  catch (error) { searchMessage(error.message); return; }
  stopSearch(false);
  const target = path.at(-1), job = {};
  searchJob = job;
  result = null;
  page = 0;
  mergeCandidates();
  selectNode({kind: 'path', n: target, index: path.length - 1}, false);
  $('search-stop').disabled = false;
  $('search-progress').hidden = false;
  $('search-progress').value = 0;
  searchMessage(`Finding sources m with s(m) = ${fmt(target)}, up to ${fmt(bound)}…`);
  renderGrid();
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
    mergeCandidates();
    const scope = result.complete ? target === 0n
      ? 'Complete: 1 is the only positive source of 0.'
      : `Complete: every predecessor is ≤ (n − 1)² = ${fmt(result.ceiling)}.`
      : target === 1n ? 'Partial: every prime maps to 1, and there are infinitely many primes.'
      : 'Partial: predecessors above the checked range may exist.';
    searchMessage(`${fmt(result.values.length)} found for ${fmt(target)}. Checked every source 1 ≤ m ≤ ${fmt(result.checked)}. ${scope}`, result.complete);
  } catch (error) {
    if (!cancelled()) searchMessage(`Search unresolved: ${error.message}. No conclusion about missing predecessors.`);
  } finally {
    if (!cancelled()) {
      stopSearch(false);
      renderGrid();
      showDetails();
    }
  }
}
function stopVerification(announce = true) {
  const wasRunning = !!verifyJob;
  verifyJob = null;
  $('verify-button').disabled = false;
  $('verify-stop').disabled = true;
  if (wasRunning && announce) $('verify-status').textContent = 'Verification stopped; candidate unresolved.';
}
function changePath(nextPath) {
  stopSearch(false);
  stopVerification(false);
  path = nextPath;
  extras = [];
  candidates = [];
  result = null;
  page = 0;
  $('verify-status').textContent = '';
  $('verify-input').value = '';
  $('root-value').textContent = fmt(path[0]);
  $('depth-value').textContent = fmt(path.length - 1);
  $('gain-value').textContent = signed(path[0] - path.at(-1));
  $('undo').disabled = path.length === 1;
  $('cycle-status').textContent = new Set(path).size < path.length ? '↺ Chosen chain contains a cycle; incoming branches can still be explored.' : '';
  selectNode({kind: 'path', n: path.at(-1), index: path.length - 1}, false);
  $('reverse-scroll').scrollLeft = 0;
  renderGrid();
  return searchPredecessors();
}
function start() {
  let n;
  try { n = integer($('root-input').value); }
  catch (error) {
    $('input-status').textContent = error.message;
    if (!path.length) {
      searchMessage('No grid started. Enter a valid target.');
      $('root-value').textContent = '—';
      $('gain-value').textContent = '—';
    }
    return;
  }
  $('input-status').textContent = '';
  document.querySelectorAll('[data-root]').forEach(button => button.setAttribute('aria-pressed', String(BigInt(button.dataset.root) === n)));
  return changePath([n]);
}
function followSelection() {
  if (!selection) return;
  let nextPath;
  if (selection.kind === 'candidate') {
    if (!candidates.includes(selection.n)) return;
    nextPath = [...path, selection.n];
  } else {
    if (selection.index === path.length - 1) return;
    nextPath = path.slice(0, selection.index + 1);
  }
  const pending = changePath(nextPath);
  mobileScroll($('grid-title'));
  return pending;
}
async function verifyPredecessor() {
  if (!path.length || verifyJob) return;
  let n;
  try { n = integer($('verify-input').value, true); }
  catch (error) { $('verify-status').textContent = error.message; return; }
  const target = path.at(-1), job = {};
  verifyJob = job;
  $('verify-button').disabled = true;
  $('verify-stop').disabled = false;
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
    mergeCandidates();
    page = Math.floor(candidates.indexOf(n) / PAGE_SIZE);
    renderGrid();
    selectNode({kind: 'candidate', n});
    $('verify-status').textContent = `Verified: ${fmt(n)} → ${fmt(target)}. Select Follow predecessor to extend the chain. This single check does not expand the exhaustive search range.`;
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
  const link = element('a');
  link.href = url;
  link.download = 'aliquot-reverse-chain.json';
  document.body.append(link);
  link.click();
  link.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
$('root-form').onsubmit = event => { event.preventDefault(); return start(); };
$('search-form').onsubmit = event => { event.preventDefault(); return searchPredecessors(); };
$('search-stop').onclick = () => stopSearch();
$('undo').onclick = () => path.length > 1 ? changePath(path.slice(0, -1)) : undefined;
$('download').onclick = download;
$('point-close').onclick = closeDetails;
$('point-follow').onclick = followSelection;
$('point-compute').onclick = computeDetails;
$('verify-form').onsubmit = event => { event.preventDefault(); return verifyPredecessor(); };
$('verify-stop').onclick = () => stopVerification();
$('page-previous').onclick = () => { if (page > 0) { page--; renderGrid(); } };
$('page-next').onclick = () => { if ((page + 1) * PAGE_SIZE < candidates.length) { page++; renderGrid(); } };
document.querySelectorAll('[data-root]').forEach(button => {
  button.onclick = () => { $('root-input').value = button.dataset.root; return start(); };
});
document.addEventListener('keydown', event => { if (event.key === 'Escape' && selection) { event.preventDefault(); closeDetails(); } });
const query = new URLSearchParams(window.location.search).get('n');
if (query !== null) $('root-input').value = query;
const ready = start();
