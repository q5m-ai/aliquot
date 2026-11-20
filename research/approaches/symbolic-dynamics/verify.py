#!/usr/bin/env python3
"""Bounded exact checks for REPORT.md; not an orbit search or a proof checker.

Run from the repository root:
    python3 research/approaches/symbolic-dynamics/verify.py
All mathematical integers in the JSON are decimal strings; counts are integers.
No probabilistic primality tests or external dependencies are used.
"""

from __future__ import annotations

import argparse
import json
from math import gcd, isqrt
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from aliquot import ComputationLimit, aliquot_sum, factorize

MAX_WORK = 20_000
COFACTOR_BOUND = 1_000
SIEVE_BOUND = 120_000
PAIR_SOURCE_CAP = 4_000_000
MODULUS_BOUND = 256
MODULAR_STEP_CAP = 1_024
NAMED_MODULI = (1, 2, 3, 8, 9, 2310, 2**8 * 3**5 * 5 * 7)
NAMED_SOURCES = (
    120, 220, 284, 7, 17, 37, 77, 211, 425,
    840, 2040, 4440, 9240, 25320,
    3847, 7697, 461640, 923640,
)


def proper_divisor_sieve(bound: int) -> list[int]:
    """Independent additive algorithm, inclusive bound; no factorization."""
    sums = [0] * (bound + 1)
    for divisor in range(1, bound // 2 + 1):
        for multiple in range(2 * divisor, bound + 1, divisor):
            sums[multiple] += divisor
    return sums


def pair_sum(n: int) -> int:
    """Independent proper-divisor pair enumeration, with a source cap."""
    if type(n) is not int or not 1 <= n <= PAIR_SOURCE_CAP:
        raise ValueError("divisor-pair source outside 1..4000000")
    total = 0
    for divisor in range(1, isqrt(n) + 1):
        if n % divisor == 0:
            other = n // divisor
            if divisor < n:
                total += divisor
            if other != divisor and other < n:
                total += other
    return total


def is_prime(n: int, *, max_work: int = MAX_WORK) -> bool:
    """Exact or raises ComputationLimit; unresolved is not False."""
    if n < 2:
        return False
    return factorize(n, max_work=max_work) == [(n, 1)]


def core120_step(u: int, *, max_work: int = MAX_WORK) -> int:
    """Actual s(120u) via the unitary-core identity, never past overlap."""
    if type(u) is not int or u < 1 or gcd(u, 120) != 1:
        raise ValueError("positive cofactor coprime to 120 required")
    return 120 * (2 * u + 3 * aliquot_sum(u, max_work=max_work))


def affine_unit_survivors(a: int, b: int, modulus: int) -> list[int]:
    """Exhaust the finite graph; each start takes at most modulus steps."""
    if modulus < 2:
        raise ValueError("modulus must be at least 2")
    survivors = []
    for start in range(1, modulus):
        value, seen = start, set()
        while gcd(value, modulus) == 1 and value not in seen:
            seen.add(value)
            value = (a * value + b) % modulus
        if value in seen:
            survivors.append(start)
    return survivors


def prime_obstruction(a: int, b: int, prime: int) -> bool:
    """The report's criterion; caller supplies a proven prime."""
    return (a % prime == b % prime == 0) or (
        a % prime == 1 and b % prime != 0
    )


def core120_residue(modulus: int) -> int:
    """Compatible residues of the report's nonintegral profinite point.

    x = -3 modulo the factor prime to 3; x = 1 modulo the 3-power.
    """
    if type(modulus) is not int or modulus < 1:
        raise ValueError("positive modulus required")
    other, power3 = modulus, 1
    while other % 3 == 0:
        other //= 3
        power3 *= 3
    if power3 == 1:
        return -3 % modulus
    return (-3 + other * ((4 * pow(other, -1, power3)) % power3)) % modulus


def residue_cycle(modulus: int, *, step_cap: int = MODULAR_STEP_CAP) -> list[int]:
    """Check a complete finite cycle, not a sample of an infinite orbit."""
    start = core120_residue(modulus)
    value, seen, states = start, set(), []
    for _ in range(step_cap):
        if gcd(value, modulus) != 1:
            raise AssertionError("claimed survivor is not a unit")
        if value in seen:
            if value != start:
                raise AssertionError("claimed cycle has a preperiod")
            return states
        seen.add(value)
        states.append(value)
        value = (2 * value + 3) % modulus
    raise ComputationLimit("modular cycle step cap reached")


def arithmetic_record(n: int, *, max_work: int = MAX_WORK) -> dict:
    independent = pair_sum(n)
    try:
        factors = factorize(n, max_work=max_work)
        actual = aliquot_sum(n, max_work=max_work)
    except ComputationLimit:
        return {"n": str(n), "status": "unresolved", "pair_sum": str(independent)}
    if actual != independent:
        raise AssertionError(f"divisor-pair mismatch at {n}")
    return {
        "n": str(n), "s": str(actual), "status": "verified",
        "factors": [[str(p), str(e)] for p, e in factors],
    }


def build_evidence(*, max_work: int = MAX_WORK) -> dict:
    if type(max_work) is not int or not 1 <= max_work <= 2_000_000:
        raise ValueError("max_work outside 1..2000000")
    sums = proper_divisor_sieve(SIEVE_BOUND)
    unitary_count = 0
    sieve_unresolved = []
    for u in range(1, COFACTOR_BOUND + 1):
        if gcd(u, 120) != 1:
            continue
        unitary_count += 1
        if sums[120 * u] != 120 * (2 * u + 3 * sums[u]):
            raise AssertionError(f"independent composite identity failed at {u}")
        for n in (u, 120 * u):
            try:
                actual = aliquot_sum(n, max_work=max_work)
            except ComputationLimit:
                sieve_unresolved.append(str(n))
                continue
            if actual != sums[n]:
                raise AssertionError(f"additive-sieve mismatch at {n}")

    # Independent small-prime list, not a second call to factorize.
    primes = [p for p in range(2, 44) if sums[p] == 1]
    classification_count = 0
    for a in range(2, 13):
        for b in range(1, 13):
            for prime in primes:
                survives = bool(affine_unit_survivors(a, b, prime))
                if survives == prime_obstruction(a, b, prime):
                    raise AssertionError(f"local criterion failed: {a}, {b}, {prime}")
                classification_count += 1

    modular_unresolved = []
    periods = {}
    for modulus in sorted(set(range(1, MODULUS_BOUND + 1)) | set(NAMED_MODULI)):
        try:
            cycle = residue_cycle(modulus)
        except ComputationLimit:
            modular_unresolved.append(str(modulus))
            continue
        periods[modulus] = len(cycle)

    named = [arithmetic_record(n, max_work=max_work) for n in NAMED_SOURCES]
    unresolved = (
        len(sieve_unresolved) + len(modular_unresolved)
        + sum(row["status"] == "unresolved" for row in named)
    )
    return {
        "scope": "finite arithmetic checks only; no conjecture resolution",
        "bounds": {
            "cofactor_inclusive": COFACTOR_BOUND,
            "additive_sieve_inclusive": SIEVE_BOUND,
            "divisor_pair_source_cap_inclusive": str(PAIR_SOURCE_CAP),
            "max_work_per_factorization": max_work,
            "moduli_inclusive": MODULUS_BOUND,
            "modular_steps_per_modulus": MODULAR_STEP_CAP,
            "affine_a_inclusive": [2, 12],
            "affine_b_inclusive": [1, 12],
            "classification_prime_inclusive": [2, 43],
            "aliquot_trace_transitions": 5,
        },
        "unitary_cofactors_checked": unitary_count,
        "factorized_sieve_comparisons": 2 * unitary_count - len(sieve_unresolved),
        "sieve_unresolved_inputs": sieve_unresolved,
        "local_classification_cases": classification_count,
        "moduli_checked": len(periods),
        "modular_unresolved_inputs": modular_unresolved,
        "largest_modular_period": max(periods.values(), default=0),
        "named_modular_cycles": [
            {"modulus": str(m), "start": str(core120_residue(m)), "period": periods[m]}
            for m in NAMED_MODULI if m in periods
        ],
        "named_arithmetic": named,
        "core120_trace": [str(n) for n in (840, 2040, 4440, 9240, 25320, 51000)],
        "trace_boundary": "425 shares factor 5 with core; do not iterate the core formula",
        "unresolved_checks": unresolved,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-work", type=int, default=MAX_WORK)
    args = parser.parse_args()
    print(json.dumps(build_evidence(max_work=args.max_work), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
