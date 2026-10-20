"""Bounded one-step C6 census with an algorithmically independent verifier."""

from . import factorize, positive_integer

MAX_BOUND = 1_000_000
DEFAULT_BOUND = 100_000


def require_bound(bound):
    positive_integer(bound, "bound")
    if bound > MAX_BOUND:
        raise ValueError(f"bound must be at most {MAX_BOUND}")


def analyze_six(n):
    positive_integer(n)
    if n % 12 != 6:
        raise ValueError("n must lie in C6: n ≡ 6 (mod 12)")
    factors = factorize(n)
    sigma = 1
    for prime, exponent in factors:
        sigma *= (prime ** (exponent + 1) - 1) // (prime - 1)
    odd_exponents = [(p, e) for p, e in factors if p != 2 and e % 2]
    prediction = "retained"
    if not odd_exponents:
        prediction = "exitsToOdd"
    elif len(odd_exponents) == 1:
        p, e = odd_exponents[0]
        if p % 4 == 1 and e % 4 == 1:
            prediction = "exitsToMultipleOfFour"
    return sigma - n, factors, prediction


def divisor_sieve(bound):
    """Add proper divisors to multiples; no factoring or product formula."""
    require_bound(bound)
    sums = [0] * (bound + 1)
    sums[0] = None  # s(0) is undefined.
    for d in range(1, bound // 2 + 1):
        for n in range(2 * d, bound + 1, d):
            sums[n] += d
    return sums


def scan_six(bound=DEFAULT_BOUND):
    require_bound(bound)
    independent_sums = divisor_sieve(bound)
    counts = dict(retained=0, exitsToOdd=0, exitsToMultipleOfFour=0)
    first_examples = {}
    for n in range(6, bound + 1, 12):
        total, factors, prediction = analyze_six(n)
        independent = independent_sums[n]
        observed = ("exitsToOdd" if independent % 2 else
                    "exitsToMultipleOfFour" if independent % 4 == 0 else "retained")
        if (total != independent or prediction != observed or independent % 3 or
                (independent != n if n == 6 else independent <= n)):
            raise ArithmeticError(f"Independent check failed at n={n}")
        counts[observed] += 1
        if observed not in first_examples:
            first_examples[observed] = {
                "n": str(n), "next": str(total),
                "factorization": [{"prime": str(p), "exponent": e} for p, e in factors],
            }
    return {
        "schema": "aliquot-six-class-scan-v1",
        "bound": str(bound),
        "sourceClass": "positive n ≡ 6 (mod 12)",
        "scope": "one step for every source in the class up to the inclusive bound",
        "arithmetic": {
            "primary": "Python int trial factorization and multiplicative divisor sum",
            "independentCheck": "Python int additive proper-divisor sieve",
        },
        "candidates": sum(counts.values()), "counts": counts,
        "checks": {
            "divisorSumsMatched": True, "exitClassificationMatched": True,
            "successorsDivisibleByThree": True, "strictGrowthAboveSix": True,
        },
        "firstExamples": first_examples,
        "conclusion": "Finite census only. No divergent orbit or proof/disproof of the conjecture is established.",
    }
