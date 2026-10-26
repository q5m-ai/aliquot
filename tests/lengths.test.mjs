import test from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFileSync} from 'node:fs';

const root = new URL('../', import.meta.url);
const source = ['site/math.js', 'site/point-info.js', 'site/length-data.js', 'site/lengths.js']
  .map(path => readFileSync(new URL(path, root), 'utf8')).join('\n');
const core = vm.createContext({});
vm.runInContext(source, core);
const run = code => vm.runInContext(code, core);

test('log axis has equal decades, clips at 100, and scales to 10,000 seeds', () => {
  for (const width of [280, 390, 1440]) for (const bound of [100, 1000, 5000, 10000]) {
    const g = run(`AliquotLengths.geometry(${width}, 480, ${bound})`);
    assert.equal(g.y(1), g.bottom);
    assert.equal(g.y(100), g.top);
    assert.equal(g.y(178), g.top);
    assert.equal(g.y(0), g.bottom);
    assert.ok(Math.abs(g.y(10) - (g.top + g.bottom) / 2) < 1e-10);
    assert.ok(g.y(2) > g.y(5) && g.y(5) > g.y(10));
    assert.equal(g.x('1'), g.left);
    assert.equal(g.x(String(bound)), g.right);
    assert.ok(Number.isFinite(g.x(String(bound))));
  }
  assert.equal(run('AliquotLengths.cap'), run('AliquotLengthData.limits.display_cap'));
  assert.equal(run('AliquotLengthData.orbits.length'), 10000);
});

test('138 retains 178 while 276 has only a certified 80-step lower bound', () => {
  assert.equal(run('AliquotLengthData.orbits[137].steps'), 178);
  assert.match(run('AliquotLengths.description(AliquotLengthData.orbits[137])'), /178 steps to 0.*100\+/);
  assert.equal(run('AliquotLengths.level(AliquotLengthData.orbits[275])'), 80);
  assert.equal(run('AliquotLengths.resolved(AliquotLengthData.orbits[275])'), false);
  assert.match(run('AliquotLengths.description(AliquotLengthData.orbits[275])'), /at least 80.*79 steps verified.*not a measured length/);
  assert.match(run('AliquotLengths.description(AliquotLengthData.orbits[5])'), /1 step.*fixed point 6 → 6/);
  assert.match(run('AliquotLengths.description(AliquotLengthData.orbits[219])'), /cycle 220 → 284 → 220/);
  assert.match(run('AliquotLengths.description(AliquotLengthData.orbits.find(row => row.status === "step_limit"))'), /at least 257.*256 steps verified.*step budget/);
});

test('shared card formatting uses every seed’s certified factors, not floating point or new factorization', () => {
  assert.equal(run(`(() => {
    const edges = new Map(AliquotLengthData.edges.map(edge => [edge.from, edge]));
    for (const row of AliquotLengthData.orbits) {
      const edge = edges.get(row.seed), details = AliquotLengths.pointDetails(row, edge);
      if (details.canCompute || details.next !== BigInt(edge.to).toLocaleString('en-CA')) return false;
      if (details.value !== BigInt(row.seed).toLocaleString('en-CA')) return false;
    }
    return true;
  })()`), true);
  const detail = run(`AliquotLengths.pointDetails(AliquotLengthData.orbits[9999], AliquotLengthData.edges.find(edge => edge.from === '10000'))`);
  assert.equal(detail.value, '10,000');
  assert.equal(detail.status, 'Abundant');
  assert.equal(detail.next, '14,211');
  assert.equal(detail.factorizationTex, '2^{4} \\times 5^{4}');
  assert.match(detail['divisor-summary'], /^24 divisors · sum 14,211$/);
});

