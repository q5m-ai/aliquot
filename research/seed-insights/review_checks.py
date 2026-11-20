#!/usr/bin/env python3
"""Coordinator-authored finite audit, independent of the worker/aliquot code.

Exact divisor pairs check named edges (sources <= 300,000,000). An additive
sieve through 300,000 checks every internal rank edge with source <= 200,000.
This neither verifies universal proofs nor classifies the witnesses' futures.
Run from the repository root; output is deterministic JSON.
"""

import json
from math import gcd, isqrt

SOURCE_BOUND = 200_000
SIEVE_BOUND = 300_000
PAIR_SOURCE_CAP = 300_000_000

PATHS = (
    (1932, 3444, 5964, 10164, 19628),
    (206220, 455028),
    (294420, 649068),
    (4528020, 9962988),
    (7703220, 16948428),
    (31517220, 69339228),
    (145824420, 320815068),
    (275247820, 302772644),
    (3580, 3980, 4420, 6164, 5260, 5828, 4924),
    (9820, 10844, 8140),
    (840, 2040, 4440, 9240, 25320, 51000, 117480),
    (461640, 923640, 1927560),
    (606, 618, 630),
    (1212, 1644, 2220),
    (732, 1004),
    (592, 586),
    (1926, 2286, 2706),
    (220, 284, 220),
    (496, 496),
    (2, 1, 0),
)


def proper(n):
    if type(n) is not int or not 1 <= n <= PAIR_SOURCE_CAP:
        raise ValueError("positive source within the declared divisor-pair cap required")
    total = -n
    for d in range(1, isqrt(n) + 1):
        if n % d == 0:
            total += d
            if d * d != n:
                total += n // d
    return total


def valuation(n, p):
    if n < 1:
        raise ValueError("positive valuation input required")
    result = 0
    while n % p == 0:
        n //= p
        result += 1
    return result


def rank(n, representation):
    a, p = representation
    if a == 6:
        return 2, int(p % 3 == 2)
    if a == 12:
        return 1, valuation(p + 7, 3)
    return 0, n


def check():
    edges = set()
    for path in PATHS:
        for source, target in zip(path, path[1:]):
            assert proper(source) == target, (source, target)
            edges.add((source, target))

    # No factorization, production code, or worker helper is used in this audit.
    sums = [0] * (SIEVE_BOUND + 1)
    for d in range(1, SIEVE_BOUND // 2 + 1):
        for n in range(2 * d, SIEVE_BOUND + 1, d):
            sums[n] += d
    for n in range(1, 1001):
        assert sums[n] == proper(n)
    primes = [p for p in range(32, SIEVE_BOUND + 1) if sums[p] == 1]
    represented = {}
    for a in range(1, 18):
        for p in primes:
            n = a * p
            if n > SIEVE_BOUND:
                break
            if n <= 527:
                continue
            assert gcd(a, p) == 1
            assert n not in represented
            represented[n] = a, p

    sources = internal_edges = exits = 0
    phase_counts = {}
    for n, shape in represented.items():
        if n > SOURCE_BOUND:
            continue
        sources += 1
        m = sums[n]
        # For these cores the exact affine formula bounds m by 4n/3+28.
        assert m <= SIEVE_BOUND, "target outside declared sieve coverage"
        if m not in represented:
            exits += 1  # Exit from the rank domain, NOT an orbit classification.
            continue
        before, after = rank(n, shape), rank(m, represented[m])
        assert after < before, (n, m, before, after)
        internal_edges += 1
        key = f"{before[0]}->{after[0]}"
        phase_counts[key] = phase_counts.get(key, 0) + 1

    expected_core_sums = [0, 1, 1, 3, 1, 6, 1, 7, 4, 8, 1, 16, 1, 10, 9, 15, 1]
    assert sums[1:18] == expected_core_sums
    for a in range(1, 18):
        if a not in (6, 12):
            assert sums[a] < a
            assert a + sums[a] <= 31 * (a - sums[a])
    for a in (2, 4, 8, 10, 14, 16):
        for residue in (1, 2):
            assert (sums[a] * residue + a + sums[a]) % 3 != 0

    # The abundance collision preserves the three coordinates' 2/3 valuations.
    small = (2, 2 + proper(2), proper(2))
    large = (6050, 6050 + proper(6050), proper(6050))
    assert [x % 6 for x in small] == [x % 6 for x in large]
    for prime in (2, 3):
        assert [valuation(x, prime) for x in small] == [valuation(x, prime) for x in large]
    assert small[1] < 2 * small[0] and large[1] > 2 * large[0]
    assert 3 * (637 + proper(637)) - 637 == 1757
    assert gcd(637 * 1757, 120) == 1

    # All six actual 84-core examples replenish the stated valuation resource.
    for k, q in enumerate((491, 701, 10781, 18341, 75041, 347201), 1):
        assert proper(q) == 1
        u, v = 5 * q, 11 * q + 16
        assert gcd(u, 84) == gcd(v, 84) == 1
        assert valuation(u + 4, 3) == 0
        assert valuation(v + 4, 3) == k
        assert v % 5 == 2

    return {
        "scope": "coordinator finite arithmetic audit; not universal proof certification",
        "imports_worker_or_production_math": False,
        "bounds": {
            "rank_sources_inclusive": str(SOURCE_BOUND),
            "additive_sieve_inclusive": str(SIEVE_BOUND),
            "named_divisor_pair_source_cap": str(PAIR_SOURCE_CAP),
            "sieve_pair_cross_check_inclusive": "1000",
        },
        "distinct_named_edges": len(edges),
        "largest_named_source": str(max(source for source, _ in edges)),
        "rank_domain_sources": sources,
        "rank_internal_edges": internal_edges,
        "rank_domain_exits_not_orbit_verdicts": exits,
        "rank_phase_counts": dict(sorted(phase_counts.items())),
        "unresolved_arithmetic_checks": 0,
        "named_paths": [[str(n) for n in path] for path in PATHS],
    }


if __name__ == "__main__":
    print(json.dumps(check(), indent=2, sort_keys=True))
