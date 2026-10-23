import test from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFileSync} from 'node:fs';

const root = new URL('../', import.meta.url);
const source = ['site/vendor/katex/katex.min.js', 'site/latex.js', 'site/math.js',
  'site/point-info.js', 'site/reverse-math.js', 'site/reverse.js']
  .map(name => readFileSync(new URL(name, root), 'utf8')).join('\n');
function browser({query = '', bound = '10000', dpr = 1, chartWidth = 1400, chartHeight = 500, cardHeight = 300} = {}) {
  const elements = new Map(), events = {}, frames = [], commands = [];
  const size = {width: chartWidth, height: chartHeight};
  const ctx = new Proxy({}, {get: (_, name) => (...args) => {
    for (const arg of args) if (typeof arg === 'number') assert.ok(Number.isFinite(arg), `non-finite canvas argument in ${String(name)}`);
    commands.push([name, ...args]);
  }, set: (_, name, value) => { commands.push([name, value]); return true; }});
  const make = tag => ({tagName: tag, textContent: '', innerHTML: '', value: '', dataset: {}, style: {},
    attributes: {}, children: [], hidden: false, disabled: false,
    setAttribute(key, value) { this.attributes[key] = String(value); },
    append(...children) { this.children.push(...children); },
    focus() { this.focused = true; },
    click() { this.clicked = true; this.onclick?.(); }, remove() { this.removed = true; },
  });
  const element = id => {
    if (!elements.has(id)) {
      const node = make('div');
      node.value = id === 'root-input' ? '16' : id === 'source-bound' ? bound : id === 'scale' ? 'linear' : '';
      node.getContext = () => ctx;
      node.getBoundingClientRect = () => ({left: 40, top: 60,
        width: id === 'point-details' ? Math.min(320, size.width - 16) : size.width,
        height: id === 'point-details' ? cardHeight : size.height});
      elements.set(id, node);
    }
    return elements.get(id);
  };
  const presets = [16, 6, 220, 1, 2].map(n => { const b = make('button'); b.dataset.root = String(n); return b; });
  const document = {getElementById: element, createElement: make,
    querySelectorAll: selector => selector === '[data-root]' ? presets : [], body: make('body')};
  const context = vm.createContext({document, window: {location: {search: query}, devicePixelRatio: dpr,
    addEventListener: (name, handler) => { events[name] = handler; }},
    requestAnimationFrame: callback => { frames.push(callback); }, setTimeout, URLSearchParams, URL, Blob});
  vm.runInContext(source, context);
  const run = code => vm.runInContext(code, context);
  const flush = () => {
    let count = 0;
    while (frames.length) { assert.ok(++count < 10, 'no idle redraw loop'); frames.shift()(); }
  };
  function point(key) {
    flush();
    const target = run(`screenPoints.find(t => t.point.key === ${JSON.stringify(key)})`);
    assert.ok(target, `rendered target ${key}`);
    return target;
  }
  const event = (key, options = {}) => {
    const p = point(key);
    return {clientX: p.x + 40, clientY: p.y + 60, pointerType: 'mouse', ...options};
  };
  return {element, run, events, presets, document, size, commands, flush, point, event,
    ready: Promise.resolve(run('ready')).then(flush), pendingFrames: () => frames.length,
    values: () => Array.from(run('candidates'), String), path: () => Array.from(run('path'), String),
    hover: key => element('graph').onpointermove(event(key)),
    pin: key => element('graph').onclick(event(key, {shiftKey: true})),
    async choose(n, options = {}) { await element('graph').onclick(event(`candidate-${n}`, options)); flush(); },
    async press(key) {
      let prevented = false;
      await element('graph').onkeydown({key, preventDefault() { prevented = true; }});
      assert.equal(prevented, true); flush();
    },
    async start(n) { element('root-input').value = String(n); await run('start()'); flush(); },
  };
}

