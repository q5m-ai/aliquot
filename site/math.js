'use strict';
// Small dependency-free browser adapter. Python is the local research engine.
// BigInt values remain exact; Number is used ONLY for approximate chart coordinates.
const AliquotMath = (() => {
  const MAX_WORK = 2000000;
  const MAX_DIGITS = 1000; // UI/memory budget, not a mathematical value ceiling.
  async function sum(n, {maxWork = MAX_WORK, cancelled = () => false,
                         yieldUI = () => new Promise(resolve => setTimeout(resolve, 0)),
                         onFactors = () => {}} = {}) {
    if (typeof n !== 'bigint' || n < 1n) throw new Error('s(n) requires a positive integer.');
    if (!Number.isSafeInteger(maxWork) || maxWork < 1) throw new Error('Invalid work budget.');
    let m = n, p = 2n, sigma = 1n, work = 0;
    const factors = [];
    // Checkpoints count both trial candidates and repeated divisions.
    async function checkpoint() {
      if (cancelled()) throw new Error('cancelled');
      if (work >= maxWork) throw new Error('Factorization work limit reached; next term unresolved. No divergence conclusion.');
      work++;
      if (work % 800 === 0) {
        await yieldUI();
        if (cancelled()) throw new Error('cancelled');
      }
    }
    if (cancelled()) throw new Error('cancelled');
    while (p * p <= m) {
      await checkpoint();
      let power = 1n, term = 1n, exponent = 0;
      while (m % p === 0n) {
        await checkpoint();
        m /= p; power *= p; term += power; exponent++;
      }
      if (exponent) factors.push({prime:p, exponent});
      sigma *= term;
      p = p === 2n ? 3n : p + 2n;
    }
    // Exhaustive trial division proves the residual prime. No probable primes.
    if (m > 1n) { sigma *= m + 1n; factors.push({prime:m, exponent:1}); }
    if (cancelled()) throw new Error('cancelled');
    onFactors(factors); // Publish only a complete, proven factorization.
    return sigma - n;
  }
  // Input factors must be the complete prime factorization returned by sum().
  // Bound enumeration even when the exact divisor count is enormous. A truncated
  // list is a sample, not a promise of the smallest divisors.
  function properDivisorsFromFactors(n, factors, limit = 200) {
    if (typeof n !== 'bigint' || n < 1n) throw new Error('Divisors require a positive integer.');
    if (!Number.isSafeInteger(limit) || limit < 1 || limit > 200) throw new Error('Invalid divisor display limit.');
    let count = 1n, sigma = 1n, product = 1n, previous = 1n;
    for (const {prime, exponent} of factors) {
      if (typeof prime !== 'bigint' || prime <= previous || !Number.isSafeInteger(exponent) || exponent < 1) throw new Error('Invalid factorization.');
      product *= prime ** BigInt(exponent);
      if (product > n) throw new Error('Factorization does not reconstruct n.');
      previous = prime;
      count *= BigInt(exponent + 1);
      sigma *= (prime ** BigInt(exponent + 1) - 1n) / (prime - 1n);
    }
    if (product !== n) throw new Error('Factorization does not reconstruct n.');
    let values = [1n];
    for (const {prime, exponent} of factors) {
      if (values.length >= limit + 1) break;
      const base = values.slice();
      let power = 1n;
      for (let e = 1; e <= exponent && values.length < limit + 1; e++) {
        power *= prime;
        for (const d of base) {
          if (values.length >= limit + 1) break;
          values.push(d * power);
        }
      }
    }
    values = values.filter(d => d < n).sort((a,b) => a < b ? -1 : a > b ? 1 : 0).slice(0,limit);
    count--;
    return {count, sum:sigma-n, values, truncated:BigInt(values.length)<count};
  }
  function log10(n) {
    const digits = n.toString();
    const head = digits.slice(0, 15);
    return Math.log10(Number(head)) + digits.length - head.length;
  }
  function coordinate(n, scale, exponent = 0) {
    if (scale === 'log') return log10(n + 1n);
    const digits = n.toString(), head = digits.slice(0, 15);
    return Number(head) * 10 ** (digits.length - head.length - exponent);
  }
  function axisLabel(value, scale, exponent = 0) {
    if (scale === 'log') {
      if (value > 6) return `1e${value.toFixed(1)}`;
      return Math.round(10 ** value - 1).toLocaleString();
    }
    return exponent ? `${value.toPrecision(3)}e${exponent}` :
      value >= 10000 ? value.toExponential(1) : Math.round(value).toLocaleString();
  }
  return {sum, properDivisorsFromFactors, MAX_WORK, MAX_DIGITS, coordinate, axisLabel};
})();
