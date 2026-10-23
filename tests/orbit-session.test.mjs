import test from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFileSync} from 'node:fs';
const source = ['math', 'reverse-math', 'orbit-data', 'orbit-graph', 'orbit-session']
  .map(name => readFileSync(new URL(`../site/${name}.js`, import.meta.url), 'utf8')).join('\n');
const plain = value => JSON.parse(JSON.stringify(value));
function session(options = {}) {
  const context = vm.createContext({setTimeout});
  vm.runInContext(source + `\nconst session = AliquotOrbitSession.create(AliquotOrbitData, ${JSON.stringify(options)});`, context);
  return {run: code => vm.runInContext(code, context), get s() { return vm.runInContext('session', context); }};
}

test('add cached predecessors recursively without confusing global and displayed leaves', async () => {
  const {s} = session();
  let result = await s.expand('12');
  assert.deepEqual(plain(result.added), ['121']);
  assert.equal(result.complete, true);
  assert.equal(s.model.nodes.get('121').next, '12');
  assert.equal(s.model.nodes.get('121').prime, false);
  assert.equal(s.model.nodes.get('12').leaf, false);
  assert.equal(s.model.nodes.get('121').predecessors.status, 'unsearched');
  assert.match(s.model.info('121').predecessors, /Not searched.*absence not established/);
  assert.equal(s.model.nodes.get('121').factors, null);
  result = await s.expand('121', {bound: 10000});
  assert.equal(result.complete, false);
  assert.equal(result.checked, '10000');
  assert.ok(result.added.includes('243'));
  const previousCount = s.model.nodes.size;
  result = await s.expand('121', {bound: 14400});
  assert.equal(result.complete, true);
  assert.equal(s.model.nodes.get('121').predecessors.ceiling, '14400');
  assert.equal(s.model.nodes.size, previousCount);
  assert.equal(s.model.nodes.get('121').untouchable, false);
  assert.ok(s.model.nodes.get('243').starts.includes('243'));
  result = await s.expand('52');
  assert.equal(result.complete, true);
  assert.equal(result.found, 0);
  assert.equal(s.model.nodes.get('52').untouchable, true);
});

test('live exact starting paths merge, preserve cycles, and never compute s(0)', async () => {
  const {s, run} = session();
  const result = await s.extend('220');
  assert.deepEqual(plain(result.added), ['220', '284']);
  assert.equal(result.computed, 2);
  assert.deepEqual(plain(s.model.trace('220')), {path: ['220', '284', '220'], cycle: ['220', '284'], status: 'cycle'});
  assert.deepEqual(plain(s.model.nodes.get('220').factors), [{prime: '2', exponent: 2}, {prime: '5', exponent: 1}, {prime: '11', exponent: 1}]);
  assert.equal(s.model.nodes.get('220').predecessors.status, 'unsearched');
  await s.extend('101');
  assert.deepEqual(plain(s.model.trace('101').path), ['101', '1', '0']);
  assert.equal(s.model.nodes.get('101').prime, true);
  assert.equal(s.model.nodes.get('1').incoming.filter(n => n === '101').length, 1);
  const count = s.data.edges.length;
  run('AliquotMath.sum = () => { throw new Error("must not factor a closed path or zero"); };');
  await s.extend('0'); await s.extend('101');
  assert.equal(s.data.edges.length, count);
  assert.equal(s.model.nodes.get('0').next, null);
});

test('prime fan expansion is batched; infinite, checked and drawn coverage stay distinct', async () => {
  const {s} = session();
  const result = await s.expand('1', {bound: 1000});
  assert.equal(result.found, 168);
  assert.equal(result.infinite, true);
  assert.equal(result.complete, false);
  assert.equal(result.revealed.length, 25);
  assert.equal(result.remaining, 118);
  assert.equal(s.model.nodes.size, 142);
  assert.match(s.model.info('1').proof, /168 primes enumerated through 1,000.*partial/);
  const second = await s.expand('1', {bound: 100});
  assert.equal(second.found, 168, 'a smaller requested bound never downgrades completed coverage');
  assert.equal(second.revealed.length, 25);
  assert.equal(second.remaining, 93);
  assert.equal(s.model.nodes.get('1').untouchable, false);
});

test('a complete inverse set need not be entirely drawn in one action', async () => {
  const {s} = session({batchSize: 1});
  await s.expand('12');
  const result = await s.expand('121', {bound: 14400});
  assert.equal(result.complete, true);
  assert.equal(result.found, 13);
  assert.equal(result.revealed.length, 1);
  assert.equal(result.remaining, 12);
  assert.equal(s.model.nodes.get('121').predecessors.values.length, 13);
});

test('graph cap retains all inverse matches while drawing only what fits', async () => {
  const {s} = session({maxNodes: 118});
  const result = await s.expand('1', {bound: 1000});
  assert.equal(s.model.nodes.size, 118);
  assert.equal(result.limited, true);
  assert.equal(result.revealed.length, 1);
  assert.equal(result.found, 168);
  assert.equal(s.model.nodes.get('1').predecessors.values.length, 168);
  const before = JSON.stringify(s.data);
  await assert.rejects(s.extend('220'), /Graph limit/);
  assert.equal(JSON.stringify(s.data), before);
});

