#!/usr/bin/env python3
"""Bounded exact examples for REPORT.md; no orbit-extension or primality heuristics.

Run from any directory. JSON mathematical integers are decimal strings. All
reported aliquot edges are independently checked by divisor-pair enumeration.
The arguments for arbitrary K and infinitely many primes are NOT software claims.
"""

from fractions import Fraction
import json
from math import gcd, isqrt
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from aliquot import ComputationLimit, aliquot_sum, factorize  # noqa: E402

MAX_WORK = 2_000_000
SOURCE_CAP = 10_000_000_000
MAX_CANDIDATES = 256
MAX_RECHARGE_K = 6
CORE = 84


def divisor_pair_sum(n):
    """Independent s(n), enumerating d=1..floor(sqrt(n)), inclusively."""
    if type(n) is not int or n < 1:
        raise ValueError("n must be a positive integer")
    total = 0
    for d in range(1, isqrt(n) + 1):
        if n % d == 0:
            total += d
            if d != n // d:
                total += n // d
    return total - n


def valuation(n, prime):
    """v_prime(n) for positive n; caller supplies a proven prime."""
    if type(n) is not int or n < 1 or type(prime) is not int or prime < 2:
        raise ValueError("positive n and prime >= 2 required")
    exponent = 0
    while n % prime == 0:
        n //= prime
        exponent += 1
    return exponent


def crt_pair(a, m, b, n):
    """Combine two congruences with positive, relatively prime moduli."""
    if m < 1 or n < 1 or gcd(m, n) != 1:
        raise ValueError("positive coprime moduli required")
    modulus = m * n
    residue = (a + m * ((b - a) * pow(m, -1, n) % n)) % modulus
    return residue, modulus


def recharge_progression(k):
    """q=1 mod 70 and 11q+20=3^k mod 3^(k+1), for bounded witness work."""
    if type(k) is not int or not 1 <= k <= MAX_RECHARGE_K:
        raise ValueError(f"witness k must be in 1..{MAX_RECHARGE_K}")
    modulus = 3 ** (k + 1)
    residue = ((3 ** k - 20) * pow(11, -1, modulus)) % modulus
    return crt_pair(1, 70, residue, modulus)


def forced_exit_progression():
    """For core 20, force s(20p)=22p+42 to have v_23=v_29=1."""
    residue, modulus = 11, 12
    for ell in (23, 29):
        local_modulus = ell ** 2
        local_residue = (ell - 42) * pow(22, -1, local_modulus) % local_modulus
        residue, modulus = crt_pair(residue, modulus, local_residue, local_modulus)
    return residue, modulus


def find_prime(residue, modulus, source_multiplier, *,
               max_candidates=MAX_CANDIDATES, source_cap=SOURCE_CAP,
               max_work=MAX_WORK):
    """Inspect only residue+j*modulus, j=0..max_candidates-1.

    A factorization failure is recorded, never interpreted as primality or
    compositeness. The result need not be the first prime if an earlier check
    was unresolved. The cap applies to source_multiplier*p, inclusively.
    """
    if not 1 <= max_candidates <= MAX_CANDIDATES:
        raise ValueError("candidate limit out of range")
    if not 1 <= source_cap <= SOURCE_CAP or max_work < 1:
        raise ValueError("invalid source/work limit")
    if modulus < 1 or not 0 <= residue < modulus or source_multiplier < 1:
        raise ValueError("invalid progression or source multiplier")
    tested = skipped = 0
    unresolved = []
    for j in range(max_candidates):
        p = residue + j * modulus
        if source_multiplier * p > source_cap:
            return {"status": "source_cap", "prime": None, "tested": tested,
                    "skipped": skipped, "unresolved_candidates": unresolved}
        if p < 2:
            skipped += 1
            continue
        tested += 1
        try:
            factors = factorize(p, max_work=max_work)
        except ComputationLimit:
            unresolved.append(str(p))
            continue
        if factors == [(p, 1)]:
            return {"status": "witness", "prime": p, "tested": tested,
                    "skipped": skipped, "unresolved_candidates": unresolved}
    return {"status": "candidate_limit", "prime": None, "tested": tested,
            "skipped": skipped, "unresolved_candidates": unresolved}


def checked_edge(source, expected, *, max_work=MAX_WORK):
    """Check one edge by two algorithms, respecting the inclusive source cap."""
    if not 1 <= source <= SOURCE_CAP:
        raise ComputationLimit("source outside verification cap")
    actual = aliquot_sum(source, max_work=max_work)
    independent = divisor_pair_sum(source)
    if actual != expected or independent != expected:
        raise AssertionError((source, expected, actual, independent))
    return {"source": str(source), "successor": str(expected),
            "independent_divisor_candidates": isqrt(source)}


