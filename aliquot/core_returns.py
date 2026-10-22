"""Perfect-core regeneration after a prime-power spike, with finite checks.

Base-4 digits group binary digits; they do not define an independent prime
valuation. No finite trace or local return is an infinite-orbit certificate.
"""

from dataclasses import dataclass
from math import gcd, isqrt

from . import ComputationLimit, DEFAULT_MAX_WORK, aliquot_sum, factorize, positive_integer
from .regeneration import certify_regeneration, valuation
from .two_adic import _divisor_pair_sum

MAX_SOURCE = 1_000_000
MAX_STEPS = 256
MAX_PRECISION = 16
CORES = {6: (1, 3), 28: (2, 7)}


def _core(core):
    if type(core) is not int or core not in CORES:
        raise ValueError("core must be 6 or 28")
    return CORES[core]


def _order(n, prime):
    # The only primes passed by this module are the proven constants 2, 3, 7.
    positive_integer(n)
    exponent = 0
    while n % prime == 0:
        n //= prime
        exponent += 1
    return exponent


def _sigma(n, max_work):
    return aliquot_sum(n, max_work=max_work) + n


@dataclass(frozen=True)
class CoreStep:
    n: int
    core: int
    a: int
    q: int
    b: int
    cofactor: int
    sigma_cofactor: int
    successor: int
    next_a: int
    next_b: int
    bridge_predicted: bool | None


def core_step(n, core, *, max_work=DEFAULT_MAX_WORK):
    """Exact step from v2(n)=a, q|n for core=2^a*q in {6,28}.

    For b>=2, bridge_predicted says whether the next term restores EXACTLY
    v2=a and vq=1. False does not necessarily mean driver loss or decline.
    For b=1 there is no prime-power spike and that predicate is None.
    """
    positive_integer(n)
    a, q = _core(core)
    if _order(n, 2) != a or n % q:
        raise ValueError("n must have the core's exact 2-exponent and contain its odd prime")
    b = _order(n, q)
    v = n // (2 ** a * q ** b)
    sigma_v = _sigma(v, max_work)
    sigma_q = (q ** (b + 1) - 1) // (q - 1)
    following = q * sigma_q * sigma_v - n
    predicted = None
    if b >= 2:
        predicted = sigma_v % q != 0 and (b % 2 == 1 or valuation(sigma_v, 2) > a)
    return CoreStep(n, core, a, q, b, v, sigma_v, following,
                    _order(following, 2), _order(following, q), predicted)


def _checked_step(n, core, max_source, max_work):
    if n > max_source:
        raise ComputationLimit("Independent-verification source limit reached.")
    step = core_step(n, core, max_work=max_work)
    independent = _divisor_pair_sum(n)
    restored = _order(independent, 2) == step.a and _order(independent, step.q) == 1
    if (step.successor != independent or
            step.sigma_cofactor != _divisor_pair_sum(step.cofactor) + step.cofactor or
            step.next_a != _order(independent, 2) or step.next_b != _order(independent, step.q) or
            (step.b >= 2 and step.bridge_predicted != restored)):
        raise ArithmeticError(f"Independent core-regeneration check failed at n={n}")
    return step


def _record(step):
    return {"n": str(step.n), "core": str(step.core), "a": step.a, "q": str(step.q),
            "b": step.b, "cofactor": str(step.cofactor), "sigmaCofactor": str(step.sigma_cofactor),
            "next": str(step.successor), "nextA": step.next_a, "nextB": step.next_b,
            "bridgePredicted": step.bridge_predicted,
            "restoredExactCore": step.next_a == step.a and step.next_b == 1,
            "retainedDriver": step.next_a == step.a and step.next_b >= 1}


def trace_driver(seed, core, *, max_steps=64, max_source=MAX_SOURCE, max_work=DEFAULT_MAX_WORK):
    """Follow actual aliquot steps THROUGH q-power spikes, not an invalid T step.

    Stop at driver exit, repetition, or an explicit unresolved computation limit.
    Driver exit is not termination or a claim that the sequence cannot return.
    """
    positive_integer(seed, "seed")
    positive_integer(max_steps, "max_steps")
    positive_integer(max_source, "max_source")
    positive_integer(max_work, "max_work")
    a, q = _core(core)
    if _order(seed, 2) != a or seed % q:
        raise ValueError("seed must lie in the selected driver class")
    if max_steps > MAX_STEPS or max_source > MAX_SOURCE:
        raise ValueError(f"limits must not exceed {MAX_STEPS} steps and {MAX_SOURCE} per source")
    terms, spikes, seen = [seed], [], {seed}
    status = "step_limit"
    for _ in range(max_steps):
        n = terms[-1]
        if n > max_source:
            status = "term_limit"
            break
        try:
            step = _checked_step(n, core, max_source, max_work)
        except ComputationLimit:
            status = "factorization_limit"
            break
        if step.b >= 2:
            spikes.append({"index": len(terms) - 1, **_record(step)})
        terms.append(step.successor)
        if step.next_a != a or step.next_b == 0:
            status = "driver_exit"
            break
        if step.successor in seen:
            status = "cycle"
            break
        seen.add(step.successor)
    return {"seed": str(seed), "core": str(core), "status": status,
            "terms": [str(n) for n in terms], "spikes": spikes,
            "stepsComputed": len(terms) - 1,
            "limits": {"steps": max_steps, "sourceTerm": str(max_source),
                       "factorizationWorkPerCall": max_work}}