test('numeric x/y plot, hidden-until-hover card, and no factoring on hover', async () => {
  const b = browser(); await b.ready;
  assert.deepEqual(b.values(), ['12', '26']);
  assert.deepEqual(b.path(), ['16']);
  assert.equal(b.element('point-details').hidden, true);
  assert.match(b.element('search-status').textContent, /2 predecessors of 16.*complete.*225/);
  const low = b.point('candidate-12'), high = b.point('candidate-26'), target = b.point('path-0');
  assert.equal(low.x, high.x);
  assert.ok(low.x < target.x);
  assert.ok(high.y < target.y && target.y < low.y, 'vertical position must encode the numeric value');
  assert.equal(low.point.k, -1);
  assert.equal(target.point.k, -0);
  b.run('AliquotMath.sum = () => {throw new Error("hover must not factor")};');
  b.hover('candidate-12');
  assert.equal(b.element('point-details').hidden, false);
  assert.equal(b.element('point-details').dataset.pinned, 'false');
  assert.equal(b.element('point-value').textContent, '12');
  assert.equal(b.element('point-next').textContent, '16');
  assert.equal(b.element('point-change').textContent, '+4');
  assert.equal(b.element('point-residue').textContent, '0 · 10₁₂');
  assert.equal(b.element('point-compute').disabled, true);
  assert.match(b.element('point-mode').textContent, /Click to step back/);
  assert.deepEqual(b.path(), ['16']);
  b.element('graph').onpointerleave();
  assert.equal(b.element('point-details').hidden, true);
  b.hover('path-0');
  assert.equal(b.element('point-next').textContent, '15');
  assert.equal(b.element('point-mode').textContent, 'Click to pin');
});

test('one click follows a predecessor, refits both axes, and never waits for a Follow button', async () => {
  const b = browser(); await b.ready;
  const initialHi = b.run('view.hi');
  await b.choose(12);
  assert.deepEqual(b.path(), ['16', '12']);
  assert.deepEqual(b.values(), ['121']);
  assert.equal(b.element('point-details').hidden, true);
  assert.equal(b.element('gain-value').textContent, '+4');
  assert.equal(b.element('frontier-value').textContent, '12');
  assert.ok(b.run('view.hi') > initialHi);
  assert.equal(b.point('candidate-121').point.k, -2);
  assert.equal(b.point('path-1').point.k, -1);
  const previousXlo = b.run('view.xlo');
  await b.choose(121);
  assert.deepEqual(b.path(), ['16', '12', '121']);
  assert.equal(b.element('gain-value').textContent, '-105');
  assert.ok(b.run('view.xlo') < previousXlo);
  await b.element('undo').onclick(); b.flush();
  assert.deepEqual(b.path(), ['16', '12']);
  b.pin('path-0'); await b.element('point-branch').onclick(); b.flush();
  assert.deepEqual(b.path(), ['16']);
  assert.equal(b.run('view.hi'), initialHi, 'refitting must also shrink, not retain a historical peak');
  assert.equal(b.element('undo').disabled, true);
});

test('chosen points pin the familiar card; divisor computation and branching remain explicit', async () => {
  const b = browser(); await b.ready;
  await b.choose(12); await b.choose(121);
  b.pin('path-1');
  assert.equal(b.element('point-details').dataset.pinned, 'true');
  assert.equal(b.element('point-previous').textContent, '121');
  assert.equal(b.element('point-next').textContent, '16');
  assert.equal(b.element('point-change').textContent, '+4');
  b.element('graph').onpointerleave();
  assert.equal(b.element('point-details').hidden, false);
  await b.element('point-compute').onclick();
  assert.equal(b.element('point-divisors').textContent, '1, 2, 3, 4, 6');
  assert.equal(b.element('point-divisor-summary').textContent, '5 divisors · sum 16');
  assert.match(b.element('point-factorization').innerHTML, /<msup>/);
  assert.deepEqual(b.path(), ['16', '12', '121']);
  assert.equal(b.element('point-compute').hidden, true);
  await b.element('point-branch').onclick(); b.flush();
  assert.deepEqual(b.path(), ['16', '12']);
  b.pin('path-1'); assert.equal(b.element('point-branch').hidden, true, 'already the frontier');
  b.element('point-close').onclick();
  assert.equal(b.element('point-details').hidden, true);
  assert.equal(b.element('graph').focused, true);
});

test('Shift-click and Space pin candidate details without advancing; an ordinary click still follows', async () => {
  const b = browser(); await b.ready;
  b.pin('candidate-26');
  assert.deepEqual(b.path(), ['16']);
  await b.element('point-compute').onclick();
  assert.equal(b.element('point-divisors').textContent, '1, 2, 13');
  assert.equal(b.element('point-next').textContent, '16');
  assert.equal(b.element('point-branch').hidden, true);
  await b.choose(26);
  assert.deepEqual(b.path(), ['16', '26']);
  assert.equal(b.element('gain-value').textContent, '-10');
  b.hover('path-1');
  assert.equal(b.element('point-divisors').textContent, '1, 2, 13', 'reuse proven factors on hover');
});

