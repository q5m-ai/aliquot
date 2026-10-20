'use strict';
// Small dependency-free browser adapter. Python is the local research engine.
// BigInt values remain exact; Number is used ONLY for approximate chart coordinates.
const AliquotMath = (() => {
  const MAX_WORK = 2000000;
  const MAX_DIGITS = 1000; // UI/memory budget, not a mathematical value ceiling.
  async function sum(n, {maxWork = MAX_WORK, cancelled = () => false,
                         yieldUI = () => new Promise(resolve => setTimeout(resolve, 0))} = {}) {
    if (typeof n !== 'bigint' || n < 1n) throw new Error('s(n) requires a positive integer.');
    if (!Number.isSafeInteger(maxWork) || maxWork < 1) throw new Error('Invalid work budget.');
    let m = n, p = 2n, sigma = 1n, work = 0;
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
      let power = 1n, term = 1n;
      while (m % p === 0n) {
        await checkpoint();
        m /= p; power *= p; term += power;
      }
      sigma *= term;
      p = p === 2n ? 3n : p + 2n;
    }
    // Exhaustive trial division proves the residual prime. No probable primes.
    if (m > 1n) sigma *= m + 1n;
    return sigma - n;
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
  return {sum, MAX_WORK, MAX_DIGITS, coordinate, axisLabel};
})();