def base_four_step(u, *, max_work=DEFAULT_MAX_WORK):
    """The square-sensitive mod-4 phase of the odd cofactor map T."""
    positive_integer(u, "u")
    if u % 2 == 0:
        raise ValueError("u must be odd")
    sigma = _sigma(u, max_work)
    square = isqrt(u) ** 2 == u
    following = 2 * sigma - u
    predicted = u % 4 if square else (-u) % 4
    if sigma % 2 != int(square) or following % 4 != predicted:
        raise ArithmeticError("Square-sensitive base-4 phase check failed.")
    return {"u": str(u), "sigma": str(sigma), "square": square,
            "residueMod4": u % 4, "next": str(following), "nextMod4": predicted}


def ambiguity_class(k, ell):
    """Reduced CRT class matching p=5 locally but forcing the unitary-5 guard.

    The constructor is bounded; the written theorem has no precision bound.
    No prime existence is inferred from this function or from a finite search.
    """
    positive_integer(k, "k")
    positive_integer(ell, "ell")
    if k > MAX_PRECISION or ell > MAX_PRECISION or ell < 2:
        raise ValueError(f"require 1<=k<={MAX_PRECISION} and 2<=ell<={MAX_PRECISION}")
    local = 4 ** k * 3 ** ell
    residue = 5 + local * ((-2 * pow(local, -1, 25)) % 25)
    modulus = 25 * local
    if gcd(residue, modulus) != 1:
        raise ArithmeticError("CRT class is not reduced.")
    return {"fourAdicDigits": k, "threeAdicDigits": ell, "localModulus": str(local),
            "primeResidue": str(residue), "primeModulus": str(modulus)}


def core_return_report():
    """Named finite examples for the written proofs and failed closure attempt."""
    basepoint = [5]
    for _ in range(2):
        u = basepoint[-1]
        sigma = _sigma(u, DEFAULT_MAX_WORK)
        if sigma != _divisor_pair_sum(u) + u:
            raise ArithmeticError("Independent local-basepoint check failed.")
        basepoint.append(2 * sigma - u)
    local_examples = []
    for k, p in [(1, 653), (2, 6053), (3, 27653), (4, 27653), (5, 27653)]:
        entry = ambiguity_class(k, 2)
        if (factorize(p) != [(p, 1)] or _divisor_pair_sum(p) != 1 or
                p % int(entry["primeModulus"]) != int(entry["primeResidue"])):
            raise ArithmeticError("Local-ambiguity prime witness failed.")
        certificate = certify_regeneration(p, 5)
        if (valuation(p + 1, 2), valuation(p + 1, 3)) != (1, 1):
            raise ArithmeticError("Input supply valuations do not match the basepoint.")
        local_examples.append({**entry, "prime": str(p),
                               "cofactorPath": certificate["cofactorPath"],
                               "aliquotPath": certificate["aliquotPath"]})
    phases = []
    for u in [5, 47, 49, 53, 55, 65, 89, 263, 265]:
        state = base_four_step(u)
        if int(state["sigma"]) != _divisor_pair_sum(u) + u:
            raise ArithmeticError("Independent base-4 check failed.")
        phases.append(state)
    bridges = [_record(_checked_step(n, core, MAX_SOURCE, DEFAULT_MAX_WORK))
               for core, n in [(6, 18), (6, 54), (6, 90), (6, 2646), (6, 12978),
                               (28, 196), (28, 1372), (28, 17836), (28, 19404), (28, 60564)]]
    corridor = []
    for p in [23, 41, 71, 121]:
        n = 84 * p
        following = aliquot_sum(n)
        if following != _divisor_pair_sum(n):
            raise ArithmeticError("Independent 84-core corridor check failed.")
        corridor.append({"n": str(n), "cofactor": str(p), "cofactorPrime": factorize(p) == [(p, 1)],
                         "valuationThreeOfCofactorPlusFour": valuation(p + 4, 3),
                         "next": str(following)})
    return {"schema": "aliquot-core-returns-v1",
            "scope": "finite checked examples; no infinite closure or novelty claim",
            "arithmetic": {"primary": "exact integer factorization and multiplicativity",
                           "independent": "divisor-pair sums for every computed source and cofactor"},
            "baseFourPhases": phases,
            "localAmbiguityBasepoint": {"prime": "5", "cofactorPath": [str(u) for u in basepoint],
                                        "scope": "fails the two-step return, not all later returns"},
            "localAmbiguityExamples": local_examples, "bridgeExamples": bridges,
            "driverTraces": [trace_driver(seed, core) for core, seed in
                             [(6, 30), (6, 1578), (28, 1316), (28, 9772)]],
            "primeCore84Corridor": corridor,
            "conclusion": "Prime-power spikes can regenerate a core, but the restoration guard is not closed."}
