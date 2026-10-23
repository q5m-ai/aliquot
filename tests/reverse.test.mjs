import test from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFileSync} from 'node:fs';

const root = new URL('../', import.meta.url);
const source = ['site/vendor/katex/katex.min.js', 'site/latex.js', 'site/math.js',
  'site/point-info.js', 'site/reverse-math.js', 'site/reverse.js']
  .map(name => readFileSync(new URL(name, root), 'utf8')).join('\n');
function browser({query = '', bound = '10000', mobile = false} = {}) {
  const elements = new Map(), events = {};
  const make = tag => ({tagName: tag, textContent: '', innerHTML: '', value: '', dataset: {}, style: {},
    attributes: {}, children: [], hidden: false, disabled: false,
    setAttribute(key, value) { this.attributes[key] = String(value); },
    append(...children) { this.children.push(...children); },
    replaceChildren(...children) { this.children = children; },
    focus() { this.focused = true; },
    scrollIntoView() { this.scrolled = true; },
    click() { this.clicked = true; this.onclick?.(); }, remove() { this.removed = true; },
  });
  const element = id => {
    if (!elements.has(id)) {
      const node = make('div');
      node.value = id === 'root-input' ? '16' : id === 'source-bound' ? bound : '';
      elements.set(id, node);
    }
    return elements.get(id);
  };
  const presets = [16, 6, 220, 1, 2].map(n => { const b = make('button'); b.dataset.root = String(n); return b; });
  const document = {getElementById: element, createElement: make, createElementNS: (_, tag) => make(tag),
    querySelectorAll: selector => selector === '[data-root]' ? presets : [], body: make('body'),
    addEventListener: (name, handler) => { events[name] = handler; }};
  const context = vm.createContext({document, window: {location: {search: query},
    matchMedia: () => ({matches: mobile})}, setTimeout, URLSearchParams, URL, Blob});
  vm.runInContext(source, context);
  const run = code => vm.runInContext(code, context);
  return {element, run, events, presets, document, ready: run('ready'),
    values: () => Array.from(run('candidates'), String),
    path: () => Array.from(run('path'), String),
    choose: n => run(`nodeButtons.find(b => b.dataset.key === 'candidate-${n}').onclick()`),
    async start(n) { element('root-input').value = String(n); await run('start()'); },
  };
}

test('default grid has exact alternative predecessors, not a spurious chain between them', async () => {
  const b = browser(); await b.ready;
  assert.deepEqual(b.values(), ['12', '26']);
  assert.deepEqual(b.path(), ['16']);
  assert.match(b.element('search-status').textContent, /2 found.*1 ≤ m ≤ 225.*Complete/);
  assert.equal(b.run('nodeButtons.length'), 3);
  assert.equal(b.element('reverse-lines').children.length, 2);
  assert.equal(b.element('point-next').textContent, '15');
  assert.equal(b.element('point-follow').disabled, true);
  b.choose(12);
  assert.equal(b.element('point-value').textContent, '12');
  assert.equal(b.element('point-next').textContent, '16');
  assert.equal(b.element('point-change').textContent, '+4');
  assert.equal(b.element('point-residue').textContent, '0 · 10₁₂');
  assert.match(b.element('point-role').textContent, /Verified edge: 12 → 16/);
  assert.deepEqual(b.path(), ['16'], 'inspection alone must not follow a branch');
  await b.element('point-compute').onclick();
  assert.equal(b.element('point-divisors').textContent, '1, 2, 3, 4, 6');
  assert.equal(b.element('point-divisor-summary').textContent, '5 divisors · sum 16');
  assert.match(b.element('point-factorization').innerHTML, /<msup>/);
  assert.equal(b.element('point-compute').hidden, true);
  assert.deepEqual(b.path(), ['16']);
});

