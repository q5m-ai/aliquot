#!/usr/bin/env python3
"""Bounded regressions for REPORT.md; not a proof or an orbit-survival search.

Run from the repository root. Uses only the standard library and the existing
exact aliquot API. A ComputationLimit is recorded as unresolved, never composite.
"""

from fractions import Fraction
from math import gcd, isqrt
from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from aliquot import ComputationLimit, aliquot_sum, factorize  # noqa: E402

MAX_WORK = 100_000
PRIME_BOUND = 10_000
SIEVE_BOUND = 500_000
THRESHOLD = 527


def valuation(n, prime):
    if type(n) is not int or n < 1 or prime not in (2, 3):
        raise ValueError("positive n and valuation prime 2 or 3 required")
    exponent = 0
    while n % prime == 0:
        n //= prime
        exponent += 1
    return exponent


def divisor_pair_sum(n):
    if type(n) is not int or n < 1:
        raise ValueError("positive n required; s(0) is undefined")
    total = 0
    for d in range(1, isqrt(n) + 1):
        if n % d == 0:
            total += d
            if d * d != n:
                total += n // d
    return total - n


def divisor_sieve(bound):
    sums = [0] * (bound + 1)
    for d in range(1, bound // 2 + 1):
        for multiple in range(2 * d, bound + 1, d):
            sums[multiple] += d
    return sums


def is_prime(n, *, max_work=MAX_WORK):
    return n >= 2 and factorize(n, max_work=max_work) == [(n, 1)]


def bounded_core(n, bound, *, max_work=MAX_WORK):
    """A coprime prime-cofactor representation, or None, by proven factoring.

    Choose the smallest core if several representations exist at small n.
    For n > bound**2 any such representation is unique.
    """
    if type(n) is not int or n < 1 or type(bound) is not int or bound < 1:
        raise ValueError("positive integer n and bound required")
    for p, exponent in reversed(factorize(n, max_work=max_work)):
        if exponent == 1 and n // p <= bound:
            return n // p, p
    return None


def rank17(n, *, max_work=MAX_WORK):
    """Rank for the restricted domain only; not a global aliquot ranking."""
    if type(n) is not int or n <= THRESHOLD:
        raise ValueError("rank is defined only above 527")
    shape = bounded_core(n, 17, max_work=max_work)
    if shape is None:
        raise ValueError("no coprime prime cofactor with core <= 17")
    core, p = shape
    if core == 6:
        return 2, int(p % 3 == 2)
    if core == 12:
        return 1, valuation(p + 7, 3)
    return 0, n


def active_budget(p):
    """Arithmetic expression; the caller separately verifies primality."""
    if type(p) is not int or p <= 3 or p % 3 == 0:
        raise ValueError("p > 3, coprime to 3, required")
    c = 13 if p % 3 == 2 else 17
    return c, valuation(p + c, 2), valuation(p + c, 3)


def guarded_return(p, *, max_work=MAX_WORK):
    """One actual 18-core return within {6,18}, or a failed finite guard.

    None means that a prime/phase guard fails, not that the aliquot orbit
    terminates. ComputationLimit propagates without being turned into None.
    The returned checkpoint need not pass the next return's guards.
    """
    if type(p) is not int or p <= 31:
        raise ValueError("p must be an integer greater than 31")
    if not is_prime(p, max_work=max_work) or p % 4 != 3:
        return None
    if p % 3 == 2:
        q, remainder = divmod(7 * p + 13, 6)
        if remainder or not is_prime(q, max_work=max_work):
            return None
        return q, (18 * p, 18 * q)
    r = (7 * p + 13) // 2
    q, remainder = divmod(7 * p + 17, 6)
    if (remainder or not is_prime(r, max_work=max_work)
            or not is_prime(q, max_work=max_work)):
        return None
    return q, (18 * p, 6 * r, 18 * q)


NAMED_PATHS = {
    "six_residue_rank": (606, 618, 630),
    "twelve_valuation_rank": (1212, 1644, 2220),
    "phase_drop_with_size_increase": (732, 1004),
    "deficient_size_rank": (592, 586),
    "two_budget_recharge_then_class_exit": (1926, 2286, 2706),
    "amicable_cycle_allowed_below_cutoff": (220, 284, 220),
    "perfect_cycle_allowed_below_cutoff": (496, 496),
    "termination_not_s_zero": (2, 1, 0),
}


def verify():
    sums = divisor_sieve(SIEVE_BOUND)
    primes = [p for p in range(2, PRIME_BOUND + 1) if sums[p] == 1]
    unresolved = []
    for p in primes:
        try:
            assert is_prime(p)
        except ComputationLimit:
            unresolved.append({"stage": "prime-list", "value": str(p)})

    affine_cases = rank_edges = 0
    phase_edges = {}
    max_affine_source = max_affine_successor = 0
    for core in range(1, 20):
        assert aliquot_sum(core, max_work=MAX_WORK) == sums[core]
        for p in primes:
            if gcd(core, p) != 1:
                continue
            n = core * p
            try:
                m = aliquot_sum(n, max_work=MAX_WORK)
                assert m == sums[n] == sums[core] * p + sums[core] + core
                affine_cases += 1
                max_affine_source = max(max_affine_source, n)
                max_affine_successor = max(max_affine_successor, m)
                if core <= 17 and n > THRESHOLD and m > THRESHOLD:
                    if bounded_core(m, 17) is not None:
                        before, after = rank17(n), rank17(m)
                        assert after < before
                        rank_edges += 1
                        key = f"{before[0]}->{after[0]}"
                        phase_edges[key] = phase_edges.get(key, 0) + 1
            except ComputationLimit:
                unresolved.append({"stage": "affine-or-rank", "value": str(n)})

    return_count = 0
    branches = {"13": 0, "17": 0}
    recharges = []
    max_return_source = 0
    for p in primes:
        if p <= 31:
            continue
        try:
            result = guarded_return(p)
            # An independent sieve-based evaluation of all finite guards.
            expected = None
            if p % 4 == 3:
                if p % 3 == 2:
                    q = (7 * p + 13) // 6
                    if sums[q] == 1:
                        expected = q, (18 * p, 18 * q)
                else:
                    r, q = (7 * p + 13) // 2, (7 * p + 17) // 6
                    if sums[r] == sums[q] == 1:
                        expected = q, (18 * p, 6 * r, 18 * q)
            assert result == expected
            if result is None:
                continue
            q, path = result
            return_count += 1
            c, a, b = active_budget(p)
            branches[str(c)] += 1
            for n, m in zip(path, path[1:]):
                assert sums[n] == aliquot_sum(n, max_work=MAX_WORK) == m
                max_return_source = max(max_return_source, n)
            new_c, new_a, new_b = active_budget(q)
            assert Fraction(q + c) == Fraction(7, 6) * (p + c)
            assert (new_c != c) == (b == 1)
            if c == new_c:
                assert (new_a, new_b) == (a - 1, b - 1)
            if new_a > a and new_b > b:
                # At most one additional accelerated return; no open-ended trace.
                following = guarded_return(q)
                if following is not None:
                    for n, m in zip(following[1], following[1][1:]):
                        assert sums[n] == aliquot_sum(n, max_work=MAX_WORK) == m
                        max_return_source = max(max_return_source, n)
                recharges.append({
                    "p": str(p), "q": str(q),
                    "before": [a, b], "after": [new_a, new_b],
                    "next_return_passes": following is not None,
                })
        except ComputationLimit:
            unresolved.append({"stage": "return-guards", "value": str(p)})

    # A bounded test of four simultaneous primes around a balanced recharge.
    # v=0..1000 inclusive; not a prime-tuples theorem or a renewed orbit.
    eligible = prime_tests = matches = 0
    for v in range(1001):
        if gcd(7 * v + 1, 6) != 1:
            continue
        eligible += 1
        forms = (864 * v + 107, 1008 * v + 127,
                 3528 * v + 451, 1176 * v + 151)
        flags = []
        for value in forms:
            try:
                flag = is_prime(value)
                assert flag == (divisor_pair_sum(value) == 1)
                prime_tests += 1
                flags.append(flag)
            except ComputationLimit:
                unresolved.append({"stage": "four-forms", "value": str(value)})
        if len(flags) == 4 and all(flags):
            matches += 1

    named_transitions = 0
    for path in NAMED_PATHS.values():
        for n, m in zip(path, path[1:]):
            try:
                assert aliquot_sum(n, max_work=MAX_WORK) == divisor_pair_sum(n) == m
                named_transitions += 1
            except ComputationLimit:
                unresolved.append({"stage": "named-path", "value": str(n)})

    return {
        "scope": "finite regression evidence, not a mathematical proof review",
        "bounds": {
            "cores_inclusive": [1, 19], "prime_cofactors_inclusive": [2, PRIME_BOUND],
            "additive_sieve_inclusive": [1, SIEVE_BOUND],
            "max_work_per_factorization_call": MAX_WORK,
            "transitions_per_affine_source": 1,
            "accelerated_returns_per_selected_start_at_most": 2,
            "actual_transitions_per_accelerated_return_at_most": 2,
            "four_form_parameters_inclusive": [0, 1000],
            "four_form_value_upper_bound": "3528451",
        },
        "prime_count": len(primes),
        "affine_cases": affine_cases,
        "largest_affine_source": str(max_affine_source),
        "largest_affine_successor": str(max_affine_successor),
        "rank17_edges_checked": rank_edges,
        "rank17_phase_edges": dict(sorted(phase_edges.items())),
        "guarded_returns": return_count,
        "guarded_return_branches": branches,
        "largest_checked_return_source": str(max_return_source),
        "both_budgets_increase": recharges,
        "four_form_eligible_parameters": eligible,
        "four_form_prime_checks": prime_tests,
        "four_form_all_prime_matches": matches,
        "named_transitions": named_transitions,
        "named_paths": {key: [str(n) for n in path] for key, path in NAMED_PATHS.items()},
        "unresolved_count": len(unresolved), "unresolved": unresolved,
    }


if __name__ == "__main__":
    evidence = verify()
    print(json.dumps(evidence, indent=2, sort_keys=True))
    if evidence["unresolved_count"]:
        raise SystemExit(2)
