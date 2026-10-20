import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

// A small, exhaustive one-step experiment, not a large-number sequence engine.
export const MAX_BOUND = 1_000_000;
export const DEFAULT_BOUND = 100_000;

function requireBound(bound) {
  if (!Number.isSafeInteger(bound) || bound < 1 || bound > MAX_BOUND) {
    throw new RangeError(`bound must be an integer in [1, ${MAX_BOUND}]`);
  }
}

export function factorize(n) {
  if (typeof n !== 'bigint' || n < 1n || n > BigInt(MAX_BOUND)) {
    throw new RangeError(`n must be a positive BigInt at most ${MAX_BOUND}`);
  }
  const factors = [];
  let remaining = n;
  for (let p = 2n; p * p <= remaining; p = p === 2n ? 3n : p + 2n) {
    let exponent = 0;
    while (remaining % p === 0n) {
      remaining /= p;
      exponent++;
    }
    if (exponent) factors.push({ prime: p, exponent });
  }
  // Trial division has proved any residual factor prime; no probable primes.
  if (remaining > 1n) factors.push({ prime: remaining, exponent: 1 });
  return factors;
}

export function aliquot(n) {
  const factors = factorize(n);
  let sigma = 1n;
  for (const { prime, exponent } of factors) {
    let power = 1n;
    let sum = 1n;
    for (let e = 0; e < exponent; e++) {
      power *= prime;
      sum += power;
    }
    sigma *= sum;
  }
  return { sum: sigma - n, factors };
}

export function analyzeSix(n) {
  const { sum, factors } = aliquot(n);
  if (n % 12n !== 6n) throw new RangeError('n must lie in C6: n ≡ 6 (mod 12)');
  const oddExponents = factors.filter(({ prime, exponent }) => prime !== 2n && exponent % 2 === 1);
  let prediction = 'retained';
  if (oddExponents.length === 0) {
    prediction = 'exitsToOdd';
  } else if (oddExponents.length === 1 &&
             oddExponents[0].prime % 4n === 1n &&
             oddExponents[0].exponent % 4 === 1) {
    prediction = 'exitsToMultipleOfFour';
  }
  return { sum, factors, prediction };
}

// Independent of factorization, multiplicativity, and the exit classification:
// add every proper divisor directly to its positive multiples.
export function divisorSieve(bound) {
  requireBound(bound);
  const sums = Array(bound + 1).fill(0n);
  sums[0] = null; // s(0) is not defined here.
  for (let d = 1; d <= Math.floor(bound / 2); d++) {
    const divisor = BigInt(d);
    for (let n = 2 * d; n <= bound; n += d) sums[n] += divisor;
  }
  return sums;
}

export function scanSix(bound = DEFAULT_BOUND) {
  requireBound(bound);
  const independentSums = divisorSieve(bound);
  const counts = { retained: 0, exitsToOdd: 0, exitsToMultipleOfFour: 0 };
  const firstExamples = {};
  let candidates = 0;
  for (let index = 6; index <= bound; index += 12) {
    const n = BigInt(index);
    const { sum, factors, prediction } = analyzeSix(n);
    const independent = independentSums[index];
    const observed = independent % 2n === 1n ? 'exitsToOdd' :
      independent % 4n === 0n ? 'exitsToMultipleOfFour' : 'retained';
    if (sum !== independent || prediction !== observed || independent % 3n !== 0n ||
        (n === 6n ? independent !== n : independent <= n)) {
      throw new Error(`Independent check failed at n=${n}`);
    }
    candidates++;
    counts[observed]++;
    if (!firstExamples[observed]) {
      firstExamples[observed] = {
        n: n.toString(),
        next: independent.toString(),
        factorization: factors.map(({ prime, exponent }) => ({ prime: prime.toString(), exponent })),
      };
    }
  }
  return {
    schema: 'aliquot-six-class-scan-v1',
    bound: bound.toString(),
    sourceClass: 'positive n ≡ 6 (mod 12)',
    scope: 'one step for every source in the class up to the inclusive bound',
    arithmetic: {
      primary: 'BigInt trial factorization and multiplicative divisor sum',
      independentCheck: 'BigInt additive proper-divisor sieve',
    },
    candidates,
    counts,
    checks: {
      divisorSumsMatched: true,
      exitClassificationMatched: true,
      successorsDivisibleByThree: true,
      strictGrowthAboveSix: true,
    },
    firstExamples,
    conclusion: 'Finite census only. No divergent orbit or proof/disproof of the conjecture is established.',
  };
}

export function parseBound(args) {
  if (args.length === 0) return DEFAULT_BOUND;
  if (args.length !== 2 || args[0] !== '--bound' || !/^[1-9]\d*$/.test(args[1])) {
    throw new Error(`Usage: node research/driver-six.mjs [--bound INTEGER] (1..${MAX_BOUND})`);
  }
  const bound = Number(args[1]);
  requireBound(bound);
  return bound;
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  try {
    console.log(JSON.stringify(scanSix(parseBound(process.argv.slice(2))), null, 2));
  } catch (error) {
    console.error(error.message);
    process.exitCode = 1;
  }
}
