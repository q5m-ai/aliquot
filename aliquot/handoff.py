"""Bounded checks of supplier replacement and a supplier round-trip, not closure.

Prime parameters are proved by exhaustive trial division. Cofactor sums and
actual scaled edges are independently checked by divisor-pair enumeration.
The progression audit includes rejected parameters; a computation limit raises
an error rather than turning an unresolved case into a mathematical failure.
"""

from fractions import Fraction
from math import gcd, isqrt

from . import ComputationLimit, DEFAULT_MAX_WORK, factorize, positive_integer
from .exponent_vectors import sigma, value

DEFAULT_BOUND = 1_000_000
MAX_BOUND = 1_000_000
MAX_PARAMETER = 20_000_000
MAX_SOURCE = 10_000_000_000
MAX_CRT_BITS = 128


def _order(n, p):
    # Internal callers supply positive n and a proved prime p.
    e = 0
    while n % p == 0:
        n //= p
        e += 1
    return e


def geometric_supply7(base, exponent):
    """v7(1+base+...+base**exponent), without expanding a huge exponent.

    This geometric identity holds for composite bases too. Interpreting it as
    a prime-power sigma column additionally requires a proved prime base.
    """
    positive_integer(base, "base")
    if base < 2 or base > MAX_SOURCE:
        raise ValueError("Geometric base must lie in 2..10000000000")
    if type(exponent) is not int or exponent < 0:
        raise ValueError("Exponent must be a nonnegative integer")
    if base % 7 == 0:
        return 0
    if base % 7 == 1:
        return _order(exponent+1, 7)
    order = next(d for d in range(2, 7) if pow(base, d, 7) == 1)
    if (exponent+1) % order:
        return 0
    return _order(base**order-1, 7) + _order((exponent+1)//order, 7)


def control_progression(core, targets, *, phase=6, max_work=DEFAULT_MAX_WORK):
    """Construct a reduced prime-parameter class with chosen output valuations.

    targets consists of (prime, exponent, nonzero unit residue) triples.
    For prime p not dividing 2*core, T(core*p)=L*p+B. This construction only
    controls ONE image. Infinitely many prime entries use Dirichlet's theorem,
    not a finite search or an assumption about simultaneous prime forms.
    """
    positive_integer(core, "core")
    positive_integer(max_work, "max_work")
    if core > MAX_BOUND or gcd(core, 14) != 1 or core == 1:
        raise ValueError("Core must be odd, greater than one, coprime to7, and at most1000000")
    if type(phase) is not int or not 1 <= phase <= 6:
        raise ValueError("Phase must be a nonzero residue modulo7")
    if not isinstance(targets, (list, tuple)) or not 1 <= len(targets) <= 8:
        raise ValueError("Expected one to eight target triples")
    _, total = _checked(core, max_work)
    if total % 7:
        raise ValueError("Core must already supply7")
    linear, constant = 2*total-core, 2*total
    residue, modulus = phase*pow(core, -1, 7) % 7, 7
    congruences = [[str(residue), str(modulus)]]
    seen, encoded_targets = set(), []
    for target in targets:
        if not isinstance(target, (list, tuple)) or len(target) != 3:
            raise ValueError("Expected (prime, exponent, unit residue)")
        prime, exponent, unit = target
        positive_integer(prime, "target prime")
        if prime > MAX_BOUND or prime in seen:
            raise ValueError("Target primes must be distinct and at most1000000")
        if factorize(prime, max_work=max_work) != [(prime, 1)]:
            raise ValueError("Target base is not prime")
        if type(exponent) is not int or not 1 <= exponent <= 8:
            raise ValueError("Controlled exponent must lie in 1..8")
        if type(unit) is not int or not 1 <= unit < prime:
            raise ValueError("Unit residue must lie in 1..prime-1")
        if (linear*constant) % prime == 0:
            raise ValueError("Target prime must not divide L*B")
        seen.add(prime)
        local_modulus = prime**(exponent+1)
        if (modulus*local_modulus).bit_length() > MAX_CRT_BITS:
            raise ValueError("CRT modulus exceeds128 bits")
        local_residue = ((prime**exponent*unit-constant)*pow(linear, -1, local_modulus)) % local_modulus
        # Distinct prime-power moduli, none divisible by7, are pairwise coprime.
        adjustment = (local_residue-residue)*pow(modulus, -1, local_modulus) % local_modulus
        residue += modulus*adjustment
        modulus *= local_modulus
        congruences.append([str(local_residue), str(local_modulus)])
        encoded_targets.append({"prime": str(prime), "exponent": exponent, "unitResidue": unit})
    if gcd(residue, modulus) != 1:
        raise ArithmeticError("Constructed progression is not reduced")
    return {"core": str(core), "L": str(linear), "B": str(constant), "phase": phase,
            "targets": encoded_targets, "residue": str(residue), "modulus": str(modulus),
            "parameterCongruences": congruences,
            "excludedPrimeDivisorsOf": str(2*core)}


def _pair_sigma(n):
    positive_integer(n)
    if n > MAX_SOURCE:
        raise ComputationLimit("Independent handoff source cap exceeded")
    total = 0
    for d in range(1, isqrt(n)+1):
        if n % d == 0:
            total += d
            if d*d != n:
                total += n//d
    return total


def _checked(n, max_work):
    positive_integer(n)
    if n > MAX_SOURCE:
        raise ComputationLimit("Handoff factorization source cap exceeded")
    factors = tuple(factorize(n, max_work=max_work))
    total = sigma(factors)
    if value(factors) != n or total != _pair_sigma(n):
        raise ArithmeticError("Independent handoff arithmetic disagrees")
    if sum(geometric_supply7(p, e) for p, e in factors) != _order(total, 7):
        raise ArithmeticError("7-supply columns disagree with the divisor sum")
    return factors, total


def _unitary13_phase(n):
    return n % 2 == 1 and n % 7 == 6 and _order(n, 13) == 1


def _guard(factors):
    # Composite cofactors are allowed. Prime parameters are used only to
    # construct infinitely many entries, NOT to define the returned guard.
    n = value(factors)
    if not _unitary13_phase(n) or n % 41 == 0:
        return False
    middle = 2*sigma(factors)-n
    return _order(middle, 13) == 2 and _order(middle, 41) == 1


def _roundtrip_guard(factors, max_work):
    n = value(factors)
    if not _unitary13_phase(n) or n % 181 == 0:
        return False
    middle = 2*sigma(factors)-n
    if _order(middle, 13) != 2 or _order(middle, 181) != 1:
        return False
    _, rest_sigma = _checked(middle//(13**2*181), max_work)
    return rest_sigma % 13 != 0


def _two_steps(u, max_work):
    positive_integer(u, "cofactor")
    positive_integer(max_work, "max_work")
    if not _unitary13_phase(u):
        raise ValueError("Expected an odd cofactor congruent to6 modulo7 with13 exactly dividing it")
    if 28*u > MAX_SOURCE:
        raise ComputationLimit("Scaled handoff source cap exceeded")
    fu, su = _checked(u, max_work)
    v = 2*su-u
    if 28*v > MAX_SOURCE:
        raise ComputationLimit("Scaled handoff second-source cap exceeded")
    fv, sv = _checked(v, max_work)
    w = 2*sv-v
    fw, sw = _checked(w, max_work)
    if gcd(u*v, 28) != 1 or v % 7 != 1:
        raise ArithmeticError("Clean-core source phases failed")
    if _pair_sigma(28*u)-28*u != 28*v or _pair_sigma(28*v)-28*v != 28*w:
        raise ArithmeticError("Actual aliquot edges disagree with the reduced map")
    return [(u,fu,su),(v,fv,sv),(w,fw,sw)]


def _encoded_state(n, factors, total):
    return {"n": str(n), "factors": [[str(p), e] for p, e in factors],
            "sigma": str(total), "residue7": n % 7,
            "suppliers7": [{"prime": str(p), "exponent": e, "supply": geometric_supply7(p, e)}
                           for p, e in factors if geometric_supply7(p, e)],
            "supply7": _order(total, 7)}


def handoff_block(p, *, max_work=DEFAULT_MAX_WORK):
    """Two actual 28-core steps, with or without the proposed replacement guard.

    The parameter must be a proved prime congruent to1 modulo7. The two source
    cofactors are always coprime to28; the endpoint may leave the clean core.
    No reduced-map continuation past that endpoint is assumed.
    """
    positive_integer(p, "prime parameter")
    positive_integer(max_work, "max_work")
    if p > MAX_PARAMETER or p % 7 != 1:
        raise ValueError("Parameter must be at most20000000 and congruent to1 modulo7")
    if factorize(p, max_work=max_work) != [(p, 1)]:
        raise ValueError("Parameter must be prime, not a probable prime or composite")
    (u,fu,su),(v,fv,sv),(w,fw,sw) = _two_steps(13*p, max_work)
    if v != 15*p+28:
        raise ArithmeticError("Prime-cofactor reduction failed")
    entry = _guard(fu)
    first_return = w % 7 == 6 and gcd(w, 28) == 1
    if first_return != (sv % 7 == 0) or v % 7 != 1:
        raise ArithmeticError("Residue-phase return criterion failed")
    back_supply = None
    if entry:
        if not first_return or 90077*w <= 126645*u:
            raise ArithmeticError("Parity-aware replacement lemma failed")
        rest = tuple((q, e) for q, e in fv if q not in (13, 41))
        r, sr = value(rest), sigma(rest)
        if r*13**2*41 != v or gcd(r, 13*41) != 1 or sr != _pair_sigma(r):
            raise ArithmeticError("Complete-block decomposition failed")
        input_supply, returned_exponent = _order(sr, 13), dict(fw).get(13, 0)
        if (input_supply == 1) != (returned_exponent == 1):
            raise ArithmeticError("Exact back-supply criterion failed")
        back_supply = {"R": str(r), "sigmaR": str(sr), "supply13": input_supply,
                       "returnedExponent13": returned_exponent,
                       "conditionMet": input_supply == 1}
    ratio = Fraction(w, u)
    return {"primeParameter": str(p), "entryGuard": entry,
            "cofactors": [_encoded_state(n, f, s) for n, f, s in [(u,fu,su),(v,fv,sv),(w,fw,sw)]],
            "aliquotPath": [str(28*x) for x in (u,v,w)],
            "middleExponent13": dict(fv).get(13, 0), "middleExponent41": dict(fv).get(41, 0),
            "twoStepFirstReturn": first_return,
            "gain": {"numerator": str(ratio.numerator), "denominator": str(ratio.denominator)},
            "returnedSupply7": sw % 7 == 0, "returnedGuard": _guard(fw),
            "backSupply13": back_supply}


def supplier_roundtrip(u, *, max_work=DEFAULT_MAX_WORK):
    """Check the 13 ->181 ->13 supplier return, retaining failed entry/renewal.

    The initial and returned class permits composite cofactors. It is distinct
    from the full guard, which additionally controls the NEXT middle split.
    """
    (u,fu,su),(v,fv,sv),(w,fw,sw) = _two_steps(u, max_work)
    pattern = _order(v,13) == 2 and _order(v,181) == 1
    back_supply = None
    if pattern:
        rest = tuple((q,e) for q,e in fv if q not in (13,181))
        r, sr = value(rest), sigma(rest)
        if r*13**2*181 != v or gcd(r,13*181) != 1 or sr != _pair_sigma(r):
            raise ArithmeticError("Round-trip complete-block decomposition failed")
        if (_order(w,13) == 1) != (sr % 13 != 0):
            raise ArithmeticError("Round-trip back-supply equivalence failed")
        back_supply = {"R": str(r), "sigmaR": str(sr), "supply13": _order(sr,13),
                       "returnedExponent13": _order(w,13), "conditionMet": sr % 13 != 0}
    entry = _roundtrip_guard(fu, max_work)
    returned_phase = _unitary13_phase(w)
    if entry and (not returned_phase or sw % 7 or 30589*w <= 41565*u):
        raise ArithmeticError("Supplier round-trip lemma failed")
    ratio = Fraction(w,u)
    return {"entryGuard": entry, "middlePattern": pattern,
            "cofactors": [_encoded_state(n,f,s) for n,f,s in [(u,fu,su),(v,fv,sv),(w,fw,sw)]],
            "aliquotPath": [str(28*x) for x in (u,v,w)],
            "twoStepFirstReturnToUnitary13Phase": returned_phase,
            "gain": {"numerator": str(ratio.numerator), "denominator": str(ratio.denominator)},
            "returnedSupply7": sw % 7 == 0, "returnedGuard": _roundtrip_guard(fw, max_work),
            "backSupply13": back_supply}


def handoff_report(*, bound=DEFAULT_BOUND, max_work=DEFAULT_MAX_WORK):
    positive_integer(bound, "prime-parameter bound")
    positive_integer(max_work, "max_work")
    if bound > MAX_BOUND:
        raise ValueError("Progression audit bound cannot exceed1000000")
    progression = control_progression(13, [(13,2,9),(41,1,15)], max_work=max_work)
    if (progression["residue"], progression["modulus"]) != ("77141", "25852099"):
        raise ArithmeticError("Concrete CRT class mismatch")
    candidates, admitted, cache = [], [], {}
    # These are ALL p=1 mod7 with 13^2*41 dividing15p+28, not a sample of successes.
    for p in range(28638, bound+1, 48503):
        fp = factorize(p, max_work=max_work)
        if fp != [(p, 1)]:
            candidates.append({"p": str(p), "status": "composite_parameter",
                               "factors": [[str(q), e] for q, e in fp]})
            continue
        middle = 15*p+28
        exponents = [_order(middle,13), _order(middle,41)]
        if exponents != [2,1]:
            candidates.append({"p": str(p), "status": "excluded_higher_power",
                               "middleExponents": exponents})
            continue
        block = handoff_block(p, max_work=max_work)
        cache[p] = block
        admitted.append(block)
        candidates.append({"p": str(p), "status": "admitted"})
    for p in (77141, 1429, 14337023):
        if p not in cache:
            cache[p] = handoff_block(p, max_work=max_work)
    saturation = control_progression(13, [(13,2,9),(41,1,15),(30757,1,1),(3361,1,1)],
                                     max_work=max_work)
    if ((int(saturation["residue"])-int(progression["residue"])) % int(progression["modulus"]) or
            (30757+1) % 13**3 or (3361+1) % 41**2 or
            _pair_sigma(30757) != 30758 or _pair_sigma(3361) != 3362):
        raise ArithmeticError("Explicit saturation refinement failed")
    return {"schema": "aliquot-parity-handoff-v1",
            "scope": "Finite supplier replacement and round-trip with failed guard renewal; no infinite-orbit or novelty claim.",
            "limits": {"primeParameterBound": str(bound), "maxParameter": str(MAX_PARAMETER),
                       "independentSourceCap": str(MAX_SOURCE), "factorizationWorkPerCall": max_work,
                       "crtBits": MAX_CRT_BITS, "crtMaxTargets": 8, "crtMaxExponent": 8},
            "progression": progression,
            "audit": {"necessaryCongruence": {"residue": "28638", "modulus": "48503"},
                      "candidates": candidates, "admitted": admitted,
                      "counts": {"candidateParameters": len(candidates), "admitted": len(admitted),
                                 "returnedSupply7": sum(row["returnedSupply7"] for row in admitted),
                                 "returnedGuard": sum(row["returnedGuard"] for row in admitted)}},
            "named": {"replacementAndFailedRenewal": cache[77141],
                      "noGuaranteedReplacement": cache[1429],
                      "replacementExponentEven": cache[14337023]},
            "congruenceObstruction": {
                "exampleRefinement": saturation,
                "auxiliarySuppliers": [{"prime": "30757", "sigma": "30758", "suppliedPrime": "13", "supply": 3},
                                       {"prime": "3361", "sigma": "3362", "suppliedPrime": "41", "supply": 2}],
                "forcedReturnedExponents": [["13", 2], ["41", 1]],
                "primeParameterWitness": None,
                "scope": "A reduced CRT refinement of the base class. Dirichlet supplies prime members; the residue itself is NOT asserted prime and no additional prime-parameter orbit is computed."},
            "supplierRoundTrip": {
                "positive": supplier_roundtrip(13*197807, max_work=max_work),
                "failedRepeat": supplier_roundtrip(3560843, max_work=max_work),
                "backSupplyCounterexample": supplier_roundtrip(13*10475711, max_work=max_work)},
            "verification": {"primes": "Exhaustive bounded trial division; no probable-prime acceptance.",
                             "sums": "All reported cofactor sums and both scaled aliquot edges checked by independent divisor pairs.",
                             "cohorts": "Named controls are separate from the bounded progression cohort; no random or blind holdout claim.",
                             "limits": "Any work/source-cap failure is unresolved and aborts the report without partial JSON.",
                             "quantifiers": "CRT/Dirichlet infinitude concerns prescribed valuations and H41, not H181's extra tail-sigma guard. Neither full guard is proved iterable."}}
