"""Exact 2–3 supply accounting and finite first-return certificates.

The infinite entry-family theorem lives in research/REGENERATION.md. These
bounded computations neither prove infinite regeneration nor claim novelty.
"""

from dataclasses import dataclass
from fractions import Fraction
from math import gcd

from . import ComputationLimit, DEFAULT_MAX_WORK, factorize, positive_integer
from .two_adic import _divisor_pair_sum

MAX_TERM = 1_000_000  # Largest source allowed in independent divisor-pair checks.
MAX_STEPS = 256
DEFAULT_STEPS = 64


def valuation(n, prime):
    """v_2 or v_3 of a positive integer; zero has no finite valuation here."""
    positive_integer(n)
    if type(prime) is not int or prime not in (2, 3):
        raise ValueError("prime must be 2 or 3")
    exponent = 0
    while n % prime == 0:
        n //= prime
        exponent += 1
    return exponent


@dataclass(frozen=True)
class CoupledStep:
    n: int
    a: int
    b: int
    cofactor: int
    sigma_cofactor: int
    sigma: int
    supply_two: int
    supply_three: int
    successor: int
    next_a: int | None
    next_b: int | None


def coupled_step(n, *, max_work=DEFAULT_MAX_WORK):
    """Compute an exact step and predict both successor valuations from LTE.

    For s(1)=0, next_a and next_b are None, never finite valuations of zero.
    Factorization exhaustion propagates as ComputationLimit.
    """
    factors = factorize(n, max_work=max_work)
    a = b = 0
    sigma_m, m_two, m_three = 1, 0, 0
    for p, e in factors:
        if p == 2:
            a = e
        elif p == 3:
            b = e
        else:
            sigma_m *= (p ** (e + 1) - 1) // (p - 1)
            if e % 2:
                m_two += valuation(p + 1, 2) + valuation(e + 1, 2) - 1
            if p % 3 == 1:
                m_three += valuation(e + 1, 3)
            elif e % 2:
                m_three += valuation(p + 1, 3) + valuation(e + 1, 3)
    m = n // (2 ** a * 3 ** b)
    supply_two = m_two + (1 + valuation(b + 1, 2) if b % 2 else 0)
    supply_three = m_three + (1 + valuation(a + 1, 3) if a % 2 else 0)
    sigma = (2 ** (a + 1) - 1) * ((3 ** (b + 1) - 1) // 2) * sigma_m
    following = sigma - n

    def predict(prime, present, supply):
        if following == 0:
            return None
        if present != supply:
            return min(present, supply)
        unit_difference = sigma // prime ** present - n // prime ** present
        return present + valuation(unit_difference, prime)

    return CoupledStep(n, a, b, m, sigma_m, sigma, supply_two, supply_three,
                       following, predict(2, a, supply_two), predict(3, b, supply_three))


def _source_cap(max_term):
    positive_integer(max_term, "max_term")
    if max_term > MAX_TERM:
        raise ValueError(f"max_term must be at most {MAX_TERM}")


def _checked_step(n, max_term, max_work):
    if n > max_term:
        raise ComputationLimit("Source exceeds the independent-verification term limit.")
    step = coupled_step(n, max_work=max_work)
    independent = _divisor_pair_sum(n)
    sigma_m = _divisor_pair_sum(step.cofactor) + step.cofactor
    expected_a = valuation(independent, 2) if independent else None
    expected_b = valuation(independent, 3) if independent else None
    if (step.successor != independent or step.sigma_cofactor != sigma_m or
            step.supply_two != valuation(independent + n, 2) or
            step.supply_three != valuation(independent + n, 3) or
            step.next_a != expected_a or step.next_b != expected_b):
        raise ArithmeticError(f"Independent coupled-valuation check failed at n={n}")
    return step


def in_return_class(n):
    """G={6u: u odd, u≡2 (mod 3)}={positive n≡30 (mod 36)}."""
    positive_integer(n)
    return n % 36 == 30


def _ratio(value):
    return {"numerator": str(value.numerator), "denominator": str(value.denominator)}


def certify_regeneration(u, d, *, max_term=MAX_TERM, max_work=DEFAULT_MAX_WORK):
    """Verify one two-step first return, guarded by a unitary factor d of T(u).

    Not a closure certificate: the returned cofactor need not satisfy the guard.
    Only sources of computed steps are capped; a known final value is not clipped.
    """
    positive_integer(u, "u")
    positive_integer(d, "d")
    positive_integer(max_work, "max_work")
    _source_cap(max_term)
    if u % 6 != 5:
        raise ValueError("u must be odd and congruent to 2 modulo 3")
    if d <= 1 or gcd(d, 6) != 1:
        raise ValueError("d must exceed 1 and be coprime to 6")
    first = _checked_step(6 * u, max_term, max_work)
    middle = first.successor // 6
    if first.successor % 6 or middle % d or gcd(d, middle // d) != 1:
        raise ValueError("d must be a unitary divisor of T(u)")
    divisor_step = _checked_step(d, max_term, max_work)
    sigma_d = divisor_step.sigma
    if sigma_d % 3:
        raise ValueError("sigma(d) must be divisible by 3")
    second = _checked_step(first.successor, max_term, max_work)
    following = second.successor // 6
    rho = Fraction(2 * sigma_d - d, d)
    actual = Fraction(second.successor, 6 * u)
    if (in_return_class(first.successor) or not in_return_class(second.successor) or
            first.a != 1 or first.b != 1 or second.a != 1 or second.b != 1 or
            valuation(second.successor, 2) != 1 or valuation(second.successor, 3) != 1 or
            actual <= rho or first.successor <= 6 * u or second.successor <= first.successor):
        raise ArithmeticError("Two-step return/growth certificate failed.")
    return {"u": str(u), "d": str(d), "sigmaD": str(sigma_d),
            "cofactorPath": [str(u), str(middle), str(following)],
            "aliquotPath": [str(6 * u), str(first.successor), str(second.successor)],
            "strictGrowthFactorLowerBound": _ratio(rho), "actualGrowthFactor": _ratio(actual),
            "firstReturnSteps": 2,
            "scope": "one certified return only; the next entry guard is not established"}


def prime_entry_class(d, *, max_work=DEFAULT_MAX_WORK):
    """CRT class for the written Dirichlet theorem; does not generate a prime."""
    positive_integer(d, "d")
    if d <= 1 or gcd(d, 6) != 1:
        raise ValueError("d must exceed 1 and be coprime to 6")
    sigma_d = coupled_step(d, max_work=max_work).sigma
    if sigma_d % 3:
        raise ValueError("sigma(d) must be divisible by 3")
    modulus = 6 * d * d
    residue = d - 2 + d * d * ((7 - d) % 6)
    if gcd(residue, modulus) != 1:
        raise ArithmeticError("The CRT entry class is not reduced.")
    return {"residue": str(residue), "modulus": str(modulus)}


def trace_first_return(seed, *, max_steps=DEFAULT_STEPS, max_term=MAX_TERM,
                       max_work=DEFAULT_MAX_WORK):
    """First positive-time return to G, including excursions outside 6|n.

    Exact return/termination/cycle detection precedes the next source-cap check.
    Limits mean unresolved, not no-return. No factorization of an unresolved
    residual is accepted. Repetition outside G proves no future return to G.
    """
    if not in_return_class(seed):
        raise ValueError("seed must be congruent to 30 modulo 36")
    positive_integer(max_steps, "max_steps")
    positive_integer(max_work, "max_work")
    _source_cap(max_term)
    if max_steps > MAX_STEPS:
        raise ValueError(f"max_steps must be at most {MAX_STEPS}")
    terms, seen = [seed], {seed: 0}
    status, cycle_start = "step_limit", None
    for _ in range(max_steps):
        current = terms[-1]
        if current > max_term:
            status = "term_limit"
            break
        try:
            step = _checked_step(current, max_term, max_work)
        except ComputationLimit:
            status = "factorization_limit"
            break
        following = step.successor
        terms.append(following)
        if following == 0:
            status = "terminated"
            break
        if in_return_class(following):
            status = "returned"
            break
        if following in seen:
            status, cycle_start = "cycle", seen[following]
            break
        seen[following] = len(terms) - 1
    return {"seed": str(seed), "status": status, "terms": [str(n) for n in terms],
            "stepsComputed": len(terms) - 1, "cycleStartIndex": cycle_start,
            "growthFactor": _ratio(Fraction(terms[-1], seed)) if status == "returned" else None,
            "limits": {"steps": max_steps, "sourceTerm": str(max_term),
                       "factorizationWorkPerCall": max_work}}


def regeneration_report():
    """Small named proof/regression examples, not an orbit-frequency census."""
    families = []
    for d, p in [(5, 53), (35, 9833), (55, 53), (385, 383), (5005, 5003)]:
        entry = prime_entry_class(d)
        if factorize(p) != [(p, 1)] or _divisor_pair_sum(p) != 1:
            raise ArithmeticError(f"Entry parameter is not a proven prime: {p}")
        if p % int(entry["modulus"]) != int(entry["residue"]):
            raise ArithmeticError("Prime does not belong to its entry class.")
        families.append({"prime": str(p), "entryClass": entry, **certify_regeneration(p, d)})
    examples = []
    for n in [72, 1122, 1470, 2634, 2646, 66, 500394]:
        step = _checked_step(n, MAX_TERM, DEFAULT_MAX_WORK)
        examples.append({"n": str(n), "a": step.a, "b": step.b,
                         "cofactor": str(step.cofactor), "sigmaCofactor": str(step.sigma_cofactor),
                         "sigma": str(step.sigma), "supplyTwo": step.supply_two,
                         "supplyThree": step.supply_three, "next": str(step.successor),
                         "nextA": step.next_a, "nextB": step.next_b})
    return {"schema": "aliquot-regeneration-examples-v1",
            "scope": "named finite certificates and counterexamples, not a source census",
            "returnClass": "positive n congruent to 30 modulo 36",
            "arithmetic": {"primary": "proven trial factorization and exact 2–3 valuation laws",
                           "independent": "divisor-pair sums, including coprime cofactor sums"},
            "coupledExamples": examples, "primeEntryExamples": families,
            "firstReturns": [trace_first_return(n) for n in [30, 66, 318, 534, 1470, 7626, 3162, 500394]],
            "conclusion": "Finite returns do not compose automatically; no perpetual regeneration or conjecture resolution."}
