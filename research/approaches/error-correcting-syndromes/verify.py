#!/usr/bin/env python3
"""Bounded exact checks for REPORT.md; not an aliquot-conjecture decision procedure.

Run from any directory with Python 3.11+. No third-party dependencies.
Every factorization uses MAX_WORK; failures are recorded, never guessed prime.
All integers in persisted JSON are decimal strings (including small counts).
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
from math import gcd, isqrt
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from aliquot import ComputationLimit, aliquot_sum, factorize

MAX_WORK = 100_000
CORE_BOUND = 40
COFACTOR_BOUND = 80
AFFINE_BOUND = 12
PRIME_BOUND = 29
TRACE_STEPS = 6
TRACE_SOURCE_CAP = 100_000
NAMED_VALUES = (
    2, 6050, 6319, 840, 2040, 4440, 9240, 25320, 51000, 117480,
    637, 1757, 4291, 20017, 397,
)


def divisor_pair_sum(n: int) -> int:
    """Independent proper-divisor enumeration, with a bounded caller input."""
    if type(n) is not int or n < 1:
        raise ValueError("n must be a positive integer")
    total = 0
    for d in range(1, isqrt(n) + 1):
        if n % d == 0:
            other = n // d
            if d < n:
                total += d
            if other != d and other < n:
                total += other
    return total


def divisor_sieve(bound: int) -> list[int | None]:
    """Independent additive sieve; s(0) stays undefined."""
    sums: list[int | None] = [None] + [0] * bound
    for d in range(1, bound // 2 + 1):
        for n in range(2 * d, bound + 1, d):
            sums[n] += d
    return sums


def small_primes(bound: int) -> list[int]:
    return [n for n in range(2, bound + 1)
            if all(n % d for d in range(2, isqrt(n) + 1))]


def has_unit_cycle(a: int, b: int, modulus: int) -> bool:
    """Exhaust all nonzero starting residues; caller supplies a prime modulus."""
    for start in range(1, modulus):
        seen = set()
        x = start
        while x != 0 and x not in seen:
            seen.add(x)
            x = (a * x + b) % modulus
        if x != 0:
            return True
    return False


def local_obstruction(a: int, b: int, prime: int) -> bool:
    """The two bad cases proved in REPORT.md; prime is assumed prime."""
    return (a % prime == 0 and b % prime == 0) or (
        a % prime == 1 and b % prime != 0
    )


def safe_residue(a: int, b: int, modulus: int, *, max_work: int = MAX_WORK) -> int:
    """CRT starting residue whose affine iterates are all units modulo modulus.

    A local obstruction raises ValueError. Factorization exhaustion propagates
    ComputationLimit. This constructs residues, NOT a prime-valued orbit.
    """
    if any(type(x) is not int or x < 1 for x in (a, b, modulus)):
        raise ValueError("a, b, modulus must be positive integers")
    answer, accumulated = 0, 1
    for prime, exponent in factorize(modulus, max_work=max_work):
        if local_obstruction(a, b, prime):
            raise ValueError(f"no unit orbit modulo {prime}")
        power = prime ** exponent
        if a % prime not in (0, 1) and b % prime != 0:
            residue = (-b * pow(a - 1, -1, power)) % power
        else:
            residue = 1
        correction = ((residue - answer) * pow(accumulated, -1, power)) % power
        answer += accumulated * correction
        accumulated *= power
    return answer


def residue_orbit(a: int, b: int, modulus: int, start: int) -> dict:
    """At most modulus+1 state visits, stopping at the first repetition."""
    if modulus < 1:
        raise ValueError("modulus must be positive")
    seen, values = {}, []
    x = start % modulus
    for _ in range(modulus + 1):
        if x in seen:
            index = seen[x]
            return {"prefix": values[:index], "cycle": values[index:]}
        seen[x] = len(values)
        values.append(x)
        x = (a * x + b) % modulus
    raise AssertionError("finite residue orbit failed to repeat")


def arithmetic_record(n: int, *, max_work: int = MAX_WORK) -> dict:
    """Named, small inputs only: factorization plus independent divisor pairs."""
    try:
        factors = factorize(n, max_work=max_work)
        successor = aliquot_sum(n, max_work=max_work)
    except ComputationLimit:
        return {"n": n, "status": "unresolved_factorization"}
    independent = divisor_pair_sum(n)
    if successor != independent:
        raise AssertionError(f"independent sum mismatch at {n}")
    return {
        "n": n, "status": "exact", "factorization": factors,
        "sigma": n + successor, "s": successor,
        "divisor_pair_s": independent,
    }


def build_report() -> dict:
    unresolved = []
    sums = divisor_sieve(CORE_BOUND * COFACTOR_BOUND)
    checked_sources = set()
    pairs = 0
    for c in range(1, CORE_BOUND + 1):
        for q in range(1, COFACTOR_BOUND + 1):
            if gcd(c, q) != 1:
                continue
            for n in (c, q, c * q):
                if n in checked_sources:
                    continue
                try:
                    actual = aliquot_sum(n, max_work=MAX_WORK)
                except ComputationLimit:
                    unresolved.append({"phase": "coprime_box", "n": n})
                    continue
                if actual != sums[n]:
                    raise AssertionError(f"sieve mismatch at {n}")
                checked_sources.add(n)
            if not all(n in checked_sources for n in (c, q, c * q)):
                continue
            left = c * sums[c * q] - sums[c] * (c * q)
            right = c * (c + sums[c]) * sums[q]
            if left != right:
                raise AssertionError(f"syndrome identity failed at {(c, q)}")
            pairs += 1

    primes = small_primes(PRIME_BOUND)
    affine_cases = 0
    for a in range(1, AFFINE_BOUND + 1):
        for b in range(1, AFFINE_BOUND + 1):
            for prime in primes:
                if has_unit_cycle(a, b, prime) == local_obstruction(a, b, prime):
                    raise AssertionError(f"local criterion mismatch: {(a, b, prime)}")
                affine_cases += 1

    crt_examples = []
    for modulus in (1, 30, 900, 30030):
        try:
            start = safe_residue(2, 3, modulus)
        except ComputationLimit:
            unresolved.append({"phase": "crt", "modulus": modulus})
            continue
        orbit = residue_orbit(2, 3, modulus, start)
        if not all(gcd(x, modulus) == 1 for x in orbit["prefix"] + orbit["cycle"]):
            raise AssertionError("CRT example contains a nonunit")
        crt_examples.append({"modulus": modulus, "start_residue": start, **orbit})

    named = [arithmetic_record(n) for n in NAMED_VALUES]
    unresolved.extend({"phase": "named", "n": row["n"]}
                      for row in named if row["status"] != "exact")

    trace, current = [], 840
    trace_stop = "step_limit"
    for step in range(TRACE_STEPS):
        if current == 0:
            trace_stop = "terminated"
            break
        if current > TRACE_SOURCE_CAP:
            trace_stop = "source_cap"
            break
        row = arithmetic_record(current)
        if row["status"] != "exact":
            unresolved.append({"phase": "trace", "n": current})
            trace_stop = "unresolved_factorization"
            break
        q, remainder = divmod(current, 120)
        if remainder:
            raise AssertionError("named trace unexpectedly lost divisibility by 120")
        cofactor = arithmetic_record(q)
        if cofactor["status"] != "exact":
            unresolved.append({"phase": "cofactor", "n": q})
            trace_stop = "unresolved_factorization"
            break
        trace.append({
            "step": step, "source": current, "successor": row["s"],
            "cofactor": q, "coprime_to_120": gcd(q, 120) == 1,
            "cofactor_s": cofactor["s"], "delta": cofactor["s"] - 1,
            "prime_model_successor": 120 * (2 * q + 3),
            "coprime_composite_formula": 120 * (2 * q + 3 * cofactor["s"]),
        })
        current = row["s"]

    semiprime_cases = 0
    for i, p in enumerate(primes):
        for q in primes[i + 1:]:
            n = p * q
            if gcd(n, 30) == 1 and n % 5 == 2:
                sigma = (p + 1) * (q + 1)
                if sigma % 5 == 3 or (3 * sigma - n) % 5 == 2:
                    raise AssertionError("semiprime obstruction failed")
                if sigma - n != divisor_pair_sum(n):
                    raise AssertionError("semiprime independent check failed")
                semiprime_cases += 1

    sigma_small = 2 + divisor_pair_sum(2)
    sigma_large = 6050 + divisor_pair_sum(6050)
    return {
        "purpose": "finite regression evidence, not a universal mathematical proof",
        "bounds": {
            "factorization_work_per_call": MAX_WORK,
            "cores_inclusive": [1, CORE_BOUND],
            "cofactors_inclusive": [1, COFACTOR_BOUND],
            "additive_sieve_inclusive": [1, CORE_BOUND * COFACTOR_BOUND],
            "affine_a_and_b_inclusive": [1, AFFINE_BOUND],
            "test_primes_inclusive": [2, PRIME_BOUND],
            "trace_seed": 840, "trace_transitions": TRACE_STEPS,
            "trace_source_cap_inclusive": TRACE_SOURCE_CAP,
            "named_values": NAMED_VALUES,
            "named_max_divisor_trial": isqrt(max(NAMED_VALUES)),
        },
        "coprime_box": {"pairs_checked": pairs, "distinct_sources_checked": len(checked_sources)},
        "affine_local_criterion": {"cases_checked": affine_cases, "primes": primes},
        "crt_residue_orbits_not_prime_orbits": crt_examples,
        "semiprime_filter_cases": semiprime_cases,
        "named_arithmetic": named,
        "invisible_abundance_example": {
            "modulus": 6, "base": 2, "multiplier": 3025, "perturbed": 6050,
            "base_abundancy": Fraction(sigma_small, 2),
            "perturbed_abundancy": Fraction(sigma_large, 6050),
            "base_signature_n_sigma_s": [2 % 6, sigma_small % 6, (sigma_small - 2) % 6],
            "perturbed_signature_n_sigma_s": [6050 % 6, sigma_large % 6, (sigma_large - 6050) % 6],
        },
        "actual_trace": trace,
        "trace_stop": trace_stop,
        "trace_final_value": current,
        "trace_continuation": "not attempted; no orbit-resolution claim",
        "unresolved_arithmetic_count": len(unresolved),
        "unresolved_arithmetic": unresolved,
    }


def decimal_data(value):
    if isinstance(value, bool) or value is None or isinstance(value, str):
        return value
    if isinstance(value, int):
        return str(value)
    if isinstance(value, Fraction):
        return {"numerator": str(value.numerator), "denominator": str(value.denominator)}
    if isinstance(value, dict):
        return {key: decimal_data(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [decimal_data(item) for item in value]
    raise TypeError(f"unsupported persisted value: {type(value).__name__}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="write deterministic JSON instead of stdout")
    args = parser.parse_args()
    report = build_report()
    text = json.dumps(decimal_data(report), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text)
    else:
        print(text, end="")
    return 1 if report["unresolved_arithmetic_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