test('inclusive search coverage and empty results remain honest after hiding advanced controls', async () => {
  const b = browser({bound: '10'}); await b.ready;
  assert.deepEqual(b.values(), []);
  assert.equal(b.element('search-status').dataset.complete, 'false');
  assert.match(b.element('search-status').textContent, /0 predecessors.*= 10.*partial.*unsearched/);
  assert.equal(b.run('screenPoints.length'), 1);
  for (const [bound, expected, complete] of [[25, ['12'], false], [26, ['12', '26'], false], [225, ['12', '26'], true]]) {
    b.element('source-bound').value = String(bound); await b.run('searchPredecessors()'); b.flush();
    assert.deepEqual(b.values(), expected);
    assert.equal(b.element('search-status').dataset.complete, String(complete));
  }
  await b.start(2);
  assert.deepEqual(b.values(), []);
  assert.match(b.element('search-status').textContent, /No positive predecessors of 2.*complete/);
});

test('all prime predecessors are plotted without pagination; zero is never a source', async () => {
  const b = browser({query: '?n=0'}); await b.ready;
  assert.deepEqual(b.values(), ['1']);
  b.hover('path-0');
  assert.equal(b.element('point-next').textContent, 'Undefined');
  assert.equal(b.element('point-divisors').textContent, 'Undefined');
  await b.choose(1);
  assert.equal(b.values().length, 1229);
  assert.equal(b.run('candidatePoints.length'), 1229);
  assert.equal(b.run('screenPoints.length'), 1231);
  assert.equal(b.element('search-status').dataset.complete, 'false');
  b.hover('path-1');
  assert.equal(b.element('point-next').textContent, '0');
  assert.equal(b.element('point-divisors').textContent, 'None');
  assert.equal(b.values().includes('0'), false);
});

test('upper-cap prime cloud retains every selectable point while coalescing identical pixels', async () => {
  const b = browser({query: '?n=1', bound: '1000000', chartWidth: 360, chartHeight: 350}); await b.ready;
  assert.equal(b.run('candidatePoints.length'), 78498);
  assert.equal(b.run('screenPoints.length'), 78499);
  assert.ok(b.run('drawnCandidateCount') < 1000);
  assert.equal(b.values().at(-1), '999983');
  await b.press('Home');
  assert.equal(b.element('point-value').textContent, '2');
  await b.press('ArrowUp');
  assert.equal(b.element('point-value').textContent, '3', 'overlapping points remain separately keyboard-inspectable');
  await b.press(' ');
  assert.equal(b.element('point-details').dataset.pinned, 'true');
  assert.deepEqual(b.path(), ['1']);
  await b.press('Enter');
  assert.deepEqual(b.path(), ['1', '3']);
  assert.deepEqual(b.values(), ['4']);
});

test('cycle markers do not block incoming branches or imply growth', async () => {
  const b = browser({query: '?n=6'}); await b.ready;
  assert.deepEqual(b.values(), ['6', '25']);
  b.hover('candidate-6');
  assert.match(b.element('point-status').textContent, /Perfect.*cycle link/);
  await b.choose(6);
  assert.match(b.element('cycle-status').textContent, /Cycle/);
  assert.equal(b.element('gain-value').textContent, '0');
  assert.equal(b.point('path-1').point.firstSeen, 0);
  await b.choose(25);
  assert.deepEqual(b.path(), ['6', '6', '25']);
  assert.equal(b.element('gain-value').textContent, '-19');
  await b.start(220); await b.choose(284); await b.choose(220);
  assert.deepEqual(b.path(), ['220', '284', '220']);
  assert.match(b.element('cycle-status').textContent, /Cycle/);
});

test('rolling 180-point window matches Explore but the exact full chain is retained', async () => {
  const b = browser({query: '?n=6'}); await b.ready;
  for (let i = 0; i < 190; i++) await b.choose(6);
  assert.equal(b.path().length, 191);
  assert.equal(b.run('pathPoints.length'), 180);
  assert.equal(b.run('pathPoints[0].index'), 11);
  assert.equal(b.run('screenPoints.length'), 182);
  assert.match(b.element('path-window').textContent, /Latest 180.*full chain is retained/);
  const trace = JSON.parse(b.run('JSON.stringify(trace())'));
  assert.deepEqual(trace.backward_path, Array(191).fill('6'));
  assert.equal(trace.forward_gain, '0');
  assert.equal(typeof trace.frontier_search.source_bound, 'string');
  b.element('download').onclick();
  assert.equal(b.document.body.children.at(-1).download, 'aliquot-reverse-chain.json');
  assert.equal(b.document.body.children.at(-1).clicked, true);
});