test('following, undoing and branching preserve every forward edge and signed gain', async () => {
  const b = browser(); await b.ready;
  b.choose(12); await b.element('point-follow').onclick();
  assert.deepEqual(b.path(), ['16', '12']);
  assert.deepEqual(b.values(), ['121']);
  assert.equal(b.element('gain-value').textContent, '+4');
  b.choose(121); await b.element('point-follow').onclick();
  assert.deepEqual(b.path(), ['16', '12', '121']);
  assert.equal(b.element('gain-value').textContent, '-105');
  assert.equal(b.element('depth-value').textContent, '2');
  b.run("nodeButtons.find(b => b.dataset.key === 'path-1').onclick()");
  assert.equal(b.element('point-previous').textContent, '121');
  assert.equal(b.element('point-next').textContent, '16');
  await b.element('undo').onclick();
  assert.deepEqual(b.path(), ['16', '12']);
  b.run("nodeButtons.find(b => b.dataset.key === 'path-0').onclick()");
  await b.element('point-follow').onclick();
  assert.deepEqual(b.path(), ['16']);
  assert.equal(b.element('undo').disabled, true);
  b.choose(26); await b.element('point-follow').onclick();
  assert.deepEqual(b.path(), ['16', '26']);
  assert.equal(b.element('gain-value').textContent, '-10');
});

test('inclusive bounds distinguish partial absence from a complete result', async () => {
  const b = browser({bound: '10'}); await b.ready;
  assert.deepEqual(b.values(), []);
  assert.equal(b.element('search-status').dataset.complete, 'false');
  assert.match(b.element('search-status').textContent, /0 found.*≤ 10.*Partial/);
  for (const [bound, expected, complete] of [[25, ['12'], false], [26, ['12', '26'], false], [225, ['12', '26'], true]]) {
    b.element('source-bound').value = String(bound); await b.run('searchPredecessors()');
    assert.deepEqual(b.values(), expected);
    assert.equal(b.element('search-status').dataset.complete, String(complete));
  }
  await b.start(2);
  assert.deepEqual(b.values(), []);
  assert.equal(b.element('search-status').dataset.complete, 'true');
  assert.ok(b.element('reverse-nodes').children.some(node => node.textContent === 'No positive predecessors exist.'));
});

test('0 has exactly source 1; 1 has a paginated partial prime search and never source 0', async () => {
  const b = browser({query: '?n=0'}); await b.ready;
  assert.deepEqual(b.values(), ['1']);
  assert.equal(b.element('point-next').textContent, 'Undefined');
  assert.equal(b.element('point-divisors').textContent, 'Undefined');
  assert.equal(b.element('search-status').dataset.complete, 'true');
  b.choose(1); await b.element('point-follow').onclick();
  assert.equal(b.element('point-next').textContent, '0');
  assert.equal(b.element('point-divisors').textContent, 'None');
  assert.equal(b.values().length, 1229);
  assert.equal(b.run('nodeButtons.length'), 10, 'eight candidates plus two chosen nodes');
  assert.match(b.element('search-status').textContent, /Partial.*infinitely many primes/);
  const before = b.run('nodeButtons[0].dataset.key');
  b.element('page-next').onclick();
  assert.notEqual(b.run('nodeButtons[0].dataset.key'), before);
  assert.equal(b.element('page-info').textContent, '9–16 of 1,229');
  b.element('page-previous').onclick();
  assert.equal(b.run('nodeButtons[0].dataset.key'), before);
});

test('cycles are visible without blocking incoming branches or inventing growth', async () => {
  const b = browser({query: '?n=6'}); await b.ready;
  assert.deepEqual(b.values(), ['6', '25']);
  b.choose(6);
  assert.match(b.element('point-role').textContent, /closes a cycle, not unbounded growth/);
  assert.equal(b.element('point-status').textContent, 'Perfect');
  await b.element('point-follow').onclick();
  assert.match(b.element('cycle-status').textContent, /contains a cycle/);
  assert.equal(b.element('gain-value').textContent, '0');
  b.choose(25); await b.element('point-follow').onclick();
  assert.deepEqual(b.path(), ['6', '6', '25']);
  assert.equal(b.element('gain-value').textContent, '-19');
  await b.start(220); b.choose(284); await b.element('point-follow').onclick();
  b.choose(220); await b.element('point-follow').onclick();
  assert.deepEqual(b.path(), ['220', '284', '220']);
  assert.match(b.element('cycle-status').textContent, /cycle/);
});

test('long paths retain all exact terms while only the latest five nodes are drawn', async () => {
  const b = browser({query: '?n=6'}); await b.ready;
  for (let i = 0; i < 20; i++) { b.choose(6); await b.element('point-follow').onclick(); }
  assert.equal(b.path().length, 21);
  assert.equal(b.run("nodeButtons.filter(b => b.dataset.key.startsWith('path-')).length"), 5);
  assert.match(b.element('path-window').textContent, /latest 5 of 21/);
  const trace = JSON.parse(b.run('JSON.stringify(trace())'));
  assert.deepEqual(trace.backward_path, Array(21).fill('6'));
  assert.equal(trace.forward_gain, '0');
  assert.equal(typeof trace.frontier_search.source_bound, 'string');
  b.element('download').onclick();
  assert.equal(b.document.body.children.at(-1).download, 'aliquot-reverse-chain.json');
  assert.equal(b.document.body.children.at(-1).clicked, true);
});

