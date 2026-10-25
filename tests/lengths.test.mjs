import test from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFileSync} from 'node:fs';

const root = new URL('../', import.meta.url);
const source = ['site/length-data.js', 'site/lengths.js'].map(path => readFileSync(new URL(path, root), 'utf8')).join('\n');
const core = vm.createContext({});
vm.runInContext(source, core);
const run = code => vm.runInContext(code, core);

test('log axis has equal decades, clips at 100, and never takes log zero', () => {
  for (const width of [280, 390, 1440]) {
    const g = run(`AliquotLengths.geometry(${width}, 480, 1000)`);
    assert.equal(g.y(1), g.bottom);
    assert.equal(g.y(100), g.top);
    assert.equal(g.y(178), g.top);
    assert.equal(g.y(0), g.bottom);
    assert.ok(Math.abs(g.y(10) - (g.top + g.bottom) / 2) < 1e-10);
    assert.ok(g.y(2) > g.y(5) && g.y(5) > g.y(10));
    assert.equal(g.x('1'), g.left);
    assert.equal(g.x('1000'), g.right);
    for (const n of [1, 2, 5, 138, 276, 1000]) assert.ok(Number.isFinite(g.x(String(n))));
  }
  assert.equal(run('AliquotLengths.cap'), run('AliquotLengthData.limits.display_cap'));
});

test('138 retains 178 while 276 has only a certified 80-step lower bound', () => {
  assert.equal(run('AliquotLengthData.orbits[137].steps'), 178);
  assert.match(run('AliquotLengths.description(AliquotLengthData.orbits[137])'), /178 steps to 0.*100\+/);
  assert.equal(run('AliquotLengths.level(AliquotLengthData.orbits[275])'), 80);
  assert.equal(run('AliquotLengths.resolved(AliquotLengthData.orbits[275])'), false);
  assert.match(run('AliquotLengths.description(AliquotLengthData.orbits[275])'), /at least 80.*79 steps verified.*not a measured length/);
  assert.match(run('AliquotLengths.description(AliquotLengthData.orbits[5])'), /1 step.*fixed point 6 → 6/);
  assert.match(run('AliquotLengths.description(AliquotLengthData.orbits[219])'), /cycle 220 → 284 → 220/);
});

function harness() {
  class Node {
    constructor(tag = 'div') { this.tag = tag; this.children = []; this.attrs = {}; this.dataset = {}; this.listeners = {}; this.value = ''; this.textContent = ''; }
    setAttribute(key, value) { this.attrs[key] = String(value); if (key.startsWith('data-')) this.dataset[key.slice(5)] = String(value); }
    get classList() {
      const update = (name, add) => { const set = new Set((this.attrs.class || '').split(' ').filter(Boolean)); add ? set.add(name) : set.delete(name); this.attrs.class = [...set].join(' '); };
      return {add: name => update(name, true), remove: name => update(name, false), contains: name => (this.attrs.class || '').split(' ').includes(name)};
    }
    append(...nodes) { for (const node of nodes) { node.parent = this; this.children.push(node); } }
    replaceChildren(...nodes) { this.children = []; this.append(...nodes); }
    remove() { this.parent.children = this.parent.children.filter(node => node !== this); }
    addEventListener(name, fn) { this.listeners[name] = fn; }
    fire(name, extra = {}) { this.listeners[name]?.({target: this, preventDefault() {}, ...extra}); }
    getBoundingClientRect() { return {left: 0, top: 0, width: 1000, height: 500}; }
    closest() { return this.dataset.seed ? this : this.parent?.closest(); }
    contains(node) { return node === this || Boolean(node?.parent && this.contains(node.parent)); }
    click() { downloads.push({filename: this.download, href: this.href}); }
  }
  const ids = Object.fromEntries(['length-chart', 'seed-range', 'selected-title', 'selected-result', 'selected-detail', 'open-orbit', 'length-summary', 'download-lengths'].map(id => [id, new Node()]));
  ids['seed-range'].value = '1000';
  const buttons = ['138', '276'].map(seed => { const n = new Node('button'); n.dataset.seed = seed; return n; });
  const downloads = [], blobs = [], revoked = [];
  const document = {getElementById: id => ids[id], querySelectorAll: () => buttons,
    createElementNS: (_, tag) => new Node(tag), createElement: tag => new Node(tag), body: new Node('body')};
  const context = vm.createContext({document, window: {addEventListener() {}},
    Blob: class {constructor(parts) { this.parts = parts; }},
    URL: {createObjectURL(blob) { blobs.push(blob); return 'blob:test'; }, revokeObjectURL(url) { revoked.push(url); }},
    setTimeout: fn => fn()});
  vm.runInContext(source, context);
  return {ids, buttons, downloads, blobs, revoked,
    groups: () => ids['length-chart'].children.filter(n => n.dataset.seed)};
}