def search_metadata(result, residue, modulus):
    return {"residue": str(residue), "modulus": str(modulus),
            "status": result["status"], "candidates_tested": result["tested"],
            "candidates_skipped": result["skipped"],
            "unresolved_candidates": result["unresolved_candidates"]}


def build_report():
    recharges = []
    unresolved_cases = []
    edges = []
    for k in range(1, MAX_RECHARGE_K + 1):
        residue, modulus = recharge_progression(k)
        result = find_prime(residue, modulus, 420)
        row = {"k": k, **search_metadata(result, residue, modulus)}
        q = result["prime"]
        if q is None:
            unresolved_cases.append(f"recharge_k_{k}:{result['status']}")
        else:
            u, following = 5 * q, 11 * q + 16
            if (gcd(u, CORE), gcd(following, CORE)) != (1, 1):
                raise AssertionError("core coprimality failed")
            if valuation(u + 4, 3) != 0 or valuation(following + 4, 3) != k:
                raise AssertionError("recharge valuation failed")
            if following % 5 != 2:
                raise AssertionError("the supplying factor 5 should be lost")
            try:
                edge = checked_edge(CORE * u, CORE * following)
            except ComputationLimit:
                row["status"] = "edge_unresolved"
                unresolved_cases.append(f"recharge_k_{k}:edge_work_limit")
            else:
                edges.append(edge)
                row.update({"q": str(q), "u": str(u), "next_u": str(following),
                            "input_charge": 0, "output_charge": k, "edge": edge})
        recharges.append(row)

    residue, modulus = forced_exit_progression()
    result = find_prime(residue, modulus, 20)
    forced_exit = search_metadata(result, residue, modulus)
    p = result["prime"]
    if p is None:
        unresolved_cases.append(f"forced_exit:{result['status']}")
    else:
        following = 22 * p + 42
        if valuation(following, 23) != 1 or valuation(following, 29) != 1:
            raise AssertionError("forced distinct factors missing")
        if gcd(p, 20) != 1 or p % 12 != 11:
            raise AssertionError("prime input guard failed")
        try:
            edge = checked_edge(20 * p, following)
        except ComputationLimit:
            forced_exit["status"] = "edge_unresolved"
            unresolved_cases.append("forced_exit:edge_work_limit")
        else:
            edges.append(edge)
            forced_exit.update({"p": str(p), "edge": edge,
                                "forced_primes": ["23", "29"],
                                "forced_exponents": [1, 1]})

    # Three guarded prime steps, then the actual step from composite cofactor 121.
    named_path = (1932, 3444, 5964, 10164, 19628)
    branch_edges = []
    for source, following in zip(named_path, named_path[1:]):
        try:
            edge = checked_edge(source, following)
        except ComputationLimit:
            unresolved_cases.append(f"named_source_{source}:edge_work_limit")
        else:
            edges.append(edge)
            branch_edges.append(edge)
    formal_next = Fraction(5 * 121 + 8, 3)
    candidate_unresolved = sum(len(row["unresolved_candidates"]) for row in recharges)
    candidate_unresolved += len(forced_exit["unresolved_candidates"])
    return {
        "purpose": "finite regression examples, not a conjecture decision",
        "limits": {"k_inclusive": [1, MAX_RECHARGE_K],
                   "candidate_indices_inclusive": [0, MAX_CANDIDATES - 1],
                   "source_cap_inclusive": str(SOURCE_CAP),
                   "factorization_work_per_call": MAX_WORK,
                   "new_witness_steps": 1, "named_branch_steps": 4},
        "recharges": recharges,
        "forced_exit": forced_exit,
        "named_branch": {"terms": [str(n) for n in named_path],
                         "checked_edges": branch_edges,
                         "invalid_formal_next_cofactor": {
                             "numerator": str(formal_next.numerator),
                             "denominator": str(formal_next.denominator)}},
        "totals": {"checked_edges": len(edges),
                   "progression_candidates_tested":
                       sum(row["candidates_tested"] for row in recharges)
                       + forced_exit["candidates_tested"],
                   "unresolved_candidate_factorizations": candidate_unresolved,
                   "unresolved_cases": unresolved_cases,
                   "max_checked_source": str(max(int(e["source"]) for e in edges)),
                   "divisor_pair_candidates":
                       sum(e["independent_divisor_candidates"] for e in edges)},
    }


if __name__ == "__main__":
    print(json.dumps(build_report(), indent=2, sort_keys=True))