test('manual exact checks add only verified points without expanding exhaustive coverage', async () => {
  const b = browser({bound: '10'}); await b.ready;
  b.element('verify-input').value = '26'; await b.run('verifyPredecessor()'); b.flush();
  assert.deepEqual(b.values(), ['26']);
  assert.equal(b.element('point-value').textContent, '26');
  assert.equal(b.element('point-divisors').textContent, '1, 2, 13');
  assert.match(b.element('verify-status').textContent, /Verified: 26 → 16/);
  assert.equal(b.run('result.checked'), 10);
  assert.equal(b.run('result.complete'), false);
  assert.match(b.element('search-status').textContent, /\+1 individually verified/);
  b.element('verify-input').value = '13'; await b.run('verifyPredecessor()');
  assert.match(b.element('verify-status').textContent, /Not a predecessor:.*= 1, not 16/);
  assert.deepEqual(b.values(), ['26']);
  await b.choose(26);
  assert.deepEqual(b.path(), ['16', '26']);
  assert.equal(b.run('extras.length'), 0);
});

test('hundreds-digit values retain exact cards/export and finite linear/log plot coordinates', async () => {
  const source = 2n ** 2000n, target = source - 1n;
  const b = browser({query: `?n=${target}`, bound: '10'}); await b.ready;
  b.element('verify-input').value = String(source); await b.run('verifyPredecessor()'); b.flush();
  assert.deepEqual(b.values(), [String(source)]);
  assert.equal(b.element('point-next').textContent, target.toLocaleString('en-CA'));
  assert.equal(b.element('point-change').textContent, '-1');
  assert.match(b.element('point-divisor-summary').textContent, /2,000 divisors.*shown \(sample\)/);
  assert.ok(b.element('point-divisors').textContent.length <= 8000);
  assert.ok(b.commands.filter(c => c[0] === 'fillText').some(c => /e\d+/.test(c[1])));
  b.element('scale').value = 'log'; b.element('scale').onchange(); b.flush();
  assert.equal(b.run('view.mode'), 'log');
  await b.choose(source);
  const trace = JSON.parse(b.run('JSON.stringify(trace())'));
  assert.deepEqual(trace.backward_path, [String(target), String(source)]);
  assert.equal(trace.forward_gain, '-1');
  assert.equal(trace.frontier_search.complete, false);
  assert.ok(b.commands.filter(c => c[0] === 'fillText').every(c => !/Infinity|NaN/.test(c[1])));
});

test('target buttons, presets, and validation never coerce large integers or allow negative sources', async () => {
  const b = browser(); await b.ready;
  await b.element('root-increment').onclick(); b.flush(); assert.deepEqual(b.path(), ['17']);
  await b.element('root-decrement').onclick(); b.flush(); assert.deepEqual(b.path(), ['16']);
  for (const invalid of ['-1', '1e3', '2.5', 'abc', '1'.repeat(1001)]) {
    await b.start(invalid);
    assert.deepEqual(b.path(), ['16']); assert.ok(b.element('input-status').textContent.length);
    assert.equal(b.element('root-increment').disabled, true);
  }
  for (const invalid of ['0', '-1', '2.5', '1000001', 'Infinity', '1e6']) {
    b.element('source-bound').value = invalid; await b.run('searchPredecessors()');
    assert.match(b.element('search-status').textContent, /Source bound/);
    assert.deepEqual(b.values(), ['12', '26']);
  }
  b.element('source-bound').value = '10000';
  for (const invalid of ['0', '-1', '1.5', '1'.repeat(1001)]) {
    b.element('verify-input').value = invalid; await b.run('verifyPredecessor()');
    assert.ok(b.element('verify-status').textContent.length); assert.deepEqual(b.values(), ['12', '26']);
  }
  const huge = 2n ** 2000n;
  await b.start(huge); b.pin('path-0');
  assert.equal(b.element('point-value').textContent, huge.toLocaleString('en-CA'));
  await b.element('point-compute').onclick();
  assert.equal(b.element('point-next').textContent, (huge - 1n).toLocaleString('en-CA'));
  await b.presets.find(button => button.dataset.root === '220').onclick(); b.flush();
  assert.deepEqual(b.path(), ['220']);
  await b.start(0); assert.equal(b.element('root-decrement').disabled, true);
  await b.element('root-decrement').onclick(); assert.deepEqual(b.path(), ['0']);
  await b.start('9'.repeat(1000)); assert.equal(b.element('root-increment').disabled, true);
  const invalidQuery = browser({query: '?n=-20'}); await invalidQuery.ready;
  assert.deepEqual(invalidQuery.path(), []);
  assert.match(invalidQuery.element('search-status').textContent, /No graph started/);
});