test('full chart, range changes and shortcuts retain correct counts and selection', () => {
  const h = harness(), {ids} = h;
  assert.equal(h.groups().length, 1000);
  assert.match(ids['selected-result'].textContent, /^178 steps to 0/);
  assert.match(ids['length-summary'].textContent, /961 reach 0.*22 reach a repeat.*17 unresolved/);
  assert.equal(ids['open-orbit'].href, '/orbits/?n=138');
  const point = h.groups().find(n => n.dataset.seed === '276');
  assert.equal(point.classList.contains('unresolved'), true);
  assert.ok(point.children.some(n => n.attrs.class === 'length-range'));
  ids['length-chart'].fire('pointermove', {target: point.children[1]});
  assert.equal(ids['selected-title'].textContent, 'Seed 276');
  assert.match(ids['selected-result'].textContent, /at least 80/);
  ids['seed-range'].value = '100'; ids['seed-range'].fire('change');
  assert.equal(h.groups().length, 100);
  assert.equal(ids['selected-title'].textContent, 'Seed 1');
  h.buttons[1].fire('click');
  assert.equal(ids['seed-range'].value, '300');
  assert.equal(h.groups().length, 300);
  assert.equal(ids['selected-title'].textContent, 'Seed 276');
});

test('dense points are selected by nearest coordinates rather than SVG paint order', () => {
  const h = harness(), g = run('AliquotLengths.geometry(1000, 500, 1000)');
  const laterPoint = h.groups().find(n => n.dataset.seed === '139');
  h.ids['length-chart'].fire('pointermove', {target: laterPoint, clientX: g.x('137'), clientY: g.y(2)});
  assert.equal(h.ids['selected-title'].textContent, 'Seed 137');
});

test('keyboard covers every seed including cycles and stops at range endpoints', () => {
  const {ids} = harness();
  ids['length-chart'].fire('keydown', {key: 'ArrowRight'});
  assert.equal(ids['selected-title'].textContent, 'Seed 139');
  assert.match(ids['selected-result'].textContent, /^2 steps/);
  ids['length-chart'].fire('keydown', {key: 'Home'});
  ids['length-chart'].fire('keydown', {key: 'ArrowLeft'});
  assert.equal(ids['selected-title'].textContent, 'Seed 1');
  for (let i = 0; i < 5; i++) ids['length-chart'].fire('keydown', {key: 'ArrowRight'});
  assert.match(ids['selected-result'].textContent, /fixed point 6/);
  ids['length-chart'].fire('keydown', {key: 'End'});
  ids['length-chart'].fire('keydown', {key: 'ArrowRight'});
  assert.equal(ids['selected-title'].textContent, 'Seed 1000');
});

test('download retains the full exact dataset even when displaying a small range', () => {
  const h = harness();
  h.ids['seed-range'].value = '100'; h.ids['seed-range'].fire('change');
  h.ids['download-lengths'].fire('click');
  assert.equal(h.downloads[0].filename, 'aliquot-orbit-lengths-1000.json');
  const data = JSON.parse(h.blobs[0].parts[0]);
  assert.equal(data.orbits.length, 1000);
  assert.equal(data.orbits[137].steps, 178);
  assert.equal(data.orbits[275].lower_bound, 80);
  assert.equal(typeof data.orbits[275].end, 'string');
  assert.equal(typeof data.edges.at(-1).from, 'string');
  assert.deepEqual(h.revoked, ['blob:test']);
});
