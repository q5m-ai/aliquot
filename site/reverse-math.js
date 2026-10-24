'use strict';
// Bounded, exhaustive inverse search. The Python tests independently verify it.
const AliquotReverse = (() => {
  const MAX_BOUND = 1000000;
  function checkTarget(n) {
    if (typeof n !== 'bigint' || n < 0n) throw new Error('Target must be a non-negative integer.');
  }
  function checkBound(bound) {
    if (!Number.isSafeInteger(bound) || bound < 1 || bound > MAX_BOUND) {
      throw new Error('Source bound must be an integer from 1 to 1,000,000.');
    }
  }
  function ceiling(n) {
    checkTarget(n);
    // s(m)=0 iff m=1; s(m)=1 iff m is prime (infinitely many sources).
    if (n === 0n) return 1n;
    if (n === 1n) return null;
    // For composite m, a proper divisor d >= sqrt(m) gives s(m) >= 1+d.
    // Hence s(m)=n>1 implies m <= (n-1)^2. Primes and 1 cannot map to n>1.
    return (n - 1n) ** 2n;
  }
  async function sieve(bound, {cancelled = () => false,
      yieldUI = () => new Promise(resolve => setTimeout(resolve, 0)), onProgress = () => {}} = {}) {
    checkBound(bound);
    if (cancelled()) throw new Error('cancelled');
    // All additions are exact integers: even the loose bound m(m-1)/2 is
    // < 5e11 here, far below 2^53. Float64 avoids 32-bit overflow assumptions.
    // Values are converted to BigInt for comparison/display/interchange.
    const sums = new Float64Array(bound + 1);
    let work = 0;
    for (let d = 1; d <= Math.floor(bound / 2); d++) {
      for (let m = 2 * d; m <= bound; m += d) {
        sums[m] += d;
        if (++work % 65536 === 0) {
          if (cancelled()) throw new Error('cancelled');
          onProgress(d, Math.floor(bound / 2));
          await yieldUI();
          if (cancelled()) throw new Error('cancelled');
        }
      }
    }
    if (cancelled()) throw new Error('cancelled');
    onProgress(Math.floor(bound / 2), Math.floor(bound / 2));
    return {bound, sums}; // Never publish a partial table.
  }
  function predecessors(table, target, bound = table.bound) {
    checkTarget(target);
    checkBound(bound);
    if (bound > table.bound) throw new Error('Source bound exceeds the completed sieve.');
    const maxSource = ceiling(target);
    const checked = maxSource !== null && maxSource < BigInt(bound) ? Number(maxSource) : bound;
    const values = [];
    // No sum in this table can exceed MAX_SAFE_INTEGER. Never round a large target.
    if (target <= BigInt(Number.MAX_SAFE_INTEGER)) {
      const exactTarget = Number(target);
      for (let m = 1; m <= checked; m++) {
        if (table.sums[m] === exactTarget) values.push(BigInt(m));
      }
    }
    return {target, bound, checked, ceiling: maxSource,
      complete: maxSource !== null && maxSource <= BigInt(bound), values};
  }
  return {MAX_BOUND, ceiling, sieve, predecessors};
})();
