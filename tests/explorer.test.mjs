import test from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import { readFileSync } from 'node:fs';

const root = new URL('../', import.meta.url);
const source = readFileSync(new URL('site/explorer.js', root), 'utf8');
function browser() {
  const elements = new Map();
  const context2d = new Proxy({}, { get: () => () => {}, set: () => true });
  const element = id => {
    if (!elements.has(id)) elements.set(id, {
      value: id === 'seed' ? '12' : id === 'scale' ? 'log' : '5',
      textContent: '', className: '', width: 0, height: 0,
      getContext: () => context2d,
      getBoundingClientRect: () => ({ width: 900, height: 400 }),
    });
    return elements.get(id);
  };
  const context = vm.createContext({
    document: { getElementById: element, querySelectorAll: () => [] },
    window: { devicePixelRatio: 1, addEventListener() {} },
    requestAnimationFrame() {}, performance, setTimeout,
  });
  vm.runInContext(source, context);
  return { element, run: code => vm.runInContext(code, context) };
}

test('exact proper-divisor sums, including visualization zero extension', async () => {
  const { run } = browser();
  for (const [n, sum] of [[0n, 0n], [1n, 0n], [2n, 1n], [12n, 16n], [28n, 28n], [220n, 284n], [284n, 220n], [12496n, 14288n], [999983n, 1n]]) {
    assert.equal(await run(`aliquot(${n}n, token)`), sum);
  }
});

test('220 detects its first cycle, never a repeated amber marker', async () => {
  const { run, element } = browser();
  element('seed').value = '220'; run('reset()');
  for (let i = 0; i < 4; i++) await run('animation = null; advance()');
  assert.equal(run('points.filter(p => p.mark).length'), 1);
  assert.equal(element('note').textContent, 'Cycle detected · period 2.');
});

test('zero, perfect numbers, input validation and step control', async () => {
  const { run, element } = browser();
  element('seed').value = '28'; run('reset()'); await run('advance()');
  assert.match(element('note').textContent, /Perfect number/);
  element('seed').value = '0'; run('reset()');
  assert.equal(run('points[0].mark'), true);
  for (const invalid of ['-1', '1.5', 'abc']) {
    element('seed').value = invalid; run('reset()');
    assert.equal(element('note').textContent, 'Enter a non-negative integer.');
  }
  element('seed').value = '1000000000000001'; run('reset()');
  assert.equal(element('note').textContent, 'Start at 10¹⁵ or below.');
  element('seed').value = '12'; run('reset()');
  element('step').onclick();
  await new Promise(resolve => setTimeout(resolve, 0));
  assert.equal(run('playing'), false);
  assert.equal(element('value').textContent, '16');
});

test('reset cancels stale work and drawing remains callable', async () => {
  const { run, element } = browser();
  const calculation = run('aliquot(999999999999989n, token)');
  element('seed').value = '12'; run('reset()');
  await assert.rejects(calculation, /cancelled/);
  run('draw(performance.now())');
});

test('site has q5m research chrome, accessible controls, and matching icons', () => {
  const html = readFileSync(new URL('site/index.html', root), 'utf8');
  for (const marker of ['aliquot<span>.q5m.ai', 'https://www.q5m.ai', 'https://github.com/q5m-ai/aliquot', 'not a proof', 'aria-label="Main navigation"', 'role="status"']) assert.ok(html.includes(marker), marker);
  assert.equal(readFileSync(new URL('favicon.svg', root), 'utf8'), readFileSync(new URL('site/favicon.svg', root), 'utf8'));
});
