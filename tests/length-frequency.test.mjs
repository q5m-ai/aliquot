import test from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFileSync} from 'node:fs';

const root = new URL('../', import.meta.url);
const source = ['site/length-data.js', 'site/length-frequency.js'].map(file => readFileSync(new URL(file, root), 'utf8')).join('\n');
const core = vm.createContext({}); vm.runInContext(source, core);
const F = vm.runInContext('AliquotLengthFrequency', core), data = vm.runInContext('AliquotLengthData', core);
const plain = value => JSON.parse(JSON.stringify(value));
// Structural fixtures, not assertions about the actual aliquot orbits of 1–8.
const fixture = [
  ['terminated', 99, 99], ['terminated', 100, 100], ['cycle', 100, 100], ['cycle', 2, 2],
  ['factorization_limit', 79, 80], ['factorization_limit', 99, 100], ['step_limit', 256, 257], ['source_limit', 0, 1],
].map(([status, steps, lower_bound], i) => ({seed: String(i + 1), status, steps, lower_bound}));

test('inclusive thresholds distinguish proven long, proven short, and genuinely unknown', () => {
  assert.deepEqual(fixture.map(row => F.classify(row, 100)), ['short', 'long', 'long', 'short', 'unknown', 'long', 'long', 'unknown']);
  const s = F.series(fixture, {threshold: 100, window: 3});
  assert.deepEqual(plain(s.cumulative.at(-1)), {x: 8, from: 1, total: 8, lower: 4, upper: 6});
  assert.deepEqual(plain(s.recent.at(-1)), {x: 8, from: 6, total: 3, lower: 2, upper: 3});
  assert.deepEqual(plain(s.blocks.at(-1)), {x: 8, from: 7, total: 2, lower: 1, upper: 2});
  assert.equal(F.classify(fixture[0], 99), 'long');
  assert.equal(F.classify(fixture[5], 101), 'unknown');
  assert.equal(F.classify(fixture[1], 101), 'short');
});

test('parity uses eligible denominators, full recent windows, and no invented zero-seed rate', () => {
  const s = F.series(fixture, {population: 'even', window: 3});
  assert.deepEqual(plain(s.cumulative[1]), {x: 1, from: 1, total: 0, lower: 0, upper: 0});
  assert.equal(F.values(s.cumulative[1], 'share'), null);
  assert.match(F.percentage(s.cumulative[1]), /no eligible seeds/);
  assert.deepEqual(plain(s.cumulative.at(-1)), {x: 8, from: 1, total: 4, lower: 2, upper: 3});
  assert.deepEqual(plain(s.recent.at(-1)), {x: 8, from: 6, total: 2, lower: 1, upper: 2});
  assert.equal(s.recent[0].x, 3);
  assert.equal(F.series(fixture, {window: 1000}).recent.length, 0);
  assert.throws(() => F.series(fixture.slice(1)), /consecutive/);
  for (const options of [{threshold: 0}, {population: 'prime'}, {window: 0}, {bound: 0}, {bound: 10001}]) {
    assert.throws(() => F.series(fixture, options), /Invalid/);
  }
});

test('percentage bounds round outward and zero-valued axes remain finite', () => {
  assert.equal(F.percentage({total: 3, lower: 1, upper: 2}), '33.33–66.67%');
  assert.equal(F.percentage({total: 7, lower: 3, upper: 4}), '42.85–57.15%');
  assert.equal(F.percentage({total: 3, lower: 1, upper: 1}), '≈ 33.33%');
  assert.equal(F.percentage({total: 5000, lower: 6, upper: 6}), '0.12%');
  for (const count of [true, false]) for (const max of [0, 0.12, 10.56, 1056]) {
    const a = F.axis(max, count);
    assert.ok(Number.isFinite(a.ceiling) && a.ceiling > 0 && a.ceiling >= max);
    assert.equal(a.ticks[0], 0);
    assert.equal(a.ticks.at(-1), a.ceiling);
    if (count) assert.ok(a.ticks.every(Number.isInteger));
  }
});

