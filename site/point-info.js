'use strict';
// Shared exact point-card presentation for the forward and reverse explorers.
const AliquotPointInfo = (() => {
  const fmt = n => n.toLocaleString('en-CA');
  function basic(n, next, previous) {
    if (n === 1n) next = 0n;
    const delta = previous === undefined ? null : n - previous;
    let status = 'Next term not computed';
    if (n === 0n) status = 'Terminated · s(0) is undefined';
    else if (n === 1n) status = 'Terminal · 1 → 0';
    else if (next !== undefined) status = next === n ? 'Perfect' : next > n ? 'Abundant' : 'Deficient';
    return {
      value: fmt(n),
      size: `${fmt(n.toString().length)} digit${n.toString().length === 1 ? '' : 's'} · ${n % 2n === 0n ? 'even' : 'odd'}`,
      residue: `${n % 12n} · ${n.toString(12).toUpperCase()}₁₂`,
      previous: previous === undefined ? '—' : fmt(previous),
      change: delta === null ? '—' : `${delta > 0n ? '+' : ''}${fmt(delta)}`,
      next: n === 0n ? 'Undefined' : next === undefined ? 'Not computed' : fmt(next),
      status,
    };
  }
  function divisors(n, factors) {
    if (n === 0n) return {factorization: 'Undefined', divisors: 'Undefined', 'divisor-summary': 'Undefined', canCompute: false};
    if (n === 1n) factors = [];
    if (!factors) return {factorization: 'Not computed', divisors: 'Not computed', 'divisor-summary': '—', canCompute: true};
    const info = AliquotMath.properDivisorsFromFactors(n, factors);
    const shown = [];
    let characters = 0;
    for (const d of info.values) {
      const text = fmt(d);
      if (characters + text.length + 2 > 8000) break;
      shown.push(text);
      characters += text.length + 2;
    }
    const truncated = BigInt(shown.length) < info.count;
    return {
      factorization: factors.length ? factors.map(({prime, exponent}) => fmt(prime) + (exponent > 1 ? `^${exponent}` : '')).join(' × ') : '—',
      factorizationTex: factors.length ? factors.map(({prime, exponent}) => prime.toString() + (exponent > 1 ? `^{${exponent}}` : '')).join(' \\times ') : null,
      divisors: shown.length ? shown.join(', ') : 'None',
      'divisor-summary': `${fmt(info.count)} divisor${info.count === 1n ? '' : 's'} · sum ${fmt(info.sum)}${truncated ? ` · ${shown.length} shown (sample)` : ''}`,
      canCompute: false,
    };
  }
  return {basic, divisors};
})();