function harness(initialWidth = 1000) {
  let width = initialWidth;
  const height = 500, downloads = [], blobs = [], revoked = [], rendered = [], windows = {};
  class Node {
    constructor(tag = 'div') {
      this.tag = tag; this.children = []; this.attrs = {}; this.dataset = {}; this.listeners = {};
      this.value = ''; this.textContent = ''; this.style = {}; this.hidden = false;
    }
    setAttribute(key, value) { this.attrs[key] = String(value); if (key.startsWith('data-')) this.dataset[key.slice(5)] = String(value); }
    get classList() { return {contains: name => (this.attrs.class || '').split(' ').includes(name)}; }
    append(...nodes) { for (const node of nodes) { node.parent = this; this.children.push(node); } }
    replaceChildren(...nodes) { for (const old of this.children) old.parent = null; this.children = []; this.append(...nodes); }
    remove() { this.parent.children = this.parent.children.filter(node => node !== this); }
    addEventListener(name, fn) { this.listeners[name] = fn; }
    fire(name, extra = {}) { this.listeners[name]?.({target: this, preventDefault() {}, ...extra}); }
    getBoundingClientRect() {
      return {left: 0, top: 0, width: this === ids['point-details'] ? Math.min(320, width - 16) : width,
        height: this === ids['point-details'] ? this.dataset.pinned === 'true' ? 650 : 340 : height};
    }
    closest() { return this.dataset.seed ? this : this.parent?.closest(); }
    contains(node) { return node === this || Boolean(node?.parent && this.contains(node.parent)); }
    click() { downloads.push({filename: this.download, href: this.href}); }
    focus() { this.focused = true; }
  }
  const ids = Object.fromEntries(['chart', 'length-chart', 'seed-range', 'length-summary', 'download-lengths',
    ...['details', 'title', 'mode', 'close', 'value', 'length', 'status', 'next', 'size', 'residue', 'factorization',
      'divisors', 'divisor-summary', 'peak', 'frontier', 'orbit', 'reverse'].map(field => `point-${field}`)].map(id => [id, new Node()]));
  ids['seed-range'].value = '1000';
  const buttons = ['138', '276'].map(seed => { const n = new Node('button'); n.dataset.seed = seed; return n; });
  const document = {getElementById: id => ids[id], querySelectorAll: () => buttons,
    createElementNS: (_, tag) => new Node(tag), createElement: tag => new Node(tag), body: new Node('body')};
  const context = vm.createContext({document, window: {addEventListener(name, fn) { windows[name] = fn; }},
    PageLatex: {render(node, tex, {fallback}) { node.textContent = fallback; rendered.push(tex); }},
    Blob: class {constructor(parts) { this.parts = parts; }},
    URL: {createObjectURL(blob) { blobs.push(blob); return 'blob:test'; }, revokeObjectURL(url) { revoked.push(url); }},
    setTimeout: fn => fn()});
  vm.runInContext(source, context);
  vm.runInContext(`AliquotMath.sum = () => { throw new Error('Hover must not factor'); };`, context);
  const groups = () => ids['length-chart'].children.filter(n => n.dataset.seed);
  const point = seed => groups().find(n => n.dataset.seed === String(seed));
  return {ids, buttons, downloads, blobs, revoked, rendered, groups, point,
    range(value) { ids['seed-range'].value = String(value); ids['seed-range'].fire('change'); },
    resize(value) { width = value; windows.resize(); },
    hover(seed) { ids['length-chart'].fire('pointermove', {target: point(seed)}); },
    pin(seed) { ids['length-chart'].fire('click', {target: point(seed)}); }};
}

test('range extends to 10,000 without removing the smaller views or inflating SVG hit nodes', () => {
  const h = harness(), {ids} = h;
  assert.equal(h.groups().length, 1000);
  assert.equal(ids['point-details'].hidden, true);
  assert.match(ids['length-summary'].textContent, /961 reach 0.*22 reach a repeat.*17 unresolved/);
  h.range(5000); assert.equal(h.groups().length, 5000);
  h.range(10000); assert.equal(h.groups().length, 10000);
  assert.match(ids['length-summary'].textContent, /10,000 starts.*8,951 reach 0.*224 reach a repeat.*825 unresolved/);
  assert.ok(h.groups().reduce((count, group) => count + group.children.length, 0) < 12000);
  assert.ok(ids['length-chart'].children.some(n => n.tag === 'text' && n.textContent === '10,000'));
  h.hover(10000);
  assert.equal(ids['point-value'].textContent, '10,000');
  assert.equal(ids['point-next'].textContent, '14,211');
  h.range(100); assert.equal(h.groups().length, 100);
  assert.equal(ids['point-details'].hidden, true);
  h.buttons[1].fire('click');
  assert.equal(ids['seed-range'].value, '300');
  assert.equal(h.groups().length, 300);
  assert.equal(ids['point-title'].textContent, 'Seed 276');
  assert.equal(ids['point-details'].dataset.pinned, 'true');
});

test('hover uses the shared exact card, is transient, and never computes an orbit', () => {
  const h = harness(), {ids} = h;
  h.hover(138);
  assert.equal(ids['point-details'].hidden, false);
  assert.equal(ids['point-details'].dataset.pinned, 'false');
  assert.equal(ids['point-mode'].textContent, 'Click to pin');
  assert.equal(ids['point-value'].textContent, '138');
  assert.equal(ids['point-status'].textContent, 'Abundant');
  assert.equal(ids['point-next'].textContent, '150');
  assert.equal(ids['point-size'].textContent, '3 digits · even');
  assert.equal(ids['point-residue'].textContent, '6 · B6₁₂');
  assert.equal(ids['point-factorization'].textContent, '2 × 3 × 23');
  assert.equal(h.rendered.at(-1), '2 \\times 3 \\times 23');
  assert.equal(ids['point-divisors'].textContent, '1, 2, 3, 6, 23, 46, 69');
  assert.equal(ids['point-divisor-summary'].textContent, '7 divisors · sum 150');
  assert.match(ids['point-length'].textContent, /^178 steps to 0/);
  assert.equal(ids['point-peak'].textContent, '179,931,895,322');
  assert.equal(ids['point-orbit'].href, '/orbits/?n=138');
  assert.equal(ids['point-reverse'].href, '/reverse/?n=138');
  const renders = h.rendered.length;
  h.hover(138); assert.equal(h.rendered.length, renders);
  ids['length-chart'].fire('pointerleave');
  assert.equal(ids['point-details'].hidden, true);
  h.hover(137); assert.equal(ids['point-status'].textContent, 'Prime · deficient');
  h.hover(6); assert.equal(ids['point-status'].textContent, 'Perfect');
  h.hover(1); assert.equal(ids['point-divisors'].textContent, 'None');
  assert.equal(ids['point-next'].textContent, '0');
});

