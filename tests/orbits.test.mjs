import test from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFileSync} from 'node:fs';

const root = new URL('../', import.meta.url);
// Keep the small arithmetic/UI regressions stable; the served 1–1,000 graph
// is checked separately by Python and a full-dataset browser smoke test.
const read = name => readFileSync(new URL(name === 'site/orbit-data.js' ? 'tests/fixtures/orbit-data-100.js' : name, root), 'utf8');
const mathSource = ['site/orbit-data.js', 'site/orbit-graph.js'].map(read).join('\n');
const core = vm.createContext({});
vm.runInContext(mathSource + '\nconst model = AliquotOrbitGraph.create(AliquotOrbitData);', core);
const run = code => vm.runInContext(code, core);
const plain = value => JSON.parse(JSON.stringify(value));

test('every seed is represented in a merged functional graph, without s(0)', () => {
  assert.equal(run('model.nodes.size'), 117);
  assert.equal(run('model.data.edges.length'), 116);
  assert.equal(run('model.data.orbits.length'), 100);
  assert.equal(run('model.data.nodes.filter(n => n.prime).length'), 25);
  assert.equal(run('model.data.nodes.filter(n => n.leaf).length'), 45);
  assert.deepEqual(plain(run('model.data.nodes.filter(n => n.untouchable).map(n => n.id)')), ['2', '5', '52', '88', '96']);
  assert.equal(run('model.nodes.get("0").next'), null);
  assert.equal(run('model.data.edges.some(e => e.from === "0")'), false);
  assert.equal(run('model.nodes.get("259").prime'), false);
});

test('trace walks forward, includes zero, and stops exactly at a repeat', () => {
  assert.deepEqual(plain(run('model.trace("52")')), {path: ['52', '46', '26', '16', '15', '9', '4', '3', '1', '0'], cycle: [], status: 'terminated'});
  assert.deepEqual(plain(run('model.trace("95")')), {path: ['95', '25', '6', '6'], cycle: ['6'], status: 'cycle'});
  assert.deepEqual(plain(run('model.trace("28")')), {path: ['28', '28'], cycle: ['28'], status: 'cycle'});
  assert.deepEqual(plain(run('model.trace("0")')), {path: ['0'], cycle: [], status: 'terminated'});
  assert.throws(() => run('model.trace("121")'), /not in the displayed graph/);
  for (const orbit of run('model.data.orbits')) {
    assert.deepEqual(plain(run(`model.trace("${orbit.seed}")`)), plain({path: orbit.path, cycle: orbit.cycle, status: orbit.status}));
  }
});

test('global certificates distinguish 52, the displayed-only leaf 12, and infinite primes', () => {
  const fiftyTwo = run('model.info("52")'), twelve = run('model.info("12")');
  assert.match(fiftyTwo.incoming, /None.*leaf in the loaded graph/);
  assert.match(fiftyTwo.predecessors, /None anywhere.*proved/);
  assert.match(fiftyTwo.proof, /Complete.*2,601/);
  assert.match(twelve.incoming, /None.*leaf in the loaded graph/);
  assert.equal(twelve.predecessors, '1 total: 121');
  assert.match(twelve.proof, /121/);
  assert.equal(run('model.info("1").predecessors'), 'All primes · infinitely many');
  assert.match(run('model.info("1").incoming'), /^25:/);
  assert.equal(run('model.info("0").predecessors'), '1 total: 1');
});

test('partial absence and forward cutoffs remain explicitly unresolved', () => {
  const result = run(`(() => {
    const data = JSON.parse(JSON.stringify(AliquotOrbitData));
    const node = data.nodes.find(n => n.id === '52');
    node.next = null;
    node.predecessors = {status: 'partial', ceiling: '2601', checked_through: '10', values: []};
    const partial = AliquotOrbitGraph.create(data);
    return {info: partial.info('52'), trace: partial.trace('52')};
  })()`);
  assert.match(result.info.predecessors, /0 found.*partial/);
  assert.doesNotMatch(result.info.predecessors, /None anywhere|untouchable/);
  assert.match(result.info.proof, /Absence is not proved/);
  assert.deepEqual(plain(result.trace), {path: ['52'], cycle: [], status: 'unresolved'});
});