test('actual dataset supports the finite increase but not automatic unresolved = long', () => {
  const s = F.series(data.orbits);
  assert.equal(s.cumulative[1000].lower, 22);
  assert.equal(s.cumulative[1000].upper, 30);
  assert.equal(s.cumulative.at(-1).lower, 581);
  assert.equal(s.cumulative.at(-1).upper, 1056);
  assert.equal(s.recent.at(-1).lower, 58);
  assert.equal(s.recent.at(-1).upper, 133);
  assert.ok(s.blocks.at(-1).lower > s.blocks[0].upper);
  assert.equal(F.classify(data.orbits[275], 100), 'unknown');
  assert.equal(F.classify(data.orbits[275], 50), 'long');
  assert.equal(F.classify(data.orbits[137], 100), 'long');
  assert.equal(F.classify(data.orbits[137], 200), 'short');
  assert.equal(F.series(data.orbits, {population: 'even'}).cumulative.at(-1).total, 5000);
  assert.equal(F.series(data.orbits, {population: 'odd'}).cumulative.at(-1).upper, 6);
});

function harness(initialWidth = 1000) {
  let width = initialWidth;
  const height = 420, windows = {}, blobs = [], downloads = [], revoked = [];
  class Node {
    constructor(tag = 'div') { this.tag = tag; this.attrs = {}; this.children = []; this.listeners = {}; this.style = {}; this.dataset = {}; this.hidden = false; this.textContent = ''; }
    setAttribute(key, value) { this.attrs[key] = String(value); }
    append(...nodes) { for (const node of nodes) { node.parent = this; this.children.push(node); } }
    replaceChildren(...nodes) { this.children = []; this.append(...nodes); }
    remove() { this.parent.children = this.parent.children.filter(node => node !== this); }
    addEventListener(name, fn) { this.listeners[name] = fn; }
    fire(name, event = {}) { this.listeners[name]?.({target: this, preventDefault() {}, ...event}); }
    getBoundingClientRect() { return {left: 0, top: 0, width: this === ids['frequency-details'] ? Math.min(320, width - 16) : width, height: this === ids['frequency-details'] ? 330 : height}; }
    focus() { this.focused = true; }
    click() { downloads.push({name: this.download, url: this.href}); }
  }
  const names = ['chart', 'plot', 'details', 'threshold', 'measure', 'population', 'bound', 'formula', 'measure-label', 'summary', 'blocks', 'close', 'download',
    ...['title', 'mode', 'count', 'share', 'total', 'known', 'uncertain', 'short'].map(s => `card-${s}`)];
  const ids = Object.fromEntries(names.map(name => [`frequency-${name}`, new Node()]));
  for (const [name, value] of Object.entries({threshold: '100', measure: 'share', population: 'all', bound: '10000'})) ids[`frequency-${name}`].value = value;
  const document = {getElementById: id => ids[id], createElementNS: (_, tag) => new Node(tag), createElement: tag => new Node(tag), body: new Node('body')};
  const context = vm.createContext({document, window: {addEventListener(name, fn) { windows[name] = fn; }},
    PageLatex: {render(node, tex, {fallback}) { node.textContent = fallback; node.tex = tex; }},
    Blob: class {constructor(parts) { this.parts = parts; }},
    URL: {createObjectURL(blob) { blobs.push(blob); return 'blob:frequency'; }, revokeObjectURL(url) { revoked.push(url); }},
    setTimeout: fn => fn()});
  vm.runInContext(source, context);
  const eventAt = x => {
    const min = ids['frequency-measure'].value === 'recent' ? 1000 : 0, max = Number(ids['frequency-bound'].value);
    return {clientX: 64 + (x - min) / Math.max(1, max - min) * (Math.max(width, 280) - 89), clientY: 200};
  };
  return {ids, blobs, downloads, revoked,
    change(name, value) { ids[`frequency-${name}`].value = String(value); ids[`frequency-${name}`].fire('change'); },
    hover(x) { ids['frequency-chart'].fire('pointermove', eventAt(x)); },
    pin(x) { ids['frequency-chart'].fire('click', eventAt(x)); },
    key(key) { ids['frequency-chart'].fire('keydown', {key}); },
    resize(w) { width = w; windows.resize(); }};
}

test('default share, cumulative count and full-window recent view show exact bounded results', () => {
  const h = harness(), {ids} = h;
  assert.equal(ids['frequency-details'].hidden, true);
  assert.match(ids['frequency-summary'].textContent, /581 confirmed 100\+.*475 still uncertain.*5.81–10.56%/);
  assert.equal(ids['frequency-blocks'].children.length, 10);
  assert.match(ids['frequency-formula'].tex, /n\\in P/);
  h.change('measure', 'count');
  assert.match(ids['frequency-measure-label'].textContent, /Cumulative count.*linear/);
  h.hover(1000);
  assert.equal(ids['frequency-card-count'].textContent, '22–30 with length ≥ 100');
  assert.equal(ids['frequency-card-share'].textContent, '2.20–3.00%');
  h.change('measure', 'recent');
  assert.match(ids['frequency-summary'].textContent, /9,001–10,000.*58 confirmed.*75 still uncertain.*5.80–13.30%/);
  h.key('Home');
  assert.equal(ids['frequency-card-title'].textContent, 'Seeds 1–1,000');
  h.change('bound', 1000);
  assert.equal(ids['frequency-blocks'].children.length, 1);
  const paths = ids['frequency-chart'].children.filter(n => n.tag === 'path');
  assert.ok(paths.length >= 3 && paths.every(n => !/NaN|Infinity/.test(n.attrs.d)));
});