test('manual exact verification adds only valid sources, even outside the scan', async () => {
  const b = browser({bound: '10'}); await b.ready;
  b.element('verify-input').value = '26'; await b.run('verifyPredecessor()');
  assert.deepEqual(b.values(), ['26']);
  assert.equal(b.element('point-value').textContent, '26');
  assert.equal(b.element('point-divisors').textContent, '1, 2, 13');
  assert.match(b.element('verify-status').textContent, /Verified: 26 → 16/);
  assert.equal(b.run('result.checked'), 10, 'manual checks must not expand exhaustive coverage');
  assert.equal(b.run('result.complete'), false);
  b.element('verify-input').value = '13'; await b.run('verifyPredecessor()');
  assert.match(b.element('verify-status').textContent, /Not a predecessor:.*= 1, not 16/);
  assert.deepEqual(b.values(), ['26']);
  await b.element('point-follow').onclick();
  assert.deepEqual(b.path(), ['16', '26']);
  assert.equal(b.run('extras.length'), 0, 'manual candidates belong only to their checked target');
});

test('manually verified hundreds-digit sources remain exact in the graph and downloaded trace', async () => {
  const source = 2n ** 2000n, target = source - 1n;
  const b = browser({query: `?n=${target}`, bound: '10'}); await b.ready;
  b.element('verify-input').value = String(source); await b.run('verifyPredecessor()');
  assert.deepEqual(b.values(), [String(source)]);
  assert.equal(b.element('point-next').textContent, target.toLocaleString('en-CA'));
  assert.equal(b.element('point-change').textContent, '-1');
  assert.match(b.element('point-divisor-summary').textContent, /2,000 divisors.*shown \(sample\)/);
  assert.ok(b.element('point-divisors').textContent.length <= 8000);
  await b.element('point-follow').onclick();
  const trace = JSON.parse(b.run('JSON.stringify(trace())'));
  assert.deepEqual(trace.backward_path, [String(target), String(source)]);
  assert.equal(trace.forward_gain, '-1');
  assert.equal(trace.frontier_search.complete, false);
});

test('invalid inputs, exact large targets, and presets do not silently coerce values', async () => {
  const b = browser(); await b.ready;
  for (const invalid of ['-1', '1e3', '2.5', 'abc', '1'.repeat(1001)]) {
    await b.start(invalid);
    assert.deepEqual(b.path(), ['16']);
    assert.ok(b.element('input-status').textContent.length);
  }
  for (const invalid of ['0', '-1', '2.5', '1000001', 'Infinity', '1e6']) {
    b.element('source-bound').value = invalid; await b.run('searchPredecessors()');
    assert.match(b.element('search-status').textContent, /Source bound/);
    assert.deepEqual(b.values(), ['12', '26']);
  }
  b.element('source-bound').value = '10000';
  for (const invalid of ['0', '-1', '1.5', '1'.repeat(1001)]) {
    b.element('verify-input').value = invalid; await b.run('verifyPredecessor()');
    assert.ok(b.element('verify-status').textContent.length);
    assert.deepEqual(b.values(), ['12', '26']);
  }
  const huge = 2n ** 2000n;
  await b.start(huge);
  assert.equal(b.element('point-value').textContent, huge.toLocaleString('en-CA'));
  assert.deepEqual(b.values(), []);
  assert.equal(b.run('result.complete'), false);
  await b.element('point-compute').onclick();
  assert.equal(b.element('point-next').textContent, (huge - 1n).toLocaleString('en-CA'));
  assert.match(b.element('point-divisor-summary').textContent, /shown \(sample\)/);
  assert.ok(b.element('point-divisors').textContent.length <= 8000);
  await b.presets.find(button => button.dataset.root === '220').onclick();
  assert.deepEqual(b.path(), ['220']);
  assert.equal(b.presets.find(button => button.dataset.root === '220').attributes['aria-pressed'], 'true');
  const invalidQuery = browser({query: '?n=-20'}); await invalidQuery.ready;
  assert.deepEqual(invalidQuery.path(), []);
  assert.match(invalidQuery.element('search-status').textContent, /No grid started/);
});

