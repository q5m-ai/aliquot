import test from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import { readFileSync } from 'node:fs';

const root = new URL('../', import.meta.url);
const source = readFileSync(new URL('site/math.js', root), 'utf8') + '\n' +
  readFileSync(new URL('site/explorer.js', root), 'utf8');
function browser() {
  const elements = new Map();
  const labels = [];
  const context2d = new Proxy({}, { get: (_, name) => (...args) => {
    for (const arg of args) if (typeof arg === 'number') assert.ok(Number.isFinite(arg), `non-finite canvas argument in ${String(name)}`);
    if (name === 'fillText') labels.push(args[0]);
  }, set: () => true });
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
  return { element, labels, run: code => vm.runInContext(code, context) };
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
  element('seed').value = '1'.repeat(1001); run('reset()');
  assert.match(element('note').textContent, /1,000-digit/);
  element('seed').value = '1000000000000001'; run('reset()');
  assert.equal(run('points[0].n'), 1000000000000001n);
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

test('steps cross the former ceiling and retain exact displayed integers', async () => {
  const { run, element } = browser();
  element('seed').value = '1000000000000000'; run('reset()');
  await run('advance()');
  assert.ok(run('points[1].n > 1000000000000000n'));
  assert.equal(element('value').textContent, run('fmt(points[1].n)'));
  run('playing=false; draw(performance.now())');
});

test('hundreds of digits plot finite coordinates in both scales', async () => {
  const { run, element, labels } = browser();
  element('seed').value = String(2n ** 2000n); run('reset()');
  await run('advance()');
  assert.equal(run('points[1].n'), 2n ** 2000n - 1n);
  run('playing=false; animation=null; draw(performance.now())');
  element('scale').value = 'linear'; run('draw(performance.now())');
  assert.ok(labels.some(label => /e\d+/.test(label)));
  assert.ok(labels.every(label => !/Infinity|NaN/.test(label)));
  element('scale').value = 'log'; run('draw(performance.now())');
});

test('budget failures and resource limits never advance or cache partial sums', async () => {
  const { run, element } = browser();
  await assert.rejects(run('AliquotMath.sum(999983n,{maxWork:10})'), /unresolved/);
  await assert.rejects(run('AliquotMath.sum(2n**100n,{maxWork:10})'), /unresolved/);
  await assert.rejects(run('AliquotMath.sum(0n)'), /positive/);
  element('seed').value = '999983'; run('reset()');
  run('const originalSum=AliquotMath.sum; AliquotMath.sum=(n,options)=>originalSum(n,{...options,maxWork:10})');
  await run('advance()');
  assert.equal(run('points.length'), 1);
  assert.equal(run('playing'), false);
  assert.equal(run('cache.has("999983")'), false);
  assert.match(element('note').textContent, /unresolved/);
  run('AliquotMath.sum=originalSum');
  // A successor can exceed the digit budget even when its source fits.
  element('seed').value = '1'+'0'.repeat(999); run('reset()');
  run('AliquotMath.sum=async()=>10n**1000n');
  await run('advance()');
  assert.equal(run('points.length'), 1);
  assert.match(element('note').textContent, /resource budget/);
});

test('repeated-factor work yields and can be cancelled', async () => {
  const { run } = browser();
  assert.equal(await run('AliquotMath.sum(2n**1000n,{yieldUI:async()=>{}})'), 2n ** 1000n - 1n);
  await assert.rejects(run('let cancelled=false; AliquotMath.sum(2n**1000n,{cancelled:()=>cancelled,yieldUI:async()=>{cancelled=true}})'), /cancelled/);
});

test('site has q5m research chrome, accessible controls, and matching icons', () => {
  const html = readFileSync(new URL('site/index.html', root), 'utf8');
  for (const marker of ['aliquot<span>.q5m.ai', 'https://www.q5m.ai', 'https://github.com/q5m-ai/aliquot', 'not a proof', 'aria-label="Main navigation"', 'role="status"']) assert.ok(html.includes(marker), marker);
  assert.equal(readFileSync(new URL('favicon.svg', root), 'utf8'), readFileSync(new URL('site/favicon.svg', root), 'utf8'));
});