test('threshold/population controls update both denominators and the block table', () => {
  const h = harness(), {ids} = h;
  h.change('population', 'even');
  assert.match(ids['frequency-summary'].textContent, /5,000 even starts.*575 confirmed.*11.50–21.00%/);
  h.key('Home');
  assert.match(ids['frequency-card-share'].textContent, /no eligible seeds/);
  h.key('ArrowRight'); assert.equal(ids['frequency-card-total'].textContent, '1 even starts');
  h.change('population', 'odd');
  assert.match(ids['frequency-summary'].textContent, /6 confirmed.*0 still uncertain.*0.12%/);
  h.change('threshold', 200);
  assert.match(ids['frequency-summary'].textContent, /confirmed 200\+/);
  assert.match(ids['frequency-formula'].tex, /L_\{200\}/);
  assert.equal(ids['frequency-blocks'].children.at(-1).children[1].textContent, '500');
  h.change('bound', 1000); h.change('measure', 'recent');
  assert.match(ids['frequency-summary'].textContent, /0 confirmed.*0 still uncertain.*0.00%/);
});

test('hover/pin/keyboard/close behave like the shared floating cards', () => {
  const h = harness(), {ids} = h, card = ids['frequency-details'];
  h.hover(1000); assert.equal(card.hidden, false); assert.equal(card.dataset.pinned, 'false');
  h.pin(1000); h.hover(5000);
  assert.equal(ids['frequency-card-title'].textContent, 'Seeds 1–1,000');
  assert.equal(card.dataset.pinned, 'true');
  ids['frequency-chart'].fire('pointerleave'); assert.equal(card.hidden, false);
  h.key('End'); assert.equal(ids['frequency-card-count'].textContent, '581–1,056 with length ≥ 100');
  h.key('ArrowLeft'); assert.equal(ids['frequency-card-title'].textContent, 'Seeds 1–9,999');
  h.key('Escape'); assert.equal(card.hidden, true);
  h.key('Enter'); assert.equal(card.dataset.pinned, 'true');
  ids['frequency-close'].fire('click'); assert.equal(card.hidden, true); assert.equal(ids['frequency-chart'].focused, true);
  h.hover(9999); assert.equal(card.hidden, true);
  h.hover(1000); assert.equal(card.hidden, false);
  ids['frequency-chart'].fire('pointerleave'); assert.equal(card.hidden, true);
});

test('a pinned aggregate card stays bounded across resize and control changes', () => {
  const h = harness(), card = h.ids['frequency-details'];
  h.pin(10000);
  h.resize(390);
  assert.equal(card.hidden, false);
  assert.ok(parseFloat(card.style.left) >= 8);
  assert.ok(parseFloat(card.style.left) + card.getBoundingClientRect().width <= 382);
  h.change('bound', 1000);
  assert.equal(h.ids['frequency-card-title'].textContent, 'Seeds 1–1,000');
  h.change('measure', 'recent');
  assert.equal(h.ids['frequency-card-title'].textContent, 'Seeds 1–1,000');
});

test('download records exact counts/denominators, source bounds and filters, not rounded rates', () => {
  const h = harness();
  h.change('population', 'even'); h.change('threshold', 50); h.change('bound', 5000);
  h.ids['frequency-download'].fire('click');
  assert.equal(h.downloads[0].name, 'aliquot-frequency-50-even-5000.json');
  const artifact = JSON.parse(h.blobs[0].parts[0]);
  assert.equal(artifact.threshold, 50); assert.equal(artifact.population, 'even'); assert.equal(artifact.bound, 5000);
  assert.equal(artifact.source_limits.max_steps, 256);
  assert.equal(artifact.cumulative.at(-1).total, 2500);
  assert.equal(artifact.recent[0].total, 500);
  assert.deepEqual(Object.keys(artifact.recent[0]), ['x', 'from', 'total', 'lower', 'upper']);
  assert.deepEqual(h.revoked, ['blob:frequency']);
});