test('cancelling or changing targets cannot publish incomplete searches or leave clickable stale coordinates', async () => {
  const b = browser(); await b.ready;
  const oldClick = b.event('candidate-12');
  b.element('source-bound').value = '1000000';
  const pending = b.run('searchPredecessors()');
  assert.notEqual(b.run('searchJob'), null);
  assert.equal(b.run('screenPoints.length'), 0);
  b.element('graph').onclick(oldClick);
  assert.deepEqual(b.path(), ['16']);
  b.element('search-stop').onclick(); await pending; b.flush();
  assert.equal(b.run('table.bound'), 10000);
  assert.equal(b.run('result'), null);
  assert.match(b.element('search-status').textContent, /stopped.*incomplete/);
  assert.equal(b.element('search-progress').hidden, true);
  const stale = b.run('searchPredecessors()');
  b.element('source-bound').value = '100'; await b.start(2); await stale; b.flush();
  assert.deepEqual(b.path(), ['2']); assert.deepEqual(b.values(), []);
  assert.equal(b.run('table.bound'), 10000);
  assert.equal(b.run('result.target'), 2n);
  assert.equal(b.element('search-status').dataset.complete, 'true');
});

test('manual failures and cancellation stay unresolved and cannot contaminate another frontier', async () => {
  const b = browser({query: '?n=1', bound: '10'}); await b.ready;
  b.run('const originalSum = AliquotMath.sum; AliquotMath.sum = (n, options) => originalSum(n, {...options, maxWork: 10})');
  b.element('verify-input').value = '999983'; await b.run('verifyPredecessor()');
  assert.match(b.element('verify-status').textContent, /Unresolved, not rejected/);
  assert.equal(b.run('records.has("999983")'), false);
  assert.equal(b.values().includes('999983'), false);
  b.run('AliquotMath.sum = originalSum');
  b.element('verify-input').value = '999999999999989';
  const pending = b.run('verifyPredecessor()');
  b.element('verify-stop').onclick(); await pending;
  assert.match(b.element('verify-status').textContent, /stopped.*unresolved/);
  assert.equal(b.run('records.has("999999999999989")'), false);
  const stale = b.run('verifyPredecessor()'); await b.start(16); await stale;
  assert.deepEqual(b.path(), ['16']);
  assert.equal(b.element('verify-status').textContent, '');
  assert.equal(b.run('extras.length'), 0);
});

test('closing, resetting or changing the pin cancels stale divisor work; failures remain explicit', async () => {
  const b = browser({query: '?n=999999999999989'}); await b.ready;
  b.pin('path-0');
  const pending = b.element('point-compute').onclick();
  b.element('point-close').onclick(); await pending;
  assert.equal(b.element('point-details').hidden, true);
  assert.equal(b.run('records.has("999999999999989")'), false);
  b.pin('path-0');
  const stale = b.element('point-compute').onclick(); await b.start(16); await stale;
  assert.equal(b.element('point-details').hidden, true);
  assert.equal(b.run('records.has("999999999999989")'), false);
  await b.start(999983); b.pin('path-0');
  b.run('const originalSum = AliquotMath.sum; AliquotMath.sum = (n, options) => originalSum(n, {...options, maxWork: 10})');
  await b.element('point-compute').onclick();
  assert.match(b.element('point-issue').textContent, /unresolved.*work limit/);
  assert.equal(b.run('records.has("999983")'), false);
  await b.press('Escape'); assert.equal(b.element('point-details').hidden, true);
});