test('deterministic geometry fits all nodes; edges flow right and cycles are visible', () => {
  const layout = run('AliquotOrbitGraph.layout(model)');
  assert.equal(layout.bands.length, 3);
  assert.match(layout.bands[0].label, /96 starting values/);
  assert.match(layout.bands[1].label, /Fixed point 6.*3 starting/);
  for (const [id, p] of layout.positions) {
    assert.ok([p.x, p.y, p.r].every(Number.isFinite), id);
    assert.ok(p.x >= 0 && p.x < layout.width && p.y >= 0 && p.y < layout.height, id);
    const next = run(`model.nodes.get('${id}').next`);
    if (next !== null) assert.ok(p.x <= layout.positions.get(next).x);
  }
  const positions = [...layout.positions];
  assert.deepEqual(plain(positions), plain([...run('AliquotOrbitGraph.layout(model)').positions]));
  for (let i = 0; i < positions.length; i++) for (let j = i + 1; j < positions.length; j++) {
    const [, a] = positions[i], [, b] = positions[j];
    assert.ok(Math.hypot(a.x - b.x, a.y - b.y) >= 21.99, 'nodes must not overlap');
  }
  assert.match(run('AliquotOrbitGraph.curve({x: 100, y: 100, r: 5}, {x: 100, y: 100, r: 5}, true)'), /C 65 60, 135 60/);
  assert.doesNotMatch(run('AliquotOrbitGraph.curve({x: 100, y: 100, r: 5}, {x: 100, y: 200, r: 5})'), /NaN|Infinity/);
});

test('window geometry keeps left-to-right flow and labels hidden cuts, not unresolved math', () => {
  const result = run(`(() => {
    const visible = new Set(['52', '46', '6', '28']);
    return {layout: AliquotOrbitGraph.layout(model, {visible}), cut: model.trace('52', visible), full: model.trace('52')};
  })()`);
  assert.equal(result.layout.positions.size, 4);
  assert.ok(result.layout.positions.get('52').x < result.layout.positions.get('46').x);
  assert.ok(result.layout.bands.some(b => b.label.includes('Known continuation outside window')));
  assert.ok(result.layout.bands.every(b => !b.label.includes('Unresolved')));
  assert.equal(result.cut.status, 'hidden');
  assert.equal(result.full.status, 'terminated');
  assert.deepEqual(plain(result.cut.path), ['52', '46']);
});

test('the rolling window is display-only, deterministic, capped and reversible', () => {
  const result = run(`(() => {
    const original = JSON.stringify(model.data), view = AliquotOrbitGraph.createWindow(model);
    const initial = view.save();
    for (const orbit of model.data.orbits) view.forward(model, orbit.seed, true);
    const grown = view.ids, saved = view.save();
    view.reset(model); const reset = view.save();
    view.restore(saved, model);
    return {initial, grown: [...grown], reset, restored: [...view.ids], unchanged: original === JSON.stringify(model.data)};
  })()`);
  assert.equal(result.initial.visible.length, 42);
  assert.equal(result.grown.length, 80);
  assert.ok(result.grown.includes('100'));
  assert.deepEqual(plain(result.reset), plain(result.initial));
  assert.deepEqual(plain(result.restored), plain(result.grown));
  assert.equal(result.unchanged, true);
  assert.throws(() => run('AliquotOrbitGraph.createWindow(model, {maxNodes: 81})'), /Invalid window/);
});

test('long forward paths roll beyond the cap; incoming batches do not starve unseen branches', () => {
  const result = run(`(() => {
    // Structural fixture only: these numbered chain edges are not arithmetic claims.
    const nodes = Array.from({length: 121}, (_, i) => ({id: String(i), next: i === 120 ? null : String(i + 1), incoming: [], starts: [], seed: false}));
    const chain = AliquotOrbitGraph.create({nodes, edges: [], orbits: []});
    const view = AliquotOrbitGraph.createWindow(chain, {maxNodes: 20, forwardBatch: 8});
    view.forward(chain, '1', true);
    const sizes = [];
    for (let i = 0; i < 16; i++) { view.forward(chain, '1'); sizes.push(view.ids.size); }
    const end = [...view.ids];
    nodes[1].incoming = nodes.slice(2).map(n => n.id);
    const seen = new Set();
    for (let i = 0; i < 8; i++) for (const id of view.incoming(chain, '1')) seen.add(id);
    return {end, sizes, seen: [...seen], final: [...view.ids]};
  })()`);
  assert.ok(result.end.includes('120'));
  assert.ok(result.sizes.every(n => n <= 20));
  assert.ok(result.end.includes('1'));
  assert.ok(result.seen.includes('119'));
  assert.ok(result.final.length <= 20);
  assert.ok(result.final.includes('1'));
});