test('search cancellation and a new target cannot publish a partial or stale sieve', async () => {
  const b = browser(); await b.ready;
  b.element('source-bound').value = '1000000';
  const pending = b.run('searchPredecessors()');
  assert.notEqual(b.run('searchJob'), null);
  b.element('search-stop').onclick();
  await pending;
  assert.equal(b.run('table.bound'), 10000);
  assert.equal(b.run('result'), null);
  assert.match(b.element('search-status').textContent, /stopped.*No completed search result/);
  assert.equal(b.element('search-progress').hidden, true);
  assert.equal(b.element('search-stop').disabled, true);
  const stale = b.run('searchPredecessors()');
  b.element('source-bound').value = '100'; await b.start(2);
  await stale;
  assert.deepEqual(b.path(), ['2']);
  assert.deepEqual(b.values(), []);
  assert.equal(b.run('table.bound'), 10000);
  assert.equal(b.run('result.target'), 2n);
  assert.equal(b.element('search-status').dataset.complete, 'true');
});

test('manual budget exhaustion is unresolved, and cancelled verification never adds a source', async () => {
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
  const stale = b.run('verifyPredecessor()');
  await b.start(16); await stale;
  assert.deepEqual(b.path(), ['16']);
  assert.equal(b.element('verify-status').textContent, '');
  assert.equal(b.run('extras.length'), 0);
});

test('point inspection can be closed/cancelled and reports factorization failures honestly', async () => {
  const b = browser({query: '?n=999999999999989', mobile: true}); await b.ready;
  const pending = b.element('point-compute').onclick();
  b.element('point-close').onclick(); await pending;
  assert.equal(b.element('point-details').hidden, true);
  assert.equal(b.run('records.has("999999999999989")'), false);
  await b.start(999983);
  b.run('const originalSum = AliquotMath.sum; AliquotMath.sum = (n, options) => originalSum(n, {...options, maxWork: 10})');
  await b.element('point-compute').onclick();
  assert.match(b.element('point-issue').textContent, /unresolved.*work limit/);
  assert.equal(b.run('records.has("999983")'), false);
  b.run('AliquotMath.sum = originalSum');
  await b.start(16); b.choose(12);
  assert.equal(b.element('point-details').scrolled, true);
  let prevented = false;
  b.events.keydown({key: 'Escape', preventDefault() { prevented = true; }});
  assert.equal(prevented, true);
  assert.equal(b.element('point-details').hidden, true);
  assert.equal(b.run("nodeButtons.find(b => b.dataset.key === 'candidate-12').focused"), true);
});

test('sieve guardrails, theorem ceiling, exact upper cap, and complete-only cancellation', async () => {
  const b = browser({bound: '1'}); await b.ready;
  for (const expression of ['0', '-1', '1.5', '1000001', 'Infinity', 'NaN']) {
    await assert.rejects(b.run(`AliquotReverse.sieve(${expression})`), /Source bound/);
  }
  for (const expression of ['-1n', '2', 'NaN']) {
    assert.throws(() => b.run(`AliquotReverse.ceiling(${expression})`), /non-negative/);
  }
  assert.equal(b.run('AliquotReverse.ceiling(0n)'), 1n);
  assert.equal(b.run('AliquotReverse.ceiling(1n)'), null);
  assert.equal(b.run('AliquotReverse.ceiling(12n)'), 121n, 'prime-square predecessor attains the ceiling');
  await assert.rejects(b.run('AliquotReverse.sieve(1000000, {cancelled: () => true})'), /cancelled/);
  await assert.rejects(b.run('let stopped = false; AliquotReverse.sieve(1000000, {cancelled: () => stopped, yieldUI: async () => {stopped = true}})'), /cancelled/);
  // Retain an upper-cap table only after all divisor contributions have completed.
  const maximum = await b.run('AliquotReverse.sieve(1000000, {yieldUI: async () => {}})');
  assert.ok(maximum.sums.every(Number.isSafeInteger));
  assert.equal(maximum.sums[1000000], 1480437);
  assert.throws(() => b.run('AliquotReverse.predecessors(table, 16n, 2)'), /completed sieve/);
  assert.equal(b.run('AliquotReverse.predecessors(table, 9007199254740993n).values.length'), 0);
});