test('step, digit and node limits retain verified prefixes and explicit unresolved frontiers', async () => {
  const tiny = session({maxSteps: 1});
  const first = await tiny.s.extend('220');
  assert.equal(first.status, 'unresolved');
  assert.equal(tiny.s.model.nodes.get('284').next, null);
  assert.match(tiny.s.model.nodes.get('284').unresolved, /1-step/);
  assert.equal(tiny.s.model.nodes.get('284').prime, null);
  const resumed = await tiny.s.extend('220');
  assert.equal(resumed.status, 'cycle');
  const capped = session({maxNodes: 118});
  const result = await capped.s.extend('220');
  assert.equal(result.status, 'unresolved');
  assert.equal(capped.s.model.nodes.get('220').next, null);
  assert.equal(capped.s.model.nodes.get('220').sum, '284');
  assert.match(result.reason, /118-node limit/);
  const digits = session({maxDigits: 3});
  const limit = await digits.s.extend('960');
  assert.equal(limit.status, 'unresolved');
  assert.equal(digits.s.model.nodes.get('960').sum, '2088');
  assert.equal(digits.s.model.nodes.get('960').next, null);
  assert.equal(digits.s.model.nodes.has('2088'), false);
  assert.match(limit.reason, /3-digit limit/);
});

test('factorization failures are unresolved, never guessed prime or termination', async () => {
  const {s} = session({maxWork: 1});
  const result = await s.extend('121');
  assert.equal(result.status, 'unresolved');
  assert.match(result.reason, /Factorization work limit/);
  assert.equal(s.model.nodes.get('121').next, null);
  assert.equal(s.model.nodes.get('121').prime, null);
  assert.equal(s.model.nodes.get('121').factors, null);
  assert.equal(s.data.complete_orbits, false);
});

test('optional divisor inspection computes only exact details, without drawing an edge', async () => {
  const {s} = session();
  await s.expand('12');
  const count = s.data.edges.length;
  await s.divisors('121');
  assert.deepEqual(plain(s.model.nodes.get('121').factors), [{prime: '11', exponent: 2}]);
  assert.equal(s.model.nodes.get('121').sum, '12');
  assert.equal(s.data.edges.length, count);
  await assert.rejects(s.divisors('0'), /positive displayed/);
});

test('Stop, reset and competing revisions discard entire unfinished transactions', async () => {
  const {s, run} = session();
  const before = JSON.stringify(s.data);
  let stop = true;
  await assert.rejects(s.extend('220', {cancelled: () => stop}), /cancelled/);
  assert.equal(JSON.stringify(s.data), before);
  stop = false;
  await assert.rejects(s.extend('220', {cancelled: () => stop, onProgress: () => { stop = true; }}), /cancelled/);
  assert.equal(JSON.stringify(s.data), before);
  run('let release; AliquotMath.sum = async () => { await new Promise(resolve => release = resolve); return 284n; };');
  const pending = s.extend('220');
  s.reset(); run('release()');
  await assert.rejects(pending, /cancelled/);
  assert.equal(JSON.stringify(s.data), before);
});

test('sieve cancellation never publishes a partial census', async () => {
  const {s} = session();
  let stop = false;
  const before = JSON.stringify(s.data);
  await assert.rejects(s.expand('1', {bound: 1000000, cancelled: () => stop,
    onProgress: () => { stop = true; }}), /cancelled/);
  assert.equal(JSON.stringify(s.data), before);
});

test('an in-progress sieve is cancellable and cannot replace the completed graph', async () => {
  const {s} = session();
  let stop = false;
  const before = JSON.stringify(s.data);
  const pending = s.expand('1', {bound: 1000000, cancelled: () => stop});
  setTimeout(() => { stop = true; }, 0);
  await assert.rejects(pending, /cancelled/);
  assert.equal(JSON.stringify(s.data), before);
  assert.equal(s.canUndo, false);
  await s.expand('12');
  assert.equal(s.model.nodes.get('121').next, '12');
});

test('undo/reset are bounded, reproduce initial state, and do not mutate the public dataset', async () => {
  const {s, run} = session();
  const initial = JSON.stringify(s.data), original = run('JSON.stringify(AliquotOrbitData)');
  await s.expand('12');
  assert.equal(s.canUndo, true);
  assert.equal(s.undo(), true);
  assert.equal(JSON.stringify(s.data), initial);
  assert.equal(s.canUndo, false);
  for (let n = 101; n < 113; n++) await s.extend(String(n));
  let undos = 0;
  while (s.undo()) undos++;
  assert.equal(undos, 10);
  s.reset();
  assert.equal(JSON.stringify(s.data), initial);
  assert.equal(run('JSON.stringify(AliquotOrbitData)'), original);
});

test('exact parsing and input limits reject malformed or unbounded requests', async () => {
  const {s} = session();
  assert.equal(s.parse('0009007199254740993'), '9007199254740993');
  for (const value of ['-1', '1.5', '1e3', 'x', '9'.repeat(1001)]) assert.throws(() => s.parse(value), /integer/);
  for (const bound of [0, 1000001, 1.5, NaN]) await assert.rejects(s.expand('1', {bound}), /Source bound/);
  await assert.rejects(s.expand('999'), /displayed node/);
  assert.throws(() => session({maxNodes: 116}), /Initial graph/);
  assert.throws(() => session({maxSteps: 65}), /Invalid/);
});