test('click/touch pins, hover cannot replace a pin, close suppresses immediate reopening', () => {
  const h = harness(), {ids} = h;
  ids['length-chart'].fire('click', {target: h.point(276), pointerType: 'touch'});
  assert.equal(ids['point-details'].dataset.pinned, 'true');
  assert.match(ids['point-length'].textContent, /at least 80.*79 steps verified/);
  h.hover(138);
  ids['length-chart'].fire('pointerleave');
  assert.equal(ids['point-title'].textContent, 'Seed 276');
  assert.equal(ids['point-details'].hidden, false);
  ids['point-close'].fire('click');
  assert.equal(ids['point-details'].hidden, true);
  assert.equal(ids['length-chart'].focused, true);
  h.hover(276); assert.equal(ids['point-details'].hidden, true);
  h.hover(138); assert.equal(ids['point-details'].hidden, false);
  h.pin(138); h.pin(138); assert.equal(ids['point-details'].hidden, true);
  h.pin(138); ids['length-chart'].fire('click'); assert.equal(ids['point-details'].hidden, true);
});

test('dense points use nearest coordinates, including at the 10k range, not SVG paint order', () => {
  const h = harness();
  for (const bound of [1000, 10000]) {
    h.range(bound);
    const g = run(`AliquotLengths.geometry(1000, 500, ${bound})`);
    h.ids['length-chart'].fire('pointermove', {target: h.point(139), clientX: g.x('137'), clientY: g.y(2)});
    assert.equal(h.ids['point-title'].textContent, 'Seed 137');
  }
});

test('keyboard inspects every seed, pins/unpins and closes without losing exact outcomes', () => {
  const h = harness(), {ids} = h;
  ids['length-chart'].fire('keydown', {key: 'ArrowRight'});
  assert.equal(ids['point-title'].textContent, 'Seed 139');
  ids['length-chart'].fire('keydown', {key: 'Enter'});
  assert.equal(ids['point-details'].dataset.pinned, 'true');
  ids['length-chart'].fire('keydown', {key: 'Home'});
  ids['length-chart'].fire('keydown', {key: 'ArrowLeft'});
  assert.equal(ids['point-title'].textContent, 'Seed 1');
  for (let i = 0; i < 5; i++) ids['length-chart'].fire('keydown', {key: 'ArrowRight'});
  assert.match(ids['point-length'].textContent, /fixed point 6/);
  h.range(10000);
  ids['length-chart'].fire('keydown', {key: 'End'});
  ids['length-chart'].fire('keydown', {key: 'ArrowRight'});
  assert.equal(ids['point-title'].textContent, 'Seed 10,000');
  assert.equal(ids['point-details'].dataset.pinned, 'true');
  ids['length-chart'].fire('keydown', {key: 'Escape'});
  assert.equal(ids['point-details'].hidden, true);
  ids['length-chart'].fire('keydown', {key: ' '});
  assert.equal(ids['point-details'].dataset.pinned, 'true');
  h.range(100);
  assert.equal(ids['point-details'].hidden, true);
});

test('card flips/clamps horizontally, follows resize, and permits tall pinned details', () => {
  const h = harness(), card = h.ids['point-details'];
  h.pin(1000);
  assert.ok(parseFloat(card.style.left) + card.getBoundingClientRect().width <= 992);
  h.resize(390);
  assert.equal(card.hidden, false);
  assert.ok(parseFloat(card.style.left) >= 8);
  assert.ok(parseFloat(card.style.left) + card.getBoundingClientRect().width <= 382);
  assert.equal(card.style.top, '8px');
  assert.ok(card.getBoundingClientRect().height > 500);
  h.resize(280);
  assert.ok(parseFloat(card.style.left) + card.getBoundingClientRect().width <= 272);
});

test('download retains all 10,000 exact records regardless of selected range', () => {
  const h = harness();
  h.range(100);
  h.ids['download-lengths'].fire('click');
  assert.equal(h.downloads[0].filename, 'aliquot-orbit-lengths-10000.json');
  const data = JSON.parse(h.blobs[0].parts[0]);
  assert.equal(data.orbits.length, 10000);
  assert.equal(data.orbits[137].steps, 178);
  assert.equal(data.orbits[275].lower_bound, 80);
  assert.equal(data.orbits.at(-1).seed, '10000');
  assert.equal(typeof data.orbits[275].end, 'string');
  assert.equal(typeof data.edges.at(-1).from, 'string');
  assert.deepEqual(h.revoked, ['blob:test']);
});
