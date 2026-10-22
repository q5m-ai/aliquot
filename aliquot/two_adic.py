"""Exact even-step valuation law and a bounded, independently checked census.

This is not an orbit solver. A factorization-budget failure remains unresolved.
"""

from dataclasses import dataclass
from math import isqrt

from . import DEFAULT_MAX_WORK, factorize, positive_integer
from .research import divisor_sieve

DEFAULT_BOUND = 100_000
MAX_BOUND = 100_000
RESIDUE_BITS = 10


def valuation_two(n):
    """v_2(n) for positive integers only; do not assign a finite value to v_2(0)."""
    positive_integer(n)
    return (n & -n).bit_length() - 1


@dataclass(frozen=True)
class EvenStep:
    n: int
    odd_part: int
    a: int
    sigma_odd: int
    b: int
    successor: int
    predicted_valuation: int
    branch: str


def even_step(n, *, max_work=DEFAULT_MAX_WORK):
    """Factor n=2^a*m and predict v_2(s(n)) from the prime-exponent law.

    b=v_2(sigma(m)) is obtained from LTE, not by inspecting sigma(m).
    The resonant branch b=a also needs the odd units, not just (a,b).
    """
    positive_integer(n)
    if n % 2:
        raise ValueError("n must be even")
    factors = factorize(n, max_work=max_work)
    a = factors[0][1]
    odd_part = n >> a
    sigma_odd, b = 1, 0
    for prime, exponent in factors[1:]:
        sigma_odd *= (prime ** (exponent + 1) - 1) // (prime - 1)
        if exponent % 2:
            b += valuation_two(prime + 1) + valuation_two(exponent + 1) - 1
    multiplier = (1 << (a + 1)) - 1
    successor = multiplier * sigma_odd - n
    if b < a:
        predicted, branch = b, "drops"
    elif b > a:
        predicted, branch = a, "stays"
    else:
        predicted = a + valuation_two(multiplier * (sigma_odd >> a) - odd_part)
        branch = "rises"
    return EvenStep(n, odd_part, a, sigma_odd, b, successor, predicted, branch)


def _divisor_pair_sum(n):
    """Independent exact proper-divisor sum, with no factorization or LTE."""
    positive_integer(n)
    if n == 1:
        return 0
    total = 1
    for divisor in range(2, isqrt(n) + 1):
        if n % divisor == 0:
            total += divisor
            partner = n // divisor
            if partner != divisor:
                total += partner
    return total


def _check_step(step, independent_successor, independent_sigma_odd):
    if (step.successor != independent_successor or
            step.sigma_odd != independent_sigma_odd or
            step.b != valuation_two(independent_sigma_odd) or
            step.predicted_valuation != valuation_two(independent_successor)):
        raise ArithmeticError(f"Independent two-adic check failed at n={step.n}")


def _example(step):
    return {"n": str(step.n), "a": step.a, "b": step.b,
            "next": str(step.successor), "nextValuation": step.predicted_valuation}


def scan_two_adic(bound=DEFAULT_BOUND):
    """Check one step for even sources, and at most two steps inside C6.

    Only the source is bounded by `bound`; successors are computed exactly.
    A separate divisor-pair algorithm checks every second transition.
    """
    positive_integer(bound, "bound")
    if bound > MAX_BOUND:
        raise ValueError(f"two-adic bound must be at most {MAX_BOUND}")
    sums = divisor_sieve(bound)
    branches = dict(drops=0, stays=0, rises=0)
    outcomes = dict(firstExitOdd=0, firstExitMultipleOfFour=0,
                    secondExitOdd=0, secondExitMultipleOfFour=0,
                    retainedThroughTwoSteps=0)
    first_examples = {}
    modulus = 1 << RESIDUE_BITS
    prime_witnesses = {}
    largest_first_successor = 0
    largest_second_successor = 0
    second_steps = 0
    for n in range(2, bound + 1, 2):
        step = even_step(n)
        _check_step(step, sums[n], sums[step.odd_part] + step.odd_part)
        branches[step.branch] += 1
        first_examples.setdefault(step.branch, _example(step))
        largest_first_successor = max(largest_first_successor, step.successor)
        if n % 12 != 6:
            continue
        if step.successor % 3 or (step.successor != n if n == 6 else step.successor <= n):
            raise ArithmeticError(f"C6 growth/divisibility check failed at n={n}")
        if step.successor % 2:
            outcomes["firstExitOdd"] += 1
        elif step.successor % 4 == 0:
            outcomes["firstExitMultipleOfFour"] += 1
        else:
            second = even_step(step.successor)
            independent_second = _divisor_pair_sum(second.n)
            independent_sigma = _divisor_pair_sum(second.odd_part) + second.odd_part
            _check_step(second, independent_second, independent_sigma)
            if independent_second % 3 or (independent_second != second.n if second.n == 6
                                         else independent_second <= second.n):
                raise ArithmeticError(f"Second C6 growth/divisibility check failed at n={n}")
            key = ("secondExitOdd" if independent_second % 2 else
                   "secondExitMultipleOfFour" if independent_second % 4 == 0 else
                   "retainedThroughTwoSteps")
            outcomes[key] += 1
            second_steps += 1
            largest_second_successor = max(largest_second_successor, independent_second)
        # For a proven prime p>3, s(6p)=6p+12. Record one edge per residue.
        p = n // 6
        if p > 3 and sums[p] == 1:
            if factorize(p) != [(p, 1)] or step.successor != n + 12:
                raise ArithmeticError(f"Prime-branch check failed at p={p}")
            prime_witnesses.setdefault(n % modulus, p)
    return {
        "schema": "aliquot-two-adic-scan-v1",
        "bound": str(bound),
        "scope": "one step for every even source; C6 sources stop at the first exit or after two steps",
        "arithmetic": {
            "primary": "Python int trial factorization, product formula, and prime-exponent valuation law",
            "independentFirstStep": "Python int additive proper-divisor sieve",
            "independentSecondStep": "Python int divisor-pair enumeration, including odd-part divisor sums",
        },
        "evenSources": sum(branches.values()),
        "valuationBranches": branches,
        "firstExamples": first_examples,
        "sixClass": {"sources": sum(outcomes.values()), "secondStepsChecked": second_steps,
                     "outcomes": outcomes, "includesFixedPointSix": bound >= 6},
        "largestFirstSuccessor": str(largest_first_successor),
        "largestSecondSuccessor": str(largest_second_successor),
        "primeBranchResidues": {
            "modulus": str(modulus), "edge": "r -> r + 12 (mod modulus)",
            "eligibleResidues": modulus // 4, "coveredResidues": len(prime_witnesses),
            "completeCoverage": len(prime_witnesses) == modulus // 4,
            "largestFirstWitnessPrime": str(max(prime_witnesses.values(), default=0)),
            "scope": "observed prime-branch edges only; no inference from missing edges",
        },
        "checks": {"divisorSumsMatched": True, "primeExponentValuationsMatched": True,
                   "successorValuationsMatched": True, "sixClassGrowthAndDivisibilityMatched": True},
        "conclusion": "Finite checks only; no proof/disproof, divergent orbit, or orbit survival probability.",
    }
