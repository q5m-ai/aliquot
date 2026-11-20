"""Bounded exact regressions for REPORT.md, not an orbit-resolution program.

Run from the repository root:
    python3 research/approaches/small-gain-feedback/verify.py

No dependencies beyond the standard library and the repository aliquot module.
All persisted orbit values and rational components are decimal strings.
"""

from fractions import Fraction
import json
from math import gcd, isqrt, lcm
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from aliquot import ComputationLimit, aliquot_sum  # noqa: E402

U_BOUND = 5_000
SOURCE_CAP = 1_000_000
MAX_WORK = 10_000
NAMED_TRACES = (
    (3580, 3980, 4420, 6164, 5260, 5828, 4924),
    (540, 1140, 2220),
    (220, 284, 220),
)


def pair_sum(n):
    """Independent proper-divisor sum, including s(1)=0, never s(0)."""
    if type(n) is not int or n < 1:
        raise ValueError("positive integer required")
    total = 0
    for d in range(1, isqrt(n) + 1):
        if n % d == 0:
            q = n // d
            if d < n:
                total += d
            if q != d and q < n:
                total += q
    return total


def divisor_sieve(bound):
    """Independent additive sieve; element zero is unused, not s(0)."""
    if type(bound) is not int or not 1 <= bound <= SOURCE_CAP:
        raise ValueError("sieve bound must be in 1..1000000")
    sums = [0] * (bound + 1)
    for d in range(1, bound // 2 + 1):
        for n in range(2 * d, bound + 1, d):
            sums[n] += d
    return sums


def cycle_weights(vertices, gains):
    """Exact finite-graph certificate; reject any expansive directed cycle.

    Returns positive integer w with gain[i,j]*w[j] <= w[i].
    Path enumeration is replaced by at most |vertices|-1 relaxation rounds.
    This checks supplied gains, not whether aliquot arithmetic supplies them.
    """
    vertices = tuple(vertices)
    if not vertices or len(set(vertices)) != len(vertices):
        raise ValueError("distinct nonempty vertices required")
    edges = {edge: Fraction(gain) for edge, gain in gains.items()}
    if any(i not in vertices or j not in vertices or gain <= 0
           for (i, j), gain in edges.items()):
        raise ValueError("positive gains on known vertices required")
    weights = dict.fromkeys(vertices, Fraction(1))
    for _ in range(len(vertices) - 1):
        updated = weights.copy()
        for (i, j), gain in edges.items():
            updated[i] = max(updated[i], gain * weights[j])
        weights = updated
    if any(gain * weights[j] > weights[i]
           for (i, j), gain in edges.items()):
        raise ValueError("expansive cycle: no nonincreasing weighted certificate")
    scale = lcm(*(w.denominator for w in weights.values()))
    return {i: int(w * scale) for i, w in weights.items()}


def rational(value):
    value = Fraction(value)
    return {"numerator": str(value.numerator), "denominator": str(value.denominator)}


def block_record(block):
    if block is None:
        return None
    n, m, t = block
    return {
        "values": [str(n), str(m), str(t)],
        "cofactors": [str(n // 20), str(m // 4), str(t // 20)],
        "gain": rational(Fraction(t, n)),
    }


def scan(*, u_bound=U_BOUND, source_cap=SOURCE_CAP, max_work=MAX_WORK):
    """At most two transitions for each coprime 20u, 1 <= u <= u_bound.

    First sources are <=100000. A second source above source_cap or an exact
    factorization budget failure is recorded as unresolved, never skipped
    silently or treated as divergence. Known successors are not iterated.
    """
    if type(u_bound) is not int or not 1 <= u_bound <= U_BOUND:
        raise ValueError("u_bound must be in 1..5000")
    if type(source_cap) is not int or not 20 * u_bound <= source_cap <= SOURCE_CAP:
        raise ValueError("source_cap must cover first sources and be <=1000000")
    if type(max_work) is not int or not 1 <= max_work <= MAX_WORK:
        raise ValueError("max_work must be in 1..10000")
    independent = divisor_sieve(source_cap)
    unresolved = []
    blocks = []
    certified = []
    attempted = completed = prime_growing = 0
    max_second_source = max_endpoint = 0
    for u in range(1, u_bound + 1):
        if gcd(u, 20) != 1:
            continue
        attempted += 1
        n = 20 * u
        try:
            m = aliquot_sum(n, max_work=max_work)
        except ComputationLimit:
            unresolved.append({"u": str(u), "stage": "first factorization"})
            continue
        if m != independent[n] or m != 22 * u + 42 * independent[u]:
            raise AssertionError(("first-step arithmetic mismatch", n, m))
        max_second_source = max(max_second_source, m)
        if m > source_cap:
            unresolved.append({"u": str(u), "stage": "second source cap", "known_successor": str(m)})
            continue
        try:
            t = aliquot_sum(m, max_work=max_work)
        except ComputationLimit:
            unresolved.append({"u": str(u), "stage": "second factorization", "known_successor": str(m)})
            continue
        if t != independent[m]:
            raise AssertionError(("second-step arithmetic mismatch", m, t))
        completed += 1
        max_endpoint = max(max_endpoint, t)
        if m % 4 or gcd(m // 4, 4) != 1 or t % 20 or gcd(t // 20, 20) != 1:
            continue
        v, w = m // 4, t // 20
        if t != 3 * v + 7 * independent[v]:
            raise AssertionError("unitary second-core identity failed")
        returned = (Fraction(33, 40) * u + Fraction(63, 40) * independent[u]
                    + Fraction(7, 20) * independent[v])
        if returned != w:
            raise AssertionError("composite return identity failed")
        block = (n, m, t)
        blocks.append(block)
        if t > n and independent[u] == 1:
            prime_growing += 1
        if 21 * independent[u] <= u and 21 * independent[v] <= v:
            if not t < n:
                raise AssertionError("leakage-threshold descent failed")
            certified.append(block)
    growing = [block for block in blocks if block[2] > block[0]]
    largest = max(blocks, key=lambda block: Fraction(block[2], block[0]), default=None)
    return {
        "u_inclusive_bound": u_bound,
        "first_source_inclusive_bound": 20 * u_bound,
        "second_source_inclusive_cap": source_cap,
        "factorization_work_per_call": max_work,
        "transitions_per_input_at_most": 2,
        "attempted_inputs": attempted,
        "completed_inputs": completed,
        "unresolved_count": len(unresolved),
        "unresolved": unresolved,
        "max_second_source": str(max_second_source),
        "max_endpoint": str(max_endpoint),
        "guarded_20_4_20_blocks": len(blocks),
        "growing_blocks": len(growing),
        "equal_endpoint_blocks": sum(t == n for n, _, t in blocks),
        "decreasing_blocks": sum(t < n for n, _, t in blocks),
        "growing_prime_input_blocks": prime_growing,
        "leakage_threshold_blocks": len(certified),
        "first_growing_block": block_record(growing[0] if growing else None),
        "largest_observed_gain_block": block_record(largest),
        "first_leakage_threshold_block": block_record(certified[0] if certified else None),
    }


def evidence():
    traces = []
    for trace in NAMED_TRACES:
        for source, expected in zip(trace, trace[1:]):
            if source > SOURCE_CAP:
                raise AssertionError("named source exceeds cap")
            actual = aliquot_sum(source, max_work=MAX_WORK)
            if actual != expected or pair_sum(source) != expected:
                raise AssertionError((source, actual, expected))
        traces.append([str(n) for n in trace])
    threshold_gains = {(20, 4): Fraction(6), (4, 20): Fraction(1, 6)}
    return {
        "purpose": "finite arithmetic regressions; no universal proof or orbit classification",
        "scan": scan(),
        "named_traces_checked_by_trial_factorization_and_divisor_pairs": traces,
        "named_transition_count": sum(len(trace) - 1 for trace in NAMED_TRACES),
        "bare_core_cycle_gain": rational(Fraction(33, 40)),
        "cofactor_leakage_threshold": rational(Fraction(1, 21)),
        "threshold_integer_weights": {str(k): str(v) for k, v in cycle_weights((20, 4), threshold_gains).items()},
        "base_prime_progression": {"residue": "179", "modulus": "3960100"},
    }


if __name__ == "__main__":
    print(json.dumps(evidence(), indent=2, sort_keys=True))