test('hover overlays flip/clamp inside the full-width canvas and track resize/scale at high DPR', async () => {
  const b = browser({dpr: 2, chartWidth: 390, chartHeight: 350}); await b.ready;
  assert.equal(b.element('graph').width, 780);
  for (const key of ['candidate-12', 'candidate-26', 'path-0']) {
    b.hover(key); b.flush();
    const card = b.element('point-details');
    assert.ok(parseFloat(card.style.left) >= 8 && parseFloat(card.style.left) <= 62);
    assert.ok(parseFloat(card.style.top) >= 8 && parseFloat(card.style.top) <= 42);
  }
  b.pin('path-0'); b.flush();
  const oldLeft = b.element('point-details').style.left;
  b.size.width = 1700; b.size.height = 700; b.events.resize(); b.flush();
  assert.equal(b.element('graph').width, 3400);
  assert.notEqual(b.element('point-details').style.left, oldLeft);
  assert.equal(b.element('point-value').textContent, '16');
  b.element('scale').value = 'log'; b.element('scale').onchange(); b.flush();
  assert.equal(b.element('point-value').textContent, '16');
  assert.equal(b.element('point-details').dataset.pinned, 'true');
  const tall = browser({chartWidth: 360, chartHeight: 350, cardHeight: 900}); await tall.ready;
  tall.pin('path-0'); tall.flush();
  assert.equal(tall.element('point-details').style.top, '8px');
  assert.equal(tall.element('point-details').style.maxHeight, undefined, 'never clip tall pinned divisor cards');
});

test('touch click advances once, chosen points pin, and keyboard selection mirrors hover', async () => {
  const b = browser({chartWidth: 360, chartHeight: 350, dpr: 2}); await b.ready;
  await b.choose(26, {pointerType: 'touch'});
  assert.deepEqual(b.path(), ['16', '26']);
  b.element('graph').onclick(b.event('path-1', {pointerType: 'touch'}));
  assert.equal(b.element('point-details').dataset.pinned, 'true');
  assert.equal(b.element('point-value').textContent, '26');
  await b.press('Escape');
  await b.start(16); await b.press('Home');
  assert.equal(b.element('point-value').textContent, '12');
  await b.press('ArrowUp'); assert.equal(b.element('point-value').textContent, '26');
  await b.press('ArrowDown'); assert.equal(b.element('point-value').textContent, '12');
  await b.press(' '); assert.deepEqual(b.path(), ['16']);
  assert.equal(b.element('point-details').dataset.pinned, 'true');
  await b.press('Enter'); assert.deepEqual(b.path(), ['16', '12']);
  await b.press('End'); await b.press('Enter');
  assert.equal(b.element('point-value').textContent, '16');
  assert.equal(b.element('point-details').dataset.pinned, 'true');
  b.element('graph').onclick({clientX: 0, clientY: 0});
  assert.equal(b.element('point-details').hidden, true);
});

test('redrawing is demand-driven and hover does not recompute the plot layout', async () => {
  const b = browser(); await b.ready;
  assert.equal(b.pendingFrames(), 0);
  const before = b.run('screenPoints');
  b.hover('candidate-12'); assert.equal(b.pendingFrames(), 1);
  b.flush(); assert.equal(b.pendingFrames(), 0);
  assert.equal(b.run('screenPoints'), before);
  b.hover('candidate-12'); assert.equal(b.pendingFrames(), 0);
  b.element('scale').onchange(); assert.equal(b.pendingFrames(), 1);
  b.flush(); assert.equal(b.pendingFrames(), 0);
});

test('sieve guardrails, exact upper cap, and theorem ceiling are unchanged by plotting', async () => {
  const b = browser({bound: '1'}); await b.ready;
  for (const expression of ['0', '-1', '1.5', '1000001', 'Infinity', 'NaN']) {
    await assert.rejects(b.run(`AliquotReverse.sieve(${expression})`), /Source bound/);
  }
  for (const expression of ['-1n', '2', 'NaN']) assert.throws(() => b.run(`AliquotReverse.ceiling(${expression})`), /non-negative/);
  assert.equal(b.run('AliquotReverse.ceiling(0n)'), 1n);
  assert.equal(b.run('AliquotReverse.ceiling(1n)'), null);
  assert.equal(b.run('AliquotReverse.ceiling(12n)'), 121n);
  await assert.rejects(b.run('AliquotReverse.sieve(1000000, {cancelled: () => true})'), /cancelled/);
  await assert.rejects(b.run('let stopped = false; AliquotReverse.sieve(1000000, {cancelled: () => stopped, yieldUI: async () => {stopped = true}})'), /cancelled/);
  const maximum = await b.run('AliquotReverse.sieve(1000000, {yieldUI: async () => {}})');
  assert.ok(maximum.sums.every(Number.isSafeInteger));
  assert.equal(maximum.sums[1000000], 1480437);
  assert.throws(() => b.run('AliquotReverse.predecessors(table, 16n, 2)'), /completed sieve/);
  assert.equal(b.run('AliquotReverse.predecessors(table, 9007199254740993n).values.length'), 0);
});
