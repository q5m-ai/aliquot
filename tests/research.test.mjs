import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import {
  MAX_BOUND, DEFAULT_BOUND, factorize, aliquot, analyzeSix, divisorSieve, scanSix, parseBound,
} from '../research/driver-six.mjs';

const root = new URL('../', import.meta.url);

test('research arithmetic agrees with direct divisor enumeration and reconstructs inputs', () => {
  for (let n = 1n; n <= 300n; n++) {
    let direct = 0n;
    for (let d = 1n; d < n; d++) if (n % d === 0n) direct += d;
    const { sum, factors } = aliquot(n);
    assert.equal(sum, direct, `s(${n})`);
    assert.equal(factors.reduce((product, { prime, exponent }) => product * prime ** BigInt(exponent), 1n), n);
    for (const { prime } of factors) {
      for (let d = 2n; d * d <= prime; d++) assert.notEqual(prime % d, 0n, `prime factor ${prime}`);
    }
  }
  assert.deepEqual(factorize(1n), []);
  assert.deepEqual(factorize(999983n), [{ prime: 999983n, exponent: 1 }]);
  assert.equal(aliquot(BigInt(MAX_BOUND)).sum, 1_480_437n);
});

test('independent additive sieve agrees with factorization for every n ≤ 10000', () => {
  const sums = divisorSieve(10_000);
  assert.equal(sums[0], null);
  for (let n = 1; n < sums.length; n++) assert.equal(aliquot(BigInt(n)).sum, sums[n], `s(${n})`);
});

test('exact C6 exit characterization includes the exponent-mod-4 condition', () => {
  for (const [n, prediction] of [
    [6n, 'retained'], [30n, 'retained'], [42n, 'retained'], [54n, 'retained'],
    [18n, 'exitsToOdd'], [450n, 'exitsToOdd'],
    [90n, 'exitsToMultipleOfFour'], [56250n, 'exitsToMultipleOfFour'],
    [2250n, 'retained'], // 2 * 3^2 * 5^3: odd exponent 3 is NOT an exit.
    [126n, 'retained'], // 2 * 3^2 * 7: prime 3 mod 4 is NOT an exit.
    [1170n, 'retained'], // 2 * 3^2 * 5 * 13: two odd exponents are NOT an exit.
  ]) {
    const result = analyzeSix(n);
    assert.equal(result.prediction, prediction, `classification of ${n}`);
    if (prediction === 'retained') assert.equal(result.sum % 12n, 6n);
    if (prediction === 'exitsToOdd') assert.equal(result.sum % 2n, 1n);
    if (prediction === 'exitsToMultipleOfFour') assert.equal(result.sum % 4n, 0n);
  }
});

test('leaving C6 need not immediately stop growth, and growth can end in termination', () => {
  const sequence = [30n, 42n, 54n, 66n, 78n, 90n, 144n, 259n, 45n, 33n, 15n, 9n, 4n, 3n, 1n, 0n];
  for (let i = 0; i + 1 < sequence.length; i++) assert.equal(aliquot(sequence[i]).sum, sequence[i + 1]);
  assert.equal(analyzeSix(90n).sum, 144n);
  assert.equal(aliquot(144n).sum, 259n);
  assert.equal(analyzeSix(438n).sum, 450n);
  assert.equal(analyzeSix(450n).sum, 759n);
});

test('fixed divisibility classes have the elementary escape witnesses in the notebook', () => {
  for (const d of [2n, 3n, 4n, 6n, 9n, 28n]) {
    const p = factorize(d)[0].prime;
    const witness = d ** (p * (p - 1n));
    assert.equal(witness % d, 0n);
    assert.equal(aliquot(witness).sum % p, 1n);
  }
});

test('scan boundaries are inclusive and empty scans are explicit', () => {
  assert.equal(scanSix(5).candidates, 0);
  assert.deepEqual(scanSix(5).firstExamples, {});
  assert.deepEqual(scanSix(6).counts, { retained: 1, exitsToOdd: 0, exitsToMultipleOfFour: 0 });
  assert.equal(scanSix(17).candidates, 1);
  assert.deepEqual(scanSix(18).counts, { retained: 1, exitsToOdd: 1, exitsToMultipleOfFour: 0 });
  assert.equal(scanSix(89).counts.exitsToMultipleOfFour, 0);
  assert.equal(scanSix(90).counts.exitsToMultipleOfFour, 1);
});

test('invalid and out-of-budget inputs are rejected rather than producing partial results', () => {
  for (const n of [0n, -1n, BigInt(MAX_BOUND) + 1n, 12, '12']) assert.throws(() => aliquot(n), RangeError);
  for (const n of [1n, 12n, 28n]) assert.throws(() => analyzeSix(n), RangeError);
  for (const bound of [0, -1, 1.5, NaN, Infinity, MAX_BOUND + 1, '100']) {
    assert.throws(() => scanSix(bound), RangeError);
    assert.throws(() => divisorSieve(bound), RangeError);
  }
  assert.equal(parseBound([]), DEFAULT_BOUND);
  assert.equal(parseBound(['--bound', '90']), 90);
  for (const args of [['--bound'], ['--other', '5'], ['--bound', '1e3'], ['--bound', '5.5'],
    ['--bound', '-5'], ['--bound', '0'], ['--bound', '1000001'], ['--bound', '9'.repeat(100)],
    ['--bound', '10', 'extra']]) assert.throws(() => parseBound(args));
});

test('committed finite census is reproduced exactly with both algorithms', () => {
  const expected = JSON.parse(readFileSync(new URL('research/results/driver-six-100000.json', root), 'utf8'));
  assert.deepEqual(scanSix(100_000), expected);
  assert.equal(expected.candidates, Object.values(expected.counts).reduce((a, b) => a + b, 0));
});

test('CLI emits JSON on success and fails without a partial report on invalid input', () => {
  const run = args => spawnSync(process.execPath, ['research/driver-six.mjs', ...args], { cwd: root, encoding: 'utf8' });
  const success = run(['--bound', '90']);
  assert.equal(success.status, 0, success.stderr);
  assert.deepEqual(JSON.parse(success.stdout), scanSix(90));
  const failure = run(['--bound', '0']);
  assert.equal(failure.status, 1);
  assert.equal(failure.stdout, '');
  assert.match(failure.stderr, /Usage|bound/);
});