test('zoom preserves the pointer anchor and has finite bounded scale', () => {
  const c = run('AliquotOrbitGraph.fit(390, 520, AliquotOrbitGraph.layout(model))');
  assert.ok(c.scale > 0);
  const after = run(`AliquotOrbitGraph.zoom(${JSON.stringify(c)}, 2, {x: 70, y: 130})`);
  assert.ok(Math.abs((70 - c.x) / c.scale - (70 - after.x) / after.scale) < 1e-8);
  assert.ok(Math.abs((130 - c.y) / c.scale - (130 - after.y) / after.scale) < 1e-8);
  assert.equal(run('AliquotOrbitGraph.zoom({x:0,y:0,scale:1}, 1000, {x:50,y:50}).scale'), 8);
  assert.equal(run('AliquotOrbitGraph.zoom({x:0,y:0,scale:1}, 0, {x:50,y:50}).scale'), .1);
});

// Dependency-free DOM/PointerEvent harness; real Chromium smoke tests separately
// exercise layout, CSP, native SVG focus, mouse capture, and mobile touch.
function browser({query = '', width = 1500, height = 700, large = false} = {}) {
  const size = {width, height}, observers = [], downloads = [], blobs = new Map(), timers = [];
  class Element {
    constructor(tag = 'div', id = '') {
      this.tagName = tag; this.id = id; this.attributes = {}; this.children = []; this.events = new Map();
      this.dataset = {}; this.style = {}; this.hidden = false; this.disabled = false; this.textContent = ''; this.innerHTML = ''; this.value = '';
      const classes = new Set();
      this.classList = {add: (...values) => values.forEach(v => classes.add(v)), remove: (...values) => values.forEach(v => classes.delete(v)),
        contains: value => classes.has(value), toggle: (value, force = !classes.has(value)) => { if (force) classes.add(value); else classes.delete(value); return force; }};
    }
    get lastElementChild() { return this.children.at(-1); }
    matches(selector) { return selector === ':focus-visible'; }
    get clientWidth() { return size.width; }
    get clientHeight() { return size.height; }
    get offsetWidth() { return Math.min(320, size.width - 16); }
    get offsetHeight() { return 450; }
    getBoundingClientRect() { return {left: 40, top: 60, width: size.width, height: size.height}; }
    setAttribute(key, value) {
      this.attributes[key] = String(value);
      if (key === 'class') this.classList.add(...String(value).split(' '));
      if (key.startsWith('data-')) this.dataset[key.slice(5)] = String(value);
    }
    getAttribute(key) { return this.attributes[key] ?? null; }
    append(...elements) { elements.forEach(el => { el.parent = this; this.children.push(el); }); }
    replaceChildren(...elements) { this.children = []; this.append(...elements); }
    addEventListener(type, handler) { if (!this.events.has(type)) this.events.set(type, []); this.events.get(type).push(handler); }
    closest() { for (let element = this; element; element = element.parent) if (element.getAttribute('data-node') !== null) return element; return null; }
    setPointerCapture() {}
    focus() { this.focused = true; this.fire('focus'); }
    fire(type, options = {}) {
      const event = {target: this, button: 0, pointerType: 'mouse', pointerId: 1, clientX: 150, clientY: 200,
        preventDefault() { this.prevented = true; }, stopPropagation() { this.stopped = true; }, ...options};
      const pending = [];
      for (let el = this; el; el = el.parent) {
        for (const handler of el.events.get(type) ?? []) pending.push(handler(event));
        if (event.stopped || ['focus', 'blur', 'pointerenter', 'pointerleave'].includes(type)) break;
      }
      event.done = Promise.all(pending);
      return event;
    }
    click() { if (this.tagName === 'a') downloads.push(this); return this.fire('click', {detail: 0}).done; }
    remove() { this.parent.children = this.parent.children.filter(n => n !== this); }
  }
  const elements = new Map([...read('site/orbits/index.html').matchAll(/\bid="([^"]+)"/g)].map(match => [match[1], new Element('div', match[1])]));
  const el = id => elements.get(id) ?? null;
  el('chart').append(el('graph'), el('point-details'));
  el('graph').append(el('graph-world'));
  el('graph-world').append(el('graph-bands'), el('graph-edges'), el('graph-nodes'));
  el('point-details').append(el('point-close'));
  el('source-bound').value = '10000';
  const document = {getElementById: el, createElement: tag => new Element(tag), createElementNS: (_ns, tag) => new Element(tag), querySelectorAll: () => [], body: new Element('body')};
  const context = vm.createContext({document, location: {search: query}, URLSearchParams, Blob,
    URL: {createObjectURL(blob) { const url = `blob:test-${blobs.size}`; blobs.set(url, blob); return url; }, revokeObjectURL(url) { blobs.delete(url); }},
    setTimeout: (callback, delay) => delay === 1000 ? timers.push(callback) : setTimeout(callback, 0),
    ResizeObserver: class {constructor(callback) { observers.push(callback); } observe() {}},
  });
  vm.runInContext(['site/vendor/katex/katex.min.js', 'site/latex.js', 'site/math.js', 'site/point-info.js',
    'site/reverse-math.js', 'site/orbit-data.js', 'site/orbit-graph.js', 'site/orbit-session.js', 'site/orbits.js']
    .map(name => large && name === 'site/orbit-data.js' ? readFileSync(new URL(name, root), 'utf8') : read(name)).join('\n'), context);
  const node = id => el('graph-nodes').children.find(n => n.getAttribute('data-node') === String(id));
  const pointer = (type, id, options = {}) => el('graph').fire(type, {target: id === null ? el('graph') : node(id), ...options});
  return {el, node, size, timers, downloads, blobs, pointer,
    transform: () => el('graph-world').getAttribute('transform'),
    hover: id => node(id).fire('pointerenter'),
    tap(id, options = {}) { pointer('pointerdown', id, options); pointer('pointerup', id, options); },
    find(id) { el('find-node').value = String(id); return el('find-form').fire('submit').done; },
    press(key) { return el('graph').fire('keydown', {key}); },
    resize(w, h) { size.width = w; size.height = h; observers.forEach(callback => callback()); },
    active: () => el('graph-nodes').children.filter(n => n.classList.contains('active')).map(n => n.getAttribute('data-node')),
  };
}

test('the actual served 1–1,000 graph loads, expands, adds starts, and resets', async () => {
  const b = browser({large: true});
  assert.equal(b.el('graph-nodes').children.length, 42);
  assert.equal(b.el('graph-edges').children.length, 41);
  for (let n = 1; n <= 30; n++) assert.ok(b.node(n));
  assert.equal(b.node(1000), undefined);
  assert.match(b.el('graph-summary').textContent, /42\/80 nodes.*1,665 values.*1,000 starts/);
  assert.match(b.el('route-status').textContent, /unresolved computation frontiers/);
  await b.find('276');
  assert.equal(b.el('point-forward').disabled, false);
  assert.equal(b.el('point-forward').textContent, 'Show next +16');
  assert.match(b.el('route-status').textContent, /unresolved within limits.*known terms outside window/);
  await b.find('121');
  assert.equal(b.el('point-expand').disabled, false);
  await b.el('point-expand').click();
  assert.ok(b.el('graph-nodes').children.length <= 80);
  assert.ok(b.node(243));
  assert.match(b.el('input-status').textContent, /Complete predecessor set/);
  await b.find('1000003');
  assert.equal(b.node(1000003).classList.contains('prime'), true);
  await b.el('reset-graph').click();
  assert.equal(b.el('graph-nodes').children.length, 42);
  assert.match(b.el('input-status').textContent, /1–1,000/);
});

async function download(b) {
  await b.el('download').click();
  return JSON.parse(await b.blobs.get(b.downloads.at(-1).href).text());
}

test('cached hidden predecessors are revealable without losing the full data or claiming absence', async () => {
  const b = browser({large: true});
  await b.find(12);
  assert.equal(b.node(121), undefined);
  assert.match(b.el('point-incoming').textContent, /None in this window.*1 known outside/);
  assert.equal(b.el('point-expand').disabled, false);
  assert.equal(b.el('point-predecessors').textContent, '1 total: 121');
  await b.el('point-expand').click();
  assert.ok(b.node(121));
  assert.match(b.el('input-status').textContent, /Added 0 predecessor arrows.*revealed 1 incoming/);
  const grown = await download(b);
  assert.equal(grown.nodes.length, 1665);
  assert.equal(grown.edges.length, 1653);
  await b.el('undo').click();
  assert.equal(b.node(121), undefined);
  const undone = await download(b);
  assert.deepEqual(undone.nodes, grown.nodes);
  assert.deepEqual(undone.edges, grown.edges);
  assert.equal(b.el('point-expand').disabled, false);
});

test('Show next rolls a long orbit forward without computing or marking hidden terms unresolved', async () => {
  const b = browser({large: true});
  await b.find(276);
  const initial = await download(b);
  assert.equal(b.el('point-forward').textContent, 'Show next +16');
  assert.ok(b.el('graph-nodes').children.some(n => n.children.some(c => c.classList.contains('node-more'))));
  const seen = new Set(initial.window.visible);
  let clicks = 0;
  while (b.el('point-forward').textContent === 'Show next +16' && clicks < 10) {
    const before = new Set(b.el('graph-nodes').children.map(n => n.dataset.node));
    await b.el('point-forward').click(); clicks++;
    const ids = b.el('graph-nodes').children.map(n => n.dataset.node);
    assert.ok(ids.length <= 80);
    assert.ok(ids.includes('276'));
    assert.ok(ids.filter(id => !before.has(id)).length <= 16);
    ids.forEach(id => seen.add(id));
    assert.match(b.el('input-status').textContent, /known forward terms/);
  }
  assert.ok(clicks > 0 && clicks < 10);
  assert.equal(b.el('point-forward').textContent, 'Extend forward +64');
  const after = await download(b);
  assert.deepEqual(after.nodes, initial.nodes);
  assert.deepEqual(after.edges, initial.edges);
  for (const id of initial.selection.path) assert.ok(seen.has(id));
  await b.el('undo').click();
  assert.equal(b.el('point-forward').textContent, 'Show next +16');
});

test('an orbit longer than the window can still extend at its visible computation frontier', async () => {
  const b = browser({large: true});
  await b.find(660);
  for (let i = 0; i < 10 && b.el('point-forward').textContent === 'Show next +16'; i++) await b.el('point-forward').click();
  assert.equal(b.el('point-forward').textContent, 'Extend forward +64');
  await b.el('point-forward').click();
  const computed = await download(b);
  assert.ok(computed.selection.path.length > 80);
  assert.equal(computed.selection.status, 'unresolved');
  for (let i = 0; i < 10 && b.el('point-forward').textContent === 'Show next +16'; i++) await b.el('point-forward').click();
  assert.ok(b.node(computed.selection.path.at(-1)));
  assert.equal(b.el('graph-nodes').children.length, 80);
  assert.equal(b.el('point-forward').textContent, 'Extend forward +64');
  assert.equal(b.el('point-forward').disabled, false);
  assert.match(b.el('route-status').textContent, /known terms outside window/);
  assert.deepEqual((await download(b)).nodes, computed.nodes, 'revealing batches does no extra arithmetic');
});

test('keyboard expansion restores focus when the window redraws the chosen node', async () => {
  const b = browser({large: true});
  await b.find(276);
  const cut = b.el('graph-nodes').children.find(n => n.children.some(c => c.classList.contains('node-more')));
  const id = cut.dataset.node;
  cut.fire('keydown', {key: 'Enter'});
  assert.equal(b.node(id).focused, true);
  assert.equal(b.node(id).getAttribute('aria-pressed'), 'true');
  assert.ok(b.el('graph-nodes').children.length <= 80);
});

test('all loaded seeds remain searchable with bounded render size and no dangling arrows', async () => {
  const b = browser({large: true});
  for (const id of [52, 88, 95, 220, 276, 496, 552, 750, 1000]) {
    await b.find(id);
    assert.ok(b.node(id));
    assert.ok(b.el('graph-nodes').children.length <= 80);
    const data = await download(b), table = new Map(data.nodes.map(n => [n.id, n]));
    for (const edge of b.el('graph-edges').children) {
      assert.ok(b.node(edge.dataset.source));
      assert.ok(b.node(table.get(edge.dataset.source).next));
      assert.doesNotMatch(edge.getAttribute('d'), /NaN|Infinity|undefined/);
    }
    assert.equal(data.nodes.length, 1665);
    assert.equal(data.orbits.length, 1000);
  }
  assert.equal(b.el('graph-nodes').children.length, 80);
  await b.el('clear-trace').click();
  assert.equal(b.el('graph-nodes').children.length, 42);
  assert.equal((await download(b)).nodes.length, 1665);
});

test('window-only Undo never consumes a mathematical action; overview retains live additions', async () => {
  const b = browser({large: true});
  await b.find(1000003);
  const math = await download(b);
  assert.equal(math.nodes.length, 1666);
  await b.find(276);
  await b.el('undo').click();
  assert.deepEqual((await download(b)).nodes, math.nodes);
  assert.ok(b.node(1000003));
  await b.el('clear-trace').click();
  assert.equal(b.node(1000003), undefined);
  assert.deepEqual((await download(b)).nodes, math.nodes);
  await b.el('undo').click();
  assert.ok(b.node(1000003));
  await b.el('undo').click();
  const original = await download(b);
  assert.equal(original.nodes.length, 1665);
  assert.equal(original.window.visible.length, 42);
});

test('SVG UI renders a small window and hover previews exact info without factoring', () => {
  const b = browser();
  assert.equal(b.el('graph-nodes').children.length, 42);
  assert.equal(b.el('graph-edges').children.length, 41);
  assert.equal(b.el('point-details').hidden, true);
  assert.match(b.el('graph-summary').textContent, /42\/80.*2 proved/);
  b.find(52); b.tap(null); b.hover(52);
  assert.equal(b.el('point-details').hidden, false);
  assert.equal(b.el('point-details').dataset.pinned, 'false');
  assert.equal(b.el('point-value').textContent, '52');
  assert.match(b.el('point-predecessors').textContent, /None anywhere.*proved/);
  assert.match(b.el('point-factorization').innerHTML, /msup/);
  assert.equal(b.el('point-divisors').textContent, '1, 2, 4, 13, 26');
  assert.deepEqual(b.active().sort((a, c) => Number(a) - Number(c)), ['0', '1', '3', '4', '9', '15', '16', '26', '46', '52']);
  b.node(52).fire('pointerleave');
  assert.equal(b.el('point-details').hidden, true);
  assert.deepEqual(b.active(), []);
  assert.equal(b.timers.length, 0, 'no idle animation or computation timer');
});

test('one click/tap pins a forward trace; closing only the card leaves the path visible', () => {
  const b = browser(), initial = b.transform();
  b.find(52); b.tap(null); b.tap(52);
  assert.equal(b.el('point-details').dataset.pinned, 'true');
  assert.equal(b.node(52).getAttribute('aria-pressed'), 'true');
  assert.match(b.el('route-status').textContent, /52 → 46 → 26 → 16 → 15 → 9 → 4 → 3 → 1 → 0/);
  assert.equal(b.el('point-reverse').href, '/reverse/?n=52');
  b.el('point-close').click();
  assert.equal(b.el('point-details').hidden, true);
  assert.equal(b.active().length, 10);
  b.tap(52, {pointerType: 'touch'});
  assert.equal(b.el('point-details').hidden, false);
  b.hover(12);
  assert.equal(b.el('point-value').textContent, '52', 'pin persists over other nodes');
  b.el('clear-trace').click();
  assert.deepEqual(b.active(), []);
  assert.equal(b.el('point-details').hidden, true);
  assert.equal(b.transform(), initial);
});

test('cycles, infinite prime predecessors, and zero are presented distinctly', () => {
  const b = browser();
  b.find(95);
  assert.match(b.el('route-status').textContent, /95 → 25 → 6 → 6.*cycle repeats/);
  assert.equal(b.el('graph-edges').children.find(n => n.getAttribute('data-source') === '6').classList.contains('active'), true);
  b.tap(1);
  assert.equal(b.node(1).classList.contains('terminal'), true);
  assert.equal(b.node(1).classList.contains('composite'), false, '1 is neither prime nor composite');
  assert.match(b.el('point-predecessors').textContent, /All primes.*infinitely many/);
  b.tap(0);
  assert.equal(b.el('point-next').textContent, 'Undefined');
  assert.equal(b.el('point-divisors').textContent, 'Undefined');
  assert.equal(b.el('route-status').textContent, '0 · terminated');
  b.tap(2);
  assert.match(b.el('point-status').textContent, /Prime/);
  assert.match(b.el('point-predecessors').textContent, /None anywhere/);
});

test('keyboard focuses small/offscreen nodes, pins with Enter/Space, and clears with Escape', () => {
  const b = browser({width: 360, height: 500}), initial = b.transform();
  b.find(88); b.tap(null); b.node(88).fire('focus');
  assert.notEqual(b.transform(), initial);
  assert.equal(b.el('point-value').textContent, '88');
  assert.equal(b.node(88).fire('keydown', {key: 'Enter'}).prevented, true);
  assert.equal(b.el('point-details').dataset.pinned, 'true');
  assert.equal(b.el('point-close').fire('keydown', {key: 'Escape'}).prevented, true);
  assert.equal(b.el('point-details').hidden, true);
  b.node(12).fire('keydown', {key: ' '});
  assert.equal(b.el('point-value').textContent, '12');
  assert.equal(b.el('point-predecessors').textContent, '1 total: 121');
  b.node(12).fire('click', {detail: 0});
  assert.equal(b.el('point-details').hidden, true, 'AT synthetic click works without pointer events');
});

test('pan, pointer cancellation, and pinch do not accidentally select starting nodes', () => {
  const b = browser();
  b.find(52); b.tap(null); b.el('fit').click();
  const original = b.transform();
  b.pointer('pointerdown', 52, {clientX: 150, clientY: 150});
  b.node(52).fire('focus');
  assert.equal(b.transform(), original, 'pointer-driven focus must not recenter the camera');
  b.pointer('pointermove', 52, {clientX: 250, clientY: 230});
  b.pointer('pointerup', 52, {clientX: 250, clientY: 230});
  assert.equal(b.transform(), original, 'dragging a node must not pan the camera');
  const moved = b.node(52).getAttribute('transform');
  b.el('arrange').click();
  assert.notEqual(b.node(52).getAttribute('transform'), moved);
  assert.equal(b.el('point-details').hidden, true);
  b.pointer('pointerdown', null); b.pointer('pointermove', null, {clientX: 250, clientY: 250}); b.pointer('pointerup', null);
  assert.notEqual(b.transform(), original, 'empty-space drag pans');
  b.pointer('pointerdown', 12); b.pointer('pointercancel', 12);
  assert.deepEqual(b.active(), []);
  b.el('fit').click();
  assert.equal(b.transform(), original);
  b.pointer('pointerdown', null, {pointerId: 1, clientX: 100, clientY: 100, pointerType: 'touch'});
  b.pointer('pointerdown', null, {pointerId: 2, clientX: 200, clientY: 100, pointerType: 'touch'});
  b.pointer('pointermove', null, {pointerId: 2, clientX: 300, clientY: 100, pointerType: 'touch'});
  b.pointer('pointerup', null, {pointerId: 2, pointerType: 'touch'});
  b.pointer('pointerup', null, {pointerId: 1, pointerType: 'touch'});
  assert.notEqual(b.transform(), original);
  assert.equal(b.el('point-details').hidden, true);
});

test('zoom buttons/wheel/keys, Fit and resize keep the overlay horizontally bounded', () => {
  const b = browser(), original = b.transform();
  b.el('zoom-in').click(); assert.notEqual(b.transform(), original);
  b.el('fit').click(); assert.equal(b.transform(), original);
  assert.equal(b.el('graph').fire('wheel', {deltaY: -100}).prevented, true);
  assert.notEqual(b.transform(), original);
  b.press('0'); assert.equal(b.transform(), original);
  b.press('+'); assert.notEqual(b.transform(), original);
  b.find(52); b.resize(360, 500);
  assert.equal(b.el('graph-world').classList.contains('vertical'), false);
  assert.equal(b.node(52).lastElementChild.getAttribute('text-anchor'), 'start');
  assert.ok(Number(b.node(52).getAttribute('transform').match(/translate\(([-\d.]+)/)[1]) < Number(b.node(46).getAttribute('transform').match(/translate\(([-\d.]+)/)[1]));
  assert.equal(b.el('point-details').hidden, false);
  assert.ok(parseFloat(b.el('point-details').style.left) >= 8);
  assert.ok(parseFloat(b.el('point-details').style.left) + b.el('point-details').offsetWidth <= 352);
});

test('find and deep links are exact; invalid values cannot invent orbits', async () => {
  const b = browser({query: '?n=00052'});
  assert.equal(b.el('point-value').textContent, '52');
  assert.equal(b.el('find-node').value, '52');
  const previous = b.el('route-status').textContent;
  for (const value of ['-1', '2.5', '1e2', '9'.repeat(1001), '<script>']) {
    await b.find(value);
    assert.ok(b.el('input-status').textContent);
    assert.equal(b.el('route-status').textContent, previous);
  }
  b.find('259');
  assert.equal(b.el('input-status').textContent, '');
  assert.equal(b.el('point-value').textContent, '259');
  assert.match(b.el('point-starts').textContent, /outside the start set/);
});

test('download preserves every exact certificate and the chosen trace as decimal strings', async () => {
  const b = browser({query: '?n=52'});
  b.el('download').click();
  assert.equal(b.downloads[0].download, 'aliquot-orbit-graph.json');
  const exported = JSON.parse(await b.blobs.get(b.downloads[0].href).text());
  assert.equal(exported.schema, 'aliquot-orbit-session-v1');
  assert.equal(exported.nodes.length, 117);
  assert.equal(exported.edges.length, 116);
  assert.equal(exported.window.limits.maxNodes, 80);
  assert.ok(exported.window.visible.length < exported.nodes.length);
  assert.ok(exported.window.visible.includes('52'));
  assert.equal(exported.selection.start, '52');
  assert.deepEqual(exported.selection.path, ['52', '46', '26', '16', '15', '9', '4', '3', '1', '0']);
  for (const node of exported.nodes) {
    assert.equal(typeof node.id, 'string');
    if (node.next !== null) assert.equal(typeof node.next, 'string');
    assert.ok(node.predecessors.values === null || node.predecessors.values.every(n => typeof n === 'string'));
  }
  for (const callback of b.timers) callback();
  assert.equal(b.blobs.size, 0);
});

test('node actions add actual branches, distinguish partial search, and support undo/reset', async () => {
  const b = browser();
  b.tap(12);
  assert.equal(b.el('point-expand').disabled, false);
  await b.el('point-expand').click();
  assert.ok(b.node(121));
  assert.match(b.el('input-status').textContent, /1 predecessor arrow.*Complete predecessor set/);
  assert.equal(b.el('point-details').hidden, true);
  assert.ok(b.active().includes('121'));
  b.tap(121);
  assert.match(b.el('point-predecessors').textContent, /Not searched/);
  assert.equal(b.el('point-compute').hidden, false);
  await b.el('point-compute').click();
  assert.equal(b.el('point-divisors').textContent, '1, 11');
  await b.el('point-expand').click();
  assert.ok(b.node(243));
  assert.match(b.el('input-status').textContent, /Partial search through 10,000/);
  await b.el('undo').click();
  assert.equal(b.node(243), undefined);
  assert.ok(b.node(121));
  await b.el('reset-graph').click();
  assert.equal(b.node(121), undefined);
  assert.equal(b.el('graph-nodes').children.length, 42);
  assert.equal(b.el('undo').disabled, true);
});

test('Explore adds new starts and an amicable component with exact card details', async () => {
  const b = browser();
  await b.find('220');
  assert.ok(b.node(220) && b.node(284));
  assert.match(b.el('route-status').textContent, /220 → 284 → 220.*cycle/);
  assert.match(b.el('input-status').textContent, /2 nodes and 2 exact arrows/);
  assert.equal(b.el('point-forward').disabled, true);
  assert.match(b.el('point-predecessors').textContent, /Not searched/);
  await b.find('101');
  assert.equal(b.node(101).classList.contains('prime'), true);
  assert.match(b.el('route-status').textContent, /101 → 1 → 0/);
  b.find(52);
  assert.equal(b.el('point-expand').disabled, true);
  assert.match(b.el('point-expand').textContent, /proved/);
});

test('live selection and Stop cancel pending work without leaking stale graph changes', async () => {
  const b = browser();
  const pending = b.find('9'.repeat(70));
  assert.equal(b.el('stop-work').hidden, false);
  assert.equal(b.el('find-button').disabled, true);
  await b.el('stop-work').click();
  // The real adapter yields at its exact work checkpoints; drive the queued
  // callback after cancellation to ensure obsolete async work cannot commit.
  for (let i = 0; i < 12; i++) { b.timers.splice(0).forEach(f => f()); await Promise.resolve(); }
  await pending;
  assert.equal(b.el('graph-nodes').children.length, 42);
  assert.equal(b.el('find-button').disabled, false);
  assert.match(b.el('input-status').textContent, /discarded/);
  b.tap(12);
  b.el('source-bound').value = '0';
  // A completed certificate can still be reused, but an invalid explicit
  // resource bound must be rejected before changing the graph.
  await b.el('point-expand').click();
  assert.equal(b.node(121), undefined);
  assert.match(b.el('input-status').textContent, /Source bound/);
});
